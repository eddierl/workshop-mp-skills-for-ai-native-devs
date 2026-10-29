# Promo codes are validated at order creation, not at basket time

Shoppers can enter a promo code on the checkout page for a live preview of the discount, but the code is only truly validated when the order is placed (`POST /api/orders`). The request body accepts an optional `coupon_code` field. If valid (exists, active, not redeemed, not expired, minimum met), the discount is calculated and stored as `discount_amount` on the order. A separate validation endpoint was rejected to keep the API surface minimal.

## Consequences

- **Gains:** One endpoint to understand, no separate route, the `discount_amount` on `orders` captures what was actually charged regardless of future coupon edits.
- **Trade-off:** The checkout preview is an estimate — a coupon could become invalid (expired, minimum no longer met) between preview and submit. Acceptable for the workshop; a production system would show a warning ("final validation at checkout").
- **Trade-off:** No separate validation endpoint means we cannot offer a "browse available coupons" feature without adding one later.
