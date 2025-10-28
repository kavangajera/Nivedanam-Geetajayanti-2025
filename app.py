import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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

# Access your spreadsheet by URL
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1yUHh1v77JFwi92kzw2d9RxQiuFWywJAH7ru4acCbACw/edit?gid=0#gid=0")

# Streamlit form
st.title("🪔 Geetajayanti Celebration - Bhavferi Entry Form")

with st.form("bhavferi_form"):
    # Yuvakendra dropdown
    yuvakendra_options = [
        "Select Yuvakendra",
        "Yuvakendra A",
        "Yuvakendra B", 
        "Yuvakendra C",
        "Yuvakendra D"
    ]
    yuvakendra = st.selectbox("Yuvakendra", yuvakendra_options)
    
    # Sanchalak Name
    sanchalak_name = st.text_input("Sanchalak Name")
    
    # Number of new yuvans
    number_of_new_yuvans = st.number_input("Number of new yuvans", min_value=0, value=0, step=1)
    
    # Date of bhavferi (default to today's date in dd/mm/yyyy format)
    date_of_bhavferi = st.date_input("Date of bhavferi", value=datetime.today())
    
    submitted = st.form_submit_button("Submit")

if submitted:
    if sanchalak_name and yuvakendra != "Select Yuvakendra" and number_of_new_yuvans >= 0:
        try:
            # Try to access the sheet for the selected Yuvakendra, create if it doesn't exist
            try:
                sheet = spreadsheet.worksheet(yuvakendra)
            except gspread.exceptions.WorksheetNotFound:
                # Create a new worksheet for this Yuvakendra
                sheet = spreadsheet.add_worksheet(title=yuvakendra, rows="100", cols="20")
                # Add headers to the new sheet
                sheet.append_row(["Sanchalak Name", "Number of new yuvans", "Date of bhavferi"])
            
            # Format date as dd/mm/yyyy
            formatted_date = date_of_bhavferi.strftime("%d/%m/%Y")
            
            # Record the entry in the appropriate sheet
            sheet.append_row([sanchalak_name, number_of_new_yuvans, formatted_date])
            st.success(f"✅ Your Bhavferi entry has been recorded successfully in {yuvakendra} sheet!")
        except Exception as e:
            st.error(f"❌ An error occurred while saving the entry: {str(e)}")
    else:
        st.warning("⚠️ Please fill in all fields correctly.")
