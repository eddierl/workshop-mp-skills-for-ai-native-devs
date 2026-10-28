"""Business logic for the Favourites feature (tickets #2 and #3)."""
from db.client import DatabaseClient
from models.schemas import FavouriteResponse


class FavouriteService:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def add_favourite(self, user_id: int, catalog_item_id: int) -> FavouriteResponse:
        """Add a product to the user's favourites.

        Raises:
            ValueError: If the catalog item does not exist.
            sqlite3.IntegrityError: If the user already favourited this item.
        """
        catalog_item = self.db.get_catalog_item_by_id(catalog_item_id)
        if not catalog_item:
            raise ValueError("Catalog item not found")

        fav = self.db.add_favourite(user_id, catalog_item_id)
        return self._to_response(fav)

    def get_favourites(self, user_id: int) -> list[FavouriteResponse]:
        """Return all of a user's favourites with catalog enrichment."""
        favs = self.db.get_favourites_by_user_id(user_id)
        return [self._to_response(fav) for fav in favs]

    def get_favourite(self, user_id: int, catalog_item_id: int) -> FavouriteResponse | None:
        """Return a single favourite if it exists."""
        fav = self.db.get_favourite_by_user_and_item(user_id, catalog_item_id)
        if fav is None:
            return None
        return self._to_response(fav)

    def remove_favourite(self, user_id: int, catalog_item_id: int) -> None:
        """Remove a product from the user's favourites."""
        self.db.delete_favourite(user_id, catalog_item_id)

    def _to_response(self, fav) -> FavouriteResponse:
        """Build a FavouriteResponse with catalog item data."""
        catalog_item = self.db.get_catalog_item_by_id(fav.catalog_item_id)
        if not catalog_item:
            # Product was deleted — skip it (pruned silently per spec)
            return None  # type: ignore[return-value]

        return FavouriteResponse(
            id=fav.id,
            user_id=fav.user_id,
            catalog_item_id=fav.catalog_item_id,
            created_at=fav.created_at,
            name=catalog_item.name,
            price=catalog_item.price,
            picture_uri=catalog_item.picture_uri,
        )
