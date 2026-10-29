"""Tests for the promo_codes schema (Ticket 8: Database schema and seed script).

These tests exercise the DatabaseClient directly, not through the API.
"""
import tempfile
from pathlib import Path

from db.client import DatabaseClient
from db.seed import seed_promo_codes


def _make_db() -> tuple[DatabaseClient, Path]:
    """Create a temporary database for testing."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db = DatabaseClient(tmp.name)
    return db, Path(tmp.name)


class TestPromoCodesSchema:
    """Verify the promo_codes table exists and has the right columns."""

    def test_promo_codes_table_exists(self):
        """The database should create a promo_codes table on init."""
        db, tmp_path = _make_db()
        try:
            with db._connection() as conn:
                tables = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            table_names = {row["name"] for row in tables}
            assert "promo_codes" in table_names
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_promo_codes_has_required_columns(self):
        """Verify all required columns exist on promo_codes."""
        db, tmp_path = _make_db()
        try:
            with db._connection() as conn:
                info = conn.execute("PRAGMA table_info(promo_codes)").fetchall()
            col_names = {row["name"] for row in info}
            assert col_names >= {
                "id",
                "code",
                "type",
                "value",
                "minimum_order_value",
                "is_active",
                "expiry_date",
                "is_redeemed",
            }
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_promo_codes_code_is_unique(self):
        """Verify the code column has a unique constraint."""
        db, tmp_path = _make_db()
        try:
            with db._connection() as conn:
                schema_row = conn.execute(
                    "SELECT sql FROM sqlite_master WHERE type='table' AND name='promo_codes'"
                ).fetchone()
            assert schema_row is not None
            assert "UNIQUE" in schema_row["sql"].upper()
        finally:
            tmp_path.unlink(missing_ok=True)


class TestOrdersSchema:
    """Verify the orders table has a discount_amount column."""

    def test_orders_has_discount_amount_column(self):
        """The orders table should have a nullable discount_amount column."""
        db, tmp_path = _make_db()
        try:
            with db._connection() as conn:
                info = conn.execute("PRAGMA table_info(orders)").fetchall()
            col_info = {row["name"]: row for row in info}
            assert "discount_amount" in col_info
            # It should be nullable (no NOT NULL constraint)
            assert col_info["discount_amount"]["notnull"] == 0
        finally:
            tmp_path.unlink(missing_ok=True)


class TestSeedScript:
    """Verify the seed script inserts test promo codes."""

    def test_seed_script_inserts_test_codes(self):
        """The seed script should insert at least two test codes."""
        db, tmp_path = _make_db()
        try:
            seed_promo_codes(db)
            with db._connection() as conn:
                codes = conn.execute(
                    "SELECT code, type, value FROM promo_codes ORDER BY code"
                ).fetchall()
            assert len(codes) >= 2
            code_types = {row["type"] for row in codes}
            assert "percentage" in code_types
            assert "fixed" in code_types
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_seed_script_is_idempotent(self):
        """Calling seed_promo_codes twice should not duplicate codes."""
        db, tmp_path = _make_db()
        try:
            seed_promo_codes(db)
            seed_promo_codes(db)
            with db._connection() as conn:
                count = conn.execute(
                    "SELECT COUNT(*) FROM promo_codes"
                ).fetchone()[0]
            assert count == 2
        finally:
            tmp_path.unlink(missing_ok=True)
