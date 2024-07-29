from typing_extensions import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from fastapi import Depends
from config import settings


class Base(DeclarativeBase): ...


SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=True,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_session = Annotated[Session, Depends(get_db)]
