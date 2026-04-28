from pydantic import (
    BaseModel,
    field_validator,
    ConfigDict
)


class ProductBase(BaseModel):
    name: str
    price: float
    description: str | None = None

    @field_validator("price")
    @classmethod
    def round_price(cls, v):
        return round(v, 2)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(ProductBase):
    pass
