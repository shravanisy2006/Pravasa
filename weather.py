"""
Pravasa weather and season advice.

- trip_weather(): weather for each day's location from Open-Meteo
  (free, no key). If the trip is this month, it's the real forecast
  (assuming you start today). For a later month, it shows what that month
  was actually like at those places last year, so travellers know what
  to expect.
- season_notes(): simple, explainable rules about seasons in Karnataka
  (monsoon on the coast, summer heat up north, waterfalls after the rains).
"""

import calendar
import datetime
from functools import lru_cache

import requests

HEADERS = {"User-Agent": "Pravasa-Karnataka-Travel-Planner/1.0 (student project)"}


def weather_icon(code):
    """Turn a WMO weather code into an emoji and words."""
    if code is None:
        return "🌡️", ""
    if code == 0:
        return "☀️", "Clear"
    if code <= 3:
        return "⛅", "Partly cloudy"
    if code in (45, 48):
        return "🌫️", "Foggy"
    if 51 <= code <= 67:
        return "🌧️", "Rain"
    if 80 <= code <= 82:
        return "🌦️", "Showers"
    if code >= 95:
        return "⛈️", "Thunderstorms"
    return "🌥️", "Cloudy"


@lru_cache(maxsize=128)
def _fetch(url, params_items):
    r = requests.get(url, params=dict(params_items), headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else [data]  # one place -> dict, many -> list


def trip_weather(points, month):
    """
    points: tuple of (lat, lon), one per trip day.
    Returns a list with one entry per day, or None if weather can't be loaded.
    """
    if not points:
        return None
    today = datetime.date.today()
    lats = ",".join(str(round(p[0], 3)) for p in points)
    lons = ",".join(str(round(p[1], 3)) for p in points)
    try:
        if month == today.month:
            # Real forecast, day 1 = today
            params = (("latitude", lats), ("longitude", lons),
                      ("daily", "temperature_2m_max,temperature_2m_min,"
                                "precipitation_probability_max,weather_code"),
                      ("timezone", "Asia/Kolkata"),
                      ("forecast_days", min(len(points), 16)))
            places = _fetch("https://api.open-meteo.com/v1/forecast", params)
            out = []
            for i, place in enumerate(places):
                d = place["daily"]
                if i >= len(d["time"]):
                    out.append(None)
                    continue
                icon, words = weather_icon(d["weather_code"][i])
                out.append({
                    "kind": "forecast",
                    "date": d["time"][i],
                    "icon": icon, "words": words,
                    "max": round(d["temperature_2m_max"][i]),
                    "min": round(d["temperature_2m_min"][i]),
                    "rain_chance": d["precipitation_probability_max"][i],
                })
            return out

        # A later month: what that month was really like last time
        year = today.year if month < today.month else today.year - 1
        last_day = calendar.monthrange(year, month)[1]
        params = (("latitude", lats), ("longitude", lons),
                  ("start_date", f"{year}-{month:02d}-01"),
                  ("end_date", f"{year}-{month:02d}-{last_day}"),
                  ("daily", "temperature_2m_max,temperature_2m_min,precipitation_sum"),
                  ("timezone", "Asia/Kolkata"))
        places = _fetch("https://archive-api.open-meteo.com/v1/archive", params)
        out = []
        for place in places:
            d = place["daily"]
            highs = [x for x in d["temperature_2m_max"] if x is not None]
            lows = [x for x in d["temperature_2m_min"] if x is not None]
            rain = [x for x in d["precipitation_sum"] if x is not None]
            if not highs:
                out.append(None)
                continue
            rainy_days = sum(1 for x in rain if x >= 2.5)
            icon = "🌧️" if rainy_days >= 12 else ("🌦️" if rainy_days >= 5 else "☀️")
            out.append({
                "kind": "typical",
                "year": year,
                "icon": icon,
                "max": round(sum(highs) / len(highs)),
                "min": round(sum(lows) / len(lows)),
                "rainy_days": rainy_days,
                "days_in_month": last_day,
            })
        return out
    except Exception as e:
        print("Weather error:", e)
        return None


def weather_text(w):
    """One friendly line describing a weather entry (English or Kannada)."""
    from i18n import t, w as word
    if not w:
        return None
    if w["kind"] == "forecast":
        return t("wx_forecast", icon=w["icon"], words=word(w["words"]), lo=w["min"],
                 hi=w["max"], rain=w["rain_chance"] if w["rain_chance"] is not None else "–",
                 date=w["date"])
    return t("wx_typical", icon=w["icon"], lo=w["min"], hi=w["max"], rainy=w["rainy_days"],
             days=w["days_in_month"], year=w["year"])


def season_notes(place, month):
    """Season tips for one place, as (kind, message).
    kind is 'good' (great time), 'offseason' (not the best months for this place),
    'warn' or 'info' (advice for the whole area)."""
    from i18n import month_short, t
    notes = []
    region = place["region"]
    text = (place["name"] + " " + place["famous_for"]).lower()
    monsoon = month in (6, 7, 8, 9)

    if month in place["best_months"]:
        if "fall" in text and month in (7, 8, 9, 10):
            notes.append(("good", t("sn_falls")))
    else:
        months = ", ".join(month_short(m) for m in place["best_months"])
        notes.append(("offseason", t("sn_offseason", months=months)))

    if monsoon and region in ("Coastal Karnataka", "Malnad", "Kodagu"):
        notes.append(("warn", t("sn_monsoon")))
    if monsoon and "Beaches" in place["categories"]:
        notes.append(("warn", t("sn_sea")))
    if month in (3, 4, 5) and region == "Hampi & North Karnataka":
        notes.append(("warn", t("sn_heat")))
    if monsoon and "trek" in text:
        notes.append(("info", t("sn_trek")))
    return notes


# Emergency and helpline numbers (verify before the final submission)
HELPLINES = [
    ("🚨 All emergencies (police, fire, ambulance)", "112"),
    ("🚑 Ambulance", "108"),
    ("👮 Police", "100"),
    ("🔥 Fire", "101"),
    ("👩 Women's helpline", "1091"),
    ("🧒 Child helpline", "1098"),
    ("🧳 India Tourist Infoline (24x7, many languages)", "1800-11-1363 / 1363"),
]
