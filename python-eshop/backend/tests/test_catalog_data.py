import sqlite3

from db.client import DatabaseClient
from db.seed import migrate_catalog, seed_database


def test_every_type_in_the_filter_has_products(client):
    for catalog_type in client.get("/api/catalog/types").json():
        body = client.get("/api/catalog/items", params={"type_id": catalog_type["id"]}).json()
        assert body["total_count"] > 0, catalog_type["type"]


def test_pin_products_are_listed_as_pins(client):
    types = {t["type"]: t["id"] for t in client.get("/api/catalog/types").json()}
    assert "Sheet" not in types

    pins = client.get("/api/catalog/items", params={"type_id": types["Pin"]}).json()
    names = sorted(item["name"] for item in pins["items"])
    assert names == [".NET Foundation Pin", "Cup<T> Pin", "Roslyn Red Pin"]


def test_older_databases_are_migrated(tmp_path):
    db = DatabaseClient(str(tmp_path / "old.db"))
    seed_database(db)
    with sqlite3.connect(db.database_path) as conn:
        conn.execute("UPDATE catalog_types SET type = 'Sheet' WHERE type = 'Pin'")
        conn.execute("UPDATE catalog_items SET name = 'Cup<T> Sheet' WHERE name = 'Cup<T> Pin'")
        conn.execute("INSERT INTO catalog_types (type) VALUES ('USB Memory Stick')")

    migrate_catalog(db)
    migrate_catalog(db)

    assert sorted(t.type for t in db.list_catalog_types()) == ["Mug", "Pin", "T-Shirt"]
    with sqlite3.connect(db.database_path) as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM catalog_items WHERE name = 'Cup<T> Pin'"
        ).fetchone()[0] == 1
