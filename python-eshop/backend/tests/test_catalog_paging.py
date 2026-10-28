import pytest

from db.client import DatabaseClient


def test_page_past_the_end_lands_on_the_last_page(client):
    first = client.get("/api/catalog/items").json()
    last_page = first["total_pages"]

    body = client.get("/api/catalog/items", params={"page": 999}).json()

    assert body["page"] == last_page
    assert body["items"]
    assert body["page"] <= body["total_pages"]


@pytest.mark.parametrize("page", [0, -3])
def test_page_zero_or_negative_is_the_first_page(client, page):
    response = client.get("/api/catalog/items", params={"page": page})

    assert response.status_code == 200
    assert response.json()["page"] == 1


def test_filter_that_matches_nothing_is_still_empty(client):
    body = client.get("/api/catalog/items", params={"brand_id": 9999}).json()

    assert body["items"] == []
    assert body["total_count"] == 0
    assert body["page"] == 1


def test_paging_through_the_seeded_catalog_is_unchanged(client):
    one = client.get("/api/catalog/items", params={"page": 1}).json()
    two = client.get("/api/catalog/items", params={"page": 2}).json()

    ids = [item["id"] for item in one["items"] + two["items"]]
    assert ids == sorted(set(ids))
    assert len(ids) == one["total_count"]


def test_zero_id_filter_is_a_filter(tmp_path):
    db = DatabaseClient(str(tmp_path / "zero.db"))
    with db._connection() as conn:
        conn.execute("INSERT INTO catalog_brands (id, brand) VALUES (0, 'Zero'), (1, 'One')")
        conn.execute("INSERT INTO catalog_types (id, type) VALUES (0, 'Zero'), (1, 'One')")
        conn.execute(
            """
            INSERT INTO catalog_items
                (name, description, price, picture_uri, catalog_brand_id, catalog_type_id)
            VALUES ('a', 'a', 1, '/x.png', 0, 0), ('b', 'b', 1, '/x.png', 1, 1)
            """
        )

    assert db.count_catalog_items(brand_id=0) == 1
    assert db.count_catalog_items(type_id=0) == 1
    assert [i.name for i in db.get_catalog_items(0, None, 0, 10)] == ["a"]
    assert [i.name for i in db.get_catalog_items(None, 0, 0, 10)] == ["a"]
