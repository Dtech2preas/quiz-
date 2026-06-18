import json
import glob
import os

def main():
    files = glob.glob("dataset/grade12/life_sciences/grade12_life_sciences_*.json")
    if not files:
        print("No files found!")
        return

    all_passed = True

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        topic = os.path.basename(file).replace("grade12_life_sciences_", "").replace(".json", "")
        print(f"--- Checking {topic} ---")

        if len(data) != 1000:
            print(f"FAIL: Expected 1000 questions, got {len(data)}")
            all_passed = False
        else:
            print(f"PASS: 1000 questions")

        seen_questions = set()
        duplicates = 0
        for q in data:
            q_text = q["question"]
            if q_text in seen_questions:
                duplicates += 1
            seen_questions.add(q_text)

        if duplicates > 0:
            print(f"FAIL: Found {duplicates} duplicate questions")
            all_passed = False
        else:
            print(f"PASS: 0 duplicates")

        diffs = {"easy": 0, "medium": 0, "hard": 0}
        for q in data:
            diffs[q["difficulty"]] += 1

        if diffs["easy"] != 300 or diffs["medium"] != 500 or diffs["hard"] != 200:
            print(f"FAIL: Distribution is incorrect: {diffs}")
            all_passed = False
        else:
            print(f"PASS: 30/50/20 distribution")

        bad_wrong_answers = sum(1 for q in data if len(q["wrong_answers_pool"]) < 6)
        if bad_wrong_answers > 0:
            print(f"FAIL: {bad_wrong_answers} questions have fewer than 6 wrong answers")
            all_passed = False
        else:
            print(f"PASS: Wrong answers length")

    if all_passed:
        print("\nALL CHECKS PASSED.")
    else:
        print("\nSOME CHECKS FAILED.")

if __name__ == "__main__":
    main()
