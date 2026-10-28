# Favourites Feature Specification

## Background

Signed-in shoppers want to save products they're interested in and revisit them later. This is a common e-commerce pattern (heart/favourite icon on product cards, a dedicated favourites page).

## Requirements

### Functional

1. **Add to favourites**: A signed-in user can add a product to their favourites list.
2. **Remove from favourites**: A signed-in user can remove a product from their favourites list.
3. **View favourites**: A signed-in user can see all their saved products on a dedicated page.
4. **Catalog enrichment**: When browsing the catalog, each product card shows whether the current user has favourited it (a heart icon).
5. **Empty state**: The favourites page shows a friendly "You haven't saved any products yet" message with a "Browse the catalog" link when the list is empty.
6. **Pruning**: If a product is deleted from the catalog, any existing favourites to it are silently removed.

### Non-functional

- Only signed-in users can use favourites (no anonymous support).
- A user can have at most one favourite per product (enforced at the database level).
- All timestamps stored as timezone-aware UTC.
- HTTP status codes: 201 for successful add, 204 for successful remove, 401 for unauthenticated, 404 for non-existent product.

## API Design

### POST /api/favourites/{product_id}

Add a product to the current user's favourites.

- **Auth**: Required (Bearer token).
- **Path param**: `product_id` (integer).
- **Response**: 201 Created with the favourite object, or 404 if the product doesn't exist.

### GET /api/favourites

List the current user's favourites.

- **Auth**: Required (Bearer token).
- **Response**: 200 OK with a list of favourite objects (same format as catalog items, enriched with `favourited_at`).

### DELETE /api/favourites/{product_id}

Remove a product from the current user's favourites.

- **Auth**: Required (Bearer token).
- **Path param**: `product_id` (integer).
- **Response**: 204 No Content, or 404 if the product isn't in their favourites.

### Catalog response enrichment

The existing `CatalogItemResponse` gains an optional field:

```python
class CatalogItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    picture_uri: str
    catalog_brand_id: int
    catalog_type_id: int
    brand_name: str | None = None
    type_name: str | None = None
    is_favourite: bool = False  # NEW: only meaningful when authenticated
```

When the request is unauthenticated, `is_favourite` is always `False`.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS favourites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    catalog_item_id INTEGER NOT NULL REFERENCES catalog_items(id),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(user_id, catalog_item_id)
);
```

## Entity

```python
@dataclass
class Favourite:
    id: int
    user_id: int
    catalog_item_id: int
    created_at: datetime
```

## Frontend

- **Route**: `/favourites` — dedicated page listing the user's saved products.
- **Catalog cards**: Each product card in catalog/listing views shows a heart icon that reflects the `is_favourite` flag. Clicking toggles the favourite (calls POST or DELETE).
- **Empty state**: When the favourites list is empty, display a message with a "Browse the catalog" button.

## Error Handling

| Scenario | Status | Body |
|----------|--------|------|
| Unauthenticated | 401 | `{"detail": "Not authenticated"}` |
| Product doesn't exist (POST) | 404 | `{"detail": "Product not found"}` |
| Not a favourite (DELETE) | 404 | `{"detail": "Not in favourites"}` |
| Already a favourite (POST) | 409 | `{"detail": "Already in favourites"}` |

## Edge Cases

- **Product removed from catalog**: Favourites to that product are pruned on the next catalog query (or via a background cleanup). For simplicity, pruned silently on catalog listing.
- **Concurrent requests**: SQLite handles single-writer concurrency. Two rapid "add" requests for the same product will result in an integrity error, caught and returned as 409.
