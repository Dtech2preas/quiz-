import json
import random
import math
import sympy as sp
from typing import List

class TopicGenerator:
    def __init__(self, topic_name: str, topic_prefix: str, subtopics: List[str]):
        self.topic_name = topic_name
        self.topic_prefix = topic_prefix
        self.subtopics = subtopics
        self.generated_questions = set()
        self.questions = []

        self.difficulty_targets = {
            "easy": 300,
            "medium": 500,
            "hard": 200
        }
        self.difficulty_counts = {
            "easy": 0,
            "medium": 0,
            "hard": 0
        }

    def add_question(self, subtopic: str, difficulty: str, question: str, correct_answer: str, wrong_answers: List[str], explanation: str):
        if self.difficulty_counts[difficulty] >= self.difficulty_targets[difficulty]:
            return False

        if question in self.generated_questions:
            return False

        correct_str = str(correct_answer)
        wrong_answers = [str(w) for w in wrong_answers if str(w) != correct_str]

        unique_wrong_answers = []
        seen = set()
        for w in wrong_answers:
            if w not in seen:
                seen.add(w)
                unique_wrong_answers.append(w)

        if len(unique_wrong_answers) < 6:
            return False

        self.generated_questions.add(question)

        question_id = f"{self.topic_prefix}_{len(self.questions) + 1:03d}"

        q_dict = {
            "id": question_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": correct_str,
            "wrong_answers_pool": unique_wrong_answers[:8],
            "explanation": explanation
        }
        self.questions.append(q_dict)
        self.difficulty_counts[difficulty] += 1
        return True

    def is_done(self):
        return len(self.questions) >= 1000

    def save_to_json(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)

def get_wrong_ints(correct_val: int, count=8) -> List[str]:
    wrongs = set()
    wrongs.add(-correct_val)
    wrongs.add(correct_val + 1)
    wrongs.add(correct_val - 1)
    wrongs.add(correct_val * 2)
    wrongs.add(int(correct_val / 2))
    wrongs.add(correct_val + 2)
    wrongs.add(correct_val - 2)
    wrongs.add(correct_val * 3)

    attempts = 0
    while len(wrongs) < count + 5 and attempts < 100:
        offset = random.randint(-20, 20)
        if offset != 0:
            wrongs.add(correct_val + offset)
        attempts += 1

    res = [str(x) for x in wrongs if x != correct_val]
    return res[:count]

def get_wrong_floats(correct_val: float, count=8, decimals=2) -> List[str]:
    wrongs = set()
    wrongs.add(round(-correct_val, decimals))
    wrongs.add(round(correct_val + 1, decimals))
    wrongs.add(round(correct_val - 1, decimals))
    wrongs.add(round(correct_val * 1.5, decimals))
    wrongs.add(round(correct_val * 0.5, decimals))
    wrongs.add(round(correct_val * 2, decimals))
    if correct_val != 0:
        wrongs.add(round(1/correct_val, decimals))

    attempts = 0
    while len(wrongs) < count + 5 and attempts < 100:
        offset = random.uniform(-20, 20)
        wrongs.add(round(correct_val + offset, decimals))
        attempts += 1

    res = [f"{x:.{decimals}f}" for x in wrongs if abs(x - correct_val) > 1e-9]
    return res[:count]

def get_wrong_exprs(correct_expr: sp.Expr, count=8) -> List[str]:
    x = list(correct_expr.free_symbols)[0] if correct_expr.free_symbols else sp.Symbol('x')
    wrongs = set()
    wrongs.add(-correct_expr)
    wrongs.add(correct_expr * 2)
    wrongs.add(correct_expr + 1)
    wrongs.add(correct_expr - 1)
    wrongs.add(correct_expr + x)
    wrongs.add(correct_expr - x)
    try:
        wrongs.add(sp.diff(correct_expr, x))
    except:
        pass

    res = []
    for w in wrongs:
        if w != correct_expr:
            res.append(sp.latex(w))

    attempts = 0
    while len(res) < count and attempts < 100:
        offset = random.choice([2, 3, 4, 5, x, 2*x, x**2])
        sign = random.choice([1, -1])
        new_expr = correct_expr + sign * offset
        new_latex = sp.latex(new_expr)
        if new_latex not in res and sp.simplify(new_expr - correct_expr) != 0:
            res.append(new_latex)
        attempts += 1

    return res[:count]
