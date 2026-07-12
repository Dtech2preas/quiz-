if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);

        // Trigger atomic update on startup if activated
        if (navigator.serviceWorker.controller) {
          navigator.serviceWorker.controller.postMessage('UPDATE_CACHE');
        } else {
          // If first install, wait for activation
          navigator.serviceWorker.addEventListener('controllerchange', () => {
            navigator.serviceWorker.controller.postMessage('UPDATE_CACHE');
          });
        }
      })
      .catch(err => {
        console.error('ServiceWorker registration failed: ', err);
      });
  });

  // Self-heal when coming back online
  window.addEventListener('online', () => {
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage('UPDATE_CACHE');
    }
  });
}
