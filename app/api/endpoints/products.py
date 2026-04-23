from fastapi import APIRouter

from app.schemas.product import Product


router = APIRouter()


@router.get("/{item_id}")
async  def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@router.post("/")
async def create_product(product: Product):
    return {"status": "success", "processed_item": product}
