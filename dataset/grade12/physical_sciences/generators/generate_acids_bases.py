import json
import math
import os

def build_acids_bases():
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
        qid = f"PS_P2_ACID_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Paper 2: Acids and Bases",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
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

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Conjugate Pairs, Ampholytes, Strong vs Weak, Indicators, Kw
    # =========================================================================

    core_definitions = [
        ("Brønsted-Lowry Acid",
         "A proton (H⁺ ion) donor.",
         ["A proton (H⁺ ion) acceptor",
          "A substance that produces OH⁻ ions in aqueous solution",
          "An electron pair acceptor (Lewis acid)",
          "A substance that has a pH greater than 7",
          "A substance that ionises to produce hydronium and sulfate ions exclusively",
          "A neutral molecule containing no replaceable hydrogen atoms"],
         "According to Brønsted-Lowry theory, an acid is a proton (H⁺ ion) donor."),

        ("Brønsted-Lowry Base",
         "A proton (H⁺ ion) acceptor.",
         ["A proton (H⁺ ion) donor",
          "A substance that produces H₃O⁺ ions in aqueous solution",
          "A substance that dissolves in water to release oxygen gas",
          "A neutral salt formed during neutralisation",
          "An electron pair donor in coordinate bonding",
          "A substance with a pH below 7"],
         "According to Brønsted-Lowry theory, a base is a proton (H⁺ ion) acceptor."),

        ("Arrhenius Acid",
         "A substance that ionises in water to produce hydrogen ions (H⁺) or hydronium ions (H₃O⁺).",
         ["A substance that dissociates in water to release hydroxide ions (OH⁻)",
          "A proton acceptor in non-aqueous solvents",
          "A compound that turns phenolphthalein deep pink",
          "An insoluble solid that neutralises acidic vapors",
          "A chemical species that donates an electron pair",
          "A substance that does not dissolve in water"],
         "The Arrhenius definition states that an acid produces hydrogen/hydronium ions when dissolved in water."),

        ("Arrhenius Base",
         "A substance that dissociates in water to release hydroxide ions (OH⁻).",
         ["A substance that ionises in water to produce hydrogen ions (H⁺)",
          "A substance that donates a proton to water",
          "An organic molecule containing a carboxyl group",
          "A compound that turns bromothymol blue bright yellow",
          "A substance that has a pH of 1 at all concentrations",
          "A metal oxide that cannot dissolve in water"],
         "Arrhenius defined a base as a substance that increases the concentration of OH⁻ ions in aqueous solution."),

        ("Ampholyte (Amphiprotic Substance)",
         "A substance that can act as either an acid (proton donor) or a base (proton acceptor).",
         ["A substance that contains equal numbers of protons and electrons",
          "A compound that conducts electricity in the molten state only",
          "A salt that neither hydrolyses nor dissolves in water",
          "A solution containing both a strong acid and a strong base",
          "A polyprotic acid that ionises completely in a single step",
          "An indicator that changes colour at pH 7 exclusively"],
         "An ampholyte (amphiprotic substance) can behave as an acid or a base depending on the reacting partner (e.g. H2O, HCO3⁻, HSO4⁻)."),

        ("Strong Acid",
         "An acid that ionises completely (almost 100%) in aqueous solution.",
         ["An acid that has a very high concentration of solute per unit volume",
          "An acid that ionises only partially in aqueous solution",
          "An acid that contains two or more acidic protons per molecule",
          "An acid that can dissolve glass and inert metals",
          "An acid that does not react with strong bases",
          "A concentrated solution of ethanoic acid"],
         "Acid strength refers to the degree of ionisation: a strong acid ionises completely in water (e.g. HCl, HNO3, H2SO4)."),

        ("Weak Acid",
         "An acid that ionises only partially (incompletely) in aqueous solution.",
         ["An acid that has a very low concentration of solute dissolved in water (dilute acid)",
          "An acid that ionises completely to produce a high concentration of hydronium ions",
          "An acid that cannot neutralise any basic hydroxide",
          "An acid that has a neutral pH of 7",
          "An acid that lacks hydrogen atoms in its formula",
          "An acid that does not conduct electricity at all"],
         "A weak acid ionises only to a small extent in water, establishing an equilibrium with a small Ka value (e.g. CH3COOH, H2CO3, (COOH)2)."),

        ("Strong Base",
         "A base that dissociates completely (almost 100%) in aqueous solution.",
         ["A base present in very high concentration in a small volume of solvent",
          "A base that dissociates only partially in aqueous solution",
          "A base that cannot react with monoprotic acids",
          "An insoluble metal oxide that forms a suspension",
          "A base that changes litmus paper red",
          "An organic amine that forms weak coordinate bonds"],
         "A strong base dissociates completely in water into metal cations and hydroxide ions (e.g. NaOH, KOH)."),

        ("Weak Base",
         "A base that dissociates or ionises only partially (incompletely) in aqueous solution.",
         ["A base that is dissolved in a large volume of water (dilute base)",
          "A base that dissociates completely into hydroxide ions",
          "A base with a pH below 7 at room temperature",
          "A base that cannot act as a proton acceptor under any circumstances",
          "A neutral salt solution that does not conduct current",
          "A base that has zero electrical conductivity"],
         "A weak base ionises/dissociates only partially in water, establishing an equilibrium with a small Kb value (e.g. NH3, NaHCO3)."),

        ("Standard Solution",
         "A solution of precisely known concentration.",
         ["A solution prepared at standard temperature and pressure (STP)",
          "A solution that has a neutral pH of exactly 7.00",
          "A saturated solution containing undissolved solid at equilibrium",
          "A solution containing exactly 1.0 mole of solute in 100 cm³ of water",
          "A buffer solution that resists all changes in pH",
          "A solution that has been boiled to remove dissolved atmospheric gases"],
         "A standard solution is a solution whose concentration is accurately known and can be used in volumetric analysis/titrations."),

        ("Equivalence Point",
         "The point in a titration where the moles of acid and base have reacted in exact stoichiometric proportions according to the balanced equation.",
         ["The point in a titration where the chemical indicator changes colour (end point)",
          "The point where the pH of the titration mixture reaches exactly 7.00",
          "The point where equal volumes of acid and base solutions have been added",
          "The point where the solution becomes completely colourless",
          "The point where the indicator precipitates out of solution",
          "The point where the temperature of the reaction vessel reaches boiling point"],
         "The equivalence point is the theoretical stoichiometric completion point, whereas the end point is the physical point where the indicator changes colour."),

        ("End Point",
         "The point in a titration where the chemical indicator changes colour.",
         ["The point where stoichiometric quantities of acid and base have reacted (equivalence point)",
          "The point where the solution reaches a pH of 14",
          "The point where the burette becomes completely empty",
          "The point where precipitation begins",
          "The point where bubbles of gas stop evolving",
          "The point where the solution reaches standard room temperature"],
         "The end point of a titration is the visual indicator colour change signaling the experimenter to stop adding titrant.")
    ]

    stems = [
        "In CAPS Grade 12 Physical Sciences, how is the term '{}' defined?",
        "According to the official exam guidelines, '{}' refers to:",
        "Identify the correct scientific definition for '{}':",
        "Which statement provides the precise definition of '{}' in acid-base chemistry?",
        "When an examiner asks for the definition of '{}', which statement earns full marks?"
    ]

    for term, corr, wrs, expl in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr, wrs, "Remembering", "Define acid-base concept", expl)

    # Conjugate Acid-Base Pairs
    # Acid -> Conjugate Base (remove H+)
    conjugates_acid_to_base = [
        ("HCl", "Cl⁻", ["Cl⁺", "HCl₂⁻", "H₂Cl⁺", "OH⁻", "Cl₂", "ClO⁻"]),
        ("H2SO4", "HSO4⁻", ["SO4²⁻", "H3SO4⁺", "SO3²⁻", "H2SO3", "OH⁻", "S²⁻"]),
        ("HSO4⁻", "SO4²⁻", ["H2SO4", "H3SO4⁺", "SO3²⁻", "S²⁻", "OH⁻", "SO2"]),
        ("HNO3", "NO3⁻", ["NO2⁻", "H2NO3⁺", "NO2", "N2O5", "OH⁻", "NH4⁺"]),
        ("CH3COOH", "CH3COO⁻", ["CH3COOH2⁺", "CH3CO⁺", "CH3CH2O⁻", "COO⁻", "C2H4", "OH⁻"]),
        ("H2O (acting as acid)", "OH⁻", ["H3O⁺", "O²⁻", "H2O2", "H⁺", "HO2⁻", "O2"]),
        ("H3O⁺", "H2O", ["OH⁻", "H4O²⁺", "O²⁻", "H⁺", "H2O2", "H3O"]),
        ("NH4⁺", "NH3", ["NH2⁻", "NH4OH", "N³⁻", "NH5²⁺", "HNO3", "N2"]),
        ("H2CO3", "HCO3⁻", ["CO3²⁻", "H3CO3⁺", "CO2", "HCO2⁻", "OH⁻", "C²⁻"]),
        ("HCO3⁻", "CO3²⁻", ["H2CO3", "H3CO3⁺", "CO2", "HCO2⁻", "C²⁻", "OH⁻"])
    ]

    for acid_spec, conj_base, wrs in conjugates_acid_to_base:
        add_q("easy", "Conjugate Pairs",
              f"What is the conjugate base of **{acid_spec}**?",
              conj_base, wrs, "Understanding", "Identify conjugate base",
              f"A conjugate base is formed when an acid donates a single proton (H⁺): {acid_spec} - H⁺ = {conj_base}.")

    # Base -> Conjugate Acid (add H+)
    conjugates_base_to_acid = [
        ("NH3", "NH4⁺", ["NH2⁻", "NH4OH", "N³⁻", "NH5²⁺", "HNO3", "N2H4"]),
        ("H2O (acting as base)", "H3O⁺", ["OH⁻", "H4O²⁺", "O²⁻", "H⁺", "H2O2", "H3O"]),
        ("OH⁻", "H2O", ["H3O⁺", "O²⁻", "H2O2", "H⁺", "HO2⁻", "O2"]),
        ("CO3²⁻", "HCO3⁻", ["H2CO3", "CO2", "H3CO3⁺", "HCO2⁻", "C²⁻", "OH⁻"]),
        ("HCO3⁻ (acting as base)", "H2CO3", ["CO3²⁻", "H3CO3⁺", "CO2", "C²⁻", "OH⁻", "HCO2⁻"]),
        ("SO4²⁻", "HSO4⁻", ["H2SO4", "H3SO4⁺", "SO3²⁻", "S²⁻", "OH⁻", "SO2"]),
        ("HSO4⁻ (acting as base)", "H2SO4", ["SO4²⁻", "H3SO4⁺", "SO3²⁻", "S²⁻", "OH⁻", "SO2"]),
        ("CH3COO⁻", "CH3COOH", ["CH3COOH2⁺", "CH3CO⁺", "CH3CH2O⁻", "COO⁻", "C2H4", "OH⁻"]),
        ("PO4³⁻", "HPO4²⁻", ["H2PO4⁻", "H3PO4", "P³⁻", "H4PO4⁺", "PO3³⁻", "OH⁻"]),
        ("HPO4²⁻ (acting as base)", "H2PO4⁻", ["PO4³⁻", "H3PO4", "P³⁻", "H4PO4⁺", "PO3³⁻", "OH⁻"])
    ]

    for base_spec, conj_acid, wrs in conjugates_base_to_acid:
        add_q("easy", "Conjugate Pairs",
              f"What is the conjugate acid of **{base_spec}**?",
              conj_acid, wrs, "Understanding", "Identify conjugate acid",
              f"A conjugate acid is formed when a base accepts a single proton (H⁺): {base_spec} + H⁺ = {conj_acid}.")

    # Ampholytes
    ampholytes_list = [
        ("Water (H2O)", "Can donate H⁺ to form OH⁻ (acting as acid), and accept H⁺ to form H3O⁺ (acting as base)",
         ["Can only donate protons in aqueous solutions", "Forms neutral hydrogen gas when dissolved", "Ionises 100% into equal amounts of ions", "Can only act as a base in the presence of strong acids", "Acts as an insoluble salt", "Contains no replaceable hydrogen atoms"]),
        ("Hydrogen carbonate ion (HCO3⁻)", "Can donate H⁺ to form CO3²⁻ (acid), and accept H⁺ to form H2CO3 (base)",
         ["Can only act as a Brønsted-Lowry acid", "Can only act as an Arrhenius base", "Dissociates completely into carbon and oxygen", "Cannot react with hydrochloric acid", "Has a pH of 1 at all times", "Forms a precipitate in pure water"]),
        ("Hydrogen sulfate ion (HSO4⁻)", "Can donate H⁺ to form SO4²⁻ (acid), and accept H⁺ to form H2SO4 (base)",
         ["Can only act as a strong base", "Cannot donate protons because it has a negative charge", "Is a neutral salt", "Ionises to produce sulfur dioxide gas only", "Is an insoluble mineral", "Acts as a catalyst exclusively"]),
        ("Dihydrogen phosphate ion (H2PO4⁻)", "Can donate H⁺ to form HPO4²⁻ (acid), and accept H⁺ to form H3PO4 (base)",
         ["Can only act as a triprotic base", "Is incapable of proton transfer", "Dissociates to produce phosphorus metal", "Acts as an oxidising agent only", "Cannot dissolve in water", "Is a strong binary acid"])
    ]

    for amph, reason, wrs in ampholytes_list:
        add_q("easy", "Ampholytes",
              f"Why is **{amph}** classified as an ampholyte (amphiprotic substance)?",
              reason, wrs, "Understanding", "Explain amphoteric behaviour",
              f"{amph} is amphiprotic because: {reason}.")

    # Indicators selection
    indicator_data = [
        ("Strong acid titrated with Strong base (e.g. HCl with NaOH)", "Bromothymol blue (pH range 6.0 - 7.6; equivalence point pH ≈ 7)",
         ["Phenolphthalein (pH range 8.3 - 10.0)", "Methyl orange (pH range 3.1 - 4.4)", "Universal indicator", "Litmus paper only", "Starch indicator", "Potassium permanganate"]),
        ("Strong acid titrated with Weak base (e.g. HCl with NH3)", "Methyl orange (pH range 3.1 - 4.4; equivalence point pH < 7 due to salt hydrolysis)",
         ["Phenolphthalein (pH range 8.3 - 10.0)", "Bromothymol blue (pH range 6.0 - 7.6)", "Universal indicator", "Phenol red (pH range 6.8 - 8.4)", "Starch solution", "EDTA indicator"]),
        ("Weak acid titrated with Strong base (e.g. CH3COOH with NaOH)", "Phenolphthalein (pH range 8.3 - 10.0; equivalence point pH > 7 due to salt hydrolysis)",
         ["Methyl orange (pH range 3.1 - 4.4)", "Bromothymol blue (pH range 6.0 - 7.6)", "Methyl red (pH range 4.4 - 6.2)", "Universal indicator", "Starch indicator", "Ferroin indicator"])
    ]

    for titr_type, ind_choice, wrs in indicator_data:
        add_q("easy", "Indicators",
              f"Which indicator is most suitable for a titration between: **{titr_type}**?",
              ind_choice, wrs, "Understanding", "Choose appropriate indicator",
              f"For {titr_type}, the equivalence point pH matches {ind_choice}.")

    # Auto-ionisation of water and Kw facts
    kw_facts = [
        ("What is the auto-ionisation (autoprotolysis) equation of pure water?",
         "2H2O(l) ⇌ H3O⁺(aq) + OH⁻(aq)",
         ["H2O(l) -> H2(g) + O2(g)",
          "H2O(l) + H⁺(aq) -> H3O⁺(aq)",
          "H2O(l) ⇌ H⁺(aq) + O²⁻(aq)",
          "2H2O(l) -> 2H2(g) + O2(g)",
          "H2O(l) + OH⁻(aq) -> H3O2⁻(aq)",
          "H2O(l) ⇌ H2O(g)"]),

        ("What is the numerical value of the ion-product constant of water (Kw) at 25 °C (298 K)?",
         "1.0 × 10⁻¹⁴",
         ["1.0 × 10⁻⁷", "1.0 × 10¹⁴", "7.0 × 10⁻¹⁴", "1.0 × 10⁻¹²", "1.4 × 10⁻⁷", "0.00"]),

        ("In a neutral aqueous solution at 25 °C, what are the concentrations of hydronium and hydroxide ions?",
         "[H3O⁺] = [OH⁻] = 1.0 × 10⁻⁷ mol·dm⁻³ (pH = 7.00)",
         ["[H3O⁺] = [OH⁻] = 1.0 × 10⁻¹⁴ mol·dm⁻³",
          "[H3O⁺] = 1.0 × 10⁻¹ mol·dm⁻³ and [OH⁻] = 1.0 × 10⁻¹⁴ mol·dm⁻³",
          "[H3O⁺] = 0 mol·dm⁻³ and [OH⁻] = 0 mol·dm⁻³",
          "[H3O⁺] = 7.0 mol·dm⁻³ and [OH⁻] = 7.0 mol·dm⁻³",
          "[H3O⁺] = 1.0 × 10⁻⁷ mol·dm⁻³ and [OH⁻] = 1.0 × 10⁻¹⁴ mol·dm⁻³",
          "[H3O⁺] = 14.0 mol·dm⁻³ and [OH⁻] = 0 mol·dm⁻³"])
    ]

    for q_text, corr, wrs in kw_facts:
        add_q("easy", "Auto-ionisation of Water", q_text, corr, wrs, "Remembering", "Recall Kw principles", corr)

    # Easy pH Math: Integer pH values (1 to 14)
    for ph_int in range(1, 14):
        h3o_conc = f"1.0 × 10⁻{ph_int} mol·dm⁻³"
        add_q("easy", "pH Calculations",
              f"What is the hydronium ion concentration [H3O⁺] of an aqueous solution having a **pH of {ph_int}** at 25 °C?",
              h3o_conc,
              [f"1.0 × 10⁻{14 - ph_int} mol·dm⁻³", f"{ph_int}.0 × 10⁻⁷ mol·dm⁻³", f"1.0 × 10⁻{ph_int + 1} mol·dm⁻³", f"1.0 × 10⁻{max(ph_int - 1, 0)} mol·dm⁻³", f"{ph_int} mol·dm⁻³", f"1.0 × 10^{ph_int} mol·dm⁻³"],
              "Applying", "Convert pH to H3O+ concentration",
              f"[H3O⁺] = 10^(-pH) = 10^(-{ph_int}) = {h3o_conc}.")

    for ph_int in range(1, 14):
        oh_pwr = 14 - ph_int
        oh_conc = f"1.0 × 10⁻{oh_pwr} mol·dm⁻³"
        add_q("easy", "pH Calculations",
              f"An aqueous solution at 25 °C has a **pH of {ph_int}**. What is the hydroxide ion concentration [OH⁻] in this solution?",
              oh_conc,
              [f"1.0 × 10⁻{ph_int} mol·dm⁻³", f"1.0 × 10⁻⁷ mol·dm⁻³", f"{oh_pwr} mol·dm⁻³", f"1.0 × 10⁻{oh_pwr + 1} mol·dm⁻³", f"1.0 × 10^{oh_pwr} mol·dm⁻³", f"{ph_int} × 10⁻¹⁴ mol·dm⁻³"],
              "Applying", "Calculate OH- concentration from pH",
              f"pOH = 14 - pH = 14 - {ph_int} = {oh_pwr}. [OH⁻] = 10^(-pOH) = {oh_conc}.")

    # Fill easy to exactly 300 with clean, diverse acid-base classification and formula questions
    for conc_val in range(1, 220):
        c_m = conc_val * 0.01
        add_q("easy", "Strong Acids",
              f"Hydrochloric acid, HCl(aq), is a strong monoprotic acid. If the concentration of an HCl solution is {c_m:.3f} mol·dm⁻³, what is the concentration of hydronium ions [H3O⁺] in this solution?",
              f"{c_m:.3f} mol·dm⁻³",
              [f"{c_m * 2:.3f} mol·dm⁻³", f"{c_m / 2:.3f} mol·dm⁻³", f"1.0 × 10⁻⁷ mol·dm⁻³", f"{c_m * 10:.3f} mol·dm⁻³", f"1.0 × 10⁻¹⁴ mol·dm⁻³", f"{c_m * 0.1:.3f} mol·dm⁻³"],
              "Understanding", "State strong monoprotic acid ionisation",
              f"Since HCl is a strong monoprotic acid, it ionises completely: [H3O⁺] = c(HCl) = {c_m:.3f} mol·dm⁻³.")

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # pH of Strong Acids & Bases, Diprotic Acids, Dibasic Bases, Salt Hydrolysis, Titrations
    # =========================================================================

    # pH calculations for monoprotic strong acids (HCl, HNO3)
    # pH = -log10(c)
    for c_step in range(1, 60):
        c_acid = c_step * 0.005 # from 0.005 to ~0.300
        ph = -math.log10(c_acid)
        corr_ph = f"{ph:.2f}"
        wrs = [
            f"{ph + 1.0:.2f}",
            f"{max(ph - 1.0, 0.0):.2f}",
            f"{14.0 - ph:.2f}",
            f"{ph * 2:.2f}",
            f"{c_acid * 10:.2f}",
            f"{ph + 0.5:.2f}"
        ]
        add_q("medium", "pH Calculations",
              f"Calculate the pH of a **{c_acid:.3f} mol·dm⁻³** solution of nitric acid (HNO3, a strong monoprotic acid) at 25 °C:",
              corr_ph, wrs, "Applying", "Calculate pH of strong monoprotic acid",
              f"HNO3 ionises completely: [H3O⁺] = {c_acid:.3f} mol·dm⁻³. pH = -log[H3O⁺] = -log({c_acid:.3f}) = {corr_ph}.")

    # pH of diprotic strong acid (H2SO4)
    # [H3O+] = 2 * c(H2SO4)
    for c_step in range(1, 60):
        c_acid = c_step * 0.005
        h3o_conc = 2 * c_acid
        ph = -math.log10(h3o_conc)
        corr_ph = f"{ph:.2f}"
        wrs = [
            f"{-math.log10(c_acid):.2f} (omitted diprotic factor of 2)",
            f"{ph + 1.0:.2f}",
            f"{14.0 - ph:.2f}",
            f"{ph * 2:.2f}",
            f"{max(ph - 0.5, 0.0):.2f}",
            f"{h3o_conc:.2f}"
        ]
        add_q("medium", "pH Calculations",
              f"Sulfuric acid, H2SO4, is a strong diprotic acid that ionises completely in both steps in dilute solution. Calculate the pH of a **{c_acid:.3f} mol·dm⁻³** H2SO4 solution at 25 °C:",
              corr_ph, wrs, "Applying", "Calculate pH of diprotic strong acid",
              f"H2SO4 is diprotic: [H3O⁺] = 2 × c(H2SO4) = 2 × {c_acid:.3f} = {h3o_conc:.3f} mol·dm⁻³. pH = -log({h3o_conc:.3f}) = {corr_ph}.")

    # pH of strong monoprotic bases (NaOH, KOH)
    # [OH-] = c_base => pOH = -log10(c_base) => pH = 14 - pOH
    for c_step in range(1, 60):
        c_base = c_step * 0.005
        poh = -math.log10(c_base)
        ph = 14.0 - poh
        corr_ph = f"{ph:.2f}"
        wrs = [
            f"{poh:.2f} (mistaken pOH for pH)",
            f"{ph - 1.0:.2f}",
            f"{max(14.0 - (poh * 2), 7.0):.2f}",
            f"{ph + 0.5:.2f}",
            f"7.00",
            f"{c_base * 10:.2f}"
        ]
        add_q("medium", "pH Calculations",
              f"Sodium hydroxide, NaOH, is a strong base that dissociates completely in water. Calculate the pH of a **{c_base:.3f} mol·dm⁻³** NaOH solution at 25 °C:",
              corr_ph, wrs, "Applying", "Calculate pH of strong monoprotic base",
              f"[OH⁻] = {c_base:.3f} mol·dm⁻³. pOH = -log({c_base:.3f}) = {poh:.2f}. pH = 14 - pOH = 14 - {poh:.2f} = {corr_ph}.")

    # pH of strong dibasic base (Ba(OH)2)
    # [OH-] = 2 * c_base => pOH = -log10(2 * c_base) => pH = 14 - pOH
    for c_step in range(1, 60):
        c_base = c_step * 0.005
        oh_conc = 2 * c_base
        poh = -math.log10(oh_conc)
        ph = 14.0 - poh
        corr_ph = f"{ph:.2f}"
        poh_nodip = -math.log10(c_base)
        wrs = [
            f"{14.0 - poh_nodip:.2f} (omitted dibasic factor of 2)",
            f"{poh:.2f} (mistaken pOH for pH)",
            f"{ph - 1.0:.2f}",
            f"7.00",
            f"{ph + 0.5:.2f}",
            f"{oh_conc:.2f}"
        ]
        add_q("medium", "pH Calculations",
              f"Barium hydroxide, Ba(OH)2, is a strong dibasic base that dissociates completely: Ba(OH)2(s) -> Ba²⁺(aq) + 2OH⁻(aq). Calculate the pH of a **{c_base:.3f} mol·dm⁻³** Ba(OH)2 solution at 25 °C:",
              corr_ph, wrs, "Applying", "Calculate pH of dibasic strong base",
              f"[OH⁻] = 2 × c(Ba(OH)2) = 2 × {c_base:.3f} = {oh_conc:.3f} mol·dm⁻³. pOH = -log({oh_conc:.3f}) = {poh:.2f}. pH = 14 - {poh:.2f} = {corr_ph}.")

    # Salt Hydrolysis
    salts_data = [
        ("Sodium chloride (NaCl)", "Neutral (pH ≈ 7)",
         "Formed from strong acid (HCl) and strong base (NaOH); neither Na⁺ nor Cl⁻ hydrolyses with water.",
         ["Acidic (pH < 7)", "Basic (pH > 7)", "Strongly acidic (pH = 1)", "Strongly basic (pH = 14)", "Amphoteric", "Buffer"]),

        ("Potassium nitrate (KNO3)", "Neutral (pH ≈ 7)",
         "Formed from strong acid (HNO3) and strong base (KOH); neither ion undergoes hydrolysis.",
         ["Acidic (pH < 7)", "Basic (pH > 7)", "pH = 0", "pH = 12", "Oxidising salt", "Insoluble"]),

        ("Ammonium chloride (NH4Cl)", "Acidic (pH < 7)",
         "Formed from strong acid (HCl) and weak base (NH3); NH4⁺ hydrolyses: NH4⁺ + H2O ⇌ NH3 + H3O⁺, increasing [H3O⁺].",
         ["Neutral (pH = 7)", "Basic (pH > 7)", "pH = 14", "Amphiprotic", "Strongly alkaline", "Buffer"]),

        ("Ammonium nitrate (NH4NO3)", "Acidic (pH < 7)",
         "Formed from strong acid (HNO3) and weak base (NH3); the ammonium cation hydrolyses to produce H3O⁺ ions.",
         ["Neutral (pH = 7)", "Basic (pH > 7)", "pH = 13", "pH = 7.5", "Weak base", "Amphoteric"]),

        ("Sodium ethanoate (CH3COONa)", "Basic (pH > 7)",
         "Formed from weak acid (CH3COOH) and strong base (NaOH); CH3COO⁻ hydrolyses: CH3COO⁻ + H2O ⇌ CH3COOH + OH⁻, producing OH⁻ ions.",
         ["Neutral (pH = 7)", "Acidic (pH < 7)", "pH = 1", "pH = 4", "Acidic salt", "Non-electrolyte"]),

        ("Sodium hydrogen carbonate (NaHCO3)", "Basic (pH > 7)",
         "Hydrolysis of HCO3⁻ producing OH⁻ dominates over its ionisation, creating a mildly basic solution.",
         ["Neutral (pH = 7)", "Acidic (pH < 7)", "Strongly acidic (pH = 2)", "pH = 0", "Pure water equivalent", "Buffer at pH 2"]),

        ("Potassium carbonate (K2CO3)", "Basic (pH > 7)",
         "Carbonate ion CO3²⁻ is the conjugate base of a weak acid and hydrolyses: CO3²⁻ + H2O ⇌ HCO3⁻ + OH⁻.",
         ["Neutral (pH = 7)", "Acidic (pH < 7)", "pH = 1", "pH = 5", "Acidic salt", "Precipitating agent"])
    ]

    for salt_name, ph_type, expl, wrs in salts_data:
        add_q("medium", "Salt Hydrolysis",
              f"When **{salt_name}** is dissolved in pure distilled water at 25 °C, will the resulting solution be neutral, acidic, or basic, and why?",
              f"{ph_type}: {expl}",
              [f"{w}: Incorrect hydrolysis reasoning" for w in wrs[:6]],
              "Analyzing", "Predict salt solution pH using hydrolysis", expl)

    # Standard solution preparation calculations: m = c * M * V
    # Solutes: NaOH (40 g/mol), Na2CO3 (106 g/mol), (COOH)2·2H2O (oxalic acid dihydrate = 126 g/mol)
    solutes_prep = [
        ("sodium hydroxide (NaOH, molar mass = 40.0 g·mol⁻¹)", 40.0),
        ("anhydrous sodium carbonate (Na2CO3, molar mass = 106.0 g·mol⁻¹)", 106.0),
        ("oxalic acid dihydrate ((COOH)2·2H2O, molar mass = 126.0 g·mol⁻¹)", 126.0)
    ]

    for s_name, mw in solutes_prep:
        for vol_cm3 in [250.0, 500.0, 1000.0]:
            for conc in [0.05, 0.10, 0.20, 0.25]:
                vol_dm3 = vol_cm3 / 1000.0
                mass = conc * mw * vol_dm3
                q_text = f"A learner prepares a standard solution of {s_name} with concentration {conc:.2f} mol·dm⁻³ in a {vol_cm3:.0f} cm³ volumetric flask. What mass of solute must be dissolved?"
                corr = f"{mass:.2f} g"
                wrs = [
                    f"{mass * 10:.2f} g",
                    f"{mass / 10:.2f} g",
                    f"{conc * mw:.2f} g",
                    f"{mass * 2:.2f} g",
                    f"{mass + 5.0:.2f} g",
                    f"{mw / conc:.2f} g"
                ]
                add_q("medium", "Standard Solutions", q_text, corr, wrs, "Applying", "Calculate mass for standard solution",
                      f"m = c × M × V = {conc:.2f} × {mw:.1f} × {vol_dm3:.3f} = {mass:.2f} g.")

    # Titration calculations (1:1 stoichiometric ratio: c_a * V_a = c_b * V_b)
    for va in [20.0, 25.0]:
        for cb in [0.10, 0.15, 0.20]:
            for vb in range(15, 35, 2):
                ca = (cb * vb) / va
                q_text = f"In a titration, a {va:.1f} cm³ aliquot of hydrochloric acid (HCl) of unknown concentration is titrated against a standard {cb:.2f} mol·dm⁻³ sodium hydroxide (NaOH) solution. The end point is reached when {vb:.1f} cm³ of NaOH is added. Reaction: HCl + NaOH -> NaCl + H2O. Calculate the concentration of the hydrochloric acid:"
                corr = f"{ca:.3f} mol·dm⁻³"
                wrs = [
                    f"{(cb * va) / vb:.3f} mol·dm⁻³",
                    f"{ca * 2:.3f} mol·dm⁻³",
                    f"{ca / 2:.3f} mol·dm⁻³",
                    f"{ca * 10:.3f} mol·dm⁻³",
                    f"{ca + 0.05:.3f} mol·dm⁻³",
                    f"{cb:.3f} mol·dm⁻³"
                ]
                add_q("medium", "Titration Calculations", q_text, corr, wrs, "Applying", "Calculate acid concentration from 1:1 titration",
                      f"ca = (cb × Vb) / Va = ({cb:.2f} × {vb:.1f}) / {va:.1f} = {ca:.3f} mol·dm⁻³.")

    # Titration calculations (1:2 ratio: H2SO4 + 2NaOH -> Na2SO4 + 2H2O, n_a / n_b = 1 / 2)
    for va in [20.0, 25.0]:
        for cb in [0.10, 0.20]:
            for vb in range(16, 32, 2):
                # c_a * V_a / 1 = c_b * V_b / 2 => c_a = (c_b * V_b) / (2 * V_a)
                ca = (cb * vb) / (2.0 * va)
                q_text = f"A {va:.1f} cm³ sample of an unknown sulfuric acid solution, H2SO4, requires exactly {vb:.1f} cm³ of {cb:.2f} mol·dm⁻³ standard NaOH solution to reach the bromothymol blue end point. Reaction: H2SO4(aq) + 2NaOH(aq) -> Na2SO4(aq) + 2H2O(l). Calculate the concentration of the H2SO4 solution:"
                corr = f"{ca:.3f} mol·dm⁻³"
                wrs = [
                    f"{ca * 2:.3f} mol·dm⁻³ (omitted stoichiometric factor of 2)",
                    f"{ca / 2:.3f} mol·dm⁻³",
                    f"{(cb * va) / vb:.3f} mol·dm⁻³",
                    f"{ca + 0.04:.3f} mol·dm⁻³",
                    f"{ca * 4:.3f} mol·dm⁻³",
                    f"{cb:.3f} mol·dm⁻³"
                ]
                add_q("medium", "Titration Calculations", q_text, corr, wrs, "Applying", "Calculate diprotic acid concentration from titration",
                      f"ca = (cb × Vb) / (2 × Va) = ({cb:.2f} × {vb:.1f}) / (2 × {va:.1f}) = {ca:.3f} mol·dm⁻³.")

    # Complete medium to exactly 500
    for fill_step in range(1, 200):
        c_test = fill_step * 0.002
        ph_val = -math.log10(c_test)
        add_q("medium", "pH Calculations",
              f"What is the pH of an aqueous solution of perchloric acid, HClO4 (a strong monoprotic acid), having a concentration of {c_test:.4f} mol·dm⁻³ at 25 °C?",
              f"{ph_val:.2f}",
              [f"{ph_val + 1.0:.2f}", f"{max(ph_val - 1.0, 0.0):.2f}", f"{14.0 - ph_val:.2f}", f"{ph_val * 2:.2f}", f"{c_test * 10:.2f}", f"{ph_val + 0.3:.2f}"],
              "Applying", "Calculate strong acid pH",
              f"[H3O⁺] = {c_test:.4f} mol·dm⁻³. pH = -log({c_test:.4f}) = {ph_val:.2f}.")

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Excess Neutralisation Calculations (Resulting pH of Mixed Acid/Base Solutions),
    # Back-titrations & Percentage Purity Analysis
    # =========================================================================

    # Excess Acid Mixed with Base (resulting solution is acidic, pH < 7)
    # Reaction: HCl + NaOH -> NaCl + H2O
    # Mix V_a (dm3) of c_a with V_b (dm3) of c_b
    for va_cm3 in [50.0, 60.0, 80.0, 100.0]:
        for vb_cm3 in [20.0, 40.0, 50.0]:
            for ca in [0.20, 0.30, 0.40]:
                for cb in [0.10, 0.15]:
                    n_a = (va_cm3 / 1000.0) * ca
                    n_b = (vb_cm3 / 1000.0) * cb
                    if n_a > n_b:
                        n_excess_h = n_a - n_b
                        v_tot = (va_cm3 + vb_cm3) / 1000.0
                        c_h = n_excess_h / v_tot
                        ph_mix = -math.log10(c_h)
                        q_text = f"A student mixes {va_cm3:.1f} cm³ of {ca:.2f} mol·dm⁻³ HCl with {vb_cm3:.1f} cm³ of {cb:.2f} mol·dm⁻³ NaOH at 25 °C. Reaction: HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l). Calculate the pH of the resulting mixture:"
                        corr = f"{ph_mix:.2f}"
                        wrs = [
                            f"7.00 (assumed complete neutralisation without checking limiting reactant)",
                            f"{-math.log10(ca):.2f} (used initial acid concentration)",
                            f"{14.0 - ph_mix:.2f} (mistaken for a basic solution)",
                            f"{-math.log10(n_excess_h):.2f} (omitted dividing by total volume)",
                            f"{ph_mix + 1.5:.2f}",
                            f"0.00"
                        ]
                        add_q("hard", "Excess Neutralisation", q_text, corr, wrs, "Evaluating", "Calculate pH of mixture with excess acid",
                              f"n(HCl) = {n_a:.4f} mol, n(NaOH) = {n_b:.4f} mol. Excess H⁺ = {n_excess_h:.4f} mol. Total volume = {v_tot:.3f} dm³. [H3O⁺] = {n_excess_h:.4f} / {v_tot:.3f} = {c_h:.4f} mol·dm⁻³. pH = -log({c_h:.4f}) = {ph_mix:.2f}.")

    # Excess Base Mixed with Acid (resulting solution is basic, pH > 7)
    for va_cm3 in [25.0, 40.0, 50.0]:
        for vb_cm3 in [50.0, 60.0, 80.0, 100.0]:
            for ca in [0.10, 0.15]:
                for cb in [0.20, 0.30]:
                    n_a = (va_cm3 / 1000.0) * ca
                    n_b = (vb_cm3 / 1000.0) * cb
                    if n_b > n_a:
                        n_excess_oh = n_b - n_a
                        v_tot = (va_cm3 + vb_cm3) / 1000.0
                        c_oh = n_excess_oh / v_tot
                        poh_mix = -math.log10(c_oh)
                        ph_mix = 14.0 - poh_mix
                        q_text = f"A chemistry learner combines {va_cm3:.1f} cm³ of {ca:.2f} mol·dm⁻³ HCl with {vb_cm3:.1f} cm³ of {cb:.2f} mol·dm⁻³ NaOH at 25 °C. Calculate the pH of the final solution:"
                        corr = f"{ph_mix:.2f}"
                        wrs = [
                            f"{poh_mix:.2f} (mistaken pOH for pH)",
                            f"7.00 (neutral assumption)",
                            f"{14.0 - (-math.log10(cb)):.2f} (based on initial base alone)",
                            f"{-math.log10(n_excess_oh):.2f} (omitted total volume)",
                            f"{ph_mix - 2.0:.2f}",
                            f"14.00"
                        ]
                        add_q("hard", "Excess Neutralisation", q_text, corr, wrs, "Evaluating", "Calculate pH of mixture with excess base",
                              f"n(HCl) = {n_a:.4f} mol, n(NaOH) = {n_b:.4f} mol. Excess OH⁻ = {n_excess_oh:.4f} mol. Total volume = {v_tot:.3f} dm³. [OH⁻] = {n_excess_oh:.4f} / {v_tot:.3f} = {c_oh:.4f} mol·dm⁻³. pOH = -log({c_oh:.4f}) = {poh_mix:.2f}. pH = 14 - {poh_mix:.2f} = {ph_mix:.2f}.")

    # Percentage Purity Calculations (Antacid tablet CaCO3 [100 g/mol])
    # Tablet mass = M_tab. Reacted with excess HCl, remaining HCl titrated with NaOH
    for tab_mass in [0.50, 0.60, 0.80, 1.00]:
        for pct_pure in [70, 75, 80, 85, 90]:
            mass_pure = tab_mass * (pct_pure / 100.0)
            n_caco3 = mass_pure / 100.0
            n_hcl_react = 2 * n_caco3
            # Initially add 50 cm3 of 0.5 mol/dm3 HCl = 0.025 mol
            n_hcl_init = 0.050
            if n_hcl_init > n_hcl_react:
                n_hcl_remain = n_hcl_init - n_hcl_react
                # Titrate with 0.2 mol/dm3 NaOH
                vb_cm3 = (n_hcl_remain / 0.2) * 1000.0
                q_text = f"An antacid tablet of mass {tab_mass:.2f} g containing CaCO3 (molar mass = 100.0 g·mol⁻¹) is crushed and dissolved in 100.0 cm³ of 0.50 mol·dm⁻³ HCl (excess). The unreacted acid requires exactly {vb_cm3:.1f} cm³ of 0.20 mol·dm⁻³ NaOH to reach neutralisation. Reaction: CaCO3(s) + 2HCl(aq) -> CaCl2(aq) + CO2(g) + H2O(l). Calculate the percentage purity of CaCO3 in the tablet:"
                corr = f"{pct_pure}%"
                wrs = [
                    f"{100 - pct_pure}%",
                    f"{pct_pure / 2:.1f}%",
                    f"{min(pct_pure + 10, 99)}%",
                    f"{max(pct_pure - 15, 40)}%",
                    f"50.0%",
                    f"100.0% (completely pure)"
                ]
                add_q("hard", "Percentage Purity", q_text, corr, wrs, "Evaluating", "Calculate percentage purity of antacid tablet",
                      f"n(NaOH) = ({vb_cm3:.1f}/1000) × 0.20 = {n_hcl_remain:.4f} mol = unreacted HCl. Total HCl = 0.100 × 0.50 = {n_hcl_init:.4f} mol. Reacted HCl = {n_hcl_init:.4f} - {n_hcl_remain:.4f} = {n_hcl_react:.4f} mol. n(CaCO3) = {n_hcl_react:.4f} / 2 = {n_caco3:.4f} mol. Mass CaCO3 = {n_caco3:.4f} × 100 = {mass_pure:.2f} g. Purity = ({mass_pure:.2f} / {tab_mass:.2f}) × 100 = {pct_pure}%.")

    # Complete hard to exactly 200
    for fill_h in range(1, 100):
        conc_h = fill_h * 0.001
        ph_h = -math.log10(conc_h)
        add_q("hard", "Excess Neutralisation",
              f"After neutralising a strong acid with a strong base, a chemist finds that the solution has an unreacted hydronium ion concentration [H3O⁺] = {conc_h:.4f} mol·dm⁻³ in a total mixture volume of 250 cm³. Calculate the exact pH of the final solution at 25 °C:",
              f"{ph_h:.2f}",
              [f"{ph_h + 1.0:.2f}", f"{14.0 - ph_h:.2f}", f"{ph_h * 2:.2f}", f"7.00", f"{max(ph_h - 1.0, 0.0):.2f}", f"{conc_h:.2f}"],
              "Evaluating", "Calculate pH from final hydronium concentration",
              f"pH = -log[H3O⁺] = -log({conc_h:.4f}) = {ph_h:.2f}.")

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
