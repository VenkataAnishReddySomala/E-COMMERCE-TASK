#!/usr/bin/env python3
"""
Database Initialization Script
This script recreates the ecommerce database from the CSV files.
Run this script to set up the database locally.
"""

import os
import sys
from database_setup import DatabaseSetup

def main():
    """Initialize the database"""
    print("=== E-commerce Database Initialization ===")
    print("This script will create the database from CSV files.")
    print("Make sure you have the ecommerce-dataset folder in the project root.")
    print()
    
    # Check if dataset exists
    if not os.path.exists('ecommerce-dataset/archive/products.csv'):
        print("❌ Error: ecommerce-dataset folder not found!")
        print("Please download the dataset first:")
        print("git clone https://github.com/recruit41/ecommerce-dataset.git")
        sys.exit(1)
    
    # Check if database already exists
    if os.path.exists('ecommerce.db'):
        response = input("⚠️  Database already exists. Do you want to recreate it? (y/N): ")
        if response.lower() != 'y':
            print("Database initialization cancelled.")
            sys.exit(0)
        else:
            os.remove('ecommerce.db')
            print("🗑️  Removed existing database.")
    
    print("🚀 Starting database initialization...")
    
    try:
        # Initialize database setup
        db_setup = DatabaseSetup()
        
        # Create tables
        print("📋 Creating database tables...")
        db_setup.create_tables()
        
        # Load data from CSV files
        csv_files = {
            'ecommerce-dataset/archive/products.csv': 'products',
            'ecommerce-dataset/archive/users.csv': 'users',
            'ecommerce-dataset/archive/orders.csv': 'orders',
            'ecommerce-dataset/archive/order_items.csv': 'order_items',
            'ecommerce-dataset/archive/inventory_items.csv': 'inventory_items',
            'ecommerce-dataset/archive/distribution_centers.csv': 'distribution_centers'
        }
        
        for csv_file, table_name in csv_files.items():
            if os.path.exists(csv_file):
                print(f"📥 Loading {table_name}...")
                db_setup.load_csv_data(csv_file, table_name)
            else:
                print(f"⚠️  Warning: {csv_file} not found")
        
        # Verify data loading
        print("✅ Verifying data...")
        db_setup.verify_data_loading()
        
        print("\n🎉 Database initialization completed successfully!")
        print("📊 You can now run 'python verify_data.py' to see the data summary.")
        
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 