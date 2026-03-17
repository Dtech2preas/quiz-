import re

with open('profile.html', 'r') as f:
    content = f.read()

# Make sure HTML is there
if '<div class="hamburger">' not in content:
    # Find nav in header
    nav_match = re.search(r'\s*<nav>', content)
    if nav_match:
        hamburger_html = """    <div class="hamburger">
        <div></div>
        <div></div>
        <div></div>
    </div>\n"""
        content = content[:nav_match.start()] + hamburger_html + content[nav_match.start():]

with open('profile.html', 'w') as f:
    f.write(content)
print("Done")
