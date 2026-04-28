from app.schemas.product import ProductCreate, ProductUpdate


products_db = []
next_product_id = 1


class ProductService:
    @staticmethod
    def get_all(
            name: str | None = None,
            min_price: float | None = None,
            max_price: float | None = None
    ):
        products = products_db

        if name:
            products = [p for p in products if name.lower() in p["name"].lower()]
        if min_price is not None:
            products = [p for p in products if p["price"] >= min_price]
        if max_price is not None:
            products = [p for p in products if p["price"] <= max_price]

        return products

    @staticmethod
    def get_by_id(product_id: int):
        return next((p for p in products_db if p["id"] == product_id), None)

    @staticmethod
    def create(data: ProductCreate):
        global next_product_id

        new_product = {"id": next_product_id, **data.model_dump()}
        products_db.append(new_product)
        next_product_id += 1
        return new_product

    @staticmethod
    def update(product_id: int, data: ProductUpdate):
        for product in products_db:
            if product["id"] == product_id:
                update_data = data.model_dump(exclude_unset=True)
                product.update(update_data)
                return product
        return None

    @staticmethod
    def delete(product_id: int):
        global products_db

        product = ProductService.get_by_id(product_id)
        if product:
            products_db = [p for p in products_db if p["id"] != product_id]
            return True
        return False
