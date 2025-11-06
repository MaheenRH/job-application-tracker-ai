import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Connect to Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
client = gspread.authorize(creds)

# Open the specific sheet tab named "Applications"
sheet = client.open_by_key(SHEET_ID).worksheet("applications")

# Add a test row
today = datetime.now().strftime("%Y-%m-%d")
test_data = [today, "Test Company", "Test Role", "Script Connection Test"]
sheet.append_row(test_data)

print("Successfully connected and added test row to Google Sheet!")
