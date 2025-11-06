# 🧠 Job Application Tracker AI

An intelligent Gmail + Google Sheets automation tool that tracks all your job applications automatically.

This project fetches job-related emails from Gmail, extracts company and role information using OpenAI GPT, and logs them neatly into a Google Sheet for organized tracking.

---

## 🚀 Features

- 📥 Automatically scans Gmail for:
  - “Thank you for applying”
  - “Application received”
  - “We are reviewing your application”
  - and similar keywords
- 🧠 Extracts company name, job role, and source using GPT
- 🧾 Logs structured entries to Google Sheets
- 🧹 Prevents duplicate entries using Gmail message IDs
- ⚡ Batches updates to stay within Google API limits
- 🔒 Secrets managed safely via `.env` (excluded from Git)

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Email Parsing | Gmail API (OAuth2) |
| Sheet Logging | Google Sheets API (Service Account) |
| AI Extraction | OpenAI GPT (gpt-4o-mini or gpt-3.5-turbo) |
| Language | Python 3.10+ |
| Auth | OAuth2 + Service Account JSON |
| Environment | Conda or venv |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/MaheenRH/job-application-tracker-ai.git
cd job-application-tracker-ai

### 2️⃣ Create and activate a virtual environment
conda create -n job_application python=3.10 -y
conda activate job_application

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your environment variables in .env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GMAIL_CREDENTIALS_PATH=path/to/gmail-oauth-client.json
GOOGLE_SHEET_ID=your_google_sheet_id

5️⃣ Run the script
python gmail_parser.py

📊 Example Output (Google Sheet)
Date	Company	Role	Source	Message ID
2025-11-05	Propio	Translation AI Engineer	Email	19a52022785443b6
2025-11-05	Twilio	Software Engineer	LinkedIn	19a485ad74e46580

🛡️ Security

Sensitive credentials are never stored in Git.

.gitignore ensures .env, .json, and token files remain local.

Each API key and OAuth token must be created via your own accounts.

⭐ Contribute

If you'd like to improve this project (UI dashboard, email filters, analytics), feel free to open an issue or submit a PR.
