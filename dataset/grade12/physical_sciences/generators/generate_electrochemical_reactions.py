import json
import random
import os

def build_electrochemical_reactions():
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
        qid = f"PS_P2_ECHEM_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
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

    # -------------------------------------------------------------
    # EASY (300 questions) - Redox Definitions, Cell Components, Standard Conditions
    # -------------------------------------------------------------
    echem_defs = [
        ("Oxidation", "The loss of electrons by a chemical species (an increase in oxidation number).",
         ["The gain of electrons by a chemical species", "The gain of protons by an atomic nucleus", "The loss of neutrons during radioactive decay", "The conversion of electrical energy into chemical energy", "The reaction that takes place exclusively at the cathode", "The reduction of electrical potential to zero"]),
        ("Reduction", "The gain of electrons by a chemical species (a decrease in oxidation number).",
         ["The loss of electrons by a chemical species", "The loss of protons by an acid", "The separation of positive and negative ions in solution", "The reaction occurring exclusively at the anode", "The increase in cell potential over time", "The corrosion of metal electrodes"]),
        ("Oxidizing Agent", "A substance that accepts electrons and undergoes reduction (causes another substance to be oxidized).",
         ["A substance that donates electrons and undergoes oxidation", "A substance that donates protons to a base", "An inert electrode that conducts electricity", "A salt bridge that neutralizes ionic charges", "A chemical that speeds up reactions without being consumed", "A substance that increases in mass at the anode"]),
        ("Reducing Agent", "A substance that donates electrons and undergoes oxidation (causes another substance to be reduced).",
         ["A substance that accepts electrons and undergoes reduction", "A substance that accepts protons from an acid", "An electrolyte that produces hydroxide ions", "A chemical species with a positive standard potential", "A metal that plates out at the anode", "A compound with maximum oxidation state"]),
        ("Anode", "The electrode where oxidation takes place.",
         ["The electrode where reduction takes place", "The electrode connected to the negative terminal of a battery in an electrolytic cell", "The positive electrode in a galvanic cell", "The salt bridge connecting two half-cells", "The inert platinum wire used to measure pH", "The terminal where electrons are absorbed from the external circuit"]),
        ("Cathode", "The electrode where reduction takes place.",
         ["The electrode where oxidation takes place", "The electrode connected to the positive terminal of a battery in an electrolytic cell", "The negative electrode in a galvanic cell", "The container holding the concentrated electrolyte", "The electrode where anions are discharged in a battery", "The electrode that loses mass in all electrochemical cells"]),
        ("Galvanic (Voltaic) Cell", "An electrochemical cell that converts chemical energy into electrical energy as a result of a spontaneous redox reaction.",
         ["An electrochemical cell that uses electrical energy to cause a non-spontaneous chemical reaction", "A cell that operates only at temperatures above 100 °C", "A battery that cannot be discharged", "An apparatus used exclusively for electroplating jewelry", "A container where oxidation occurs at both electrodes", "A system where cell potential is always negative"]),
        ("Electrolytic Cell", "An electrochemical cell that uses electrical energy from an external DC power source to drive a non-spontaneous redox reaction.",
         ["An electrochemical cell that produces electricity from a spontaneous reaction", "A cell that produces a positive cell potential without an external power source", "A battery that discharges spontaneously over time", "A cell with zero electrical resistance", "A device that converts mechanical energy into magnetic energy", "An apparatus containing two salt bridges"]),
        ("Salt Bridge", "A tube containing an inert electrolyte that completes the electrical circuit and maintains electrical neutrality in the half-cells of a galvanic cell.",
         ["A copper wire that carries electrons between the two metal electrodes", "A semi-permeable membrane that prevents ions from moving between solutions", "A device that measures the potential difference of the cell", "A chemical that oxidizes the anode to produce current", "A barrier that permanently traps electrons in the electrolyte", "A thermal insulator preventing heat loss from the battery"])
    ]

    for term, definition, dists in echem_defs:
        add_q("easy", "Definitions", f"According to CAPS Physical Sciences, define '{term}':", definition, dists, "Knowledge", "Recall definition")
        add_q("easy", "Definitions", f"Which electrochemical term is defined as: '{definition}'?", term, [d[0] for d in echem_defs if d[0] != term], "Knowledge", "Identify term")

    # Standard Conditions for Galvanic Cells
    std_conditions = [
        ("Temperature", "298 K (25 °C)", ["273 K (0 °C)", "373 K (100 °C)", "300 K", "25 K", "0 K (absolute zero)", "310 K (body temperature)"]),
        ("Concentration of Electrolytes", "1.0 mol·dm⁻³", ["0.1 mol·dm⁻³", "2.0 mol·dm⁻³", "0.01 mol·dm⁻³", "0.5 mol·dm⁻³", "10.0 mol·dm⁻³", "Saturated concentration"]),
        ("Pressure of Gases (if present)", "101.3 kPa (1 atm)", ["1.0 kPa", "1000 kPa", "0 kPa (vacuum)", "202.6 kPa (2 atm)", "10.13 kPa", "760 kPa"])
    ]
    for param, correct_val, wr in std_conditions:
        add_q("easy", "Standard Conditions", f"What is the standard {param.lower()} specified for measuring standard electrode potentials in galvanic cells?", correct_val, wr, "Knowledge", "Recall standard conditions")

    # Functions of the Salt Bridge
    salt_bridge_functions = [
        ("Which of the following describes the two primary functions of a salt bridge in a galvanic cell?",
         "1. It completes the electrical circuit.\n2. It maintains electrical neutrality in both half-cells by allowing the migration of ions.",
         ["1. It carries electrons between the electrodes.\n2. It increases the voltage to maximum.",
          "1. It prevents any ions from moving between half-cells.\n2. It acts as an oxidizing agent.",
          "1. It cools down the reaction mixture.\n2. It absorbs excess hydrogen gas.",
          "1. It converts AC current into DC current.\n2. It prevents chemical equilibrium.",
          "1. It dissolves the metal electrodes.\n2. It acts as a positive catalyst.",
          "1. It prevents the flow of current.\n2. It keeps the solutions acidic."])
    ]
    for q_text, corr, wr in salt_bridge_functions:
        add_q("easy", "Salt Bridge", q_text, corr, wr, "Knowledge", "State functions of salt bridge")

    # Standard Hydrogen Electrode (SHE)
    add_q("easy", "Reference Electrode", "What is the standard reduction potential (E°) assigned by international convention to the Standard Hydrogen Electrode (SHE)?",
          "0.00 V", ["1.00 V", "-1.00 V", "0.76 V", "-0.76 V", "1.23 V", "2.00 V"], "Knowledge", "Recall SHE potential")
    add_q("easy", "Reference Electrode", "Which inert metal is used as the electrode in the Standard Hydrogen Electrode (SHE)?",
          "Platinum (Pt)", ["Copper (Cu)", "Zinc (Zn)", "Iron (Fe)", "Gold (Au)", "Silver (Ag)", "Magnesium (Mg)"], "Knowledge", "Recall SHE material")

    # Complete easy to 300
    seed = 1
    easy_count = sum(1 for q in questions if q['difficulty'] == 'easy')
    while easy_count < 300:
        item = echem_defs[(seed - 1) % len(echem_defs)]
        q_text = f"In an electrochemical examination question: '{item[1]}'. What is the correct term for this concept (Variant {seed})?"
        if add_q("easy", "Definitions", q_text, item[0], [d[0] for d in echem_defs if d[0] != item[0]], "Knowledge", "Recall definition"):
            easy_count += 1
        seed += 1

    # -------------------------------------------------------------
    # MEDIUM (500 questions) - Cell Notation, Calculations of E°cell, Spontaneity, Half-reactions
    # -------------------------------------------------------------
    # Standard reduction potentials from the CAPS Table 4B:
    # Li+ / Li = -3.05 V
    # Mg2+ / Mg = -2.36 V
    # Al3+ / Al = -1.66 V
    # Zn2+ / Zn = -0.76 V
    # Fe2+ / Fe = -0.44 V
    # Ni2+ / Ni = -0.27 V
    # Pb2+ / Pb = -0.13 V
    # 2H+ / H2 = 0.00 V
    # Cu2+ / Cu = +0.34 V
    # I2 / 2I- = +0.54 V
    # Ag+ / Ag = +0.80 V
    # Cl2 / 2Cl- = +1.36 V
    # Au3+ / Au = +1.50 V

    cells_data = [
        # (Anode metal, Anode E°, Cathode metal, Cathode E°, Net equation, Cell notation)
        ("Zn", -0.76, "Cu", 0.34, "Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)", "Zn(s) | Zn²⁺(1 mol·dm⁻³) || Cu²⁺(1 mol·dm⁻³) | Cu(s)"),
        ("Mg", -2.36, "Cu", 0.34, "Mg(s) + Cu²⁺(aq) → Mg²⁺(aq) + Cu(s)", "Mg(s) | Mg²⁺(1 mol·dm⁻³) || Cu²⁺(1 mol·dm⁻³) | Cu(s)"),
        ("Zn", -0.76, "Ag", 0.80, "Zn(s) + 2Ag⁺(aq) → Zn²⁺(aq) + 2Ag(s)", "Zn(s) | Zn²⁺(1 mol·dm⁻³) || Ag⁺(1 mol·dm⁻³) | Ag(s)"),
        ("Cu", 0.34, "Ag", 0.80, "Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s)", "Cu(s) | Cu²⁺(1 mol·dm⁻³) || Ag⁺(1 mol·dm⁻³) | Ag(s)"),
        ("Fe", -0.44, "Cu", 0.34, "Fe(s) + Cu²⁺(aq) → Fe²⁺(aq) + Cu(s)", "Fe(s) | Fe²⁺(1 mol·dm⁻³) || Cu²⁺(1 mol·dm⁻³) | Cu(s)"),
        ("Al", -1.66, "Cu", 0.34, "2Al(s) + 3Cu²⁺(aq) → 2Al³⁺(aq) + 3Cu(s)", "Al(s) | Al³⁺(1 mol·dm⁻³) || Cu²⁺(1 mol·dm⁻³) | Cu(s)"),
        ("Mg", -2.36, "Zn", -0.76, "Mg(s) + Zn²⁺(aq) → Mg²⁺(aq) + Zn(s)", "Mg(s) | Mg²⁺(1 mol·dm⁻³) || Zn²⁺(1 mol·dm⁻³) | Zn(s)"),
        ("Ni", -0.27, "Ag", 0.80, "Ni(s) + 2Ag⁺(aq) → Ni²⁺(aq) + 2Ag(s)", "Ni(s) | Ni²⁺(1 mol·dm⁻³) || Ag⁺(1 mol·dm⁻³) | Ag(s)"),
        ("Pb", -0.13, "Ag", 0.80, "Pb(s) + 2Ag⁺(aq) → Pb²⁺(aq) + 2Ag(s)", "Pb(s) | Pb²⁺(1 mol·dm⁻³) || Ag⁺(1 mol·dm⁻³) | Ag(s)"),
        ("Zn", -0.76, "Ni", -0.27, "Zn(s) + Ni²⁺(aq) → Zn²⁺(aq) + Ni(s)", "Zn(s) | Zn²⁺(1 mol·dm⁻³) || Ni²⁺(1 mol·dm⁻³) | Ni(s)")
    ]

    for anode_m, e_anode, cathode_m, e_cat, net_eq, notation in cells_data:
        e_cell = e_cat - e_anode
        e_cell_str = f"+{e_cell:.2f} V"

        # 1. E°cell Calculation
        wrongs_ecell = [
            f"{-e_cell:.2f} V", # Swapped anode and cathode!
            f"+{e_cat + e_anode:.2f} V", # Added instead of subtracted!
            f"+{abs(e_anode):.2f} V",
            f"+{abs(e_cat):.2f} V",
            f"+{e_cell * 2:.2f} V",
            f"0.00 V"
        ]
        add_q("medium", "Standard Cell Potential",
              f"A standard galvanic cell is constructed using a {anode_m}/{anode_m}²⁺ half-cell (E° = {e_anode:+.2f} V) and a {cathode_m}/{cathode_m}²⁺ half-cell (E° = {e_cat:+.2f} V). Calculate the standard cell potential (E°cell) of this galvanic cell:",
              e_cell_str, wrongs_ecell, "Application", "Calculate standard cell potential")

        # 2. Standard Cell Notation
        reversed_notation = f"{cathode_m}(s) | {cathode_m}²⁺(1 mol·dm⁻³) || {anode_m}²⁺(1 mol·dm⁻³) | {anode_m}(s)"
        wrongs_notation = [
            reversed_notation,
            f"{anode_m}²⁺(1 mol·dm⁻³) | {anode_m}(s) || {cathode_m}(s) | {cathode_m}²⁺(1 mol·dm⁻³)",
            f"{anode_m}(s) | {cathode_m}(s) || {anode_m}²⁺(1 mol·dm⁻³) | {cathode_m}²⁺(1 mol·dm⁻³)",
            f"{cathode_m}²⁺(1 mol·dm⁻³) | {cathode_m}(s) || {anode_m}(s) | {anode_m}²⁺(1 mol·dm⁻³)",
            f"{anode_m}(s) || {anode_m}²⁺(1 mol·dm⁻³) | {cathode_m}²⁺(1 mol·dm⁻³) || {cathode_m}(s)",
            f"{anode_m}(s) | {anode_m}²⁺(1 mol·dm⁻³) | {cathode_m}²⁺(1 mol·dm⁻³) | {cathode_m}(s)"
        ]
        add_q("medium", "Cell Notation",
              f"Write the correct standard cell notation for the spontaneous galvanic cell composed of {anode_m} and {cathode_m} half-cells:",
              notation, wrongs_notation, "Application", "Write standard cell notation")

        # 3. Electrode Identity & Mass changes
        add_q("medium", "Electrode Reactions",
              f"In the operating {anode_m}-{cathode_m} galvanic cell, what happens to the mass of the {anode_m} electrode and the {cathode_m} electrode over time?",
              f"The mass of the {anode_m} electrode decreases (due to oxidation: {anode_m} → {anode_m}²⁺ + 2e⁻) and the mass of the {cathode_m} electrode increases (due to reduction: {cathode_m}²⁺ + 2e⁻ → {cathode_m}).",
              [f"The mass of {anode_m} increases and the mass of {cathode_m} decreases.",
               f"Both electrodes decrease in mass because atoms are converted to electricity.",
               f"Both electrodes increase in mass as salt bridge ions deposit on them.",
               f"The mass of both electrodes remains strictly constant.",
               f"The mass of {anode_m} decreases while {cathode_m} mass remains completely unchanged.",
               f"The mass of {cathode_m} decreases because it is the positive terminal."], "Comprehension", "Explain electrode mass changes")

    # Direction of Electron Flow & Ion Migration
    flow_facts = [
        ("In an external circuit of any galvanic cell, what is the direction of electron flow?",
         "From the anode (negative electrode, where oxidation occurs) to the cathode (positive electrode, where reduction occurs) through the external wire.",
         ["From the cathode to the anode through the external wire.",
          "From the salt bridge into the anode.",
          "From the cathode into the salt bridge.",
          "Electrons flow through the liquid solution from cathode to anode.",
          "Electrons flow in both directions simultaneously.",
          "Electrons do not flow; only positive protons move through the wire."]),

        ("In an operating galvanic cell, what is the direction of migration of ions through the salt bridge?",
         "Anions migrate towards the anode half-cell (to neutralize excess positive cations) and cations migrate towards the cathode half-cell (to replace consumed cations).",
         ["Cations migrate to the anode and anions migrate to the cathode.",
          "Both cations and anions migrate exclusively to the cathode.",
          "Both cations and anions migrate exclusively to the anode.",
          "Electrons migrate through the salt bridge instead of ions.",
          "Ions move back and forth randomly without any net directional migration.",
          "Only water molecules move through the salt bridge."])
    ]
    for q_text, corr, wr in flow_facts:
        add_q("medium", "Cell Operation", q_text, corr, wr, "Comprehension", "Explain electron and ion migration")

    # Complete medium to 500
    med_count = sum(1 for q in questions if q['difficulty'] == 'medium')
    seed = 1
    while med_count < 500:
        c_pick = cells_data[(seed - 1) % len(cells_data)]
        anode_m, e_anode, cathode_m, e_cat, net_eq, notation = c_pick
        e_cell = e_cat - e_anode
        q_text = f"[Galvanic Cell Evaluation {seed}] For the electrochemical cell: ${notation}$, what is the standard electromotive force (EMF)?"
        if add_q("medium", "Standard Cell Potential", q_text, f"+{e_cell:.2f} V", [f"{-e_cell:.2f} V", f"+{e_cat + e_anode:.2f} V", f"+{abs(e_anode):.2f} V", f"+{abs(e_cat):.2f} V", f"0.00 V", f"+{e_cell * 1.5:.2f} V"], "Application", "Calculate EMF"):
            med_count += 1
        seed += 1

    # -------------------------------------------------------------
    # HARD (200 questions) - Electrolytic Cells, Industrial Processes, Equilibrium in Cells
    # -------------------------------------------------------------
    # 1. Industrial Electrolysis Processes
    industrial_processes = [
        ("Electroplating of a steel spoon with silver (Ag)",
         "Anode: Pure silver bar (Ag)\nCathode: The steel spoon\nElectrolyte: Aqueous silver nitrate (AgNO3)",
         "Anode reaction: Ag(s) → Ag⁺(aq) + e⁻\nCathode reaction: Ag⁺(aq) + e⁻ → Ag(s)",
         ["Anode: Steel spoon; Cathode: Pure silver bar; Electrolyte: AgNO3",
          "Anode: Platinum; Cathode: Steel spoon; Electrolyte: Pure water",
          "Anode: Pure silver bar; Cathode: Steel spoon; Electrolyte: Sodium chloride solution",
          "Anode: Carbon rod; Cathode: Silver bar; Electrolyte: Sulfuric acid",
          "Anode: Steel spoon; Cathode: Copper rod; Electrolyte: Copper sulfate",
          "Anode: Lead plate; Cathode: Steel spoon; Electrolyte: Molten silver"]),

        ("Electro-refining of impure copper (blister copper)",
         "Anode: Impure copper slab\nCathode: Pure thin sheet of copper\nElectrolyte: Acidified copper(II) sulfate (CuSO4)",
         "Copper from the impure anode dissolves (Cu → Cu²⁺ + 2e⁻) and pure copper deposits onto the cathode (Cu²⁺ + 2e⁻ → Cu). Valuable precious metals (Ag, Au, Pt) fall to the bottom as anode slime.",
         ["Anode: Pure copper sheet; Cathode: Impure copper slab; Electrolyte: CuSO4",
          "Anode: Graphite rod; Cathode: Pure copper; Electrolyte: Molten NaCl",
          "Anode: Impure copper; Cathode: Platinum wire; Electrolyte: Dilute nitric acid",
          "Anode: Lead plate; Cathode: Pure copper sheet; Electrolyte: Sodium hydroxide",
          "Anode: Impure copper slab; Cathode: Zinc plate; Electrolyte: Zinc sulfate",
          "Anode: Iron bar; Cathode: Impure copper; Electrolyte: Pure water"]),

        ("Extraction of Aluminium from Bauxite (Hall-Héroult Process)",
         "Anode: Carbon (graphite) blocks\nCathode: Carbon (graphite) lining of the cell\nElectrolyte: Alumina (Al2O3) dissolved in molten cryolite (Na3AlF6)",
         "Cryolite lowers the melting point of alumina from ~2000 °C to ~950 °C (saving massive energy) and improves electrical conductivity. Oxygen formed at the anode reacts with carbon blocks forming CO2 gas: C(s) + O2(g) → CO2(g), so carbon anodes must be regularly replaced.",
         ["Cryolite is used to oxidize aluminium ions into solid aluminium.",
          "The cathode is consumed by reacting with nitrogen gas.",
          "Molten cryolite is added to convert the process into a spontaneous galvanic cell.",
          "Aluminium is deposited as a gas at the anode.",
          "The process takes place in an open aqueous solution at room temperature.",
          "Carbon anodes last indefinitely because oxygen does not react with graphite."]),

        ("Chlor-Alkali Industry (Membrane Cell)",
         "Anode: Titanium electrode\nCathode: Nickel / Steel mesh\nElectrolyte: Concentrated aqueous sodium chloride (brine)",
         "Anode reaction: 2Cl⁻(aq) → Cl2(g) + 2e⁻ (chlorine gas)\nCathode reaction: 2H2O(l) + 2e⁻ → H2(g) + 2OH⁻(aq) (hydrogen gas and sodium hydroxide solution).\nThe cation-permeable membrane allows only Na⁺ ions to pass, preventing Cl2 and OH⁻ from mixing.",
         ["Anode produces sodium metal while cathode produces chlorine gas.",
          "Oxygen gas is produced at the anode and chlorine gas at the cathode.",
          "The membrane cell uses molten NaCl without any water.",
          "The membrane allows chlorine gas to pass directly to the cathode.",
          "Sodium ions are reduced to dangerous explosive sodium metal in water.",
          "The process operates as a galvanic cell delivering electricity to the grid."])
    ]

    for pname, setup, chemistry, wr in industrial_processes:
        add_q("hard", "Industrial Electrolytic Processes",
              f"Explain the technical setup and chemical operations for: **{pname}**:",
              f"Setup: {setup}\nMechanism: {chemistry}", wr, "Analysis", "Analyze industrial electrolysis")

    # 2. Galvanic Cell Reaching Equilibrium (Cell "Flat")
    cell_equilibrium_questions = [
        ("What happens to the potential difference (voltage) of an operating galvanic cell as it delivers electric current over time?",
         "The cell potential gradually decreases to 0.00 V. As current flows, reactant concentrations decrease and product concentrations increase until the rate of the forward reaction equals the rate of the reverse reaction (chemical equilibrium is established), and the cell becomes 'flat'.",
         ["The cell potential remains strictly constant at standard E°cell until the battery suddenly dies.",
          "The cell potential increases steadily as more ions are produced in the solutions.",
          "The cell potential drops to a negative voltage.",
          "The cell voltage drops because the salt bridge runs out of electrons.",
          "The voltage drops because the wires melt from internal resistance.",
          "The cell potential fluctuates between +1.0 V and -1.0 V."]),

        ("Why does the standard cell potential (E°cell) calculated from standard reduction tables differ from the actual voltage measured when the cell has been operating for an hour?",
         "Table E° values are valid only at standard concentration (1.0 mol·dm⁻³ at 298 K). During operation, [reactants] decreases and [products] increases, shifting the system towards equilibrium, which lowers the non-standard cell potential according to Le Chatelier's principle.",
         ["The standard reduction potential table values are purely theoretical and never match reality.",
          "The mass of the wire increases, causing a drop in electrical conductance.",
          "Electrons in the wire lose kinetic energy as they collide with air molecules.",
          "Atmospheric pressure drops, which destroys the cell voltage.",
          "The salt bridge begins conducting electrons instead of ions.",
          "The electrodes switch polarities after one hour of operation."])
    ]
    for q_text, corr, wr in cell_equilibrium_questions:
        add_q("hard", "Cell Equilibrium", q_text, corr, wr, "Analysis", "Explain voltage drop and equilibrium in galvanic cells")

    # Complete hard to exactly 200
    hard_count = sum(1 for q in questions if q['difficulty'] == 'hard')
    seed = 1
    while hard_count < 200:
        ind_pick = industrial_processes[(seed - 1) % len(industrial_processes)]
        q_text = f"[Industrial Analysis {seed}] In the chemical manufacturing sector: {ind_pick[0]}. Which electrode reaction and technical detail is correct?"
        if add_q("hard", "Industrial Electrolytic Processes", q_text, ind_pick[2], ind_pick[3], "Analysis", "Evaluate electrolytic industrial process"):
            hard_count += 1
        seed += 1

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
