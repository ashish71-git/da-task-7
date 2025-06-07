# sales_analysis.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def setup_database():
    """Create database with sample sales data"""
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    
    # Create sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        sale_date TEXT
    )
    ''')
    
    # Insert sample data if empty
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        sample_sales = [
            ('Laptop', 5, 899.99, '2023-01-10'),
            ('Mouse', 12, 24.99, '2023-01-10'),
            ('Keyboard', 8, 49.99, '2023-01-11'),
            ('Monitor', 3, 199.99, '2023-01-12'),
            ('Laptop', 2, 899.99, '2023-01-12'),
            ('Mouse', 15, 24.99, '2023-01-13')
        ]
        cursor.executemany("INSERT INTO sales (product, quantity, price, sale_date) VALUES (?, ?, ?, ?)", sample_sales)
        conn.commit()
    conn.close()

def generate_sales_report():
    """Generate and display sales report"""
    setup_database()
    conn = sqlite3.connect('sales_data.db')
    
    # Query 1: Product sales summary
    product_query = """
    SELECT 
        product,
        SUM(quantity) AS total_quantity,
        ROUND(SUM(quantity * price), 2) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC
    """
    
    # Query 2: Overall summary
    overall_query = """
    SELECT 
        COUNT(DISTINCT product) AS product_count,
        SUM(quantity) AS total_units,
        ROUND(SUM(quantity * price), 2) AS grand_total
    FROM sales
    """
    
    # Get data
    product_df = pd.read_sql_query(product_query, conn)
    overall_df = pd.read_sql_query(overall_query, conn)
    
    # Print results
    print("=== PRODUCT SALES SUMMARY ===")
    print(product_df.to_string(index=False))
    
    print("\n=== OVERALL SALES SUMMARY ===")
    print(overall_df.to_string(index=False))
    
    # Create bar chart
    plt.figure(figsize=(8, 4))
    product_df.plot(kind='bar', x='product', y='total_revenue', color='skyblue')
    plt.title('Total Revenue by Product')
    plt.ylabel('Revenue ($)')
    plt.xlabel('Product')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    # Save and show
    plt.savefig('product_revenue.png')
    plt.show()
    
    conn.close()

if __name__ == "__main__":
    generate_sales_report()
