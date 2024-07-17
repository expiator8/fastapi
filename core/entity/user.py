from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR, ForeignKey, CHAR
from core.database import Base, TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship, DynamicMapped
from sqlalchemy.dialects.mysql import BIGINT

if TYPE_CHECKING:
    from .product import Product


class User(Base, TimeStampMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(VARCHAR(length=50))
    email: Mapped[str] = mapped_column(VARCHAR(length=100))
    products: DynamicMapped["Product"] = relationship(
        init=False,
        back_populates="user",
        lazy="dynamic",
    )
    user_profile: Mapped[UserProfile | None] = relationship(
        init=False, back_populates="user"
    )
    hashed_password: Mapped[str] = mapped_column(VARCHAR(length=128))
    id: Mapped[str] = mapped_column(
        CHAR(36),
        init=False,
        primary_key=True,
        default_factory=lambda: str(uuid.uuid4()),
    )


class UserProfile(Base, TimeStampMixin):
    __tablename__ = "user_profile"

    first_name: Mapped[str | None] = mapped_column(VARCHAR(length=100))
    last_name: Mapped[str | None] = mapped_column(VARCHAR(length=100))
    # birth_date
    address: Mapped[str | None] = mapped_column(VARCHAR(length=255))
    phone_number: Mapped[str | None] = mapped_column(VARCHAR(length=30))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        unique=True,
    )
    user: Mapped["User"] = relationship(
        init=False,
        back_populates="user_profile",
        single_parent=True,
    )
    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        init=False,
        primary_key=True,
        autoincrement=True,
    )
