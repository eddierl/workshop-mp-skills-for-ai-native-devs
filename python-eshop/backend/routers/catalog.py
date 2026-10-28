from fastapi import APIRouter, Depends, Query

from dependencies import get_catalog_service
from models.schemas import CatalogBrandResponse, CatalogListResponse, CatalogTypeResponse
from services.catalog_service import CatalogService

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


@router.get("/brands", response_model=list[CatalogBrandResponse])
def list_brands(service: CatalogService = Depends(get_catalog_service)):
    return service.list_brands()


@router.get("/types", response_model=list[CatalogTypeResponse])
def list_types(service: CatalogService = Depends(get_catalog_service)):
    return service.list_types()


@router.get("/items", response_model=CatalogListResponse)
def list_items(
    brand_id: int | None = Query(default=None),
    type_id: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    service: CatalogService = Depends(get_catalog_service),
):
    return service.list_items(brand_id, type_id, page)
