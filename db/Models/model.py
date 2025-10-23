from pydantic import BaseModel
from datetime import datetime


class Card(BaseModel):
    nombre: str
    puntos: int
    telefono: str
    status: str
    fecha_creacion: datetime