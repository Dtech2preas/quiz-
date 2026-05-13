// This script applies user themes across the site
(function() {
    function applyThemeAndFont() {
        const theme = localStorage.getItem('dtech_theme');
        const font = localStorage.getItem('dtech_font');

        const ultimateProfile = localStorage.getItem('dtech_ultimate_profile');
        const ultimateGlobal = localStorage.getItem('dtech_ultimate_global');

        const isProfilePage = window.location.pathname.includes('profile.html') || window.location.pathname.includes('public_profile.html');

        const applyToBody = () => {
            // Check if we're viewing someone else's ultimate profile
            const isViewingSomeoneElsesUltimate = document.body.classList.contains('viewing-ultimate-profile');

            // Retain the ultimate viewing flag if it's there
            document.body.className = Array.from(document.body.classList)
                .filter(c => (!c.startsWith('theme_') && !c.startsWith('font_') && !c.startsWith('ultimate_')) || c === 'viewing-ultimate-profile' || (document.body.classList.contains('viewing-ultimate-profile') && c.startsWith('ultimate_')))
                .join(' ');

            // If public_profile.html applied its own ultimate theme from the API, DO NOT OVERRIDE with viewer's local storage
            if (isViewingSomeoneElsesUltimate && isProfilePage) {
                return;
            }

            let ultimateApplied = false;

            if (ultimateGlobal) {
                document.body.classList.add(ultimateGlobal);
                ultimateApplied = true;
            } else if (ultimateProfile && isProfilePage) {
                document.body.classList.add(ultimateProfile);
                ultimateApplied = true;
            }

            // If an ultimate theme is applied locally, it overrides standard themes and fonts
            if (!ultimateApplied) {
                if (theme) document.body.classList.add(theme);
                if (font) document.body.classList.add(font);
            }
        };

        if (document.body) {
            applyToBody();
        } else {
            window.addEventListener('DOMContentLoaded', applyToBody);
        }

        // Setup observer so if public_profile.html dynamically adds the viewing-ultimate-profile flag later, we rerun
        window.addEventListener('DOMContentLoaded', () => {
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.attributeName === 'class') {
                        if (document.body.classList.contains('viewing-ultimate-profile') && !document.body.dataset.ultimateProcessed) {
                            document.body.dataset.ultimateProcessed = 'true';
                            applyToBody();
                        }
                    }
                });
            });
            if (document.body) {
                observer.observe(document.body, { attributes: true });
            }
        });
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
            display: inline-flex;
            position: relative;
            border-radius: 50%;
            padding: 6px;
            z-index: 1;
        }

        /* Inner overlay to ensure avatar image sits above the border effects */
        .avatar-border-wrapper > img, .avatar-border-wrapper > div {
            z-index: 2;
            position: relative;
        }

        /* Gold Aura */
        .avatar-border-wrapper.border_gold {
            background: linear-gradient(135deg, #fbbf24, #b45309, #fde047, #b45309);
            background-size: 300% 300%;
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.6), inset 0 0 15px rgba(251, 191, 36, 0.4);
            animation: gradientMove 4s ease infinite;
        }
        .avatar-border-wrapper.border_gold::before {
            content: ''; position: absolute; top: -4px; left: -4px; right: -4px; bottom: -4px;
            border-radius: 50%; border: 2px dashed rgba(251, 191, 36, 0.8);
            animation: cosmicRotate 10s linear infinite; z-index: -1;
        }

        /* Diamond Aura */
        .avatar-border-wrapper.border_diamond {
            background: linear-gradient(135deg, #60a5fa, #3b82f6, #93c5fd, #2563eb);
            background-size: 300% 300%;
            box-shadow: 0 0 25px rgba(96, 165, 250, 0.7), inset 0 0 20px rgba(96, 165, 250, 0.5);
            animation: gradientMove 3s ease infinite;
        }
        .avatar-border-wrapper.border_diamond::before {
            content: ''; position: absolute; top: -6px; left: -6px; right: -6px; bottom: -6px;
            border-radius: 50%;
            background: conic-gradient(from 0deg, transparent, rgba(96, 165, 250, 0.8), transparent 30%);
            animation: cosmicRotate 2s linear infinite; z-index: -1;
        }

        /* Fire Border */
        .avatar-border-wrapper.border_fire {
            background: #ef4444;
            box-shadow: 0 0 20px #ef4444, 0 0 40px #f97316, inset 0 0 20px #facc15;
            animation: firePulse 1.5s infinite alternate;
        }
        .avatar-border-wrapper.border_fire::before {
            content: ''; position: absolute; top: -8px; left: -8px; right: -8px; bottom: -8px;
            border-radius: 50%;
            background: radial-gradient(circle, transparent 40%, rgba(239, 68, 68, 0.4) 60%, transparent 80%);
            animation: fireRing 2s infinite linear; z-index: -1;
        }

        /* Neon Aura */
        .avatar-border-wrapper.border_neon {
            background: linear-gradient(135deg, #f472b6, #db2777);
            box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #f472b6, 0 0 40px #db2777, 0 0 50px #db2777, 0 0 60px #db2777;
            animation: neonFlicker 2s infinite alternate;
        }

        /* Cosmic Border */
        .avatar-border-wrapper.border_cosmic {
            background: linear-gradient(135deg, #4c1d95, #c026d3, #1e3a8a, #4c1d95);
            background-size: 400% 400%;
            box-shadow: 0 0 30px rgba(192, 38, 211, 0.8), inset 0 0 20px rgba(30, 58, 138, 0.8);
            animation: gradientMove 5s ease infinite;
        }
        .avatar-border-wrapper.border_cosmic::before, .avatar-border-wrapper.border_cosmic::after {
            content: ''; position: absolute; border-radius: 50%; z-index: -1;
            background: conic-gradient(from 0deg, transparent, rgba(192, 38, 211, 0.8) 10%, transparent 40%);
        }
        .avatar-border-wrapper.border_cosmic::before {
            top: -5px; left: -5px; right: -5px; bottom: -5px; animation: cosmicRotate 3s linear infinite;
        }
        .avatar-border-wrapper.border_cosmic::after {
            top: -10px; left: -10px; right: -10px; bottom: -10px; animation: cosmicRotate 5s linear infinite reverse;
        }

        /* Rainbow Border */
        .avatar-border-wrapper.border_rainbow {
            background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3, #ff0000);
            background-size: 400% 400%;
            box-shadow: 0 0 25px rgba(255, 255, 255, 0.6);
            animation: rainbowShift 4s linear infinite;
        }
        .avatar-border-wrapper.border_rainbow::before {
            content: ''; position: absolute; top: -6px; left: -6px; right: -6px; bottom: -6px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3, #ff0000);
            background-size: 400% 400%;
            filter: blur(8px);
            animation: rainbowShift 4s linear infinite; z-index: -1;
        }

        /* Glitch Border */
        .avatar-border-wrapper.border_glitch {
            background: #000;
            box-shadow: 4px 4px 0px rgba(244, 63, 94, 0.8), -4px -4px 0px rgba(59, 130, 246, 0.8);
            animation: glitchBorder 0.2s infinite;
        }
        .avatar-border-wrapper.border_glitch::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 50%;
            box-shadow: inset 0 0 15px #10b981;
            background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(16, 185, 129, 0.5) 5px, rgba(16, 185, 129, 0.5) 10px);
            z-index: 1; pointer-events: none;
            mix-blend-mode: overlay;
        }

        @keyframes firePulse { 0% { box-shadow: 0 0 20px #ef4444, 0 0 30px #f97316; transform: scale(1); } 100% { box-shadow: 0 0 30px #ef4444, 0 0 50px #facc15, 0 0 10px #facc15 inset; transform: scale(1.02); } }
        @keyframes fireRing { 0% { transform: scale(0.8) rotate(0deg); opacity: 1; } 100% { transform: scale(1.3) rotate(180deg); opacity: 0; } }
        @keyframes cosmicRotate { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes gradientMove { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes rainbowShift { 0% { background-position: 0% 50%; } 100% { background-position: 100% 50%; } }
        @keyframes neonFlicker { 0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #f472b6, 0 0 40px #db2777, 0 0 50px #db2777; } 20%, 24%, 55% { box-shadow: none; } }
        @keyframes glitchBorder {
            0% { transform: translate(0); box-shadow: 4px 4px 0px rgba(244, 63, 94, 0.8), -4px -4px 0px rgba(59, 130, 246, 0.8); }
            20% { transform: translate(-3px, 2px); box-shadow: -4px 4px 0px rgba(244, 63, 94, 0.8), 4px -4px 0px rgba(59, 130, 246, 0.8); }
            40% { transform: translate(-2px, -2px); box-shadow: 4px -4px 0px rgba(244, 63, 94, 0.8), -4px 4px 0px rgba(59, 130, 246, 0.8); }
            60% { transform: translate(3px, 2px); box-shadow: -4px -4px 0px rgba(244, 63, 94, 0.8), 4px 4px 0px rgba(59, 130, 246, 0.8); }
            80% { transform: translate(2px, -2px); box-shadow: 4px 4px 0px rgba(244, 63, 94, 0.8), -4px -4px 0px rgba(59, 130, 246, 0.8); }
            100% { transform: translate(0); box-shadow: 4px 4px 0px rgba(244, 63, 94, 0.8), -4px -4px 0px rgba(59, 130, 246, 0.8); }
        }

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
            position: relative;
            overflow: hidden;
        }

        /* Cyberpunk Banner */
        .profile-banner-wrapper.banner_cyber {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            border-bottom: 2px solid #3b82f6;
            box-shadow: inset 0 -10px 20px rgba(59, 130, 246, 0.5);
        }
        .profile-banner-wrapper.banner_cyber::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(to right, transparent, rgba(59, 130, 246, 0.2), transparent);
            transform: skewX(-20deg); animation: cyberSweep 3s infinite linear;
        }
        .profile-banner-wrapper.banner_cyber::after {
            content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, #f472b6, #3b82f6, #10b981);
            background-size: 200% 200%; animation: rainbowShift 2s linear infinite;
        }

        /* Deep Space Banner */
        .profile-banner-wrapper.banner_space {
            background: radial-gradient(circle at bottom, #1b2735 0%, #090a0f 100%);
            border-bottom: 2px solid #c026d3;
        }
        .profile-banner-wrapper.banner_space::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background-image: radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 4px),
                              radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 3px),
                              radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 4px),
                              radial-gradient(rgba(255,255,255,.4), rgba(255,255,255,.1) 2px, transparent 3px);
            background-size: 550px 550px, 350px 350px, 250px 250px, 150px 150px;
            background-position: 0 0, 40px 60px, 130px 270px, 70px 100px;
            animation: spaceDrift 60s linear infinite;
            opacity: 0.8;
        }

        /* Sunset Mountains Banner */
        .profile-banner-wrapper.banner_sunset {
            background: linear-gradient(to right, #ff512f, #f09819);
            border-bottom: 2px solid #facc15;
            background-size: 200% 200%;
            animation: gradientMove 5s ease infinite;
        }
        .profile-banner-wrapper.banner_sunset::before {
            content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 60%;
            background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);
        }
        .profile-banner-wrapper.banner_sunset::after {
            content: ''; position: absolute; top: 20%; right: 10%; width: 60px; height: 60px;
            background: #fef08a; border-radius: 50%;
            box-shadow: 0 0 40px #facc15, 0 0 80px #f97316;
            animation: sunPulse 4s infinite alternate;
        }

        @keyframes cyberSweep { 0% { left: -100%; } 100% { left: 200%; } }
        @keyframes spaceDrift { 0% { background-position: 0 0, 40px 60px, 130px 270px, 70px 100px; } 100% { background-position: 550px 550px, 390px 410px, 380px 520px, 220px 250px; } }
        @keyframes sunPulse { 0% { transform: scale(1); box-shadow: 0 0 20px #facc15, 0 0 40px #f97316; } 100% { transform: scale(1.1); box-shadow: 0 0 40px #facc15, 0 0 80px #f97316; } }

        /* ========================================================== */
        /* ULTIMATE PREMIUM PROFILES (GLOBAL AND PROFILE OVERHAULS)     */
        /* ========================================================== */

        /* 1. God Tier / Ascended */
        body.ultimate_god {
            background: linear-gradient(135deg, #2a1f0c, #1f1805);
            background-size: 200% 200%;
            animation: godBgShift 15s ease infinite;
            color: #fff8e7;
            font-family: 'Cinzel', 'Georgia', serif;
        }
        body.ultimate_god::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at 50% 10%, rgba(255, 215, 0, 0.25) 0%, transparent 70%);
            pointer-events: none;
            z-index: 9998;
            mix-blend-mode: screen;
            animation: godPulse 4s ease-in-out infinite alternate;
        }
        body.ultimate_god .container {
            background: rgba(30, 25, 15, 0.85);
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 50px rgba(255, 215, 0, 0.2), inset 0 0 20px rgba(255, 215, 0, 0.1);
            border: 2px solid rgba(255, 215, 0, 0.5);
            border-radius: 24px;
            position: relative;
        }
        body.ultimate_god .profile-header {
            background: linear-gradient(to bottom, rgba(255, 215, 0, 0.1), transparent);
            border-bottom: 1px solid rgba(255, 215, 0, 0.3);
            position: relative;
            overflow: visible;
        }
        body.ultimate_god .avatar-wrapper {
            box-shadow: 0 0 60px rgba(255, 215, 0, 0.8), inset 0 0 20px rgba(255, 255, 255, 0.5);
            border: 4px solid #ffd700;
            transform: scale(1.15);
            animation: floatGod 4s ease-in-out infinite;
            background: linear-gradient(45deg, #ffd700, #ffdf00, #d4af37);
            padding: 4px;
        }
        body.ultimate_god .avatar-wrapper img {
            border-radius: 50%;
            border: 2px solid #2a1f0c;
        }
        body.ultimate_god .avatar-wrapper::after {
            content: '🌟'; position: absolute; top: -15px; right: -15px; font-size: 2.5rem; animation: starTwinkleGod 2s infinite alternate; text-shadow: 0 0 20px #ffd700;
        }
        body.ultimate_god h1, body.ultimate_god h2, body.ultimate_god h3 {
            background: linear-gradient(to right, #ffd700, #ffdf00, #fff, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }
        body.ultimate_god .btn {
            background: linear-gradient(45deg, #d4af37, #ffd700, #ffdf00);
            color: #2a1f0c;
            font-weight: bold;
            border: 1px solid #fff;
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.6);
            border-radius: 30px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        body.ultimate_god .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(255, 215, 0, 0.8);
        }

        @keyframes godBgShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes godPulse { 0% { opacity: 0.5; transform: scale(1); } 100% { opacity: 0.8; transform: scale(1.05); } }
        @keyframes floatGod { 0%, 100% { transform: translateY(0) scale(1.15); } 50% { transform: translateY(-15px) scale(1.15); } }
        @keyframes starTwinkleGod { 0% { transform: scale(0.8) rotate(0deg); opacity: 0.6; } 100% { transform: scale(1.2) rotate(15deg); opacity: 1; } }
        @keyframes starTwinkle { 0% { opacity: 0.5; transform: scale(0.8) rotate(0deg); } 100% { opacity: 1; transform: scale(1.2) rotate(20deg); } }


        /* 2. Hacker / Terminal */
        body.ultimate_hacker {
            background: #000;
            color: #10b981;
            font-family: 'Courier New', Courier, monospace;
        }
        body.ultimate_hacker::before {
            content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(16, 185, 129, 0.1) 2px, rgba(16, 185, 129, 0.1) 4px);
            pointer-events: none; z-index: 9998;
        }
        body.ultimate_hacker .container { background: #050505; border: 1px solid #10b981; box-shadow: inset 0 0 20px rgba(16, 185, 129, 0.2); border-radius: 0; }
        body.ultimate_hacker .profile-header { background: #000; border-bottom: 1px dashed #10b981; }
        body.ultimate_hacker .avatar-wrapper { border-radius: 0; border: 2px solid #10b981; background: #000; box-shadow: 4px 4px 0 rgba(16, 185, 129, 0.5); }
        body.ultimate_hacker h1::before { content: '> root@dtech:~$ '; color: #34d399; }
        body.ultimate_hacker .btn { background: transparent; color: #10b981; border: 1px solid #10b981; border-radius: 0; text-transform: uppercase; }
        body.ultimate_hacker .btn:hover { background: #10b981; color: #000; }
        body.ultimate_hacker .stat-card { border: 1px dashed #059669; background: #000; }


        /* 3. RPG Hero Status */
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        body.ultimate_rpg {
            background: #1e1b4b;
            color: #e2e8f0;
            font-family: 'Press Start 2P', monospace;
            font-size: 0.8rem;
        }
        body.ultimate_rpg .container {
            background: #312e81;
            border: 4px solid #fcd34d;
            box-shadow: 4px 4px 0 #000, -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000;
            border-radius: 0;
            margin-top: 3rem;
        }
        body.ultimate_rpg .profile-header { background: #1e1b4b; border-bottom: 4px solid #fcd34d; }
        body.ultimate_rpg .avatar-wrapper { border-radius: 0; border: 4px solid #fcd34d; box-shadow: 4px 4px 0 #000; image-rendering: pixelated; }
        body.ultimate_rpg h1, body.ultimate_rpg h2, body.ultimate_rpg h3 { color: #fcd34d; text-shadow: 2px 2px #000; line-height: 1.5; }
        body.ultimate_rpg .btn { background: #ef4444; color: white; border: 4px solid #fca5a5; border-right-color: #991b1b; border-bottom-color: #991b1b; border-radius: 0; box-shadow: 2px 2px 0 #000; }
        body.ultimate_rpg .btn:active { border-top-color: #991b1b; border-left-color: #991b1b; border-right-color: #fca5a5; border-bottom-color: #fca5a5; }
        body.ultimate_rpg .stat-card { border: 2px solid #cbd5e1; background: #475569; }
        body.ultimate_rpg .profile-stats .stat-card::before { content: 'HP '; color: #ef4444; }


        /* 4. Cyberpunk Overdrive */
        body.ultimate_cyberpunk {
            background: #09090b;
            color: #f4f4f5;
            font-family: 'Arial', sans-serif;
            text-transform: uppercase;
        }
        body.ultimate_cyberpunk::after {
            content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 2px, 3px 100%; pointer-events: none; z-index: 9999;
        }
        body.ultimate_cyberpunk .container { background: linear-gradient(135deg, #18181b 0%, #0f172a 100%); border-top: 4px solid #06b6d4; border-bottom: 4px solid #ec4899; clip-path: polygon(0 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%); border-radius: 0; }
        body.ultimate_cyberpunk .profile-header { background: transparent; border-bottom: 2px solid #3f3f46; position: relative; }
        body.ultimate_cyberpunk .profile-header::before { content: 'SYS.ACTIVE'; position: absolute; top: 10px; right: 10px; color: #ec4899; font-size: 0.7rem; letter-spacing: 2px; }
        body.ultimate_cyberpunk .avatar-wrapper { border-radius: 0; border: 2px solid #06b6d4; background: #000; box-shadow: -5px 5px 0 #ec4899; clip-path: polygon(20% 0%, 100% 0, 100% 80%, 80% 100%, 0 100%, 0% 20%); }
        body.ultimate_cyberpunk h1, body.ultimate_cyberpunk h2, body.ultimate_cyberpunk h3 { color: #fef08a; text-shadow: 2px 0px #ec4899, -2px 0px #06b6d4; letter-spacing: 1px; }
        body.ultimate_cyberpunk .btn { background: #fef08a; color: #000; border: none; font-weight: bold; border-radius: 0; clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); box-shadow: inset -2px -2px 0px rgba(0,0,0,0.5); }
        body.ultimate_cyberpunk .btn:hover { background: #06b6d4; color: #fff; text-shadow: 1px 1px #000; }
        body.ultimate_cyberpunk .stat-card { background: #18181b; border: 1px solid #3f3f46; border-left: 4px solid #06b6d4; }

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

                    if (data.equipped_cosmetics.ultimate_profile) {
                        localStorage.setItem('dtech_ultimate_profile', data.equipped_cosmetics.ultimate_profile);
                    } else {
                        localStorage.removeItem('dtech_ultimate_profile');
                    }
                    if (data.equipped_cosmetics.ultimate_global) {
                        localStorage.setItem('dtech_ultimate_global', data.equipped_cosmetics.ultimate_global);
                    } else {
                        localStorage.removeItem('dtech_ultimate_global');
                    }

                    applyThemeAndFont();
                }
            }).catch(e => console.error(e));
    }
})();
