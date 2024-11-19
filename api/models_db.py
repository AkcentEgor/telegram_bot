from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

import os
from dotenv import load_dotenv

# Настройки базы данных
load_dotenv()
DATABASE_URL = os.getenv('POSTGRES_DATABASE_URL')

# Создание асинхронного движка SQLAlchemy и сессии
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

# Модель данных для базы данных
class MeterReading(Base):
    __tablename__ = "meter_readings"
    personal_account = Column(Integer, index=True, primary_key=True)
    address = Column(String)
    meter = Column(Integer)

# Создание таблицы при старте приложения
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


