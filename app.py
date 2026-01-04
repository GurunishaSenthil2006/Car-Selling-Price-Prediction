import streamlit as st # pyright: ignore[reportMissingImports]
import pickle
import numpy as np
import datetime

# Page setup
st.set_page_config(
    page_title="Car Price Prediction",
    layout="wide"
)

# Load model
model = pickle.load(open("car_price_model.pkl", "rb"))

st.title("🚗 Car Selling Price Prediction")
st.markdown("Predict used car selling price using Machine Learning")
st.markdown("---")

current_year = datetime.datetime.now().year

# ================= INPUT SECTION =================
left_col, right_col = st.columns(2)

# ---------- LEFT COLUMN (4 Inputs) ----------
with left_col:
    st.subheader("Car Details")

    present_price = st.number_input(
        "Showroom Price (in lakhs)", min_value=0.0, step=0.1
    )

    kms_driven = st.number_input(
        "Kilometers Driven", min_value=0, step=1000
    )

    purchase_year = st.number_input(
        "Purchase Year", min_value=1995, max_value=current_year, step=1
    )

    owner = st.selectbox(
        "Number of Previous Owners", [0, 1, 3]
    )

# ---------- RIGHT COLUMN (4 Inputs + Predict) ----------
with right_col:
    st.subheader("Additional Information")

    fuel_type = st.selectbox(
        "Fuel Type", ["Petrol", "Diesel", "CNG"]
    )

    seller_type = st.selectbox(
        "Seller Type", ["Dealer", "Individual"]
    )

    transmission = st.selectbox(
        "Transmission", ["Manual", "Automatic"]
    )

    seller_location = st.selectbox(   # 🔹 EXTRA INPUT (UI balance)
        "Seller Location", ["Urban", "Rural"]
    )


# ================= OUTPUT SECTION (CENTERED) =================
st.markdown("---")
predict = st.button("🔍 Predict Selling Price")

if predict:
    # Calculate car age
    car_age = current_year - purchase_year

    # Encode categorical inputs (same as training)
    fuel_diesel = 1 if fuel_type == "Diesel" else 0
    fuel_petrol = 1 if fuel_type == "Petrol" else 0

    seller_individual = 1 if seller_type == "Individual" else 0
    transmission_manual = 1 if transmission == "Manual" else 0

    input_data = np.array([[
        present_price,
        kms_driven,
        owner,
        car_age,
        fuel_diesel,
        fuel_petrol,
        seller_individual,
        transmission_manual
    ]])

    prediction = model.predict(input_data)[0]

    # Center output
    center_col = st.columns([1, 2, 1])[1]
    with center_col:
        st.markdown("## 💰 Predicted Selling Price")
        st.success(f"₹ {prediction:.2f} lakhs")
