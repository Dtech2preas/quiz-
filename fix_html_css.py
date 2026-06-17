import os
import re

def main():
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    for file in files:
        with open(file, 'r') as f:
            content = f.read()

        def replace_html_body_func(match):
            block = match.group(0)
            if "overflow-x" not in block:
                if "{" in block:
                    return block.replace("{", "{ overflow-x: hidden; ", 1)
            return block

        new_content = re.sub(r'html\s*,\s*body\s*{[^}]*}', replace_html_body_func, content)

        if new_content != content:
            with open(file, 'w') as f:
                f.write(new_content)
            print(f"Updated html, body css in {file}")

if __name__ == '__main__':
    main()
