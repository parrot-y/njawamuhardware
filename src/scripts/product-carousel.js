document.addEventListener('DOMContentLoaded', () => {
    // Hot Deals Carousel Logic
    const initCarousel = () => {
        const track = document.querySelector('.deals-track');
        if (!track) return;

        const prevBtn = document.querySelector('.deals-nav-prev');
        const nextBtn = document.querySelector('.deals-nav-next');
        const cards = document.querySelectorAll('.deal-card');

        if (!prevBtn || !nextBtn || cards.length === 0) return;

        let currentIndex = 0;
        const cardWidth = cards[0].offsetWidth + 30; /* 30px is gap */
        const visibleCards = Math.floor(track.parentElement.offsetWidth / cardWidth) || 1;
        const maxIndex = Math.max(0, cards.length - visibleCards);

        // Update Button States
        const updateButtons = () => {
            prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            prevBtn.style.pointerEvents = currentIndex === 0 ? 'none' : 'all';

            nextBtn.style.opacity = currentIndex >= maxIndex ? '0.5' : '1';
            nextBtn.style.pointerEvents = currentIndex >= maxIndex ? 'none' : 'all';
        };

        // Scroll Function
        const scrollCarousel = (direction) => {
            if (direction === 'next' && currentIndex < maxIndex) {
                currentIndex++;
            } else if (direction === 'prev' && currentIndex > 0) {
                currentIndex--;
            }

            const translateX = currentIndex * -cardWidth;
            track.style.transform = `translateX(${translateX}px)`;
            updateButtons();
        };

        // Event Listeners
        prevBtn.addEventListener('click', () => scrollCarousel('prev'));
        nextBtn.addEventListener('click', () => scrollCarousel('next'));

        // Window Resize Handler
        window.addEventListener('resize', () => {
            // Update measurements on resize
            /* Simplified logic - could be improved with ResizeObserver */
            track.style.transform = 'translateX(0)';
            currentIndex = 0;
            updateButtons();
        });

        // Initialize state
        updateButtons();
    };

    initCarousel();
});
