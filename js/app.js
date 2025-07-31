// Main Application Class
class ECommerceApp {
    constructor() {
        this.currentPage = 1;
        this.currentFilters = {};
        this.productsPerPage = 12;
        this.currentView = 'products';
        this.cart = [];
        
        this.initializeApp();
    }

    async initializeApp() {
        try {
            await this.setupEventListeners();
            await this.loadInitialData();
            await this.loadProducts();
        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.showError('Failed to initialize the application. Please refresh the page.');
        }
    }

    setupEventListeners() {
        // Search functionality
        const searchToggle = document.getElementById('searchToggle');
        const searchContainer = document.getElementById('searchContainer');
        const searchInput = document.getElementById('searchInput');

        searchToggle.addEventListener('click', () => {
            searchContainer.classList.toggle('active');
            if (searchContainer.classList.contains('active')) {
                searchInput.focus();
            }
        });

        // Search input with debouncing
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.handleSearch(e.target.value);
            }, 500);
        });

        // Filter change events
        document.getElementById('categoryFilter').addEventListener('change', (e) => {
            this.currentFilters.category = e.target.value;
            this.currentPage = 1;
            this.loadProducts();
        });

        document.getElementById('brandFilter').addEventListener('change', (e) => {
            this.currentFilters.brand = e.target.value;
            this.currentPage = 1;
            this.loadProducts();
        });

        document.getElementById('priceFilter').addEventListener('change', (e) => {
            this.currentFilters.price_range = e.target.value;
            this.currentPage = 1;
            this.loadProducts();
        });

        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const view = e.target.dataset.view;
                this.switchView(view);
            });
        });
    }

    async loadInitialData() {
        try {
            // Load categories and brands for filters
            const [categoriesResponse, brandsResponse] = await Promise.all([
                ApiResponseHandler.execute(() => api.getCategories()),
                ApiResponseHandler.execute(() => api.getBrands())
            ]);

            if (categoriesResponse.success) {
                this.populateCategoryFilter(categoriesResponse.data);
            }

            if (brandsResponse.success) {
                this.populateBrandFilter(brandsResponse.data);
            }
        } catch (error) {
            console.error('Failed to load initial data:', error);
        }
    }

    populateCategoryFilter(categories) {
        const select = document.getElementById('categoryFilter');
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.category;
            option.textContent = `${category.category} (${category.count})`;
            select.appendChild(option);
        });
    }

    populateBrandFilter(brands) {
        const select = document.getElementById('brandFilter');
        brands.forEach(brand => {
            const option = document.createElement('option');
            option.value = brand.brand;
            option.textContent = `${brand.brand} (${brand.count})`;
            select.appendChild(option);
        });
    }

    async loadProducts() {
        this.showLoading(true);
        this.hideError();

        try {
            const response = await ApiResponseHandler.execute(() => 
                api.getProducts(this.currentPage, this.productsPerPage, this.currentFilters)
            );

            if (response.success) {
                this.displayProducts(response.data);
                this.updatePagination(response.data);
            } else {
                this.showError(response.error);
            }
        } catch (error) {
            this.showError('Failed to load products. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    displayProducts(data) {
        const productsGrid = document.getElementById('productsGrid');
        productsGrid.innerHTML = '';

        if (!data.products || data.products.length === 0) {
            productsGrid.innerHTML = `
                <div class="no-products">
                    <i class="fas fa-box-open"></i>
                    <h3>No products found</h3>
                    <p>Try adjusting your filters or search terms.</p>
                </div>
            `;
            return;
        }

        data.products.forEach(product => {
            const productCard = this.createProductCard(product);
            productsGrid.appendChild(productCard);
        });
    }

    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-image">
                <i class="fas fa-image"></i>
            </div>
            <div class="product-info">
                <h3 class="product-name">${this.escapeHtml(product.name)}</h3>
                <p class="product-brand">${this.escapeHtml(product.brand)}</p>
                <p class="product-category">${this.escapeHtml(product.category)}</p>
                <p class="product-price">$${parseFloat(product.price).toFixed(2)}</p>
                <div class="product-actions">
                    <button class="btn-view" onclick="app.viewProduct(${product.id})">
                        View Details
                    </button>
                    <button class="btn-add-cart" onclick="app.addToCart(${product.id})">
                        <i class="fas fa-cart-plus"></i>
                    </button>
                </div>
            </div>
        `;
        return card;
    }

    async viewProduct(productId) {
        this.showLoading(true);
        this.hideError();

        try {
            const response = await ApiResponseHandler.execute(() => 
                api.getProduct(productId)
            );

            if (response.success) {
                this.displayProductDetail(response.data);
            } else {
                this.showError(response.error);
            }
        } catch (error) {
            this.showError('Failed to load product details.');
        } finally {
            this.showLoading(false);
        }
    }

    displayProductDetail(product) {
        const productsContainer = document.getElementById('productsContainer');
        const productDetail = document.getElementById('productDetail');
        const productDetailContent = document.getElementById('productDetailContent');

        productsContainer.style.display = 'none';
        productDetail.style.display = 'block';

        productDetailContent.innerHTML = `
            <div class="product-detail-image">
                <i class="fas fa-image"></i>
            </div>
            <div class="product-detail-info">
                <h1>${this.escapeHtml(product.name)}</h1>
                <div class="product-detail-meta">
                    <p><strong>Brand:</strong> ${this.escapeHtml(product.brand)}</p>
                    <p><strong>Category:</strong> ${this.escapeHtml(product.category)}</p>
                    <p><strong>Department:</strong> ${this.escapeHtml(product.department)}</p>
                    <p><strong>Product ID:</strong> ${product.id}</p>
                </div>
                <div class="product-detail-price">$${parseFloat(product.price).toFixed(2)}</div>
                <div class="product-detail-description">
                    ${product.description ? this.escapeHtml(product.description) : 'No description available.'}
                </div>
                <div class="product-detail-actions">
                    <button class="btn-add-cart-large" onclick="app.addToCart(${product.id})">
                        <i class="fas fa-cart-plus"></i> Add to Cart
                    </button>
                </div>
            </div>
        `;
    }

    showProductsList() {
        const productsContainer = document.getElementById('productsContainer');
        const productDetail = document.getElementById('productDetail');

        productsContainer.style.display = 'block';
        productDetail.style.display = 'none';
    }

    updatePagination(data) {
        const currentPageSpan = document.getElementById('currentPage');
        const totalPagesSpan = document.getElementById('totalPages');
        const btnPrev = document.getElementById('btnPrev');
        const btnNext = document.getElementById('btnNext');

        const totalPages = Math.ceil(data.total / this.productsPerPage);
        
        currentPageSpan.textContent = this.currentPage;
        totalPagesSpan.textContent = totalPages;

        btnPrev.disabled = this.currentPage <= 1;
        btnNext.disabled = this.currentPage >= totalPages;
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.loadProducts();
        }
    }

    nextPage() {
        this.currentPage++;
        this.loadProducts();
    }

    async handleSearch(query) {
        if (query.trim() === '') {
            this.currentFilters = {};
            this.currentPage = 1;
            await this.loadProducts();
            return;
        }

        this.currentFilters.search = query.trim();
        this.currentPage = 1;
        await this.loadProducts();
    }

    clearFilters() {
        document.getElementById('categoryFilter').value = '';
        document.getElementById('brandFilter').value = '';
        document.getElementById('priceFilter').value = '';
        document.getElementById('searchInput').value = '';
        
        this.currentFilters = {};
        this.currentPage = 1;
        this.loadProducts();
    }

    switchView(view) {
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-view="${view}"]`).classList.add('active');

        this.currentView = view;
        
        // For now, just show products. Categories and brands views can be implemented later
        this.showProductsList();
        this.loadProducts();
    }

    addToCart(productId) {
        // Simple cart implementation
        this.cart.push(productId);
        this.updateCartCount();
        
        // Show success message
        this.showNotification('Product added to cart!', 'success');
    }

    updateCartCount() {
        const cartCount = document.querySelector('.cart-count');
        cartCount.textContent = this.cart.length;
    }

    showLoading(show) {
        const loadingSpinner = document.getElementById('loadingSpinner');
        loadingSpinner.style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        
        errorText.textContent = message;
        errorMessage.style.display = 'block';
    }

    hideError() {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.style.display = 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#28a745' : '#17a2b8'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .no-products {
        grid-column: 1 / -1;
        text-align: center;
        padding: 4rem 0;
        color: #6c757d;
    }
    
    .no-products i {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .no-products h3 {
        margin-bottom: 0.5rem;
        color: #495057;
    }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ECommerceApp();
});

// Global functions for onclick handlers
window.loadProducts = function() {
    app.loadProducts();
};

window.previousPage = function() {
    app.previousPage();
};

window.nextPage = function() {
    app.nextPage();
};

window.clearFilters = function() {
    app.clearFilters();
};

window.showProductsList = function() {
    app.showProductsList();
}; 