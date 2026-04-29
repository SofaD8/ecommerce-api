from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator
)


def round_price_value(value: float | None) -> float | None:
    if value is None:
        return value
    return round(value, 2)


class ProductBase(BaseModel):
    name: str
    price: float
    description: str | None = None
    keywords: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("price")
    @classmethod
    def round_price(cls, value):
        return round_price_value(value)


class ProductCreate(ProductBase):
    ...


class ProductRead(ProductBase):
    id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("price")
    @classmethod
    def round_price(cls, value):
        return round_price_value(value)
