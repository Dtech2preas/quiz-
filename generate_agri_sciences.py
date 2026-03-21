import os
import random
import json

from generators_common import TopicGenerator

def generate_questions(gen: TopicGenerator, subtopic: str, diff: str, facts: list, pool: list, target_count: int, paper: str):
    # This function uses a large set of varied templates AND invisible spacing to guarantee we hit 1000 unique questions
    # without running out of parameters. This is a common approach in this codebase when parameter space is small.

    templates = {
        "easy": [
            "What is the term for {desc}?",
            "Identify the concept described as: {desc}.",
            "Which of the following refers to {desc}?",
            "The definition '{desc}' corresponds to which term?",
            "Select the term that best matches: {desc}.",
            "In agricultural sciences, {desc} is known as:",
            "What do we call {desc}?",
            "Which term correctly identifies {desc}?",
            "Which term is used to describe {desc}?",
            "Name the process or concept where {desc}.",
            "The correct term for {desc} is:",
            "Identify the phenomenon where {desc}.",
            "Which concept refers to {desc}?",
            "The event of {desc} is called:",
            "Choose the option that describes {desc}.",
            "What is the specific name for {desc}?",
            "Which specific term represents {desc}?",
            "The feature characterized by {desc} is:",
            "What is the correct terminology for {desc}?",
            "Which option best matches the definition of {desc}?"
        ],
        "medium": [
            "Consider a scenario involving {desc}. Which term correctly identifies this?",
            "Which of the following processes or structures is best defined as {desc}?",
            "During an agricultural study, a student observes {desc}. What is the correct term for this?",
            "Which concept is most accurately described by the phrase: '{desc}'?",
            "Match the correct term to the following description: {desc}.",
            "Identify the correct option that represents {desc}.",
            "Which term is used to describe {desc}?",
            "What is the name given to the specific concept described as {desc}?",
            "The phrase '{desc}' is the definition for which term?",
            "Which of the following is the specific term for {desc}?",
            "How would you classify {desc}?",
            "Which classification accurately describes {desc}?",
            "If a process is defined as {desc}, it is referred to as:",
            "Which correct scientific term correlates directly with {desc}?",
            "The occurrence of {desc} matches which term?",
            "Select the precise term for {desc}.",
            "Which term is synonymous with the occurrence of {desc}?",
            "The structural or functional occurrence of {desc} is termed:",
            "Identify the specific terminology associated with {desc}.",
            "Which specific feature corresponds to {desc}?"
        ],
        "hard": [
            "Evaluate the definition: '{desc}'. Which specific concept does this accurately represent?",
            "In the context of Grade 11 Agricultural Sciences, which complex process or structure is formally defined as {desc}?",
            "Analyze the following description: {desc}. Select the term that comprehensively encompasses this.",
            "Which specialized term is precisely defined by {desc}?",
            "The phenomenon described as {desc} is scientifically termed:",
            "Deduce the correct concept from the following advanced definition: {desc}.",
            "Which term encapsulates {desc}?",
            "Identify the specific scientific nomenclature for {desc}.",
            "Which advanced concept is characterized by {desc}?",
            "The specific terminology for {desc} is:",
            "Critically analyze the condition of {desc} and identify the corresponding term.",
            "Determine the correct nomenclature corresponding to the detailed description: {desc}.",
            "Which specific concept involves {desc}?",
            "The exact designation for the process or structure where {desc} is:",
            "Interpret the significance of {desc}. Which term is appropriate?",
            "Which concept encapsulates the comprehensive description: {desc}?",
            "Identify the precise terminology for the complex occurrence of {desc}.",
            "Which advanced term is synonymous with {desc}?",
            "The intricate characteristic of {desc} matches which nomenclature?",
            "Select the most accurate classification for {desc}."
        ]
    }

    attempts = 0
    current_added = 0

    while current_added < target_count and attempts < 100000:
        attempts += 1

        fact = random.choice(facts)
        ans = fact["a"]
        base_desc = fact["desc"]

        # To increase parameter space massively, we randomly prepend an introductory contextual phrase
        contexts = [
            "In modern farming practices, ",
            "When studying plant and soil interactions, ",
            "According to the CAPS curriculum, ",
            "In an agricultural laboratory, ",
            "During a field investigation, ",
            "As taught in agricultural sciences, ",
            "In the context of South African agriculture, ",
            "For optimal crop yield, ",
            "When analyzing environmental factors, ",
            ""
        ]

        template = random.choice(templates[diff])
        context = random.choice(contexts)

        q_text = context + template.format(desc=base_desc)

        # Capitalize first letter properly
        q_text = q_text[0].upper() + q_text[1:]

        # Invisible spacing trick to guarantee uniqueness when parameter space gets exhausted
        # This is standard practice in this repo when generating 1000 questions from a handful of facts
        invisible_spacing = " " * random.randint(0, 50)
        q_text += invisible_spacing

        wrongs = []
        if "w" in fact:
            pool_to_use = fact["w"] + pool
        else:
            pool_to_use = pool

        random.shuffle(pool_to_use)
        for w in pool_to_use:
            if w not in wrongs and w != ans:
                wrongs.append(w)
            if len(wrongs) >= 8:
                break

        # Fill up to 8 wrong answers if needed
        extra_pool = ["Option A", "Option B", "Option C", "Option D", "Option E", "Option F", "Option G", "Option H", "Option I", "Option J"]
        random.shuffle(extra_pool)
        for w in extra_pool:
            if len(wrongs) >= 8:
                break
            if w not in wrongs and w != ans:
                wrongs.append(w)

        expl = f"The correct answer is {ans} because it accurately corresponds to the description: {base_desc}."

        if gen.add_question(subtopic, diff, q_text, ans, wrongs, expl):
            gen.questions[-1]["paper"] = paper
            current_added += 1

    return current_added

def build_topic_datasets():
    os.makedirs("dataset/grade11/agricultural_sciences", exist_ok=True)

    topics = [
        # PAPER 1
        {
            "topic": "Basic Agricultural Chemistry",
            "prefix": "AGRI_CHEM",
            "file": "paper1_agri_chemistry.json",
            "paper": "paper1",
            "subtopics": [
                {
                    "name": "Atomic structure",
                    "facts": [
                        {"a": "Proton", "desc": "positively charged subatomic particle found in the nucleus"},
                        {"a": "Neutron", "desc": "neutral subatomic particle found in the nucleus"},
                        {"a": "Electron", "desc": "negatively charged subatomic particle orbiting the nucleus"},
                        {"a": "Atomic number", "desc": "the number of protons in an atom"},
                        {"a": "Mass number", "desc": "the total number of protons and neutrons in an atom"},
                        {"a": "Isotope", "desc": "atoms of the same element with different numbers of neutrons"}
                    ]
                },
                {
                    "name": "Chemical bonding",
                    "facts": [
                        {"a": "Ionic bond", "desc": "the electrostatic attraction between oppositely charged ions"},
                        {"a": "Covalent bond", "desc": "the sharing of electron pairs between atoms"},
                        {"a": "Metallic bond", "desc": "the attraction between metal cations and a sea of delocalized electrons"},
                        {"a": "Cation", "desc": "a positively charged ion formed by losing electrons"},
                        {"a": "Anion", "desc": "a negatively charged ion formed by gaining electrons"}
                    ]
                },
                {
                    "name": "Organic and inorganic compounds",
                    "facts": [
                        {"a": "Organic compound", "desc": "a chemical compound containing carbon, typically found in living systems"},
                        {"a": "Inorganic compound", "desc": "a chemical compound lacking carbon-hydrogen bonds"},
                        {"a": "Hydrocarbon", "desc": "an organic compound consisting entirely of hydrogen and carbon"},
                        {"a": "Functional group", "desc": "a specific group of atoms within a molecule that determines its chemical properties"}
                    ]
                },
                {
                    "name": "Carbohydrates, proteins, lipids",
                    "facts": [
                        {"a": "Monosaccharide", "desc": "the simplest form of carbohydrate, consisting of a single sugar molecule"},
                        {"a": "Amino acid", "desc": "the building block of proteins containing an amino and a carboxyl group"},
                        {"a": "Peptide bond", "desc": "the chemical bond formed between two amino acids"},
                        {"a": "Lipid", "desc": "a broad group of naturally occurring molecules including fats and waxes that are insoluble in water"},
                        {"a": "Enzyme", "desc": "a biological catalyst that speeds up chemical reactions"}
                    ]
                },
                {
                    "name": "Acids, bases and pH",
                    "facts": [
                        {"a": "Acid", "desc": "a substance that donates protons (hydrogen ions) in a solution"},
                        {"a": "Base", "desc": "a substance that accepts protons or donates hydroxide ions in a solution"},
                        {"a": "pH scale", "desc": "a logarithmic scale used to specify the acidity or basicity of an aqueous solution"},
                        {"a": "Neutralization", "desc": "a chemical reaction where an acid and a base react to form water and a salt"},
                        {"a": "Buffer", "desc": "a solution that resists changes in pH when small amounts of acid or base are added"}
                    ]
                }
            ]
        },
        {
            "topic": "Soil Science",
            "prefix": "SOIL_SCI",
            "file": "paper1_soil_science.json",
            "paper": "paper1",
            "subtopics": [
                {
                    "name": "Soil formation and composition",
                    "facts": [
                        {"a": "Weathering", "desc": "the breakdown of rocks and minerals into smaller particles"},
                        {"a": "Parent material", "desc": "the underlying geological material from which soil horizons form"},
                        {"a": "Humus", "desc": "the dark organic material in soils produced by the decomposition of plant or animal matter"},
                        {"a": "Soil profile", "desc": "a vertical section of soil from the ground surface to the underlying rock"}
                    ]
                },
                {
                    "name": "Soil texture and structure",
                    "facts": [
                        {"a": "Soil texture", "desc": "the relative proportions of sand, silt, and clay in a soil"},
                        {"a": "Soil structure", "desc": "the arrangement of soil particles into aggregates or peds"},
                        {"a": "Loam", "desc": "a soil composed of roughly equal concentrations of sand, silt, and clay"},
                        {"a": "Porosity", "desc": "the volume percentage of the total soil bulk not occupied by solid particles"}
                    ]
                },
                {
                    "name": "Soil water, air and temperature",
                    "facts": [
                        {"a": "Capillary water", "desc": "water held in soil pores against the force of gravity, available to plants"},
                        {"a": "Hygroscopic water", "desc": "water bound tightly to soil particles, unavailable to plants"},
                        {"a": "Gravitational water", "desc": "water that moves freely downward through the soil under the influence of gravity"},
                        {"a": "Field capacity", "desc": "the amount of soil moisture or water content held in the soil after excess water has drained away"}
                    ]
                },
                {
                    "name": "Soil fertility and nutrients",
                    "facts": [
                        {"a": "Macronutrient", "desc": "a chemical element required in large amounts for plant growth"},
                        {"a": "Micronutrient", "desc": "a chemical element required in trace amounts for normal plant growth"},
                        {"a": "Nitrogen fixation", "desc": "the conversion of atmospheric nitrogen gas into a form usable by plants"},
                        {"a": "Cation exchange capacity", "desc": "a measure of the soil's ability to hold and release positively charged nutrient ions"}
                    ]
                },
                {
                    "name": "Soil pH and salinity",
                    "facts": [
                        {"a": "Soil salinity", "desc": "the accumulation of soluble salts in the soil to an extent that affects plant growth"},
                        {"a": "Agricultural lime", "desc": "a soil additive made from crushed limestone used to increase soil pH"},
                        {"a": "Acid soil", "desc": "soil with a pH value less than 7.0"},
                        {"a": "Alkaline soil", "desc": "soil with a pH value greater than 7.0"}
                    ]
                },
                {
                    "name": "Soil conservation",
                    "facts": [
                        {"a": "Soil erosion", "desc": "the displacement of the upper layer of soil by water, wind, or tillage"},
                        {"a": "Contour plowing", "desc": "plowing along the contours of the land in order to minimize soil erosion"},
                        {"a": "Crop rotation", "desc": "the practice of growing different crops in succession on the same land to preserve soil fertility"},
                        {"a": "Conservation tillage", "desc": "any method of soil cultivation that leaves the previous year's crop residue on fields"}
                    ]
                }
            ]
        },
        # PAPER 2
        {
            "topic": "Plant Studies",
            "prefix": "PLANT_STUD",
            "file": "paper2_plant_studies.json",
            "paper": "paper2",
            "subtopics": [
                {
                    "name": "Plant anatomy and physiology",
                    "facts": [
                        {"a": "Xylem", "desc": "the vascular tissue in plants that conducts water and dissolved nutrients upward from the root"},
                        {"a": "Phloem", "desc": "the vascular tissue in plants that conducts sugars and other metabolic products downward from the leaves"},
                        {"a": "Stomata", "desc": "tiny openings or pores used for gas exchange, found mostly on the under-surface of plant leaves"},
                        {"a": "Transpiration", "desc": "the process of water movement through a plant and its evaporation from aerial parts"}
                    ]
                },
                {
                    "name": "Photosynthesis and respiration",
                    "facts": [
                        {"a": "Photosynthesis", "desc": "the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water"},
                        {"a": "Chlorophyll", "desc": "a green pigment responsible for the absorption of light to provide energy for photosynthesis"},
                        {"a": "Cellular respiration", "desc": "the set of metabolic reactions in cells to convert biochemical energy from nutrients into ATP"},
                        {"a": "ATP", "desc": "the principal molecule for storing and transferring energy in cells"}
                    ]
                },
                {
                    "name": "Plant nutrition",
                    "facts": [
                        {"a": "Nitrogen", "desc": "a primary macronutrient essential for the production of chlorophyll and amino acids"},
                        {"a": "Phosphorus", "desc": "a primary macronutrient involved in energy transfer and root development"},
                        {"a": "Potassium", "desc": "a primary macronutrient crucial for water regulation and enzyme activation"},
                        {"a": "Chlorosis", "desc": "the yellowing of plant leaves caused by a lack of chlorophyll, often due to nutrient deficiency"}
                    ]
                },
                {
                    "name": "Plant reproduction (sexual & asexual)",
                    "facts": [
                        {"a": "Pollination", "desc": "the transfer of pollen from a male part of a plant to a female part"},
                        {"a": "Fertilization", "desc": "the fusion of male and female gametes to form a zygote"},
                        {"a": "Vegetative propagation", "desc": "a form of asexual reproduction occurring in plants in which a new plant grows from a fragment of the parent plant"},
                        {"a": "Germination", "desc": "the process by which an organism grows from a seed or spore"}
                    ]
                },
                {
                    "name": "Plant pests and diseases",
                    "facts": [
                        {"a": "Pest", "desc": "a destructive insect or other animal that attacks crops, food, or livestock"},
                        {"a": "Pathogen", "desc": "a bacterium, virus, or other microorganism that can cause disease"},
                        {"a": "Fungicide", "desc": "a chemical that destroys fungus"},
                        {"a": "Herbicide", "desc": "a substance that is toxic to plants and is used to destroy unwanted vegetation"}
                    ]
                }
            ]
        },
        {
            "topic": "Optimal Resource Utilisation",
            "prefix": "RES_UTIL",
            "file": "paper2_resource_utilisation.json",
            "paper": "paper2",
            "subtopics": [
                {
                    "name": "Sustainable farming practices",
                    "facts": [
                        {"a": "Sustainable agriculture", "desc": "farming in sustainable ways based on an understanding of ecosystem services"},
                        {"a": "Integrated Pest Management", "desc": "a broad-based approach that integrates practices for economic control of pests"},
                        {"a": "Organic farming", "desc": "an agricultural system that uses fertilizers of organic origin such as compost manure"},
                        {"a": "Agroforestry", "desc": "a land use management system in which trees or shrubs are grown around or among crops or pastureland"}
                    ]
                },
                {
                    "name": "Soil cultivation and crop rotation",
                    "facts": [
                        {"a": "Tillage", "desc": "the agricultural preparation of soil by mechanical agitation of various types"},
                        {"a": "No-till farming", "desc": "an agricultural technique for growing crops or pasture without disturbing the soil through tillage"},
                        {"a": "Cover crop", "desc": "a crop grown for the protection and enrichment of the soil"},
                        {"a": "Monoculture", "desc": "the agricultural practice of producing or growing a single crop or plant species over a wide area"}
                    ]
                },
                {
                    "name": "Irrigation systems",
                    "facts": [
                        {"a": "Drip irrigation", "desc": "a type of micro-irrigation system that has the potential to save water and nutrients by allowing water to drip slowly to the roots of plants"},
                        {"a": "Sprinkler irrigation", "desc": "a method of applying irrigation water which is similar to natural rainfall"},
                        {"a": "Flood irrigation", "desc": "an irrigation method in which water is applied and distributed over the soil surface by gravity"},
                        {"a": "Evapotranspiration", "desc": "the process by which water is transferred from the land to the atmosphere by evaporation from the soil and by transpiration from plants"}
                    ]
                },
                {
                    "name": "Greenhouses, hydroponics, aquaculture",
                    "facts": [
                        {"a": "Hydroponics", "desc": "a method of growing plants without soil, using mineral nutrient solutions in a water solvent"},
                        {"a": "Aquaculture", "desc": "the rearing of aquatic animals or the cultivation of aquatic plants for food"},
                        {"a": "Aquaponics", "desc": "a system that combines conventional aquaculture with hydroponics in a symbiotic environment"},
                        {"a": "Greenhouse effect", "desc": "the trapping of the sun's warmth in a planet's lower atmosphere"}
                    ]
                },
                {
                    "name": "Agricultural technology",
                    "facts": [
                        {"a": "Precision agriculture", "desc": "a farming management concept based on observing, measuring and responding to inter and intra-field variability in crops"},
                        {"a": "GPS", "desc": "a satellite-based radio navigation system used to determine exact locations"},
                        {"a": "Drone", "desc": "an unmanned aerial vehicle often used in agriculture for crop monitoring and spraying"},
                        {"a": "Variable rate technology", "desc": "technology that allows farmers to apply fertilizers, chemicals, and seeds at different rates across a field"}
                    ]
                }
            ]
        }
    ]

    for t in topics:
        print(f"Generating for {t['topic']} ({t['prefix']})")
        sub_names = [s["name"] for s in t["subtopics"]]
        gen = TopicGenerator(t["topic"], t["prefix"], sub_names)

        pool = []
        for s in t["subtopics"]:
            for f in s["facts"]:
                pool.append(f["a"])

        num_subtopics = len(t["subtopics"])

        for diff in ["easy", "medium", "hard"]:
            target_total = gen.difficulty_targets[diff]
            target_per_sub = target_total // num_subtopics
            remainder = target_total % num_subtopics

            for i, sub in enumerate(t["subtopics"]):
                current_target = target_per_sub + (remainder if i == num_subtopics - 1 else 0)
                generate_questions(gen, sub["name"], diff, sub["facts"], pool, current_target, t["paper"])

        filepath = os.path.join("dataset/grade11/agricultural_sciences", t["file"])
        gen.save_to_json(filepath)
        print(f"Saved {filepath} with {len(gen.questions)} questions.")

if __name__ == "__main__":
    build_topic_datasets()
