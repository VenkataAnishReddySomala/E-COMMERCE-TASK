# 🚀 E-commerce REST API - Milestone 2 Documentation

## 📋 Overview

This REST API provides endpoints to access product data from the e-commerce database. Built with Flask and SQLite, it offers comprehensive product information with filtering, pagination, and error handling.

## 🛠️ Technology Stack

- **Backend Framework**: Flask (Python)
- **Database**: SQLite
- **CORS**: Enabled for frontend integration
- **Response Format**: JSON
- **HTTP Status Codes**: Standard REST conventions

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Database setup (run `python init_database.py` first)

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python app.py
```

The API will be available at: `http://localhost:5000`

## 📚 API Endpoints

### 1. Home Endpoint
**GET /** - API information and available endpoints

**Response:**
```json
{
  "message": "E-commerce REST API - Milestone 2",
  "version": "1.0.0",
  "endpoints": {
    "GET /api/products": "List all products (with optional pagination)",
    "GET /api/products/<id>": "Get specific product by ID",
    "GET /api/products/categories": "Get all product categories",
    "GET /api/products/brands": "Get all product brands",
    "GET /api/products/stats": "Get product statistics"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. Get All Products
**GET /api/products** - List all products with optional pagination and filtering

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `category` (optional): Filter by category
- `brand` (optional): Filter by brand
- `department` (optional): Filter by department (Men/Women)
- `min_price` (optional): Minimum price filter
- `max_price` (optional): Maximum price filter

**Example Requests:**
```bash
# Get all products (first 20)
curl http://localhost:5000/api/products

# Get products with pagination
curl http://localhost:5000/api/products?page=1&limit=5

# Get products by category
curl http://localhost:5000/api/products?category=Jeans

# Get products by price range
curl http://localhost:5000/api/products?min_price=50&max_price=100

# Get women's products with pagination
curl http://localhost:5000/api/products?department=Women&page=1&limit=10
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Seven7 Women's Long Sleeve Stripe Belted Top",
      "brand": "Seven7",
      "category": "Tops & Tees",
      "department": "Women",
      "retail_price": 49.0,
      "cost": 27.05,
      "sku": "C4CA4238A0B923820DCC509A6F75849B",
      "distribution_center": "Memphis TN",
      "dc_latitude": 35.1174,
      "dc_longitude": -89.9711
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_items": 29120,
    "total_pages": 1456,
    "has_next": true,
    "has_prev": false
  },
  "filters_applied": {
    "category": null,
    "brand": null,
    "department": null,
    "min_price": null,
    "max_price": null
  }
}
```

### 3. Get Product by ID
**GET /api/products/{id}** - Get a specific product by its ID

**Example Request:**
```bash
curl http://localhost:5000/api/products/1
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Seven7 Women's Long Sleeve Stripe Belted Top",
    "brand": "Seven7",
    "category": "Tops & Tees",
    "department": "Women",
    "retail_price": 49.0,
    "cost": 27.05,
    "sku": "C4CA4238A0B923820DCC509A6F75849B",
    "distribution_center": "Memphis TN",
    "dc_latitude": 35.1174,
    "dc_longitude": -89.9711
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Product not found",
  "message": "No product found with ID 99999"
}
```

### 4. Get Product Categories
**GET /api/products/categories** - Get all product categories with statistics

**Example Request:**
```bash
curl http://localhost:5000/api/products/categories
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "category": "Intimates",
      "product_count": 2363,
      "avg_price": 45.23,
      "min_price": 0.02,
      "max_price": 999.0
    },
    {
      "category": "Jeans",
      "product_count": 1999,
      "avg_price": 78.45,
      "min_price": 12.50,
      "max_price": 450.0
    }
  ]
}
```

### 5. Get Product Brands
**GET /api/products/brands** - Get all product brands with counts

**Example Request:**
```bash
curl http://localhost:5000/api/products/brands
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "brand": "Calvin Klein",
      "product_count": 125,
      "avg_price": 89.50
    },
    {
      "brand": "Nike",
      "product_count": 98,
      "avg_price": 65.30
    }
  ]
}
```

### 6. Get Product Statistics
**GET /api/products/stats** - Get overall product statistics

**Example Request:**
```bash
curl http://localhost:5000/api/products/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_products": 29120,
    "unique_categories": 26,
    "unique_brands": 2756,
    "departments": 2,
    "avg_price": 59.22,
    "min_price": 0.02,
    "max_price": 999.0,
    "men_products": 13131,
    "women_products": 15989
  }
}
```

## 🔧 Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (product not found)
- **500**: Internal Server Error

### Error Response Format
```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

## 🧪 Testing

### Automated Testing
Run the test script to verify all endpoints:
```bash
python test_api.py
```

### Manual Testing with curl
```bash
# Test home endpoint
curl http://localhost:5000/

# Test products endpoint
curl http://localhost:5000/api/products

# Test specific product
curl http://localhost:5000/api/products/1

# Test with filters
curl "http://localhost:5000/api/products?category=Jeans&limit=5"
```

### Testing with Postman
1. Import the API endpoints into Postman
2. Set base URL: `http://localhost:5000`
3. Test each endpoint with different parameters

## 📊 Database Schema

The API connects to the SQLite database with the following product table structure:

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    cost REAL,
    category TEXT,
    name TEXT,
    brand TEXT,
    retail_price REAL,
    department TEXT,
    sku TEXT,
    distribution_center_id INTEGER
);
```

## 🔒 CORS Configuration

CORS is enabled for frontend integration. The API accepts requests from any origin during development.

## 📈 Performance Features

- **Pagination**: Efficient handling of large datasets
- **Filtering**: Multiple filter options for precise queries
- **Database Indexing**: Optimized queries using primary keys
- **Connection Pooling**: Efficient database connection management

## 🚀 Deployment Considerations

For production deployment:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up proper CORS configuration
3. Implement authentication/authorization
4. Add rate limiting
5. Use environment variables for configuration
6. Set up logging and monitoring

## 📝 Example Usage Scenarios

### E-commerce Frontend Integration
```javascript
// Get products for a category page
fetch('/api/products?category=Jeans&page=1&limit=12')
  .then(response => response.json())
  .then(data => {
    // Display products
    data.data.forEach(product => {
      console.log(product.name, product.retail_price);
    });
  });

// Get specific product details
fetch('/api/products/123')
  .then(response => response.json())
  .then(data => {
    // Display product details
    console.log(data.data);
  });
```

### Mobile App Integration
```python
# Python requests example
import requests

# Get products with filters
response = requests.get('http://localhost:5000/api/products', params={
    'category': 'Tops & Tees',
    'department': 'Women',
    'min_price': 30,
    'max_price': 100,
    'page': 1,
    'limit': 20
})

products = response.json()
```

## ✅ Milestone 2 Requirements Met

- ✅ **GET /api/products**: List all products with pagination
- ✅ **GET /api/products/{id}**: Get specific product by ID
- ✅ **Proper JSON response format**: All responses in JSON
- ✅ **Error handling**: 404 for not found, 400 for invalid ID, 500 for server errors
- ✅ **CORS headers**: Enabled for frontend integration
- ✅ **HTTP status codes**: Proper REST conventions
- ✅ **Database connection**: Reads from SQLite database
- ✅ **Testing support**: Test script and curl examples provided 