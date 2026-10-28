from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_order_service, require_authenticated_user
from models.schemas import CreateOrderRequest, OrderDetailResponse, OrderSummaryResponse
from services.basket_service import EmptyBasketError
from services.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderDetailResponse)
def create_order(
    body: CreateOrderRequest,
    buyer_id: str = Depends(require_authenticated_user),
    service: OrderService = Depends(get_order_service),
):
    try:
        return service.create_from_basket(buyer_id, body.basket_id)
    except EmptyBasketError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("", response_model=list[OrderSummaryResponse])
def list_orders(
    buyer_id: str = Depends(require_authenticated_user),
    service: OrderService = Depends(get_order_service),
):
    return service.list_for_user(buyer_id)


@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order(
    order_id: int,
    buyer_id: str = Depends(require_authenticated_user),
    service: OrderService = Depends(get_order_service),
):
    try:
        return service.get_detail(buyer_id, order_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
