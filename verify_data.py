import sqlite3
import pandas as pd

def verify_database():
    """Verify the loaded data with some basic analytics"""
    print("=== E-commerce Database Verification ===\n")
    
    # Connect to database
    conn = sqlite3.connect('ecommerce.db')
    
    # 1. Check table row counts
    print("1. Database Table Row Counts:")
    print("-" * 40)
    tables = ['products', 'users', 'orders', 'order_items', 'inventory_items', 'distribution_centers']
    
    for table in tables:
        count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn)
        print(f"{table:20} : {count['count'].iloc[0]:,} rows")
    
    print("\n2. Sample Products:")
    print("-" * 40)
    products_sample = pd.read_sql_query("""
        SELECT id, name, brand, category, retail_price, department 
        FROM products 
        LIMIT 5
    """, conn)
    print(products_sample.to_string(index=False))
    
    print("\n3. Product Categories Distribution:")
    print("-" * 40)
    categories = pd.read_sql_query("""
        SELECT category, COUNT(*) as count 
        FROM products 
        GROUP BY category 
        ORDER BY count DESC 
        LIMIT 10
    """, conn)
    print(categories.to_string(index=False))
    
    print("\n4. Department Distribution:")
    print("-" * 40)
    departments = pd.read_sql_query("""
        SELECT department, COUNT(*) as count 
        FROM products 
        GROUP BY department 
        ORDER BY count DESC
    """, conn)
    print(departments.to_string(index=False))
    
    print("\n5. Order Status Distribution:")
    print("-" * 40)
    order_status = pd.read_sql_query("""
        SELECT status, COUNT(*) as count 
        FROM orders 
        GROUP BY status 
        ORDER BY count DESC
    """, conn)
    print(order_status.to_string(index=False))
    
    print("\n6. Sample Users:")
    print("-" * 40)
    users_sample = pd.read_sql_query("""
        SELECT id, first_name, last_name, email, city, country 
        FROM users 
        LIMIT 5
    """, conn)
    print(users_sample.to_string(index=False))
    
    print("\n7. Distribution Centers:")
    print("-" * 40)
    dist_centers = pd.read_sql_query("""
        SELECT * FROM distribution_centers
    """, conn)
    print(dist_centers.to_string(index=False))
    
    print("\n8. Basic Analytics:")
    print("-" * 40)
    
    # Average product price
    avg_price = pd.read_sql_query("""
        SELECT AVG(retail_price) as avg_price, 
               MIN(retail_price) as min_price, 
               MAX(retail_price) as max_price 
        FROM products
    """, conn)
    print(f"Product Price Range:")
    print(f"  Average: ${avg_price['avg_price'].iloc[0]:.2f}")
    print(f"  Minimum: ${avg_price['min_price'].iloc[0]:.2f}")
    print(f"  Maximum: ${avg_price['max_price'].iloc[0]:.2f}")
    
    # Total orders and revenue
    orders_summary = pd.read_sql_query("""
        SELECT COUNT(*) as total_orders,
               COUNT(DISTINCT user_id) as unique_customers
        FROM orders
    """, conn)
    print(f"\nOrders Summary:")
    print(f"  Total Orders: {orders_summary['total_orders'].iloc[0]:,}")
    print(f"  Unique Customers: {orders_summary['unique_customers'].iloc[0]:,}")
    
    conn.close()
    print("\n=== Database Verification Complete ===")

if __name__ == "__main__":
    verify_database() 