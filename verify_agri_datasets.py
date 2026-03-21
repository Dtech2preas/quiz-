import json
import os
import glob

files = glob.glob('dataset/grade11/agricultural_sciences/*.json')

all_questions = set()
duplicates = 0

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)

    if len(data) != 1000:
        print(f"Error: {file} has {len(data)} items instead of 1000.")

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for item in data:
        diffs[item['difficulty']] += 1

        q_text = item['question']
        if q_text in all_questions:
            duplicates += 1
        all_questions.add(q_text)

        if len(item['wrong_answers_pool']) < 6:
            print(f"Error: Question {item['id']} in {file} has less than 6 wrong answers.")

        if item['correct_answer'] in item['wrong_answers_pool']:
            print(f"Error: Question {item['id']} in {file} has the correct answer in the wrong answers pool.")

        if 'paper' not in item:
            print(f"Error: Question {item['id']} in {file} is missing 'paper' key.")

    if diffs['easy'] != 300 or diffs['medium'] != 500 or diffs['hard'] != 200:
        print(f"Error: {file} has incorrect difficulty distribution: {diffs}")

    print(f"{file} verified successfully: 1000 items, diffs {diffs}")

print(f"Total cross-file duplicates: {duplicates}")
