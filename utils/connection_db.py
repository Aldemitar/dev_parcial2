import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from data.models import Usuario

CLEVER_DB="postgresql+asyncpg://dev_parcial2_db_user:mZHbGxR0CMEHiWs1FAzdnUJpUaQN4wxe@dpg-d0d8gkruibrs73bs3h9g-a/dev_parcial2_db"

engine : AsyncEngine = create_async_engine(CLEVER_DB, echo=True)
async_session =sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session