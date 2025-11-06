import os
import gspread
from google.oauth2.service_account import Credentials as ServiceCreds
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SERVICE_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceCreds.from_service_account_file(SERVICE_PATH, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet("applications")

sheet.append_row([datetime.now().strftime("%Y-%m-%d"), "✅ Test Company", "AI Engineer", "Direct Test", "99999"])
print("✅ Successfully wrote test row to Google Sheet!")
