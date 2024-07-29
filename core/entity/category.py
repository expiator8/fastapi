from typing import List, TYPE_CHECKING
from sqlalchemy import VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from ..utils import TimeStampMixin

if TYPE_CHECKING:
    from .product import ProductCategory


class Category(Base, TimeStampMixin):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(VARCHAR(length=20))
    products: Mapped[List["ProductCategory"]] = relationship(
        back_populates="category",
    )
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )
