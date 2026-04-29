from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_db import ProductModel
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    async def get_all(
            db: AsyncSession,
            name: str | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            keyword: str | None = None
    ):
        query = select(ProductModel)

        if name:
            query = query.where(ProductModel.name.ilike(f"%{name}%"))    # noqa
        if min_price is not None:
            query = query.where(ProductModel.price >= min_price)
        if max_price is not None:
            query = query.where(ProductModel.price <= max_price)
        if keyword:
            query = query.where(
                or_(
                    ProductModel.description.ilike(f"%{keyword}%"),
                    ProductModel.keyword.contains([keyword])
                )
            )

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: int):
        return await db.get(ProductModel, product_id)

    @staticmethod
    async def create(db: AsyncSession, data: ProductCreate):
        new_product = ProductModel(**data.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    @staticmethod
    async def update(db: AsyncSession, product_id: int, data: ProductUpdate):
        product = await ProductService.get_by_id(db, product_id)
        if product:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)

            await db.commit()
            await db.refresh(product)
            return product
        return None

    @staticmethod
    async def delete(db: AsyncSession, product_id: int):
        product = await ProductService.get_by_id(db, product_id)
        if product:
            await db.delete(product)
            await db.commit()
            return True
        return False
