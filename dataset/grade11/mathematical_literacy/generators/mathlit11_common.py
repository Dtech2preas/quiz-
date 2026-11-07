import json
import os
import sys
import time

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

def run_mathlit11_generator(gen_func, filename, prefix, topic_name, paper):
    t0 = time.time()
    generator = gen_func()
    questions = generator.questions

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fpath = os.path.join(base_dir, filename)

    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    standardized = []

    for idx, q in enumerate(questions):
        diff = q.get("difficulty", "medium").lower()
        if diff in diff_counts:
            diff_counts[diff] += 1
        subtopic = q.get("subtopic", topic_name)
        corr = str(q.get("correct_answer", "")).strip()
        wrongs = [str(w).strip() for w in q.get("wrong_answers_pool", []) if str(w).strip() != corr]

        q_dict = {
            "id": f"{prefix}_{idx+1:04d}",
            "topic": topic_name,
            "subtopic": subtopic,
            "paper": paper,
            "difficulty": diff,
            "question": q["question"].strip(),
            "correct_answer": corr,
            "wrong_answers_pool": wrongs[:8],
            "explanation": q.get("explanation", f"The correct answer is {corr}.").strip(),
            "tags": {
                "grade": "11",
                "subject": "Mathematical Literacy",
                "paper": paper,
                "topic": topic_name,
                "subtopic": subtopic,
                "cognitive_level": "Knowledge" if diff == "easy" else ("Application" if diff == "medium" else "Analysis"),
                "difficulty": diff
            }
        }
        standardized.append(q_dict)

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(standardized, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(standardized)} Qs for Grade 11 Mathematical Literacy: {topic_name} ({diff_counts}) -> {filename} in {time.time()-t0:.2f}s")
    return standardized
