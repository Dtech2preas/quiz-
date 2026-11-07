import json
import os
import random
import time

def standardize_agrisci11_topic(filename, prefix, topic_name, paper, generator_func):
    t0 = time.time()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fpath = os.path.join(base_dir, filename)

    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Deduplicate and collect valid questions
    seen_texts = set()
    easy_q = []
    med_q = []
    hard_q = []

    # Gather a pool of distractors per subtopic
    subtopic_distractors = {}

    for q in data:
        sub = q.get("subtopic", topic_name)
        if sub not in subtopic_distractors:
            subtopic_distractors[sub] = set()

        corr = str(q.get("correct_answer", "")).strip()
        subtopic_distractors[sub].add(corr)
        for w in q.get("wrong_answers_pool", []):
            w_str = str(w).strip()
            if w_str and w_str != corr:
                subtopic_distractors[sub].add(w_str)

        q_text = q.get("question", "").strip()
        if q_text in seen_texts:
            continue
        seen_texts.add(q_text)

        d = q.get("difficulty", "medium").lower()
        if d == "easy":
            easy_q.append(q)
        elif d == "hard":
            hard_q.append(q)
        else:
            med_q.append(q)

    # Convert sets to lists
    for sub in subtopic_distractors:
        subtopic_distractors[sub] = list(subtopic_distractors[sub])

    targets = {"easy": 300, "medium": 500, "hard": 200}
    current = {"easy": easy_q, "medium": med_q, "hard": hard_q}

    # 2. Invoke generator_func to synthesize needed questions
    generator_func(current, targets, seen_texts, subtopic_distractors, prefix, topic_name, paper)

    # 3. Assemble and re-verify
    final_questions = []
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}

    for d in ["easy", "medium", "hard"]:
        selected = current[d][:targets[d]]
        diff_counts[d] = len(selected)
        final_questions.extend(selected)

    # Format IDs and tags
    for idx, q in enumerate(final_questions):
        q["id"] = f"{prefix}_{idx+1:04d}"
        q["paper"] = paper
        q["topic"] = topic_name
        d = q.get("difficulty", "medium").lower()
        sub = q.get("subtopic", topic_name)
        q["tags"] = {
            "grade": "11",
            "subject": "Agricultural Sciences",
            "paper": paper,
            "topic": topic_name,
            "subtopic": sub,
            "cognitive_level": "Knowledge" if d == "easy" else ("Application" if d == "medium" else "Analysis"),
            "difficulty": d
        }

    # Save to file
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(final_questions, f, indent=2, ensure_ascii=False)

    print(f"Standardized {len(final_questions)} Qs for Grade 11 Agricultural Sciences: {topic_name} ({diff_counts}) -> {filename} in {time.time()-t0:.2f}s")
    return final_questions
