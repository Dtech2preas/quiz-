import os
import sys
import random

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from agrisci11_common import standardize_agrisci11_topic

def synth_resource_utilisation(current, targets, seen_texts, distractors, prefix, topic_name, paper):
    provinces = ["Free State", "Limpopo", "Mpumalanga", "North West", "Western Cape", "Eastern Cape", "KwaZulu-Natal", "Northern Cape"]
    crops = ["maize", "wheat", "sorghum", "sunflower", "soybean", "sugarcane", "canola", "cotton", "potatoes", "citrus", "lucerne"]
    farmers = ["Sipho", "Johan", "Lerato", "Kobus", "Zanele", "Thabo", "Devan", "Anke", "Pieter", "Nandi", "Lindiwe"]

    res_pool = [
        ("Drip irrigation", "low-pressure micro-irrigation system delivering water and dissolved nutrients directly to plant root zones", "Irrigation systems"),
        ("Center pivot irrigation", "mechanized overhead sprinkler irrigation system rotating around a central pivot point", "Irrigation systems"),
        ("Flood irrigation", "surface irrigation method where water is pumped or brought to the field and allowed to flow over the ground", "Irrigation systems"),
        ("Conservation agriculture", "farming system promoting minimal soil disturbance, permanent soil organic cover, and diversified crop rotations", "Sustainable farming practices"),
        ("Crop rotation", "practice of planting different crops sequentially on the same plot of land to break pest cycles and enhance soil health", "Soil cultivation and crop rotation"),
        ("Green manuring", "incorporation of undecomposed green plant tissue (usually legumes) into the soil to improve organic matter and fertility", "Soil cultivation and crop rotation"),
        ("Hydroponics", "technique of cultivating crops without soil in inert substrates using balanced mineral nutrient aqueous solutions", "Greenhouses, hydroponics, aquaculture"),
        ("Aquaponics", "closed-loop symbiotic system integrating conventional aquaculture (raising fish) with hydroponic plant cultivation", "Greenhouses, hydroponics, aquaculture"),
        ("Greenhouse cultivation", "controlled environment agriculture inside translucent structures to optimize temperature, humidity, and PAR light", "Greenhouses, hydroponics, aquaculture"),
        ("Precision agriculture", "management strategy using GNSS, remote sensing, and variable rate technology to optimize input efficiency", "Agricultural technology"),
        ("Drones (UAVs)", "unmanned aerial vehicles equipped with multispectral sensors for rapid crop health NDVI monitoring and targeted spraying", "Agricultural technology"),
        ("Variable Rate Technology (VRT)", "automated agricultural equipment dynamically adjusting fertilizer or seeding rates across field zones", "Agricultural technology"),
        ("Soil compaction", "densification of soil particles due to heavy tractor axle loads reducing macro-porosity and root elongation", "Soil cultivation and crop rotation"),
        ("Minimum tillage", "reduced tillage method that minimizes mechanical soil disturbance to preserve soil structure and earthworms", "Soil cultivation and crop rotation")
    ]

    all_terms = [r[0] for r in res_pool]

    for d in ["easy", "medium", "hard"]:
        needed = targets[d] - len(current[d])
        counter = 0
        while needed > 0 and counter < 5000:
            counter += 1
            term, desc, sub = random.choice(res_pool)
            prov = random.choice(provinces)
            crop = random.choice(crops)
            farmer = random.choice(farmers)

            if d == "easy":
                templates = [
                    f"In sustainable resource utilisation, which system or practice is defined as the {desc}?",
                    f"Identify the agricultural practice or technology described as: {desc}.",
                    f"What is the term for the {desc}?",
                    f"Which technological or management method corresponds to the {desc}?",
                    f"In modern farm resource management, the {desc} is called:"
                ]
            elif d == "medium":
                templates = [
                    f"Farmer {farmer} in {prov} upgrades their {crop} enterprise by implementing the {desc}. What is the name of this system?",
                    f"During a farm sustainability assessment in {prov}, evaluators inspect the {desc} used in {crop} production. Name the term.",
                    f"On a progressive commercial farm in {prov}, {farmer} adopts the {desc} to optimize water and energy use. Identify the practice.",
                    f"An agricultural engineering consultant in {prov} recommends the {desc} for intensive {crop} farming. Which option fits?"
                ]
            else:
                templates = [
                    f"Critically assess the resource efficiency and lifecycle impact where the {desc} is integrated into commercial {crop} farming in {prov}.",
                    f"Analyze the eco-hydrological impact of adopting the {desc} to address climate resilience on {farmer}'s farm in {prov}.",
                    f"In an advanced agro-ecological study in {prov}, researchers quantify the long-term carbon footprint when applying the {desc}."
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

def generate_agrisci11_resource_utilisation():
    standardize_agrisci11_topic(
        filename="paper2_resource_utilisation.json",
        prefix="AGRI11_P2_RES",
        topic_name="Sustainable Resource Utilisation",
        paper="paper2",
        generator_func=synth_resource_utilisation
    )

if __name__ == "__main__":
    generate_agrisci11_resource_utilisation()
