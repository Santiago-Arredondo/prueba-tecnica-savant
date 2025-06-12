from fastapi import APIRouter, UploadFile, File, Request, Form
from fastapi.responses import RedirectResponse
from datetime import datetime
import os
import shutil

from app.services.ocr import extract_text_from_pdf, extract_text_from_image
from app.services.llm import summarize_text, extract_entities
from app.utils.file_handler import save_document,get_all_documents
from pydantic import BaseModel
from typing import List


router = APIRouter()

UPLOAD_FOLDER = "app/documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class DocumentData(BaseModel):
    filename: str
    timestamp: str
    summary: str
    entities: List[str]

@router.post("/upload-file",
               summary="Subir y procesar archivo",
    description="Permite subir un archivo PDF o imagen (JPG/PNG), extraer el texto con OCR, generar un resumen y extraer entidades. El resultado se guarda en el historial."
             )
async def upload_file(file: UploadFile = File(...),
             lang: str = Form(default="eng+spa", description="Idiomas para OCR, separados por '+', por ejemplo: 'eng+spa' para inglés y español")
            ):  
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


@router.get(
    "/history",
    response_model=List[DocumentData],
    summary="Obtener historial",
    description="Devuelve el historial de documentos procesados con resumen y entidades."
)
async def get_history(request: Request):
    documents = get_all_documents()
    return {"history": documents}



