import os

leaderboards = ['leaderboard.html']

old_text = """<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
                Live Updated: Just now"""

new_text = """<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
                Last updated<br><span class="global-update-timer" style="font-weight:normal;color:var(--text-muted);font-size:0.75rem;"></span>"""

for file in leaderboards:
    with open(file, 'r') as f:
        content = f.read()

    if "Live Updated: Just now" in content:
        content = content.replace(old_text, new_text)
        with open(file, 'w') as f:
            f.write(content)
        print(f"Replaced text in {file}")
