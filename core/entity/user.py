from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR, ForeignKey, CHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship, DynamicMapped
from ..database import Base
from ..utils import TimeStampMixin

if TYPE_CHECKING:
    from .product import Product


class User(Base, TimeStampMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(VARCHAR(length=50))
    email: Mapped[str] = mapped_column(VARCHAR(length=100))
    products: DynamicMapped["Product"] = relationship(
        back_populates="user",
        lazy="dynamic",
    )
    user_profile: Mapped[UserProfile | None] = relationship(
        back_populates="user",
        uselist=False,
    )
    hashed_password: Mapped[str] = mapped_column(VARCHAR(length=128))
    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        default=str(uuid.uuid4()),
    )


class UserProfile(Base, TimeStampMixin):
    __tablename__ = "user_profile"

    first_name: Mapped[str | None] = mapped_column(VARCHAR(length=100))
    last_name: Mapped[str | None] = mapped_column(VARCHAR(length=100))
    address: Mapped[str | None] = mapped_column(VARCHAR(length=255))
    phone_number: Mapped[str | None] = mapped_column(VARCHAR(length=30))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        unique=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="user_profile",
        single_parent=True,
    )
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )


class UserAccessToken(Base, TimeStampMixin):
    """회원 Access Token 테이블 모델"""

    __tablename__ = "user_access_token"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    access_token: Mapped[str] = mapped_column(VARCHAR(length=255), unique=True)
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )
