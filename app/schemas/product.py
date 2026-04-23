from pydantic import BaseModel,field_validator


class Product(BaseModel):
    name: str
    price: float
    description: str | None = None

    @field_validator("price")
    @classmethod
    def round_price(cls, v):
        return round(v, 2)
