const CACHE_PREFIX = 'dtech-app-shell-v';
const INITIAL_CACHE_NAME = CACHE_PREFIX + '1';
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

let cachedActiveCacheName = null;
let isUpdating = false;

// Force a fresh read of the cache keys to avoid stale memoization during lifecycle transitions
async function getActiveCacheName(forceRefresh = false) {
  if (cachedActiveCacheName && !forceRefresh) return cachedActiveCacheName;

  const cacheNames = await caches.keys();
  // Filter for our main caches and sort descending
  const mainCaches = cacheNames.filter(name => name.startsWith(CACHE_PREFIX) && !name.includes('temp'));
  if (mainCaches.length > 0) {
    mainCaches.sort((a, b) => {
      const numA = parseInt(a.replace(CACHE_PREFIX, '')) || 0;
      const numB = parseInt(b.replace(CACHE_PREFIX, '')) || 0;
      return numB - numA;
    });
    cachedActiveCacheName = mainCaches[0];
    return cachedActiveCacheName;
  }
  cachedActiveCacheName = INITIAL_CACHE_NAME;
  return cachedActiveCacheName;
}

self.addEventListener('install', (event) => {
  // We only run a basic install for the very first time the SW registers.
  // Subsequent updates are handled entirely by the UPDATE_CACHE atomic process.
  // This prevents standard SW updates from non-atomically overwriting or destroying dynamic caches.
  event.waitUntil(
    (async () => {
      const cacheNames = await caches.keys();
      const hasExistingCache = cacheNames.some(name => name.startsWith(CACHE_PREFIX) && !name.includes('temp'));

      if (!hasExistingCache) {
        const cache = await caches.open(INITIAL_CACHE_NAME);
        await cache.addAll(ASSETS_TO_CACHE);
      }
      await self.skipWaiting();
    })()
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      // Clear memoization to ensure we read the latest state
      cachedActiveCacheName = null;
      await self.clients.claim();
      // We intentionally do NOT delete old caches here.
      // Cache cleanup is exclusively handled by the atomic UPDATE_CACHE process.
    })()
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
    (async () => {
      const activeCacheName = await getActiveCacheName();
      const cachedResponse = await caches.match(event.request, { ignoreSearch: true });

      // 1. & 4. If in cache, serve IMMEDIATELY (Offline navigation guard)
      if (cachedResponse) {
        return cachedResponse;
      }

      // If NOT in cache, attempt network
      return fetch(event.request).then((networkResponse) => {
        // 1. Cache immediately on success (Never lose a page)
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(activeCacheName).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(async () => {
        // 5. Smart Retry & Fallback (if network fails and it wasn't in cache)
        if (event.request.destination === 'document' || url.pathname.endsWith('.html')) {
          const cache = await caches.open(activeCacheName);

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
    })()
  );
});

// 3. & 6. Atomic Cache Update
self.addEventListener('message', (event) => {
  if (event.data === 'UPDATE_CACHE') {
    if (isUpdating) {
        console.log('[SW] Update already in progress. Ignoring duplicate trigger.');
        return;
    }
    isUpdating = true;

    event.waitUntil(
      (async () => {
        let newCacheName = null;
        let tempCacheName = null;
        let promotionSuccessful = false;
        try {
          // Force refresh active cache name to ensure we are updating from the latest state
          const activeCacheName = await getActiveCacheName(true);
          const currentVersion = parseInt(activeCacheName.replace(CACHE_PREFIX, '')) || 0;
          const nextVersion = currentVersion + 1;
          newCacheName = CACHE_PREFIX + nextVersion;
          tempCacheName = 'dtech-app-shell-temp-' + Date.now();

          const tempCache = await caches.open(tempCacheName);

          // Download all static assets into a temporary cache
          await Promise.all(ASSETS_TO_CACHE.map(async (asset) => {
            const response = await fetch(asset);
            if (!response.ok) throw new Error('Failed to fetch ' + asset);
            if (response.type === 'opaque') throw new Error('Opaque response for ' + asset);

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
          const tempCachedRequests = await tempCache.keys();
          const tempCachedUrls = tempCachedRequests.map(req => new URL(req.url).pathname);
          const allDownloaded = ASSETS_TO_CACHE.every(asset => {
             const normalizedAsset = asset === '/' ? '/' : asset;
             return tempCachedUrls.includes(normalizedAsset);
          });

          if (!allDownloaded) throw new Error('Not all assets downloaded');

          // Explicitly verify critical files exist
          const criticalFiles = ['/', '/login.html', '/offline_engine.js', '/register_sw.js'];
          for (const file of criticalFiles) {
            if (!tempCachedUrls.includes(file)) {
              throw new Error('Critical file missing from temp cache: ' + file);
            }
          }

          // Atomic promotion: create the new versioned cache
          const newCache = await caches.open(newCacheName);

          // 1. Copy over verified static assets
          for (const request of tempCachedRequests) {
            const response = await tempCache.match(request);
            await newCache.put(request, response);
          }

          // 2. Carry over any dynamic/runtime cached pages from the old cache
          const oldCache = await caches.open(activeCacheName);
          const oldRequests = await oldCache.keys();
          for (const oldReq of oldRequests) {
            const urlPath = new URL(oldReq.url).pathname;
            const normalizedPath = urlPath === '/' ? '/' : urlPath;
            if (!ASSETS_TO_CACHE.includes(normalizedPath)) {
               const oldResponse = await oldCache.match(oldReq);
               if (oldResponse) await newCache.put(oldReq, oldResponse);
            }
          }

          promotionSuccessful = true;
          cachedActiveCacheName = newCacheName; // Update active cache reference instantly

          // Clean up old caches and the temp cache
          const cacheNames = await caches.keys();
          await Promise.all(
            cacheNames.map((name) => {
              if (name !== newCacheName && name.startsWith(CACHE_PREFIX)) {
                return caches.delete(name);
              }
            })
          );

          await caches.delete(tempCacheName);
          console.log('[SW] Atomic update complete. Promoted to ' + newCacheName);

        } catch (error) {
          console.error('[SW] Atomic update failed, retaining old cache:', error);
          // Cleanup temp caches and incomplete new caches if failed
          if (tempCacheName) await caches.delete(tempCacheName);
          if (newCacheName && !promotionSuccessful) {
             await caches.delete(newCacheName);
          }

          // Failsafe cleanup of any orphaned temp caches
          const cacheNames = await caches.keys();
          for (const name of cacheNames) {
            if (name.includes('temp')) {
              await caches.delete(name);
            }
          }
        } finally {
            isUpdating = false;
        }
      })()
    );
  }
});
