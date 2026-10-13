import streamlit as st

st.set_page_config(page_title="Karnataka Travel Planner", page_icon="🧭")

st.title("Karnataka AI Travel Planner")
st.write("Plan your trip in English or ಕನ್ನಡ")

days = st.slider("How many days?", 1, 10, 3)
budget = st.number_input("Budget (₹)", min_value=1000, value=15000, step=1000)
interests = st.multiselect(
    "What do you enjoy?",
    ["Nature", "Heritage", "Temples", "Beaches", "Wildlife", "Food"]
)

if st.button("Plan my trip"):
    st.success(f"Planning a {days}-day trip with ₹{budget} for: {', '.join(interests)}")