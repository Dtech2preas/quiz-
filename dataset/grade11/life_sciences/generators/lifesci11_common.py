import json
import os
import time

class LifeSci11Generator:
    def __init__(self, filename, prefix, topic_name, paper):
        self.filename = filename
        self.prefix = prefix
        self.topic_name = topic_name
        self.paper = paper
        self.questions = []
        self.seen_texts = set()
        self.diff_counts = {"easy": 0, "medium": 0, "hard": 0}
        self.targets = {"easy": 300, "medium": 500, "hard": 200}
        self.start_time = time.time()

    def add_q(self, difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive=None):
        difficulty = difficulty.lower()
        if difficulty not in self.targets:
            difficulty = "medium"

        if self.diff_counts[difficulty] >= self.targets[difficulty]:
            return False

        q_clean = q_text.strip()
        if q_clean in self.seen_texts:
            return False

        corr_str = str(correct).strip()
        clean_wrongs = []
        w_seen = set()
        for w in wrongs:
            w_str = str(w).strip()
            if w_str and w_str != corr_str and w_str not in w_seen:
                w_seen.add(w_str)
                clean_wrongs.append(w_str)

        if len(clean_wrongs) < 6:
            return False

        if not cognitive:
            cognitive = "Knowledge" if difficulty == "easy" else ("Application" if difficulty == "medium" else "Analysis")

        self.seen_texts.add(q_clean)
        self.diff_counts[difficulty] += 1
        q_id = f"{self.prefix}_{len(self.questions)+1:04d}"

        self.questions.append({
            "id": q_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "paper": self.paper,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": corr_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "11",
                "subject": "Life Sciences",
                "paper": self.paper,
                "topic": self.topic_name,
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def is_done(self):
        return (self.diff_counts["easy"] >= self.targets["easy"] and
                self.diff_counts["medium"] >= self.targets["medium"] and
                self.diff_counts["hard"] >= self.targets["hard"])

    def save(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        fpath = os.path.join(base_dir, self.filename)
        assert self.diff_counts == self.targets, f"Target mismatch for {self.filename}: {self.diff_counts} vs {self.targets}"
        assert len(self.questions) == 1000, f"Expected 1000 questions, got {len(self.questions)}"

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)

        print(f"[{time.time()-self.start_time:.2f}s] Saved 1000 Qs for Grade 11 Life Sciences: {self.topic_name} ({self.diff_counts}) -> {self.filename}")
        return self.questions
