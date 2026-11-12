
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your environment settings."
    )

# Connect to Gemini
# One SDK attempt prevents long automatic retry delays.
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=90000,
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)

# Select Gemini model
MODEL = "gemini-3.5-flash-lite"


def explain_report(report_text, language="English"):

    if not report_text.strip():
        raise ValueError("Report text is empty.")

    if language not in ["English", "Hindi", "Both"]:
        raise ValueError("Unsupported language.")

    prompt = f"""
You are MediExplain, an AI Report Simplification Assistant.

Your job is to explain different types of reports
in simple and understandable language.

The report may be:
- Medical
- Educational
- Financial
- Scientific
- Business
- General

IMPORTANT RULES:

1. Use simple language.
2. Preserve all original numbers and units.
3. Never invent missing information.
4. Explain difficult technical terms.
5. Clearly mention uncertain OCR readings.
6. Do not create unnecessary fear.
7. Do not make unsupported conclusions.
8. For medical reports, do not diagnose diseases
   or prescribe medicines.
9. For financial reports, do not give personal
   investment advice.
10. Mention when professional advice is needed.
11. Protect personal information in the report.

OUTPUT LANGUAGE: {language}

If the language is Both, provide the complete
explanation in English first and Hindi second.

Use these sections:

1. Simple Report Summary
2. Important Findings
3. Values and Data Explained
4. Difficult Terms Explained
5. Questions to Ask a Relevant Professional
6. Important Disclaimer

REPORT TEXT:

{report_text[:40000]}
"""

    config = types.GenerateContentConfig(
        system_instruction=(
            "You are a careful and helpful report "
            "simplification assistant. Explain facts "
            "accurately without inventing information."
        ),
        temperature=0.2
    )

    try:
        print("Sending request to Gemini...")

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=config
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        print("Gemini explanation received successfully.")
        return response.text

    except Exception as error:
        error_code = getattr(error, "code", None)
        error_message = str(error).lower()

        # Handle daily free-tier quota exhaustion
        if (
            error_code == 429
            and (
                "requests per day limit exceeded" in error_message
                or "generaterequestsperdayperprojectpermodel-freetier"
                in error_message
            )
        ):
            raise RuntimeError(
                "Gemini daily free-tier quota exhausted. "
                "Please wait for the quota to reset."
            ) from error

        raise RuntimeError(
            f"Gemini could not process the report: {error}"
        ) from error
