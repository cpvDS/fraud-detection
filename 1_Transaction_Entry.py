import streamlit as st
import pandas as pd
from datetime import datetime

from auth import login_required
login_required()


st.set_page_config(layout="wide")
st.title("Transaction Entry")

# ---------------------------
# Load travel notices
#@st.cache_data
def load_travel_data():
    return pd.read_csv("user_travel_notices.csv", dtype={"user_id": int}, parse_dates=["start_date", "end_date"])

travel_df = load_travel_data()

# ---------------------------
# Travel approval logic
def is_travel_approved(user_id, country, txn_date, travel_df):
    try:
        user_id = int(str(user_id).replace(",", "").strip())
        country = country.strip().lower()

        travel_record = travel_df[travel_df['user_id'] == user_id]

        if not travel_record.empty:
            for _, row in travel_record.iterrows():
                if (
                    row['to_country'].strip().lower() == country and
                    row['start_date'] <= txn_date <= row['end_date']
                ):
                    return True
    except Exception as e:
        st.warning(f"Travel check error: {e}")
    return False

# ---------------------------
# Fraud rule logic
def apply_rules(tx):
    if tx["amount"] > 10000:
        return True
    if not is_travel_approved(tx["user_id"], tx["country"], pd.to_datetime(tx["login_time"]), travel_df):
        if tx["country"] in ["Nigeria", "Russia", "Iran"]:
            return True
    if tx["is_new_device"] and tx["num_failed_logins"] > 2:
        return True
    if pd.to_datetime(tx["login_time"]).hour < 5:
        return True
    if tx["txn_velocity_last_hour"] > 5:
        return True
    return False

# ---------------------------
# Manual transaction form
with st.form("manual_entry_form"):
    st.subheader("Enter Transaction Details")

    user_id = st.text_input("User ID", "1234")
    amount = st.number_input("Amount", min_value=1.0, max_value=20000.0, value=100.0)
    country = st.selectbox("Country", options=["Kuwait", "UAE", "Saudi Arabia", "Russia", "Nigeria", "Iran"])
    device_type = st.selectbox("Device Type", options=["Mobile", "Desktop", "Tablet"])
    login_hour = st.slider("Login Hour (24h)", 0, 23, 12)
    txn_velocity = st.slider("Transactions Last Hour", 0, 10, 1)
    failed_logins = st.slider("Failed Logins", 0, 10, 0)
    is_new_device = st.checkbox("New Device?", value=False)

    submitted = st.form_submit_button("Check for Fraud")

# ---------------------------
# Result
if submitted:
    #login_time = pd.to_datetime(f"2025-06-05 {login_hour}:00:00")  # fixed sample date
    now = datetime.now()
    login_time = datetime(now.year, now.month, now.day, login_hour)
    tx_data = {
        "user_id": user_id,
        "amount": amount,
        "country": country,
        "device_type": device_type,
        "login_time": login_time,
        "txn_velocity_last_hour": txn_velocity,
        "num_failed_logins": failed_logins,
        "is_new_device": int(is_new_device)
    }

    # Show transaction details for confirmation
    #st.write("🔍 Transaction Info", tx_data)

    # Check for travel match info
    if is_travel_approved(tx_data["user_id"], tx_data["country"], tx_data["login_time"], travel_df):
        st.info(" Travel notice match found — allowed.")

    # Apply fraud rules
    is_fraud = apply_rules(tx_data)

    if is_fraud:
        st.error("This transaction is flagged as **POTENTIAL FRAUD**.")
    else:
        st.success("This transaction appears **legitimate**.")
