-- =====================================================
-- SAMPLE QUERIES FOR E-COMMERCE DATASET
-- =====================================================

-- 1. SAMPLE PRODUCTS (First 10 records)
-- =====================================================
SELECT 
    id,
    name,
    brand,
    category,
    retail_price,
    department,
    sku
FROM products 
LIMIT 10;

-- 2. PRODUCTS BY CATEGORY (Top 5 from each major category)
-- =====================================================
SELECT 
    category,
    name,
    brand,
    retail_price,
    department
FROM products 
WHERE category IN ('Intimates', 'Jeans', 'Tops & Tees', 'Fashion Hoodies & Sweatshirts', 'Swim')
ORDER BY category, retail_price DESC
LIMIT 25;

-- 3. SAMPLE USERS (First 10 customers)
-- =====================================================
SELECT 
    id,
    first_name,
    last_name,
    email,
    age,
    gender,
    city,
    country,
    traffic_source
FROM users 
LIMIT 10;

-- 4. USERS BY COUNTRY (Sample from different countries)
-- =====================================================
SELECT 
    country,
    first_name,
    last_name,
    email,
    age,
    gender
FROM users 
WHERE country IN ('United States', 'Brasil', 'South Korea', 'Canada', 'United Kingdom')
ORDER BY country, first_name
LIMIT 20;

-- 5. SAMPLE ORDERS (First 10 orders)
-- =====================================================
SELECT 
    order_id,
    user_id,
    status,
    gender,
    created_at,
    num_of_item
FROM orders 
LIMIT 10;

-- 6. ORDERS BY STATUS (Sample from each status)
-- =====================================================
SELECT 
    status,
    order_id,
    user_id,
    created_at,
    num_of_item
FROM orders 
WHERE status IN ('Shipped', 'Complete', 'Processing', 'Cancelled', 'Returned')
ORDER BY status, created_at
LIMIT 25;

-- 7. SAMPLE ORDER ITEMS (First 10 items)
-- =====================================================
SELECT 
    id,
    order_id,
    product_id,
    status,
    sale_price,
    created_at
FROM order_items 
LIMIT 10;

-- 8. ORDER ITEMS WITH PRODUCT DETAILS (Sample)
-- =====================================================
SELECT 
    oi.id,
    oi.order_id,
    oi.sale_price,
    oi.status,
    p.name as product_name,
    p.brand,
    p.category
FROM order_items oi
JOIN products p ON oi.product_id = p.id
LIMIT 15;

-- 9. SAMPLE INVENTORY ITEMS (First 10)
-- =====================================================
SELECT 
    id,
    product_id,
    created_at,
    sold_at,
    cost,
    product_category,
    product_name
FROM inventory_items 
LIMIT 10;

-- 10. INVENTORY ITEMS BY STATUS (Available vs Sold)
-- =====================================================
SELECT 
    CASE 
        WHEN sold_at IS NULL THEN 'Available'
        ELSE 'Sold'
    END as status,
    product_name,
    product_category,
    cost,
    created_at,
    sold_at
FROM inventory_items 
ORDER BY status, created_at
LIMIT 20;

-- 11. DISTRIBUTION CENTERS (All 10 centers)
-- =====================================================
SELECT 
    id,
    name,
    latitude,
    longitude
FROM distribution_centers
ORDER BY id;

-- 12. PRODUCTS BY DISTRIBUTION CENTER (Sample)
-- =====================================================
SELECT 
    dc.name as distribution_center,
    p.name as product_name,
    p.category,
    p.retail_price
FROM products p
JOIN distribution_centers dc ON p.distribution_center_id = dc.id
ORDER BY dc.name, p.category
LIMIT 20;

-- 13. COMPLETE ORDER DETAILS (Sample with all related data)
-- =====================================================
SELECT 
    o.order_id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.email,
    o.status as order_status,
    o.created_at as order_date,
    oi.sale_price,
    p.name as product_name,
    p.category,
    p.brand
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.id
ORDER BY o.order_id
LIMIT 15;

-- 14. PRODUCT STATISTICS BY DEPARTMENT
-- =====================================================
SELECT 
    department,
    COUNT(*) as total_products,
    AVG(retail_price) as avg_price,
    MIN(retail_price) as min_price,
    MAX(retail_price) as max_price,
    COUNT(DISTINCT category) as unique_categories
FROM products 
GROUP BY department
ORDER BY total_products DESC;

-- 15. TOP BRANDS BY PRODUCT COUNT
-- =====================================================
SELECT 
    brand,
    COUNT(*) as product_count,
    AVG(retail_price) as avg_price
FROM products 
GROUP BY brand
HAVING COUNT(*) > 10
ORDER BY product_count DESC
LIMIT 10;

-- 16. CUSTOMER ORDER SUMMARY (Sample customers with order counts)
-- =====================================================
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.num_of_item) as total_items_ordered
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.first_name, u.last_name, u.email
HAVING COUNT(o.order_id) > 0
ORDER BY total_orders DESC
LIMIT 15;

-- 17. RECENT ORDERS (Last 10 orders)
-- =====================================================
SELECT 
    order_id,
    user_id,
    status,
    created_at,
    num_of_item
FROM orders 
ORDER BY created_at DESC
LIMIT 10;

-- 18. HIGH-VALUE PRODUCTS (Products over $200)
-- =====================================================
SELECT 
    id,
    name,
    brand,
    category,
    retail_price,
    department
FROM products 
WHERE retail_price > 200
ORDER BY retail_price DESC
LIMIT 10;

-- 19. PRODUCTS BY PRICE RANGE
-- =====================================================
SELECT 
    CASE 
        WHEN retail_price < 25 THEN 'Budget ($0-$25)'
        WHEN retail_price < 50 THEN 'Mid-Range ($25-$50)'
        WHEN retail_price < 100 THEN 'Premium ($50-$100)'
        ELSE 'Luxury ($100+)'
    END as price_range,
    COUNT(*) as product_count,
    AVG(retail_price) as avg_price
FROM products 
GROUP BY 
    CASE 
        WHEN retail_price < 25 THEN 'Budget ($0-$25)'
        WHEN retail_price < 50 THEN 'Mid-Range ($25-$50)'
        WHEN retail_price < 100 THEN 'Premium ($50-$100)'
        ELSE 'Luxury ($100+)'
    END
ORDER BY avg_price;

-- 20. SAMPLE DATA FOR DEMO (Most comprehensive query)
-- =====================================================
SELECT 
    'PRODUCTS' as table_name,
    id,
    name as description,
    retail_price as value,
    category as category
FROM products 
WHERE id <= 5

UNION ALL

SELECT 
    'USERS' as table_name,
    id,
    first_name || ' ' || last_name as description,
    age as value,
    country as category
FROM users 
WHERE id <= 5

UNION ALL

SELECT 
    'ORDERS' as table_name,
    order_id as id,
    status as description,
    num_of_item as value,
    'Order' as category
FROM orders 
WHERE order_id <= 5

ORDER BY table_name, id; 