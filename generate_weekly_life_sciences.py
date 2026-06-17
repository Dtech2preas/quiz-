import json
import random
import os
import datetime

def load_json(filepath):
    try:
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return None

map_data = load_json("map.json")

weekly_map_path = "dataset/weekly_quiz/weekly_map.json"
weekly_map = load_json(weekly_map_path)

files = map_data["grade12"]["life_sciences"]

for week in weekly_map:
    if "grade12" not in weekly_map[week]:
        weekly_map[week]["grade12"] = {}

    all_medium_questions = []
    all_hard_questions = []

    for f_entry in files:
        filepath = os.path.join("dataset", "grade12", "life_sciences", f_entry["file"])
        questions = load_json(filepath)
        if questions:
            for q in questions:
                if q.get("difficulty") == "medium":
                    all_medium_questions.append(q)
                elif q.get("difficulty") == "hard":
                    all_hard_questions.append(q)

    exam_questions = []
    if len(all_medium_questions) >= 25:
        exam_questions.extend(random.sample(all_medium_questions, 25))
    else:
        exam_questions.extend(all_medium_questions)

    if len(all_hard_questions) >= 25:
        exam_questions.extend(random.sample(all_hard_questions, 25))
    else:
        exam_questions.extend(all_hard_questions)

    shortfall = 50 - len(exam_questions)
    if shortfall > 0:
        used_ids = {q.get("id", "") for q in exam_questions}
        remaining_pool = [q for q in all_medium_questions + all_hard_questions if q.get("id", "") not in used_ids]
        if len(remaining_pool) >= shortfall:
            exam_questions.extend(random.sample(remaining_pool, shortfall))
        else:
            exam_questions.extend(remaining_pool)

    random.shuffle(exam_questions)

    if len(exam_questions) > 0:
        exam_key = "life_sciences"
        exam_filename = f"{exam_key}_{week}.json"
        exam_filepath = os.path.join("dataset", "weekly_quiz", "grade12", exam_filename)

        for i, q in enumerate(exam_questions):
            q["exam_id"] = f"EXAM_{week}_grade12_{exam_key}_{i+1}"

        os.makedirs(os.path.dirname(exam_filepath), exist_ok=True)
        with open(exam_filepath, "w", encoding="utf-8") as f:
            json.dump(exam_questions, f, indent=2)

        weekly_map[week]["grade12"][exam_key] = {
            "file": f"grade12/{exam_filename}",
            "label": "Life Sciences Weekly Exam",
            "total_questions": len(exam_questions)
        }

with open(weekly_map_path, "w", encoding="utf-8") as f:
    json.dump(weekly_map, f, indent=2)
