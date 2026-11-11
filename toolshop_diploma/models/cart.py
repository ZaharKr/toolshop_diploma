from pydantic import BaseModel, ConfigDict, Field


class AddCartItemRequest(BaseModel):
    product_id: str
    quantity: int = 1


class CartCreateResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str


class CartItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    product_id: str | None = None
    quantity: int | None = None


class CartResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    cart_items: list[CartItem] = Field(default_factory=list)
