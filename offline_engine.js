const API_URL = 'https://billowing-hall-4748.nakiaklocko57.workers.dev';
// Utility snippet to trigger dataset caching manually (e.g. from dashboard)
window.startOfflineDownload = async function(grade) {
    if (!grade) grade = localStorage.getItem('user_grade') || 'grade12';

    // Add banner
    const bannerHtml = `
        <div id="caching-progress-banner" style="position: fixed; top: 0; left: 0; width: 100%; background: #2d3748; color: #fff; padding: 10px; z-index: 10000; box-shadow: 0 2px 4px rgba(0,0,0,0.3); text-align: center; border-bottom: 1px solid #4a5568;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; max-width: 600px; margin: 0 auto; width: 100%;">
                <div id="caching-progress-text" style="font-size: 12px; font-weight: bold; color: #eab308; margin-bottom: 5px;">Downloading offline datasets...</div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', bannerHtml);

    try {
        const result = await OfflineAPI.syncManifestAndDatasets(grade);
        const banner = document.getElementById('caching-progress-banner');
        if (result.success) {
            banner.innerHTML = `<div style="text-align:center; color: #10b981; font-weight: bold;">Download Complete! You can now use the app offline.</div>`;
            setTimeout(() => banner.remove(), 3000);
        } else {
            banner.innerHTML = `<div style="text-align:center; color: #ef4444; font-weight: bold;">Download failed: ${result.message}</div>`;
            setTimeout(() => banner.remove(), 5000);
        }
    } catch (e) {
        console.error(e);
        const banner = document.getElementById('caching-progress-banner');
        if (banner) {
            banner.innerHTML = `<div style="text-align:center; color: #ef4444; font-weight: bold;">Download failed.</div>`;
            setTimeout(() => banner.remove(), 5000);
        }
    }
};

// Check for Android App Flag slightly delayed to let WebView finish loading interface
window.addEventListener('load', () => {
    setTimeout(() => {
        if (window.IS_ANDROID_APP) {
            const userGrade = localStorage.getItem('user_grade');
            if (userGrade) {
                // Auto start caching on load for android app if needed
                OfflineAPI.getDB().then(db => {
                    db.transaction('manifest').objectStore('manifest').get('latest').onsuccess = (e) => {
                        const manifest = e.target.result;
                        if (!manifest || manifest.downloadedGrade !== userGrade) {
                             window.startOfflineDownload(userGrade);
                        }
                    };
                });
            }
        }
    }, 1000);
});
// OfflineEngine: A unified IndexedDB-backed data layer for the DTECH platform.

const DB_NAME = 'dtech_offline_db';
const DB_VERSION = 1;

class OfflineEngineClass {
    constructor() {
        this.db = null;
        this.dbPromise = this.initDB();
    }

    async initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(DB_NAME, DB_VERSION);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                if (!db.objectStoreNames.contains('manifest')) {
                    db.createObjectStore('manifest', { keyPath: 'id' });
                }

                if (!db.objectStoreNames.contains('datasets')) {
                    const datasetStore = db.createObjectStore('datasets', { keyPath: 'path' });
                    datasetStore.createIndex('grade', 'grade', { unique: false });
                    datasetStore.createIndex('subject', 'subject', { unique: false });
                }

                if (!db.objectStoreNames.contains('user')) {
                    db.createObjectStore('user', { keyPath: 'id' });
                }

                if (!db.objectStoreNames.contains('sync_queue')) {
                    const syncQueue = db.createObjectStore('sync_queue', { keyPath: 'id', autoIncrement: true });
                    syncQueue.createIndex('status', 'status', { unique: false });
                }

                if (!db.objectStoreNames.contains('metadata')) {
                    db.createObjectStore('metadata', { keyPath: 'key' });
                }
            };

            request.onsuccess = (event) => {
                this.db = event.target.result;
                resolve(this.db);
            };

            request.onerror = (event) => {
                console.error("IndexedDB initialization error:", event.target.error);
                reject(event.target.error);
            };
        });
    }

    async getDB() {
        if (this.db) return this.db;
        return await this.dbPromise;
    }

    async get(storeName, key) {
        const db = await this.getDB();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.get(key);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    async put(storeName, data) {
        const db = await this.getDB();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.put(data);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    async delete(storeName, key) {
        const db = await this.getDB();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.delete(key);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }

    async getAll(storeName) {
        const db = await this.getDB();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Core OfflineAPI Implementation

    async getProfile(userId) {
        if (!userId) {
            userId = localStorage.getItem('user_id');
        }
        if (!userId) return null;

        const cachedUser = await this.get('user', userId);

        if (navigator.onLine) { // Force online fetch if possible
            try {
                const queryParams = localStorage.getItem('last_query_params') || '';
                const response = await fetch(`${API_URL}/api/user/${userId}${queryParams}`);
                if (response.ok) {
                    const data = await response.json();
                    data.id = userId;
                    await this.put('user', data);
                    return data;
                }
            } catch (e) {
                console.warn("Failed to fetch profile online, returning cached version.", e);
            }
        }

        return cachedUser || { id: userId, xp: 0, dtech_points: 0, offline: true };
    }

    async getPublicProfile(username) {
        let cached = await this.get('metadata', `public_profile_${username}`);

        if (navigator.onLine) {
            try {
                const response = await fetch(`${API_URL}/api/public-user/${username}`);
                if (response.ok) {
                    const data = await response.json();
                    await this.put('metadata', { key: `public_profile_${username}`, data: data });
                    return data;
                }
                if (response.status === 404) return null;
            } catch (e) {
                console.warn("Failed to fetch public profile online", e);
            }
        }

        if (cached) return cached.data;
        return { offline: true, error: "Public profiles are unavailable offline." };
    }

    async getLeaderboard(grade, queryParams = '') {
        let cacheKey = `leaderboard_${grade}${queryParams}`;
        let cached = await this.get('metadata', cacheKey);

        if (navigator.onLine) {
            try {
                const response = await fetch(`${API_URL}/api/leaderboard?grade=${grade}${queryParams}`);
                if (response.ok) {
                    const data = await response.json();
                    await this.put('metadata', { key: cacheKey, data: data });
                    return data;
                }
            } catch (e) {
                console.warn("Failed to fetch leaderboard online", e);
            }
        }

        if (cached) return cached.data;
        return { overall: [], offline: true, error: "Leaderboards are unavailable offline." };
    }

    async enqueueSync(url, payload) {
        const action = {
            url: url,
            payload: payload,
            created: Date.now(),
            status: 'pending'
        };
        await this.put('sync_queue', action);
        this.attemptSync(); // Fire and forget
    }

    async getDataset(path) {
        // We expect absolute paths here for uniformity like /dataset/grade12/math/paper1.json
        const cleanPath = path.startsWith('/') ? path : '/' + path;

        const cached = await this.get('datasets', cleanPath);
        if (cached && cached.data) {
            return cached.data;
        }

        if (navigator.onLine) {
            try {
                const response = await fetch(cleanPath);
                if (response.ok) {
                    const data = await response.json();
                    // We shouldn't blindly cache here without verifying against manifest,
                    // but for direct fetches, we return data. Manifest engine handles caching proper.
                    return data;
                }
            } catch (e) {
                console.error("Failed to fetch dataset online", e);
            }
        }

        throw new Error(`Dataset ${cleanPath} not found offline and network unavailable.`);
    }

    // Attempt to sync pending items
    async attemptSync() {
        if (!navigator.onLine) return; // Wait until online

        const queue = await this.getAll('sync_queue');
        if (queue.length === 0) return;

        let allSuccess = true;
        for (const item of queue) {
            try {
                // Prepend API_URL to sync urls if they are relative to backend
                let syncUrl = item.url;
                if (syncUrl.startsWith('/api/')) {
                    syncUrl = API_URL + syncUrl;
                }

                const response = await fetch(syncUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(item.payload)
                });

                if (response.ok) {
                    await this.delete('sync_queue', item.id);
                } else {
                    allSuccess = false;
                    console.error("Sync failed for item", item, response.status);
                }
            } catch (e) {
                allSuccess = false;
                console.error("Sync fetch failed for item", item, e);
                break; // Stop if network is down
            }
        }
    }

    // Dataset Downloader Logic
    async syncManifestAndDatasets(grade) {
        if (!navigator.onLine) {
            return { success: false, message: "Offline. Cannot download datasets." };
        }

        try {
            // Fetch remote manifest
            const res = await fetch('/manifest.json');
            if (!res.ok) throw new Error("Failed to fetch manifest");
            const remoteManifest = await res.json();

            // Filter datasets for the requested grade + common files like map.json
            const datasetsToDownload = remoteManifest.datasets.filter(ds => ds.grade === grade || ds.grade === "");

            let downloadedCount = 0;
            const tempStore = [];

            for (const ds of datasetsToDownload) {
                // Fetch the file
                const fileRes = await fetch(ds.path);
                if (!fileRes.ok) throw new Error(`Failed to fetch ${ds.path}`);

                const fileData = await fileRes.json();

                // TODO: Verify SHA-256 hash here if needed, in JS it's async using crypto.subtle
                // Wait for the raw text to hash it exactly as it is on the server
                // We fetched json above, let's re-fetch as text just for the hash, or we should have fetched text first.
                // Re-fetching is okay since service worker caches it.
                const textRes = await fetch(ds.path);
                const fileText = await textRes.text();

                const hashBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(fileText));
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

                if (hashHex !== ds.hash) {
                    throw new Error(`Hash mismatch for ${ds.path}. Expected ${ds.hash}, got ${hashHex}. Download aborted.`);
                }

                tempStore.push({
                    path: ds.path,
                    grade: ds.grade,
                    subject: ds.subject,
                    hash: ds.hash,
                    data: fileData,
                    updatedAt: Date.now()
                });

                downloadedCount++;
            }

            // Atomic Commit
            const db = await this.getDB();
            return new Promise((resolve, reject) => {
                const transaction = db.transaction(['datasets', 'manifest'], 'readwrite');
                const dsStore = transaction.objectStore('datasets');
                const manifestStore = transaction.objectStore('manifest');

                // Save datasets
                tempStore.forEach(ds => dsStore.put(ds));

                // Update manifest state
                manifestStore.put({ id: 'latest', version: remoteManifest.version, downloadedGrade: grade });

                transaction.oncomplete = () => {
                    resolve({ success: true, count: downloadedCount });
                };

                transaction.onerror = (e) => {
                    reject(e.target.error);
                };
            });

        } catch (e) {
            console.error("Dataset sync failed:", e);
            return { success: false, message: e.message };
        }
    }
}



// Listen for online event to trigger sync
window.addEventListener('online', () => {
    OfflineAPI.attemptSync();
});

const OfflineAPI = new OfflineEngineClass();
window.OfflineAPI = OfflineAPI;
