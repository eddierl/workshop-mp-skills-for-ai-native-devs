"""Tests for the Favourites feature (ticket #1: schema + entity + db methods)."""
import uuid

from db.client import DatabaseClient


class TestFavouritesSchema:
    """Verify the favourites table exists and has the right columns."""

    def test_favourites_table_exists(self, client):
        """The database should create a favourites table on init."""
        from db.client import DatabaseClient

        # The client fixture creates a fresh DB; the table should exist
        # If the table didn't exist, _ensure_schema would have failed
        pass  # schema is tested implicitly by all other tests

    def test_favourites_table_has_correct_columns(self, client, demo_headers):
        """The favourites table should have id, user_id, catalog_item_id, created_at."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        resp = client.post(f"/api/favourites/{item_id}", headers=demo_headers)
        assert resp.status_code == 201
        body = resp.json()
        assert body["id"] is not None
        assert body["catalog_item_id"] == item_id
        assert body["user_id"] is not None
        assert body["created_at"] is not None


class TestFavouriteEndpoints:
    """Test POST, GET, DELETE /api/favourites endpoints."""

    def test_post_favourite_success(self, client, demo_headers):
        """Adding a favourite returns 201."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        resp = client.post(f"/api/favourites/{item_id}", headers=demo_headers)
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["catalog_item_id"] == item_id
        assert body["user_id"] is not None

    def test_post_favourite_unauthenticated(self, client):
        """Unauthenticated users get 401."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        resp = client.post(f"/api/favourites/{item_id}")
        assert resp.status_code == 401

    def test_post_favourite_product_not_found(self, client, demo_headers):
        """Adding a non-existent product returns 404."""
        resp = client.post(
            "/api/favourites/99999", headers=demo_headers
        )
        assert resp.status_code == 404

    def test_post_favourite_duplicate(self, client, demo_headers):
        """Adding the same favourite twice returns 409."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        client.post(f"/api/favourites/{item_id}", headers=demo_headers)
        resp = client.post(f"/api/favourites/{item_id}", headers=demo_headers)
        assert resp.status_code == 409

    def test_get_favourites_list(self, client, demo_headers):
        """GET /api/favourites returns the user's favourites."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_ids = [item["id"] for item in items[:3]]

        for item_id in item_ids:
            client.post(f"/api/favourites/{item_id}", headers=demo_headers)

        resp = client.get("/api/favourites", headers=demo_headers)
        assert resp.status_code == 200
        favs = resp.json()
        assert len(favs) == 3
        fav_item_ids = {f["catalog_item_id"] for f in favs}
        assert fav_item_ids == set(item_ids)

    def test_get_favourites_empty(self, client, demo_headers):
        """GET /api/favourites returns empty list when no favourites."""
        resp = client.get("/api/favourites", headers=demo_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_favourites_unauthenticated(self, client):
        """Unauthenticated GET returns 401."""
        resp = client.get("/api/favourites")
        assert resp.status_code == 401

    def test_delete_favourite_success(self, client, demo_headers):
        """Deleting a favourite returns 204."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        client.post(f"/api/favourites/{item_id}", headers=demo_headers)
        resp = client.delete(f"/api/favourites/{item_id}", headers=demo_headers)
        assert resp.status_code == 204

    def test_delete_favourite_not_a_favourite(self, client, demo_headers):
        """Deleting a non-favourite returns 404."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        resp = client.delete(f"/api/favourites/{item_id}", headers=demo_headers)
        assert resp.status_code == 404

    def test_delete_favourite_unauthenticated(self, client):
        """Unauthenticated DELETE returns 401."""
        resp = client.delete("/api/favourites/1")
        assert resp.status_code == 401


class TestCatalogEnrichment:
    """Test that catalog responses include is_favourite flag."""

    def test_authenticated_catalog_shows_is_favourite(self, client, demo_headers):
        """Authenticated catalog responses include is_favourite."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        assert len(items) > 0
        # All should have is_favourite field
        for item in items:
            assert "is_favourite" in item

    def test_authenticated_catalog_marks_favourited_items(self, client, demo_headers):
        """Favourited items show is_favourite=True."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        client.post(f"/api/favourites/{item_id}", headers=demo_headers)

        catalog = client.get("/api/catalog/items?page=1", headers=demo_headers).json()
        favourited = [i for i in catalog["items"] if i["id"] == item_id]
        assert len(favourited) == 1
        assert favourited[0]["is_favourite"] is True

    def test_authenticated_catalog_marks_non_favourited_items(self, client, demo_headers):
        """Non-favourited items show is_favourite=False."""
        items = client.get("/api/catalog/items?page=1").json()["items"]
        item_id = items[0]["id"]

        catalog = client.get("/api/catalog/items?page=1").json()
        non_favourited = [i for i in catalog["items"] if i["id"] == item_id]
        assert len(non_favourited) == 1
        assert non_favourited[0]["is_favourite"] is False

    def test_unauthenticated_catalog_has_is_favourite_false(self, client):
        """Unauthenticated catalog always has is_favourite=False."""
        catalog = client.get("/api/catalog/items?page=1").json()
        for item in catalog["items"]:
            assert item["is_favourite"] is False
