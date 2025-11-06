# ============================================
# gmail_parser.py
# ============================================
from __future__ import print_function
import os
import base64
import re
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import gspread
from google.oauth2.service_account import Credentials as ServiceCreds
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Import GPT extractor
from extract_job_info import extract_job_info

# --------------------------------------------
# Load environment
# --------------------------------------------
load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SVC_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH")

# --------------------------------------------
# Connect to Google Sheets
# --------------------------------------------
sheet_scope = ["https://www.googleapis.com/auth/spreadsheets"]
svc_creds = ServiceCreds.from_service_account_file(SVC_CREDENTIALS_PATH, scopes=sheet_scope)
client = gspread.authorize(svc_creds)
sheet = client.open_by_key(SHEET_ID).worksheet("applications")  # case-sensitive!

# --------------------------------------------
# Gmail Scopes
# --------------------------------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service():
    """Authenticate with Gmail API (using OAuth)."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, SCOPES)
            # ✅ Properly indented local server auth
            creds = flow.run_local_server(port=0, prompt='consent')

        # Save new token for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    print("✅ Gmail connection established.")
    return service


# --------------------------------------------
# Helper: clean HTML & text in emails
# --------------------------------------------
def clean_email_body(body):
    """Convert HTML to plain text and remove extra spaces."""
    try:
        body = BeautifulSoup(body, "html.parser").get_text()
    except Exception:
        pass
    body = re.sub(r"\s+", " ", body).strip()
    return body


# --------------------------------------------
# Prevent duplicate Gmail IDs
# --------------------------------------------
def get_existing_ids():
    """Cache message IDs already stored in sheet."""
    try:
        rows = sheet.get_all_values()
        return {r[4].strip() for r in rows[1:] if len(r) > 4 and r[4].strip()}
    except Exception:
        return set()


# --------------------------------------------
# Main: fetch and log job application emails
# --------------------------------------------
def fetch_applications():
    """Fetch recent job application emails and log to sheet."""
    service = get_gmail_service()
    existing_ids = get_existing_ids()

    two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y/%m/%d")
    query = (
        f'("application received" OR "thank you for applying" OR '
        f'"we received your application" OR "your application to" OR '
        f'"we are reviewing your application" OR "interview" OR "hiring team") '
        f'after:{two_days_ago}'
    )

    print(f"🔍 Searching Gmail for messages since {two_days_ago}...")
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    print(f"📬 Found {len(messages)} messages matching query: {query}")

    if not messages:
        print("No new job application emails found.")
        return

    batch_rows = []
    for msg in messages:
        msg_id = msg["id"]
        if msg_id in existing_ids:
            continue

        msg_data = service.users().messages().get(userId="me", id=msg_id).execute()
        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")

        # Extract body
        parts = msg_data["payload"].get("parts", [])
        body_data = None
        for part in parts:
            if part["mimeType"] == "text/plain":
                body_data = part["body"].get("data")
                break

        if not body_data:
            continue

        body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
        body = clean_email_body(body)

        # Extract job info with GPT
        company, role, source = extract_job_info(subject, body)

        if company and role:
            batch_rows.append([
                datetime.now().strftime("%Y-%m-%d"),
                company,
                role,
                source,
                msg_id
            ])
            print(f"✅ Logged (pending batch): {company} — {role} ({source})")
        else:
            print(f"⚠️ Skipping {msg_id}: incomplete extraction.")

    # Batch update (faster + quota safe)
    if batch_rows:
        sheet.append_rows(batch_rows, value_input_option="RAW")
        print(f"✅ Logged {len(batch_rows)} new rows to Google Sheet.")
    else:
        print("No new rows to add.")

    print("✨ Gmail parsing completed.")


# --------------------------------------------
# Run script
# --------------------------------------------
if __name__ == "__main__":
    fetch_applications()
