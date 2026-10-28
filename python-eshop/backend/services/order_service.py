from db.client import DatabaseClient
from models.schemas import OrderDetailResponse, OrderItemResponse, OrderSummaryResponse
from services.basket_service import BasketService, EmptyBasketError


DEFAULT_ADDRESS = {
    "street": "123 Main St.",
    "city": "Kent",
    "state": "OH",
    "country": "United States",
    "zip_code": "44240",
}


class OrderService:
    def __init__(self, db: DatabaseClient, basket_service: BasketService):
        self.db = db
        self.basket_service = basket_service

    def create_from_basket(self, buyer_id: str, basket_id: int) -> OrderDetailResponse:
        basket = self.db.get_basket_by_id(basket_id)
        if not basket or basket.buyer_id != buyer_id:
            raise ValueError("Basket not found")
        if not basket.items:
            raise EmptyBasketError("Cannot checkout with an empty basket")

        catalog_ids = [item.catalog_item_id for item in basket.items]
        catalog_items = {
            item.id: item for item in self.db.get_catalog_items_by_ids(catalog_ids)
        }

        order_items_data = []
        for basket_item in basket.items:
            catalog_item = catalog_items.get(basket_item.catalog_item_id)
            if not catalog_item:
                continue
            order_items_data.append(
                (
                    catalog_item.id,
                    catalog_item.name,
                    catalog_item.picture_uri,
                    basket_item.unit_price,
                    basket_item.quantity,
                )
            )

        order = self.db.create_order(
            buyer_id=buyer_id,
            ship_to_street=DEFAULT_ADDRESS["street"],
            ship_to_city=DEFAULT_ADDRESS["city"],
            ship_to_state=DEFAULT_ADDRESS["state"],
            ship_to_country=DEFAULT_ADDRESS["country"],
            ship_to_zip_code=DEFAULT_ADDRESS["zip_code"],
            items=order_items_data,
        )
        self.basket_service.delete_basket(basket_id)
        return self._to_detail(order)

    def list_for_user(self, buyer_id: str) -> list[OrderSummaryResponse]:
        orders = self.db.list_orders_for_buyer(buyer_id)
        return [
            OrderSummaryResponse(
                id=order.id,
                order_date=order.order_date,
                total=round(
                    sum(item.unit_price * item.units for item in order.items), 2
                ),
                item_count=sum(item.units for item in order.items),
            )
            for order in orders
        ]

    def get_detail(self, buyer_id: str, order_id: int) -> OrderDetailResponse:
        order = self.db.get_order_by_id(order_id, buyer_id)
        if not order:
            raise ValueError("Order not found")
        return self._to_detail(order)

    def _to_detail(self, order) -> OrderDetailResponse:
        items = [
            OrderItemResponse(
                id=item.id,
                catalog_item_id=item.catalog_item_id,
                product_name=item.product_name,
                picture_uri=item.picture_uri,
                unit_price=item.unit_price,
                units=item.units,
                line_total=round(item.unit_price * item.units, 2),
            )
            for item in order.items
        ]
        total = round(sum(item.line_total for item in items), 2)
        return OrderDetailResponse(
            id=order.id,
            order_date=order.order_date,
            ship_to_street=order.ship_to_street,
            ship_to_city=order.ship_to_city,
            ship_to_state=order.ship_to_state,
            ship_to_country=order.ship_to_country,
            ship_to_zip_code=order.ship_to_zip_code,
            items=items,
            total=total,
        )
