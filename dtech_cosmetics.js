// This script applies user themes across the site
(function() {
    function applyThemeAndFont() {
        const theme = localStorage.getItem('dtech_theme');
        const font = localStorage.getItem('dtech_font');

        const applyToBody = () => {
            // Remove previous
            document.body.className = Array.from(document.body.classList)
                .filter(c => !c.startsWith('theme_') && !c.startsWith('font_'))
                .join(' ');

            if (theme) document.body.classList.add(theme);
            if (font) document.body.classList.add(font);
        };

        if (document.body) {
            applyToBody();
        } else {
            window.addEventListener('DOMContentLoaded', applyToBody);
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

        /* Theme: Dark Mode */
        body.theme_dark {
            --bg-dark: #000000;
            --bg-card: #0a0a0a;
            --accent-blue: #444444;
            --border-color: #222222;
            --header-bg: #000000;
            --text-main: #e0e0e0;
            --text-muted: #888888;
        }
        body.theme_dark header { border-bottom: 1px solid #333333; }

        /* Theme: Forest */
        body.theme_forest {
            --bg-dark: #0d1a13;
            --bg-card: #142e1d;
            --accent-blue: #10b981;
            --border-color: #1b452b;
            --header-bg: #08120c;
        }
        body.theme_forest header { border-bottom: 2px solid #10b981; }

        /* Theme: Ocean */
        body.theme_ocean {
            --bg-dark: #081829;
            --bg-card: #112a4a;
            --accent-blue: #0891b2;
            --border-color: #1b4273;
            --header-bg: #05101c;
        }
        body.theme_ocean header { border-bottom: 2px solid #0891b2; }

        /* Theme: Sunset */
        body.theme_sunset {
            --bg-dark: #2c1011;
            --bg-card: #451a1a;
            --accent-blue: #f97316;
            --border-color: #6d2828;
            --header-bg: #1c0a0a;
        }
        body.theme_sunset header { border-bottom: 2px solid #f97316; }

        /* Custom Fonts */
        body.font_retro { font-family: 'Courier New', Courier, monospace; }
        body.font_handwriting { font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', cursive, sans-serif; }
        body.font_serif { font-family: 'Times New Roman', Times, serif; }

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
        .avatar-border-wrapper.border_fire { background: linear-gradient(180deg, #ef4444, #f97316, #facc15); box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); animation: firePulse 2s infinite; }
        .avatar-border-wrapper.border_cosmic { background: linear-gradient(135deg, #4c1d95, #c026d3, #1e3a8a); box-shadow: 0 0 15px rgba(192, 38, 211, 0.5); animation: cosmicRotate 4s linear infinite; }
        .avatar-border-wrapper.border_rainbow { background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); animation: rainbowShift 3s linear infinite; background-size: 200% 200%; }
        .avatar-border-wrapper.border_glitch { background: repeating-linear-gradient(45deg, #000, #000 5px, #10b981 5px, #10b981 10px); box-shadow: 2px 2px 0px #f43f5e, -2px -2px 0px #3b82f6; animation: glitchBorder 0.5s infinite; }

        @keyframes firePulse { 0% { box-shadow: 0 0 10px rgba(239,68,68,0.5); } 50% { box-shadow: 0 0 20px rgba(249,115,22,0.8); } 100% { box-shadow: 0 0 10px rgba(239,68,68,0.5); } }
        @keyframes cosmicRotate { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }
        @keyframes rainbowShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes glitchBorder { 0% { transform: translate(0); } 20% { transform: translate(-2px, 1px); } 40% { transform: translate(-1px, -1px); } 60% { transform: translate(2px, 1px); } 80% { transform: translate(1px, -1px); } 100% { transform: translate(0); } }

        /* Global Name Colors */
        .name_red { color: #ef4444 !important; font-weight: bold; }
        .name_blue { color: #3b82f6 !important; font-weight: bold; }
        .name_green { color: #10b981 !important; font-weight: bold; }
        .name_gold { color: #fbbf24 !important; font-weight: bold; text-shadow: 0 0 8px rgba(251, 191, 36, 0.6); }

        /* Global Profile Banners */
        .profile-banner-wrapper {
            width: 100%;
            height: 150px;
            background-color: var(--header-bg);
            border-bottom: 1px solid var(--border-color);
            background-size: cover;
            background-position: center;
            border-radius: 12px 12px 0 0;
            margin-bottom: -50px;
        }
        .profile-banner-wrapper.banner_cyber { background: linear-gradient(to right, #0f2027, #203a43, #2c5364); border-bottom: 2px solid #3b82f6; }
        .profile-banner-wrapper.banner_space { background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%); }
        .profile-banner-wrapper.banner_sunset { background: linear-gradient(to right, #ff512f, #f09819); }
    `;

    if (document.head) {
        document.head.appendChild(style);
    } else {
        window.addEventListener('DOMContentLoaded', () => {
            document.head.appendChild(style);
        });
    }

    // Apply theme on load
    applyThemeAndFont();

    // Re-fetch equipped items occasionally to sync localStorage
    const userId = localStorage.getItem("user_id");
    if (userId) {
        fetch(`https://billowing-hall-4748.nakiaklocko57.workers.dev/api/user/${userId}`)
            .then(res => res.json())
            .then(data => {
                if (data.equipped_cosmetics) {
                    if (data.equipped_cosmetics.theme) {
                        localStorage.setItem('dtech_theme', data.equipped_cosmetics.theme);
                    } else {
                        localStorage.removeItem('dtech_theme');
                    }
                    if (data.equipped_cosmetics.font) {
                        localStorage.setItem('dtech_font', data.equipped_cosmetics.font);
                    } else {
                        localStorage.removeItem('dtech_font');
                    }
                    // For quiz celebrations / certificates / banners, we can cache them globally too
                    if (data.equipped_cosmetics.quiz_celebration) {
                        localStorage.setItem('dtech_effect', data.equipped_cosmetics.quiz_celebration);
                    } else {
                        localStorage.removeItem('dtech_effect');
                    }
                    if (data.equipped_cosmetics.certificate_template) {
                        localStorage.setItem('dtech_cert', data.equipped_cosmetics.certificate_template);
                    } else {
                        localStorage.removeItem('dtech_cert');
                    }
                    if (data.equipped_cosmetics.profile_banner) {
                        localStorage.setItem('dtech_banner', data.equipped_cosmetics.profile_banner);
                    } else {
                        localStorage.removeItem('dtech_banner');
                    }
                    if (data.equipped_cosmetics.name_color) {
                        localStorage.setItem('dtech_name_color', data.equipped_cosmetics.name_color);
                    } else {
                        localStorage.removeItem('dtech_name_color');
                    }
                    applyThemeAndFont();
                }
            }).catch(e => console.error(e));
    }
})();
