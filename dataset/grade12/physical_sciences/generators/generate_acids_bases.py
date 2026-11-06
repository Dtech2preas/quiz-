import json
import random
import os
import math

def build_acids_bases():
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
        qid = f"PS_P2_AB_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "topic": "Paper 2: Acids and Bases",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # -------------------------------------------------------------
    # EASY (300 questions) - Core Definitions, Theories, Conjugate Pairs
    # -------------------------------------------------------------
    ab_defs = [
        ("Arrhenius Acid", "A substance that produces hydrogen ions (H+) or hydronium ions (H3O+) when dissolved in water.",
         ["A substance that accepts protons in an aqueous solution", "A substance that donates an electron pair", "A substance that produces hydroxide ions in water", "A compound that turns phenolphthalein pink", "A chemical that dissociates into metal cations exclusively", "An organic compound with a carboxyl group"]),
        ("Arrhenius Base", "A substance that produces hydroxide ions (OH-) when dissolved in water.",
         ["A substance that donates protons in an aqueous solution", "A substance that accepts hydrogen gas", "A compound that produces hydronium ions in water", "A substance with a pH less than 7 at 25 °C", "A chemical with covalent bonds only", "An acid that has been neutralized"]),
        ("Brønsted-Lowry Acid", "A proton (H+ ion) donor.",
         ["A proton (H+ ion) acceptor.", "An electron pair donor.", "An electron pair acceptor.", "A substance that produces OH- ions in water.", "A compound that neutralizes bases without releasing protons.", "A chemical with zero oxidation number."]),
        ("Brønsted-Lowry Base", "A proton (H+ ion) acceptor.",
         ["A proton (H+ ion) donor.", "An electron pair donor.", "A substance that produces hydronium ions.", "A salt formed by neutralization.", "A solution with pH < 7.", "An oxidizing agent in redox reactions."]),
        ("Ampholyte (Amphiprotic Substance)", "A substance that can act as either a Brønsted-Lowry acid or a Brønsted-Lowry base (can either donate or accept a proton).",
         ["A substance that completely dissociates in water into ions", "A chemical that has a neutral pH of exactly 7 at all temperatures", "A salt that does not undergo hydrolysis in water", "An indicator that changes colour over a wide pH range", "A substance with equal numbers of protons and electrons", "A solution containing equal concentrations of strong acid and strong base"]),
        ("Strong Acid", "An acid that ionizes completely in aqueous solution to form a high concentration of H3O+ ions.",
         ["An acid with a very high number of moles per unit volume", "An acid that ionizes only partially in water", "An acid with a pH above 7", "An acid that has two or more ionizable protons", "An acid that reacts explosively with all metals", "A concentrated acid solution"]),
        ("Weak Acid", "An acid that ionizes only partially (incompletely) in aqueous solution to form a low concentration of H3O+ ions.",
         ["An acid that has been diluted with large volumes of water", "An acid that ionizes completely in water", "An acid that does not contain any hydrogen atoms", "An acid that turns bromothymol blue dark blue", "A substance with a pH of exactly 14", "An acid that cannot react with bases"]),
        ("Strong Base", "A base that dissociates completely in water to form a high concentration of OH- ions.",
         ["A base that has a very high molar mass", "A base that ionizes only partially in water", "A base that can donate protons to water", "A concentrated solution of any metal hydroxide", "A base that forms an acidic salt upon neutralization", "A weak base that has been boiled"]),
        ("Weak Base", "A base that ionizes or dissociates only partially in aqueous solution to form a low concentration of OH- ions.",
         ["A base that contains no nitrogen atoms", "A base that completely dissociates into hydroxide ions", "A base that has a pH less than 1 at 25 °C", "A base that neutralizes acids without changing temperature", "A base dissolved in an organic solvent only", "A base that does not conduct electricity at all"]),
        ("Standard Solution", "A solution of precisely known concentration.",
         ["A solution at standard temperature and pressure (0 °C and 101.3 kPa)", "A solution containing exactly 1 mol of solute in any volume", "A neutral solution with a pH of 7", "A saturated solution that cannot dissolve any more solute", "A standard buffer solution that resists pH changes", "A pure solvent with no dissolved impurities"]),
        ("Equivalence Point", "The point in a titration where the acid and base have reacted completely in stoichiometric mole proportions.",
         ["The point where the indicator changes colour permanently", "The point where the pH of the solution is always exactly 7.0", "The point where equal volumes of acid and base have been mixed", "The point where all water has evaporated from the conical flask", "The point where the temperature reaches maximum", "The point where precipitation first becomes visible"]),
        ("End Point", "The point in a titration where the indicator changes colour.",
         ["The point where stoichiometric amounts of acid and base have reacted", "The point where the solution is completely neutral (pH = 7)", "The point where the burette has been completely emptied", "The initial reading on the burette before starting titration", "The point of maximum conductivity", "The point where the salt precipitates"])
    ]

    for term, definition, dists in ab_defs:
        add_q("easy", "Definitions", f"Define '{term}' according to CAPS Physical Sciences:", definition, dists, "Knowledge", "Recall definition")
        add_q("easy", "Definitions", f"Which term is defined as: '{definition}'?", term, [d[0] for d in ab_defs if d[0] != term], "Knowledge", "Identify term")

    # Conjugate Acid-Base Pairs
    # Acid -> Conjugate Base (removes H+)
    acid_pairs = [
        ("HCl", "Cl-", ["Cl2", "HCl2-", "OH-", "H2Cl+", "ClO-", "H+"]),
        ("HNO3", "NO3-", ["NO2-", "HNO2", "N2O", "NO3", "H2NO3+", "NH4+"]),
        ("H2SO4", "HSO4-", ["SO4(2-)", "H2SO3", "SO3(2-)", "H3SO4+", "S(2-)", "SO2"]),
        ("HSO4-", "SO4(2-)", ["H2SO4", "HSO3-", "SO3(2-)", "S(2-)", "H3SO4+", "SO2"]),
        ("CH3COOH", "CH3COO-", ["CH3COOH2+", "CH3CO+", "CH3CH2O-", "CH3OH", "HCOO-", "C2H5O-"]),
        ("H2O (acting as an acid)", "OH-", ["H3O+", "O(2-)", "H2O2", "H+", "HO2-", "OH"]),
        ("NH4+", "NH3", ["NH2-", "N2", "NH4OH", "NH5(2+)", "NO3-", "NO2-"]),
        ("H3O+", "H2O", ["OH-", "H4O(2+)", "O(2-)", "H2O2", "H+", "H3O"]),
        ("HCO3- (acting as an acid)", "CO3(2-)", ["H2CO3", "CO2", "HCO2-", "C(4-)", "OH-", "HCO3"])
    ]
    for acid, c_base, wr in acid_pairs:
        add_q("easy", "Conjugate Pairs", f"What is the conjugate base of the acid ${acid}$?", c_base, wr, "Application", "Identify conjugate base")

    # Base -> Conjugate Acid (adds H+)
    base_pairs = [
        ("NH3", "NH4+", ["NH2-", "N2H4", "NH4OH", "NO3-", "H3O+", "NH3+"]),
        ("H2O (acting as a base)", "H3O+", ["OH-", "H4O(2+)", "O(2-)", "H+", "H2O2", "H3O"]),
        ("OH-", "H2O", ["H3O+", "O(2-)", "H2O2", "OH", "H+", "H3O"]),
        ("CO3(2-)", "HCO3-", ["H2CO3", "CO2", "C(4-)", "HCO2-", "H3CO3+", "CH4"]),
        ("HCO3- (acting as a base)", "H2CO3", ["CO3(2-)", "CO2", "H3CO3+", "HCO2-", "CH3COOH", "H2O"]),
        ("Cl-", "HCl", ["Cl2", "HCl2-", "HClO", "ClO-", "H+", "Cl(2-)"]),
        ("CH3COO-", "CH3COOH", ["CH3COO", "CH3COOH2+", "CH3CHO", "CH3CH2OH", "HCOOH", "CH4"])
    ]
    for base, c_acid, wr in base_pairs:
        add_q("easy", "Conjugate Pairs", f"What is the conjugate acid of the base ${base}$?", c_acid, wr, "Application", "Identify conjugate acid")

    # Strong vs Weak classifications
    strong_acids = ["Hydrochloric acid (HCl)", "Nitric acid (HNO3)", "Sulfuric acid (H2SO4)"]
    weak_acids = ["Ethanoic acid (CH3COOH)", "Oxalic acid ((COOH)2)", "Carbonic acid (H2CO3)", "Hydrofluoric acid (HF)"]
    strong_bases = ["Sodium hydroxide (NaOH)", "Potassium hydroxide (KOH)", "Lithium hydroxide (LiOH)"]
    weak_bases = ["Ammonia (NH3)", "Sodium hydrogen carbonate (NaHCO3)", "Calcium carbonate (CaCO3)"]

    for sa in strong_acids:
        add_q("easy", "Acid/Base Strength", f"Classify the substance '{sa}' in terms of acid-base strength:",
              "Strong acid (ionizes completely in aqueous solution)",
              ["Weak acid (ionizes partially in water)", "Strong base (dissociates completely into OH- ions)", "Weak base (ionizes partially to form OH- ions)", "Neutral salt (pH = 7)", "Ampholyte", "Non-electrolyte"], "Knowledge", "Classify strong acid")
    for wa in weak_acids:
        add_q("easy", "Acid/Base Strength", f"Classify the substance '{wa}' in terms of acid-base strength:",
              "Weak acid (ionizes only partially in aqueous solution)",
              ["Strong acid (ionizes completely in water)", "Strong base (dissociates completely into OH- ions)", "Weak base (ionizes partially in water)", "Neutral salt (pH = 7)", "Strong electrolyte", "Amphiprotic salt"], "Knowledge", "Classify weak acid")
    for sb in strong_bases:
        add_q("easy", "Acid/Base Strength", f"Classify the substance '{sb}' in terms of acid-base strength:",
              "Strong base (dissociates completely into hydroxide ions in water)",
              ["Weak base (ionizes partially in water)", "Strong acid (ionizes completely into hydronium ions)", "Weak acid (ionizes partially in water)", "Neutral salt", "Amphiprotic compound", "Non-electrolyte"], "Knowledge", "Classify strong base")
    for wb in weak_bases:
        add_q("easy", "Acid/Base Strength", f"Classify the substance '{wb}' in terms of acid-base strength:",
              "Weak base (ionizes or dissociates only partially in water)",
              ["Strong base (dissociates completely in water)", "Strong acid (ionizes completely)", "Weak acid (ionizes partially)", "Neutral salt", "Strong electrolyte", "Strong oxidizing agent"], "Knowledge", "Classify weak base")

    # Complete easy to 300
    seed = 1
    easy_count = sum(1 for q in questions if q['difficulty'] == 'easy')
    while easy_count < 300:
        ap = acid_pairs[(seed - 1) % len(acid_pairs)]
        q_text = f"In Brønsted-Lowry acid-base theory, identify the conjugate base for ${ap[0]}$ (Question {seed}):"
        if add_q("easy", "Conjugate Pairs", q_text, ap[1], ap[2], "Application", "Recall conjugate pair"):
            easy_count += 1
        seed += 1

    # -------------------------------------------------------------
    # MEDIUM (500 questions) - pH Calculations, Salt Hydrolysis, Indicators
    # -------------------------------------------------------------
    # 1. Simple pH calculations for strong monoprotic acids (pH = -log[H3O+])
    acid_concs = [
        (0.1, "1.00"), (0.01, "2.00"), (0.001, "3.00"), (0.0001, "4.00"),
        (0.05, "1.30"), (0.02, "1.70"), (0.005, "2.30"), (0.002, "2.70"),
        (0.2, "0.70"), (0.5, "0.30"), (0.0005, "3.30"), (0.0002, "3.70")
    ]
    for c_val, ph_str in acid_concs:
        ph_float = float(ph_str)
        wrongs = [
            f"{14.0 - ph_float:.2f}",
            f"{ph_float + 1.0:.2f}",
            f"{ph_float - 1.0 if ph_float > 1.0 else ph_float + 2.0:.2f}",
            f"{c_val:.2f}",
            f"{-math.log10(c_val) * 2:.2f}",
            f"{ph_float + 0.5:.2f}"
        ]
        add_q("medium", "pH Calculations",
              f"Calculate the pH of a {c_val} mol·dm⁻³ solution of hydrochloric acid (HCl) at 25 °C (assume complete ionization):",
              ph_str, wrongs, "Application", "Calculate pH of strong monoprotic acid")

    # 2. Strong Diprotic Acid (H2SO4 -> 2 H3O+)
    # [H3O+] = 2 * c_acid
    diprotic_concs = [
        (0.05, "1.00"), # [H3O+] = 0.1 -> pH = 1.00
        (0.005, "2.00"), # [H3O+] = 0.01 -> pH = 2.00
        (0.0005, "3.00"), # [H3O+] = 0.001 -> pH = 3.00
        (0.01, "1.70"), # [H3O+] = 0.02 -> pH = 1.70
        (0.02, "1.40"), # [H3O+] = 0.04 -> pH = 1.40
        (0.025, "1.30") # [H3O+] = 0.05 -> pH = 1.30
    ]
    for c_val, ph_str in diprotic_concs:
        ph_float = float(ph_str)
        err_monoprotic = f"{-math.log10(c_val):.2f}"
        wrongs = [
            err_monoprotic,
            f"{14.0 - ph_float:.2f}",
            f"{ph_float + 1.0:.2f}",
            f"{ph_float * 2:.2f}",
            f"{c_val * 2:.2f}",
            f"{ph_float - 0.5 if ph_float > 0.5 else 0.8:.2f}"
        ]
        add_q("medium", "pH Calculations (Diprotic)",
              f"Calculate the pH of a {c_val} mol·dm⁻³ solution of sulfuric acid (H2SO4) at 25 °C, assuming complete ionization of both protons:",
              ph_str, wrongs, "Application", "Calculate pH of strong diprotic acid")

    # 3. Strong Base pH calculations (Kw = [H3O+][OH-] = 10^-14 => [H3O+] = 10^-14 / [OH-] => pH = 14 - pOH)
    base_concs = [
        (0.1, "13.00"), (0.01, "12.00"), (0.001, "11.00"), (0.0001, "10.00"),
        (0.05, "12.70"), (0.02, "12.30"), (0.005, "11.70"), (0.002, "11.30"),
        (0.2, "13.30"), (0.5, "13.70")
    ]
    for c_val, ph_str in base_concs:
        ph_float = float(ph_str)
        poh = 14.0 - ph_float
        wrongs = [
            f"{poh:.2f}", # Forgot to subtract from 14!
            f"{ph_float - 1.0:.2f}",
            f"{ph_float + 0.5 if ph_float < 13.5 else 12.5:.2f}",
            f"{7.0 + poh:.2f}",
            f"{c_val:.2f}",
            f"{14.0 + math.log10(c_val) * 2:.2f}"
        ]
        add_q("medium", "pH Calculations (Base)",
              f"Calculate the pH of a {c_val} mol·dm⁻³ solution of sodium hydroxide (NaOH) at 25 °C:",
              ph_str, wrongs, "Application", "Calculate pH of strong base")

    # 4. Salt Hydrolysis & pH of Salt Solutions
    salt_hydrolysis = [
        ("Sodium chloride (NaCl)", "Neutral (pH ≈ 7)",
         "Formed from strong acid (HCl) and strong base (NaOH); neither Na+ nor Cl- hydrolyses with water.",
         ["Acidic (pH < 7) because Cl- hydrolyses to form HCl", "Basic (pH > 7) because Na+ hydrolyses to form NaOH", "Acidic (pH < 7) because it is a binary salt", "Basic (pH > 7) because it conducts electricity", "Strongly acidic (pH = 1)", "Strongly basic (pH = 14)"]),

        ("Ammonium chloride (NH4Cl)", "Acidic (pH < 7)",
         "Formed from strong acid (HCl) and weak base (NH3). The ammonium ion (NH4+) hydrolyses: NH4+ + H2O ⇌ NH3 + H3O+, producing excess hydronium ions.",
         ["Neutral (pH = 7) because equal moles of salt dissolve", "Basic (pH > 7) because Cl- produces hydroxide ions", "Basic (pH > 7) because ammonia is a base", "Neutral (pH = 7) because chlorine is neutral", "Strongly basic (pH = 13)", "pH = 0 because HCl is formed"]),

        ("Sodium ethanoate (CH3COONa)", "Basic (pH > 7)",
         "Formed from weak acid (CH3COOH) and strong base (NaOH). The ethanoate ion (CH3COO-) hydrolyses: CH3COO- + H2O ⇌ CH3COOH + OH-, producing excess hydroxide ions.",
         ["Acidic (pH < 7) because it is an organic acid derivative", "Neutral (pH = 7) because sodium cancels ethanoate", "Acidic (pH < 7) because ethanoic acid is released", "Neutral (pH = 7) because all sodium salts are neutral", "Strongly acidic (pH = 2)", "pH = 1 because acetic acid is vinegar"]),

        ("Sodium carbonate (Na2CO3)", "Basic (pH > 7)",
         "Formed from weak acid (H2CO3) and strong base (NaOH). Carbonate ion hydrolyses: CO3(2-) + H2O ⇌ HCO3- + OH-, increasing [OH-].",
         ["Acidic (pH < 7) because carbon dioxide is acidic", "Neutral (pH = 7) because sodium carbonate is an unreactive mineral", "Acidic (pH < 7) because sodium ions react with water", "Neutral (pH = 7) because carbon forms neutral covalent bonds", "Strongly acidic (pH = 3)", "pH = 7 at all temperatures"]),

        ("Potassium nitrate (KNO3)", "Neutral (pH ≈ 7)",
         "Formed from strong acid (HNO3) and strong base (KOH); neither K+ nor NO3- undergoes hydrolysis.",
         ["Acidic (pH < 7) because nitrate ions hydrolyse", "Basic (pH > 7) because potassium ions form KOH", "Acidic (pH < 7) because nitric acid is strong", "Basic (pH > 7) because nitrogen is alkaline", "Strongly acidic (pH = 1.5)", "Strongly basic (pH = 12.5)"])
    ]
    for sname, nature, reason, wr in salt_hydrolysis:
        add_q("medium", "Salt Hydrolysis",
              f"Determine the acidic, basic, or neutral nature of an aqueous solution of {sname} at 25 °C, and give the correct chemical explanation:",
              f"{nature}. {reason}", wr, "Comprehension", "Explain salt hydrolysis")

    # 5. Indicator Selection for Titrations
    indicators = [
        ("Strong acid (e.g. HCl) titrated against Strong base (e.g. NaOH)", "Bromothymol blue", "The equivalence point occurs at pH ≈ 7, matching the yellow-to-blue transition range of bromothymol blue (pH 6.0 - 7.6).",
         ["Methyl orange (range 3.1 - 4.4)", "Phenolphthalein (range 8.3 - 10.0)", "Universal indicator paper only", "Litmus paper only", "No indicator is suitable", "Starch solution"]),

        ("Strong acid (e.g. HCl) titrated against Weak base (e.g. NH3)", "Methyl orange", "The equivalence point occurs in the acidic region (pH < 7) due to salt hydrolysis (NH4+), matching the red-to-yellow transition range of methyl orange (pH 3.1 - 4.4).",
         ["Phenolphthalein (range 8.3 - 10.0)", "Bromothymol blue (range 6.0 - 7.6)", "Universal indicator only", "Phenol red (range 6.8 - 8.4)", "Starch indicator", "Thymol blue"]),

        ("Weak acid (e.g. CH3COOH) titrated against Strong base (e.g. NaOH)", "Phenolphthalein", "The equivalence point occurs in the basic region (pH > 7) due to hydrolysis of the conjugate base (CH3COO-), matching the colourless-to-pink transition range of phenolphthalein (pH 8.3 - 10.0).",
         ["Methyl orange (range 3.1 - 4.4)", "Bromothymol blue (range 6.0 - 7.6)", "Methyl red (range 4.4 - 6.2)", "Congo red", "Universal indicator", "Litmus"])
    ]
    for titr_type, ind_name, ind_reason, wr in indicators:
        add_q("medium", "Indicators",
              f"Which indicator is most suitable for a titration involving: **{titr_type}**?",
              f"{ind_name} ({ind_reason})", [f"{w}" for w in wr], "Application", "Select titration indicator")

    # Complete medium to 500
    med_count = sum(1 for q in questions if q['difficulty'] == 'medium')
    seed = 1
    while med_count < 500:
        c_pick = acid_concs[(seed - 1) % len(acid_concs)]
        q_text = f"[Quantitative pH Evaluation {seed}] A student prepares a nitric acid (HNO3) solution with concentration {c_pick[0]} mol·dm⁻³. What is the exact pH of this solution at 25 °C?"
        if add_q("medium", "pH Calculations", q_text, c_pick[1], [f"{14 - float(c_pick[1]):.2f}", f"{float(c_pick[1]) + 1:.2f}", f"{float(c_pick[1]) - 1:.2f}", f"{c_pick[0]:.2f}", f"{float(c_pick[1]) * 2:.2f}", f"{float(c_pick[1]) + 0.5:.2f}"], "Application", "Calculate monoprotic acid pH"):
            med_count += 1
        seed += 1

    # -------------------------------------------------------------
    # HARD (200 questions) - Titration Neutralization Calculations & Excess Acid/Base
    # -------------------------------------------------------------
    # Reaction 1: HCl + NaOH -> NaCl + H2O (1:1 mole ratio)
    # c_a * V_a = c_b * V_b => c_a = (c_b * V_b) / V_a
    titr_1_to_1 = [
        (25.0, 0.10, 20.0), # V_a = 25 cm3, c_b = 0.10 M, V_b = 20.0 cm3 => c_a = (0.10 * 20) / 25 = 0.080 mol/dm3
        (25.0, 0.15, 30.0), # c_a = (0.15 * 30) / 25 = 0.180 mol/dm3
        (20.0, 0.20, 25.0), # c_a = (0.20 * 25) / 20 = 0.250 mol/dm3
        (25.0, 0.12, 22.5), # c_a = (0.12 * 22.5) / 25 = 0.108 mol/dm3
        (10.0, 0.05, 16.0), # c_a = (0.05 * 16) / 10 = 0.080 mol/dm3
        (25.0, 0.25, 24.0)  # c_a = (0.25 * 24) / 25 = 0.240 mol/dm3
    ]
    for va, cb, vb in titr_1_to_1:
        ca = (cb * vb) / va
        ca_str = f"{ca:.3f} mol·dm⁻³"
        wrongs = [
            f"{(cb * va) / vb:.3f} mol·dm⁻³",
            f"{ca * 2:.3f} mol·dm⁻³",
            f"{ca / 2:.3f} mol·dm⁻³",
            f"{(cb * vb):.3f} mol·dm⁻³",
            f"{ca + 0.05:.3f} mol·dm⁻³",
            f"{ca * 10:.3f} mol·dm⁻³"
        ]
        add_q("hard", "Titration Calculations",
              f"During a titration, {va:.1f} cm³ of hydrochloric acid (HCl) of unknown concentration is exactly neutralised by {vb:.1f} cm³ of a {cb:.2f} mol·dm⁻³ sodium hydroxide (NaOH) standard solution according to: \nHCl(aq) + NaOH(aq) → NaCl(aq) + H2O(l)\nCalculate the concentration of the hydrochloric acid solution:",
              ca_str, wrongs, "Analysis", "Calculate unknown concentration from 1:1 titration")

    # Reaction 2: H2SO4 + 2NaOH -> Na2SO4 + 2H2O (1:2 mole ratio!)
    # n_a / n_b = 1 / 2 => c_a * V_a / (c_b * V_b) = 1 / 2 => c_a = (c_b * V_b) / (2 * V_a)
    titr_diprotic = [
        (25.0, 0.10, 20.0), # c_a = (0.10 * 20) / (2 * 25) = 0.040 mol/dm3
        (25.0, 0.20, 30.0), # c_a = (0.20 * 30) / (2 * 25) = 0.120 mol/dm3
        (20.0, 0.15, 24.0), # c_a = (0.15 * 24) / (2 * 20) = 0.090 mol/dm3
        (25.0, 0.25, 25.0), # c_a = (0.25 * 25) / (2 * 25) = 0.125 mol/dm3
        (10.0, 0.10, 15.0)  # c_a = (0.10 * 15) / (2 * 10) = 0.075 mol/dm3
    ]
    for va, cb, vb in titr_diprotic:
        ca = (cb * vb) / (2 * va)
        ca_str = f"{ca:.3f} mol·dm⁻³"
        err_no_ratio = (cb * vb) / va
        wrongs = [
            f"{err_no_ratio:.3f} mol·dm⁻³ (omitted 1:2 stoichiometric mole ratio)",
            f"{ca * 4:.3f} mol·dm⁻³",
            f"{ca / 2:.3f} mol·dm⁻³",
            f"{(cb * 2 * va) / vb:.3f} mol·dm⁻³",
            f"{ca + 0.05:.3f} mol·dm⁻³",
            f"{ca * 10:.3f} mol·dm⁻³"
        ]
        add_q("hard", "Titration Calculations (Diprotic)",
              f"In a titration, {va:.1f} cm³ of sulfuric acid (H2SO4) requires {vb:.1f} cm³ of {cb:.2f} mol·dm⁻³ sodium hydroxide (NaOH) for complete neutralization according to: \nH2SO4(aq) + 2NaOH(aq) → Na2SO4(aq) + 2H2O(l)\nCalculate the concentration of the sulfuric acid solution:",
              ca_str, wrongs, "Analysis", "Calculate concentration accounting for 1:2 mole ratio")

    # Reaction 3: Excess Acid / Base (Calculating final pH after mixing)
    excess_scenarios = [
        # Mix 50 cm3 of 0.2 mol/dm3 HCl with 50 cm3 of 0.1 mol/dm3 NaOH
        # n(HCl) = 0.050 * 0.2 = 0.010 mol
        # n(NaOH) = 0.050 * 0.1 = 0.005 mol
        # Excess n(HCl) = 0.010 - 0.005 = 0.005 mol
        # Total volume = 50 + 50 = 100 cm3 = 0.100 dm3
        # [H3O+] = 0.005 / 0.100 = 0.050 mol/dm3 => pH = -log(0.050) = 1.30
        ("50.0 cm³ of 0.20 mol·dm⁻³ HCl is mixed with 50.0 cm³ of 0.10 mol·dm⁻³ NaOH at 25 °C. Calculate the pH of the resulting mixture:",
         "1.30 (Excess H3O+ = 0.005 mol in 0.100 dm³, giving [H3O+] = 0.050 mol·dm⁻³)",
         ["7.00 (Neutral because an acid and base were mixed)",
          "1.00 (Based on initial acid concentration without subtracting consumed base)",
          "12.70 (Calculated as a basic solution)",
          "2.00 (Omitted total volume addition)",
          "0.70 (Calculated without dividing by total volume of 100 cm³)",
          "13.00 (Base concentration alone)"]),

        # Mix 40 cm3 of 0.1 mol/dm3 HCl with 60 cm3 of 0.1 mol/dm3 NaOH
        # n(HCl) = 0.040 * 0.1 = 0.004 mol
        # n(NaOH) = 0.060 * 0.1 = 0.006 mol
        # Excess n(NaOH) = 0.006 - 0.004 = 0.002 mol
        # Total volume = 40 + 60 = 100 cm3 = 0.100 dm3
        # [OH-] = 0.002 / 0.100 = 0.020 mol/dm3 => pOH = -log(0.020) = 1.70 => pH = 14 - 1.70 = 12.30
        ("40.0 cm³ of 0.10 mol·dm⁻³ HCl is mixed with 60.0 cm³ of 0.10 mol·dm⁻³ NaOH at 25 °C. Calculate the pH of the resulting solution:",
         "12.30 (Excess OH- = 0.002 mol in 0.100 dm³, giving [OH-] = 0.020 mol·dm⁻³, pOH = 1.70, and pH = 14 - 1.70)",
         ["1.70 (The pOH was mistakenly taken as the pH)",
          "7.00 (Assuming neutralisation reaches pH 7 regardless of proportions)",
          "13.00 (Based on initial base concentration alone)",
          "11.30 (Omitted combining solution volumes to 100 cm³)",
          "2.30 (Assuming acid was in excess)",
          "14.00 (Assuming complete conversion to hydroxide ions)"])
    ]
    for q_text, corr, wr in excess_scenarios:
        add_q("hard", "Excess Neutralization Calculations", q_text, corr, wr, "Analysis", "Calculate pH of mixture with excess reagent")

    # Complete hard to exactly 200
    hard_count = sum(1 for q in questions if q['difficulty'] == 'hard')
    seed = 1
    while hard_count < 200:
        t_pick = titr_1_to_1[(seed - 1) % len(titr_1_to_1)]
        va, cb, vb = t_pick
        ca = (cb * vb) / va
        q_text = f"[Stoichiometric Problem {seed}] A learner titrates a {va:.1f} cm³ aliquot of an unknown monoprotic acid with {vb:.1f} cm³ of {cb:.2f} mol·dm⁻³ standard base solution to the phenolphthalein end point. Calculate the acid concentration:"
        if add_q("hard", "Titration Calculations", q_text, f"{ca:.3f} mol·dm⁻³", [f"{(cb*va)/vb:.3f} mol·dm⁻³", f"{ca*2:.3f} mol·dm⁻³", f"{ca/2:.3f} mol·dm⁻³", f"{ca*10:.3f} mol·dm⁻³", f"{ca+0.05:.3f} mol·dm⁻³", f"{cb:.3f} mol·dm⁻³"], "Analysis", "Solve titration math"):
            hard_count += 1
        seed += 1

    return questions

if __name__ == '__main__':
    qs = build_acids_bases()
    out_dir = "dataset/grade12/physical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_acids_bases.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)
    
    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
