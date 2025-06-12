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
-  LLM local: [`Ollama`](https://ollama.com) con modelo `mistral`
-  OCR con `pytesseract`
-  Contenedorización con Docker
-  Frontend sencillo con TailwindCSS

##  Requisitos previos

- Instalar dependencias:

```bash
pip install -r requirements.txt
```


###  LLM local con Ollama

Este proyecto usa Ollama para procesar texto con un modelo de lenguaje local.

#### Instrucciones:

1. Instala Ollama desde: https://ollama.com/download
2. Ejecuta el modelo:

```bash
ollama run mistral
```
Esto dejará un servidor escuchando en `http://localhost:11434`. **Hay que mantenerlo activo** mientras se usa la app.

>  Si se usa Docker, asegurarse de que Ollama esté corriendo en la máquina local (host) antes de iniciar el contenedor.

---



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

### Ejecutar Test
- Interfaz web: http://localhost:8000

- Swagger API: http://localhost:8000/docs