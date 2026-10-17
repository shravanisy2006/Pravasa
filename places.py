"""
Pravasa place helpers: photos, history, real road routes and map links.

- get_place_info(): a photo and a short history from Wikipedia (free, no key).
- get_road_route(): real road distance, drive time and the road shape
  from OSRM, a free open-source routing service (no key).
- google_maps_link() / google_maps_day_link(): links that open Google Maps
  directions. They're just web addresses, so they need no API key, and on a
  phone they open turn-by-turn navigation.

- get_gallery(): several photos of each place from Wikimedia Commons.
- get_traveller_notes(): what travellers say, from Wikivoyage (written by travellers).

Results are remembered (lru_cache), so the same lookup is never made twice.
Every function fails safely: if the internet or a service is down, it
returns None and the app shows the rest of the plan anyway.
"""

import re
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


# ---------- Photo gallery (Wikimedia Commons) ----------

def get_gallery(name, district, limit=6):
    """Up to `limit` photos of a place: [{'url', 'credit', 'page'}], or []."""
    try:
        return _fetch_gallery(name, district, limit)
    except Exception as e:
        print("Gallery error:", e)
        return []


@lru_cache(maxsize=512)
def _fetch_gallery(name, district, limit):
    params = {
        "action": "query", "format": "json",
        "generator": "search",
        "gsrnamespace": 6,                    # 6 = files (photos)
        "gsrsearch": f"{name} {district} Karnataka filetype:bitmap",
        "gsrlimit": limit * 2,                # ask for extra, some get filtered out
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": 900,                    # a 900-pixel-wide copy
    }
    r = requests.get("https://commons.wikimedia.org/w/api.php",
                     params=params, headers=HEADERS, timeout=8)
    r.raise_for_status()
    pages = sorted(r.json().get("query", {}).get("pages", {}).values(),
                   key=lambda pg: pg.get("index", 99))  # best matches first
    photos = []
    for pg in pages:
        title = pg.get("title", "").lower()
        if not title.endswith((".jpg", ".jpeg", ".png")):
            continue
        info = (pg.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        artist = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
        licence = meta.get("LicenseShortName", {}).get("value", "")
        if not info.get("thumburl"):
            continue
        photos.append({
            "url": info["thumburl"],
            "page": info.get("descriptionurl", ""),
            "credit": ", ".join(x for x in (artist[:60], licence) if x),
        })
        if len(photos) >= limit:
            break
    return photos


# ---------- What travellers say (Wikivoyage, the free traveller-written guide) ----------

def get_traveller_notes(name, district):
    """A short traveller-written summary {'title', 'text', 'url'} from Wikivoyage, or None."""
    try:
        return _fetch_traveller_notes(name, district)
    except Exception as e:
        print("Wikivoyage error:", e)
        return None


@lru_cache(maxsize=512)
def _fetch_traveller_notes(name, district):
    params = {
        "action": "query", "format": "json",
        "generator": "search", "gsrsearch": f"{name} {district}", "gsrlimit": 1,
        "prop": "extracts|info", "exintro": 1, "explaintext": 1, "exsentences": 3,
        "inprop": "url", "redirects": 1,
    }
    r = requests.get("https://en.wikivoyage.org/w/api.php",
                     params=params, headers=HEADERS, timeout=6)
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    if not pages:
        return None
    page = next(iter(pages.values()))
    text = (page.get("extract") or "").strip()
    if not text:
        return None
    return {"title": page.get("title"), "text": text, "url": page.get("fullurl")}


def google_reviews_link(name):
    """Opens the place on Google Maps, where its visitor reviews are."""
    from urllib.parse import quote
    return f"https://www.google.com/maps/search/?api=1&query={quote(name + ', Karnataka')}"


def get_hero_photo():
    """A large photo for the top of the page (Hampi's lead Wikipedia image)."""
    try:
        return _fetch_hero_photo()
    except Exception as e:
        print("Hero photo error:", e)
        return None


@lru_cache(maxsize=1)
def _fetch_hero_photo():
    params = {"action": "query", "format": "json", "titles": "Hampi",
              "prop": "pageimages", "piprop": "thumbnail", "pithumbsize": 1800,
              "redirects": 1}
    r = requests.get("https://en.wikipedia.org/w/api.php",
                     params=params, headers=HEADERS, timeout=6)
    r.raise_for_status()
    page = next(iter(r.json()["query"]["pages"].values()))
    return page.get("thumbnail", {}).get("source")


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