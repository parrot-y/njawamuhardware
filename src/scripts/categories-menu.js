/**
 * NJAWAMU Hardware — Category Sidebar
 * A premium slide-in sidebar with hardware categories.
 */

class CategorySidebar {
    constructor() {
        this.isOpen = false;
        this.activeCategory = null;

        this.categoryData = {
            PAINTS: {
                title: 'Paints & Finishes', icon: 'fa-paint-roller', color: '#e67e22',
                items: ['Gloss Paints', 'Emulsion Paints', 'Undercoats', 'Primers', 'Thinners']
            },
            ELECTRICALS: {
                title: 'Electrical Supplies', icon: 'fa-plug', color: '#f1c40f',
                items: ['Cables & Wires', 'Switches & Sockets', 'Lighting Fixtures', 'Conduits', 'Circuit Breakers']
            },
            NAILS: {
                title: 'Nails & Fasteners', icon: 'fa-hammer', color: '#7f8c8d',
                items: ['Wire Nails', 'Roofing Nails', 'Screws', 'Bolts & Nuts', 'Washers']
            },
            FITTINGS: {
                title: 'Plumbing & Fittings', icon: 'fa-faucet', color: '#3498db',
                items: ['PPR Pipes & Fittings', 'PVC Pipes', 'GI Fittings', 'Gate Valves', 'Water Tanks']
            },
            TOOLS: {
                title: 'Tools & Equipment', icon: 'fa-wrench', color: '#2ecc71',
                items: ['Hand Tools', 'Power Tools', 'Measuring Tools', 'Safety Gear']
            },
            CEMENT: {
                title: 'Building Materials', icon: 'fa-trowel-bricks', color: '#95a5a6',
                items: ['Cement', 'Sand', 'Ballast', 'Bricks & Blocks']
            }
        };

        this._buildDOM();
        this._bindTriggers();
    }

    _buildDOM() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'csb-overlay';
        this.panel = document.createElement('aside');
        this.panel.className = 'csb-panel';
        this.panel.innerHTML = this._template();

        document.body.appendChild(this.overlay);
        document.body.appendChild(this.panel);

        this.panel.querySelector('.csb-close').addEventListener('click', () => this.close());
        this.overlay.addEventListener('click', () => this.close());

        this.panel.querySelectorAll('.csb-cat-item').forEach(item => {
            item.addEventListener('click', () => {
                this._toggleAccordion(item.dataset.key);
            });
        });
    }

    _template() {
        return `
        <div class="csb-header">
            <div class="csb-header-logo">
                <img src="assets/images/logo.png" alt="NJAWAMU Hardware">
                <div class="csb-brand-text">
                    <span class="csb-brand-name">NJAWAMU</span>
                    <span class="csb-brand-sub">Hardware</span>
                </div>
            </div>
            <button class="csb-close"><i class="fas fa-times"></i></button>
        </div>

        <nav class="csb-body">
            <p class="csb-section-label">HARDWARE CATEGORIES</p>
            <ul class="csb-cat-list">
                ${Object.entries(this.categoryData).map(([key, cat]) => `
                <li class="csb-cat-item" data-key="${key}">
                    <div class="csb-cat-row">
                        <span class="csb-cat-icon-wrap" style="background:${cat.color}22;color:${cat.color}">
                            <i class="fas ${cat.icon}"></i>
                        </span>
                        <span class="csb-cat-label">${cat.title}</span>
                        <i class="fas fa-chevron-right csb-chevron"></i>
                    </div>
                    <ul class="csb-sub-list" data-key="${key}">
                        <li class="csb-sub-header">
                            <a href="catalog.html?category=${key}" class="csb-view-all">View All</a>
                        </li>
                        ${cat.items.map(item => `<li class="csb-sub-item"><a href="catalog.html?category=${key}&q=${encodeURIComponent(item)}" class="csb-sub-link">${item}</a></li>`).join('')}
                    </ul>
                </li>`).join('')}
            </ul>
        </nav>

        <div class="csb-footer">
            <a href="tel:+254726822382" class="csb-footer-link"><i class="fas fa-phone"></i> Call Order</a>
            <a href="https://wa.me/254726822382" class="csb-footer-link csb-whatsapp"><i class="fab fa-whatsapp"></i> WhatsApp</a>
        </div>`;
    }

    _toggleAccordion(key) {
        const item = this.panel.querySelector(`.csb-cat-item[data-key="${key}"]`);
        const subList = this.panel.querySelector(`.csb-sub-list[data-key="${key}"]`);
        const isActive = item.classList.contains('active');

        this.panel.querySelectorAll('.csb-cat-item.active').forEach(el => el.classList.remove('active'));
        this.panel.querySelectorAll('.csb-sub-list.open').forEach(el => {
            el.classList.remove('open');
            el.style.maxHeight = '0';
        });

        if (!isActive) {
            item.classList.add('active');
            subList.classList.add('open');
            subList.style.maxHeight = subList.scrollHeight + 'px';
        }
    }

    open() {
        this.isOpen = true;
        this.panel.classList.add('open');
        this.overlay.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }

    close() {
        this.isOpen = false;
        this.panel.classList.remove('open');
        this.overlay.classList.remove('visible');
        document.body.style.overflow = '';
    }

    toggle() { this.isOpen ? this.close() : this.open(); }

    _bindTriggers() {
        document.getElementById('nav-hamburger')?.addEventListener('click', () => this.toggle());
        document.getElementById('categoriesBtn')?.addEventListener('click', () => this.toggle());
        // For mobile menu button in top bar
        document.querySelector('.mobile-hamburger')?.addEventListener('click', () => this.toggle());
    }
}

window.addEventListener('DOMContentLoaded', () => {
    window.categorySidebar = new CategorySidebar();
});
