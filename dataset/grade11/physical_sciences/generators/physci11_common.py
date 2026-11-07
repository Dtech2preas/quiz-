import json
import os
import time

def process_physci11_topic(filename, prefix, topic_name, paper):
    t0 = time.time()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fpath = os.path.join(base_dir, filename)

    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    seen = set()
    cleaned = []

    for q in data:
        q_text = q["question"].strip()
        if q_text in seen:
            continue
        seen.add(q_text)

        d = q.get("difficulty", "medium").lower()
        if d not in diffs:
            d = "medium"

        corr = str(q.get("correct_answer", "")).strip()
        wrongs = [str(w).strip() for w in q.get("wrong_answers_pool", []) if str(w).strip() != corr]

        uw = []
        w_seen = set()
        for w in wrongs:
            if w not in w_seen:
                w_seen.add(w)
                uw.append(w)

        if len(uw) < 6:
            continue

        diffs[d] += 1
        subtopic = q.get("subtopic", topic_name)
        q_dict = {
            "id": f"{prefix}_{len(cleaned)+1:03d}",
            "topic": topic_name,
            "subtopic": subtopic,
            "paper": paper,
            "difficulty": d,
            "question": q_text,
            "correct_answer": corr,
            "wrong_answers_pool": uw[:8],
            "explanation": q.get("explanation", f"The correct answer is {corr}.").strip(),
            "tags": q.get("tags") or {
                "grade": "11",
                "subject": "Physical Sciences",
                "paper": paper,
                "topic": topic_name,
                "subtopic": subtopic,
                "cognitive_level": "Knowledge" if d == "easy" else ("Application" if d == "medium" else "Analysis"),
                "difficulty": d
            }
        }
        cleaned.append(q_dict)

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(cleaned)} questions for Grade 11 Physical Sciences: {topic_name} ({diffs}) -> {filename} in {time.time()-t0:.2f}s")
    return cleaned
