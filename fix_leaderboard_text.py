import os

with open('leaderboard.html', 'r') as f:
    content = f.read()

content = content.replace("Live Updated: Just now", """Last updated<br><span class="global-update-timer" style="font-weight:normal;color:var(--text-muted);font-size:0.75rem;"></span>""")

with open('leaderboard.html', 'w') as f:
    f.write(content)
