import streamlit as st
import pandas as pd
from datetime import date
from auth import login_required
login_required()

st.set_page_config(layout="wide")
st.title("Add Travel Notice")

#stre@st.cache_data
def load_travel_data():
    travel_df = pd.read_csv("user_travel_notices.csv", parse_dates=["start_date", "end_date"])
    return travel_df

travel_df = load_travel_data()

# Editable grid
if st.checkbox("Edit travel notices"):
    edited_df = st.data_editor(
        travel_df,
        use_container_width=True,
        num_rows="dynamic",
        height=300,
        key="editable_travel_table"
    )

    if st.button("Save Changes"):
        edited_df.to_csv("user_travel_notices.csv", index=False)
        st.success("Changes saved!")
        st.rerun()
          # <- this refreshes the app with new data


# Manual form to add a new travel notice
st.subheader("➕ Add New Travel Notice")
with st.form("travel_notice_form"):
    user_id = st.text_input("User ID")
    to_country = st.selectbox("Destination Country", ["Nigeria", "UK", "India", "UAE", "USA"])
    start_date = st.date_input("Start Date", date.today())
    end_date = st.date_input("End Date", date.today())

    submitted = st.form_submit_button("Save Notice")

if submitted:
    new_notice = {
        "user_id": int(user_id.replace(",", "")),
        "to_country": to_country,
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        travel_df = pd.read_csv("user_travel_notices.csv")
    except FileNotFoundError:
        travel_df = pd.DataFrame(columns=new_notice.keys())

    travel_df = travel_df.append(new_notice, ignore_index=True)
    travel_df.to_csv("user_travel_notices.csv", index=False)
    st.success("Travel notice saved!")
