-- DROP TABLES if they exist (for repeated runs)
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Customers;

-- Create Customers table
CREATE TABLE Customers (
  customer_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(100),
  signup_date DATE
);

-- Create Products table
CREATE TABLE Products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(100),
  category VARCHAR(50),
  price DECIMAL(10,2)
);

-- Create Orders table
CREATE TABLE Orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  status VARCHAR(20),
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Create OrderItems table (many-to-many between Orders and Products)
CREATE TABLE OrderItems (
  order_item_id INT PRIMARY KEY,
  order_id INT,
  product_id INT,
  quantity INT,
  FOREIGN KEY (order_id) REFERENCES Orders(order_id),
  FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Create Payments table
CREATE TABLE Payments (
  payment_id INT PRIMARY KEY,
  order_id INT,
  payment_date DATE,
  amount DECIMAL(10,2),
  payment_method VARCHAR(50),
  FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Create Reviews table
CREATE TABLE Reviews (
  review_id INT PRIMARY KEY,
  product_id INT,
  customer_id INT,
  rating INT CHECK (rating BETWEEN 1 AND 5),
  review_date DATE,
  comment TEXT,
  FOREIGN KEY (product_id) REFERENCES Products(product_id),
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Insert sample Customers
INSERT INTO Customers VALUES
(1, 'Alice', 'Smith', 'alice.smith@example.com', '2022-01-15'),
(2, 'Bob', 'Johnson', 'bob.johnson@example.com', '2022-02-20'),
(3, 'Charlie', 'Williams', 'charlie.williams@example.com', '2022-03-05'),
(4, 'Diana', 'Brown', 'diana.brown@example.com', '2022-04-10'),
(5, 'Ethan', 'Jones', 'ethan.jones@example.com', '2022-05-12');

-- Insert sample Products
INSERT INTO Products VALUES
(1, 'Wireless Mouse', 'Electronics', 25.99),
(2, 'Bluetooth Headphones', 'Electronics', 79.99),
(3, 'Coffee Mug', 'Home & Kitchen', 12.50),
(4, 'Notebook', 'Office Supplies', 3.99),
(5, 'Desk Lamp', 'Home & Kitchen', 45.00);

-- Insert sample Orders
INSERT INTO Orders VALUES
(1, 1, '2023-01-10', 'Delivered'),
(2, 2, '2023-01-12', 'Shipped'),
(3, 1, '2023-02-05', 'Cancelled'),
(4, 3, '2023-02-20', 'Delivered'),
(5, 4, '2023-03-01', 'Delivered');

-- Insert sample OrderItems
INSERT INTO OrderItems VALUES
(1, 1, 1, 2),  -- Alice bought 2 Wireless Mice
(2, 1, 3, 1),  -- Alice bought 1 Coffee Mug
(3, 2, 2, 1),  -- Bob bought 1 Bluetooth Headphones
(4, 4, 4, 3),  -- Charlie bought 3 Notebooks
(5, 5, 5, 1);  -- Diana bought 1 Desk Lamp

-- Insert sample Payments
INSERT INTO Payments VALUES
(1, 1, '2023-01-11', 63.48, 'Credit Card'),
(2, 2, '2023-01-13', 79.99, 'PayPal'),
(3, 4, '2023-02-21', 11.97, 'Credit Card'),
(4, 5, '2023-03-02', 45.00, 'Credit Card');

-- Insert sample Reviews
INSERT INTO Reviews VALUES
(1, 1, 1, 5, '2023-01-15', 'Great mouse, very responsive!'),
(2, 2, 2, 4, '2023-01-20', 'Good sound quality, but a bit pricey.'),
(3, 3, 1, 3, '2023-02-01', 'Mug is okay, nothing special.'),
(4, 5, 4, 5, '2023-03-05', 'Perfect lighting for my desk.');

-- --- Sample advanced queries ---

-- 1) Total sales amount per product category
SELECT p.category,
       SUM(oi.quantity * p.price) AS total_sales
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
JOIN Orders o ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY total_sales DESC;

-- 2) Average rating per product
SELECT p.product_name,
       AVG(r.rating) AS avg_rating,
       COUNT(r.review_id) AS review_count
FROM Products p
LEFT JOIN Reviews r ON p.product_id = r.product_id
GROUP BY p.product_name
ORDER BY avg_rating DESC NULLS LAST;

-- 3) Customer lifetime value (sum of all delivered order payments per customer)
SELECT c.customer_id, c.first_name, c.last_name,
       COALESCE(SUM(pay.amount), 0) AS lifetime_value
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id AND o.status = 'Delivered'
LEFT JOIN Payments pay ON o.order_id = pay.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY lifetime_value DESC;

-- 4) Customers who have never left a review
SELECT c.customer_id, c.first_name, c.last_name
FROM Customers c
LEFT JOIN Reviews r ON c.customer_id = r.customer_id
WHERE r.review_id IS NULL;

-- 5) Orders with multiple products
SELECT o.order_id, COUNT(oi.order_item_id) AS product_count
FROM Orders o
JOIN OrderItems oi ON o.order_id = oi.order_id
GROUP BY o.order_id
HAVING COUNT(oi.order_item_id) > 1;

-- 6) Most recent orders per customer
WITH ranked_orders AS (
  SELECT o.*,
         ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS rn
  FROM Orders o
)
SELECT ro.customer_id, ro.order_id, ro.order_date, ro.status
FROM ranked_orders ro
WHERE ro.rn = 1;


