# E-commerce Website Project

This project is building an e-commerce website from scratch with 6 milestones.

## Milestone 1: Database Design and Loading Data ✅

### Completed Tasks:
1. ✅ Downloaded the dataset from https://github.com/recruit41/ecommerce-dataset
2. ✅ Extracted products.csv from archive.zip
3. ✅ Designed and created database tables for all CSV files
4. ✅ Wrote code to load CSV data into the database
5. ✅ Verified data loading by querying the database

### Database Schema:
- **products**: Product catalog with id, cost, category, name, brand, retail_price, department, sku, distribution_center_id
- **users**: Customer information with personal details and location
- **orders**: Order records with status tracking
- **order_items**: Individual items in each order
- **inventory_items**: Inventory tracking for products
- **distribution_centers**: Distribution center locations

### Setup Instructions:
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the database setup script:
   ```bash
   python database_setup.py
   ```

3. The script will:
   - Create SQLite database (`ecommerce.db`)
   - Create all necessary tables
   - Load data from CSV files
   - Verify data loading with row counts and sample data

### Data Verification:
The script provides detailed logging of:
- Number of rows loaded in each table
- Sample data from products table
- Database table structure

**Verification Results:**
- **Products**: 29,120 products across various categories
- **Users**: 100,000 customer records
- **Orders**: 125,226 orders with 80,044 unique customers
- **Order Items**: 181,759 individual items in orders
- **Inventory Items**: 490,705 inventory records
- **Distribution Centers**: 10 locations across the US

**Key Insights:**
- Product price range: $0.02 - $999.00 (Average: $59.22)
- Top categories: Intimates, Jeans, Tops & Tees
- Order statuses: Shipped (37,577), Complete (31,354), Processing (25,156)
- Geographic coverage: Customers from multiple countries including US, Brazil, South Korea

## Project Structure:
```
E-commerce webpage/
├── ecommerce-dataset/          # Downloaded dataset
│   └── archive/               # Extracted CSV files
├── database_setup.py          # Database setup script
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
└── ecommerce.db              # SQLite database (created after running setup)
```

## Next Milestones:
- Milestone 2: [To be defined]
- Milestone 3: [To be defined]
- Milestone 4: [To be defined]
- Milestone 5: [To be defined]
- Milestone 6: [To be defined] 