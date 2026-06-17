import json
import random
import os

class UniversalGenerator:
    def __init__(self, output_dir, file_prefix, topic_title, subtopics, concepts, difficulty_distribution, templates, distractors_pool, contexts, svg_templates=None):
        self.output_dir = output_dir
        self.file_prefix = file_prefix
        self.title = topic_title
        self.subtopics = subtopics
        self.concepts = concepts
        self.difficulty_distribution = difficulty_distribution
        self.templates = templates
        self.distractors_pool = distractors_pool
        self.contexts = contexts
        self.svg_templates = svg_templates if svg_templates else []
        self.questions = []
        self.seen_questions = set()

        self.target_counts = {
            diff: int(1000 * prop) for diff, prop in self.difficulty_distribution.items()
        }
        self.current_counts = {diff: 0 for diff in self.difficulty_distribution}

    def add_question(self, q_obj):
        diff = q_obj["difficulty"]
        if self.current_counts[diff] < self.target_counts[diff]:
            q_text = q_obj["question"]
            if q_text not in self.seen_questions:
                self.seen_questions.add(q_text)
                self.questions.append(q_obj)
                self.current_counts[diff] += 1
                return True
        return False

    def generate(self):
        attempts = 0
        max_attempts = 200000

        while len(self.questions) < 1000 and attempts < max_attempts:
            attempts += 1

            needed_diffs = [d for d, c in self.current_counts.items() if c < self.target_counts[d]]
            if not needed_diffs:
                break

            diff = random.choice(needed_diffs)
            subtopic = random.choice(self.subtopics)
            template = random.choice(self.templates[diff])

            term, desc, fact = random.choice(self.concepts)
            context = random.choice(self.contexts)

            q_text = template.format(context=context, term=term, desc=desc, fact=fact)

            variations = ["", " Choose the best option.", " Select the correct answer.", " Analyze carefully.", " What is the most appropriate response?"]
            q_text += random.choice(variations)

            if q_text in self.seen_questions:
                continue

            diagram_svg = None
            if self.svg_templates and random.random() < 0.1:
                 diagram_svg = random.choice(self.svg_templates)
                 q_text += " Refer to the provided diagram if necessary."

            if diff == "easy" or "Which concept" in q_text or "Which of the following terms" in q_text or "Identify the term" in q_text or "What is this term" in q_text:
                correct_answer = term
                wrong_answers = []
                for t, d, f in self.concepts:
                    if t != term:
                        wrong_answers.append(t)

                if self.distractors_pool:
                    wrong_answers.extend(random.sample(self.distractors_pool, min(10, len(self.distractors_pool))))

            elif diff == "medium" or "statement is biologically accurate" in q_text or "true regarding" in q_text:
                correct_answer = fact.capitalize()
                wrong_answers = []
                for t, d, f in self.concepts:
                    if f != fact:
                        wrong_answers.append(f.capitalize())
                fake_facts = [
                    "It occurs universally in all organisms without exception.",
                    "It is completely independent of environmental factors.",
                    "It requires a massive input of energy to initiate.",
                    "It is the only factor responsible for this variation.",
                    "It only happens during specific, rare conditions."
                ]
                wrong_answers.extend(fake_facts)

            else:
                 if "outcome" in q_text or "expand" in q_text:
                     correct_answer = fact.capitalize()
                     wrong_answers = [f.capitalize() for t, d, f in self.concepts if f != fact]
                     wrong_answers.extend(["It stops immediately.", "It reverses its normal function.", "It speeds up exponentially."])
                 else:
                     correct_answer = term
                     wrong_answers = [t for t, d, f in self.concepts if t != term]
                     if self.distractors_pool:
                         wrong_answers.extend(random.sample(self.distractors_pool, min(10, len(self.distractors_pool))))

            unique_wrongs = list(set([str(w).strip() for w in wrong_answers if str(w).strip() != str(correct_answer).strip()]))
            random.shuffle(unique_wrongs)

            if len(unique_wrongs) < 6:
                fallbacks = ["Nucleus", "Mitochondria", "Chloroplast", "Cell membrane", "Cytoplasm", "Ribosome", "Vacuole", "Golgi apparatus"]
                for fb in fallbacks:
                    if fb not in unique_wrongs and fb != correct_answer:
                        unique_wrongs.append(fb)

            unique_wrongs = unique_wrongs[:8]

            if len(unique_wrongs) < 6:
                continue

            e_text = f"The correct answer is {correct_answer}. Specifically, {term} is {desc}, and a key fact is that {fact}."

            q_obj = {
                "id": f"{self.file_prefix}_{len(self.questions)+1:04d}",
                "topic": self.title,
                "subtopic": subtopic,
                "difficulty": diff,
                "question": q_text.strip(),
                "correct_answer": str(correct_answer).strip(),
                "wrong_answers_pool": unique_wrongs,
                "explanation": e_text.strip(),
                "diagram": diagram_svg
            }

            self.add_question(q_obj)

        print(f"[{self.title}] Generated {len(self.questions)} questions. (Easy: {self.current_counts['easy']}, Medium: {self.current_counts['medium']}, Hard: {self.current_counts['hard']})")
        return self.questions
