import re

with open('profile.html', 'r') as f:
    content = f.read()

# Add HTML (Search explicitly for the nav in the header, not any nav)
header_idx = content.find("<header>")
nav_in_header_idx = content.find("<nav>", header_idx)

if nav_in_header_idx != -1 and 'class="hamburger"' not in content:
    hamburger_html = """<div class="hamburger">
        <div></div>
        <div></div>
        <div></div>
    </div>\n    """
    content = content[:nav_in_header_idx] + hamburger_html + content[nav_in_header_idx:]

with open('profile.html', 'w') as f:
    f.write(content)
