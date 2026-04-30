from fastapi import APIRouter

from app.api.endpoints import (
    products,
    # orders,
    # users,
    tasks)


api_router = APIRouter()


api_router.include_router(products.router, prefix="/products", tags=["products"])
#api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
#api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
