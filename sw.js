const CACHE_NAME = 'dtech-app-shell-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/login.html',
  '/signup.html',
  '/dashboard.html',
  '/offline.html',
  '/quiz.html',
  '/subjects.html',
  '/test_run_grades.html',
  '/test_run_subjects.html',
  '/test_run_quiz.html',
  '/weekly_quiz.html',
  '/profile.html',
  '/public_profile.html',
  '/store.html',
  '/earn_points.html',
  '/stats.html',
  '/admin.html',
  '/leaderboard.html',
  '/global_leaderboard.html',
  '/dtech_cosmetics.js',
  '/security.js',
  '/offline_engine.js',
  '/firebase_config.js',
  '/register_sw.js',
  '/update_timer.js',
  '/logo.png',
  '/test.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Cache-first strategy for static assets
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  if (url.origin !== location.origin) return;
  if (url.pathname.startsWith('/api/')) return;
  if (url.pathname.startsWith('/dataset/')) return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Stale-while-revalidate for HTML files
        if (event.request.destination === 'document' || url.pathname.endsWith('.html')) {
          event.waitUntil(
            fetch(event.request).then(networkResponse => {
              if (networkResponse && networkResponse.ok) {
                caches.open(CACHE_NAME).then(cache => {
                  cache.put(event.request, networkResponse);
                });
              }
            }).catch(() => {}) // Ignore if offline
          );
        }
        return cachedResponse;
      }

      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(async () => {
        // Network failed and no direct cache hit.
        if (event.request.destination === 'document' || url.pathname.endsWith('.html')) {
          const cache = await caches.open(CACHE_NAME);

          // Ultimate fallback to offline.html
          const offlineCache = await cache.match('/offline.html');
          if (offlineCache) return offlineCache;

          // Try to fallback to dashboard if offline.html somehow fails
          const dashboardCache = await cache.match('/dashboard.html');
          if (dashboardCache) return dashboardCache;

          // If all else fails, return a basic inline response to avoid Chrome errors
          return new Response(
            '<html><body><h2>Offline</h2><p>Please connect to the internet.</p><a href="/dashboard.html">Retry</a></body></html>',
            { headers: { 'Content-Type': 'text/html' } }
          );
        }
        // If it's not a document, return a generic error instead of failing outright if we don't want Chrome error
        // But throwing is fine for images/scripts since the page will still load.
        throw new Error('Network and cache failed');
      });
    })
  );
});