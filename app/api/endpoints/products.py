from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Response
)

from app.schemas.product import (
    ProductCreate,
    ProductRead,
    ProductUpdate
)
from app.services.product_service import ProductService


router = APIRouter()


@router.get("/", response_model=list[ProductRead])
async def get_products(
    min_price: float | None = Query(None, ge=0, description="Filter by minimum price"),
    max_price: float | None = Query(None, ge=0, description="Filter by maximum price"),
    name: str | None = Query(None, description="Filter by name")
):
    return ProductService.get_all(
        name=name,
        min_price=min_price,
        max_price=max_price
    )


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int):
    product = ProductService.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductRead)
async def create_product(product_in: ProductCreate):
    return ProductService.create(product_in)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, product_in: ProductUpdate):
    updated = ProductService.update(product_id, product_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int):
    deleted = ProductService.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return Response(status_code=204)
