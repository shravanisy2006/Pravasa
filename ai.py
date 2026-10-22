"""
Pravasa AI helpers (Google Gemini).

Three jobs:
1. understand_audio(): listen to a voice recording (Kannada or English) and,
   in ONE step, write down what was said AND pull out the trip settings.
2. understand_request(): the same for typed text.
3. stream_story(): write a short, friendly trip description in English or
   Kannada, sent word by word so it appears on screen straight away.
   The AI only gets places from OUR plan, so it can't invent new ones.

Speed settings: "thinking" is kept low (these are simple tasks) and voice
is understood in a single request instead of two.

If no API key is set, or a call fails, the functions return None and the
app keeps working without the AI parts.
"""

import base64
import json
import os
import re

from dotenv import load_dotenv

load_dotenv()  # reads GEMINI_API_KEY from the .env file on your laptop

MODEL = "gemini-3.8-flash"  # change here if Google renames the model
# A smaller, quicker model for understanding requests (voice and typed).
# If it isn't available on your key, Pravasa automatically uses MODEL instead.
QUICK_MODEL = "gemini-3.5-flash-lite"
FAST = {"thinking_level": "low"}  # less "thinking" = faster answers
_quick_ok = True  # becomes False if the quick model fails, so we stop trying it

ALLOWED = {
    "start_city": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi"],
    "interests": ["Nature", "Heritage", "Temples", "Beaches", "Wildlife", "Food"],
    "transport": ["Own car / cab", "Bus (KSRTC)", "Bike"],
    "stay_style": ["Budget", "Comfort", "Premium"],
}

SETTINGS_INSTRUCTIONS = (
    "Reply with ONLY a JSON object, no other text, with these keys:\n"
    '  "days": number 1-10,\n'
    '  "budget": number in rupees,\n'
    f'  "start_city": one of {ALLOWED["start_city"]},\n'
    f'  "interests": list from {ALLOWED["interests"]},\n'
    '  "month": number 1-12 or null if not mentioned,\n'
    f'  "transport": one of {ALLOWED["transport"]},\n'
    f'  "stay_style": one of {ALLOWED["stay_style"]},\n'
    '  "language": "kn" if the message is mainly Kannada, otherwise "en".\n'
    "Use null for anything not mentioned. Map ideas to the closest interest, "
    "e.g. waterfalls or hills -> Nature, forts or palaces -> Heritage, "
    "safari -> Wildlife."
)

_CLIENT = None


def _api_key():
    """Find the Gemini key: .env on your laptop, or Secrets on Streamlit Cloud."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:  # no secrets file on this computer
        return None


def _client():
    """Create the Gemini client once and reuse it (or None if no API key)."""
    global _CLIENT
    key = _api_key()
    if not key:
        return None
    if _CLIENT is None:
        from google import genai
        _CLIENT = genai.Client(api_key=key)
    return _CLIENT


def ai_available():
    return bool(_api_key())


def _ask(system_instruction, prompt, quick=False):
    """Send one request to Gemini and return its text (or None on failure).
    quick=True tries the faster QUICK_MODEL first, then falls back to MODEL."""
    global _quick_ok
    client = _client()
    if client is None:
        return None
    models = [QUICK_MODEL, MODEL] if (quick and _quick_ok) else [MODEL]
    for model in models:
        try:
            interaction = client.interactions.create(
                model=model,
                system_instruction=system_instruction,
                input=prompt,
                generation_config=FAST,
            )
            return interaction.output_text
        except Exception as e:  # network problem, quota reached, wrong key...
            print(f"Gemini error ({model}):", e)
            if model == QUICK_MODEL:
                _quick_ok = False  # use the main model from now on
    return None


def _parse_settings(reply):
    """Turn the AI's JSON reply into clean, safe trip settings."""
    if not reply:
        return None
    match = re.search(r"\{.*\}", reply, re.DOTALL)  # the {...} part only
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None

    # Keep only valid values, so a strange answer can't break the app
    clean = {}
    if isinstance(data.get("days"), (int, float)):
        clean["days"] = int(min(max(data["days"], 1), 10))
    if isinstance(data.get("budget"), (int, float)) and data["budget"] >= 1000:
        clean["budget"] = int(data["budget"])
    if isinstance(data.get("month"), (int, float)) and 1 <= data["month"] <= 12:
        clean["month"] = int(data["month"])
    for key in ("start_city", "transport", "stay_style"):
        if data.get(key) in ALLOWED[key]:
            clean[key] = data[key]
    interests = [i for i in (data.get("interests") or []) if i in ALLOWED["interests"]]
    if interests:
        clean["interests"] = interests
    clean["language"] = "kn" if data.get("language") == "kn" else "en"
    if isinstance(data.get("transcript"), str):
        clean["transcript"] = data["transcript"].strip()
    return clean


def understand_request(text):
    """Read a typed trip request (English or Kannada) and return settings."""
    system = (
        "You extract trip settings from a traveller's message about a trip in "
        "Karnataka. The message may be in English, Kannada or a mix.\n"
        + SETTINGS_INSTRUCTIONS
    )
    return _parse_settings(_ask(system, text, quick=True))


def understand_audio(audio_bytes, mime_type="audio/wav"):
    """Listen to a voice request and return settings plus a 'transcript'."""
    system = (
        "You listen to a traveller's voice message about a trip in Karnataka. "
        "It may be in Kannada, English or a mix.\n"
        + SETTINGS_INSTRUCTIONS
        + '\nAlso include "transcript": exactly what was said, with Kannada '
          "words in Kannada script and English words in English."
    )
    prompt = [
        {"type": "text", "text": "Here is the voice message."},
        {"type": "audio",
         "data": base64.b64encode(audio_bytes).decode("utf-8"),
         "mime_type": mime_type},
    ]
    return _parse_settings(_ask(system, prompt, quick=True))


def _story_request(result, start_city, language):
    lines = []
    for day in result["days"]:
        names = [f"{s['place']['name']} ({s['place']['famous_for']})" for s in day["stops"]]
        lines.append(f"Day {day['day']}: " + ("; ".join(names) or "free day"))
    lang = "Kannada (ಕನ್ನಡ script)" if language == "kn" else "English"
    system = (
        "You are Pravasa, a warm Karnataka travel guide. "
        f"Write in {lang}. Describe the itinerary day by day: two or three "
        "lively sentences per day, with one interesting fact or bit of history. "
        "Only mention the places listed. Do not invent prices, timings or new "
        "places. Keep it under 150 words."
    )
    prompt = f"Trip starting from {start_city}:\n" + "\n".join(lines)
    return system, prompt


def stream_story(result, start_city, language="en"):
    """Yield the trip story a few words at a time (for st.write_stream)."""
    client = _client()
    if client is None:
        return
    system, prompt = _story_request(result, start_city, language)
    try:
        stream = client.interactions.create(
            model=MODEL,
            system_instruction=system,
            input=prompt,
            generation_config=FAST,
            stream=True,
        )
        for event in stream:
            if event.event_type == "step.delta" and event.delta.type == "text":
                yield event.delta.text
    except Exception as e:
        print("Gemini story error:", e)
