# Reto Técnico – Procesamiento de Documentos con IA

Este proyecto implementa una API en Python con FastAPI que permite:

- Subir archivos PDF o imágenes (JPG, PNG)
- Extraer texto mediante OCR (Tesseract)
- Generar un resumen básico del contenido
- Extraer entidades clave usando expresiones regulares
- Visualizar un historial de documentos procesados en una interfaz web


##  Tecnologías utilizadas

- Python 3.10
- FastAPI
- OCR con `pytesseract`
- Visualización web con TailwindCSS
- Contenedorización con Docker
- Almacenamiento local en `storage.json`


##  Requisitos previos

### 1. Python local

- Tener Python 3.10+ instalado
- Instalar las dependencias:

```bash
pip install -r requirements.txt

```

## Ejecución

### 1. Local
- python -m venv .venv
- source .venv/bin/activate          
- pip install -r requirements.txt
- uvicorn app.main:app --reload

### 2. Docker
- docker build -t prueba_tecnica_savant .
- docker run -p 8000:8000 prueba_tecnica_savant
Con Docker, es importante asegurarse de tener Docker Desktop abierto antes de ejecutar el contenedor.

- Interfaz web: http://localhost:8000

- Swagger API: http://localhost:8000/docs
