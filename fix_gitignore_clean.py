with open('.gitignore', 'r') as f:
    content = f.read()

content = content.replace("android_app/local.propertiespdfs/", "android_app/local.properties\n")
# clean up duplicate pdfs/ and *.pdf
lines = content.split('\n')
unique_lines = []
for line in lines:
    if line not in unique_lines:
        unique_lines.append(line)

with open('.gitignore', 'w') as f:
    f.write('\n'.join(unique_lines))
