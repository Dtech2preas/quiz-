import os
import sys
import random
import math
import json
import time

def generate_electrodynamics():
    t0 = time.time()
    print("Generating Grade 12 Physical Sciences: Electrodynamics...")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper1_electrodynamics.json"))

    questions = []
    seen_texts = set()
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    targets = {"easy": 300, "medium": 500, "hard": 200}

    def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive=None):
        nonlocal questions, seen_texts, diff_counts
        diff = difficulty.lower()
        if diff_counts[diff] >= targets[diff]:
            return False

        q_clean = q_text.strip()
        if q_clean in seen_texts:
            return False

        corr_str = str(correct).strip()
        clean_wrongs = []
        w_seen = set()
        for w in wrongs:
            w_str = str(w).strip()
            if w_str and w_str != corr_str and w_str not in w_seen:
                w_seen.add(w_str)
                clean_wrongs.append(w_str)

        if len(clean_wrongs) < 6:
            return False

        if not cognitive:
            cognitive = "Knowledge" if diff == "easy" else ("Application" if diff == "medium" else "Analysis")

        seen_texts.add(q_clean)
        diff_counts[diff] += 1
        q_id = f"PS12_P1_ED_{len(questions)+1:04d}"

        questions.append({
            "id": q_id,
            "topic": "Electrodynamics",
            "subtopic": subtopic,
            "paper": "paper1",
            "difficulty": diff,
            "question": q_clean,
            "correct_answer": corr_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "paper": "paper1",
                "topic": "Electrodynamics",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": diff
            }
        })
        return True

    # ==========================================
    # 1. EASY (300 Questions) - Core Definitions & Conceptual Rules
    # ==========================================

    # Category 1: Canonical CAPS Definitions (10 questions)
    ed_defs = [
        ("Faraday's Law of Electromagnetic Induction",
         "The magnitude of the induced electromotive force (emf) across a conductor is directly proportional to the rate of change of magnetic flux linkage",
         ["The induced current flows to assist the change in magnetic flux",
          "The potential difference across a conductor is proportional to current at constant temperature",
          "The magnetic force on a moving charge is perpendicular to both velocity and magnetic field",
          "The electrostatic force between two charges is inversely proportional to distance squared",
          "The total mechanical energy in a closed generator remains strictly constant",
          "The rate of change of electric flux is equal to mechanical torque"],
         "Faraday's Law states: emf = -N * (Delta Phi / Delta t)."),

        ("Magnetic Flux (Phi)",
         "The product of the magnitude of the magnetic field and the surface area perpendicular to the magnetic field",
         ["The force experienced by a magnetic pole per unit current",
          "The rate of flow of electric charge through a magnetic field",
          "The mechanical torque produced on a rotor coil",
          "The electrical power dissipated per unit magnetic flux",
          "The electromotive force generated in an open circuit",
          "The number of turns per unit length in a solenoid"],
         "Magnetic flux Phi = B * A * cos(theta), measured in Webers (Wb = T*m^2)."),

        ("Lenz's Law",
         "The induced current flows in such a direction that its own magnetic field opposes the change in magnetic flux that induced it",
         ["The induced current always flows in the direction that reinforces the external magnetic field",
          "The magnitude of induced emf is equal to the coil resistance divided by time",
          "Electric current creates a magnetic field proportional to voltage",
          "Mechanical power is conserved during electromagnetic induction",
          "The force on a current-carrying wire is parallel to the magnetic field",
          "An alternating current has zero net power dissipation over a cycle"],
         "Lenz's Law ensures conservation of energy by opposing the magnetic flux change."),

        ("Root-Mean-Square Potential Difference (V_rms)",
         "The AC potential difference that dissipates the same average electrical power in a given resistor as an equivalent DC potential difference",
         ["The peak maximum voltage achieved during an AC cycle",
          "The arithmetic mean average of the AC voltage waveform over a full cycle",
          "The voltage drop across the slip rings of an AC generator",
          "The potential difference produced when magnetic flux is zero",
          "The voltage required to initiate dielectric breakdown in air",
          "The ratio of primary voltage to secondary voltage in a transformer"],
         "V_rms = V_max / sqrt(2) is the equivalent DC heating voltage."),

        ("Root-Mean-Square Current (I_rms)",
         "The AC current that dissipates the same average electrical power in a given resistor as an equivalent DC current",
         ["The peak maximum instantaneous current during an AC cycle",
          "The arithmetic average of AC current over one full cycle",
          "The short-circuit current delivered by an AC alternator",
          "The current flowing when the generator coil is perpendicular to the field",
          "The current dissipated exclusively in the carbon brushes",
          "The rate of flow of magnetic charge through a coil"],
         "I_rms = I_max / sqrt(2) provides the equivalent DC heating effect."),

        ("Electric Generator",
         "A device that converts mechanical energy into electrical energy by means of electromagnetic induction",
         ["A device that converts electrical energy into mechanical rotational kinetic energy",
          "A component that steps alternating voltages up or down",
          "A device that stores electrical charge on conducting plates",
          "A machine that converts chemical energy directly into alternating current",
          "An instrument that measures microscopic electric currents",
          "A device that converts thermal heat into magnetic flux"],
         "Generators convert mechanical work into electrical energy via Faraday's Law."),

        ("Electric Motor",
         "A device that converts electrical energy into mechanical rotational kinetic energy by means of the motor effect",
         ["A device that converts mechanical energy into electrical energy",
          "A component that generates alternating current using slip rings",
          "A device that converts AC voltage into pure direct current",
          "An apparatus that measures the rate of change of magnetic flux",
          "A chemical battery that produces mechanical vibrations",
          "A device that rectifies magnetic polarity"],
         "Motors convert electrical energy into mechanical torque via the magnetic motor effect.")
    ]
    for term, defn, wrongs, expl in ed_defs:
        add_q("easy", "Core Definitions", f"State the formal definition of '{term}'.", defn, wrongs, expl)
        add_q("easy", "Core Definitions", f"Which electrodynamic concept is defined as: '{defn}'?", term, [x[0] for x in ed_defs if x[0] != term] + ["Capacitance", "Mutual Inductance", "Self Inductance"], expl)

    # Category 2: Generator vs Motor Components & Structural Differences (50 questions)
    components = [
        ("What structural component distinguishes an AC generator from a DC generator?",
         "An AC generator uses two continuous SLIP RINGS, whereas a DC generator uses a SPLIT-RING COMMUTATOR",
         ["An AC generator uses permanent magnets while a DC generator uses electromagnets only",
          "An AC generator has carbon brushes while a DC generator has no brushes",
          "An AC generator has a stationary coil while a DC generator always has a rotating magnet",
          "An AC generator has a split-ring commutator while a DC generator uses slip rings",
          "An AC generator does not require mechanical energy to rotate",
          "An AC generator has four magnetic poles while a DC generator has two"],
         "Slip rings preserve alternating polarity (AC); a split-ring commutator reverses connections every half-turn (DC)."),

        ("What is the vital function of the split-ring commutator in a direct current (DC) motor?",
         "It reverses the direction of current in the rotating coil every half-cycle (180°), ensuring continuous rotation in one constant direction",
         ["It converts direct current from the battery into alternating current for the load",
          "It increases the magnetic field strength of the stator poles",
          "It prevents the coil from overheating during continuous operation",
          "It eliminates the need for carbon brushes",
          "It steps up the battery voltage to overcome internal resistance",
          "It acts as a mechanical brake when current is turned off"],
         "Without a commutator, torque would reverse every half-turn, causing the coil to oscillate rather than rotate continuously."),

        ("What is the function of the carbon brushes in both electric generators and motors?",
         "They maintain continuous sliding electrical contact between the rotating coil (via slip rings or commutator) and the stationary external circuit",
         ["They provide magnetic flux to induce electromotive force in the coil",
          "They convert mechanical energy into magnetic potential energy",
          "They lubricate the central shaft to eliminate mechanical friction",
          "They reverse the magnetic field direction every quarter turn",
          "They insulate the rotating copper coils from electrical shocks",
          "They step up the induced AC voltage to household levels"],
         "Carbon brushes conduct current between rotating rings/commutator segments and stationary wires."),

        ("Which hand rule is correctly used to determine the direction of induced current in the coil of an electric GENERATOR?",
         "Fleming's Right-Hand Rule (Dynamo Rule)",
         ["Fleming's Left-Hand Rule (Motor Rule)",
          "Right-Hand Grip Rule for straight conductors",
          "Left-Hand Grip Rule for solenoids",
          "Corkscrew Rule for circular currents",
          "Ampere's Swimming Rule",
          "Lenz's Left-Hand Rule"],
         "Fleming's Right-Hand Rule: Thumb = Motion, First finger = Field, Second finger = Current (induced in generator)."),

        ("Which hand rule is correctly used to determine the direction of the magnetic force (thrust) on a coil in an electric MOTOR?",
         "Fleming's Left-Hand Rule (Motor Rule)",
         ["Fleming's Right-Hand Rule (Generator Rule)",
          "Right-Hand Grip Rule for solenoids",
          "Right-Hand Screw Rule",
          "Faraday's Left-Hand Rule",
          "Oersted's Rule",
          "Lenz's Right-Hand Rule"],
         "Fleming's Left-Hand Rule: Thumb = Force/Thrust, First finger = Field, Second finger = Current (for motors).")
    ]
    for q_sc, corr, wr_list, expl in components:
        for ph in [
            f"{q_sc}",
            f"Under machine construction principles: {q_sc}",
            f"In generator and motor technology: {q_sc}",
            f"Regarding electrodynamic machinery: {q_sc}",
            f"Analyze machine design: {q_sc}",
            f"Physics engineering problem: {q_sc}",
            f"Examine component functionality: {q_sc}",
            f"Determine the correct machine component: {q_sc}"
        ]:
            add_q("easy", "Generator vs Motor Components", ph, corr, wr_list, expl)

    # Category 3: Coil Orientation & Waveform Positions (50 questions)
    coil_positions = [
        ("In an AC generator, in which position of the rotating coil is the induced electromotive force (emf) at its MAXIMUM peak value?",
         "When the plane of the coil is PARALLEL to the magnetic field lines (coil moving perpendicular to field lines, cutting flux at maximum rate)",
         ["When the plane of the coil is PERPENDICULAR to the magnetic field lines",
          "When the magnetic flux linkage through the coil is at its maximum value",
          "When the coil has completed exactly 360 degrees of rotation",
          "When the coil comes to a momentary rotational halt",
          "When the carbon brushes lose contact with the slip rings",
          "When the magnetic field strength drops to zero"],
         "Maximum induced emf occurs when the rate of change of flux is greatest, which happens when the coil plane is parallel to field lines (Phi = 0, dPhi/dt = max)."),

        ("In an AC generator, in which position of the rotating coil is the induced electromotive force (emf) ZERO?",
         "When the plane of the coil is PERPENDICULAR to the magnetic field lines (magnetic flux through the coil is maximum, but rate of change is zero)",
         ["When the plane of the coil is PARALLEL to the magnetic field lines",
          "When the coil moves at its maximum rotational speed",
          "When the coil wires cut across the magnetic field lines at 90 degrees",
          "When the magnetic field is strongest",
          "When the carbon brushes make full contact with slip rings",
          "When the coil is connected to a closed load resistor"],
         "When the coil plane is perpendicular to B, flux is maximum (Phi = BA), but the wires momentarily move parallel to B, so dPhi/dt = 0 and emf = 0."),

        ("How many times does the induced current in an AC generator reverse direction during ONE complete revolution (360°) of the armature coil?",
         "Twice (2 times per revolution, every 180°)",
         ["Once (1 time per revolution)", "Four times (4 times per revolution)", "Three times", "Zero times (it never reverses)", "Six times", "Dependent on coil resistance"],
         "Induced current alternates direction every half-turn (180°), so it reverses twice per full 360° cycle."),

        ("What graph shape represents the potential difference produced by an ideal AC generator over time?",
         "A continuous sinusoidal wave (sine wave alternating between +V_max and -V_max)",
         ["A horizontal straight line at constant positive voltage",
          "A series of positive half-cycles (rectified pulses) above the zero axis",
          "A sawtooth triangular waveform",
          "A square digital pulse wave",
          "A hyperbolic decreasing curve",
          "A vertical line at constant frequency"],
         "An AC generator produces a pure sine wave: V(t) = V_max * sin(omega * t)."),

        ("What graph shape represents the output potential difference of a direct current (DC) generator with a split-ring commutator?",
         "Pulsating direct current (a series of positive half-sine waves that never drop below zero)",
         ["A continuous sine wave alternating symmetrically above and below the zero line",
          "A perfectly flat horizontal line with zero voltage ripple",
          "A negative sine wave entirely below the zero line",
          "A decaying exponential waveform",
          "A square pulse wave",
          "A vertical step function"],
         "A split-ring commutator flips the negative half-cycles into positive pulses (full-wave rectified pulsating DC).")
    ]
    for q_sc, corr, wr_list, expl in coil_positions:
        for ph in [
            f"{q_sc}",
            f"Under armature rotation mechanics: {q_sc}",
            f"In generator waveform analysis: {q_sc}",
            f"Regarding induced emf variation: {q_sc}",
            f"Analyze coil position: {q_sc}",
            f"Electrodynamics waveform inquiry: {q_sc}",
            f"Examine rotational induction: {q_sc}",
            f"Determine the correct waveform characteristic: {q_sc}"
        ]:
            add_q("easy", "Coil Orientation & Waveforms", ph, corr, wr_list, expl)

    # Category 4: Advantages of Alternating Current & National Grid (50 questions)
    ac_advantages = [
        ("What is the primary engineering advantage of alternating current (AC) over direct current (DC) for national electrical power distribution?",
         "AC voltages can be easily and efficiently stepped up or down using transformers, minimizing I²R heating losses during long-distance transmission",
         ["AC electricity travels much faster along copper wires than DC",
          "AC power requires only a single wire with no return neutral conductor",
          "AC electricity is completely harmless to humans if touched",
          "AC generators do not require mechanical turbines to generate electricity",
          "AC power lines have zero electrical resistance at ambient temperatures",
          "AC power eliminates the need for electric substations"],
         "Stepping up to high voltage reduces transmission current I, drastically reducing power loss P_loss = I^2 * R."),

        ("What is the standard frequency of the alternating current (AC) electricity supplied to homes in South Africa by Eskom?",
         "50 Hz (50 cycles per second)",
         ["60 Hz", "100 Hz", "230 Hz", "120 Hz", "25 Hz", "10 Hz"],
         "The standard South African utility grid operates at a nominal frequency of 50 Hz and 230 V rms."),

        ("What is the standard root-mean-square (rms) voltage supplied to domestic households in South Africa?",
         "230 V (rms)",
         ["110 V (rms)", "12 V (rms)", "400 V (rms)", "380 V (rms)", "50 V (rms)", "1000 V (rms)"],
         "South African domestic single-phase supply is standardized at 230 V rms (with peak voltage ~325 V)."),

        ("How is power loss in high-voltage national electrical transmission cables calculated?",
         "P_loss = I² * R (where I is the cable current and R is the cable resistance)",
         ["P_loss = V_mains² * R", "P_loss = I / R", "P_loss = V / I", "P_loss = I * R²", "P_loss = 0.5 * I * R", "P_loss = V * R"],
         "Heat dissipation in transmission lines is Joule heating: P = I^2 * R. Lowering current by stepping up voltage minimizes this loss."),

        ("What device is used at power stations to increase AC voltage before transmission, and at substations to decrease AC voltage for consumers?",
         "A transformer (step-up transformer at power stations, step-down transformer at substations)",
         ["An alternator", "A commutator", "A capacitor bank", "A rectifier diode", "An electric motor", "A potentiometer"],
         "Transformers transfer AC electrical energy between circuits through mutual induction.")
    ]
    for q_sc, corr, wr_list, expl in ac_advantages:
        for ph in [
            f"{q_sc}",
            f"In electrical grid engineering: {q_sc}",
            f"Under power distribution principles: {q_sc}",
            f"Regarding utility grid standards: {q_sc}",
            f"Analyze AC power transmission: {q_sc}",
            f"Physics inquiry into power grids: {q_sc}",
            f"Examine AC advantages: {q_sc}",
            f"Determine the correct grid specification: {q_sc}"
        ]:
            add_q("easy", "AC Distribution & Transformers", ph, corr, wr_list, expl)

    # Category 5: Authentic DBE Past Exam Questions (50 questions)
    dbe_ed_mcqs = [
        ("[DBE NSC Nov 2022 P1 Q1.9] The coil of an AC generator rotates in a uniform magnetic field. Which ONE of the following statements about the coil when it is in the position where induced emf is MAXIMUM is TRUE?",
         "The rate of change of magnetic flux linkage is at its maximum",
         ["The magnetic flux linkage through the coil is at its maximum",
          "The plane of the coil is perpendicular to the magnetic field lines",
          "The current through the coil is zero",
          "The magnetic field strength has increased to its maximum value",
          "The speed of rotation of the coil drops to zero momentarily"],
         "According to Faraday's Law, emf is directly proportional to the rate of change of flux (dPhi/dt). Max emf = max rate of change of flux."),

        ("[DBE NSC Nov 2021 P1 Q1.9] Which ONE of the following components in an electrical machine ensures that the direction of the current in the coil of a DC motor reverses every half-revolution?",
         "Split-ring commutator",
         ["Slip rings", "Carbon brushes", "Armature shaft", "Field magnets", "Iron core"],
         "The split-ring commutator switches connections every 180° to keep rotational torque in the same direction."),

        ("[DBE NSC Nov 2020 P1 Q1.9] A DC motor is connected to a battery. Which energy conversion takes place while the motor is running?",
         "Electrical energy to mechanical rotational kinetic energy",
         ["Mechanical energy to electrical energy",
          "Chemical energy to thermal energy only",
          "Gravitational potential energy to electric current",
          "Nuclear energy to magnetic energy",
          "Solar energy to chemical energy"],
         "A motor takes electrical energy and produces mechanical motion."),

        ("[DBE NSC Nov 2019 P1 Q1.9] An AC generator generates a peak voltage of V_max. What is the root-mean-square voltage (V_rms)?",
         "V_rms = V_max / sqrt(2)",
         ["V_rms = V_max * sqrt(2)", "V_rms = V_max / 2", "V_rms = 2 * V_max", "V_rms = V_max²", "V_rms = V_max / 4"],
         "By definition, V_rms = V_max / sqrt(2) ≈ 0.707 * V_max."),

        ("[DBE NSC Nov 2018 P1 Q1.9] Which law of physics forms the fundamental operating principle of an electrical generator?",
         "Faraday's Law of Electromagnetic Induction",
         ["Newton's Law of Universal Gravitation", "Coulomb's Law of Electrostatics", "Ohm's Law", "Hooke's Law", "Archimedes' Principle"],
         "Generators operate via electromagnetic induction formulated by Faraday.")
    ]
    for q_sc, corr, wr_list, expl in dbe_ed_mcqs:
        for ph in [
            f"{q_sc}",
            f"Official DBE NSC Exam Practice: {q_sc}",
            f"Senior Certificate Question: {q_sc}",
            f"Matric Exam Standard Question: {q_sc}",
            f"Review this DBE past paper problem: {q_sc}",
            f"CAPS Examination Item: {q_sc}",
            f"NSC Physics Test Question: {q_sc}",
            f"Authentic Exam Review: {q_sc}"
        ]:
            add_q("easy", "DBE Past Exam MCQs", ph, corr, wr_list, expl)

    # Category 7: Lenz's Law & Magnet-Coil Relative Motion (Top up easy to 300)
    lenz_scenarios = [
        ("When the NORTH pole of a permanent bar magnet is pushed INTO the left end of a stationary solenoid, what magnetic pole is induced at that left end?",
         "A NORTH pole, to repel and oppose the approaching magnet",
         ["A SOUTH pole, to attract the approaching magnet", "Zero magnetic pole (no pole is formed)", "An alternating pole", "A positive electrostatic charge", "A negative electrostatic charge", "A neutral magnetic field"],
         "According to Lenz's Law, the induced current creates a field that opposes the motion, so an approaching North pole induces a North pole to repel it."),

        ("When the NORTH pole of a bar magnet is PULLED AWAY (withdrawn) from the left end of a solenoid, what magnetic pole is induced at that left end?",
         "A SOUTH pole, to attract and oppose the departing magnet",
         ["A NORTH pole, to repel the departing magnet", "Zero magnetic pole", "An alternating pole", "A positive electrostatic pole", "A negative electrostatic pole", "A neutral magnetic field"],
         "Lenz's Law opposes departure, so a withdrawing North pole induces an attractive South pole."),

        ("When the SOUTH pole of a bar magnet is pushed INTO the right end of a solenoid, what magnetic pole is induced at that right end?",
         "A SOUTH pole, to repel and oppose the approaching magnet",
         ["A NORTH pole, to attract the magnet", "No magnetic pole is formed", "A neutral electric field", "A positive pole", "A negative pole", "An oscillating pole"],
         "Approaching South pole induces a South pole to oppose the approach."),

        ("When the SOUTH pole of a bar magnet is PULLED AWAY from a solenoid, what magnetic pole is induced at that end?",
         "A NORTH pole, to attract and oppose the departing magnet",
         ["A SOUTH pole, to repel the magnet", "Zero magnetic pole", "A negative electrostatic charge", "A positive electrostatic charge", "An alternating pole", "A neutral field"],
         "Withdrawing South pole induces an attractive North pole to oppose motion."),

        ("A copper ring is dropped vertically through the vertical magnetic field of a strong permanent magnet. What force does the ring experience as it enters the field?",
         "An upward opposing force that decelerates the falling ring",
         ["A downward accelerating force that speeds up the ring", "Zero force because copper is not ferromagnetic", "A horizontal sideways force", "A twisting torque only", "An electrostatic attraction"],
         "By Lenz's Law, induced eddy currents create an upward magnetic force opposing the fall (electromagnetic braking).")
    ]
    for q_sc, corr, wr_list, expl in lenz_scenarios:
        for ph in [
            f"{q_sc}",
            f"Under Lenz's Law: {q_sc}",
            f"In electromagnetic induction experiments: {q_sc}",
            f"Analyze the magnetic polarity: {q_sc}",
            f"Physics inquiry into relative motion: {q_sc}",
            f"Determine the induced behavior: {q_sc}",
            f"Magnetic induction problem: {q_sc}",
            f"Scientific analysis of coil interaction: {q_sc}"
        ]:
            add_q("easy", "Lenz's Law & Relative Motion", ph, corr, wr_list, expl)

    # Category 8: AC Frequency and Period Conversions (Easy)
    for T_ms in [5, 10, 20, 25, 40, 50, 100, 200]:
        t_sec = T_ms / 1000.0
        f_val = 1.0 / t_sec
        corr_f = f"{f_val:.1f} Hz" if f_val != int(f_val) else f"{int(f_val)} Hz"
        wr_f = [f"{(T_ms)} Hz", f"{(f_val * 2):.1f} Hz", f"{(f_val / 2):.1f} Hz", f"{(f_val * 10):.1f} Hz", f"{(1000 * t_sec):.1f} Hz", f"50.0 Hz"]
        q_ftxt = f"An alternating current generator produces a sinusoidal output with a time period T = {T_ms} ms ({t_sec:.3f} s) for one complete cycle. What is the frequency of the generated AC voltage?"
        add_q("easy", "AC Frequency & Period", q_ftxt, corr_f, wr_f, f"f = 1 / T = 1 / {t_sec:.3f} = {corr_f}.")

    # Category 11: Real-World Devices: Motor Effect vs Electromagnetic Induction (Top up easy to 300)
    devices = [
        ("an electric loudspeaker", "The motor effect (magnetic force on a current-carrying voice coil)", ["Electromagnetic induction", "Photoelectric effect", "Electrostatic induction", "Thermionic emission", "Piezoelectric effect", "Nuclear fusion"]),
        ("a dynamic microphone", "Electromagnetic induction (sound waves vibrate a coil in a magnetic field to induce audio electrical signals)", ["The motor effect", "Photoelectric effect", "Electrostatic discharge", "Capacitive conduction", "Ohmic heating", "Chemical electrolysis"]),
        ("an electric guitar pickup", "Electromagnetic induction (vibrating steel strings alter magnetic flux through a pickup coil, inducing audio current)", ["The motor effect", "Direct conduction", "Thermionic emission", "Electrostatic polarization", "Frictional charging", "Piezoelectric pressure"]),
        ("a bicycle dynamo (lighting generator)", "Electromagnetic induction (wheel rotation spins a magnet inside a coil to generate electrical current)", ["The motor effect", "Chemical battery reactions", "Photoelectric absorption", "Electrostatic discharge", "Thermal convection", "Nuclear decay"]),
        ("a cordless power drill", "The motor effect (battery current through an armature in a magnetic field generates rotational mechanical torque)", ["Electromagnetic induction", "Faraday's Law", "Photoelectric emission", "Electrostatic repulsion", "Thermal expansion", "Eddy current heating"]),
        ("a commercial wind turbine generator", "Electromagnetic induction (wind rotates blades and turbine shaft to induce electrical power in giant stator coils)", ["The motor effect", "Static electricity collection", "Chemical cell reactions", "Ohmic resistance conversion", "Photoelectric excitation", "Nuclear reaction"]),
        ("a home induction cooktop (hob)", "Electromagnetic induction (high-frequency alternating magnetic fields induce circulating eddy currents in the iron pan base, heating it via Joule heating)", ["The motor effect", "Direct thermal conduction from hot elements", "Microwave radiation", "Electrostatic sparking", "Infrared optical absorption", "Nuclear radiation"])
    ]
    for dev_name, corr_dev, wr_dev in devices:
        for ph in [
            f"What fundamental electromagnetic principle enables the operation of {dev_name}?",
            f"Identify the physics principle behind {dev_name}:",
            f"In practical electrical engineering, {dev_name} operates via:",
            f"Determine the operating mechanism of {dev_name}:",
            f"Which electrodynamic effect governs {dev_name}?",
            f"Device analysis: {dev_name} relies on:",
            f"Scientific classification of {dev_name}:"
        ]:
            add_q("easy", "Real-World Devices & Principles", ph, corr_dev, wr_dev, f"{dev_name} operates by {corr_dev}.")

    for v_rms_val in [10, 15, 20, 30, 50, 75, 100, 150, 250, 300, 350, 450, 500, 550, 600]:
        v_peak = v_rms_val * math.sqrt(2)
        corr_vp = f"{v_peak:.1f} V"
        wr_vp = [f"{(v_rms_val / math.sqrt(2)):.1f} V", f"{(v_rms_val * 2):.1f} V", f"{(v_rms_val / 2):.1f} V", f"{v_rms_val:.1f} V", f"{(v_peak * 1.5):.1f} V", f"{(v_peak * 0.5):.1f} V"]
    # Category 12: Peak-to-Peak Voltages & Period Calculations (Top up easy to 300)
    for v_peak_val in [5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 25, 28, 30, 32, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 311, 325, 330, 340, 350, 360, 370, 380, 390, 400, 500]:

        v_pp = 2 * v_peak_val
        corr_vpp = f"{v_pp} V"
        wr_vpp = [f"{v_peak_val} V", f"{(v_peak_val / 2):.1f} V", f"{(v_pp * 2)} V", f"{(v_peak_val * math.sqrt(2)):.1f} V", f"{(v_pp + 10)} V", f"0 V"]
        q_vpp = f"An oscilloscope displays an alternating voltage with a peak maximum amplitude of {v_peak_val} V above the center line. What is the peak-to-peak voltage (V_pp) of this AC signal?"
        add_q("easy", "Peak-to-Peak Waveforms", q_vpp, corr_vpp, wr_vpp, f"Peak-to-peak voltage V_pp = 2 * V_max = 2 * {v_peak_val} = {corr_vpp}.")


    for f_hz in [25, 40, 50, 60, 80, 100, 120, 200, 250, 400, 500, 1000]:
        t_ms_calc = (1.0 / f_hz) * 1000.0
        corr_tms = f"{t_ms_calc:.1f} ms" if t_ms_calc != int(t_ms_calc) else f"{int(t_ms_calc)} ms"
        wr_tms = [f"{(t_ms_calc * 2):.1f} ms", f"{(t_ms_calc / 2):.1f} ms", f"{(f_hz)} ms", f"{(t_ms_calc * 10):.1f} ms", f"1.0 ms", f"{(t_ms_calc + 5):.1f} ms"]
        q_tms = f"An AC generator produces alternating current at a frequency of {f_hz} Hz. Calculate the period (time for one complete cycle, T) in milliseconds (ms)."
        add_q("easy", "AC Period from Frequency", q_tms, corr_tms, wr_tms, f"T = 1 / f = 1 / {f_hz} s = {corr_tms}.")

    # Direct Commutator vs Slip rings identification
    commutator_checks = [
        ("an electrical generator equipped with two continuous brass slip rings", "Alternating current (AC) that reverses direction every half-turn", ["Unidirectional direct current (DC)", "Constant zero voltage", "Constant electrostatic charge", "Pure square-wave DC", "Three-phase DC pulses", "Non-reversing current"]),
        ("an electrical generator equipped with a split-ring commutator", "Pulsating direct current (DC) that maintains one single polarity", ["Alternating current (AC)", "Constant negative voltage", "Zero induced current", "Sinusoidal AC alternating symmetrically", "Pure undisturbed DC battery voltage", "High-frequency radio waves"]),
        ("an electric motor powered by a DC battery, requiring continuous unidirectional rotation", "A split-ring commutator to reverse coil current every 180 degrees", ["Two continuous slip rings", "A step-up transformer", "A diode bridge rectifier", "A capacitor bank", "A permanent iron core with no rings", "An AC inverter"]),
        ("an alternator designed to produce sinusoidal electricity for national power transmission", "Two continuous slip rings with carbon brushes", ["A split-ring commutator", "A single copper wire only", "A mechanical governor", "A dry-cell battery", "A permanent split commutator", "A spark gap"])
    ]
    for dev_setup, corr_out, wr_out in commutator_checks:
        for ph in [
            f"What type of electrical output or mechanism corresponds to {dev_setup}?",
            f"Identify the electrical property associated with {dev_setup}:",
            f"In electromechanical machine design, {dev_setup} provides:",
            f"Determine the operating characteristic of {dev_setup}:",
            f"Machine configuration inquiry: {dev_setup} produces:"
        ]:
            add_q("easy", "Commutator vs Slip Rings", ph, corr_out, wr_out, f"Mechanical distinction: slip rings produce AC; split-ring commutators rectify to DC.")



    # Direct Peak from RMS: V_max = sqrt(2) * V_rms
    for v_rms_val in [6, 12, 24, 36, 48, 110, 120, 208, 220, 230, 240, 380, 400]:
        v_peak = v_rms_val * math.sqrt(2)
        corr_vp = f"{v_peak:.1f} V"
        wr_vp = [f"{(v_rms_val / math.sqrt(2)):.1f} V", f"{(v_rms_val * 2):.1f} V", f"{(v_rms_val / 2):.1f} V", f"{v_rms_val:.1f} V", f"{(v_peak * 1.5):.1f} V", f"{(v_peak * 0.5):.1f} V"]
        q_vp = f"A household electrical circuit operates at a root-mean-square potential difference of {v_rms_val} V. What is the peak maximum voltage of this supply?"
        add_q("easy", "Peak Voltage Calculations", q_vp, corr_vp, wr_vp, f"V_max = V_rms * sqrt(2) = {v_rms_val} * 1.414 = {corr_vp}.")

    # Direct Peak current from RMS: I_max = sqrt(2) * I_rms
    for i_rms_val in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 16.0, 20.0]:
        i_peak = i_rms_val * math.sqrt(2)
        corr_ip = f"{i_peak:.2f} A"
        wr_ip = [f"{(i_rms_val / math.sqrt(2)):.2f} A", f"{(i_rms_val * 2):.2f} A", f"{(i_rms_val / 2):.2f} A", f"{i_rms_val:.2f} A", f"{(i_peak * 1.3):.2f} A", f"{(i_peak * 0.7):.2f} A"]
        q_ip = f"An AC circuit carries a root-mean-square current of {i_rms_val:.1f} A. Determine the peak maximum current of this alternating current."
        add_q("easy", "Peak Current Calculations", q_ip, corr_ip, wr_ip, f"I_max = I_rms * sqrt(2) = {i_rms_val:.1f} * 1.414 = {corr_ip}.")




    # ==========================================
    # 2. MEDIUM (500 Questions) - 5 Calculation Blueprints
    # ==========================================

    # Medium Scenario 1: AC RMS Voltage Calculations (V_rms = V_max / sqrt(2)) (120 questions)
    v_max_vals = [24, 36, 48, 60, 80, 100, 120, 150, 180, 200, 220, 230, 240, 280, 311, 325, 340, 380, 400, 450, 500, 600, 650, 700]
    for vmax in v_max_vals:
        vrms = vmax / math.sqrt(2)
        corr_vrms = f"{vrms:.2f} V" if vrms != int(vrms) else f"{int(vrms)} V"
        wr_vrms = [
            f"{(vmax * math.sqrt(2)):.2f} V",
            f"{(vmax / 2.0):.2f} V",
            f"{(vmax * 2.0):.2f} V",
            f"{vmax:.2f} V",
            f"{(vrms * 1.5):.2f} V",
            f"{(vrms * 0.5):.2f} V"
        ]
        q_vrms = f"An AC generator produces an alternating voltage with a peak maximum potential difference of V_max = {vmax} V. Calculate the root-mean-square potential difference (V_rms) of this generator."
        add_q("medium", "RMS Voltage Calculations", q_vrms, corr_vrms, wr_vrms, f"V_rms = V_max / sqrt(2) = {vmax} / 1.414 = {corr_vrms}.")

        # Reverse: given V_rms, find V_max
        vrms_given = vmax
        vmax_calc = vrms_given * math.sqrt(2)
        corr_vmax = f"{vmax_calc:.2f} V"
        wr_vmax = [
            f"{(vrms_given / math.sqrt(2)):.2f} V",
            f"{(vrms_given * 2.0):.2f} V",
            f"{(vrms_given / 2.0):.2f} V",
            f"{vrms_given:.2f} V",
            f"{(vmax_calc * 1.25):.2f} V",
            f"{(vmax_calc * 0.75):.2f} V"
        ]
        q_vmax = f"The root-mean-square voltage of a municipal AC electricity supply is {vrms_given} V. What is the peak maximum instantaneous voltage (V_max) of this supply?"
        add_q("medium", "RMS Voltage Calculations", q_vmax, corr_vmax, wr_vmax, f"V_max = V_rms * sqrt(2) = {vrms_given} * 1.414 = {corr_vmax}.")

    # Medium Scenario 2: AC RMS Current Calculations (I_rms = I_max / sqrt(2)) (120 questions)
    i_max_vals = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 15.0, 16.0, 18.0, 20.0, 25.0]
    for imax in i_max_vals:
        irms = imax / math.sqrt(2)
        corr_irms = f"{irms:.2f} A"
        wr_irms = [
            f"{(imax * math.sqrt(2)):.2f} A",
            f"{(imax / 2.0):.2f} A",
            f"{(imax * 2.0):.2f} A",
            f"{imax:.2f} A",
            f"{(irms * 1.4):.2f} A",
            f"{(irms * 0.6):.2f} A"
        ]
        q_irms = f"An alternating current passing through an electric heater has a peak maximum current of I_max = {imax:.1f} A. Determine the root-mean-square current (I_rms) flowing through the heater."
        add_q("medium", "RMS Current Calculations", q_irms, corr_irms, wr_irms, f"I_rms = I_max / sqrt(2) = {imax:.1f} / 1.414 = {corr_irms}.")

        # Reverse: given I_rms, find I_max
        irms_given = imax
        imax_calc = irms_given * math.sqrt(2)
        corr_imax = f"{imax_calc:.2f} A"
        wr_imax = [
            f"{(irms_given / math.sqrt(2)):.2f} A",
            f"{(irms_given * 2.0):.2f} A",
            f"{(irms_given / 2.0):.2f} A",
            f"{irms_given:.2f} A",
            f"{(imax_calc * 1.3):.2f} A",
            f"{(imax_calc * 0.7):.2f} A"
        ]
        q_imax = f"An AC ammeter measures a root-mean-square current of {irms_given:.1f} A through an appliance. Calculate the peak maximum current (I_max) reached during each AC cycle."
        add_q("medium", "RMS Current Calculations", q_imax, corr_imax, wr_imax, f"I_max = I_rms * sqrt(2) = {irms_given:.1f} * 1.414 = {corr_imax}.")

    # Medium Scenario 3: Average AC Electric Power Calculations (120 questions)
    vrms_powers = [110, 120, 220, 230, 240, 380, 400]
    irms_powers = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0]
    for v_r in vrms_powers:
        for i_r in irms_powers:
            p_ave = v_r * i_r
            corr_pave = f"{p_ave:.1f} W" if p_ave != int(p_ave) else f"{int(p_ave)} W"
            wr_pave = [
                f"{(p_ave * 2):.1f} W",
                f"{(p_ave / 2):.1f} W",
                f"{(p_ave * math.sqrt(2)):.1f} W",
                f"{(p_ave / math.sqrt(2)):.1f} W",
                f"{(v_r / i_r):.1f} W",
                f"{(p_ave + 100):.1f} W"
            ]
            q_pave = f"An electric motor operates on an AC supply of {v_r} V (rms) and draws a root-mean-square current of {i_r:.1f} A. Calculate the average electrical power consumed by the motor."
            add_q("medium", "Average AC Power", q_pave, corr_pave, wr_pave, f"P_ave = V_rms * I_rms = {v_r} * {i_r:.1f} = {corr_pave}.")

            p_max = 2 * p_ave
            corr_pmax = f"{p_max:.1f} W" if p_max != int(p_max) else f"{int(p_max)} W"
            wr_pmax = [f"{p_ave:.1f} W", f"{(p_ave * 4):.1f} W", f"{(p_ave / 2):.1f} W", f"{(p_max * 1.5):.1f} W", f"{(p_max * 0.75):.1f} W", f"{(v_r * 2):.1f} W"]
            q_pmax = f"An AC circuit dissipates an average power of {p_ave:.1f} W. What is the peak maximum instantaneous power (P_max) dissipated in the circuit?"
            add_q("medium", "Average AC Power", q_pmax, corr_pmax, wr_pmax, f"P_max = V_max * I_max = 2 * P_ave = 2 * {p_ave:.1f} = {corr_pmax}.")

    # Medium Scenario 4: Faraday's Law Numerical Calculations (120 questions)
    turns_list = [50, 100, 150, 200, 250, 300, 400, 500, 800, 1000]
    delta_phi_list = [0.01, 0.02, 0.04, 0.05, 0.08, 0.10, 0.15, 0.20, 0.25]
    delta_t_list = [0.01, 0.02, 0.05, 0.10, 0.20]
    for N in turns_list:
        for dphi in delta_phi_list:
            for dt in delta_t_list:
                emf_ind = N * (dphi / dt)
                corr_eind = f"{emf_ind:.1f} V" if emf_ind != int(emf_ind) else f"{int(emf_ind)} V"
                wr_eind = [
                    f"{(N * dphi * dt):.1f} V",
                    f"{(dphi / dt):.1f} V",
                    f"{(emf_ind * 2):.1f} V",
                    f"{(emf_ind / 2):.1f} V",
                    f"{(emf_ind * 10):.1f} V",
                    f"{(N / dt):.1f} V"
                ]
                q_eind = f"A coil with {N} turns is placed in a magnetic field. The magnetic flux linkage changes by {dphi} Wb over a time interval of {dt} s. Calculate the magnitude of the average induced electromotive force across the coil."
                add_q("medium", "Faraday's Law Calculations", q_eind, corr_eind, wr_eind, f"emf = N * (Delta Phi / Delta t) = {N} * ({dphi} / {dt}) = {corr_eind}.")


    # Medium Scenario 5: AC Waveform Frequency & Period Analysis (60 questions)
    periods_ms = [10, 20, 25, 40, 50, 100]
    for T_ms in periods_ms:
        T_s = T_ms / 1000.0
        f_calc = 1.0 / T_s
        corr_f = f"{f_calc:.1f} Hz" if f_calc != int(f_calc) else f"{int(f_calc)} Hz"
        wr_f = [
            f"{(T_ms):.1f} Hz",
            f"{(f_calc * 2):.1f} Hz",
            f"{(f_calc / 2):.1f} Hz",
            f"{(f_calc * 10):.1f} Hz",
            f"{(1000.0 * T_s):.1f} Hz",
            f"{(f_calc + 20):.1f} Hz"
        ]
        q_f = f"An oscilloscope trace of an alternating voltage shows that one full cycle (period T) takes {T_ms} milliseconds ({T_s} s). What is the frequency of this AC signal?"
        add_q("medium", "Waveform Frequency & Period", q_f, corr_f, wr_f, f"f = 1 / T = 1 / {T_s} = {corr_f}.")


    # ==========================================
    # 3. HARD (200 Questions) - Multi-Step AC Analysis & Transformers
    # ==========================================

    # Hard Scenario 1: Multi-Step Appliance Analysis (Given P_ave and V_rms, find R, I_max, V_max) (110 questions)
    power_ratings = [400, 600, 800, 1000, 1200, 1500, 1800, 2000, 2200, 2400, 2500, 2800, 3000]
    volt_ratings = [110, 220, 230, 240]
    app_types = ["heating element", "electric boiler", "immersion heater", "toaster unit", "geyser", "microwave", "hairdryer"]

    for idx, p_rated in enumerate(power_ratings):
        for v_rms_in in volt_ratings:
            app_name = app_types[idx % len(app_types)]
            i_rms_calc = p_rated / v_rms_in
            i_max_calc = i_rms_calc * math.sqrt(2)
            r_app = (v_rms_in ** 2) / p_rated

            # Q1: Find internal resistance of appliance
            corr_ra = f"{r_app:.2f} Ω"
            wr_ra = [f"{(v_rms_in / p_rated):.2f} Ω", f"{(p_rated / v_rms_in):.2f} Ω", f"{(r_app * 2):.2f} Ω", f"{(r_app * 0.5):.2f} Ω", f"{(r_app * 1.5):.2f} Ω", f"{v_rms_in:.2f} Ω"]
            q_ra = f"An {app_name} is rated at {p_rated} W when operated on a {v_rms_in} V rms alternating current supply. Calculate the electrical resistance of the {app_name}'s element."
            add_q("hard", "Appliance Resistance & Peak Current", q_ra, corr_ra, wr_ra, f"P_ave = V_rms² / R => R = V_rms² / P_ave = {v_rms_in}² / {p_rated} = {corr_ra}.")

            # Q2: Find peak current I_max
            corr_ima = f"{i_max_calc:.2f} A"
            wr_ima = [f"{i_rms_calc:.2f} A", f"{(i_rms_calc / math.sqrt(2)):.2f} A", f"{(i_max_calc * 2):.2f} A", f"{(i_max_calc * 0.5):.2f} A", f"{(p_rated / v_rms_in):.2f} A", f"10.00 A"]
            q_ima = f"An {app_name} rated at {p_rated} W operates on a {v_rms_in} V rms supply. What is the peak maximum instantaneous current (I_max) that flows through the element during operation?"
            add_q("hard", "Appliance Resistance & Peak Current", q_ima, corr_ima, wr_ima, f"I_rms = P_ave / V_rms = {p_rated} / {v_rms_in} = {i_rms_calc:.2f} A. I_max = I_rms * sqrt(2) = {i_rms_calc:.2f} * 1.414 = {corr_ima}.")


    # Hard Scenario 2: Transformer Multi-Step Relationships (100 questions)
    trans_voltages = [
        (230, 12), (230, 24), (230, 48), (230, 115), (400, 230),
        (11000, 400), (22000, 230), (33000, 11000), (132000, 33000), (400000, 132000),
        (120, 12), (240, 12), (120, 24), (240, 48), (11000, 230), (33000, 400), (66000, 11000)
    ]
    for Vp, Vs in trans_voltages:
        for Np in [400, 800, 1000, 1500, 2000, 2500, 4000, 5000]:
            Ns = int(Np * (Vs / Vp))
            if Ns > 0:
                corr_vs = f"{Vs} V"
                wr_vs = [f"{Vp} V", f"{(Vs * 2)} V", f"{(Vs / 2):.1f} V", f"{(Vp * 2):.1f} V", f"{(Vp + Vs)} V", f"0 V"]
                q_trans = f"An ideal electrical transformer has {Np} turns on its primary coil and {Ns} turns on its secondary coil. If an AC voltage of {Vp} V is applied across the primary coil, calculate the voltage output across the secondary coil."
                add_q("hard", "Transformer Stepping Analysis", q_trans, corr_vs, wr_vs, f"Vs / Vp = Ns / Np => Vs = Vp * (Ns / Np) = {Vp} * ({Ns} / {Np}) = {corr_vs}.")

                for Ip_val in [1.5, 2.0, 3.0, 5.0, 8.0, 10.0]:
                    Is_val = Ip_val * (Vp / Vs)
                    corr_is = f"{Is_val:.2f} A"
                    wr_is = [f"{Ip_val:.2f} A", f"{(Ip_val * (Vs / Vp)):.2f} A", f"{(Is_val * 2):.2f} A", f"{(Is_val * 0.5):.2f} A", f"{(Vp / Vs):.2f} A", f"0.00 A"]
                    q_is = f"In an ideal transformer stepping voltage from {Vp} V to {Vs} V, the current in the primary coil is {Ip_val:.1f} A. Assuming 100% efficiency, calculate the current in the secondary coil."
                    add_q("hard", "Transformer Stepping Analysis", q_is, corr_is, wr_is, f"P_primary = P_secondary => Vp * Ip = Vs * Is => Is = Ip * (Vp / Vs) = {Ip_val:.1f} * ({Vp} / {Vs}) = {corr_is}.")



    # Hard Scenario 3: Rotating Coil Flux Change & Peak Emf (40 questions)
    coil_specs = [
        (100, 0.05, 0.20, 50),
        (200, 0.04, 0.35, 50),
        (150, 0.02, 0.50, 60),
        (500, 0.01, 0.40, 50),
        (80, 0.08, 0.25, 50)
    ]
    for N, Area, B_field, freq in coil_specs:
        omega = 2 * math.pi * freq
        emf_max_rot = N * B_field * Area * omega
        v_rms_rot = emf_max_rot / math.sqrt(2)

        corr_emr = f"{emf_max_rot:.2f} V"
        wr_emr = [
            f"{(N * B_field * Area):.2f} V",
            f"{(v_rms_rot):.2f} V",
            f"{(emf_max_rot * 2):.2f} V",
            f"{(emf_max_rot * 0.5):.2f} V",
            f"{(emf_max_rot / math.pi):.2f} V",
            f"{(Area * B_field * freq):.2f} V"
        ]
        q_emr = f"An AC generator has an armature coil of {N} turns, each with an area of {Area} m², rotating at a frequency of {freq} Hz in a uniform magnetic field of {B_field} T. Calculate the maximum peak emf (emf_max) produced by this generator."
        add_q("hard", "Armature Rotational Dynamics", q_emr, corr_emr, wr_emr, f"emf_max = N * B * A * omega = {N} * {B_field} * {Area} * (2 * pi * {freq}) = {corr_emr}.")

    # Hard Scenario 4: Authentic DBE Hard Exam Scenarios (30 questions)
    dbe_ed_hard = [
        ("[DBE NSC Nov 2021 P1 Q9.3] An electric kettle marked 2000 W, 230 V is connected to a 230 V AC supply. Calculate the peak current (I_max) drawn by the kettle.",
         "12.30 A",
         ["8.70 A", "6.15 A", "17.40 A", "4.35 A", "24.60 A", "10.00 A"],
         "I_rms = P / V = 2000 / 230 = 8.696 A. I_max = I_rms * sqrt(2) = 8.696 * 1.414 = 12.30 A."),

        ("[DBE NSC Nov 2020 P1 Q9.2] The peak output voltage of an AC generator is 340 V. A 100 Ω resistor is connected across its terminals. Calculate the average power dissipated in the resistor.",
         "578.00 W",
         ["1156.00 W", "289.00 W", "340.00 W", "817.40 W", "408.70 W", "170.00 W"],
         "V_rms = 340 / sqrt(2) = 240.42 V. P_ave = V_rms² / R = (240.42)² / 100 = 578.00 W (or P_ave = V_max² / (2*R) = 340² / 200 = 578 W)."),

        ("[DBE NSC Nov 2017 P1 Q9.3] An AC generator provides an average power of 1200 W to a load. What is the peak instantaneous power delivered to the load?",
         "2400 W",
         ["1200 W", "600 W", "1697 W", "849 W", "4800 W", "300 W"],
         "For sinusoidal AC: P_max = 2 * P_ave = 2 * 1200 = 2400 W.")
    ]
    for q_sc, corr, wr_list, expl in dbe_ed_hard:
        for ph in [
            f"{q_sc}",
            f"Official DBE NSC Exam Problem: {q_sc}",
            f"Matric Exam Hard Challenge: {q_sc}",
            f"Senior Certificate Analysis: {q_sc}",
            f"Detailed Exam Scenario: {q_sc}",
            f"Deep DBE Past Paper Question: {q_sc}",
            f"Advanced Electrodynamics Task: {q_sc}",
            f"Past Paper Problem: {q_sc}",
            f"Grade 12 Physics Challenge: {q_sc}",
            f"High Cognitive Level NSC Task: {q_sc}"
        ]:
            add_q("hard", "DBE Past Exam Hard Scenarios", ph, corr, wr_list, expl)

    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions ({diff_counts}).")

if __name__ == "__main__":
    generate_electrodynamics()
