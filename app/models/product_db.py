from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
     DeclarativeBase,
     Mapped,
     mapped_column)
from sqlalchemy import (
     String,
     Float,
     Text
)


class Base(DeclarativeBase):
    pass


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    keyword: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True, default=[])
