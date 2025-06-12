from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.ocr import extract_text_from_image, extract_text_from_pdf
from app.services.llm import summarize_text, extract_entities
from app.utils.file_handler import save_document, get_all_documents
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Interfaz web",
    description="Interfaz web con formulario para subir archivos PDF o imagen, procesarlos y ver el historial."
)
def home(request: Request):
    docs = get_all_documents()
    return templates.TemplateResponse("index.html", {"request": request, "documents": docs})

@router.post(
    "/upload-file",
    summary="Subida desde interfaz web",
    description="Maneja la carga de archivos desde el formulario HTML, aplica OCR (PDF o imagen), y guarda los resultados."
)
async def upload_web(request: Request, file: UploadFile, lang: str = Form(default="eng+spa", description="Idiomas OCR, separados por '+'. Ej: 'eng+spa' para inglés y español")):
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
