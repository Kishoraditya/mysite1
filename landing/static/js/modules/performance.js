/**
 * Performance optimization module
 * @module performance
 */

/**
 * Initialize performance optimizations
 * @function init
 */
export function init() {
    // Defer non-critical resources
    const deferredScripts = document.querySelectorAll('script[data-defer]');
    
    if ('requestIdleCallback' in window) {
        window.requestIdleCallback(() => {
            deferredScripts.forEach(script => {
                const newScript = document.createElement('script');
                Array.from(script.attributes).forEach(attr => {
                    if (attr.name !== 'data-defer') {
                        newScript.setAttribute(attr.name, attr.value);
                    }
                });
                newScript.textContent = script.textContent;
                script.parentNode.replaceChild(newScript, script);
            });
        });
    } else {
        // Fallback for browsers that don't support requestIdleCallback
        setTimeout(() => {
            deferredScripts.forEach(script => {
                const newScript = document.createElement('script');
                Array.from(script.attributes).forEach(attr => {
                    if (attr.name !== 'data-defer') {
                        newScript.setAttribute(attr.name, attr.value);
                    }
                });
                newScript.textContent = script.textContent;
                script.parentNode.replaceChild(newScript, script);
            });
        }, 2000);
    }
    
    // Report performance metrics
    if ('performance' in window && 'getEntriesByType' in performance) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const paintMetrics = performance.getEntriesByType('paint');
                const navigationTiming = performance.getEntriesByType('navigation')[0];
                
                if (paintMetrics.length > 0) {
                    paintMetrics.forEach(metric => {
                        console.log(`${metric.name}: ${metric.startTime}ms`);
                    });
                }
                
                if (navigationTiming) {
                    console.log(`DOM Content Loaded: ${navigationTiming.domContentLoadedEventEnd}ms`);
                    console.log(`Load Event: ${navigationTiming.loadEventEnd}ms`);
                }
            }, 0);
        });
    }
}
