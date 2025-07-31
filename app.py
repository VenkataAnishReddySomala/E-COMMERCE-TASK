#!/usr/bin/env python3
"""
E-commerce REST API - Milestone 2
Flask application providing RESTful API endpoints for products
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Database configuration
DATABASE = 'ecommerce.db'

def get_db_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def dict_from_row(row):
    """Convert sqlite3.Row object to dictionary"""
    return dict(zip(row.keys(), row))

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'message': 'E-commerce REST API - Milestone 2',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/products': 'List all products (with optional pagination)',
            'GET /api/products/<id>': 'Get specific product by ID',
            'GET /api/products/categories': 'Get all product categories',
            'GET /api/products/brands': 'Get all product brands',
            'GET /api/products/stats': 'Get product statistics'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    GET /api/products - List all products with optional pagination
    Query parameters:
    - page: Page number (default: 1)
    - limit: Items per page (default: 20, max: 100)
    - category: Filter by category
    - brand: Filter by brand
    - department: Filter by department (Men/Women)
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit', 20, type=int), 100)  # Max 100 items per page
        category = request.args.get('category')
        brand = request.args.get('brand')
        department = request.args.get('department')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Calculate offset for pagination
        offset = (page - 1) * limit
        
        # Build the query
        query = """
            SELECT 
                p.id,
                p.name,
                p.brand,
                p.category,
                p.department,
                p.retail_price,
                p.cost,
                p.sku,
                dc.name as distribution_center,
                dc.latitude as dc_latitude,
                dc.longitude as dc_longitude
            FROM products p
            LEFT JOIN distribution_centers dc ON p.distribution_center_id = dc.id
            WHERE 1=1
        """
        
        params = []
        
        # Add filters
        if category:
            query += " AND p.category = ?"
            params.append(category)
        
        if brand:
            query += " AND p.brand = ?"
            params.append(brand)
        
        if department:
            query += " AND p.department = ?"
            params.append(department)
        
        if min_price is not None:
            query += " AND p.retail_price >= ?"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND p.retail_price <= ?"
            params.append(max_price)
        
        # Add ordering and pagination
        query += " ORDER BY p.id LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        # Get total count for pagination
        count_query = """
            SELECT COUNT(*) as total
            FROM products p
            WHERE 1=1
        """
        
        count_params = []
        if category:
            count_query += " AND p.category = ?"
            count_params.append(category)
        if brand:
            count_query += " AND p.brand = ?"
            count_params.append(brand)
        if department:
            count_query += " AND p.department = ?"
            count_params.append(department)
        if min_price is not None:
            count_query += " AND p.retail_price >= ?"
            count_params.append(min_price)
        if max_price is not None:
            count_query += " AND p.retail_price <= ?"
            count_params.append(max_price)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            # Get total count
            cursor = conn.execute(count_query, count_params)
            total_count = cursor.fetchone()['total']
            
            # Get products
            cursor = conn.execute(query, params)
            products = [dict_from_row(row) for row in cursor.fetchall()]
            
            # Calculate pagination info
            total_pages = (total_count + limit - 1) // limit
            
            return jsonify({
                'success': True,
                'data': products,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total_items': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': {
                    'category': category,
                    'brand': brand,
                    'department': department,
                    'min_price': min_price,
                    'max_price': max_price
                }
            })
            
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error in get_products: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    GET /api/products/{id} - Get a specific product by ID
    """
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            query = """
                SELECT 
                    p.id,
                    p.name,
                    p.brand,
                    p.category,
                    p.department,
                    p.retail_price,
                    p.cost,
                    p.sku,
                    dc.name as distribution_center,
                    dc.latitude as dc_latitude,
                    dc.longitude as dc_longitude
                FROM products p
                LEFT JOIN distribution_centers dc ON p.distribution_center_id = dc.id
                WHERE p.id = ?
            """
            
            cursor = conn.execute(query, (product_id,))
            product = cursor.fetchone()
            
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found',
                    'message': f'No product found with ID {product_id}'
                }), 404
            
            return jsonify({
                'success': True,
                'data': dict_from_row(product)
            })
            
        finally:
            conn.close()
            
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid product ID',
            'message': 'Product ID must be a valid integer'
        }), 400
    except Exception as e:
        logger.error(f"Error in get_product: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    """GET /api/products/categories - Get all product categories with counts"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            query = """
                SELECT 
                    category,
                    COUNT(*) as product_count,
                    AVG(retail_price) as avg_price,
                    MIN(retail_price) as min_price,
                    MAX(retail_price) as max_price
                FROM products
                GROUP BY category
                ORDER BY product_count DESC
            """
            
            cursor = conn.execute(query)
            categories = [dict_from_row(row) for row in cursor.fetchall()]
            
            return jsonify({
                'success': True,
                'data': categories
            })
            
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error in get_categories: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/brands', methods=['GET'])
def get_brands():
    """GET /api/products/brands - Get all product brands with counts"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            query = """
                SELECT 
                    brand,
                    COUNT(*) as product_count,
                    AVG(retail_price) as avg_price
                FROM products
                GROUP BY brand
                HAVING COUNT(*) > 1
                ORDER BY product_count DESC
                LIMIT 50
            """
            
            cursor = conn.execute(query)
            brands = [dict_from_row(row) for row in cursor.fetchall()]
            
            return jsonify({
                'success': True,
                'data': brands
            })
            
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error in get_brands: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/stats', methods=['GET'])
def get_product_stats():
    """GET /api/products/stats - Get product statistics"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            query = """
                SELECT 
                    COUNT(*) as total_products,
                    COUNT(DISTINCT category) as unique_categories,
                    COUNT(DISTINCT brand) as unique_brands,
                    COUNT(DISTINCT department) as departments,
                    AVG(retail_price) as avg_price,
                    MIN(retail_price) as min_price,
                    MAX(retail_price) as max_price,
                    SUM(CASE WHEN department = 'Men' THEN 1 ELSE 0 END) as men_products,
                    SUM(CASE WHEN department = 'Women' THEN 1 ELSE 0 END) as women_products
                FROM products
            """
            
            cursor = conn.execute(query)
            stats = dict_from_row(cursor.fetchone())
            
            return jsonify({
                'success': True,
                'data': stats
            })
            
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error in get_product_stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists(DATABASE):
        print(f"❌ Database file '{DATABASE}' not found!")
        print("Please run 'python init_database.py' first to create the database.")
        exit(1)
    
    print("🚀 Starting E-commerce REST API...")
    print("📍 API will be available at: http://localhost:5000")
    print("📚 API Documentation available at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 