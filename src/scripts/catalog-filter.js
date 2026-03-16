/**
 * Catalog Filter Logic - NJAWAMU V3 (Optimized)
 * Loads data from products.json and implements infinite scroll
 */

document.addEventListener('DOMContentLoaded', () => {
    // Constants
    const ITEMS_PER_PAGE = 24;

    // State
    let allProducts = [];
    let filteredProducts = [];
    let displayedCount = 0;
    let isLoading = false;

    // DOM Elements
    const categorySelect = document.getElementById('filterCategory');
    const subcategorySelect = document.getElementById('filterSubcategory'); // Added
    const findProductsBtn = document.getElementById('findProductsBtn');
    const resetBtn = document.getElementById('resetFiltersBtn');
    const productGrid = document.getElementById('productGrid');
    const resultsCountEl = document.getElementById('resultsCount');
    const sortBySelect = document.getElementById('sortBy');
    const catalogSearchInput = document.querySelector('.search-part-input');
    const catalogSearchBtn = document.querySelector('.search-btn-v3');
    const catalogFilterBtn = document.getElementById('catalogFilterBtn');
    const filterBackdrop = document.getElementById('filterBackdrop');
    const catalogSidebar = document.querySelector('.catalog-sidebar');

    // --- Initialization ---

    async function init() {
        setupEventListeners();
        await loadProducts();
        initCategoryDropdown(); // Population happens after load

        // Handle initial URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const categoryParam = urlParams.get('category');
        const searchParam = urlParams.get('search');
        const itemParam = urlParams.get('item');

        if (categoryParam) {
            const mappedName = getCategoryFromSlug(categoryParam);
            categorySelect.value = mappedName;
            updateBreadcrumb(mappedName);
            updateSubcategoryOptions(mappedName);
        }

        if (itemParam && subcategorySelect) {
            // Basic matching for URL param
            const subcatMatch = Array.from(subcategorySelect.options).find(o => o.value.toLowerCase() === itemParam.toLowerCase());
            if (subcatMatch) subcategorySelect.value = subcatMatch.value;
        }

        applyFilters(searchParam || '');
    }

    async function loadProducts() {
        try {
            const response = await fetch('assets/data/products.json');
            if (!response.ok) throw new Error('Failed to load products');
            allProducts = await response.json();
            window.NJAWAMUProducts = allProducts;
        } catch (error) {
            console.error('Error fetching products:', error);
            allProducts = window.NJAWAMUProducts || [];
        }
    }

    function setupEventListeners() {
        catalogFilterBtn?.addEventListener('click', toggleMobileFilter);
        filterBackdrop?.addEventListener('click', closeMobileFilter);
        document.getElementById('closeFiltersBtn')?.addEventListener('click', closeMobileFilter);

        categorySelect?.addEventListener('change', () => {
            updateSubcategoryOptions(categorySelect.value);
            applyFilters();
        });

        subcategorySelect?.addEventListener('change', () => {
            applyFilters();
        });

        findProductsBtn?.addEventListener('click', () => {
            applyFilters();
            closeMobileFilter();
        });

        resetBtn?.addEventListener('click', () => {
            categorySelect.value = '';
            if (subcategorySelect) subcategorySelect.innerHTML = '<option value="">All Subcategories</option>';
            applyFilters();
            closeMobileFilter();
        });

        sortBySelect?.addEventListener('change', () => {
            sortAndReRender();
        });

        if (catalogSearchInput) {
            catalogSearchInput.addEventListener('input', debounce(() => applyFilters(catalogSearchInput.value.trim()), 300));
            catalogSearchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') applyFilters(catalogSearchInput.value.trim());
            });
        }

        catalogSearchBtn?.addEventListener('click', () => applyFilters(catalogSearchInput?.value.trim() || ''));

        window.addEventListener('scroll', () => {
            if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 800) {
                loadMoreProducts();
            }
        });
    }

    // --- Core Logic ---

    function applyFilters(searchQuery = '') {
        isLoading = true;
        const category = categorySelect?.value;
        const subcategory = subcategorySelect?.value;

        filteredProducts = allProducts.filter(p => {
            const matchCategory = !category || p.category === category;
            const matchSubcategory = !subcategory || p.subcategory === subcategory;

            let matchSearch = true;
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                matchSearch = p.name.toLowerCase().includes(q) ||
                    (p.description && p.description.toLowerCase().includes(q)) ||
                    (p.subcategory && p.subcategory.toLowerCase().includes(q)) ||
                    (p.id && p.id.toLowerCase().includes(q));
            }

            return matchCategory && matchSubcategory && matchSearch;
        });

        sortAndReRender();
        updateActiveFilterChips();
        isLoading = false;
    }

    function sortAndReRender() {
        const sort = sortBySelect?.value || '';
        if (sort === 'price-asc') {
            filteredProducts.sort((a, b) => parsePrice(a.price) - parsePrice(b.price));
        } else if (sort === 'price-desc') {
            filteredProducts.sort((a, b) => parsePrice(b.price) - parsePrice(a.price));
        } else if (sort === 'rating-desc') {
            filteredProducts.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        } else if (sort === 'name-asc') {
            filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
        }

        renderBatch(false);
    }

    function renderBatch(append = false) {
        if (!productGrid) return;

        if (!append) {
            productGrid.innerHTML = '';
            displayedCount = 0;
            updateResultCount(filteredProducts.length);
        }

        if (filteredProducts.length === 0) {
            showNoResults();
            return;
        }

        const nextBatch = filteredProducts.slice(displayedCount, displayedCount + ITEMS_PER_PAGE);
        const fragment = document.createDocumentFragment();

        nextBatch.forEach((product, index) => {
            const card = createProductCard(product, displayedCount + index);
            fragment.appendChild(card);
        });

        productGrid.appendChild(fragment);
        displayedCount += nextBatch.length;
    }

    function loadMoreProducts() {
        if (displayedCount < filteredProducts.length) {
            renderBatch(true);
        }
    }

    function createProductCard(product, globalIndex) {
        const stars = Math.round(product.rating || 4.5);
        const starsHtml = '★'.repeat(stars) + '☆'.repeat(5 - stars);
        const reviewCount = 20 + (globalIndex % 150);

        const card = document.createElement('div');
        card.className = 'product-card';
        card.style.animationDelay = `${(globalIndex % ITEMS_PER_PAGE) * 30}ms`;

        card.innerHTML = `
            <div class="product-image-wrapper">
                <span class="product-stock-badge">In Stock</span>
                <img src="${product.image}" alt="${product.name}" class="product-image" loading="lazy" onerror="this.src='assets/images/hero/hero-1.webp'">
                <div class="product-actions">
                    <a href="product-details.html?id=${product.id}" class="action-btn btn-view">
                        <i class="fas fa-eye"></i> View
                    </a>
                    <button class="action-btn btn-cart add-to-cart-btn" data-id="${product.id}">
                        <i class="fas fa-shopping-cart"></i> +Cart
                    </button>
                </div>
            </div>
            <div class="product-details">
                <span class="product-category">${product.category} | ${product.subcategory || ''}</span>
                <h3 class="product-title">${product.name}</h3>
                <div class="product-rating-row">
                    <span class="product-stars">${starsHtml}</span>
                    <span class="product-review-count">(${reviewCount})</span>
                </div>
                <div class="product-price-row">
                    <span class="product-price">${product.price}</span>
                    <button class="product-wishlist-btn" data-id="${product.id}" title="Add to Wishlist">
                        <i class="far fa-heart"></i>
                    </button>
                </div>
            </div>
        `;

        card.querySelector('.product-wishlist-btn').addEventListener('click', function (e) {
            e.stopPropagation();
            this.classList.toggle('active');
            const icon = this.querySelector('i');
            icon.className = this.classList.contains('active') ? 'fas fa-heart' : 'far fa-heart';
            if (this.classList.contains('active')) this.style.color = '#e74c3c';
            else this.style.color = '';
        });

        return card;
    }

    // --- Helpers ---

    function updateResultCount(count) {
        if (!resultsCountEl) return;
        const cat = categorySelect?.value;
        const sub = subcategorySelect?.value;
        let label = cat ? `in <strong>${cat}</strong>` : '';
        if (sub) label += ` > <strong>${sub}</strong>`;

        resultsCountEl.innerHTML = count === 0
            ? 'No products found'
            : `Showing <strong>${count}</strong> product${count !== 1 ? 's' : ''} ${label}`;
    }

    function showNoResults() {
        productGrid.innerHTML = `
            <div class="no-results-state" style="grid-column: 1/-1; text-align: center; padding: 80px 20px;">
                <div style="font-size: 3.5rem; margin-bottom: 16px;">🔍</div>
                <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">No Products Found</h3>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">Try adjusting your filters or search terms.</p>
                <a href="catalog.html" style="display: inline-block; background: var(--accent-primary); color: white; padding: 12px 28px; border-radius: 8px; font-weight: 700; text-decoration: none;">Browse All Products</a>
            </div>
        `;
    }

    function updateActiveFilterChips() {
        const activeFiltersEl = document.getElementById('activeFilters');
        const chipsEl = document.getElementById('activeFilterChips');
        if (!chipsEl) return;

        chipsEl.innerHTML = '';
        const category = categorySelect?.value;
        const subcategory = subcategorySelect?.value;

        if (category) {
            const chip = document.createElement('span');
            chip.className = 'filter-chip';
            chip.innerHTML = `${category} <button class="chip-remove">✕</button>`;
            chip.querySelector('.chip-remove').addEventListener('click', () => {
                categorySelect.value = '';
                updateSubcategoryOptions('');
                applyFilters();
            });
            chipsEl.appendChild(chip);
        }

        if (subcategory) {
            const chip = document.createElement('span');
            chip.className = 'filter-chip';
            chip.innerHTML = `${subcategory} <button class="chip-remove">✕</button>`;
            chip.querySelector('.chip-remove').addEventListener('click', () => {
                subcategorySelect.value = '';
                applyFilters();
            });
            chipsEl.appendChild(chip);
        }

        if (activeFiltersEl) activeFiltersEl.style.display = (category || subcategory) ? 'flex' : 'none';
    }

    function getCategoryFromSlug(slug) {
        const map = {
            'paints': 'PAINTS', 'paints-coatings': 'PAINTS',
            'electricals': 'ELECTRICALS', 'electrical-supplies': 'ELECTRICALS',
            'plumbing': 'PIPES', 'plumbing-fixtures': 'PIPES',
            'hardware-fasteners': 'HARDWARE & FASTENERS', 'hardware%26fasteners': 'HARDWARE & FASTENERS',
            'iron-sheets': 'IRON SHEETS', 'building-materials': 'BUILDING MATERIALS',
            'tools': 'TOOLS', 'nails': 'NAILS', 'padlocks': 'PADLOCKS'
        };
        return map[slug.toLowerCase()] || slug;
    }

    function toggleMobileFilter() {
        catalogSidebar?.classList.add('active');
        filterBackdrop?.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMobileFilter() {
        catalogSidebar?.classList.remove('active');
        filterBackdrop?.classList.remove('active');
        document.body.style.overflow = '';
    }

    function updateBreadcrumb(name) {
        const breadcrumb = document.getElementById('catalogBreadcrumb');
        if (breadcrumb) breadcrumb.textContent = name;
    }

    function initCategoryDropdown() {
        if (!categorySelect) return;
        const categories = [...new Set(allProducts.map(p => p.category))].sort();

        categorySelect.innerHTML = '<option value="">All Categories</option>';
        categories.forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = cat;
            categorySelect.appendChild(opt);
        });
    }

    function updateSubcategoryOptions(category) {
        if (!subcategorySelect) return;
        subcategorySelect.innerHTML = '<option value="">All Subcategories</option>';

        if (!category) return;

        const subcategories = [...new Set(
            allProducts
                .filter(p => p.category === category && p.subcategory)
                .map(p => p.subcategory)
        )].sort();

        subcategories.forEach(sub => {
            const opt = document.createElement('option');
            opt.value = sub;
            opt.textContent = sub;
            subcategorySelect.appendChild(opt);
        });
    }

    function parsePrice(priceStr) {
        if (!priceStr || typeof priceStr !== 'string') return 0;
        return parseFloat(priceStr.replace(/[^0-9.]/g, '')) || 0;
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    init();
});
