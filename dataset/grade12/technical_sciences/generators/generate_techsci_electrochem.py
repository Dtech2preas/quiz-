import json
import os

def build_electrochemistry():
    questions = []
    seen_questions = set()
    counts = {"easy": 0, "medium": 0, "hard": 0}

    def add_q(difficulty, subtopic, q_text, correct, wrongs, cognitive, outcome, explanation):
        target = 300 if difficulty == "easy" else 500 if difficulty == "medium" else 200
        if counts[difficulty] >= target:
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
        qid = f"TS_P2_ECHEM_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Electrochemistry",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Electrochemistry",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Redox Rules, Galvanic vs Electrolytic, Daniell Cell Basics
    # =========================================================================

    core_definitions = [
        ("Oxidation",
         "The loss of electrons by a chemical substance during a redox reaction (accompanied by an increase in oxidation number).",
         ["The gain of electrons by a chemical substance during a redox reaction",
          "The complete neutralization of an acid by an alkali hydroxide base",
          "The migration of positively charged cations towards the negative cathode",
          "The dissolution of a salt crystal into aqueous hydrated ions",
          "The absorption of thermal energy during an endothermic chemical change",
          "The decrease in oxidation number caused by electron capture"],
         "Oxidation is the LOSS of electrons (OIL: Oxidation Is Loss; increase in oxidation state)."),

        ("Reduction",
         "The gain of electrons by a chemical substance during a redox reaction (accompanied by a decrease in oxidation number).",
         ["The loss of electrons by a chemical substance to an external circuit",
          "The physical reduction in mass of the sacrificial zinc anode",
          "The corrosion of metallic iron in the presence of water and oxygen",
          "The emission of alpha particles from an unstable atomic nucleus",
          "The conversion of an aqueous solution into a solid precipitate",
          "The increase in oxidation number from zero to positive values"],
         "Reduction is the GAIN of electrons (RIG: Reduction Is Gain; decrease in oxidation state)."),

        ("Oxidizing Agent",
         "A substance that gains electrons and undergoes reduction, thereby causing another substance to be oxidized.",
         ["A substance that loses electrons and undergoes oxidation",
          "An inert electrolyte used in the construction of a salt bridge",
          "A metallic electrode that donates electrons to the external circuit",
          "A chemical catalyst that speeds up both forward and reverse reactions",
          "A solvent that dissolves ionic compounds without reacting",
          "A substance that prevents any electron transfer from taking place"],
         "An oxidizing agent accepts electrons (is reduced) and causes the oxidation of another substance."),

        ("Reducing Agent",
         "A substance that loses (donates) electrons and undergoes oxidation, thereby causing another substance to be reduced.",
         ["A substance that accepts electrons and undergoes reduction",
          "An inert platinum electrode that provides a conduction surface",
          "A porous diaphragm that blocks anion migration across half-cells",
          "An acid that donates hydronium ions in aqueous solution",
          "A substance whose oxidation number decreases during the reaction",
          "A chemical that gains two or more electrons from the cathode"],
         "A reducing agent donates electrons (is oxidized) and causes the reduction of another substance."),

        ("Anode",
         "The electrode in an electrochemical cell where OXIDATION always occurs (An Ox); it is the negative terminal in a Galvanic cell and the positive terminal in an Electrolytic cell.",
         ["The electrode where reduction always takes place in all cells",
          "The electrode that always attracts negative anions in a galvanic cell",
          "The electrode whose mass always increases during electrolysis",
          "The positive terminal of a spontaneous chemical galvanic battery",
          "The inert glass tube containing potassium nitrate electrolyte",
          "The terminal where hydrogen gas is always produced during refining"],
         "Anode: Oxidation always occurs here (An Ox). Negative in galvanic; positive in electrolytic."),

        ("Cathode",
         "The electrode in an electrochemical cell where REDUCTION always occurs (Red Cat); it is the positive terminal in a Galvanic cell and the negative terminal in an Electrolytic cell.",
         ["The electrode where oxidation always occurs in an electrochemical cell",
          "The electrode connected to the positive terminal of an external DC supply",
          "The electrode where metallic corrosion always dissolves the metal",
          "The negative terminal of a discharging primary galvanic cell",
          "The porous partition separating anode and cathode half-cells",
          "The terminal that donates electrons directly to the external wire"],
         "Cathode: Reduction always occurs here (Red Cat). Positive in galvanic; negative in electrolytic."),

        ("Galvanic (Voltaic) Cell",
         "An electrochemical cell that converts CHEMICAL energy into ELECTRICAL energy by means of a self-sustaining, spontaneous redox reaction (e.g. Daniell cell, car battery).",
         ["A cell that uses electrical energy from an external source to drive a non-spontaneous reaction",
          "A cell used solely for electroplating cheaper metals with gold or silver",
          "A high-temperature furnace used to extract aluminium from molten bauxite",
          "An industrial cell designed to produce chlorine gas and sodium hydroxide",
          "A storage tank that stores alternating current in chemical bonds",
          "A device that converts mechanical rotational kinetic energy into direct current"],
         "Galvanic cells convert chemical energy to electrical energy via spontaneous redox reactions."),

        ("Electrolytic Cell",
         "An electrochemical cell that uses ELECTRICAL energy from an external direct current (DC) power source to drive a NON-SPONTANEOUS chemical redox reaction.",
         ["A cell that generates an electric current from spontaneous chemical reactions",
          "A battery that discharges spontaneously to power an electric motor",
          "A device that converts chemical energy directly into mechanical work",
          "A cell containing a salt bridge that produces an EMF of 1.10 V",
          "An electrical component that steps up alternating voltages on the grid",
          "A self-charging power unit that operates without any external energy"],
         "Electrolytic cells use electrical energy from an external source to force non-spontaneous reactions."),

        ("Electrolyte",
         "A liquid or aqueous solution containing free-moving ions that conducts electricity through the migration of these ions.",
         ["A solid metallic rod that conducts electricity via delocalized valence electrons",
          "A non-polar organic liquid that completely blocks the passage of electric current",
          "An inert gas used to prevent oxidation in high-temperature welding arcs",
          "A ceramic insulator that supports high-voltage transmission lines",
          "A pure covalent liquid (such as distilled water) with zero dissolved solutes",
          "A chemical polymer that forms cross-linked chains when heated"],
         "An electrolyte is an ionic solution/melt with mobile ions that conducts electric current."),

        ("Salt Bridge",
         "A U-tube containing an inert electrolyte (such as KNO₃ or KCl gel) that connects two half-cells, completing the circuit and maintaining electrical neutrality by allowing ions to migrate.",
         ["A copper wire that carries valence electrons between the two half-cells",
          "A semiconductor diode that prevents reverse current flow in galvanic cells",
          "A heating element that maintains the cell electrolyte at exactly 100 °C",
          "A chemical barrier that prevents any ions from moving between containers",
          "A metallic strip that steps down the voltage delivered to the load",
          "An instrument that measures the internal resistance of the battery"],
         "A salt bridge completes the electrical circuit and maintains electrical neutrality in half-cells via ion migration.")
    ]

    stems = [
        "In Grade 12 Technical Sciences Electrochemistry, how is **'{}'** defined?",
        "According to the CAPS curriculum, **'{}'** refers to:",
        "Which statement gives the precise scientific definition of **'{}'**?",
        "Identify the correct CAPS definition for **'{}'**:",
        "In an examination context, which statement accurately defines **'{}'**?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Standard Conditions for Electrochemical Cells (Easy)
    std_conditions = [
        ("Standard concentration of aqueous electrolytes", "1.0 mol·dm⁻³ (1 M)", ["0.1 mol·dm⁻³", "2.0 mol·dm⁻³", "0.5 mol·dm⁻³", "10.0 mol·dm⁻³", "saturated solution", "0.01 mol·dm⁻³"]),
        ("Standard temperature for standard electrode potentials", "25 °C (298 K)", ["0 °C (273 K)", "100 °C (373 K)", "20 °C (293 K)", "50 °C (323 K)", "37 °C (310 K)", "-273 °C (0 K)"]),
        ("Standard pressure for gaseous electrodes (e.g. standard hydrogen electrode)", "101.3 kPa (1 atmosphere / 1.013 × 10⁵ Pa)", ["10.0 kPa", "200 kPa", "1.0 kPa", "500 kPa", "0 kPa (vacuum)", "1013 kPa"])
    ]

    for cond_name, cond_ans, cond_wrongs in std_conditions:
        for st_cond in [
            f"What is the exact standard condition value for **{cond_name}** in electrochemistry?",
            f"In standard electrode potential measurements, **{cond_name}** is fixed at:",
            f"Identify the standard state condition for **{cond_name}**:"
        ]:
            if counts["easy"] >= 300:
                break
            w_c = cond_wrongs
            add_q("easy", "Standard Conditions", st_cond, cond_ans, w_c, "Remembering", f"State {cond_name}", f"Standard condition: {cond_name} = {cond_ans}.")

    # Galvanic vs Electrolytic Cell Fundamental Differences (Easy)
    cell_differences = [
        ("Energy conversion in a Galvanic cell vs an Electrolytic cell",
         "A Galvanic cell converts CHEMICAL energy into ELECTRICAL energy; an Electrolytic cell converts ELECTRICAL energy into CHEMICAL energy.",
         ["A Galvanic cell converts electrical to chemical; an Electrolytic cell converts chemical to electrical.",
          "Both cells convert mechanical kinetic energy into electrical energy.",
          "A Galvanic cell produces nuclear energy while an Electrolytic cell stores thermal heat.",
          "Both cells require an external direct current power supply to function.",
          "A Galvanic cell operates only on AC while an Electrolytic cell operates on DC.",
          "A Galvanic cell uses heat to produce light while an Electrolytic cell produces sound."],
         "Galvanic: Chemical -> Electrical (spontaneous). Electrolytic: Electrical -> Chemical (non-spontaneous)."),

        ("Spontaneity of redox reactions in Galvanic vs Electrolytic cells",
         "Galvanic cells operate via SPONTANEOUS redox reactions (E°cell > 0); Electrolytic cells drive NON-SPONTANEOUS redox reactions requiring external electrical input.",
         ["Galvanic cells are non-spontaneous; Electrolytic cells are completely spontaneous.",
          "Both cells have negative cell potentials and are non-spontaneous.",
          "Both cells operate spontaneously without any chemical energy change.",
          "Galvanic reactions only occur when heated to over 1000 °C.",
          "Electrolytic reactions proceed spontaneously once initiated by a spark.",
          "Galvanic cells require continuous mechanical stirring to remain spontaneous."],
         "Galvanic reactions are spontaneous (E°cell > 0); electrolytic reactions are non-spontaneous and driven by a DC power supply."),

        ("Polarity of the Anode in Galvanic vs Electrolytic cells",
         "The anode is the NEGATIVE terminal in a Galvanic cell (source of electrons), but the POSITIVE terminal in an Electrolytic cell (connected to the positive DC terminal).",
         ["The anode is positive in a galvanic cell and negative in an electrolytic cell.",
          "The anode is always positive in all electrochemical cells without exception.",
          "The anode is always negative in all electrochemical cells without exception.",
          "The anode has zero electrical polarity because no ions touch it.",
          "The anode polarity alternates between positive and negative at 50 Hz.",
          "The anode polarity depends solely on ambient atmospheric humidity."],
         "Anode polarity: Negative in Galvanic (releases electrons to circuit); Positive in Electrolytic (connected to DC positive)."),

        ("Polarity of the Cathode in Galvanic vs Electrolytic cells",
         "The cathode is the POSITIVE terminal in a Galvanic cell (attracts electrons), but the NEGATIVE terminal in an Electrolytic cell (connected to the negative DC terminal).",
         ["The cathode is negative in a galvanic cell and positive in an electrolytic cell.",
          "The cathode is always negative in all electrochemical systems.",
          "The cathode is always positive in all electrochemical systems.",
          "The cathode has zero electrical polarity in both cells.",
          "The cathode polarity reverses every time an ion is reduced.",
          "The cathode polarity depends on the type of salt bridge used."],
         "Cathode polarity: Positive in Galvanic; Negative in Electrolytic (connected to DC negative terminal).")
    ]

    for diff_name, diff_ans, diff_wrongs, diff_expl in cell_differences:
        for st_diff in [
            "What is the fundamental difference regarding **'{}'**?",
            "In Grade 12 Technical Sciences, compare **'{}'**:",
            "Which comparative statement accurately distinguishes **'{}'**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Cell Comparisons", st_diff.format(diff_name), diff_ans, diff_wrongs, "Understanding", f"Compare {diff_name}", diff_expl)

    # Daniell Cell Specific Fundamentals (Easy)
    daniell_basics = [
        ("The Anode half-cell of a standard Daniell cell",
         "Zinc metal (Zn(s)) immersed in an aqueous zinc sulfate (ZnSO₄(aq)) solution, where zinc undergoes oxidation: Zn(s) → Zn²⁺(aq) + 2e⁻.",
         ["Copper metal immersed in copper sulfate solution undergoing reduction",
          "An inert graphite rod immersed in concentrated hydrochloric acid",
          "A lead plate coated with lead dioxide in sulfuric acid",
          "A platinum wire bubbling with hydrogen gas at 101.3 kPa",
          "Zinc metal undergoing reduction to gain electrons from solution",
          "Copper metal dissolving into copper ions and electrons"],
         "Daniell cell anode: Zn(s) in ZnSO₄(aq); oxidation: Zn(s) -> Zn²⁺(aq) + 2e⁻."),

        ("The Cathode half-cell of a standard Daniell cell",
         "Copper metal (Cu(s)) immersed in an aqueous copper(II) sulfate (CuSO₄(aq)) solution, where copper ions undergo reduction: Cu²⁺(aq) + 2e⁻ → Cu(s).",
         ["Zinc metal immersed in zinc sulfate undergoing oxidation",
          "An inert platinum plate bubbling with oxygen gas",
          "A silver wire immersed in concentrated nitric acid",
          "Copper metal dissolving to form blue copper sulfate crystals",
          "Copper metal acting as the negative terminal of the cell",
          "Zinc ions gaining electrons to deposit zinc onto copper"],
         "Daniell cell cathode: Cu(s) in CuSO₄(aq); reduction: Cu²⁺(aq) + 2e⁻ -> Cu(s)."),

        ("Direction of electron flow in the external wire of a Galvanic cell",
         "Electrons flow spontaneously through the external circuit from the ANODE (negative terminal) to the CATHODE (positive terminal).",
         ["Electrons flow from the cathode to the anode through the external wire.",
          "Electrons flow through the salt bridge from the cathode to the anode.",
          "Electrons alternate direction continuously like alternating current.",
          "Electrons flow from the copper cathode to the zinc anode.",
          "Electrons remain stationary while positive ions travel through the wire.",
          "Electrons only move when an external DC voltage is applied."],
         "In external wire: electrons always travel from ANODE to CATHODE."),

        ("Migration of anions and cations in the salt bridge of a Galvanic cell",
         "Negative ANIONS migrate towards the ANODE half-cell (to neutralize accumulating positive Zn²⁺ ions); positive CATIONS migrate towards the CATHODE half-cell (to replace consumed Cu²⁺ ions).",
         ["Cations migrate to the anode and anions migrate to the cathode.",
          "Both cations and anions migrate towards the negative anode exclusively.",
          "Electrons flow through the salt bridge from the zinc beaker to the copper beaker.",
          "Ions remain stationary in the gel while water molecules circulate.",
          "Anions migrate to the cathode while cations evaporate into the air.",
          "The salt bridge prevents all ion movement to protect the electrodes."],
         "In the salt bridge: Anions migrate to Anode; Cations migrate to Cathode, maintaining electrical neutrality.")
    ]

    for dan_name, dan_ans, dan_wrongs, dan_expl in daniell_basics:
        for st_dan in [
            "In a standard Daniell galvanic cell, identify **'{}'**:",
            "Which description accurately explains **'{}'**?",
            "What occurs at **'{}'** in a working Daniell cell?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Daniell Cell Basics", st_dan.format(dan_name), dan_ans, dan_wrongs, "Understanding", f"Explain {dan_name}", dan_expl)

    # Functions of salt bridge (Easy)
    salt_bridge_funcs = [
        ("Primary function 1: Completing the electrical circuit",
         "Allows the continuous flow of electrical charge by providing an ionic conduction pathway between the two separate electrolyte solutions.",
         ["Supplies free electrons directly to the external voltmeter",
          "Increases the external resistance of the load circuit to infinity",
          "Converts alternating current into smooth direct current",
          "Steps up the potential difference from 1.10 V to 230 V",
          "Pumps metallic copper atoms into the zinc half-cell",
          "Reverses the polarity of the electrodes every half cycle"]),

        ("Primary function 2: Maintaining electrical neutrality",
         "Neutralizes the buildup of excess positive charges in the anode half-cell and excess negative charges in the cathode half-cell by ionic diffusion.",
         ["Eliminates all chemical ions from both electrolyte solutions",
          "Causes the zinc anode to stop dissolving in the acid",
          "Forces electrons to travel through the liquid electrolyte",
          "Generates hydrogen gas bubbles to cool the cell",
          "Acts as a physical wall preventing any ion migration",
          "Prevents the voltmeter needle from moving"],)
    ]

    for sb_title, sb_ans, sb_wrongs in salt_bridge_funcs:
        for st_sb in [
            f"What is the significance of the salt bridge in terms of **{sb_title}**?",
            f"How does the salt bridge fulfill the role of **{sb_title}** in a galvanic cell?",
            f"Which statement describes the salt bridge's role in **{sb_title}**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Salt Bridge Functions", st_sb, sb_ans, sb_wrongs, "Understanding", f"Explain {sb_title}", sb_ans)

    # Electroplating and Industrial Electrolysis Basics (Easy)
    industrial_echem_easy = [
        ("Object to be electroplated (e.g. iron spoon to be coated with silver)",
         "Connected to the CATHODE (negative terminal) so that positive silver cations (Ag⁺) migrate towards it, accept electrons, and reduce to deposit a metallic silver coating: Ag⁺ + e⁻ → Ag(s).",
         ["Connected to the anode so that it dissolves into the electrolyte solution",
          "Connected to the salt bridge to equalize electrical neutrality",
          "Suspended between the electrodes without electrical contact",
          "Connected to the positive terminal of the DC battery",
          "Immersed in concentrated sulfuric acid without any electric current",
          "Connected to an AC mains supply so the coating alternates direction"],
         "Electroplating: The object to be coated is ALWAYS the CATHODE (negative terminal), where metal ions reduce and deposit: Mⁿ⁺ + ne⁻ -> M(s)."),

        ("Metal used for electroplating (e.g. pure silver bar)",
         "Connected to the ANODE (positive terminal) so that it oxidizes and dissolves continuously, replenishing the metal cations in the electrolyte: Ag(s) → Ag⁺ + e⁻.",
         ["Connected to the cathode where it receives deposited ions",
          "Placed inside the salt bridge to purify the electrolyte",
          "Connected to the negative terminal of the DC power pack",
          "Used as an inert non-reactive conductor that never dissolves",
          "Coated with plastic insulation to prevent current leakage",
          "Allowed to float on top of the liquid electrolyte"],
         "Electroplating anode: Made of the coating metal; oxidizes (dissolves) to replenish cations: M(s) -> Mⁿ⁺ + ne⁻."),

        ("Electrorefining of Impure Blister Copper",
         "Impure blister copper is placed at the ANODE (it oxidizes and dissolves: Cu → Cu²⁺ + 2e⁻); a thin sheet of pure copper is placed at the CATHODE (pure copper deposits: Cu²⁺ + 2e⁻ → Cu); impurities like gold and silver settle as valuable anode sludge.",
         ["Impure copper is placed at the cathode and pure copper at the anode",
          "Both electrodes are made of pure carbon graphite rods",
          "The electrolyte is pure distilled water without any copper salts",
          "The reaction occurs spontaneously without any DC power supply",
          "Valuable gold and silver impurities dissolve into the cathode sheet",
          "The process operates on alternating current at 50 Hz"],
         "Copper refining: Impure copper = Anode (+); Pure copper = Cathode (-); Electrolyte = acidified CuSO₄(aq). Anode sludge contains Au, Ag, Pt."),

        ("Chlor-Alkali Industry Products (Electrolysis of Brine)",
         "Electrolysis of concentrated sodium chloride solution (brine) produces THREE major commercial industrial chemicals: Chlorine gas (Cl₂ at anode), Hydrogen gas (H₂ at cathode), and aqueous Sodium Hydroxide (NaOH).",
         ["Produces metallic sodium metal, oxygen gas, and hydrochloric acid",
          "Produces solid salt crystals, distilled water, and ammonia gas",
          "Produces copper metal, sulfuric acid, and sulfur dioxide gas",
          "Produces methane gas, carbon monoxide, and sodium carbonate",
          "Produces ozone gas, liquid nitrogen, and sodium metal",
          "Produces hydrogen peroxide, chlorine gas, and molten sodium"],
         "Chlor-Alkali membrane cell products: Cl₂ gas (anode), H₂ gas (cathode), and NaOH(aq)."),

        ("Hall-Héroult Process (Extraction of Aluminium from Bauxite)",
         "Alumina (Al₂O₃) is dissolved in MOLTEN CRYOLITE (Na₃AlF₆) to lower its melting point from over 2000 °C to approximately 950 °C, drastically reducing electrical energy consumption.",
         ["Cryolite acts as a reducing agent that converts alumina into copper",
          "Cryolite prevents aluminium metal from sinking to the bottom",
          "Alumina is dissolved in concentrated sulfuric acid at room temperature",
          "Aluminium is extracted by displacement using solid scrap iron",
          "Cryolite converts alternating current into high-voltage direct current",
          "Cryolite eliminates the formation of any carbon dioxide emissions"],
         "Cryolite (Na₃AlF₆) dissolves alumina and lowers melting point from ~2072 °C to ~950 °C, saving massive energy.")
    ]

    for ind_name, ind_ans, ind_wrongs, ind_expl in industrial_echem_easy:
        for st_ind in [
            "In industrial electrochemistry, describe **'{}'**:",
            "What is the operational principle of **'{}'**?",
            "Which statement accurately explains **'{}'**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Industrial Electrolysis", st_ind.format(ind_name), ind_ans, ind_wrongs, "Understanding", f"Explain {ind_name}", ind_expl)

    # Standard Daniell Cell Voltage
    for q_volt in [
        "What is the standard cell potential (E°cell) of a standard Daniell cell (Zn-Cu) operating under standard conditions?",
        "Under standard conditions (1 mol·dm⁻³, 25 °C), the electromotive force (EMF) of a standard Zn-Cu cell is:",
        "Calculate the standard cell potential for the Daniell cell: Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s):",
        "The standard EMF delivered by a Zn-Cu galvanic cell on open circuit is:"
    ]:
        if counts["easy"] >= 300:
            break
        c_v = "+1.10 V"
        w_v = ["-1.10 V", "+0.42 V", "+2.20 V", "+0.76 V", "-0.34 V", "+1.50 V", "0.00 V"]
        expl_v = "E°cell = E°cathode - E°anode = E°(Cu²⁺/Cu) - E°(Zn²⁺/Zn) = (+0.34 V) - (-0.76 V) = +1.10 V."
        add_q("easy", "Daniell Cell Potential", q_volt, c_v, w_v, "Applying", "Calculate Daniell cell potential", expl_v)

    # Observations at electrodes during Daniell cell discharge (filling easy to 300)
    daniell_obs = [
        ("Zinc electrode observation", "The mass of the zinc electrode DECREASES (it erodes/dissolves) because zinc atoms oxidize to form aqueous ions: Zn(s) → Zn²⁺(aq) + 2e⁻."),
        ("Copper electrode observation", "The mass of the copper electrode INCREASES (a reddish-brown deposit forms) because copper ions reduce to form solid copper: Cu²⁺(aq) + 2e⁻ → Cu(s)."),
        ("Copper sulfate solution observation", "The blue color of the copper(II) sulfate solution FADES / DECREASES IN INTENSITY because blue Cu²⁺(aq) ions are consumed from solution during reduction."),
        ("Zinc sulfate solution observation", "The concentration of Zn²⁺(aq) ions INCREASES in the anode half-cell as zinc metal dissolves continuously into solution.")
    ]

    for obs_item, obs_desc in daniell_obs:
        for st_obs in [
            f"What physical observation is made regarding the **{obs_item}** as a Daniell galvanic cell operates?",
            f"During the continuous discharge of a Daniell cell, what occurs to the **{obs_item}**?",
            f"Which statement correctly records the experimental observation for the **{obs_item}**?"
        ]:
            if counts["easy"] >= 300:
                break
            c_obs = obs_desc
            w_obs = [
                "No observable change occurs because galvanic cells maintain constant electrode mass.",
                "The electrode dissolves into toxic chlorine gas bubbles.",
                "The blue color intensifies because copper ions are produced by the cathode.",
                "The electrode gains mass through absorption of sulfuric acid liquid.",
                "The electrode converts into a liquid mercury amalgam spontaneously.",
                "The solution turns bright yellow due to precipitation of sulfur powder."
            ]
            add_q("easy", "Cell Observations", st_obs, c_obs, w_obs, "Understanding", f"State observation for {obs_item}", obs_desc)

    # Oxidation Numbers and Rules (Easy)
    ox_number_examples = [
        ("pure zinc metal (Zn(s))", "0", "an uncombined neutral chemical element in its free elemental state always has an oxidation number of zero"),
        ("copper metal in solid copper wire (Cu(s))", "0", "atoms in any uncombined elemental metal have an oxidation number of 0"),
        ("oxygen gas (O2(g))", "0", "pure diatomic elemental molecules have an oxidation number of zero"),
        ("zinc ion in aqueous ZnSO4 (Zn2+)", "+2", "the oxidation number of a simple monatomic ion equals the electrical charge on the ion (+2)"),
        ("copper(II) ion in aqueous CuSO4 (Cu2+)", "+2", "for monatomic cations, the oxidation state corresponds to its positive ionic charge (+2)"),
        ("silver ion in aqueous AgNO3 (Ag+)", "+1", "the silver cation carries a single positive charge (+1)"),
        ("aluminium ion in AlCl3 (Al3+)", "+3", "the aluminium monatomic cation carries an ionic charge of +3"),
        ("chloride ion in NaCl or HCl (Cl-)", "-1", "monatomic halide anions have an oxidation number of -1"),
        ("oxide ion in metal oxides (O2-)", "-2", "oxygen in typical ionic and covalent compounds has an oxidation state of -2"),
        ("hydrogen in H2O or HCl", "+1", "hydrogen bonded to non-metals has an oxidation number of +1"),
        ("hydrogen in metal hydrides (e.g. NaH)", "-1", "hydrogen bonded to highly electropositive metals forms hydride ions with an oxidation number of -1"),
        ("oxygen in hydrogen peroxide (H2O2)", "-1", "in peroxides, each oxygen atom has an exceptional oxidation state of -1"),
        ("sulfur in the sulfate polyatomic ion (SO4^2-)", "+6", "in SO₄²⁻: S + 4(-2) = -2 => S - 8 = -2 => S = +6"),
        ("nitrogen in the nitrate ion (NO3^-)", "+5", "in NO₃⁻: N + 3(-2) = -1 => N - 6 = -1 => N = +5")
    ]

    for spec_name, ox_val, ox_reason in ox_number_examples:
        for st_ox in [
            f"What is the **OXIDATION NUMBER** of the indicated atom in **{spec_name}**?",
            f"Determine the correct oxidation state for **{spec_name}**:",
            f"According to oxidation number rules, identify the oxidation state in **{spec_name}**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_oxn = f"{ox_val}"
            w_oxn = [
                f"{int(ox_val) + 1:+d}" if ox_val != "0" else "+1",
                f"{int(ox_val) - 1:+d}" if ox_val != "0" else "-1",
                f"{int(ox_val) * 2:+d}" if ox_val not in ["0", "+1", "-1"] else "+2",
                f"{-int(ox_val):+d}" if ox_val != "0" else "-2",
                "+4",
                "-3",
                "+7"
            ]
            expl_oxn = f"Oxidation number of {spec_name} is {ox_val} because {ox_reason}."
            add_q("easy", "Oxidation Numbers", st_ox, c_oxn, w_oxn, "Applying", f"Determine oxidation number in {spec_name.split()[0]}", expl_oxn)

    # Direct Redox Identification in Chemical Equations (Easy)
    redox_equations_easy = [
        ("Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)", "Zinc metal (Zn(s))", "Copper(II) ions (Cu²⁺(aq))", "Zn(s)", "Cu²⁺(aq)"),
        ("Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g)", "Magnesium metal (Mg(s))", "Hydrogen ions (H⁺(aq))", "Mg(s)", "H⁺(aq)"),
        ("2Al(s) + 3Cu²⁺(aq) → 2Al³⁺(aq) + 3Cu(s)", "Aluminium metal (Al(s))", "Copper(II) ions (Cu²⁺(aq))", "Al(s)", "Cu²⁺(aq)"),
        ("Fe(s) + Sn²⁺(aq) → Fe²⁺(aq) + Sn(s)", "Iron metal (Fe(s))", "Tin(II) ions (Sn²⁺(aq))", "Fe(s)", "Sn²⁺(aq)"),
        ("Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s)", "Copper metal (Cu(s))", "Silver ions (Ag⁺(aq))", "Cu(s)", "Ag⁺(aq)"),
        ("Cl₂(g) + 2Br⁻(aq) → 2Cl⁻(aq) + Br₂(l)", "Bromide ions (Br⁻(aq))", "Chlorine gas (Cl₂(g))", "Br⁻(aq)", "Cl₂(g)"),
        ("2Na(s) + Cl₂(g) → 2NaCl(s)", "Sodium metal (Na(s))", "Chlorine gas (Cl₂(g))", "Na(s)", "Cl₂(g)")
    ]

    for eq_str, spec_ox, spec_red, red_agent, ox_agent in redox_equations_easy:
        if counts["easy"] >= 300:
            break
        # Substance oxidized
        q_sox = f"In the redox reaction represented by **{eq_str}**, which chemical substance undergoes **OXIDATION**?"
        c_sox = f"{spec_ox} (loses electrons; oxidation state increases)"
        w_sox = [
            f"{spec_red} (confused oxidation with reduction)",
            "The spectator sulfate counter-ions",
            "The external connecting copper wire",
            "The water solvent molecules",
            "The salt bridge electrolyte gel",
            "None of the species undergo oxidation"
        ]
        expl_sox = f"In {eq_str}, {spec_ox} loses electrons and is oxidized to form ions."
        add_q("easy", "Redox Equation Analysis", q_sox, c_sox, w_sox, "Understanding", f"Identify substance oxidized in {eq_str.split()[0]}", expl_sox)

        # Substance reduced
        if counts["easy"] < 300:
            q_sred = f"In the redox reaction **{eq_str}**, which chemical species undergoes **REDUCTION**?"
            c_sred = f"{spec_red} (gains electrons; oxidation state decreases)"
            w_sred = [
                f"{spec_ox} (confused reduction with oxidation)",
                "The solid metal electrode",
                "The salt bridge ions",
                "The glass beaker container",
                "Atmospheric nitrogen gas",
                "The DC power supply"
            ]
            expl_sred = f"In {eq_str}, {spec_red} gains electrons and is reduced."
            add_q("easy", "Redox Equation Analysis", q_sred, c_sred, w_sred, "Understanding", f"Identify substance reduced in {eq_str.split()[0]}", expl_sred)

        # Reducing agent
        if counts["easy"] < 300:
            q_rag = f"For the reaction **{eq_str}**, identify the **REDUCING AGENT**:"
            c_rag = f"{red_agent} (donates electrons to the other species)"
            w_rag = [
                f"{ox_agent} (confused reducing agent with oxidizing agent)",
                "The voltmeter instrument",
                "The spectator anion",
                "The potassium nitrate salt",
                "The water solvent",
                "The glass container"
            ]
            expl_rag = f"The reducing agent is the substance that is oxidized: {red_agent}."
            add_q("easy", "Redox Equation Analysis", q_rag, c_rag, w_rag, "Understanding", f"Identify reducing agent in {eq_str.split()[0]}", expl_rag)

    # Qualitative Practical Aspects of Electrochemistry (Easy)
    practical_echem = [
        ("Why Direct Current (DC) and NOT Alternating Current (AC) must be used for electroplating",
         "Direct current (DC) maintains fixed polarities (constant cathode and anode), ensuring that metal cations continuously migrate in one direction and deposit smoothly onto the object; alternating current (AC) reverses polarity 100 times every second, causing ions to alternately deposit and dissolve with no net plating.",
         ["AC electricity produces too much magnetic force that repels metal ions",
          "DC electricity has zero electrical resistance while AC has infinite resistance",
          "AC electricity destroys the chemical bonds of the plating metal completely",
          "DC electricity heats the electrolyte solution to boiling immediately",
          "AC mains voltage cannot pass through liquid electrolytes under any circumstances",
          "DC electricity converts the plating metal into an inert non-conductive plastic"],
         "Electroplating requires continuous unidirectional current (DC) so the cathode remains negative and ions deposit directionally."),

        ("Why an object must be thoroughly cleaned and degreased before electroplating",
         "To remove grease, oils, and oxide films that would physically block direct contact between metal ions and the conductive surface, ensuring a smooth, adherent, and uniform electroplated coating that does not peel off.",
         ["To prevent the object from dissolving into the acidic electrolyte",
          "To convert the base metal into a standard hydrogen electrode",
          "To allow the object to float stably on the surface of the bath",
          "To eliminate all electrical resistance from the base metal core",
          "To increase the potential difference of the DC power supply",
          "To prevent the electrolyte from producing hazardous chlorine gas"],
         "Grease and oxides act as insulators and prevent the plated layer from adhering to the metal surface."),

        ("Consequence of accidentally REVERSING the battery polarity during electroplating of an iron spoon with silver",
         "The iron spoon becomes the positive anode and oxidizes (dissolves / corrodes), while the silver bar becomes the cathode and silver deposits onto itself.",
         ["The silver bar dissolves twice as rapidly and coats the spoon with a double layer",
          "The cell immediately converts into a standard Daniell galvanic battery",
          "The electrolyte solution instantly freezes into solid crystalline ice",
          "No reaction whatsoever occurs because electroplating is irreversible",
          "The iron spoon is plated with gold rather than silver",
          "A dangerous nuclear chain reaction is triggered in the electrolyte"],
         "Reversing polarity makes the spoon the anode; the spoon oxidizes and dissolves, while silver deposits on the silver bar."),

        ("Function and significance of the Standard Hydrogen Electrode (SHE)",
         "A universal reference electrode assigned a standard potential of exactly 0.00 V (at 101.3 kPa, 1 mol·dm⁻³ H⁺, 25 °C), against which the standard reduction potentials (E°) of all other redox half-cells are measured and calibrated.",
         ["A portable commercial battery used to power electric motor vehicles",
          "A high-temperature furnace used to smelt aluminium from bauxite",
          "A device used exclusively to eliminate internal resistance in galvanic cells",
          "A safety switch designed to cut power when hydrogen gas accumulates",
          "An instrument that measures the electrical conductivity of pure water",
          "A fuel cell that produces zero greenhouse gas emissions"],
         "SHE: Pt(s) | H₂(g, 101.3 kPa) | H⁺(aq, 1 M) is the global benchmark assigned E° = 0.00 V.")
    ]

    for p_title, p_ans, p_wrongs, p_expl in practical_echem:
        for st_pe in [
            "In experimental Technical Sciences electrochemistry, explain: **{}**",
            "What is the scientific explanation for: **{}**?",
            "Which statement accurately evaluates: **{}**"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Practical Electrochemistry", st_pe.format(p_title), p_ans, p_wrongs, "Understanding", f"Explain {p_title}", p_expl)

    # Core Reference Values & Redox Table Hierarchy (Easy)
    table_hierarchy_easy = [
        ("The Standard Hydrogen Electrode (SHE) reference reduction potential", "0.00 V", ["+1.00 V", "-1.00 V", "+0.76 V", "-0.34 V", "+1.10 V", "+2.87 V", "-3.05 V"]),
        ("The strongest oxidizing agent on the standard reduction potentials table", "Fluorine gas (F2(g), E° = +2.87 V)",
         ["Lithium metal (Li(s))", "Hydrogen ions (H⁺(aq))", "Copper metal (Cu(s))", "Zinc ions (Zn²⁺(aq))", "Sodium metal (Na(s))", "Oxygen gas (O₂(g))"]),
        ("The strongest reducing agent on the standard reduction potentials table", "Lithium metal (Li(s), E° = -3.05 V)",
         ["Fluorine gas (F₂(g))", "Gold ions (Au³⁺(aq))", "Silver metal (Ag(s))", "Potassium ions (K⁺(aq))", "Chloride ions (Cl⁻(aq))", "Water molecules (H₂O)"]),
        ("Consequence of removing the salt bridge from an operating Galvanic cell",
         "The electric current drops immediately to ZERO (0 A) because the internal circuit is broken and charge accumulation ceases further reaction.",
         ["The cell potential doubles instantly to +2.20 V",
          "The zinc electrode dissolves ten times faster",
          "The cell converts into an alternating current generator",
          "Electrons begin to travel through the surrounding air",
          "The battery explodes due to excessive internal heat",
          "The voltmeter needle fluctuates wildly between positive and negative"]),
        ("Role of the high-resistance voltmeter in measuring Galvanic cell EMF",
         "Measures the maximum potential difference (electromotive force, EMF) across the cell terminals on open circuit when negligible current flows.",
         ["Measures the rate of flow of chemical ions across the salt bridge",
          "Supplies direct current to recharge the zinc anode",
          "Converts alternating current from the battery into direct current",
          "Steps up the cell voltage to standard mains voltage (230 V)",
          "Prevents oxidation from taking place at the zinc electrode",
          "Measures the temperature of the liquid electrolyte in degrees Celsius"])
    ]

    for th_title, th_ans, th_wrongs in table_hierarchy_easy:
        for st_th in [
            f"What is **{th_title}**?",
            f"According to the standard electrochemical series, identify **{th_title}**:",
            f"In Grade 12 Technical Sciences, identify **{th_title}**:"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Redox Table Hierarchy", st_th, th_ans, th_wrongs, "Remembering", f"Identify {th_title}", f"{th_title}: {th_ans}.")

    # Direct Easy Electrical Charge Calculations: Q = I * delta_t (Level 1 / Easy)
    charges_echem_easy = [
        (1.0, 60, "student demonstration cell"), (2.0, 30, "small plating bath"),
        (2.5, 40, "nickel plating beaker"), (3.0, 50, "copper voltameter"),
        (4.0, 30, "zinc refining cell"), (5.0, 20, "silver plating setup"),
        (5.0, 60, "lead storage cell"), (6.0, 45, "electrocleaning tank"),
        (8.0, 25, "galvanizing bath"), (10.0, 30, "chlor-alkali pilot cell"),
        (10.0, 60, "industrial electroplating bath"), (12.0, 50, "copper refining tank"),
        (15.0, 40, "tin plating line"), (20.0, 30, "aluminium smelting model")
    ]

    for curr_e, time_e, dev_e in charges_echem_easy:
        if counts["easy"] >= 300:
            break
        q_val_e = curr_e * time_e
        c_q_e = f"{q_val_e:.0f} C"
        w_q_e = [
            f"{curr_e / time_e:.3f} C",
            f"{time_e / curr_e:.1f} C",
            f"{q_val_e * 10:.0f} C",
            f"{q_val_e / 2:.0f} C",
            f"{q_val_e + 100:.0f} C",
            f"{curr_e * 96500:.0f} C",
            f"{q_val_e * 2:.0f} C"
        ]
        q_text_qe = f"A steady electric current of I = {curr_e:.1f} A is passed through a **{dev_e}** for a time period of Δt = {time_e} seconds. Calculate the total quantity of electric charge (Q) transferred through the cell:"
        expl_qe = f"Charge formula: Q = I × Δt = {curr_e:.1f} A × {time_e} s = {c_q_e}."
        add_q("easy", "Charge & Current in Electrolysis", q_text_qe, c_q_e, w_q_e, "Applying", f"Calculate charge for {dev_e}", expl_qe)

        # Finding current I = Q / t
        if counts["easy"] < 300:
            c_ie = f"{curr_e:.1f} A"
            w_ie = [
                f"{q_val_e * time_e:.0f} A",
                f"{time_e / q_val_e:.3f} A",
                f"{curr_e * 2:.1f} A",
                f"{curr_e / 2:.1f} A",
                f"{curr_e + 5.0:.1f} A",
                f"{q_val_e:.0f} A",
                f"{curr_e * 10:.1f} A"
            ]
            q_text_ie = f"A total electric charge of Q = {q_val_e:.0f} C passes through an electrolytic bath in Δt = {time_e} seconds. Determine the electric current (I):"
            expl_ie = f"Current: I = Q / Δt = {q_val_e:.0f} C / {time_e} s = {c_ie}."
            add_q("easy", "Charge & Current in Electrolysis", q_text_ie, c_ie, w_ie, "Applying", "Calculate current from charge and time", expl_ie)

    # Core Principles & Metal Displacement Rules (Easy)
    displacement_rules = [
        ("Why Zinc metal can displace Copper from Copper(II) sulfate solution, but Copper cannot displace Zinc",
         "Zinc is a stronger reducing agent (more negative standard reduction potential, E° = -0.76 V) than copper (E° = +0.34 V), meaning zinc oxidizes more readily and transfers electrons spontaneously to Cu²⁺ ions.",
         ["Copper has a higher electrical resistance than zinc in aqueous solutions",
          "Zinc has a lower atomic mass than copper so it floats on copper sulfate",
          "Copper is an inert noble gas that does not participate in chemical bonding",
          "Zinc ions attract water molecules with twice the hydration enthalpy of copper",
          "Copper reacts only when heated to 1000 °C in an electrolytic cell",
          "The sulfate anions prevent copper from releasing valence electrons"],
         "Zinc (E° = -0.76 V) is a stronger reducing agent than copper (E° = +0.34 V) and displaces Cu²⁺ spontaneously."),

        ("Why Magnesium metal reacts vigorously with dilute hydrochloric acid to produce hydrogen gas, while Copper metal does not react at all",
         "Magnesium has a negative standard reduction potential (E° = -2.36 V), making it a stronger reducing agent than hydrogen (E° = 0.00 V), so it reduces H⁺ to H₂ gas; copper has a positive reduction potential (E° = +0.34 V) and cannot reduce H⁺ ions.",
         ["Copper is protected by an impervious layer of copper carbonate varnish",
          "Hydrochloric acid neutralizes copper metal into pure water and salt",
          "Magnesium is an alkali metal that reacts explosively with all liquids",
          "Copper absorbs hydrogen gas rather than releasing it as bubbles",
          "Magnesium operates as an electrolytic cell when immersed in acid",
          "Copper only conducts electricity when cooled to absolute zero"],
         "Metals with E° < 0.00 V (like Mg) reduce H⁺ to H₂(g); metals with E° > 0.00 V (like Cu) cannot reduce H⁺."),

        ("Why the carbon anodes in the Hall-Héroult aluminium smelting cell must be replaced periodically",
         "The oxygen gas (O₂) liberated at the anode by the oxidation of oxide ions reacts with the carbon anodes at the high operating temperature (~950 °C) to form carbon dioxide gas (C + O₂ → CO₂), continuously consuming the carbon blocks.",
         ["The carbon anodes dissolve into molten aluminium to increase its hardness",
          "The carbon blocks melt into liquid carbon at 950 °C and drain away",
          "The electrical current converts carbon into radioactive graphite dust",
          "Cryolite liquid dissolves solid carbon chemically into sodium fluoride",
          "The carbon anodes absorb electrons until they shatter mechanically",
          "The carbon blocks are eroded by abrasive alumina powder scrubbing"],
         "At ~950 °C: C(s) + O₂(g) -> CO₂(g). The carbon anodes burn away and must be regularly replaced."),

        ("Why molten cryolite (Na3AlF6) is mixed with alumina (Al2O3) in the industrial extraction of aluminium",
         "To lower the melting point of alumina from over 2000 °C to approximately 950 °C and improve the electrical conductivity of the electrolyte, saving vast quantities of electrical energy.",
         ["To prevent molten aluminium from conducting electric current",
          "To act as a physical catalyst that converts aluminium into titanium",
          "To eliminate the need for any carbon anodes in the smelting pot",
          "To prevent the formation of any carbon dioxide emissions during smelting",
          "To increase the boiling point of aluminium metal above 5000 °C",
          "To convert alternating mains current into low-voltage direct current"],
         "Cryolite lowers the melting point from ~2072 °C to ~950 °C, dramatically cutting electricity consumption."),

        ("The nature and industrial value of 'Anode Slime / Anode Sludge' formed during copper refining",
         "Insoluble metallic impurities from the impure blister copper (such as gold, silver, and platinum) that do not oxidize at the operating cell potential, settling to the bottom as highly valuable precious metal sludge.",
         ["Toxic radioactive lead waste that must be buried in concrete bunkers",
          "Pure copper crystals that failed to adhere to the cathode sheet",
          "Solidified copper sulfate crystals that precipitated due to cooling",
          "Insoluble carbon soot particles produced by burning connecting cables",
          "A hazardous chemical gel that ruins the electrolytic refining tank",
          "Oxidized iron and zinc rust flakes that float on the liquid surface"],
         "Anode slime contains unoxidized precious metals (Au, Ag, Pt) that are refined for significant commercial value.")
    ]

    for dr_title, dr_ans, dr_wrongs, dr_expl in displacement_rules:
        for st_dr in [
            "In Technical Sciences electrochemistry, explain: **{}**",
            "What is the chemical explanation for: **{}**?",
            "Which statement accurately evaluates: **{}**"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Displacement Rules & Metallurgy", st_dr.format(dr_title), dr_ans, dr_wrongs, "Understanding", f"Explain {dr_title}", dr_expl)

    # Additional Direct Charge & Time Calculations (Easy)
    more_charges_easy = [
        (0.5, 120), (1.5, 60), (2.0, 90), (3.0, 120), (4.0, 60), (5.0, 90),
        (6.0, 60), (7.0, 30), (8.0, 45), (10.0, 90), (12.0, 30), (15.0, 60),
        (16.0, 45), (20.0, 45), (25.0, 20), (25.0, 40), (30.0, 20), (50.0, 10),
        (0.8, 150), (1.2, 80), (2.2, 100), (3.5, 80), (4.5, 50), (5.5, 40),
        (6.5, 30), (7.5, 40), (8.5, 60), (9.0, 50), (11.0, 40), (13.0, 30),
        (14.0, 25), (18.0, 20), (22.0, 30), (24.0, 25), (28.0, 15), (32.0, 10)
    ]

    for curr_m_e, time_m_e in more_charges_easy:
        if counts["easy"] >= 300:
            break
        q_m_val = curr_m_e * time_m_e
        c_qm = f"{q_m_val:.0f} C"
        w_qm = [
            f"{curr_m_e / time_m_e:.3f} C",
            f"{time_m_e / curr_m_e:.1f} C",
            f"{q_m_val * 2:.0f} C",
            f"{q_m_val / 2:.0f} C",
            f"{q_m_val + 50:.0f} C",
            f"{curr_m_e * 60:.0f} C",
            f"{q_m_val * 10:.0f} C"
        ]
        q_text_m_e = f"An electrochemist passes an electric current of I = {curr_m_e:.1f} A through an aqueous cell for Δt = {time_m_e} seconds. Calculate the total charge (Q) transferred:"
        expl_m_e = f"Q = I × Δt = {curr_m_e:.1f} A × {time_m_e} s = {c_qm}."
        add_q("easy", "Charge & Current in Electrolysis", q_text_m_e, c_qm, w_qm, "Applying", "Calculate charge in electrolysis", expl_m_e)

        if counts["easy"] < 300:
            c_im_val = f"{curr_m_e:.1f} A"
            w_im_val = [
                f"{q_m_val * time_m_e:.0f} A",
                f"{time_m_e / q_m_val:.3f} A",
                f"{curr_m_e * 2:.1f} A",
                f"{curr_m_e / 2:.1f} A",
                f"{curr_m_e + 4.0:.1f} A",
                f"{q_m_val:.0f} A",
                f"{curr_m_e * 5:.1f} A"
            ]
            q_text_im_e = f"A charge of Q = {q_m_val:.0f} C flows through an electroplating cell in Δt = {time_m_e} seconds. Determine the magnitude of the electric current (I):"
            expl_im_e = f"I = Q / Δt = {q_m_val:.0f} C / {time_m_e} s = {c_im_val}."
            add_q("easy", "Charge & Current in Electrolysis", q_text_im_e, c_im_val, w_im_val, "Applying", "Calculate current in electrolysis", expl_im_e)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Cell Potential Calculations: E°cell = E°cathode - E°anode, Cell Notation, Half-Reactions
    # =========================================================================

    # Standard Reduction Potential Table Data (Volts vs SHE)
    # Format: (Metal/species, Symbol, Oxidized form, Reduced form, E° standard reduction potential in Volts)
    redox_couples = [
        ("Fluorine", "F2/F-", "F2(g) + 2e-", "2F-(aq)", 2.87),
        ("Lead(IV) / Lead(II)", "PbO2/Pb2+", "PbO2(s) + 4H+ + 2e-", "Pb2+(aq) + 2H2O", 1.46),
        ("Chlorine", "Cl2/Cl-", "Cl2(g) + 2e-", "2Cl-(aq)", 1.36),
        ("Oxygen / Water", "O2/H2O", "O2(g) + 4H+ + 4e-", "2H2O", 1.23),
        ("Silver", "Ag+/Ag", "Ag+(aq) + e-", "Ag(s)", 0.80),
        ("Iron(III) / Iron(II)", "Fe3+/Fe2+", "Fe3+(aq) + e-", "Fe2+(aq)", 0.77),
        ("Iodine", "I2/I-", "I2(s) + 2e-", "2I-(aq)", 0.54),
        ("Copper", "Cu2+/Cu", "Cu2+(aq) + 2e-", "Cu(s)", 0.34),
        ("Standard Hydrogen Electrode (SHE)", "2H+/H2", "2H+(aq) + 2e-", "H2(g)", 0.00),
        ("Lead", "Pb2+/Pb", "Pb2+(aq) + 2e-", "Pb(s)", -0.13),
        ("Tin", "Sn2+/Sn", "Sn2+(aq) + 2e-", "Sn(s)", -0.14),
        ("Nickel", "Ni2+/Ni", "Ni2+(aq) + 2e-", "Ni(s)", -0.25),
        ("Iron", "Fe2+/Fe", "Fe2+(aq) + 2e-", "Fe(s)", -0.44),
        ("Chromium", "Cr3+/Cr", "Cr3+(aq) + 3e-", "Cr(s)", -0.74),
        ("Zinc", "Zn2+/Zn", "Zn2+(aq) + 2e-", "Zn(s)", -0.76),
        ("Aluminium", "Al3+/Al", "Al3+(aq) + 3e-", "Al(s)", -1.66),
        ("Magnesium", "Mg2+/Mg", "Mg2+(aq) + 2e-", "Mg(s)", -2.36),
        ("Sodium", "Na+/Na", "Na+(aq) + e-", "Na(s)", -2.71),
        ("Potassium", "K+/K", "K+(aq) + e-", "K(s)", -2.93),
        ("Lithium", "Li+/Li", "Li+(aq) + e-", "Li(s)", -3.05)
    ]

    # Galvanic Cell Pairings: Cathode has more positive E°, Anode has more negative E°
    # E°cell = E°cathode - E°anode
    pairings = []
    for i in range(len(redox_couples)):
        for j in range(i + 1, len(redox_couples)):
            cath = redox_couples[i]
            anod = redox_couples[j]
            # cath has higher E° than anod
            pairings.append((cath, anod))

    for cath, anod in pairings:
        if counts["medium"] >= 500:
            break
        c_name, c_sym, c_ox, c_red, c_e0 = cath
        a_name, a_sym, a_ox, a_red, a_e0 = anod
        e_cell = c_e0 - a_e0
        corr_ecell = f"+{e_cell:.2f} V" if e_cell > 0 else f"{e_cell:.2f} V"
        wrs_ecell = [
            f"-{e_cell:.2f} V (inverted anode and cathode potentials)",
            f"{c_e0 + a_e0:+.2f} V (added potentials instead of subtracting)",
            f"{a_e0 - c_e0:+.2f} V (E°anode - E°cathode)",
            f"{c_e0:+.2f} V (stated cathode potential only)",
            f"{a_e0:+.2f} V (stated anode potential only)",
            f"{e_cell * 2:+.2f} V",
            f"0.00 V (assumed equilibrium potential)"
        ]

        # 1. E°cell Calculation Question
        q_text_ecell = (f"A galvanic cell is constructed under standard conditions using a **{c_name} half-cell** (E° = {c_e0:+.2f} V) "
                        f"and a **{a_name} half-cell** (E° = {a_e0:+.2f} V). Calculate the standard cell potential (E°_cell):")
        expl_ecell = f"E°_cell = E°_cathode - E°_anode = ({c_e0:+.2f} V) - ({a_e0:+.2f} V) = {corr_ecell}."
        add_q("medium", "Standard Cell Potential Calculations", q_text_ecell, corr_ecell, wrs_ecell, "Applying", f"Calculate E°cell for {c_name}-{a_name} cell", expl_ecell)

        # 2. Identifying Cathode and Anode
        if counts["medium"] < 500:
            q_text_id = f"For the galvanic cell pairing **{c_name}** (E° = {c_e0:+.2f} V) and **{a_name}** (E° = {a_e0:+.2f} V), identify the CATHODE and ANODE:"
            corr_id = f"Cathode: {c_name} (more positive E°, reduction); Anode: {a_name} (more negative E°, oxidation)."
            wrs_id = [
                f"Cathode: {a_name}; Anode: {c_name}.",
                f"Both electrodes act as anodes simultaneously.",
                f"Both electrodes act as cathodes simultaneously.",
                f"Cathode: {a_name} (oxidation); Anode: {c_name} (reduction).",
                f"Cathode: {c_name} (oxidation); Anode: {a_name} (reduction).",
                f"Neither electrode can be identified without an external battery."
            ]
            expl_id = f"The half-cell with the more positive reduction potential acts as the CATHODE ({c_name}, E° = {c_e0:+.2f} V); the one with the more negative potential acts as the ANODE ({a_name}, E° = {a_e0:+.2f} V)."
            add_q("medium", "Electrode Identification", q_text_id, corr_id, wrs_id, "Understanding", f"Identify cathode/anode for {c_name}-{a_name}", expl_id)

        # 3. Standard Cell Notation
        if counts["medium"] < 500 and "/" in a_sym and "/" in c_sym and not ("O2" in a_sym or "O2" in c_sym or "PbO2" in c_sym or "Cl2" in c_sym or "F2" in c_sym):
            a_solid, a_ion = a_sym.split("/")[1], a_sym.split("/")[0]
            c_ion, c_solid = c_sym.split("/")[0], c_sym.split("/")[1]
            cell_not = f"{a_solid}(s) | {a_ion}(aq) || {c_ion}(aq) | {c_solid}(s)"
            q_text_not = f"Write the correct standard cell notation for the galvanic cell composed of **{a_name}** and **{c_name}**:"
            corr_not = cell_not
            wrs_not = [
                f"{c_solid}(s) | {c_ion}(aq) || {a_ion}(aq) | {a_solid}(s) (inverted anode and cathode)",
                f"{a_solid}(s) || {a_ion}(aq) | {c_ion}(aq) || {c_solid}(s)",
                f"{a_ion}(aq) | {a_solid}(s) || {c_solid}(s) | {c_ion}(aq)",
                f"{a_solid}(s) + {c_ion}(aq) → {a_ion}(aq) + {c_solid}(s)",
                f"{a_solid}(s) | {c_solid}(s) || {a_ion}(aq) | {c_ion}(aq)",
                f"{c_ion}(aq) | {c_solid}(s) || {a_solid}(s) | {a_ion}(aq)",
                f"{a_solid}(s) / {a_ion}(aq) // {c_ion}(aq) / {c_solid}(s)"
            ]
            expl_not = f"Standard cell notation convention: Anode | Anode electrolyte || Cathode electrolyte | Cathode -> {corr_not}."
            add_q("medium", "Cell Notation", q_text_not, corr_not, wrs_not, "Applying", f"Write cell notation for {a_name}-{c_name}", expl_not)

        # 4. Identifying Oxidizing and Reducing Agents
        if counts["medium"] < 500:
            q_text_agent = f"In the spontaneous reaction between **{c_name}** and **{a_name}**, identify the OXIDIZING AGENT and the REDUCING AGENT:"
            corr_agent = f"Oxidizing agent: {c_name} ions ({c_sym.split('/')[0]}); Reducing agent: {a_name} metal ({a_sym.split('/')[1] if '/' in a_sym else a_name})."
            wrs_agent = [
                f"Oxidizing agent: {a_name} metal; Reducing agent: {c_name} ions (inverted agents).",
                f"Both species act as reducing agents simultaneously.",
                f"Both species act as oxidizing agents simultaneously.",
                f"Oxidizing agent: the salt bridge electrolyte; Reducing agent: the external wire.",
                f"Oxidizing agent: {c_name} solid metal; Reducing agent: {a_name} aqueous ions.",
                f"Neither substance undergoes redox because cell potential is positive."
            ]
            expl_agent = f"The species reduced ({c_name} ions) is the oxidizing agent; the species oxidized ({a_name} metal) is the reducing agent."
            add_q("medium", "Oxidizing and Reducing Agents", q_text_agent, corr_agent, wrs_agent, "Understanding", f"Identify agents in {c_name}-{a_name}", expl_agent)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Industrial Electrolysis In-Depth, Non-Standard Conditions & Le Chatelier, Faraday Calculations
    # =========================================================================

    # 1. Industrial Electrolysis Details (Hard)
    chlor_alkali_hard = [
        ("Chlor-Alkali Membrane Cell Reactions and Mechanism",
         "At the titanium ANODE: 2Cl⁻(aq) → Cl₂(g) + 2e⁻ (oxidation of chloride ions to toxic green chlorine gas). At the nickel CATHODE: 2H₂O(l) + 2e⁻ → H₂(g) + 2OH⁻(aq) (reduction of water to hydrogen gas and hydroxide ions). The fluoropolymer cation-exchange membrane allows ONLY Na⁺ cations to migrate from anode to cathode compartment, producing pure NaOH(aq) free from chloride contamination.",
         ["Sodium ions are reduced at the cathode to form dangerous molten sodium metal",
          "Water is oxidized at the anode to produce oxygen gas and sulfuric acid",
          "The membrane allows chloride anions to migrate into the cathode chamber",
          "Chlorine gas is produced at the cathode while hydrogen gas evolves at the anode",
          "The process operates spontaneously without any external direct current supply",
          "The cell uses molten rock salt at 800 °C rather than aqueous brine solution"],
         "Membrane cell: Anode (Ti): 2Cl⁻ -> Cl₂ + 2e⁻. Cathode (Ni): 2H₂O + 2e⁻ -> H₂ + 2OH⁻. Na⁺ passes through membrane to form pure NaOH."),

        ("Why Hydrogen Gas (H2) and NOT Metallic Sodium (Na) is Produced at the Cathode in Brine Electrolysis",
         "Water (H₂O) has a much more positive reduction potential (E° = -0.83 V) than sodium ions (Na⁺, E° = -2.71 V); therefore, water is a stronger oxidizing agent and is much more easily reduced than sodium ions in aqueous solution.",
         ["Sodium metal forms first but reacts immediately with the titanium cathode",
          "Sodium ions have a positive charge and are repelled by the negative cathode",
          "Sodium ions are oxidized at the cathode rather than reduced",
          "Chlorine gas blocks sodium ions from physically touching the cathode surface",
          "The cation-exchange membrane absorbs all sodium ions permanently",
          "Sodium metal can only be reduced in an acidic electrolyte at pH below 1"],
         "In aqueous brine, H₂O (E° = -0.83 V) is reduced preferentially over Na⁺ (E° = -2.71 V) because H₂O is a much stronger oxidizing agent."),

        ("Hall-Héroult Aluminium Extraction: Cathode and Anode Reactions",
         "At the carbon/graphite CATHODE: Al³⁺ + 3e⁻ → Al(l) (reduction of aluminium ions to dense molten aluminium, which sinks to the bottom). At the carbon/graphite ANODES: 2O²⁻ → O₂(g) + 4e⁻ (oxidation of oxide ions); at the high operating temperature (~950 °C), the evolved oxygen reacts with the carbon anodes to form CO₂ (C + O₂ → CO₂), causing the anodes to burn away and requiring periodic replacement.",
         ["Aluminium ions are oxidized at the anode to form solid aluminium crust",
          "Oxygen gas is produced at the cathode and bubbles out harmlessly",
          "The carbon anodes are permanent and never need replacement during operation",
          "Cryolite is consumed continuously as the primary source of aluminium metal",
          "The cell operates at room temperature (25 °C) to save electrical energy",
          "Aluminium metal floats on top of the molten cryolite electrolyte"],
         "Hall-Héroult: Cathode: Al³⁺ + 3e⁻ -> Al(l). Anode: 2O²⁻ -> O₂ + 4e⁻; C + O₂ -> CO₂ (carbon anodes burn away and must be replaced)."),

        ("Why Solid Alumina (Al2O3) Cannot Be Electrolyzed Directly",
         "Solid Al₂O₃ has an extremely high melting point (~2072 °C) which is technically and economically impractical to maintain; moreover, solid alumina contains fixed ions in a rigid crystal lattice that cannot move, so it does not conduct electric current until melted or dissolved in molten cryolite.",
         ["Solid alumina is a superconductor that shorts out the electrical generators",
          "Solid alumina reacts explosively with carbon electrodes at room temperature",
          "Alumina contains no aluminium atoms until mixed with cryolite catalyst",
          "Solid alumina conducts electricity exclusively through free valence electrons",
          "Direct electrolysis of alumina would produce radioactive isotopes",
          "Solid alumina decomposes spontaneously into toxic sulfur trioxide gas"],
         "Solid Al₂O₃ has fixed ions (insulator) and melts at >2000 °C. Dissolving in cryolite at ~950 °C enables mobile ions and viable electrolysis.")
    ]

    for ind_h_title, ind_h_ans, ind_h_wrongs, ind_h_expl in chlor_alkali_hard:
        for st_ih in [
            "Critically analyze the chemical reactions and electrochemical principles of: **{}**",
            "In industrial Technical Sciences chemistry, examine: **{}**",
            "Which evaluation provides the complete, scientifically verified explanation of: **{}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Industrial Electrolysis In-Depth", st_ih.format(ind_h_title), ind_h_ans, ind_h_wrongs, "Evaluating", f"Analyze {ind_h_title}", ind_h_expl)

    # 2. Non-Standard Conditions and Le Chatelier's Principle on Cell EMF (Hard)
    # Zn(s) + Cu²⁺(aq) <=> Zn²⁺(aq) + Cu(s)
    le_chatelier_echem = [
        ("INCREASING the concentration of copper(II) ions [Cu2+] in the cathode half-cell of a Daniell cell",
         "The cell EMF INCREASES (E_cell > 1.10 V), because according to Le Chatelier's principle, increasing the reactant concentration [Cu²⁺] shifts the dynamic equilibrium forward (to the right), favoring the forward redox reaction.",
         ["The cell EMF decreases because higher ion concentration increases internal resistance",
          "The cell potential drops to exactly 0.00 V and the cell ceases to operate",
          "The cell converts into an electrolytic cell requiring external battery power",
          "The zinc electrode begins to gain mass while copper dissolves",
          "The concentration of [Cu²⁺] has zero effect on cell potential according to Nernst",
          "The polarity of the electrodes reverses immediately"],
         "Increasing reactant [Cu²⁺] shifts equilibrium forward -> cell EMF increases (E_cell > 1.10 V)."),

        ("INCREASING the concentration of zinc ions [Zn2+] in the anode half-cell of a Daniell cell",
         "The cell EMF DECREASES (E_cell < 1.10 V), because according to Le Chatelier's principle, increasing the product concentration [Zn²⁺] opposes the forward reaction and shifts equilibrium in the reverse direction.",
         ["The cell EMF increases because more zinc ions are available to carry current",
          "The cell EMF remains completely constant at +1.10 V regardless of concentration",
          "The copper electrode dissolves rapidly into the cathode electrolyte",
          "The cell potential doubles because zinc is the negative terminal",
          "The salt bridge explodes due to osmotic pressure buildup",
          "The cell reaction becomes irreversible and non-spontaneous"],
         "Increasing product [Zn²⁺] opposes forward reaction -> shifts equilibrium in reverse direction -> cell EMF decreases (E_cell < 1.10 V)."),

        ("What happens to the cell potential (EMF) when a Galvanic cell reaches chemical dynamic EQUILIBRIUM?",
         "The cell potential becomes exactly ZERO (E_cell = 0.00 V), the rate of the forward reaction equals the rate of the reverse reaction, and the cell can no longer deliver electrical energy (the battery is 'flat' or 'dead').",
         ["The cell potential reaches its maximum theoretical value (E_cell = +2.20 V)",
          "The cell potential alternates continuously between +1.10 V and -1.10 V",
          "The cell potential becomes negative and drives spontaneous reverse current",
          "All chemical reactions cease completely at the atomic level",
          "The internal resistance drops to zero and current becomes infinite",
          "The salt bridge dissolves completely into the two beakers"],
         "At equilibrium: rates of forward and reverse reactions are equal -> E_cell = 0.00 V (battery is flat/dead)."),

        ("Effect of increasing the SURFACE AREA of the electrodes in a Galvanic cell",
         "The cell EMF remains UNCHANGED (potential difference depends on the chemical nature of materials and concentration, not surface area), but the cell can deliver a LARGER CURRENT and operates for a LONGER DURATION because internal resistance decreases.",
         ["The cell EMF doubles because twice as many atoms are exposed to the electrolyte",
          "The cell EMF drops to zero because large electrodes short-circuit the cell",
          "The cell converts into an electrolytic cell due to excessive surface area",
          "The rate of electron flow through the salt bridge drops to zero",
          "The standard reduction potential of the metal becomes twice as positive",
          "The electrode dissolves twice as slowly at maximum current draw"],
         "Larger electrode surface area: E°cell remains unchanged, but internal resistance decreases -> cell can deliver higher current for longer duration.")
    ]

    for lc_title, lc_ans, lc_wrongs, lc_expl in le_chatelier_echem:
        for st_lc in [
            "Predict the electrochemical consequence based on Le Chatelier's principle: **{}**",
            "In advanced Grade 12 Technical Sciences, analyze: **{}**",
            "Which deduction correctly explains the effect of: **{}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Le Chatelier & Cell Potential", st_lc.format(lc_title), lc_ans, lc_wrongs, "Evaluating", f"Apply Le Chatelier to {lc_title}", lc_expl)

    # 3. Quantitative Electrolysis & Faraday Calculations (Hard)
    # Q = I * delta_t; n(e-) = Q / F (F = 96 500 C/mol)
    # Mass deposited: m = n(metal) * M, where n(metal) = n(e-) / valence
    faraday_calcs = [
        ("copper metal from CuSO4 (Cu2+ + 2e- → Cu, M = 63.5 g·mol⁻¹)", 2.0, 63.5, 2, [1.0, 2.5, 5.0, 8.0, 10.0, 15.0, 20.0, 25.0], [900, 1800, 2700, 3600, 5400, 7200]),
        ("silver metal from AgNO3 (Ag+ + e- → Ag, M = 108.0 g·mol⁻¹)", 1.0, 108.0, 1, [0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0], [600, 1200, 1800, 2400, 3600, 5400]),
        ("gold metal from KAu(CN)2 (Au3+ + 3e- → Au, M = 197.0 g·mol⁻¹)", 3.0, 197.0, 3, [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0], [900, 1800, 2700, 3600, 7200]),
        ("nickel metal from NiSO4 (Ni2+ + 2e- → Ni, M = 58.7 g·mol⁻¹)", 2.0, 58.7, 2, [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0], [1200, 1800, 2400, 3600, 7200]),
        ("zinc metal from ZnSO4 (Zn2+ + 2e- → Zn, M = 65.4 g·mol⁻¹)", 2.0, 65.4, 2, [2.5, 5.0, 7.5, 10.0, 15.0, 20.0], [1800, 2700, 3600, 5400, 7200]),
        ("chromium metal from CrO3 (Cr3+ + 3e- → Cr, M = 52.0 g·mol⁻¹)", 3.0, 52.0, 3, [5.0, 10.0, 15.0, 20.0, 25.0, 30.0], [1800, 3600, 5400, 7200]),
        ("tin metal from SnSO4 (Sn2+ + 2e- → Sn, M = 118.7 g·mol⁻¹)", 2.0, 118.7, 2, [1.0, 2.0, 3.0, 5.0, 8.0, 10.0], [1200, 1800, 3600, 5400]),
        ("aluminium metal from Al2O3 (Al3+ + 3e- → Al, M = 27.0 g·mol⁻¹)", 3.0, 27.0, 3, [20.0, 50.0, 100.0, 150.0, 200.0], [3600, 7200, 10800, 14400])
    ]

    for metal_desc, valence, mol_mass, z_val, curr_list, time_list in faraday_calcs:
        for i_amps in curr_list:
            for t_sec in time_list:
                if counts["hard"] >= 200:
                    break
                q_coulombs = i_amps * t_sec
                moles_e = q_coulombs / 96500.0
                moles_metal = moles_e / z_val
                mass_dep = moles_metal * mol_mass
                t_min = t_sec // 60
                corr_mdep = f"{mass_dep:.2f} g"
                wrs_mdep = [
                    f"{mass_dep * z_val:.2f} g (forgot to divide by electron valence z = {z_val})",
                    f"{mass_dep / z_val:.2f} g",
                    f"{mass_dep * 2:.2f} g",
                    f"{mass_dep / 2:.2f} g",
                    f"{q_coulombs:.0f} g (confused charge in Coulombs with mass in grams)",
                    f"{mass_dep + 5.0:.2f} g",
                    f"{mass_dep * 1.5:.2f} g"
                ]
                q_text_f = (f"During industrial electroplating, a steady electric current of I = {i_amps:.1f} A passes through an electrolytic bath containing "
                            f"**{metal_desc}** for a duration of Δt = {t_sec} s ({t_min} minutes). Given Faraday's constant F = 96 500 C·mol⁻¹, "
                            f"calculate the mass of metal deposited at the cathode:")
                expl_f = (f"1. Total charge: Q = I × Δt = {i_amps:.1f} A × {t_sec} s = {q_coulombs:.0f} C. "
                          f"2. Moles of electrons: n(e⁻) = Q / F = {q_coulombs:.0f} C / 96 500 C·mol⁻¹ = {moles_e:.4f} mol. "
                          f"3. Moles of metal: n(metal) = n(e⁻) / {z_val} = {moles_metal:.4f} mol. "
                          f"4. Mass deposited: m = n × M = {moles_metal:.4f} mol × {mol_mass:.1f} g·mol⁻¹ = {corr_mdep}.")
                add_q("hard", "Quantitative Electrolysis Calculations", q_text_f, corr_mdep, wrs_mdep, "Evaluating", f"Calculate mass deposited for {metal_desc.split()[0]}", expl_f)

                # Solving for time required: t = (m * z * F) / (I * M)
                if counts["hard"] < 200:
                    corr_time = f"{t_sec} s ({t_min} min)"
                    wrs_time = [
                        f"{t_sec * 2} s",
                        f"{t_sec // 2} s",
                        f"{int(t_sec * z_val)} s",
                        f"{t_sec + 300} s",
                        f"{int(q_coulombs)} s",
                        f"{int(t_sec * 1.5)} s",
                        f"{t_sec // 4} s"
                    ]
                    q_text_time = (f"How long (in seconds) must an electroplating current of I = {i_amps:.1f} A be passed through the solution of "
                                   f"**{metal_desc}** to deposit exactly {mass_dep:.2f} g of metal at the cathode? (F = 96 500 C·mol⁻¹):")
                    expl_time = (f"1. Moles of metal: n = {mass_dep:.2f} g / {mol_mass:.1f} g·mol⁻¹ = {moles_metal:.4f} mol. "
                                 f"2. Charge required: Q = n × z × F = {moles_metal:.4f} × {z_val} × 96 500 = {q_coulombs:.0f} C. "
                                 f"3. Time: Δt = Q / I = {q_coulombs:.0f} C / {i_amps:.1f} A = {corr_time}.")
                    add_q("hard", "Quantitative Electrolysis Calculations", q_text_time, corr_time, wrs_time, "Evaluating", f"Calculate time required to deposit {metal_desc.split()[0]}", expl_time)

    # 4. Chlor-Alkali Gas Volume Calculations (Hard)
    # 2Cl- -> Cl2 + 2e-; 1 mol Cl2 (22.4 dm3 at STP) = 2 * 96500 C = 193 000 C
    for i_ca in [10.0, 20.0, 50.0, 100.0, 200.0]:
        for t_ca in [1800, 3600, 7200]:
            if counts["hard"] >= 200:
                break
            q_ca = i_ca * t_ca
            n_cl2 = q_ca / (2.0 * 96500.0)
            vol_cl2 = n_cl2 * 22.4
            corr_vcl2 = f"{vol_cl2:.2f} dm³"
            wrs_vcl2 = [
                f"{vol_cl2 * 2:.2f} dm³ (forgot that 1 mol Cl₂ requires 2 moles of electrons)",
                f"{vol_cl2 / 2:.2f} dm³",
                f"{n_cl2:.2f} dm³ (confused moles of gas with volume in dm³)",
                f"{vol_cl2 * 10:.2f} dm³",
                f"{vol_cl2 + 5.0:.2f} dm³",
                f"{22.4:.2f} dm³",
                f"{vol_cl2 * 1.5:.2f} dm³"
            ]
            q_text_ca = (f"In a membrane cell for the chlor-alkali process, a steady current of I = {i_ca:.0f} A flows through concentrated brine for "
                         f"Δt = {t_ca} s ({t_ca // 60} minutes). Calculate the volume of dry CHLORINE GAS (Cl2) liberated at the anode at STP (Vm = 22.4 dm³·mol⁻¹):")
            expl_ca = (f"1. Charge: Q = I × Δt = {i_ca:.0f} A × {t_ca} s = {q_ca:.0f} C. "
                       f"2. Moles of Cl₂: n(Cl₂) = Q / (2 × 96 500 C·mol⁻¹) = {n_cl2:.4f} mol. "
                       f"3. Volume at STP: V = n × Vm = {n_cl2:.4f} mol × 22.4 dm³·mol⁻¹ = {corr_vcl2}.")
            add_q("hard", "Chlor-Alkali Gas Volumes", q_text_ca, corr_vcl2, wrs_vcl2, "Evaluating", "Calculate chlorine gas volume in chlor-alkali cell", expl_ca)

    return questions

if __name__ == '__main__':
    qs = build_electrochemistry()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_electrochemistry.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
