import calendar
import datetime
import json
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import streamlit as st

from ai import ai_available, stream_story, understand_audio, understand_request
from extras import hotel_search_link, hotels_near, nearby_places, transport_options
from places import get_place_info, get_road_route, google_maps_day_link, google_maps_link
from planner import START_CITIES, STAY_STYLES, TRANSPORT, plan_trip
from trip_map import add_real_roads, build_trip_map
from voice import plan_script, speak

st.set_page_config(page_title="Pravasa - Karnataka Travel Planner", page_icon="🧭")

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

st.title("Pravasa: Karnataka AI Travel Planner")
st.write("Plan your trip in English or ಕನ್ನಡ")
st.caption(f"{len(destinations)} verified destinations across Karnataka")

# ---------- Option 1: just describe the trip (type or speak) ----------
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


st.subheader("Tell me about your trip")

# Voice input: ONE AI request both hears the words and understands the trip
recording = st.audio_input("🎤 Speak in Kannada or English")
if recording is not None:
    audio_bytes = recording.getvalue()
    audio_id = hash(audio_bytes)
    if st.session_state.get("last_audio") != audio_id:  # only process new recordings
        st.session_state["last_audio"] = audio_id
        if not ai_available():
            st.error("The AI isn't set up yet: add your GEMINI_API_KEY to the .env file.")
        else:
            with st.spinner("Listening and planning..."):
                settings = understand_audio(audio_bytes, recording.type or "audio/wav")
            if settings and settings.get("interests"):
                st.session_state["request"] = settings.get("transcript", "")
                st.session_state["heard"] = settings.get("transcript", "")
                apply_settings(settings)
            elif settings and settings.get("transcript"):
                st.session_state["request"] = settings["transcript"]
                st.warning("I heard you, but please also say what you enjoy "
                           "(temples, beaches, nature...).")
            else:
                st.error("Sorry, I couldn't catch that. Please try recording again.")

request = st.text_area(
    "Or type in English or Kannada",
    key="request",
    placeholder="e.g. 4 days from Bengaluru, love beaches and temples, ₹20000 budget\n"
                "ಅಥವಾ: ಮೈಸೂರಿನಿಂದ 3 ದಿನದ ಪ್ರವಾಸ, ಕಾಡು ಮತ್ತು ಜಲಪಾತ ಇಷ್ಟ",
)
if st.session_state.get("heard"):
    st.info(f"🎧 I heard: {st.session_state['heard']}")

if st.button("✨ Plan it for me"):
    if not ai_available():
        st.error("The AI isn't set up yet: add your GEMINI_API_KEY to the .env file.")
    elif not request.strip():
        st.warning("Type or speak a few words about your trip first.")
    else:
        st.session_state["heard"] = ""
        with st.spinner("Understanding your request..."):
            settings = understand_request(request)
        if settings and settings.get("interests"):
            apply_settings(settings)
        elif settings:
            st.warning("Please also say what you enjoy (temples, beaches, nature...).")
        else:
            st.error("Sorry, I couldn't understand that. Try again or use the form below.")

# ---------- Option 2: fill the form ----------
st.subheader("Or choose the details")
col1, col2 = st.columns(2)
with col1:
    st.selectbox("Starting from", list(START_CITIES.keys()), key="start_city")
    st.slider("How many days?", 1, 10, key="days")
    st.selectbox("How will you travel?", list(TRANSPORT.keys()), key="transport")
with col2:
    st.selectbox("Travel month", MONTHS, key="month_name")
    st.number_input("Budget (₹)", min_value=1000, step=1000, key="budget")
    st.selectbox("Stay style", list(STAY_STYLES.keys()), key="stay_style")
st.multiselect("What do you enjoy?", INTERESTS, key="interests")
st.radio("Trip description language", ["English", "ಕನ್ನಡ"], key="language", horizontal=True)

clicked = st.button("Plan my trip", type="primary")

# ---------- Build the plan ----------
if clicked or st.session_state.pop("plan_now", False):
    s = st.session_state
    if not s.interests:
        st.warning("Pick at least one interest so I know what to plan for.")
        st.stop()
    month = MONTHS.index(s.month_name) + 1
    s["result"] = plan_trip(destinations, s.days, s.interests, s.start_city,
                            month, s.transport, s.stay_style)
    s["result_info"] = {"days": s.days, "start_city": s.start_city,
                        "budget": s.budget, "language": s.language,
                        "transport": s.transport, "stay_style": s.stay_style}
    s["story"] = None  # write a fresh story for this new plan

# ---------- Show the plan ----------
if "result" in st.session_state:
    info = st.session_state["result_info"]
    with st.spinner("Finding real road routes..."):
        result = add_real_roads(st.session_state["result"], info["start_city"],
                                info["transport"])
    costs = result["costs"]

    st.subheader(f"Your {info['days']}-day trip from {info['start_city']}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated cost", f"₹{costs['Total']:,}")
    m2.metric("Your budget", f"₹{info['budget']:,}")
    m3.metric("Total distance", f"{result['total_km']:,} km")
    if not result["real_roads"]:
        st.caption("Some distances are estimates (the road routing service couldn't be reached).")

    if costs["Total"] > info["budget"]:
        st.warning(
            f"This plan is about ₹{costs['Total'] - info['budget']:,} over budget. "
            "Try fewer days, a cheaper stay style, or travelling by bus."
        )
    else:
        st.success(f"Within budget, with about ₹{info['budget'] - costs['Total']:,} to spare.")

    # The story and Listen button go here, but are filled in LAST,
    # so the map and day plans appear without waiting for the AI
    story_box = st.container()

    # Fetch photos/history and hotels for every stop at the same time
    with st.spinner("Loading photos and places to stay..."):
        stops = [s["place"] for d in result["days"] for s in d["stops"]]
        nights = [d["stops"][-1]["place"] for d in result["days"][:-1] if d["stops"]]
        with ThreadPoolExecutor(max_workers=10) as pool:
            wiki_jobs = {p["id"]: pool.submit(get_place_info, p["name"], p["district"])
                         for p in stops}
            hotel_jobs = {p["id"]: pool.submit(hotels_near, p["lat"], p["lon"],
                                               info["stay_style"]) for p in nights}
            wiki_info = {k: f.result() for k, f in wiki_jobs.items()}
            hotel_info = {k: f.result() for k, f in hotel_jobs.items()}

    # Route map for the whole trip
    st.subheader("🗺️ Your route")
    trip_map = build_trip_map(result, info["start_city"])
    st.iframe(trip_map.get_root().render(), height=460)
    st.caption("Each colour is one day. Click a dot for details.")

    # One tab per day
    planned_ids = {s["place"]["id"] for d in result["days"] for s in d["stops"]}
    last_day = result["days"][-1]["day"]
    tabs = st.tabs([f"Day {d['day']}" for d in result["days"]])
    for tab, day in zip(tabs, result["days"]):
        with tab:
            if not day["stops"]:
                st.info("A free day to relax, shop or revisit a favourite spot.")
                continue
            if day.get("gmaps"):
                st.link_button("🧭 Open today's full route in Google Maps", day["gmaps"])

            for stop in day["stops"]:
                place = stop["place"]
                st.markdown(f"### {place['name']}")
                st.caption(f"{place['name_kn']} · {place['district']}")

                road = "by road" if stop.get("real_road") else "estimated"
                travel = f"{stop['travel_km']} km ({road}) · about {stop['travel_hours']} hours to get here"
                if stop["long_travel_day"]:
                    st.warning(f"Long travel day: {travel}.")
                else:
                    st.write(f"🚗 {travel}")

                wiki = wiki_info.get(place["id"])
                photo_col, text_col = st.columns([1, 2])
                with photo_col:
                    if wiki and wiki.get("image"):
                        st.image(wiki["image"], width="stretch")
                    st.link_button("📍 Directions", google_maps_link(place["lat"], place["lon"]),
                                   width="stretch")
                with text_col:
                    st.markdown(f"**Famous for:** {place['famous_for']}")
                    if wiki and wiki.get("summary"):
                        st.write(wiki["summary"])
                        st.caption(f"Source: [Wikipedia]({wiki['url']})")

                fee = place.get("entry_fee_inr_approx")
                fee_text = "Free" if fee == 0 else (f"about ₹{fee}" if fee else place.get("fee_note", "Check locally"))
                st.write(
                    f"⏱️ Spend about {place['visit_hours']} hours · "
                    f"🎟️ Entry: {fee_text} · 🕘 {place['timings']}"
                )
                st.write(f"🍛 Try: {place['local_food']}")

                with st.expander("🚌 Ways to get here"):
                    options = transport_options(stop["travel_km"], place, info["transport"])
                    st.dataframe(
                        pd.DataFrame([{
                            "": "⭐ Best for you" if o["recommended"] else "",
                            "How": o["mode"], "Time": o["time"],
                            "Approx. cost": o["cost"], "Tip": o["note"],
                        } for o in options]),
                        hide_index=True, width="stretch",
                    )

                near = nearby_places(place, destinations, planned_ids)
                if near:
                    with st.expander("📌 Also nearby"):
                        for n in near:
                            st.markdown(f"**{n['place']['name']}** ({n['km']} km): "
                                        f"{n['place']['famous_for']}")
                st.divider()

            # Where to stay tonight (not needed on the last day: you head home)
            if day["day"] != last_day:
                night = day["stops"][-1]["place"]
                st.markdown(f"#### 🏨 Where to stay tonight, near {night['name']}")
                stays = hotel_info.get(night["id"])
                if stays:
                    for h in stays:
                        extra = f" · ⭐ {h['stars']}" if h["stars"] else ""
                        line = f"**{h['name']}** · {h['type']} · {h['km']} km away{extra}"
                        if h["phone"]:
                            line += f" · 📞 {h['phone']}"
                        st.markdown(line + f" · [Map]({h['maps']})")
                    st.caption("Suggestions from OpenStreetMap. Check prices, reviews "
                               "and availability before booking.")
                else:
                    st.write("I couldn't load nearby stays right now.")
                st.link_button("🔎 See more hotels nearby", hotel_search_link(night["name"]))

    st.caption(
        f"Return journey to {info['start_city']}: about {result['return_km']} km "
        "(included in the travel cost)."
    )

    st.subheader("Cost breakdown (approximate)")
    breakdown = {k: v for k, v in costs.items() if k != "Total"}
    st.bar_chart(pd.Series(breakdown, name="₹"))

    with story_box:
        speech_lang = "kn" if info["language"] == "ಕನ್ನಡ" else "en"
        if ai_available():
            with st.container(border=True):
                st.markdown("#### ✨ Your trip, in short")
                if st.session_state.get("story") is None:
                    # Appears word by word while the AI writes it
                    st.session_state["story"] = st.write_stream(
                        stream_story(result, info["start_city"], speech_lang)) or ""
                else:
                    st.markdown(st.session_state["story"])
                if not st.session_state["story"]:
                    st.caption("The trip story couldn't be written right now.")

        listen_label = "🔊 ಪ್ರವಾಸವನ್ನು ಕೇಳಿ (Listen)" if speech_lang == "kn" else "🔊 Listen to your trip"
        if st.button(listen_label):
            script = st.session_state.get("story") or plan_script(
                result, info["start_city"], speech_lang)
            with st.spinner("Preparing audio..."):
                audio = speak(script, speech_lang)
            if audio:
                st.audio(audio, format="audio/mp3", autoplay=True)
            else:
                st.error("Couldn't create the audio right now. Check your internet connection.")

# ---------- All destinations ----------
with st.expander("See all destinations on a map"):
    df = pd.DataFrame(destinations)
    st.map(df, latitude="lat", longitude="lon")
    st.dataframe(df[["name", "name_kn", "district", "categories", "famous_for"]])