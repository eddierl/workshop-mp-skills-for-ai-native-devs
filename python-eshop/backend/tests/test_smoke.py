from config import settings


def test_catalog_is_readable_without_auth(client):
    response = client.get("/api/catalog/items")

    assert response.status_code == 200
    body = response.json()
    assert body["total_count"] > 0
    assert len(body["items"]) == settings.catalog_page_size


def test_add_to_basket_round_trip(client, anon_headers):
    added = client.post(
        "/api/basket/items",
        json={"catalog_item_id": 1, "quantity": 2},
        headers=anon_headers,
    )
    assert added.status_code == 200

    basket = client.get("/api/basket", headers=anon_headers).json()
    assert basket["item_count"] == 2
    assert basket["items"][0]["catalog_item_id"] == 1


def test_suite_does_not_touch_the_dev_database(client, tmp_path):
    assert settings.database_path.startswith(str(tmp_path))
