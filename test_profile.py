import re

with open('profile.html', 'r') as f:
    content = f.read()

print("First nav found at:", content.find("<nav>"))
print("First nav context:")
print(content[content.find("<nav>") - 50 : content.find("<nav>") + 50])

print("First header found at:", content.find("<header>"))
