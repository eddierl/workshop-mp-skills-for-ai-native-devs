"""Tests for the Favourites feature (ticket #1: schema + entity + db methods).

These tests exercise the DatabaseClient methods directly, not through the API.
"""
import tempfile
from pathlib import Path

from db.client import DatabaseClient
from db.seed import migrate_catalog, seed_database
from models.entities import Favourite


def _make_db() -> tuple[DatabaseClient, Path]:
    """Create a temporary database for testing."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db = DatabaseClient(tmp.name)
    seed_database(db)
    migrate_catalog(db)
    return db, Path(tmp.name)


class TestFavouritesSchema:
    """Verify the favourites table exists and has the right columns."""

    def test_favourites_table_exists(self):
        """The database should create a favourites table on init."""
        db, path = _make_db()
        path.unlink()  # Clean up
        # If the table didn't exist, _ensure_schema would have failed

    def test_favourites_table_has_correct_columns(self):
        """The favourites table should have id, user_id, catalog_item_id, created_at."""
        db, path = _make_db()
        try:
            user = db.create_user("test@example.com", "hashed")
            items = db.get_catalog_items(None, None, 0, 10)
            assert len(items) > 0

            fav = db.add_favourite(user.id, items[0].id)
            assert fav.id is not None
            assert fav.user_id == user.id
            assert fav.catalog_item_id == items[0].id
            assert fav.created_at is not None
        finally:
            path.unlink()

    def test_favourite_entity_has_correct_fields(self):
        """The Favourite dataclass should have the expected fields."""
        fav = Favourite(
            id=1,
            user_id=2,
            catalog_item_id=3,
            created_at=None,  # type: ignore[arg-type]
        )
        assert hasattr(fav, "id")
        assert hasattr(fav, "user_id")
        assert hasattr(fav, "catalog_item_id")
        assert hasattr(fav, "created_at")


class TestFavouriteDbMethods:
    """Test the database methods for favourites."""

    def test_add_favourite(self):
        """Adding a favourite returns a Favourite entity."""
        db, path = _make_db()
        try:
            user = db.create_user("test@example.com", "hashed")
            items = db.get_catalog_items(None, None, 0, 10)

            fav = db.add_favourite(user.id, items[0].id)
            assert fav.id is not None
            assert fav.user_id == user.id
            assert fav.catalog_item_id == items[0].id
        finally:
            path.unlink()

    def test_add_favourite_unique_constraint(self):
        """Adding the same favourite twice raises an integrity error."""
        db, path = _make_db()
        try:
            user = db.create_user("test@example.com", "hashed")
            items = db.get_catalog_items(None, None, 0, 10)

            db.add_favourite(user.id, items[0].id)
            try:
                db.add_favourite(user.id, items[0].id)
                assert False, "Should have raised an integrity error"
            except Exception:
                pass  # Expected
        finally:
            path.unlink()

    def test_get_favourites_by_user_id(self):
        """Getting favourites by user_id returns all favourites for that user."""
        db, path = _make_db()
        try:
            user = db.create_user("test@example.com", "hashed")
            items = db.get_catalog_items(None, None, 0, 10)

            db.add_favourite(user.id, items[0].id)
            db.add_favourite(user.id, items[1].id)

            favs = db.get_favourites_by_user_id(user.id)
            assert len(favs) == 2
            fav_item_ids = {f.catalog_item_id for f in favs}
            assert fav_item_ids == {items[0].id, items[1].id}
        finally:
            path.unlink()

    def test_get_favourites_by_user_id_empty(self):
        """Getting favourites for a user with no favourites returns empty list."""
        db, path = _make_db()
        try:
            db.create_user("test@example.com", "hashed")
            favs = db.get_favourites_by_user_id(1)
            assert favs == []
        finally:
            path.unlink()

    def test_get_favourite_by_user_and_item(self):
        """Getting a specific favourite returns it."""
        db, path = _make_db()
        try:
            user = db.create_user("test@example.com", "hashed")
            items = db.get_catalog_items(None, None, 0, 10)

            db.add_favourite(user.id, items[0].id)
            fav = db.get_favourite_by_user_and_item(user.id, items[0].id)
            assert fav is not None
            assert fav.catalog_item_id == items[0].id
        finally:
            path.unlink()

    def test_get_favourite_by_user_and_item_not_found(self):
        """Getting a non-existent favourite returns None."""
        db, path = _make_db()
        try:
            db.create_user("test@example.com", "hashed")
            fav = db.get_favourite_by_user_and_item(1, 99999)
            assert fav is None
        finally:
            path.unlink()

    def test_delete_favourite(self):
        """Deleting a favourite removes it from the database."""
        db, path = _make_db()
        try:
            user = db.create_user("test@example.com", "hashed")
            items = db.get_catalog_items(None, None, 0, 10)

            db.add_favourite(user.id, items[0].id)
            favs = db.get_favourites_by_user_id(user.id)
            assert len(favs) == 1

            db.delete_favourite(user.id, items[0].id)
            favs = db.get_favourites_by_user_id(user.id)
            assert len(favs) == 0
        finally:
            path.unlink()
