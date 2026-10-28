# eShop

A small online store used for the Perth AI "Matt Pocock skills" workshop.

## Catalog

**CatalogItem**: A product available for sale in the shop, identified by a numeric ID, with a name, description, price, and image.

_Avoid_: Product, item, listing

**CatalogBrand**: The manufacturer or brand under which a product is sold (e.g. "Acme Corp").

_Avoid_: Brand, maker

**CatalogType**: The category or classification of a product (e.g. "T-Shirt", "Mug").

_Avoid_: Category, type, classification

## Customer

**User**: A registered shopper with an email address and password hash. Only authenticated users can place orders and manage their basket.

_Avoid_: Customer, shopper, account, member

**Basket**: A collection of products a user intends to buy, keyed by a UUID for anonymous users or by email for signed-in users.

_Avoid_: Cart, shopping cart, order

**BasketItem**: A single line within a basket: a product reference, quantity, and the price at the time of adding.

_Avoid_: Line item

**Order**: A completed purchase containing the buyer's details, shipping address, and the products they bought at the time of purchase.

_Avoid_: Purchase, transaction, receipt

**OrderItem**: A single product within an order, capturing the product name, image, price, and quantity at the time of purchase.

_Avoid_: Line item

## Favourites

**Favourite**: A reference from a signed-in user to a catalog item they have saved for later viewing. One per user per product.

_Avoid_: Bookmark, saved item, wish list

**Favourites list**: A signed-in user's collection of favourites. Displayed on a dedicated page with an empty state if the list is empty.

_Avoid_: Wishlist, saved items, book marks
