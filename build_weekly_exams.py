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
            paper1_files = []
            paper2_files = []
            unclassified_files = []

            for file_entry in files:
                text_to_check = (file_entry['file'] + " " + file_entry['label']).lower()
                is_paper1 = 'paper 1' in text_to_check or 'paper_1' in text_to_check or 'paper1' in text_to_check
                is_paper2 = 'paper 2' in text_to_check or 'paper_2' in text_to_check or 'paper2' in text_to_check

                if is_paper1:
                    paper1_files.append(file_entry)
                elif is_paper2:
                    paper2_files.append(file_entry)
                else:
                    unclassified_files.append(file_entry)

            def build_exam_for_files(exam_files, paper_suffix="", label_suffix=""):
                if not exam_files:
                    return

                all_medium_questions = []
                all_hard_questions = []

                for f_entry in exam_files:
                    filepath = os.path.join('dataset', grade, subject, f_entry['file'])
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
                    exam_key = subject
                    if paper_suffix:
                        exam_key = f"{subject}_{paper_suffix}"

                    exam_filename = f"{exam_key}_{exam_week_str}.json"
                    exam_filepath = os.path.join('dataset', 'weekly_quiz', grade, exam_filename)

                    # Assign sequential IDs to the selected questions for the exam context
                    for i, q in enumerate(exam_questions):
                        q['exam_id'] = f"EXAM_{exam_week_str}_{grade}_{exam_key}_{i+1}"

                    save_json(exam_filepath, exam_questions)

                    subject_title = subject.replace('_', ' ').title()
                    exam_label = f"{subject_title} Weekly Exam"
                    if label_suffix:
                        exam_label = f"{subject_title} {label_suffix} Weekly Exam"

                    weekly_map[exam_week_str][grade][exam_key] = {
                        "file": f"{grade}/{exam_filename}", # relative path from weekly_quiz
                        "label": exam_label,
                        "total_questions": len(exam_questions)
                    }

                    print(f"Generated exam for {grade} - {exam_key} with {len(exam_questions)} questions.")

            if len(paper1_files) > 0 or len(paper2_files) > 0:
                if len(paper1_files) > 0:
                    build_exam_for_files(paper1_files, "paper1", "Paper 1")
                if len(paper2_files) > 0:
                    build_exam_for_files(paper2_files, "paper2", "Paper 2")
            else:
                build_exam_for_files(unclassified_files)

    save_json(weekly_map_path, weekly_map)
    print(f"Updated weekly map for {exam_week_str}")

if __name__ == "__main__":
    generate_weekly_exams()
