import os
import sys
import random

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from agrisci11_common import standardize_agrisci11_topic

def synth_chemistry(current, targets, seen_texts, distractors, prefix, topic_name, paper):
    provinces = ["Free State", "Limpopo", "Mpumalanga", "North West", "Western Cape", "Eastern Cape", "KwaZulu-Natal"]
    crops = ["maize", "wheat", "sorghum", "sunflower", "soybean", "sugarcane", "canola", "cotton", "potatoes"]
    farmers = ["Sipho", "Johan", "Lerato", "Kobus", "Zanele", "Thabo", "Devan", "Anke", "Pieter", "Nandi"]

    # Pool of concepts for Basic Agricultural Chemistry
    chem_pool = [
        ("Covalent bond", "sharing of electron pairs between non-metal atoms", "Chemical bonding"),
        ("Ionic bond", "electrostatic attraction between oppositely charged ions", "Chemical bonding"),
        ("Hydrogen bond", "weak attraction involving a bonded hydrogen atom and an electronegative atom", "Chemical bonding"),
        ("Proton", "positively charged subatomic particle located in the nucleus", "Atomic structure"),
        ("Neutron", "neutral subatomic particle found in the atomic nucleus", "Atomic structure"),
        ("Electron", "negatively charged particle orbiting the atomic nucleus in shells", "Atomic structure"),
        ("Atomic number", "number of protons found in the nucleus of an atom", "Atomic structure"),
        ("Mass number", "total number of protons and neutrons in an atomic nucleus", "Atomic structure"),
        ("Monosaccharide", "simplest form of sugar that cannot be hydrolyzed into simpler carbohydrates", "Carbohydrates, proteins, lipids"),
        ("Disaccharide", "sugar formed when two monosaccharides are joined by a glycosidic bond", "Carbohydrates, proteins, lipids"),
        ("Polysaccharide", "complex carbohydrate polymer consisting of numerous bonded sugar units", "Carbohydrates, proteins, lipids"),
        ("Triglyceride", "ester derived from glycerol and three fatty acid chains", "Carbohydrates, proteins, lipids"),
        ("Peptide bond", "covalent bond linking amino acids together in a protein polypeptide", "Carbohydrates, proteins, lipids"),
        ("Enzyme", "biological protein catalyst that accelerates metabolic reactions in crops", "Carbohydrates, proteins, lipids"),
        ("pH scale", "logarithmic measure of the hydronium ion concentration in a soil solution", "Acids, bases and pH"),
        ("Acidic soil", "soil possessing a pH below 7.0 with high exchangeable Al3+ and H+ ions", "Acids, bases and pH"),
        ("Alkaline soil", "soil having a pH above 7.0 with high basic cation saturation", "Acids, bases and pH"),
        ("Calcitic lime", "calcium carbonate (CaCO3) applied to raise soil pH and neutralize acidity", "Acids, bases and pH"),
        ("Dolomitic lime", "calcium magnesium carbonate applied to correct soil acidity and supply magnesium", "Acids, bases and pH"),
        ("Inorganic compound", "chemical substance lacking carbon-hydrogen bonds, such as rock phosphate or potash", "Organic and inorganic compounds")
    ]

    all_terms = [c[0] for c in chem_pool]

    for d in ["easy", "medium", "hard"]:
        needed = targets[d] - len(current[d])
        counter = 0
        while needed > 0 and counter < 5000:
            counter += 1
            term, desc, sub = random.choice(chem_pool)
            prov = random.choice(provinces)
            crop = random.choice(crops)
            farmer = random.choice(farmers)

            if d == "easy":
                templates = [
                    f"In basic agricultural chemistry, which term is defined as the {desc}?",
                    f"Select the chemical concept corresponding to: {desc}.",
                    f"What is the term for the {desc} in plant biochemistry?",
                    f"Name the concept accurately described as: {desc}.",
                    f"According to agricultural sciences, the {desc} is referred to as:"
                ]
            elif d == "medium":
                templates = [
                    f"During a soil analysis in {prov} for {farmer}'s {crop} crop, agronomists identify the {desc}. Which term identifies this?",
                    f"On a commercial farm in {prov}, technicians investigate the {desc} affecting {crop} growth. Identify the concept.",
                    f"When studying nutrient uptake in {crop} production, Farmer {farmer} reviews the {desc}. What is the correct term?",
                    f"An agricultural laboratory in {prov} evaluates {crop} tissue samples for the {desc}. Which term represents this?",
                    f"In modern South African farming, the practical significance of the {desc} in {crop} cultivation is known as:"
                ]
            else:
                templates = [
                    f"Evaluate the chemical mechanism where {desc} during intensive {crop} cultivation in {prov}. Which principle is represented?",
                    f"Analyze the soil chemistry data from {farmer}'s {crop} lands in {prov} exhibiting the {desc}. What is the scientific designation?",
                    f"In an advanced agronomic trial in {prov}, researchers determine the precise role of the {desc} in {crop} metabolism. Identify this entity.",
                    f"Critically assess the biochemical pathway characterized by the {desc} on {farmer}'s farm. Which concept applies?"
                ]

            q_text = random.choice(templates)
            if q_text in seen_texts:
                continue

            seen_texts.add(q_text)
            wrongs = [t for t in all_terms if t != term]
            random.shuffle(wrongs)

            q_obj = {
                "subtopic": sub,
                "difficulty": d,
                "question": q_text,
                "correct_answer": term,
                "wrong_answers_pool": wrongs[:8],
                "explanation": f"The correct answer is {term} because it refers to the {desc}."
            }
            current[d].append(q_obj)
            needed -= 1

def generate_agrisci11_chemistry():
    standardize_agrisci11_topic(
        filename="paper1_agri_chemistry.json",
        prefix="AGRI11_P1_CHEM",
        topic_name="Basic Agricultural Chemistry",
        paper="paper1",
        generator_func=synth_chemistry
    )

if __name__ == "__main__":
    generate_agrisci11_chemistry()
