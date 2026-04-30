from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_db import ProductModel
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.base import BaseService


class ProductService(
    BaseService[ProductModel,
    ProductCreate,
    ProductUpdate]
):
    def __init__(self):
        super().__init__(ProductModel)

    async def get_all(
            self,
            db: AsyncSession,
            name: str | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            keyword: str | None = None
    ):
        query = select(self.model)

        if name:
            query = query.where(getattr(self.model, "name").ilike(f"%{name}%"))
        if min_price is not None:
            query = query.where(self.model.price >= min_price)
        if max_price is not None:
            query = query.where(self.model.price <= max_price)
        if keyword:
            desc_col = getattr(self.model, "description")
            key_col = getattr(self.model, "keyword")
            query = query.where(
                or_(
                    desc_col.ilike(f"%{keyword}%"),
                    key_col.contains([keyword])
                )
            )

        result = await db.execute(query)
        return result.scalars().all()


product_service = ProductService()
