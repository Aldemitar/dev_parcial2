from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from sqlalchemy import Enum as SqlEnum
import enum

class EstadoEnum(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Eliminado = "Eliminado"

class EstadoTarea(enum.Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecucion"
    realizada = "Realizada"
    cancelada = "Cancelada"

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(index=True, unique=True)
    estado: EstadoEnum
    premium: bool

class Tarea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, nullable=False)
    descripcion: str = Field(max_length=300, nullable=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_modificacion: Optional[datetime] = Field(default_factory=datetime.utcnow)
    estado: EstadoTarea = Field(sa_column=SqlEnum(EstadoTarea), default=EstadoTarea.pendiente)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)