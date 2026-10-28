import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from models.entities import (
    Basket,
    BasketItem,
    CatalogBrand,
    CatalogItem,
    CatalogType,
    Order,
    OrderItem,
    User,
)


class DatabaseClient:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self._ensure_schema()

    @contextmanager
    def _connection(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _ensure_schema(self):
        schema_path = Path(__file__).parent / "schema.sql"
        with self._connection() as conn:
            conn.executescript(schema_path.read_text(encoding="utf-8"))

    def count_catalog_items(
        self, brand_id: int | None = None, type_id: int | None = None
    ) -> int:
        query = "SELECT COUNT(*) FROM catalog_items WHERE 1=1"
        params: list = []
        if brand_id:
            query += " AND catalog_brand_id = ?"
            params.append(brand_id)
        if type_id:
            query += " AND catalog_type_id = ?"
            params.append(type_id)
        with self._connection() as conn:
            row = conn.execute(query, params).fetchone()
            return int(row[0])

    def get_catalog_items(
        self,
        brand_id: int | None,
        type_id: int | None,
        offset: int,
        limit: int,
    ) -> list[CatalogItem]:
        query = """
            SELECT ci.*, cb.brand AS brand_name, ct.type AS type_name
            FROM catalog_items ci
            JOIN catalog_brands cb ON cb.id = ci.catalog_brand_id
            JOIN catalog_types ct ON ct.id = ci.catalog_type_id
            WHERE 1=1
        """
        params: list = []
        if brand_id:
            query += " AND ci.catalog_brand_id = ?"
            params.append(brand_id)
        if type_id:
            query += " AND ci.catalog_type_id = ?"
            params.append(type_id)
        query += " ORDER BY ci.id LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [_row_to_catalog_item(row) for row in rows]

    def get_catalog_item_by_id(self, item_id: int) -> CatalogItem | None:
        query = """
            SELECT ci.*, cb.brand AS brand_name, ct.type AS type_name
            FROM catalog_items ci
            JOIN catalog_brands cb ON cb.id = ci.catalog_brand_id
            JOIN catalog_types ct ON ct.id = ci.catalog_type_id
            WHERE ci.id = ?
        """
        with self._connection() as conn:
            row = conn.execute(query, (item_id,)).fetchone()
            return _row_to_catalog_item(row) if row else None

    def get_catalog_items_by_ids(self, item_ids: list[int]) -> list[CatalogItem]:
        if not item_ids:
            return []
        placeholders = ",".join("?" * len(item_ids))
        query = f"""
            SELECT ci.*, cb.brand AS brand_name, ct.type AS type_name
            FROM catalog_items ci
            JOIN catalog_brands cb ON cb.id = ci.catalog_brand_id
            JOIN catalog_types ct ON ct.id = ci.catalog_type_id
            WHERE ci.id IN ({placeholders})
        """
        with self._connection() as conn:
            rows = conn.execute(query, item_ids).fetchall()
            return [_row_to_catalog_item(row) for row in rows]

    def list_catalog_brands(self) -> list[CatalogBrand]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT id, brand FROM catalog_brands ORDER BY brand"
            ).fetchall()
            return [CatalogBrand(id=row["id"], brand=row["brand"]) for row in rows]

    def list_catalog_types(self) -> list[CatalogType]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT id, type FROM catalog_types ORDER BY type"
            ).fetchall()
            return [CatalogType(id=row["id"], type=row["type"]) for row in rows]

    def get_user_by_email(self, email: str) -> User | None:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT id, email, password_hash FROM users WHERE email = ?",
                (email.lower(),),
            ).fetchone()
            if not row:
                return None
            return User(
                id=row["id"], email=row["email"], password_hash=row["password_hash"]
            )

    def create_user(self, email: str, password_hash: str) -> User:
        with self._connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email.lower(), password_hash),
            )
            return User(id=cursor.lastrowid, email=email.lower(), password_hash=password_hash)

    def get_basket_by_buyer_id(self, buyer_id: str) -> Basket | None:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT id, buyer_id FROM baskets WHERE buyer_id = ?", (buyer_id,)
            ).fetchone()
            if not row:
                return None
            return self._load_basket(conn, row["id"], row["buyer_id"])

    def get_basket_by_id(self, basket_id: int) -> Basket | None:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT id, buyer_id FROM baskets WHERE id = ?", (basket_id,)
            ).fetchone()
            if not row:
                return None
            return self._load_basket(conn, row["id"], row["buyer_id"])

    def create_basket(self, buyer_id: str) -> Basket:
        with self._connection() as conn:
            cursor = conn.execute(
                "INSERT INTO baskets (buyer_id) VALUES (?)", (buyer_id,)
            )
            return Basket(id=cursor.lastrowid, buyer_id=buyer_id, items=[])

    def add_basket_item(
        self, basket_id: int, catalog_item_id: int, unit_price: float, quantity: int
    ) -> None:
        with self._connection() as conn:
            existing = conn.execute(
                """
                SELECT id, quantity FROM basket_items
                WHERE basket_id = ? AND catalog_item_id = ?
                """,
                (basket_id, catalog_item_id),
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE basket_items SET quantity = quantity + ? WHERE id = ?",
                    (quantity, existing["id"]),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO basket_items (basket_id, catalog_item_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (basket_id, catalog_item_id, quantity, unit_price),
                )

    def update_basket_item_quantity(self, item_id: int, quantity: int) -> None:
        with self._connection() as conn:
            if quantity <= 0:
                conn.execute("DELETE FROM basket_items WHERE id = ?", (item_id,))
            else:
                conn.execute(
                    "UPDATE basket_items SET quantity = ? WHERE id = ?", (quantity, item_id)
                )

    def remove_empty_basket_items(self, basket_id: int) -> None:
        with self._connection() as conn:
            conn.execute(
                "DELETE FROM basket_items WHERE basket_id = ? AND quantity <= 0",
                (basket_id,),
            )

    def delete_basket(self, basket_id: int) -> None:
        with self._connection() as conn:
            conn.execute("DELETE FROM basket_items WHERE basket_id = ?", (basket_id,))
            conn.execute("DELETE FROM baskets WHERE id = ?", (basket_id,))

    def create_order(
        self,
        buyer_id: str,
        ship_to_street: str,
        ship_to_city: str,
        ship_to_state: str,
        ship_to_country: str,
        ship_to_zip_code: str,
        items: list[tuple[int, str, str, float, int]],
    ) -> Order:
        order_date = datetime.utcnow().isoformat()
        with self._connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO orders (
                    buyer_id, order_date,
                    ship_to_street, ship_to_city, ship_to_state,
                    ship_to_country, ship_to_zip_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    buyer_id,
                    order_date,
                    ship_to_street,
                    ship_to_city,
                    ship_to_state,
                    ship_to_country,
                    ship_to_zip_code,
                ),
            )
            order_id = cursor.lastrowid
            order_items: list[OrderItem] = []
            for catalog_item_id, product_name, picture_uri, unit_price, units in items:
                item_cursor = conn.execute(
                    """
                    INSERT INTO order_items (
                        order_id, catalog_item_id, product_name,
                        picture_uri, unit_price, units
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        order_id,
                        catalog_item_id,
                        product_name,
                        picture_uri,
                        unit_price,
                        units,
                    ),
                )
                order_items.append(
                    OrderItem(
                        id=item_cursor.lastrowid,
                        catalog_item_id=catalog_item_id,
                        product_name=product_name,
                        picture_uri=picture_uri,
                        unit_price=unit_price,
                        units=units,
                    )
                )
            return Order(
                id=order_id,
                buyer_id=buyer_id,
                order_date=datetime.fromisoformat(order_date),
                ship_to_street=ship_to_street,
                ship_to_city=ship_to_city,
                ship_to_state=ship_to_state,
                ship_to_country=ship_to_country,
                ship_to_zip_code=ship_to_zip_code,
                items=order_items,
            )

    def list_orders_for_buyer(self, buyer_id: str) -> list[Order]:
        with self._connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM orders WHERE buyer_id = ? ORDER BY order_date DESC
                """,
                (buyer_id,),
            ).fetchall()
            return [self._load_order(conn, row) for row in rows]

    def get_order_by_id(self, order_id: int, buyer_id: str) -> Order | None:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM orders WHERE id = ? AND buyer_id = ?",
                (order_id, buyer_id),
            ).fetchone()
            if not row:
                return None
            return self._load_order(conn, row)

    def has_catalog_data(self) -> bool:
        with self._connection() as conn:
            row = conn.execute("SELECT COUNT(*) FROM catalog_items").fetchone()
            return int(row[0]) > 0

    def _load_basket(self, conn, basket_id: int, buyer_id: str) -> Basket:
        rows = conn.execute(
            """
            SELECT bi.id, bi.catalog_item_id, bi.quantity, bi.unit_price,
                   ci.name AS product_name, ci.picture_uri
            FROM basket_items bi
            JOIN catalog_items ci ON ci.id = bi.catalog_item_id
            WHERE bi.basket_id = ?
            ORDER BY bi.id
            """,
            (basket_id,),
        ).fetchall()
        items = [
            BasketItem(
                id=row["id"],
                catalog_item_id=row["catalog_item_id"],
                quantity=row["quantity"],
                unit_price=row["unit_price"],
                product_name=row["product_name"],
                picture_uri=row["picture_uri"],
            )
            for row in rows
        ]
        return Basket(id=basket_id, buyer_id=buyer_id, items=items)

    def _load_order(self, conn, row) -> Order:
        item_rows = conn.execute(
            """
            SELECT id, catalog_item_id, product_name, picture_uri, unit_price, units
            FROM order_items WHERE order_id = ? ORDER BY id
            """,
            (row["id"],),
        ).fetchall()
        items = [
            OrderItem(
                id=item["id"],
                catalog_item_id=item["catalog_item_id"],
                product_name=item["product_name"],
                picture_uri=item["picture_uri"],
                unit_price=item["unit_price"],
                units=item["units"],
            )
            for item in item_rows
        ]
        return Order(
            id=row["id"],
            buyer_id=row["buyer_id"],
            order_date=datetime.fromisoformat(row["order_date"]),
            ship_to_street=row["ship_to_street"],
            ship_to_city=row["ship_to_city"],
            ship_to_state=row["ship_to_state"],
            ship_to_country=row["ship_to_country"],
            ship_to_zip_code=row["ship_to_zip_code"],
            items=items,
        )


def _row_to_catalog_item(row) -> CatalogItem:
    return CatalogItem(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        price=row["price"],
        picture_uri=row["picture_uri"],
        catalog_brand_id=row["catalog_brand_id"],
        catalog_type_id=row["catalog_type_id"],
        brand_name=row["brand_name"],
        type_name=row["type_name"],
    )
