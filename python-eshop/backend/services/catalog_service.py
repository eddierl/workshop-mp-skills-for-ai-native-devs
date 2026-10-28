import math

from config import settings
from db.client import DatabaseClient
from models.schemas import (
    CatalogBrandResponse,
    CatalogItemResponse,
    CatalogListResponse,
    CatalogTypeResponse,
)


class CatalogService:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def list_brands(self) -> list[CatalogBrandResponse]:
        return [
            CatalogBrandResponse(id=brand.id, brand=brand.brand)
            for brand in self.db.list_catalog_brands()
        ]

    def list_types(self) -> list[CatalogTypeResponse]:
        return [
            CatalogTypeResponse(id=catalog_type.id, type=catalog_type.type)
            for catalog_type in self.db.list_catalog_types()
        ]

    def list_items(
        self, brand_id: int | None, type_id: int | None, page: int
    ) -> CatalogListResponse:
        page = max(page, 1)
        page_size = settings.catalog_page_size
        total_count = self.db.count_catalog_items(brand_id, type_id)
        total_pages = max(1, math.ceil(total_count / page_size)) if total_count else 1
        offset = (page - 1) * page_size
        items = self.db.get_catalog_items(brand_id, type_id, offset, page_size)
        return CatalogListResponse(
            items=[
                CatalogItemResponse(
                    id=item.id,
                    name=item.name,
                    description=item.description,
                    price=item.price,
                    picture_uri=item.picture_uri,
                    catalog_brand_id=item.catalog_brand_id,
                    catalog_type_id=item.catalog_type_id,
                    brand_name=item.brand_name,
                    type_name=item.type_name,
                )
                for item in items
            ],
            page=page,
            page_size=page_size,
            total_count=total_count,
            total_pages=total_pages,
        )
