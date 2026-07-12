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
    caches.match(event.request, { ignoreSearch: true }).then((cachedResponse) => {
      // 1. & 4. If in cache, serve IMMEDIATELY (Offline navigation guard)
      if (cachedResponse) {
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

// 3. & 6. Atomic Cache Update
self.addEventListener('message', (event) => {
  if (event.data === 'UPDATE_CACHE') {
    event.waitUntil(
      (async () => {
        try {
          const tempCacheName = 'dtech-app-shell-temp-' + Date.now();
          const tempCache = await caches.open(tempCacheName);

          // Download all assets into a temporary cache
          await Promise.all(ASSETS_TO_CACHE.map(async (asset) => {
            const response = await fetch(asset);
            if (!response.ok) throw new Error('Failed to fetch ' + asset);

            // Protect against captive portals serving HTML instead of JS/CSS
            const contentType = response.headers.get('content-type');
            if (!asset.endsWith('.html') && asset !== '/' && !asset.endsWith('.png')) {
              if (contentType && contentType.includes('text/html')) {
                throw new Error('Captive portal detected for ' + asset);
              }
            }
            await tempCache.put(asset, response);
          }));

          // Verify everything was downloaded
          const cachedRequests = await tempCache.keys();
          const cachedUrls = cachedRequests.map(req => new URL(req.url).pathname);
          const allDownloaded = ASSETS_TO_CACHE.every(asset => {
             const normalizedAsset = asset === '/' ? '/' : asset;
             return cachedUrls.includes(normalizedAsset);
          });

          if (!allDownloaded) throw new Error('Not all assets downloaded');

          // Atomic promotion: delete old main cache completely to remove stale assets, then copy new ones
          await caches.delete(CACHE_NAME);
          const mainCache = await caches.open(CACHE_NAME);

          for (const request of cachedRequests) {
            const response = await tempCache.match(request);
            await mainCache.put(request, response);
          }

          await caches.delete(tempCacheName);
          console.log('[SW] Atomic update complete.');

        } catch (error) {
          console.error('[SW] Atomic update failed, retaining old cache:', error);
          // Cleanup temp caches if any failed
          const cacheNames = await caches.keys();
          for (const name of cacheNames) {
            if (name.startsWith('dtech-app-shell-temp-')) {
              await caches.delete(name);
            }
          }
        }
      })()
    );
  }
});
