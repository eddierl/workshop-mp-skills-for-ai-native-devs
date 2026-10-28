import pytest

from db.client import DatabaseClient


def fill_basket(client, headers):
    client.post("/api/basket/items", json={"catalog_item_id": 1, "quantity": 2}, headers=headers)
    return client.post(
        "/api/basket/items", json={"catalog_item_id": 3}, headers=headers
    ).json()


def checkout(client, headers, basket_id):
    return client.post("/api/orders", json={"basket_id": basket_id}, headers=headers)


def test_checkout_records_the_order_and_empties_the_basket(client, demo_headers):
    basket = fill_basket(client, demo_headers)

    order = checkout(client, demo_headers, basket["id"]).json()

    assert len(order["items"]) == len(basket["items"])
    assert order["total"] == basket["total"]
    assert client.get("/api/basket", headers=demo_headers).json()["items"] == []


def test_failure_mid_checkout_leaves_no_order_and_the_basket_intact(
    client, demo_headers, monkeypatch
):
    basket = fill_basket(client, demo_headers)

    def fail(*args, **kwargs):
        raise RuntimeError("simulated crash while emptying the basket")

    with monkeypatch.context() as patch:
        patch.setattr(DatabaseClient, "_delete_basket_rows", fail)
        with pytest.raises(RuntimeError):
            checkout(client, demo_headers, basket["id"])

    assert client.get("/api/orders", headers=demo_headers).json() == []
    after = client.get("/api/basket", headers=demo_headers).json()
    assert after["id"] == basket["id"]
    assert after["item_count"] == basket["item_count"]

    assert checkout(client, demo_headers, basket["id"]).status_code == 200
    assert len(client.get("/api/orders", headers=demo_headers).json()) == 1


def test_checking_out_the_same_basket_twice_makes_one_order(client, demo_headers):
    basket = fill_basket(client, demo_headers)

    assert checkout(client, demo_headers, basket["id"]).status_code == 200
    assert checkout(client, demo_headers, basket["id"]).status_code == 404
    assert len(client.get("/api/orders", headers=demo_headers).json()) == 1
