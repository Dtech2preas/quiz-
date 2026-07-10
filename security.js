// security.js
// Provides client-side protections for quiz content.

(function() {
    // Determine if we are on a protected page
    const pathname = window.location.pathname;
    const isProtectedPage = pathname.includes('quiz.html') ||
                            pathname.includes('weekly_quiz.html') ||
                            pathname.includes('test_run_quiz.html');

    if (!isProtectedPage) return;

    // --- LEVEL 1: Block interactions (Text selection, copy, right click, drag-drop) ---

    // Disable right-click / context menu
    document.addEventListener('contextmenu', event => event.preventDefault());

    // Disable copying, cutting, pasting
    document.addEventListener('copy', event => event.preventDefault());
    document.addEventListener('cut', event => event.preventDefault());
    document.addEventListener('paste', event => event.preventDefault());

    // Disable drag and drop
    document.addEventListener('dragstart', event => event.preventDefault());
    document.addEventListener('drop', event => event.preventDefault());

    // Inject CSS to disable text selection and add watermark
    const style = document.createElement('style');
    style.innerHTML = `
        /* Disable text selection */
        * {
            -webkit-user-select: none !important; /* Safari */
            -moz-user-select: none !important; /* Firefox */
            -ms-user-select: none !important; /* IE10+/Edge */
            user-select: none !important; /* Standard */
            -webkit-touch-callout: none !important; /* iOS Safari */
        }

        /* Ensure inputs still work */
        input, textarea {
            -webkit-user-select: auto !important;
            -moz-user-select: auto !important;
            -ms-user-select: auto !important;
            user-select: auto !important;
        }

        /* Watermark overlay */
        .security-watermark {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none; /* Let clicks pass through */
            z-index: 9999;
            opacity: 0.05;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-content: center;
            overflow: hidden;
            transform: rotate(-30deg) scale(2);
        }

        .security-watermark-text {
            font-size: 2rem;
            color: #000;
            font-weight: bold;
            margin: 20px 50px;
            white-space: nowrap;
        }

        /* Warning modal */
        #security-warning-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.8);
            z-index: 10000;
            justify-content: center;
            align-items: center;
        }
        #security-warning-modal .modal-content {
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            max-width: 400px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        #security-warning-modal h2 { margin-top: 0; color: #d32f2f; }
        #security-warning-modal button {
            margin-top: 20px;
            padding: 10px 20px;
            background: #1976d2;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
        }
    `;
    document.head.appendChild(style);

    // --- Add Watermark dynamically ---
    window.addEventListener('load', () => {
        let watermarkString = "D-TECH";
        try {
            // Try to get user details from local storage or memory
            const userProfile = JSON.parse(localStorage.getItem('user_profile'));
            if (userProfile && userProfile.username) {
                watermarkString = `${userProfile.username} - ${userProfile.userId || ''}`;
            } else {
                const userId = localStorage.getItem('userId');
                if (userId) watermarkString = `User: ${userId}`;
            }
        } catch (e) {
            console.warn("Could not retrieve user info for watermark.");
        }

        const watermarkDiv = document.createElement('div');
        watermarkDiv.className = 'security-watermark';

        // Tile the text a bit
        for (let i = 0; i < 30; i++) {
            const span = document.createElement('span');
            span.className = 'security-watermark-text';
            span.innerText = watermarkString;
            watermarkDiv.appendChild(span);
        }
        document.body.appendChild(watermarkDiv);

        // Add warning modal to DOM
        const warningModal = document.createElement('div');
        warningModal.id = 'security-warning-modal';
        warningModal.innerHTML = `
            <div class="modal-content">
                <h2>Warning</h2>
                <p>Please stay in the quiz. Leaving the app repeatedly may reduce your rewards.</p>
                <button id="security-warning-close">Understood</button>
            </div>
        `;
        document.body.appendChild(warningModal);

        document.getElementById('security-warning-close').addEventListener('click', () => {
            warningModal.style.display = 'none';
        });
    });

    // --- LEVEL 4: Detect app switching (Visibility API) ---
    // Track how many times user leaves the page
    let leaveCount = parseInt(sessionStorage.getItem('securityLeaveCount') || '0', 10);

    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            leaveCount++;
            sessionStorage.setItem('securityLeaveCount', leaveCount);

            // If they leave more than 3 times, show warning when they return
        } else {
            if (leaveCount > 3) {
                const modal = document.getElementById('security-warning-modal');
                if (modal) {
                    modal.style.display = 'flex';
                }
                // Reset count after warning?
                leaveCount = 0;
                sessionStorage.setItem('securityLeaveCount', leaveCount);
            }
        }
    });

    // --- LEVEL 5: Browser protection (Disable DevTools shortcuts) ---
    document.addEventListener('keydown', (event) => {
        // F12
        if (event.key === 'F12' || event.keyCode === 123) {
            event.preventDefault();
        }
        // Ctrl+Shift+I / Cmd+Option+I (DevTools)
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && (event.key === 'I' || event.key === 'i')) {
            event.preventDefault();
        }
        // Ctrl+Shift+J / Cmd+Option+J (Console)
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && (event.key === 'J' || event.key === 'j')) {
            event.preventDefault();
        }
        // Ctrl+U / Cmd+Option+U (View Source)
        if ((event.ctrlKey || event.metaKey) && (event.key === 'U' || event.key === 'u')) {
            event.preventDefault();
        }
        // Ctrl+S / Cmd+S (Save Page)
        if ((event.ctrlKey || event.metaKey) && (event.key === 'S' || event.key === 's')) {
            event.preventDefault();
        }
        // Ctrl+P / Cmd+P (Print Page)
        if ((event.ctrlKey || event.metaKey) && (event.key === 'P' || event.key === 'p')) {
            event.preventDefault();
        }
    });

})();
