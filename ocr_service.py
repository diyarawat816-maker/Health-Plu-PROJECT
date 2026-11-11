
import io
import os

import pymupdf
import pytesseract

from PIL import Image, ImageEnhance, ImageFilter


# Tesseract installation path
# Windows uses the installed Windows executable.
# Render/Linux uses the system-installed Tesseract.
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
else:
    pytesseract.pytesseract.tesseract_cmd = "tesseract"


def preprocess_image(image):
    """Improve image quality before OCR."""

    image = image.convert("RGB")

    image = image.resize(
        (image.width * 2, image.height * 2),
        Image.Resampling.LANCZOS
    )

    image = ImageEnhance.Contrast(image).enhance(1.5)

    image = image.filter(ImageFilter.SHARPEN)

    return image


def extract_from_image(file_bytes: bytes) -> str:
    """Extract text from an image."""

    image = Image.open(io.BytesIO(file_bytes))

    image = preprocess_image(image)

    text = pytesseract.image_to_string(
        image,
        lang="eng",
        config="--oem 3 --psm 6"
    )

    return text.strip()


def extract_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF."""

    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    if len(document) > 20:
        document.close()
        raise ValueError("Maximum 20 pages allowed.")

    extracted_pages = []

    try:
        for page in document:

            text = page.get_text().strip()

            # Use OCR if the PDF page has little or no text
            if len(text) < 20:

                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2),
                    alpha=False
                )

                image = Image.open(
                    io.BytesIO(pix.tobytes("png"))
                )

                image = preprocess_image(image)

                text = pytesseract.image_to_string(
                    image,
                    lang="eng",
                    config="--oem 3 --psm 6"
                )

            extracted_pages.append(text)

    finally:
        document.close()

    return "\n\n".join(extracted_pages).strip()


def extract_text(file_bytes: bytes, extension: str) -> str:
    """Main function used by the application."""

    extension = extension.lower()

    if extension in [".jpg", ".jpeg", ".png"]:
        return extract_from_image(file_bytes)

    elif extension == ".pdf":
        return extract_from_pdf(file_bytes)

    else:
        raise ValueError("Unsupported file format.")



