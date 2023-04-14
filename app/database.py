from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import SQLALCHEMY_DATABASE_URL


def get_db_context():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

metadata = MetaData().create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
