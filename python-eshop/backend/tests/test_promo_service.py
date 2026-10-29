"""Tests for the PromoService (Ticket 9: Promo validation service).

These tests exercise the API through the client fixture against a throwaway
database, seeding promo codes and checking order totals.
"""
from dependencies import get_db
from db.seed import seed_promo_codes


def fill_basket(client, headers):
    """Add two items to the basket and return the basket as a dict."""
    client.post("/api/basket/items", json={"catalog_item_id": 1, "quantity": 2}, headers=headers)
    return client.post("/api/basket/items", json={"catalog_item_id": 3}, headers=headers).json()


def checkout(client, headers, basket_id, coupon_code=None):
    """Place an order, optionally with a coupon_code."""
    body = {"basket_id": basket_id}
    if coupon_code is not None:
        body["coupon_code"] = coupon_code
    return client.post("/api/orders", json=body, headers=headers)


class TestValidPercentageCoupon:
    """SE20: 20% off, no minimum."""

    def test_applies_percentage_discount_above_minimum(self, client, demo_headers):
        seed_promo_codes(get_db())
        basket = fill_basket(client, demo_headers)
        order = checkout(client, demo_headers, basket["id"], "SE20").json()
        # Debug: check what's in the order
        print(f'Order: {order}')
        print(f'Discount: {order.get("discount_amount")}')
        assert order["discount_amount"] is not None
        assert order["discount_amount"] > 0
        assert order["total"] < basket["total"]
        # 20% off: total should be 80% of basket total (rounded)
        expected = round(basket["total"] * 0.80, 2)
        assert order["total"] == expected


class TestValidFixedCoupon:
    """FLAT10: $10 off, $50 minimum."""

    def test_applies_fixed_discount_above_minimum(self, client, demo_headers):
        seed_promo_codes(get_db())
        basket = fill_basket(client, demo_headers)
        # Ensure basket total is >= $50
        assert basket["total"] >= 50
        order = checkout(client, demo_headers, basket["id"], "FLAT10").json()
        assert order["discount_amount"] == 10.0
        assert order["total"] == round(basket["total"] - 10.0, 2)

    def test_fixed_coupon_rejected_when_below_minimum(self, client, demo_headers):
        seed_promo_codes(get_db())
        # Create a small basket (below $50 minimum for FLAT10)
        # Item 1 (catalog_item_id=1) costs $8.50
        client.post("/api/basket/items", json={"catalog_item_id": 1, "quantity": 1}, headers=demo_headers)
        small_basket = client.get("/api/basket", headers=demo_headers).json()
        assert small_basket["total"] < 50
        order = checkout(client, demo_headers, small_basket["id"], "FLAT10").json()
        assert order["discount_amount"] is None
        assert order["total"] == small_basket["total"]


class TestInvalidCoupon:
    """Various invalid coupon scenarios."""

    def test_invalid_code_placed_at_full_price(self, client, demo_headers):
        fill_basket(client, demo_headers)
        order = checkout(client, demo_headers, 1, "BADCODE").json()
        assert order["discount_amount"] is None

    def test_expired_coupon_placed_at_full_price(self, client, demo_headers):
        db = client.db
        # Insert an expired coupon directly
        with db._connection() as conn:
            conn.execute(
                """
                INSERT INTO promo_codes (code, type, value, expiry_date)
                VALUES ('EXPIRED', 'percentage', 10.0, '2020-01-01T00:00:00')
                """
            )
        basket = fill_basket(client, demo_headers)
        order = checkout(client, demo_headers, basket["id"], "EXPIRED").json()
        assert order["discount_amount"] is None

    def test_redeemed_coupon_placed_at_full_price(self, client, demo_headers):
        db = client.db
        # Insert a redeemed coupon directly
        with db._connection() as conn:
            conn.execute(
                """
                INSERT INTO promo_codes (code, type, value, is_redeemed)
                VALUES ('USED', 'percentage', 15.0, 1)
                """
            )
        basket = fill_basket(client, demo_headers)
        order = checkout(client, demo_headers, basket["id"], "USED").json()
        assert order["discount_amount"] is None

    def test_inactive_coupon_placed_at_full_price(self, client, demo_headers):
        db = client.db
        # Insert an inactive coupon directly
        with db._connection() as conn:
            conn.execute(
                """
                INSERT INTO promo_codes (code, type, value, is_active)
                VALUES ('INACTIVE', 'percentage', 10.0, 0)
                """
            )
        basket = fill_basket(client, demo_headers)
        order = checkout(client, demo_headers, basket["id"], "INACTIVE").json()
        assert order["discount_amount"] is None


class TestEmptyBasket:
    """Coupon with empty basket should still raise empty basket error."""

    def test_empty_basket_rejected_even_with_valid_coupon(self, client, demo_headers):
        seed_promo_codes(get_db())
        # Get or create an empty basket
        empty_basket = client.get("/api/basket", headers=demo_headers).json()
        response = checkout(client, demo_headers, empty_basket["id"], "SE20")
        assert response.status_code == 400


class TestDiscountCapping:
    """Discount should never make the order total negative."""

    def test_discount_capped_at_zero_total(self, client, demo_headers):
        db = client.db
        # Insert a huge percentage coupon
        with db._connection() as conn:
            conn.execute(
                """
                INSERT INTO promo_codes (code, type, value)
                VALUES ('HUGE', 'percentage', 200.0)
                """
            )
        # Create a small basket (item 1 costs $8.50, add just one)
        client.post("/api/basket/items", json={"catalog_item_id": 1, "quantity": 1}, headers=demo_headers)
        small_basket = client.get("/api/basket", headers=demo_headers).json()
        order = checkout(client, demo_headers, small_basket["id"], "HUGE").json()
        # Total should be 0, not negative
        assert order["total"] == 0.0
        assert order["discount_amount"] == round(small_basket["total"], 2)
