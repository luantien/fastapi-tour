import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

def get_connection_string():
    engine = os.environ.get("DB_ENGINE")
    dbhost = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")
    return f"{engine}://{username}:{password}@{dbhost}/{dbname}"

SQLALCHEMY_DATABASE_URL = get_connection_string()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

metadata = MetaData()
metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
