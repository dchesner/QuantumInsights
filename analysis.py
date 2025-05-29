# data_analysis.py

import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt

# === Step 1: Setup Database Connection ===
# Change connection string to your database credentials
DB_USER = 'your_username'
DB_PASS = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'your_db'

engine = sqlalchemy.create_engine(
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# === Step 2: Define your SQL Queries ===

# Example query 1: Total sales by product category (adapt as per your schema)
query_total_sales = """
SELECT p.category,
       SUM(oi.quantity * p.price) AS total_sales
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
JOIN Orders o ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY total_sales DESC;
"""

# Example query 2: Customer order counts and average rating
query_customer_summary = """
SELECT c.customer_id,
       c.customer_name,
       COUNT(o.order_id) AS total_orders,
       AVG(r.rating) AS average_rating
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
LEFT JOIN Reviews r ON o.order_id = r.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_orders DESC;
"""

# === Step 3: Functions to execute queries and return DataFrames ===

def get_total_sales():
    """Run total sales by category query and return DataFrame."""
    df = pd.read_sql(query_total_sales, engine)
    return df

def get_customer_summary():
    """Run customer order count and rating summary query."""
    df = pd.read_sql(query_customer_summary, engine)
    return df

# === Step 4: Analysis and Visualization ===

def plot_total_sales(df):
    plt.figure(figsize=(10,6))
    df.plot(kind='bar', x='category', y='total_sales', legend=False, color='teal')
    plt.title('Total Sales by Product Category')
    plt.ylabel('Total Sales ($)')
    plt.xlabel('Product Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('total_sales_by_category.png')  # Save figure as image
    plt.show()

def export_customer_summary(df):
    df.to_csv('customer_summary_report.csv', index=False)
    print("Customer summary exported to customer_summary_report.csv")

# === Step 5: Main function to run everything ===

def main():
    print("Loading total sales data...")
    sales_df = get_total_sales()
    print(sales_df.head(), "\n")

    print("Visualizing total sales by category...")
    plot_total_sales(sales_df)

    print("Loading customer summary data...")
    customer_df = get_customer_summary()
    print(customer_df.head(), "\n")

    print("Exporting customer summary report...")
    export_customer_summary(customer_df)

if __name__ == "__main__":
    main()

