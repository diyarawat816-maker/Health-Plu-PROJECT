
from PIL import Image, ImageDraw
from ocr_service import extract_text

import io

# Create a sample medical report image
image = Image.new("RGB", (900, 400), "white")
draw = ImageDraw.Draw(image)

report = [
    "MEDICAL BLOOD TEST REPORT",
    "Patient Name: Sample Patient",
    "Hemoglobin: 10.5 g/dL",
    "Reference Range: 12-16 g/dL",
    "Glucose: 95 mg/dL",
    "Report Status: Complete"
]

y = 40

for line in report:
    draw.text((40, y), line, fill="black")
    y += 50

# Save sample image in memory
buffer = io.BytesIO()
image.save(buffer, format="PNG")

# Run OCR
result = extract_text(
    buffer.getvalue(),
    ".png"
)

print("\n--- EXTRACTED REPORT TEXT ---")
print(result)
