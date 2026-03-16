/**
 * Hero Section — Cinematic Video + Image Carousel
 * Handles crossfade between video and image slides.
 * Videos auto-play when active and pause when inactive.
 */

document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.hero-bg-slide');
    const dots = document.querySelectorAll('.hero-dot');
    const prevBtn = document.getElementById('heroPrev');
    const nextBtn = document.getElementById('heroNext');

    if (!slides.length) return;

    let currentIndex = 0;
    let intervalId;
    const INTERVAL = 2500; // Accelerated to 2.5 seconds per slide

    function handleVideoState(slide, shouldPlay) {
        const video = slide.querySelector('video');
        if (!video) return;
        if (shouldPlay) {
            video.currentTime = 0;
            video.play().catch(() => { }); // Silently catch autoplay blocks
        } else {
            video.pause();
        }
    }

    function showSlide(index) {
        if (index >= slides.length) index = 0;
        if (index < 0) index = slides.length - 1;

        // Deactivate all slides
        slides.forEach(slide => {
            slide.classList.remove('active');
            slide.style.animation = 'none'; // Reset Ken Burns for image slides
            handleVideoState(slide, false);
        });
        dots.forEach(dot => dot.classList.remove('active'));

        // Activate new slide
        currentIndex = index;
        void slides[currentIndex].offsetWidth; // Force reflow
        slides[currentIndex].classList.add('active');
        if (dots[currentIndex]) dots[currentIndex].classList.add('active');

        // Play video if it's a video slide
        handleVideoState(slides[currentIndex], true);
    }

    function nextSlide() { showSlide(currentIndex + 1); }
    function prevSlide() { showSlide(currentIndex - 1); }

    function startAutoPlay() {
        stopAutoPlay();
        intervalId = setInterval(nextSlide, INTERVAL);
    }

    function stopAutoPlay() {
        if (intervalId) clearInterval(intervalId);
    }

    // Dot clicks
    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            stopAutoPlay();
            showSlide(parseInt(dot.dataset.slide, 10));
            startAutoPlay();
        });
    });

    // Arrow clicks
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            stopAutoPlay();
            prevSlide();
            startAutoPlay();
        });
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            stopAutoPlay();
            nextSlide();
            startAutoPlay();
        });
    }

    // Pause carousel on hover
    const heroSection = document.getElementById('hero');
    if (heroSection) {
        heroSection.addEventListener('mouseenter', stopAutoPlay);
        heroSection.addEventListener('mouseleave', startAutoPlay);
    }

    // Touch swipe support
    let touchStartX = 0;
    if (heroSection) {
        heroSection.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        heroSection.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].screenX;
            if (Math.abs(diff) > 50) {
                stopAutoPlay();
                if (diff > 0) nextSlide(); else prevSlide();
                startAutoPlay();
            }
        }, { passive: true });
    }

    // Ensure the first video plays on load
    handleVideoState(slides[0], true);

    // Start auto-rotation
    startAutoPlay();
});
