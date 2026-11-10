import json
import os

def build_electrochemical_reactions():
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
        qid = f"PS_P2_ELEC_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Paper 2: Electrochemical Reactions",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "topic": "Paper 2: Electrochemical Reactions",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Oxidation Numbers, Cell Components, Standard Conditions
    # =========================================================================

    core_definitions = [
        ("Oxidation",
         "The loss of electrons by a chemical species (resulting in an increase in oxidation number).",
         ["The gain of electrons by a chemical species",
          "A reaction that consumes oxygen from the atmosphere exclusively",
          "The migration of anions toward the cathode",
          "The transformation of electrical energy into chemical potential energy",
          "The precipitation of a solid metal onto an electrode",
          "A process where the oxidation number decreases"],
         "Oxidation is defined in terms of electron transfer as the loss of electrons (OIL: Oxidation Is Loss)."),

        ("Reduction",
         "The gain of electrons by a chemical species (resulting in a decrease in oxidation number).",
         ["The loss of electrons by a chemical species",
          "The loss of mass by a metal anode during electrolysis",
          "The formation of gaseous products at the positive electrode",
          "The decrease in volume of a gas at constant pressure",
          "A process that produces electrical current spontaneously",
          "The oxidation number increasing from negative to positive"],
         "Reduction is defined as the gain of electrons (RIG: Reduction Is Gain)."),

        ("Oxidising Agent",
         "A substance that accepts electrons and is itself reduced in the process.",
         ["A substance that donates electrons and is itself oxidised",
          "An inert platinum electrode that conducts electricity",
          "A salt bridge electrolyte that supplies mobile spectator ions",
          "A chemical species that always loses protons",
          "A substance that increases the activation energy of redox",
          "A metal that dissolves at the anode"],
         "An oxidising agent causes another substance to be oxidised by accepting electrons from it, thereby undergoing reduction itself."),

        ("Reducing Agent",
         "A substance that donates electrons and is itself oxidised in the process.",
         ["A substance that accepts electrons and is itself reduced",
          "A porous membrane that blocks cation movement",
          "The positive terminal of a galvanic cell",
          "A solvent that absorbs heat during electrolysis",
          "A substance whose oxidation number decreases during reaction",
          "An inert gas blanket used to shield reactions"],
         "A reducing agent causes another substance to be reduced by donating electrons to it, thereby undergoing oxidation itself."),

        ("Anode",
         "The electrode where oxidation takes place.",
         ["The electrode where reduction takes place",
          "The electrode that always attracts cations from solution",
          "The positive terminal in a galvanic cell",
          "The negative terminal in an electrolytic cell",
          "The glass tube containing potassium nitrate",
          "The electrode where metal ions always plate out"],
         "By international definition (and mnemonic 'An Ox'), oxidation ALWAYS occurs at the anode in both galvanic and electrolytic cells."),

        ("Cathode",
         "The electrode where reduction takes place.",
         ["The electrode where oxidation takes place",
          "The negative terminal in a galvanic cell",
          "The positive terminal in an electrolytic cell",
          "The electrode that always loses mass by dissolving",
          "The porous barrier separating two half-cells",
          "The source of electrons in an external battery"],
         "By international definition (and mnemonic 'Red Cat'), reduction ALWAYS occurs at the cathode in both galvanic and electrolytic cells."),

        ("Electrolyte",
         "A solution or molten liquid that conducts electricity through the movement of freely mobile ions.",
         ["A solid metal wire that conducts electricity via delocalised electrons",
          "A non-polar organic liquid such as pure benzene",
          "A substance that prevents any chemical reaction from occurring",
          "The external voltmeter connected across two electrodes",
          "A dry powder consisting of neutral covalent molecules",
          "A chemical indicator that measures cell potential"],
         "An electrolyte is an ionic liquid or aqueous solution containing freely mobile ions that conduct electric current."),

        ("Galvanic (Voltaic) Cell",
         "An electrochemical cell that converts chemical potential energy into electrical energy through a spontaneous redox reaction.",
         ["A cell that uses electrical energy from an external power source to drive a non-spontaneous chemical reaction",
          "A cell where electrical current is used to electroplate a metal",
          "A cell operating under non-standard conditions exclusively",
          "An apparatus used to extract aluminium from molten cryolite",
          "A cell where oxidation occurs at the cathode",
          "A storage battery that has completely discharged to 0 V"],
         "A galvanic cell uses a spontaneous chemical reaction (exothermic, positive E°_cell) to produce an electric current."),

        ("Electrolytic Cell",
         "An electrochemical cell that uses electrical energy from an external source to drive a non-spontaneous chemical reaction.",
         ["A cell that converts chemical potential energy into electrical energy spontaneously",
          "A battery that powers a flashlight during discharge",
          "A device that measures standard electrode potential against SHE",
          "A cell that operates without any electrodes or ions",
          "A spontaneous cell where the anode is the positive terminal",
          "A cell that has reached dynamic chemical equilibrium"],
         "An electrolytic cell requires an external power supply to force non-spontaneous redox reactions (endothermic) to occur."),

        ("Salt Bridge",
         "A U-tube containing an inert ionic electrolyte (such as KNO3 or KCl) that completes the internal circuit and maintains electrical neutrality in half-cells by ion migration.",
         ["A copper wire that carries electrons between two beakers",
          "A semipermeable barrier that allows metal atoms to dissolve",
          "A power supply that provides direct electrical current",
          "A platinum plate that absorbs hydrogen gas",
          "A glass rod used to stir electrolyte solutions",
          "An insulator that prevents any ions from moving"],
         "The salt bridge completes the electrical circuit and maintains electrical neutrality: anions migrate to the anode half-cell, cations migrate to the cathode half-cell."),

        ("Standard Hydrogen Electrode (SHE)",
         "A reference electrode consisting of platinum immersed in 1.0 mol·dm⁻³ H⁺(aq) with H2(g) bubbled at 101.3 kPa and 298 K, assigned an electrode potential of exactly 0.00 V.",
         ["An electrode made of pure sodium metal with a potential of +1.00 V",
          "A standard copper rod immersed in copper sulfate at room temperature",
          "A battery terminal operating at zero Kelvin",
          "A dry cell that supplies exactly 1.50 V of electric potential",
          "A carbon rod immersed in sulfuric acid with no defined potential",
          "An electrode that only functions in basic solutions"],
         "The Standard Hydrogen Electrode (SHE) is the universal reference electrode against which all other reduction potentials are measured; its standard potential is defined as 0.00 V.")
    ]

    stems = [
        "In CAPS Grade 12 Physical Sciences, how is the term '{}' defined?",
        "According to the official exam guidelines, '{}' refers to:",
        "Identify the correct scientific definition for '{}':",
        "Which statement provides the precise definition of '{}' in electrochemistry?",
        "When an examiner asks for the definition of '{}', which statement earns full marks?"
    ]

    for term, corr, wrs, expl in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr, wrs, "Remembering", "Define electrochemical concept", expl)

    # Standard conditions specifications
    std_conditions = [
        ("Temperature", "298 K (or 25 °C)", ["273 K (0 °C)", "100 °C (373 K)", "300 K", "0 K", "25 K", "100 K"]),
        ("Concentration of electrolyte solutions", "1.0 mol·dm⁻³", ["0.1 mol·dm⁻³", "2.0 mol·dm⁻³", "10.0 mol·dm⁻³", "0.5 mol·dm⁻³", "100 mol·dm⁻³", "0.01 mol·dm⁻³"]),
        ("Pressure of gaseous reactants/products", "101.3 kPa (or 1 atmosphere)", ["1.0 kPa", "1000 kPa", "0.0 kPa", "202.6 kPa", "10.13 kPa", "50.0 kPa"])
    ]

    for cond_type, val, wrs in std_conditions:
        add_q("easy", "Standard Conditions",
              f"What is the standard condition specified for **{cond_type.lower()}** when measuring standard electrode potentials (E°)?",
              val, wrs, "Remembering", "Recall standard electrochemical condition",
              f"Standard {cond_type.lower()} in electrochemistry is {val}.")

    # Galvanic vs Electrolytic Cell Comparisons
    cell_comparisons = [
        ("Energy conversion in a Galvanic cell", "Chemical potential energy is converted into electrical energy.",
         ["Electrical energy is converted into chemical potential energy.", "Thermal energy is converted directly into nuclear energy.", "Mechanical energy is converted into chemical energy.", "Light energy is converted into voltage.", "Potential energy is destroyed.", "Kinetic energy is stored as pressure."]),
        ("Energy conversion in an Electrolytic cell", "Electrical energy from an external source is converted into chemical potential energy.",
         ["Chemical potential energy is converted into electrical energy spontaneously.", "Nuclear energy is converted into heat.", "Gravitational energy is converted into voltage.", "Thermal energy is converted into kinetic energy.", "No energy conversion takes place.", "Chemical bonds are converted into light exclusively."]),
        ("Polarity of the Anode in a Galvanic cell", "Negative (-), because electrons are released at the anode by oxidation.",
         ["Positive (+), because it attracts anions.", "Neutral (0), because charges balance.", "Alternating between positive and negative.", "The same polarity as the cathode.", "Positive (+), because it is connected to a battery.", "Undefined until current stops flowing."]),
        ("Polarity of the Cathode in a Galvanic cell", "Positive (+), because electrons from the external circuit enter to reduce cations.",
         ["Negative (-), because electrons gather there.", "Neutral (0), because ions neutralise it.", "Variable depending on the voltmeter.", "Negative (-), because it repels anions.", "Zero, because it is an inert electrode.", "Alternating at 50 Hz."]),
        ("Polarity of the Anode in an Electrolytic cell", "Positive (+), because it is connected to the positive terminal of the external DC power source.",
         ["Negative (-), because oxidation occurs there.", "Neutral (0), because ions discharge.", "Negative (-), because it receives electrons from the battery.", "Alternating (+/-) continuously.", "Zero, because it is grounded.", "Positive (+), because reduction happens there."]),
        ("Polarity of the Cathode in an Electrolytic cell", "Negative (-), because it is connected to the negative terminal of the external DC power source.",
         ["Positive (+), because reduction occurs there.", "Neutral (0), because metal plates on it.", "Positive (+), because it loses electrons.", "Undefined until electrolysis finishes.", "Zero, because no current enters.", "Negative (-), because it donates electrons to the battery."]),
        ("Direction of electron flow in the external circuit", "From the ANODE to the CATHODE in both galvanic and electrolytic cells.",
         ["From the cathode to the anode in both cells.", "From anode to cathode in galvanic, but cathode to anode in electrolytic.", "Through the salt bridge from cathode to anode.", "From the positive terminal to the negative terminal in galvanic.", "Bidirectional alternating current.", "Electrons do not flow in the external circuit."]),
        ("Movement of ions in the salt bridge of a Galvanic cell", "Anions migrate toward the ANODE half-cell; cations migrate toward the CATHODE half-cell.",
         ["Cations migrate to the anode; anions migrate to the cathode.", "Both cations and anions migrate exclusively to the cathode.", "Both cations and anions migrate exclusively to the anode.", "Ions remain stationary while electrons pass through the bridge.", "Electrons flow through the salt bridge.", "Ions evaporate into the surrounding air."])
    ]

    for comp_item, corr, wrs in cell_comparisons:
        add_q("easy", "Cell Comparisons",
              f"What is the correct principle regarding: **{comp_item}**?",
              corr, wrs, "Understanding", "Compare galvanic and electrolytic cells", corr)

    # Oxidation numbers determination for species
    ox_species = [
        ("H in H2O", "+1", ["-1", "0", "+2", "-2", "+3", "-3"]),
        ("O in H2O", "-2", ["+2", "-1", "0", "+1", "-4", "+4"]),
        ("O in H2O2 (hydrogen peroxide)", "-1", ["-2", "+2", "0", "+1", "-3", "+4"]),
        ("Cl in Cl2(g)", "0 (pure elemental state)", ["-1", "+1", "+3", "+5", "+7", "-2"]),
        ("Fe in Fe²⁺", "+2", ["+3", "0", "+1", "-2", "+4", "-1"]),
        ("Fe in Fe³⁺", "+3", ["+2", "0", "+1", "-3", "+4", "-1"]),
        ("S in SO4²⁻", "+6", ["+4", "-2", "+2", "0", "+7", "-6"]),
        ("S in SO2", "+4", ["+6", "-2", "+2", "0", "+3", "-4"]),
        ("S in H2S", "-2", ["+2", "+4", "+6", "0", "-1", "+1"]),
        ("S in pure rhombic S8", "0", ["-2", "+2", "+4", "+6", "-1", "+1"]),
        ("N in NO3⁻", "+5", ["+3", "-3", "+4", "+2", "+1", "0"]),
        ("N in NO2", "+4", ["+2", "+3", "+5", "-3", "0", "+1"]),
        ("N in NO", "+2", ["+4", "+3", "+1", "-3", "0", "+5"]),
        ("N in NH3", "-3", ["+3", "+5", "-1", "0", "+1", "-5"]),
        ("N in NH4⁺", "-3", ["+3", "+5", "-1", "+1", "0", "-4"]),
        ("C in CO2", "+4", ["+2", "-4", "-2", "0", "+6", "-1"]),
        ("C in CO", "+2", ["+4", "-2", "0", "-4", "+1", "+3"]),
        ("C in CH4", "-4", ["+4", "-2", "+2", "0", "-1", "+1"]),
        ("Mn in MnO4⁻ (permanganate)", "+7", ["+2", "+4", "+6", "+3", "0", "-1"]),
        ("Mn in MnO2", "+4", ["+2", "+7", "+6", "+3", "0", "-2"]),
        ("Mn in Mn²⁺", "+2", ["+4", "+7", "+3", "0", "-2", "+1"]),
        ("Cr in Cr2O7²⁻ (dichromate)", "+6", ["+3", "+7", "+4", "+2", "0", "-2"]),
        ("Cr in CrO4²⁻ (chromate)", "+6", ["+3", "+4", "+2", "+7", "0", "-1"]),
        ("Cr in Cr³⁺", "+3", ["+6", "+2", "0", "+4", "-3", "+1"]),
        ("Cu in Cu(s)", "0 (pure elemental metal)", ["+2", "+1", "-2", "+3", "-1", "+4"]),
        ("Cu in CuSO4", "+2", ["+1", "0", "-2", "+3", "+4", "-1"]),
        ("Cl in KClO3", "+5", ["-1", "+1", "+3", "+7", "0", "-2"]),
        ("Cl in HClO", "+1", ["-1", "+3", "+5", "+7", "0", "-2"]),
        ("P in H3PO4", "+5", ["+3", "-3", "+4", "+2", "0", "-1"]),
        ("H in NaH (sodium hydride)", "-1", ["+1", "0", "+2", "-2", "+3", "-3"])
    ]

    for spec, corr_ox, wrs in ox_species:
        add_q("easy", "Oxidation Numbers",
              f"What is the oxidation number of **{spec}**?",
              corr_ox, wrs, "Understanding", "Determine oxidation state",
              f"The oxidation state of {spec} is {corr_ox}.")

    # Standard Reduction Potentials from CAPS Table 4
    table4_species = [
        ("F2(g) + 2e⁻ ⇌ 2F⁻", "+2.87 V", "Fluorine gas / Fluoride ion", "Strongest oxidising agent on Table 4"),
        ("Co³⁺ + e⁻ ⇌ Co²⁺", "+1.81 V", "Cobalt(III) / Cobalt(II)", "Powerful oxidising couple"),
        ("Au³⁺ + 3e⁻ ⇌ Au(s)", "+1.50 V", "Gold(III) / Gold metal", "Noble metal reduction"),
        ("Cl2(g) + 2e⁻ ⇌ 2Cl⁻", "+1.36 V", "Chlorine gas / Chloride ion", "Strong non-metal oxidising agent"),
        ("Cr2O7²⁻ + 14H⁺ + 6e⁻ ⇌ 2Cr³⁺ + 7H2O", "+1.33 V", "Acidified dichromate", "Common laboratory oxidising agent"),
        ("O2(g) + 4H⁺ + 4e⁻ ⇌ 2H2O", "+1.23 V", "Oxygen in acidic medium", "Acidic oxygen reduction"),
        ("Br2(l) + 2e⁻ ⇌ 2Br⁻", "+1.07 V", "Bromine liquid / Bromide ion", "Halogen oxidising agent"),
        ("NO3⁻ + 4H⁺ + 3e⁻ ⇌ NO(g) + 2H2O", "+0.96 V", "Nitrate in acidic medium", "Nitrate reduction"),
        ("Ag⁺ + e⁻ ⇌ Ag(s)", "+0.80 V", "Silver ion / Silver metal", "Precious metal reduction"),
        ("Fe³⁺ + e⁻ ⇌ Fe²⁺", "+0.77 V", "Iron(III) / Iron(II)", "Iron redox couple"),
        ("I2(s) + 2e⁻ ⇌ 2I⁻", "+0.54 V", "Iodine solid / Iodide ion", "Mild non-metal oxidising agent"),
        ("Cu²⁺ + 2e⁻ ⇌ Cu(s)", "+0.34 V", "Copper(II) / Copper metal", "Cathode half-reaction in Daniell cell"),
        ("SO4²⁻ + 4H⁺ + 2e⁻ ⇌ SO2(g) + 2H2O", "+0.17 V", "Sulfate in acid", "Sulfate reduction"),
        ("Cu⁺ + e⁻ ⇌ Cu(s)", "+0.52 V", "Copper(I) / Copper metal", "Cuprous reduction"),
        ("2H⁺ + 2e⁻ ⇌ H2(g)", "0.00 V", "Standard Hydrogen Electrode (SHE)", "Universal zero reference standard"),
        ("Pb²⁺ + 2e⁻ ⇌ Pb(s)", "-0.13 V", "Lead(II) / Lead metal", "Standard lead electrode"),
        ("Sn²⁺ + 2e⁻ ⇌ Sn(s)", "-0.14 V", "Tin(II) / Tin metal", "Standard tin electrode"),
        ("Ni²⁺ + 2e⁻ ⇌ Ni(s)", "-0.25 V", "Nickel(II) / Nickel metal", "Standard nickel electrode"),
        ("Co²⁺ + 2e⁻ ⇌ Co(s)", "-0.28 V", "Cobalt(II) / Cobalt metal", "Standard cobalt electrode"),
        ("Fe²⁺ + 2e⁻ ⇌ Fe(s)", "-0.44 V", "Iron(II) / Iron metal", "Iron oxidation/reduction"),
        ("Cr³⁺ + 3e⁻ ⇌ Cr(s)", "-0.74 V", "Chromium(III) / Chromium metal", "Chromium electrode"),
        ("Zn²⁺ + 2e⁻ ⇌ Zn(s)", "-0.76 V", "Zinc(II) / Zinc metal", "Anode half-reaction in Daniell cell"),
        ("Mn²⁺ + 2e⁻ ⇌ Mn(s)", "-1.18 V", "Manganese(II) / Manganese metal", "Manganese electrode"),
        ("Al³⁺ + 3e⁻ ⇌ Al(s)", "-1.66 V", "Aluminium(III) / Aluminium metal", "Active metal reducing agent"),
        ("Mg²⁺ + 2e⁻ ⇌ Mg(s)", "-2.37 V", "Magnesium(II) / Magnesium metal", "Strong alkaline earth reducing metal"),
        ("Na⁺ + e⁻ ⇌ Na(s)", "-2.71 V", "Sodium(I) / Sodium metal", "Highly active alkali metal"),
        ("Ca²⁺ + 2e⁻ ⇌ Ca(s)", "-2.87 V", "Calcium(II) / Calcium metal", "Highly active alkaline earth metal"),
        ("Ba²⁺ + 2e⁻ ⇌ Ba(s)", "-2.90 V", "Barium(II) / Barium metal", "Active alkaline earth reducing agent"),
        ("K⁺ + e⁻ ⇌ K(s)", "-2.93 V", "Potassium(I) / Potassium metal", "Very strong reducing metal"),
        ("Li⁺ + e⁻ ⇌ Li(s)", "-3.04 V", "Lithium(I) / Lithium metal", "Strongest reducing agent on Table 4")
    ]

    for half_eq, e_val, couple_name, note in table4_species:
        # Standard reduction potential lookup
        wrs = [
            f"-{e_val.replace('+', '').replace('-', '')} V" if '+' in e_val else f"+{e_val.replace('-', '')} V",
            "0.00 V",
            "+1.10 V",
            "-0.76 V",
            "+0.34 V",
            "-3.04 V"
        ]
        add_q("easy", "Standard Potentials",
              f"According to Table 4 (Standard Reduction Potentials), what is the standard reduction potential (E°) for the half-reaction: **{half_eq}**?",
              e_val, wrs, "Remembering", "Recall standard reduction potential",
              f"For the couple {couple_name} ({half_eq}), E° = {e_val}. ({note}).")

    # Coupling standard half-cells with SHE (Standard Hydrogen Electrode)
    for half_eq, e_val, couple_name, note in table4_species:
        val_float = float(e_val.replace(" V", "").replace("+", ""))
        if abs(val_float) < 0.01:
            continue
        if val_float > 0:
            # Metal is cathode, SHE is anode
            cell_emf = f"{val_float:.2f} V"
            q_text = f"A standard galvanic cell is assembled using a {couple_name} half-cell (E° = {e_val}) and a Standard Hydrogen Electrode (SHE, E° = 0.00 V). What is the standard cell potential (E°cell) of this galvanic cell?"
            expl = f"Since E°({couple_name}) = {e_val} is greater than 0.00 V, the {couple_name} electrode acts as the cathode and SHE acts as the anode. E°cell = E°cathode - E°anode = {val_float:.2f} - 0.00 = +{val_float:.2f} V."
            anode_id = "Standard Hydrogen Electrode (SHE)"
            cathode_id = f"{couple_name} half-cell"
        else:
            # Metal is anode, SHE is cathode
            cell_emf = f"{abs(val_float):.2f} V"
            q_text = f"A standard galvanic cell is assembled using a {couple_name} half-cell (E° = {e_val}) and a Standard Hydrogen Electrode (SHE, E° = 0.00 V). What is the standard cell potential (E°cell) of this galvanic cell?"
            expl = f"Since E°({couple_name}) = {e_val} is less than 0.00 V, the {couple_name} electrode acts as the anode (undergoing oxidation) and SHE acts as the cathode. E°cell = E°cathode - E°anode = 0.00 - ({val_float:.2f}) = +{abs(val_float):.2f} V."
            anode_id = f"{couple_name} half-cell"
            cathode_id = "Standard Hydrogen Electrode (SHE)"

        wrs = [
            f"-{cell_emf}",
            f"{float(cell_emf.replace(' V', '')) * 2:.2f} V",
            f"{float(cell_emf.replace(' V', '')) / 2:.2f} V",
            "0.00 V",
            f"{float(cell_emf.replace(' V', '')) + 1.10:.2f} V",
            f"{abs(float(cell_emf.replace(' V', '')) - 0.76):.2f} V"
        ]
        add_q("easy", "Standard Potentials", q_text, cell_emf, wrs, "Applying", "Calculate standard galvanic EMF with SHE", expl)

        # Anode identification with SHE
        q_anode = f"In a standard galvanic cell constructed from a {couple_name} half-cell (E° = {e_val}) and a Standard Hydrogen Electrode (SHE, E° = 0.00 V), which half-cell functions as the ANODE?"
        wrs_anode = [cathode_id, "Both half-cells simultaneously", "Neither, because current cannot flow with SHE", "Platinum wire outside the solution", "The voltmeter terminal", "The porous salt bridge"]
        add_q("easy", "Cell Components", q_anode, anode_id, wrs_anode, "Understanding", "Identify anode when coupled with SHE",
              f"The half-cell with the lower (more negative) reduction potential undergoes oxidation and functions as the anode. Here, that is {anode_id}.")

    # Function of salt bridge and SHE components
    extra_easy_concepts = [
        ("What is the function of the platinum (Pt) electrode in a Standard Hydrogen Electrode (SHE)?",
         "It acts as an inert electrical conductor and provides a catalytic metal surface for electron transfer between H⁺(aq) and H2(g).",
         ["It reacts with hydrogen gas to form platinum hydride precipitate",
          "It oxidises spontaneously to platinum(IV) ions to generate voltage",
          "It maintains the pH of the solution at exactly 7.00",
          "It dissolves to release electrons directly into the voltmeter",
          "It prevents hydrogen gas from bubbling out of the tube",
          "It replaces the salt bridge in the internal circuit"],
         "Platinum is inert (does not react) and provides an electron-conducting surface for the H2(g) / H⁺(aq) redox equilibrium."),

        ("Why is potassium nitrate (KNO3) widely used as the electrolyte in a salt bridge?",
         "K⁺ and NO3⁻ ions do not react or form insoluble precipitates with common half-cell electrolytes, and have similar ionic mobilities.",
         ["KNO3 reacts vigorously with electrodes to supply extra voltage",
          "KNO3 completely stops ions from migrating between beakers",
          "KNO3 converts the galvanic cell into an electrolytic cell",
          "KNO3 evaporates quickly to create a vacuum seal",
          "Potassium metal plates out onto the glass walls of the bridge",
          "Nitrate ions decompose into nitrogen gas to power the circuit"],
         "KNO3 is soluble, neutral, and neither potassium cations nor nitrate anions form precipitates with standard metal ions (like Pb²⁺, Ag⁺, Cu²⁺, Zn²⁺)."),

        ("What happens to the reading on the voltmeter of a functioning galvanic cell if the salt bridge is removed?",
         "The voltmeter reading immediately drops to 0.00 V because the internal circuit is broken and charge accumulates.",
         ["The voltmeter reading doubles because resistance decreases",
          "The voltmeter reading stays constant indefinitely",
          "The cell reverses polarity and displays a negative voltage",
          "The voltmeter short-circuits and current spikes to infinity",
          "The electrodes begin to dissolve much faster",
          "The cathode starts to oxidise spontaneously"],
         "Removing the salt bridge breaks the internal electrical circuit; charge cannot be neutralized, current ceases immediately, and voltage drops to 0 V."),

        ("Which statement correctly describes the movement of ions through the salt bridge in an operating Zn-Cu galvanic cell?",
         "Nitrate anions (NO3⁻) migrate into the zinc anode half-cell; potassium cations (K⁺) migrate into the copper cathode half-cell.",
         ["Potassium cations (K⁺) migrate to the anode; nitrate anions (NO3⁻) migrate to the cathode.",
          "Both cations and anions migrate exclusively into the cathode beaker.",
          "Both cations and anions migrate exclusively into the anode beaker.",
          "Electrons travel through the salt bridge from anode to cathode.",
          "No ions move; only water molecules diffuse through the agar gel.",
          "Zinc ions travel through the salt bridge to deposit onto the copper electrode."],
         "Anions migrate to the anode to neutralize accumulating positive Zn²⁺ ions; cations migrate to the cathode to replace consumed Cu²⁺ ions."),

        ("In any electrochemical cell (galvanic or electrolytic), what fundamental reaction ALWAYS occurs at the CATHODE?",
         "Reduction (gain of electrons).",
         ["Oxidation (loss of electrons)",
          "Dissolution of the solid electrode into cations",
          "Neutralization of acid by base",
          "Hydrolysis of water into hydronium ions",
          "Precipitation of insoluble salt bridges",
          "Esterification of organic electrolytes"],
         "The mnemonic 'Red Cat' reminds us that REDuction always occurs at the CAThode.")
    ]

    for q_t, c_a, w_p, exp in extra_easy_concepts:
        add_q("easy", "Cell Components", q_t, c_a, w_p, "Understanding", "Understand electrochemical cell components", exp)

    # Fill easy to exactly 300 with diverse reduction potential comparisons from Table 4
    for i, (half1, e1, name1, _) in enumerate(table4_species):
        for j, (half2, e2, name2, _) in enumerate(table4_species):
            if counts["easy"] >= 300:
                break
            if i >= j:
                continue
            v1 = float(e1.replace(" V", "").replace("+", ""))
            v2 = float(e2.replace(" V", "").replace("+", ""))
            if abs(v1 - v2) < 0.05:
                continue
            # Higher E° is stronger oxidising agent
            if v1 > v2:
                stronger_ox = name1
                weaker_ox = name2
                high_v, low_v = e1, e2
            else:
                stronger_ox = name2
                weaker_ox = name1
                high_v, low_v = e2, e1

            q_text = f"Comparing {name1} (E° = {e1}) and {name2} (E° = {e2}), which species is the STRONGER oxidising agent under standard conditions?"
            wrs = [
                weaker_ox,
                "Both species have identical oxidising strength",
                "Neither species can act as an oxidising agent",
                "The species with the more negative reduction potential",
                "Standard Hydrogen Electrode (SHE)",
                "Pure water at 298 K"
            ]
            add_q("easy", "Standard Potentials", q_text, stronger_ox, wrs, "Understanding", "Compare oxidising strength from reduction potentials",
                  f"The half-cell with the more positive standard reduction potential is the stronger oxidising agent ({stronger_ox} with E° = {high_v} vs {weaker_ox} with E° = {low_v}).")

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Cell EMF Calculations, Cell Notation, Electrode Mass Changes, Industrial Electrolysis
    # =========================================================================

    metals_table = [
        ("Li/Li⁺", -3.04, "Li", 1),
        ("K/K⁺", -2.93, "K", 1),
        ("Ca/Ca²⁺", -2.87, "Ca", 2),
        ("Na/Na⁺", -2.71, "Na", 1),
        ("Mg/Mg²⁺", -2.37, "Mg", 2),
        ("Al/Al³⁺", -1.66, "Al", 3),
        ("Mn/Mn²⁺", -1.18, "Mn", 2),
        ("Zn/Zn²⁺", -0.76, "Zn", 2),
        ("Cr/Cr³⁺", -0.74, "Cr", 3),
        ("Fe/Fe²⁺", -0.44, "Fe", 2),
        ("Ni/Ni²⁺", -0.25, "Ni", 2),
        ("Sn/Sn²⁺", -0.14, "Sn", 2),
        ("Pb/Pb²⁺", -0.13, "Pb", 2),
        ("Cu/Cu²⁺", +0.34, "Cu", 2),
        ("Ag/Ag⁺", +0.80, "Ag", 1),
        ("Pt/Pt²⁺", +1.20, "Pt", 2),
        ("Au/Au³⁺", +1.50, "Au", 3)
    ]

    for i in range(len(metals_table)):
        for j in range(i + 1, len(metals_table)):
            if counts["medium"] >= 500:
                break
            anode_pair, e_anode, a_metal, a_charge = metals_table[i] # more negative E° => Anode
            cathode_pair, e_cathode, c_metal, c_charge = metals_table[j] # more positive E° => Cathode
            e_cell = e_cathode - e_anode
            corr_emf = f"{e_cell:.2f} V"

            wrs_emf = [
                f"{-(e_cell):.2f} V",
                f"{e_cathode + e_anode:.2f} V",
                f"{abs(e_anode) - abs(e_cathode):.2f} V",
                f"{e_cell * 2:.2f} V",
                f"{e_cell / 2:.2f} V",
                "0.00 V",
                f"{e_cell + 0.50:.2f} V"
            ]

            # 1. EMF calculation question
            add_q("medium", "Cell Potential Calculations",
                  f"A standard galvanic cell is constructed using a {anode_pair} half-cell (E° = {e_anode:+.2f} V) and a {cathode_pair} half-cell (E° = {e_cathode:+.2f} V). Calculate the standard cell potential (E°cell):",
                  corr_emf, wrs_emf, "Applying", "Calculate standard cell potential",
                  f"Anode ({a_metal}) is oxidised (more negative E°); Cathode ({c_metal}) is reduced. E°cell = E°cathode - E°anode = ({e_cathode:+.2f}) - ({e_anode:+.2f}) = {corr_emf}.")

            # 2. Anode/Cathode identification question
            add_q("medium", "Cell Components",
                  f"In the galvanic cell combining {anode_pair} (E° = {e_anode:+.2f} V) and {cathode_pair} (E° = {e_cathode:+.2f} V), which electrode functions as the ANODE and what reaction occurs there?",
                  f"{a_metal} is the anode; oxidation occurs ({a_metal} -> {a_metal}{a_charge}+ + {a_charge}e⁻).",
                  [f"{c_metal} is the anode; oxidation occurs.",
                   f"{a_metal} is the cathode; reduction occurs.",
                   f"{c_metal} is the cathode; oxidation occurs.",
                   f"Both electrodes undergo oxidation simultaneously.",
                   f"{a_metal} is the anode; reduction occurs.",
                   f"Neither electrode reacts because E° values have opposite signs.",
                   f"{c_metal} dissolves while {a_metal} plates out."],
                  "Understanding", "Identify anode and cathode in galvanic cell",
                  f"The half-cell with the more negative reduction potential ({a_metal}, E° = {e_anode:+.2f} V) undergoes oxidation and acts as the ANODE.")

            # 3. Cell notation question
            a_ion_str = f"{a_metal}{'+' if a_charge == 1 else f'{a_charge}+'}"
            c_ion_str = f"{c_metal}{'+' if c_charge == 1 else f'{c_charge}+'}"
            notation_corr = f"{a_metal}(s) | {a_ion_str}(1 mol·dm⁻³) || {c_ion_str}(1 mol·dm⁻³) | {c_metal}(s)"
            notation_wrong1 = f"{c_metal}(s) | {c_ion_str}(1 mol·dm⁻³) || {a_ion_str}(1 mol·dm⁻³) | {a_metal}(s)"
            notation_wrong2 = f"{a_metal}(s) || {c_metal}(s)"
            notation_wrong3 = f"{c_metal}(s) || {a_metal}(s)"
            notation_wrong4 = f"Pt | {a_metal}(s) || {c_metal}(s) | Pt"
            notation_wrong5 = f"{a_ion_str}(aq) | {a_metal}(s) || {c_metal}(s) | {c_ion_str}(aq)"
            notation_wrong6 = f"{a_metal}(s) | {c_metal}(s) || electrolyte"
            wrs_not = [notation_wrong1, notation_wrong2, notation_wrong3, notation_wrong4, notation_wrong5, notation_wrong6]
            add_q("medium", "Cell Notation",
                  f"What is the standard cell notation for the galvanic cell constructed from {anode_pair} (E° = {e_anode:+.2f} V) and {cathode_pair} (E° = {e_cathode:+.2f} V)?",
                  notation_corr, wrs_not, "Applying", "Write standard cell notation",
                  f"Standard cell notation follows: Anode | Anode electrolyte || Cathode electrolyte | Cathode. Therefore: {notation_corr}.")

            # 4. Spontaneous net redox equation question
            if a_charge == c_charge:
                net_eq = f"{a_metal}(s) + {c_ion_str}(aq) -> {a_ion_str}(aq) + {c_metal}(s)"
                net_wrongs = [
                    f"{c_metal}(s) + {a_ion_str}(aq) -> {c_ion_str}(aq) + {a_metal}(s)",
                    f"{a_metal}(s) + {c_metal}(s) -> {a_ion_str}(aq) + {c_ion_str}(aq)",
                    f"{a_ion_str}(aq) + {c_ion_str}(aq) -> {a_metal}(s) + {c_metal}(s)",
                    f"{a_metal}(s) -> {a_ion_str}(aq) + {c_metal}(s)",
                    f"{a_metal}(s) + {c_ion_str}(aq) + 2e⁻ -> {a_ion_str}(aq) + {c_metal}(s)",
                    f"{c_ion_str}(aq) -> {c_metal}(s) + 2e⁻"
                ]
            else:
                net_eq = f"{c_charge}{a_metal}(s) + {a_charge}{c_ion_str}(aq) -> {c_charge}{a_ion_str}(aq) + {a_charge}{c_metal}(s)"
                net_wrongs = [
                    f"{a_charge}{a_metal}(s) + {c_charge}{c_ion_str}(aq) -> {a_charge}{a_ion_str}(aq) + {c_charge}{c_metal}(s)",
                    f"{a_metal}(s) + {c_metal}(s) -> {a_ion_str}(aq) + {c_ion_str}(aq)",
                    f"{c_metal}(s) + {a_ion_str}(aq) -> {c_ion_str}(aq) + {a_metal}(s)",
                    f"{a_ion_str}(aq) + {c_ion_str}(aq) -> {a_metal}(s) + {c_metal}(s)",
                    f"{c_charge}{a_metal}(s) + {a_charge}{c_metal}(s) -> products",
                    f"{a_metal}(s) + {c_ion_str}(aq) -> {a_ion_str}(aq) + {c_metal}(s)"
                ]
            add_q("medium", "Net Cell Reactions",
                  f"What is the balanced overall (net) cell reaction for the galvanic cell combining {anode_pair} (E° = {e_anode:+.2f} V) and {cathode_pair} (E° = {e_cathode:+.2f} V)?",
                  net_eq, net_wrongs, "Applying", "Write balanced overall cell reaction",
                  f"Balancing electron transfer between oxidation ({a_metal} -> {a_ion_str} + {a_charge}e⁻) and reduction ({c_ion_str} + {c_charge}e⁻ -> {c_metal}) yields: {net_eq}.")

    # Electrode Mass and Electrolyte Color Changes
    obs_scenarios = [
        ("Zn-Cu Daniell Cell",
         "Zinc anode: mass decreases (dissolves); Copper cathode: mass increases (copper plates out); CuSO4 electrolyte: blue color fades as Cu²⁺ ions are reduced.",
         ["Zinc anode: mass increases; Copper cathode: mass decreases; CuSO4 blue color intensifies.",
          "Both electrodes gain mass equally; solution becomes colorless immediately.",
          "Both electrodes lose mass; blue color turns yellow.",
          "Zinc anode mass stays constant; copper cathode dissolves completely.",
          "Zinc anode plates out zinc; copper cathode evolves hydrogen gas.",
          "Copper cathode becomes negative; zinc anode turns bright red."]),

        ("Mg-Ag Galvanic Cell",
         "Magnesium anode: dissolves rapidly and loses mass; Silver cathode: shiny silver needles deposit and mass increases; [Ag⁺] in solution decreases.",
         ["Magnesium anode gains mass; Silver cathode dissolves completely.",
          "Both electrodes stay at constant mass; magnesium solution turns brown.",
          "Magnesium cathode oxidises; silver anode reduces.",
          "Silver cathode dissolves into silver vapor.",
          "Magnesium anode becomes positive; silver cathode loses all mass.",
          "Magnesium plate explodes upon contact with silver nitrate."]),

        ("Al-Cu Galvanic Cell",
         "Aluminium anode: mass decreases as Al dissolves into Al³⁺; Copper cathode: mass increases as Cu²⁺ plates out as solid copper; blue Cu²⁺ solution fades.",
         ["Aluminium cathode dissolves; Copper anode gains mass.",
          "Both electrodes gain mass and turn green.",
          "Aluminium anode mass increases; copper cathode mass decreases.",
          "Aluminium dissolves to form Al(s) crystals in the salt bridge.",
          "Copper cathode dissolves to form green copper(I) oxide gas.",
          "Neither electrode changes mass because standard conditions are maintained."]),

        ("Fe-Cu Galvanic Cell",
         "Iron anode: corrodes and loses mass (Fe -> Fe²⁺ + 2e⁻); Copper cathode: gains mass (Cu²⁺ + 2e⁻ -> Cu); pale green Fe²⁺ appears while blue Cu²⁺ disappears.",
         ["Iron cathode gains mass; copper anode dissolves.",
          "Iron anode turns into pure gold; copper cathode evaporates.",
          "Both electrodes lose mass at exactly the same rate.",
          "Copper cathode dissolves; iron anode remains completely unreactive.",
          "Iron anode mass increases by absorbing copper ions.",
          "No mass changes occur because both are transition metals."])
    ]

    for sc_name, corr_obs, wr_obs in obs_scenarios:
        add_q("medium", "Electrode Observations",
              f"What physical changes are observed at the electrodes and in the electrolytes during the continuous operation of a **{sc_name}**?",
              corr_obs, wr_obs, "Analyzing", "Predict electrode mass and color changes", corr_obs)

    # Industrial Electrolytic Cells
    industrial_cells = [
        ("Electroplating of a steel spoon with silver (Ag)",
         "Cathode: Steel spoon (to be coated); Anode: Pure silver bar (supplies Ag⁺ ions); Electrolyte: Silver nitrate solution (AgNO3(aq)).",
         ["Cathode: Pure silver bar; Anode: Steel spoon; Electrolyte: Sulfuric acid.",
          "Cathode: Steel spoon; Anode: Inert platinum; Electrolyte: Pure molten sodium chloride.",
          "Cathode: Positive terminal; Anode: Negative terminal; Electrolyte: Distilled water.",
          "Cathode: Zinc rod; Anode: Steel spoon; Electrolyte: Copper sulfate.",
          "Cathode: Carbon rod; Anode: Steel spoon; Electrolyte: Silver metal powder.",
          "Cathode: Molten bauxite; Anode: Cryolite; Electrolyte: Steel."]),

        ("Electrolytic refining (purification) of copper",
         "Anode: Impure blister copper (dissolves into solution); Cathode: Pure copper sheet (pure Cu plates out); Electrolyte: Acidified copper(II) sulfate (CuSO4(aq)).",
         ["Anode: Pure copper; Cathode: Impure copper; Electrolyte: Sodium chloride solution.",
          "Anode: Carbon rod; Cathode: Impure copper; Electrolyte: Copper oxide melt.",
          "Anode: Impure copper; Cathode: Platinum wire; Electrolyte: Distilled water.",
          "Anode: Lead rod; Cathode: Pure copper; Electrolyte: Sulfuric acid alone.",
          "Anode: Pure copper; Cathode: Impure copper; Electrolyte: Molten cryolite.",
          "Anode: Zinc plate; Cathode: Pure copper; Electrolyte: Copper nitrate."]),

        ("Anode sludge (slime) in copper refining",
         "Precious, less reactive metals (such as silver, gold, and platinum) that are not oxidised at the anode potential and settle to the bottom of the tank.",
         ["Toxic waste containing dissolved sulfuric acid and copper ions.",
          "Solid copper metal that evaporated from the cathode.",
          "Precipitated copper sulfate crystals that failed to dissolve.",
          "Impurities of zinc and iron that oxidised and plated onto the bottom.",
          "Carbon soot from the electrical generator.",
          "Insoluble sodium chloride precipitate."]),

        ("Chlor-alkali Membrane Cell",
         "Anode reaction: 2Cl⁻(aq) -> Cl2(g) + 2e⁻ (chlorine gas evolved); Cathode reaction: 2H2O(l) + 2e⁻ -> H2(g) + 2OH⁻(aq) (hydrogen gas evolved and NaOH solution formed); Cation membrane allows only Na⁺ ions to pass.",
         ["Anode: Sodium metal formed; Cathode: Chlorine gas evolved; Membrane: Blocks all ions.",
          "Anode: Oxygen gas formed; Cathode: Hydrochloric acid formed; Membrane: Anion permeable.",
          "Anode: Hydrogen gas; Cathode: Chlorine gas; Electrolyte: Molten sodium metal.",
          "Anode: Water oxidised to ozone; Cathode: Salt precipitates; Membrane: Non-porous glass.",
          "Anode: Sodium hydroxide formed; Cathode: Chlorine gas; Membrane: Platinum foil.",
          "Anode: Chlorine gas; Cathode: Sodium metal; Electrolyte: Pure water."]),

        ("Function of the ion-exchange membrane in the Chlor-alkali cell",
         "It prevents chloride ions (Cl⁻) and hydroxide ions (OH⁻) from mixing (which would form hypochlorite/bleach or explosive Cl2/H2 mixtures), while allowing Na⁺ cations to pass to form pure NaOH.",
         ["It prevents electric current from flowing through the cell.",
          "It blocks sodium ions and forces chlorine into the cathode chamber.",
          "It acts as a heating element to boil the brine solution.",
          "It condenses hydrogen gas into liquid water.",
          "It supplies electrons directly to the anode.",
          "It filters out solid rock salt impurities from entering the waste drain."]),

        ("Aluminium extraction (Hall-Héroult Process)",
         "Bauxite (Al2O3) is dissolved in molten cryolite (Na3AlF6) to lower the melting point from ~2000 °C to ~950 °C; carbon anodes are consumed by reacting with O2 to form CO2 and must be replaced regularly.",
         ["Aluminium is extracted by reduction with carbon monoxide in a blast furnace.",
          "Cryolite acts as a catalyst that prevents aluminium from oxidising.",
          "Carbon anodes are completely inert and never need replacement.",
          "Aluminium is produced at the anode as a gaseous vapor.",
          "The electrolyte is aqueous aluminium sulfate at room temperature.",
          "The process operates at room temperature with zero electrical power."]),

        ("Why carbon anodes must be regularly replaced in aluminium smelting",
         "The oxygen released at the anode reacts with the hot carbon electrodes at 950 °C to produce carbon dioxide gas (C + O2 -> CO2), continually burning away the anode.",
         ["Carbon melts and drips into the molten aluminium at the cathode.",
          "Carbon anodes are coated with aluminium metal and cease conducting.",
          "Carbon dissolves into cryolite to form insoluble graphite sludge.",
          "Electrical sparks crack the carbon rods every 10 minutes.",
          "Cryolite eats through carbon via an acid-base neutralization.",
          "Carbon turns into diamond under the high electrochemical pressure."]),

        ("Downs Cell for the electrolysis of molten sodium chloride",
         "Anode: 2Cl⁻(l) -> Cl2(g) + 2e⁻; Cathode: Na⁺(l) + e⁻ -> Na(l); Molten NaCl is used instead of aqueous brine to prevent water from being preferentially reduced to H2(g).",
         ["Aqueous NaCl is used to produce solid sodium metal at the cathode.",
          "Oxygen gas is produced at the anode and chlorine gas at the cathode.",
          "Sodium metal sinks to the bottom because it is denser than molten salt.",
          "Carbon electrodes reduce NaCl without any electrical input.",
          "The Downs cell operates at 25 °C without heating.",
          "Hydrogen gas is the valuable main product harvested at the anode."])
    ]

    for cell_topic, corr, wrs in industrial_cells:
        add_q("medium", "Industrial Processes",
              f"What are the correct chemical components and principles for: **{cell_topic}**?",
              corr, wrs, "Understanding", "Explain industrial electrolytic process", corr)

    # Systematic EMF calculations with diverse reduction potentials
    step = 1
    while counts["medium"] < 500:
        e1 = -0.10 - (step * 0.01)
        e2 = 0.20 + (step * 0.01)
        e_diff = e2 - e1
        corr_val = f"{e_diff:.2f} V"
        wrs_generic = [
            f"{-e_diff:.2f} V",
            f"{e2 + e1:.2f} V",
            f"{abs(e1) - abs(e2):.2f} V",
            f"{e_diff * 2:.2f} V",
            f"{e_diff / 2:.2f} V",
            "0.00 V",
            f"{e_diff + 0.35:.2f} V"
        ]
        add_q("medium", "Cell Potential Calculations",
              f"An electrochemical cell operates with standard reduction potentials E°(anode) = {e1:.2f} V and E°(cathode) = {e2:.2f} V. Determine the standard electromotive force (EMF) of this cell:",
              corr_val, wrs_generic,
              "Applying", "Calculate generic standard EMF",
              f"E°cell = E°cathode - E°anode = ({e2:.2f}) - ({e1:.2f}) = {corr_val}.")
        step += 1

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Voltage Decay / Flat Battery Equilibrium, Le Chatelier on EMF, Faraday's Law Calculations
    # =========================================================================

    decay_principles = [
        ("Why does the reading on the voltmeter of a functioning galvanic cell steadily decrease over time until it reaches 0.00 V (a 'flat' battery)?",
         "As the cell operates, reactant concentrations decrease and product concentrations increase, shifting the reaction toward chemical equilibrium where forward and reverse rates are equal and E_cell = 0 V.",
         ["The metal atoms in the wires are permanently consumed by the electric current.",
          "The electrons lose all their charge as they travel through the resistor.",
          "The salt bridge dries out and completely stops conducting heat.",
          "The activation energy of the forward reaction rises to infinity.",
          "The temperature of the cell reaches absolute zero.",
          "The cathode loses all its protons to the voltmeter."],
         "As reactants are converted into products, the reaction approaches chemical equilibrium (Q = K). At equilibrium, the driving force (cell potential) is 0 V."),

        ("What is the state of a galvanic cell when its terminal voltage (EMF) drops to exactly 0.00 V?",
         "The cell reaction has reached chemical equilibrium (rates of forward and reverse reactions are equal, ΔG = 0, and internal resistance becomes very high).",
         ["All reactant and product atoms have been completely destroyed.",
          "The cell has reached standard conditions (298 K, 1 atm).",
          "The reaction has reached completion with 100% conversion of reactants.",
          "The salt bridge contains only pure water.",
          "The circuit has short-circuited and voltage reversed.",
          "The electrolyte has solidified into an insulator."],
         "At E_cell = 0.00 V, the cell has reached dynamic chemical equilibrium; delta G is zero and the battery is completely discharged ('flat')."),

        ("In an operating Zn-Cu galvanic cell: Zn(s) + Cu²⁺(aq) ⇌ Zn²⁺(aq) + Cu(s) (ΔH < 0). How will increasing the concentration of Cu²⁺ ions in the cathode half-cell affect the initial cell voltage (EMF)?",
         "The cell EMF increases (voltage rises above 1.10 V), because increasing reactant [Cu²⁺] shifts the equilibrium in the forward direction according to Le Chatelier's principle.",
         ["The cell EMF decreases because more ions impede electron movement.",
          "The cell EMF remains exactly 1.10 V because E°cell depends only on temperature.",
          "The cell EMF drops immediately to zero.",
          "The polarity of the electrodes reverses.",
          "The copper electrode begins to dissolve at the cathode.",
          "The internal resistance drops to zero permanently."],
         "Cu²⁺ is a reactant. Increasing [Cu²⁺] favors the forward reaction, increasing the driving force and cell EMF."),

        ("In the same Zn-Cu cell: Zn(s) + Cu²⁺(aq) ⇌ Zn²⁺(aq) + Cu(s), how will increasing the concentration of Zn²⁺ ions in the anode half-cell affect the cell potential?",
         "The cell EMF decreases (voltage drops below 1.10 V), because increasing product [Zn²⁺] opposes the forward reaction according to Le Chatelier's principle.",
         ["The cell EMF increases because more zinc ions are available to conduct current.",
          "The cell EMF remains completely unchanged.",
          "The zinc electrode stops oxidising completely.",
          "The cell converts into an electrolytic cell.",
          "The copper cathode begins to oxidise.",
          "The value of E°cell increases."],
         "Zn²⁺ is a product. Increasing [Zn²⁺] favors the reverse reaction, opposing electron release and decreasing cell EMF."),

        ("In the Zn-Cu cell: Zn(s) + Cu²⁺(aq) ⇌ Zn²⁺(aq) + Cu(s) (ΔH < 0), what is the effect of increasing the operating temperature of the cell on the cell EMF?",
         "The cell EMF decreases, because the forward redox reaction is exothermic (ΔH < 0); increasing temperature shifts the equilibrium in the endothermic reverse direction.",
         ["The cell EMF increases because ions have greater kinetic energy.",
          "The cell EMF remains constant because temperature does not affect equilibrium.",
          "The cell EMF drops to zero instantly.",
          "The cell switches polarity and becomes electrolytic.",
          "The cell EMF doubles for every 10 °C rise.",
          "The cathode stops conducting electricity."],
         "Because the forward reaction is exothermic, raising the temperature shifts the equilibrium in reverse by Le Chatelier's principle, lowering the EMF."),

        ("In a galvanic cell, what is the effect of doubling the surface area of both the anode and cathode plates on the initial cell EMF and cell longevity?",
         "The initial cell EMF remains unchanged (EMF is an intensive property), but internal resistance decreases, maximum current increases, and the cell operates for longer before going flat.",
         ["The initial cell EMF doubles, but longevity is halved.",
          "Both initial EMF and cell longevity are halved.",
          "The initial cell EMF decreases because capacitance increases.",
          "The cell short-circuits immediately due to excessive surface contact.",
          "The reaction stops because larger plates block ion migration.",
          "The cell EMF increases by 50% without affecting current."],
         "Standard cell potential (EMF) is an intensive property and does NOT depend on electrode size. However, larger surface area reduces internal resistance and increases total available reactant atoms."),

        ("In an operating Daniell cell, sodium hydroxide (NaOH(aq)) is added to the copper(II) half-cell, precipitating blue Cu(OH)2(s). How does this affect the cell potential?",
         "The cell EMF decreases, because OH⁻ precipitates Cu²⁺ ions as Cu(OH)2, lowering reactant [Cu²⁺] and shifting equilibrium in reverse according to Le Chatelier's principle.",
         ["The cell EMF increases because sodium ions carry extra current.",
          "The cell EMF remains unchanged because Cu(OH)2 is a solid.",
          "The cell immediately reverses direction and oxidises copper.",
          "The copper cathode begins to evolve chlorine gas.",
          "The cell EMF doubles because the pH rises.",
          "The cell explodes due to heat of neutralization."],
         "Precipitating Cu²⁺ reduces reactant concentration; by Le Chatelier's principle, the system shifts reverse, decreasing the EMF.")
    ]

    for q_text, corr, wrs, expl in decay_principles:
        add_q("hard", "Cell Equilibrium & EMF", q_text, corr, wrs, "Evaluating", "Evaluate equilibrium and concentration effects on EMF", expl)

    # Quantitative Faraday's Law Electrolysis Problems
    # Q = I * t, n(e-) = Q / 96500, n(metal) = n(e-) / z, mass = n * M
    # Silver deposition: Ag+ + e- -> Ag (M = 107.9, z = 1)
    ag_currents = [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0]
    ag_times = [15.0, 25.0, 30.0, 45.0, 60.0, 75.0, 90.0, 120.0]

    for current in ag_currents:
        for time_min in ag_times:
            if counts["hard"] >= 200:
                break
            time_s = time_min * 60.0
            charge = current * time_s
            n_e = charge / 96500.0
            mass_ag = n_e * 107.9
            q_text = f"An electroplating cell is operated using a constant electric current of {current:.1f} A for exactly {time_min:.0f} minutes to deposit silver onto a spoon from an AgNO3 solution. Half-reaction: Ag⁺(aq) + e⁻ -> Ag(s). Using Faraday's constant (F = 96 500 C·mol⁻¹) and molar mass of silver (107.9 g·mol⁻¹), calculate the mass of silver plated:"
            corr = f"{mass_ag:.3f} g"
            wrs = [
                f"{mass_ag * 2:.3f} g (divided by 2 for divalent assumption)",
                f"{mass_ag / 60:.3f} g (omitted minute-to-second conversion)",
                f"{charge:.1f} g",
                f"{mass_ag * 0.5:.3f} g",
                f"{mass_ag + 2.5:.3f} g",
                f"{(current * time_min) / 107.9:.3f} g",
                f"{mass_ag * 1.5:.3f} g"
            ]
            expl = f"Q = I × t = {current:.1f} × ({time_min:.0f} × 60) = {charge:.1f} C. n(e⁻) = Q / F = {charge:.1f} / 96500 = {n_e:.5f} mol. Since 1 mol e⁻ deposits 1 mol Ag: n(Ag) = {n_e:.5f} mol. Mass = n × M = {n_e:.5f} × 107.9 = {mass_ag:.3f} g."
            add_q("hard", "Electrolysis Stoichiometry", q_text, corr, wrs, "Evaluating", "Calculate mass deposited by electroplating", expl)

    # Copper electroplating: Cu²⁺ + 2e⁻ -> Cu (M = 63.5, z = 2)
    cu_currents = [2.0, 3.5, 5.0, 6.5, 8.0, 10.0, 12.0]
    cu_times = [20.0, 35.0, 45.0, 60.0, 80.0, 100.0]

    for current in cu_currents:
        for time_min in cu_times:
            if counts["hard"] >= 200:
                break
            time_s = time_min * 60.0
            charge = current * time_s
            n_e = charge / 96500.0
            n_cu = n_e / 2.0
            mass_cu = n_cu * 63.5
            q_text = f"In an electrolytic cell for copper refining, a current of {current:.1f} A passes through an acidified CuSO4 solution for {time_min:.0f} minutes. Half-reaction: Cu²⁺(aq) + 2e⁻ -> Cu(s). Calculate the mass of pure copper deposited on the cathode (molar mass of Cu = 63.5 g·mol⁻¹, F = 96 500 C·mol⁻¹):"
            corr = f"{mass_cu:.3f} g"
            wrs = [
                f"{mass_cu * 2:.3f} g (omitted 2e⁻ factor)",
                f"{mass_cu / 2:.3f} g",
                f"{mass_cu / 60:.3f} g (omitted time conversion)",
                f"{charge:.1f} g",
                f"{mass_cu + 1.5:.3f} g",
                f"{(current * time_min * 63.5) / 96500:.3f} g",
                f"{mass_cu * 3:.3f} g"
            ]
            expl = f"Q = I × t = {current:.1f} × ({time_min:.0f} × 60) = {charge:.1f} C. n(e⁻) = {charge:.1f} / 96500 = {n_e:.5f} mol. Since Cu²⁺ requires 2e⁻: n(Cu) = n(e⁻) / 2 = {n_cu:.5f} mol. Mass = n × M = {n_cu:.5f} × 63.5 = {mass_cu:.3f} g."
            add_q("hard", "Electrolysis Stoichiometry", q_text, corr, wrs, "Evaluating", "Calculate copper mass refined in electrolytic cell", expl)

    # Chlorine gas production at anode: 2Cl- -> Cl2 + 2e- (molar volume at STP = 22.4 dm3/mol)
    for current in [4.0, 5.0, 8.0, 10.0, 15.0]:
        for time_min in [30.0, 45.0, 60.0, 90.0]:
            if counts["hard"] >= 200:
                break
            time_s = time_min * 60.0
            charge = current * time_s
            n_e = charge / 96500.0
            n_cl2 = n_e / 2.0
            vol_cl2 = n_cl2 * 22.4
            q_text = f"In a membrane cell for the chlor-alkali process, a steady direct current of {current:.1f} A is passed through concentrated brine for {time_min:.0f} minutes. Anode half-reaction: 2Cl⁻(aq) -> Cl2(g) + 2e⁻. Calculate the volume of chlorine gas produced at STP (molar gas volume at STP = 22.4 dm³·mol⁻¹, F = 96 500 C·mol⁻¹):"
            corr = f"{vol_cl2:.3f} dm³"
            wrs = [
                f"{vol_cl2 * 2:.3f} dm³ (omitted 2e⁻ factor)",
                f"{vol_cl2 / 2:.3f} dm³",
                f"{vol_cl2 / 60:.3f} dm³ (omitted time conversion)",
                f"{charge:.1f} dm³",
                f"{vol_cl2 + 1.2:.3f} dm³",
                f"{(current * time_min) / 22.4:.3f} dm³",
                f"{vol_cl2 * 1.5:.3f} dm³"
            ]
            expl = f"Q = I × t = {current:.1f} × ({time_min:.0f} × 60) = {charge:.1f} C. n(e⁻) = {charge:.1f} / 96500 = {n_e:.5f} mol. n(Cl2) = n(e⁻) / 2 = {n_cl2:.5f} mol. Volume = n × 22.4 = {vol_cl2:.3f} dm³."
            add_q("hard", "Electrolysis Stoichiometry", q_text, corr, wrs, "Evaluating", "Calculate gas volume from chlor-alkali electrolysis", expl)

    # Systematic non-standard electrolyte concentration effects
    step = 1
    while counts["hard"] < 200:
        r_conc = 1.0 + step * 0.05
        p_conc = round(0.50 - (step * 0.002), 3)
        q_text = f"A galvanic cell Zn(s) | Zn²⁺(aq, {p_conc:.3f} mol·dm⁻³) || Cu²⁺(aq, {r_conc:.2f} mol·dm⁻³) | Cu(s) operates under non-standard conditions. Comparing this cell to the standard Daniell cell (where [Cu²⁺] = [Zn²⁺] = 1.00 mol·dm⁻³), how does the initial cell voltage (EMF) compare and why?"
        corr = "The cell voltage is HIGHER than 1.10 V, because higher reactant [Cu²⁺] and lower product [Zn²⁺] shift the equilibrium in the forward direction according to Le Chatelier's principle."
        wrs = [
            "The cell voltage is LOWER than 1.10 V, because ion crowding increases internal resistance.",
            "The cell voltage is exactly EQUAL to 1.10 V, because concentration never affects cell EMF.",
            "The cell voltage drops immediately to 0.00 V because conditions are non-standard.",
            "The polarity of the cell terminals is reversed.",
            "The cell converts into an electrolytic cell requiring external electrical energy.",
            "The zinc electrode stops dissolving and copper begins to oxidise.",
            "The internal resistance drops to zero permanently."
        ]
        expl = f"Reactant concentration [Cu²⁺] = {r_conc:.2f} mol·dm⁻³ is higher than standard, and product concentration [Zn²⁺] = {p_conc:.3f} mol·dm⁻³ is lower. By Le Chatelier's principle, the system shifts forward, increasing the driving potential above standard EMF (1.10 V)."
        add_q("hard", "Cell Equilibrium & EMF", q_text, corr, wrs, "Evaluating", "Evaluate non-standard concentration on cell EMF", expl)
        step += 1

    return questions

if __name__ == '__main__':
    qs = build_electrochemical_reactions()
    out_dir = "dataset/grade12/physical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_electrochemical_reactions.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
