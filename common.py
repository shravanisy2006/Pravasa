"""
Pravasa shared pieces used by every page: the places data, the traveller's
choices (kept while moving between pages), building a plan, the ಕನ್ನಡ / English
switch, and the light place photos behind sections.
"""

import calendar
import datetime
import json
from contextlib import contextmanager

import streamlit as st

import ui
from i18n import is_kn, t
from places import get_place_info
from planner import plan_trip

MONTHS = list(calendar.month_name)[1:]  # January ... December
INTERESTS = ["Nature", "Heritage", "Temples", "Beaches", "Wildlife", "Food"]

# Page files, so any page can send the traveller to another one
HOME, PLAN, TRIP, EXPLORE, HELP = ("views/home.py", "views/plan.py", "views/trip.py",
                                   "views/explore.py", "views/help.py")


@st.cache_data
def load_destinations():
    with open("destinations.json", encoding="utf-8") as f:
        return json.load(f)


def default_prefs():
    return {
        "start_city": "Bengaluru",
        "days": 3,
        "transport": "Own car / cab",
        "month_name": MONTHS[datetime.date.today().month - 1],
        "budget": 15000,
        "stay_style": "Budget",
        "interests": [],
        "language": "English",
    }


def prefs():
    """The traveller's choices. Stored outside any widget so they survive page changes."""
    if "prefs" not in st.session_state:
        st.session_state["prefs"] = default_prefs()
    return st.session_state["prefs"]


def apply_ai_settings(settings):
    """Copy what the AI understood into the traveller's choices."""
    p = prefs()
    for key in ("start_city", "days", "transport", "budget", "stay_style", "interests"):
        if key in settings:
            p[key] = settings[key]
    if "month" in settings:
        p["month_name"] = MONTHS[settings["month"] - 1]
    p["language"] = "ಕನ್ನಡ" if settings["language"] == "kn" else "English"
    for key in p:  # so the Plan page shows these new choices
        st.session_state.pop(f"f_{key}", None)


def build_plan_and_open():
    """Plan the trip from the saved choices, then open the My trip page."""
    p = prefs()
    month = MONTHS.index(p["month_name"]) + 1
    st.session_state["result"] = plan_trip(load_destinations(), p["days"], p["interests"],
                                           p["start_city"], month, p["transport"],
                                           p["stay_style"])
    st.session_state["result_info"] = {**p, "month": month, "interests": list(p["interests"])}
    st.session_state["story"] = None  # a fresh story for the new plan
    st.switch_page(TRIP)


# ---------- ಕನ್ನಡ / English switch ----------

def _switch_language():
    choice = st.session_state.get("lang_w")
    if choice is None:  # clicked the selected option again: keep the language
        return
    st.session_state["ui_lang"] = "kn" if choice == "ಕನ್ನಡ" else "en"
    # The trip story follows the site language
    prefs()["language"] = "ಕನ್ನಡ" if choice == "ಕನ್ನಡ" else "English"
    st.session_state.pop("f_language", None)


def lang_switch():
    """The ಕನ್ನಡ / English buttons at the top right of each page."""
    st.session_state["lang_w"] = "ಕನ್ನಡ" if is_kn() else "English"
    with st.container(key="langbar"):
        st.segmented_control(t("language"), ["ಕನ್ನಡ", "English"], key="lang_w",
                             on_change=_switch_language, label_visibility="collapsed")


# ---------- Page pieces ----------

def page_banner(title, sub=None):
    """The light photo band at the top of every page except Home."""
    with st.container(key="banner"):
        text_col, lang_col = st.columns([5, 1.3], vertical_alignment="top")
        with text_col:
            st.html(ui.banner(title, sub))
        with lang_col:
            lang_switch()
    st.html(ui.flag_band())


def photo_section(key, place_name, district):
    """A full-width section with a light photo of a Karnataka place behind it.
    Use it with `with photo_section(...):` and put the section's content inside."""
    info = get_place_info(place_name, district) or {}
    style = ui.section_photo_style(f"photo_{key}", info.get("image"))
    if style:
        st.html(style)
    return st.container(key=f"photo_{key}")


@contextmanager
def loading(title, sub=""):
    """Show a friendly loading card while something slow runs, then remove it."""
    box = st.empty()
    box.html(ui.loader(title, sub))
    try:
        yield
    finally:
        box.empty()


def footer():
    st.html(ui.footer())
