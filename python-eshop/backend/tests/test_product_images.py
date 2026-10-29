from db.ensure_assets import missing_product_images


def test_every_product_image_ships_with_the_repo():
    assert missing_product_images() == []


def test_every_catalog_picture_is_served(client):
    items = []
    page = 1
    while True:
        body = client.get("/api/catalog/items", params={"page": page}).json()
        items.extend(body["items"])
        if page >= body["total_pages"]:
            break
        page += 1

    assert items
    for item in items:
        response = client.get(item["picture_uri"])
        assert response.status_code == 200, item["picture_uri"]
        assert response.headers["content-type"] == "image/png"


def test_basket_lines_carry_a_served_picture(client, anon_headers):
    basket = client.post(
        "/api/basket/items", json={"catalog_item_id": 3}, headers=anon_headers
    ).json()

    picture = basket["items"][0]["picture_uri"]
    assert client.get(picture).status_code == 200
