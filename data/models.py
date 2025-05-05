from sqlalchemy import Column, String, Integer, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum

class EstadoEnum(enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Eliminado = "Eliminado"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    estado: Mapped[EstadoEnum] = mapped_column(Enum(EstadoEnum), nullable=False)
    premium: Mapped[bool] = mapped_column(Boolean, nullable=False)