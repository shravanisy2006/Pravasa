"""
Pravasa trip planner: picks real places from destinations.json and fits them into days.

How it works, in plain words:
1. Keep only places that match the traveller's interests.
2. Give each place a score: more matching interests = higher score,
   and a bonus if the trip month is one of its best months.
3. Build the trip day by day. Each day has about 9 usable hours.
   From where the traveller currently is, pick the place that gives the
   best score for the least travel time, as long as travel + visit fits
   in the hours left today. Repeat until the day is full.
4. Add up an estimated cost: entry fees, travel, stay and food.
"""

import math

# Starting cities the traveller can choose from (latitude, longitude)
START_CITIES = {
    "Bengaluru": (12.9716, 77.5946),
    "Mysuru": (12.2958, 76.6394),
    "Mangaluru": (12.9141, 74.8560),
    "Hubballi": (15.3647, 75.1240),
}

# Rough travel assumptions per transport mode (approximate, for planning only)
TRANSPORT = {
    "Own car / cab": {"speed_kmph": 45, "cost_per_km": 12},
    "Bus (KSRTC)": {"speed_kmph": 35, "cost_per_km": 2},
    "Bike": {"speed_kmph": 40, "cost_per_km": 4},
}

# Approximate cost per night and food per day for each stay style
STAY_STYLES = {
    "Budget": {"stay_per_night": 1200, "food_per_day": 600},
    "Comfort": {"stay_per_night": 3000, "food_per_day": 1000},
    "Premium": {"stay_per_night": 7000, "food_per_day": 1800},
}

HOURS_PER_DAY = 9      # sightseeing + travel hours available each day
ROAD_FACTOR = 1.3      # roads are longer than the straight-line distance
TRAVEL_PENALTY = 0.3   # how strongly long drives are avoided (higher = stay closer)


def straight_line_km(a, b):
    """Distance in km between two (lat, lon) points (haversine formula)."""
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(h))


def road_km(a, b):
    """Estimated road distance in km."""
    return straight_line_km(a, b) * ROAD_FACTOR


def score_place(place, interests, month):
    """Higher score = better match for this traveller."""
    matches = len(set(place["categories"]) & set(interests))
    score = matches * 10
    if month in place["best_months"]:
        score += 5
    return score


def plan_trip(destinations, days, interests, start_city, month,
              transport="Own car / cab", stay_style="Budget"):
    """Return a day-by-day plan and a cost estimate."""
    speed = TRANSPORT[transport]["speed_kmph"]
    cost_per_km = TRANSPORT[transport]["cost_per_km"]

    # Step 1 and 2: keep matching places and score them
    candidates = []
    for place in destinations:
        s = score_place(place, interests, month)
        if s >= 10:  # at least one interest matches
            candidates.append((place, s))

    current = START_CITIES[start_city]
    visited = set()
    covered = set()   # interests already included in the trip
    plan = []
    total_km = 0
    total_fees = 0

    # Step 3: fill each day
    for day in range(1, days + 1):
        hours_left = HOURS_PER_DAY
        stops = []

        while True:
            best = None
            best_value = -1
            for place, s in candidates:
                if place["id"] in visited:
                    continue
                km = road_km(current, (place["lat"], place["lon"]))
                travel_h = km / speed
                fits_today = travel_h + place["visit_hours"] <= hours_left
                # The first stop of a day may be a long drive (up to a full day)
                long_first_drive = not stops and travel_h <= HOURS_PER_DAY
                if not fits_today and not long_first_drive:
                    continue
                # Bonus for interests the trip hasn't covered yet,
                # so someone who picks "Beaches" actually reaches a beach
                new_interests = (set(place["categories"]) & set(interests)) - covered
                value = (s + 20 * len(new_interests)) / (1 + TRAVEL_PENALTY * travel_h)
                if value > best_value:
                    best, best_value = (place, km, travel_h, fits_today), value

            if best is None:
                break  # nothing else fits today

            place, km, travel_h, fits_today = best
            visited.add(place["id"])
            covered.update(set(place["categories"]) & set(interests))
            hours_left -= travel_h + place["visit_hours"]
            current = (place["lat"], place["lon"])
            total_km += km
            total_fees += place.get("entry_fee_inr_approx") or 0
            stops.append({
                "place": place,
                "travel_km": round(km),
                "travel_hours": round(travel_h, 1),
                "long_travel_day": not fits_today,
            })
            if not fits_today:
                break  # a long drive uses up the day

        plan.append({"day": day, "stops": stops})

    # Journey back to the starting city at the end of the trip
    return_km = road_km(current, START_CITIES[start_city])
    total_km += return_km

    # Step 4: cost estimate
    style = STAY_STYLES[stay_style]
    nights = max(days - 1, 0)
    costs = {
        "Travel": round(total_km * cost_per_km),
        "Stay": nights * style["stay_per_night"],
        "Food": days * style["food_per_day"],
        "Entry fees": total_fees,
    }
    costs["Total"] = sum(costs.values())

    return {
        "days": plan,
        "costs": costs,
        "total_km": round(total_km),
        "return_km": round(return_km),
    }