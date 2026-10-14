"""
Pravasa extras: how to get there, what's nearby, and where to stay.

- transport_options(): simple, explainable rules that compare cab, bus,
  train, auto and walking for one leg of the trip, with rough costs.
- nearby_places(): other places from our dataset close to a stop, so the
  traveller knows what else is around.
- hotels_near(): real hotels, guest houses and homestays near tonight's
  stop, from OpenStreetMap (free, no key). Prices aren't available for
  free, so these are labelled as suggestions to check before booking.
"""

from functools import lru_cache

import requests

from planner import straight_line_km

HEADERS = {"User-Agent": "Pravasa-Karnataka-Travel-Planner/1.0 (student project)"}

# Rough fares (₹ per km) and average speeds (km/h) used for comparisons
MODES = {
    "Cab / own car": {"fare": 12, "speed": 45, "icon": "🚗"},
    "KSRTC bus": {"fare": 1.6, "speed": 35, "icon": "🚌"},
    "Train": {"fare": 1.0, "speed": 50, "icon": "🚆"},
    "Auto-rickshaw": {"fare": 18, "speed": 25, "icon": "🛺"},
    "Walk": {"fare": 0, "speed": 4.5, "icon": "🚶"},
}

# Areas with no railway line at all
NO_RAIL_DISTRICTS = {"Kodagu"}


def _option(mode, km, note, recommended=False):
    m = MODES[mode]
    return {
        "mode": f"{m['icon']} {mode}",
        "time": f"~{max(km / m['speed'], 0.1):.1f} h",
        "cost": "Free" if m["fare"] == 0 else f"~₹{max(round(km * m['fare'], -1), 10):,.0f}",
        "note": note,
        "recommended": recommended,
    }


def transport_options(km, place, chosen_mode):
    """Compare ways of covering `km` to reach `place`. Returns a list of dicts."""
    options = []
    if km <= 2:
        options.append(_option("Walk", km, "Close enough to walk", recommended=True))
        options.append(_option("Auto-rickshaw", km, "If it's hot or you're tired"))
        return options

    if km <= 25:
        options.append(_option("Auto-rickshaw", km, "Easy for short hops within town",
                               recommended=chosen_mode == "Bus (KSRTC)"))
        options.append(_option("Cab / own car", km, "Most flexible",
                               recommended=chosen_mode != "Bus (KSRTC)"))
        options.append(_option("KSRTC bus", km, "Cheapest; local buses run often"))
        return options

    # Longer journeys
    has_rail = place["district"] not in NO_RAIL_DISTRICTS and km >= 80
    options.append(_option("Cab / own car", km, "Door to door, stop anywhere on the way",
                           recommended=chosen_mode == "Own car / cab"))
    options.append(_option("KSRTC bus", km, "Good value; book Airavat/Rajahamsa on ksrtc.in",
                           recommended=chosen_mode == "Bus (KSRTC)"))
    if has_rail:
        options.append(_option("Train", km,
                               f"Nearest station: {place['nearest_railway']}, then a short cab"))
    elif place["district"] in NO_RAIL_DISTRICTS:
        options.append({"mode": "🚆 Train", "time": "-", "cost": "-",
                        "note": "No railway in Kodagu; reach by road only",
                        "recommended": False})
    if chosen_mode == "Bike":
        options.insert(0, {"mode": "🏍️ Bike", "time": f"~{km / 40:.1f} h",
                           "cost": f"~₹{round(km * 4, -1):,.0f} (fuel)",
                           "note": "Your choice; ride in daylight on ghat roads",
                           "recommended": True})
    return options


def nearby_places(place, destinations, exclude_ids, radius_km=40, limit=3):
    """Other dataset places within `radius_km` of `place`, closest first."""
    here = (place["lat"], place["lon"])
    found = []
    for other in destinations:
        if other["id"] == place["id"] or other["id"] in exclude_ids:
            continue
        km = straight_line_km(here, (other["lat"], other["lon"]))
        if km <= radius_km:
            found.append((km, other))
    found.sort(key=lambda x: x[0])
    return [{"place": p, "km": round(km)} for km, p in found[:limit]]


# Which kinds of stay suit each stay style (OpenStreetMap "tourism" tags)
STYLE_TYPES = {
    "Budget": ["hostel", "guest_house", "hotel"],
    "Comfort": ["hotel", "guest_house", "resort"],
    "Premium": ["resort", "hotel"],
}
TYPE_LABELS = {"hotel": "Hotel", "guest_house": "Guest house / homestay",
               "hostel": "Hostel", "resort": "Resort", "motel": "Motel"}


@lru_cache(maxsize=256)
def _osm_stays(lat, lon, radius_m):
    query = f"""
    [out:json][timeout:10];
    nwr["tourism"~"^(hotel|guest_house|hostel|resort|motel)$"]["name"](around:{radius_m},{lat},{lon});
    out center 40;
    """
    r = requests.post("https://overpass-api.de/api/interpreter",
                      data={"data": query}, headers=HEADERS, timeout=12)
    r.raise_for_status()
    return r.json().get("elements", [])


def hotels_near(lat, lon, stay_style, limit=3):
    """Up to `limit` named stays near (lat, lon), best match for the style first.
    Returns a list (possibly empty), or None if OpenStreetMap can't be reached."""
    try:
        elements = _osm_stays(round(lat, 4), round(lon, 4), 5000)
    except Exception as e:
        print("OpenStreetMap error:", e)
        return None

    preferred = STYLE_TYPES[stay_style]
    stays = []
    for el in elements:
        tags = el.get("tags", {})
        kind = tags.get("tourism")
        h_lat = el.get("lat") or el.get("center", {}).get("lat")
        h_lon = el.get("lon") or el.get("center", {}).get("lon")
        if not h_lat or not h_lon:
            continue
        rank = preferred.index(kind) if kind in preferred else len(preferred)
        stays.append({
            "name": tags["name"],
            "type": TYPE_LABELS.get(kind, "Stay"),
            "km": round(straight_line_km((lat, lon), (h_lat, h_lon)), 1),
            "stars": tags.get("stars"),
            "phone": tags.get("phone") or tags.get("contact:phone"),
            "website": tags.get("website") or tags.get("contact:website"),
            "maps": f"https://www.google.com/maps/search/?api=1&query={h_lat},{h_lon}",
            "rank": rank,
        })
    # Best style match first, then closest
    stays.sort(key=lambda s: (s["rank"], s["km"]))
    return stays[:limit]


def hotel_search_link(place_name):
    """Fallback: a Google Maps search for hotels near the place."""
    q = requests.utils.quote(f"hotels near {place_name}, Karnataka")
    return f"https://www.google.com/maps/search/?api=1&query={q}"