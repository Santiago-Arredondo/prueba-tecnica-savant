from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import RedirectResponse
from datetime import datetime
import shutil
import os

from app.utils.file_handler import save_document
from app.services.ocr import extract_text_from_image, extract_text_from_pdf
from app.services.llm import summarize_text, extract_entities

router = APIRouter()

UPLOAD_FOLDER = "documents/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Guardar archivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detectar tipo
    text = ""
    if file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(file_path)
    elif file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        return {"error": "Formato no soportado"}

    # Procesar con LLM simulado
    summary = summarize_text(text)
    entities = extract_entities(text)

    # Guardar en historial
    doc_data = {
        "filename": file.filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": summary,
        "entities": entities,
    }
    save_document(doc_data)

    return RedirectResponse("/", status_code=303)

@router.get("/history")
async def get_history(request: Request):
    documents = save_document.get_all_documents()


