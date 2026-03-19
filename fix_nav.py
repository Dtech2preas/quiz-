import glob
import re

files = glob.glob("*.html")

NAV_HTML = """    <nav id="nav-menu">
        <a href="dashboard.html">Dashboard</a>
        <a href="subjects.html">Take a Quiz</a>
        <a href="weekly_quiz.html">Weekly Exam</a>
        <a href="leaderboard.html">Grade Leaderboards</a>
        <a href="global_leaderboard.html">Global Leaderboard</a>
        <a href="stats.html">Detailed Stats</a>
        <a href="profile.html">Profile</a>
        <a href="index.html" onclick="localStorage.clear()">Logout</a>
    </nav>"""

NAV_QUIZ_HTML = """    <nav id="nav-menu">
        <a href="dashboard.html">Dashboard</a>
        <a href="subjects.html">Exit Quiz</a>
        <a href="weekly_quiz.html">Weekly Exam</a>
        <a href="leaderboard.html">Grade Leaderboards</a>
        <a href="global_leaderboard.html">Global Leaderboard</a>
        <a href="stats.html">Detailed Stats</a>
        <a href="profile.html">Profile</a>
        <a href="index.html" onclick="localStorage.clear()">Logout</a>
    </nav>"""

for file in files:
    # Skip index.html and signup.html as they don't have the logged-in nav menu
    if file in ["index.html", "signup.html", "test.html"]:
        continue

    with open(file, "r") as f:
        content = f.read()

    # The regex looks for <nav id="nav-menu">... anything ...</nav>
    nav_pattern = re.compile(r'<nav id="nav-menu">.*?</nav>', re.DOTALL)

    if file in ["quiz.html", "weekly_quiz.html"]:
        new_content = nav_pattern.sub(NAV_QUIZ_HTML, content)
    else:
        new_content = nav_pattern.sub(NAV_HTML, content)

    # Some files like dashboard.html might have a standalone Logout button right after Global Leaderboard.
    # The regex above replaces the entire nav, so if they had an extra <button> for logout inside the nav,
    # it gets replaced by the standard <a href="index.html">Logout</a> which is fine and standardizes it.

    if content != new_content:
        with open(file, "w") as f:
            f.write(new_content)
        print(f"Updated {file}")
