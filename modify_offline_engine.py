import sys

with open('offline_engine.js', 'r') as f:
    content = f.read()

# We need to add the UI injection and event listeners
ui_injection = """
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
"""

if "function initOfflineUI()" not in content:
    content += "\n" + ui_injection

with open('offline_engine.js', 'w') as f:
    f.write(content)
