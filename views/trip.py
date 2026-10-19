"""My trip: the planned trip with map, day-by-day plan, costs, story and PDF."""

from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import streamlit as st

import ui
from ai import ai_available, stream_story
from common import HOME, PLAN, footer, load_destinations, page_banner, photo_section
from extras import hotel_search_link, hotels_near, nearby_places, transport_options
from i18n import CITY_FROM_KN, is_kn, month_name, pf, t, time_text, w
from places import (get_gallery, get_place_info, get_place_info_kn, get_traveller_notes,
                    google_maps_link, google_reviews_link)
from report import build_pdf
from trip_map import add_real_roads, build_trip_map
from voice import plan_script, speak
from weather import season_notes, trip_weather, weather_text

destinations = load_destinations()

# ---------- No trip yet ----------
if "result" not in st.session_state:
    page_banner(t("nav_trip"), t("trip_empty_sub"))
    with photo_section("empty", "Gokarna - Om Beach", "Uttara Kannada"), \
            st.container(key="empty"):
        st.html(f'<p class="pv-h3" style="margin-top:0">{t("no_trip")}</p>'
                f'<p>{ui.e(t("no_trip_body"))}</p>')
        c1, c2, _ = st.columns([1, 1, 2])
        with c1:
            st.page_link(HOME, label=t("speak_or_type"), icon="🎤")
        with c2:
            st.page_link(PLAN, label=t("choose_details"), icon="🗓️")
    footer()
    st.stop()

# ---------- The trip ----------
info = st.session_state["result_info"]
month = info["month"]
with st.spinner(t("finding_routes")):
    result = add_real_roads(st.session_state["result"], info["start_city"], info["transport"])
costs = result["costs"]

day_word = "day" if info["days"] == 1 else "days"
page_banner(
    t("trip_title", n=info["days"], days=day_word, city=info["start_city"],
      city_from=CITY_FROM_KN.get(info["start_city"], info["start_city"])),
    t("trip_sub", interests=", ".join(w(i) for i in info["interests"]),
      month=month_name(month), transport=w(info["transport"]).lower() if not is_kn()
      else w(info["transport"]), stay=w(info["stay_style"]).lower() if not is_kn()
      else w(info["stay_style"])))

if st.session_state.get("heard"):
    st.caption(f"🎧 {t('you_said')}: {st.session_state['heard']}")
st.html(ui.stats_strip(costs["Total"], info["budget"], result["total_km"]))
if costs["Total"] > info["budget"]:
    st.caption(t("save_money"))
if not result["real_roads"]:
    st.caption(t("est_roads"))
st.page_link(PLAN, label=t("change_details"), icon="✏️")

# The story and Listen button go here, but are filled in LAST,
# so the map and day plans appear without waiting for the AI
story_box = st.container()

# Season tips for the whole trip (area-wide advice, shown once)
trip_tips = []
for d in result["days"]:
    for stp in d["stops"]:
        for kind, msg in season_notes(stp["place"], month):
            if kind in ("warn", "info") and msg not in trip_tips:
                trip_tips.append(msg)
if trip_tips:
    with st.expander(f"⚠️ {t('season_exp', month=month_name(month))}", expanded=True):
        for msg in trip_tips:
            st.markdown(f"- {msg}")

# Fetch photos, notes, hotels and weather for the whole trip at the same time
with st.spinner(t("loading")):
    stops = [s["place"] for d in result["days"] for s in d["stops"]]
    nights = [d["stops"][-1]["place"] for d in result["days"][:-1] if d["stops"]]
    with ThreadPoolExecutor(max_workers=10) as pool:
        wiki_jobs = {p["id"]: pool.submit(get_place_info, p["name"], p["district"]) for p in stops}
        gallery_jobs = {p["id"]: pool.submit(get_gallery, p["name"], p["district"]) for p in stops}
        notes_jobs = {p["id"]: pool.submit(get_traveller_notes, p["name"], p["district"])
                      for p in stops}
        hotel_jobs = {p["id"]: pool.submit(hotels_near, p["lat"], p["lon"], info["stay_style"])
                      for p in nights}
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
        # In Kannada mode, also look for each place's Kannada Wikipedia page
        kn_wiki = {}
        if is_kn():
            kn_jobs = {k: pool.submit(get_place_info_kn, (v or {}).get("title"))
                       for k, v in wiki_info.items()}
            kn_wiki = {k: f.result() for k, f in kn_jobs.items()}

# ---------- Route map ----------
st.html(ui.section_title(t("route_title"), t("route_sub")))
trip_map = build_trip_map(result, info["start_city"])
st.iframe(trip_map.get_root().render(), height=480)

# ---------- Day by day ----------
st.html(ui.section_title(t("day_by_day")))
planned_ids = {s["place"]["id"] for d in result["days"] for s in d["stops"]}
last_day = result["days"][-1]["day"]
tabs = st.tabs([t("day_n", n=d["day"]) for d in result["days"]])
for i, (tab, day) in enumerate(zip(tabs, result["days"])):
    with tab:
        top_left, top_right = st.columns([2, 1], vertical_alignment="center")
        with top_left:
            day_weather = weather[i] if weather and i < len(weather) else None
            if day_weather:
                st.markdown(weather_text(day_weather))
        with top_right:
            if day.get("gmaps") and day["stops"]:
                st.link_button(t("open_day_maps"), day["gmaps"], icon="🧭", width="stretch")
        if not day["stops"]:
            st.info(t("free_day"))
            continue

        for n, stop in enumerate(day["stops"], start=1):
            place = stop["place"]
            est = "" if stop.get("real_road") else t("estimate_tag")
            travel = t("travel_line", km=stop["travel_km"], est=est, h=stop["travel_hours"])
            travel = f"{t('long_drive')}: {travel}" if stop["long_travel_day"] else f"🚗 {travel}"
            fee = place.get("entry_fee_inr_approx")
            fee_text = (t("free") if fee == 0 else
                        (t("about_fee", x=fee) if fee else place.get("fee_note", t("check_locally"))))
            wiki = wiki_info.get(place["id"])

            with st.container(key=f"place_{day['day']}_{place['id']}"):
                photo_col, text_col = st.columns([1, 1.7], gap="medium")
                with photo_col:
                    photos = list(gallery_info.get(place["id"]) or [])
                    if not photos and wiki and wiki.get("image"):
                        photos = [{"url": wiki["image"], "page": wiki["url"], "credit": "Wikipedia"}]
                    st.html(ui.gallery(f"g{day['day']}-{n}", photos,
                                       place["name_kn"] if is_kn() else place["name"]))
                    st.link_button(t("directions"), google_maps_link(place["lat"], place["lon"]),
                                   icon="📍", width="stretch")
                with text_col:
                    st.html(ui.place_header(n, place, travel, stop["long_travel_day"]))
                    wiki_kn = kn_wiki.get(place["id"])
                    if wiki_kn:
                        st.html(ui.wiki_text(wiki_kn["summary"], wiki_kn["url"]))
                    elif wiki and wiki.get("summary"):
                        st.html(ui.wiki_text(wiki["summary"], wiki["url"], in_english=is_kn()))
                    for kind, msg in season_notes(place, month):
                        if kind == "good":
                            st.success(msg, icon="🌊")
                        elif kind == "offseason":
                            st.warning(msg, icon="📅")
                st.html(ui.facts(place, fee_text))

                notes = notes_info.get(place["id"])
                if notes:
                    st.html(ui.travellers_say(notes))
                st.link_button(t("reviews_btn"), google_reviews_link(place["name"]), icon="⭐")

                more_left, more_right = st.columns(2)
                with more_left, st.expander(t("ways_here")):
                    options = transport_options(stop["travel_km"], place, info["transport"])
                    st.dataframe(pd.DataFrame([{
                        "": "⭐" if o["recommended"] else "",
                        t("col_how"): w(o["mode"]), t("col_time"): time_text(o["time"]),
                        t("col_cost"): time_text(o["cost"]), t("col_tip"): w(o["note"]),
                    } for o in options]), hide_index=True, width="stretch")
                near = nearby_places(place, destinations, planned_ids)
                with more_right, st.expander(t("also_nearby")):
                    if near:
                        for nb in near:
                            name = nb["place"]["name_kn"] if is_kn() else nb["place"]["name"]
                            st.markdown(f"**{name}**, {nb['km']} {'ಕಿ.ಮೀ' if is_kn() else 'km'}: "
                                        f"{pf(nb['place'], 'famous_for')}")
                    else:
                        st.caption(t("none_nearby"))

        # Where to stay tonight (not needed on the last day: you head home)
        if day["day"] != last_day:
            night = day["stops"][-1]["place"]
            night_name = night["name_kn"] if is_kn() else night["name"]
            with st.container(key=f"night_{day['day']}"):
                st.html(f'<p class="pv-h3" style="margin-top:0">'
                        f'{ui.e(t("stay_tonight", place=night_name))}</p>')
                stays = hotel_info.get(night["id"])
                if stays:
                    st.html("".join(ui.hotel_line(h) for h in stays))
                    st.caption(t("stays_note"))
                else:
                    st.caption(t("no_stays"))
                st.link_button(t("more_hotels"), hotel_search_link(night["name"]), icon="🏨")

st.caption(t("drive_home", city=w(info["start_city"]), km=result["return_km"]))

# ---------- Costs and download, over a light photo of Udupi ----------
with photo_section("costs", "Udupi Sri Krishna Matha", "Udupi"):
    st.html(ui.section_title(t("costs_title")))
    cost_col, dl_col = st.columns([1.4, 1], gap="large", vertical_alignment="center")
    with cost_col:
        breakdown = {w(k): v for k, v in costs.items() if k != "Total"}
        st.bar_chart(pd.Series(breakdown, name="₹"), horizontal=True, height=220, color="#C8102E")
    with dl_col:
        st.html(f'<p class="pv-h3" style="margin-top:0">{t("take_it")}</p>'
                f'<p class="pv-sub">{ui.e(t("take_it_sub"))}</p>')
        download_box = st.container()  # filled at the end, once the story is ready

# ---------- Fill in the story (streams in word by word) ----------
night_hotels = {d["day"]: hotel_info.get(d["stops"][-1]["place"]["id"])
                for d in result["days"] if d["stops"]}
with story_box:
    speech_lang = "kn" if info["language"] == "ಕನ್ನಡ" else "en"
    with st.container(key="story"):
        if ai_available():
            st.html(f'<p class="pv-h3" style="margin-top:0">{t("story_title")}</p>')
            if st.session_state.get("story") is None:
                st.session_state["story"] = st.write_stream(
                    stream_story(result, info["start_city"], speech_lang)) or ""
            else:
                st.markdown(st.session_state["story"])
            if not st.session_state["story"]:
                st.caption(t("story_unavailable"))
        if st.button(t("listen"), icon="🔊", key="listen"):
            script = st.session_state.get("story") or plan_script(
                result, info["start_city"], speech_lang)
            with st.spinner(t("preparing_audio")):
                audio = speak(script, speech_lang)
            if audio:
                st.audio(audio, format="audio/mp3", autoplay=True)
            else:
                st.error(t("audio_error"))

with download_box:
    story_now = st.session_state.get("story")
    st.download_button(
        t("download_pdf"),
        data=lambda: build_pdf(result, info, story_now, weather, night_hotels),
        file_name=f"pravasa-{info['days']}-day-trip.pdf",
        mime="application/pdf", type="primary", icon="📄",
    )

footer()
