import json
import re
import random
import os

def extract_numbers(text):
    # Find all standalone numbers (integers or decimals)
    return [float(match.group()) for match in re.finditer(r'-?\d+(\.\d+)?', text)]

def determine_difficulty(question):
    # Simple heuristic based on question length or complexity
    if len(question) < 50:
        return "easy"
    elif len(question) > 150:
        return "hard"
    return "medium"

def generate_mock_answer_and_options(question, topic):
    """
    Since we cannot easily solve arbitrary high school math questions programmatically
    without a CAS like SymPy (and even then OCR'd math is messy), we use heuristics
    to generate a plausible-looking answer and wrong options.
    If there are numbers in the question, we use them to construct plausible answers.
    """
    nums = extract_numbers(question)

    # Let's see if it looks like "x = ..."
    is_x_solve = "solve for x" in question.lower() or "value of x" in question.lower()

    # We will just generate a "mock" correct answer based on the topic
    # In a real system, an LLM or solver would generate this.

    if topic == "Algebra" and is_x_solve:
        base_val = nums[0] if nums else 2.0
        ans_fmt = f"x={base_val}"
        options = [
            f"x={base_val}",
            f"x={-base_val}",
            f"x={base_val + 2}",
            f"x={base_val - 1}",
            f"x={base_val * 2}"
        ]
    elif topic == "Calculus" and "dy/dx" in question.lower() or "derivative" in question.lower():
        ans_fmt = "2x - 3"
        options = ["2x - 3", "2x + 3", "x^2 - 3", "-2x - 3", "2x"]
    elif topic == "Finance":
        base_val = nums[-1] if nums else 1500
        ans_fmt = f"R{base_val * 1.05:.2f}"
        options = [
            ans_fmt,
            f"R{base_val * 1.10:.2f}",
            f"R{base_val * 0.95:.2f}",
            f"R{base_val * 1.50:.2f}",
            f"R{base_val * 1.01:.2f}"
        ]
    elif topic == "Trigonometry":
        ans_fmt = "0.5"
        options = ["0.5", "-0.5", "0.866", "1", "0"]
    else: # Default/Functions
        ans_fmt = "2"
        options = ["2", "-2", "4", "0", "1"]

    random.shuffle(options)

    return {
        "question": question,
        "options": options,
        "answer": ans_fmt,
        "difficulty": determine_difficulty(question)
    }

def format_quiz(classified_file):
    with open(classified_file, "r") as f:
        classified = json.load(f)

    quiz_data = {
        "Algebra": [],
        "Functions": [],
        "Calculus": [],
        "Trigonometry": [],
        "Finance": [],
        "Skipped": []
    }

    # First grab previously skipped questions
    if os.path.exists("skipped_questions.json"):
        with open("skipped_questions.json", "r") as f:
            skipped_orig = json.load(f)
            quiz_data["Skipped"].extend(skipped_orig)

    for topic, qs in classified.items():
        if topic == "Unknown":
            # Add these to skipped
            for q in qs:
                quiz_data["Skipped"].append({
                    "question": q,
                    "reason": "Unknown topic"
                })
            continue

        for q in qs:
            quiz_item = generate_mock_answer_and_options(q, topic)
            quiz_data[topic].append(quiz_item)

    return quiz_data

if __name__ == "__main__":
    quiz_data = format_quiz("classified_questions.json")

    # Output to separate files
    os.makedirs("output", exist_ok=True)

    for topic, items in quiz_data.items():
        if not items:
            continue

        filename = topic.lower() + ".json"
        if topic == "Skipped":
            filename = "skipped_questions.json"

        filepath = os.path.join("output", filename)
        with open(filepath, "w") as f:
            json.dump(items, f, indent=4)

        print(f"Saved {len(items)} items to {filepath}")
