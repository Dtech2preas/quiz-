import json
import os
import time

def process_techsci_topic(filename, prefix, topic_name):
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
        
        d = q.get("difficulty", "medium")
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
        q_dict = {
            "id": f"{prefix}_{len(cleaned)+1:04d}",
            "topic": topic_name,
            "question": q_text,
            "correct_answer": corr,
            "wrong_answers_pool": uw[:8],
            "explanation": q.get("explanation", "").strip(),
            "difficulty": d,
            "tags": q.get("tags", {
                "Grade": "12",
                "Subject": "Technical Sciences",
                "CAPS Topic": topic_name,
                "Difficulty": d
            })
        }
        cleaned.append(q_dict)
        
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
        
    print(f"Generated {len(cleaned)} questions for {topic_name} ({diffs}) -> {filename} in {time.time()-t0:.2f}s")
    return cleaned
