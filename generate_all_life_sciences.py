import json
import random
import os
import hashlib
from typing import List, Dict

class KnowledgeBase:
    def __init__(self):
        self.entities = {}

    def add_entity(self, topic, subtopic, entity_name, attributes):
        if topic not in self.entities:
            self.entities[topic] = {}
        if subtopic not in self.entities[topic]:
            self.entities[topic][subtopic] = []

        attributes['name'] = entity_name
        self.entities[topic][subtopic].append(attributes)

    def get_entities(self, topic, subtopic):
        return self.entities.get(topic, {}).get(subtopic, [])

    def get_all_names(self, topic):
        names = []
        if topic in self.entities:
            for subtopic, ents in self.entities[topic].items():
                names.extend([e['name'] for e in ents])
        return list(set(names))

class QuestionEngine:
    def __init__(self, topic_name: str, topic_prefix: str, file_name: str, knowledge_base: KnowledgeBase):
        self.topic_name = topic_name
        self.topic_prefix = topic_prefix
        self.file_name = file_name
        self.kb = knowledge_base
        self.generated_signatures = set()
        self.questions = []

        # Increase targets slightly to get more volume if available,
        # but the script stops if no unique signatures are possible.
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

    def generate_signature(self, subtopic, family, primary_entity, answer):
        # Create a unique signature for the educational content
        raw = f"{subtopic}|{family}|{primary_entity}|{answer}"
        return hashlib.md5(raw.encode()).hexdigest()

    def add_question(self, subtopic: str, difficulty: str, family: str, primary_entity: str, question: str, correct_answer: str, wrong_answers: List[str], explanation: str):
        if self.difficulty_counts[difficulty] >= self.difficulty_targets[difficulty]:
            return False

        signature = self.generate_signature(subtopic, family, primary_entity, correct_answer)
        if signature in self.generated_signatures:
            return False

        # Ensure correct_answer is not in wrong_answers
        wrong_answers = [str(w) for w in wrong_answers if str(w) != str(correct_answer)]

        # Deduplicate wrong answers
        unique_wrong_answers = list(dict.fromkeys(wrong_answers))

        if len(unique_wrong_answers) < 3:
            all_names = self.kb.get_all_names(self.topic_name)
            random.shuffle(all_names)
            for n in all_names:
                if n != correct_answer and n not in unique_wrong_answers:
                    unique_wrong_answers.append(n)
                if len(unique_wrong_answers) >= 6:
                    break

        if len(unique_wrong_answers) < 3:
             extra = ["Option A", "Option B", "Option C", "Option D", "Option E"]
             for e in extra:
                 if e not in unique_wrong_answers and e != correct_answer:
                     unique_wrong_answers.append(e)

        self.generated_signatures.add(signature)

        paper = "paper1" if "P1" in self.topic_prefix else "paper2"
        question_id = f"{self.topic_prefix}_{len(self.questions) + 1:03d}"

        q_dict = {
            "id": question_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "paper": paper,
            "difficulty": difficulty,
            "question": question, # Frontend expects 'question', not 'family'
            "correct_answer": str(correct_answer),
            "wrong_answers_pool": unique_wrong_answers[:8],
            "explanation": explanation
        }
        self.questions.append(q_dict)
        self.difficulty_counts[difficulty] += 1
        return True

    def save_to_json(self):
        filepath = os.path.join("dataset/life_sciences", self.file_name)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)
        print(f"Saved {filepath} with {len(self.questions)} questions.")


def generate_easy_recall(engine: QuestionEngine, subtopic: str, entity: dict):
    q_texts = [
        f"Which of the following represents {entity['desc']}?",
        f"What is the biological term for {entity['desc']}?",
        f"Identify the concept defined as: {entity['desc']}."
    ]
    ans = entity['name']
    wrongs = entity.get('w', [])
    expl = f"The correct answer is {ans} because it is defined as: {entity['desc']}."
    return engine.add_question(subtopic, "easy", "recall_definition", entity['name'], random.choice(q_texts), ans, wrongs, expl)

def generate_easy_identification(engine: QuestionEngine, subtopic: str, entity: dict):
    q_texts = [
        f"The term '{entity['name']}' is best described by which of the following statements?",
        f"Which statement accurately defines {entity['name']}?",
        f"Select the correct description for {entity['name']}."
    ]
    ans = entity['desc']
    all_ents = engine.kb.get_entities(engine.topic_name, subtopic)
    wrongs = [e['desc'] for e in all_ents if e['name'] != entity['name']]
    expl = f"{entity['name']} is specifically defined as {entity['desc']}."
    return engine.add_question(subtopic, "easy", "recall_term", entity['name'], random.choice(q_texts), ans, wrongs, expl)

def generate_medium_scenario(engine: QuestionEngine, subtopic: str, entity: dict):
    scenarios = [
        f"A biologist observes {entity['desc']} occurring in a specimen. What biological concept is being observed?",
        f"During an experiment, it is noted that {entity['desc']}. Which term applies to this observation?",
        f"A student is studying a process characterized by {entity['desc']}. What process are they studying?",
        f"In a laboratory setting, a researcher documents {entity['desc']}. This describes:",
        f"A medical case study highlights {entity['desc']}. What is the correct biological identification for this?"
    ]
    ans = entity['name']
    wrongs = entity.get('w', [])
    expl = f"The scenario describes {entity['desc']}, which is the definition of {ans}."
    return engine.add_question(subtopic, "medium", "scenario_observation", entity['name'], random.choice(scenarios), ans, wrongs, expl)

def generate_medium_compare(engine: QuestionEngine, subtopic: str, e1: dict, e2: dict):
    q_text = f"Unlike {e2['name']} (which involves {e2['desc']}), which term is specifically characterized by {e1['desc']}?"
    ans = e1['name']
    wrongs = [e2['name']]
    expl = f"{e1['name']} involves {e1['desc']}, whereas {e2['name']} involves {e2['desc']}."
    return engine.add_question(subtopic, "medium", "compare", f"{e1['name']}_{e2['name']}", q_text, ans, wrongs, expl)

def generate_hard_statement_analysis(engine: QuestionEngine, subtopic: str, e1: dict, e2: dict):
    mode = random.choice([
        ("true", "true", "Both I and II are correct"),
        ("true", "false", "Only I is correct"),
        ("false", "true", "Only II is correct"),
        ("false", "false", "Neither I nor II is correct")
    ])

    s1_name = e1['name']
    s1_desc = e1['desc'] if mode[0] == "true" else e2['desc']

    s2_name = e2['name']
    s2_desc = e2['desc'] if mode[1] == "true" else e1['desc']

    q_text = f"Consider the following statements:\nI. {s1_name} is defined as {s1_desc}.\nII. {s2_name} is defined as {s2_desc}.\nWhich of the statements is/are biologically accurate?"
    ans = mode[2]
    wrongs = [m for m in ["Both I and II are correct", "Only I is correct", "Only II is correct", "Neither I nor II is correct"] if m != ans]
    expl = f"Statement I is {mode[0]} ({e1['name']} is {e1['desc']}). Statement II is {mode[1]} ({e2['name']} is {e2['desc']}). Therefore, {ans}."

    return engine.add_question(subtopic, "hard", "statement_analysis", f"{e1['name']}_{e2['name']}", q_text, ans, wrongs, expl)

def generate_hard_cause_effect(engine: QuestionEngine, subtopic: str, entity: dict):
    scenarios = [
        f"If a mutation severely impaired the biological feature described as '{entity['desc']}', which structure or process would be primarily affected?",
        f"A disease disrupts the process of {entity['desc']}. Which biological entity is directly malfunctioning?",
        f"An environmental toxin completely halts {entity['desc']}. What is the correct term for the affected biological mechanism?"
    ]
    ans = entity['name']
    wrongs = entity.get('w', [])
    expl = f"The description '{entity['desc']}' defines {entity['name']}. An impairment here directly affects {entity['name']}."
    return engine.add_question(subtopic, "hard", "cause_effect", entity['name'], random.choice(scenarios), ans, wrongs, expl)

def populate_knowledge_base():
    kb = KnowledgeBase()
    with open('extracted_topics.json', 'r') as f:
        topics_data = json.load(f)

    for t in topics_data:
        topic_name = t['topic']
        for s in t['subtopics']:
            subtopic_name = s['name']
            for fact in s['facts']:
                kb.add_entity(topic_name, subtopic_name, fact['a'], {"desc": fact['desc'], "w": fact.get("w", [])})

    return kb, topics_data

def build_datasets():
    kb, topics_data = populate_knowledge_base()

    for t in topics_data:
        engine = QuestionEngine(t['topic'], t['prefix'], t['file'], kb)

        # We need to fill quotas using the families.
        # This loop tries to generate questions until the engine targets are met.
        attempts = 0
        max_attempts = 500000

        while attempts < max_attempts and (engine.difficulty_counts['easy'] < engine.difficulty_targets['easy'] or
                                           engine.difficulty_counts['medium'] < engine.difficulty_targets['medium'] or
                                           engine.difficulty_counts['hard'] < engine.difficulty_targets['hard']):
            attempts += 1
            subtopic = random.choice(t['subtopics'])['name']
            ents = kb.get_entities(t['topic'], subtopic)
            if not ents:
                continue

            e1 = random.choice(ents)
            e2 = random.choice(ents)
            while e1 == e2 and len(ents) > 1:
                e2 = random.choice(ents)

            # Easy
            if engine.difficulty_counts['easy'] < engine.difficulty_targets['easy']:
                if random.choice([True, False]):
                    generate_easy_recall(engine, subtopic, e1)
                else:
                    generate_easy_identification(engine, subtopic, e1)

            # Medium
            if engine.difficulty_counts['medium'] < engine.difficulty_targets['medium']:
                if random.choice([True, False]) and e1 != e2:
                    generate_medium_compare(engine, subtopic, e1, e2)
                else:
                    generate_medium_scenario(engine, subtopic, e1)

            # Hard
            if engine.difficulty_counts['hard'] < engine.difficulty_targets['hard']:
                if random.choice([True, False]) and e1 != e2:
                    generate_hard_statement_analysis(engine, subtopic, e1, e2)
                else:
                    generate_hard_cause_effect(engine, subtopic, e1)

        engine.save_to_json()

if __name__ == "__main__":
    build_datasets()
