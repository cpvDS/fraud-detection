import streamlit as st

def login_required():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Hide sidebar
        st.markdown("""
            <style>
                [data-testid="stSidebar"] { display: none; }
            </style>
        """, unsafe_allow_html=True)

        st.title("Login Required")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            expected_user = st.secrets["auth"]["username"]
            expected_pass = st.secrets["auth"]["password"]
            if username == expected_user and password == expected_pass:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect credentials")
        st.stop()
