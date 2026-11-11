from pydantic import BaseModel, ConfigDict, Field


class ProductImage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    file_name: str | None = None
    title: str | None = None


class Category(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    name: str | None = None
    slug: str | None = None


class Brand(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    name: str | None = None


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    description: str | None = None
    price: float | None = None
    in_stock: bool | None = None
    product_image: ProductImage | None = None
    category: Category | None = None
    brand: Brand | None = None


class ProductsPage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    current_page: int | None = None
    data: list[Product] = Field(default_factory=list)
    total: int | None = None
    per_page: int | None = None
