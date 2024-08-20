from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_URL_ASYNC


def get_db_context():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_async_db_context():
    async with AsyncSessionLocal() as async_db:
        yield async_db

engine = create_engine(SQLALCHEMY_DATABASE_URL)
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)

metadata = MetaData().create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(async_engine, autocommit=False, autoflush=False)

Base = declarative_base()
