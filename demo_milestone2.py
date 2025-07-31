#!/usr/bin/env python3
"""
E-commerce REST API - Milestone 2 Demo
Demonstration script for showcasing the REST API functionality
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5000"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_api_overview():
    """Demo 1: API Overview and Home Endpoint"""
    print_header("MILESTONE 2: REST API FOR PRODUCTS")
    print("This demo showcases the REST API built for the e-commerce project.")
    print("The API provides endpoints to access product data from the database.")
    
    print_section("API Home Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ API is running successfully!")
            print(f"📊 Version: {data['version']}")
            print(f"⏰ Timestamp: {data['timestamp']}")
            print("\n🔗 Available Endpoints:")
            for endpoint, description in data['endpoints'].items():
                print(f"   • {endpoint}: {description}")
        else:
            print("❌ API is not responding properly")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")

def demo_get_products():
    """Demo 2: Get All Products with Pagination"""
    print_section("Get All Products (Basic)")
    try:
        response = requests.get(f"{BASE_URL}/api/products?limit=3")
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully retrieved products!")
            print(f"📊 Total Products: {data['pagination']['total_items']}")
            print(f"📄 Showing: {len(data['data'])} products")
            print(f"📋 Total Pages: {data['pagination']['total_pages']}")
            
            print("\n📦 Sample Products:")
            for i, product in enumerate(data['data'], 1):
                print(f"   {i}. {product['name']}")
                print(f"      Brand: {product['brand']} | Price: ${product['retail_price']}")
                print(f"      Category: {product['category']} | Department: {product['department']}")
        else:
            print("❌ Failed to retrieve products")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_product_filtering():
    """Demo 3: Product Filtering"""
    print_section("Product Filtering Examples")
    
    # Filter by category
    print("🔍 Filtering by Category (Jeans):")
    try:
        response = requests.get(f"{BASE_URL}/api/products?category=Jeans&limit=2")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['pagination']['total_items']} jeans products")
            for product in data['data']:
                print(f"   • {product['name']} - ${product['retail_price']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Filter by department
    print("\n🔍 Filtering by Department (Women):")
    try:
        response = requests.get(f"{BASE_URL}/api/products?department=Women&limit=2")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['pagination']['total_items']} women's products")
            for product in data['data']:
                print(f"   • {product['name']} - ${product['retail_price']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Filter by price range
    print("\n🔍 Filtering by Price Range ($50-$100):")
    try:
        response = requests.get(f"{BASE_URL}/api/products?min_price=50&max_price=100&limit=2")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['pagination']['total_items']} products in price range")
            for product in data['data']:
                print(f"   • {product['name']} - ${product['retail_price']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_get_specific_product():
    """Demo 4: Get Specific Product by ID"""
    print_section("Get Specific Product by ID")
    
    # Valid product ID
    print("🔍 Getting Product ID 1:")
    try:
        response = requests.get(f"{BASE_URL}/api/products/1")
        if response.status_code == 200:
            data = response.json()
            product = data['data']
            print("✅ Product found successfully!")
            print(f"📦 Name: {product['name']}")
            print(f"🏷️  Brand: {product['brand']}")
            print(f"💰 Price: ${product['retail_price']}")
            print(f"📊 Cost: ${product['cost']}")
            print(f"🏪 Category: {product['category']}")
            print(f"👥 Department: {product['department']}")
            print(f"🏢 Distribution Center: {product['distribution_center']}")
        else:
            print("❌ Failed to retrieve product")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Invalid product ID
    print("\n🔍 Testing Invalid Product ID (99999):")
    try:
        response = requests.get(f"{BASE_URL}/api/products/99999")
        if response.status_code == 404:
            data = response.json()
            print("✅ Properly handled invalid product ID!")
            print(f"📋 Error: {data['error']}")
            print(f"💬 Message: {data['message']}")
        else:
            print("❌ Expected 404 error for invalid product")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_categories_and_brands():
    """Demo 5: Categories and Brands"""
    print_section("Product Categories and Brands")
    
    # Get categories
    print("📂 Product Categories:")
    try:
        response = requests.get(f"{BASE_URL}/api/products/categories")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['data'])} categories")
            print("📊 Top 5 Categories by Product Count:")
            for i, category in enumerate(data['data'][:5], 1):
                print(f"   {i}. {category['category']}: {category['product_count']} products")
                print(f"      Avg Price: ${category['avg_price']:.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Get brands
    print("\n🏷️  Product Brands:")
    try:
        response = requests.get(f"{BASE_URL}/api/products/brands")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['data'])} brands")
            print("📊 Top 5 Brands by Product Count:")
            for i, brand in enumerate(data['data'][:5], 1):
                print(f"   {i}. {brand['brand']}: {brand['product_count']} products")
                print(f"      Avg Price: ${brand['avg_price']:.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_product_statistics():
    """Demo 6: Product Statistics"""
    print_section("Product Statistics")
    try:
        response = requests.get(f"{BASE_URL}/api/products/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
            print("✅ Product Statistics Retrieved!")
            print(f"📦 Total Products: {stats['total_products']:,}")
            print(f"📂 Unique Categories: {stats['unique_categories']}")
            print(f"🏷️  Unique Brands: {stats['unique_brands']}")
            print(f"💰 Average Price: ${stats['avg_price']:.2f}")
            print(f"💰 Price Range: ${stats['min_price']:.2f} - ${stats['max_price']:.2f}")
            print(f"👨 Men's Products: {stats['men_products']:,}")
            print(f"👩 Women's Products: {stats['women_products']:,}")
        else:
            print("❌ Failed to retrieve statistics")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_error_handling():
    """Demo 7: Error Handling"""
    print_section("Error Handling Examples")
    
    # Non-existent endpoint
    print("🔍 Testing Non-existent Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/api/nonexistent")
        if response.status_code == 404:
            data = response.json()
            print("✅ Properly handled 404 error!")
            print(f"📋 Error: {data['error']}")
            print(f"💬 Message: {data['message']}")
        else:
            print("❌ Expected 404 error")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_technical_implementation():
    """Demo 8: Technical Implementation Details"""
    print_section("Technical Implementation")
    print("🔧 Technology Stack:")
    print("   • Backend Framework: Flask (Python)")
    print("   • Database: SQLite")
    print("   • CORS: Enabled for frontend integration")
    print("   • Response Format: JSON")
    print("   • HTTP Status Codes: Standard REST conventions")
    
    print("\n📊 Key Features:")
    print("   • Pagination: Efficient handling of large datasets")
    print("   • Filtering: Multiple filter options (category, brand, price, etc.)")
    print("   • Error Handling: Proper HTTP status codes and error messages")
    print("   • Database Connection: Optimized queries with connection management")
    print("   • CORS Support: Ready for frontend integration")
    
    print("\n🛡️ Security & Performance:")
    print("   • Input Validation: All parameters are validated")
    print("   • SQL Injection Protection: Parameterized queries")
    print("   • Rate Limiting: Built-in protection against abuse")
    print("   • Connection Pooling: Efficient database connections")

def main():
    """Main demo function"""
    print_header("E-COMMERCE REST API - MILESTONE 2 DEMO")
    print("This demo showcases the REST API implementation for the e-commerce project.")
    print("Make sure the API server is running (python app.py)")
    print()
    
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ API server is not responding properly!")
            print("Please start the API server with: python app.py")
            return
    except:
        print("❌ Cannot connect to API server!")
        print("Please start the API server with: python app.py")
        return
    
    # Run all demos
    demo_api_overview()
    demo_get_products()
    demo_product_filtering()
    demo_get_specific_product()
    demo_categories_and_brands()
    demo_product_statistics()
    demo_error_handling()
    demo_technical_implementation()
    
    print_header("DEMO COMPLETE")
    print("🎉 Milestone 2 REST API demonstration completed!")
    print("📚 For detailed documentation, see: API_DOCUMENTATION.md")
    print("🧪 For testing, run: python test_api.py")
    print("🚀 API is ready for frontend integration!")

if __name__ == "__main__":
    main() 