import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, VARCHAR, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from ..utils import TimeStampMixin

if TYPE_CHECKING:
    from .user import User
    from .category import Category


class Product(Base, TimeStampMixin):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(VARCHAR(length=50))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        back_populates="products",
    )
    categories: Mapped[List["ProductCategory"]] = relationship(
        back_populates="product",
    )
    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        default=uuid.uuid4,
    )


class ProductCategory(Base):
    __tablename__ = "product_category"
    product_id: Mapped[str] = mapped_column(
        ForeignKey("product.id"),
        primary_key=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        primary_key=True,
    )
    product: Mapped["Product"] = relationship(back_populates="categories")
    category: Mapped["Category"] = relationship(back_populates="products")
