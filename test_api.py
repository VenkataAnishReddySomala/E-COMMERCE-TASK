#!/usr/bin/env python3
"""
Test script for E-commerce REST API - Milestone 2
Tests all API endpoints to ensure they work correctly
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, description, expected_status=200):
    """Test a single API endpoint"""
    print(f"\n🔍 Testing: {description}")
    print(f"📍 Endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ Status: PASS")
            
            # Try to parse JSON response
            try:
                data = response.json()
                print(f"📄 Response Type: JSON")
                print(f"📏 Response Size: {len(response.text)} characters")
                
                # Show sample of response data
                if isinstance(data, dict):
                    if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                        print(f"📋 Sample Data: {data['data'][0]}")
                    elif 'message' in data:
                        print(f"📋 Message: {data['message']}")
                elif isinstance(data, list) and len(data) > 0:
                    print(f"📋 Sample Data: {data[0]}")
                    
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                print(f"📄 Raw Response: {response.text[:200]}...")
                
        else:
            print(f"❌ Status: FAIL (Expected {expected_status}, got {response.status_code})")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("-" * 60)

def test_api():
    """Run all API tests"""
    print("🚀 E-commerce REST API - Milestone 2 Testing")
    print("=" * 60)
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Test home endpoint
    test_endpoint("/", "API Home Endpoint")
    
    # Test products endpoint (basic)
    test_endpoint("/api/products", "Get All Products (Basic)")
    
    # Test products endpoint with pagination
    test_endpoint("/api/products?page=1&limit=5", "Get Products with Pagination")
    
    # Test products endpoint with filters
    test_endpoint("/api/products?category=Jeans&limit=3", "Get Products by Category")
    test_endpoint("/api/products?department=Women&limit=3", "Get Products by Department")
    test_endpoint("/api/products?min_price=50&max_price=100&limit=3", "Get Products by Price Range")
    
    # Test specific product endpoint
    test_endpoint("/api/products/1", "Get Product by ID (Valid)")
    test_endpoint("/api/products/99999", "Get Product by ID (Invalid)", 404)
    
    # Test categories endpoint
    test_endpoint("/api/products/categories", "Get Product Categories")
    
    # Test brands endpoint
    test_endpoint("/api/products/brands", "Get Product Brands")
    
    # Test stats endpoint
    test_endpoint("/api/products/stats", "Get Product Statistics")
    
    # Test error handling
    test_endpoint("/api/nonexistent", "Non-existent Endpoint", 404)
    
    print("\n🎉 API Testing Complete!")
    print("=" * 60)

def test_curl_commands():
    """Show curl commands for manual testing"""
    print("\n📋 CURL Commands for Manual Testing:")
    print("=" * 60)
    
    commands = [
        ("Get API Info", f"curl {BASE_URL}/"),
        ("Get All Products", f"curl {BASE_URL}/api/products"),
        ("Get Products with Pagination", f"curl {BASE_URL}/api/products?page=1&limit=5"),
        ("Get Products by Category", f"curl {BASE_URL}/api/products?category=Jeans"),
        ("Get Specific Product", f"curl {BASE_URL}/api/products/1"),
        ("Get Categories", f"curl {BASE_URL}/api/products/categories"),
        ("Get Brands", f"curl {BASE_URL}/api/products/brands"),
        ("Get Statistics", f"curl {BASE_URL}/api/products/stats"),
    ]
    
    for description, command in commands:
        print(f"\n{description}:")
        print(f"  {command}")

if __name__ == "__main__":
    print("🔧 API Testing Tool")
    print("Make sure the API server is running (python app.py)")
    print()
    
    # Wait a moment for user to read
    input("Press Enter to start testing...")
    
    # Run tests
    test_api()
    
    # Show curl commands
    test_curl_commands() 