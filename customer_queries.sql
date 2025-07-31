-- =====================================================
-- CUSTOMER DETAILS QUERIES FOR E-COMMERCE DATASET
-- =====================================================

-- 1. BASIC CUSTOMER INFORMATION (First 10 customers)
-- =====================================================
SELECT 
    id,
    first_name,
    last_name,
    email,
    age,
    gender,
    city,
    state,
    country,
    traffic_source,
    created_at
FROM users 
LIMIT 10;

-- 2. CUSTOMER DEMOGRAPHICS BY COUNTRY
-- =====================================================
SELECT 
    country,
    COUNT(*) as total_customers,
    AVG(age) as avg_age,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) as female_count,
    COUNT(DISTINCT city) as unique_cities
FROM users 
GROUP BY country
ORDER BY total_customers DESC
LIMIT 15;

-- 3. CUSTOMER AGE DISTRIBUTION
-- =====================================================
SELECT 
    CASE 
        WHEN age < 18 THEN 'Under 18'
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 50 THEN '36-50'
        WHEN age BETWEEN 51 AND 65 THEN '51-65'
        ELSE 'Over 65'
    END as age_group,
    COUNT(*) as customer_count,
    ROUND(AVG(age), 1) as avg_age
FROM users 
GROUP BY 
    CASE 
        WHEN age < 18 THEN 'Under 18'
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 50 THEN '36-50'
        WHEN age BETWEEN 51 AND 65 THEN '51-65'
        ELSE 'Over 65'
    END
ORDER BY avg_age;

-- 4. CUSTOMERS BY TRAFFIC SOURCE
-- =====================================================
SELECT 
    traffic_source,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as percentage
FROM users 
GROUP BY traffic_source
ORDER BY customer_count DESC;

-- 5. TOP CITIES BY CUSTOMER COUNT
-- =====================================================
SELECT 
    city,
    country,
    COUNT(*) as customer_count,
    AVG(age) as avg_age,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) as female_count
FROM users 
GROUP BY city, country
HAVING COUNT(*) > 5
ORDER BY customer_count DESC
LIMIT 20;

-- 6. CUSTOMER LOCATION DETAILS (Sample from different countries)
-- =====================================================
SELECT 
    id,
    first_name || ' ' || last_name as full_name,
    email,
    age,
    gender,
    street_address,
    city,
    state,
    postal_code,
    country,
    latitude,
    longitude
FROM users 
WHERE country IN ('United States', 'Brasil', 'South Korea', 'Canada', 'United Kingdom')
ORDER BY country, first_name
LIMIT 15;

-- 7. CUSTOMERS WITH ORDER HISTORY (Active customers)
-- =====================================================
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.email,
    u.age,
    u.gender,
    u.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.num_of_item) as total_items_ordered,
    MAX(o.created_at) as last_order_date
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.first_name, u.last_name, u.email, u.age, u.gender, u.country
ORDER BY total_orders DESC
LIMIT 20;

-- 8. CUSTOMER PURCHASE BEHAVIOR ANALYSIS
-- =====================================================
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.country,
    COUNT(o.order_id) as order_count,
    SUM(o.num_of_item) as total_items,
    AVG(o.num_of_item) as avg_items_per_order,
    COUNT(DISTINCT o.status) as order_statuses_used,
    MIN(o.created_at) as first_order,
    MAX(o.created_at) as last_order
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.first_name, u.last_name, u.country
HAVING COUNT(o.order_id) > 0
ORDER BY order_count DESC
LIMIT 15;

-- 9. CUSTOMERS BY ORDER STATUS PREFERENCE
-- =====================================================
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.email,
    u.country,
    o.status as preferred_status,
    COUNT(*) as status_count
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.first_name, u.last_name, u.email, u.country, o.status
HAVING COUNT(*) > 1
ORDER BY u.id, status_count DESC
LIMIT 20;

-- 10. CUSTOMER SPENDING ANALYSIS
-- =====================================================
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.country,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.sale_price) as total_spent,
    AVG(oi.sale_price) as avg_order_value,
    MAX(oi.sale_price) as highest_single_purchase
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.id, u.first_name, u.last_name, u.country
ORDER BY total_spent DESC
LIMIT 15;

-- 11. NEW CUSTOMERS (Recently registered)
-- =====================================================
SELECT 
    id,
    first_name || ' ' || last_name as customer_name,
    email,
    age,
    gender,
    country,
    created_at as registration_date
FROM users 
ORDER BY created_at DESC
LIMIT 15;

-- 12. CUSTOMER GENDER DISTRIBUTION BY COUNTRY
-- =====================================================
SELECT 
    country,
    COUNT(*) as total_customers,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) as male_customers,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) as female_customers,
    ROUND(COUNT(CASE WHEN gender = 'M' THEN 1 END) * 100.0 / COUNT(*), 2) as male_percentage,
    ROUND(COUNT(CASE WHEN gender = 'F' THEN 1 END) * 100.0 / COUNT(*), 2) as female_percentage
FROM users 
GROUP BY country
ORDER BY total_customers DESC
LIMIT 10;

-- 13. CUSTOMERS WITH COMPLETE PROFILES
-- =====================================================
SELECT 
    id,
    first_name || ' ' || last_name as customer_name,
    email,
    age,
    gender,
    street_address,
    city,
    state,
    postal_code,
    country,
    traffic_source,
    created_at
FROM users 
WHERE first_name IS NOT NULL 
  AND last_name IS NOT NULL 
  AND email IS NOT NULL 
  AND age IS NOT NULL 
  AND gender IS NOT NULL
  AND street_address IS NOT NULL
  AND city IS NOT NULL
  AND country IS NOT NULL
LIMIT 10;

-- 14. CUSTOMER ACTIVITY TIMELINE (Sample)
-- =====================================================
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.created_at as registration_date,
    o.order_id,
    o.created_at as order_date,
    o.status as order_status,
    o.num_of_item as items_ordered
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id <= 10
ORDER BY u.id, o.created_at;

-- 15. CUSTOMER SEGMENTATION BY ACTIVITY
-- =====================================================
SELECT 
    CASE 
        WHEN order_count = 0 THEN 'No Orders'
        WHEN order_count = 1 THEN 'Single Order'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Regular Customer'
        WHEN order_count BETWEEN 6 AND 10 THEN 'Frequent Customer'
        ELSE 'VIP Customer'
    END as customer_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(age), 1) as avg_age,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as percentage
FROM (
    SELECT 
        u.id,
        u.age,
        COUNT(o.order_id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id, u.age
) customer_orders
GROUP BY 
    CASE 
        WHEN order_count = 0 THEN 'No Orders'
        WHEN order_count = 1 THEN 'Single Order'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Regular Customer'
        WHEN order_count BETWEEN 6 AND 10 THEN 'Frequent Customer'
        ELSE 'VIP Customer'
    END
ORDER BY customer_count DESC;

-- 16. CUSTOMER DETAILS WITH ORDER SUMMARY (Comprehensive view)
-- =====================================================
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name as customer_name,
    u.email,
    u.age,
    u.gender,
    u.country,
    u.city,
    u.traffic_source,
    u.created_at as registration_date,
    COUNT(o.order_id) as total_orders,
    SUM(o.num_of_item) as total_items_ordered,
    SUM(oi.sale_price) as total_spent,
    MAX(o.created_at) as last_order_date,
    COUNT(DISTINCT o.status) as order_statuses_used
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.id, u.first_name, u.last_name, u.email, u.age, u.gender, 
         u.country, u.city, u.traffic_source, u.created_at
ORDER BY total_orders DESC, total_spent DESC
LIMIT 20; 