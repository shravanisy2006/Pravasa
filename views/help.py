"""Help & safety: emergency numbers, when to go where, and about Pravasa."""

import streamlit as st

import ui
from common import footer, page_banner, photo_section
from i18n import t
from weather import HELPLINES

page_banner(t("nav_help"), t("h_banner_sub"))

# Numbers and seasons, over a light photo of Jog Falls
with photo_section("safety", "Jog Falls", "Shivamogga"):
    left, right = st.columns([1, 1.2], gap="large")
    with left, st.container(key="helpbox"):
        st.html(f'<p class="pv-h3" style="margin-top:0">{t("emergency")}</p>'
                f'<p class="pv-sub">{ui.e(t("tap_call"))}</p>')
        st.html(ui.helplines(HELPLINES))
    with right, st.container(key="seasonbox"):
        st.html(f'<p class="pv-h3" style="margin-top:0">{t("when_where")}</p>')
        st.html(ui.season_guide())

# About Pravasa, over a light photo of Gol Gumbaz
with photo_section("about", "Gol Gumbaz", "Vijayapura"):
    st.html(ui.section_title(t("about_title")))
    a1, a2 = st.columns(2, gap="large")
    with a1, st.container(key="aboutbox"):
        st.markdown(f"{t('about_p1')}\n\n{t('about_p2')}")
    with a2, st.container(key="sourcebox"):
        sources = "\n".join(f"- {t(k)}" for k in
                            ("src_routes", "src_photos", "src_travellers", "src_hotels",
                             "src_weather"))
        st.markdown(f"**{t('sources_title')}**\n\n{sources}\n\n{t('estimates_note')}")

footer()
