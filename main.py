
from ocr_service import extract_text
from ai_service import explain_report


def simplify_uploaded_report(file_bytes, extension, language="Both"):
    """Extract and explain an uploaded report."""

    # Step 1: Extract text from the uploaded file
    report_text = extract_text(file_bytes, extension)

    if not report_text.strip():
        raise ValueError(
            "No readable text found in the uploaded report."
        )

    print("\n--- EXTRACTED REPORT TEXT ---")
    print(report_text)

    # Step 2: Explain the extracted text using Gemini
    explanation = explain_report(
        report_text,
        language=language
    )

    return explanation

