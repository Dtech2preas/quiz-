import json
import random
import os
import itertools
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

        paper = "paper1" if "P1" in self.topic_prefix else "paper2"
        question_id = f"{self.topic_prefix}_{len(self.questions) + 1:03d}"

        q_dict = {
            "id": question_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "paper": paper,
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


def generic_generate(gen: TopicGenerator, data: list):
    # This takes a list of data definitions and tries to generate questions until full.
    # Data is a list of dicts:
    # { "subtopic": "...", "diff": "easy", "templates": [...], "facts": [{"term": "...", "desc": "...", "wrong": [...]}] }

    # Pre-calculate counts to optimize loop
    diffs = ["easy", "medium", "hard"]

    attempts = 0
    max_attempts = 50000

    while not gen.is_done() and attempts < max_attempts:
        attempts += 1
        # pick a random data block
        block = random.choice(data)

        subtopic = block["subtopic"]
        diff = block["diff"]

        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        template = random.choice(block["templates"])

        # some facts might be combinations
        if "fact_generator" in block:
            fact = block["fact_generator"]()
        else:
            fact = random.choice(block["facts"])

        q_text = template["q"].format(**fact)
        ans = str(fact["a"])

        wrongs = []
        if "w" in fact:
            wrongs.extend(fact["w"])

        # grab extra wrongs from other facts in the same block
        other_facts = [f for f in block.get("facts", []) if str(f.get("a")) != ans]
        random.shuffle(other_facts)
        for of in other_facts:
            wa = str(of.get("a"))
            if wa not in wrongs and wa != ans:
                wrongs.append(wa)

            # also pull from 'w' of other facts
            for w in of.get("w", []):
                if str(w) not in wrongs and str(w) != ans:
                    wrongs.append(str(w))

        # if we still need wrongs, use the block's default wrong pool
        if "wrong_pool" in block:
            pool = list(block["wrong_pool"])
            random.shuffle(pool)
            for w in pool:
                if w not in wrongs and w != ans:
                    wrongs.append(w)

        expl = template["e"].format(**fact) if "e" in template else f"{ans} is the correct answer."

        gen.add_question(subtopic, diff, q_text, ans, wrongs, expl)


# To make 1000 unique questions without too much repetitive code, we will generate combinations.
# For biology, we can mix sentence structures, specific traits, animals/plants, processes, etc.
# We will create a robust combinatorial generator using a python script that writes the data.
