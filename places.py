"""
Pravasa place helpers: photos, history, real road routes and map links.

- get_place_info(): a photo and a short history from Wikipedia (free, no key).
- get_road_route(): real road distance, drive time and the road shape
  from OSRM, a free open-source routing service (no key).
- google_maps_link() / google_maps_day_link(): links that open Google Maps
  directions. They're just web addresses, so they need no API key, and on a
  phone they open turn-by-turn navigation.

Results are remembered (lru_cache), so the same lookup is never made twice.
Every function fails safely: if the internet or a service is down, it
returns None and the app shows the rest of the plan anyway.
"""

from functools import lru_cache

import requests

# Wikipedia asks apps to identify themselves
HEADERS = {"User-Agent": "Pravasa-Karnataka-Travel-Planner/1.0 (student project)"}


def get_place_info(name, district):
    """Return {'summary', 'image', 'url'} from Wikipedia, or None."""
    try:
        return _fetch_place_info(name, district)
    except Exception as e:
        print("Wikipedia error:", e)
        return None  # not remembered, so it's tried again next time


@lru_cache(maxsize=512)
def _fetch_place_info(name, district):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{name} {district} Karnataka",
        "gsrlimit": 1,
        "prop": "extracts|pageimages|info",
        "exintro": 1,          # only the introduction
        "explaintext": 1,      # plain text, no HTML
        "exsentences": 4,      # keep it short
        "piprop": "thumbnail",
        "pithumbsize": 600,    # image width in pixels
        "inprop": "url",
        "redirects": 1,
    }
    r = requests.get("https://en.wikipedia.org/w/api.php",
                     params=params, headers=HEADERS, timeout=6)
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    if not pages:
        return None
    page = next(iter(pages.values()))
    return {
        "title": page.get("title"),
        "summary": page.get("extract", ""),
        "image": page.get("thumbnail", {}).get("source"),
        "url": page.get("fullurl"),
    }


def get_road_route(points):
    """
    points: tuple of (lat, lon) in visiting order.
    Returns {'km', 'hours', 'legs': [(km, hours), ...], 'path': [(lat, lon), ...]}
    or None if the routing service can't be reached.
    """
    if len(points) < 2:
        return None
    try:
        return _fetch_road_route(points)
    except Exception as e:
        print("Routing error:", e)
        return None  # not remembered, so it's tried again next time


@lru_cache(maxsize=512)
def _fetch_road_route(points):
    # OSRM wants "lon,lat;lon,lat;..."
    coords = ";".join(f"{lon},{lat}" for lat, lon in points)
    url = f"https://router.project-osrm.org/route/v1/driving/{coords}"
    r = requests.get(url, params={"overview": "full", "geometries": "geojson"},
                     headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != "Ok":
        return None
    route = data["routes"][0]
    return {
        "km": round(route["distance"] / 1000),
        "hours": round(route["duration"] / 3600, 1),
        "legs": [(round(leg["distance"] / 1000), round(leg["duration"] / 3600, 1))
                 for leg in route["legs"]],
        # GeoJSON gives [lon, lat]; maps want (lat, lon)
        "path": [(lat, lon) for lon, lat in route["geometry"]["coordinates"]],
    }


def google_maps_link(lat, lon):
    """Directions to one place from wherever the user is right now."""
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=driving"


def google_maps_day_link(points):
    """Directions for a whole day: start, stops in order, last stop."""
    if len(points) < 2:
        return None
    origin = f"{points[0][0]},{points[0][1]}"
    destination = f"{points[-1][0]},{points[-1][1]}"
    middle = "|".join(f"{lat},{lon}" for lat, lon in points[1:-1])
    link = (f"https://www.google.com/maps/dir/?api=1&origin={origin}"
            f"&destination={destination}&travelmode=driving")
    if middle:
        link += f"&waypoints={middle}"
    return link