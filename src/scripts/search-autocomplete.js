/**
 * Search Autocomplete Logic
 * Provides real-time suggestions for the search inputs.
 */

document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = document.querySelectorAll('.search-input-v2, .search-part-input');

    // Create autocomplete container if it doesn't exist (for header)
    // The header already has a form. We'll append the results container to the form or wrapper.

    searchInputs.forEach(input => {
        // Wrapper for positioning
        const wrapper = input.parentElement; // Usually the form
        if (!wrapper.style.position) wrapper.style.position = 'relative';

        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'search-autocomplete-results';
        resultsContainer.style.display = 'none';
        wrapper.appendChild(resultsContainer);

        input.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();

            if (query.length < 2) {
                resultsContainer.style.display = 'none';
                return;
            }

            if (!window.RenovyteProducts) return;

            const matches = window.RenovyteProducts.filter(p =>
                p.name.toLowerCase().includes(query) ||
                p.subcategory?.toLowerCase().includes(query) ||
                p.category.toLowerCase().includes(query)
            ).slice(0, 5); // Limit to 5 results

            if (matches.length > 0) {
                renderResults(matches, resultsContainer);
            } else {
                resultsContainer.style.display = 'none';
            }
        });

        // Hide on click outside
        document.addEventListener('click', (e) => {
            if (!wrapper.contains(e.target)) {
                resultsContainer.style.display = 'none';
            }
        });
    });

    function renderResults(products, container) {
        container.innerHTML = `
            <ul class="autocomplete-list">
                ${products.map(p => `
                    <li>
                        <a href="product-details.html?id=${p.id}" class="autocomplete-item">
                            <img src="${p.image}" alt="${p.name}" class="autocomplete-thumb" onerror="this.src='assets/images/hero/hero-1.webp'">
                            <div class="autocomplete-info">
                                <span class="autocomplete-title">${p.name}</span>
                                <span class="autocomplete-meta">${p.subcategory || p.category}</span>
                            </div>
                            <span class="autocomplete-price">${p.price}</span>
                        </a>
                    </li>
                `).join('')}
                <li class="autocomplete-footer">
                    <button type="submit" class="view-all-results">View all results</button>
                </li>
            </ul>
        `;

        // Add premium styles dynamically if not present
        if (!document.getElementById('autocomplete-styles')) {
            const style = document.createElement('style');
            style.id = 'autocomplete-styles';
            style.textContent = `
                .search-autocomplete-results {
                    position: absolute;
                    top: calc(100% + 10px);
                    left: 20px;
                    right: 20px;
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(25px) saturate(180%);
                    -webkit-backdrop-filter: blur(25px) saturate(180%);
                    border: 1px solid rgba(0, 0, 0, 0.08); /* Sophisticated border */
                    border-radius: 24px;
                    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
                    z-index: 1000;
                    overflow: hidden;
                    animation: premiumSlideDown 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
                    transform-origin: top center;
                }
                
                @keyframes premiumSlideDown {
                    from { opacity: 0; transform: translateY(-10px) scale(0.98); }
                    to { opacity: 1; transform: translateY(0) scale(1); }
                }

                .autocomplete-list {
                    list-style: none;
                    margin: 0;
                    padding: 8px;
                }

                .autocomplete-item {
                    display: flex;
                    align-items: center;
                    padding: 14px 18px;
                    text-decoration: none;
                    color: #1c1c1e;
                    border-radius: 16px;
                    margin-bottom: 4px;
                    transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
                }

                .autocomplete-item:last-child {
                    margin-bottom: 0;
                }

                .autocomplete-item:hover {
                    background: rgba(184, 134, 11, 0.08);
                    transform: translateX(5px);
                }

                .autocomplete-thumb {
                    width: 52px;
                    height: 52px;
                    object-fit: contain;
                    border-radius: 12px;
                    background: #f8f8fa;
                    margin-right: 16px;
                    padding: 6px;
                    border: 1px solid rgba(0,0,0,0.03);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
                }

                .autocomplete-info {
                    flex: 1;
                    min-width: 0;
                }

                .autocomplete-title {
                    display: block;
                    font-size: 0.95rem;
                    font-weight: 700;
                    margin-bottom: 2px;
                    color: #1c1c1e;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }

                .autocomplete-meta {
                    display: block;
                    font-size: 0.75rem;
                    font-weight: 600;
                    color: #8e8e93;
                    letter-spacing: 0.3px;
                }

                .autocomplete-price {
                    font-size: 0.9rem;
                    color: var(--accent-primary, #B8860B);
                    font-weight: 800;
                    margin-left: 15px;
                    font-family: 'Outfit', sans-serif;
                }

                .autocomplete-footer {
                    padding: 10px;
                    text-align: center;
                    border-top: 1px solid rgba(0,0,0,0.04);
                }

                .view-all-results {
                    width: 100%;
                    background: rgba(0,0,0,0.02);
                    border: none;
                    color: var(--accent-primary, #B8860B);
                    padding: 12px;
                    cursor: pointer;
                    font-size: 0.85rem;
                    font-weight: 800;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    border-radius: 12px;
                    transition: all 0.2s;
                }

                .view-all-results:hover {
                    background: var(--accent-primary);
                    color: white;
                    box-shadow: 0 8px 16px rgba(184, 134, 11, 0.2);
                }

                /* Shimmer Loading Animation */
                .shimmer {
                    background: linear-gradient(90deg, #f0f0f0 25%, #f7f7f7 50%, #f0f0f0 75%);
                    background-size: 200% 100%;
                    animation: shimmer 1.5s infinite;
                }
                
                @keyframes shimmer {
                    0% { background-position: 200% 0; }
                    100% { background-position: -200% 0; }
                }

                /* Container Adjustment for Catalog Page */
                .search-part-number .search-autocomplete-results {
                    left: 0;
                    right: 0;
                    border-radius: 0 0 24px 24px;
                    margin-top: -30px; /* Pull up to touch the pill */
                    padding-top: 30px;
                    z-index: 90;
                    background: rgba(255, 255, 255, 0.9);
                }
            `;
            document.head.appendChild(style);
        }

        container.style.display = 'block';
    }
});
