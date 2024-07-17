from typing_extensions import Annotated
from datetime import datetime
from sqlalchemy import text, create_engine
from sqlalchemy.orm import (
    MappedAsDataclass,
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    Session,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from fastapi import Depends


class TimeStampMixin(MappedAsDataclass):
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True, precision=6),
        init=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True, precision=6),
        init=False,
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )


class Base(MappedAsDataclass, DeclarativeBase): ...


SQLALCHEMY_DATABASE_URL = "postgresql://root:1234@localhost:5432/mydb"

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
