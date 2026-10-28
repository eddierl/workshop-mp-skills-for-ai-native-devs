from fastapi import APIRouter, Depends, Query

from dependencies import get_catalog_service, get_current_user_email
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
    page: int = Query(default=1),
    user_email: str | None = Depends(get_current_user_email),
    service: CatalogService = Depends(get_catalog_service),
):
    user_id: int | None = None
    if user_email:
        user = service.db.get_user_by_email(user_email)
        if user:
            user_id = user.id
    return service.list_items(brand_id, type_id, page, user_id=user_id)
