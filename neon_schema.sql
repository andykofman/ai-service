-- Create users table
CREATE TABLE users (
    user_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    email VARCHAR
);

-- Create products table
CREATE TABLE products (
    product_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    price INTEGER,
    description VARCHAR
);

-- Create orders table
CREATE TABLE orders (
    order_id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(user_id),
    product_id VARCHAR REFERENCES products(product_id),
    quantity INTEGER,
    status VARCHAR,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);

-- Create conversations table
CREATE TABLE conversations (
    conv_id VARCHAR PRIMARY KEY,
    user_id VARCHAR,
    timestamp VARCHAR,
    message VARCHAR,
    direction VARCHAR,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_users_user_id ON users(user_id);
CREATE INDEX idx_products_product_id ON products(product_id);
CREATE INDEX idx_orders_order_id ON orders(order_id);
CREATE INDEX idx_conversations_conv_id ON conversations(conv_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_product_id ON orders(product_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id); 