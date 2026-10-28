CREATE TABLE IF NOT EXISTS catalog_brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS catalog_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS catalog_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    picture_uri TEXT NOT NULL,
    catalog_brand_id INTEGER NOT NULL REFERENCES catalog_brands(id),
    catalog_type_id INTEGER NOT NULL REFERENCES catalog_types(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS baskets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_id TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS basket_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    basket_id INTEGER NOT NULL REFERENCES baskets(id) ON DELETE CASCADE,
    catalog_item_id INTEGER NOT NULL REFERENCES catalog_items(id),
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    ship_to_street TEXT NOT NULL,
    ship_to_city TEXT NOT NULL,
    ship_to_state TEXT NOT NULL,
    ship_to_country TEXT NOT NULL,
    ship_to_zip_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    catalog_item_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    picture_uri TEXT NOT NULL,
    unit_price REAL NOT NULL,
    units INTEGER NOT NULL
);
