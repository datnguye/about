// Related Articles Carousel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('related-carousel');
    const prevBtn = document.getElementById('related-prev');
    const nextBtn = document.getElementById('related-next');
    const indicators = document.querySelectorAll('.related-articles-indicator');
    
    if (!carousel || !prevBtn || !nextBtn) return;
    
    const cardWidth = 320; // Card width + gap
    let currentIndex = 0;
    let maxIndex = 0;
    
    function calculateMaxIndex() {
        const containerWidth = carousel.offsetWidth;
        const visibleCards = Math.floor(containerWidth / cardWidth);
        maxIndex = Math.max(0, carousel.children.length - visibleCards);
    }
    
    function updateIndicators() {
        indicators.forEach((dot, index) => {
            if (index === currentIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }
    
    function updateButtons() {
        prevBtn.style.opacity = currentIndex > 0 ? '1' : '0.3';
        nextBtn.style.opacity = currentIndex < maxIndex ? '1' : '0.3';
        prevBtn.style.cursor = currentIndex > 0 ? 'pointer' : 'not-allowed';
        nextBtn.style.cursor = currentIndex < maxIndex ? 'pointer' : 'not-allowed';
    }
    
    function scrollToIndex(index) {
        currentIndex = Math.max(0, Math.min(index, maxIndex));
        carousel.scrollTo({
            left: currentIndex * cardWidth,
            behavior: 'smooth'
        });
        updateIndicators();
        updateButtons();
    }
    
    // Button event listeners
    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) scrollToIndex(currentIndex - 1);
    });
    
    nextBtn.addEventListener('click', () => {
        if (currentIndex < maxIndex) scrollToIndex(currentIndex + 1);
    });
    
    // Indicator clicks
    indicators.forEach((dot, index) => {
        dot.addEventListener('click', () => scrollToIndex(index));
    });
    
    // Keyboard navigation
    carousel.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            scrollToIndex(currentIndex - 1);
        }
        if (e.key === 'ArrowRight') {
            e.preventDefault();
            scrollToIndex(currentIndex + 1);
        }
    });
    
    // Touch/swipe support
    let startX = 0;
    let isDragging = false;
    
    carousel.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
    }, { passive: true });
    
    carousel.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        // Allow natural scrolling
    }, { passive: true });
    
    carousel.addEventListener('touchend', (e) => {
        if (!isDragging) return;
        isDragging = false;
        
        const endX = e.changedTouches[0].clientX;
        const diff = startX - endX;
        
        if (Math.abs(diff) > 50) { // Minimum swipe distance
            if (diff > 0) scrollToIndex(currentIndex + 1);
            else scrollToIndex(currentIndex - 1);
        }
    }, { passive: true });
    
    // Mouse drag support
    let isMouseDown = false;
    let mouseStartX = 0;
    
    carousel.addEventListener('mousedown', (e) => {
        isMouseDown = true;
        mouseStartX = e.clientX;
        carousel.style.cursor = 'grabbing';
        e.preventDefault();
    });
    
    carousel.addEventListener('mousemove', (e) => {
        if (!isMouseDown) return;
        e.preventDefault();
    });
    
    carousel.addEventListener('mouseup', (e) => {
        if (!isMouseDown) return;
        isMouseDown = false;
        carousel.style.cursor = 'grab';
        
        const diff = mouseStartX - e.clientX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) scrollToIndex(currentIndex + 1);
            else scrollToIndex(currentIndex - 1);
        }
    });
    
    carousel.addEventListener('mouseleave', () => {
        if (isMouseDown) {
            isMouseDown = false;
            carousel.style.cursor = 'grab';
        }
    });
    
    // Scroll event listener to update current index based on scroll position
    let scrollTimeout;
    carousel.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const scrollLeft = carousel.scrollLeft;
            const newIndex = Math.round(scrollLeft / cardWidth);
            if (newIndex !== currentIndex) {
                currentIndex = newIndex;
                updateIndicators();
                updateButtons();
            }
        }, 150);
    });
    
    // Initialize
    function init() {
        calculateMaxIndex();
        updateIndicators();
        updateButtons();
        carousel.style.cursor = 'grab';
    }
    
    // Update on window resize
    window.addEventListener('resize', () => {
        calculateMaxIndex();
        updateButtons();
    });
    
    // Initialize carousel
    init();
});