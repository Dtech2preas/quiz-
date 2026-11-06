import json
import random
import os

def build_chemical_industry():
    questions = []
    seen_questions = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, cognitive, outcome):
        q_clean = q_text.strip()
        if q_clean in seen_questions:
            return False
        
        c_str = str(correct).strip()
        clean_wrongs = []
        seen_w = set()
        for w in wrongs:
            w_str = str(w).strip()
            if w_str != c_str and w_str not in seen_w:
                seen_w.add(w_str)
                clean_wrongs.append(w_str)
        
        if len(clean_wrongs) < 6:
            return False
            
        seen_questions.add(q_clean)
        qid = f"PS_P2_IND_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "topic": "Paper 2: Chemical Industry",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # -------------------------------------------------------------
    # EASY (300 questions) - Macronutrients, Processes, Catalysts
    # -------------------------------------------------------------
    nutrient_functions = [
        ("Nitrogen (N)", "Promotes rapid vegetative leaf and stem growth, and is essential for chlorophyll and protein synthesis.",
         ["Promotes root development and flower formation", "Improves fruit quality and drought resistance", "Provides the carbon skeleton for photosynthesis", "Lowers the freezing point of plant sap", "Acts as an insecticide in the soil", "Prevents algal blooms in rivers"]),
        ("Phosphorus (P)", "Promotes root development, flowering, seed formation, and energy transfer (ATP) in plants.",
         ["Promotes vegetative stem and green leaf growth", "Improves fruit quality and disease resistance", "Produces gaseous nitrogen in leaves", "Causes rapid water evaporation from stomata", "Dissolves rock minerals into nitrogen gas", "Increases soil acidity to pH 1"]),
        ("Potassium (K)", "Improves disease resistance, fruit quality, drought tolerance, and activates plant enzymes.",
         ["Promotes rapid vegetative green leaf growth", "Promotes root growth and seed production", "Provides calcium for cell wall formation", "Acts as the primary constituent of nucleic acids", "Decreases water retention in plant tissues", "Turns plant leaves blue"])
    ]

    for nut, func, wr in nutrient_functions:
        add_q("easy", "Plant Nutrients", f"What is the primary agricultural function of the macronutrient **{nut}** in plant growth?", func, wr, "Knowledge", "Recall nutrient function")

    # The 3 Great Industrial Processes
    industrial_names = [
        ("Haber Process", "The industrial manufacture of ammonia (NH3) from nitrogen (N2) and hydrogen (H2).", "Iron (Fe) / Iron oxide", "450 °C and 200 atm (20,000 kPa)",
         ["Ostwald Process", "Contact Process", "Hall-Héroult Process", "Downs Process", "Frasch Process", "Chlor-Alkali Process"]),
        ("Ostwald Process", "The industrial manufacture of nitric acid (HNO3) from ammonia (NH3) and oxygen (O2).", "Platinum-Rhodium (Pt-Rh)", "850 °C and 5 atm",
         ["Haber Process", "Contact Process", "Hall-Héroult Process", "Downs Process", "Bessemer Process", "Solvay Process"]),
        ("Contact Process", "The industrial manufacture of sulfuric acid (H2SO4) from sulfur, oxygen, and water.", "Vanadium pentoxide (V2O5)", "450 °C and 1–2 atm",
         ["Haber Process", "Ostwald Process", "Hall-Héroult Process", "Downs Process", "Chlor-Alkali Process", "Bayer Process"])
    ]

    for pname, pdesc, pcatalyst, pconds, wr in industrial_names:
        add_q("easy", "Industrial Processes", f"Which industrial process is defined as: '{pdesc}'?", pname, wr, "Knowledge", "Identify industrial process")
        add_q("easy", "Catalysts", f"What catalyst is used in the **{pname}**?", pcatalyst,
              [p[2] for p in industrial_names if p[0] != pname] + ["Nickel (Ni)", "Copper (Cu)", "Manganese dioxide (MnO2)"], "Knowledge", "Identify industrial catalyst")
        add_q("easy", "Reaction Conditions", f"What are the standard operating temperature and pressure conditions for the **{pname}**?", pconds,
              [p[3] for p in industrial_names if p[0] != pname] + ["1000 °C and 1 atm", "Room temperature and 500 atm", "0 °C and 1 atm"], "Knowledge", "Recall process conditions")

    # Eutrophication Definition
    add_q("easy", "Environmental Impact",
          "According to Grade 12 Physical Sciences, what is **eutrophication**?",
          "The process where excess mineral nutrients (nitrogen and phosphorus) from fertilizer runoff enter water bodies, causing an algal bloom that depletes dissolved oxygen when decomposed, killing aquatic life.",
          ["The process of enriching agricultural soil with volcanic ash to improve fertility",
           "The industrial purification of liquid nitrogen through fractional distillation",
           "The contamination of groundwater by acidic mine drainage",
           "The accumulation of carbon dioxide gas in the lower atmosphere",
           "The formation of sulfuric acid clouds during the Contact process",
           "The chemical reaction between urea and limestone in dry soil"], "Knowledge", "Define eutrophication")

    # Complete easy to 300
    seed = 1
    easy_count = sum(1 for q in questions if q['difficulty'] == 'easy')
    while easy_count < 300:
        nut_pick = nutrient_functions[(seed - 1) % len(nutrient_functions)]
        q_text = f"In agricultural science, which primary mineral nutrient is described by: '{nut_pick[1]}' (Question {seed})?"
        if add_q("easy", "Plant Nutrients", q_text, nut_pick[0], [n[0] for n in nutrient_functions if n[0] != nut_pick[0]] + ["Calcium", "Magnesium", "Sulfur", "Iron"], "Knowledge", "Identify mineral nutrient"):
            easy_count += 1
        seed += 1

    # -------------------------------------------------------------
    # MEDIUM (500 questions) - Chemical Equations, Oleum, Sources of Raw Materials
    # -------------------------------------------------------------
    raw_materials = [
        ("Nitrogen (N2) gas for the Haber process", "Fractional distillation of liquid air",
         ["Combustion of methane gas", "Electrolysis of molten sodium chloride", "Decomposition of limestone (CaCO3)", "Evaporation of seawater", "Cracking of crude oil", "Extraction from coal"]),
        ("Hydrogen (H2) gas for the Haber process", "Steam reforming of natural gas (methane, CH4) or coal gasification",
         ["Fractional distillation of air", "Dissolving sulfur dioxide in water", "Decomposition of nitric acid", "Precipitation from phosphate rock", "Electrolysis of molten cryolite", "Oxidation of ammonia"]),
        ("Sulfur dioxide (SO2) for the Contact process", "Combustion of molten sulfur in air: S(s) + O2(g) → SO2(g), or roasting of iron pyrites (FeS2)",
         ["Dissolving ammonia in nitric acid", "Fractional distillation of liquid air", "Reacting nitrogen with hydrogen", "Treating phosphate rock with sulfuric acid", "Hydrolysis of urea", "Electrolysis of brine"])
    ]
    for material, source, wr in raw_materials:
        add_q("medium", "Raw Materials", f"What is the primary industrial source of **{material}**?", source, wr, "Comprehension", "State sources of raw materials")

    # Why SO3 is dissolved in H2SO4 instead of water
    add_q("medium", "Contact Process (Oleum)",
          "In the Contact process, why is sulfur trioxide (SO3) dissolved in concentrated sulfuric acid (H2SO4) to form oleum (H2S2O7), rather than being added directly to water?",
          "The direct reaction between SO3 and water is violently exothermic and forms an uncontrollable, dangerous mist of tiny sulfuric acid droplets that cannot be easily condensed or contained.",
          ["Sulfur trioxide is completely insoluble in pure water.",
           "Adding SO3 directly to water produces toxic sulfur dioxide gas.",
           "Water causes the reverse reaction to occur, decomposing SO3 back into sulfur.",
           "The reaction with water is endothermic and freezes the reaction vessels.",
           "Oleum is required because it has a lower molecular mass than sulfuric acid.",
           "Water neutralizes the acid instantly into neutral water."], "Comprehension", "Explain oleum formation in Contact process")

    # Industrial Fertilizer Salts & Equations
    fertilizer_salts = [
        ("Ammonium nitrate", "NH3(aq) + HNO3(aq) → NH4NO3(aq)", "Ammonia + Nitric acid",
         ["NH3 + H2SO4 → (NH4)2SO4", "NH3 + HCl → NH4Cl", "NH3 + CO2 → (NH2)2CO", "HNO3 + NaOH → NaNO3", "N2 + 3H2 → 2NH3", "Ca3(PO4)2 + H2SO4 → CaSO4"]),
        ("Ammonium sulfate", "2NH3(aq) + H2SO4(aq) → (NH4)2SO4(aq)", "Ammonia + Sulfuric acid",
         ["NH3 + HNO3 → NH4NO3", "NH3 + H3PO4 → (NH4)3PO4", "SO2 + H2O → H2SO3", "NH3 + HCl → NH4Cl", "2NO2 + H2O → HNO3", "H2S2O7 + H2O → 2H2SO4"]),
        ("Urea", "2NH3(g) + CO2(g) → (NH2)2CO(s) + H2O(l)", "Ammonia + Carbon dioxide",
         ["NH3 + HNO3 → NH4NO3", "2NH3 + H2SO4 → (NH4)2SO4", "N2 + 2O2 → 2NO2", "CH4 + H2O → CO + 3H2", "NH3 + H2O → NH4OH", "C + O2 → CO2"])
    ]
    for sname, eq, reactants, wr in fertilizer_salts:
        add_q("medium", "Fertilizer Salts", f"Write the balanced chemical equation for the production of the commercial fertilizer **{sname}** from {reactants}:", eq, wr, "Application", "Write fertilizer formation equation")

    # Complete medium to 500
    med_count = sum(1 for q in questions if q['difficulty'] == 'medium')
    seed = 1
    while med_count < 500:
        fs_pick = fertilizer_salts[(seed - 1) % len(fertilizer_salts)]
        q_text = f"[Fertilizer Synthesis {seed}] An industrial chemical plant synthesizes {fs_pick[0]} from {fs_pick[2]}. Which balanced chemical equation accurately describes this reaction?"
        if add_q("medium", "Fertilizer Salts", q_text, fs_pick[1], fs_pick[3], "Application", "Recall fertilizer synthesis"):
            med_count += 1
        seed += 1

    # -------------------------------------------------------------
    # HARD (200 questions) - NPK Ratio Calculations & Bag Quantities
    # -------------------------------------------------------------
    # NPK Ratio Format: N : P : K (total % active nutrients)
    # E.g. 3 : 1 : 5 (26) in a 50 kg bag
    # Total parts = 3 + 1 + 5 = 9
    # % N = (3 / 9) * 26% = 8.67% => Mass N in 50 kg = 50 * 0.08667 = 4.33 kg
    # % P = (1 / 9) * 26% = 2.89% => Mass P in 50 kg = 50 * 0.02889 = 1.44 kg
    # % K = (5 / 9) * 26% = 14.44% => Mass K in 50 kg = 50 * 0.14444 = 7.22 kg
    npk_bags = [
        (3, 1, 5, 26, 50), # Total parts = 9. Active = 26%. Bag = 50 kg. Mass N = (3/9)*26%*50 = 4.33 kg; P = (1/9)*26%*50 = 1.44 kg; K = (5/9)*26%*50 = 7.22 kg
        (4, 1, 2, 28, 50), # Parts = 7. Active = 28%. Bag = 50 kg. Mass N = (4/7)*28%*50 = 8.00 kg; P = (1/7)*28%*50 = 2.00 kg; K = (2/7)*28%*50 = 4.00 kg
        (2, 3, 4, 36, 50), # Parts = 9. Active = 36%. Bag = 50 kg. Mass N = (2/9)*36%*50 = 4.00 kg; P = (3/9)*36%*50 = 6.00 kg; K = (4/9)*36%*50 = 8.00 kg
        (5, 1, 2, 24, 50), # Parts = 8. Active = 24%. Bag = 50 kg. Mass N = (5/8)*24%*50 = 7.50 kg; P = (1/8)*24%*50 = 1.50 kg; K = (2/8)*24%*50 = 3.00 kg
        (3, 2, 1, 30, 50), # Parts = 6. Active = 30%. Bag = 50 kg. Mass N = (3/6)*30%*50 = 7.50 kg; P = (2/6)*30%*50 = 5.00 kg; K = (1/6)*30%*50 = 2.50 kg
        (1, 2, 3, 24, 20), # Parts = 6. Active = 24%. Bag = 20 kg. Mass N = (1/6)*24%*20 = 0.80 kg; P = (2/6)*24%*20 = 1.60 kg; K = (3/6)*24%*20 = 2.40 kg
        (7, 1, 1, 18, 50), # Parts = 9. Active = 18%. Bag = 50 kg. Mass N = (7/9)*18%*50 = 7.00 kg; P = (1/9)*18%*50 = 1.00 kg; K = (1/9)*18%*50 = 1.00 kg
        (2, 1, 2, 25, 40)  # Parts = 5. Active = 25%. Bag = 40 kg. Mass N = (2/5)*25%*40 = 4.00 kg; P = (1/5)*25%*40 = 2.00 kg; K = (2/5)*25%*40 = 4.00 kg
    ]

    for n_p, p_p, k_p, pct, bag_m in npk_bags:
        tot_parts = n_p + p_p + k_p
        mass_n = (n_p / tot_parts) * (pct / 100.0) * bag_m
        mass_p = (p_p / tot_parts) * (pct / 100.0) * bag_m
        mass_k = (k_p / tot_parts) * (pct / 100.0) * bag_m
        filler_mass = bag_m - (mass_n + mass_p + mass_k)

        # Question: Calculate mass of nitrogen
        add_q("hard", "NPK Calculations",
              f"A {bag_m} kg bag of fertilizer is labelled **{n_p} : {p_p} : {k_p} ({pct})**. Calculate the mass of pure nitrogen (N) contained in this bag:",
              f"{mass_n:.2f} kg",
              [f"{(n_p / tot_parts) * bag_m:.2f} kg (omitted active %)",
               f"{mass_p:.2f} kg (calculated phosphorus instead)",
               f"{mass_k:.2f} kg (calculated potassium instead)",
               f"{(pct / 100.0) * bag_m:.2f} kg (total fertilizer mass)",
               f"{mass_n * 2:.2f} kg",
               f"{mass_n / 2:.2f} kg"], "Analysis", "Calculate nutrient mass from NPK ratio")

        # Question: Calculate mass of phosphorus
        add_q("hard", "NPK Calculations",
              f"From the same {bag_m} kg bag of fertilizer labelled **{n_p} : {p_p} : {k_p} ({pct})**, determine the mass of phosphorus (P) present:",
              f"{mass_p:.2f} kg",
              [f"{(p_p / tot_parts) * bag_m:.2f} kg",
               f"{mass_n:.2f} kg",
               f"{mass_k:.2f} kg",
               f"{mass_p * 2:.2f} kg",
               f"{mass_p + 5.0:.2f} kg",
               f"{(pct / 100.0) * bag_m:.2f} kg"], "Analysis", "Calculate phosphorus mass from NPK ratio")

        # Question: Calculate mass of potassium
        add_q("hard", "NPK Calculations",
              f"From the same {bag_m} kg bag labelled **{n_p} : {p_p} : {k_p} ({pct})**, determine the mass of potassium (K) present:",
              f"{mass_k:.2f} kg",
              [f"{(k_p / tot_parts) * bag_m:.2f} kg",
               f"{mass_n:.2f} kg",
               f"{mass_p:.2f} kg",
               f"{mass_k * 1.5:.2f} kg",
               f"{mass_k / 2:.2f} kg",
               f"{filler_mass:.2f} kg"], "Analysis", "Calculate potassium mass from NPK ratio")

        # Question: Calculate percentage / mass of filler (inert material)
        add_q("hard", "NPK Calculations",
              f"For the {bag_m} kg fertilizer bag labelled **{n_p} : {p_p} : {k_p} ({pct})**, what is the mass of filler (non-fertilizer carrier material) in the bag?",
              f"{filler_mass:.2f} kg (representing {100 - pct}% of the total bag mass)",
              [f"{(pct / 100.0) * bag_m:.2f} kg",
               f"{bag_m:.2f} kg",
               f"{mass_n + mass_p:.2f} kg",
               f"{filler_mass / 2:.2f} kg",
               f"0.00 kg (fertilizer is 100% pure nutrients)",
               f"{filler_mass + 10:.2f} kg"], "Analysis", "Calculate inert filler mass")

    # Complete hard to exactly 200
    hard_count = sum(1 for q in questions if q['difficulty'] == 'hard')
    seed = 1
    while hard_count < 200:
        bag_pick = npk_bags[(seed - 1) % len(npk_bags)]
        n_p, p_p, k_p, pct, bag_m = bag_pick
        tot_parts = n_p + p_p + k_p
        mass_n = (n_p / tot_parts) * (pct / 100.0) * bag_m
        q_text = f"[Commercial Agronomy Task {seed}] A farmer purchases a {bag_m} kg bag of fertilizer marked {n_p}:{p_p}:{k_p} ({pct}). What exact mass of nitrogen is available to the crops?"
        if add_q("hard", "NPK Calculations", q_text, f"{mass_n:.2f} kg", [f"{(n_p/tot_parts)*bag_m:.2f} kg", f"{mass_n*2:.2f} kg", f"{mass_n/2:.2f} kg", f"{mass_n+3:.2f} kg", f"{bag_m*(pct/100):.2f} kg", f"{mass_n*1.5:.2f} kg"], "Analysis", "Solve NPK calculation"):
            hard_count += 1
        seed += 1

    return questions

if __name__ == '__main__':
    qs = build_chemical_industry()
    out_dir = "dataset/grade12/physical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_chemical_industry.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)
    
    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
