/**
 * Catalog Filter Logic - NJAWAMU Hardware
 * Dynamically renders hardware products from RenovyteProducts database
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
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
        document.body.style.overflow = 'hidden';
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

    // Check URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    let categoryParam = urlParams.get('category');
    const searchParam = urlParams.get('search');

    const resultsCountEl = document.getElementById('resultsCount');
    const sortBySelect = document.getElementById('sortBy');

    // Sort-by listener
    sortBySelect?.addEventListener('change', () => applyFilters(catalogSearchInput?.value.trim() || ''));

    // Initialize Category Dropdown from Data
    function initCategoryDropdown() {
        if (!categorySelect) return;
        const allProducts = window.RenovyteProducts || [];
        const categories = [...new Set(allProducts.map(p => p.category))].sort();

        // Clear current options except the first one
        categorySelect.innerHTML = '<option value="">All Categories</option>';
        categories.forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = cat;
            categorySelect.appendChild(opt);
        });

        // Re-apply parameter if it matches
        if (categoryParam) {
            const matched = categories.find(c => c.toLowerCase() === categoryParam.toLowerCase().replace(/-/g, ' '));
            if (matched) categorySelect.value = matched;
        }
    }

    initCategoryDropdown();
    applyFilters(searchParam || '');

    // Live search wiring
    const catalogSearchInput = document.querySelector('.search-part-input');
    const catalogSearchBtn = document.querySelector('.search-btn-v3');

    if (catalogSearchInput) {
        if (searchParam) catalogSearchInput.value = searchParam;
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
        if (!priceStr || priceStr === "Contact for Price") return 0;
        return parseFloat(priceStr.replace(/[^0-9.]/g, '')) || 0;
    }

    function renderProducts(products) {
        if (!productGrid) return;

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
                    <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">No Hardware Found</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 24px;">Try adjusting your filters or search terms.</p>
                    <a href="catalog.html" style="display: inline-block; background: var(--accent-primary); color: white; padding: 12px 28px; border-radius: 8px; font-weight: 700; text-decoration: none;">Browse All Products</a>
                </div>
            `;
            return;
        }

        const sorted = sortProducts(products);
        const displayLimit = 150;
        const toDisplay = sorted.slice(0, displayLimit);

        toDisplay.forEach((product, index) => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.style.animationDelay = `${index * 10}ms`;
            card.innerHTML = `
                <div class="product-image-wrapper">
                    <span class="product-stock-badge">In Stock</span>
                    <img src="${product.image}" alt="${product.name}" class="product-image" loading="lazy" onerror="this.src='assets/images/featured/placeholder.png'">
                    <div class="product-actions">
                        <a href="https://wa.me/254726822382?text=I%20am%20interested%20in%20${encodeURIComponent(product.name)}%20(SKU:%20${product.sku})" target="_blank" class="action-btn btn-cart">
                            <i class="fab fa-whatsapp"></i> Inquire
                        </a>
                    </div>
                </div>
                <div class="product-details">
                    <span class="product-category">${product.category}</span>
                    <h3 class="product-title">${product.name}</h3>
                    <div class="product-sku" style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 8px;">SKU: ${product.sku}</div>
                    <div class="product-price-row">
                        <span class="product-price">${product.price}</span>
                    </div>
                </div>
            `;
            productGrid.appendChild(card);
        });

        if (products.length > displayLimit) {
            const moreEl = document.createElement('div');
            moreEl.style.gridColumn = '1/-1';
            moreEl.style.textAlign = 'center';
            moreEl.style.padding = '20px';
            moreEl.style.color = 'var(--text-secondary)';
            moreEl.textContent = `... and ${products.length - displayLimit} more products matching your search.`;
            productGrid.appendChild(moreEl);
        }
    }

    function applyFilters(searchQuery = '') {
        const q = searchQuery.toLowerCase();
        const selectedCat = categorySelect.value;

        // Render chips
        const activeFiltersEl = document.getElementById('activeFilters');
        const chipsEl = document.getElementById('activeFilterChips');
        if (chipsEl) {
            chipsEl.innerHTML = '';
            const activeList = [];
            if (selectedCat) activeList.push({ label: selectedCat, clear: () => { categorySelect.value = ''; applyFilters(q); } });
            if (q) activeList.push({ label: `Search: ${q}`, clear: () => { if (catalogSearchInput) catalogSearchInput.value = ''; applyFilters(''); } });

            if (activeFiltersEl) activeFiltersEl.style.display = activeList.length ? 'flex' : 'none';

            activeList.forEach(item => {
                const chip = document.createElement('span');
                chip.className = 'filter-chip';
                chip.innerHTML = `${item.label} <button class="chip-remove">✕</button>`;
                chip.querySelector('.chip-remove').addEventListener('click', item.clear);
                chipsEl.appendChild(chip);
            });
        }

        const allProducts = window.RenovyteProducts || [];

        const filtered = allProducts.filter(p => {
            const matchCategory = !selectedCat || p.category === selectedCat;
            const matchSearch = !q ||
                p.name.toLowerCase().includes(q) ||
                p.sku.toLowerCase().includes(q) ||
                p.category.toLowerCase().includes(q);
            return matchCategory && matchSearch;
        });

        renderProducts(filtered);
    }

    findPartsBtn?.addEventListener('click', () => {
        applyFilters(catalogSearchInput?.value.trim() || '');
    });

    resetBtn?.addEventListener('click', () => {
        categorySelect.value = '';
        if (catalogSearchInput) catalogSearchInput.value = '';
        applyFilters('');
    });
});
