from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.ocr import extract_text_from_image, extract_text_from_pdf
from app.services.llm import summarize_text, extract_entities
from app.utils.file_handler import save_document, get_all_documents
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    docs = get_all_documents()
    return templates.TemplateResponse("index.html", {"request": request, "documents": docs})

@router.post("/upload-file")
async def upload_web(request: Request, file: UploadFile):
    content = await file.read()
    ext = file.filename.lower()

    if ext.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif ext.endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(content)
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "documents": get_all_documents(),
            "error": "Formato no soportado"
        })

    summary = summarize_text(text)
    entities = extract_entities(text)

    doc = {
        "filename": file.filename,
        "summary": summary,
        "entities": entities,
        "timestamp": datetime.now().isoformat()
    }

    save_document(doc)
    return RedirectResponse(url="/", status_code=303)
