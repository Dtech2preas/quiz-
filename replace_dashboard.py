import os

file = 'dashboard.html'
with open(file, 'r') as f:
    content = f.read()

old_text = '<h2 id="welcome-message" style="margin: 0; margin-bottom: 0.5rem;">Welcome, User! <span id="user-grade-badge" style="font-size: 0.9rem; background: var(--accent-blue); color: white; padding: 0.2rem 0.6rem; border-radius: 12px; vertical-align: middle; margin-left: 0.5rem;"></span></h2>'

new_text = '<h2 id="welcome-message" style="margin: 0; margin-bottom: 0.2rem;">Welcome, User! <span id="user-grade-badge" style="font-size: 0.9rem; background: var(--accent-blue); color: white; padding: 0.2rem 0.6rem; border-radius: 12px; vertical-align: middle; margin-left: 0.5rem;"></span></h2>\n            <div class="global-update-timer" style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem;"></div>'

if old_text in content:
    content = content.replace(old_text, new_text)

    with open(file, 'w') as f:
        f.write(content)
    print("Replaced text in dashboard.html")
