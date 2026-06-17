import os
import re

def main():
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    for file in files:
        with open(file, 'r') as f:
            content = f.read()

        # Find "body {" or "body{" or "body {" or similar
        # Add "overflow-x: hidden;" if it does not already exist
        def replace_func(match):
            body_block = match.group(0)
            if "overflow-x" not in body_block:
                if "{" in body_block:
                    return body_block.replace("{", "{ overflow-x: hidden; ", 1)
            return body_block

        # Replace 'body {' and 'body{ '
        new_content = re.sub(r'body\s*{[^}]*}', replace_func, content)

        if new_content != content:
            with open(file, 'w') as f:
                f.write(new_content)
            print(f"Updated {file}")

if __name__ == '__main__':
    main()
