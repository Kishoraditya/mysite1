// mysite/static/js/tests/setup.js

// Configure JSDOM environment if necessary (Jest often does this automatically,
// but explicit setup can be helpful if you need specific JSDOM options)
// For most cases, Jest's default jsdom environment is sufficient.

// Mock DOM methods globally
// These mocks will be available in all test files after this setup runs
global.document.addEventListener = jest.fn();
global.window.addEventListener = jest.fn();

// Mock console methods globally
global.console.warn = jest.fn();
global.console.error = jest.fn();
global.log = jest.fn(); // Note: Your test uses console.log, so mock that explicitly
global.console.log = jest.fn();


// Mock performance API globally
Object.defineProperty(global.window, 'performance', {
  value: {
    getEntriesByType: jest.fn().mockReturnValue([
      { name: 'first-paint', startTime: 100 },
      { name: 'first-contentful-paint', startTime: 200 }
    ]),
    mark: jest.fn(),
    measure: jest.fn()
  },
  // Ensure it's writable so tests can potentially override if needed
  writable: true,
});

// Mock setTimeout globally (if your code uses it)
jest.useFakeTimers();

// Add any other necessary global mocks here