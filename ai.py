"""
Pravasa AI helpers (Google Gemini).

Two jobs:
1. understand_request(): turn a free-text request in English or Kannada,
   e.g. "ಬೆಂಗಳೂರಿನಿಂದ 3 ದಿನದ ದೇವಸ್ಥಾನ ಪ್ರವಾಸ, ₹10000 ಬಜೆಟ್",
   into trip settings (days, budget, interests...).
2. write_story(): turn the finished plan into a friendly trip description,
   in English or Kannada. The AI is only given places from OUR plan,
   so it describes real, verified places instead of inventing new ones.

If no API key is set, or the AI call fails, both functions return None
and the app keeps working without the AI parts.
"""

import json
import os
import re

from dotenv import load_dotenv

load_dotenv()  # reads GEMINI_API_KEY from the .env file on your laptop

MODEL = "gemini-3.8-flash"  # change here if Google renames the model

ALLOWED = {
    "start_city": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi"],
    "interests": ["Nature", "Heritage", "Temples", "Beaches", "Wildlife", "Food"],
    "transport": ["Own car / cab", "Bus (KSRTC)", "Bike"],
    "stay_style": ["Budget", "Comfort", "Premium"],
}


def _client():
    """Create a Gemini client, or return None if there's no API key."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    from google import genai
    return genai.Client(api_key=key)


def ai_available():
    return bool(os.getenv("GEMINI_API_KEY"))


def _ask(system_instruction, prompt):
    """Send one request to Gemini and return its text (or None on failure)."""
    client = _client()
    if client is None:
        return None
    try:
        interaction = client.interactions.create(
            model=MODEL,
            system_instruction=system_instruction,
            input=prompt,
        )
        return interaction.output_text
    except Exception as e:  # network problem, quota reached, wrong key...
        print("Gemini error:", e)
        return None


def understand_request(text):
    """Read a free-text trip request (English or Kannada) and return settings."""
    system = (
        "You extract trip settings from a traveller's message about a trip in "
        "Karnataka. The message may be in English, Kannada or a mix. "
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
    reply = _ask(system, text)
    if not reply:
        return None

    # Pull out the {...} part in case the model adds extra words
    match = re.search(r"\{.*\}", reply, re.DOTALL)
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
    return clean


def write_story(result, start_city, language="en"):
    """Write a friendly description of the planned trip."""
    # Give the AI only the facts from our plan
    lines = []
    for day in result["days"]:
        names = [
            f"{s['place']['name']} ({s['place']['famous_for']}; "
            f"try {s['place']['local_food']})"
            for s in day["stops"]
        ]
        lines.append(f"Day {day['day']}: " + ("; ".join(names) or "free day"))
    plan_text = "\n".join(lines)

    lang = "Kannada (ಕನ್ನಡ script)" if language == "kn" else "English"
    system = (
        "You are Pravasa, a warm and knowledgeable Karnataka travel guide. "
        f"Write in {lang}. Describe the given itinerary day by day in a lively, "
        "friendly way: one short paragraph per day, with a line of history or an "
        "interesting fact for each place and a practical tip. "
        "Only mention the places listed. Do not invent prices, timings or new "
        "places. Keep it under 300 words."
    )
    prompt = f"Trip starting from {start_city}:\n{plan_text}"
    return _ask(system, prompt)