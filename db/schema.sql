PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS currency_rates;
DROP TABLE IF EXISTS shipping_regions;
DROP TABLE IF EXISTS product_details;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT,
    population INTEGER
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    country_code TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (country_code) REFERENCES countries(code)
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE product_details (
    product_id INTEGER PRIMARY KEY,
    stock INTEGER NOT NULL,
    rating REAL,
    weight REAL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE shipping_regions (
    country_code TEXT PRIMARY KEY,
    region TEXT,
    shipping_zone TEXT,
    estimated_days TEXT,
    FOREIGN KEY (country_code) REFERENCES countries(code)
);

CREATE TABLE currency_rates (
    currency_code TEXT PRIMARY KEY,
    rate_to_usd REAL,
    updated_at TEXT
);