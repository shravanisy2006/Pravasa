import calendar
import datetime
import json
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import streamlit as st

import ui
from ai import ai_available, stream_story, understand_audio, understand_request
from extras import hotel_search_link, hotels_near, nearby_places, transport_options
from places import (get_gallery, get_hero_photo, get_place_info, get_traveller_notes,
                    google_maps_link, google_reviews_link)
from planner import START_CITIES, STAY_STYLES, TRANSPORT, plan_trip
from report import build_pdf
from trip_map import add_real_roads, build_trip_map
from voice import plan_script, speak
from weather import HELPLINES, season_notes, trip_weather, weather_text

st.set_page_config(page_title="Pravasa · Karnataka trip planner",
                   page_icon="static/icon.png", layout="wide")
st.html(ui.STYLE)
hero_photo = get_hero_photo()  # light photo of Hampi behind the top section
if hero_photo:
    st.html(ui.hero_photo_style(hero_photo))

# Load the destination dataset
with open("destinations.json", encoding="utf-8") as f:
    destinations = json.load(f)

MONTHS = list(calendar.month_name)[1:]  # January ... December
INTERESTS = ["Nature", "Heritage", "Temples", "Beaches", "Wildlife", "Food"]

# Default values for the form, set once when the app first opens
defaults = {
    "start_city": "Bengaluru",
    "days": 3,
    "transport": "Own car / cab",
    "month_name": MONTHS[datetime.date.today().month - 1],
    "budget": 15000,
    "stay_style": "Budget",
    "interests": [],
    "language": "English",
    "request": "",
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)


def apply_settings(settings):
    """Fill the form with what the AI understood, then plan straight away."""
    for key in ("start_city", "days", "transport", "budget", "stay_style", "interests"):
        if key in settings:
            st.session_state[key] = settings[key]
    if "month" in settings:
        st.session_state["month_name"] = MONTHS[settings["month"] - 1]
    st.session_state["language"] = "ಕನ್ನಡ" if settings["language"] == "kn" else "English"
    st.session_state["plan_now"] = True
    st.rerun()


NO_KEY = "The AI isn't set up yet: add your GEMINI_API_KEY to the .env file."

# =====================================================================
# Hero: the brand on the left, "tell us your trip" on the right
# =====================================================================
with st.container(key="hero"):
    intro_col, ask_col = st.columns([1.1, 1], gap="large", vertical_alignment="center")
    with intro_col:
        st.html(ui.hero_intro(len(destinations)))

    with ask_col, st.container(key="ask"):
        st.html('<p class="pv-ask-title">Where shall we go?</p>'
                '<p class="pv-ask-sub">Speak or type your trip: days, budget, '
                'where you start and what you love.</p>')

        # Voice: ONE AI request both hears the words and understands the trip
        recording = st.audio_input("Speak in Kannada or English")
        if recording is not None:
            audio_bytes = recording.getvalue()
            audio_id = hash(audio_bytes)
            if st.session_state.get("last_audio") != audio_id:  # new recordings only
                st.session_state["last_audio"] = audio_id
                if not ai_available():
                    st.error(NO_KEY)
                else:
                    with st.spinner("Listening and planning..."):
                        settings = understand_audio(audio_bytes, recording.type or "audio/wav")
                    if settings and settings.get("interests"):
                        st.session_state["request"] = settings.get("transcript", "")
                        st.session_state["heard"] = settings.get("transcript", "")
                        apply_settings(settings)
                    elif settings and settings.get("transcript"):
                        st.session_state["request"] = settings["transcript"]
                        st.warning("Got it. Now add what you enjoy, like temples, "
                                   "beaches or nature.")
                    else:
                        st.error("That recording wasn't clear. Record again, a little "
                                 "closer to the mic.")

        request = st.text_area(
            "Or type it",
            key="request",
            height=110,
            placeholder="4 days from Bengaluru, love beaches and temples, ₹20,000\n"
                        "ಮೈಸೂರಿನಿಂದ 3 ದಿನದ ಪ್ರವಾಸ, ಕಾಡು ಮತ್ತು ಜಲಪಾತ ಇಷ್ಟ",
        )
        if st.session_state.get("heard"):
            st.caption(f"🎧 Heard: {st.session_state['heard']}")

        if st.button("Plan my trip", type="primary", key="plan_from_text", width="stretch"):
            if not ai_available():
                st.error(NO_KEY)
            elif not request.strip():
                st.warning("Type or speak a few words about your trip first.")
            else:
                st.session_state["heard"] = ""
                with st.spinner("Reading your request..."):
                    settings = understand_request(request)
                if settings and settings.get("interests"):
                    apply_settings(settings)
                elif settings:
                    st.warning("Add what you enjoy, like temples, beaches or nature.")
                else:
                    st.error("Pravasa couldn't read that request. Rephrase it, or "
                             "choose the details below.")

st.html(ui.flag_band())

# =====================================================================
# Or choose everything yourself
# =====================================================================
planned = "result" in st.session_state or st.session_state.get("plan_now")
with st.expander("Choose the details yourself", expanded=not planned):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Starting from", list(START_CITIES.keys()), key="start_city")
        st.slider("How many days?", 1, 10, key="days")
    with col2:
        st.selectbox("Travel month", MONTHS, key="month_name")
        st.number_input("Budget (₹)", min_value=1000, step=1000, key="budget")
    with col3:
        st.selectbox("How will you travel?", list(TRANSPORT.keys()), key="transport")
        st.selectbox("Stay style", list(STAY_STYLES.keys()), key="stay_style")
    st.pills("What do you enjoy?", INTERESTS, selection_mode="multi", key="interests")
    st.radio("Trip story language", ["English", "ಕನ್ನಡ"], key="language", horizontal=True)
    clicked = st.button("Plan with these details", type="primary", key="plan_from_form")

# =====================================================================
# Build the plan
# =====================================================================
if clicked or st.session_state.pop("plan_now", False):
    s = st.session_state
    if not s.interests:
        st.warning("Pick at least one thing you enjoy, so Pravasa knows what to plan.")
        st.stop()
    month = MONTHS.index(s.month_name) + 1
    s["result"] = plan_trip(destinations, s.days, s.interests, s.start_city,
                            month, s.transport, s.stay_style)
    s["result_info"] = {"days": s.days, "start_city": s.start_city,
                        "budget": s.budget, "language": s.language,
                        "transport": s.transport, "stay_style": s.stay_style,
                        "month": month, "interests": list(s.interests)}
    s["story"] = None  # write a fresh story for this new plan

# =====================================================================
# Show the plan
# =====================================================================
if "result" in st.session_state:
    info = st.session_state["result_info"]
    month = info["month"]
    with st.spinner("Finding real road routes..."):
        result = add_real_roads(st.session_state["result"], info["start_city"],
                                info["transport"])
    costs = result["costs"]

    day_word = "day" if info["days"] == 1 else "days"
    st.html(ui.section_title(
        f"Your {info['days']} {day_word} from {info['start_city']}",
        f"{', '.join(info.get('interests', []))} in {MONTHS[month - 1]}, "
        f"by {info['transport'].lower()}, {info['stay_style'].lower()} stays"))
    st.html(ui.stats_strip(costs["Total"], info["budget"], result["total_km"]))
    if costs["Total"] > info["budget"]:
        st.caption("To save money: fewer days, a budget stay style, or KSRTC buses.")
    if not result["real_roads"]:
        st.caption("Some distances are estimates because the road service didn't respond.")

    # The story and Listen button go here, but are filled in LAST,
    # so the map and day plans appear without waiting for the AI
    story_box = st.container()

    # Season tips for the whole trip (region-wide advice, shown once)
    trip_tips = []
    for d in result["days"]:
        for stp in d["stops"]:
            for kind, msg in season_notes(stp["place"], month):
                if not msg.startswith("Not the ideal") and kind != "good" and msg not in trip_tips:
                    trip_tips.append(msg)
    if trip_tips:
        with st.expander(f"⚠️ Travelling in {MONTHS[month - 1]}: what to know", expanded=True):
            for msg in trip_tips:
                st.markdown(f"- {msg}")

    # Fetch photos, hotels and weather for the whole trip at the same time
    with st.spinner("Loading photos, weather and places to stay..."):
        stops = [s["place"] for d in result["days"] for s in d["stops"]]
        nights = [d["stops"][-1]["place"] for d in result["days"][:-1] if d["stops"]]
        with ThreadPoolExecutor(max_workers=10) as pool:
            wiki_jobs = {p["id"]: pool.submit(get_place_info, p["name"], p["district"])
                         for p in stops}
            gallery_jobs = {p["id"]: pool.submit(get_gallery, p["name"], p["district"])
                            for p in stops}
            notes_jobs = {p["id"]: pool.submit(get_traveller_notes, p["name"], p["district"])
                          for p in stops}
            hotel_jobs = {p["id"]: pool.submit(hotels_near, p["lat"], p["lon"],
                                               info["stay_style"]) for p in nights}
            # Weather at the last stop of each day (where you'll be that evening)
            day_spots = tuple(
                (d["stops"][-1]["place"]["lat"], d["stops"][-1]["place"]["lon"])
                if d["stops"] else d["start_point"] for d in result["days"])
            weather_job = pool.submit(trip_weather, day_spots, month)
            wiki_info = {k: f.result() for k, f in wiki_jobs.items()}
            gallery_info = {k: f.result() for k, f in gallery_jobs.items()}
            notes_info = {k: f.result() for k, f in notes_jobs.items()}
            hotel_info = {k: f.result() for k, f in hotel_jobs.items()}
            weather = weather_job.result()

    # ---------- Route map ----------
    st.html(ui.section_title("Your route", "Each colour is one day. Tap a dot to see the place."))
    trip_map = build_trip_map(result, info["start_city"])
    st.iframe(trip_map.get_root().render(), height=480)

    # ---------- Day by day ----------
    st.html(ui.section_title("Day by day"))
    planned_ids = {s["place"]["id"] for d in result["days"] for s in d["stops"]}
    last_day = result["days"][-1]["day"]
    tabs = st.tabs([f"Day {d['day']}" for d in result["days"]])
    for i, (tab, day) in enumerate(zip(tabs, result["days"])):
        with tab:
            top_left, top_right = st.columns([2, 1], vertical_alignment="center")
            with top_left:
                day_weather = weather[i] if weather and i < len(weather) else None
                if day_weather:
                    st.markdown(weather_text(day_weather))
            with top_right:
                if day.get("gmaps") and day["stops"]:
                    st.link_button("Open this day in Google Maps", day["gmaps"],
                                   icon="🧭", width="stretch")
            if not day["stops"]:
                st.info("A free day. Rest, shop, or go back to a favourite spot.")
                continue

            for n, stop in enumerate(day["stops"], start=1):
                place = stop["place"]
                road = "" if stop.get("real_road") else " (estimate)"
                travel = (f"🚗 {stop['travel_km']} km{road}, about "
                          f"{stop['travel_hours']} h to get here")
                if stop["long_travel_day"]:
                    travel = "Long drive: " + travel[2:]
                fee = place.get("entry_fee_inr_approx")
                fee_text = ("Free" if fee == 0 else
                            (f"About ₹{fee}" if fee else place.get("fee_note", "Check locally")))
                wiki = wiki_info.get(place["id"])

                with st.container(key=f"place_{day['day']}_{place['id']}"):
                    photo_col, text_col = st.columns([1, 1.7], gap="medium")
                    with photo_col:
                        photos = list(gallery_info.get(place["id"]) or [])
                        if not photos and wiki and wiki.get("image"):
                            photos = [{"url": wiki["image"], "page": wiki["url"],
                                       "credit": "Wikipedia"}]
                        st.html(ui.gallery(f"g{day['day']}-{n}", photos, place["name"]))
                        st.link_button("Directions", google_maps_link(place["lat"], place["lon"]),
                                       icon="📍", width="stretch")
                    with text_col:
                        st.html(ui.place_header(n, place, travel, stop["long_travel_day"]))
                        if wiki and wiki.get("summary"):
                            st.html(ui.wiki_text(wiki["summary"], wiki["url"]))
                        for kind, msg in season_notes(place, month):
                            if kind == "good":
                                st.success(msg, icon="🌊")
                            elif msg.startswith("Not the ideal"):
                                st.warning(msg, icon="📅")
                    st.html(ui.facts(place, fee_text))

                    notes = notes_info.get(place["id"])
                    if notes:
                        st.html(ui.travellers_say(notes))
                    st.link_button("Read visitor reviews on Google Maps",
                                   google_reviews_link(place["name"]), icon="⭐")

                    more_left, more_right = st.columns(2)
                    with more_left, st.expander("Ways to get here"):
                        options = transport_options(stop["travel_km"], place, info["transport"])
                        st.dataframe(
                            pd.DataFrame([{
                                "": "⭐" if o["recommended"] else "",
                                "How": o["mode"], "Time": o["time"],
                                "Cost": o["cost"], "Tip": o["note"],
                            } for o in options]),
                            hide_index=True, width="stretch",
                        )
                    near = nearby_places(place, destinations, planned_ids)
                    with more_right, st.expander("Also nearby"):
                        if near:
                            for nb in near:
                                st.markdown(f"**{nb['place']['name']}**, {nb['km']} km: "
                                            f"{nb['place']['famous_for']}")
                        else:
                            st.caption("No other listed places within 40 km.")

            # Where to stay tonight (not needed on the last day: you head home)
            if day["day"] != last_day:
                night = day["stops"][-1]["place"]
                with st.container(key=f"night_{day['day']}"):
                    st.html(f'<p class="pv-h3" style="margin-top:0">Stay tonight near '
                            f'{ui.e(night["name"])}</p>')
                    stays = hotel_info.get(night["id"])
                    if stays:
                        st.html("".join(ui.hotel_line(h) for h in stays))
                        st.caption("Suggestions from OpenStreetMap. Check prices and reviews "
                                   "before booking.")
                    else:
                        st.caption("No listed stays found close by. Search the wider area:")
                    st.link_button("See more hotels nearby", hotel_search_link(night["name"]),
                                   icon="🏨")

    st.caption(f"Drive home to {info['start_city']} at the end: about "
               f"{result['return_km']} km, included in the cost.")

    # ---------- Costs, help and download ----------
    st.html(ui.section_title("Costs and essentials"))
    cost_col, help_col = st.columns([1.3, 1], gap="large")
    with cost_col:
        breakdown = {k: v for k, v in costs.items() if k != "Total"}
        st.bar_chart(pd.Series(breakdown, name="₹"), horizontal=True, height=220,
                     color="#C8102E")
        download_box = st.container()  # filled at the end, once the story is ready
    with help_col:
        st.html('<p class="pv-h3" style="margin-top:0">Emergency numbers</p>')
        st.html(ui.helplines(HELPLINES))

    # ---------- Fill in the story (streams in word by word) ----------
    night_hotels = {d["day"]: hotel_info.get(d["stops"][-1]["place"]["id"])
                    for d in result["days"] if d["stops"]}
    with story_box:
        speech_lang = "kn" if info["language"] == "ಕನ್ನಡ" else "en"
        with st.container(key="story"):
            if ai_available():
                st.html('<p class="pv-h3" style="margin-top:0">Your trip, in short</p>')
                if st.session_state.get("story") is None:
                    st.session_state["story"] = st.write_stream(
                        stream_story(result, info["start_city"], speech_lang)) or ""
                else:
                    st.markdown(st.session_state["story"])
                if not st.session_state["story"]:
                    st.caption("The trip story isn't available right now. Your full plan is below.")
            listen_label = "ಪ್ರವಾಸವನ್ನು ಕೇಳಿ" if speech_lang == "kn" else "Listen to your trip"
            if st.button(listen_label, icon="🔊", key="listen"):
                script = st.session_state.get("story") or plan_script(
                    result, info["start_city"], speech_lang)
                with st.spinner("Preparing audio..."):
                    audio = speak(script, speech_lang)
                if audio:
                    st.audio(audio, format="audio/mp3", autoplay=True)
                else:
                    st.error("Audio needs an internet connection. Check it and try again.")

    with download_box:
        story_now = st.session_state.get("story")
        st.download_button(
            "Download itinerary (PDF)",
            data=lambda: build_pdf(result, info, story_now, weather, night_hotels),
            file_name=f"pravasa-{info['days']}-day-trip.pdf",
            mime="application/pdf",
            type="primary",
            icon="📄",
        )

# =====================================================================
# Browse every place
# =====================================================================
with st.expander(f"Browse all {len(destinations)} places on a map"):
    df = pd.DataFrame(destinations)
    st.map(df, latitude="lat", longitude="lon", color="#A61E5B")
    st.dataframe(df[["name", "name_kn", "district", "categories", "famous_for"]],
                 hide_index=True, width="stretch")

st.html(ui.footer())