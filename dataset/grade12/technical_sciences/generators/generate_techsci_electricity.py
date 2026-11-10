import json
import os

def build_electricity():
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
        qid = f"TS_P1_ELEC_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Electricity",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Electricity",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Ohm's Law, Factors Affecting Resistance, Series/Parallel Concepts
    # =========================================================================

    core_definitions = [
        ("Ohm's Law",
         "The potential difference across a conductor is directly proportional to the current in the conductor, provided its temperature remains constant (V ∝ I, or V = I * R).",
         ["The current in a conductor is directly proportional to its electrical resistance",
          "The potential difference across all branches in a parallel circuit is zero",
          "The electrical power dissipated in a resistor is proportional to time squared",
          "The resistance of a metallic wire is inversely proportional to its length",
          "The total emf of a battery is independent of the load connected across it",
          "The rate of flow of charge decreases as voltage increases"],
         "Ohm's Law states: Potential difference across a conductor is directly proportional to current, provided temperature remains constant: V = I * R."),

        ("Potential Difference (Voltage, V)",
         "The work done per unit positive charge in moving the charge between two points in an electric circuit (V = W / Q, measured in Volts, V, or J·C⁻¹).",
         ["The rate of flow of electric charge per second through a conductor",
          "The total resistance of all external resistors in a circuit",
          "The mechanical energy stored in a charged capacitor",
          "The magnetic force exerted on a moving electron beam",
          "The electrical power converted into heat per hour",
          "The number of coulombs passing through an ammeter per minute"],
         "Potential difference is defined as work done per unit charge: V = W / Q. 1 Volt = 1 Joule per Coulomb."),

        ("Electric Current (I)",
         "The rate of flow of electric charge through a cross-section of a conductor (I = Q / Δt, measured in Amperes, A, or C·s⁻¹).",
         ["The electrical potential energy carried by each individual electron",
          "The total opposition to the flow of charge in an electric circuit",
          "The maximum voltage delivered by a dry cell battery on open circuit",
          "The speed at which electromagnetic waves travel along copper cables",
          "The work required to move one coulomb across a resistor",
          "The power rating of a household electrical appliance in watts"],
         "Current is the rate of flow of charge: I = Q / Δt. 1 Ampere = 1 Coulomb per second."),

        ("Electrical Resistance (R)",
         "A material's opposition to the flow of electric charge (R = V / I, measured in Ohms, Ω, or V·A⁻¹).",
         ["The rate at which a battery generates electrical energy",
          "The capacity of an electric circuit to store electrostatic charge",
          "The magnetic flux density inside a current-carrying solenoid",
          "The maximum current that can safely pass through an ammeter",
          "The potential difference developed across open battery terminals",
          "The ratio of electric charge divided by operational time"],
         "Resistance is a conductor's opposition to current: R = V / I (measured in Ohms, Ω)."),

        ("Electromotive Force (EMF, ε)",
         "The maximum electrical potential energy transferred (supplied) by a battery per unit charge passing through it (measured in Volts across the terminals on an open circuit when no current flows).",
         ["The voltage drop across the internal resistance when full current flows",
          "The mechanical force that moves copper wires through magnetic fields",
          "The terminal potential difference measured when a short circuit occurs",
          "The total current delivered by a battery divided by its internal resistance",
          "The power dissipated by external resistors in a parallel bank",
          "The rate of chemical consumption of battery zinc electrodes"],
         "EMF (ε) is the total energy supplied by the source per coulomb of charge; it equals terminal voltage when zero current flows (open circuit)."),

        ("Internal Resistance (r)",
         "The resistance inside the battery or power source itself that opposes the flow of charge through the internal electrolyte and plates.",
         ["The external resistance of the load resistors connected in series",
          "The infinite resistance of an ideal digital voltmeter",
          "The resistance of connecting wires in a laboratory circuit board",
          "The opposition of air to the passage of high-voltage sparks",
          "The resistance of a semiconductor diode in reverse bias",
          "The resistance of an ammeter shunt resistor"],
         "Every practical chemical battery possesses internal resistance (r) due to its electrodes and chemical electrolyte."),

        ("Lost Volts (V_lost)",
         "The potential difference dropped across the battery's internal resistance when current flows through the circuit (V_lost = I * r = ε - V_terminal).",
         ["The voltage that escapes into the surrounding air via radiation",
          "The potential difference across the main switch when open",
          "The voltage drop across an ammeter of zero resistance",
          "The electric potential lost when a fuse blows in a house",
          "The voltage across parallel branches that carry zero current",
          "The reduction in battery EMF when ambient temperature drops"],
         "Lost volts represent the voltage used internally to push current through the battery itself: V_lost = I * r."),

        ("Kilowatt-Hour (kWh)",
         "A commercial unit of electrical energy equivalent to the energy consumed by an appliance with a power rating of 1 kilowatt operating continuously for 1 hour (1 kWh = 1 000 W * 3 600 s = 3.6 * 10⁶ J).",
         ["The power delivered by a 1 000-watt motor in one second",
          "The current flowing through a 1 000-ohm resistor at 230 V",
          "A unit of electrical capacitance used in power factor correction",
          "The rate of electrical energy generation per square meter of solar panel",
          "The monthly tariff charged by Eskom for transmission access",
          "The voltage required to push 1 ampere through 1 000 meters of wire"],
         "1 kWh is the commercial unit of energy: 1 kW × 1 hour = 1000 J/s × 3600 s = 3.6 × 10⁶ J (3.6 MJ).")
    ]

    stems = [
        "In Grade 12 Technical Sciences, how is **'{}'** defined?",
        "According to the examination guidelines, **'{}'** refers to:",
        "Which statement provides the exact CAPS definition for **'{}'**?",
        "Identify the correct scientific definition for **'{}'**:",
        "When an examiner asks for the definition of **'{}'**, which statement receives full marks?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Factors Affecting Resistance of a Conductor
    factors_resistance = [
        ("Length of the conductor (L)",
         "Resistance is directly proportional to length (R ∝ L): doubling the length of a wire doubles its resistance, because electrons collide with twice as many lattice ions.",
         ["Resistance is inversely proportional to length (R ∝ 1/L).",
          "Resistance is proportional to the square of length (R ∝ L²).",
          "Length has zero effect on the resistance of a metallic conductor.",
          "Longer wires have higher cross-sectional areas automatically.",
          "Doubling the length increases current by a factor of four.",
          "Longer wires become superconductors at room temperature."]),

        ("Cross-sectional area of the conductor (A)",
         "Resistance is inversely proportional to cross-sectional area (R ∝ 1/A): a thicker wire provides more parallel pathways for charge carriers, resulting in lower electrical resistance.",
         ["Resistance is directly proportional to cross-sectional area (R ∝ A).",
          "Thicker wires always have higher electrical resistance.",
          "Resistance is proportional to the square of the area (R ∝ A²).",
          "Cross-sectional area affects only magnetic flux, not resistance.",
          "Doubling the wire diameter doubles the electrical resistance.",
          "Thick wires eliminate all potential difference across circuits."]),

        ("Temperature of a metallic conductor",
         "As temperature increases, the resistance of a metal increases, because higher thermal energy causes the positive metal ions in the lattice to vibrate with greater amplitude, increasing the frequency of electron collisions.",
         ["Resistance decreases as temperature increases in pure metals.",
          "Temperature has zero effect on metallic electrical resistance.",
          "Higher temperature stops all electron movement in copper.",
          "The metal converts into an insulator at 50 °C.",
          "Heating a copper wire increases its cross-sectional area to reduce resistance to zero.",
          "Resistance drops to zero at the boiling point of water."]),

        ("Material type (Resistivity, ρ)",
         "Different materials have different intrinsic resistivities (R = ρ * L / A); copper and silver have very low resistivity (excellent conductors), while nichrome has high resistivity (used as heating elements).",
         ["All metals have exactly identical electrical resistivity.",
          "Resistivity depends on the length and diameter of the wire.",
          "Insulators have lower resistivity than metallic conductors.",
          "Nichrome wire has lower resistance than pure copper wire.",
          "Resistivity is measured in units of amperes per volt.",
          "Resistivity drops to zero in all materials when voltage is applied."])
    ]

    for factor_name, fact_desc, wr_facts in factors_resistance:
        add_q("easy", "Resistance Factors",
              f"How does the **{factor_name}** affect the electrical resistance of a conductor?",
              fact_desc, wr_facts, "Understanding", f"Explain effect of {factor_name.split()[0]} on resistance", fact_desc)

    # Series vs Parallel Circuit Fundamentals
    circuit_rules = [
        ("Current in a series circuit",
         "The electric current is the same at every point throughout a series circuit (I_total = I1 = I2 = I3).",
         ["Current splits equally across every resistor in series.",
          "Current decreases by half after passing through each series resistor.",
          "Current is highest near the positive terminal and drops to zero at the end.",
          "Current alternates direction continuously in a DC series circuit.",
          "Current is inversely proportional to battery EMF in series.",
          "Current increases as more resistors are connected in series."]),

        ("Potential difference in a parallel circuit",
         "The potential difference across each parallel branch is identical and equals the potential difference across the entire parallel combination (V_parallel = V1 = V2 = V3).",
         ["The potential difference divides equally across parallel branches.",
          "The branch with the largest resistor has the largest voltage drop.",
          "Potential difference is zero across all parallel branches.",
          "Voltage increases with each additional parallel branch connected.",
          "Potential difference is inversely proportional to branch resistance.",
          "Voltage drops to zero across the battery when branches are added."]),

        ("Effect of adding an extra resistor in PARALLEL to a circuit",
         "The total equivalent resistance of the circuit DECREASES, causing the total current delivered by the battery to INCREASE.",
         ["The total equivalent resistance increases, and total current decreases.",
          "The total equivalent resistance remains completely unchanged.",
          "The total current delivered by the battery drops to zero.",
          "The voltage across the battery doubles immediately.",
          "The circuit short-circuits and all current ceases to flow.",
          "The battery internal resistance drops to zero."]),

        ("Effect of adding an extra resistor in SERIES to a circuit",
         "The total equivalent resistance of the circuit INCREASES (R_total = R1 + R2 + ...), causing the total current delivered by the battery to DECREASE.",
         ["The total equivalent resistance decreases, and total current increases.",
          "The total current delivered by the battery remains unchanged.",
          "The voltage of the battery increases to maintain constant current.",
          "The power dissipated by the circuit doubles.",
          "The circuit converts into an AC circuit.",
          "The current divides between the series resistors."])
    ]

    for q_cr, c_cr, w_cr in circuit_rules:
        add_q("easy", "Circuit Rules", q_cr, c_cr, w_cr, "Understanding", "Understand series and parallel circuit behavior", c_cr)

    # Fill easy to exactly 300 with diverse, qualitative appliance ratings and electrical safety questions
    appliances = [
        ("electric water geyser", 3000.0, "high-power thermal heating element"),
        ("domestic electric kettle", 2000.0, "fast boiling thermal appliance"),
        ("microwave oven", 1200.0, "electromagnetic food heating appliance"),
        ("kitchen toaster", 900.0, "nichrome wire radiant heating element"),
        ("clothes washing machine", 500.0, "electric motor and water pump"),
        ("refrigerator compressor", 200.0, "cyclic cooling motor compressor"),
        ("desktop computer with monitor", 150.0, "electronic computing load"),
        ("flat-screen television", 100.0, "audio-visual display unit"),
        ("fluorescent tube light", 40.0, "gas discharge illumination lamp"),
        ("energy-saving LED lamp", 10.0, "high-efficiency semiconductor illumination")
    ]

    # Direct Easy Calculations: Q = I * delta_t, I = Q / delta_t
    charges_easy = [
        (0.5, 10, "small LED indicator"), (1.0, 20, "flashlight bulb"), (2.0, 15, "desk lamp"),
        (2.5, 30, "soldering iron"), (3.0, 60, "table fan"), (4.0, 45, "laptop charger"),
        (5.0, 12, "car headlamp"), (6.0, 50, "drill motor"), (8.0, 25, "battery charger"),
        (10.0, 30, "electric kettle element"), (12.0, 40, "portable heater"), (15.0, 20, "microwave oven"),
        (0.2, 50, "digital multimeter"), (0.4, 25, "microcontroller"), (1.5, 100, "aquarium pump"),
        (2.0, 180, "electric blanket"), (3.5, 40, "exhaust fan"), (5.0, 120, "television monitor"),
        (7.5, 60, "toaster element"), (16.0, 30, "workshop compressor")
    ]

    for curr_val, time_val, dev_desc in charges_easy:
        if counts["easy"] >= 300:
            break
        q_charge = curr_val * time_val
        c_q = f"{q_charge:.1f} C"
        w_q = [
            f"{curr_val / time_val:.3f} C (divided current by time)",
            f"{time_val / curr_val:.2f} C (divided time by current)",
            f"{q_charge * 10:.1f} C",
            f"{q_charge / 2:.1f} C",
            f"{q_charge + 50:.1f} C",
            f"{curr_val * 60:.1f} C",
            f"{time_val:.1f} C"
        ]
        q_text_q = f"A current of {curr_val:.1f} A passes through a {dev_desc} for {time_val} seconds. Calculate the quantity of electric charge (Q) that flows through the device:"
        expl_q = f"Charge formula: Q = I × Δt = {curr_val:.1f} A × {time_val} s = {c_q}."
        add_q("easy", "Electric Charge & Current", q_text_q, c_q, w_q, "Applying", "Calculate charge from current and time", expl_q)

        # Finding current I = Q / t
        if counts["easy"] < 300:
            c_i_val = f"{curr_val:.1f} A"
            w_i_val = [
                f"{q_charge * time_val:.1f} A (multiplied charge by time)",
                f"{time_val / q_charge:.3f} A (inverted: t / Q)",
                f"{curr_val * 2:.1f} A",
                f"{curr_val / 2:.1f} A",
                f"{curr_val + 5.0:.1f} A",
                f"{q_charge:.1f} A",
                f"{curr_val * 10:.1f} A"
            ]
            q_text_i_calc = f"A total charge of {q_charge:.1f} C flows through a cross-section of a wire connected to a {dev_desc} in {time_val} seconds. Determine the electric current (I):"
            expl_i_calc = f"Current formula: I = Q / Δt = {q_charge:.1f} C / {time_val} s = {c_i_val}."
            add_q("easy", "Electric Charge & Current", q_text_i_calc, c_i_val, w_i_val, "Applying", "Calculate current from charge and time", expl_i_calc)

    # Work done and potential difference: W = V * Q, V = W / Q
    for v_val in [3.0, 6.0, 9.0, 12.0, 24.0, 110.0, 230.0]:
        for q_val in [1.5, 2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 20.0]:
            if counts["easy"] >= 300:
                break
            w_work = v_val * q_val
            c_work = f"{w_work:.1f} J"
            w_work_wrongs = [
                f"{v_val / q_val:.2f} J (divided voltage by charge)",
                f"{q_val / v_val:.4f} J (divided charge by voltage)",
                f"{w_work * 2:.1f} J",
                f"{w_work / 2:.1f} J",
                f"{w_work + 50:.1f} J",
                f"{v_val:.1f} J",
                f"{w_work * 10:.1f} J"
            ]
            q_text_w = f"A charge of Q = {q_val:.1f} C moves between two points across a potential difference of V = {v_val:.1f} V. Calculate the electrical work done (W):"
            expl_w = f"Work done: W = V × Q = {v_val:.1f} V × {q_val:.1f} C = {c_work}."
            add_q("easy", "Work & Potential Difference", q_text_w, c_work, w_work_wrongs, "Applying", "Calculate electrical work done from voltage and charge", expl_w)

            if counts["easy"] < 300:
                c_v_calc = f"{v_val:.1f} V"
                w_v_wrongs = [
                    f"{w_work * q_val:.1f} V (multiplied work by charge)",
                    f"{q_val / w_work:.4f} V (inverted: Q / W)",
                    f"{v_val * 2:.1f} V",
                    f"{v_val / 2:.1f} V",
                    f"{v_val + 10.0:.1f} V",
                    f"{w_work:.1f} V",
                    f"{v_val * 1.5:.1f} V"
                ]
                q_text_v = f"An electric cell does {w_work:.1f} J of work to move a charge of {q_val:.1f} C through a circuit. Determine the potential difference (V) across the circuit:"
                expl_v = f"Potential difference: V = W / Q = {w_work:.1f} J / {q_val:.1f} C = {c_v_calc}."
                add_q("easy", "Work & Potential Difference", q_text_v, c_v_calc, w_v_wrongs, "Applying", "Calculate potential difference from work and charge", expl_v)

    # Electrical safety, meters and components
    safety_components = [
        ("Fuse",
         "A safety device containing a thin metal wire with a low melting point that melts and breaks the circuit when the electric current exceeds a predetermined safe limit.",
         ["A device that increases circuit voltage during peak hours",
          "A variable resistor used to control motor rotation speed",
          "A component that stores chemical energy for emergency power",
          "An instrument that measures the frequency of alternating current",
          "A semiconductor that converts heat directly into electricity",
          "A mechanical switch that connects domestic circuits to earth continuously"],
         "A fuse contains a thin wire that melts (blows) when excessive current passes through, interrupting current flow to prevent fire and damage."),

        ("Earth Wire (Green/Yellow conductor)",
         "A low-resistance safety conductor that connects the metal chassis of an electrical appliance to the ground, safely diverting fault currents to prevent human electric shock.",
         ["The wire carrying 230 V live current into the appliance",
          "The return path wire that completes the normal AC power circuit",
          "A wire that steps down the household voltage from 230 V to 12 V",
          "A conductor that prevents appliances from drawing electrical current",
          "A wire designed to increase the external load resistance",
          "A radio frequency grounding cable that improves television reception"],
         "The earth wire connects metallic casings to earth so that any live fault currents flow directly to ground, tripping the breaker rather than shocking a user."),

        ("Circuit Breaker",
         "An automatic electrical switch designed to protect an electrical circuit from damage caused by overload or short circuit by interrupting current flow mechanically.",
         ["A resistor that slows down the speed of electric current",
          "A device that increases electrical energy supply during loadshedding",
          "A transformer that converts AC voltage to direct voltage",
          "An electronic sensor that measures household energy consumption in kWh",
          "A device that boosts the battery EMF when voltage drops",
          "A cooling fan designed to reduce heat in distribution boards"],
         "A circuit breaker automatically trips and interrupts excessive current flow caused by overloads or short circuits."),

        ("Ideal Ammeter Connection and Resistance",
         "Connected in SERIES with the circuit component; an ideal ammeter has zero electrical resistance (0 Ω) so that it does not alter the total circuit current.",
         ["Connected in parallel with infinite resistance so no current passes through it",
          "Connected in parallel with zero resistance to short-circuit the load",
          "Connected in series with infinite resistance to prevent electron flow",
          "Connected across the battery terminals with high resistance",
          "Connected anywhere in the circuit with a standard 100 Ω resistance",
          "Connected only to the earth wire to measure stray currents"],
         "Ammeters must be placed in series and have near-zero resistance (0 Ω) so they do not reduce circuit current."),

        ("Ideal Voltmeter Connection and Resistance",
         "Connected in PARALLEL across the component; an ideal voltmeter has infinite electrical resistance (∞ Ω) so that it draws negligible current from the circuit.",
         ["Connected in series with zero resistance to allow maximum current",
          "Connected in series with infinite resistance to shut down current",
          "Connected in parallel with zero resistance to measure branch current",
          "Connected across the mains fuse with a 10 Ω resistance",
          "Connected to the earth pin with low internal resistance",
          "Connected in series across the power switch only"],
         "Voltmeters must be connected in parallel and possess near-infinite resistance (∞ Ω) so they do not bypass current from the component being measured."),

        ("Consequence of connecting an Ammeter in PARALLEL across a load",
         "Because an ammeter has nearly zero resistance, it creates a short circuit across the load, drawing excessive current that can damage the meter and power source.",
         ["It measures the potential difference across the load with extreme precision",
          "It increases the resistance of the circuit to infinity",
          "It causes the voltage across the circuit to double instantly",
          "It converts the load from a resistor into a capacitor",
          "It reduces the total current in the circuit to zero",
          "It causes no effect because ammeters work identically in series and parallel"],
         "An ammeter in parallel acts as a short circuit path because its resistance is zero, causing massive current flow and potential damage."),

        ("Consequence of connecting a Voltmeter in SERIES with a circuit load",
         "Because a voltmeter has extremely high (nearly infinite) resistance, the total circuit current drops to almost zero, causing lamps not to glow, while the voltmeter reads the full source EMF.",
         ["A massive short-circuit occurs and the fuse blows immediately",
          "The lamp glows twice as brightly due to amplified voltage",
          "The battery discharges completely in a matter of seconds",
          "The circuit current increases to its maximum possible value",
          "The voltmeter explodes due to excessive current flow",
          "The circuit resistance drops to zero ohms"],
         "A voltmeter in series adds infinite resistance to the circuit; virtually zero current flows, and the voltmeter indicates the battery EMF."),

        ("Ohmic vs Non-Ohmic Conductors",
         "An ohmic conductor maintains constant resistance at constant temperature obeying V = IR (linear I-V graph); a non-ohmic conductor (like a filament bulb or diode) has resistance that changes with voltage or temperature.",
         ["An ohmic conductor has infinite resistance at all times",
          "A non-ohmic conductor produces electricity without any source",
          "Ohmic conductors only conduct alternating current (AC)",
          "Non-ohmic conductors have a constant resistance regardless of temperature",
          "Ohmic conductors violate Ohm's law at high temperatures",
          "All metallic conductors are non-ohmic under standard conditions"],
         "Ohmic conductors produce a straight line on an I-V graph (R = constant). Non-ohmic conductors (like filament bulbs and diodes) have curves where resistance varies."),

        ("Color code of South African Three-Core Mains Cable",
         "Brown wire is Live (L), Blue wire is Neutral (N), and Green/Yellow striped wire is Earth (E).",
         ["Brown is Earth, Blue is Live, Green/Yellow is Neutral",
          "Blue is Live, Brown is Neutral, Green/Yellow is Earth",
          "Black is Live, White is Neutral, Red is Earth",
          "Red is Earth, Black is Neutral, Green is Live",
          "Green is Live, Yellow is Neutral, Blue is Earth",
          "All three wires carry identical 230 V live voltages"],
         "SABS/IEC standard: Brown = Live, Blue = Neutral, Green/Yellow striped = Earth.")
    ]

    for comp_name, comp_ans, comp_wrongs, comp_expl in safety_components:
        for st_comp in [
            "What is the function and operational principle of the **'{}'**?",
            "In electrical systems and circuit design, which description accurately explains the **'{}'**?",
            "Which statement correctly characterizes the role of the **'{}'**?",
            "Identify the correct technical fact regarding the **'{}'**:"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Safety & Meters", st_comp.format(comp_name), comp_ans, comp_wrongs, "Understanding", f"Explain {comp_name}", comp_expl)

    # Qualitative questions on factors affecting resistance
    wires_qual = [
        ("pure copper wire", "aluminum alloy wire", "copper has a lower electrical resistivity than aluminum"),
        ("nichrome heating wire", "copper connecting wire", "nichrome has a much higher resistivity and is designed to dissipate heat"),
        ("thick copper cable (4.0 mm²)", "thin copper wire (0.5 mm²)", "a larger cross-sectional area provides more pathways for free electrons, reducing resistance"),
        ("long 50-meter extension cord", "short 1-meter lead", "electrical resistance is directly proportional to conductor length (R ∝ L)"),
        ("red-hot glowing filament", "cold filament at room temperature", "elevated temperature increases lattice ion vibrations, causing more frequent electron collisions and higher resistance")
    ]

    for wire_a, wire_b, reason_wire in wires_qual:
        if counts["easy"] >= 300:
            break
        q_w_comp = f"Comparing a **{wire_a}** to an otherwise identical **{wire_b}**, why does the {wire_a} have a different electrical resistance?"
        c_w_comp = f"Because {reason_wire}."
        w_w_comp = [
            "Because voltage creates electrical charge inside longer wires.",
            "Because current always travels faster through thin wires than thick wires.",
            "Because resistance is completely independent of material or dimensions.",
            "Because thicker wires force electrons to travel in single file.",
            "Because cold wires have more vibrating ions than hot wires.",
            "Because shorter wires generate their own electromotive force."
        ]
        add_q("easy", "Conductor Properties", q_w_comp, c_w_comp, w_w_comp, "Understanding", "Compare resistance of conductors", f"R = ρ * L / A; {reason_wire}.")

    # Appliance power and energy concepts
    for app_name, p_rating, app_desc in appliances:
        for v_mains in [220, 230, 240]:
            for hrs_op in [1, 2, 5, 8]:
                if counts["easy"] >= 300:
                    break
                kwh_calc = (p_rating * hrs_op) / 1000.0
                q_text_app = f"A standard household **{app_name}** ({app_desc}) rated at {p_rating:.0f} W operates for {hrs_op} hour(s) on a {v_mains} V supply. How much electrical energy does it consume in kilowatt-hours (kWh)?"
                c_app = f"{kwh_calc:.2f} kWh"
                w_app = [
                    f"{p_rating * hrs_op:.0f} kWh (forgot to divide watts by 1000 to get kilowatts)",
                    f"{kwh_calc * 1000:.1f} kWh",
                    f"{kwh_calc / 2:.2f} kWh",
                    f"{kwh_calc * 2:.2f} kWh",
                    f"{hrs_op / (p_rating / 1000):.2f} kWh (divided time by power)",
                    f"{v_mains * hrs_op:.1f} kWh",
                    f"{kwh_calc + 5.0:.2f} kWh"
                ]
                expl_app = f"Energy (kWh) = Power (kW) × time (hours) = ({p_rating:.0f} / 1000 kW) × {hrs_op} h = {c_app}."
                add_q("easy", "Appliance Power Ratings", q_text_app, c_app, w_app, "Applying", f"Calculate energy consumption of {app_name}", expl_app)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Direct Calculations: V=IR, Series/Parallel Equivalent Resistance, Power P=VI=I²R=V²/R, Cost of Electricity
    # =========================================================================

    # 1. Ohm's Law Calculations: V = I * R => I = V / R => R = V / I
    resistor_vals = [2.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 100.0]
    voltages_med = [3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 24.0, 36.0, 48.0, 60.0, 120.0, 230.0]

    for r_res in resistor_vals:
        for v_volt in voltages_med:
            if counts["medium"] >= 500:
                break
            i_curr = v_volt / r_res
            corr_i = f"{i_curr:.2f} A"
            wrs_i = [
                f"{v_volt * r_res:.1f} A (multiplied voltage by resistance instead of dividing)",
                f"{r_res / v_volt:.4f} A (inverted Ohm's law: R / V)",
                f"{i_curr * 2:.2f} A",
                f"{i_curr / 2:.2f} A",
                f"{i_curr + 2.5:.2f} A",
                f"{v_volt:.1f} A",
                f"{i_curr * 1.5:.2f} A"
            ]
            q_text_ohm = f"An ohmic resistor of resistance R = {r_res:.1f} Ω is connected across a potential difference of V = {v_volt:.1f} V. Calculate the electric current (I) passing through the resistor:"
            expl_ohm = f"Ohm's Law: I = V / R = {v_volt:.1f} V / {r_res:.1f} Ω = {corr_i}."
            add_q("medium", "Ohm's Law Calculations", q_text_ohm, corr_i, wrs_i, "Applying", "Calculate current using Ohm's Law", expl_ohm)

            # Resistance from V and I
            if counts["medium"] < 500:
                corr_r = f"{r_res:.1f} Ω"
                wrs_r = [
                    f"{v_volt * i_curr:.1f} Ω (multiplied V by I)",
                    f"{i_curr / v_volt:.4f} Ω (inverted: I / V)",
                    f"{r_res * 2:.1f} Ω",
                    f"{r_res / 2:.1f} Ω",
                    f"{r_res + 10.0:.1f} Ω",
                    f"{v_volt:.1f} Ω",
                    f"{r_res * 1.4:.1f} Ω"
                ]
                q_text_r = f"When a potential difference of {v_volt:.1f} V is applied across an unknown heating coil, a current of {i_curr:.2f} A flows through it. Determine the resistance (R) of the coil:"
                expl_r = f"R = V / I = {v_volt:.1f} V / {i_curr:.2f} A = {corr_r}."
                add_q("medium", "Ohm's Law Calculations", q_text_r, corr_r, wrs_r, "Applying", "Calculate resistance from voltage and current", expl_r)

    # 2. Resistors in Parallel: 1/Rp = 1/R1 + 1/R2 => Rp = (R1 * R2) / (R1 + R2)
    parallel_pairs = [
        (4.0, 4.0), (6.0, 3.0), (10.0, 10.0), (12.0, 6.0), (12.0, 4.0), (20.0, 5.0),
        (20.0, 20.0), (30.0, 15.0), (30.0, 10.0), (40.0, 10.0), (50.0, 50.0), (60.0, 30.0),
        (60.0, 20.0), (100.0, 25.0), (100.0, 100.0)
    ]

    for r1, r2 in parallel_pairs:
        for v_batt in [6.0, 12.0, 24.0, 48.0]:
            if counts["medium"] >= 500:
                break
            rp = (r1 * r2) / (r1 + r2)
            itot = v_batt / rp
            corr_rp = f"{rp:.2f} Ω"
            wrs_rp = [
                f"{r1 + r2:.1f} Ω (added resistors in series instead of parallel)",
                f"{(r1 + r2) / 2:.2f} Ω (averaged the resistances)",
                f"{rp * 2:.2f} Ω",
                f"{rp / 2:.2f} Ω",
                f"{r1 * r2:.1f} Ω (multiplied without dividing by sum)",
                f"{rp + 4.0:.2f} Ω",
                f"{rp * 1.5:.2f} Ω"
            ]
            q_text_par = f"Two resistors of resistance R1 = {r1:.1f} Ω and R2 = {r2:.1f} Ω are connected in PARALLEL across an ideal {v_batt:.0f} V battery. Calculate the equivalent parallel resistance (R_p) of the circuit:"
            expl_par = f"Parallel resistance formula: 1/R_p = 1/R1 + 1/R2 => R_p = (R1 × R2) / (R1 + R2) = ({r1:.1f} × {r2:.1f}) / ({r1:.1f} + {r2:.1f}) = {r1 * r2:.1f} / {r1 + r2:.1f} = {corr_rp}."
            add_q("medium", "Parallel Resistance Calculations", q_text_par, corr_rp, wrs_rp, "Applying", "Calculate equivalent parallel resistance", expl_par)

            # Total current in parallel circuit
            if counts["medium"] < 500:
                corr_itot = f"{itot:.2f} A"
                wrs_itot = [
                    f"{v_batt / (r1 + r2):.2f} A (divided by series sum of resistances)",
                    f"{itot * 2:.2f} A",
                    f"{itot / 2:.2f} A",
                    f"{v_batt / r1:.2f} A (calculated current in branch 1 only)",
                    f"{v_batt / r2:.2f} A (calculated current in branch 2 only)",
                    f"{itot + 3.0:.2f} A",
                    f"{itot * 1.4:.2f} A"
                ]
                q_text_itot = f"For the same circuit with R1 = {r1:.1f} Ω and R2 = {r2:.1f} Ω connected in parallel across the {v_batt:.0f} V source, calculate the TOTAL CURRENT (I_total) supplied by the battery:"
                expl_itot = f"I_total = V / R_p = {v_batt:.0f} V / {rp:.2f} Ω = {corr_itot} (or I_total = I1 + I2 = {v_batt/r1:.2f} A + {v_batt/r2:.2f} A = {corr_itot})."
                add_q("medium", "Parallel Current Calculations", q_text_itot, corr_itot, wrs_itot, "Applying", "Calculate total current in parallel circuit", expl_itot)

    # 3. Commercial Electrical Cost Calculations:
    # Energy (kWh) = Power (kW) * time (hours); Cost = Energy (kWh) * Tariff (R/kWh)
    powers_kw = [0.5, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 3.5] # kW
    hours_run = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 24.0] # hours
    tariffs_r = [1.80, 2.20, 2.50, 2.80, 3.00, 3.50] # Rands per kWh

    for p_kw in powers_kw:
        for t_hrs in hours_run:
            for tariff in tariffs_r:
                if counts["medium"] >= 500:
                    break
                kwh_used = p_kw * t_hrs
                cost_rands = kwh_used * tariff
                corr_cost = f"R {cost_rands:.2f}"
                wrs_cost = [
                    f"R {cost_rands * 1000:.2f} (forgot to convert watts to kilowatts)",
                    f"R {kwh_used:.2f} (calculated kWh used without multiplying by tariff)",
                    f"R {cost_rands * 2:.2f}",
                    f"R {cost_rands / 2:.2f}",
                    f"R {(p_kw * 1000 * t_hrs * 3600 * tariff) * 1e-6:.2f}",
                    f"R {cost_rands + 15.0:.2f}",
                    f"R {cost_rands * 1.5:.2f}"
                ]
                q_text_cost = f"An electrical appliance rated at {p_kw:.1f} kW ({p_kw * 1000:.0f} W) is operated continuously for {t_hrs:.0f} hours. If electricity costs R {tariff:.2f} per kilowatt-hour (kWh), calculate the total cost of operating the appliance:"
                expl_cost = f"1. Energy consumed = Power (kW) × Time (hours) = {p_kw:.1f} kW × {t_hrs:.0f} h = {kwh_used:.2f} kWh. 2. Cost = Energy (kWh) × Tariff = {kwh_used:.2f} kWh × R {tariff:.2f} = {corr_cost}."
                add_q("medium", "Electricity Cost Calculations", q_text_cost, corr_cost, wrs_cost, "Applying", "Calculate cost of electrical energy", expl_cost)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Internal Resistance & EMF (ε = I(R + r)), Lost Volts, Series-Parallel Multi-Branch
    # =========================================================================

    # 1. Internal Resistance Calculations: ε = V_terminal + I * r => r = (ε - V_terminal) / I
    emfs = [6.0, 9.0, 12.0, 18.0, 24.0] # Volts
    internal_rs = [0.20, 0.40, 0.50, 0.60, 0.80, 1.0, 1.2, 1.5, 2.0] # Ohms
    external_loads = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0] # Ohms

    for emf_val in emfs:
        for r_int in internal_rs:
            for r_ext in external_loads:
                if counts["hard"] >= 200:
                    break
                tot_r = r_ext + r_int
                i_circ = emf_val / tot_r
                v_lost = i_circ * r_int
                v_term = emf_val - v_lost
                corr_rint = f"{r_int:.2f} Ω"
                wrs_rint = [
                    f"{(emf_val - v_term):.2f} Ω (calculated lost volts instead of internal resistance)",
                    f"{r_ext:.2f} Ω (external load resistance)",
                    f"{r_int * 2:.2f} Ω",
                    f"{r_int / 2:.2f} Ω",
                    f"{emf_val / i_circ:.2f} Ω (total circuit resistance R + r)",
                    f"{r_int + 0.8:.2f} Ω",
                    f"{r_int * 1.5:.2f} Ω"
                ]
                q_text_ir = f"A battery has an open-circuit electromotive force (EMF) of ε = {emf_val:.1f} V. When connected to an external load resistor of R = {r_ext:.1f} Ω, the terminal potential difference across the battery drops to V_terminal = {v_term:.2f} V, and a current of {i_circ:.2f} A flows. Calculate the internal resistance (r) of the battery:"
                expl_ir = f"1. Lost volts: V_lost = ε - V_terminal = {emf_val:.1f} V - {v_term:.2f} V = {v_lost:.2f} V. 2. Internal resistance: r = V_lost / I = {v_lost:.2f} V / {i_circ:.2f} A = {corr_rint}."
                add_q("hard", "Internal Resistance Calculations", q_text_ir, corr_rint, wrs_rint, "Evaluating", "Calculate battery internal resistance from EMF and load voltage", expl_ir)

                # Terminal Voltage Calculation: V_terminal = ε - I*r
                if counts["hard"] < 200:
                    corr_vterm = f"{v_term:.2f} V"
                    wrs_vterm = [
                        f"{emf_val:.1f} V (neglected internal resistance: assumed zero lost volts)",
                        f"{v_lost:.2f} V (calculated lost volts instead of terminal voltage)",
                        f"{emf_val + v_lost:.2f} V (added lost volts to EMF)",
                        f"{v_term * 1.5:.2f} V",
                        f"{v_term / 2:.2f} V",
                        f"{v_term + 2.5:.2f} V",
                        f"0.00 V"
                    ]
                    q_text_vt = f"A power supply of EMF ε = {emf_val:.1f} V and internal resistance r = {r_int:.2f} Ω is connected to a circuit drawing a current of {i_circ:.2f} A. Calculate the operating TERMINAL VOLTAGE (V_terminal) available to the external circuit:"
                    expl_vt = f"V_terminal = ε - I × r = {emf_val:.1f} V - ({i_circ:.2f} A × {r_int:.2f} Ω) = {emf_val:.1f} V - {v_lost:.2f} V = {corr_vterm}."
                    add_q("hard", "Terminal Voltage Calculations", q_text_vt, corr_vterm, wrs_vterm, "Evaluating", "Calculate terminal voltage taking internal resistance into account", expl_vt)

    # 2. Series-Parallel Complex Circuit Analysis:
    # Resistor R1 in series with a parallel pair (R2 // R3)
    # Total external R = R1 + (R2 * R3) / (R2 + R3)
    for r1 in [2.0, 3.0, 4.0, 5.0]:
        for r2 in [6.0, 12.0, 20.0]:
            for r3 in [3.0, 6.0, 5.0]:
                for v_source in [12.0, 18.0, 24.0]:
                    if counts["hard"] >= 200:
                        break
                    r_par = (r2 * r3) / (r2 + r3)
                    r_tot = r1 + r_par
                    i_main = v_source / r_tot
                    v_r1 = i_main * r1
                    v_par = i_main * r_par
                    i_branch2 = v_par / r2
                    corr_ibr2 = f"{i_branch2:.2f} A"
                    wrs_ibr2 = [
                        f"{i_main:.2f} A (assumed main current flows through branch 2)",
                        f"{i_main / 2:.2f} A (assumed equal current split)",
                        f"{v_source / r2:.2f} A (neglected series resistor R1)",
                        f"{i_branch2 * 2:.2f} A",
                        f"{i_branch2 / 2:.2f} A",
                        f"{i_branch2 + 1.2:.2f} A",
                        f"{i_branch2 * 1.5:.2f} A"
                    ]
                    q_text_sp = f"In a series-parallel circuit, resistor R1 = {r1:.1f} Ω is connected in series with a parallel combination of R2 = {r2:.1f} Ω and R3 = {r3:.1f} Ω across an ideal {v_source:.0f} V source. Calculate the electric current flowing through branch resistor R2:"
                    expl_sp = f"1. Parallel combination: R_p = ({r2:.1f} × {r3:.1f}) / ({r2:.1f} + {r3:.1f}) = {r_par:.2f} Ω. 2. Total resistance: R_tot = {r1:.1f} + {r_par:.2f} = {r_tot:.2f} Ω. 3. Total current: I_main = {v_source:.0f} V / {r_tot:.2f} Ω = {i_main:.2f} A. 4. Voltage across parallel bank: V_p = I_main × R_p = {i_main:.2f} A × {r_par:.2f} Ω = {v_par:.2f} V. 5. Current through R2: I2 = V_p / R2 = {v_par:.2f} V / {r2:.1f} Ω = {corr_ibr2}."
                    add_q("hard", "Series-Parallel Circuit Analysis", q_text_sp, corr_ibr2, wrs_ibr2, "Evaluating", "Calculate branch current in series-parallel circuit", expl_sp)

    return questions

if __name__ == '__main__':
    qs = build_electricity()
    out_dir = "dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_electricity.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
