from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import Buyer, get_basket_service, get_buyer
from models.schemas import (
    AddBasketItemRequest,
    BasketResponse,
    UpdateBasketItemsRequest,
)
from services.basket_service import BasketService

router = APIRouter(prefix="/api/basket", tags=["basket"])


@router.get("", response_model=BasketResponse)
def get_basket(
    buyer: Buyer = Depends(get_buyer),
    service: BasketService = Depends(get_basket_service),
):
    return service.get_or_create_basket(buyer.id)


@router.post("/items", response_model=BasketResponse)
def add_item(
    body: AddBasketItemRequest,
    buyer: Buyer = Depends(get_buyer),
    service: BasketService = Depends(get_basket_service),
):
    try:
        return service.add_item(buyer.id, body.catalog_item_id, body.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/items", response_model=BasketResponse)
def update_items(
    body: UpdateBasketItemsRequest,
    buyer: Buyer = Depends(get_buyer),
    service: BasketService = Depends(get_basket_service),
):
    try:
        return service.set_quantities(buyer.id, body.quantities)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
