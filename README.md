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
1. Clone the repository and install Python dependencies:
   ```bash
   git clone <your-repo-url>
   cd ecommerce-website
   pip install -r requirements.txt
   ```

2. Download the dataset:
   ```bash
   git clone https://github.com/recruit41/ecommerce-dataset.git
   ```

3. Initialize the database:
   ```bash
   python init_database.py
   ```

4. The script will:
   - Create SQLite database (`ecommerce.db`)
   - Create all necessary tables
   - Load data from CSV files
   - Verify data loading with row counts and sample data

**Note:** The database file (`ecommerce.db`) is not included in the repository due to size limitations. Each developer needs to run the initialization script locally.

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
├── ecommerce-dataset/          # Downloaded dataset (not in repo)
│   └── archive/               # Extracted CSV files
├── database_setup.py          # Database setup script
├── init_database.py           # Database initialization script
├── quick_start.py             # Automated setup script
├── verify_data.py             # Data verification script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
└── ecommerce.db               # SQLite database (generated locally, not in repo)
```

## Quick Start:
For new developers, simply run:
```bash
python quick_start.py
```
This will automatically:
1. Install dependencies
2. Download the dataset
3. Initialize the database
4. Verify the setup

## Milestone 2: REST API for Products ✅

### Completed Tasks:
1. ✅ Created Flask REST API application (`app.py`)
2. ✅ Implemented GET /api/products endpoint with pagination and filtering
3. ✅ Implemented GET /api/products/{id} endpoint for specific products
4. ✅ Added proper JSON response format and error handling
5. ✅ Enabled CORS headers for frontend integration
6. ✅ Created comprehensive API documentation
7. ✅ Added testing script for API verification

### API Endpoints:
- **GET /** - API information and available endpoints
- **GET /api/products** - List all products (with pagination, filtering)
- **GET /api/products/{id}** - Get specific product by ID
- **GET /api/products/categories** - Get product categories with statistics
- **GET /api/products/brands** - Get product brands with counts
- **GET /api/products/stats** - Get overall product statistics

### Features:
- **Pagination**: Efficient handling of large datasets (default: 20 items, max: 100)
- **Filtering**: By category, brand, department, price range
- **Error Handling**: 404 for not found, 400 for invalid ID, 500 for server errors
- **CORS Support**: Ready for frontend integration
- **JSON Responses**: Consistent response format with success/error indicators

### Setup and Testing:
1. Start the API server:
   ```bash
   python app.py
   ```

2. Test the API:
   ```bash
   python test_api.py
   ```

3. Manual testing with curl:
   ```bash
   curl http://localhost:5000/
   curl http://localhost:5000/api/products
   curl http://localhost:5000/api/products/1
   ```

### API Documentation:
See `API_DOCUMENTATION.md` for comprehensive documentation including:
- All endpoint details
- Request/response examples
- Error handling
- Testing instructions
- Deployment considerations

## Project Structure:
```
E-commerce webpage/
├── ecommerce-dataset/          # Downloaded dataset (not in repo)
│   └── archive/               # Extracted CSV files
├── app.py                     # Flask REST API application
├── test_api.py                # API testing script
├── API_DOCUMENTATION.md       # Comprehensive API documentation
├── database_setup.py          # Database setup script
├── init_database.py           # Database initialization script
├── quick_start.py             # Automated setup script
├── verify_data.py             # Data verification script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
└── ecommerce.db               # SQLite database (generated locally, not in repo)
```

## Milestone 3: Frontend UI for Products ✅

### Completed Tasks:
1. ✅ Created modern, responsive frontend application (`index.html`)
2. ✅ Implemented products list view with grid layout
3. ✅ Implemented product detail view with complete information
4. ✅ Integrated with REST API from Milestone 2
5. ✅ Added advanced filtering (category, brand, price range)
6. ✅ Implemented search functionality with debouncing
7. ✅ Added pagination and navigation
8. ✅ Created responsive design for mobile and desktop
9. ✅ Added loading states and error handling
10. ✅ Implemented cart functionality with notifications

### Frontend Features:
- **Products List View**: Responsive grid layout with product cards
- **Product Detail View**: Complete product information with navigation
- **API Integration**: Full integration with Flask REST API
- **Advanced Filtering**: Category, brand, and price range filters
- **Search Functionality**: Real-time search with debouncing
- **Pagination**: Efficient navigation through product pages
- **Responsive Design**: Mobile-first design approach
- **Loading States**: Professional loading indicators
- **Error Handling**: User-friendly error messages
- **Cart System**: Simple add-to-cart functionality

### Technology Stack:
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with Flexbox and Grid
- **Vanilla JavaScript**: No framework dependencies
- **Font Awesome**: Icon library for UI elements
- **Google Fonts**: Inter font family for typography

### Setup and Testing:
1. Ensure the API server is running (Milestone 2):
   ```bash
   python app.py
   ```

2. Open the frontend application:
   - Open `index.html` in a web browser
   - Or use a local server for better performance

3. Test the frontend:
   ```bash
   # Open test_frontend.html to run comprehensive tests
   ```

### Frontend Structure:
```
E-commerce webpage/
├── index.html                 # Main application entry point
├── styles/
│   └── main.css              # Complete styling system
├── js/
│   ├── api.js                # API integration and caching
│   └── app.js                # Main application logic
├── test_frontend.html        # Frontend testing utility
└── MILESTONE3_SUMMARY.md     # Frontend documentation
```

### Key Features:
- **Responsive Grid**: Adapts to different screen sizes
- **Product Cards**: Beautiful cards with hover effects
- **Filter System**: Advanced filtering with clear options
- **Search Bar**: Collapsible search with real-time results
- **Navigation**: Seamless navigation between views
- **Performance**: Caching and optimized loading
- **Accessibility**: Semantic HTML and keyboard navigation

## Next Milestones:
- Milestone 4: [To be defined]
- Milestone 5: [To be defined]
- Milestone 6: [To be defined] 