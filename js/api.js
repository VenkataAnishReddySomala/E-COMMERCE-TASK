// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API Service Class
class ApiService {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    // Generic fetch method with error handling
    async fetchAPI(endpoint, options = {}) {
        try {
            const url = `${this.baseURL}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Get all products with pagination and filters
    async getProducts(page = 1, limit = 12, filters = {}) {
        const params = new URLSearchParams({
            page: page.toString(),
            limit: limit.toString(),
            ...filters
        });

        return this.fetchAPI(`/products?${params}`);
    }

    // Get a single product by ID
    async getProduct(id) {
        return this.fetchAPI(`/products/${id}`);
    }

    // Get all categories
    async getCategories() {
        return this.fetchAPI('/products/categories');
    }

    // Get all brands
    async getBrands() {
        return this.fetchAPI('/products/brands');
    }

    // Get product statistics
    async getProductStats() {
        return this.fetchAPI('/products/stats');
    }

    // Search products (custom implementation)
    async searchProducts(query, page = 1, limit = 12) {
        const params = new URLSearchParams({
            page: page.toString(),
            limit: limit.toString(),
            search: query
        });

        return this.fetchAPI(`/products?${params}`);
    }
}

// Create global API instance
const api = new ApiService();

// API Response Handler
class ApiResponseHandler {
    static handleSuccess(data) {
        return {
            success: true,
            data: data,
            error: null
        };
    }

    static handleError(error) {
        return {
            success: false,
            data: null,
            error: error.message || 'An error occurred'
        };
    }

    static async execute(apiCall) {
        try {
            const data = await apiCall();
            return this.handleSuccess(data);
        } catch (error) {
            return this.handleError(error);
        }
    }
}

// Cache Manager for API responses
class CacheManager {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    set(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }

    get(key) {
        const cached = this.cache.get(key);
        if (!cached) return null;

        const isExpired = Date.now() - cached.timestamp > this.cacheTimeout;
        if (isExpired) {
            this.cache.delete(key);
            return null;
        }

        return cached.data;
    }

    clear() {
        this.cache.clear();
    }

    generateKey(endpoint, params = {}) {
        return `${endpoint}_${JSON.stringify(params)}`;
    }
}

// Create global cache instance
const cache = new CacheManager();

// Enhanced API Service with caching
class CachedApiService extends ApiService {
    async getProducts(page = 1, limit = 12, filters = {}) {
        const cacheKey = cache.generateKey('products', { page, limit, ...filters });
        const cachedData = cache.get(cacheKey);
        
        if (cachedData) {
            return cachedData;
        }

        const data = await super.getProducts(page, limit, filters);
        cache.set(cacheKey, data);
        return data;
    }

    async getCategories() {
        const cacheKey = cache.generateKey('categories');
        const cachedData = cache.get(cacheKey);
        
        if (cachedData) {
            return cachedData;
        }

        const data = await super.getCategories();
        cache.set(cacheKey, data);
        return data;
    }

    async getBrands() {
        const cacheKey = cache.generateKey('brands');
        const cachedData = cache.get(cacheKey);
        
        if (cachedData) {
            return cachedData;
        }

        const data = await super.getBrands();
        cache.set(cacheKey, data);
        return data;
    }

    async getProductStats() {
        const cacheKey = cache.generateKey('stats');
        const cachedData = cache.get(cacheKey);
        
        if (cachedData) {
            return cachedData;
        }

        const data = await super.getProductStats();
        cache.set(cacheKey, data);
        return data;
    }
}

// Create enhanced API instance
const cachedApi = new CachedApiService();

// Export for use in other modules
window.ApiService = ApiService;
window.ApiResponseHandler = ApiResponseHandler;
window.CacheManager = CacheManager;
window.api = cachedApi; 