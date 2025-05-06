from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from utils.connection_db import init_db

from utils.connection_db import init_db, get_session
from data.models import Usuario
from data.schemas import UsuarioCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from typing import List

from operations.operations_db import crear_usuario_db, obtener_usuarios_db



@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)):
    return await crear_usuario_db(usuario, session)

@app.get("/usuarios", response_model=List[Usuario])
async def obtener_usuarios(session: AsyncSession = Depends(get_session)):
    return await obtener_usuarios_db(session)