# app/api.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.services.ocr import extract_text_from_file
from app.services.llm import summarize_text, extract_entities
from .utils.file_handler import save_document_info, get_all_documents
from datetime import datetime

import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        text = await extract_text_from_file(file)
        summary = summarize_text(text)
        entities = extract_entities(text)

        info = {
            "filename": file.filename,
            "summary": summary,
            "entities": entities,
            "timestamp": datetime.now().isoformat()
        }

        save_document_info(info)
        return JSONResponse(content=info)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def history():
    return get_all_documents()
