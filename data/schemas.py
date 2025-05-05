from sqlmodel import SQLModel
from data.models import EstadoEnum

class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    estado: EstadoEnum
    premium: bool