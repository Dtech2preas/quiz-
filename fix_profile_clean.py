with open('profile.html', 'r') as f:
    content = f.read()

bad_snippet = """<h2>Settings</h2>
        <div></div>
        <div></div>
        <div></div>
    </div>"""
good_snippet = """<h2>Settings</h2>"""
content = content.replace(bad_snippet, good_snippet)

with open('profile.html', 'w') as f:
    f.write(content)
