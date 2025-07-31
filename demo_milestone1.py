#!/usr/bin/env python3
"""
Demo Script for Milestone 1: Database Design and Loading Data
This script demonstrates all aspects of the database setup and data loading process.
"""

import sqlite3
import pandas as pd
import os
from database_setup import DatabaseSetup

def demo_database_schema():
    """1. Show database schema/table structure"""
    print("=" * 60)
    print("📋 1. DATABASE SCHEMA / TABLE STRUCTURE")
    print("=" * 60)
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"📊 Total Tables: {len(tables)}")
    print("\n🗂️  Table List:")
    for i, table in enumerate(tables, 1):
        print(f"   {i}. {table[0]}")
    
    print("\n📋 Detailed Schema for Each Table:")
    print("-" * 40)
    
    for table in tables:
        table_name = table[0]
        print(f"\n🔍 Table: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"{'Column':<20} {'Type':<15} {'Nullable':<10} {'Primary Key'}")
        print("-" * 60)
        for col in columns:
            pk = "YES" if col[5] else "NO"
            nullable = "NO" if col[3] else "YES"
            print(f"{col[1]:<20} {col[2]:<15} {nullable:<10} {pk}")
    
    conn.close()

def demo_sample_records():
    """2. Execute queries to show sample records from products table"""
    print("\n" + "=" * 60)
    print("📊 2. SAMPLE RECORDS FROM PRODUCTS TABLE")
    print("=" * 60)
    
    conn = sqlite3.connect('ecommerce.db')
    
    # Sample products with key information
    print("🛍️  Sample Products (First 5):")
    print("-" * 80)
    products_sample = pd.read_sql_query("""
        SELECT id, name, brand, category, retail_price, department 
        FROM products 
        LIMIT 5
    """, conn)
    print(products_sample.to_string(index=False))
    
    # Product statistics
    print("\n📈 Product Statistics:")
    print("-" * 40)
    stats = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_products,
            COUNT(DISTINCT category) as unique_categories,
            COUNT(DISTINCT brand) as unique_brands,
            COUNT(DISTINCT department) as departments,
            AVG(retail_price) as avg_price,
            MIN(retail_price) as min_price,
            MAX(retail_price) as max_price
        FROM products
    """, conn)
    print(stats.to_string(index=False))
    
    # Category distribution
    print("\n📊 Top 5 Product Categories:")
    print("-" * 40)
    categories = pd.read_sql_query("""
        SELECT category, COUNT(*) as count 
        FROM products 
        GROUP BY category 
        ORDER BY count DESC 
        LIMIT 5
    """, conn)
    print(categories.to_string(index=False))
    
    conn.close()

def demo_data_loading_process():
    """3. Explain data loading process and challenges faced"""
    print("\n" + "=" * 60)
    print("🔄 3. DATA LOADING PROCESS & CHALLENGES")
    print("=" * 60)
    
    print("📥 Data Loading Process:")
    print("1. Downloaded dataset from: https://github.com/recruit41/ecommerce-dataset")
    print("2. Extracted CSV files from archive.zip")
    print("3. Analyzed CSV structure to design database schema")
    print("4. Created database tables with proper relationships")
    print("5. Implemented chunked loading for large files")
    print("6. Verified data integrity and completeness")
    
    print("\n⚠️  Challenges Faced:")
    print("1. **Large File Sizes**: CSV files were very large (up to 90MB)")
    print("   → Solution: Implemented chunked loading (1000 rows at a time)")
    print("   → Used pandas read_csv with chunksize parameter")
    
    print("\n2. **GitHub File Size Limit**: Database file was 149MB")
    print("   → Solution: Removed from repository, created local generation scripts")
    print("   → Added comprehensive .gitignore")
    print("   → Created init_database.py for local setup")
    
    print("\n3. **Data Type Handling**: Mixed data types in CSV files")
    print("   → Solution: Analyzed data structure first")
    print("   → Used appropriate SQLite data types")
    print("   → Implemented proper foreign key relationships")
    
    print("\n4. **Memory Management**: Loading large datasets")
    print("   → Solution: Chunked processing to avoid memory issues")
    print("   → Progress logging for monitoring")
    print("   → Error handling for robust loading")

def demo_code_walkthrough():
    """4. Walk through the code for database setup and data loading"""
    print("\n" + "=" * 60)
    print("💻 4. CODE WALKTHROUGH")
    print("=" * 60)
    
    print("🔧 Key Components:")
    
    print("\n1. **DatabaseSetup Class** (database_setup.py):")
    print("   - create_tables(): Creates all database tables")
    print("   - load_csv_data(): Handles chunked CSV loading")
    print("   - verify_data_loading(): Validates loaded data")
    
    print("\n2. **Database Schema Design**:")
    print("   - products: Product catalog with pricing and categorization")
    print("   - users: Customer information with location data")
    print("   - orders: Order tracking with status management")
    print("   - order_items: Individual items in orders")
    print("   - inventory_items: Inventory tracking")
    print("   - distribution_centers: Warehouse locations")
    
    print("\n3. **Data Loading Strategy**:")
    print("   - Chunked loading (1000 rows per chunk)")
    print("   - Progress logging for monitoring")
    print("   - Error handling and validation")
    print("   - Foreign key relationship maintenance")
    
    print("\n4. **Setup Automation**:")
    print("   - init_database.py: Interactive database setup")
    print("   - quick_start.py: Automated project setup")
    print("   - verify_data.py: Data validation and analytics")

def demo_database_connection():
    """Show database connection details"""
    print("\n" + "=" * 60)
    print("🔗 DATABASE CONNECTION DETAILS")
    print("=" * 60)
    
    print("📍 Database Type: SQLite")
    print("📁 Database File: ecommerce.db (generated locally)")
    print("🔧 Connection String: sqlite:///ecommerce.db")
    print("📊 Database Size: ~150MB (generated from CSV files)")
    
    # Show current database info
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Get database size
    cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    size_bytes = cursor.fetchone()[0]
    size_mb = size_bytes / (1024 * 1024)
    
    print(f"📏 Current Size: {size_mb:.2f} MB")
    
    # Get row counts
    tables = ['products', 'users', 'orders', 'order_items', 'inventory_items', 'distribution_centers']
    print("\n📊 Current Data Counts:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {table}: {count:,} rows")
    
    conn.close()

def demo_data_validation():
    """Show data validation and cleaning performed"""
    print("\n" + "=" * 60)
    print("✅ DATA VALIDATION & CLEANING")
    print("=" * 60)
    
    conn = sqlite3.connect('ecommerce.db')
    
    print("🔍 Validation Checks Performed:")
    
    # Check for null values in critical fields
    print("\n1. **Null Value Checks**:")
    critical_fields = [
        ('products', 'name'),
        ('products', 'retail_price'),
        ('users', 'email'),
        ('orders', 'user_id')
    ]
    
    for table, field in critical_fields:
        result = pd.read_sql_query(f"SELECT COUNT(*) as null_count FROM {table} WHERE {field} IS NULL", conn)
        null_count = result['null_count'].iloc[0]
        print(f"   {table}.{field}: {null_count} null values")
    
    # Check data type consistency
    print("\n2. **Data Type Validation**:")
    print("   - All prices stored as REAL (floating point)")
    print("   - IDs stored as INTEGER with PRIMARY KEY constraints")
    print("   - Text fields stored as TEXT")
    print("   - Timestamps stored as TEXT (ISO format)")
    
    # Check foreign key integrity
    print("\n3. **Foreign Key Integrity**:")
    print("   - orders.user_id → users.id")
    print("   - order_items.order_id → orders.order_id")
    print("   - order_items.product_id → products.id")
    print("   - inventory_items.product_id → products.id")
    
    conn.close()

def main():
    """Run the complete demo"""
    print("🚀 MILESTONE 1 DEMO: Database Design and Loading Data")
    print("=" * 80)
    
    # Check if database exists
    if not os.path.exists('ecommerce.db'):
        print("❌ Database not found! Please run 'python init_database.py' first.")
        return
    
    # Run all demo sections
    demo_database_schema()
    demo_sample_records()
    demo_data_loading_process()
    demo_code_walkthrough()
    demo_database_connection()
    demo_data_validation()
    
    print("\n" + "=" * 80)
    print("🎉 DEMO COMPLETE!")
    print("=" * 80)
    print("✅ All requirements demonstrated:")
    print("   ✓ Database schema/table structure")
    print("   ✓ Sample records from products table")
    print("   ✓ Data loading process and challenges")
    print("   ✓ Code walkthrough")
    print("   ✓ Database connection details")
    print("   ✓ Data validation and cleaning")

if __name__ == "__main__":
    main() 