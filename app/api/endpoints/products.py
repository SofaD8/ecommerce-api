from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Depends,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.product import (
    ProductCreate,
    ProductRead,
    ProductUpdate
)
from app.services.product_service import ProductService
from app.db.session import get_db


router = APIRouter()
product_service = ProductService()


@router.get("/", response_model=list[ProductRead])
async def get_products(
    min_price: float | None = Query(None, ge=0, description="Filter by minimum price"),
    max_price: float | None = Query(None, ge=0, description="Filter by maximum price"),
    name: str | None = Query(None, description="Filter by name"),
    keyword: str | None = Query(None, description="Filter by keyword"),
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_all(
        db,
        name=name,
        min_price=min_price,
        max_price=max_price,
        keyword=keyword
    )


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_service.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create(db, obj_in=product_in)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
        product_id: int,
        product_in: ProductUpdate,
        db: AsyncSession = Depends(get_db)
):
    updated = await product_service.update(db, obj_id=product_id, obj_in=product_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int,db: AsyncSession = Depends(get_db)):
    deleted = await product_service.delete(db, obj_id=product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
