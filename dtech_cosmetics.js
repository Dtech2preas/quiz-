// This script applies user themes across the site
(function() {
    function applyTheme() {
        const theme = localStorage.getItem('dtech_theme');
        if (theme) {
            document.body.classList.add(theme);
        }
    }

    // Define the theme styles dynamically or via injected stylesheet
    const style = document.createElement('style');
    style.innerHTML = `
        /* Theme: Gold */
        body.theme_gold {
            --bg-dark: #1f1b0f;
            --bg-card: #2e2615;
            --accent-blue: #fbbf24;
            --border-color: #52421a;
            --header-bg: #17130a;
        }
        body.theme_gold header { border-bottom: 2px solid #fbbf24; }

        /* Theme: Diamond */
        body.theme_diamond {
            --bg-dark: #0f172a;
            --bg-card: #141e33;
            --accent-blue: #60a5fa;
            --border-color: #23385e;
            --header-bg: #0b1120;
        }
        body.theme_diamond header { border-bottom: 2px solid #60a5fa; }

        /* Theme: Neon */
        body.theme_neon {
            --bg-dark: #120914;
            --bg-card: #1f1024;
            --accent-blue: #f472b6;
            --border-color: #4a1d41;
            --header-bg: #0d060e;
        }
        body.theme_neon header { border-bottom: 2px solid #f472b6; text-shadow: 0 0 10px #f472b6; }
        body.theme_neon .rank-card, body.theme_neon .stat-card { box-shadow: 0 0 10px rgba(244, 114, 182, 0.2); }

        /* Global Profile Avatar Borders */
        .avatar-border-wrapper {
            display: inline-block;
            position: relative;
            border-radius: 50%;
            padding: 4px;
        }
        .avatar-border-wrapper.border_gold { background: linear-gradient(135deg, #fbbf24, #b45309); box-shadow: 0 0 15px rgba(251, 191, 36, 0.5); }
        .avatar-border-wrapper.border_diamond { background: linear-gradient(135deg, #60a5fa, #3b82f6); box-shadow: 0 0 15px rgba(96, 165, 250, 0.5); }
        .avatar-border-wrapper.border_neon { background: linear-gradient(135deg, #f472b6, #db2777); box-shadow: 0 0 15px rgba(244, 114, 182, 0.5); }
    `;
    document.head.appendChild(style);

    // Apply theme on load
    applyTheme();

    // Re-fetch equipped items occasionally to sync localStorage
    const userId = localStorage.getItem("user_id");
    if (userId && window.location.pathname.includes('dashboard.html')) {
        fetch(\`https://billowing-hall-4748.nakiaklocko57.workers.dev/api/user/\${userId}\`)
            .then(res => res.json())
            .then(data => {
                if (data.equipped_cosmetics && data.equipped_cosmetics.theme) {
                    localStorage.setItem('dtech_theme', data.equipped_cosmetics.theme);
                    document.body.className = '';
                    document.body.classList.add(data.equipped_cosmetics.theme);
                } else {
                    localStorage.removeItem('dtech_theme');
                    document.body.className = '';
                }
            }).catch(e => console.error(e));
    }
})();
