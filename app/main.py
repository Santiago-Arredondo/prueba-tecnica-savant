# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import router as api_router
from app.web import router as web_router  # nueva importación

app = FastAPI()

# Montar archivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir las rutas API
app.include_router(api_router)

# Incluir las rutas Web (formulario e historial en HTML)
app.include_router(web_router)
