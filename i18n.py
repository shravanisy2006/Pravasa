"""
Pravasa in two languages: English and Kannada (ಕನ್ನಡ).

Every piece of text on the website lives here, once in English ("en") and
once in Kannada ("kn"). Pages call t("key") and get the text in the language
the visitor chose with the ಕನ್ನಡ / English switch.

To correct a translation, change the Kannada text below. Keep the {words}
in curly brackets exactly as they are: the app fills them in.
"""

import streamlit as st

STRINGS = {
    # ---------- Menu bar ----------
    "nav_home": {"en": "Home", "kn": "ಮುಖಪುಟ"},
    "nav_plan": {"en": "Plan a trip", "kn": "ಪ್ರವಾಸ ಯೋಜಿಸಿ"},
    "nav_trip": {"en": "My trip", "kn": "ನನ್ನ ಪ್ರವಾಸ"},
    "nav_explore": {"en": "Explore Karnataka", "kn": "ಕರ್ನಾಟಕ ಅನ್ವೇಷಿಸಿ"},
    "nav_help": {"en": "Help & safety", "kn": "ಸಹಾಯ ಮತ್ತು ಸುರಕ್ಷತೆ"},
    "language": {"en": "Language", "kn": "ಭಾಷೆ"},

    # ---------- Home ----------
    "lede": {"en": "Say where you'd like to go, in ಕನ್ನಡ or English. Pravasa plans the days, "
                   "the roads and the stays across Karnataka.",
             "kn": "ನೀವು ಎಲ್ಲಿಗೆ ಹೋಗಬೇಕೆಂದು ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಹೇಳಿ. ಕರ್ನಾಟಕದಾದ್ಯಂತ "
                   "ದಿನಗಳು, ದಾರಿಗಳು ಮತ್ತು ವಸತಿಯನ್ನು ಪ್ರವಾಸ ಯೋಜಿಸುತ್ತದೆ."},
    "point1": {"en": "{n} hand-checked places, from Hampi to the coast",
               "kn": "ಹಂಪಿಯಿಂದ ಕರಾವಳಿಯವರೆಗೆ {n} ಪರಿಶೀಲಿಸಿದ ಸ್ಥಳಗಳು"},
    "point2": {"en": "Real road distances, weather and season advice",
               "kn": "ನಿಜವಾದ ರಸ್ತೆ ದೂರ, ಹವಾಮಾನ ಮತ್ತು ಋತುವಿನ ಸಲಹೆ"},
    "point3": {"en": "Speaks and listens in Kannada",
               "kn": "ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡುತ್ತದೆ, ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತದೆ"},
    "ask_title": {"en": "Where shall we go?", "kn": "ಎಲ್ಲಿಗೆ ಹೋಗೋಣ?"},
    "ask_sub": {"en": "Speak or type your trip: days, budget, where you start and what you love.",
                "kn": "ನಿಮ್ಮ ಪ್ರವಾಸದ ಬಗ್ಗೆ ಹೇಳಿ ಅಥವಾ ಬರೆಯಿರಿ: ಎಷ್ಟು ದಿನ, ಬಜೆಟ್, ಎಲ್ಲಿಂದ "
                      "ಹೊರಡುವಿರಿ ಮತ್ತು ನಿಮಗೆ ಏನು ಇಷ್ಟ."},
    "speak_label": {"en": "Speak in Kannada or English", "kn": "ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಮಾತನಾಡಿ"},
    "type_label": {"en": "Or type it", "kn": "ಅಥವಾ ಬರೆಯಿರಿ"},
    "plan_btn": {"en": "Plan my trip", "kn": "ನನ್ನ ಪ್ರವಾಸ ಯೋಜಿಸಿ"},
    "listening": {"en": "Listening and planning...", "kn": "ಕೇಳಿಸಿಕೊಂಡು ಯೋಜಿಸುತ್ತಿದೆ..."},
    "reading": {"en": "Reading your request...", "kn": "ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು ಓದುತ್ತಿದೆ..."},
    "add_interest_voice": {"en": "Got it. Now add what you enjoy, like temples, beaches or nature.",
                           "kn": "ಅರ್ಥವಾಯಿತು. ಈಗ ನಿಮಗೆ ಇಷ್ಟವಾದುದನ್ನು ಸೇರಿಸಿ, ಉದಾಹರಣೆಗೆ "
                                 "ದೇವಾಲಯಗಳು, ಕಡಲತೀರಗಳು ಅಥವಾ ಪ್ರಕೃತಿ."},
    "add_interest": {"en": "Add what you enjoy, like temples, beaches or nature.",
                     "kn": "ನಿಮಗೆ ಇಷ್ಟವಾದುದನ್ನು ಸೇರಿಸಿ, ಉದಾಹರಣೆಗೆ ದೇವಾಲಯಗಳು, ಕಡಲತೀರಗಳು "
                           "ಅಥವಾ ಪ್ರಕೃತಿ."},
    "unclear": {"en": "That recording wasn't clear. Record again, a little closer to the mic.",
                "kn": "ಧ್ವನಿ ಸ್ಪಷ್ಟವಾಗಿರಲಿಲ್ಲ. ಮೈಕ್‌ಗೆ ಸ್ವಲ್ಪ ಹತ್ತಿರವಾಗಿ ಮತ್ತೆ ರೆಕಾರ್ಡ್ ಮಾಡಿ."},
    "type_first": {"en": "Type or speak a few words about your trip first.",
                   "kn": "ಮೊದಲು ನಿಮ್ಮ ಪ್ರವಾಸದ ಬಗ್ಗೆ ಕೆಲವು ಪದಗಳನ್ನು ಬರೆಯಿರಿ ಅಥವಾ ಹೇಳಿ."},
    "cant_read": {"en": "Pravasa couldn't read that request. Rephrase it, or choose the "
                        "details yourself.",
                  "kn": "ಈ ವಿನಂತಿ ಅರ್ಥವಾಗಲಿಲ್ಲ. ಬೇರೆ ರೀತಿಯಲ್ಲಿ ಹೇಳಿ, ಅಥವಾ ವಿವರಗಳನ್ನು "
                        "ನೀವೇ ಆರಿಸಿ."},
    "no_key": {"en": "The AI isn't set up yet: add your GEMINI_API_KEY to the .env file.",
               "kn": "AI ಇನ್ನೂ ಸಿದ್ಧವಾಗಿಲ್ಲ: .env ಫೈಲ್‌ಗೆ GEMINI_API_KEY ಸೇರಿಸಿ."},
    "planning_now": {"en": "Planning your trip…", "kn": "ನಿಮ್ಮ ಪ್ರವಾಸ ಸಿದ್ಧವಾಗುತ್ತಿದೆ…"},
    "planning_sub": {"en": "Finding places, roads and stays across Karnataka",
                     "kn": "ಕರ್ನಾಟಕದಾದ್ಯಂತ ಸ್ಥಳಗಳು, ದಾರಿಗಳು ಮತ್ತು ವಸತಿ ಹುಡುಕುತ್ತಿದೆ"},
    "listening_sub": {"en": "Understanding what you said",
                      "kn": "ನೀವು ಹೇಳಿದ್ದನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುತ್ತಿದೆ"},
    "try_label": {"en": "Or tap an example", "kn": "ಅಥವಾ ಒಂದು ಉದಾಹರಣೆ ಆರಿಸಿ"},
    "choose_self": {"en": "Prefer to choose every detail yourself?",
                    "kn": "ಎಲ್ಲಾ ವಿವರಗಳನ್ನು ನೀವೇ ಆರಿಸಲು ಬಯಸುವಿರಾ?"},
    "explore_title": {"en": "Explore by what you love", "kn": "ನಿಮ್ಮ ಇಷ್ಟದಂತೆ ಅನ್ವೇಷಿಸಿ"},
    "explore_sub": {"en": "Pick a theme to see every place that fits it.",
                    "kn": "ಒಂದು ವಿಷಯವನ್ನು ಆರಿಸಿ, ಅದಕ್ಕೆ ಹೊಂದುವ ಎಲ್ಲಾ ಸ್ಥಳಗಳನ್ನು ನೋಡಿ."},
    "see_places": {"en": "See {n} places", "kn": "{n} ಸ್ಥಳಗಳನ್ನು ನೋಡಿ"},
    "how_title": {"en": "How Pravasa plans your trip",
                  "kn": "ಪ್ರವಾಸ ನಿಮ್ಮ ಪ್ರಯಾಣವನ್ನು ಹೇಗೆ ಯೋಜಿಸುತ್ತದೆ"},
    "step1_t": {"en": "Tell Pravasa your trip", "kn": "ನಿಮ್ಮ ಪ್ರವಾಸದ ಬಗ್ಗೆ ಹೇಳಿ"},
    "step1_d": {"en": "Speak or type in Kannada or English: how many days, your budget, "
                      "where you start and what you love.",
                "kn": "ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಹೇಳಿ ಅಥವಾ ಬರೆಯಿರಿ: ಎಷ್ಟು ದಿನ, ನಿಮ್ಮ ಬಜೆಟ್, "
                      "ಎಲ್ಲಿಂದ ಹೊರಡುವಿರಿ ಮತ್ತು ನಿಮಗೆ ಏನು ಇಷ್ಟ."},
    "step2_t": {"en": "Pravasa plans it", "kn": "ಪ್ರವಾಸ ಯೋಜನೆ ಮಾಡುತ್ತದೆ"},
    "step2_d": {"en": "It picks real places that match, fits them into each day using real "
                      "road times, and checks the season and your budget.",
                "kn": "ನಿಮಗೆ ಹೊಂದುವ ನಿಜವಾದ ಸ್ಥಳಗಳನ್ನು ಆರಿಸಿ, ರಸ್ತೆ ಪ್ರಯಾಣದ ಸಮಯದಂತೆ "
                      "ಪ್ರತಿದಿನಕ್ಕೆ ಹೊಂದಿಸುತ್ತದೆ, ಋತು ಮತ್ತು ಬಜೆಟ್ ಅನ್ನು ಪರಿಶೀಲಿಸುತ್ತದೆ."},
    "step3_t": {"en": "Go and enjoy", "kn": "ಹೊರಡಿ, ಆನಂದಿಸಿ"},
    "step3_d": {"en": "Follow the day-by-day plan with maps, photos, stays and weather. "
                      "Listen to it in Kannada or save it as a PDF.",
                "kn": "ನಕ್ಷೆ, ಫೋಟೋಗಳು, ವಸತಿ ಮತ್ತು ಹವಾಮಾನದೊಂದಿಗೆ ದಿನವಾರು ಯೋಜನೆಯನ್ನು "
                      "ಅನುಸರಿಸಿ. ಅದನ್ನು ಕನ್ನಡದಲ್ಲಿ ಕೇಳಿ ಅಥವಾ PDF ಆಗಿ ಉಳಿಸಿ."},
    "footer": {"en": "Pravasa plans with data from OpenStreetMap, OSRM, Wikipedia, Wikimedia "
                     "Commons, Wikivoyage and Open-Meteo. Costs, fees and timings are "
                     "estimates; please confirm locally before you travel.",
               "kn": "ಪ್ರವಾಸ OpenStreetMap, OSRM, ವಿಕಿಪೀಡಿಯ, ವಿಕಿಮೀಡಿಯ ಕಾಮನ್ಸ್, ವಿಕಿವಾಯೇಜ್ "
                     "ಮತ್ತು Open-Meteo ಮಾಹಿತಿಯನ್ನು ಬಳಸುತ್ತದೆ. ವೆಚ್ಚ, ಶುಲ್ಕ ಮತ್ತು ಸಮಯಗಳು "
                     "ಅಂದಾಜು; ಪ್ರಯಾಣಕ್ಕೆ ಮೊದಲು ಸ್ಥಳೀಯವಾಗಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."},

    # ---------- Plan a trip ----------
    "plan_banner_sub": {"en": "Choose where you start, when you go and what you love. "
                              "Pravasa does the rest.",
                        "kn": "ಎಲ್ಲಿಂದ ಹೊರಡುವಿರಿ, ಯಾವಾಗ ಹೋಗುವಿರಿ ಮತ್ತು ನಿಮಗೆ ಏನು ಇಷ್ಟ ಎಂದು "
                              "ಆರಿಸಿ. ಉಳಿದುದನ್ನು ಪ್ರವಾಸ ನೋಡಿಕೊಳ್ಳುತ್ತದೆ."},
    "your_trip": {"en": "Your trip", "kn": "ನಿಮ್ಮ ಪ್ರವಾಸ"},
    "f_start": {"en": "Starting from", "kn": "ಎಲ್ಲಿಂದ ಹೊರಡುವಿರಿ"},
    "f_days": {"en": "How many days?", "kn": "ಎಷ್ಟು ದಿನ?"},
    "f_month": {"en": "Travel month", "kn": "ಪ್ರಯಾಣದ ತಿಂಗಳು"},
    "f_budget": {"en": "Budget (₹)", "kn": "ಬಜೆಟ್ (₹)"},
    "f_transport": {"en": "How will you travel?", "kn": "ಹೇಗೆ ಪ್ರಯಾಣಿಸುವಿರಿ?"},
    "f_stay": {"en": "Stay style", "kn": "ವಸತಿಯ ಬಗೆ"},
    "f_interests": {"en": "What do you enjoy?", "kn": "ನಿಮಗೆ ಏನು ಇಷ್ಟ?"},
    "f_language": {"en": "Trip story language", "kn": "ಪ್ರವಾಸ ಕಥೆಯ ಭಾಷೆ"},
    "pick_interest": {"en": "Pick at least one thing you enjoy, so Pravasa knows what to plan.",
                      "kn": "ಯೋಜನೆಗಾಗಿ ನಿಮಗೆ ಇಷ್ಟವಾದ ಕನಿಷ್ಠ ಒಂದನ್ನು ಆರಿಸಿ."},

    # ---------- My trip ----------
    "trip_empty_sub": {"en": "Your plan will appear here once you've made one.",
                       "kn": "ನೀವು ಯೋಜನೆ ಮಾಡಿದ ನಂತರ ಅದು ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ."},
    "no_trip": {"en": "No trip planned yet", "kn": "ಇನ್ನೂ ಯಾವ ಪ್ರವಾಸವನ್ನೂ ಯೋಜಿಸಿಲ್ಲ"},
    "no_trip_body": {"en": "Tell Pravasa about your trip on the home page, by voice or text, "
                           "or choose every detail yourself.",
                     "kn": "ಮುಖಪುಟದಲ್ಲಿ ಧ್ವನಿ ಅಥವಾ ಬರಹದ ಮೂಲಕ ನಿಮ್ಮ ಪ್ರವಾಸದ ಬಗ್ಗೆ ಹೇಳಿ, "
                           "ಅಥವಾ ಎಲ್ಲಾ ವಿವರಗಳನ್ನು ನೀವೇ ಆರಿಸಿ."},
    "speak_or_type": {"en": "Speak or type your trip", "kn": "ಮಾತನಾಡಿ ಅಥವಾ ಬರೆಯಿರಿ"},
    "choose_details": {"en": "Choose the details", "kn": "ವಿವರಗಳನ್ನು ಆರಿಸಿ"},
    "trip_title": {"en": "Your {n} {days} from {city}", "kn": "{city_from} {n} ದಿನಗಳ ಪ್ರವಾಸ"},
    "trip_sub": {"en": "{interests} in {month}, by {transport}, {stay} stays",
                 "kn": "{interests}, {month}, {transport}, {stay} ವಸತಿ"},
    "you_said": {"en": "You said", "kn": "ನೀವು ಹೇಳಿದ್ದು"},
    "est_total": {"en": "Estimated total", "kn": "ಅಂದಾಜು ಒಟ್ಟು ವೆಚ್ಚ"},
    "your_budget": {"en": "Your budget", "kn": "ನಿಮ್ಮ ಬಜೆಟ್"},
    "under": {"en": "₹{x} under budget", "kn": "ಬಜೆಟ್‌ಗಿಂತ ₹{x} ಕಡಿಮೆ"},
    "over": {"en": "₹{x} over budget", "kn": "ಬಜೆಟ್‌ಗಿಂತ ₹{x} ಹೆಚ್ಚು"},
    "total_drive": {"en": "Total driving, including the way home",
                    "kn": "ಒಟ್ಟು ಪ್ರಯಾಣ, ಮನೆಗೆ ಮರಳುವ ದಾರಿಯೂ ಸೇರಿ"},
    "save_money": {"en": "To save money: fewer days, a budget stay style, or KSRTC buses.",
                   "kn": "ಹಣ ಉಳಿಸಲು: ಕಡಿಮೆ ದಿನಗಳು, ಕಡಿಮೆ ವೆಚ್ಚದ ವಸತಿ ಅಥವಾ KSRTC ಬಸ್ಸುಗಳು."},
    "est_roads": {"en": "Some distances are estimates because the road service didn't respond.",
                  "kn": "ರಸ್ತೆ ಸೇವೆ ಸಿಗದ ಕಾರಣ ಕೆಲವು ದೂರಗಳು ಅಂದಾಜು."},
    "change_details": {"en": "Change the details", "kn": "ವಿವರಗಳನ್ನು ಬದಲಿಸಿ"},
    "season_exp": {"en": "Travelling in {month}: what to know",
                   "kn": "{month} ತಿಂಗಳಲ್ಲಿ ಪ್ರಯಾಣ: ತಿಳಿದಿರಬೇಕಾದದ್ದು"},
    "finding_routes": {"en": "Finding real road routes...", "kn": "ರಸ್ತೆ ಮಾರ್ಗಗಳನ್ನು ಹುಡುಕುತ್ತಿದೆ..."},
    "loading": {"en": "Loading photos, weather and places to stay...",
                "kn": "ಫೋಟೋಗಳು, ಹವಾಮಾನ ಮತ್ತು ವಸತಿ ಮಾಹಿತಿ ತರುತ್ತಿದೆ..."},
    "route_title": {"en": "Your route", "kn": "ನಿಮ್ಮ ಮಾರ್ಗ"},
    "route_sub": {"en": "Each colour is one day. Tap a dot to see the place.",
                  "kn": "ಪ್ರತಿ ಬಣ್ಣ ಒಂದು ದಿನ. ಸ್ಥಳ ನೋಡಲು ಚುಕ್ಕೆಯ ಮೇಲೆ ಒತ್ತಿ."},
    "day_by_day": {"en": "Day by day", "kn": "ದಿನವಾರು ಯೋಜನೆ"},
    "day_n": {"en": "Day {n}", "kn": "ದಿನ {n}"},
    "open_day_maps": {"en": "Open this day in Google Maps", "kn": "ಈ ದಿನದ ದಾರಿ Google Mapsನಲ್ಲಿ"},
    "free_day": {"en": "A free day. Rest, shop, or go back to a favourite spot.",
                 "kn": "ಬಿಡುವಿನ ದಿನ. ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ, ಶಾಪಿಂಗ್ ಮಾಡಿ ಅಥವಾ ಇಷ್ಟದ ಸ್ಥಳಕ್ಕೆ "
                       "ಮತ್ತೆ ಹೋಗಿ."},
    "travel_line": {"en": "{km} km{est}, about {h} h to get here",
                    "kn": "{km} ಕಿ.ಮೀ{est}, ಇಲ್ಲಿಗೆ ತಲುಪಲು ಸುಮಾರು {h} ಗಂಟೆ"},
    "estimate_tag": {"en": " (estimate)", "kn": " (ಅಂದಾಜು)"},
    "long_drive": {"en": "Long drive", "kn": "ದೀರ್ಘ ಪ್ರಯಾಣ"},
    "stop_n": {"en": "Stop {n}", "kn": "ನಿಲ್ದಾಣ {n}"},
    "directions": {"en": "Directions", "kn": "ದಾರಿ"},
    "read_more_wiki": {"en": "Read more on Wikipedia", "kn": "ವಿಕಿಪೀಡಿಯದಲ್ಲಿ ಇನ್ನಷ್ಟು ಓದಿ"},
    "english_note": {"en": "", "kn": " (ಇಂಗ್ಲಿಷ್)"},
    "fact_time": {"en": "Time to spend", "kn": "ಕಳೆಯಬಹುದಾದ ಸಮಯ"},
    "fact_entry": {"en": "Entry", "kn": "ಪ್ರವೇಶ ಶುಲ್ಕ"},
    "fact_open": {"en": "Open", "kn": "ತೆರೆದಿರುವ ಸಮಯ"},
    "fact_food": {"en": "Local food to try", "kn": "ಸವಿಯಬೇಕಾದ ಸ್ಥಳೀಯ ಆಹಾರ"},
    "about_hours": {"en": "About {h} hours", "kn": "ಸುಮಾರು {h} ಗಂಟೆ"},
    "free": {"en": "Free", "kn": "ಉಚಿತ"},
    "about_fee": {"en": "About ₹{x}", "kn": "ಸುಮಾರು ₹{x}"},
    "check_locally": {"en": "Check locally", "kn": "ಸ್ಥಳದಲ್ಲಿ ವಿಚಾರಿಸಿ"},
    "travellers_say": {"en": "What travellers say", "kn": "ಪ್ರವಾಸಿಗರು ಏನು ಹೇಳುತ್ತಾರೆ"},
    "travellers_src": {"en": "From the Wikivoyage traveller guide to {link}, written by travellers",
                       "kn": "ಪ್ರವಾಸಿಗರೇ ಬರೆದ ವಿಕಿವಾಯೇಜ್ ಮಾರ್ಗದರ್ಶಿಯಿಂದ: {link} (ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ)"},
    "reviews_btn": {"en": "Read visitor reviews on Google Maps",
                    "kn": "Google Mapsನಲ್ಲಿ ಪ್ರವಾಸಿಗರ ವಿಮರ್ಶೆಗಳನ್ನು ಓದಿ"},
    "ways_here": {"en": "Ways to get here", "kn": "ಇಲ್ಲಿಗೆ ತಲುಪುವ ದಾರಿಗಳು"},
    "col_how": {"en": "How", "kn": "ಹೇಗೆ"},
    "col_time": {"en": "Time", "kn": "ಸಮಯ"},
    "col_cost": {"en": "Cost", "kn": "ವೆಚ್ಚ"},
    "col_tip": {"en": "Tip", "kn": "ಸಲಹೆ"},
    "also_nearby": {"en": "Also nearby", "kn": "ಹತ್ತಿರದ ಇತರ ಸ್ಥಳಗಳು"},
    "none_nearby": {"en": "No other listed places within 40 km.",
                    "kn": "40 ಕಿ.ಮೀ ಒಳಗೆ ಬೇರೆ ಸ್ಥಳಗಳಿಲ್ಲ."},
    "stay_tonight": {"en": "Stay tonight near {place}", "kn": "ಇಂದು ರಾತ್ರಿ {place} ಬಳಿ ವಸತಿ"},
    "stays_note": {"en": "Suggestions from OpenStreetMap. Check prices and reviews before booking.",
                   "kn": "OpenStreetMap ಸಲಹೆಗಳು. ಬುಕ್ ಮಾಡುವ ಮೊದಲು ದರ ಮತ್ತು ವಿಮರ್ಶೆಗಳನ್ನು "
                         "ಪರಿಶೀಲಿಸಿ."},
    "no_stays": {"en": "No listed stays found close by. Search the wider area:",
                 "kn": "ಹತ್ತಿರದಲ್ಲಿ ಯಾವುದೇ ವಸತಿ ಪಟ್ಟಿಯಲ್ಲಿಲ್ಲ. ಸುತ್ತಮುತ್ತ ಹುಡುಕಿ:"},
    "more_hotels": {"en": "See more hotels nearby", "kn": "ಹತ್ತಿರದ ಇನ್ನಷ್ಟು ಹೋಟೆಲ್‌ಗಳು"},
    "km_away": {"en": "{km} km away", "kn": "{km} ಕಿ.ಮೀ ದೂರ"},
    "map": {"en": "map", "kn": "ನಕ್ಷೆ"},
    "drive_home": {"en": "Drive home to {city} at the end: about {km} km, included in the cost.",
                   "kn": "ಕೊನೆಯಲ್ಲಿ ಮರಳುವ ಪ್ರಯಾಣ ({city}): ಸುಮಾರು {km} ಕಿ.ಮೀ, ವೆಚ್ಚದಲ್ಲಿ ಸೇರಿದೆ."},
    "costs_title": {"en": "What it costs", "kn": "ಎಷ್ಟು ಖರ್ಚಾಗುತ್ತದೆ"},
    "take_it": {"en": "Take it with you", "kn": "ಜೊತೆಗೆ ಕೊಂಡೊಯ್ಯಿರಿ"},
    "take_it_sub": {"en": "The whole plan in one PDF, with Kannada place names, weather, stays "
                          "and emergency numbers.",
                    "kn": "ಕನ್ನಡ ಸ್ಥಳನಾಮಗಳು, ಹವಾಮಾನ, ವಸತಿ ಮತ್ತು ತುರ್ತು ಸಂಖ್ಯೆಗಳೊಂದಿಗೆ "
                          "ಸಂಪೂರ್ಣ ಯೋಜನೆ ಒಂದೇ PDFನಲ್ಲಿ."},
    "download_pdf": {"en": "Download itinerary (PDF)", "kn": "ಯೋಜನೆ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ (PDF)"},
    "story_title": {"en": "Your trip, in short", "kn": "ನಿಮ್ಮ ಪ್ರವಾಸ, ಸಂಕ್ಷಿಪ್ತವಾಗಿ"},
    "story_unavailable": {"en": "The trip story isn't available right now. Your full plan is below.",
                          "kn": "ಪ್ರವಾಸ ಕಥೆ ಈಗ ಲಭ್ಯವಿಲ್ಲ. ಸಂಪೂರ್ಣ ಯೋಜನೆ ಕೆಳಗಿದೆ."},
    "listen": {"en": "Listen to your trip", "kn": "ಪ್ರವಾಸವನ್ನು ಕೇಳಿ"},
    "preparing_audio": {"en": "Preparing audio...", "kn": "ಧ್ವನಿ ಸಿದ್ಧಪಡಿಸುತ್ತಿದೆ..."},
    "audio_error": {"en": "Audio needs an internet connection. Check it and try again.",
                    "kn": "ಧ್ವನಿಗೆ ಇಂಟರ್ನೆಟ್ ಬೇಕು. ಸಂಪರ್ಕ ಪರಿಶೀಲಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."},
    "photos_soon": {"en": "Photos of {name} will appear here",
                    "kn": "{name} ಫೋಟೋಗಳು ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತವೆ"},
    "photo_n": {"en": "Photo {i} of {n}", "kn": "{n} ಫೋಟೋಗಳಲ್ಲಿ {i}"},
    "prev_photo": {"en": "Previous photo", "kn": "ಹಿಂದಿನ ಫೋಟೋ"},
    "next_photo": {"en": "Next photo", "kn": "ಮುಂದಿನ ಫೋಟೋ"},

    # ---------- Explore ----------
    "x_banner_sub": {"en": "{n} hand-checked places, from the Western Ghats to the coast and "
                           "the old capitals of the north.",
                     "kn": "ಪಶ್ಚಿಮ ಘಟ್ಟಗಳಿಂದ ಕರಾವಳಿಯವರೆಗೆ ಮತ್ತು ಉತ್ತರದ ಪ್ರಾಚೀನ "
                           "ರಾಜಧಾನಿಗಳವರೆಗೆ {n} ಪರಿಶೀಲಿಸಿದ ಸ್ಥಳಗಳು."},
    "x_themes": {"en": "Themes", "kn": "ವಿಷಯಗಳು"},
    "x_regions": {"en": "Regions", "kn": "ಪ್ರದೇಶಗಳು"},
    "x_all": {"en": "All of Karnataka", "kn": "ಇಡೀ ಕರ್ನಾಟಕ"},
    "x_search": {"en": "Search by name or district", "kn": "ಹೆಸರು ಅಥವಾ ಜಿಲ್ಲೆಯಿಂದ ಹುಡುಕಿ"},
    "x_search_ph": {"en": "Hampi, Coorg, Udupi...", "kn": "ಹಂಪಿ, ಉಡುಪಿ, ಮೈಸೂರು..."},
    "x_season": {"en": "Only places that are in season this month",
                 "kn": "ಈ ತಿಂಗಳಿಗೆ ಸೂಕ್ತವಾದ ಸ್ಥಳಗಳು ಮಾತ್ರ"},
    "x_found": {"en": "{n} places found", "kn": "{n} ಸ್ಥಳಗಳು ಸಿಕ್ಕಿವೆ"},
    "x_found_one": {"en": "1 place found", "kn": "1 ಸ್ಥಳ ಸಿಕ್ಕಿದೆ"},
    "x_none": {"en": "No places match these filters. Remove a filter to see more.",
               "kn": "ಈ ಆಯ್ಕೆಗಳಿಗೆ ಹೊಂದುವ ಸ್ಥಳಗಳಿಲ್ಲ. ಕೆಲವು ಆಯ್ಕೆಗಳನ್ನು ತೆಗೆದು ನೋಡಿ."},
    "x_more": {"en": "Show more places ({n} left)", "kn": "ಇನ್ನಷ್ಟು ಸ್ಥಳಗಳು ({n} ಉಳಿದಿವೆ)"},
    "reviews": {"en": "Reviews", "kn": "ವಿಮರ್ಶೆಗಳು"},
    "x_closing": {"en": "Found places you like? Pick their themes and let Pravasa plan the days.",
                  "kn": "ಇಷ್ಟವಾದ ಸ್ಥಳಗಳು ಸಿಕ್ಕವೇ? ಅವುಗಳ ವಿಷಯಗಳನ್ನು ಆರಿಸಿ, ದಿನಗಳ ಯೋಜನೆಯನ್ನು "
                        "ಪ್ರವಾಸಕ್ಕೆ ಬಿಡಿ."},
    "card_meta": {"en": "{district} district, best in {months}",
                  "kn": "{district} ಜಿಲ್ಲೆ, ಸೂಕ್ತ ಸಮಯ: {months}"},
    "no_photo": {"en": "No photo yet", "kn": "ಫೋಟೋ ಇನ್ನೂ ಇಲ್ಲ"},

    # ---------- Help & safety ----------
    "h_banner_sub": {"en": "Numbers to keep handy, the best time to visit each part of "
                           "Karnataka, and how Pravasa works.",
                     "kn": "ಕೈಗೆಟುಕುವಂತೆ ಇಟ್ಟುಕೊಳ್ಳಬೇಕಾದ ಸಂಖ್ಯೆಗಳು, ಕರ್ನಾಟಕದ ಪ್ರತಿ ಭಾಗಕ್ಕೆ "
                           "ಭೇಟಿ ನೀಡಲು ಸೂಕ್ತ ಸಮಯ ಮತ್ತು ಪ್ರವಾಸ ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ."},
    "emergency": {"en": "Emergency numbers", "kn": "ತುರ್ತು ಸಂಖ್ಯೆಗಳು"},
    "tap_call": {"en": "Tap a number to call it from your phone.",
                 "kn": "ಫೋನ್‌ನಿಂದ ಕರೆ ಮಾಡಲು ಸಂಖ್ಯೆಯ ಮೇಲೆ ಒತ್ತಿ."},
    "when_where": {"en": "When to go where", "kn": "ಎಲ್ಲಿಗೆ ಯಾವಾಗ ಹೋಗಬೇಕು"},
    "th_area": {"en": "Area", "kn": "ಪ್ರದೇಶ"},
    "th_best": {"en": "Best time", "kn": "ಸೂಕ್ತ ಸಮಯ"},
    "th_mind": {"en": "Keep in mind", "kn": "ಗಮನದಲ್ಲಿಡಿ"},
    "about_title": {"en": "About Pravasa", "kn": "ಪ್ರವಾಸದ ಬಗ್ಗೆ"},
    "about_p1": {"en": "Pravasa plans Karnataka trips from a sentence, typed or spoken, in "
                       "Kannada or English. Unlike a chatbot, it doesn't make places up: every "
                       "stop comes from a checked list of 55 destinations, and distances come "
                       "from real road routes.",
                 "kn": "ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಹೇಳಿದ ಅಥವಾ ಬರೆದ ಒಂದೇ ವಾಕ್ಯದಿಂದ ಪ್ರವಾಸ "
                       "ಕರ್ನಾಟಕ ಪ್ರವಾಸವನ್ನು ಯೋಜಿಸುತ್ತದೆ. ಸಾಮಾನ್ಯ ಚಾಟ್‌ಬಾಟ್‌ಗಳಂತೆ ಇದು "
                       "ಸ್ಥಳಗಳನ್ನು ಕಲ್ಪಿಸಿಕೊಳ್ಳುವುದಿಲ್ಲ: ಪ್ರತಿಯೊಂದು ನಿಲ್ದಾಣವೂ 55 ಪರಿಶೀಲಿಸಿದ "
                       "ಸ್ಥಳಗಳ ಪಟ್ಟಿಯಿಂದ ಬರುತ್ತದೆ, ಮತ್ತು ದೂರಗಳು ನಿಜವಾದ ರಸ್ತೆ ಮಾರ್ಗಗಳಿಂದ "
                       "ಬರುತ್ತವೆ."},
    "about_p2": {"en": "The AI (Google Gemini) understands your request and writes the trip "
                       "story. The planning itself (which places, in what order, and the costs) "
                       "is done by Pravasa's own planner, so you can trust the numbers.",
                 "kn": "AI (Google Gemini) ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಂಡು ಪ್ರವಾಸ ಕಥೆಯನ್ನು "
                       "ಬರೆಯುತ್ತದೆ. ಯಾವ ಸ್ಥಳಗಳು, ಯಾವ ಕ್ರಮದಲ್ಲಿ ಮತ್ತು ಎಷ್ಟು ವೆಚ್ಚ ಎಂಬ "
                       "ಯೋಜನೆಯನ್ನು ಪ್ರವಾಸದ ತನ್ನದೇ ಯೋಜಕ ಮಾಡುತ್ತದೆ, ಆದ್ದರಿಂದ ಅಂಕಿಅಂಶಗಳನ್ನು "
                       "ನಂಬಬಹುದು."},
    "sources_title": {"en": "Where the information comes from", "kn": "ಮಾಹಿತಿ ಎಲ್ಲಿಂದ ಬರುತ್ತದೆ"},
    "src_routes": {"en": "Road routes: OSRM, built on OpenStreetMap",
                   "kn": "ರಸ್ತೆ ಮಾರ್ಗಗಳು: OSRM (OpenStreetMap ಆಧಾರಿತ)"},
    "src_photos": {"en": "Photos and history: Wikipedia and Wikimedia Commons",
                   "kn": "ಫೋಟೋಗಳು ಮತ್ತು ಇತಿಹಾಸ: ವಿಕಿಪೀಡಿಯ ಮತ್ತು ವಿಕಿಮೀಡಿಯ ಕಾಮನ್ಸ್"},
    "src_travellers": {"en": "What travellers say: Wikivoyage",
                       "kn": "ಪ್ರವಾಸಿಗರ ಅನಿಸಿಕೆ: ವಿಕಿವಾಯೇಜ್"},
    "src_hotels": {"en": "Hotels and homestays: OpenStreetMap",
                   "kn": "ಹೋಟೆಲ್ ಮತ್ತು ಹೋಮ್‌ಸ್ಟೇ: OpenStreetMap"},
    "src_weather": {"en": "Weather: Open-Meteo", "kn": "ಹವಾಮಾನ: Open-Meteo"},
    "estimates_note": {"en": "Fees, timings and costs are estimates. Please confirm locally "
                             "before you travel.",
                       "kn": "ಶುಲ್ಕ, ಸಮಯ ಮತ್ತು ವೆಚ್ಚಗಳು ಅಂದಾಜು. ಪ್ರಯಾಣಕ್ಕೆ ಮೊದಲು "
                             "ಸ್ಥಳೀಯವಾಗಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."},

    # ---------- Weather and seasons ----------
    "wx_forecast": {"en": "{icon} {words}, {lo}–{hi}°C, {rain}% chance of rain (forecast for {date})",
                    "kn": "{icon} {words}, {lo}–{hi}°C, ಮಳೆಯ ಸಾಧ್ಯತೆ {rain}% ({date} ಮುನ್ಸೂಚನೆ)"},
    "wx_typical": {"en": "{icon} Usually {lo}–{hi}°C, rain on about {rainy} of {days} days "
                         "(same month in {year})",
                   "kn": "{icon} ಸಾಮಾನ್ಯವಾಗಿ {lo}–{hi}°C, {days} ದಿನಗಳಲ್ಲಿ ಸುಮಾರು {rainy} ದಿನ "
                         "ಮಳೆ ({year}ರ ಇದೇ ತಿಂಗಳು)"},
    "sn_falls": {"en": "Waterfalls are at their fullest after the monsoon rains.",
                 "kn": "ಮುಂಗಾರು ಮಳೆಯ ನಂತರ ಜಲಪಾತಗಳು ತುಂಬಿ ಹರಿಯುತ್ತಿರುತ್ತವೆ."},
    "sn_offseason": {"en": "Not the ideal season here. Best months: {months}.",
                     "kn": "ಇದು ಇಲ್ಲಿಗೆ ಸೂಕ್ತ ಋತುವಲ್ಲ. ಉತ್ತಮ ತಿಂಗಳುಗಳು: {months}."},
    "sn_monsoon": {"en": "Monsoon: very heavy rain. Ghat roads can be slippery and landslides "
                         "happen; carry rain gear and drive in daylight.",
                   "kn": "ಮುಂಗಾರು: ಭಾರೀ ಮಳೆ. ಘಟ್ಟದ ರಸ್ತೆಗಳು ಜಾರುತ್ತವೆ, ಭೂಕುಸಿತ ಆಗಬಹುದು; "
                         "ಮಳೆ ಉಡುಪು ಒಯ್ಯಿರಿ ಮತ್ತು ಹಗಲಿನಲ್ಲೇ ಪ್ರಯಾಣಿಸಿ."},
    "sn_sea": {"en": "The sea is rough in the monsoon. Don't swim; stay off the rocks.",
               "kn": "ಮುಂಗಾರಿನಲ್ಲಿ ಸಮುದ್ರ ಪ್ರಕ್ಷುಬ್ಧವಾಗಿರುತ್ತದೆ. ಈಜಬೇಡಿ; ಬಂಡೆಗಳ ಮೇಲೆ "
                     "ಹೋಗಬೇಡಿ."},
    "sn_heat": {"en": "Summer here is very hot (often 38°C+). Visit early morning or late "
                      "afternoon and carry plenty of water.",
                "kn": "ಇಲ್ಲಿ ಬೇಸಿಗೆ ತುಂಬಾ ಬಿಸಿ (ಹೆಚ್ಚಾಗಿ 38°C ಮೇಲೆ). ಬೆಳಿಗ್ಗೆ ಬೇಗ ಅಥವಾ "
                      "ಸಂಜೆ ಭೇಟಿ ನೀಡಿ, ಸಾಕಷ್ಟು ನೀರು ಒಯ್ಯಿರಿ."},
    "sn_trek": {"en": "Treks may be closed or leech-heavy in the monsoon; check with the "
                      "forest office.",
                "kn": "ಮುಂಗಾರಿನಲ್ಲಿ ಚಾರಣ ಮಾರ್ಗಗಳು ಮುಚ್ಚಿರಬಹುದು ಅಥವಾ ಜಿಗಣೆಗಳು "
                      "ಹೆಚ್ಚಿರಬಹುದು; ಅರಣ್ಯ ಕಚೇರಿಯಲ್ಲಿ ವಿಚಾರಿಸಿ."},
}

# Words used inside the data (choices, places, weather)
WORDS_KN = {
    # starting cities
    "Bengaluru": "ಬೆಂಗಳೂರು", "Mysuru": "ಮೈಸೂರು", "Mangaluru": "ಮಂಗಳೂರು", "Hubballi": "ಹುಬ್ಬಳ್ಳಿ",
    # transport and stay
    "Own car / cab": "ಸ್ವಂತ ಕಾರು / ಟ್ಯಾಕ್ಸಿ", "Bus (KSRTC)": "ಬಸ್ (KSRTC)", "Bike": "ಬೈಕ್",
    "Budget": "ಕಡಿಮೆ ವೆಚ್ಚ", "Comfort": "ಆರಾಮದಾಯಕ", "Premium": "ಐಷಾರಾಮಿ",
    # themes
    "Nature": "ಪ್ರಕೃತಿ", "Heritage": "ಪರಂಪರೆ", "Temples": "ದೇವಾಲಯಗಳು",
    "Beaches": "ಕಡಲತೀರಗಳು", "Wildlife": "ವನ್ಯಜೀವಿ", "Food": "ಆಹಾರ",
    # regions
    "Mysuru region": "ಮೈಸೂರು ಪ್ರದೇಶ", "Kodagu": "ಕೊಡಗು", "Malnad": "ಮಲೆನಾಡು",
    "Hampi & North Karnataka": "ಹಂಪಿ ಮತ್ತು ಉತ್ತರ ಕರ್ನಾಟಕ", "Coastal Karnataka": "ಕರಾವಳಿ ಕರ್ನಾಟಕ",
    "Bengaluru region": "ಬೆಂಗಳೂರು ಪ್ರದೇಶ",
    # districts
    "Mandya": "ಮಂಡ್ಯ", "Chamarajanagar": "ಚಾಮರಾಜನಗರ", "Vijayanagara": "ವಿಜಯನಗರ",
    "Bagalkote": "ಬಾಗಲಕೋಟೆ", "Vijayapura": "ವಿಜಯಪುರ", "Bidar": "ಬೀದರ್",
    "Chitradurga": "ಚಿತ್ರದುರ್ಗ", "Hassan": "ಹಾಸನ", "Chikkamagaluru": "ಚಿಕ್ಕಮಗಳೂರು",
    "Shivamogga": "ಶಿವಮೊಗ್ಗ", "Udupi": "ಉಡುಪಿ", "Uttara Kannada": "ಉತ್ತರ ಕನ್ನಡ",
    "Dakshina Kannada": "ದಕ್ಷಿಣ ಕನ್ನಡ", "Chikkaballapura": "ಚಿಕ್ಕಬಳ್ಳಾಪುರ",
    "Bengaluru Urban": "ಬೆಂಗಳೂರು ನಗರ", "Mysuru (near Kushalnagar)": "ಮೈಸೂರು (ಕುಶಾಲನಗರ ಬಳಿ)",
    # costs
    "Travel": "ಪ್ರಯಾಣ", "Stay": "ವಸತಿ", "Entry fees": "ಪ್ರವೇಶ ಶುಲ್ಕ", "Total": "ಒಟ್ಟು",
    # weather words
    "Clear": "ಸ್ಪಷ್ಟ ಆಕಾಶ", "Partly cloudy": "ಭಾಗಶಃ ಮೋಡ", "Foggy": "ಮಂಜು", "Rain": "ಮಳೆ",
    "Showers": "ತುಂತುರು ಮಳೆ", "Thunderstorms": "ಗುಡುಗು ಸಹಿತ ಮಳೆ", "Cloudy": "ಮೋಡ ಕವಿದ",
    # stays
    "Hotel": "ಹೋಟೆಲ್", "Guest house / homestay": "ಅತಿಥಿ ಗೃಹ / ಹೋಮ್‌ಸ್ಟೇ", "Hostel": "ಹಾಸ್ಟೆಲ್",
    "Resort": "ರೆಸಾರ್ಟ್", "Motel": "ಮೋಟೆಲ್",
    # ways to get there
    "🚗 Cab / own car": "🚗 ಟ್ಯಾಕ್ಸಿ / ಸ್ವಂತ ಕಾರು", "🚌 KSRTC bus": "🚌 KSRTC ಬಸ್",
    "🚆 Train": "🚆 ರೈಲು", "🛺 Auto-rickshaw": "🛺 ಆಟೋ ರಿಕ್ಷಾ", "🚶 Walk": "🚶 ನಡಿಗೆ",
    "🏍️ Bike": "🏍️ ಬೈಕ್",
    "Close enough to walk": "ನಡೆದು ಹೋಗುವಷ್ಟು ಹತ್ತಿರ",
    "If it's hot or you're tired": "ಬಿಸಿಲು ಹೆಚ್ಚಿದ್ದರೆ ಅಥವಾ ದಣಿದಿದ್ದರೆ",
    "Easy for short hops within town": "ಊರಿನೊಳಗಿನ ಸಣ್ಣ ಪ್ರಯಾಣಕ್ಕೆ ಸುಲಭ",
    "Most flexible": "ಅತ್ಯಂತ ಅನುಕೂಲಕರ",
    "Cheapest; local buses run often": "ಅತಿ ಕಡಿಮೆ ವೆಚ್ಚ; ಸ್ಥಳೀಯ ಬಸ್ಸುಗಳು ಆಗಾಗ ಇರುತ್ತವೆ",
    "Door to door, stop anywhere on the way": "ನೇರವಾಗಿ ಸ್ಥಳಕ್ಕೆ, ದಾರಿಯಲ್ಲಿ ಎಲ್ಲಿ ಬೇಕಾದರೂ ನಿಲ್ಲಿಸಬಹುದು",
    "Good value; book Airavat/Rajahamsa on ksrtc.in": "ಉತ್ತಮ ಮೌಲ್ಯ; ಐರಾವತ/ರಾಜಹಂಸ ಬಸ್ಸುಗಳನ್ನು ksrtc.inನಲ್ಲಿ ಬುಕ್ ಮಾಡಿ",
    "No railway in Kodagu; reach by road only": "ಕೊಡಗಿನಲ್ಲಿ ರೈಲು ಮಾರ್ಗವಿಲ್ಲ; ರಸ್ತೆಯ ಮೂಲಕ ಮಾತ್ರ",
    "Your choice; ride in daylight on ghat roads": "ನಿಮ್ಮ ಆಯ್ಕೆ; ಘಟ್ಟದ ರಸ್ತೆಗಳಲ್ಲಿ ಹಗಲಿನಲ್ಲಿ ಸವಾರಿ ಮಾಡಿ",
}

MONTHS_KN = ["ಜನವರಿ", "ಫೆಬ್ರವರಿ", "ಮಾರ್ಚ್", "ಏಪ್ರಿಲ್", "ಮೇ", "ಜೂನ್", "ಜುಲೈ", "ಆಗಸ್ಟ್",
             "ಸೆಪ್ಟೆಂಬರ್", "ಅಕ್ಟೋಬರ್", "ನವೆಂಬರ್", "ಡಿಸೆಂಬರ್"]

# "from Bengaluru" etc. in Kannada
CITY_FROM_KN = {"Bengaluru": "ಬೆಂಗಳೂರಿನಿಂದ", "Mysuru": "ಮೈಸೂರಿನಿಂದ",
                "Mangaluru": "ಮಂಗಳೂರಿನಿಂದ", "Hubballi": "ಹುಬ್ಬಳ್ಳಿಯಿಂದ"}

HELPLINE_KN = {
    "🚨 All emergencies (police, fire, ambulance)": "🚨 ಎಲ್ಲಾ ತುರ್ತು ಸೇವೆಗಳು (ಪೊಲೀಸ್, ಅಗ್ನಿಶಾಮಕ, ಆಂಬ್ಯುಲೆನ್ಸ್)",
    "🚑 Ambulance": "🚑 ಆಂಬ್ಯುಲೆನ್ಸ್",
    "👮 Police": "👮 ಪೊಲೀಸ್",
    "🔥 Fire": "🔥 ಅಗ್ನಿಶಾಮಕ",
    "👩 Women's helpline": "👩 ಮಹಿಳಾ ಸಹಾಯವಾಣಿ",
    "🧒 Child helpline": "🧒 ಮಕ್ಕಳ ಸಹಾಯವಾಣಿ",
    "🧳 India Tourist Infoline (24x7, many languages)":
        "🧳 ಭಾರತ ಪ್ರವಾಸಿ ಸಹಾಯವಾಣಿ (ದಿನದ 24 ಗಂಟೆ, ಹಲವು ಭಾಷೆಗಳಲ್ಲಿ)",
}

SEASON_ROWS = {
    "en": [
        ("Coast (Udupi, Gokarna, Mangaluru)", "Oct to Mar", "Jun to Sep: heavy monsoon, rough sea"),
        ("Malnad and Kodagu (Coorg, Chikkamagaluru)", "Sep to Feb", "Jun to Aug: very wet, leeches on treks"),
        ("Waterfalls (Jog, Shivanasamudra, Abbey)", "Jul to Oct", "Mar to May: often low water"),
        ("Hampi and North Karnataka", "Oct to Feb", "Mar to May: very hot, 38°C and above"),
        ("Mysuru and Bengaluru", "Most of the year", "Dasara in Sep/Oct is busy but magical"),
        ("Wildlife parks (Bandipur, Kabini)", "Oct to May", "Some safaris limited in the monsoon"),
    ],
    "kn": [
        ("ಕರಾವಳಿ (ಉಡುಪಿ, ಗೋಕರ್ಣ, ಮಂಗಳೂರು)", "ಅಕ್ಟೋಬರ್–ಮಾರ್ಚ್", "ಜೂನ್–ಸೆಪ್ಟೆಂಬರ್: ಭಾರೀ ಮುಂಗಾರು, ಪ್ರಕ್ಷುಬ್ಧ ಸಮುದ್ರ"),
        ("ಮಲೆನಾಡು ಮತ್ತು ಕೊಡಗು (ಚಿಕ್ಕಮಗಳೂರು)", "ಸೆಪ್ಟೆಂಬರ್–ಫೆಬ್ರವರಿ", "ಜೂನ್–ಆಗಸ್ಟ್: ತುಂಬಾ ಮಳೆ, ಚಾರಣದಲ್ಲಿ ಜಿಗಣೆಗಳು"),
        ("ಜಲಪಾತಗಳು (ಜೋಗ, ಶಿವನಸಮುದ್ರ, ಅಬ್ಬೆ)", "ಜುಲೈ–ಅಕ್ಟೋಬರ್", "ಮಾರ್ಚ್–ಮೇ: ಸಾಮಾನ್ಯವಾಗಿ ನೀರು ಕಡಿಮೆ"),
        ("ಹಂಪಿ ಮತ್ತು ಉತ್ತರ ಕರ್ನಾಟಕ", "ಅಕ್ಟೋಬರ್–ಫೆಬ್ರವರಿ", "ಮಾರ್ಚ್–ಮೇ: ತುಂಬಾ ಬಿಸಿ, 38°C ಮೇಲೆ"),
        ("ಮೈಸೂರು ಮತ್ತು ಬೆಂಗಳೂರು", "ವರ್ಷದ ಬಹುತೇಕ ಸಮಯ", "ಸೆಪ್ಟೆಂಬರ್/ಅಕ್ಟೋಬರ್‌ನ ದಸರಾ: ಜನಸಂದಣಿ, ಆದರೆ ಅದ್ಭುತ"),
        ("ವನ್ಯಜೀವಿ ಉದ್ಯಾನಗಳು (ಬಂಡೀಪುರ, ಕಬಿನಿ)", "ಅಕ್ಟೋಬರ್–ಮೇ", "ಮುಂಗಾರಿನಲ್ಲಿ ಕೆಲವು ಸಫಾರಿಗಳು ಸೀಮಿತ"),
    ],
}


# One-tap examples on the home page. Their settings are ready-made,
# so they plan instantly without waiting for the AI.
EXAMPLES = [
    ({"en": "3 days from Mysuru: wildlife and nature",
      "kn": "ಮೈಸೂರಿನಿಂದ 3 ದಿನ: ಕಾಡು ಮತ್ತು ಪ್ರಕೃತಿ"},
     {"days": 3, "start_city": "Mysuru", "interests": ["Wildlife", "Nature"], "budget": 15000}),
    ({"en": "A temple weekend from Bengaluru, ₹8,000",
      "kn": "ಬೆಂಗಳೂರಿನಿಂದ ವಾರಾಂತ್ಯದ ದೇವಾಲಯ ಪ್ರವಾಸ, ₹8,000"},
     {"days": 2, "start_city": "Bengaluru", "interests": ["Temples", "Heritage"], "budget": 8000}),
    ({"en": "4 days on the coast from Mangaluru",
      "kn": "ಮಂಗಳೂರಿನಿಂದ 4 ದಿನ ಕರಾವಳಿ ಪ್ರವಾಸ"},
     {"days": 4, "start_city": "Mangaluru", "interests": ["Beaches", "Food", "Temples"],
      "budget": 20000}),
]


def lang():
    """'kn' or 'en': the language the visitor chose."""
    try:
        return st.session_state.get("ui_lang", "en")
    except Exception:
        return "en"


def is_kn():
    return lang() == "kn"


def t(key, **values):
    """The text for `key` in the chosen language, with {values} filled in."""
    text = STRINGS[key].get(lang()) or STRINGS[key]["en"]
    return text.format(**values) if values else text


def w(word):
    """Translate a word from the data (a city, theme, district...) when in Kannada."""
    if not is_kn() or not word:
        return word
    if word in WORDS_KN:
        return WORDS_KN[word]
    if " / " in word:  # e.g. "Chamarajanagar / Mandya"
        return " / ".join(WORDS_KN.get(part, part) for part in word.split(" / "))
    if word.startswith("Nearest station: "):
        station = word.split(": ", 1)[1].split(", then")[0]
        return f"ಹತ್ತಿರದ ರೈಲು ನಿಲ್ದಾಣ: {station}, ಅಲ್ಲಿಂದ ಟ್ಯಾಕ್ಸಿ"
    return word


def pf(place, field):
    """A place's text field (famous_for, local_food) in the chosen language."""
    if is_kn() and place.get(f"{field}_kn"):
        return place[f"{field}_kn"]
    return place[field]


def month_name(month_number):
    """Month name in the chosen language (1 = January)."""
    import calendar
    return MONTHS_KN[month_number - 1] if is_kn() else calendar.month_name[month_number]


def month_short(month_number):
    import calendar
    return MONTHS_KN[month_number - 1] if is_kn() else calendar.month_abbr[month_number]


def time_text(text):
    """'~1.5 h' -> '~1.5 ಗಂಟೆ', and similar small units, when in Kannada."""
    if not is_kn():
        return text
    return (text.replace(" h", " ಗಂಟೆ").replace("Free", "ಉಚಿತ").replace("(fuel)", "(ಇಂಧನ)"))
