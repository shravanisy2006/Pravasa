import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Karnataka Travel Planner", page_icon="🧭")

# Load the destination dataset
with open("destinations.json", encoding="utf-8") as f:
    destinations = json.load(f)

st.title("Karnataka AI Travel Planner")
st.write("Plan your trip in English or ಕನ್ನಡ")
st.caption(f"{len(destinations)} verified destinations across Karnataka")

days = st.slider("How many days?", 1, 10, 3)
budget = st.number_input("Budget (₹)", min_value=1000, value=15000, step=1000)
interests = st.multiselect(
    "What do you enjoy?",
    ["Nature", "Heritage", "Temples", "Beaches", "Wildlife", "Food"]
)

if st.button("Plan my trip"):
    st.success(f"Planning a {days}-day trip with ₹{budget} for: {', '.join(interests)}")

# Show all destinations on a map
st.subheader("All destinations")
df = pd.DataFrame(destinations)
st.map(df, latitude="lat", longitude="lon")

with st.expander("See the full list"):
    st.dataframe(df[["name", "name_kn", "district", "categories", "famous_for"]])