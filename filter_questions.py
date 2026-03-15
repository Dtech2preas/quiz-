import json

SKIP_PHRASES = [
    "show that",
    "prove",
    "explain",
    "justify",
    "draw",
    "sketch",
    "write a paragraph",
    "hence deduce"
]

def should_skip(question_text):
    if len(question_text) > 350:
        return True, "Length > 350 characters"

    q_lower = question_text.lower()
    for phrase in SKIP_PHRASES:
        if phrase in q_lower:
            return True, f"Contains skipped phrase: '{phrase}'"

    return False, ""

def filter_questions(questions):
    usable = []
    skipped = []

    for q in questions:
        skip, reason = should_skip(q)
        if skip:
            skipped.append({
                "question": q,
                "reason": reason
            })
        else:
            usable.append(q)

    return usable, skipped

if __name__ == "__main__":
    with open("parsed_questions.json", "r") as f:
        questions = json.load(f)

    usable, skipped = filter_questions(questions)

    print(f"Total: {len(questions)}")
    print(f"Usable: {len(usable)}")
    print(f"Skipped: {len(skipped)}")

    with open("usable_questions.json", "w") as f:
        json.dump(usable, f, indent=4)

    with open("skipped_questions.json", "w") as f:
        json.dump(skipped, f, indent=4)
