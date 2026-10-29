"""Promo code validation and discount calculation (Ticket 9)."""
from datetime import datetime, timezone
from typing import NamedTuple

from db.client import DatabaseClient


class PromoResult(NamedTuple):
    """Result of validating a promo code against an order subtotal.

    Attributes:
        discount_amount: The monetary discount to apply (0.0 if no discount).
        error: A string describing why the code was invalid, or None if valid.
    """

    discount_amount: float
    error: str | None = None


class _PromoRow(NamedTuple):
    id: int
    code: str
    type: str
    value: float
    minimum_order_value: float | None
    is_active: int
    expiry_date: str | None
    is_redeemed: int


class PromoService:
    """Validate promo codes and calculate discounts."""

    def __init__(self, db: DatabaseClient):
        self.db = db

    def validate(self, code: str, subtotal: float) -> PromoResult:
        """Validate a promo code and return the discount (if any).

        Args:
            code: The promo code string to validate.
            subtotal: The order subtotal (before discount).

        Returns:
            A PromoResult with the discount amount (0.0 if no discount applies)
            and an optional error message.
        """
        row = self._find_active_code(code)
        if row is None:
            return PromoResult(discount_amount=0.0, error="NOT_FOUND")
        if row.is_redeemed:
            return PromoResult(discount_amount=0.0, error="ALREADY_REDEEMED")
        if row.expiry_date is not None:
            expiry = datetime.fromisoformat(row.expiry_date)
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry < datetime.now(timezone.utc):
                return PromoResult(discount_amount=0.0, error="EXPIRED")
        if row.minimum_order_value is not None and subtotal < row.minimum_order_value:
            return PromoResult(discount_amount=0.0, error="MINIMUM_NOT_MET")

        discount = self._calculate_discount(row, subtotal)
        return PromoResult(discount_amount=discount, error=None)

    def mark_redeemed(self, code: str) -> None:
        """Mark a promo code as redeemed."""
        with self.db._connection() as conn:
            conn.execute(
                "UPDATE promo_codes SET is_redeemed = 1 WHERE code = ?",
                (code,),
            )

    # -- private helpers --------------------------------------------------

    def _find_active_code(self, code: str) -> _PromoRow | None:
        """Return an active, unredeemed promo code row, or None."""
        with self.db._connection() as conn:
            row = conn.execute(
                """
                SELECT id, code, type, value, minimum_order_value,
                       is_active, expiry_date, is_redeemed
                FROM promo_codes
                WHERE code = ? AND is_active = 1 AND is_redeemed = 0
                """,
                (code,),
            ).fetchone()
        if row is None:
            return None
        return _PromoRow(
            id=row["id"],
            code=row["code"],
            type=row["type"],
            value=row["value"],
            minimum_order_value=row["minimum_order_value"],
            is_active=row["is_active"],
            expiry_date=row["expiry_date"],
            is_redeemed=row["is_redeemed"],
        )

    def _calculate_discount(self, row: _PromoRow, subtotal: float) -> float:
        """Calculate the discount amount for a valid promo code."""
        if row.type == "percentage":
            discount = subtotal * (row.value / 100.0)
        else:  # fixed
            discount = row.value
        # Cap at subtotal (never go below $0)
        return round(min(discount, subtotal), 2)
