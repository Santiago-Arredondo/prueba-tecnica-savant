from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf(content: bytes) -> str:
    """
    Convierte cada página del PDF en imagen y aplica OCR para extraer texto.
    """
    images = convert_from_bytes(content)
    text = "\n".join(pytesseract.image_to_string(img) for img in images)
    return text

def extract_text_from_image(content: bytes) -> str:
    """
    Aplica OCR directamente a la imagen (JPG, PNG).
    """
    img = Image.open(io.BytesIO(content))
    text = pytesseract.image_to_string(img)
    return text
