function initCartLogic() {
    if (window.cartInitialized) return;
    window.cartInitialized = true;

    // --- GLOBAL EXPORTS ---
    // Moved to top to ensure availability even if later setup fails
    window.addItemToCart = (item) => addItemToCart(item);
    window.toggleCartDrawer = () => toggleCartDrawer();
    window.updateCartBadges = () => updateCartBadges();
    window.updateCartDrawer = () => updateCartDrawer();

    // Defines standard local storage key
    const CART_KEY = 'kas_cart';

    // State
    let cart = [];
    try {
        const stored = localStorage.getItem(CART_KEY);
        cart = stored ? JSON.parse(stored) : [];
        if (!Array.isArray(cart)) cart = [];
        // Sanitize: remove any null/broken items
        cart = cart.filter(item => item && typeof item === 'object');
    } catch (e) {
        console.error("Cart data corrupted:", e);
        cart = [];
    }

    // --- INTERNAL HELPERS ---

    function saveCart() {
        try {
            localStorage.setItem(CART_KEY, JSON.stringify(cart));
        } catch (e) {
            console.error("Failed to save cart:", e);
        }
    }

    function updateCartBadges() {
        try {
            const count = cart.reduce((total, item) => total + (item.quantity || 0), 0);
            const badges = document.querySelectorAll('.cart-badge');
            badges.forEach(badge => {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'flex' : 'none';
                // Pop animation
                badge.style.transform = 'scale(1.5)';
                badge.style.background = '#27AE60';
                setTimeout(() => {
                    badge.style.transform = 'scale(1)';
                    badge.style.background = '';
                }, 400);
            });
        } catch (e) {
            console.error("Error updating cart badges:", e);
        }
    }

    function toggleCartDrawer() {
        const drawer = document.getElementById('cartDrawer');
        if (!drawer) return;
        drawer.classList.toggle('active');
        document.body.style.overflow = drawer.classList.contains('active') ? 'hidden' : '';
    }

    function addItemToCart(itemOrId) {
        let item = itemOrId;

        // If only an ID is passed, look up the product in global database
        if (typeof itemOrId === 'string' && window.RenovyteProducts) {
            const product = window.RenovyteProducts.find(p => p.id === itemOrId);
            if (product) {
                item = {
                    id: product.id,
                    title: product.name,
                    price: parseInt(product.price.replace(/[^0-9]/g, '')) || 0,
                    image: product.image,
                    quantity: 1
                };
            }
        }

        if (!item || !item.title) return;

        // Check if item exists
        const existing = cart.find(i => (i.id && i.id === item.id) || i.title === item.title);
        if (existing) {
            existing.quantity = (existing.quantity || 0) + (item.quantity || 1);
        } else {
            item.quantity = item.quantity || 1;
            item.price = item.price || 0;
            cart.push(item);
        }

        saveCart();
        updateCartBadges();
        updateCartDrawer();

        // Show Toast
        if (typeof showToast === 'function') {
            showToast(`Added to cart: ${item.title}`);
        } else {
            displayInternalToast(`Added to cart: ${item.title}`);
        }

        // Open drawer for immediate feedback
        setTimeout(() => {
            const drawer = document.getElementById('cartDrawer');
            if (drawer && !drawer.classList.contains('active')) {
                toggleCartDrawer();
            }
        }, 100);
    }

    function updateCartDrawer() {
        const list = document.querySelector('.cart-items-list');
        const totalEl = document.querySelector('.total-amount');
        if (!list || !totalEl) return;

        if (cart.length === 0) {
            list.innerHTML = '<div class="empty-cart-msg">Your basket is empty</div>';
            totalEl.innerText = 'KSh 0';
            return;
        }

        try {
            let total = 0;
            list.innerHTML = cart.map((item, index) => {
                const qty = item.quantity || 1;
                const price = item.price || 0;
                total += price * qty;
                const displayPrice = price === 0 ? "Contact for Price" : `KSh ${price.toLocaleString()}`;
                return `
                    <div class="cart-item">
                        <img src="${item.image}" alt="${item.title}" class="cart-item-img" onerror="this.src='assets/images/logo.png'">
                        <div class="cart-item-info">
                            <div class="cart-item-title">${item.title}</div>
                            <div class="cart-item-price">${qty} x ${displayPrice}</div>
                            <button class="cart-item-remove" data-index="${index}">Remove</button>
                        </div>
                    </div>
                `;
            }).join('');

            totalEl.innerText = total === 0 ? "Contact for Price" : `KSh ${total.toLocaleString()}`;

            // Re-bind remove buttons
            list.querySelectorAll('.cart-item-remove').forEach(btn => {
                btn.onclick = (e) => {
                    const index = e.target.getAttribute('data-index');
                    removeItem(index);
                };
            });
        } catch (e) {
            console.error("Error updating cart drawer content:", e);
            list.innerHTML = '<div class="empty-cart-msg">Error loading basket content</div>';
        }
    }

    function removeItem(index) {
        cart.splice(index, 1);
        saveCart();
        updateCartBadges();
        updateCartDrawer();
    }

    function openCheckoutModal() {
        if (cart.length === 0) {
            if (typeof showToast === 'function') showToast('Your basket is empty');
            return;
        }
        const modal = document.getElementById('checkoutModal');
        if (modal) {
            modal.classList.add('active');
            const drawer = document.getElementById('cartDrawer');
            if (drawer && drawer.classList.contains('active')) toggleCartDrawer();
        }
    }

    function closeCheckoutModal() {
        const modal = document.getElementById('checkoutModal');
        if (modal) modal.classList.remove('active');
    }

    function finalizeCheckout() {
        const name = document.getElementById('customerName')?.value.trim();
        const location = document.getElementById('customerLocation')?.value.trim();

        if (!name || !location) {
            alert('Please fill in all details');
            return;
        }

        let total = 0;
        let itemsList = "";

        cart.forEach((item, i) => {
            const itemTotal = (item.price || 0) * (item.quantity || 1);
            total += itemTotal;
            itemsList += `${i + 1}. *${item.title || 'Unknown'}*\n`;
            itemsList += `   Qty: ${item.quantity || 1} | Total: KES ${itemTotal.toLocaleString()}\n\n`;
        });

        const invoiceId = `INV-${Math.floor(Math.random() * 9000) + 1000}`;
        const date = new Date().toLocaleDateString('en-GB');

        let message = `🚀 *NEW ORDER: ${invoiceId}*\n`;
        message += `📅 *Date:* ${date}\n`;
        message += `--------------------------------\n`;
        message += `👤 *Customer:* ${name}\n`;
        message += `📍 *Delivery:* ${location}\n`;
        message += `--------------------------------\n\n`;
        message += `*ORDERED ITEMS:*\n${itemsList}`;
        message += `--------------------------------\n`;
        message += `💰 *GRAND TOTAL: KES ${total.toLocaleString()}*\n`;
        message += `--------------------------------\n\n`;
        message += `⚠️ *Kindly confirm compatibility for this vehicle.*\n\n`;
        message += `_Please acknowledge this order to proceed with delivery. Thank you for shopping with NJAWAMU Hardware!_`;

        if (window.BusinessConfig) {
            window.BusinessConfig.openWhatsApp(message);
        } else {
            console.log("WhatsApp Message:", message);
            const waUrl = `https://wa.me/254723699157?text=${encodeURIComponent(message)}`;
            window.open(waUrl, '_blank');
        }
        closeCheckoutModal();
    }

    function createCartDrawer() {
        if (document.getElementById('cartDrawer')) return;

        // Inject Styles if not already present
        if (!document.getElementById('cartStyles')) {
            const style = document.createElement('style');
            style.id = 'cartStyles';
            style.textContent = `
                .cart-drawer { position: fixed; top: 0; right: 0; width: 100%; height: 100%; z-index: 10001; visibility: hidden; transition: all 0.3s; }
                .cart-drawer.active { visibility: visible; }
                .cart-drawer-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); opacity: 0; transition: opacity 0.3s; }
                .cart-drawer.active .cart-drawer-overlay { opacity: 1; }
                .cart-drawer-content { position: absolute; top: 0; right: -400px; width: 400px; max-width: 90%; height: 100%; background: white; box-shadow: -5px 0 15px rgba(0,0,0,0.1); transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1); display: flex; flex-direction: column; }
                .cart-drawer.active .cart-drawer-content { right: 0; }
                
                .cart-header { padding: 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; background: #f9fafb; }
                .cart-header h3 { margin: 0; font-size: 1.2rem; color: #111; font-weight: 600; }
                .close-cart { background: none; border: none; font-size: 1.2rem; cursor: pointer; color: #666; transition: color 0.2s; }
                .close-cart:hover { color: #e11d48; }

                .cart-items-list { flex: 1; overflow-y: auto; padding: 20px; }
                .cart-item { display: flex; gap: 15px; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #f3f4f6; align-items: center; }
                .cart-item-img { width: 70px; height: 70px; object-fit: contain; border-radius: 8px; background: #f9fafb; padding: 5px; }
                .cart-item-info { flex: 1; }
                .cart-item-title { font-weight: 500; font-size: 0.95rem; margin-bottom: 4px; color: #333; }
                .cart-item-price { color: #e11d48; font-weight: 600; font-size: 0.9rem; }
                .cart-item-remove { background: none; border: none; color: #9ca3af; font-size: 0.8rem; cursor: pointer; padding: 0; margin-top: 5px; text-decoration: underline; }
                .cart-item-remove:hover { color: #e11d48; }

                .cart-footer { padding: 20px; border-top: 1px solid #eee; background: #f9fafb; }
                .cart-total { display: flex; justify-content: space-between; font-weight: 700; font-size: 1.1rem; margin-bottom: 15px; color: #111; }
                .whatsapp-checkout-btn { width: 100%; padding: 14px; background: #25D366; color: white; border: none; border-radius: 10px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer; transition: transform 0.2s, background 0.2s; font-size: 1rem; }
                .whatsapp-checkout-btn:hover { background: #128C7E; transform: translateY(-2px); }

                .empty-cart-msg { text-align: center; color: #9ca3af; margin-top: 50px; font-style: italic; }

                /* Checkout Modal */
                .checkout-modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 10002; display: none; align-items: center; justify-content: center; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); }
                .checkout-modal.active { display: flex; }
                .checkout-modal-content { background: white; width: 450px; max-width: 95%; border-radius: 16px; overflow: hidden; animation: modalPop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
                @keyframes modalPop { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
                
                .checkout-header { padding: 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
                .checkout-body { padding: 20px; display: flex; flex-direction: column; gap: 15px; }
                .form-group { display: flex; flex-direction: column; gap: 8px; }
                .form-group label { font-weight: 600; font-size: 0.9rem; color: #444; }
                .form-group input, .form-group textarea { padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit; font-size: 1rem; }
                .checkout-footer { padding: 20px; border-top: 1px solid #eee; }
                .btn-confirm-order { width: 100%; padding: 14px; background: #000; color: white; border: none; border-radius: 10px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 1rem; }
            `;
            document.head.appendChild(style);
        }

        // Create Drawer Structure
        const drawer = document.createElement('div');
        drawer.id = 'cartDrawer';
        drawer.className = 'cart-drawer';
        drawer.innerHTML = `
            <div class="cart-drawer-overlay"></div>
            <div class="cart-drawer-content">
                <div class="cart-header">
                    <h3>Your Basket</h3>
                    <button class="close-cart"><i class="fas fa-times"></i></button>
                </div>
                <div class="cart-items-list"></div>
                <div class="cart-footer">
                    <div class="cart-total">
                        <span>Total:</span>
                        <span class="total-amount">KSh 0</span>
                    </div>
                    <button class="whatsapp-checkout-btn">
                        <i class="fab fa-whatsapp"></i> Checkout via WhatsApp
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(drawer);

        // Checkout Modal
        const modal = document.createElement('div');
        modal.id = 'checkoutModal';
        modal.className = 'checkout-modal';
        modal.innerHTML = `
            <div class="checkout-modal-content">
                <div class="checkout-header">
                    <h3>Complete Your Order</h3>
                    <button class="close-modal"><i class="fas fa-times"></i></button>
                </div>
                <div class="checkout-body">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" id="customerName" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <label>Delivery Location</label>
                        <textarea id="customerLocation" placeholder="e.g. Nairobi, Westlands, Delta Towers" rows="2" required></textarea>
                    </div>
                </div>
                <div class="checkout-footer">
                    <button class="btn-confirm-order"><i class="fab fa-whatsapp"></i> Send Order</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Events
        drawer.querySelector('.close-cart').onclick = toggleCartDrawer;
        drawer.querySelector('.cart-drawer-overlay').onclick = toggleCartDrawer;
        drawer.querySelector('.whatsapp-checkout-btn').onclick = openCheckoutModal;
        modal.querySelector('.close-modal').onclick = closeCheckoutModal;
        modal.querySelector('.btn-confirm-order').onclick = finalizeCheckout;
        modal.addEventListener('click', (e) => { if (e.target === modal) closeCheckoutModal(); });

        updateCartDrawer();
    }

    function displayInternalToast(message) {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
            const style = document.createElement('style');
            style.textContent = `
                .toast-container { position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; }
                .toast { background: #10B981; color: white; padding: 12px 24px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 10px; animation: slideIn 0.3s ease-out forwards; min-width: 250px; }
                @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                @keyframes fadeOut { to { opacity: 0; transform: translateY(10px); } }
            `;
            document.head.appendChild(style);
        }
        const toast = document.createElement('div');
        toast.className = 'toast success';
        toast.innerHTML = `<i class="fas fa-check-circle"></i> <span>${message}</span>`;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    // --- INITIALIZE UI ---
    try {
        updateCartBadges();
        createCartDrawer();
    } catch (e) {
        console.error("Cart UI Initialization failed:", e);
    }

    // --- DELEGATED EVENT LISTENERS ---

    // Add to cart buttons
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.add-to-cart-btn, .add-cart-btn, .pd-btn-cart');
        if (!btn) return;

        e.preventDefault();

        // Data collection
        let id = btn.getAttribute('data-id') || btn.dataset.id || Date.now();
        let title = '';
        let priceText = '';
        let imgSrc = '';
        let quantity = 1;

        // Details page check
        const pdTitle = document.querySelector('.pd-title');
        const pdPrice = document.querySelector('.pd-price');
        const pdImg = document.querySelector('.pd-main-img');
        const qtyInput = document.getElementById('buyQty');

        // Check if we are on details page and the button is the main PD action
        if (pdTitle && pdPrice && (btn.classList.contains('pd-btn-cart') || btn.closest('.pd-action-area'))) {
            title = pdTitle.innerText;
            priceText = pdPrice.innerText;
            imgSrc = pdImg?.src || '';
            quantity = parseInt(qtyInput?.value) || 1;
        } else {
            // Card fallback (Catalog/Home)
            const card = btn.closest('.product-card') || btn.closest('.deal-card');
            if (card) {
                title = card.querySelector('.product-title, .deal-title')?.innerText || 'Unknown';
                priceText = card.querySelector('.product-price, .current-price')?.innerText || '0';
                imgSrc = card.querySelector('img')?.src || '';
            }
        }

        let price = 0;
        if (priceText.toLowerCase().includes('contact') || priceText.toLowerCase().includes('price')) {
            price = 0;
        } else {
            price = parseInt(priceText.replace(/[^0-9]/g, '')) || 0;
        }

        addItemToCart({ id, title, price, image: imgSrc, quantity });

        // Visual Feedback on Button
        const originalHTML = btn.innerHTML;
        const originalBG = btn.style.background;
        btn.innerHTML = '<i class="fas fa-check"></i> Added!';
        btn.style.background = '#27AE60';
        btn.style.color = '#fff';
        btn.disabled = true;

        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.style.background = originalBG;
            btn.style.color = '';
            btn.disabled = false;
        }, 2000);
    });

    // Cart icons
    document.addEventListener('click', (e) => {
        const cartBtn = e.target.closest('.nav-icon-btn-v2[aria-label="Cart"], .cart-btn[aria-label="Cart"], .cart-btn');
        if (cartBtn && !cartBtn.classList.contains('add-to-cart-btn')) {
            e.preventDefault();
            toggleCartDrawer();
        }
    });

    // Sticky bar proxy
    document.addEventListener('click', (e) => {
        if (e.target.closest('#stickyCartBtn')) {
            const mainCartBtn = document.querySelector('.pd-btn-cart[data-id]');
            if (mainCartBtn) mainCartBtn.click();
        }
    });
}

// Global initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCartLogic);
} else {
    initCartLogic();
}
