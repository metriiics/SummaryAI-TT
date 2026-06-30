from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

import os
from dotenv import load_dotenv
load_dotenv()

user_db = os.getenv('DB_USER')
passwd_db = os.getenv('DB_PASS')
host_db = os.getenv('DB_HOST')
port_db = os.getenv('DB_PORT')
name_db = os.getenv('DB_NAME')

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{user_db}:{passwd_db}@"
    f"{host_db}:{port_db}/"
    f"{name_db}"
)

engine = create_engine(
    url=DATABASE_URL
)

session_factory = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db() -> Session:
    db = session_factory()
    try:
        yield db
    finally:
        db.close()