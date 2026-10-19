"""Explore Karnataka: browse every place, filter by theme, region and season."""

from concurrent.futures import ThreadPoolExecutor

import streamlit as st

import ui
from common import (INTERESTS, MONTHS, PLAN, footer, load_destinations, page_banner,
                    photo_section, prefs)
from i18n import t, w
from places import get_place_info, google_maps_link, google_reviews_link

destinations = load_destinations()
page_banner(t("nav_explore"), t("x_banner_sub", n=len(destinations)))

# A theme picked on the home page arrives in the web address (?interest=Beaches)
start_theme = st.query_params.get("interest")
if start_theme in INTERESTS and "x_themes" not in st.session_state:
    st.session_state["x_themes"] = [start_theme]

regions = sorted({d["region"] for d in destinations})
# The filters sit over a light photo of the Kudremukh hills
with photo_section("filters", "Kudremukh National Park", "Chikkamagaluru"), \
        st.container(key="filters"):
    f1, f2 = st.columns([1.3, 1], gap="large")
    with f1:
        themes = st.pills(t("x_themes"), INTERESTS, selection_mode="multi", key="x_themes",
                          format_func=w)
        chosen_regions = st.multiselect(t("x_regions"), regions, key="x_regions",
                                        placeholder=t("x_all"), format_func=w)
    with f2:
        search = st.text_input(t("x_search"), key="x_search", placeholder=t("x_search_ph"))
        good_now = st.toggle(t("x_season"), key="x_season")

this_month = MONTHS.index(prefs()["month_name"]) + 1
q = (search or "").strip().lower()
matches = [
    d for d in destinations
    if (not themes or set(themes) & set(d["categories"]))
    and (not chosen_regions or d["region"] in chosen_regions)
    and (not q or q in d["name"].lower() or q in d["name_kn"] or q in d["district"].lower()
         or q in d["region"].lower() or q in w(d["district"]) or q in w(d["region"]))
    and (not good_now or this_month in d["best_months"])
]

found = t("x_found_one") if len(matches) == 1 else t("x_found", n=len(matches))
st.html(f'<p class="pv-sub" style="margin:1.5rem 0 .25rem">{ui.e(found)}</p>')
if not matches:
    st.info(t("x_none"))
    footer()
    st.stop()

# Show 12 at a time, with photos loaded together (back to 12 when filters change)
filters_now = (tuple(themes or []), tuple(chosen_regions), q, good_now)
if st.session_state.get("x_filters") != filters_now:
    st.session_state["x_filters"] = filters_now
    st.session_state["x_shown"] = 12
shown = st.session_state["x_shown"]
visible = matches[:shown]
with ThreadPoolExecutor(max_workers=12) as pool:
    photos = dict(zip([d["id"] for d in visible],
                      pool.map(lambda d: get_place_info(d["name"], d["district"]), visible)))

for start in range(0, len(visible), 3):
    cols = st.columns(3, gap="medium")
    for col, place in zip(cols, visible[start:start + 3]):
        info = photos.get(place["id"]) or {}
        with col, st.container(key=f"card_{place['id']}"):
            st.html(ui.place_card(place, info.get("image")))
            b1, b2 = st.columns(2)
            with b1:
                st.link_button(t("directions"), google_maps_link(place["lat"], place["lon"]),
                               icon="📍", width="stretch")
            with b2:
                st.link_button(t("reviews"), google_reviews_link(place["name"]),
                               icon="⭐", width="stretch")

if shown < len(matches):
    if st.button(t("x_more", n=len(matches) - shown), key="x_more"):
        st.session_state["x_shown"] = shown + 12
        st.rerun()

st.html(f'<p class="pv-sub" style="margin-top:2rem">{ui.e(t("x_closing"))}</p>')
st.page_link(PLAN, label=t("nav_plan"), icon="🗓️")
footer()
