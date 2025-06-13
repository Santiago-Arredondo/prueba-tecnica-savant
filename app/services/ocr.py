from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf(content: bytes, lang="eng+spa") -> str:
    try:
        images = convert_from_bytes(content)
        texts = [
            pytesseract.image_to_string(img, lang=lang, config="--psm 6").strip()
            for img in images
        ]
        return "\n".join(t for t in texts if t).strip()
    except Exception as e:
        return f"OCR Error: {str(e)}"

def extract_text_from_image(content: bytes, lang="eng+spa") -> str:
    try:
        img = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(img, lang=lang, config="--psm 6").strip()
    except Exception as e:
        return f"OCR Error: {str(e)}"
