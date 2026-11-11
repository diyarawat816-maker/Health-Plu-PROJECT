
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

# Select AI model
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


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

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a careful and helpful report "
                "simplification assistant. Explain facts "
                "accurately without inventing information."
            ),
            temperature=0.2
        )
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text
