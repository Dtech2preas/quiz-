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
    def __init__(self, topic_name: str, topic_prefix: str, file_name: str, knowledge_base: KnowledgeBase, global_question_texts: set):
        self.topic_name = topic_name
        self.topic_prefix = topic_prefix
        self.file_name = file_name
        self.kb = knowledge_base
        self.generated_signatures = set()
        self.global_question_texts = global_question_texts
        self.skipped_duplicates = 0
        self.exact_duplicates_removed = 0
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

    def generate_signature(self, question_text):
        # Normalize text: lower, trim, collapse spaces
        import string
        import re
        normalized = re.sub(f'[{re.escape(string.punctuation)}]', '', question_text)
        normalized = " ".join(normalized.lower().split())
        return hashlib.md5(normalized.encode()).hexdigest()

    def add_question(self, subtopic: str, difficulty: str, family: str, primary_entity: str, question: str, correct_answer: str, wrong_answers: List[str], explanation: str):
        if self.difficulty_counts[difficulty] >= self.difficulty_targets[difficulty]:
            return False

        signature = self.generate_signature(question)
        if signature in self.global_question_texts:
            self.exact_duplicates_removed += 1
            return False

        edu_sig = f"{subtopic}|{family}|{primary_entity}|{correct_answer}"
        if edu_sig in self.generated_signatures:
            self.skipped_duplicates += 1
            return False
        self.global_question_texts.add(signature)
        self.generated_signatures.add(edu_sig)

        # Ensure correct_answer is not in wrong_answers
        wrong_answers = [str(w) for w in wrong_answers if str(w) != str(correct_answer)]

        # Deduplicate wrong answers
        unique_wrong_answers = list(dict.fromkeys(wrong_answers))

        if len(unique_wrong_answers) < 6:
            all_names = self.kb.get_all_names(self.topic_name)
            random.shuffle(all_names)
            for n in all_names:
                if str(n) != str(correct_answer) and str(n) not in unique_wrong_answers:
                    unique_wrong_answers.append(str(n))
                if len(unique_wrong_answers) >= 6:
                    break

        if len(unique_wrong_answers) < 6:
             extra = ["Option A", "Option B", "Option C", "Option D", "Option E", "Option F", "Option G", "Option H"]
             for e in extra:
                 if str(e) not in unique_wrong_answers and str(e) != str(correct_answer):
                     unique_wrong_answers.append(str(e))
                 if len(unique_wrong_answers) >= 6:
                     break

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
        filepath = os.path.join("dataset/grade12/life_sciences", self.file_name)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)
        print(f"Saved {filepath} with {len(self.questions)} questions. (Exact text dups removed: {self.exact_duplicates_removed}, Edu signature dups skipped: {self.skipped_duplicates})")
        return len(self.questions), self.exact_duplicates_removed, self.skipped_duplicates


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
    templates = [
        f"Unlike {e2['name']} (which involves {e2['desc']}), which term is specifically characterized by {e1['desc']}?",
        f"While {e2['name']} is defined as {e2['desc']}, what biological term best describes {e1['desc']}?",
        f"Distinguish between these concepts: {e2['name']} relates to {e2['desc']}, but which term refers to {e1['desc']}?"
    ]
    q_text = random.choice(templates)
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



def generate_easy_recall_2(engine: QuestionEngine, subtopic: str, entity: dict):
    q_texts = [
        f"Which term is used to describe {entity['desc']}?",
        f"What is the correct name for {entity['desc']}?",
        f"Identify the structure or process characterized by {entity['desc']}."
    ]
    ans = entity['name']
    wrongs = entity.get('w', [])
    expl = f"{ans} is characterized by {entity['desc']}."
    return engine.add_question(subtopic, "easy", "recall_definition_2", entity['name'], random.choice(q_texts), ans, wrongs, expl)

def generate_easy_identification_2(engine: QuestionEngine, subtopic: str, entity: dict):
    q_texts = [
        f"Choose the statement that correctly describes '{entity['name']}'.",
        f"Which of the following is true regarding {entity['name']}?",
        f"What is the primary characteristic of {entity['name']}?"
    ]
    ans = entity['desc']
    all_ents = engine.kb.get_entities(engine.topic_name, subtopic)
    wrongs = [e['desc'] for e in all_ents if e['name'] != entity['name']]
    expl = f"The primary characteristic of {entity['name']} is {entity['desc']}."
    return engine.add_question(subtopic, "easy", "recall_term_2", entity['name'], random.choice(q_texts), ans, wrongs, expl)

def generate_medium_scenario_2(engine: QuestionEngine, subtopic: str, entity: dict):
    scenarios = [
        f"During a field study, ecologists observe an organism exhibiting {entity['desc']}. What biological term applies?",
        f"A laboratory test confirms that {entity['desc']}. Which process is occurring?",
        f"If a student notes that {entity['desc']}, what are they describing?",
        f"A doctor explains a condition involving {entity['desc']}. What term is the doctor referring to?",
        f"In an exam question, a diagram shows {entity['desc']}. What does the diagram represent?"
    ]
    ans = entity['name']
    wrongs = entity.get('w', [])
    expl = f"The observation of {entity['desc']} indicates {ans}."
    return engine.add_question(subtopic, "medium", "scenario_observation_2", entity['name'], random.choice(scenarios), ans, wrongs, expl)

def generate_medium_compare_2(engine: QuestionEngine, subtopic: str, e1: dict, e2: dict):
    templates = [
        f"How does {e1['name']} differ from {e2['name']} based on the fact that {e1['name']} involves {e1['desc']}?",
        f"While {e2['name']} involves {e2['desc']}, {e1['name']} involves...",
        f"Compare {e1['name']} and {e2['name']}. {e1['name']} is defined by..."
    ]
    q_text = random.choice(templates)
    ans = e1['desc']
    wrongs = [e2['desc']]
    expl = f"{e1['name']} is defined by {e1['desc']}, which distinguishes it from {e2['name']}."
    return engine.add_question(subtopic, "medium", "compare_2", f"{e1['name']}_{e2['name']}", q_text, ans, wrongs, expl)



def generate_easy_recall_3(engine: QuestionEngine, subtopic: str, entity: dict):
    q_texts = [
        f"Select the biological term that matches this description: {entity['desc']}.",
        f"What is {entity['desc']} known as in biology?",
        f"Which of the following answers is defined as {entity['desc']}?"
    ]
    ans = entity['name']
    wrongs = entity.get('w', [])
    expl = f"{ans} is precisely defined as {entity['desc']}."
    return engine.add_question(subtopic, "easy", "recall_definition_3", entity['name'], random.choice(q_texts), ans, wrongs, expl)

def generate_easy_identification_3(engine: QuestionEngine, subtopic: str, entity: dict):
    q_texts = [
        f"Read the following options. Which one best describes '{entity['name']}'?",
        f"Of the descriptions provided below, which one defines {entity['name']}?"
    ]
    ans = entity['desc']
    all_ents = engine.kb.get_entities(engine.topic_name, subtopic)
    wrongs = [e['desc'] for e in all_ents if e['name'] != entity['name']]
    expl = f"{entity['name']} is best described as {entity['desc']}."
    return engine.add_question(subtopic, "easy", "recall_term_3", entity['name'], random.choice(q_texts), ans, wrongs, expl)

def generate_medium_scenario_3(engine: QuestionEngine, subtopic: str, entity: dict):
    scenarios = [
        f"A medical researcher isolates a compound involved in {entity['desc']}. What is the correct term for this biological phenomenon?",
        f"A textbook describes a process that leads to {entity['desc']}. What is the name of this process?",
        f"During a presentation, a scientist discusses {entity['desc']}. What topic are they covering?"
    ]
    ans = entity['name']
    wrongs = entity.get('w', [])
    expl = f"The scenario explicitly details {entity['desc']}, matching {ans}."
    return engine.add_question(subtopic, "medium", "scenario_observation_3", entity['name'], random.choice(scenarios), ans, wrongs, expl)

def generate_medium_compare_3(engine: QuestionEngine, subtopic: str, e1: dict, e2: dict):
    templates = [
        f"Both {e1['name']} and {e2['name']} are important biological concepts. Which statement correctly identifies {e1['name']}?",
        f"While distinguishing between {e1['name']} and {e2['name']}, what is the primary feature of {e1['name']}?"
    ]
    q_text = random.choice(templates)
    ans = e1['desc']
    wrongs = [e2['desc']]
    expl = f"{e1['name']} features {e1['desc']} while {e2['name']} features {e2['desc']}."
    return engine.add_question(subtopic, "medium", "compare_3", f"{e1['name']}_{e2['name']}", q_text, ans, wrongs, expl)

def generate_hard_statement_analysis_2(engine: QuestionEngine, subtopic: str, e1: dict, e2: dict):
    mode = random.choice([
        ("true", "false", "Statement I is true, Statement II is false"),
        ("false", "true", "Statement I is false, Statement II is true"),
        ("false", "false", "Both statements are false")
    ])

    s1_name = e1['name']
    s1_desc = e1['desc'] if mode[0] == "true" else e2['desc']

    s2_name = e2['name']
    s2_desc = e2['desc'] if mode[1] == "true" else e1['desc']

    q_text = f"Evaluate the following statements regarding biological concepts:\nI. {s1_name} relates to {s1_desc}.\nII. {s2_name} relates to {s2_desc}.\nWhich of the following is correct?"
    ans = mode[2]
    wrongs = [m for m in ["Statement I is true, Statement II is false", "Statement I is false, Statement II is true", "Both statements are false", "Both statements are true"] if m != ans]
    expl = f"Statement I is {mode[0]} ({e1['name']} is {e1['desc']}). Statement II is {mode[1]} ({e2['name']} is {e2['desc']}). Therefore, {ans}."

    return engine.add_question(subtopic, "hard", "statement_analysis_2", f"{e1['name']}_{e2['name']}", q_text, ans, wrongs, expl)

def generate_hard_cause_effect_2(engine: QuestionEngine, subtopic: str, entity: dict):
    scenarios = [
        f"What would be the most likely outcome if {entity['name']} (which involves {entity['desc']}) were inhibited by a drug?",
        f"A genetic defect prevents the normal functioning of {entity['name']}. Since this involves {entity['desc']}, what is the immediate consequence?"
    ]
    ans = "Failure of the processes described by: " + entity['desc']
    all_ents = engine.kb.get_entities(engine.topic_name, subtopic)
    wrongs = ["Failure of the processes described by: " + e['desc'] for e in all_ents if e['name'] != entity['name']]
    expl = f"Because {entity['name']} is defined as {entity['desc']}, inhibiting it causes a failure in those exact processes."
    return engine.add_question(subtopic, "hard", "cause_effect_2", entity['name'], random.choice(scenarios), ans, wrongs, expl)

def generate_complex_scenario_2(engine: QuestionEngine, subtopic: str, e1: dict):
    scenarios = [
        f"In a clinical trial, a new therapy aims to enhance the biological function defined as: {e1['desc']}. What is the primary target of this therapy?",
        f"A biology student observes an interaction where {e1['desc']} is the defining characteristic. What is the correct terminology for this observation?"
    ]
    ans = e1['name']
    wrongs = e1.get('w', [])
    expl = f"The scenario is built around the definition of {e1['name']}, which is {e1['desc']}."
    return engine.add_question(subtopic, "hard", "complex_scenario_2", e1['name'], random.choice(scenarios), ans, wrongs, expl)

def generate_genetics_cross(engine: QuestionEngine, subtopic: str, e1: dict):
    # dynamic punnett square / genetics
    traits = [
        ("Tall", "Short", "T", "t"), ("Purple", "White", "P", "p"),
        ("Round", "Wrinkled", "R", "r"), ("Black", "Brown", "B", "b"),
        ("Yellow", "Green", "Y", "y"), ("Smooth", "Rough", "S", "s"),
        ("Red", "White", "R", "r"), ("Axial", "Terminal", "A", "a")
    ]
    trait = random.choice(traits)
    dom_trait, rec_trait, dom_allele, rec_allele = trait

    crosses = [
        ("homozygous dominant", "homozygous recessive", dom_allele*2, rec_allele*2, "100% heterozygous", "100% " + dom_trait),
        ("heterozygous", "heterozygous", dom_allele+rec_allele, dom_allele+rec_allele, "25% homozygous dominant, 50% heterozygous, 25% homozygous recessive", "75% " + dom_trait + ", 25% " + rec_trait),
        ("heterozygous", "homozygous recessive", dom_allele+rec_allele, rec_allele*2, "50% heterozygous, 50% homozygous recessive", "50% " + dom_trait + ", 50% " + rec_trait),
        ("homozygous dominant", "heterozygous", dom_allele*2, dom_allele+rec_allele, "50% homozygous dominant, 50% heterozygous", "100% " + dom_trait),
        ("homozygous recessive", "homozygous recessive", rec_allele*2, rec_allele*2, "100% homozygous recessive", "100% " + rec_trait)
    ]

    c = random.choice(crosses)
    parent1, parent2, p1_geno, p2_geno, geno_ratio, pheno_ratio = c

    q_type = random.choice(["phenotype", "genotype"])
    if q_type == "phenotype":
        q_text = f"In a certain plant species, the allele for {dom_trait} ({dom_allele}) is dominant over the allele for {rec_trait} ({rec_allele}). If a {parent1} plant is crossed with a {parent2} plant, what is the expected phenotypic ratio of their offspring?"
        ans = pheno_ratio
        wrongs = [
            f"100% {dom_trait}", f"100% {rec_trait}", f"50% {dom_trait}, 50% {rec_trait}",
            f"75% {dom_trait}, 25% {rec_trait}", f"25% {dom_trait}, 75% {rec_trait}",
            f"100% heterozygous", "Cannot be determined"
        ]
    else:
        q_text = f"In a certain plant species, the allele for {dom_trait} ({dom_allele}) is dominant over the allele for {rec_trait} ({rec_allele}). If a {parent1} plant is crossed with a {parent2} plant, what is the expected genotypic ratio of their offspring?"
        ans = geno_ratio
        wrongs = [
            "100% homozygous dominant", "100% homozygous recessive", "100% heterozygous",
            "50% homozygous dominant, 50% heterozygous", "50% heterozygous, 50% homozygous recessive",
            "25% homozygous dominant, 50% heterozygous, 25% homozygous recessive",
            "75% homozygous dominant, 25% homozygous recessive"
        ]

    expl = f"A {parent1} parent ({p1_geno}) crossed with a {parent2} parent ({p2_geno}) yields a Punnett square with {geno_ratio}, resulting in {pheno_ratio}."
    return engine.add_question(subtopic, "medium", "genetics_cross", e1['name'], q_text, ans, wrongs, expl)

def generate_dna_translation(engine: QuestionEngine, subtopic: str, e1: dict):
    # dynamic dna to mrna / amino acids
    # Generate random codon
    bases = ["A", "T", "C", "G"]
    dna = "".join(random.choices(bases, k=3))

    def transcribe(d):
        return d.replace("A", "U").replace("T", "A").replace("C", "g").replace("G", "C").replace("g", "G")

    def translate_anticodon(m):
        return m.replace("A", "U").replace("U", "A").replace("C", "g").replace("G", "C").replace("g", "G")

    mrna = transcribe(dna)
    trna = translate_anticodon(mrna)

    q_type = random.choice(["dna_to_mrna", "mrna_to_trna", "dna_to_trna"])

    if q_type == "dna_to_mrna":
        q_text = f"During transcription, a DNA strand with the sequence '{dna}' will produce an mRNA codon with which sequence?"
        ans = mrna
        wrongs = [trna, dna, mrna[::-1], dna[::-1], "".join(random.choices(["A", "U", "C", "G"], k=3)), "".join(random.choices(["A", "U", "C", "G"], k=3))]
        expl = f"In transcription, DNA pairs with mRNA using complementary base pairing (A-U, T-A, C-G, G-C). Thus, '{dna}' becomes '{mrna}'."
    elif q_type == "mrna_to_trna":
        q_text = f"During translation, an mRNA codon with the sequence '{mrna}' will pair with a tRNA anticodon containing which sequence?"
        ans = trna
        wrongs = [dna, mrna, trna[::-1], mrna[::-1], "".join(random.choices(["A", "U", "C", "G"], k=3)), "".join(random.choices(["A", "U", "C", "G"], k=3))]
        expl = f"In translation, mRNA pairs with tRNA anticodons (A-U, U-A, C-G, G-C). Thus, '{mrna}' pairs with '{trna}'."
    else:
        q_text = f"A DNA triplet sequence is '{dna}'. What will be the corresponding sequence on the tRNA anticodon during protein synthesis?"
        ans = trna
        wrongs = [mrna, dna, trna[::-1], mrna[::-1], "".join(random.choices(["A", "U", "C", "G"], k=3)), "".join(random.choices(["A", "U", "C", "G"], k=3))]
        expl = f"DNA '{dna}' transcribes to mRNA '{mrna}', which then pairs with tRNA '{trna}'."

    return engine.add_question(subtopic, "medium", "dna_translation", e1['name'], q_text, ans, wrongs, expl)

def generate_experimental_design(engine: QuestionEngine, subtopic: str, e1: dict):
    # dynamic experiment identifying variables
    topics = [
        ("temperature", "enzyme activity", "pH level, enzyme concentration"),
        ("light intensity", "the rate of photosynthesis", "temperature, carbon dioxide concentration"),
        ("carbon dioxide concentration", "plant growth", "light intensity, temperature, water"),
        ("salt concentration", "the mass of potato tissue", "initial mass, time, temperature"),
        ("humidity", "the rate of transpiration", "temperature, wind speed, light"),
        ("wind speed", "the rate of transpiration", "temperature, humidity, light"),
        ("oxygen concentration", "rate of cellular respiration", "temperature, glucose availability"),
        ("thyroxin levels", "metabolic rate", "age, gender, diet"),
        ("adrenaline", "heart rate", "activity level, age")
    ]

    exp = random.choice(topics)
    indep, dep, controlled = exp

    # We can also randomize the wording of the dependent variable
    investigation = f"the effect of {indep} on {dep}"

    q_type = random.choice(["independent", "dependent", "controlled"])

    if q_type == "independent":
        q_text = f"In an investigation to determine {investigation}, which factor represents the independent variable?"
        ans = indep
        wrongs = [dep] + controlled.split(', ') + ["sample size", "time of day"]
        expl = f"The independent variable is the one changed or manipulated by the investigator, which is {indep}."
    elif q_type == "dependent":
        q_text = f"In an investigation to determine {investigation}, which factor represents the dependent variable?"
        ans = dep
        wrongs = [indep] + controlled.split(', ') + ["sample size", "measuring equipment"]
        expl = f"The dependent variable is the one measured as the outcome, which is {dep}."
    else:
        c_var = random.choice(controlled.split(', '))
        q_text = f"In an investigation to determine {investigation}, which of the following is a variable that must be kept constant (controlled) to ensure a fair test?"
        ans = c_var
        wrongs = [indep, dep, "the hypothesis", "the conclusion", "the random error"]
        expl = f"To ensure a fair test, factors other than the independent variable ({indep}) that might affect the dependent variable ({dep}) must be controlled, such as {c_var}."

    return engine.add_question(subtopic, "hard", "experimental_design", e1['name'], q_text, ans, wrongs, expl)

def generate_graph_analysis(engine: QuestionEngine, subtopic: str, e1: dict):
    graphs = [
        ("population size over time", "Logistic growth curve", "Lag phase, Log/Exponential phase, Decelerating phase, Equilibrium phase", "Carrying capacity"),
        ("population size of a predator and prey over time", "Predator-Prey curve", "Prey peak, Predator peak, Prey trough", "Phase lag"),
        ("enzyme activity against temperature", "Optimum temperature curve", "Increasing activity, Peak/Optimum, Denaturation (rapid drop)", "Optimum temperature"),
        ("enzyme activity against pH", "Optimum pH curve", "Increasing activity, Peak/Optimum, Denaturation (rapid drop)", "Optimum pH"),
        ("hormone levels during a 28-day menstrual cycle", "Menstrual cycle hormone graph", "FSH peak, LH surge (ovulation), Progesterone rise", "Day 14 (Ovulation)"),
        ("rate of photosynthesis against light intensity", "Photosynthesis curve", "Linear increase, Saturation point, Constant rate", "Light saturation point"),
        ("rate of transpiration against humidity", "Transpiration curve", "Initial high rate, Gradual decrease, Low constant rate", "Stomatal closure")
    ]
    graph = random.choice(graphs)
    desc, name, phases, key_point = graph

    q_texts = [
        f"A graph showing {desc} reaches a maximum point and levels off or changes rapidly. What is the primary biological significance of this key point ({key_point})?",
        f"When interpreting a graph of {desc}, what term best describes the stage associated with '{key_point}'?",
        f"In a {name}, which of the following is a critical phase or point represented?",
        f"Consider a {name} showing {desc}. What is the most significant event or value represented on the graph?"
    ]

    ans = key_point
    wrongs = phases.split(', ') + ["Zero point", "Infinite growth", "Extinction phase", "Initial decline"]
    expl = f"The graph represents {name}. The key point described is the {key_point}, a critical juncture in the process."

    return engine.add_question(subtopic, "hard", "graph_analysis", e1['name'], random.choice(q_texts), ans, wrongs, expl)

def generate_complex_scenario(engine: QuestionEngine, subtopic: str, e1: dict):
    scenarios = [
        f"A patient presents with symptoms that indicate a failure in the normal physiological regulation of {e1['desc']}. Based on your knowledge of Grade 12 Life Sciences, which of the following structures or pathways is most likely defective?",
        f"An ecologist notes that an environmental disruption has severely impacted the natural occurrence of {e1['desc']}. What is the most immediate biological consequence of this?",
        f"During a laboratory analysis, scientists observe an anomaly characterized by an abnormal form of {e1['desc']}. What concept does this observation directly correlate with?"
    ]
    ans = e1['name']
    wrongs = e1.get('w', [])
    expl = f"The scenario describes {e1['desc']}, which is the core definition of {ans}."
    return engine.add_question(subtopic, "hard", "complex_scenario", e1['name'], random.choice(scenarios), ans, wrongs, expl)


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
    global_question_texts = set()
    total_generated = 0
    total_exact_dups = 0
    total_skipped = 0
    topic_counts = {}
    total_generated = 0
    total_exact_dups = 0
    total_skipped = 0
    topic_counts = {}

    for t in topics_data:
        engine = QuestionEngine(t['topic'], t['prefix'], t['file'], kb, global_question_texts)

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
                choice = random.random()
                if choice < 0.16:
                    generate_easy_recall(engine, subtopic, e1)
                elif choice < 0.32:
                    generate_easy_identification(engine, subtopic, e1)
                elif choice < 0.48:
                    generate_easy_recall_2(engine, subtopic, e1)
                elif choice < 0.64:
                    generate_easy_identification_2(engine, subtopic, e1)
                elif choice < 0.8:
                    generate_easy_recall_3(engine, subtopic, e1)
                else:
                    generate_easy_identification_3(engine, subtopic, e1)

            # Medium
            if engine.difficulty_counts['medium'] < engine.difficulty_targets['medium']:
                choice = random.random()
                if engine.topic_name == "Genetics and Inheritance" and choice < 0.2:
                    generate_genetics_cross(engine, subtopic, e1)
                elif engine.topic_name == "DNA: Code of Life" and choice < 0.2:
                    generate_dna_translation(engine, subtopic, e1)
                elif choice < 0.35 and e1 != e2:
                    generate_medium_compare(engine, subtopic, e1, e2)
                elif choice < 0.5 and e1 != e2:
                    generate_medium_compare_2(engine, subtopic, e1, e2)
                elif choice < 0.65 and e1 != e2:
                    generate_medium_compare_3(engine, subtopic, e1, e2)
                elif choice < 0.8:
                    generate_medium_scenario(engine, subtopic, e1)
                elif choice < 0.9:
                    generate_medium_scenario_2(engine, subtopic, e1)
                else:
                    generate_medium_scenario_3(engine, subtopic, e1)

            # Hard
            if engine.difficulty_counts['hard'] < engine.difficulty_targets['hard']:
                choice = random.random()
                if choice < 0.15:
                    generate_experimental_design(engine, subtopic, e1)
                elif choice < 0.3:
                    generate_graph_analysis(engine, subtopic, e1)
                elif choice < 0.45:
                    generate_complex_scenario(engine, subtopic, e1)
                elif choice < 0.6:
                    generate_complex_scenario_2(engine, subtopic, e1)
                elif choice < 0.7 and e1 != e2:
                    generate_hard_statement_analysis(engine, subtopic, e1, e2)
                elif choice < 0.8 and e1 != e2:
                    generate_hard_statement_analysis_2(engine, subtopic, e1, e2)
                elif choice < 0.9:
                    generate_hard_cause_effect(engine, subtopic, e1)
                else:
                    generate_hard_cause_effect_2(engine, subtopic, e1)

        engine.save_to_json()
        total_generated += len(engine.questions)
        total_exact_dups += engine.exact_duplicates_removed
        total_skipped += engine.skipped_duplicates
        topic_counts[t['topic']] = len(engine.questions)



    print("\n--- GENERATION REPORT ---")
    print(f"Total questions generated: {total_generated}")
    print(f"Exact duplicate questions removed globally: {total_exact_dups}")
    print(f"Questions skipped due to local signature duplication: {total_skipped}")
    print("\nQuestions per topic:")
    for topic, count in topic_counts.items():
        print(f"  {topic}: {count}")
        if count < 100:
            print(f"  --> WARNING: {topic} generated significantly fewer questions than expected!")

if __name__ == "__main__":
    build_datasets()
