import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine, text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseSetup:
    def __init__(self, db_name='ecommerce.db'):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        
    def create_tables(self):
        """Create database tables based on CSV structure"""
        logger.info("Creating database tables...")
        
        # Create products table
        products_schema = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            cost REAL,
            category TEXT,
            name TEXT,
            brand TEXT,
            retail_price REAL,
            department TEXT,
            sku TEXT,
            distribution_center_id INTEGER
        )
        """
        
        # Create users table
        users_schema = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            age INTEGER,
            gender TEXT,
            state TEXT,
            street_address TEXT,
            postal_code TEXT,
            city TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            traffic_source TEXT,
            created_at TEXT
        )
        """
        
        # Create orders table
        orders_schema = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            status TEXT,
            gender TEXT,
            created_at TEXT,
            returned_at TEXT,
            shipped_at TEXT,
            delivered_at TEXT,
            num_of_item INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        
        # Create order_items table
        order_items_schema = """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            user_id INTEGER,
            product_id INTEGER,
            inventory_item_id INTEGER,
            status TEXT,
            created_at TEXT,
            shipped_at TEXT,
            delivered_at TEXT,
            returned_at TEXT,
            sale_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        """
        
        # Create inventory_items table
        inventory_items_schema = """
        CREATE TABLE IF NOT EXISTS inventory_items (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            created_at TEXT,
            sold_at TEXT,
            cost REAL,
            product_category TEXT,
            product_name TEXT,
            product_brand TEXT,
            product_retail_price REAL,
            product_department TEXT,
            product_sku TEXT,
            product_distribution_center_id INTEGER,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        """
        
        # Create distribution_centers table
        distribution_centers_schema = """
        CREATE TABLE IF NOT EXISTS distribution_centers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            latitude REAL,
            longitude REAL
        )
        """
        
        with self.engine.connect() as conn:
            conn.execute(text(products_schema))
            conn.execute(text(users_schema))
            conn.execute(text(orders_schema))
            conn.execute(text(order_items_schema))
            conn.execute(text(inventory_items_schema))
            conn.execute(text(distribution_centers_schema))
            conn.commit()
            
        logger.info("Database tables created successfully!")
    
    def load_csv_data(self, csv_file, table_name, chunk_size=1000):
        """Load CSV data into database table"""
        logger.info(f"Loading data from {csv_file} into {table_name}...")
        
        try:
            # Read CSV in chunks to handle large files
            chunk_count = 0
            for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                chunk.to_sql(table_name, self.engine, if_exists='append', index=False)
                chunk_count += 1
                logger.info(f"Loaded chunk {chunk_count} for {table_name}")
                
            logger.info(f"Successfully loaded {table_name} data!")
            
        except Exception as e:
            logger.error(f"Error loading {table_name}: {str(e)}")
            raise
    
    def verify_data_loading(self):
        """Verify that data was loaded correctly"""
        logger.info("Verifying data loading...")
        
        with self.engine.connect() as conn:
            # Check row counts
            tables = ['products', 'users', 'orders', 'order_items', 'inventory_items', 'distribution_centers']
            
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) as count FROM {table}"))
                count = result.fetchone()[0]
                logger.info(f"{table}: {count} rows")
            
            # Check sample data from products
            result = conn.execute(text("SELECT * FROM products LIMIT 3"))
            sample_products = result.fetchall()
            logger.info(f"Sample products: {sample_products}")
            
            # Check data types and structure
            result = conn.execute(text("PRAGMA table_info(products)"))
            columns = result.fetchall()
            logger.info(f"Products table structure: {columns}")

def main():
    """Main function to set up database and load data"""
    logger.info("Starting database setup and data loading...")
    
    # Initialize database setup
    db_setup = DatabaseSetup()
    
    # Create tables
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
            db_setup.load_csv_data(csv_file, table_name)
        else:
            logger.warning(f"CSV file not found: {csv_file}")
    
    # Verify data loading
    db_setup.verify_data_loading()
    
    logger.info("Database setup and data loading completed successfully!")

if __name__ == "__main__":
    main() 