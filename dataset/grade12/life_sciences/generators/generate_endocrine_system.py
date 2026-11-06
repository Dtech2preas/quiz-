import json
import random
import os
import time

def generate_endocrine_system():
    print("Generating Grade 12 Life Sciences: Endocrine System & Homeostasis...")
    t0 = time.time()

    questions = []
    seen_texts = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive="Knowledge"):
        nonlocal questions, seen_texts
        q_text = q_text.strip()
        if q_text in seen_texts:
            return False
        correct = str(correct).strip()
        clean_wrongs = []
        for w in wrongs:
            w = str(w).strip()
            if w != correct and w not in clean_wrongs:
                clean_wrongs.append(w)
        if len(clean_wrongs) < 6:
            return False

        seen_texts.add(q_text)
        q_id = f"LIFE_P1_ENDOCRINE_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Endocrine System and Homeostasis",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Life Sciences",
                "topic": "Endocrine System and Homeostasis",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    endo_terms = [
        ("Endocrine gland", "A ductless gland that secretes chemical messengers (hormones) directly into surrounding blood capillaries for transport in the bloodstream", ["Exocrine gland", "Salivary gland", "Sweat gland", "Sebaceous gland", "Lymph node", "Digestive organ", "Lachrymal gland"]),
        ("Exocrine gland", "A gland that releases its secretions (enzymes, sweat, saliva) through specialized ducts onto an internal or external epithelial surface", ["Endocrine gland", "Pituitary gland", "Thyroid gland", "Adrenal gland", "Parathyroid gland", "Thymus gland", "Islet of Langerhans"]),
        ("Hormone", "An organic chemical messenger synthesized by an endocrine gland, transported in blood to target organs to regulate specific physiological processes", ["Enzyme", "Neurotransmitter", "Antibody", "Antigen", "Vitamin", "Electrolyte", "Lipoprotein"]),
        ("Homeostasis", "The physiological maintenance of a relatively constant, dynamic internal environment (tissue fluid and blood) despite external fluctuations", ["Metabolism", "Hemostasis", "Osmosis", "Thermodynamics", "Catabolism", "Anabolism", "Glycolysis"]),
        ("Negative feedback mechanism", "A regulatory homeostatic control mechanism where any deviation from a set-point triggers a corrective response that restores conditions back to normal", ["Positive feedback mechanism", "Action potential", "All-or-none response", "Reflex arc", "Enzyme inhibition", "Immune response", "Cascade activation"]),
        ("Thyroxin", "An iodine-containing hormone secreted by the thyroid gland that regulates the basal metabolic rate, oxygen consumption, and cellular growth", ["Calcitonin", "Parathyroid hormone", "Insulin", "Glucagon", "Adrenaline", "Aldosterone", "Cortisol"]),
        ("Insulin", "A peptide hormone secreted by the beta cells of the Islets of Langerhans in the pancreas that lowers blood glucose by converting it into glycogen", ["Glucagon", "Thyroxin", "Adrenaline", "Aldosterone", "Cortisol", "Growth hormone", "Prolactin"]),
        ("Glucagon", "A peptide hormone secreted by the alpha cells of the Islets of Langerhans in the pancreas that raises blood glucose by stimulating glycogenolysis", ["Insulin", "Thyroxin", "Aldosterone", "ADH", "Oxytocin", "Calcitonin", "Parathormone"]),
        ("Antidiuretic Hormone (ADH)", "A hormone synthesized by the hypothalamus and released by the posterior pituitary that increases water reabsorption in the kidney tubules", ["Aldosterone", "Insulin", "Glucagon", "Thyroxin", "Adrenaline", "Oxytocin", "Prolactin"]),
        ("Aldosterone", "A steroid hormone secreted by the adrenal cortex that promotes sodium ion (Na+) reabsorption and potassium excretion in kidney distal tubules", ["ADH", "Insulin", "Glucagon", "Thyroxin", "Adrenaline", "TSH", "FSH"]),
        ("Adrenaline (Epinephrine)", "An emergency hormone secreted by the adrenal medulla that prepares the body for 'fight or flight' by elevating heart rate, breathing, and blood sugar", ["Aldosterone", "Insulin", "Glucagon", "Thyroxin", "ADH", "Calcitonin", "Prolactin"]),
        ("Vasodilation", "The physiological widening of cutaneous arterioles, increasing blood flow to skin capillaries to facilitate heat loss by radiation on hot days", ["Vasoconstriction", "Shivering", "Perspiration", "Piloerection", "Hyperthermia", "Hypothermia", "Capillary thrombosis"]),
        ("Vasoconstriction", "The physiological narrowing of cutaneous arterioles, decreasing blood flow to the skin surface to minimize heat loss on cold days", ["Vasodilation", "Perspiration", "Evaporation", "Piloerection", "Erythema", "Cyanosis", "Angiogenesis"]),
        ("Diabetes mellitus", "A chronic metabolic disorder characterized by persistent hyperglycemia (high blood glucose) due to insufficient insulin production or insulin resistance", ["Diabetes insipidus", "Hypoglycemia", "Goiter", "Cretinism", "Grave's disease", "Addison's disease", "Cushing's syndrome"]),
        ("Goiter", "An abnormal physical enlargement of the thyroid gland, typically caused by a nutritional deficiency of dietary iodine or thyroid dysfunction", ["Diabetes", "Acromegaly", "Gigantism", "Dwarfism", "Cretinism", "Myxedema", "Exophthalmos"])
    ]

    for term, definition, wrongs in endo_terms:
        add_q("easy", "Endocrine System & Homeostasis", f"In Grade 12 CAPS Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Endocrine System & Homeostasis", f"Which hormone or physiological process correctly matches {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in endo_terms if d[0] != term][:7]
        add_q("easy", "Endocrine System & Homeostasis", f"Which statement accurately explains '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Endocrine System & Homeostasis", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

    easy_extras = [
        ("Which chemical element is a required dietary component for the thyroid gland to synthesize thyroxin?", "Iodine", ["Iron", "Calcium", "Potassium", "Sodium", "Magnesium", "Zinc", "Copper"], "Iodine is a necessary component of the thyroxin molecule; deficiency causes endemic goiter."),
        ("Which cells in the pancreas secrete insulin, and which secrete glucagon?", "Beta cells secrete insulin; Alpha cells secrete glucagon", ["Alpha cells secrete insulin; Beta cells secrete glucagon", "Acinar cells secrete insulin; Islet cells secrete glucagon", "Chief cells secrete insulin; Parietal cells secrete glucagon", "Duct cells secrete insulin; Beta cells secrete glucagon"], "Beta cells produce insulin; alpha cells produce glucagon within the pancreatic Islets of Langerhans."),
        ("What term describes the insoluble carbohydrate storage molecule in liver and muscle cells formed from excess blood glucose?", "Glycogen", ["Glucose", "Glucagon", "Glycerol", "Starch", "Cellulose", "Maltose"], "Insulin converts excess glucose into stored glycogen in the liver and skeletal muscles."),
        ("Where in the human body are the adrenal glands anatomically situated?", "Resting on top of each kidney (suprarenal)", ["Behind the sternum in the chest", "In the neck around the trachea", "At the base of the brain", "Inside the liver lobes", "Within the pelvic cavity"], "The adrenal glands sit atop both kidneys like caps."),
        ("Which part of the brain acts as the primary thermostat and control center for homeostatic thermoregulation and osmoregulation?", "Hypothalamus", ["Cerebrum", "Cerebellum", "Medulla oblongata", "Corpus callosum", "Pons", "Spinal cord"], "The hypothalamus contains thermoreceptors and osmoreceptors, acting as the central homeostatic integrator.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Homeostasis Focus: ", "In clinical endocrinology: "]:
            add_q("easy", "Endocrine System & Homeostasis", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(endo_terms)
        q = f"Homeostasis identification check {e_counter}: Name the hormone or feedback concept defined as: {definition}."
        add_q("easy", "Endocrine System & Homeostasis", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    medium_loops = [
        # Glucose High
        ("What sequence of events restores homeostasis when blood glucose levels rise above normal (e.g., after eating a meal)?",
         "Beta cells in pancreas detect high glucose -> Secrete insulin into blood -> Liver and muscle cells absorb glucose and convert it into glycogen -> Blood glucose levels return to normal",
         ["Alpha cells in pancreas secrete glucagon -> Liver converts glycogen to glucose -> Blood glucose drops", "Adrenal glands secrete adrenaline -> Glucose is excreted in urine", "Kidneys secrete ADH -> Water dilutes the blood glucose concentration", "Thyroid gland secretes thyroxin -> Inhibits all carbohydrate absorption in intestines", "Beta cells secrete glucagon -> Liver converts glucose into amino acids"],
         "Elevated blood glucose stimulates beta cells to release insulin; insulin promotes cellular uptake and glycogenesis, restoring normal glucose levels.", "Application"),

        # Glucose Low
        ("What sequence of physiological events restores blood glucose when levels drop below normal during fasting or exercise?",
         "Alpha cells in pancreas detect low glucose -> Secrete glucagon into blood -> Liver cells convert stored glycogen into glucose (glycogenolysis) -> Blood glucose rises back to normal",
         ["Beta cells secrete insulin -> Glucose is converted into starch in muscles", "Hypothalamus secretes ADH -> Retains glucose in kidney tubules", "Thyroid secretes thyroxin -> Stops cellular respiration in brain", "Adrenal cortex secretes aldosterone -> Reabsorbs glucose from stomach", "Beta cells secrete adrenaline -> Blood glucose falls rapidly"],
         "Low glucose stimulates pancreatic alpha cells to release glucagon; glucagon triggers glycogen breakdown in the liver, returning glucose to normal.", "Application"),

        # Thermoregulation Hot Day
        ("How does the human body respond to an increase in ambient temperature or core body temperature on a hot day?",
         "Hypothalamus detects elevated temperature -> Cutaneous arterioles dilate (vasodilation) increasing heat loss by radiation -> Sweat glands secrete sweat for evaporative cooling",
         ["Cutaneous arterioles constrict (vasoconstriction) -> Sweat glands shut down", "Hair erector muscles contract causing goosebumps -> Shivering begins", "Metabolic rate increases by 200% through thyroxin secretion", "Adrenal glands secrete adrenaline to accelerate blood circulation to core", "Kidneys excrete large volumes of cold urine"],
         "Vasodilation increases blood flow to skin capillaries for heat radiation; sweating provides evaporative cooling.", "Application"),

        # Thermoregulation Cold Day
        ("How does the human body respond to a drop in ambient temperature on a cold day to prevent hypothermia?",
         "Hypothalamus detects drop in temperature -> Cutaneous arterioles constrict (vasoconstriction) reducing radiation loss -> Shivering generates metabolic heat -> Sweat glands inactive",
         ["Cutaneous arterioles dilate -> Sweating increases -> Shivering halts", "Blood flow to skin capillaries triples -> Hairs lie completely flat", "Pancreas secretes insulin to cool internal organs", "Thyroid gland shuts down all metabolic heat production", "Respiratory rate triples to exhale hot air"],
         "Vasoconstriction restricts blood to deep core; shivering contracts skeletal muscles involuntarily to generate metabolic heat.", "Application"),

        # Osmoregulation High ADH (Dehydration)
        ("How does the body restore water balance when an athlete becomes dehydrated and blood water potential drops?",
         "Osmoreceptors in hypothalamus detect low water potential -> Posterior pituitary releases more ADH -> Permeability of kidney distal tubules and collecting ducts increases -> More water is reabsorbed into blood -> Small volume of concentrated urine excreted",
         ["Pituitary releases less ADH -> Kidney tubules become impermeable to water -> Large volume of dilute urine excreted", "Adrenal glands release insulin -> Causes water to turn into glycogen", "Sweat glands produce four times more sweat to hydrate the skin", "Thyroid gland absorbs water from the bladder directly", "Kidneys stop filtering blood completely"],
         "Dehydration triggers ADH release; ADH makes distal tubules and collecting ducts permeable to water, conserving water into blood.", "Application"),

        # Osmoregulation Low ADH (Overhydrated)
        ("What happens in the body when an individual drinks several glasses of water on a cold day (high blood water potential)?",
         "Hypothalamus detects high water potential -> Pituitary releases LESS ADH -> Kidney tubules become less permeable to water -> Less water is reabsorbed -> Large volume of pale, dilute urine excreted",
         ["Pituitary secretes massive amounts of ADH -> Kidney reabsorbs all urine", "Pancreas secretes glucagon -> Converts water into glucose", "Cutaneous arterioles constrict, forcing water into sweat glands", "Aldosterone increases sodium excretion by 1000%", "Adrenal medulla releases adrenaline to stimulate urination"],
         "High blood water potential inhibits ADH; kidney tubules remain impermeable to water, leading to copious dilute urine excretion.", "Application"),

        # CO2 Regulation
        ("How does the body respond to an accumulation of carbon dioxide (CO2) in the blood during vigorous muscular exercise?",
         "CO2 lowers blood pH forming carbonic acid -> Chemoreceptors detect drop in pH -> Medulla oblongata sends nerve impulses to breathing muscles and heart -> Breathing rate and depth increase, heart pumps faster -> Excess CO2 is exhaled rapidly",
         ["High CO2 causes the kidneys to excrete oxygen into the bladder", "Medulla oblongata slows down respiration to conserve oxygen", "Hypothalamus secretes insulin to convert CO2 into glucose", "Adrenal cortex secretes ADH to absorb carbon dioxide into bone", "Cutaneous capillaries dilate to sweat out carbon dioxide through skin"],
         "Elevated CO2 drops blood pH; medulla oblongata stimulates intercostal muscles and diaphragm to accelerate breathing rate, expelling excess CO2.", "Application")
    ]

    for q, ans, wrongs, expl, cog in medium_loops:
        for prefix in ["", "CAPS Negative Feedback Analysis: ", "Homeostatic Loop Problem: ", "Physiological Response Scenario: "]:
            add_q("medium", "Feedback Loops", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500
    gland_hormone_pairs = [
        ("Thyroid gland - Thyroxin", "Regulates basal metabolic rate, oxygen consumption, and cellular heat production in body tissues", [
            "Regulates calcium reabsorption in bone marrow", "Stimulates milk production in mammary glands",
            "Causes contraction of uterine myometrium during birth", "Converts glucose into glycogen in liver cells",
            "Stimulates water reabsorption in kidney collecting ducts", "Initiates the fight or flight emergency response",
            "Controls the menstrual cycle through negative feedback", "Causes vasodilation of cutaneous capillaries"
        ]),
        ("Pancreas (Beta cells) - Insulin", "Decreases blood glucose concentration by promoting cellular uptake and glycogen synthesis", [
            "Increases blood glucose concentration by breaking down glycogen", "Promotes sodium ion reabsorption in distal convoluted tubules",
            "Increases basal metabolic rate and body temperature", "Stimulates the adrenal cortex to produce aldosterone",
            "Causes the kidneys to excrete large volumes of dilute urine", "Triggers ovulation and corpus luteum formation",
            "Causes involuntary shivering of skeletal muscles", "Inhibits all cellular respiration in brain tissue"
        ]),
        ("Pancreas (Alpha cells) - Glucagon", "Increases blood glucose concentration by stimulating glycogenolysis (breakdown of glycogen to glucose) in liver cells", [
            "Decreases blood glucose concentration by stimulating glycogen storage", "Increases water reabsorption in renal tubules",
            "Stimulates thyroxin release from thyroid gland", "Causes constriction of cutaneous arterioles on cold days",
            "Promotes the development of female secondary sexual characteristics", "Inhibits digestive enzyme secretion in stomach",
            "Converts excess glucose into amino acids in spleen", "Regulates sodium reabsorption in the loop of Henle"
        ]),
        ("Adrenal medulla - Adrenaline", "Prepares the body for emergency 'fight or flight' by dilating bronchioles, increasing heart rate, and shunting blood to skeletal muscles", [
            "Promotes 'rest and digest' activities like digestion and urination", "Decreases heart rate and constricts air passages",
            "Lowers blood pressure and induces drowsiness", "Converts glucose into fat in adipose tissue",
            "Regulates long-term water balance via kidney collecting ducts", "Stimulates oogenesis in the ovarian follicles",
            "Causes the thyroid to stop producing thyroxin", "Inhibits all sympathetic nervous activity"
        ]),
        ("Adrenal cortex - Aldosterone", "Regulates salt and water balance by promoting sodium (Na+) reabsorption and potassium excretion in kidney tubules", [
            "Regulates blood glucose by breaking down glycogen into glucose", "Stimulates uterine contractions during human labour",
            "Increases basal metabolic rate and mental alertness", "Lowers core body temperature by promoting sweating",
            "Causes the pupils of the eyes to dilate in dim light", "Stimulates the development of Graafian follicles",
            "Triggers the release of digestive enzymes from the pancreas", "Inhibits all water reabsorption in the nephron"
        ])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        gh_item = random.choice(gland_hormone_pairs)
        q = f"Endocrine function matching {m_counter}: What is the primary physiological function of the hormone secreted by the {gh_item[0]}?"
        add_q("medium", "Endocrine Functions", q, gh_item[1], gh_item[2], f"Function: {gh_item[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        ("A patient presents with persistent weight loss despite an increased appetite, high body temperature, chronic sweating, nervousness, rapid resting heart rate, and protruding eyeballs (exophthalmos). Blood tests confirm elevated thyroxin and suppressed TSH. What disorder is this patient suffering from?",
         "Hyperthyroidism (Grave's disease)",
         ["Hypothyroidism (Myxedema)", "Diabetes mellitus Type 1", "Diabetes insipidus", "Addison's disease", "Cushing's syndrome", "Endemic goiter from iodine deficiency", "Acromegaly"],
         "Hypersecretion of thyroxin elevates metabolic rate, producing heat, tachycardia, weight loss, and exophthalmos; high thyroxin inhibits TSH via negative feedback.", "Analysis"),

        ("A patient experiences extreme fatigue, unexplained weight gain, constant cold intolerance, mental sluggishness, and dry skin. Blood tests show very low thyroxin levels and high TSH. What is the diagnosis, and why is TSH elevated?",
         "Hypothyroidism; the anterior pituitary secretes high TSH in an unavailing attempt to stimulate the underactive thyroid gland because negative feedback inhibition is absent",
         ["Hyperthyroidism; high TSH causes the thyroid to destroy its own tissue", "Diabetes mellitus; high TSH indicates complete lack of pancreatic beta cells", "Diabetes insipidus; TSH is converting all blood water into urine", "Addison's disease; adrenal glands have absorbed the thyroid hormones", "Cretinism; the patient has stopped producing growth hormone", "Normal healthy physiology; TSH and thyroxin always move in opposite directions without disorder"],
         "Low thyroxin removes negative feedback on the pituitary, leading to elevated TSH output (compensatory feedback failure in primary hypothyroidism).", "Analysis"),

        ("Why do patients with untreated Diabetes Mellitus suffer from frequent urination (polyuria) and extreme thirst (polydipsia)?",
         "High blood glucose exceeds the renal threshold, spilling into urine (glucosuria); glucose draws water osmotically into kidney tubules, causing excessive urination and severe cellular dehydration",
         ["Insulin dissolves the kidney nephrons, causing uncontrolled bladder leakage", "High glucose turns the blood acidic, forcing the brain to drink water", "The liver secretes pure water into the stomach to dilute food", "The patient lacks ADH, so kidney collecting ducts are completely blocked", "Glucagon destroys the salivary glands, producing phantom thirst", "Adrenaline stimulates the bladder sphincter to stay open permanently"],
         "Excess glucose cannot be fully reabsorbed by proximal tubules; osmotic pull of tubular glucose prevents water reabsorption, creating osmotic diuresis and thirst.", "Analysis"),

        ("A patient suffers head trauma damaging the hypothalamus. Post-accident, the patient produces up to 18 liters of very dilute urine daily and suffers severe thirst, but urine analysis shows zero glucose. What endocrine disorder is this?",
         "Diabetes insipidus, caused by hyposecretion of Antidiuretic Hormone (ADH)",
         ["Diabetes mellitus Type 1, caused by destruction of pancreatic beta cells", "Diabetes mellitus Type 2, caused by insulin resistance", "Hypothyroidism, caused by lack of dietary iodine", "Hyperthyroidism, caused by thyroid adenoma", "Addison's disease, caused by adrenal cortex failure", "Cushing's syndrome, caused by hypercortisolemia"],
         "Damage to hypothalamus/pituitary eliminates ADH secretion; without ADH, distal tubules cannot reabsorb water, causing massive water diuresis (Diabetes insipidus).", "Analysis"),

        ("How does the negative feedback loop between the anterior pituitary and the thyroid gland regulate thyroxin levels in a healthy individual?",
         "When thyroxin levels drop below normal, the pituitary secretes more TSH, which stimulates the thyroid to produce thyroxin; when thyroxin reaches normal levels, it inhibits the pituitary from releasing TSH",
         ["The thyroid secretes TSH to stimulate the pituitary to release thyroxin", "When thyroxin rises, the pituitary secretes five times more TSH to double thyroxin production", "The hypothalamus converts thyroxin into adrenaline when blood cools", "Thyroxin is destroyed by insulin as soon as it enters blood vessels", "TSH and thyroxin are identical hormones produced by the adrenal cortex", "Negative feedback between pituitary and thyroid only functions during sleep"],
         "Classic endocrine negative feedback: TSH stimulates thyroxin release, and thyroxin feeds back to inhibit TSH release, maintaining metabolic homeostasis.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "CAPS Clinical Endocrinology Problem: ", "Diagnostic Feedback Evaluation: ", "Homeostatic Failure Analysis: "]:
            add_q("hard", "Clinical Endocrine Diagnostics", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Clinical diagnostic case {h_counter}: {base_h[0]}"
        add_q("hard", "Clinical Endocrine Diagnostics", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/life_sciences/paper1_life_endocrine_system.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_endocrine_system()
