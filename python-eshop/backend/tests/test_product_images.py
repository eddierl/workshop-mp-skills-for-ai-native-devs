import tempfile
import unittest
from pathlib import Path

from db.client import DatabaseClient
from db.ensure_assets import PRODUCT_IMAGE_COUNT, ensure_product_images
from db.seed import sync_picture_uris


class EnsureProductImagesTests(unittest.TestCase):
    def test_creates_missing_svgs_offline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            products_dir = Path(temp_dir)

            ensure_product_images(products_dir)

            for number in range(1, PRODUCT_IMAGE_COUNT + 1):
                svg_path = products_dir / f"{number}.svg"
                self.assertTrue(svg_path.is_file(), f"missing {svg_path.name}")
                self.assertIn(f"#{number}", svg_path.read_text(encoding="utf-8"))

    def test_does_not_overwrite_existing_svgs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            products_dir = Path(temp_dir)
            existing = products_dir / "1.svg"
            existing.write_text("<svg>custom</svg>", encoding="utf-8")

            ensure_product_images(products_dir)

            self.assertEqual(existing.read_text(encoding="utf-8"), "<svg>custom</svg>")


class SyncPictureUrisTests(unittest.TestCase):
    def test_migrates_png_paths_to_svg(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(Path(temp_dir) / "test.db")
            db = DatabaseClient(db_path)

            with db._connection() as conn:
                conn.execute("INSERT INTO catalog_brands (brand) VALUES ('Azure')")
                conn.execute("INSERT INTO catalog_types (type) VALUES ('Mug')")
                conn.execute(
                    """
                    INSERT INTO catalog_items (
                        name, description, price, picture_uri,
                        catalog_brand_id, catalog_type_id
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "Test Mug",
                        "Test Mug",
                        9.99,
                        "/static/images/products/1.png",
                        1,
                        1,
                    ),
                )
                conn.execute(
                    """
                    INSERT INTO orders (
                        buyer_id, order_date, ship_to_street, ship_to_city,
                        ship_to_state, ship_to_country, ship_to_zip_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    ("buyer-1", "2026-01-01", "1 Main", "Perth", "WA", "AU", "6000"),
                )
                conn.execute(
                    """
                    INSERT INTO order_items (
                        order_id, catalog_item_id, product_name, picture_uri,
                        unit_price, units
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (1, 1, "Test Mug", "/static/images/products/1.png", 9.99, 1),
                )

            sync_picture_uris(db)

            with db._connection() as conn:
                catalog_uri = conn.execute(
                    "SELECT picture_uri FROM catalog_items WHERE id = 1"
                ).fetchone()["picture_uri"]
                order_uri = conn.execute(
                    "SELECT picture_uri FROM order_items WHERE id = 1"
                ).fetchone()["picture_uri"]

            self.assertEqual(catalog_uri, "/static/images/products/1.svg")
            self.assertEqual(order_uri, "/static/images/products/1.svg")


if __name__ == "__main__":
    unittest.main()
