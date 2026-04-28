from fastapi import APIRouter, HTTPException

from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import product_service


router = APIRouter()


@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate):
    return product_service.create(product)


@router.get("/{product_id}", response_model=ProductRead)
async def read_product(product_id: int):
    product = product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/", response_model=list[ProductRead])
async def read_products():
    return product_service.get_all()
