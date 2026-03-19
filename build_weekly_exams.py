import json
import os
import random
import datetime

def load_json(filepath):
    try:
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def generate_weekly_exams():
    map_data = load_json('map.json')
    if not map_data:
        print("Could not load map.json")
        return

    # Calculate current week ISO standard "YYYY-Www"
    today = datetime.date.today()
    # Let's say we label the exam by the week number so it's consistent
    year, week, _ = today.isocalendar()
    exam_week_str = f"{year}-W{week:02d}"

    # We will build a weekly map registry
    weekly_map_path = 'dataset/weekly_quiz/weekly_map.json'
    weekly_map = load_json(weekly_map_path)
    if not weekly_map:
        weekly_map = {}

    if exam_week_str not in weekly_map:
        weekly_map[exam_week_str] = {}

    for grade, subjects in map_data.items():
        if grade not in weekly_map[exam_week_str]:
            weekly_map[exam_week_str][grade] = {}

        for subject, files in subjects.items():
            all_medium_questions = []
            all_hard_questions = []

            for file_entry in files:
                filepath = os.path.join('dataset', grade, subject, file_entry['file'])
                questions = load_json(filepath)
                if questions:
                    for q in questions:
                        if q.get('difficulty') == 'medium':
                            all_medium_questions.append(q)
                        elif q.get('difficulty') == 'hard':
                            all_hard_questions.append(q)

            exam_questions = []

            # Select Medium
            if len(all_medium_questions) >= 25:
                exam_questions.extend(random.sample(all_medium_questions, 25))
            else:
                exam_questions.extend(all_medium_questions)

            # Select Hard
            if len(all_hard_questions) >= 25:
                exam_questions.extend(random.sample(all_hard_questions, 25))
            else:
                exam_questions.extend(all_hard_questions)

            shortfall = 50 - len(exam_questions)
            if shortfall > 0:
                used_ids = {q.get('id', '') for q in exam_questions}
                remaining_pool = [q for q in all_medium_questions + all_hard_questions if q.get('id', '') not in used_ids]
                if len(remaining_pool) >= shortfall:
                    exam_questions.extend(random.sample(remaining_pool, shortfall))
                else:
                    exam_questions.extend(remaining_pool)

            random.shuffle(exam_questions)

            if len(exam_questions) > 0:
                exam_filename = f"{subject}_{exam_week_str}.json"
                exam_filepath = os.path.join('dataset', 'weekly_quiz', grade, exam_filename)

                # Assign sequential IDs to the selected questions for the exam context
                for i, q in enumerate(exam_questions):
                    q['exam_id'] = f"EXAM_{exam_week_str}_{grade}_{subject}_{i+1}"

                save_json(exam_filepath, exam_questions)

                weekly_map[exam_week_str][grade][subject] = {
                    "file": f"{grade}/{exam_filename}", # relative path from weekly_quiz
                    "label": f"{subject.replace('_', ' ').title()} Weekly Exam",
                    "total_questions": len(exam_questions)
                }

                print(f"Generated exam for {grade} - {subject} with {len(exam_questions)} questions.")

    save_json(weekly_map_path, weekly_map)
    print(f"Updated weekly map for {exam_week_str}")

if __name__ == "__main__":
    generate_weekly_exams()
