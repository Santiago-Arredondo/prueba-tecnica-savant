# Reto Técnico - Procesamiento de Documentos con IA

API en Python con FastAPI que permite subir PDFs o imágenes, extraer texto con OCR, resumir contenido y extraer entidades clave.

## Requisitos

- Docker
- Python 3.10 (si se ejecuta localmente)

## Cómo ejecutar

### Con Docker
```bash
docker build -t prueba_tecnica_savant .
docker run -p 8000:8000 prueba_tecnica_savant
