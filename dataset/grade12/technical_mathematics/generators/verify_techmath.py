import json
import os
import sys

def audit_file(filepath):
    if not os.path.exists(filepath):
        print(f"FAIL: File not found: {filepath}")
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    total = len(data)
    if total != 1000:
        print(f"FAIL {filepath}: total is {total}, expected 1000")
        return False
        
    diffs = {"easy": 0, "medium": 0, "hard": 0}
    seen = set()
    errors = []
    
    for idx, q in enumerate(data):
        qid = q.get("id", f"idx_{idx}")
        diff = q.get("difficulty")
        if diff in diffs:
            diffs[diff] += 1
        else:
            errors.append(f"{qid}: invalid difficulty '{diff}'")
            
        qtext = q.get("question", "").strip()
        if not qtext:
            errors.append(f"{qid}: empty question text")
        elif qtext in seen:
            errors.append(f"{qid}: duplicate question '{qtext[:40]}...'")
        seen.add(qtext)
        
        c_ans = str(q.get("correct_answer", "")).strip()
        if not c_ans:
            errors.append(f"{qid}: empty correct answer")
            
        wrongs = q.get("wrong_answers_pool", [])
        if len(wrongs) < 6:
            errors.append(f"{qid}: only {len(wrongs)} distractors (minimum 6 required)")
        if c_ans in wrongs:
            errors.append(f"{qid}: correct answer '{c_ans}' appears in wrong_answers_pool")
            
        for tag in ["[Case", "(Variant", "[Exam Question"]:
            if tag in qtext:
                errors.append(f"{qid}: contains synthetic tag '{tag}'")
                
        exp = q.get("explanation", "").strip()
        if len(exp) < 15:
            errors.append(f"{qid}: explanation too short ({len(exp)} chars)")
            
        tags = q.get("tags", {})
        if tags and tags.get("subject") != "Technical Mathematics":
            errors.append(f"{qid}: tags.subject is '{tags.get('subject')}', expected 'Technical Mathematics'")
            
    if diffs != {"easy": 300, "medium": 500, "hard": 200}:
        errors.append(f"Difficulty counts {diffs} do not match {{easy: 300, medium: 500, hard: 200}}")
        
    if errors:
        print(f"FAIL {filepath}: {len(errors)} errors found (showing first 5):")
        for err in errors[:5]:
            print(f"  - {err}")
        return False
        
    print(f"PASS {filepath}: 1000 Qs (300 Easy, 500 Medium, 200 Hard), 0 duplicates, >=6 distractors, 0 tags, 100% explanations.")
    return True

if __name__ == "__main__":
    target_files = [
        "dataset/grade12/technical_mathematics/paper1_tech_algebra.json",
        "dataset/grade12/technical_mathematics/paper1_tech_functions.json",
        "dataset/grade12/technical_mathematics/paper1_tech_finance.json",
        "dataset/grade12/technical_mathematics/paper1_tech_calculus.json",
        "dataset/grade12/technical_mathematics/paper2_tech_analytical.json",
        "dataset/grade12/technical_mathematics/paper2_tech_trig.json",
        "dataset/grade12/technical_mathematics/paper2_tech_circle_angular.json",
        "dataset/grade12/technical_mathematics/paper2_tech_mensuration.json"
    ]
    if len(sys.argv) > 1:
        target_files = sys.argv[1:]
        
    all_ok = True
    for tf in target_files:
        ok = audit_file(tf)
        if not ok:
            all_ok = False
            
    if all_ok:
        print("\nALL CHECKED DATASETS PASS THE DBE EXAM STANDARD AUDIT!")
    else:
        print("\nSOME DATASETS FAILED AUDIT.")
        sys.exit(1)
