with open("quiz.html", "r") as f:
    quiz_content = f.read()

with open("weekly_quiz.html", "r") as f:
    weekly_content = f.read()

# Extract styles from quiz.html
import re
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
quiz_style = style_pattern.search(quiz_content).group(0)

# Extract scripts from quiz.html (specifically the hamburger menu logic and confetti)
# We will just manually merge the HTML structure and JS logic for the weekly quiz.
