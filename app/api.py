from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from datetime import datetime
import os
import shutil

from app.services.ocr import extract_text_from_pdf, extract_text_from_image
from app.services.llm import summarize_text, extract_entities
from app.utils.file_handler import save_document
from app.utils.file_handler import get_all_documents


router = APIRouter()

UPLOAD_FOLDER = "app/documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    
    ext = file.filename.lower()
    if ext.endswith(".pdf"):
        if not content.strip():
            return {"error": "El archivo PDF está vacío"}
        text = extract_text_from_pdf(content)
    elif ext.endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(content)
    else:
        return {"error": "Formato no soportado"}

    summary = summarize_text(text)
    entities = extract_entities(text)

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
    documents = get_all_documents()
    return {"history": documents}



