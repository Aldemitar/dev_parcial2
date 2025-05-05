from sqlmodel import SQLModel, Field
import enum

class EstadoEnum(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Eliminado = "Eliminado"

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(index=True, unique=True)
    estado: EstadoEnum
    premium: bool
