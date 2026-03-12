/**
 * NJAWAMU Hardware — Animation Layer v2
 * Scroll-triggered reveals + dynamic card stagger (works on all pages)
 */

(function () {
    'use strict';

    /* ─────────────────────────────────────────
     * 1.  IntersectionObserver  (core engine)
     * ───────────────────────────────────────── */
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const delay = el.dataset.delay || 0;
                setTimeout(() => el.classList.add('reveal-active'), Number(delay));
                revealObserver.unobserve(el);
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -60px 0px' }
    );

    /* ─────────────────────────────────────────
     * 2.  Observe a single element
     * ───────────────────────────────────────── */
    function observe(el) {
        if (!el || el.dataset.observed) return;
        el.dataset.observed = '1';
        el.classList.add('reveal-element');
        revealObserver.observe(el);
    }

    /* ─────────────────────────────────────────
     * 3.  Stagger a list of elements
     * ───────────────────────────────────────── */
    function staggerObserve(elements, baseDelay = 0, step = 80) {
        elements.forEach((el, i) => {
            if (!el.dataset.delay) el.dataset.delay = baseDelay + i * step;
            observe(el);
        });
    }

    /* ─────────────────────────────────────────
     * 4.  Initial page scan
     * ───────────────────────────────────────── */
    function scanPage() {
        /* Explicit reveal elements (already marked in HTML) */
        document.querySelectorAll('.reveal-element:not([data-observed])').forEach(el => {
            revealObserver.observe(el);
            el.dataset.observed = '1';
        });

        /* Featured product grid — stagger */
        document.querySelectorAll('.featured-grid').forEach(grid => {
            staggerObserve([...grid.children]);
        });

        /* Quick-access category cards — stagger */
        document.querySelectorAll('.categories-grid').forEach(grid => {
            staggerObserve([...grid.children], 0, 70);
        });

        /* Hot-deal cards */
        document.querySelectorAll('.deal-card').forEach((card, i) => {
            if (!card.dataset.delay) card.dataset.delay = i * 100;
            observe(card);
        });

        /* Section headers / tags / titles */
        document.querySelectorAll(
            '.section-tag, .section-title-v2, .featured-header, ' +
            '.quick-categories-header, .deals-header'
        ).forEach(el => observe(el));

        /* Product cards rendered in catalog (static fallback scan) */
        document.querySelectorAll('.product-card:not([data-observed])').forEach((card, i) => {
            card.dataset.delay = (i % 6) * 60;   // reset delay per visual row
            observe(card);
        });

        /* Footer columns */
        document.querySelectorAll('.footer-col').forEach((col, i) => {
            col.dataset.delay = i * 80;
            observe(col);
        });
    }

    /* ─────────────────────────────────────────
     * 5.  MutationObserver — handles catalog cards
     *     rendered after initial page load
     * ───────────────────────────────────────── */
    let cardBatch = [];
    let batchTimer = null;

    function flushBatch() {
        batchTimer = null;
        cardBatch.forEach((card, i) => {
            card.dataset.delay = card.dataset.delay || i * 60;
            observe(card);
        });
        cardBatch = [];
    }

    const mutationObserver = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType !== 1) return;

                /* Directly added product card */
                if (node.classList.contains('product-card')) {
                    cardBatch.push(node);
                }
                /* Container that holds product cards */
                else {
                    node.querySelectorAll('.product-card:not([data-observed])').forEach(c => {
                        cardBatch.push(c);
                    });
                }

                /* Any new reveal-elements added dynamically */
                node.querySelectorAll && node.querySelectorAll('.reveal-element:not([data-observed])').forEach(el => {
                    revealObserver.observe(el);
                    el.dataset.observed = '1';
                });
            });
        });

        if (cardBatch.length && !batchTimer) {
            batchTimer = setTimeout(flushBatch, 30);
        }
    });

    mutationObserver.observe(document.body, { childList: true, subtree: true });

    /* ─────────────────────────────────────────
     * 6.  Parallax on hero slides
     * ───────────────────────────────────────── */
    function parallaxHero() {
        const slides = document.querySelectorAll('.hero-bg-slide');
        if (!slides.length) return;
        window.addEventListener('scroll', () => {
            const scroll = window.pageYOffset;
            slides.forEach(slide => {
                if (slide.classList.contains('active')) {
                    slide.style.backgroundPositionY = `${scroll * 0.35}px`;
                }
            });
        }, { passive: true });
    }

    /* ─────────────────────────────────────────
     * 7.  Smooth counter animation (stats)
     * ───────────────────────────────────────── */
    function animateCounters() {
        document.querySelectorAll('[data-count]').forEach(el => {
            const target = parseInt(el.dataset.count, 10);
            let current = 0;
            const step = Math.ceil(target / 60);
            const timer = setInterval(() => {
                current = Math.min(current + step, target);
                el.textContent = current.toLocaleString();
                if (current >= target) clearInterval(timer);
            }, 20);
        });
    }

    /* ─────────────────────────────────────────
     * 8.  Boot
     * ───────────────────────────────────────── */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            scanPage();
            parallaxHero();
        });
    } else {
        scanPage();
        parallaxHero();
    }

    window.addEventListener('load', animateCounters);

})();
