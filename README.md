### Why I Chose This Project

While applying for jobs, I realized how difficult it was to keep track of every single application. I would apply on different platforms — LinkedIn, company websites, Indeed, etc. and each confirmation email would get buried in my Gmail inbox. I tried writing everything down manually in a spreadsheet, but it quickly became overwhelming and time-consuming.

That’s when I decided to build something that could do this automatically for me. A small AI system that reads my Gmail, detects job application emails, extracts key information like company name, role, and source, and saves everything neatly into a Google Sheet — so I could focus on preparing for interviews instead of tracking applications.

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

## 📊 Example Google Sheet Output

<img width="1337" height="396" alt="Screenshot 2025-11-06 at 4 23 41 PM" src="https://github.com/user-attachments/assets/4e416168-659f-437d-aa66-ed2d7b2073de" />

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/MaheenRH/job-application-tracker-ai.git
cd job-application-tracker-ai



