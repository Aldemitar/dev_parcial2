import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from data.models import Usuario

CLEVER_DB="postgresql+asyncpg://upeaaahcees6r1uha5dj:sUa4rcAheEZGmJLLitewJbsCWaBq65@boik0dmexa61wv34gl6t-postgresql.services.clever-cloud.com:50013/boik0dmexa61wv34gl6t"

engine : AsyncEngine = create_async_engine(CLEVER_DB, echo=True)
async_session =sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session