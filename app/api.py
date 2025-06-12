from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import RedirectResponse
from datetime import datetime
import shutil
import os

from app.utils.file_handler import save_document
from app.services.ocr import extract_text_from_file
from app.services.llm import summarize_text, extract_entities

router = APIRouter()

UPLOAD_FOLDER = "documents/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Guardar archivo en disco
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Reabrir el archivo como UploadFile simulado (para extraer texto con OCR)
    with open(file_path, "rb") as f:
        class TempUploadFile:
            filename = file.filename
            async def read(self):
                return f.read()

        temp_file = TempUploadFile()
        text = await extract_text_from_file(temp_file)

    # Procesamiento con "IA"
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


