/**
 * Accessibility enhancements module
 * @module accessibility
 */

/**
 * Initialize accessibility enhancements
 * @function init
 */
export function init() {
    // Add skip to content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to content';
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Ensure all interactive elements have appropriate ARIA attributes
    const buttons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
    buttons.forEach(button => {
        if (!button.textContent.trim()) {
            console.warn('Button without text content or ARIA label:', button);
        }
    });
    
    // Ensure all images have alt text
    const images = document.querySelectorAll('img:not([alt])');
    images.forEach(img => {
        console.warn('Image without alt text:', img);
        img.alt = ''; // Set empty alt for decorative images
    });
    
    // Add keyboard navigation for custom components
    document.addEventListener('keydown', (e) => {
        // Handle Escape key
        if (e.key === 'Escape') {
            // Close any open modals or dropdowns
            const modals = document.querySelectorAll('.modal.is-active');
            modals.forEach(modal => {
                modal.classList.remove('is-active');
                modal.setAttribute('aria-hidden', 'true');
            });
        }
    });
}
