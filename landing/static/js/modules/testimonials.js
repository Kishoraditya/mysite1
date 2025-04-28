/**
 * Testimonials slider module
 * @module testimonials
 */

/**
 * Initialize testimonials slider
 * @function init
 * @param {Object} options - Slider options
 */
export function init(options = {}) {
    const defaults = {
        autoplay: true,
        interval: 5000,
        transition: 500
    };
    
    const settings = { ...defaults, ...options };
    const sliders = document.querySelectorAll('.testimonials-slider');
    
    sliders.forEach(slider => {
        const testimonials = slider.querySelectorAll('.testimonial');
        if (testimonials.length <= 1) return;
        
        // Add navigation
        const nav = document.createElement('div');
        nav.className = 'slider-nav';
        
        const prevBtn = document.createElement('button');
        prevBtn.className = 'slider-prev';
        prevBtn.innerHTML = '&larr;';
        prevBtn.setAttribute('aria-label', 'Previous testimonial');
        
        const nextBtn = document.createElement('button');
        nextBtn.className = 'slider-next';
        nextBtn.innerHTML = '&rarr;';
        nextBtn.setAttribute('aria-label', 'Next testimonial');
        
        nav.appendChild(prevBtn);
        nav.appendChild(nextBtn);
        slider.appendChild(nav);
        
        // Set up slider
        let currentIndex = 0;
        let interval = null;
        
        // Hide all testimonials except the first one
        testimonials.forEach((testimonial, index) => {
            if (index !== 0) {
                testimonial.style.display = 'none';
            }
            testimonial.setAttribute('aria-hidden', index !== 0);
        });
        
        // Function to show a specific testimonial
        const showTestimonial = (index) => {
            testimonials.forEach((testimonial, i) => {
                testimonial.style.display = i === index ? 'block' : 'none';
                testimonial.setAttribute('aria-hidden', i !== index);
            });
            currentIndex = index;
        };
        
        // Function to show the next testimonial
        const showNext = () => {
            const nextIndex = (currentIndex + 1) % testimonials.length;
            showTestimonial(nextIndex);
        };
        
        // Function to show the previous testimonial
        const showPrev = () => {
            const prevIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
            showTestimonial(prevIndex);
        };
        
        // Set up event listeners
        nextBtn.addEventListener('click', () => {
            showNext();
            if (interval) {
                clearInterval(interval);
                startAutoplay();
            }
        });
        
        prevBtn.addEventListener('click', () => {
            showPrev();
            if (interval) {
                clearInterval(interval);
                startAutoplay();
            }
        });
        
        // Function to start autoplay
        const startAutoplay = () => {
            if (settings.autoplay) {
                interval = setInterval(showNext, settings.interval);
            }
        };
        
        // Start autoplay
        startAutoplay();
        
        // Pause autoplay when hovering over the slider
        slider.addEventListener('mouseenter', () => {
            if (interval) {
                clearInterval(interval);
            }
        });
        
        // Resume autoplay when mouse leaves the slider
        slider.addEventListener('mouseleave', () => {
            if (settings.autoplay) {
                startAutoplay();
            }
        });
    });
}
