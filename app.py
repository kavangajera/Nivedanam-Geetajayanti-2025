import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Nivedanam Form", page_icon="🕉️")

# Google Sheets setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from Streamlit secrets
service_account_info = st.secrets["google_service_account"]
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
client = gspread.authorize(creds)

# Access your sheet by URL (safer than by name)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1abcD3FgHiJklMnOPQRstuVWxyz1234567890/edit#gid=0").sheet1

# Streamlit form
st.title("🪔 Geetajayanti Celebration - Nivedanam Form")

with st.form("nivedanam_form"):
    name = st.text_input("Full Name")
    gotra = st.text_input("Gotra")
    nivedanam = st.text_area("Your Nivedanam")
    submitted = st.form_submit_button("Submit")

if submitted:
    if name and gotra and nivedanam:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, name, gotra, nivedanam])
        st.success("✅ Your Nivedanam has been recorded successfully!")
    else:
        st.warning("⚠️ Please fill in all fields.")
