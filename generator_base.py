import json
import random
import math
import os
import itertools
from typing import List, Dict, Any, Tuple

# We will need to define a base generator function/class to handle the 1000 limit, difficulty dist, uniqueness, etc.
class TopicGenerator:
    def __init__(self, topic_name: str, topic_prefix: str, subtopics: List[str]):
        self.topic_name = topic_name
        self.topic_prefix = topic_prefix
        self.subtopics = subtopics
        self.generated_questions = set()
        self.questions = []

        # Difficulties count:
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

        # Ensure correct answer is not in wrong answers
        wrong_answers = [str(w) for w in wrong_answers if str(w) != str(correct_answer)]

        # Deduplicate wrong answers
        unique_wrong_answers = []
        seen = set()
        for w in wrong_answers:
            if w not in seen:
                seen.add(w)
                unique_wrong_answers.append(w)

        # We need at least 6 wrong answers
        if len(unique_wrong_answers) < 6:
            # Generate more random ones or skip
            return False

        self.generated_questions.add(question)
        self.difficulty_counts[difficulty] += 1

        question_id = f"{self.topic_prefix}_{len(self.questions) + 1:03d}"

        q_dict = {
            "id": question_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": str(correct_answer),
            "wrong_answers_pool": unique_wrong_answers[:8],
            "explanation": explanation
        }
        self.questions.append(q_dict)
        return True

    def is_done(self):
        return len(self.questions) >= 1000

    def save_to_json(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.questions, f, indent=2)
