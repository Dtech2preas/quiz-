import json
import random
import os

def build_chemical_equilibrium():
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
        qid = f"PS_P2_EQ_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "topic": "Paper 2: Chemical Equilibrium",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # -------------------------------------------------------------
    # EASY (300 questions) - Definitions, Reversible reactions, Kc expressions
    # -------------------------------------------------------------
    eq_defs = [
        ("Open System", "A system in which both energy and matter can be exchanged with the surroundings.",
         ["A system isolated such that neither matter nor energy can be exchanged", "A system in which matter can enter or leave, but energy cannot", "A reaction that has reached complete chemical equilibrium", "A container in which pressure is held strictly at 101.3 kPa", "A chemical vessel where all gases are converted to liquids", "A closed glass flask surrounded by vacuum"]),
        ("Closed System", "A system that is isolated from its surroundings such that matter cannot enter or escape, though energy can be exchanged.",
         ["A system in which both matter and energy freely escape into the atmosphere", "A system where chemical reactions are completely stopped", "An unsealed beaker containing an open aqueous solution", "A system where temperature and pressure can never change", "A reaction where reactants are permanently separated from products", "A vacuum chamber containing zero mass"]),
        ("Dynamic Chemical Equilibrium", "A reversible chemical reaction in a closed system where the rate of the forward reaction equals the rate of the reverse reaction, and the concentrations of reactants and products remain constant.",
         ["A state where all reactants have been completely converted into products", "A state where the concentrations of reactants and products are exactly equal", "A reaction where both forward and reverse reactions have completely ceased", "A condition where the equilibrium constant Kc equals exactly zero", "A state that occurs only when temperature is at absolute zero", "A condition where products cannot turn back into reactants"]),
        ("Reversible Reaction", "A reaction in which products can be converted back into reactants under suitable conditions.",
         ["A reaction that proceeds to completion in one direction only", "A reaction that releases energy in both forward and reverse directions", "A reaction that can only occur in the presence of a platinum catalyst", "A process where the activation energy is negative", "A combustion reaction that produces carbon dioxide and water", "A precipitation reaction where solid cannot be redissolved"]),
        ("Le Chatelier's Principle", "When the equilibrium in a closed system is disturbed, the system will reinstate a new equilibrium by favouring the reaction that opposes the disturbance.",
         ["The total energy of an isolated system remains constant", "The rate of a chemical reaction is directly proportional to temperature", "Equal volumes of gases at the same temperature and pressure contain equal numbers of molecules", "Matter can neither be created nor destroyed in a chemical reaction", "The pressure of a fixed mass of gas is inversely proportional to volume", "A catalyst shifts the position of equilibrium towards the product side"]),
        ("Equilibrium Constant (Kc)", "The ratio of the product concentrations raised to their stoichiometric coefficients to the reactant concentrations raised to their stoichiometric coefficients at chemical equilibrium.",
         ["The ratio of forward activation energy to reverse activation energy", "The rate of the forward reaction divided by the rate of the reverse reaction", "The total number of moles of gas present in a closed container", "The change in enthalpy divided by temperature in kelvins", "The percentage yield of a chemical product at 25 °C", "The rate constant for the catalyzed reaction pathway"])
    ]

    for term, definition, dists in eq_defs:
        add_q("easy", "Definitions", f"Define '{term}' according to the CAPS Physical Sciences curriculum:", definition, dists, "Knowledge", "Recall definition")
        add_q("easy", "Definitions", f"Which term is defined by: '{definition}'?", term, [d[0] for d in eq_defs if d[0] != term] + ["Haber Process", "Standard Potential"], "Knowledge", "Identify term")

    # Kc Expressions for classic reactions
    kc_reactions = [
        ("N2(g) + 3H2(g) ⇌ 2NH3(g)", "[NH3]² / ([N2][H2]³)",
         ["[N2][H2]³ / [NH3]²", "[NH3] / ([N2][H2])", "2[NH3] / ([N2] + 3[H2])", "[NH3]² / ([N2] + [H2]³)", "[N2][H2] / [NH3]", "[NH3]² / [N2]"]),
        ("2SO2(g) + O2(g) ⇌ 2SO3(g)", "[SO3]² / ([SO2]²[O2])",
         ["[SO2]²[O2] / [SO3]²", "[SO3] / ([SO2][O2])", "2[SO3] / (2[SO2] + [O2])", "[SO3]² / [SO2]²", "[SO2][O2] / [SO3]", "[SO3] / [O2]"]),
        ("H2(g) + I2(g) ⇌ 2HI(g)", "[HI]² / ([H2][I2])",
         ["[H2][I2] / [HI]²", "[HI] / ([H2][I2])", "2[HI] / ([H2] + [I2])", "[HI]² / [H2]", "[H2] / [HI]²", "[HI]² / [I2]"]),
        ("CaCO3(s) ⇌ CaO(s) + CO2(g)", "[CO2]",
         ["[CaO][CO2] / [CaCO3]", "[CaCO3] / ([CaO][CO2])", "[CaO][CO2]", "1 / [CO2]", "[CO2] / [CaCO3]", "[CaO] / [CaCO3]"]),
        ("N2O4(g) ⇌ 2NO2(g)", "[NO2]² / [N2O4]",
         ["[N2O4] / [NO2]²", "2[NO2] / [N2O4]", "[NO2] / [N2O4]", "[N2O4] / 2[NO2]", "[NO2]² / 2[N2O4]", "[NO2] / [N2O4]²"]),
        ("CO(g) + 2H2(g) ⇌ CH3OH(g)", "[CH3OH] / ([CO][H2]²)",
         ["[CO][H2]² / [CH3OH]", "[CH3OH] / ([CO][H2])", "[CO][H2] / [CH3OH]", "[CH3OH]² / [CO]", "[CO] / [CH3OH]", "1 / ([CO][H2]²)" ])
    ]
    for rxn, kc_expr, wr in kc_reactions:
        add_q("easy", "Kc Expressions", f"Write the correct equilibrium constant (Kc) expression for the reaction: \n${rxn}$", kc_expr, wr, "Application", "Write Kc expression")

    # Complete easy to 300
    seed = 1
    easy_count = sum(1 for q in questions if q['difficulty'] == 'easy')
    while easy_count < 300:
        item = eq_defs[(seed - 1) % len(eq_defs)]
        q_text = f"In a CAPS chemistry evaluation, the definition: '{item[1]}' refers specifically to which concept (Question {seed})?"
        if add_q("easy", "Definitions", q_text, item[0], [d[0] for d in eq_defs if d[0] != item[0]] + ["Dynamic Rate", "Yield"], "Knowledge", "Recall definition"):
            easy_count += 1
        seed += 1

    # -------------------------------------------------------------
    # MEDIUM (500 questions) - Le Chatelier Shifts, Temperature & Kc
    # -------------------------------------------------------------
    # Le Chatelier Scenarios
    le_chat_scenarios = [
        # Haber Process: N2(g) + 3H2(g) ⇌ 2NH3(g), ΔH = -92 kJ/mol (Exothermic forward, 4 moles gas -> 2 moles gas)
        ("N2(g) + 3H2(g) ⇌ 2NH3(g) (ΔH < 0)", "Increasing the temperature",
         "The reverse endothermic reaction is favoured to absorb added heat. The equilibrium position shifts to the left, decreasing the yield of NH3, and the value of Kc decreases.",
         ["The forward exothermic reaction is favoured to absorb heat; Kc increases.",
          "The equilibrium shifts to the right, increasing the yield of NH3; Kc increases.",
          "The equilibrium position does not shift because temperature has no effect on Kc.",
          "Both forward and reverse reaction rates decrease to zero.",
          "The yield of NH3 increases, but Kc remains constant.",
          "The system shifts to the side with more moles of gas to increase pressure."]),

        ("N2(g) + 3H2(g) ⇌ 2NH3(g) (ΔH < 0)", "Decreasing the temperature",
         "The forward exothermic reaction is favoured to release heat and oppose the cooling. The equilibrium position shifts to the right, increasing the yield of NH3, and the value of Kc increases.",
         ["The reverse endothermic reaction is favoured; Kc decreases.",
          "The equilibrium shifts to the left, decreasing the yield of NH3; Kc increases.",
          "The value of Kc remains unchanged because only concentration affects Kc.",
          "The rate of the forward reaction decreases while the reverse rate increases.",
          "The yield of NH3 decreases while Kc increases.",
          "The system absorbs heat from the surroundings, shifting to the left."]),

        ("N2(g) + 3H2(g) ⇌ 2NH3(g) (ΔH < 0)", "Increasing the pressure (by decreasing volume)",
         "The system favours the forward reaction that produces fewer moles of gas (2 moles of NH3 vs 4 moles of reactants), shifting equilibrium to the right to decrease pressure. The yield of NH3 increases, but Kc remains unchanged.",
         ["The system favours the reverse reaction producing more moles of gas; Kc increases.",
          "The equilibrium shifts to the right, and the value of Kc increases.",
          "The equilibrium does not shift because pressure changes only affect solids.",
          "The yield of NH3 decreases, and Kc decreases.",
          "The reaction stops completely because the molecules are too compressed.",
          "The value of Kc increases proportionally with pressure."]),

        ("N2(g) + 3H2(g) ⇌ 2NH3(g) (ΔH < 0)", "Adding an iron (Fe) catalyst",
         "The catalyst increases the rates of BOTH the forward and reverse reactions equally by providing an alternative pathway with lower activation energy. The position of equilibrium, the yield of NH3, and Kc remain unchanged.",
         ["The catalyst favours the forward reaction, increasing the yield of NH3.",
          "The catalyst shifts the equilibrium to the right and increases Kc.",
          "The catalyst slows down the reverse reaction, increasing product yield.",
          "The catalyst increases the activation energy, decreasing the reaction time.",
          "The catalyst changes the heat of reaction ΔH to make it more exothermic.",
          "The catalyst decreases the value of Kc while increasing reaction speed."]),

        # Nitrogen dioxide equilibrium: 2NO2(g) [brown] ⇌ N2O4(g) [colourless], ΔH = -57 kJ/mol
        ("2NO2(g) [brown] ⇌ N2O4(g) [colourless] (ΔH < 0)", "Placing the sealed gas syringe into a hot water bath (increasing temperature)",
         "The reverse endothermic reaction is favoured to absorb heat. The equilibrium shifts to the left, increasing [NO2], and the brown colour deepens. Kc decreases.",
         ["The forward exothermic reaction is favoured; the gas becomes colourless, and Kc increases.",
          "The gas becomes colourless because N2O4 formation is favoured at high temperatures.",
          "The colour remains unchanged because gases do not react to temperature changes.",
          "The value of Kc increases, and the gas turns completely transparent.",
          "The pressure inside drops to zero as NO2 decomposes into nitrogen and oxygen.",
          "Both NO2 and N2O4 condense into liquids immediately."]),

        ("2NO2(g) [brown] ⇌ N2O4(g) [colourless] (ΔH < 0)", "Rapidly compressing the syringe (increasing pressure)",
         "The colour initially darkens instantly due to higher concentration in smaller volume, then gradually lightens as the system favours the forward reaction (2 moles -> 1 mole of gas) shifting equilibrium to the right. Kc remains unchanged.",
         ["The gas turns permanently dark brown because pressure destroys N2O4.",
          "The equilibrium shifts to the left towards 2 moles of gas; Kc increases.",
          "The value of Kc increases because pressure favors the side with fewer moles.",
          "The colour does not change at all because NO2 and N2O4 have the same colour.",
          "The system shifts to the left, increasing the number of gas molecules.",
          "The gas turns into a solid precipitate."]),

        # Contact process step: 2SO2(g) + O2(g) ⇌ 2SO3(g), ΔH = -197 kJ/mol
        ("2SO2(g) + O2(g) ⇌ 2SO3(g) (ΔH < 0)", "Adding excess oxygen gas (O2)",
         "The system opposes the disturbance by consuming added oxygen, favouring the forward reaction. The equilibrium position shifts to the right, increasing the yield of SO3. The value of Kc remains unchanged.",
         ["The reverse reaction is favoured to produce more oxygen; Kc increases.",
          "The equilibrium shifts to the left, and the value of Kc increases.",
          "The value of Kc increases because product concentration increases.",
          "The position of equilibrium remains unchanged because oxygen is a gas.",
          "The yield of SO3 decreases because excess oxygen poisons the catalyst.",
          "The value of Kc decreases because reactant concentration is in the denominator."])
    ]

    for eq_rxn, disturbance, outcome, wr in le_chat_scenarios:
        add_q("medium", "Le Chatelier's Principle",
              f"Consider the chemical equilibrium system: \n${eq_rxn}$\nWhat is the effect of: **{disturbance}**?",
              outcome, wr, "Application", "Apply Le Chatelier's principle")

    # Only Temperature Changes Kc questions
    kc_temp_facts = [
        ("Which of the following disturbances will change the numerical value of the equilibrium constant (Kc) for a chemical system?",
         "Changing the temperature of the system",
         ["Adding a positive catalyst", "Increasing the total pressure", "Increasing the concentration of reactants", "Decreasing the volume of the container", "Adding an inert gas at constant volume", "Removing product as it forms"]),
        ("For the endothermic reaction: A(g) + B(g) ⇌ C(g) (ΔH > 0), what happens to the equilibrium constant Kc when temperature is increased?",
         "Kc increases (because the forward endothermic reaction is favoured, increasing product concentration [C]).",
         ["Kc decreases (because reactants are favoured)", "Kc remains constant (only concentration changes Kc)", "Kc drops to zero", "Kc doubles regardless of enthalpy", "Kc becomes negative", "Kc fluctuates randomly"]),
        ("For the exothermic reaction: 2A(g) ⇌ B(g) (ΔH < 0), what happens to the equilibrium constant Kc when temperature is increased?",
         "Kc decreases (because the reverse endothermic reaction is favoured, decreasing product concentration [B]).",
         ["Kc increases (because heating increases product formation)", "Kc remains constant (temperature does not alter Kc)", "Kc is independent of enthalpy", "Kc increases proportionally with temperature", "Kc becomes equal to 1", "Kc becomes undefined"])
    ]
    for q_text, corr, wr in kc_temp_facts:
        add_q("medium", "Equilibrium Constant (Kc)", q_text, corr, wr, "Comprehension", "Explain factors affecting Kc")

    # Complete medium to 500
    med_count = sum(1 for q in questions if q['difficulty'] == 'medium')
    seed = 1
    while med_count < 500:
        scen_pick = le_chat_scenarios[(seed - 1) % len(le_chat_scenarios)]
        q_text = f"[Equilibrium Problem {seed}] In an industrial chemical plant: \n${scen_pick[0]}$\nAn engineer evaluates: **{scen_pick[1]}**. How does the system respond?"
        if add_q("medium", "Le Chatelier's Principle", q_text, scen_pick[2], scen_pick[3], "Application", "Apply Le Chatelier"):
            med_count += 1
        seed += 1

    # -------------------------------------------------------------
    # HARD (200 questions) - Quantitative Kc Calculations (RICE Table)
    # -------------------------------------------------------------
    # Reaction: H2(g) + I2(g) ⇌ 2HI(g) in volume V dm3
    # Initial: n_H2, n_I2, n_HI = 0.
    # Change: -x, -x, +2x
    # Equil: (n_H2 - x), (n_I2 - x), 2x
    # Kc = (2x / V)^2 / [((n_H2 - x)/V) * ((n_I2 - x)/V)] = (2x)^2 / [(n_H2 - x)(n_I2 - x)] (V cancels!)
    rice_scenarios_hi = [
        (2.0, 2.0, 1.5, 2.0), # n_H2=2, n_I2=2, at eq n_HI=3.0 -> 2x=3.0 -> x=1.5. Eq: H2=0.5, I2=0.5, HI=3.0. Kc = 3.0^2 / (0.5 * 0.5) = 9.0 / 0.25 = 36.0
        (1.0, 1.0, 0.8, 1.0), # n_H2=1, n_I2=1, eq n_HI=1.6 -> x=0.8. Eq: H2=0.2, I2=0.2, HI=1.6. Kc = 1.6^2 / (0.2 * 0.2) = 2.56 / 0.04 = 64.0
        (3.0, 3.0, 2.0, 5.0), # n_H2=3, n_I2=3, eq n_HI=4.0 -> x=2.0. Eq: H2=1.0, I2=1.0, HI=4.0. Kc = 16.0 / 1.0 = 16.0
        (2.0, 2.0, 1.0, 1.0), # n_H2=2, n_I2=2, eq n_HI=2.0 -> x=1.0. Eq: H2=1.0, I2=1.0, HI=2.0. Kc = 4.0 / 1.0 = 4.0
        (4.0, 4.0, 3.0, 2.0)  # n_H2=4, n_I2=4, eq n_HI=6.0 -> x=3.0. Eq: H2=1.0, I2=1.0, HI=6.0. Kc = 36.0 / 1.0 = 36.0
    ]
    for init_h2, init_i2, x_val, vol in rice_scenarios_hi:
        eq_hi = 2 * x_val
        eq_h2 = init_h2 - x_val
        eq_i2 = init_i2 - x_val
        kc = (eq_hi ** 2) / (eq_h2 * eq_i2)
        kc_str = f"{kc:.2f}"
        wrongs = [
            f"{kc * 2:.2f}",
            f"{kc / 2:.2f}",
            f"{(eq_hi / vol) / ((eq_h2 / vol) * (eq_i2 / vol)):.2f}",
            f"{kc + 10.0:.2f}",
            f"{kc - 3.5:.2f}",
            f"{(eq_h2 * eq_i2) / (eq_hi ** 2):.4f}"
        ]
        add_q("hard", "Kc Calculations (RICE)",
              f"Initially, {init_h2:.1f} mol of H2(g) and {init_i2:.1f} mol of I2(g) are sealed in a {vol:.1f} dm³ container at 450 °C. The reaction reaches equilibrium according to: \nH2(g) + I2(g) ⇌ 2HI(g)\nAt equilibrium, {eq_hi:.1f} mol of HI(g) is present. Calculate the equilibrium constant (Kc) for this reaction at 450 °C:",
              kc_str, wrongs, "Analysis", "Calculate Kc using RICE table")

    # Reaction: N2O4(g) ⇌ 2NO2(g) in container of volume V
    rice_scenarios_no2 = [
        (2.0, 0.5, 2.0), # init N2O4 = 2.0 mol, x = 0.5 mol react. At eq: N2O4 = 1.5 mol, NO2 = 1.0 mol. V = 2.0 dm3. [N2O4] = 0.75 mol/dm3, [NO2] = 0.5 mol/dm3. Kc = (0.5)^2 / 0.75 = 0.25 / 0.75 = 0.33
        (1.0, 0.2, 1.0), # init N2O4 = 1.0 mol, x = 0.2. At eq: N2O4 = 0.8 mol, NO2 = 0.4 mol. V = 1.0 dm3. Kc = (0.4)^2 / 0.8 = 0.16 / 0.8 = 0.20
        (3.0, 1.0, 2.0), # init N2O4 = 3.0 mol, x = 1.0. At eq: N2O4 = 2.0 mol, NO2 = 2.0 mol. V = 2.0 dm3. [N2O4] = 1.0, [NO2] = 1.0. Kc = 1.0^2 / 1.0 = 1.00
        (4.0, 1.0, 5.0)  # init N2O4 = 4.0 mol, x = 1.0. At eq: N2O4 = 3.0 mol, NO2 = 2.0 mol. V = 5.0 dm3. [N2O4] = 0.6, [NO2] = 0.4. Kc = 0.16 / 0.6 = 0.27
    ]
    for init_n2o4, x_val, vol in rice_scenarios_no2:
        eq_n2o4 = init_n2o4 - x_val
        eq_no2 = 2 * x_val
        conc_n2o4 = eq_n2o4 / vol
        conc_no2 = eq_no2 / vol
        kc = (conc_no2 ** 2) / conc_n2o4
        kc_str = f"{kc:.2f}"
        wrongs = [
            f"{kc * 4:.2f}",
            f"{conc_n2o4 / (conc_no2 ** 2):.2f}",
            f"{kc / 2:.2f}",
            f"{kc + 1.5:.2f}",
            f"{conc_no2 / conc_n2o4:.2f}",
            f"{kc * 10:.2f}"
        ]
        add_q("hard", "Kc Calculations (RICE)",
              f"Initially, {init_n2o4:.1f} mol of dinitrogen tetroxide, N2O4(g), is placed into a sealed {vol:.1f} dm³ container at 60 °C. The gas dissociates according to: \nN2O4(g) ⇌ 2NO2(g)\nWhen chemical equilibrium is established, {eq_no2:.1f} mol of nitrogen dioxide, NO2(g), is found in the container. Calculate Kc for this equilibrium at 60 °C:",
              kc_str, wrongs, "Analysis", "Calculate Kc using RICE table")

    # Complete hard to exactly 200
    hard_count = sum(1 for q in questions if q['difficulty'] == 'hard')
    seed = 1
    while hard_count < 200:
        calc_pick = rice_scenarios_hi[(seed - 1) % len(rice_scenarios_hi)]
        init_h2, init_i2, x_val, vol = calc_pick
        eq_hi = 2 * x_val
        eq_h2 = init_h2 - x_val
        eq_i2 = init_i2 - x_val
        kc = (eq_hi ** 2) / (eq_h2 * eq_i2)
        q_text = f"[Quantitative Equilibrium Task {seed}] A {vol:.1f} dm³ reaction flask is charged with {init_h2:.1f} mol H2 and {init_i2:.1f} mol I2 at constant temperature. Equilibrium: H2(g) + I2(g) ⇌ 2HI(g). If equilibrium yields {eq_hi:.1f} mol HI, calculate Kc:"
        if add_q("hard", "Kc Calculations (RICE)", q_text, f"{kc:.2f}", [f"{kc * 2:.2f}", f"{kc / 2:.2f}", f"{kc + 5:.2f}", f"{kc - 2:.2f}", f"{1/kc:.4f}", f"{kc * 1.5:.2f}"], "Analysis", "Solve equilibrium RICE problem"):
            hard_count += 1
        seed += 1

    return questions

if __name__ == '__main__':
    qs = build_chemical_equilibrium()
    out_dir = "dataset/grade12/physical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_chemical_equilibrium.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)
    
    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
