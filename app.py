import calendar
import datetime
import json

import pandas as pd
import streamlit as st

from planner import START_CITIES, STAY_STYLES, TRANSPORT, plan_trip

st.set_page_config(page_title="Pravasa - Karnataka Travel Planner", page_icon="🧭")

# Load the destination dataset
with open("destinations.json", encoding="utf-8") as f:
    destinations = json.load(f)

st.title("Pravasa: Karnataka AI Travel Planner")
st.write("Plan your trip in English or ಕನ್ನಡ")
st.caption(f"{len(destinations)} verified destinations across Karnataka")

# ---------- Trip inputs ----------
col1, col2 = st.columns(2)
with col1:
    start_city = st.selectbox("Starting from", list(START_CITIES.keys()))
    days = st.slider("How many days?", 1, 10, 3)
    transport = st.selectbox("How will you travel?", list(TRANSPORT.keys()))
with col2:
    month_names = list(calendar.month_name)[1:]  # January ... December
    this_month = datetime.date.today().month
    month_name = st.selectbox("Travel month", month_names, index=this_month - 1)
    budget = st.number_input("Budget (₹)", min_value=1000, value=15000, step=1000)
    stay_style = st.selectbox("Stay style", list(STAY_STYLES.keys()))

interests = st.multiselect(
    "What do you enjoy?",
    ["Nature", "Heritage", "Temples", "Beaches", "Wildlife", "Food"],
)

# ---------- Build the plan ----------
if st.button("Plan my trip", type="primary"):
    if not interests:
        st.warning("Pick at least one interest so I know what to plan for.")
        st.stop()

    month = month_names.index(month_name) + 1
    result = plan_trip(destinations, days, interests, start_city, month,
                       transport, stay_style)
    costs = result["costs"]

    # Summary
    st.subheader(f"Your {days}-day trip from {start_city}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated cost", f"₹{costs['Total']:,}")
    m2.metric("Your budget", f"₹{budget:,}")
    m3.metric("Total distance", f"{result['total_km']:,} km")

    if costs["Total"] > budget:
        st.warning(
            f"This plan is about ₹{costs['Total'] - budget:,} over budget. "
            "Try fewer days, a cheaper stay style, or travelling by bus."
        )
    else:
        st.success(f"Within budget, with about ₹{budget - costs['Total']:,} to spare.")

    # One tab per day
    tabs = st.tabs([f"Day {d['day']}" for d in result["days"]])
    for tab, day in zip(tabs, result["days"]):
        with tab:
            if not day["stops"]:
                st.info("A free day to relax, shop or revisit a favourite spot.")
            for stop in day["stops"]:
                place = stop["place"]
                st.markdown(f"### {place['name']}")
                st.caption(f"{place['name_kn']} · {place['district']}")
                if stop["long_travel_day"]:
                    st.warning(
                        f"Long travel day: about {stop['travel_km']} km "
                        f"(~{stop['travel_hours']} hours) to get here."
                    )
                else:
                    st.write(f"🚗 {stop['travel_km']} km · about {stop['travel_hours']} hours to get here")
                st.write(place["famous_for"])
                fee = place.get("entry_fee_inr_approx")
                fee_text = "Free" if fee == 0 else (f"about ₹{fee}" if fee else place.get("fee_note", "Check locally"))
                st.write(
                    f"⏱️ Spend about {place['visit_hours']} hours · "
                    f"🎟️ Entry: {fee_text} · 🕘 {place['timings']}"
                )
                st.write(f"🍛 Try: {place['local_food']}")
                st.divider()

    st.caption(
        f"Return journey to {start_city}: about {result['return_km']} km "
        "(included in the travel cost)."
    )

    # Cost breakdown
    st.subheader("Cost breakdown (approximate)")
    breakdown = {k: v for k, v in costs.items() if k != "Total"}
    st.bar_chart(pd.Series(breakdown, name="₹"))

# ---------- All destinations ----------
with st.expander("See all destinations on a map"):
    df = pd.DataFrame(destinations)
    st.map(df, latitude="lat", longitude="lon")
    st.dataframe(df[["name", "name_kn", "district", "categories", "famous_for"]])