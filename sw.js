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

  // We only cache same-origin requests, except datasets/APIs
  if (url.origin !== location.origin) return;
  if (url.pathname.startsWith('/api/')) return;
  if (url.pathname.startsWith('/dataset/')) return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // 1. & 4. If in cache, serve IMMEDIATELY (Offline navigation guard)
      if (cachedResponse) {
        // 2. Background cache update for ALL assets silently
        event.waitUntil(
          fetch(event.request).then(networkResponse => {
            if (networkResponse && networkResponse.ok) {
              caches.open(CACHE_NAME).then(cache => {
                cache.put(event.request, networkResponse);
              });
            }
          }).catch(() => {}) // Ignore if offline
        );
        return cachedResponse;
      }

      // If NOT in cache, attempt network
      return fetch(event.request).then((networkResponse) => {
        // 1. Cache immediately on success (Never lose a page)
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(async () => {
        // 5. Smart Retry & Fallback (if network fails and it wasn't in cache)
        if (event.request.destination === 'document' || url.pathname.endsWith('.html')) {
          const cache = await caches.open(CACHE_NAME);

          const offlineCache = await cache.match('/offline.html');
          if (offlineCache) return offlineCache;

          const dashboardCache = await cache.match('/dashboard.html');
          if (dashboardCache) return dashboardCache;

          return new Response(
            '<html><body><h2>Offline</h2><p>Please connect to the internet.</p><button onclick="window.location.reload()">Retry</button></body></html>',
            { headers: { 'Content-Type': 'text/html' } }
          );
        }
        throw new Error('Network and cache failed');
      });
    })
  );
});

// 3. & 6. Cache Verification & Self-healing
self.addEventListener('message', (event) => {
  if (event.data === 'VERIFY_CACHE') {
    event.waitUntil(
      caches.open(CACHE_NAME).then(async (cache) => {
        const cachedRequests = await cache.keys();
        const cachedUrls = cachedRequests.map(req => new URL(req.url).pathname);

        // Find missing essential assets
        const missingAssets = ASSETS_TO_CACHE.filter(asset => {
          // Normalize paths for comparison
          const normalizedAsset = asset === '/' ? '/' : asset;
          return !cachedUrls.includes(normalizedAsset);
        });

        // Re-cache missing assets
        if (missingAssets.length > 0) {
          console.log('[SW] Self-healing missing assets:', missingAssets);
          await cache.addAll(missingAssets).catch(e => console.warn('[SW] Self-healing partially failed offline', e));
        }

        // Also update existing essential assets in background to keep them fresh
        const existingAssets = ASSETS_TO_CACHE.filter(asset => !missingAssets.includes(asset));
        existingAssets.forEach(asset => {
          fetch(asset).then(response => {
            if (response.ok) cache.put(asset, response);
          }).catch(() => {});
        });
      })
    );
  }
});
