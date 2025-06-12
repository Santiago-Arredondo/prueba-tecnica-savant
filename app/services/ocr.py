from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf(content: bytes, lang="eng+spa") -> str:
    try:
        images = convert_from_bytes(content)
        return "\n".join(pytesseract.image_to_string(img, lang=lang) for img in images)
    except Exception as e:
        return f"OCR Error: {str(e)}"

def extract_text_from_image(content: bytes,lang="eng+spa") -> str:
    try:
        img = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(img, lang=lang)
    except Exception as e:
        return f"OCR Error: {str(e)}"
