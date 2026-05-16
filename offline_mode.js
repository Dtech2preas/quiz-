// Force unregister any existing zombie Service Workers
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for(let registration of registrations) {
            registration.unregister();
        }
    });
}
// offline_mode.js - Handles offline detection, caching logic, UI adjustments, and Android batch syncing

document.addEventListener('DOMContentLoaded', () => {
    // Inject Free Mode Banner
    const bannerHtml = `
        <div id="offline-banner" style="display: none; background: #eab308; color: #1f2937; padding: 10px; text-align: center; font-weight: bold; z-index: 9999; position: sticky; top: 0; width: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            ⚠️ FREE MODE (OFFLINE)
            <button onclick="showOfflineInfo()" style="margin-left: 10px; background: #1f2937; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">What is this?</button>
        </div>
    `;
    document.body.insertAdjacentHTML('afterbegin', bannerHtml);

    // Inject Info Modal
    const modalHtml = `
        <div id="offline-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 10000; justify-content: center; align-items: center;">
            <div style="background: var(--bg-card, #2d3748); color: var(--text-color, #fff); padding: 20px; border-radius: 10px; max-width: 400px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h2 style="color: #eab308; margin-top: 0;">Free Mode (Offline)</h2>
                <p style="margin-bottom: 15px;">You are currently disconnected from the internet. The app has enabled <strong>Free Mode</strong>, allowing you to access quizzes and study materials stored on your phone's storage.</p>
                <p style="margin-bottom: 15px;"><strong>What does this mean?</strong></p>
                <ul style="text-align: left; margin-bottom: 15px;">
                    <li>You can still take quizzes and view your dashboard.</li>
                    <li>Store, Ads, and D-TECH points are disabled to prevent errors.</li>
                    <li>Your progress (scores, XP) will be saved locally on your phone.</li>
                    <li>When you reconnect to the internet, your progress will automatically sync to the server for everyone to see on the leaderboards!</li>
                </ul>
                <button onclick="closeOfflineInfo()" style="background: #eab308; color: #1f2937; font-weight: bold; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">Got it!</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    // Inject background progress banner for caching
    const progressBannerHtml = `
        <div id="caching-progress-banner" style="display: none; position: fixed; top: 0; left: 0; width: 100%; background: #2d3748; color: #fff; padding: 10px; z-index: 10000; box-shadow: 0 2px 4px rgba(0,0,0,0.3); text-align: center; border-bottom: 1px solid #4a5568;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; max-width: 600px; margin: 0 auto; width: 100%;">
                <div id="caching-progress-text" style="font-size: 12px; font-weight: bold; color: #eab308; margin-bottom: 5px;">Starting download...</div>
                <div style="width: 100%; background: #1a202c; border-radius: 5px; height: 6px; overflow: hidden;">
                    <div id="caching-progress-bar" style="width: 0%; height: 100%; background: #eab308; transition: width 0.3s;"></div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', progressBannerHtml);

    // Inject Sync Overlay
    const syncOverlayHtml = `
        <div id="sync-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 20000; justify-content: center; align-items: center; flex-direction: column; color: white;">
            <div class="spinner" style="border: 4px solid rgba(255,255,255,0.3); border-top: 4px solid #eab308; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin-bottom: 20px;"></div>
            <h2 style="margin: 0; font-size: 1.5rem; color: #eab308;">Syncing your progress...</h2>
            <p style="margin-top: 10px; font-size: 1rem;">Please wait</p>
            <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', syncOverlayHtml);

    // Offline status logic
    function updateOnlineStatus() {
        const isOffline = !navigator.onLine;
        const banner = document.getElementById('offline-banner');

        if (isOffline) {
            banner.style.display = 'block';
            disableFeatures();
        } else {
            banner.style.display = 'none';
            enableFeatures();
            if (!window.IS_ANDROID_APP) {
                // If not android, sync normally when back online
                syncOfflineProgress();
            }
        }
    }

    function disableFeatures() {
        // Disable store, ads, dtech points links
        const navLinks = document.querySelectorAll('a');
        navLinks.forEach(link => {
            const href = link.getAttribute('href') || '';
            if (href.includes('store.html') || href.includes('earn_points.html')) {
                link.style.pointerEvents = 'none';
                link.style.opacity = '0.5';
                link.title = 'Disabled in Free Mode';
            }
        });

        // Hide specific buttons
        const adButton = document.getElementById('watch-ad-btn');
        if (adButton) adButton.style.display = 'none';
    }

    function enableFeatures() {
        const navLinks = document.querySelectorAll('a');
        navLinks.forEach(link => {
            const href = link.getAttribute('href') || '';
            if (href.includes('store.html') || href.includes('earn_points.html')) {
                link.style.pointerEvents = 'auto';
                link.style.opacity = '1';
                link.title = '';
            }
        });
    }

    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    // Initial check
    updateOnlineStatus();
});

// Expose modal functions to window
window.showOfflineInfo = function() {
    document.getElementById('offline-modal').style.display = 'flex';
};
window.closeOfflineInfo = function() {
    document.getElementById('offline-modal').style.display = 'none';
};

// Queue progress function
window.queueOfflineProgress = function(quizData) {
    let queue = JSON.parse(localStorage.getItem('dtech_offline_queue') || '[]');
    queue.push(quizData);
    localStorage.setItem('dtech_offline_queue', JSON.stringify(queue));
};

// Compute local virtual XP from queue
function getLocalVirtualStats() {
    let queue = JSON.parse(localStorage.getItem('dtech_offline_queue') || '[]');
    let localXp = 0;
    let localPoints = 0;

    for (const item of queue) {
        if (item.url.includes('/api/submit-quiz')) {
            const percentage = (item.data.correct_answers / item.data.total_questions) * 100;
            if (percentage >= 50) {
                localXp += 50; // Approximated max for first try, UI read is approximate
                localPoints += 10;
            }
        } else if (item.url.includes('/api/submit-weekly-exam')) {
            const percentage = (item.data.correct_answers / item.data.total_questions) * 100;
            if (percentage >= 50) {
                localXp += 100;
                localPoints += 20;
            }
        } else if (item.url.includes('/api/store/sync-points')) {
            if (item.data.added_points) localPoints += item.data.added_points;
            if (item.data.push_claim) localPoints += 100;
        }
    }

    return { xp: localXp, points: localPoints };
}

// Helper to attempt caching once we know we're on Android
let isCachingInitiated = false;
function attemptCacheDatasets() {
    if (isCachingInitiated) return;

    const userGrade = localStorage.getItem('user_grade');
    // Only trigger dataset caching if it's the Android app and user is logged in
    if (window.IS_ANDROID_APP && userGrade) {
        const cacheKey = `dtech_datasets_cached_${userGrade}`;
        if (!localStorage.getItem(cacheKey)) {
            if (window.AndroidCacher) {
                isCachingInitiated = true;
                window.AndroidCacher.cacheGradeDatasets(userGrade);
            }
        }
    }
}

// Check for Android App Flag slightly delayed to let WebView finish loading interface
window.addEventListener('load', () => {
    setTimeout(() => {
        attemptCacheDatasets();
    }, 1000);
});

// Fallback listener for Android app detection (if called directly by WebView)
window.onAndroidAppDetected = function() {
    attemptCacheDatasets();
};

// Intercept fetch to mock backend responses when offline or batching in Android
const originalFetch = window.fetch;
window.fetch = async function(...args) {
    const url = typeof args[0] === 'string' ? args[0] : args[0].url;

    const isWrite = url.includes('/api/submit-quiz') || url.includes('/api/submit-weekly-exam') || url.includes('/api/store/sync-points');
    const isOfflineOrBatching = !navigator.onLine || window.IS_ANDROID_APP;

    if (isWrite && isOfflineOrBatching) {
        const options = args[1] || {};
        if (options.body) {
            const data = JSON.parse(options.body);
            window.queueOfflineProgress({ url: url, data: data });

            // Return fake success
            return new Response(JSON.stringify({
                success: true,
                message: "Progress saved locally.",
                xpEarned: 0,
                pointsEarned: 0,
                offline: true,
                batched: true
            }), { status: 200, headers: { 'Content-Type': 'application/json' } });
        }
    }

    // For reads, we intercept to append virtual local stats if available
    if (window.IS_ANDROID_APP && url.includes('/api/user/')) {
        try {
            const response = await originalFetch.apply(this, args);
            if (response.ok) {
                const data = await response.json();
                const virtualStats = getLocalVirtualStats();
                data.xp = (data.xp || 0) + virtualStats.xp;
                data.dtech_points = (data.dtech_points || 0) + virtualStats.points;
                data.level = Math.floor(data.xp / 100) + 1;
                // Note: rank cannot be easily simulated, we use server rank
                return new Response(JSON.stringify(data), { status: 200, headers: { 'Content-Type': 'application/json' } });
            }
        } catch (e) {
            // Fallback if truly offline
            if (!navigator.onLine) {
                const virtualStats = getLocalVirtualStats();
                return new Response(JSON.stringify({
                    xp: virtualStats.xp,
                    dtech_points: virtualStats.points,
                    rank: "Offline",
                    level: Math.floor(virtualStats.xp / 100) + 1,
                    username: "Offline User",
                    offline: true
                }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            }
        }
    }

    if (!navigator.onLine && url.includes('/api/user/')) {
         const virtualStats = getLocalVirtualStats();
         return new Response(JSON.stringify({
            xp: virtualStats.xp,
            dtech_points: virtualStats.points,
            rank: "Offline",
            level: Math.floor(virtualStats.xp / 100) + 1,
            username: "Offline User",
            offline: true
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }

    return originalFetch.apply(this, args);
};

// Standard offline sync for browsers
window.syncOfflineProgress = async function() {
    if (window.IS_ANDROID_APP) return; // Handled differently

    let queue = JSON.parse(localStorage.getItem('dtech_offline_queue') || '[]');
    if (queue.length === 0) return;

    for (let i = 0; i < queue.length; i++) {
        try {
            await originalFetch(queue[i].url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(queue[i].data)
            });
        } catch(e) {
            console.error('Failed to sync item:', e);
            queue = queue.slice(i);
            localStorage.setItem('dtech_offline_queue', JSON.stringify(queue));
            return;
        }
    }
    localStorage.removeItem('dtech_offline_queue');
};

let isSyncing = false;

// Android Batch Sync invoked by Back Button or onPause
window.triggerFinalSync = async function(closeApp = true) {
    if (!window.IS_ANDROID_APP) return;
    if (isSyncing) return;

    let queue = JSON.parse(localStorage.getItem('dtech_offline_queue') || '[]');
    if (queue.length === 0) {
        if (closeApp && window.AndroidExit) {
            window.AndroidExit.closeApp();
        }
        return;
    }

    const userId = localStorage.getItem('user_id');
    if (!userId) {
        localStorage.removeItem('dtech_offline_queue');
        if (closeApp && window.AndroidExit) {
            window.AndroidExit.closeApp();
        }
        return;
    }

    if (closeApp) {
        const overlay = document.getElementById('sync-overlay');
        if (overlay) overlay.style.display = 'flex';
    }

    isSyncing = true;
    try {
        const response = await originalFetch('/api/batch-sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, queue: queue })
        });
        if (response.ok) {
            // Success, clear queue
            localStorage.removeItem('dtech_offline_queue');
        } else {
            console.error('Batch sync responded with error status:', response.status);
        }
    } catch(e) {
        console.error('Failed batch sync:', e);
    } finally {
        isSyncing = false;
    }

    if (closeApp && window.AndroidExit) {
        window.AndroidExit.closeApp();
    }
};
