from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import api, web

app = FastAPI()

app.include_router(api.router)
app.include_router(web.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
