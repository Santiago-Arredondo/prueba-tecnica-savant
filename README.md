# Reto Técnico - Procesamiento de Documentos con IA

Este proyecto implementa una API en Python con FastAPI que permite:

- Subir archivos PDF o imágenes (JPG, PNG)
- Extraer texto mediante OCR (Tesseract)
- Generar un resumen del contenido
- Extraer entidades clave
- Visualizar un historial de documentos procesados

##  Tecnologías utilizadas

-  Python 3.10
-  FastAPI
-  Simulación de modelo LLM (extensible a transformers u ollama)
-  OCR con `pytesseract`
-  Contenedorización con Docker
-  Frontend sencillo con TailwindCSS


### Ejecutar Con Docker
```bash
docker build -t prueba_tecnica_savant .
docker run -p 8000:8000 prueba_tecnica_savant
```

### Ejecutar Localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
