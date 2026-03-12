/**
 * ShuffleBanner.js
 * Reusable logic for the animated "shuffling" banners for NJAWAMU Hardware.
 */

class ShuffleBanner {
    constructor(config) {
        this.containerId = config.containerId;
        this.nameId = config.nameId;
        this.imgId = config.imgId;

        // Specialized configs for Hardware
        this.slideConfigs = [
            {
                displayName: 'PREMIUM PAINTS',
                dataCategory: 'PAINTS',
                prefix: 'QUALITY',
                bannerImg: 'assets/images/featured/placeholder.png'
            },
            {
                displayName: 'ELECTRICALS',
                dataCategory: 'ELECTRICALS',
                prefix: 'STAFE & RELIABLE',
                bannerImg: 'assets/images/featured/placeholder.png'
            },
            {
                displayName: 'PLUMBING',
                dataCategory: 'FITTINGS',
                prefix: 'DURABLE',
                bannerImg: 'assets/images/featured/placeholder.png'
            },
            {
                displayName: 'BUILDING TOOLS',
                dataCategory: 'NAILS',
                prefix: 'PROFESSIONAL',
                bannerImg: 'assets/images/featured/placeholder.png'
            }
        ];

        this.interval = config.interval || 5000;
        this.currentSlideIndex = 0;
        this.init();
    }

    init() {
        this.partNameEl = document.getElementById(this.nameId);
        this.partImgEl = document.getElementById(this.imgId);
        this.bannerInnerEl = document.getElementById(this.containerId);
        this.prefixEl = this.bannerInnerEl ? this.bannerInnerEl.querySelector('.banner-prefix') : null;

        if (!this.partNameEl || !this.partImgEl || !this.bannerInnerEl) return;

        this.start();
    }

    start() {
        this.update(0);
        setInterval(() => this.next(), this.interval);
    }

    update(index) {
        const config = this.slideConfigs[index];
        const imgSrc = config.bannerImg;
        const imgAlt = config.displayName;

        // Fade out
        this.bannerInnerEl.classList.add('banner-fade-out');

        setTimeout(() => {
            if (this.prefixEl) this.prefixEl.textContent = config.prefix;
            this.partNameEl.textContent = config.displayName;
            this.partImgEl.src = imgSrc;
            this.partImgEl.alt = imgAlt;

            requestAnimationFrame(() => {
                this.bannerInnerEl.classList.remove('banner-fade-out');
                this.bannerInnerEl.classList.add('banner-fade-in');
            });

            setTimeout(() => {
                this.bannerInnerEl.classList.remove('banner-fade-in');
            }, 500);
        }, 350);
    }

    next() {
        this.currentSlideIndex = (this.currentSlideIndex + 1) % this.slideConfigs.length;
        this.update(this.currentSlideIndex);
    }
}

window.initShuffleBanners = () => {
    new ShuffleBanner({
        containerId: 'headerBannerInner',
        nameId: 'bannerPartName',
        imgId: 'bannerPartImg'
    });

    const wideBanner = document.getElementById('wideBannerInner');
    if (wideBanner) {
        new ShuffleBanner({
            containerId: 'wideBannerInner',
            nameId: 'widePartName',
            imgId: 'widePartImg'
        });
    }
};

document.addEventListener('DOMContentLoaded', window.initShuffleBanners);
