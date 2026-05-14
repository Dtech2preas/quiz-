const CACHE_NAME = 'dtech-quiz-cache-v1';

// Core assets to cache immediately
const CORE_ASSETS = [
    '/',
    '/index.html',
    '/login.html',
    '/signup.html',
    '/dashboard.html',
    '/quiz.html',
    '/weekly_quiz.html',
    '/test.html',
    '/test_run_grades.html',
    '/test_run_subjects.html',
    '/test_run_quiz.html',
    '/leaderboard.html',
    '/global_leaderboard.html',
    '/profile.html',
    '/public_profile.html',
    '/store.html',
    '/earn_points.html',
    '/stats.html',
    '/admin.html',
    '/map.json',
    '/dtech_cosmetics.js',
    '/offline_mode.js',
    '/favicon.ico',
    '/icons/favicon.ico'
];

self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(CORE_ASSETS.map(url => new Request(url, { cache: 'reload' })));
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
    // Clear old caches
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Helper function to fetch and cache dynamic files
async function fetchAndCache(request) {
    const cache = await caches.open(CACHE_NAME);
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        const cachedResponse = await cache.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        // If it's a page navigation, return a fallback or root
        if (request.mode === 'navigate') {
            return cache.match('/');
        }
        throw error;
    }
}

self.addEventListener('fetch', (event) => {
    // Only cache GET requests
    if (event.request.method !== 'GET') {
        return;
    }

    // API calls should prioritize network, fallback to cache
    const url = new URL(event.request.url);
    if (url.origin.includes('workers.dev') || url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(event.request).catch(async () => {
                const cache = await caches.open(CACHE_NAME);
                const cachedResponse = await cache.match(event.request);
                return cachedResponse || new Response(JSON.stringify({ error: 'Offline', offline: true }), {
                    headers: { 'Content-Type': 'application/json' },
                    status: 503
                });
            })
        );
        return;
    }

    // Static assets & datasets: Network first, fallback to cache
    event.respondWith(fetchAndCache(event.request));
});

self.addEventListener('message', async (event) => {
    if (event.data && event.data.action === 'CACHE_GRADE_DATASETS') {
        const grade = event.data.grade;
        try {
            // Helper function to fetch with a timeout
            const fetchWithTimeout = async (url, options, timeout = 10000) => {
                const controller = new AbortController();
                const id = setTimeout(() => controller.abort(), timeout);
                try {
                    const response = await fetch(url, { ...options, signal: controller.signal });
                    clearTimeout(id);
                    return response;
                } catch (err) {
                    clearTimeout(id);
                    throw err;
                }
            };

            // Fetch map.json with timeout and cache fallback
            let mapResponse;
            try {
                mapResponse = await fetchWithTimeout('/map.json', {}, 5000);
            } catch (err) {
                console.warn('Network fetch for map.json failed or timed out, trying cache...', err);
                const cache = await caches.open(CACHE_NAME);
                mapResponse = await cache.match('/map.json');
                if (!mapResponse) throw new Error('map.json not found in cache and network fetch failed.');
            }

            const mapData = await mapResponse.json();

            const datasetsToCache = [];
            if (mapData[grade]) {
                for (const subject in mapData[grade]) {
                    const files = mapData[grade][subject];
                    for (const fileObj of files) {
                        datasetsToCache.push(`/dataset/${grade}/${subject}/${fileObj.file}`);
                    }
                }
            }

            if (datasetsToCache.length > 0) {
                const cache = await caches.open(CACHE_NAME);
                let completedCount = 0;

                // Fetch datasets sequentially to avoid network congestion and allow for progress updates
                for (const url of datasetsToCache) {
                    try {
                        const response = await fetchWithTimeout(url, {}, 5000);
                        if (response.ok) {
                            await cache.put(url, response.clone());
                        }
                    } catch(e) {
                        console.error('Failed to cache dataset:', url, e);
                    }
                    completedCount++;
                    event.ports[0].postMessage({
                        status: 'progress',
                        current: completedCount,
                        total: datasetsToCache.length
                    });
                }
            }

            // Notify client that caching is complete
            event.ports[0].postMessage({ status: 'success', cachedCount: datasetsToCache.length });
        } catch (error) {
            console.error('Service Worker: Error caching datasets', error);
            event.ports[0].postMessage({ status: 'error', error: error.toString() });
        }
    }
});
