var API_URL = 'https://billowing-hall-4748.nakiaklocko57.workers.dev';
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
        const result = await OfflineAPI.syncManifestAndDatasets(grade, (current, total) => {
            const progressText = document.getElementById('caching-progress-text');
            if (progressText) {
                progressText.innerText = `Downloading offline datasets... (${current}/${total})`;
            }
        });
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

        let baseUser = await this.get('user', userId);

        if (navigator.onLine) { // Force online fetch if possible
            try {
                const queryParams = localStorage.getItem('last_query_params') || '';
                const response = await fetch(`${API_URL}/api/user/${userId}${queryParams}`);
                if (response.ok) {
                    const data = await response.json();
                    data.id = userId;
                    await this.put('user', data);
                    baseUser = data;
                }
            } catch (e) {
                console.warn("Failed to fetch profile online, returning cached version.", e);
            }
        }

        if (!baseUser) {
            baseUser = { id: userId, xp: 0, dtech_points: 0, offline: true };
        }

        // Apply pending local stats from sync_queue to provide a "live" offline experience
        try {
            const queue = await this.getAll('sync_queue');
            let pendingXp = 0;
            let pendingMathXp = 0;
            let pendingPhysicsXp = 0;
            let pendingPoints = 0;
            let pendingQuestions = 0;
            let pendingCorrect = 0;
            let pendingQuizzes = 0;
            let pendingExams = 0;

            for (const item of queue) {
                const payload = item.payload;
                if (!payload) continue;

                // Compare IDs loosely in case of integer vs string
                if (payload.user_id != userId && payload.userId != userId) continue;

                if (item.url.includes('/api/submit-quiz')) {
                    pendingXp += (payload.personalXp || 0);
                    pendingQuestions += (payload.total_questions || 0);
                    pendingCorrect += (payload.correct_answers || 0);
                    pendingQuizzes += 1;

                    if (payload.subject === 'math' || payload.subject === 'mathematics') {
                        pendingMathXp += (payload.personalXp || 0);
                    } else if (payload.subject === 'physics' || payload.subject === 'physical_sciences') {
                        pendingPhysicsXp += (payload.personalXp || 0);
                    }
                } else if (item.url.includes('/api/submit-weekly-exam')) {
                    pendingXp += (payload.totalXp || 0);
                    pendingPoints += (payload.points || 0);
                    pendingQuestions += (payload.total_questions || payload.totalQs || 0);
                    pendingCorrect += (payload.correct_answers || payload.score || 0);
                    pendingExams += 1;

                    if (payload.subject === 'math' || payload.subject === 'mathematics') {
                        pendingMathXp += (payload.totalXp || 0);
                    } else if (payload.subject === 'physics' || payload.subject === 'physical_sciences') {
                        pendingPhysicsXp += (payload.totalXp || 0);
                    }
                } else if (item.url.includes('/api/store/sync-points')) {
                    if (payload.push_claim) {
                        pendingPoints += 100;
                    } else {
                        pendingPoints += (payload.added_points || payload.points || 0);
                    }
                }
            }

            // Create a cloned user object to avoid mutating the IndexedDB cache directly
            const liveUser = JSON.parse(JSON.stringify(baseUser));
            liveUser.offline_pending = true;

            // Apply global values
            liveUser.personal_total_xp = (liveUser.personal_total_xp || liveUser.total_xp || 0) + pendingXp;
            liveUser.total_xp = liveUser.personal_total_xp; // some UI relies on total_xp
            liveUser.dtech_points = (liveUser.dtech_points || 0) + pendingPoints;
            liveUser.available_balance = (liveUser.available_balance || liveUser.dtech_points || 0) + pendingPoints;

            // Apply subjects XP
            liveUser.personal_math_xp = (liveUser.personal_math_xp || liveUser.math_xp || 0) + pendingMathXp;
            liveUser.math_xp = liveUser.personal_math_xp;
            liveUser.personal_physics_xp = (liveUser.personal_physics_xp || liveUser.physics_xp || 0) + pendingPhysicsXp;
            liveUser.physics_xp = liveUser.personal_physics_xp;

            // Apply stats safely nested inside `stats` object if it exists
            if (!liveUser.stats) liveUser.stats = {};
            liveUser.stats.total_questions_answered = (liveUser.stats.total_questions_answered || 0) + pendingQuestions;
            liveUser.stats.correct_answers = (liveUser.stats.correct_answers || 0) + pendingCorrect;
            liveUser.stats.quizzes_completed = (liveUser.stats.quizzes_completed || 0) + pendingQuizzes;
            liveUser.stats.exams_completed = (liveUser.stats.exams_completed || 0) + pendingExams;
            liveUser.stats.incorrect_answers = liveUser.stats.total_questions_answered - liveUser.stats.correct_answers;

            return liveUser;

        } catch (e) {
            console.error("Error merging offline stats", e);
            return baseUser;
        }
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
        let itemsSynced = 0;

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
                    itemsSynced++;
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

        if (itemsSynced > 0) {
            window.dispatchEvent(new Event('offlineSyncComplete'));
        }
    }

    // Dataset Downloader Logic
    async syncManifestAndDatasets(grade, progressCallback) {
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
            const totalDatasets = datasetsToDownload.length;

            if (progressCallback) {
                progressCallback(0, totalDatasets);
            }

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
                if (progressCallback) {
                    progressCallback(downloadedCount, totalDatasets);
                }
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


// ---------------------------------------------------
// Free Mode UI & Notifications (Offline Experience)
// ---------------------------------------------------
function initOfflineUI() {
    // Inject Toast Container
    if (!document.getElementById('dtech-offline-toast-container')) {
        const toastContainer = document.createElement('div');
        toastContainer.id = 'dtech-offline-toast-container';
        toastContainer.style.cssText = 'position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 10001; display: flex; flex-direction: column; gap: 10px; pointer-events: none; width: max-content; max-width: 90%;';
        document.body.appendChild(toastContainer);
    }

    // Inject Free Mode Badge
    if (!document.getElementById('dtech-free-mode-badge')) {
        const badge = document.createElement('div');
        badge.id = 'dtech-free-mode-badge';
        badge.innerHTML = `
            <div style="display: flex; align-items: center; gap: 6px; background: #eab308; color: #1e293b; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 1l22 22"/><path d="M16.72 11.06A10.94 10.94 0 0119 12.55"/><path d="M5 12.55a10.94 10.94 0 015.17-2.39"/><path d="M10.71 5.05A16 16 0 0122.58 9"/><path d="M1.42 9a15.91 15.91 0 018.7-4.16"/><path d="M8.53 16.11a6 6 0 016.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
                Free Mode
            </div>
        `;
        badge.style.cssText = 'position: fixed; bottom: 80px; right: 20px; z-index: 9999; display: none;';
        badge.onclick = showFreeModeModal;
        document.body.appendChild(badge);
    }

    // Inject Modal
    if (!document.getElementById('dtech-free-mode-modal')) {
        const modal = document.createElement('div');
        modal.id = 'dtech-free-mode-modal';
        modal.innerHTML = `
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 10002; display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.3s ease; padding: 20px; box-sizing: border-box;">
                <div style="background: #1e293b; color: #f8fafc; border-radius: 12px; padding: 24px; max-width: 400px; width: 100%; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); transform: translateY(20px); transition: transform 0.3s ease;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px; color: #eab308;">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 1l22 22"/><path d="M16.72 11.06A10.94 10.94 0 0119 12.55"/><path d="M5 12.55a10.94 10.94 0 015.17-2.39"/><path d="M10.71 5.05A16 16 0 0122.58 9"/><path d="M1.42 9a15.91 15.91 0 018.7-4.16"/><path d="M8.53 16.11a6 6 0 016.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
                        <h2 style="margin: 0; font-size: 20px;">Free Mode</h2>
                    </div>
                    <p style="font-size: 14px; line-height: 1.6; margin-bottom: 12px; color: #cbd5e1;">Free Mode is automatically enabled when there is no internet connection.</p>
                    <ul style="font-size: 14px; line-height: 1.6; margin-bottom: 20px; color: #cbd5e1; padding-left: 20px;">
                        <li>All quizzes, exams, XP, streaks, and progress continue to work normally.</li>
                        <li>Progress is stored securely on your device.</li>
                        <li>Once internet is available again, everything is automatically synchronized with the server.</li>
                    </ul>
                    <p style="font-size: 14px; line-height: 1.6; margin-bottom: 24px; color: #94a3b8; font-style: italic;">No user action is required.</p>
                    <button onclick="hideFreeModeModal()" style="width: 100%; background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer;">Got it</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    updateBadgeVisibility();
}

function showFreeModeModal() {
    const modal = document.getElementById('dtech-free-mode-modal');
    if (modal) {
        modal.firstElementChild.style.opacity = '1';
        modal.firstElementChild.style.pointerEvents = 'auto';
        modal.firstElementChild.firstElementChild.style.transform = 'translateY(0)';
    }
}

window.hideFreeModeModal = function() {
    const modal = document.getElementById('dtech-free-mode-modal');
    if (modal) {
        modal.firstElementChild.style.opacity = '0';
        modal.firstElementChild.style.pointerEvents = 'none';
        modal.firstElementChild.firstElementChild.style.transform = 'translateY(20px)';
    }
}

function showOfflineToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('dtech-offline-toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    const bgColors = {
        'info': 'rgba(30, 41, 59, 0.95)',
        'success': 'rgba(16, 185, 129, 0.95)',
        'warning': 'rgba(234, 179, 8, 0.95)'
    };
    const textColors = {
        'info': '#f8fafc',
        'success': '#ffffff',
        'warning': '#1e293b'
    };

    toast.style.cssText = `
        background: ${bgColors[type] || bgColors['info']};
        color: ${textColors[type] || textColors['info']};
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
        text-align: center;
        backdrop-filter: blur(4px);
    `;
    toast.innerText = message;

    container.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    }, 10);

    // Animate out
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function updateBadgeVisibility() {
    const badge = document.getElementById('dtech-free-mode-badge');
    if (badge) {
        badge.style.display = navigator.onLine ? 'none' : 'block';
    }
}

window.addEventListener('load', () => {
    initOfflineUI();
});

window.addEventListener('offline', () => {
    updateBadgeVisibility();
    showOfflineToast("You're offline. Free Mode has been enabled. Your progress will continue to be saved locally.", 'warning', 5000);
});

window.addEventListener('online', () => {
    updateBadgeVisibility();
    showOfflineToast("You're back online. We've found offline progress and are syncing it to your account.", 'info', 4000);
});

window.addEventListener('offlineSyncComplete', () => {
    showOfflineToast("Sync complete. Your progress has been safely uploaded.", 'success', 4000);
});
// ---------------------------------------------------
