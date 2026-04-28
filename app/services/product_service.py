from app.schemas.product import ProductCreate


class ProductService:
    def __init__(self):
        self._products = []
        self._counter = 1

    def create(self, product_data: ProductCreate):
        product = {
            "id": self._counter,
            **product_data.model_dump()
        }
        self._products.append(product)
        self._counter += 1
        return product

    def get_by_id(self, product_id: int):
        return next((p for p in self._products if p["id"] == product_id), None)

    def get_all(self):
        return self._products


product_service = ProductService()
