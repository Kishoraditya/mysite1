/**
 * Jest tests for JavaScript performance optimizations
 */

describe('Main JS initialization', () => {
  let originalConsoleLog;
  let originalPerformance;

  beforeEach(() => {
    jest.resetModules();
    
    // Save original console.log
    originalConsoleLog = console.log;
    console.log = jest.fn();
    
    // Save original performance object
    originalPerformance = window.performance;
    
    // Mock DOM methods
    document.addEventListener = jest.fn((event, handler) => {
      if (event === 'DOMContentLoaded') {
        // Store and immediately call the handler
        handler();
      }
    });
    
    window.addEventListener = jest.fn((event, handler) => {
      if (event === 'load') {
        // Store the handler to call it later
        window.loadHandler = handler;
      }
    });
    
    // Mock performance API
    window.performance = {
      getEntriesByType: jest.fn().mockReturnValue([
        { name: 'first-paint', startTime: 100 },
        { name: 'first-contentful-paint', startTime: 200 }
      ])
    };
  });

  afterEach(() => {
    // Restore original console.log
    console.log = originalConsoleLog;
    
    // Restore original performance object
    window.performance = originalPerformance;
  });

  test('should initialize modules when DOM is ready', () => {
    // Import the module after setting up mocks
    const { init } = require('../main.js');
    
    // Check if DOMContentLoaded event listener was added
    expect(document.addEventListener).toHaveBeenCalledWith(
      'DOMContentLoaded',
      expect.any(Function)
    );
    
    // Verify init was called (via console.log)
    expect(console.log).toHaveBeenCalledWith('Initializing modules');
  });

  test('should report performance metrics', () => {
    // Import the module after setting up mocks
    require('../main.js');
    
    // Check if load event listener was added
    expect(window.addEventListener).toHaveBeenCalledWith(
      'load',
      expect.any(Function)
    );
    
    // Call the load handler
    window.loadHandler();
    
    // Verify performance metrics were collected
    expect(window.performance.getEntriesByType).toHaveBeenCalledWith('paint');
    expect(console.log).toHaveBeenCalledWith('Paint metrics:', expect.any(Array));
  });
});

describe('Performance features', () => {
  beforeEach(() => {
    jest.resetModules();
    document.addEventListener = jest.fn();
    window.addEventListener = jest.fn();
    Object.defineProperty(window, 'performance', {
      value: {
        getEntriesByType: jest.fn(() => [
          { name: 'first-paint', startTime: 100 },
          { name: 'first-contentful-paint', startTime: 200 },
        ]),
      },
      writable: true,
    });
  });

  test('should report performance metrics', () => {
    jest.isolateModules(() => {
      require('../main.js');
      const loadCall = window.addEventListener.mock.calls.find(
        call => call[0] === 'load'
      );
      expect(loadCall).toBeDefined();
      const loadHandler = loadCall[1];
      loadHandler();
      expect(window.performance.getEntriesByType).toHaveBeenCalledWith('paint');
    });
  });
});
