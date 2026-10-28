from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError

from services.passwords import MAX_PASSWORD_BYTES

MAX_LINE_QUANTITY = 99

LineQuantity = Annotated[int, Field(ge=0, le=MAX_LINE_QUANTITY)]


class CatalogBrandResponse(BaseModel):
    id: int
    brand: str


class CatalogTypeResponse(BaseModel):
    id: int
    type: str


class CatalogItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    picture_uri: str
    catalog_brand_id: int
    catalog_type_id: int
    brand_name: str | None = None
    type_name: str | None = None


class CatalogListResponse(BaseModel):
    items: list[CatalogItemResponse]
    page: int
    page_size: int
    total_count: int
    total_pages: int


class BasketItemResponse(BaseModel):
    id: int
    catalog_item_id: int
    quantity: int
    unit_price: float
    product_name: str
    picture_uri: str
    line_total: float


class BasketResponse(BaseModel):
    id: int
    buyer_id: str
    items: list[BasketItemResponse]
    total: float
    item_count: int


class AddBasketItemRequest(BaseModel):
    catalog_item_id: int
    quantity: int = Field(default=1, ge=1, le=MAX_LINE_QUANTITY)


class UpdateBasketItemsRequest(BaseModel):
    quantities: dict[str, LineQuantity]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > MAX_PASSWORD_BYTES:
            raise PydanticCustomError(
                "password_too_long",
                "Password must be at most {limit} bytes "
                "(72 plain characters, fewer with accents or emoji)",
                {"limit": MAX_PASSWORD_BYTES},
            )
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str


class OrderItemResponse(BaseModel):
    id: int
    catalog_item_id: int
    product_name: str
    picture_uri: str
    unit_price: float
    units: int
    line_total: float


class OrderSummaryResponse(BaseModel):
    id: int
    order_date: datetime
    total: float
    item_count: int


class OrderDetailResponse(BaseModel):
    id: int
    order_date: datetime
    ship_to_street: str
    ship_to_city: str
    ship_to_state: str
    ship_to_country: str
    ship_to_zip_code: str
    items: list[OrderItemResponse]
    total: float


class CreateOrderRequest(BaseModel):
    basket_id: int
