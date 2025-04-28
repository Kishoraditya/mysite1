// landing/static/js/main.js

/**
 * Main entrypoint for landing page JS
 * - init() sets up any DOM-based modules
 * - performanceTracker() collects paint metrics on window.load
 */

// exported for testing
export function init() {
    console.log('Initializing modules');
  }
  
  export function performanceTracker() {
    const paints = window.performance.getEntriesByType('paint');
    console.log('Paint metrics:', paints);
  }
  
  document.addEventListener('DOMContentLoaded', init);
  window.addEventListener('load', performanceTracker);
  