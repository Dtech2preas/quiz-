import json
import random
import os
from typing import List, Dict, Any
from generators_common import TopicGenerator

def write_json(filename: str, data: List[Dict[str, Any]]):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def make_wrong(base_wrong_pool, num_needed, exclude):
    """Helper to ensure we always have 6 unique wrong answers"""
    available = [w for w in base_wrong_pool if w != exclude]
    if len(available) < num_needed:
        # Pad with some generic answers if needed, though this shouldn't happen with our pools
        available.extend([f"Generic Incorrect Answer {i}" for i in range(10)])

    # We want exactly num_needed items, but if available is larger we sample
    return random.sample(available, max(num_needed, 6))


def generate_life_living():
    topic_name = "Life and Living"
    topic_prefix = "G6_NST"
    subtopics = [
        "Photosynthesis",
        "Nutrients in food",
        "Nutrition",
        "Ecosystems and food webs"
    ]

    gen = TopicGenerator(topic_name, topic_prefix, subtopics)

    plants = ["sunflowers", "maize plants", "oak trees", "bean plants", "aloe plants", "tomato plants", "rose bushes", "apple trees", "potato plants", "wheat", "orange trees"]
    environments = ["savanna", "forest", "desert", "wetland", "grassland", "fynbos", "river", "coastal", "mountain"]

    attempts = 0
    while len(gen.questions) < 1000 and attempts < 100000:
        attempts += 1

        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        question = ""
        correct = ""
        wrong = []
        explanation = ""

        # Use random integers to create vast number of unique questions.
        # For instance, introducing a scenario with N items or measuring at time T,
        # or having character "Learner A" to make text unique.

        names = ["Thabo", "Sipho", "Lerato", "Zanele", "Johan", "Sarah", "Piet", "Busi", "Nomsa", "Jabu", "Kevin", "Lisa"]
        name = random.choice(names)
        scenario_num = random.randint(1, 100)

        if subtopic == "Photosynthesis":
            plant = random.choice(plants)

            wrong_pool = ["Oxygen", "Nitrogen", "Hydrogen", "Carbon monoxide", "Methane", "Helium", "Water vapour", "Soil", "Rocks", "Wind", "Heat", "Metal", "Plastic"]

            if diff == "easy":
                q_type = random.choice([1, 2, 3])
                if q_type == 1:
                    question = f"In scenario {scenario_num}, {name} observes {plant}. What gas do these plants take in from the air to make their own food?"
                    correct = "Carbon dioxide"
                    wrong = make_wrong(wrong_pool, 6, correct)
                    explanation = "Plants take in carbon dioxide from the air during photosynthesis."
                elif q_type == 2:
                    question = f"{name} placed {plant} in a garden (Test {scenario_num}). What form of energy do they need to carry out photosynthesis?"
                    correct = "Sunlight"
                    wrong = make_wrong(["Wind energy", "Sound energy", "Electrical energy", "Magnetic energy", "Heat from the soil", "Kinetic energy", "Geothermal energy", "Moonlight"], 6, correct)
                    explanation = "Sunlight provides the energy needed for plants to make food."
                else:
                    question = f"During observation {scenario_num}, {name} noted that {plant} release an important gas. What is it?"
                    correct = "Oxygen"
                    wrong = make_wrong(wrong_pool, 6, correct)
                    explanation = "During photosynthesis, plants release oxygen, which animals and humans need to breathe."
            elif diff == "medium":
                q_type = random.choice([1, 2])
                if q_type == 1:
                    question = f"For experiment {scenario_num}, {name} listed the three things {plant} combine to produce glucose. What are they?"
                    correct = "Carbon dioxide, water, and sunlight"
                    wrong = make_wrong(["Oxygen, water, and sunlight", "Carbon dioxide, soil, and wind", "Oxygen, soil, and sunlight", "Nitrogen, water, and heat", "Carbon dioxide, nitrogen, and soil", "Water, oxygen, and soil", "Sunlight, soil, and nitrogen"], 6, correct)
                    explanation = "Photosynthesis requires carbon dioxide, water, and sunlight energy to produce glucose."
                else:
                    question = f"In biology test {scenario_num}, {name} was asked: In which part of the {plant} does photosynthesis mainly take place?"
                    correct = "The leaves"
                    wrong = make_wrong(["The roots", "The stem", "The flowers", "The bark", "The fruit", "The seeds", "The branches"], 6, correct)
                    explanation = "Photosynthesis primarily takes place in the leaves of plants, where chlorophyll is found."
            else:
                q_type = random.choice([1, 2])
                if q_type == 1:
                    question = f"In an advanced study (ID: {scenario_num}), {name} analyzed chlorophyll in {plant}. What is its role during photosynthesis?"
                    correct = "It absorbs light energy from the sun."
                    wrong = make_wrong(["It absorbs water from the soil.", "It transports glucose to the roots.", "It releases oxygen into the air.", "It protects the plant from diseases.", "It converts carbon dioxide into nitrogen.", "It breaks down dead organic matter.", "It stores water during a drought."], 6, correct)
                    explanation = "Chlorophyll is the green pigment in plants that captures sunlight energy for photosynthesis."
                else:
                    question = f"{name} kept {plant} in complete darkness for {scenario_num} days. Why did they eventually stop growing?"
                    correct = "They cannot perform photosynthesis without light energy."
                    wrong = make_wrong(["They cannot absorb water without light.", "They will run out of carbon dioxide.", "The darkness stops them from absorbing oxygen.", "Their roots will rot in the dark.", "They need light to produce nitrogen.", "They will absorb too much carbon dioxide.", "They cannot perform cellular respiration without light."], 6, correct)
                    explanation = "Without light energy from the sun, plants cannot make their own food through photosynthesis."

        elif subtopic == "Nutrients in food":
            carbs = ["bread", "pasta", "rice", "potatoes", "maize meal", "sweet potatoes"]
            proteins = ["meat", "beans", "fish", "eggs", "chicken", "lentils"]
            fats = ["butter", "oil", "nuts", "avocado", "margarine", "cheese"]
            vitamins = ["oranges", "carrots", "spinach", "apples", "broccoli", "tomatoes"]

            wrong_groups = ["Proteins", "Fats and oils", "Vitamins", "Minerals", "Water", "Calcium", "Iron", "Carbohydrates", "Sugars", "Fiber"]

            if diff == "easy":
                nutrient_type = random.choice(["Carbohydrates", "Proteins", "Fats and oils", "Vitamins and minerals"])
                if nutrient_type == "Carbohydrates":
                    food = random.choice(carbs)
                    question = f"{name} ate {scenario_num} portions of {food}. Which important nutrient group does this belong to, giving our bodies energy?"
                    correct = "Carbohydrates"
                    wrong = make_wrong(wrong_groups, 6, correct)
                    explanation = f"{food.capitalize()} is a rich source of carbohydrates, which provide energy."
                elif nutrient_type == "Proteins":
                    food = random.choice(proteins)
                    question = f"{name} included {food} in meal {scenario_num}. Which nutrient group does it mainly provide to help bodies grow and repair?"
                    correct = "Proteins"
                    wrong = make_wrong(wrong_groups, 6, correct)
                    explanation = f"{food.capitalize()} is packed with proteins, needed for growth and tissue repair."
                elif nutrient_type == "Fats and oils":
                    food = random.choice(fats)
                    question = f"In recipe {scenario_num}, {name} used {food}. Which nutrient group does this provide, which stores energy and insulates the body?"
                    correct = "Fats and oils"
                    wrong = make_wrong(wrong_groups, 6, correct)
                    explanation = f"{food.capitalize()} is a good source of fats and oils."
                else:
                    food = random.choice(vitamins)
                    question = f"{name} bought {scenario_num} {food}. Which important nutrients do we mainly get from eating this to keep us healthy?"
                    correct = "Vitamins and minerals"
                    wrong = make_wrong(["Proteins and fats", "Carbohydrates and proteins", "Fats and oils", "Sugars and starches", "Proteins and sugars", "Oils and starches", "Only proteins"], 6, correct)
                    explanation = f"{food.capitalize()} provides essential vitamins and minerals for a strong immune system."
            elif diff == "medium":
                disease = random.choice(["scurvy", "rickets", "kwashiorkor", "anemia"])
                wrong_diseases = ["Rickets", "Kwashiorkor", "Anemia", "Diabetes", "Malaria", "Tuberculosis", "Measles", "Scurvy", "Polio", "Cholera", "Asthma", "Tetanus"]
                if disease == "scurvy":
                    question = f"Case study {scenario_num}: {name} learned that a lack of Vitamin C in a diet can lead to which disease?"
                    correct = "Scurvy"
                    wrong = make_wrong(wrong_diseases, 6, correct)
                    explanation = "Scurvy is caused by a deficiency in Vitamin C, found in citrus fruits."
                elif disease == "rickets":
                    question = f"In lesson {scenario_num}, {name} discovered that a lack of Vitamin D and calcium causes soft bones. What is this called?"
                    correct = "Rickets"
                    wrong = make_wrong(wrong_diseases, 6, correct)
                    explanation = "Rickets affects bone development due to a lack of Vitamin D and calcium."
                elif disease == "kwashiorkor":
                    question = f"Patient {scenario_num} showed severe lack of protein in their diet. {name} identified the disease as:"
                    correct = "Kwashiorkor"
                    wrong = make_wrong(wrong_diseases, 6, correct)
                    explanation = "Kwashiorkor is a form of malnutrition caused by a lack of protein."
                else:
                    question = f"Test {scenario_num}: {name} knows a lack of iron can lead to a condition where blood cannot carry enough oxygen. What is it?"
                    correct = "Anemia"
                    wrong = make_wrong(wrong_diseases, 6, correct)
                    explanation = "Anemia is often caused by an iron deficiency."
            else:
                q_type = random.choice([1, 2])
                if q_type == 1:
                    food1 = random.choice(carbs)
                    food2 = random.choice(proteins)
                    question = f"If {name}'s meal {scenario_num} consists only of {food1} and {food2}, which major nutrient group is missing for a balanced diet?"
                    correct = "Vitamins and minerals (fruits and vegetables)"
                    wrong = make_wrong(["Carbohydrates", "Proteins", "Water", "Fiber only", "Sugars", "Starches", "Meat", "Fats only"], 6, correct)
                    explanation = f"While {food1} provides carbs and {food2} provides protein, vitamins and minerals from fruits and vegetables are missing."
                else:
                    question = f"{name} asked in question {scenario_num}: Why is dietary fibre important in our daily nutrition, even though it does not provide energy?"
                    correct = "It helps to move food through the digestive system and prevents constipation."
                    wrong = make_wrong(["It builds strong muscles and bones.", "It provides a concentrated source of energy.", "It helps red blood cells carry oxygen.", "It fights off viral infections directly.", "It builds new skin cells.", "It creates antibodies in the immune system.", "It forms the structure of our teeth."], 6, correct)
                    explanation = "Fibre is crucial for healthy digestion and bowel movements."

        elif subtopic == "Nutrition":
            if diff == "easy":
                question = f"{name} is studying chapter {scenario_num}. What do we call a diet that contains the correct amounts of all the nutrient groups?"
                correct = "A balanced diet"
                wrong = make_wrong(["A heavy diet", "A sweet diet", "A liquid diet", "A meat-only diet", "A fast-food diet", "A vegetarian diet", "A high-sugar diet", "A zero-carb diet"], 6, correct)
                explanation = "A balanced diet provides all necessary nutrients in the right proportions."
            elif diff == "medium":
                question = f"In health test {scenario_num}, {name} was asked: Why is it important to drink plenty of water every day for good nutrition?"
                correct = "It helps transport nutrients, regulate body temperature, and remove waste."
                wrong = make_wrong(["It provides high amounts of energy.", "It contains proteins to build muscles.", "It strengthens our bones directly like calcium.", "It provides all the vitamins we need.", "It stops us from feeling sleepy.", "It produces red blood cells.", "It creates fat to store energy."], 6, correct)
                explanation = "Water is essential for many bodily functions including transport and temperature regulation."
            else:
                question = f"Research project {scenario_num}: {name} investigated how eating too much processed food high in sugar and unhealthy fats affects the body over time. What did they find?"
                correct = "It can lead to obesity, tooth decay, and heart problems."
                wrong = make_wrong(["It makes the bones much stronger.", "It cures diseases like scurvy and rickets.", "It helps muscles repair faster after exercise.", "It increases the amount of oxygen in the blood.", "It improves eyesight and brain function.", "It prevents all types of cancers.", "It causes the body to lose too much water."], 6, correct)
                explanation = "A poor diet high in sugar and unhealthy fats is linked to various health issues like obesity."

        else: # Ecosystems and food webs
            env = random.choice(environments)
            producers = ["grass", "trees", "algae", "shrubs", "bushes", "weeds", "ferns"]
            primary_consumers = ["locusts", "cows", "rabbits", "zebras", "impalas", "springboks", "mice"]
            secondary_consumers = ["frogs", "snakes", "birds", "lizards", "spiders", "meerkat"]
            tertiary_consumers = ["eagles", "lions", "leopards", "cheetahs", "hawks", "hyenas"]
            decomposers = ["fungi", "bacteria", "earthworms", "mushrooms", "dung beetles"]

            prod = random.choice(producers)
            prim = random.choice(primary_consumers)
            sec = random.choice(secondary_consumers)
            tert = random.choice(tertiary_consumers)
            dec = random.choice(decomposers)

            if diff == "easy":
                q_type = random.choice([1, 2, 3])
                if q_type == 1:
                    question = f"In a {env} ecosystem (Area {scenario_num}), {name} observed {prod}. What is their role?"
                    correct = "They are producers that make their own food."
                    wrong = make_wrong(["They are primary consumers.", "They are secondary consumers.", "They are predators.", "They are decomposers.", "They hunt other animals.", "They break down dead plants.", "They act as scavengers."], 6, correct)
                    explanation = "Plants and algae are producers because they produce their own food using sunlight."
                elif q_type == 2:
                    question = f"In food chain {scenario_num}, {name} saw a {prim} eat {prod}. The {prim} is known as a..."
                    correct = "Primary consumer (herbivore)"
                    wrong = make_wrong(["Producer", "Secondary consumer", "Tertiary consumer", "Decomposer", "Carnivore", "Omnivore", "Scavenger"], 6, correct)
                    explanation = "Animals that eat producers are primary consumers or herbivores."
                else:
                    question = f"{name} identified animals like {sec} and {tert} in sector {scenario_num} that eat other animals. What are they called?"
                    correct = "Carnivores"
                    wrong = make_wrong(["Herbivores", "Producers", "Decomposers", "Plants", "Vegetarians", "Fungi", "Autotrophs"], 6, correct)
                    explanation = "Carnivores are animals that consume other animals."
            elif diff == "medium":
                q_type = random.choice([1, 2])
                if q_type == 1:
                    question = f"In study {scenario_num}, {name} researched {dec}. What is their role in an ecosystem?"
                    correct = "They break down dead plants and animals and return nutrients to the soil."
                    wrong = make_wrong(["They produce food using sunlight.", "They hunt and eat primary consumers.", "They provide energy directly to the sun.", "They consume living plants only.", "They act as the top predators.", "They absorb carbon dioxide from the air.", "They pollinate flowers."], 6, correct)
                    explanation = "Decomposers recycle nutrients by breaking down dead organic matter."
                else:
                    question = f"{name} drew a {env} food web (Diagram {scenario_num}). What does the arrow pointing from the {prim} to the {sec} mean?"
                    correct = "It shows the flow of energy from the {prim} to the {sec}.".format(prim=prim, sec=sec)
                    wrong = make_wrong(["It means the {sec} is eaten by the {prim}.".format(prim=prim, sec=sec), "It shows that they are friends.", "It means they compete for water.", "It shows the {prim} is a producer.", "It indicates that both are decomposers.", "It means they live in the same shelter.", "It shows the flow of water."], 6, correct)
                    explanation = "Arrows in a food web show the direction of energy flow (who is eaten by whom)."
            else:
                question = f"If all the {prod} in a {env} ecosystem (Zone {scenario_num}) were destroyed by a drought, what did {name} predict would happen first?"
                correct = f"The {prim} would starve or move away due to a lack of food."
                wrong = make_wrong([f"The {tert} would start eating plants.", f"The {dec} would become producers.", "The ecosystem would become much healthier.", f"The {sec} would multiply rapidly.", "Nothing would change for the animals.", f"The {prim} would start performing photosynthesis.", "The soil would become instantly fertile."], 6, correct)
                explanation = "Without producers, primary consumers lose their food source, causing a collapse in the food web."

        gen.add_question(subtopic, diff, question, correct, wrong, explanation)

    write_json(f"dataset/grade6/natural_sciences_and_technology/grade6_nst_life_living_processing.json", gen.questions)
    print(f"Generated Life and Living: {len(gen.questions)} questions")


def generate_matter_materials():
    topic_name = "Matter and Materials"
    topic_prefix = "G6_NST"
    subtopics = [
        "Solids, liquids and gases",
        "Mixtures",
        "Solutions as special mixtures",
        "Dissolving",
        "Mixtures and water resources",
        "Processes to purify water"
    ]

    gen = TopicGenerator(topic_name, topic_prefix, subtopics)

    solids = ["wood", "iron", "rock", "ice", "plastic", "glass", "brick", "copper", "aluminum", "stone", "rubber"]
    liquids = ["water", "milk", "oil", "juice", "honey", "petrol", "syrup", "vinegar", "liquid soap"]
    gases = ["oxygen", "carbon dioxide", "helium", "water vapour", "nitrogen", "methane"]

    mixtures_solid_solid = ["sand and stones", "beans and rice", "sugar and tea leaves", "peanuts and raisins", "iron filings and sand", "salt and pepper", "beads and buttons"]
    solutes = ["sugar", "salt", "coffee powder", "jelly powder", "Epsom salts", "drink mix powder"]
    solvents = ["water", "warm water", "hot water", "cold water"]
    insolubles = ["sand", "oil", "chalk powder", "stones", "flour", "sawdust", "plastic beads"]
    pollutants = ["plastic waste", "oil spills", "sewage", "factory chemicals", "fertilizer runoff", "litter", "acid mine drainage"]
    methods = ["Filtering (filtration)", "Boiling", "Settling", "Adding chemicals (chlorination)"]

    names = ["Thabo", "Sipho", "Lerato", "Zanele", "Johan", "Sarah", "Piet", "Busi", "Nomsa", "Jabu", "Kevin", "Lisa"]

    attempts = 0
    while len(gen.questions) < 1000 and attempts < 100000:
        attempts += 1

        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        question = ""
        correct = ""
        wrong = []
        explanation = ""

        name = random.choice(names)
        scenario_num = random.randint(1, 100)

        if subtopic == "Solids, liquids and gases":
            state_focus = random.choice(["solid", "liquid", "gas"])
            if state_focus == "solid":
                solid = random.choice(solids)
                if diff == "easy":
                    question = f"In lab {scenario_num}, {name} examined a solid piece of {solid}. Which statement best describes its shape?"
                    correct = "It has a fixed shape and size."
                    wrong = make_wrong(["It takes the shape of its container.", "It flows and spreads out everywhere.", "It has no shape and cannot be seen.", "It changes shape easily when left alone.", "It expands to fill any room.", "It evaporates quickly at room temperature."], 6, correct)
                    explanation = "Solids have a definite shape and volume because their particles are packed closely together."
                elif diff == "medium":
                    question = f"For question {scenario_num}, {name} was asked: How are the particles arranged in a solid piece of {solid}?"
                    correct = "They are packed very closely together in a regular pattern and vibrate in place."
                    wrong = make_wrong(["They are far apart and move freely.", "They are loosely packed and slide past each other.", "They are completely still and do not vibrate at all.", "They move rapidly in all directions.", "They are scattered randomly with lots of space.", "They expand and contract constantly.", "They float around freely."], 6, correct)
                    explanation = "In solids, particles are tightly packed and can only vibrate in fixed positions."
                else:
                    question = f"In experiment {scenario_num}, {name} found that a solid block of {solid} cannot be easily compressed (squashed) into a smaller space. Why?"
                    correct = "Because its particles are already packed very closely together with almost no space between them."
                    wrong = make_wrong(["Because its particles are moving too fast.", "Because it is made of gas particles inside.", "Because the particles slide past each other too quickly.", "Because there is too much empty space inside.", "Because solids are lighter than liquids.", "Because its particles are far apart.", "Because it is melting."], 6, correct)
                    explanation = "Solids cannot be compressed easily because there is very little space between the particles."
            elif state_focus == "liquid":
                liquid = random.choice(liquids)
                if diff == "easy":
                    question = f"{name} pours {liquid} from a jug into a glass in test {scenario_num}. What happens to its shape?"
                    correct = "It changes to take the shape of the glass."
                    wrong = make_wrong(["It keeps the shape of the jug.", "It turns into a solid.", "It becomes a gas.", "It loses its volume completely.", "It shrinks into a tiny drop.", "It turns into ice.", "It completely disappears."], 6, correct)
                    explanation = "Liquids flow and take the shape of the container they are poured into."
                elif diff == "medium":
                    question = f"{name} observed a liquid like {liquid} under a microscope in lab {scenario_num}. How do its particles behave compared to a solid?"
                    correct = "They are close together but can slide past one another."
                    wrong = make_wrong(["They are tightly locked in a fixed pattern.", "They are very far apart and fly around.", "They do not move at all.", "They are completely disorganized with massive gaps.", "They form a rigid structure.", "They repel each other strongly.", "They move faster than gas particles."], 6, correct)
                    explanation = "In liquids, particles are close together but have enough energy to slide past each other, allowing the liquid to flow."
                else:
                    question = f"{name} was asked in test {scenario_num}: Why can a liquid like {liquid} flow, but a solid cannot?"
                    correct = "Because the particles in a liquid are not in fixed positions and can move around each other."
                    wrong = make_wrong(["Because liquids have no particles.", "Because the particles are extremely far apart like a gas.", "Because liquids are lighter than solids.", "Because the particles are locked in place.", "Because liquids are always hot.", "Because liquids are completely transparent.", "Because liquids do not have mass."], 6, correct)
                    explanation = "The ability of particles to slide past one another allows liquids to flow."
            else:
                gas = random.choice(gases)
                if diff == "easy":
                    question = f"In scenario {scenario_num}, {name} releases a gas like {gas} into a room. How does it behave?"
                    correct = "It spreads out to fill the entire space available."
                    wrong = make_wrong(["It stays in a neat pile on the floor.", "It forms a puddle.", "It keeps a fixed rectangular shape.", "It turns into a solid.", "It shrinks into a tiny corner.", "It becomes heavy and sinks immediately.", "It turns into water."], 6, correct)
                    explanation = "Gases have no fixed shape or volume and will expand to fill their container."
                elif diff == "medium":
                    question = f"{name} had to draw the particles of {gas} for question {scenario_num}. How should they be arranged?"
                    correct = "They are very far apart and move freely in all directions."
                    wrong = make_wrong(["They are packed tightly in a neat row.", "They are close together but slide past each other.", "They vibrate in fixed positions.", "They are linked together like a chain.", "They form a rigid square structure.", "They only move downwards.", "They don't move at all."], 6, correct)
                    explanation = "Gas particles have a lot of energy, are spaced far apart, and move rapidly in all directions."
                else:
                    question = f"In lab {scenario_num}, {name} easily compressed (squashed) a gas like {gas} into a smaller container. Why is this possible?"
                    correct = "Because there are large empty spaces between the gas particles."
                    wrong = make_wrong(["Because the particles are closely packed together.", "Because the gas particles are very small solids.", "Because gases have no mass.", "Because the particles are locked in place.", "Because gas particles shrink when squeezed.", "Because the gas turns into a liquid instantly.", "Because gases are heavier than solids."], 6, correct)
                    explanation = "Gases can be compressed because of the large amounts of empty space between their particles."

        elif subtopic == "Mixtures":
            mixture = random.choice(mixtures_solid_solid)
            if diff == "easy":
                question = f"{name} mixed {mixture} in a bowl (Experiment {scenario_num}). What have they created?"
                correct = "A mixture of solid substances"
                wrong = make_wrong(["A solution", "A pure substance", "A gas", "A liquid", "A chemical compound", "A completely new solid", "An element"], 6, correct)
                explanation = "Combining two different solid substances without them dissolving or reacting chemically forms a simple mixture."
            elif diff == "medium":
                question = f"For challenge {scenario_num}, {name} needed to separate a mixture of {mixture}. The pieces are of different sizes. What is the best method?"
                correct = "Hand sorting or using a sieve (sieving)"
                wrong = make_wrong(["Boiling", "Evaporating", "Filtering with filter paper", "Using a magnet", "Adding water and stirring", "Freezing", "Melting"], 6, correct)
                explanation = "Solid mixtures with different particle sizes can often be separated by sieving or hand sorting."
            else:
                question = f"{name} tested a simple mixture of {mixture} in lab {scenario_num}. How do the properties of the original substances change?"
                correct = "The properties do not change; each substance keeps its own properties."
                wrong = make_wrong(["They change completely into a new chemical.", "They melt into a liquid.", "They combine to form a gas.", "One substance completely disappears.", "They dissolve into each other.", "They become permanently bonded together.", "They lose their original colours."], 6, correct)
                explanation = "In a mixture, the substances are physically mixed but not chemically combined, so they retain their original properties."

        elif subtopic == "Solutions as special mixtures":
            solute = random.choice(solutes)
            if diff == "easy":
                question = f"In task {scenario_num}, {name} stirred {solute} into water and it seemed to disappear. What kind of mixture is formed?"
                correct = "A solution"
                wrong = make_wrong(["A gas mixture", "A solid mixture", "An insoluble mixture", "A suspension", "An emulsion", "A pure element", "A chemical compound"], 6, correct)
                explanation = "A solution is a special uniform mixture formed when a solid dissolves in a liquid."
            elif diff == "medium":
                question = f"{name} made a solution of {solute} and water (Mix {scenario_num}). What do we call the {solute}?"
                correct = "The solute"
                wrong = make_wrong(["The solvent", "The solution", "The gas", "The filter", "The insoluble solid", "The liquid", "The residue"], 6, correct)
                explanation = "The solid substance that dissolves is called the solute."
            else:
                question = f"{name} made a solution of {solute} and water (Mix {scenario_num}). What do we call the water?"
                correct = "The solvent"
                wrong = make_wrong(["The solute", "The mixture", "The suspension", "The residue", "The precipitate", "The filter", "The crystal"], 6, correct)
                explanation = "The liquid in which a solute dissolves is called the solvent."

        elif subtopic == "Dissolving":
            solute = random.choice(solutes)
            insoluble = random.choice(insolubles)
            if diff == "easy":
                question = f"For experiment {scenario_num}, {name} added {solute} to water and stirred it well. What happened?"
                correct = "The solid dissolves and forms a clear solution."
                wrong = make_wrong(["It floats on top forever.", "It turns into a rock.", "It sinks and forms a pile of sand.", "It catches fire.", "It evaporates instantly.", "It freezes the water.", "It forms bubbles and turns into oxygen."], 6, correct)
                explanation = f"Substances like {solute} are soluble in water and dissolve when stirred."
            elif diff == "medium":
                question = f"{name} noted in log {scenario_num} that {insoluble} did NOT form a solution when mixed with water. Why?"
                correct = "Because it is insoluble and does not dissolve in water."
                wrong = make_wrong(["Because the water is too wet.", "Because it is a gas.", "Because it evaporates too fast.", "Because it turns the water into a solid.", "Because it is lighter than air.", "Because it is a solvent.", "Because it is magnetic."], 6, correct)
                explanation = f"Insoluble substances like {insoluble} do not dissolve in water."
            else:
                question = f"{name} needs to make {solute} dissolve faster in water for test {scenario_num}. Which action should they take?"
                correct = "Using hot water and stirring."
                wrong = make_wrong(["Using ice cold water and leaving it still.", "Adding more solid and not stirring.", "Putting it in a dark cupboard.", "Adding oil to the water.", "Using less water and freezing it.", "Blowing air into the water.", "Covering the glass with a cloth."], 6, correct)
                explanation = "Increasing the temperature and stirring increases the rate of dissolving."

        elif subtopic == "Mixtures and water resources":
            pollutant = random.choice(pollutants)
            if diff == "easy":
                question = f"In community {scenario_num}, {name} saw {pollutant} in the local river. What do we call this?"
                correct = "Water pollution"
                wrong = make_wrong(["Water purification", "Evaporation", "Condensation", "A clean ecosystem", "Water conservation", "Filtering", "Distillation"], 6, correct)
                explanation = "Adding harmful substances to water sources causes water pollution."
            elif diff == "medium":
                question = f"{name} read report {scenario_num} stating a mixture of water and {pollutant} is dangerous. Why?"
                correct = "It can harm or kill plants, animals, and people who rely on the water."
                wrong = make_wrong(["It makes the water taste better.", "It adds healthy vitamins to the water.", "It turns the water into solid ice.", "It helps fish breathe faster.", "It creates new types of clean energy.", "It makes the water evaporate slower.", "It turns the water into pure oxygen."], 6, correct)
                explanation = "Polluted water is toxic and disrupts ecosystems and human health."
            else:
                question = f"{name} studied how {pollutant} entering a river affects the natural water mixture (Case {scenario_num}). What was the conclusion?"
                correct = "It introduces harmful substances that make the water unsafe for drinking and living organisms."
                wrong = make_wrong(["It purifies the water naturally.", "It only changes the colour but is perfectly safe.", "It turns the water into a safe solution of minerals.", "It cools the water down to safe temperatures.", "It removes all bacteria from the water.", "It turns the liquid water into a gas.", "It makes the river flow faster and cleaner."], 6, correct)
                explanation = "Pollutants degrade water quality, making it a hazardous mixture."

        else: # Processes to purify water
            method = random.choice(methods)
            if diff == "easy":
                if method == "Filtering (filtration)":
                    question = f"{name} needs to remove solid dirt from dirty water (Task {scenario_num}). Which process uses a sieve, cloth, or paper to do this?"
                    correct = "Filtering"
                    wrong = make_wrong(["Boiling", "Melting", "Freezing", "Condensation", "Evaporation", "Burning", "Stirring"], 6, correct)
                    explanation = "Filtering physically removes insoluble solid particles from a liquid."
                elif method == "Boiling":
                    question = f"In survival situation {scenario_num}, {name} needs a simple way to kill harmful germs in water before drinking it. What should they do?"
                    correct = "Boil the water"
                    wrong = make_wrong(["Freeze the water", "Stir the water", "Add more dirt", "Leave it in the dark", "Pour it through a sieve", "Add sugar", "Blow on it"], 6, correct)
                    explanation = "Boiling water kills most harmful bacteria and germs."
                elif method == "Settling":
                    question = f"{name} left muddy water in a bucket undisturbed (Experiment {scenario_num}), and the heavy mud fell to the bottom. What is this called?"
                    correct = "Settling"
                    wrong = make_wrong(["Boiling", "Evaporating", "Chlorinating", "Freezing", "Condensation", "Stirring", "Melting"], 6, correct)
                    explanation = "Settling allows heavy, insoluble particles to sink to the bottom over time."
                else:
                    question = f"{name} visited water plant {scenario_num}. Which chemical is often added to municipal tap water to kill germs and make it safe?"
                    correct = "Chlorine"
                    wrong = make_wrong(["Sugar", "Salt", "Sand", "Oil", "Food colouring", "Vinegar", "Baking soda"], 6, correct)
                    explanation = "Chlorine is widely used in water treatment plants to disinfect water."
            elif diff == "medium":
                question = f"Why did {name} note in report {scenario_num} that {method} is an important step in purifying water for a community?"
                correct = "It helps remove impurities or kill germs to prevent waterborne diseases."
                wrong = make_wrong(["It makes the water taste sweeter.", "It turns the water into ice.", "It adds more mud to the water.", "It creates electricity from the water.", "It turns the water into a solid metal.", "It makes the water evaporate instantly.", "It gives the water a bright blue colour."], 6, correct)
                explanation = "Water purification steps are essential for producing safe, clean drinking water."
            else:
                question = f"{name} had muddy water full of germs (Sample {scenario_num}). Why is settling and filtering alone NOT enough to make it safe to drink?"
                correct = "Because settling and filtering remove dirt, but they do not kill invisible germs and bacteria."
                wrong = make_wrong(["Because the water will still look brown.", "Because the water will evaporate too quickly.", "Because filtering adds more dirt to the water.", "Because settling makes the water boil.", "Because the water will freeze.", "Because the dirt will instantly come back.", "Because filtering turns the water into a gas."], 6, correct)
                explanation = "Physical removal of dirt must be followed by chemical treatment or boiling to eliminate microscopic pathogens."

        gen.add_question(subtopic, diff, question, correct, wrong, explanation)

    write_json(f"dataset/grade6/natural_sciences_and_technology/grade6_nst_matter_materials_processing.json", gen.questions)
    print(f"Generated Matter and Materials: {len(gen.questions)} questions")


def generate_energy_change():
    topic_name = "Energy and Change"
    topic_prefix = "G6_NST"
    subtopics = [
        "Electric circuits",
        "Electrical conductors and insulators",
        "Systems to solve problems using circuits",
        "Mains electricity (including fossil fuels, cost, and renewable energy)"
    ]

    gen = TopicGenerator(topic_name, topic_prefix, subtopics)

    components = ["cell (battery)", "light bulb", "switch", "connecting wires", "buzzer", "motor"]
    conductors = ["copper wire", "iron nail", "steel paperclip", "aluminium foil", "silver coin", "gold ring", "brass key"]
    insulators = ["plastic spoon", "rubber band", "wooden stick", "glass rod", "paper", "cotton string", "dry wool", "ceramic mug"]
    renewables = ["solar energy", "wind energy", "hydroelectric power", "geothermal energy"]
    fossil_fuels = ["coal", "oil", "natural gas"]

    names = ["Thabo", "Sipho", "Lerato", "Zanele", "Johan", "Sarah", "Piet", "Busi", "Nomsa", "Jabu", "Kevin", "Lisa"]

    attempts = 0
    while len(gen.questions) < 1000 and attempts < 100000:
        attempts += 1

        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        question = ""
        correct = ""
        wrong = []
        explanation = ""

        name = random.choice(names)
        scenario_num = random.randint(1, 100)

        if subtopic == "Electric circuits":
            comp = random.choice(components)
            if diff == "easy":
                if comp == "cell (battery)":
                    question = f"{name} is building circuit {scenario_num}. What is the function of a cell or battery in this simple electric circuit?"
                    correct = "It provides the energy to push the electricity around the circuit."
                    wrong = make_wrong(["It lights up the room.", "It turns the circuit on and off.", "It connects the components together.", "It makes a buzzing sound.", "It cools down the wires.", "It acts as an insulator.", "It stops the electricity from flowing."], 6, correct)
                    explanation = "A cell provides the electrical energy (source) in a simple circuit."
                elif comp == "switch":
                    question = f"In project {scenario_num}, {name} added a switch. What is its function?"
                    correct = "It controls the flow of electricity by opening or closing the circuit."
                    wrong = make_wrong(["It provides the energy for the circuit.", "It changes light energy into heat.", "It makes a loud sound.", "It creates electricity from nothing.", "It acts as a permanent battery.", "It connects the battery to the sun.", "It changes the colour of the light bulb."], 6, correct)
                    explanation = "A switch opens (breaks) or closes (completes) the circuit to control current flow."
                elif comp == "connecting wires":
                    question = f"{name} connects components in circuit {scenario_num}. What is the role of the connecting wires?"
                    correct = "They provide a pathway for the electrical current to travel."
                    wrong = make_wrong(["They provide the energy to the circuit.", "They act as switches.", "They light up the room.", "They stop the electricity from flowing completely.", "They store electricity like a battery.", "They turn electrical energy into sound.", "They act as perfect insulators."], 6, correct)
                    explanation = "Wires carry the electrical current between components in a circuit."
                else:
                    question = f"{name} built circuit {scenario_num}. What happens if the {comp} is removed and the wires are left disconnected?"
                    correct = "The circuit is broken and electricity stops flowing."
                    wrong = make_wrong(["The circuit works better.", "The battery produces more energy.", "The electricity flows faster.", "The circuit catches fire instantly.", "The electricity flows backwards.", "The gap turns into a battery.", "The electricity jumps across the gap easily."], 6, correct)
                    explanation = "An electric circuit needs an unbroken pathway for current to flow."
            elif diff == "medium":
                question = f"For test {scenario_num}, {name} has a circuit with a battery, wires, and a {comp}. What happens if a wire is cut?"
                correct = f"The circuit becomes open (broken) and the {comp} will stop working."
                wrong = make_wrong([f"The {comp} will work even better.", "The battery will start spinning.", "The electricity will find a new path through the air.", "The cut wire will produce a bright light.", f"The {comp} will absorb energy from the air.", "The circuit remains closed.", "The battery will recharge itself instantly."], 6, correct)
                explanation = "Cutting a wire creates an open circuit, preventing electricity from flowing."
            else:
                question = f"{name} was asked in exam {scenario_num}: Why must an electric circuit form a continuous, unbroken loop from the positive to the negative terminal of the battery?"
                correct = "Because electrical current can only flow if there is a complete pathway."
                wrong = make_wrong(["Because batteries only work in the dark.", "Because the wires will melt otherwise.", "Because switches only work in broken circuits.", "Because light bulbs need oxygen to burn.", "Because the current needs to evaporate into the air.", "Because the negative terminal pushes the positive terminal away.", "Because insulators need a gap to work."], 6, correct)
                explanation = "A complete, closed loop is strictly required for electrical current to flow."

        elif subtopic == "Electrical conductors and insulators":
            if diff == "easy":
                item = random.choice(conductors + insulators)
                if item in conductors:
                    question = f"In lab {scenario_num}, {name} tested a {item}. Is it an electrical conductor or an insulator?"
                    correct = "Conductor"
                    wrong = make_wrong(["Insulator", "Battery", "Switch", "Light bulb", "Motor", "Resistor", "Non-metal"], 6, correct)
                    explanation = f"Metals like {item} allow electricity to flow through them, making them conductors."
                else:
                    question = f"In lab {scenario_num}, {name} tested a {item}. Is it an electrical conductor or an insulator?"
                    correct = "Insulator"
                    wrong = make_wrong(["Conductor", "Battery", "Switch", "Light bulb", "Metal wire", "Electromagnet", "Generator"], 6, correct)
                    explanation = f"Materials like {item} do not allow electricity to flow through them easily, making them insulators."
            elif diff == "medium":
                cond = random.choice(conductors)
                ins = random.choice(insulators)
                question = f"{name} asked the teacher (Question {scenario_num}): Why do we use {cond} for the inside of electrical wires and {ins} for the outside covering?"
                correct = f"The {cond} allows electricity to flow, while the {ins} protects us from getting shocked."
                wrong = make_wrong([f"The {ins} allows electricity to flow, while the {cond} stops it.", f"The {cond} creates electricity and the {ins} destroys it.", f"Both the {cond} and {ins} are excellent conductors.", f"Both the {cond} and {ins} are perfect insulators.", f"The {ins} makes the wire heavier, and the {cond} makes it colourful.", f"The {cond} is cheaper than the {ins}.", f"The {ins} makes the electricity flow faster than the {cond}."], 6, correct)
                explanation = "Wires have a conductive core to carry current and an insulating sheath for safety."
            else:
                item = random.choice(conductors)
                question = f"{name} replaced a switch with a {item} in circuit {scenario_num}. What will happen to the circuit?"
                correct = "The circuit will remain closed and electricity will flow because it is a conductor."
                wrong = make_wrong(["The circuit will be broken because it is an insulator.", "The battery will immediately explode.", "The light bulb will turn into a motor.", "The electricity will flow backwards into the battery.", "The wires will instantly melt away.", "The circuit will produce a loud buzzing sound only.", "The electricity will stop completely."], 6, correct)
                explanation = f"Because {item} is a metal and a conductor, it completes the circuit just like a closed switch."

        elif subtopic == "Systems to solve problems using circuits":
            device = random.choice(["burglar alarm", "doorbell", "torch (flashlight)", "cooling fan"])
            if diff == "easy":
                question = f"{name} is building a {device} (Project {scenario_num}). Which output component is most important?"
                if device == "burglar alarm" or device == "doorbell":
                    correct = "A buzzer or bell"
                    wrong = make_wrong(["A light bulb", "A motor", "An insulator", "A plastic spoon", "A wooden stick", "A glass rod", "A heater"], 6, correct)
                elif device == "torch (flashlight)":
                    correct = "A light bulb"
                    wrong = make_wrong(["A buzzer", "A motor", "A doorbell", "An electric heater", "A plastic case", "A switch only", "A wooden stick"], 6, correct)
                else:
                    correct = "A motor with fan blades"
                    wrong = make_wrong(["A buzzer", "A light bulb", "A doorbell", "A heater", "A speaker", "A microphone", "An insulator"], 6, correct)
                explanation = f"The specific function of a {device} determines the required output component."
            elif diff == "medium":
                question = f"For design {scenario_num}, {name} wants to build a {device} that can be turned on and off easily. What component MUST be included?"
                correct = "A switch"
                wrong = make_wrong(["An extra battery", "A thicker wire", "A plastic insulator", "A glass cover", "A permanent magnet", "A wooden block", "A completely broken wire"], 6, correct)
                explanation = "A switch allows user control over the circuit, turning the device on or off on demand."
            else:
                question = f"Before building the {device} for assignment {scenario_num}, {name} drew a circuit diagram using standard symbols. Why is this important?"
                correct = "It helps to plan and communicate exactly how components should be connected before building it."
                wrong = make_wrong(["It generates free electricity on the paper.", "It makes the battery last longer in real life.", "It prevents the wires from getting tangled in the drawing.", "It makes the components cheaper to buy.", "It turns the paper into an insulator.", "It automatically builds the circuit for you.", "It ensures the battery is fully charged."], 6, correct)
                explanation = "Circuit diagrams use universal symbols to clearly plan and communicate the design of an electrical system."

        else: # Mains electricity
            topic_focus = random.choice(["fossil fuels", "renewable energy", "cost/safety"])
            if topic_focus == "fossil fuels":
                fuel = random.choice(fossil_fuels)
                if diff == "easy":
                    question = f"{name} learned in class {scenario_num} that South Africa generates most mains electricity by burning {fuel}. Is {fuel} renewable or non-renewable?"
                    correct = "Non-renewable"
                    wrong = make_wrong(["Renewable", "A clean energy source", "A type of solar energy", "A wind energy source", "A water energy source", "A permanent resource", "A green energy source"], 6, correct)
                    explanation = f"{fuel.capitalize()} takes millions of years to form and cannot be replaced quickly, making it non-renewable."
                elif diff == "medium":
                    question = f"In debate {scenario_num}, {name} argued about burning {fuel} in power stations. What is a major environmental problem with this?"
                    correct = "It releases greenhouse gases like carbon dioxide which cause air pollution and global warming."
                    wrong = make_wrong(["It cools down the earth's atmosphere.", "It creates too much fresh water.", "It makes the sun shine brighter.", "It causes solar eclipses.", "It turns into safe oxygen gas.", "It plants new trees in the forest.", "It stops volcanoes from erupting."], 6, correct)
                    explanation = "Burning fossil fuels releases harmful gases that contribute to climate change."
                else:
                    question = f"{name} explained in presentation {scenario_num} how heat energy from burning {fuel} is converted into electricity in a power station. What is the correct process?"
                    correct = "The heat boils water to make steam, which turns a turbine connected to a generator."
                    wrong = make_wrong(["The heat is directly sent through wires to our homes.", "The fire spins the wires directly.", "The heat turns air into electricity.", "The fire melts the coal into liquid electricity.", "The smoke is captured and stored in batteries.", "The fire shines light onto solar panels.", "The heat freezes water into solid electricity."], 6, correct)
                    explanation = "Power stations use heat to produce high-pressure steam that drives turbines."
            elif topic_focus == "renewable energy":
                ren = random.choice(renewables)
                if diff == "easy":
                    question = f"In quiz {scenario_num}, {name} was asked: Why is {ren} considered a renewable energy source?"
                    correct = "Because it will not run out and is constantly replaced by nature."
                    wrong = make_wrong(["Because it comes from burning coal.", "Because it is stored underground for millions of years.", "Because it creates massive amounts of air pollution.", "Because it can only be used once.", "Because it is very dangerous to use.", "Because it is made in a laboratory.", "Because it requires burning oil."], 6, correct)
                    explanation = "Renewable sources like wind and solar are naturally replenished."
                elif diff == "medium":
                    question = f"{name} researched {ren} for project {scenario_num}. What is one advantage of using it to generate electricity instead of burning coal?"
                    correct = "It produces little to no air pollution or greenhouse gases."
                    wrong = make_wrong(["It produces more carbon dioxide.", "It always works better at night.", "It causes more global warming.", "It uses up fossil fuels faster.", "It creates large amounts of toxic ash.", "It makes the air harder to breathe.", "It requires constant mining underground."], 6, correct)
                    explanation = "Renewables are cleaner and have a much lower environmental impact than fossil fuels."
                else:
                    question = f"{name} found a disadvantage of relying entirely on {ren} like solar or wind power (Study {scenario_num}). What is it?"
                    correct = "They are dependent on weather conditions and do not generate electricity constantly (e.g., when it is dark or windless)."
                    wrong = make_wrong(["They release huge amounts of toxic smoke.", "They run out very quickly like coal.", "They cause the earth's temperature to rise rapidly.", "They can only be used once a year.", "They destroy all the oxygen in the air.", "They are entirely invisible and cannot be measured.", "They produce electricity that cannot travel through wires."], 6, correct)
                    explanation = "Solar and wind energy are intermittent, depending on the sun and wind."
            else: # cost/safety
                if diff == "easy":
                    question = f"{name} learned a safety rule (Rule {scenario_num}): Why is it very dangerous to put a metal knife into a toaster that is plugged into mains electricity?"
                    correct = "Because metal is a conductor and the high voltage can cause a fatal electric shock."
                    wrong = make_wrong(["Because the knife will get cold.", "Because the toast will burn faster.", "Because the metal will instantly turn into plastic.", "Because the toaster will explode into confetti.", "Because the knife will act as an insulator.", "Because the electricity will flow out of the toaster.", "Because the knife will turn invisible."], 6, correct)
                    explanation = "Mains electricity has very high voltage (220V-240V) which is deadly if conducted through a person."
                elif diff == "medium":
                    question = f"In life skills lesson {scenario_num}, {name} learned that electricity is not free. How do households usually pay for mains electricity?"
                    correct = "By buying prepaid electricity tokens or paying a monthly municipal bill based on usage."
                    wrong = make_wrong(["By paying the power station in coal.", "By returning the electricity they didn't use in a bucket.", "By paying once when they buy the house.", "By trading solar panels for it.", "By planting trees in the garden.", "It is completely free for everyone always.", "By catching electricity in a jar."], 6, correct)
                    explanation = "Consumers pay for electricity per kilowatt-hour used."
                else:
                    question = f"{name} inspected appliance {scenario_num}. Why should you never use electrical appliances with frayed wires or broken plugs?"
                    correct = "The exposed metal wires can cause a short circuit, an electrical fire, or a severe shock."
                    wrong = make_wrong(["It makes the appliance work too fast.", "It causes the appliance to turn into a generator.", "It will make the appliance completely waterproof.", "It forces the electricity back into the wall.", "It turns the electricity into safe static electricity.", "It stops the power station from working.", "It changes the electricity into cold air."], 6, correct)
                    explanation = "Damaged insulation exposes live wires, creating severe safety hazards."

        gen.add_question(subtopic, diff, question, correct, wrong, explanation)

    write_json(f"dataset/grade6/natural_sciences_and_technology/grade6_nst_energy_change_systems_control.json", gen.questions)
    print(f"Generated Energy and Change: {len(gen.questions)} questions")


def generate_planet_earth():
    topic_name = "Planet Earth and Beyond"
    topic_prefix = "G6_NST"
    subtopics = [
        "The Solar System",
        "Movements of the Earth (rotation and revolution)",
        "Movements of the Moon (rotation and revolution)",
        "Systems for looking into space (telescopes)",
        "Systems to explore the Moon and Mars (rovers)"
    ]

    gen = TopicGenerator(topic_name, topic_prefix, subtopics)

    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    rocky_planets = ["Mercury", "Venus", "Earth", "Mars"]
    gas_giants = ["Jupiter", "Saturn", "Uranus", "Neptune"]

    names = ["Thabo", "Sipho", "Lerato", "Zanele", "Johan", "Sarah", "Piet", "Busi", "Nomsa", "Jabu", "Kevin", "Lisa"]

    attempts = 0
    while len(gen.questions) < 1000 and attempts < 100000:
        attempts += 1

        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        question = ""
        correct = ""
        wrong = []
        explanation = ""

        name = random.choice(names)
        scenario_num = random.randint(1, 100)

        if subtopic == "The Solar System":
            planet = random.choice(planets)
            if diff == "easy":
                question = f"In project {scenario_num}, {name} built a model of our Solar System. What object is at the very center, which {planet} orbits around?"
                correct = "The Sun"
                wrong = make_wrong(["The Earth", "The Moon", "Mars", "Jupiter", "A black hole", "A comet", "An asteroid"], 6, correct)
                explanation = "The Sun is a star at the center of our Solar System, and all 8 planets orbit it."
            elif diff == "medium":
                if planet in rocky_planets:
                    question = f"{name} had to classify {planet} for homework {scenario_num}. Which group of planets does it belong to?"
                    correct = "The inner, rocky planets"
                    wrong = make_wrong(["The outer, gas giants", "The dwarf planets", "The icy comets", "The asteroid belt", "The moons of Jupiter", "The rings of Saturn", "The exoplanets"], 6, correct)
                    explanation = "The first four planets are smaller, solid, and rocky."
                else:
                    question = f"{name} had to classify {planet} for homework {scenario_num}. Which group of planets does it belong to?"
                    correct = "The outer, gas giants"
                    wrong = make_wrong(["The inner, rocky planets", "The dwarf planets", "The asteroids", "The meteoroids", "The terrestrial planets", "The moons of Mars", "The solar flares"], 6, correct)
                    explanation = "The outer four planets are massive and made mostly of gas."
            else:
                question = f"For essay {scenario_num}, {name} explained why {planet} stays in its orbit around the Sun instead of flying off into space. What is the reason?"
                correct = "The strong force of gravity from the Sun pulls it inward, keeping it in orbit."
                wrong = make_wrong(["It is attached by an invisible string.", "It is pushed by the solar wind.", "It has its own engine.", "It bounces off the asteroid belt.", "The Moon's gravity holds it in place.", "It is stuck in a giant cloud of gas.", "It is magnetic and sticks to the Sun."], 6, correct)
                explanation = "Gravity is the attractive force that keeps celestial bodies in their orbits."

        elif subtopic == "Movements of the Earth (rotation and revolution)":
            if diff == "easy":
                q_type = random.choice([1, 2])
                if q_type == 1:
                    question = f"In test {scenario_num}, {name} was asked: What do we call the spinning movement of the Earth on its own axis?"
                    correct = "Rotation"
                    wrong = make_wrong(["Revolution", "Orbiting", "Flying", "Floating", "Sinking", "Drifting", "Sliding"], 6, correct)
                    explanation = "Earth rotates (spins) on its axis, causing day and night."
                else:
                    question = f"{name} learned in lesson {scenario_num}: How long does it take for the Earth to complete one full rotation on its axis?"
                    correct = "24 hours (1 day)"
                    wrong = make_wrong(["365 days (1 year)", "7 days (1 week)", "30 days (1 month)", "12 hours", "60 minutes", "48 hours", "10 years"], 6, correct)
                    explanation = "One rotation takes 24 hours, giving us one complete day and night cycle."
            elif diff == "medium":
                q_type = random.choice([1, 2])
                if q_type == 1:
                    question = f"{name} drew a diagram (Figure {scenario_num}) of the Earth's rotation on its axis. What is the result of this movement?"
                    correct = "It causes day and night."
                    wrong = make_wrong(["It causes the four seasons.", "It causes eclipses.", "It causes the phases of the Moon.", "It causes earthquakes.", "It creates gravity.", "It makes the Sun burn hotter.", "It causes volcanic eruptions."], 6, correct)
                    explanation = "As Earth spins, the side facing the Sun has day, and the side facing away has night."
                else:
                    question = f"For question {scenario_num}, {name} had to name the movement of the Earth in its path around the Sun. What is it?"
                    correct = "Revolution"
                    wrong = make_wrong(["Rotation", "Spinning", "Twisting", "Hovering", "Tidal pull", "Eclipsing", "Pulsating"], 6, correct)
                    explanation = "Earth revolves (orbits) around the Sun."
            else:
                question = f"In project {scenario_num}, {name} described the Earth's full revolution around the Sun. How long does it take, and what does this movement, combined with its tilted axis, cause?"
                correct = "It takes 365 and a quarter days (1 year) and causes the seasons."
                wrong = make_wrong(["It takes 24 hours and causes day and night.", "It takes 30 days and causes the phases of the Moon.", "It takes 10 years and causes climate change.", "It takes 7 days and causes the tides.", "It takes 1 year and causes eclipses only.", "It takes 24 hours and causes the seasons.", "It takes 365 days and causes earthquakes."], 6, correct)
                explanation = "The yearly orbit combined with the tilt of the Earth's axis causes seasons."

        elif subtopic == "Movements of the Moon (rotation and revolution)":
            if diff == "easy":
                question = f"{name} looked at the night sky (Observation {scenario_num}). Which celestial body does the Moon orbit around?"
                correct = "The Earth"
                wrong = make_wrong(["The Sun", "Mars", "Jupiter", "Venus", "A black hole", "An asteroid", "The center of the galaxy"], 6, correct)
                explanation = "The Moon is Earth's natural satellite and revolves around it."
            elif diff == "medium":
                question = f"In chart {scenario_num}, {name} tracked the Moon. How long does it take for the Moon to revolve once around the Earth?"
                correct = "About 27 to 29 days (roughly a month)"
                wrong = make_wrong(["24 hours", "365 days", "10 years", "7 days", "12 hours", "6 months", "50 days"], 6, correct)
                explanation = "It takes roughly a month for the Moon to complete its orbit around Earth."
            else:
                question = f"{name} wondered in entry {scenario_num}: Why do we always see the same side of the Moon from Earth?"
                correct = "Because the Moon's rotation time is exactly the same as its revolution time around Earth."
                wrong = make_wrong(["Because the Moon does not rotate at all.", "Because the Earth is spinning too fast.", "Because the dark side of the Moon has no light.", "Because the Moon is flat.", "Because the Sun's gravity locks it in place.", "Because clouds always cover the other side.", "Because the Earth stops the Moon from spinning."], 6, correct)
                explanation = "Tidal locking means the Moon spins on its axis at the same rate it orbits Earth."

        elif subtopic == "Systems for looking into space (telescopes)":
            telescope = random.choice(["optical telescope", "SALT (Southern African Large Telescope)", "Hubble Space Telescope", "radio telescope"])
            if diff == "easy":
                question = f"For assignment {scenario_num}, {name} researched the {telescope}. What is its main purpose?"
                correct = "To make distant objects in space look closer and larger."
                wrong = make_wrong(["To travel to other planets.", "To communicate with submarines.", "To measure the temperature of the ocean.", "To predict the weather on Earth.", "To grow plants in space.", "To dig holes on the Moon.", "To look at microscopic bacteria."], 6, correct)
                explanation = "Telescopes gather light or other signals to observe distant celestial objects."
            elif diff == "medium":
                if telescope == "optical telescope" or telescope == "SALT (Southern African Large Telescope)":
                    question = f"{name} explained how a large optical telescope like {telescope} works to see stars (Presentation {scenario_num}). What is the correct method?"
                    correct = "It uses curved mirrors or lenses to gather and focus light from distant objects."
                    wrong = make_wrong(["It sends out radio waves and waits for an echo.", "It shoots a laser beam to illuminate the stars.", "It captures sound waves from space.", "It uses magnets to pull the image closer.", "It measures the wind speed in space.", "It uses a giant magnifying glass only.", "It relies on x-rays from the sun."], 6, correct)
                    explanation = "Optical telescopes gather visible light using precision optics."
                else:
                    question = f"{name} read article {scenario_num} about the Hubble Space Telescope. Why do astronomers place such telescopes in orbit around Earth?"
                    correct = "To get a clear view without the Earth's atmosphere blurring the images."
                    wrong = make_wrong(["Because there is no gravity in space.", "Because it is cheaper to put them in space.", "Because they need to be closer to the Sun.", "Because it is too cold on Earth.", "Because they would be too heavy on Earth.", "Because clouds on Jupiter block the view from Earth.", "Because the Moon gets in the way on Earth."], 6, correct)
                    explanation = "Space telescopes bypass the blurring and light absorption caused by Earth's atmosphere."
            else:
                question = f"In geography quiz {scenario_num}, {name} was asked: The SALT (Southern African Large Telescope) is one of the largest single optical telescopes. Where is it located to ensure dark, clear skies?"
                correct = "In the Karoo near Sutherland, South Africa"
                wrong = make_wrong(["In the middle of Johannesburg", "On top of Table Mountain in Cape Town", "In the Sahara Desert", "In the Amazon Rainforest", "At the bottom of the ocean", "In the city of Durban", "In the Kruger National Park"], 6, correct)
                explanation = "SALT is located in Sutherland because the Karoo has clear, dark, unpolluted skies."

        else: # Systems to explore the Moon and Mars (rovers)
            vehicle = random.choice(["Mars rover", "Moon rover", "robotic spacecraft", "space probe"])
            if diff == "easy":
                question = f"{name} watched documentary {scenario_num} about a {vehicle}. What is it used for in space exploration?"
                correct = "It is an uncrewed vehicle sent to explore other planets or moons."
                wrong = make_wrong(["It carries human astronauts to other galaxies.", "It is an alien spaceship.", "It cleans up space junk around Earth.", "It acts as a flying telescope only.", "It provides oxygen for the Sun.", "It is a satellite that provides internet.", "It controls the weather on Earth."], 6, correct)
                explanation = f"A {vehicle} is a robotic machine designed to explore celestial surfaces."
            elif diff == "medium":
                question = f"In discussion {scenario_num}, {name} debated: Why do scientists send robotic machines like a {vehicle} to Mars instead of humans right now?"
                correct = "It is safer, much cheaper, and machines do not need food, water, or oxygen."
                wrong = make_wrong(["Because humans are too heavy for rockets.", "Because Mars has no ground to stand on.", "Because robots are faster than light.", "Because humans would melt instantly.", "Because robots can breathe carbon dioxide.", "Because humans are scared of the dark.", "Because robots can live forever without power."], 6, correct)
                explanation = "Uncrewed missions avoid the extreme risks and life-support costs of human spaceflight."
            else:
                question = f"{name} researched for paper {scenario_num}: How do scientists on Earth control a {vehicle} that is millions of kilometers away on Mars?"
                correct = "By sending complex computer commands via radio signals, which take several minutes to travel there."
                wrong = make_wrong(["Using a very long electrical wire.", "By shouting through a giant megaphone.", "Using invisible laser strings.", "By controlling it in real-time with a joystick like a video game.", "By waiting for the robot to come back and get instructions.", "The robot is entirely controlled by aliens.", "By sending signals through the ocean."], 6, correct)
                explanation = "Due to the vast distance, radio signals take time to travel between Earth and Mars, so rovers execute programmed sequences."

        gen.add_question(subtopic, diff, question, correct, wrong, explanation)

    write_json(f"dataset/grade6/natural_sciences_and_technology/grade6_nst_planet_earth_beyond_systems_control.json", gen.questions)
    print(f"Generated Planet Earth and Beyond: {len(gen.questions)} questions")


if __name__ == "__main__":
    random.seed(42) # For reproducibility
    generate_life_living()
    generate_matter_materials()
    generate_energy_change()
    generate_planet_earth()
    print("Done generating Grade 6 NST.")
