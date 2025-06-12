# app/services/ocr.py
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from fastapi import UploadFile
import io

async def extract_text_from_file(file: UploadFile) -> str:
    content = await file.read()
    if file.filename.lower().endswith(".pdf"):
        images = convert_from_bytes(content)
        return "\n".join(pytesseract.image_to_string(img) for img in images)
    elif file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        img = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(img)
    else:
        raise ValueError("Formato no soportado: solo PDF o imágenes JPG/PNG")
