"""
Pravasa trip map: real road distances and a route map for the planned trip.

add_real_roads() takes the plan from planner.py and, for each day, asks the
routing service for the real road route (start -> stop 1 -> stop 2 ...).
Where it works, the estimated distances are replaced with real ones and the
travel cost is recalculated. Where it doesn't, the estimates stay.

build_trip_map() draws the whole trip on a Folium (Leaflet) map: one colour
per day, numbered stops, and the real road path when available.
"""

import copy

import folium

from places import get_road_route, google_maps_day_link
from planner import START_CITIES, TRANSPORT

DAY_COLOURS = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4",
               "#008080", "#9a6324", "#800000", "#000075", "#808000"]

CAR_SPEED = TRANSPORT["Own car / cab"]["speed_kmph"]


def add_real_roads(result, start_city, transport):
    """Return a copy of the plan with real road distances where available."""
    plan = copy.deepcopy(result)
    # Routing gives car times; buses and bikes are a bit slower
    slow_factor = CAR_SPEED / TRANSPORT[transport]["speed_kmph"]

    current = START_CITIES[start_city]
    all_real = True
    real_km = 0

    for day in plan["days"]:
        points = [current] + [(s["place"]["lat"], s["place"]["lon"]) for s in day["stops"]]
        day["start_point"] = current
        day["gmaps"] = google_maps_day_link(points)
        day["route"] = None

        if day["stops"]:
            route = get_road_route(tuple(points))
            if route:
                day["route"] = route
                real_km += route["km"]
                for stop, (km, hours) in zip(day["stops"], route["legs"]):
                    stop["travel_km"] = km
                    stop["travel_hours"] = round(hours * slow_factor, 1)
                    stop["real_road"] = True
            else:
                all_real = False
            current = points[-1]

    # Drive home at the end
    home = START_CITIES[start_city]
    back = get_road_route((current, home)) if current != home else {"km": 0}
    if back:
        plan["return_km"] = back["km"]
        real_km += back["km"]
    else:
        all_real = False

    plan["real_roads"] = all_real
    if all_real:
        # Recalculate the travel cost with real distances
        costs = plan["costs"]
        costs["Travel"] = round(real_km * TRANSPORT[transport]["cost_per_km"])
        costs["Total"] = sum(v for k, v in costs.items() if k != "Total")
        plan["total_km"] = real_km
    return plan


def build_trip_map(plan, start_city):
    """Draw the trip on a map and return the Folium map object."""
    home = START_CITIES[start_city]
    m = folium.Map(location=home, zoom_start=7, tiles="OpenStreetMap")
    bounds = [home]

    folium.Marker(
        home,
        tooltip=f"Start: {start_city}",
        icon=folium.Icon(color="black", icon="home"),
    ).add_to(m)

    for day in plan["days"]:
        if not day["stops"]:
            continue
        colour = DAY_COLOURS[(day["day"] - 1) % len(DAY_COLOURS)]
        points = [day["start_point"]] + [(s["place"]["lat"], s["place"]["lon"])
                                         for s in day["stops"]]
        bounds.extend(points)

        # Real road path if we have it, otherwise a dashed straight line
        if day.get("route"):
            folium.PolyLine(day["route"]["path"], color=colour, weight=4,
                            opacity=0.85, tooltip=f"Day {day['day']}").add_to(m)
        else:
            folium.PolyLine(points, color=colour, weight=3, dash_array="8",
                            tooltip=f"Day {day['day']} (approximate)").add_to(m)

        for i, stop in enumerate(day["stops"], start=1):
            p = stop["place"]
            folium.CircleMarker(
                (p["lat"], p["lon"]), radius=9, color="white", weight=2,
                fill=True, fill_color=colour, fill_opacity=1,
                tooltip=f"Day {day['day']} · {i}. {p['name']}",
                popup=folium.Popup(f"<b>{p['name']}</b><br>{p['name_kn']}<br>"
                                   f"{p['famous_for']}", max_width=250),
            ).add_to(m)

    if len(bounds) > 1:
        m.fit_bounds(bounds, padding=(30, 30))
    return m