from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from utils.connection_db import init_db

from utils.connection_db import init_db, get_session
from data.models import Usuario, EstadoEnum, Tarea, EstadoTarea
from data.schemas import UsuarioCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from typing import List

from operations.operations_db import crear_usuario_db, obtener_usuarios_db, obtener_usuario_por_email_db, actualizar_estado_usuario_db, actualizar_premium_usuario_db, obtener_usuarios_activos_db, obtener_usuarios_activos_premium_db, crear_tarea_db

import os

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)

@app.post("/usuarios", status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
async def crear_usuario(usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)):
    return await crear_usuario_db(usuario, session)

@app.get("/usuarios", response_model=List[Usuario], tags=["Usuarios"])
async def obtener_usuarios(session: AsyncSession = Depends(get_session)):
    return await obtener_usuarios_db(session)

@app.get("/usuarios/activos", response_model=List[Usuario], tags=["Usuarios"])
async def obtener_usuarios_activos(session: AsyncSession = Depends(get_session)):
    usuarios = await obtener_usuarios_activos_db(session)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios activos")
    return usuarios

@app.get("/usuarios/{email}", response_model=Usuario, tags=["Usuarios"])
async def obtener_usuario_por_email(email: str, session: AsyncSession = Depends(get_session)):
    return await obtener_usuario_por_email_db(email, session)

@app.patch("/usuarios/{email}/estado", response_model=Usuario, tags=["Usuarios"])
async def actualizar_estado_usuario(email: str, estado: EstadoEnum, session: AsyncSession = Depends(get_session)):
    return await actualizar_estado_usuario_db(email, estado, session)

@app.patch("/usuarios/{email}/premium", response_model=Usuario, tags=["Usuarios"])
async def actualizar_premium_usuario(email: str, premium: bool, session: AsyncSession = Depends(get_session)):
    return await actualizar_premium_usuario_db(email, premium, session)

@app.get("/usuarios/activos/premium", response_model=List[Usuario], tags=["Usuarios"])
async def obtener_usuarios_activos_premium(session: AsyncSession = Depends(get_session)):
    usuarios = await obtener_usuarios_activos_premium_db(session)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios activos y que sean premium")
    return usuarios

@app.post("/tareas", status_code=status.HTTP_201_CREATED, tags=["Tareas"])
async def crear_tarea(tarea: Tarea, session: AsyncSession = Depends(get_session)):
    return await crear_tarea_db(tarea, session)