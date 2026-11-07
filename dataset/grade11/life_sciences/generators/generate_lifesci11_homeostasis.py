import os
import sys
import random

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from lifesci11_common import LifeSci11Generator

def generate_lifesci11_homeostasis():
    gen = LifeSci11Generator(
        filename="paper1_life_homeostasis.json",
        prefix="LIFE11_P1_HOMEO",
        topic_name="Homeostasis in Humans",
        paper="paper1"
    )

    names = ["Sipho", "Sarah", "Johan", "Lerato", "Thabo", "Fatima", "David", "Nandi", "Kobus", "Anke", "Priya", "Pieter", "Bongani", "Chloe", "Nomvula", "Tariq", "Keletso", "Willem", "Wayne", "Zola", "Buhle", "Ayanda", "Jaco", "Mpho"]
    ages = [19, 24, 29, 36, 43, 51, 58, 65, 73]
    cities = ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Bloemfontein", "Polokwane", "Mbombela", "Kimberley", "Gqeberha", "East London", "Potchefstroom", "Rustenburg"]
    hospitals = ["General Hospital", "Academic Medical Centre", "Regional Clinic", "Pathology Laboratory", "Endocrine Care Unit", "Nephrology Clinic", "District Infirmary", "University Teaching Hospital"]

    # 1. EASY QUESTIONS (300)
    homeo_facts = [
        ("Homeostasis", "the maintenance of a relatively constant internal environment within narrow physiological limits", ["Hemostasis", "Metabolism", "Thermodynamics", "Catabolism", "Anabolism", "Glycolysis", "Osmosis"]),
        ("Negative feedback mechanism", "a self-regulating control system where any change from the setpoint triggers a corrective response to reverse the change", ["Positive feedback mechanism", "Action potential", "All-or-none response", "Reflex arc", "Enzyme inhibition", "Immune cascade", "Coagulation"]),
        ("Hypothalamus", "the brain region acting as the primary control center and thermoregulatory center for human homeostasis", ["Medulla oblongata", "Cerebellum", "Cerebrum", "Corpus callosum", "Pons", "Thalamus", "Pituitary stalk"]),
        ("Vasoconstriction", "the narrowing of blood arterioles near the skin surface in cold conditions to reduce heat loss by radiation", ["Vasodilation", "Perspiration", "Shivering", "Erection of hairs", "Piloerection", "Bronchodilation", "Arteriosclerosis"]),
        ("Vasodilation", "the widening of dermal blood arterioles in hot conditions to increase blood flow and heat loss by radiation", ["Vasoconstriction", "Sweating", "Piloerection", "Shivering", "Hemostasis", "Arterial spasm", "Atherosclerosis"]),
        ("Insulin", "hormone secreted by beta cells of the Islets of Langerhans that decreases blood glucose by promoting glycogen synthesis", ["Glucagon", "Adrenaline", "Thyroxin", "Aldosterone", "Cortisol", "Growth hormone", "Prolactin"]),
        ("Glucagon", "hormone secreted by alpha cells of the Islets of Langerhans that increases blood glucose by stimulating glycogenolysis", ["Insulin", "Thyroxin", "Adrenaline", "ADH", "Oxytocin", "Calcitonin", "Parathormone"]),
        ("Antidiuretic Hormone (ADH)", "hormone released by the posterior pituitary that increases water permeability of kidney collecting ducts", ["Aldosterone", "Insulin", "Glucagon", "Thyroxin", "Adrenaline", "Oxytocin", "Prolactin"]),
        ("Aldosterone", "steroid hormone secreted by the adrenal cortex that stimulates reabsorption of sodium ions in kidney tubules", ["ADH", "Cortisol", "Adrenaline", "Insulin", "Glucagon", "Thyroxin", "Calcitonin"]),
        ("Medulla oblongata", "brain stem region containing respiratory and cardiovascular centers regulating carbon dioxide levels", ["Hypothalamus", "Cerebellum", "Cerebrum", "Spinal cord", "Corpus callosum", "Hippocampus", "Thalamus"]),
        ("Thermoregulation", "the biological process of maintaining body core temperature around 37 degrees Celsius", ["Osmoregulation", "Glucoregulation", "Hemostasis", "Metabolism", "Respiration", "Perspiration", "Excretion"]),
        ("Osmoregulation", "the regulation of water and solute concentrations in body fluids and blood plasma", ["Thermoregulation", "Glucoregulation", "Hemostasis", "Excretion", "Transpiration", "Egestion", "Secretion"])
    ]

    for term, f_def, wrs in homeo_facts:
        for t_tmpl in [
            f"What is the term for {f_def}?",
            f"Identify the concept defined as: {f_def}.",
            f"Which term refers to {f_def}?",
            f"In human physiology, {f_def} is known as:",
            f"Select the biological term that describes {f_def}."
        ]:
            gen.add_q("easy", "Homeostatic Principles", t_tmpl, term, wrs, f"{term} is {f_def}.")

    # Additional easy components
    subsystems = [
        ("Skin", "the largest organ containing sweat glands, dermal arterioles, and thermoreceptors", ["Liver", "Kidney", "Pancreas", "Brain", "Heart", "Lungs"]),
        ("Kidneys", "the paired excretory organs responsible for filtering blood and osmoregulation under ADH control", ["Lungs", "Liver", "Spleen", "Pancreas", "Gallbladder", "Stomach"]),
        ("Pancreas", "the dual endocrine/exocrine gland containing the Islets of Langerhans regulating blood glucose", ["Liver", "Adrenal gland", "Thyroid", "Hypothalamus", "Pituitary", "Kidney"]),
        ("Sweat glands", "coiled tubular exocrine glands in the dermis secreting perspiration for evaporative cooling", ["Sebaceous glands", "Endocrine glands", "Ceruminous glands", "Adrenal glands", "Lymph glands", "Mammary glands"]),
        ("Beta cells", "endocrine cells in the pancreatic islets that synthesize and secrete insulin", ["Alpha cells", "Acinar cells", "Hepatocytes", "Nephrons", "Glial cells", "Parietal cells"]),
        ("Alpha cells", "endocrine cells in the pancreatic islets that synthesize and secrete glucagon", ["Beta cells", "Chief cells", "Hepatocytes", "Podocytes", "Osteocytes", "Goblet cells"])
    ]
    for organ, o_desc, wrs in subsystems:
        for pre in ["Which organ or structure is ", "Identify the anatomical component described as ", "Name the physiological structure that represents "]:
            gen.add_q("easy", "Homeostatic Organs", f"{pre}{o_desc}?", organ, wrs, f"{organ} is {o_desc}.")

    # Top up easy with varied clinical student contexts
    tries = 0
    while gen.diff_counts["easy"] < gen.targets["easy"] and tries < 5000:
        tries += 1
        fact = random.choice(homeo_facts)
        name = random.choice(names)
        city = random.choice(cities)
        hosp = random.choice(hospitals)
        templates = [
            f"During a Life Sciences practical at {hosp} in {city}, {name} is asked to identify the term for {fact[1]}. What is the correct term?",
            f"In a physiological study session at {hosp} in {city}, {name} reviews the concept of {fact[1]}. Which term is correct?",
            f"At {hosp} in {city}, a student named {name} analyzes the definition: '{fact[1]}'. Identify the corresponding biological term.",
            f"When evaluating patient equilibrium at {hosp} in {city}, {name} notes that {fact[1]} is occurring. What term designates this?"
        ]
        q_txt = random.choice(templates)
        gen.add_q("easy", "Homeostatic Principles", q_txt, fact[0], fact[2], f"{fact[0]} refers to {fact[1]}.")

    # 2. MEDIUM QUESTIONS (500)
    scenarios = [
        ("consumes a carbohydrate-dense meal, causing systemic blood glucose to rise above the physiological baseline",
         "Beta cells of the Islets of Langerhans secrete insulin, prompting hepatocytes and myocytes to convert excess glucose into glycogen",
         ["Alpha cells secrete glucagon to convert glycogen into glucose", "Adrenal cortex releases aldosterone to excrete glucose in urine", "Posterior pituitary secretes ADH to dilute the glucose pool", "Thyroid gland secretes calcitonin to convert glucose to calcium", "Liver directly excretes glucose into the gall bladder", "Kidneys halt glomerular filtration entirely"]),

        ("has been fasting for 16 hours, causing systemic blood glucose levels to drop below 3.5 mmol/L",
         "Alpha cells of the Islets of Langerhans secrete glucagon, which stimulates hepatic glycogenolysis to restore blood glucose",
         ["Beta cells secrete insulin to accelerate cellular respiration", "Kidneys reabsorb water to concentrate existing glucose", "Hypothalamus initiates shivering to synthesize glucose", "Adrenal glands secrete aldosterone to break down stored lipids", "Pancreas shuts down all endocrine secretions", "Thyroid gland secretes thyroxin to halt metabolic activity"]),

        ("is exercising vigorously outdoors on an afternoon with an ambient temperature of 38 degrees Celsius",
         "Dermal arterioles dilate (vasodilation) to increase radiative heat loss, while sweat glands secrete perspiration for evaporative cooling",
         ["Dermal arterioles constrict (vasoconstriction) and erector pili muscles contract", "Metabolic rate surges and shivering thermogenesis is initiated", "Sweat glands stop functioning to preserve body hydration", "Hypothalamus stimulates thyroxin release to generate heat", "Blood flow is diverted completely away from the cutaneous vascular bed", "Kidneys excrete large volumes of dilute urine"]),

        ("is exposed to severe freezing sub-zero winds without insulated thermal protective clothing",
         "Vasoconstriction of peripheral arterioles minimizes blood flow to the skin, while involuntary shivering generates metabolic heat",
         ["Vasodilation increases blood flow to the skin to warm the surface", "Sweating increases to release trapped body moisture", "Insulin secretion surges to metabolize lipid reserves rapidly", "Hypothalamus halts thyroid-stimulating hormone secretion", "Arterioles dilate and skeletal muscles undergo complete flaccidity", "Respiratory rate decreases to trap air in the lungs"]),

        ("runs a 15 km road race in warm weather without fluid replacement, resulting in acute dehydration",
         "Hypothalamic osmoreceptors detect elevated blood osmotic pressure; posterior pituitary releases ADH, maximizing water reabsorption in renal collecting ducts",
         ["Pituitary halts ADH release, prompting kidneys to produce copious dilute urine", "Pancreas secretes insulin to convert blood solutes into glycogen", "Adrenal cortex ceases aldosterone secretion to prevent water retention", "Sweat glands increase perspiration rate despite fluid deficit", "Hypothalamus diminishes thirst sensation", "Kidneys permanently arrest glomerular filtration"]),

        ("drinks 1.5 liters of pure water within 20 minutes while resting comfortably at room temperature",
         "Blood plasma becomes hypo-osmotic; osmoreceptors inhibit ADH secretion, reducing collecting duct permeability and yielding dilute urine",
         ["ADH secretion surges, maximizing water reabsorption across the nephrons", "Aldosterone increases to maximum levels to eliminate extra water", "Insulin is secreted to absorb water into somatic cells", "Dermal blood vessels vasoconstrict to retain moisture", "Thyroid gland increases basal metabolic rate to evaporate fluid", "Kidneys produce zero urine output"]),

        ("performs high-intensity interval sprinting, generating substantial amounts of metabolic carbon dioxide (CO2)",
         "Excess CO2 forms carbonic acid, reducing blood pH; medulla oblongata detects this and signals intercostal muscles and diaphragm to increase ventilation rate and depth",
         ["Elevated CO2 prompts the medulla to slow breathing rate to preserve oxygen", "Hypothalamus induces cutaneous vasodilation to expel CO2 gas", "Pancreas secretes glucagon to neutralize the carbonic acid", "Posterior pituitary secretes ADH to filter CO2 via the kidneys", "Lungs halt exhalation until CO2 reaches baseline equilibrium", "Heart rate slows to prevent CO2 circulation to the brain"])
    ]

    tries_m = 0
    while gen.diff_counts["medium"] < gen.targets["medium"] and tries_m < 10000:
        tries_m += 1
        scen = random.choice(scenarios)
        name = random.choice(names)
        age = random.choice(ages)
        city = random.choice(cities)
        hosp = random.choice(hospitals)
        templates_m = [
            f"At {hosp} in {city}, {name}, a {age}-year-old individual, {scen[0]}. Which corrective physiological homeostatic response is initiated?",
            f"In an observation unit at {hosp} in {city}, a {age}-year-old patient ({name}) {scen[0]}. What is the primary homeostatic adjustment?",
            f"During clinical monitoring in {city}, {name} ({age} years old) {scen[0]}. Identify the correct negative feedback response:",
            f"Physicians at {hosp} evaluate {name}, aged {age}, who {scen[0]}. How does the body restore physiological equilibrium?"
        ]
        q_txt = random.choice(templates_m)
        gen.add_q("medium", "Feedback Mechanisms", q_txt, scen[1], scen[2], f"When an individual {scen[0]}, {scen[1]}.")

    # 3. HARD QUESTIONS (200)
    hard_cases = [
        ("extreme hypothermic exposure leading to terminal paradoxical undressing",
         "Exhaustion of smooth muscle tone in contracted dermal arterioles triggers profound rebound vasodilation, transmitting an intense sensation of heat prior to fatal collapse",
         ["Core temperature spikes above 40 degrees Celsius due to uncontrollable shivering", "Hypothalamus permanently ceases all neuroendocrine regulation", "Insulin levels surge causing sudden massive metabolic heat release", "Sweat glands produce boiling sweat that injures dermal tissue", "Kidneys excrete all blood plasma causing hypovolemia", "Lungs collapse due to freeze-drying of alveolar surfactant"],
         "Hypothermic paralysis of vascular smooth muscle causes sudden vasodilation, giving the false impression of overheating.", "Analysis"),

        ("severe uncontrolled Type 1 diabetes mellitus manifesting with ketoacidosis",
         "Inability of somatic cells to uptake glucose forces hepatocytes to metabolize fatty acids into acidic ketone bodies, inducing systemic acidosis",
         ["Blood glucose converts into toxic ethanol within the renal tubules", "Beta cells secrete digestive proteases that dissolve somatic tissues", "Excess insulin causes somatic cell rupture and acid spill", "Pituitary ceases growth hormone secretion leading to rapid muscular atrophy", "Kidneys reabsorb all urine solutes causing fluid intoxication", "Thyroid stops functioning leading to severe myxedema"],
         "Without insulin, cells starve amid hyperglycemia, relying on fatty acid beta-oxidation which yields acidic ketones.", "Analysis"),

        ("pre-dive intentional hyperventilation culminating in shallow-water blackout",
         "Forced hyperventilation drastically depletes arterial CO2 without increasing oxygen saturation, delaying respiratory drive until cerebral hypoxia induces unconsciousness",
         ["Hyperventilation floods pulmonary alveoli with poisonous nitrogen gas", "Excess oxygen induces immediate spasm of the internal carotid arteries", "Diaphragm enters tetanic paralysis preventing respiratory motion", "Blood pH plummets to acidic levels that denature respiratory enzymes", "Heart rate abruptly drops to zero beats per minute", "Medulla oblongata sustains an immediate ischemic stroke"],
         "Respiratory urge is driven by rising CO2; suppressing CO2 allows hypoxia to cause syncope before any urge to breathe occurs.", "Analysis"),

        ("clinical heat stroke contrasted against infectious pyrogenic fever",
         "Heat stroke represents thermoregulatory effector failure with uncontrollably rising core temperature and anhidrosis, whereas fever is an intentional upward resetting of the hypothalamic setpoint with intact effector control",
         ["Heat stroke is caused by bacterial lipopolysaccharides whereas fever is strictly environmental", "In heat stroke the hypothalamic setpoint is shifted downward to zero", "Fever occurs only in cold climates whereas heat stroke occurs exclusively indoors", "Heat stroke involves hyperactive sweating that drowns pulmonary alveoli", "In fever dermal arterioles remain permanently constricted until lysis", "Heat stroke elevates insulin to lethal concentrations in blood"],
         "Fever is a regulated setpoint shift; heat stroke is an effector failure where heat dissipation cannot match thermal load.", "Analysis"),

        ("syndrome of inappropriate antidiuretic hormone secretion (SIADH)",
         "Persistent excessive ADH secretion results in continuous renal water retention, blood dilution, and severe dilutional hyponatremia",
         ["Lack of ADH causes excretion of massive volumes of hypotonic urine", "Excess aldosterone eliminates all potassium while retaining glucose", "Pancreas stops producing insulin leading to extreme hyperglycemia", "Sweat glands shut down permanently causing extreme pyrexia", "Renal glomeruli become impermeable to blood filtration", "Adrenal glands hypertrophy and secrete excessive adrenaline"],
         "SIADH causes uninhibited water retention in collecting ducts, dangerously diluting blood sodium levels.", "Analysis")
    ]

    tries_h = 0
    while gen.diff_counts["hard"] < gen.targets["hard"] and tries_h < 5000:
        tries_h += 1
        hc = random.choice(hard_cases)
        name = random.choice(names)
        age = random.choice(ages)
        city = random.choice(cities)
        hosp = random.choice(hospitals)
        templates_h = [
            f"In a specialist clinical audit at {hosp} in {city}, physicians examine the case of a {age}-year-old patient ({name}) presenting with {hc[0]}. How is this pathophysiological outcome explained?",
            f"During advanced medical rounds at {hosp} in {city}, consultants assess a {age}-year-old individual ({name}) with {hc[0]}. What is the physiological mechanism?",
            f"Pathology findings from {hosp} in {city} for {name} (age {age}) document {hc[0]}. Critically analyze the underlying cause:",
            f"An intensive care case review in {city} explores the survival response of a {age}-year-old patient ({name}) who developed {hc[0]}. Identify the accurate diagnosis:"
        ]
        q_txt = random.choice(templates_h)
        gen.add_q("hard", "Advanced Homeostatic Analysis", q_txt, hc[1], hc[2], hc[3], hc[4])

    gen.save()

if __name__ == "__main__":
    generate_lifesci11_homeostasis()
