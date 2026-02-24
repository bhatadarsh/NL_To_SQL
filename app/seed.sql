-- =============================================================
-- seed.sql - Create all tables and insert sample data
-- Run this once to set up your PostgreSQL database
-- =============================================================

-- Drop tables if they exist (in correct order due to FK constraints)
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS employees CASCADE;

-- =============================================================
-- TABLE: customers
-- =============================================================
CREATE TABLE customers (
    customer_id  SERIAL PRIMARY KEY,
    name         VARCHAR(100),
    email        VARCHAR(100),
    phone        VARCHAR(20),
    country      VARCHAR(50),
    city         VARCHAR(50),
    age          INT,
    gender       VARCHAR(10),
    created_at   DATE
);

INSERT INTO customers (name, email, phone, country, city, age, gender, created_at) VALUES
('Amit Sharma',    'amit.sharma@email.com',    '9876543210', 'India',   'Mumbai',    32, 'Male',   '2022-01-15'),
('Priya Verma',    'priya.verma@email.com',    '9876543211', 'India',   'Delhi',     27, 'Female', '2022-02-20'),
('Rahul Singh',    'rahul.singh@email.com',    '9876543212', 'India',   'Bangalore', 35, 'Male',   '2022-03-10'),
('Sneha Patel',    'sneha.patel@email.com',    '9876543213', 'India',   'Ahmedabad', 29, 'Female', '2022-04-05'),
('Vikram Nair',    'vikram.nair@email.com',    '9876543214', 'India',   'Chennai',   41, 'Male',   '2022-05-18'),
('John Smith',     'john.smith@email.com',     '1234567890', 'USA',     'New York',  38, 'Male',   '2022-06-22'),
('Emily Johnson',  'emily.j@email.com',        '1234567891', 'USA',     'Chicago',   25, 'Female', '2022-07-14'),
('David Brown',    'david.brown@email.com',    '1234567892', 'USA',     'Houston',   44, 'Male',   '2022-08-30'),
('Sara Wilson',    'sara.wilson@email.com',    '1234567893', 'UK',      'London',    31, 'Female', '2022-09-12'),
('James Taylor',   'james.taylor@email.com',   '1234567894', 'UK',      'Manchester',28, 'Male',   '2022-10-05'),
('Yuki Tanaka',    'yuki.tanaka@email.com',    '8190001234', 'Japan',   'Tokyo',     33, 'Female', '2022-11-20'),
('Chen Wei',       'chen.wei@email.com',       '8600001234', 'China',   'Shanghai',  39, 'Male',   '2022-12-01'),
('Aisha Khan',     'aisha.khan@email.com',     '9230001234', 'Pakistan','Karachi',   26, 'Female', '2023-01-10'),
('Carlos Mendez',  'carlos.m@email.com',       '5210001234', 'Mexico',  'Mexico City',45,'Male',   '2023-02-14'),
('Fatima Al-Sayed','fatima.al@email.com',      '9710001234', 'UAE',     'Dubai',     30, 'Female', '2023-03-22');

-- =============================================================
-- TABLE: products
-- =============================================================
CREATE TABLE products (
    product_id   SERIAL PRIMARY KEY,
    product_name VARCHAR(150),
    category     VARCHAR(50),
    brand        VARCHAR(50),
    price        DECIMAL(10,2),
    discount     DECIMAL(5,2),
    stock        INT,
    rating       DECIMAL(3,2),
    added_at     DATE
);

INSERT INTO products (product_name, category, brand, price, discount, stock, rating, added_at) VALUES
('iPhone 15 Pro',        'Electronics', 'Apple',    1199.99, 5.00,  50,  4.8, '2023-09-20'),
('Samsung Galaxy S24',   'Electronics', 'Samsung',   999.99, 8.00,  75,  4.6, '2024-01-17'),
('Sony WH-1000XM5',      'Electronics', 'Sony',      349.99, 10.00, 100, 4.7, '2023-05-10'),
('MacBook Air M3',       'Electronics', 'Apple',    1299.99, 3.00,  30,  4.9, '2024-03-08'),
('Dell XPS 15',          'Electronics', 'Dell',      1099.99, 7.00,  40,  4.5, '2023-11-15'),
('Levis 501 Jeans',      'Clothing',   'Levis',       69.99, 15.00, 200, 4.3, '2022-08-01'),
('Nike Air Max 270',     'Clothing',   'Nike',        150.00, 12.00, 150, 4.4, '2022-09-15'),
('Adidas Ultraboost 23', 'Clothing',   'Adidas',      180.00, 10.00, 120, 4.5, '2023-02-20'),
('Zara Formal Shirt',    'Clothing',   'Zara',         49.99, 20.00, 300, 4.1, '2023-04-10'),
('H&M Winter Jacket',    'Clothing',   'H&M',          89.99, 25.00, 80,  4.2, '2023-10-05'),
('Atomic Habits',        'Books',      'Penguin',      15.99, 5.00,  500, 4.8, '2022-01-10'),
('The Alchemist',        'Books',      'HarperCollins',12.99, 0.00,  450, 4.7, '2022-01-10'),
('Clean Code',           'Books',      'Pearson',      35.99, 8.00,  200, 4.6, '2022-03-15'),
('LG 55 inch 4K TV',     'Electronics','LG',          599.99, 15.00, 25,  4.4, '2023-07-20'),
('Instant Pot Duo',      'Kitchen',    'Instant Pot',  89.99, 18.00, 90,  4.6, '2023-01-12');

-- =============================================================
-- TABLE: orders
-- =============================================================
CREATE TABLE orders (
    order_id         SERIAL PRIMARY KEY,
    customer_id      INT REFERENCES customers(customer_id),
    order_date       DATE,
    delivery_date    DATE,
    status           VARCHAR(20),
    payment_method   VARCHAR(30),
    total_amount     DECIMAL(10,2),
    shipping_address VARCHAR(200)
);

INSERT INTO orders (customer_id, order_date, delivery_date, status, payment_method, total_amount, shipping_address) VALUES
(1,  '2024-01-05', '2024-01-10', 'delivered', 'UPI',          1199.99, 'Mumbai, India'),
(2,  '2024-01-08', '2024-01-14', 'delivered', 'Credit Card',   349.99, 'Delhi, India'),
(3,  '2024-01-12', '2024-01-18', 'delivered', 'COD',           699.99, 'Bangalore, India'),
(4,  '2024-01-15', '2024-01-22', 'shipped',   'UPI',           150.00, 'Ahmedabad, India'),
(5,  '2024-01-20', '2024-01-28', 'delivered', 'Credit Card',  1299.99, 'Chennai, India'),
(6,  '2024-02-01', '2024-02-07', 'delivered', 'Credit Card',   999.99, 'New York, USA'),
(7,  '2024-02-05', '2024-02-12', 'pending',   'PayPal',         89.99, 'Chicago, USA'),
(8,  '2024-02-10', '2024-02-18', 'delivered', 'Credit Card',  1099.99, 'Houston, USA'),
(9,  '2024-02-14', '2024-02-20', 'shipped',   'Credit Card',   180.00, 'London, UK'),
(10, '2024-02-18', '2024-02-25', 'cancelled', 'PayPal',         69.99, 'Manchester, UK'),
(11, '2024-03-01', '2024-03-08', 'delivered', 'Credit Card',   349.99, 'Tokyo, Japan'),
(12, '2024-03-05', '2024-03-12', 'delivered', 'Credit Card',   599.99, 'Shanghai, China'),
(1,  '2024-03-10', '2024-03-17', 'delivered', 'UPI',            35.99, 'Mumbai, India'),
(2,  '2024-03-15', '2024-03-22', 'shipped',   'UPI',            89.99, 'Delhi, India'),
(3,  '2024-04-01', '2024-04-08', 'delivered', 'COD',           150.00, 'Bangalore, India'),
(13, '2024-04-05', '2024-04-12', 'delivered', 'Credit Card',    49.99, 'Karachi, Pakistan'),
(14, '2024-04-10', '2024-04-18', 'pending',   'Credit Card',  1199.99, 'Mexico City, Mexico'),
(15, '2024-04-15', '2024-04-22', 'delivered', 'Credit Card',   999.99, 'Dubai, UAE'),
(5,  '2024-04-20', '2024-04-27', 'delivered', 'UPI',            15.99, 'Chennai, India'),
(6,  '2024-05-01', '2024-05-08', 'shipped',   'Credit Card',   180.00, 'New York, USA');

-- =============================================================
-- TABLE: order_items
-- =============================================================
CREATE TABLE order_items (
    item_id     SERIAL PRIMARY KEY,
    order_id    INT REFERENCES orders(order_id),
    product_id  INT REFERENCES products(product_id),
    quantity    INT,
    unit_price  DECIMAL(10,2),
    total_price DECIMAL(10,2),
    discount    DECIMAL(5,2)
);

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price, discount) VALUES
(1,  1,  1, 1199.99, 1199.99, 5.00),
(2,  3,  1,  349.99,  349.99, 10.00),
(3,  2,  1,  999.99,  699.99, 8.00),
(4,  7,  1,  150.00,  150.00, 12.00),
(5,  4,  1, 1299.99, 1299.99, 3.00),
(6,  2,  1,  999.99,  999.99, 8.00),
(7,  15, 1,   89.99,   89.99, 18.00),
(8,  5,  1, 1099.99, 1099.99, 7.00),
(9,  8,  1,  180.00,  180.00, 10.00),
(10, 6,  1,   69.99,   69.99, 15.00),
(11, 3,  1,  349.99,  349.99, 10.00),
(12, 14, 1,  599.99,  599.99, 15.00),
(13, 13, 1,   35.99,   35.99, 8.00),
(14, 15, 1,   89.99,   89.99, 18.00),
(15, 7,  1,  150.00,  150.00, 12.00),
(16, 9,  1,   49.99,   49.99, 20.00),
(17, 1,  1, 1199.99, 1199.99, 5.00),
(18, 2,  1,  999.99,  999.99, 8.00),
(19, 11, 1,   15.99,   15.99, 5.00),
(20, 8,  1,  180.00,  180.00, 10.00);

-- =============================================================
-- TABLE: employees
-- =============================================================
CREATE TABLE employees (
    employee_id  SERIAL PRIMARY KEY,
    name         VARCHAR(100),
    email        VARCHAR(100),
    department   VARCHAR(50),
    role         VARCHAR(50),
    salary       DECIMAL(10,2),
    joining_date DATE,
    is_active    BOOLEAN
);

INSERT INTO employees (name, email, department, role, salary, joining_date, is_active) VALUES
('Ravi Kumar',     'ravi.k@company.com',    'Sales',     'Sales Manager',      75000.00, '2020-01-10', TRUE),
('Meera Joshi',    'meera.j@company.com',   'Support',   'Support Lead',       60000.00, '2020-03-15', TRUE),
('Arjun Reddy',    'arjun.r@company.com',   'Warehouse', 'Warehouse Head',     55000.00, '2019-06-20', TRUE),
('Pooja Iyer',     'pooja.i@company.com',   'Sales',     'Sales Executive',    45000.00, '2021-02-01', TRUE),
('Kiran Shah',     'kiran.s@company.com',   'Support',   'Support Executive',  42000.00, '2021-05-10', TRUE),
('Neha Gupta',     'neha.g@company.com',    'Marketing', 'Marketing Manager',  70000.00, '2020-08-15', TRUE),
('Suresh Pillai',  'suresh.p@company.com',  'Warehouse', 'Warehouse Staff',    38000.00, '2022-01-20', TRUE),
('Divya Menon',    'divya.m@company.com',   'Sales',     'Sales Executive',    45000.00, '2022-03-01', FALSE),
('Ankit Tiwari',   'ankit.t@company.com',   'Support',   'Support Executive',  42000.00, '2022-06-10', TRUE),
('Rohit Kapoor',   'rohit.k@company.com',   'Marketing', 'Marketing Executive',48000.00, '2023-01-15', TRUE);

-- =============================================================
-- TABLE: reviews
-- =============================================================
CREATE TABLE reviews (
    review_id   SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id  INT REFERENCES products(product_id),
    rating      INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date DATE,
    is_verified BOOLEAN
);

INSERT INTO reviews (customer_id, product_id, rating, review_text, review_date, is_verified) VALUES
(1,  1,  5, 'Excellent phone, super fast and great camera!',        '2024-01-12', TRUE),
(2,  3,  4, 'Amazing noise cancellation, battery could be better.', '2024-01-16', TRUE),
(3,  2,  4, 'Great Android phone, smooth performance.',             '2024-01-20', TRUE),
(4,  7,  5, 'Very comfortable shoes, worth the price.',             '2024-01-24', TRUE),
(5,  4,  5, 'Best laptop I have ever used. M3 chip is blazing!',    '2024-01-30', TRUE),
(6,  2,  4, 'Solid phone. Samsung never disappoints.',              '2024-02-08', TRUE),
(7,  15, 3, 'Good product but delivery was delayed.',               '2024-02-14', TRUE),
(8,  5,  5, 'Dell XPS is a powerhouse. Highly recommend.',          '2024-02-20', TRUE),
(9,  8,  4, 'Very stylish and comfortable running shoes.',          '2024-02-22', TRUE),
(10, 6,  3, 'Decent jeans but sizing runs small.',                  '2024-02-26', FALSE),
(11, 3,  5, 'Best headphones in this price range.',                 '2024-03-10', TRUE),
(12, 14, 4, 'Great TV, picture quality is stunning.',               '2024-03-14', TRUE),
(1,  13, 5, 'Clean Code changed how I write software.',             '2024-03-18', TRUE),
(2,  15, 4, 'Instant Pot is a game changer for cooking.',           '2024-03-24', TRUE),
(3,  7,  4, 'Nike Air Max is very comfortable for daily use.',      '2024-04-05', TRUE),
(13, 9,  3, 'Good shirt but material is slightly thin.',            '2024-04-10', FALSE),
(5,  11, 5, 'Atomic Habits is a must read book!',                   '2024-04-25', TRUE),
(6,  8,  5, 'Ultraboost is worth every penny.',                     '2024-05-05', TRUE);