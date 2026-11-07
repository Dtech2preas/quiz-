import os
import sys
import random

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from agrisci11_common import standardize_agrisci11_topic

def synth_plant_studies(current, targets, seen_texts, distractors, prefix, topic_name, paper):
    provinces = ["Free State", "Limpopo", "Mpumalanga", "North West", "Western Cape", "Eastern Cape", "KwaZulu-Natal"]
    crops = ["maize", "wheat", "sorghum", "sunflower", "soybean", "sugarcane", "canola", "cotton", "potatoes", "citrus", "apples"]
    farmers = ["Sipho", "Johan", "Lerato", "Kobus", "Zanele", "Thabo", "Devan", "Anke", "Pieter", "Nandi", "Lindiwe"]

    plant_pool = [
        ("Xylem", "vascular tissue responsible for the upward transport of water and dissolved minerals from roots to shoots", "Plant anatomy and physiology"),
        ("Phloem", "vascular tissue conducting photosynthesized sugars and organic solutes bidirectionally throughout the plant", "Plant anatomy and physiology"),
        ("Stomata", "microscopic pore complexes on leaf surfaces regulated by guard cells for gas exchange and transpiration", "Plant anatomy and physiology"),
        ("Transpiration", "evaporative loss of water vapor from aerial plant surfaces primarily through stomatal apertures", "Plant anatomy and physiology"),
        ("Photosynthesis", "light-driven biochemical synthesis of carbohydrates from carbon dioxide and water with oxygen release", "Photosynthesis and respiration"),
        ("Cellular respiration", "metabolic oxidation of glucose yielding adenosine triphosphate (ATP), water, and carbon dioxide", "Photosynthesis and respiration"),
        ("Chlorophyll", "green photosynthetic pigment embedded in thylakoid membranes absorbing blue and red light spectra", "Photosynthesis and respiration"),
        ("Nitrogen (N)", "essential macronutrient vital for vegetative development, amino acid synthesis, and chlorophyll structure", "Plant nutrition"),
        ("Phosphorus (P)", "essential macronutrient critical for ATP energy transfer, nucleic acids, and vigorous root expansion", "Plant nutrition"),
        ("Potassium (K)", "macronutrient that regulates stomatal aperture mechanisms, osmotic potential, and enzyme activation", "Plant nutrition"),
        ("Pollination", "transfer of pollen grains from the male anther to the receptive female stigma in angiosperms", "Plant reproduction (sexual & asexual)"),
        ("Grafting", "horticultural technique uniting a scion shoot with a compatible rootstock to grow as a unified plant", "Plant reproduction (sexual & asexual)"),
        ("Integrated Pest Management (IPM)", "holistic crop protection strategy combining biological, cultural, physical, and chemical controls", "Plant pests and diseases"),
        ("Aphids", "phloem-sap sucking insect vectors capable of transmitting viral pathogens across crop monocultures", "Plant pests and diseases"),
        ("Fungicide", "chemical or bio-pesticide formulated to eradicate or inhibit fungal spores and mycelial growth", "Plant pests and diseases")
    ]

    all_terms = [p[0] for p in plant_pool]

    for d in ["easy", "medium", "hard"]:
        needed = targets[d] - len(current[d])
        counter = 0
        while needed > 0 and counter < 5000:
            counter += 1
            term, desc, sub = random.choice(plant_pool)
            prov = random.choice(provinces)
            crop = random.choice(crops)
            farmer = random.choice(farmers)

            if d == "easy":
                templates = [
                    f"In plant studies, which term designates the {desc}?",
                    f"Identify the plant structure or physiological process described as: {desc}.",
                    f"What is the term for the {desc}?",
                    f"Which physiological component corresponds to the {desc}?",
                    f"In crop botany, the {desc} is formally termed:"
                ]
            elif d == "medium":
                templates = [
                    f"In an orchard in {prov}, Farmer {farmer} inspects {crop} trees and observes the {desc}. Which term identifies this?",
                    f"During a crop scouting session in {prov}, agronomists evaluate the {desc} in {crop} development. Name this concept.",
                    f"On an irrigated farm in {prov}, extension staff investigate the {desc} impacting {crop} yield. What is the correct term?",
                    f"A greenhouse horticulturist in {prov} manages {crop} growth by monitoring the {desc}. Identify the term."
                ]
            else:
                templates = [
                    f"Critically analyze the physiological mechanism where the {desc} governs dry matter partitioning in {crop} under heat stress in {prov}.",
                    f"Evaluate the pathological significance of the {desc} in designing biosecurity protocols for {crop} orchards in {prov}.",
                    f"In an advanced plant physiology investigation in {prov}, researchers quantify how the {desc} affects overall harvest index in {crop}."
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

def generate_agrisci11_plant_studies():
    standardize_agrisci11_topic(
        filename="paper2_plant_studies.json",
        prefix="AGRI11_P2_PLANT",
        topic_name="Plant Studies",
        paper="paper2",
        generator_func=synth_plant_studies
    )

if __name__ == "__main__":
    generate_agrisci11_plant_studies()
