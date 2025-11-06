# ============================================
# extract_job_info.py
# ============================================
import os
import time
import json
import re
import openai
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# --------------------------------------------
# Extract company, role, and source from email
# --------------------------------------------
def extract_job_info(subject, body, retries=3):
    """
    Use GPT to extract company, role, and source from email content.
    Automatically retries on rate-limit errors and skips incomplete results.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    You are an AI that extracts key job application details from emails.

    From the following email, extract:
    - company: organization or employer name
    - role: the title or job position applied for
    - source: LinkedIn, Indeed, Workday, or Email if unspecified

    Return ONLY JSON like this:
    {{
      "company": "Google",
      "role": "Machine Learning Engineer",
      "source": "LinkedIn"
    }}

    Email content:
    Subject: {subject}
    Body: {body[:1800]}
    """

    for attempt in range(retries):
        try:
            response = llm.invoke([HumanMessage(content=prompt)]).content.strip()
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if not match:
                raise ValueError("No JSON found in LLM response")

            data = json.loads(match.group())
            company = data.get("company", "").strip()
            role = data.get("role", "").strip()
            source = data.get("source", "").strip() or "Email"

            # ✅ Skip incomplete or placeholder values
            if company and role and company.lower() != "n/a" and role.lower() != "n/a":
                return company, role, source
            else:
                return None, None, None

        except openai.RateLimitError:
            wait = (attempt + 1) * 20
            print(f"⏳ Rate limit hit. Waiting {wait}s before retry ({attempt+1}/{retries})...")
            time.sleep(wait)

        except Exception as e:
            print(f"⚠️ GPT extraction failed: {e}")
            break

    return None, None, None
