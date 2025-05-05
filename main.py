from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from utils.connection_db import init_db

from utils.connection_db import init_db, get_session
from data.models import Usuario
from data.schemas import UsuarioCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)):
    nuevo_usuario = Usuario(**usuario.dict())
    session.add(nuevo_usuario)
    try:
        await session.commit()
        await session.refresh(nuevo_usuario)
        return nuevo_usuario
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Correo ya registrado")