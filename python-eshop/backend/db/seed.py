from db.client import DatabaseClient
from services.passwords import hash_password

BRANDS = ["Azure", ".NET", "Visual Studio", "SQL Server", "Other"]
TYPES = ["Mug", "T-Shirt", "Pin"]

PRODUCTS = [
    (2, 2, ".NET Bot Black Sweatshirt", ".NET Bot Black Sweatshirt", 19.5, 1),
    (1, 2, ".NET Black & White Mug", ".NET Black & White Mug", 8.50, 2),
    (2, 5, "Prism White T-Shirt", "Prism White T-Shirt", 12.0, 3),
    (2, 2, ".NET Foundation Sweatshirt", ".NET Foundation Sweatshirt", 12.0, 4),
    (3, 5, "Roslyn Red Pin", "Roslyn Red Pin", 8.5, 5),
    (2, 2, ".NET Blue Sweatshirt", ".NET Blue Sweatshirt", 12.0, 6),
    (2, 5, "Roslyn Red T-Shirt", "Roslyn Red T-Shirt", 12.0, 7),
    (2, 5, "Kudu Purple Sweatshirt", "Kudu Purple Sweatshirt", 8.5, 8),
    (1, 5, "Cup<T> White Mug", "Cup<T> White Mug", 12.0, 9),
    (3, 2, ".NET Foundation Pin", ".NET Foundation Pin", 12.0, 10),
    (3, 2, "Cup<T> Pin", "Cup<T> Pin", 8.5, 11),
    (2, 5, "Prism White TShirt", "Prism White TShirt", 12.0, 12),
]

DEMO_EMAIL = "demouser@perthai.com.au"
DEMO_PASSWORD = "Pass@word1"


def seed_database(db: DatabaseClient) -> None:
    if db.has_catalog_data():
        return

    with db._connection() as conn:
        for brand in BRANDS:
            conn.execute("INSERT INTO catalog_brands (brand) VALUES (?)", (brand,))

        for catalog_type in TYPES:
            conn.execute("INSERT INTO catalog_types (type) VALUES (?)", (catalog_type,))

        for type_id, brand_id, name, description, price, image_num in PRODUCTS:
            picture_uri = f"/static/images/products/{image_num}.png"
            conn.execute(
                """
                INSERT INTO catalog_items (
                    name, description, price, picture_uri,
                    catalog_brand_id, catalog_type_id
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, description, price, picture_uri, brand_id, type_id),
            )

        password_hash = hash_password(DEMO_PASSWORD)
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (DEMO_EMAIL, password_hash),
        )


RENAMED_PRODUCTS = {
    "Roslyn Red Sheet": "Roslyn Red Pin",
    ".NET Foundation Sheet": ".NET Foundation Pin",
    "Cup<T> Sheet": "Cup<T> Pin",
}


def migrate_catalog(db: DatabaseClient) -> None:
    """Bring a database seeded by an older version in line with the seed data.

    The three "Sheet" products were always pin badges (their images show
    pins), and "USB Memory Stick" was a type with no products.
    """
    with db._connection() as conn:
        conn.execute("UPDATE catalog_types SET type = 'Pin' WHERE type = 'Sheet'")
        for old_name, new_name in RENAMED_PRODUCTS.items():
            conn.execute(
                "UPDATE catalog_items SET name = ?, description = ? WHERE name = ?",
                (new_name, new_name, old_name),
            )
        conn.execute(
            """
            DELETE FROM catalog_types
            WHERE type = 'USB Memory Stick'
              AND id NOT IN (SELECT catalog_type_id FROM catalog_items)
            """
        )


def sync_picture_uris(db: DatabaseClient) -> None:
    """Update legacy .svg paths to .png after product images are added."""
    with db._connection() as conn:
        conn.execute(
            """
            UPDATE catalog_items
            SET picture_uri = REPLACE(picture_uri, '.svg', '.png')
            WHERE picture_uri LIKE '%.svg'
            """
        )
        conn.execute(
            """
            UPDATE order_items
            SET picture_uri = REPLACE(picture_uri, '.svg', '.png')
            WHERE picture_uri LIKE '%.svg'
            """
        )
