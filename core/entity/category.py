from typing import List, TYPE_CHECKING
from core.database import Base, TimeStampMixin
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT

if TYPE_CHECKING:
    from .product import ProductCategory


class Category(Base, TimeStampMixin):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(VARCHAR(length=20))
    products: Mapped[List["ProductCategory"]] = relationship(
        init=False,
        back_populates="category",
    )
    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        init=False,
        primary_key=True,
        autoincrement=True,
    )
