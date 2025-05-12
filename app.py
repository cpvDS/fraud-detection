import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    return pd.read_csv("full_fraud_dataset.csv", parse_dates=["login_time"])

df = load_data()
st.title("Fraud Detection Demo App")

#@st.cache_data
def load_travel_data():
    travel_df = pd.read_csv("user_travel_notices.csv", parse_dates=["start_date", "end_date"])
    return travel_df
travel_df = load_travel_data()


if st.checkbox("Show raw data"):   
    st.dataframe(df, use_container_width=True, height=200)

# Apply simple rule-based fraud checks
def apply_rules(row):
    if row["amount"] > 10000:
        return True
    if not is_travel_approved(row["user_id"], row["country"], pd.to_datetime(row["login_time"]), travel_df):
        if row["country"] in ["Nigeria", "Russia", "Iran"]:  # only block risky countries
            return True

 
    if row["is_new_device"] == 1 and row["num_failed_logins"] > 2:
        return True
    if pd.to_datetime(row["login_time"]).hour < 5:
        return True
    if row["txn_velocity_last_hour"] > 5:
        return True
    return False

def is_travel_approved(user_id, country, txn_date, travel_df):
    try:
        travel_record = travel_df[travel_df['user_id'] == int(user_id)]
        if not travel_record.empty:
            for _, row in travel_record.iterrows():
                if (row['to_country'] == country and 
                    row['start_date'] <= txn_date <= row['end_date']):
                    return True
    except:
        pass
    return False

df["flagged_by_rules"] = df.apply(apply_rules, axis=1)

flagged = df[df["flagged_by_rules"] == True]
frauds_only = flagged[flagged["is_fraud"] == 1]
st.subheader("🛑 Actual Frauds Flagged by Rules")
st.write(frauds_only[["transaction_id", "user_id", "amount", "country", "login_time", "device_type", "ip_address","txn_velocity_last_hour","transaction_type","num_failed_logins","risk_score","is_high_risk_merchant"]])

st.metric("Total Transactions", len(df))
st.metric("Flagged by Rules", len(flagged))
st.metric("Actual Frauds (is_fraud = 1)", df['is_fraud'].sum())

true_positives = flagged[flagged["is_fraud"] == 1]
false_positives = flagged[flagged["is_fraud"] == 0]

st.metric("True Positives (Fraud caught)", len(true_positives))
st.metric("False Positives (Flagged but not fraud)", len(false_positives))
st.metric("Precision (%)", round((len(true_positives) / len(flagged)) * 100, 2))
st.metric("Recall (%)", round((len(true_positives) / df["is_fraud"].sum()) * 100, 2))

