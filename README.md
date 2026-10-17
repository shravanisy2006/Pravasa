# Pravasa (ಪ್ರವಾಸ): Karnataka AI Travel Planner

Pravasa plans a personalised, day-by-day trip across Karnataka from a typed or **spoken** request in **Kannada or English**. The plan is built from a verified dataset of real places, with real road distances, so the AI never invents destinations, distances or prices.

**Live app:** https://YOUR-APP-NAME.streamlit.app

**Problem statement:** AI Travel Planner for Karnataka. Generate personalised itineraries based on budget, interests, duration, transport and travel preferences.

---

## The problem

Tourists planning a Karnataka trip piece it together from blogs, travel agents and generic AI chatbots:

- Blogs and agents aren't personalised to your budget, days and interests.
- AI chatbots write confident itineraries with **made-up travel times, distances and prices**.
- Almost nothing works in **Kannada**, by voice, for the state's own people.

## What makes Pravasa different

| Typical AI trip planner | Pravasa |
|---|---|
| The LLM invents places and timings | Places come from a curated dataset of 55 Karnataka destinations |
| Distances are guesses | Real road distances and routes from OpenStreetMap routing (OSRM) |
| English text only | Kannada or English, typed **or spoken**, with answers read aloud in Kannada |
| No season awareness | Season warnings (monsoon, summer heat) plus real weather data |
| Just text | Map, photos, history, transport options, hotels, budget check and a PDF |

The AI (Google Gemini) is used only where it's strong: understanding free-form requests and writing a friendly narrative about places that our planner has already chosen.

## Features

**Planning**
- Plan from a form, a typed sentence, or your voice (Kannada or English)
- Day-by-day itinerary that fits each day into about 9 hours of travel and sightseeing
- Budget check with a cost breakdown for travel, stay, food and entry fees

**Each place**
- Photo and short history from Wikipedia, plus what it's famous for
- Timings, approximate entry fee, how long to spend there, and local food to try
- Ways to get there (cab, KSRTC bus, train, auto or walk) with time and cost, and the best option marked
- Nearby places worth a detour
- 📍 Directions button that opens Google Maps

**The whole trip**
- Route map with real roads, one colour per day, and a Google Maps link for each day
- Where to stay each night: real hotels and homestays from OpenStreetMap, matched to your stay style
- Weather for each day (a live forecast, or the same month's real weather last year)
- Season tips and warnings
- AI trip story in Kannada or English, with 🔊 Listen to hear it read aloud
- Emergency and helpline numbers
- 📄 Download the full itinerary as a PDF, with Kannada text

## Tech stack

| Part | Tool |
|---|---|
| App and UI | Python, Streamlit |
| AI (understanding requests, voice transcription, trip story) | Google Gemini API |
| Kannada text-to-speech | gTTS |
| Road distances and routes | OSRM (OpenStreetMap routing) |
| Maps | Folium (Leaflet) and Google Maps links |
| Place photos and history | Wikipedia API |
| Hotels | OpenStreetMap (Overpass API) |
| Weather | Open-Meteo |
| PDF | fpdf2 with Noto Sans and Noto Sans Kannada fonts |
| Hosting | Streamlit Community Cloud |

## How it works

```
Voice (Kannada/English) ─┐
Typed request ───────────┼─► Gemini: understand → trip settings ─┐
Form ────────────────────┘                                       │
                                                                 ▼
destinations.json ─────────────────► Planner (planner.py)
(55 verified places)                 scores places by interest and season,
                                     fits them into days, estimates cost
                                                                 │
              ┌──────────────────────────────────────────────────┤ (fetched in parallel)
              ▼                ▼               ▼                 ▼
         OSRM routes     Wikipedia      OpenStreetMap      Open-Meteo
         real km/time    photos+history  hotels            weather
              └──────────────────────────────────────────────────┤
                                                                 ▼
                     Streamlit app: map, day tabs, costs, season tips
                                                                 │
                     Gemini trip story ─► gTTS voice ─► PDF download
```

## Project structure

| File | What it does |
|---|---|
| `app.py` | The Streamlit app (all screens) |
| `planner.py` | Picks places and fits them into days; cost estimate |
| `destinations.json` | Dataset of 55 Karnataka destinations |
| `ai.py` | Gemini: voice and text understanding, trip story |
| `voice.py` | Reads the trip aloud (Kannada or English) |
| `places.py` | Wikipedia info, road routes, Google Maps links |
| `trip_map.py` | Real road distances and the route map |
| `extras.py` | Transport options, nearby places, hotels |
| `weather.py` | Weather, season tips, helplines |
| `report.py` | PDF itinerary |
| `fonts/` | Noto fonts for Kannada in the PDF (SIL Open Font License) |

## Run it on your computer

You need Python 3.12 and a free Gemini API key from [Google AI Studio](https://aistudio.google.com).

```bash
git clone https://github.com/shravanisy2006/Pravasa.git
cd Pravasa
python -m venv venv
venv\Scripts\activate          # on Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to a new file called `.env` and put your key in it:

```
GEMINI_API_KEY=your-key-here
```

Then start the app:

```bash
streamlit run app.py
```

The app still works without a key. You can plan with the form, and only the AI features (typed or voice requests, and the trip story) are switched off.

## Notes and limitations

- Entry fees, timings and costs are approximate. Please confirm locally before travelling.
- Hotel suggestions come from OpenStreetMap and don't include live prices or availability.
- The weather forecast assumes the trip starts today. For later months, it shows that month's real weather from last year.
- No login is needed.

## Future scope

- More destinations, plus user reviews and ratings
- Live hotel and bus or train booking through partner APIs
- More Indian languages, and a fully voice-driven conversation
- An offline mobile app for areas with poor network
