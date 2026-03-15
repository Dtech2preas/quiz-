import re

with open("full_ocr_text.txt", "r") as f:
    text = f.read()

# Extract questions. Let's look for numbers like "1.1", "1.1.1", etc.
questions = []
lines = text.split('\n')
current_q = ""

for line in lines:
    line = line.strip()
    # match pattern like 1.1, 1.1.1, 2.1 etc. at start of line
    if re.match(r'^\d+\.\d+(\.\d+)?\s+', line):
        if current_q:
            questions.append(current_q.strip())
        current_q = line
    elif current_q and line:
        current_q += " " + line

if current_q:
    questions.append(current_q.strip())

for i, q in enumerate(questions[:20]):
    print(f"--- Q{i+1} ---")
    print(q)
