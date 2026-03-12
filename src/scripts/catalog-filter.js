/**
 * Catalog Filter Logic - Renovyte V2
 * Dynamically renders products from RenovyteProducts database
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const makeSelect = document.getElementById('filterMake');
    const modelSelect = document.getElementById('filterModel');
    const yearSelect = document.getElementById('filterYear');
    const engineSelect = document.getElementById('filterEngine');
    const categorySelect = document.getElementById('filterCategory');
    const findPartsBtn = document.getElementById('findPartsBtn');
    const resetBtn = document.getElementById('resetFiltersBtn');
    const productGrid = document.getElementById('productGrid');
    // Mobile Filter Logic
    const catalogFilterBtn = document.getElementById('catalogFilterBtn');
    const catalogSidebar = document.querySelector('.catalog-sidebar');
    const filterBackdrop = document.getElementById('filterBackdrop');

    catalogFilterBtn?.addEventListener('click', () => {
        catalogSidebar?.classList.add('active');
        filterBackdrop?.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scroll
    });

    const closeFilterDrawer = () => {
        catalogSidebar?.classList.remove('active');
        filterBackdrop?.classList.remove('active');
        document.body.style.overflow = '';
    };

    filterBackdrop?.addEventListener('click', closeFilterDrawer);
    document.getElementById('closeFiltersBtn')?.addEventListener('click', closeFilterDrawer);

    // Close on action buttons for mobile
    findPartsBtn?.addEventListener('click', () => {
        if (window.innerWidth <= 992) closeFilterDrawer();
    });
    resetBtn?.addEventListener('click', () => {
        if (window.innerWidth <= 992) closeFilterDrawer();
    });

    // Hardware Categories Configuration
    const hardwareCategories = [
        'Paints',
        'Electricals',
        'Plumbing',
        'Hardware & Fasteners',
        'Iron Sheets',
        'Building Materials'
    ];

    // Data Normalization Utility
    const normalizeValue = (type, val) => {
        if (!val || val === 'Universal') return val;
        let s = val.toString().trim();

        if (type === 'make') {
            s = s.toUpperCase();
            // Backward compatibility for common typos
            if (s === 'DODGER') return 'DODGE';
            if (s === 'INFINITY') return 'INFINITI';
            if (s === 'LANDROVER') return 'LAND ROVER';
            return s;
        }

        if (type === 'engine') {
            s = s.toLowerCase();
            // 1.8L -> 1800cc
            if (s.includes('l')) {
                const num = parseFloat(s);
                if (!isNaN(num)) return (num * 1000) + 'cc';
            }
            // 3.2 -> 3200cc
            if (!s.includes('cc')) {
                const num = parseFloat(s);
                if (!isNaN(num)) {
                    if (num < 10) return (num * 1000) + 'cc';
                    return num + 'cc';
                }
            }
            return s.split(' ')[0]; // Handle "2500cc Diesel" -> "2500cc"
        }
        return s;
    };

    // Slug to Category Name mapping — covers all URL forms used across the site
    const categoryMap = {
        'paints': 'Paints',
        'paints-coatings': 'Paints',
        'electricals': 'Electricals',
        'electrical-supplies': 'Electricals',
        'plumbing': 'Plumbing',
        'plumbing-fixtures': 'Plumbing',
        'hardware%26fasteners': 'Hardware & Fasteners',
        'hardware-fasteners': 'Hardware & Fasteners',
        'iron-sheets': 'Iron Sheets',
        'building-materials': 'Building Materials'
    };

    // Check URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    let categoryParam = urlParams.get('category');
    const searchParam = urlParams.get('search');
    const subcategoryParam = urlParams.get('item');

    // Parse and apply URL category BEFORE initial render (prevent all-products flash)
    if (categoryParam) {
        const mappedName = categoryMap[categoryParam.toLowerCase()] || categoryParam;
        categoryParam = mappedName;
        categorySelect.value = mappedName;
        // Update breadcrumb to show selected category
        const breadcrumb = document.getElementById('catalogBreadcrumb');
        if (breadcrumb) breadcrumb.textContent = mappedName;
    }

    const resultsCountEl = document.getElementById('resultsCount');
    const sortBySelect = document.getElementById('sortBy');

    // Parse other vehicle URL parameters
    const makeParam = urlParams.get('make');
    const modelParam = urlParams.get('model');
    const yearParam = urlParams.get('year');
    const engineParam = urlParams.get('engine');

    // Sort-by listener
    sortBySelect?.addEventListener('change', () => applyFilters(searchParam, subcategoryParam));

    initCategoryDropdown();

    // Disable legacy vehicle filters if they exist in DOM
    if (makeSelect) makeSelect.disabled = true;
    if (modelSelect) modelSelect.disabled = true;
    if (yearSelect) yearSelect.disabled = true;
    if (engineSelect) engineSelect.disabled = true;

    applyFilters(searchParam, subcategoryParam);

    // Live search wiring — catalog search input
    const catalogSearchInput = document.querySelector('.search-part-input');
    const catalogSearchBtn = document.querySelector('.search-btn-v3');

    if (catalogSearchInput) {
        catalogSearchInput.addEventListener('input', () => {
            applyFilters(catalogSearchInput.value.trim());
        });
        catalogSearchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') applyFilters(catalogSearchInput.value.trim());
        });
    }
    if (catalogSearchBtn) {
        catalogSearchBtn.addEventListener('click', () => {
            applyFilters(catalogSearchInput?.value.trim() || '');
        });
    }


    // --- Core Functions ---

    function sortProducts(products) {
        const sort = sortBySelect?.value || '';
        const cloned = [...products];
        if (sort === 'price-asc') {
            cloned.sort((a, b) => parsePrice(a.price) - parsePrice(b.price));
        } else if (sort === 'price-desc') {
            cloned.sort((a, b) => parsePrice(b.price) - parsePrice(a.price));
        } else if (sort === 'rating-desc') {
            cloned.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        } else if (sort === 'name-asc') {
            cloned.sort((a, b) => a.name.localeCompare(b.name));
        }
        return cloned;
    }

    function parsePrice(priceStr) {
        if (!priceStr) return 0;
        return parseFloat(priceStr.replace(/[^0-9.]/g, '')) || 0;
    }

    function renderProducts(products) {
        if (!productGrid) return;

        // Update result count
        if (resultsCountEl) {
            const cat = categorySelect?.value;
            const label = cat ? `in <strong>${cat}</strong>` : '';
            resultsCountEl.innerHTML = products.length === 0
                ? 'No products found'
                : `Showing <strong>${products.length}</strong> product${products.length !== 1 ? 's' : ''} ${label}`;
        }

        productGrid.innerHTML = '';

        if (products.length === 0) {
            productGrid.innerHTML = `
                <div class="no-results-state" style="grid-column: 1/-1; text-align: center; padding: 80px 20px;">
                    <div style="font-size: 3.5rem; margin-bottom: 16px;">🔍</div>
                    <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">No Parts Found</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 24px;">Try adjusting your filters or search terms.</p>
                    <a href="catalog.html" style="display: inline-block; background: var(--accent-primary); color: white; padding: 12px 28px; border-radius: 8px; font-weight: 700; text-decoration: none;">Browse All Products</a>
                </div>
            `;
            return;
        }

        const sorted = sortProducts(products);

        sorted.forEach((product, index) => {
            const stars = Math.round(product.rating || 4.5);
            const starsHtml = '★'.repeat(stars) + '☆'.repeat(5 - stars);
            const reviewCount = Math.floor(Math.random() * 180 + 20);
            const card = document.createElement('div');
            card.className = 'product-card';
            card.style.animationDelay = `${index * 40}ms`;
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
                    <span class="product-category">${product.category}</span>
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
            productGrid.appendChild(card);
        });

        // Wishlist toggle
        productGrid.querySelectorAll('.product-wishlist-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const icon = btn.querySelector('i');
                const isWished = icon.classList.contains('fa-solid', 'fa-heart') || btn.classList.contains('active');
                if (isWished) {
                    icon.className = 'far fa-heart';
                    btn.classList.remove('active');
                } else {
                    icon.className = 'fas fa-heart';
                    btn.classList.add('active');
                    btn.style.color = '#e74c3c';
                }
            });
        });
    }

    function applyFilters(searchQuery = '', subcatOverride = null) {
        const actualSearchQuery = (typeof searchQuery === 'string') ? searchQuery : '';

        const filters = {
            category: categorySelect.value,
            make: makeSelect.value,
            model: modelSelect.value,
            year: yearSelect.value,
            engine: engineSelect.value
        };

        const vehicleFiltersActive = filters.make || filters.model || filters.year || filters.engine;

        // Render active filter chips
        const activeFiltersEl = document.getElementById('activeFilters');
        const chipsEl = document.getElementById('activeFilterChips');
        if (chipsEl) {
            chipsEl.innerHTML = '';
            const activeList = [];
            if (filters.category) activeList.push({ label: filters.category, clear: () => { categorySelect.value = ''; applyFilters(); } });
            if (filters.make) activeList.push({ label: `Make: ${filters.make}`, clear: () => { makeSelect.value = ''; applyFilters(); } });
            if (filters.model) activeList.push({ label: `Model: ${filters.model}`, clear: () => { modelSelect.value = ''; applyFilters(); } });
            if (filters.year) activeList.push({ label: `Year: ${filters.year}`, clear: () => { yearSelect.value = ''; applyFilters(); } });
            if (filters.engine) activeList.push({ label: `Engine: ${filters.engine}`, clear: () => { engineSelect.value = ''; applyFilters(); } });

            if (activeFiltersEl) activeFiltersEl.style.display = activeList.length ? 'flex' : 'none';

            activeList.forEach(item => {
                const chip = document.createElement('span');
                chip.className = 'filter-chip';
                chip.innerHTML = `${item.label} <button class="chip-remove">✕</button>`;
                chip.querySelector('.chip-remove').addEventListener('click', item.clear);
                chipsEl.appendChild(chip);
            });
        }

        // Clear all handler
        document.getElementById('clearAllFilters')?.addEventListener('click', () => {
            categorySelect.value = ''; makeSelect.value = '';
            modelSelect.value = ''; yearSelect.value = ''; engineSelect.value = '';
            renderProducts(window.RenovyteProducts || []);
            if (activeFiltersEl) activeFiltersEl.style.display = 'none';
        });

        const activeSubcat = subcatOverride || subcategoryParam;
        const allProducts = window.RenovyteProducts || [];

        // --- PHASE 1: Strict filters (category, search, subcategory) ---
        const strictFiltered = allProducts.filter(p => {
            const matchCategory = !filters.category || p.category === filters.category;

            let matchSearch = true;
            if (actualSearchQuery) {
                const q = actualSearchQuery.toLowerCase();
                matchSearch = p.name.toLowerCase().includes(q) ||
                    (p.description && p.description.toLowerCase().includes(q)) ||
                    (p.subcategory && p.subcategory.toLowerCase().includes(q)) ||
                    (p.id && p.id.toLowerCase().includes(q));
            }

            let matchSubcategory = true;
            if (activeSubcat) {
                const subQ = activeSubcat.toLowerCase().replace(/-/g, ' ');
                matchSubcategory = p.subcategory && p.subcategory.toLowerCase().includes(subQ);
            }

            return matchCategory && matchSearch && matchSubcategory;
        });

        // --- PHASE 2: Disabled vehicle filters ---
        // The requirement is to show all products within the category regardless of Make/Model/Year/Engine choices.
        let finalResults = strictFiltered;

        // --- Compatibility notice banner disabled ---

        renderProducts(finalResults);
    }

    /**
     * Show/hide compatibility notice banner.
     * (Disabled - clears existing banner if present)
     */
    function showCompatibilityBanner(vehicleFiltersActive, isFallback) {
        let banner = document.getElementById('compatibilityBanner');
        if (banner) banner.remove();
    }

    // --- Dropdown Management ---

    function initCategoryDropdown() {
        if (!categorySelect) return;
        // Keep initial option if exists
        const currentOptions = Array.from(categorySelect.options).map(o => o.value);
        hardwareCategories.forEach(cat => {
            if (!currentOptions.includes(cat)) {
                const opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                categorySelect.appendChild(opt);
            }
        });
    }

    // Legacy listeners disabled

    findPartsBtn?.addEventListener('click', () => {
        applyFilters();
        closeFilterDrawer();
    });

    resetBtn?.addEventListener('click', () => {
        categorySelect.value = '';
        makeSelect.value = '';
        resetSelect(modelSelect, 'Select Model');
        if (yearSelect) yearSelect.value = '';
        if (engineSelect) engineSelect.value = '';
        modelSelect.disabled = true;
        if (yearSelect) yearSelect.disabled = true;
        if (engineSelect) engineSelect.disabled = true;
        renderProducts(window.RenovyteProducts || []);
        closeFilterDrawer();
    });

    // Helper functions
    function populateDropdown(select, items) {
        items.forEach(item => {
            const opt = document.createElement('option');
            opt.value = item;
            opt.textContent = item;
            select.appendChild(opt);
        });
    }

    function resetSelect(select, text) {
        select.innerHTML = `<option value="">${text}</option>`;
    }
});
