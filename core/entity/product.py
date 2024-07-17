from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy import ForeignKey, VARCHAR, CHAR
from core.database import Base, TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User
    from .category import Category


class Product(Base, TimeStampMixin):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(VARCHAR(length=50))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        init=False,
        back_populates="products",
    )
    categories: Mapped[List["ProductCategory"]] = relationship(
        init=False,
        back_populates="product",
    )
    id: Mapped[str] = mapped_column(
        CHAR(36),
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4,
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
