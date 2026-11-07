import os
import sys
import random

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from agrisci11_common import standardize_agrisci11_topic

def synth_soil_science(current, targets, seen_texts, distractors, prefix, topic_name, paper):
    provinces = ["Free State", "Limpopo", "Mpumalanga", "North West", "Western Cape", "Eastern Cape", "KwaZulu-Natal", "Northern Cape"]
    crops = ["maize", "wheat", "sorghum", "sunflower", "soybean", "sugarcane", "canola", "cotton", "potatoes", "citrus"]
    farmers = ["Sipho", "Johan", "Lerato", "Kobus", "Zanele", "Thabo", "Devan", "Anke", "Pieter", "Nandi", "Lindiwe"]

    soil_pool = [
        ("Soil texture", "relative proportion of sand, silt, and clay mineral particles in a soil", "Soil texture and structure"),
        ("Soil structure", "aggregation or grouping of individual soil particles into larger clusters called peds", "Soil texture and structure"),
        ("Field capacity", "amount of water held in the soil after excess gravitational water has completely drained away", "Soil water, air and temperature"),
        ("Permanent wilting point", "soil water percentage at which plants wilt and can no longer extract sufficient moisture to recover", "Soil water, air and temperature"),
        ("Hygroscopic water", "thin film of water held tightly by molecular forces around soil particles that is unavailable to plants", "Soil water, air and temperature"),
        ("Capillary water", "water held in soil micropores against the pull of gravity available for plant uptake", "Soil water, air and temperature"),
        ("Gravitational water", "excess water occupying soil macropores that moves rapidly downward due to gravity", "Soil water, air and temperature"),
        ("Humus", "dark, amorphous organic residue formed by the deep decomposition of plant and animal residues", "Soil fertility and nutrients"),
        ("Cation Exchange Capacity (CEC)", "measure of the soil's capacity to retain and exchange essential positively charged nutrient ions", "Soil fertility and nutrients"),
        ("Soil salinization", "accumulation of soluble salts in the root zone impairing plant osmotic water uptake", "Soil pH and salinity"),
        ("Soil sodicity", "high concentration of exchangeable sodium ions on soil colloids causing dispersion and crusting", "Soil pH and salinity"),
        ("Gypsum (CaSO4)", "mineral amendment used to displace exchangeable sodium in sodic soils to improve soil structure", "Soil pH and salinity"),
        ("Contour ploughing", "tillage practice along lines of equal elevation across a slope to retard surface runoff and erosion", "Soil conservation"),
        ("Strip cropping", "growing alternating strips of erosion-susceptible row crops and dense cover crops across the slope", "Soil conservation"),
        ("Terracing", "constructing broad, stepped earth ridges on steep hillsides to reduce water runoff velocity", "Soil conservation"),
        ("Mulching", "layer of organic material applied over the soil surface to conserve moisture and suppress weeds", "Soil conservation"),
        ("Soil bulk density", "mass of oven-dry soil per unit total volume including solids and pore spaces", "Soil texture and structure"),
        ("Soil porosity", "percentage of total soil volume occupied by voids filled with air and water", "Soil water, air and temperature")
    ]

    all_terms = [s[0] for s in soil_pool]

    for d in ["easy", "medium", "hard"]:
        needed = targets[d] - len(current[d])
        counter = 0
        while needed > 0 and counter < 5000:
            counter += 1
            term, desc, sub = random.choice(soil_pool)
            prov = random.choice(provinces)
            crop = random.choice(crops)
            farmer = random.choice(farmers)

            if d == "easy":
                templates = [
                    f"In soil science, which concept is defined as the {desc}?",
                    f"Identify the soil property described as: {desc}.",
                    f"What is the term for the {desc}?",
                    f"Which parameter represents the {desc}?",
                    f"The term corresponding to the {desc} is:"
                ]
            elif d == "medium":
                templates = [
                    f"While conducting soil profiling in {prov} for {crop} farming, Farmer {farmer} examines the {desc}. What is this property?",
                    f"An agronomist in {prov} inspects field conditions affecting {crop} emergence and notes the {desc}. Identify the term.",
                    f"During a land capability evaluation in {prov}, extension officers assess the {desc}. Which concept describes this?",
                    f"On a commercial farm in {prov}, Farmer {farmer} monitors the {desc} to optimize irrigation for {crop}. Name this term."
                ]
            else:
                templates = [
                    f"Critically analyze the soil physical dynamics where the {desc} determines water movement under {crop} production in {prov}.",
                    f"Evaluate the pedological significance of the {desc} in mitigating land degradation on {farmer}'s farm in {prov}.",
                    f"In an advanced edaphological study in {prov}, researchers determine how the {desc} influences nutrient retention in {crop} soils."
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

def generate_agrisci11_soil_science():
    standardize_agrisci11_topic(
        filename="paper1_soil_science.json",
        prefix="AGRI11_P1_SOIL",
        topic_name="Soil Science",
        paper="paper1",
        generator_func=synth_soil_science
    )

if __name__ == "__main__":
    generate_agrisci11_soil_science()
