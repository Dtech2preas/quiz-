import json
import os

def build_chemical_industry():
    questions = []
    seen_questions = set()
    counts = {"easy": 0, "medium": 0, "hard": 0}

    def add_q(difficulty, subtopic, q_text, correct, wrongs, cognitive, outcome, explanation):
        if counts[difficulty] >= (300 if difficulty == "easy" else 500 if difficulty == "medium" else 200):
            return False

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
        counts[difficulty] += 1
        qid = f"PS_P2_IND_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Paper 2: Chemical Industry",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
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

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Plant Nutrients, Industrial Processes & Catalysts, Definitions
    # =========================================================================

    nutrient_data = [
        ("Nitrogen (N)",
         "Promotes rapid vegetative leaf and stem growth, protein synthesis, and chlorophyll formation.",
         ["Promotes strong root development and seed formation",
          "Improves fruit quality and drought resistance in crops",
          "Regulates the opening and closing of leaf stomata",
          "Provides the structural carbon framework for sugars",
          "Acts as a soil pesticide against fungal infestations",
          "Neutralizes excess acidity in agricultural soils"],
         "Nitrogen is essential for green leafy growth, amino acids, proteins, and chlorophyll in all plants.",
         "Chlorosis (yellowing of older leaves) and stunted vegetative growth",
         ["Purple pigmentation on stems and leaf undersides",
          "Scorching, curling, and brown spots on leaf tips and margins",
          "Blossom end rot in tomato fruits",
          "Complete wilting within 2 hours of planting",
          "Sudden blackening of root tips",
          "Excessive rapid flowering with zero foliage"]),

        ("Phosphorus (P)",
         "Promotes strong root system development, flowering, seed and fruit formation, and energy transfer (ATP).",
         ["Promotes vegetative green leaf growth and deep green pigmentation",
          "Improves fruit flavor, skin toughness, and disease resistance",
          "Regulates water balance through stomatal osmotic control",
          "Supplies elemental sulfur for cysteine synthesis",
          "Replaces nitrogen in nucleic acids",
          "Accelerates water evaporation through leaf cuticles"],
         "Phosphorus is essential for cell division, ATP energy transfer, and strong root system establishment.",
         "Purplish discoloration on stems and leaves, accompanied by poor, stunted root growth",
         ["Chlorosis (pale yellowing of all green leaves)",
          "Burnt marginal leaf edges and weak brittle stems",
          "Excessive leaf growth with no roots",
          "White chalky powder on fruit surfaces",
          "Rapid rotting of ripe fruit in storage",
          "Immediate bleaching of chlorophyll into carotene"]),

        ("Potassium (K)",
         "Improves disease resistance, fruit quality, drought tolerance, enzyme activation, and stomatal water regulation.",
         ["Promotes rapid green leaf foliage and vegetative biomass",
          "Promotes root growth, seed germination, and ATP energy storage",
          "Forms the central metal ion in chlorophyll molecules",
          "Provides nitrogen atoms for protein construction",
          "Lowers soil pH by generating sulfuric acid",
          "Prevents weeds from absorbing groundwater"],
         "Potassium regulates osmotic potential, activates over 60 enzymes, and enhances overall crop stress tolerance.",
         "Browning and scorching of leaf margins and tips, weak stems, and poor fruit development",
         ["General chlorosis starting with older leaves turning bright yellow",
          "Purplish coloration on the underside of young leaves",
          "Rapid shedding of root hairs",
          "Total absence of floral buds",
          "Excessive root expansion cracking the topsoil",
          "Leaves turning completely translucent"])
    ]

    crops = [
        ("maize (corn)", "cereal grain"),
        ("wheat", "winter grain"),
        ("spinach", "leafy green vegetable"),
        ("cabbage", "brassica leafy vegetable"),
        ("lettuce", "salad leafy crop"),
        ("potatoes", "root tuber crop"),
        ("carrots", "root vegetable"),
        ("tomatoes", "fruiting crop"),
        ("citrus trees (oranges/lemons)", "orchard fruit"),
        ("sugarcane", "high-biomass perennial grass"),
        ("sunflowers", "oilseed crop"),
        ("pasture lawn grass", "turf grass"),
        ("apples", "deciduous fruit tree"),
        ("grapes (vineyards)", "fruit vine"),
        ("lucerne (alfalfa)", "legume forage crop")
    ]

    # Nutrients functions and deficiencies across crops
    for nut, func, wr_func, exp_func, defic, wr_def in nutrient_data:
        exp_def = f"A deficiency of {nut} leads to {defic.lower()}."
        # Core function
        add_q("easy", "Plant Nutrients",
              f"What is the primary agricultural function of the primary plant macronutrient **{nut}** in crop development?",
              func, wr_func, "Remembering", "Recall nutrient function", exp_func)

        # Deficiency symptom
        add_q("easy", "Plant Nutrients",
              f"What visible deficiency symptom is typically observed when agricultural crops lack sufficient **{nut}**?",
              defic, wr_def, "Understanding", "Identify nutrient deficiency symptom", exp_def)

        # Crop-specific applications
        for crop_name, crop_type in crops:
            add_q("easy", "Plant Nutrients",
                  f"When cultivating **{crop_name}** ({crop_type}), which primary macronutrient is most critical for: {func.split(',')[0].lower()}?",
                  nut, [n[0] for n in nutrient_data if n[0] != nut] + ["Calcium (Ca)", "Magnesium (Mg)", "Sulfur (S)", "Iron (Fe)"],
                  "Applying", f"Select nutrient for {crop_name}",
                  f"For {crop_name}, {nut} is required because it {func.lower()}.")

    # The 3 Great Industrial Processes & Operating Conditions
    processes = [
        ("Haber Process",
         "The industrial manufacture of ammonia (NH3) from nitrogen gas (N2) and hydrogen gas (H2).",
         "N2(g) + 3H2(g) ⇌ 2NH3(g) (ΔH = -92 kJ·mol⁻¹)",
         "Iron (Fe) or iron oxide (Fe3O4) with promoters (Al2O3 / K2O)",
         "450 °C",
         "200 atm (approx. 20 000 kPa)",
         ["Ostwald Process", "Contact Process", "Hall-Héroult Process", "Downs Process", "Solvay Process", "Bessemer Process"]),

        ("Ostwald Process",
         "The industrial manufacture of nitric acid (HNO3) from ammonia (NH3), oxygen (O2), and water.",
         "Catalytic oxidation of ammonia followed by oxidation and absorption: 4NH3 + 5O2 -> 4NO + 6H2O",
         "Platinum-Rhodium gauze (Pt/Rh)",
         "850 °C to 900 °C",
         "1 to 5 atm (approx. 100 to 500 kPa)",
         ["Haber Process", "Contact Process", "Hall-Héroult Process", "Downs Process", "Frasch Process", "Chlor-Alkali Process"]),

        ("Contact Process",
         "The industrial manufacture of sulfuric acid (H2SO4) from sulfur, air (O2), and water via sulfur trioxide and oleum.",
         "Catalytic oxidation of SO2: 2SO2(g) + O2(g) ⇌ 2SO3(g) (ΔH = -197 kJ·mol⁻¹)",
         "Vanadium pentoxide (V2O5)",
         "450 °C",
         "1 to 2 atm (approx. 100 to 200 kPa)",
         ["Haber Process", "Ostwald Process", "Hall-Héroult Process", "Downs Process", "Bayer Process", "Castner-Kellner Process"])
    ]

    for pname, pdesc, peq, pcatalyst, ptemp, ppres, wr_p in processes:
        add_q("easy", "Industrial Processes",
              f"Which industrial chemical process is defined as: **'{pdesc}'**?",
              pname, wr_p, "Remembering", "Identify industrial process",
              f"{pname} is {pdesc.lower()}.")

        add_q("easy", "Catalysts",
              f"What catalyst is industrially employed in the **{pname}**?",
              pcatalyst,
              [p[3] for p in processes if p[0] != pname] + ["Nickel (Ni)", "Copper (Cu)", "Manganese dioxide (MnO2)", "Silver (Ag)"],
              "Remembering", f"Recall catalyst for {pname}",
              f"The standard catalyst for the {pname} is {pcatalyst}.")

        add_q("easy", "Reaction Conditions",
              f"What is the typical operating temperature used in the **{pname}**?",
              ptemp,
              [p[4] for p in processes if p[0] != pname] + ["25 °C (room temp)", "100 °C", "2000 °C", "0 °C"],
              "Remembering", f"Recall temperature for {pname}",
              f"The operational temperature in the {pname} is maintained around {ptemp}.")

        add_q("easy", "Reaction Conditions",
              f"What is the typical operating pressure used in the **{pname}**?",
              ppres,
              [p[5] for p in processes if p[0] != pname] + ["1000 atm", "0.01 atm (vacuum)", "50 atm", "500 atm"],
              "Remembering", f"Recall pressure for {pname}",
              f"The operating pressure in the {pname} is {ppres}.")

    # Definitions and Concepts
    general_concepts = [
        ("Eutrophication",
         "The enrichment of an aquatic ecosystem with excess chemical nutrients (especially nitrates and phosphates), causing rapid algal growth and subsequent dissolved oxygen depletion.",
         ["The acidification of groundwater caused by sulfuric acid runoff from gold mines",
          "The chemical decomposition of limestone rocks by industrial acid rain",
          "The accumulation of carbon dioxide gas in the troposphere creating global warming",
          "The industrial distillation of liquid air into pure nitrogen and oxygen",
          "The artificial addition of inert gypsum filler to agricultural fertilizers",
          "The erosion of fertile topsoil by wind and rain in arid regions"],
         "Eutrophication is caused by nutrient runoff (nitrates and phosphates), leading to algal blooms and dead aquatic zones."),

        ("Inert Filler Material",
         "A chemically inactive substance (such as sand, limestone, gypsum, or clay) added to commercial fertilizers to facilitate even spreading and prevent burning of plant roots.",
         ["A toxic pesticide added to fertilizers to kill insects in the soil",
          "A catalytic agent that accelerates nitrogen absorption by roots",
          "A concentrated source of extra potassium ions in the fertilizer bag",
          "A chemical dye that turns the fertilizer pellets green",
          "An organic compound that prevents water from dissolving the pellets",
          "A radioactive tracer used to monitor soil moisture levels"],
         "Filler material (typically limestone, gypsum, or sand) bulks out the fertilizer for even application and prevents high salt concentration root burn."),

        ("Macronutrient",
         "An essential chemical element required by agricultural crops in relatively large quantities for healthy growth and development.",
         ["A trace mineral needed only in microscopic amounts by plants",
          "A synthetic chemical pesticide that protects against fungal blight",
          "A pollutant that causes aquatic dead zones when released into rivers",
          "A non-metallic catalyst used in the manufacture of ammonia",
          "An inert carrier material that makes up the bulk of a fertilizer bag",
          "A hormone that stimulates premature leaf shedding in autumn"],
         "Macronutrients (N, P, K, Ca, Mg, S) are required in large quantities, unlike micronutrients which are needed in trace amounts."),

        ("Non-mineral Nutrients",
         "Carbon (C), hydrogen (H), and oxygen (O), which plants obtain naturally from carbon dioxide in air and water from soil, rather than from mineral fertilizers.",
         ["Nitrogen, phosphorus, and potassium obtained from rock mining",
          "Calcium, magnesium, and sulfur absorbed through commercial lime",
          "Iron, zinc, and copper added as chemical chelates to irrigation water",
          "Insoluble plastics added to bulk out fertilizer bags",
          "Silica sand and gypsum mixed into potting soil",
          "Synthetic pesticides sprayed on crop foliage"],
         "Carbon, hydrogen, and oxygen are supplied by air (CO2) and water (H2O) and form the bulk of plant biomass via photosynthesis.")
    ]

    for cname, cdef, wr_defs, cexp in general_concepts:
        stems = [
            f"In Grade 12 Physical Sciences, how is **{cname}** defined?",
            f"Which statement correctly describes the concept of **{cname}**?",
            f"According to the CAPS curriculum, what does **{cname}** refer to?"
        ]
        for st in stems:
            add_q("easy", "Definitions", st, cdef, wr_defs, "Remembering", f"Define {cname}", cexp)

    # Fertilizer salts formulas and naming
    salts_easy = [
        ("Ammonium nitrate", "NH4NO3", ["(NH4)2SO4", "NH4Cl", "KNO3", "NaNO3", "(NH2)2CO", "Ca(NO3)2"]),
        ("Ammonium sulfate", "(NH4)2SO4", ["NH4NO3", "(NH4)3PO4", "K2SO4", "CaSO4", "(NH2)2CO", "MgSO4"]),
        ("Ammonium phosphate", "(NH4)3PO4", ["NH4NO3", "(NH4)2SO4", "Ca3(PO4)2", "K3PO4", "Na3PO4", "NH4H2PO4"]),
        ("Urea", "(NH2)2CO", ["NH4NO3", "(NH4)2SO4", "NH4Cl", "CH3CONH2", "KNO3", "CaCN2"]),
        ("Potassium nitrate", "KNO3", ["K2SO4", "KCl", "NH4NO3", "NaNO3", "K3PO4", "K2CO3"]),
        ("Potassium chloride (muriate of potash)", "KCl", ["K2SO4", "KNO3", "NaCl", "CaCl2", "K3PO4", "NH4Cl"]),
        ("Potassium sulfate", "K2SO4", ["KCl", "KNO3", "Na2SO4", "(NH4)2SO4", "MgSO4", "CaSO4"]),
        ("Sulfur trioxide", "SO3", ["SO2", "H2SO4", "H2S2O7", "S8", "SO4²⁻", "H2S"]),
        ("Oleum (fuming sulfuric acid)", "H2S2O7", ["H2SO4", "H2SO3", "SO3", "H2S", "H2S2O8", "(NH4)2SO4"]),
        ("Nitrogen dioxide", "NO2", ["NO", "N2O", "N2O4", "N2O5", "HNO3", "NH3"]),
        ("Nitric oxide (nitrogen monoxide)", "NO", ["NO2", "N2O", "N2O4", "NH3", "HNO3", "N2"])
    ]

    for sname, sform, wr_forms in salts_easy:
        add_q("easy", "Fertilizer Salts",
              f"What is the correct chemical formula for the agricultural chemical / fertilizer compound **{sname}**?",
              sform, wr_forms, "Remembering", f"Recall formula of {sname}",
              f"The chemical formula for {sname} is {sform}.")

    # Fill easy to exactly 300 with rich, diverse questions about raw materials and sources
    raw_materials_easy = [
        ("Nitrogen gas (N2) for the Haber process", "Fractional distillation of liquid air",
         ["Steam reforming of natural gas", "Cracking of petroleum crude oil", "Electrolysis of sea water", "Roasting of iron pyrites", "Evaporation of brine pools", "Thermal decomposition of limestone"]),
        ("Hydrogen gas (H2) for the Haber process", "Steam reforming of natural gas (methane, CH4) or coal gasification",
         ["Fractional distillation of liquid air", "Combustion of charcoal in air", "Decomposition of nitric acid", "Precipitation of phosphate rock", "Electrolysis of molten bauxite", "Condensation of atmospheric humidity"]),
        ("Sulfur (S) for the Contact process", "Frasch mining process of underground sulfur deposits, or recovery from petroleum/natural gas refining",
         ["Fractional distillation of air", "Direct extraction from seawater", "Electrolysis of potassium chloride", "Thermal decomposition of ammonium sulfate", "Bacterial fermentation of compost", "Condensation of volcanic ash"]),
        ("Phosphate rock (fluorapatite) for phosphate fertilizers", "Open-cast mining from phosphate rock deposits (such as Phalaborwa and Langebaan in South Africa)",
         ["Fractional distillation of ocean water", "Synthesis from nitrogen and hydrogen gases", "Combustion of bituminous coal", "Extraction from atmospheric dust", "Electrolytic refining of blister copper", "Condensation of volcanic steam"]),
        ("Potassium salts (sylvite / KCl) for potassium fertilizers", "Mining of underground evaporite potash salt deposits (such as sylvinite and carnallite)",
         ["Distillation of liquid air", "Electrolysis of acidified water", "Precipitation from sulfuric acid gas", "Oxidation of ammonia gas", "Roasting of iron ore in blast furnaces", "Extraction from timber sawdust"])
    ]

    for raw_item, source, wr_src in raw_materials_easy:
        stems_raw = [
            f"What is the primary industrial source of **{raw_item}**?",
            f"Where does industry obtain **{raw_item}** on a commercial scale?",
            f"Which industrial method provides **{raw_item}** for South African fertilizer production?"
        ]
        for st in stems_raw:
            add_q("easy", "Raw Materials", st, source, wr_src, "Remembering", f"Recall source of {raw_item.split()[0]}",
                  f"{raw_item} is industrially obtained via {source.lower()}.")

    # Complete easy to 300 with questions on NPK ratio labels
    npk_label_samples = [
        ("3 : 1 : 5 (26)", "3 parts Nitrogen, 1 part Phosphorus, 5 parts Potassium, with 26% active nutrient content and 74% filler",
         ["3% Nitrogen, 1% Phosphorus, 5% Potassium, and 26 kg total bag mass",
          "3 parts Potassium, 1 part Phosphorus, 5 parts Nitrogen, with 26% inert sand",
          "A fertilizer containing 26 different mineral trace elements in a 3:1:5 ratio",
          "30% Nitrogen, 10% Phosphorus, 50% Potassium, with 26% moisture",
          "3 kg Nitrogen, 1 kg Phosphorus, 5 kg Potassium, and 26 kg lime",
          "A fertilizer suitable only for soil with a pH of 2.6"]),

        ("2 : 3 : 2 (22)", "2 parts Nitrogen, 3 parts Phosphorus, 2 parts Potassium, with 22% active nutrient content and 78% filler",
         ["2% Nitrogen, 3% Phosphorus, 2% Potassium, and 22 kg total mass",
          "2 parts Potassium, 3 parts Nitrogen, 2 parts Phosphorus, with 22% water",
          "A fertilizer containing 22% inert stone and 78% pure nitrogen",
          "2 kg Nitrogen, 3 kg Phosphorus, 2 kg Potassium, and 22 kg filler",
          "20% Nitrogen, 30% Phosphorus, 20% Potassium, with 22% sulfur",
          "A ratio designed exclusively for hydroponic tomato crops"]),

        ("7 : 1 : 1 (30)", "7 parts Nitrogen, 1 part Phosphorus, 1 part Potassium, with 30% active nutrient content and 70% filler",
         ["7% Nitrogen, 1% Phosphorus, 1% Potassium, with 30 kg bag mass",
          "7 parts Potassium, 1 part Phosphorus, 1 part Nitrogen, with 30% sand",
          "A fertilizer where 70% of the bag is pure nitrogen",
          "7 kg Nitrogen, 1 kg Phosphorus, 1 kg Potassium, and 30 kg limestone",
          "70% Nitrogen, 10% Phosphorus, 10% Potassium, with 30% gypsum",
          "A high-phosphorus fertilizer for root development in fruit trees"]),

        ("1 : 1 : 1 (36)", "Equal proportions of Nitrogen, Phosphorus, and Potassium (1:1:1), with 36% active nutrient content and 64% filler",
         ["1% Nitrogen, 1% Phosphorus, 1% Potassium, with 36 kg total weight",
          "1 part Potassium, 1 part Nitrogen, 1 part Calcium, with 36% water",
          "A fertilizer containing 36 kg of active nitrogen alone",
          "10% Nitrogen, 10% Phosphorus, 10% Potassium, and 36% filler",
          "A chemical blend that contains no inert carrier material",
          "An organic fertilizer certified 100% natural manure"])
    ]

    for label_str, meaning, wr_means in npk_label_samples:
        add_q("easy", "NPK Notation",
              f"On a commercial fertilizer bag, what does the label **'{label_str}'** mean?",
              meaning, wr_means, "Understanding", "Interpret NPK ratio label",
              f"The numbers N:P:K indicate the relative mass ratio of Nitrogen, Phosphorus, and Potassium. The bracketed number is the total percentage of active fertilizer nutrients by mass in the bag.")

    # Fill easy to exactly 300
    for n_val in range(1, 7):
        for p_val in range(1, 6):
            for k_val in range(1, 7):
                for pct_val in [12, 14, 16, 18, 20, 22, 24, 25, 26, 28, 30, 32, 34, 35, 36, 40]:
                    if counts["easy"] >= 300:
                        break
                    tot_parts = n_val + p_val + k_val
                    q_text = f"A commercial bag of fertilizer is labelled **{n_val} : {p_val} : {k_val} ({pct_val})**. What percentage of the total bag mass consists of inert filler material?"
                    filler_pct = 100 - pct_val
                    corr_str = f"{filler_pct}%"
                    wrs = [
                        f"{pct_val}%",
                        f"{tot_parts}%",
                        f"{round((n_val / tot_parts) * 100)}%",
                        f"{round((p_val / tot_parts) * 100)}%",
                        f"{round((k_val / tot_parts) * 100)}%",
                        "0% (it contains no filler)",
                        f"{filler_pct / 2:.1f}%",
                        f"{filler_pct + 10}%"
                    ]
                    add_q("easy", "NPK Notation", q_text, corr_str, wrs, "Applying", "Calculate filler percentage from NPK label",
                          f"The bracketed number ({pct_val}%) is the percentage of active nutrients. The percentage of inert filler is 100% - {pct_val}% = {filler_pct}%.")

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Chemical Equations, Le Chatelier Compromises, Oleum, Crop Selection, Eutrophication
    # =========================================================================

    chemical_equations = [
        # Haber Process
        ("Haber Process overall synthesis",
         "N2(g) + 3H2(g) ⇌ 2NH3(g) (ΔH = -92 kJ·mol⁻¹)",
         ["N2(g) + H2(g) ⇌ 2NH(g)", "2NH3(g) ⇌ N2(g) + 3H2(g)", "N2(g) + 2H2(g) -> N2H4(l)", "NH3(g) + H2O(l) ⇌ NH4⁺(aq) + OH⁻(aq)", "N2(g) + 3H2O(l) -> 2NH3(g) + 1.5O2(g)", "2N2(g) + 6H2(g) -> 4NH3(g) (ΔH > 0)"],
         "The Haber synthesis combines nitrogen and hydrogen gas in a 1:3 ratio over an iron catalyst: N2(g) + 3H2(g) ⇌ 2NH3(g)."),

        # Ostwald Process Step 1
        ("Ostwald Process Step 1 (Catalytic oxidation of ammonia)",
         "4NH3(g) + 5O2(g) -> 4NO(g) + 6H2O(g) (over Pt-Rh catalyst at 850 °C)",
         ["2NH3(g) + 2O2(g) -> N2O(g) + 3H2O(g)", "NH3(g) + 2O2(g) -> HNO3(l) + H2O(l)", "4NH3(g) + 3O2(g) -> 2N2(g) + 6H2O(g)", "4NH3(g) + 7O2(g) -> 4NO2(g) + 6H2O(g)", "2NH3(g) + O2(g) -> 2NO(g) + 3H2(g)", "NH3(g) + O2(g) -> NO2(g) + H2(g)"],
         "Step 1 of the Ostwald process oxidises ammonia using a platinum-rhodium gauze catalyst at 850-900 °C: 4NH3 + 5O2 -> 4NO + 6H2O."),

        # Ostwald Process Step 2
        ("Ostwald Process Step 2 (Oxidation of nitric oxide)",
         "2NO(g) + O2(g) ⇌ 2NO2(g) (formation of brown nitrogen dioxide gas)",
         ["NO(g) + O2(g) -> NO3(g)", "4NO(g) + 3O2(g) -> 2N2O5(g)", "2NO(g) -> N2(g) + O2(g)", "NO(g) + H2O(l) -> HNO2(aq)", "2NO(g) + 2H2(g) -> N2(g) + 2H2O(g)", "NO(g) + O3(g) -> NO2(g) + O2(g)"],
         "Step 2 cools the gas and reacts colorless NO with excess oxygen to form dense red-brown NO2: 2NO + O2 ⇌ 2NO2."),

        # Ostwald Process Step 3
        ("Ostwald Process Step 3 (Absorption of nitrogen dioxide in water)",
         "3NO2(g) + H2O(l) -> 2HNO3(aq) + NO(g) (or 4NO2 + 2H2O + O2 -> 4HNO3)",
         ["NO2(g) + H2O(l) -> HNO2(aq)", "2NO2(g) + H2O(l) -> N2O(g) + H2SO4(aq)", "NO2(g) + 2H2O(l) -> NH4NO3(aq)", "4NO2(g) + H2O(l) -> 2HNO3(aq) + N2O3(g)", "NO2(g) + H2(g) -> NH3(g) + O2(g)", "2NO2(g) + H2O(l) -> HNO3(aq) + HNO2(aq)"],
         "Step 3 absorbs nitrogen dioxide in water to yield nitric acid; the byproduct NO is recycled back to Step 2: 3NO2 + H2O -> 2HNO3 + NO."),

        # Contact Process Step 1
        ("Contact Process Step 1 (Production of sulfur dioxide)",
         "S(s) + O2(g) -> SO2(g) (or 4FeS2 + 11O2 -> 2Fe2O3 + 8SO2 by roasting iron pyrites)",
         ["S(s) + 2O2(g) -> SO4(g)", "2S(s) + 3O2(g) -> 2SO3(g)", "S(s) + H2O(l) -> H2S(g) + O2(g)", "SO2(g) + H2O(l) -> H2SO3(aq)", "FeS2(s) + O2(g) -> Fe(s) + 2SO2(g)", "S8(s) + 4O2(g) -> 8SO(g)"],
         "Molten sulfur is sprayed into dry air to burn cleanly into sulfur dioxide: S(s) + O2(g) -> SO2(g)."),

        # Contact Process Step 2
        ("Contact Process Step 2 (Catalytic oxidation of sulfur dioxide)",
         "2SO2(g) + O2(g) ⇌ 2SO3(g) (ΔH = -197 kJ·mol⁻¹, over V2O5 at 450 °C)",
         ["SO2(g) + O2(g) -> SO4(g)", "SO2(g) + H2O(l) -> H2SO3(l)", "2SO3(g) ⇌ 2SO2(g) + O2(g)", "SO2(g) + 2O2(g) -> SO6(g)", "2SO2(g) + O2(g) -> 2SO(g) + 2O2(g)", "SO2(g) + O3(g) -> SO3(g) + O2(g)"],
         "The key reversible step in the Contact process oxidises SO2 to SO3 using vanadium pentoxide (V2O5) catalyst: 2SO2 + O2 ⇌ 2SO3."),

        # Contact Process Step 3a (Oleum formation)
        ("Contact Process Step 3a (Formation of oleum)",
         "SO3(g) + H2SO4(l) -> H2S2O7(l) (sulfur trioxide dissolved in concentrated sulfuric acid)",
         ["SO3(g) + H2O(l) -> H2SO4(l) (direct violent reaction with water)", "SO3(g) + 2H2SO4(l) -> H4S3O11(l)", "2SO3(g) + H2SO4(l) -> H2S3O10(l)", "SO3(g) + H2(g) -> H2SO3(l)", "SO3(g) + HNO3(aq) -> H2SO4(l) + NO2(g)", "SO3(g) + SO2(g) -> S2O5(g)"],
         "SO3 is dissolved into concentrated 98% H2SO4 to form oleum (pyrosulfuric acid, H2S2O7) rather than water."),

        # Contact Process Step 3b (Dilution of oleum)
        ("Contact Process Step 3b (Dilution of oleum to produce sulfuric acid)",
         "H2S2O7(l) + H2O(l) -> 2H2SO4(l)",
         ["H2S2O7(l) + 2H2O(l) -> 2H2SO3(l) + O2(g)", "H2S2O7(l) -> 2SO3(g) + H2O(l)", "H2S2O7(l) + O2(g) -> 2H2SO5(l)", "H2S2O7(l) + H2SO4(l) -> 3SO3(g) + 2H2O(l)", "H2S2O7(l) + 2H2O(l) -> 2H2S(g) + 5O2(g)", "H2S2O7(l) -> H2SO4(l) + SO3(g)"],
         "Controlled addition of water to oleum safely produces two molecules of pure, concentrated sulfuric acid: H2S2O7 + H2O -> 2H2SO4."),

        # Fertilizer Salt Syntheses
        ("Ammonium nitrate production",
         "NH3(g) + HNO3(aq) -> NH4NO3(aq) (acid-base neutralization of ammonia by nitric acid)",
         ["2NH3 + HNO3 -> (NH4)2NO3", "NH3 + 2HNO3 -> NH4(NO3)2", "N2 + 2HNO3 -> 2NH4NO3", "NH4OH + HNO3 -> NH4NO3 + H2", "NH3 + NO2 + H2O -> NH4NO3", "2NH3 + N2O5 -> 2NH4NO3"],
         "Ammonia reacts with nitric acid in an exothermic acid-base neutralization to produce ammonium nitrate: NH3 + HNO3 -> NH4NO3."),

        ("Ammonium sulfate production",
         "2NH3(g) + H2SO4(aq) -> (NH4)2SO4(aq) (reaction of ammonia with sulfuric acid)",
         ["NH3 + H2SO4 -> NH4HSO4", "2NH3 + 2H2SO4 -> 2(NH4)2SO4 + H2", "NH3 + H2SO4 -> (NH4)2SO4", "4NH3 + H2SO4 -> (NH4)4SO4", "2NH4OH + SO3 -> (NH4)2SO4 + H2O", "NH3 + SO2 + H2O -> (NH4)2SO3"],
         "Two moles of ammonia neutralize one mole of diprotic sulfuric acid: 2NH3 + H2SO4 -> (NH4)2SO4."),

        ("Ammonium phosphate production",
         "3NH3(g) + H3PO4(aq) -> (NH4)3PO4(aq) (reaction of ammonia with phosphoric acid)",
         ["NH3 + H3PO4 -> (NH4)3PO4", "2NH3 + H3PO4 -> (NH4)2HPO4", "NH3 + H3PO4 -> NH4H2PO4", "3NH4OH + P2O5 -> (NH4)3PO4", "NH3 + 3H3PO4 -> NH4(H2PO4)3", "6NH3 + P4O10 + 6H2O -> 4(NH4)3PO4"],
         "Three moles of ammonia neutralize one mole of triprotic phosphoric acid to form triammonium phosphate: 3NH3 + H3PO4 -> (NH4)3PO4."),

        ("Urea production",
         "2NH3(g) + CO2(g) ⇌ (NH2)2CO(s) + H2O(l) (synthesis from ammonia and carbon dioxide)",
         ["NH3 + CO2 -> NH2COOH", "2NH3 + CO -> (NH2)2CO + H2", "NH3 + CO2 -> (NH4)2CO3", "4NH3 + 2CO2 -> 2(NH2)2CO + O2", "2NH3 + CH4 -> (NH2)2CO + 3H2", "NH3 + HCN + H2O -> (NH2)2CO"],
         "Urea is synthesized industrially at high pressure from ammonia and carbon dioxide: 2NH3 + CO2 -> (NH2)2CO + H2O."),

        ("Superphosphate manufacture from rock phosphate",
         "Ca3(PO4)2(s) + 2H2SO4(aq) -> Ca(H2PO4)2(aq) + 2CaSO4(s) (single superphosphate)",
         ["Ca3(PO4)2 + H2SO4 -> CaSO4 + 2H3PO4", "Ca3(PO4)2 + 3H2SO4 -> 3CaSO4 + 2H3PO4", "Ca3(PO4)2 + 2H2O -> 3CaO + 2H3PO4", "Ca3(PO4)2 + 4HNO3 -> 3Ca(NO3)2 + 2H3PO4", "Ca3(PO4)2 + H2SO4 -> Ca2(PO4)2 + CaSO4", "2Ca3(PO4)2 + 6H2SO4 -> 6CaSO4 + P4O10"],
         "Insoluble rock phosphate Ca3(PO4)2 is treated with sulfuric acid to make soluble monocalcium phosphate Ca(H2PO4)2 (superphosphate), which plant roots can absorb."),

        ("Triple superphosphate manufacture",
         "Ca3(PO4)2(s) + 4H3PO4(aq) -> 3Ca(H2PO4)2(aq) (treatment with phosphoric acid, yielding no calcium sulfate byproduct)",
         ["Ca3(PO4)2 + 2H3PO4 -> 2Ca(H2PO4)2 + CaHPO4", "Ca3(PO4)2 + H3PO4 -> 3CaHPO4", "Ca3(PO4)2 + 6H3PO4 -> 3Ca(H2PO4)2 + 2P2O5", "Ca3(PO4)2 + 4H2SO4 -> 3CaSO4 + 4H3PO4", "Ca3(PO4)2 + 2H2O -> 2CaHPO4 + Ca(OH)2", "3Ca3(PO4)2 + 12H3PO4 -> 9Ca(H2PO4)2"],
         "Triple superphosphate is produced by treating rock phosphate with phosphoric acid instead of sulfuric acid, yielding a much higher percentage of available phosphorus without CaSO4 filler.")
    ]

    for eq_title, corr_eq, wr_eqs, expl_eq in chemical_equations:
        stems_eq = [
            f"What is the balanced chemical equation representing: **{eq_title}**?",
            f"Which chemical equation correctly describes: **{eq_title}**?",
            f"Identify the official CAPS-approved equation for: **{eq_title}**:"
        ]
        for st in stems_eq:
            add_q("medium", "Chemical Equations", st, corr_eq, wr_eqs, "Application", f"Write equation for {eq_title}", expl_eq)

    # Le Chatelier Compromise Explanations in Haber and Contact Processes
    compromise_questions = [
        ("Why is a compromise temperature of 450 °C used in the Haber process, rather than a much lower temperature (e.g. 50 °C) or a much higher temperature (e.g. 1000 °C)?",
         "Because the forward reaction is exothermic (ΔH < 0), low temperatures favor higher equilibrium yield of NH3 but result in an impractically slow reaction rate; 450 °C balances acceptable yield with an economically viable reaction rate.",
         ["At lower temperatures the iron catalyst melts and becomes poisoned.",
          "High temperatures cause nitrogen and hydrogen gases to solidify.",
          "450 °C is the only temperature at which the reaction is endothermic.",
          "Lower temperatures reverse the equilibrium completely into nitrogen dioxide.",
          "450 °C causes nitrogen molecules to lose all activation energy.",
          "Iron catalyst only conducts electrons at exactly 450 °C."],
         "In exothermic equilibrium reactions, lower temperature increases yield (Le Chatelier) but drastically slows reaction rate. 450 °C is the optimum economic compromise."),

        ("Why is an extremely high pressure of 200 atm (20 000 kPa) utilized in the Haber process?",
         "According to Le Chatelier's principle, high pressure shifts the equilibrium toward the side with fewer gas moles (4 moles of reactant gas -> 2 moles of product gas), increasing both the equilibrium yield and the reaction rate.",
         ["High pressure cools the reaction vessel to prevent overheating.",
          "High pressure is required to keep the iron catalyst in the solid state.",
          "High pressure prevents toxic nitric oxide from escaping the chamber.",
          "High pressure converts ammonia gas into liquid nitrogen instantly.",
          "High pressure eliminates the need for any chemical catalyst.",
          "High pressure ensures that nitrogen molecules undergo nuclear fusion."],
         "The reaction N2(g) + 3H2(g) ⇌ 2NH3(g) converts 4 moles of gas into 2 moles of gas. Increasing pressure favors the forward reaction and increases collision frequency."),

        ("Why is the Contact process operated at a relatively low pressure (1 to 2 atm), unlike the Haber process which requires 200 atm?",
         "The equilibrium conversion of SO2 to SO3 at 1 to 2 atm is already exceptionally high (approx. 98%), so the enormous financial cost and safety hazards of high-pressure equipment are unnecessary.",
         ["High pressure causes vanadium pentoxide catalyst to vaporize.",
          "The Contact process reaction produces more gas moles on the product side.",
          "Sulfur dioxide explodes violently when compressed above 3 atm.",
          "Sulfuric acid can only exist as a gas at high pressures.",
          "Atmospheric pressure prevents oleum from forming.",
          "The forward reaction in the Contact process is endothermic."],
         "Because the equilibrium yield of SO3 is already ~98% at 1-2 atm and 450 °C, building high-pressure reactors would yield negligible extra product while exponentially increasing capital costs."),

        ("In the Contact process, why is sulfur trioxide (SO3) dissolved into concentrated sulfuric acid (H2SO4) to form oleum, instead of being added directly to water?",
         "The direct reaction between SO3 and water is violently exothermic and vaporizes the water, producing a dense, uncontrollable, highly corrosive mist of sulfuric acid droplets that cannot be condensed or contained.",
         ["Sulfur trioxide is completely insoluble in pure liquid water.",
          "Direct reaction with water produces neutral hydrogen sulfide gas.",
          "Water acts as a permanent catalyst poison that destroys V2O5.",
          "Oleum is non-corrosive and safer to transport in wooden barrels.",
          "Water reverses the oxidation and converts SO3 back into elemental sulfur.",
          "Direct reaction with water freezes the absorption tower into ice."],
         "SO3 + H2O -> H2SO4 has an extreme enthalpy of reaction that boils water into a hazardous acid fog. Dissolving SO3 in conc. H2SO4 to form oleum avoids this uncontrolled vaporization."),

        ("What role does the Vanadium pentoxide (V2O5) catalyst play in Step 2 of the Contact process?",
         "It increases the rates of both the forward and reverse reactions equally by providing an alternative reaction pathway with a lower activation energy, without altering the equilibrium position or yield of SO3.",
         ["It shifts the dynamic equilibrium toward the right, producing 100% yield.",
          "It lowers the activation energy of the forward reaction exclusively.",
          "It reacts stoichiometrically with SO2 to supply oxygen atoms permanently.",
          "It absorbs excess heat to make the reaction endothermic.",
          "It prevents sulfur trioxide from decomposing into sulfur dioxide.",
          "It increases the total pressure inside the catalyst bed."],
         "Catalysts provide an alternative reaction pathway with lower activation energy; they increase reaction rate equally in both directions without altering equilibrium constants or yields.")
    ]

    for q_comp, c_comp, w_comp, exp_comp in compromise_questions:
        add_q("medium", "Reaction Conditions", q_comp, c_comp, w_comp, "Understanding", "Explain industrial compromises using Le Chatelier", exp_comp)

    # Crop-specific fertilizer recommendations
    crop_recommendations = [
        ("A farmer cultivating leafy green vegetables (such as spinach, lettuce, and cabbage)",
         "High Nitrogen (N) fertilizer (such as 7:1:1 or 5:1:2)",
         "Nitrogen stimulates vegetative leaf and shoot development, vigorous green foliage, and chlorophyll synthesis.",
         ["High Phosphorus (P) fertilizer (such as 2:3:2)", "High Potassium (K) fertilizer (such as 3:1:5)", "Zero-nitrogen bone meal", "Pure limestone with zero NPK", "Potassium chloride alone", "Gypsum sulfur powder"]),

        ("A farmer planting new seedlings, maize root crops, or potatoes requiring extensive root system establishment",
         "High Phosphorus (P) fertilizer (such as 2:3:2 or 1:3:1)",
         "Phosphorus promotes early root development, strong lateral root branching, and rapid seed establishment.",
         ["High Nitrogen (N) fertilizer (such as 8:1:1)", "High Potassium (K) fertilizer (such as 1:1:3)", "Pure urea (46-0-0)", "Sand filler alone", "Ammonium nitrate alone", "Elemental sulfur powder"]),

        ("An orchard farmer growing fruit trees (such as citrus, peaches, and apples) approaching flowering and fruit ripening",
         "High Potassium (K) fertilizer (such as 3:1:5 or 1:1:3)",
         "Potassium enhances flower bud formation, fruit sugar content, fruit size, skin toughness, and drought resistance.",
         ["High Nitrogen (N) fertilizer (such as 7:1:1)", "High Phosphorus (P) fertilizer (such as 2:3:2)", "Rock phosphate alone", "Pure limestone powder", "Superphosphate alone", "Urea spray exclusively"]),

        ("A turf manager maintaining an established sports lawn or golf course fairway for deep green carpet foliage",
         "High Nitrogen (N) fertilizer (such as 7:1:1 or 8:1:1)",
         "Nitrogen accelerates blade foliage growth and maintains dark green chlorophyll coloration under frequent mowing.",
         ["High Phosphorus (P) fertilizer (such as 1:3:1)", "High Potassium (K) fertilizer (such as 1:1:5)", "Raw phosphate rock", "Potassium sulfate alone", "Pure calcium carbonate", "Iron filings alone"]),

        ("A commercial tomato grower whose plants are setting flowers and developing heavy fruit clusters",
         "High Potassium (K) fertilizer with moderate nitrogen (such as 3:1:5)",
         "Potassium supports osmotic pressure for fruit swelling, uniform ripening, and resistance against blossom blight.",
         ["High Nitrogen (N) fertilizer (such as 9:1:1)", "High Phosphorus (P) fertilizer (such as 1:4:1)", "Pure sulfur pellets", "Inert clay filler", "Ammonium sulfate alone", "Unrefined rock salt"])
    ]

    for crop_scenario, rec_fert, rec_exp, wr_recs in crop_recommendations:
        add_q("medium", "Fertilizer Selection",
              f"Which fertilizer formulation is most scientifically recommended for: **{crop_scenario}**, and what is the biochemical rationale?",
              f"{rec_fert}: {rec_exp}",
              [f"{w}: {rec_exp}" for w in wr_recs],
              "Applying", "Recommend fertilizer based on agronomic requirements",
              f"Recommendation: {rec_fert}. Rationale: {rec_exp}.")

    # Eutrophication step-by-step scientific sequence
    eutrophication_steps = [
        (1, "Excessive artificial fertilizers (nitrates and phosphates) applied to agricultural fields are washed away by rainfall runoff into nearby freshwater rivers, streams, and dams (leaching/runoff).",
         ["Algae grow on the surface of the water forming an algal bloom.",
          "Submerged aquatic plants die due to lack of penetrating sunlight.",
          "Decomposing bacteria consume all dissolved oxygen in the water.",
          "Fish and other aquatic animals suffocate and die.",
          "Sunlight is blocked from reaching the bottom of the water body.",
          "Water turns completely transparent and acidic."]),

        (2, "The sudden influx of high concentrations of dissolved nitrates and phosphates acts as abundant plant food, causing explosive proliferation of surface algae (an algal bloom).",
         ["Submerged aquatic plants flourish and produce excessive oxygen.",
          "Fish population multiplies ten-fold due to abundant algae food.",
          "Water temperature drops to 0 °C freezing all living organisms.",
          "Decomposer bacteria die immediately from fertilizer toxicity.",
          "Rainfall ceases permanently over the affected catchment area.",
          "Nitrogen gas bubbles out and creates acid rain."]),

        (3, "The thick green layer of surface algal bloom blankets the water surface, blocking sunlight from penetrating deeper into the water body.",
         ["Sunlight intensity under the water doubles due to reflection.",
          "Photosynthesis of deep-water plants increases dramatically.",
          "Water pressure drops to zero atm.",
          "All dissolved minerals precipitate as rock salt on the riverbed.",
          "The pH of the river drops to 0.",
          "Water clarity reaches 100% visibility."]),

        (4, "Deprived of solar radiation, submerged benthic aquatic plants are unable to perform photosynthesis and consequently die.",
         ["Submerged plants switch to eating dissolved nitrogen gas directly.",
          "Submerged plants grow up to the surface and absorb air.",
          "Fish begin photosynthesizing using ultraviolet radiation.",
          "Algae on the surface sink to form solid coal deposits.",
          "Water becomes enriched with dissolved oxygen.",
          "Decomposer bacteria evaporate into the atmosphere."]),

        (5, "The algae eventually exhaust available mineral nutrients and die, leaving vast quantities of dead organic biomass in the water.",
         ["Algae mutate into toxic carnivorous plants.",
          "Algae convert dead submerged plants into pure diamond.",
          "Fish consume all the dead algae and survive indefinitely.",
          "Water boils from the heat released by dead organic matter.",
          "All aquatic life migrates upstream into underground aquifers.",
          "The water body expands into an ocean."]),

        (6, "Populations of aerobic saprophytic (decomposer) bacteria multiply rapidly as they feed on the abundant dead plant and algal organic matter.",
         ["Decomposer bacteria produce massive quantities of dissolved oxygen.",
          "Anaerobic bacteria consume nitrogen gas from the air.",
          "Bacteria are killed by sunlight through the water surface.",
          "Decomposers turn all organic matter into petroleum oil.",
          "Viruses destroy all bacteria within seconds.",
          "Algae resurrect and resume photosynthesis."]),

        (7, "The enormous population of aerobic decomposer bacteria consumes vast quantities of dissolved oxygen (O2) for cellular respiration, causing biochemical oxygen demand (BOD) to spike and oxygen levels to crash (hypoxia/anoxia).",
         ["Bacteria release massive bubbles of pure oxygen gas.",
          "Dissolved oxygen levels rise to saturation (100% O2).",
          "Water becomes alkaline with a pH of 14.",
          "Water evaporates leaving a dry salt lake.",
          "Nitrate ions are converted into pure platinum.",
          "Fish breathe carbon dioxide instead of oxygen."]),

        (8, "Due to severe oxygen depletion (hypoxia/anoxia), fish, crustaceans, and other aerobic aquatic organisms suffocate and die, creating biological 'dead zones'.",
         ["Fish adapt immediately by developing atmospheric lungs.",
          "Fish thrive and multiply in the oxygen-depleted water.",
          "Water becomes crystal clear drinking water.",
          "Aquatic plants regrow rapidly from fish carcasses.",
          "The ecosystem permanently achieves perfect ecological balance.",
          "Freshwater converts into saline ocean water."])
    ]

    for step_num, step_desc, wr_steps in eutrophication_steps:
        add_q("medium", "Eutrophication Sequence",
              f"In the scientific progression of freshwater **eutrophication**, what is Step {step_num}?",
              step_desc, wr_steps, "Understanding", f"Explain eutrophication step {step_num}",
              f"Step {step_num} of eutrophication is: {step_desc}")

    # Fill medium to exactly 500 with diverse stoichiometry and NPK interpretation questions
    for n_p in range(1, 8):
        for p_p in range(1, 7):
            for k_p in range(1, 8):
                for pct in [14, 18, 20, 22, 24, 25, 26, 28, 30, 32, 34, 35, 36, 38, 40, 42]:
                    if counts["medium"] >= 500:
                        break
                    tot = n_p + p_p + k_p
                    max_nut = "Nitrogen" if (n_p >= p_p and n_p >= k_p) else "Phosphorus" if (p_p >= n_p and p_p >= k_p) else "Potassium"
                    min_nut = "Nitrogen" if (n_p <= p_p and n_p <= k_p) else "Phosphorus" if (p_p <= n_p and p_p <= k_p) else "Potassium"
                    q_text = f"An agronomist analyzes a commercial fertilizer labelled **{n_p} : {p_p} : {k_p} ({pct})**. Which primary macronutrient is present in the GREATEST proportion by mass, and what is its specific proportion of the active nutrients?"
                    corr_ans = f"{max_nut}, representing {max(n_p, p_p, k_p)}/{tot} ({round((max(n_p, p_p, k_p)/tot)*100, 1)}%) of total active nutrients."
                    wrs = [
                        f"{min_nut}, representing {min(n_p, p_p, k_p)}/{tot} ({round((min(n_p, p_p, k_p)/tot)*100, 1)}%) of active nutrients.",
                        "All three nutrients are present in exactly equal proportions (33.3% each).",
                        f"Inert filler, representing {100 - pct}% of active nutrients.",
                        f"{max_nut}, representing {pct}% of the total bag mass.",
                        f"{min_nut}, representing {100 - pct}% of active nutrients.",
                        f"Phosphorus, representing {tot}% of the bag mass.",
                        f"Calcium, representing {tot * 2}% of the nutrients."
                    ]
                    add_q("medium", "NPK Analysis", q_text, corr_ans, wrs, "Analyzing", "Determine dominant nutrient in NPK ratio",
                          f"In the ratio {n_p}:{p_p}:{k_p}, the highest number corresponds to {max_nut} ({max(n_p, p_p, k_p)} out of {tot} parts, or {round((max(n_p, p_p, k_p)/tot)*100, 1)}% of active nutrients).")

                    # Calculate percentage of Nitrogen in bag
                    if counts["medium"] < 500:
                        pct_n = round((n_p / tot) * pct, 2)
                        q_text_n = f"For a commercial fertilizer labelled **{n_p} : {p_p} : {k_p} ({pct})**, what is the exact percentage by mass of pure Nitrogen (N) in the total contents of the bag?"
                        corr_pct_n = f"{pct_n:.2f}%"
                        wrs_pct_n = [
                            f"{(n_p / tot) * 100:.2f}% (calculated percentage of active nutrients without multiplying by active content)",
                            f"{(p_p / tot) * pct:.2f}%",
                            f"{(k_p / tot) * pct:.2f}%",
                            f"{pct:.2f}% (total active percentage)",
                            f"{pct_n * 2:.2f}%",
                            f"{pct_n / 2:.2f}%",
                            f"{100 - pct:.2f}%"
                        ]
                        add_q("medium", "NPK Percentage", q_text_n, corr_pct_n, wrs_pct_n, "Applying", "Calculate percentage of nitrogen in fertilizer bag",
                              f"% N in bag = (Ratio part of N / Total parts) × Active % = ({n_p} / {tot}) × {pct}% = {pct_n:.2f}%.")

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Quantitative NPK Calculations, Bag Masses, Active Nutrient Mass, Filler Mass
    # =========================================================================

    # Rich grid of authentic NPK bags
    bag_masses = [10, 20, 25, 40, 50]
    ratios_active = [
        (3, 1, 5, 26),
        (4, 1, 2, 28),
        (2, 3, 2, 22),
        (2, 3, 4, 36),
        (5, 1, 2, 24),
        (3, 2, 1, 30),
        (7, 1, 1, 30),
        (8, 1, 1, 36),
        (1, 2, 3, 24),
        (2, 1, 2, 25),
        (1, 3, 1, 20),
        (3, 1, 1, 25),
        (2, 2, 1, 25),
        (1, 1, 1, 33),
        (4, 2, 1, 28),
        (3, 1, 2, 30),
        (2, 4, 1, 35),
        (1, 2, 1, 20),
        (5, 2, 1, 32),
        (6, 1, 3, 30)
    ]

    for bag_m in bag_masses:
        for n_p, p_p, k_p, pct in ratios_active:
            if counts["hard"] >= 200:
                break
            tot_parts = n_p + p_p + k_p
            # Exact calculations
            mass_active = bag_m * (pct / 100.0)
            mass_n = (n_p / tot_parts) * mass_active
            mass_p = (p_p / tot_parts) * mass_active
            mass_k = (k_p / tot_parts) * mass_active
            mass_filler = bag_m - mass_active

            # 1. Mass of Nitrogen
            q_n = f"A {bag_m} kg bag of commercial fertilizer is labelled **{n_p} : {p_p} : {k_p} ({pct})**. Calculate the exact mass of pure Nitrogen (N) present in this bag:"
            c_n = f"{mass_n:.2f} kg"
            w_n = [
                f"{(n_p / tot_parts) * bag_m:.2f} kg (omitted active percentage factor)",
                f"{mass_p:.2f} kg (calculated phosphorus mass instead)",
                f"{mass_k:.2f} kg (calculated potassium mass instead)",
                f"{mass_active:.2f} kg (total active fertilizer mass)",
                f"{mass_n * 2:.2f} kg",
                f"{mass_n / 2:.2f} kg",
                f"{bag_m * (pct / 100.0):.2f} kg"
            ]
            exp_n = f"Total ratio parts = {n_p} + {p_p} + {k_p} = {tot_parts}. Active mass in {bag_m} kg bag = {bag_m} × ({pct}/100) = {mass_active:.2f} kg. Mass of N = ({n_p}/{tot_parts}) × {mass_active:.2f} = {mass_n:.2f} kg."
            add_q("hard", "NPK Calculations", q_n, c_n, w_n, "Evaluating", "Calculate nitrogen mass in fertilizer bag", exp_n)

            # 2. Mass of Phosphorus
            if counts["hard"] < 200:
                q_p = f"From the same {bag_m} kg bag labelled **{n_p} : {p_p} : {k_p} ({pct})**, calculate the exact mass of pure Phosphorus (P) contained in the bag:"
                c_p = f"{mass_p:.2f} kg"
                w_p = [
                    f"{(p_p / tot_parts) * bag_m:.2f} kg (omitted active percentage)",
                    f"{mass_n:.2f} kg (calculated nitrogen mass instead)",
                    f"{mass_k:.2f} kg (calculated potassium mass instead)",
                    f"{mass_p * 2:.2f} kg",
                    f"{mass_p / 2:.2f} kg",
                    f"{mass_filler:.2f} kg (filler mass)",
                    f"{mass_p + 3.5:.2f} kg"
                ]
                exp_p = f"Total ratio parts = {tot_parts}. Active mass = {bag_m} × {pct/100} = {mass_active:.2f} kg. Mass of P = ({p_p}/{tot_parts}) × {mass_active:.2f} = {mass_p:.2f} kg."
                add_q("hard", "NPK Calculations", q_p, c_p, w_p, "Evaluating", "Calculate phosphorus mass in fertilizer bag", exp_p)

            # 3. Mass of Potassium
            if counts["hard"] < 200:
                q_k = f"For the {bag_m} kg fertilizer bag labelled **{n_p} : {p_p} : {k_p} ({pct})**, determine the exact mass of pure Potassium (K) available in the bag:"
                c_k = f"{mass_k:.2f} kg"
                w_k = [
                    f"{(k_p / tot_parts) * bag_m:.2f} kg (omitted active percentage)",
                    f"{mass_n:.2f} kg",
                    f"{mass_p:.2f} kg",
                    f"{mass_k * 1.5:.2f} kg",
                    f"{mass_k / 2:.2f} kg",
                    f"{mass_active:.2f} kg",
                    f"{mass_k + 4.0:.2f} kg"
                ]
                exp_k = f"Total ratio parts = {tot_parts}. Active mass = {bag_m} × {pct/100} = {mass_active:.2f} kg. Mass of K = ({k_p}/{tot_parts}) × {mass_active:.2f} = {mass_k:.2f} kg."
                add_q("hard", "NPK Calculations", q_k, c_k, w_k, "Evaluating", "Calculate potassium mass in fertilizer bag", exp_k)

            # 4. Mass of Inert Filler
            if counts["hard"] < 200:
                q_f = f"In a {bag_m} kg bag of fertilizer marked **{n_p} : {p_p} : {k_p} ({pct})**, what is the total mass of inert filler material (such as gypsum, sand, or limestone)?"
                c_f = f"{mass_filler:.2f} kg"
                w_f = [
                    f"{mass_active:.2f} kg (active nutrients mass)",
                    f"{bag_m:.2f} kg (total bag mass)",
                    f"{mass_n + mass_p:.2f} kg",
                    f"{mass_filler / 2:.2f} kg",
                    f"0.00 kg (bag contains 100% active fertilizer)",
                    f"{mass_filler + 10.0:.2f} kg",
                    f"{bag_m * (n_p / tot_parts):.2f} kg"
                ]
                exp_f = f"The active fertilizer content is {pct}%, so inert filler makes up 100% - {pct}% = {100 - pct}%. Mass of filler = {bag_m} × ({100 - pct}/100) = {mass_filler:.2f} kg."
                add_q("hard", "NPK Calculations", q_f, c_f, w_f, "Evaluating", "Calculate inert filler mass in fertilizer bag", exp_f)

    # Complete hard to exactly 200 with stoichiometric fertilizer synthesis calculations
    synth_masses = [
        # (Reactant mass, Reactant name, Product name, M_reactant, M_product, mol_ratio, reaction_desc)
        (140.0, "nitrogen gas (N2)", "ammonia (NH3)", 28.0, 17.0, 2.0, "N2 + 3H2 -> 2NH3"),
        (280.0, "nitrogen gas (N2)", "ammonia (NH3)", 28.0, 17.0, 2.0, "N2 + 3H2 -> 2NH3"),
        (68.0, "ammonia (NH3)", "nitric acid (HNO3)", 17.0, 63.0, 1.0, "NH3 -> NO -> NO2 -> HNO3 (1:1 theoretical yield)"),
        (170.0, "ammonia (NH3)", "nitric acid (HNO3)", 17.0, 63.0, 1.0, "Ostwald process 1:1 molar conversion"),
        (34.0, "ammonia (NH3)", "ammonium nitrate (NH4NO3)", 17.0, 80.0, 1.0, "NH3 + HNO3 -> NH4NO3"),
        (85.0, "ammonia (NH3)", "ammonium nitrate (NH4NO3)", 17.0, 80.0, 1.0, "NH3 + HNO3 -> NH4NO3"),
        (64.0, "sulfur (S)", "sulfuric acid (H2SO4)", 32.0, 98.0, 1.0, "S -> SO2 -> SO3 -> H2S2O7 -> 2H2SO4 (1:1 theoretical yield)"),
        (160.0, "sulfur (S)", "sulfuric acid (H2SO4)", 32.0, 98.0, 1.0, "Contact process 1:1 molar yield of S to H2SO4"),
        (34.0, "ammonia (NH3)", "ammonium sulfate ((NH4)2SO4)", 17.0, 132.0, 0.5, "2NH3 + H2SO4 -> (NH4)2SO4 (2:1 molar ratio)"),
        (68.0, "ammonia (NH3)", "ammonium sulfate ((NH4)2SO4)", 17.0, 132.0, 0.5, "2NH3 + H2SO4 -> (NH4)2SO4 (2:1 molar ratio)")
    ]

    for r_mass, r_name, p_name, m_r, m_p, ratio, eq_desc in synth_masses:
        if counts["hard"] >= 200:
            break
        n_r = r_mass / m_r
        n_p = n_r * ratio
        mass_p = n_p * m_p
        q_synth = f"An industrial fertilizer plant completely reacts {r_mass:.1f} kg of pure {r_name} in the synthesis of {p_name}. According to the reaction stoichiometry ({eq_desc}), calculate the maximum theoretical mass of {p_name} produced (molar masses: {r_name.split()[0]} = {m_r:.1f} g·mol⁻¹, {p_name.split()[0]} = {m_p:.1f} g·mol⁻¹):"
        c_synth = f"{mass_p:.1f} kg"
        w_synth = [
            f"{mass_p * 2:.1f} kg",
            f"{mass_p / 2:.1f} kg",
            f"{r_mass:.1f} kg (assumed 100% mass equivalence)",
            f"{mass_p * 0.75:.1f} kg",
            f"{mass_p + 25.0:.1f} kg",
            f"{(r_mass * m_r) / m_p:.1f} kg",
            f"{mass_p * 1.5:.1f} kg"
        ]
        exp_synth = f"Moles of {r_name} = {r_mass:.1f} × 10³ g / {m_r:.1f} g·mol⁻¹ = {n_r * 1000:.1f} mol. Moles of {p_name} = {n_p * 1000:.1f} mol. Theoretical mass = ({n_p * 1000:.1f} mol × {m_p:.1f} g·mol⁻¹) / 1000 = {mass_p:.1f} kg."
        add_q("hard", "Industrial Stoichiometry", q_synth, c_synth, w_synth, "Evaluating", f"Calculate mass of {p_name} produced", exp_synth)

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
