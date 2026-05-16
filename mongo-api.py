from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Despliegue en Render
client = MongoClient(os.environ["MONGO_URI"])

# Pruebas locales
# client = MongoClient("mongodb://ISIS2304C15202610:eNSy5oIPVvfj@157.253.236.88:8087")
db = client["ISIS2304C15202610"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


# PUNTO 6
@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(
        db["comentarios_bares"].find(
            {"bar_id": bar_id},
            {"_id": 0}
        )
    )
    return comentarios

# PUNTO 7
@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    datos.pop("_id", None)
    return {'mensaje': 'Comentario guardado'}

# PUNTO 8
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(
        db["eventos"].find(
            {"bar_id": bar_id},
            {"_id": 0}
        )
    )
    return eventos

# PUNTO 9
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id']         = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    datos.pop("_id", None)
    return {'mensaje': 'Evento guardado'}