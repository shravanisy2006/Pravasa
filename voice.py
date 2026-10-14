"""
Pravasa voice output: reads the trip aloud in Kannada or English.

Uses gTTS (Google Text-to-Speech), which is free, needs no API key, and
supports Kannada ("kn"). It needs an internet connection.
"""

import io
import re

import streamlit as st


def clean_for_speech(text):
    """Remove markdown symbols (**, #, links) so they aren't read out."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # [label](url) -> label
    text = re.sub(r"[*#_`>|]", "", text)
    return re.sub(r"\s+", " ", text).strip()


@st.cache_data(ttl=24 * 3600, show_spinner=False)
def speak(text, language="en"):
    """Return MP3 audio bytes for `text`, or None if it fails."""
    from gtts import gTTS
    try:
        buffer = io.BytesIO()
        gTTS(clean_for_speech(text), lang="kn" if language == "kn" else "en",
             tld="co.in").write_to_fp(buffer)
        return buffer.getvalue()
    except Exception as e:
        print("Text-to-speech error:", e)
        return None


def plan_script(result, start_city, language="en"):
    """A simple spoken summary of the plan, used when there's no AI story."""
    lines = []
    for day in result["days"]:
        if language == "kn":
            names = ", ".join(s["place"]["name_kn"] for s in day["stops"]) or "ವಿಶ್ರಾಂತಿ ದಿನ"
            lines.append(f"ದಿನ {day['day']}: {names}.")
        else:
            names = ", ".join(s["place"]["name"] for s in day["stops"]) or "a free day"
            lines.append(f"Day {day['day']}: {names}.")
    total = result["costs"]["Total"]
    if language == "kn":
        intro = "ನಿಮ್ಮ ಪ್ರವಾಸದ ಯೋಜನೆ ಇಲ್ಲಿದೆ."
        outro = f"ಅಂದಾಜು ಒಟ್ಟು ವೆಚ್ಚ {total} ರೂಪಾಯಿ. ಶುಭ ಪ್ರಯಾಣ!"
    else:
        intro = f"Here is your trip from {start_city}."
        outro = f"The estimated total cost is {total} rupees. Have a great trip!"
    return " ".join([intro, *lines, outro])