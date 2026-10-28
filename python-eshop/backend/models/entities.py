from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CatalogBrand:
    id: int
    brand: str


@dataclass
class CatalogType:
    id: int
    type: str


@dataclass
class CatalogItem:
    id: int
    name: str
    description: str
    price: float
    picture_uri: str
    catalog_brand_id: int
    catalog_type_id: int
    brand_name: str | None = None
    type_name: str | None = None


@dataclass
class User:
    id: int
    email: str
    password_hash: str


@dataclass
class BasketItem:
    id: int
    catalog_item_id: int
    quantity: int
    unit_price: float
    product_name: str | None = None
    picture_uri: str | None = None


@dataclass
class Basket:
    id: int
    buyer_id: str
    items: list[BasketItem] = field(default_factory=list)


@dataclass
class OrderItem:
    id: int
    catalog_item_id: int
    product_name: str
    picture_uri: str
    unit_price: float
    units: int


@dataclass
class Order:
    id: int
    buyer_id: str
    order_date: datetime
    ship_to_street: str
    ship_to_city: str
    ship_to_state: str
    ship_to_country: str
    ship_to_zip_code: str
    items: list[OrderItem] = field(default_factory=list)
