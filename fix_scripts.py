import os

html_files = [
    'dashboard.html',
    'leaderboard.html',
    'global_leaderboard.html'
]

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    if '<script src="update_timer.js"></script>' not in content:
        # Add script before the closing </head> or </body>
        content = content.replace('</head>', '<script src="update_timer.js"></script>\n</head>')

        with open(file, 'w') as f:
            f.write(content)
        print(f"Added update_timer.js script to {file}")
