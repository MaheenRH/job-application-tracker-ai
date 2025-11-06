import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SVC_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

creds = Credentials.from_service_account_file(
    SVC_CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet("applications")

# ⚠️ Clears everything but keeps header
sheet.batch_clear(["A2:E1000"])
print("✅ Cleared all old rows (kept headers).")

