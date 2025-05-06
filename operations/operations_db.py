from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List

from data.models import Usuario
from data.schemas import UsuarioCreate, EstadoEnum

async def crear_usuario_db(usuario: UsuarioCreate, session: AsyncSession) -> Usuario:
    nuevo_usuario = Usuario(**usuario.dict())
    session.add(nuevo_usuario)
    try:
        await session.commit()
        await session.refresh(nuevo_usuario)
        return nuevo_usuario
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Correo ya registrado")

async def obtener_usuarios_db(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(select(Usuario))
    return result.scalars().all()

async def obtener_usuario_por_email_db(email: str, session: AsyncSession) -> Usuario:
    result = await session.execute(select(Usuario).filter(Usuario.email == email))
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

async def actualizar_estado_usuario_db(email: str, estado: EstadoEnum, session: AsyncSession):
    usuario = await obtener_usuario_por_email_db(email, session)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.estado = estado
    session.add(usuario)
    
    try:
        await session.commit()
        return usuario
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el estado")