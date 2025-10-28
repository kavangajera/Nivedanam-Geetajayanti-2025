import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup (no user login required)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Geetajayanti Celebration nivedanam").sheet1  # Replace with your sheet name

# Streamlit UI
st.set_page_config(page_title="Simple Form", page_icon="📝")
st.title("📝 Submit Your Response")

with st.form("user_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    feedback = st.text_area("Your Feedback")
    submitted = st.form_submit_button("Submit")

if submitted:
    if name and email and feedback:
        sheet.append_row([name, email, feedback])
        st.success("✅ Your response has been recorded!")
    else:
        st.warning("⚠️ Please fill all fields before submitting.")
