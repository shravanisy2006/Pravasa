"""Home: speak or type your trip, or start exploring by what you love."""

from concurrent.futures import ThreadPoolExecutor

import streamlit as st

import ui
from ai import ai_available, understand_audio, understand_request
from common import (EXPLORE, INTERESTS, PLAN, apply_ai_settings, build_plan_and_open, footer,
                    kannada_phrases, lang_switch, load_destinations, loading, photo_section)
import datetime

from festivals import festivals_in
from i18n import EXAMPLES, lang, month_name, t
from places import get_place_info

destinations = load_destinations()

# =====================================================================
# Hero: the brand on the left, "tell us your trip" on the right
# =====================================================================
with st.container(key="hero"):
    lang_switch()
    intro_col, ask_col = st.columns([1.1, 1], gap="large", vertical_alignment="center")
    with intro_col:
        st.html(ui.hero_intro(len(destinations)))

    with ask_col, st.container(key="ask"):
        st.html(f'<p class="pv-ask-title">{ui.e(t("ask_title"))}</p>'
                f'<p class="pv-ask-sub">{ui.e(t("ask_sub"))}</p>')

        # Voice: ONE AI request both hears the words and understands the trip
        recording = st.audio_input(t("speak_label"))
        if recording is not None:
            audio_bytes = recording.getvalue()
            audio_id = hash(audio_bytes)
            if st.session_state.get("last_audio") != audio_id:  # new recordings only
                st.session_state["last_audio"] = audio_id
                if not ai_available():
                    st.error(t("no_key"))
                else:
                    with loading(t("listening"), t("listening_sub")):
                        settings = understand_audio(audio_bytes, recording.type or "audio/wav")
                    if settings and (settings.get("interests") or settings.get("must_visit")):
                        st.session_state["heard"] = settings.get("transcript", "")
                        apply_ai_settings(settings)
                        build_plan_and_open()
                    elif settings and settings.get("transcript"):
                        st.session_state["request"] = settings["transcript"]
                        st.warning(t("add_interest_voice"))
                    else:
                        st.error(t("unclear"))

        request = st.text_area(
            t("type_label"),
            key="request",
            height=110,
            placeholder="4 days from Bengaluru, love beaches and temples, ₹20,000\n"
                        "ಮೈಸೂರಿನಿಂದ 3 ದಿನದ ಪ್ರವಾಸ, ಕಾಡು ಮತ್ತು ಜಲಪಾತ ಇಷ್ಟ",
        )

        if st.button(t("plan_btn"), type="primary", key="plan_from_text", width="stretch"):
            if not ai_available():
                st.error(t("no_key"))
            elif not request.strip():
                st.warning(t("type_first"))
            else:
                st.session_state["heard"] = ""
                with loading(t("reading"), t("planning_sub")):
                    settings = understand_request(request)
                if settings and (settings.get("interests") or settings.get("must_visit")):
                    apply_ai_settings(settings)
                    build_plan_and_open()
                elif settings:
                    st.warning(t("add_interest"))
                else:
                    st.error(t("cant_read"))
        # One-tap examples: ready-made settings, so they plan instantly (no AI wait)
        st.html(f'<p class="pv-try">{ui.e(t("try_label"))}</p>')
        with st.container(horizontal=True, wrap=True, gap="small", key="examples"):
            for n, (label, settings) in enumerate(EXAMPLES):
                if st.button(label[lang()], key=f"ex_{n}"):
                    apply_ai_settings({**settings, "language": lang()})
                    st.session_state["heard"] = ""
                    build_plan_and_open()
        st.page_link(PLAN, label=t("choose_self"), icon="🗓️")

st.html(ui.flag_band())

# =====================================================================
# Celebrate Karnataka: festivals that usually happen this month
# =====================================================================
this_month = datetime.date.today().month
st.html(ui.section_title(t("fest_home_title", month=month_name(this_month)), t("fest_home_sub")))
st.html(ui.festival_cards(festivals_in(this_month)))

# ...and a few Kannada words to celebrate the language
kannada_phrases("home_phrases", limit=5)

# =====================================================================
# Explore by what you love
# =====================================================================
st.html(ui.section_title(t("explore_title"), t("explore_sub")))

# One well-known place pictures each theme
THEME_PHOTO = {"Nature": ("Jog Falls", "Shivamogga"),
               "Heritage": ("Hampi - Vittala Temple", "Vijayanagara"),
               "Temples": ("Belur Chennakeshava Temple", "Hassan"),
               "Beaches": ("Gokarna - Om Beach", "Uttara Kannada"),
               "Wildlife": ("Bandipur National Park", "Chamarajanagar"),
               "Food": ("Udupi Sri Krishna Matha", "Udupi")}
with ThreadPoolExecutor(max_workers=6) as pool:
    theme_info = dict(zip(INTERESTS, pool.map(lambda th: get_place_info(*THEME_PHOTO[th]),
                                              INTERESTS)))

for row in (INTERESTS[:3], INTERESTS[3:]):
    cols = st.columns(3, gap="medium")
    for col, theme in zip(cols, row):
        count = sum(theme in d["categories"] for d in destinations)
        info = theme_info.get(theme) or {}
        with col, st.container(key=f"tile_{theme}"):
            st.html(ui.theme_tile(theme, count, info.get("image")))
            st.page_link(EXPLORE, label=t("see_places", n=count), icon="➡️",
                         query_params={"interest": theme})

# =====================================================================
# How Pravasa works, over a light photo of Mysuru Palace
# =====================================================================
with photo_section("how", "Mysuru Palace", "Mysuru"):
    st.html(ui.section_title(t("how_title")))
    st.html(ui.how_it_works())

footer()
