from ai_service import explain_report

report = """
Blood Test Report

Haemoglobin: 12.5 g/dL
Glucose: 95 mg/dL
"""

result = explain_report(
    report,
    language="Both"
)

print("\n===== MEDIEXPLAIN AI RESULT =====\n")
print(result)