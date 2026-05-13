// offline_mode.js - Handles offline detection, caching logic, and UI adjustments

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

    // Inject loading overlay for caching
    const loadingHtml = `
        <div id="caching-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg-dark, #1a202c); z-index: 10001; justify-content: center; align-items: center; flex-direction: column;">
            <div class="spinner" style="border: 4px solid rgba(255,255,255,0.1); width: 40px; height: 40px; border-radius: 50%; border-left-color: #fbbf24; animation: spin 1s linear infinite; margin-bottom: 20px;"></div>
            <h2 style="color: #fff; margin: 0;">Setting up offline database...</h2>
            <p style="color: #a0aec0;">Please wait while we download your grade's materials.</p>
        </div>
        <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
    `;
    document.body.insertAdjacentHTML('beforeend', loadingHtml);

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
            syncOfflineProgress();
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

// Queue progress function (to be called by quiz.html when offline)
window.queueOfflineProgress = function(quizData) {
    let queue = JSON.parse(localStorage.getItem('dtech_offline_queue') || '[]');
    queue.push(quizData);
    localStorage.setItem('dtech_offline_queue', JSON.stringify(queue));
};



// Service Worker Registration and Caching Logic
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(registration => {
            console.log('ServiceWorker registered:', registration.scope);

            // Wait to ensure window.IS_ANDROID_APP is set by Android App onPageFinished
            setTimeout(() => {
                const userGrade = localStorage.getItem('user_grade');
                // Only trigger dataset caching if it's the Android app and user is logged in
                if (window.IS_ANDROID_APP && userGrade) {
                    const cacheKey = `dtech_datasets_cached_${userGrade}`;
                    if (!localStorage.getItem(cacheKey)) {
                        cacheGradeDatasets(userGrade, cacheKey);
                    }
                }
            }, 1000);

        }).catch(err => {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}

function cacheGradeDatasets(grade, cacheKey) {
    const overlay = document.getElementById('caching-overlay');
    if (overlay) overlay.style.display = 'flex';

    const messageChannel = new MessageChannel();
    messageChannel.port1.onmessage = (event) => {
        if (event.data.status === 'success') {
            console.log('Datasets cached successfully!');
            localStorage.setItem(cacheKey, 'true');
        } else {
            console.error('Failed to cache datasets:', event.data.error);
        }
        if (overlay) overlay.style.display = 'none';
    };

    navigator.serviceWorker.controller.postMessage(
        { action: 'CACHE_GRADE_DATASETS', grade: grade },
        [messageChannel.port2]
    );
}

// Fallback listener for Android app detection (if called directly by WebView)
window.onAndroidAppDetected = function() {
    const userGrade = localStorage.getItem('user_grade');
    if (userGrade && navigator.serviceWorker && navigator.serviceWorker.controller) {
        const cacheKey = `dtech_datasets_cached_${userGrade}`;
        if (!localStorage.getItem(cacheKey)) {
            cacheGradeDatasets(userGrade, cacheKey);
        }
    }
};

// Intercept fetch to mock backend responses when offline
const originalFetch = window.fetch;
window.fetch = async function(...args) {
    if (!navigator.onLine) {
        const url = typeof args[0] === 'string' ? args[0] : args[0].url;

        // Mock submit-quiz
        if (url.includes('/api/submit-quiz') || url.includes('/api/submit-weekly-exam')) {
            const options = args[1] || {};
            if (options.body) {
                const data = JSON.parse(options.body);
                window.queueOfflineProgress({ url: url, data: data });
                return new Response(JSON.stringify({
                    success: true,
                    message: "Offline: Progress saved locally.",
                    xpEarned: 0,
                    pointsEarned: 0,
                    offline: true
                }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            }
        }

        // Mock user stats fetch
        if (url.includes('/api/user/')) {
            return new Response(JSON.stringify({
                xp: 0,
                dtech_points: 0,
                rank: "Offline",
                level: 1,
                username: "Offline User",
                offline: true
            }), { status: 200, headers: { 'Content-Type': 'application/json' } });
        }
    }

    return originalFetch.apply(this, args);
};

// Update sync to use the mocked queue format
window.syncOfflineProgress = async function() {
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
