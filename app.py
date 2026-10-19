"""
Pravasa: Karnataka AI travel planner.

This file only sets up the look and the menu bar at the top.
Each page lives in the views/ folder:
  home.py     - the front page: speak or type your trip
  plan.py     - choose every detail yourself
  trip.py     - your planned trip: map, day by day, costs, PDF
  explore.py  - browse all the places in Karnataka
  help.py     - emergency numbers, seasons, about Pravasa
"""

import streamlit as st

import ui
from i18n import t
from places import get_hero_photo

st.set_page_config(page_title="Pravasa · Karnataka trip planner",
                   page_icon="static/icon.png", layout="wide")
st.html(ui.STYLE)
hero_photo = get_hero_photo()  # light photo of Hampi behind the page headers
if hero_photo:
    st.html(ui.hero_photo_style(hero_photo))
st.logo("static/logo.png", size="large")

# Menu titles follow the chosen language (ಕನ್ನಡ / English)
pages = [
    st.Page("views/home.py", title=t("nav_home"), icon="🏠", default=True),
    st.Page("views/plan.py", title=t("nav_plan"), icon="🗓️", url_path="plan"),
    st.Page("views/trip.py", title=t("nav_trip"), icon="🧭", url_path="trip"),
    st.Page("views/explore.py", title=t("nav_explore"), icon="🏞️", url_path="explore"),
    st.Page("views/help.py", title=t("nav_help"), icon="🆘", url_path="help"),
]
st.navigation(pages, position="top").run()
