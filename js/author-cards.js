/**
 * Author Cards Functionality
 * Handles collapse/expand, auto-scroll behavior, and mobile initialization
 */

// Global state
let autoCollapsed = false;

/**
 * Toggle all author cards collapse/expand
 */
function toggleAuthorCards(event) {
    event.stopPropagation(); // Prevent card click event
    const container = document.body;
    container.classList.toggle('author-cards-collapsed');
}

/**
 * Expand author cards when clicking on collapsed card
 */
function expandAuthorCards(event) {
    const container = document.body;
    if (container.classList.contains('author-cards-collapsed')) {
        // Only expand if clicked on the card itself, not on social links
        if (!event.target.closest('.author-social a')) {
            container.classList.remove('author-cards-collapsed');
            autoCollapsed = false; // Mark as manually expanded
        }
    }
}

/**
 * Handle auto-collapse/expand based on scroll position
 */
function handleAuthorCardsScroll() {
    const container = document.body;
    const scrollPosition = window.scrollY;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    
    // Calculate how close to bottom (10% of the way down)
    const scrollPercentage = (scrollPosition + windowHeight) / documentHeight;
    
    if (scrollPercentage > 0.1) {
        // Just started scrolling - auto collapse if not already collapsed
        if (!container.classList.contains('author-cards-collapsed')) {
            container.classList.add('author-cards-collapsed');
            autoCollapsed = true;
        }
    } else if (scrollPercentage <= 0.1 && autoCollapsed) {
        // Scrolled back to top and was auto-collapsed - expand again
        container.classList.remove('author-cards-collapsed');
        autoCollapsed = false;
    }
}

/**
 * Initialize mobile collapsed state
 */
function initializeMobileState() {
    if (window.innerWidth <= 1199) {
        document.body.classList.add('author-cards-collapsed');
        autoCollapsed = false; // Don't auto-expand on mobile
    } else {
        // Remove collapsed state when switching to desktop
        document.body.classList.remove('author-cards-collapsed');
    }
}

/**
 * Initialize author cards functionality
 */
function initializeAuthorCards() {
    // Set up scroll listener for auto-collapse
    window.addEventListener('scroll', handleAuthorCardsScroll);
    
    // Initialize mobile state
    initializeMobileState();
    
    // Handle window resize
    window.addEventListener('resize', initializeMobileState);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeAuthorCards);