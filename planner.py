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

Places the traveller names ("to Hampi") are "must-see": they are always
included and visited first. Sights inside the starting city itself are left
out of trips of 2+ days (you live there, or will see them anyway), unless
the traveller names them.
"""

import math

# Starting cities the traveller can choose from (latitude, longitude):
# every district headquarters in Karnataka plus a few big towns
START_CITIES = {
    "Bengaluru": (12.9716, 77.5946),
    "Mysuru": (12.2958, 76.6394),
    "Mangaluru": (12.9141, 74.8560),
    "Hubballi": (15.3647, 75.1240),
    "Bagalkote": (16.1691, 75.6615),
    "Ballari": (15.1394, 76.9214),
    "Belagavi": (15.8497, 74.4977),
    "Bidar": (17.9104, 77.5199),
    "Chamarajanagar": (11.9261, 76.9437),
    "Chikkaballapur": (13.4355, 77.7315),
    "Chikkamagaluru": (13.3161, 75.7720),
    "Chitradurga": (14.2251, 76.3980),
    "Davanagere": (14.4644, 75.9218),
    "Dharwad": (15.4589, 75.0078),
    "Gadag": (15.4298, 75.6340),
    "Hassan": (13.0072, 76.0962),
    "Haveri": (14.7951, 75.3991),
    "Hosapete": (15.2689, 76.3909),
    "Kalaburagi": (17.3297, 76.8343),
    "Karwar": (14.8136, 74.1295),
    "Kolar": (13.1367, 78.1292),
    "Koppal": (15.3547, 76.1548),
    "Madikeri": (12.4244, 75.7382),
    "Mandya": (12.5218, 76.8951),
    "Raichur": (16.2120, 77.3439),
    "Ramanagara": (12.7209, 77.2799),
    "Shivamogga": (13.9299, 75.5681),
    "Sirsi": (14.6195, 74.8354),
    "Tumakuru": (13.3379, 77.1173),
    "Udupi": (13.3409, 74.7421),
    "Vijayapura": (16.8302, 75.7100),
    "Yadgir": (16.7700, 77.1376),
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
HOME_KM = 8            # places this close to the starting city count as "in your own city"
MUST_BONUS = 200       # makes places the traveller asked for come first


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
              transport="Own car / cab", stay_style="Budget", must_visit=()):
    """Return a day-by-day plan and a cost estimate.
    must_visit: ids of places the traveller asked for by name."""
    speed = TRANSPORT[transport]["speed_kmph"]
    cost_per_km = TRANSPORT[transport]["cost_per_km"]

    must = set(must_visit)
    home = START_CITIES[start_city]

    # Step 1 and 2: keep matching places and score them
    candidates = []
    for place in destinations:
        s = score_place(place, interests, month)
        if place["id"] in must:
            candidates.append((place, max(s, 10)))
        elif s >= 10:  # at least one interest matches
            in_home_city = straight_line_km(home, (place["lat"], place["lon"])) < HOME_KM
            if not (in_home_city and days > 1):
                candidates.append((place, s))

    current = home
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
                # (a must-see place is always reachable this way, however far)
                is_must = place["id"] in must
                long_first_drive = not stops and (travel_h <= HOURS_PER_DAY or is_must)
                if not fits_today and not long_first_drive:
                    continue
                # Bonus for interests the trip hasn't covered yet,
                # so someone who picks "Beaches" actually reaches a beach
                new_interests = (set(place["categories"]) & set(interests)) - covered
                value = ((s + 20 * len(new_interests) + (MUST_BONUS if is_must else 0))
                         / (1 + TRAVEL_PENALTY * travel_h))
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
