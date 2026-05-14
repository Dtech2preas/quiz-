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
    const progressBanner = document.getElementById('caching-progress-banner');
    const progressBar = document.getElementById('caching-progress-bar');
    const progressText = document.getElementById('caching-progress-text');

    if (progressBanner) progressBanner.style.display = 'block';

    const messageChannel = new MessageChannel();

    // Add a fallback timeout in case the service worker completely fails to respond
    let swTimeout = setTimeout(() => {
        console.error("Service worker caching timed out completely.");
        if (progressBanner) {
            if (progressText) progressText.innerText = 'Download timed out.';
            setTimeout(() => {
                progressBanner.style.display = 'none';
            }, 3000);
        }
    }, 60000); // 60 seconds total timeout for safety, gets cleared on success/error

    messageChannel.port1.onmessage = (event) => {
        if (event.data.status === 'progress') {
            const current = event.data.current;
            const total = event.data.total;
            const percentage = Math.round((current / total) * 100);
            if (progressBar) progressBar.style.width = percentage + '%';
            if (progressText) progressText.innerText = `${percentage}% - ${current} of ${total} files downloaded`;

            // Reset the timeout on each progress ping
            clearTimeout(swTimeout);
            swTimeout = setTimeout(() => {
                console.error("Service worker caching timed out during progress.");
                if (progressBanner) {
                    if (progressText) progressText.innerText = 'Download stalled and timed out.';
                    setTimeout(() => {
                        progressBanner.style.display = 'none';
                    }, 3000);
                }
            }, 15000); // 15 seconds without a progress update
        } else if (event.data.status === 'success') {
            clearTimeout(swTimeout);
            console.log('Datasets cached successfully!');
            localStorage.setItem(cacheKey, 'true');
            if (progressBanner) {
                if (progressText) progressText.innerText = 'Download complete!';
                if (progressBar) progressBar.style.width = '100%';
                setTimeout(() => {
                    progressBanner.style.display = 'none';
                }, 2000);
            }
        } else {
            clearTimeout(swTimeout);
            console.error('Failed to cache datasets:', event.data.error);
            if (progressBanner) {
                if (progressText) progressText.innerText = 'Download finished with some errors.';
                setTimeout(() => {
                    progressBanner.style.display = 'none';
                }, 3000);
            }
        }
    };

    if (navigator.serviceWorker) {
        if (navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage(
                { action: 'CACHE_GRADE_DATASETS', grade: grade },
                [messageChannel.port2]
            );
        } else {
            // Wait for the service worker to be ready and active
            navigator.serviceWorker.ready.then(registration => {
                if (registration.active) {
                    registration.active.postMessage(
                        { action: 'CACHE_GRADE_DATASETS', grade: grade },
                        [messageChannel.port2]
                    );
                } else {
                    clearTimeout(swTimeout);
                    if (progressBanner) {
                        if (progressText) progressText.innerText = 'Service Worker failed to activate.';
                        setTimeout(() => progressBanner.style.display = 'none', 3000);
                    }
                }
            }).catch(err => {
                clearTimeout(swTimeout);
                if (progressBanner) {
                    if (progressText) progressText.innerText = 'Service Worker error.';
                    setTimeout(() => progressBanner.style.display = 'none', 3000);
                }
            });
        }
    } else {
        clearTimeout(swTimeout);
        if (progressBanner) {
            if (progressText) progressText.innerText = 'Service Worker not supported.';
            setTimeout(() => progressBanner.style.display = 'none', 3000);
        }
    }
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
