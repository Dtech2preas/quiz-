function getNextUpdateStr() {
    const now = new Date();
    // Minutes remaining until next 5-minute interval
    let minRemaining = 4 - (now.getMinutes() % 5);
    let secRemaining = 59 - now.getSeconds();

    // If perfectly aligned and somehow not returning instantly, or just crossed 0
    if (minRemaining < 0) {
        minRemaining = 4;
        secRemaining = 59;
    }

    if (minRemaining === 0 && secRemaining === 0) {
        return "Updating...";
    }

    return `${minRemaining}m ${secRemaining}s`;
}

function initGlobalUpdateTimer() {
    const timerElements = document.querySelectorAll('.global-update-timer');
    if (timerElements.length === 0) return;

    function updateTimers() {
        const timeStr = getNextUpdateStr();
        timerElements.forEach(el => {
            if (timeStr === "Updating...") {
                el.innerHTML = `<span style="color: var(--accent-yellow);">Updating...</span>`;
            } else {
                el.innerHTML = `Next update in: <span style="font-weight: bold; color: var(--text-main);">${timeStr}</span>`;
            }
        });
    }

    updateTimers();
    setInterval(updateTimers, 1000);
}

document.addEventListener('DOMContentLoaded', initGlobalUpdateTimer);
