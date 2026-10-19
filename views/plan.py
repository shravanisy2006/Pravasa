"""Plan a trip: choose every detail yourself."""

import streamlit as st

from common import (INTERESTS, MONTHS, build_plan_and_open, footer, page_banner, photo_section,
                    prefs)
from i18n import month_name, t, w
from planner import START_CITIES, STAY_STYLES, TRANSPORT

page_banner(t("nav_plan"), t("plan_banner_sub"))

p = prefs()

# Each box starts with your saved choice (so it's kept when you switch pages)
for key, value in p.items():
    st.session_state.setdefault(f"f_{key}", value)

# The form sits over a light photo of Coorg's Abbey Falls
with photo_section("plan", "Abbey Falls", "Kodagu"), st.container(key="planform"):
    st.html(f'<p class="pv-h3" style="margin-top:0">{t("your_trip")}</p>')
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.selectbox(t("f_start"), list(START_CITIES.keys()), key="f_start_city", format_func=w)
        st.slider(t("f_days"), 1, 10, key="f_days")
    with col2:
        st.selectbox(t("f_month"), MONTHS, key="f_month_name",
                     format_func=lambda m: month_name(MONTHS.index(m) + 1))
        st.number_input(t("f_budget"), min_value=1000, step=1000, key="f_budget")
    with col3:
        st.selectbox(t("f_transport"), list(TRANSPORT.keys()), key="f_transport", format_func=w)
        st.selectbox(t("f_stay"), list(STAY_STYLES.keys()), key="f_stay_style", format_func=w)

    st.pills(t("f_interests"), INTERESTS, selection_mode="multi", key="f_interests",
             format_func=w)
    st.radio(t("f_language"), ["English", "ಕನ್ನಡ"], key="f_language", horizontal=True)

    # Save what's on screen, so it's remembered on other pages
    for key in p:
        p[key] = st.session_state[f"f_{key}"]

    if st.button(t("plan_btn"), type="primary", key="plan_from_form"):
        if not p["interests"]:
            st.warning(t("pick_interest"))
        else:
            build_plan_and_open()

footer()
