import sqlite3
from datetime import datetime, timedelta, timezone

from config import settings


def place_order(client, headers):
    basket = client.post(
        "/api/basket/items", json={"catalog_item_id": 1}, headers=headers
    ).json()
    response = client.post("/api/orders", json={"basket_id": basket["id"]}, headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


def test_order_date_is_utc_and_matches_when_it_was_placed(client, demo_headers):
    before = datetime.now(timezone.utc)
    order = place_order(client, demo_headers)
    after = datetime.now(timezone.utc)

    placed = datetime.fromisoformat(order["order_date"].replace("Z", "+00:00"))
    assert placed.utcoffset() == timedelta(0)
    assert before <= placed <= after

    listed = client.get("/api/orders", headers=demo_headers).json()[0]["order_date"]
    assert datetime.fromisoformat(listed.replace("Z", "+00:00")) == placed


def test_orders_stored_without_a_timezone_are_read_as_utc(client, demo_headers):
    order = place_order(client, demo_headers)
    with sqlite3.connect(settings.database_path) as conn:
        conn.execute(
            "UPDATE orders SET order_date = '2026-08-26T11:37:12.671981' WHERE id = ?",
            (order["id"],),
        )

    detail = client.get(f"/api/orders/{order['id']}", headers=demo_headers).json()

    read = datetime.fromisoformat(detail["order_date"].replace("Z", "+00:00"))
    assert read == datetime(2026, 8, 26, 11, 37, 12, 671981, tzinfo=timezone.utc)
