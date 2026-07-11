const CACHE_NAME = 'dtech-app-shell-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/login.html',
  '/signup.html',
  '/dashboard.html',
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
  // We only want to cache GET requests for our own origin that aren't API calls or datasets
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  if (url.origin !== location.origin) return;
  if (url.pathname.startsWith('/api/')) return; // Let OfflineAPI handle APIs
  if (url.pathname.startsWith('/dataset/')) return; // Let OfflineAPI handle datasets

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version if found
        if (response) {
          // Stale-while-revalidate for HTML files to keep them fresh
          if (event.request.destination === 'document' || url.pathname.endsWith('.html')) {
             event.waitUntil(
                 fetch(event.request).then(networkResponse => {
                     caches.open(CACHE_NAME).then(cache => {
                         cache.put(event.request, networkResponse);
                     });
                 }).catch(() => {}) // Ignore if offline
             );
          }
          return response;
        }

        // Otherwise fetch from network
        return fetch(event.request).then((networkResponse) => {
          // Cache the new asset dynamically
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
          }
          return networkResponse;
        }).catch(() => {
           // If network fails and it's an HTML page, maybe fallback to index/dashboard
           if (event.request.destination === 'document' || url.pathname.endsWith('.html')) {
               return caches.match('/dashboard.html');
           }
        });
      })
  );
});
