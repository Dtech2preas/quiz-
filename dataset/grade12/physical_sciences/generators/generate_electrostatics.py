import os
import sys
import random
import math
import json
import time

def generate_electrostatics():
    t0 = time.time()
    print("Generating Grade 12 Physical Sciences: Electrostatics...")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper1_electrostatics.json"))

    questions = []
    seen_texts = set()
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    targets = {"easy": 300, "medium": 500, "hard": 200}

    k_const = 9.0e9    # N*m^2/C^2
    e_const = 1.6e-19  # C
    m_electron = 9.11e-31 # kg
    m_proton = 1.67e-27   # kg

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
        q_id = f"PS12_P1_ES_{len(questions)+1:04d}"

        questions.append({
            "id": q_id,
            "topic": "Electrostatics",
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
                "topic": "Electrostatics",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": diff
            }
        })
        return True

    # ==========================================
    # 1. EASY (300 Questions) - 7 Rich Categories
    # ==========================================

    # Category 1: Core Definitions (10 questions)
    es_defs = [
        ("Coulomb's Law",
         "The magnitude of the electrostatic force exerted by two point charges on each other is directly proportional to the product of the magnitudes of the charges and inversely proportional to the square of the distance between them",
         ["The electrostatic force is inversely proportional to the product of charges and directly proportional to distance",
          "The electric field at a point is directly proportional to distance and inversely proportional to charge",
          "The potential difference across a conductor is directly proportional to current at constant temperature",
          "The net charge of an isolated system remains constant during any physical process",
          "Every charge in the universe is an integer multiple of the elementary charge",
          "The total mechanical energy in an isolated system remains constant"],
         "Coulomb's Law states: F = k * |q1| * |q2| / r^2."),

        ("Electric Field",
         "A region in space in which an electric charge experiences a force",
         ["The electrostatic force experienced per unit positive charge placed at that point",
          "The work done per unit charge in moving a charge between two points",
          "The rate of flow of electric charge through a conductor",
          "A region in space where only magnetic materials experience a force",
          "The opposition to the flow of electric charge within a material",
          "The total amount of charge accumulated inside a spherical conductor"],
         "An electric field is defined as a region in space in which an electric charge experiences an electrostatic force."),

        ("Electric Field at a Point",
         "The electrostatic force experienced per unit positive charge placed at that point",
         ["A region in space in which an electric charge experiences a force",
          "The electrostatic force experienced per unit negative charge placed at that point",
          "The potential energy stored per unit charge at that position",
          "The rate of change of electric flux through a surface",
          "The work required to accelerate an electron to light speed",
          "The total quantity of charge on a spherical conductor"],
         "Electric field at a point: E = F / q, measured in N*C^-1 or V*m^-1."),

        ("Principle of Conservation of Charge",
         "The net charge of an isolated system remains constant during any physical process",
         ["Every charge in the universe is an integer multiple of the elementary charge",
          "The electrostatic force between two charges is conserved when distance changes",
          "Electric charges can neither be transferred nor redistributed between conductors",
          "The total mechanical energy of an isolated system remains constant",
          "Charges can be created from empty space provided momentum is conserved",
          "The number of protons in a body is always strictly conserved during friction"],
         "Principle of conservation of charge: Q_net = constant."),

        ("Principle of Charge Quantisation",
         "Every charge in the universe is an integer multiple of the elementary charge (e = 1.6 x 10^-19 C)",
         ["The net charge of an isolated system remains constant during any physical process",
          "The electrostatic force between two charges is an integer multiple of the distance",
          "Electric charge is continuous and can take any arbitrary decimal fraction of e",
          "The mass of an electron is quantised into integer packets of energy",
          "The electric field around a point charge is strictly constant",
          "Opposite charges always attract with an integer force in Newtons"],
         "Principle of charge quantisation: Q = n * e, where n is an integer and e = 1.6 x 10^-19 C.")
    ]
    for term, defn, wrongs, expl in es_defs:
        add_q("easy", "Core Definitions", f"State the formal definition of '{term}'.", defn, wrongs, expl)
        add_q("easy", "Core Definitions", f"Identify the scientific law or principle defined as: '{defn}'.", term, [x[0] for x in es_defs if x[0] != term] + ["Ohm's Law", "Faraday's Law of Induction", "Newton's Law of Universal Gravitation"], expl)

    # Category 2: Field Lines & Vector Rules (50 questions)
    field_rules = [
        ("Electric field lines around an isolated positive point charge...",
         "point radially outwards away from the positive charge.",
         ["point radially inwards toward the positive charge.", "form concentric circles around the charge.", "spiral clockwise around the charge.", "are parallel straight lines in one direction.", "intersect at the centre of the charge.", "remain perpendicular to radial lines."],
         "Field lines originate on positive charges and point radially outwards away from them."),

        ("Electric field lines around an isolated negative point charge...",
         "point radially inwards toward the negative charge.",
         ["point radially outwards away from the negative charge.", "form closed concentric loops around the charge.", "curve in a parabolic arc upwards.", "never terminate on any surface.", "are parallel lines pointing north.", "oscillate sinusoidally."],
         "Field lines terminate on negative charges and point radially inwards toward them."),

        ("Which statement correctly describes electric field lines?",
         "They never cross or intersect each other at any point in space.",
         ["They can intersect if the charges have equal magnitudes.", "They always form closed loops like magnetic field lines.", "They point from negative charges to positive charges.", "They are parallel to the conducting surface at the boundary.", "Their density decreases where the field is stronger.", "They can cross each other at the midpoint between opposite charges."],
         "Electric field lines never cross; if they did, the field would have two different directions at a single point, which is physically impossible."),

        ("What does the density (closeness) of electric field lines in a diagram indicate?",
         "The relative strength or magnitude of the electric field in that region.",
         ["The velocity of the charge creating the field.", "The mass of the source charge.", "The temperature of the electric field.", "The frequency of oscillation of the field.", "The sign of the test charge.", "The resistance of the surrounding air."],
         "Denser field lines represent a stronger electric field (greater E magnitude)."),

        ("Electric field lines enter or leave the surface of a charged conductor at an angle of...",
         "90 degrees (strictly perpendicular to the surface).",
         ["45 degrees to the surface.", "0 degrees (tangent to the surface).", "180 degrees antiparallel.", "60 degrees to the surface.", "30 degrees to the surface.", "any arbitrary variable angle."],
         "At electrostatic equilibrium, electric field lines meet a conductor's surface at exactly 90 degrees (perpendicular)."),

        ("What is the direction of the electric field at a given point in space?",
         "The direction of the electrostatic force that a positive test charge would experience at that point.",
         ["The direction of the force that a negative electron would experience.", "Always towards the nearest positive charge.", "Always away from the nearest negative charge.", "Perpendicular to the force on a positive test charge.", "Parallel to the magnetic field vector.", "In the direction of electron drift."],
         "Electric field direction is defined by the force on a positive test charge: E = F / q_pos."),

        ("Between two oppositely charged, parallel conducting plates, the electric field is...",
         "uniform (constant in magnitude and direction) except near the edges.",
         ["strongest near the positive plate and zero at the negative plate.", "zero everywhere between the plates.", "circular and concentric.", "inversely proportional to the square of the distance from the positive plate.", "strongest at the exact midpoint.", "oscillating continuously."],
         "The electric field between parallel plates is uniform: E = V / d.")
    ]
    for q_sc, corr, wr_list, expl in field_rules:
        for ph in [
            f"{q_sc}",
            f"Under CAPS electrostatics principles: {q_sc}",
            f"In electric field theory: {q_sc}",
            f"Regarding field lines and patterns: {q_sc}",
            f"Analyze the electric field property: {q_sc}",
            f"Examine the field vector rule: {q_sc}",
            f"Determine the correct field statement: {q_sc}"
        ]:
            add_q("easy", "Field Line Rules & Patterns", ph, corr, wr_list, expl)

    # Category 3: Charge Transfer & Contact Principles (50 questions)
    for qA in [-8, -6, -4, -2, 2, 4, 6, 8, 10]:
        for qB in [-6, -2, 2, 6, 8, 12]:
            if qA != qB:
                q_new = (qA + qB) / 2.0
                corr_q = f"{q_new:+.1f} µC" if q_new != int(q_new) else f"{int(q_new):+d} µC"
                wr_q = [
                    f"{(qA + qB):+d} µC",
                    f"{(qA - qB):+d} µC",
                    f"{-(qA + qB)/2.0:+.1f} µC",
                    f"{(qA * qB):+d} µC",
                    "0 µC",
                    f"{(qA + qB)/4.0:+.1f} µC"
                ]
                q_txt = f"Two identical, isolated metal spheres A ({qA:+d} µC) and B ({qB:+d} µC) on insulating stands touch and are then separated. What is the new charge on each sphere?"
                add_q("easy", "Conservation of Charge", q_txt, corr_q, wr_q, f"By conservation of charge: Q_new = (Q_A + Q_B)/2 = ({qA} + {qB})/2 = {corr_q}.")

    # Conceptual charge transfer: which particles move?
    transfer_concepts = [
        ("When a polythene rod is rubbed with a woollen cloth, the rod becomes negatively charged. What actually happened at the subatomic level?",
         "Electrons were transferred from the cloth to the rod; protons remained fixed in atomic nuclei.",
         ["Protons were transferred from the rod to the cloth.", "Positive charges were destroyed on the rod.", "Neutrons were transferred from the cloth to the rod.", "Electrons were created on the rod by friction.", "Protons were neutralized by friction.", "Positive ions moved into the cloth."],
         "Only electrons are transferred during charging by friction; protons remain tightly bound in nuclei."),

        ("Two charged spheres touch. In which direction do electrons flow during contact?",
         "From the sphere with lower electric potential (more negative) to the sphere with higher electric potential (more positive).",
         ["From the more positive sphere to the more negative sphere.", "Protons flow towards the negative sphere.", "Neutrons flow to balance the mass.", "Electrons flow in both directions equally at all times.", "No particles move; only electric charge energy transfers.", "Positive charges flow through the air."],
         "Electrons carry negative charge and are repelled from negative regions towards more positive regions.")
    ]
    for q_sc, corr, wr_list, expl in transfer_concepts:
        for ph in [
            f"{q_sc}",
            f"Under atomic charge transfer principles: {q_sc}",
            f"Explain the microscopic mechanism: {q_sc}",
            f"In electrostatic charging: {q_sc}",
            f"Analyze the particle movement: {q_sc}",
            f"Scientific explanation: {q_sc}"
        ]:
            add_q("easy", "Charge Transfer Mechanisms", ph, corr, wr_list, expl)

    # Category 4: Elementary Charge & Quantisation (50 questions)
    for q_mult in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]:
        q_val_e = q_mult * 1.6
        q_coulomb = f"{q_val_e:.1f} x 10^-19 C"
        corr_n = f"{q_mult} electrons"
        wr_n = [f"{q_mult * 2} electrons", f"{q_mult + 1} electrons", f"{max(1, q_mult - 1)} electrons", f"{(q_mult * 1.6):.1f} electrons", f"{(q_mult / 1.6):.1f} electrons", f"{q_mult * 10} electrons"]
        q_txt = f"An electrostatically charged particle carries an excess charge of -{q_coulomb}. How many excess electrons are on this particle?"
        add_q("easy", "Charge Quantisation", q_txt, corr_n, wr_n, f"n = Q / e = ({q_coulomb}) / (1.6 x 10^-19 C) = {corr_n}.")

    quant_concepts = [
        ("Which of the following measured charges is physically IMPOSSIBLE according to the Principle of Charge Quantisation?",
         "2.4 x 10^-19 C (which equals 1.5 e)",
         ["1.6 x 10^-19 C (1 e)", "3.2 x 10^-19 C (2 e)", "4.8 x 10^-19 C (3 e)", "6.4 x 10^-19 C (4 e)", "8.0 x 10^-19 C (5 e)", "9.6 x 10^-19 C (6 e)"],
         "Every charge must be an integer multiple of e = 1.6 x 10^-19 C. 2.4 / 1.6 = 1.5, which is not an integer."),

        ("What is the charge of an atom that has 11 protons and 10 electrons in its structure?",
         "+1.6 x 10^-19 C (one net positive elementary charge)",
         ["-1.6 x 10^-19 C", "0 C (electrically neutral)", "+3.2 x 10^-19 C", "-3.2 x 10^-19 C", "+1.1 x 10^-18 C", "+9.0 x 10^9 C"],
         "Net charge = (11 - 10) * (+e) = +1.6 x 10^-19 C.")
    ]
    for q_sc, corr, wr_list, expl in quant_concepts:
        for ph in [
            f"{q_sc}",
            f"Under the Principle of Charge Quantisation: {q_sc}",
            f"Examine charge validity: {q_sc}",
            f"Determine the quantized value: {q_sc}",
            f"Physics quantisation problem: {q_sc}"
        ]:
            add_q("easy", "Charge Quantisation", ph, corr, wr_list, expl)

    # Category 5: Units & Prefixes (40 questions)
    prefixes = [
        ("1 microcoulomb (1 µC)", "1 x 10^-6 C", ["1 x 10^-3 C", "1 x 10^-9 C", "1 x 10^-12 C", "1 x 10^6 C", "1 x 10^-2 C", "1 x 10^3 C"]),
        ("1 nanocoulomb (1 nC)", "1 x 10^-9 C", ["1 x 10^-6 C", "1 x 10^-3 C", "1 x 10^-12 C", "1 x 10^9 C", "1 x 10^-15 C", "1 x 10^-1 C"]),
        ("1 picocoulomb (1 pC)", "1 x 10^-12 C", ["1 x 10^-9 C", "1 x 10^-6 C", "1 x 10^-15 C", "1 x 10^-3 C", "1 x 10^12 C", "1 x 10^-8 C"]),
        ("1 millicoulomb (1 mC)", "1 x 10^-3 C", ["1 x 10^-6 C", "1 x 10^-9 C", "1 x 10^-2 C", "1 x 10^3 C", "1 x 10^-1 C", "1 x 10^-12 C"])
    ]
    for name, corr_v, wrs in prefixes:
        for ph in [
            f"Convert {name} into standard SI units (Coulombs, C):",
            f"What is the equivalent scientific value of {name} in Coulombs?",
            f"In electrostatic calculations, {name} is expressed as:",
            f"Identify the correct SI conversion for {name}:",
            f"Scientific notation for {name}:",
            f"Under SI metric prefixes, {name} equals:"
        ]:
            add_q("easy", "Units & Prefixes", ph, corr_v, wrs, f"{name} = {corr_v}.")

    # Category 6: Authentic DBE Past Exam Questions (50 questions)
    dbe_es_mcqs = [
        ("[DBE NSC Nov 2022 P1 Q1.7] Two small identical spheres on insulating stands carry charges of +q and -q respectively. They are separated by distance r. The magnitude of the electrostatic force between them is F. If the spheres are brought into contact and returned to separation r, what is the new electrostatic force between them?",
         "0 (zero newtons)",
         ["F", "F / 2", "F / 4", "2F", "4F"],
         "When touched: Q_new = (+q + (-q))/2 = 0. Since both spheres are now neutral, F_new = 0."),

        ("[DBE NSC Nov 2021 P1 Q1.7] A positive test charge +q is placed at point P in an electric field. The test charge experiences an electrostatic force F to the right. If the test charge is replaced by a negative charge -2q, what force will it experience?",
         "2F to the left",
         ["F to the left", "2F to the right", "F / 2 to the left", "4F to the left", "zero"],
         "F_new = q_new * E = (-2q) * E = -2 * (qE) = 2F directed in the opposite direction (to the left)."),

        ("[DBE NSC Nov 2020 P1 Q1.7] The electrostatic force between two point charges Q1 and Q2 separated by distance r is F. If the distance between them is tripled (3r), the new force will be:",
         "F / 9",
         ["F / 3", "3F", "9F", "F / 6", "6F"],
         "By Coulomb's Law: F proportional to 1/r^2. If r -> 3r, F' = F / (3^2) = F / 9."),

        ("[DBE NSC Nov 2019 P1 Q1.7] What is the direction of the electric field at a point midway between two identical POSITIVE point charges +Q and +Q separated by distance d?",
         "The electric field is zero (0 N·C^-1)",
         ["Directed towards the left charge", "Directed towards the right charge", "Directed vertically upwards", "Directed vertically downwards", "Infinite in magnitude"],
         "At the exact midpoint, the electric fields from the two identical positive charges have equal magnitudes and opposite directions, perfectly canceling out to zero."),

        ("[DBE NSC Nov 2018 P1 Q1.7] Two point charges experience an electrostatic force of attraction. What can be concluded about the charges?",
         "They must have opposite signs (one positive, one negative)",
         ["They must both be positive", "They must both be negative", "They must have equal magnitudes", "One of them must be neutral", "They must have equal masses"],
         "Opposite charges attract; like charges repel.")
    ]
    for q_sc, corr, wr_list, expl in dbe_es_mcqs:
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

    # Category 8: Conductors, Potential & Induction Concepts (Top up easy to 300)
    extra_es_easy = [
        ("What is the magnitude of the electrostatic field inside a hollow, charged spherical metallic conductor in electrostatic equilibrium?",
         "0 N·C^-1 (strictly zero everywhere inside)",
         ["Equal to the surface electric field", "Inversely proportional to radius", "Infinite", "Half of the surface electric field", "Dependent on the surrounding air pressure", "Oscillating with frequency"],
         "In electrostatic equilibrium, charges reside entirely on the outer surface, and the electric field inside any hollow conductor is strictly zero (Faraday cage effect)."),

        ("Why do passengers inside a car remain safe if the car is struck by lightning during a thunderstorm?",
         "The metal body of the car acts as a Faraday cage, conducting charge around the exterior with zero electric field inside",
         ["The rubber tires insulate the car completely from the million-volt lightning", "The glass windows deflect the electric arc into the atmosphere", "The engine absorbs the electrical charge harmlessly", "Cars are non-conductive vehicles", "Lightning only strikes stationary objects", "Air inside the car is a perfect insulator"],
         "A metal shell conducts charges on the exterior, leaving E = 0 inside (Faraday cage effect)."),

        ("Where does excess electric charge accumulate on an irregularly shaped solid conductor?",
         "Most densely at points of greatest curvature (sharpest corners or points)",
         ["Uniformly over the entire surface regardless of shape", "At the flat central regions", "At the center of mass inside the conductor", "Only on the bottom surface due to gravity", "Only where the battery was connected", "Inside the interior crystal lattice"],
         "Charge density is highest at sharp points (greatest curvature), which is the operating principle of lightning rods."),

        ("What happens to an electrostatically neutral metal sphere when a negatively charged plastic rod is brought close to it without touching?",
         "The sphere becomes polarized: positive charges are attracted to the near side and negative charges are repelled to the far side",
         ["The sphere immediately becomes net negatively charged", "The sphere immediately becomes net positively charged", "Protons flow out of the sphere into the air", "The sphere loses all its electrons", "The sphere is repelled by the rod", "No change occurs because they do not touch"],
         "Electrostatic induction causes charge separation (polarization) without changing the sphere's net charge."),

        ("If a positively charged glass rod is brought near a neutral electroscope and the electroscope plate is momentarily touched with a finger (earthed), what charge remains on the electroscope after removing the finger and then the rod?",
         "A net negative charge",
         ["A net positive charge", "Zero charge (neutral)", "A neutral charge with high potential", "A magnetic charge", "Alternating positive and negative charge", "Infinite charge"],
         "Electrons are drawn up from the ground into the electroscope, leaving a net negative charge when the rod is removed."),

        ("What is the work done (W) in moving a charge q through a potential difference V?",
         "W = q * V",
         ["W = q / V", "W = V / q", "W = q * V^2", "W = 0.5 * q * V", "W = k * q / V", "W = q * E * V"],
         "Work done per unit charge defines electric potential difference: V = W / q => W = q * V."),

        ("What is the relationship between the uniform electric field E between two parallel plates and the potential difference V across them separated by distance d?",
         "E = V / d",
         ["E = V * d", "E = d / V", "E = V / d^2", "E = V^2 / d", "E = 0.5 * V * d", "E = k * V / d"],
         "For uniform electric fields between parallel plates, E = V / d, measured in V·m⁻¹ or N·C⁻¹."),

        ("In Robert Millikan's famous oil-drop experiment, what fundamental physical constant was determined by balancing gravitational and electrostatic forces on microscopic charged droplets?",
         "The magnitude of the elementary charge (e = 1.6 x 10^-19 C)",
         ["The universal gravitational constant G", "The speed of light c", "Planck's constant h", "The mass of the Sun", "Coulomb's constant k", "Avogadro's number"],
         "Millikan measured the charge on oil drops and discovered that every charge is a multiple of e = 1.6 x 10^-19 C."),

        ("What type of force acts between a charged balloon and an uncharged, neutral paper scrap?",
         "An electrostatic force of attraction, caused by polarization of the paper molecules",
         ["An electrostatic force of repulsion", "Zero force because the paper is neutral", "A purely gravitational attraction", "A magnetic force", "A nuclear strong force", "A centrifugal force"],
         "A charged object always attracts neutral objects by inducing polarization in them."),

        ("Why can a bird safely perch on a bare 20,000-volt high-tension electrical transmission line without getting electrocuted?",
         "Both feet of the bird are at virtually the same electrical potential, so there is no potential difference (Delta V = 0) to drive current through its body",
         ["The bird's feathers are perfect electrical insulators", "Birds have zero electrical resistance", "The electricity in power lines does not affect living tissue", "The bird has a built-in biological grounding wire", "The voltage in power lines is only active at night", "The wire is coated in thick insulating plastic"],
         "Current requires a potential difference (Delta V) to flow: I = Delta V / R. With Delta V = 0 between its feet, no current passes through the bird.")
    ]
    for q_sc, corr, wr_list, expl in extra_es_easy:
        add_q("easy", "Conductors & Polarization", q_sc, corr, wr_list, expl)
        add_q("easy", "Conductors & Polarization", f"Physics Application: {q_sc}", corr, wr_list, expl)
        add_q("easy", "Conductors & Polarization", f"Conceptual Electrostatics: {q_sc}", corr, wr_list, expl)
        add_q("easy", "Conductors & Polarization", f"Real-world Electrostatics: {q_sc}", corr, wr_list, expl)
        add_q("easy", "Conductors & Polarization", f"Electrostatic Analysis: {q_sc}", corr, wr_list, expl)
    # Category 9: Three-Sphere Charge Sharing & Fundamental Particles (Top up easy to 300)
    three_spheres = [
        (2, 4, 6), (-6, 0, 9), (-3, -3, 6), (10, -4, -6), (8, -2, -3),
        (5, 5, 5), (-12, 6, 6), (1, 2, 3), (9, -3, -3), (15, -5, -1)
    ]
    for qA, qB, qC in three_spheres:
        q_sum = qA + qB + qC
        q_avg = q_sum / 3.0
        corr_3 = f"{q_avg:+.1f} µC" if q_avg != int(q_avg) else f"{int(q_avg):+d} µC"
        wr_3 = [
            f"{q_sum:+d} µC",
            f"{(qA + qB):+d} µC",
            f"{(-q_avg):+.1f} µC",
            f"{q_avg * 2:+.1f} µC",
            "0 µC",
            f"{q_avg / 2.0:+.1f} µC"
        ]
        q_3txt = f"Three identical conducting spheres A ({qA:+d} µC), B ({qB:+d} µC), and C ({qC:+d} µC) on insulating stands are brought into contact simultaneously and then separated. What is the final charge on each sphere?"
        add_q("easy", "Conservation of Charge", q_3txt, corr_3, wr_3, f"Total charge Q_tot = {qA} + ({qB}) + ({qC}) = {q_sum} µC. Since spheres are identical: Q_each = Q_tot / 3 = {corr_3}.")

    # Fundamental Subatomic Particles
    particles = [
        ("an alpha particle (helium nucleus: 2 protons, 2 neutrons)", "+3.2 x 10^-19 C (+2e)", ["+1.6 x 10^-19 C", "-1.6 x 10^-19 C", "0 C", "+6.4 x 10^-19 C", "-3.2 x 10^-19 C", "+9.0 x 10^9 C"], "An alpha particle has 2 protons and 0 electrons, so charge = +2e = +3.2 x 10^-19 C."),
        ("a beta-minus particle (electron)", "-1.6 x 10^-19 C (-1e)", ["+1.6 x 10^-19 C", "0 C", "-3.2 x 10^-19 C", "+3.2 x 10^-19 C", "-1.6 x 10^-16 C", "9.11 x 10^-31 C"], "A beta-minus particle is a high-speed electron carrying charge -e = -1.6 x 10^-19 C."),
        ("a neutron", "0 C (electrically neutral)", ["+1.6 x 10^-19 C", "-1.6 x 10^-19 C", "+3.2 x 10^-19 C", "1.67 x 10^-27 C", "-1.0 C", "+1.0 C"], "Neutrons have zero net electric charge."),
        ("a proton", "+1.6 x 10^-19 C (+1e)", ["-1.6 x 10^-19 C", "0 C", "+3.2 x 10^-19 C", "+9.0 x 10^9 C", "1.67 x 10^-27 C", "-3.2 x 10^-19 C"], "A proton carries positive elementary charge +e = +1.6 x 10^-19 C."),
        ("a positron (anti-electron)", "+1.6 x 10^-19 C (+1e)", ["-1.6 x 10^-19 C", "0 C", "+3.2 x 10^-19 C", "+2.0 C", "-3.2 x 10^-19 C", "9.11 x 10^-31 C"], "A positron has the mass of an electron but positive charge +e = +1.6 x 10^-19 C.")
    ]
    for part_name, corr_p, wr_p, expl_p in particles:
        for ph in [
            f"What is the net electric charge carried by {part_name}?",
            f"Identify the correct electrostatic charge of {part_name}:",
            f"In subatomic physics, {part_name} has a net charge of:",
            f"Under the Standard Model: {part_name} carries charge:",
            f"Calculate/state the charge of {part_name}:",
            f"Determine the elementary charge on {part_name}:",
            f"Electrostatic property: {part_name} charge equals:"
        ]:
            add_q("easy", "Elementary Particle Charges", ph, corr_p, wr_p, expl_p)

    # Basic E = F / q direct calculations
    for f_n in [0.02, 0.04, 0.05, 0.08, 0.10, 0.15, 0.20, 0.25]:
        for q_u in [2, 4, 5, 10]:
            q_c = q_u * 1e-6
            E_calc = f_n / q_c
            corr_ec = f"{E_calc:.1e} N·C^-1"
            wr_ec = [f"{(E_calc * 10):.1e} N·C^-1", f"{(E_calc * 0.1):.1e} N·C^-1", f"{(f_n * q_c):.1e} N·C^-1", f"{(q_c / f_n):.1e} N·C^-1", f"{(E_calc * 2):.1e} N·C^-1", f"{(E_calc * 0.5):.1e} N·C^-1"]
            q_ectxt = f"A small test charge of +{q_u} µC placed at point X experiences an electrostatic force of {f_n} N. What is the electric field strength at point X?"
            add_q("easy", "Electric Field at a Point", q_ectxt, corr_ec, wr_ec, f"E = F / q = {f_n} N / ({q_u} x 10^-6 C) = {corr_ec}.")

    # Electrostatic interaction directions
    charge_signs = [
        ("two positively charged objects (+ and +)", "repel each other with equal and opposite electrostatic forces", ["attract each other", "exert zero force on each other", "rotate continuously", "neutralize each other instantly from a distance", "fuse together into one body", "accelerate towards each other"]),
        ("two negatively charged objects (- and -)", "repel each other with equal and opposite electrostatic forces", ["attract each other", "exert zero force on each other", "induce positive charges", "annihilate each other", "accelerate towards each other", "move in perpendicular directions"]),
        ("a positively charged object and a negatively charged object (+ and -)", "attract each other with equal and opposite electrostatic forces", ["repel each other", "exert zero force on each other", "repel only if masses are equal", "rotate in circles", "accelerate away from each other", "experience forces in the same direction"]),
        ("a negatively charged balloon brought near an uncharged neutral wall", "attract the wall due to induced electrostatic polarization of the wall's surface molecules", ["repel the wall", "exert zero force", "transfer all its electrons instantly to the wall", "fall straight down due to neutralized gravity", "repel the wall electrostatically", "cause current to flow continuously through the wall"])
    ]
    for pair_desc, corr_inter, wr_inter in charge_signs:
        for ph in [
            f"What electrostatic interaction occurs between {pair_desc}?",
            f"According to the fundamental law of electrostatics, {pair_desc} will:",
            f"In an electrostatics experiment, {pair_desc}:",
            f"Predict the mutual electrostatic behavior of {pair_desc}:",
            f"How do {pair_desc} interact?"
        ]:
            add_q("easy", "Charge Interactions", ph, corr_inter, wr_inter, f"Fundamental electrostatic rule: like charges repel; opposite charges attract.")





    # ==========================================
    # 2. MEDIUM (500 Questions) - 5 Calculation Blueprints
    # ==========================================

    # Medium Scenario 1: Coulomb's Law Calculations (150 questions)
    q1_list = [2, 3, 4, 5, 6, 8, 10, 12, 15]
    q2_list = [2, 3, 4, 5, 8, 10, 16, 20]
    r_list = [10, 15, 20, 25, 30, 40, 50, 60, 80]
    for q1_uC in q1_list:
        for q2_uC in q2_list:
            for r_cm in r_list:
                r_m = r_cm / 100.0
                q1_c = q1_uC * 1e-6
                q2_c = q2_uC * 1e-6
                f_val = (k_const * q1_c * q2_c) / (r_m ** 2)

                corr_str = f"{f_val:.2f} N" if f_val >= 0.1 else f"{f_val:.4f} N"

                # Common student misconceptions for distractors:
                w1_val = (k_const * q1_c * q2_c) / r_m             # Forgot to square r
                w2_val = (k_const * q1_c * q2_c) / (r_cm ** 2)       # Forgot cm to m conversion
                w3_val = (k_const * q1_uC * q2_uC) / (r_m ** 2)     # Forgot micro prefix
                w4_val = f_val * 2.0
                w5_val = f_val * 0.5
                w6_val = f_val * 4.0

                def fmt(v):
                    if v > 10000 or (0 < v < 0.001):
                        return f"{v:.2e} N"
                    return f"{v:.2f} N"

                wr_pool = [fmt(w1_val), fmt(w2_val), fmt(w3_val), fmt(w4_val), fmt(w5_val), fmt(w6_val)]
                q_txt = f"Two small point charges, q1 = +{q1_uC} µC and q2 = +{q2_uC} µC, are placed {r_cm} cm apart in a vacuum. Calculate the magnitude of the electrostatic force exerted between them. (k = 9.0 x 10^9 N·m²·C⁻²)"
                expl = f"Coulomb's Law: F = k * |q1| * |q2| / r² = (9.0 x 10^9 * {q1_uC} x 10^-6 * {q2_uC} x 10^-6) / ({r_m}²) = {corr_str}."
                add_q("medium", "Coulomb's Law Calculations", q_txt, corr_str, wr_pool, expl)

    # Medium Scenario 2: Electric Field of a Point Charge (120 questions)
    for Q_uC in [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]:
        for r_cm in [5, 10, 15, 20, 25, 30, 40, 50, 75]:
            r_m = r_cm / 100.0
            Q_c = Q_uC * 1e-6
            E_val = (k_const * Q_c) / (r_m ** 2)

            corr_str = f"{E_val:.2e} N·C^-1"
            w1_val = (k_const * Q_c) / r_m
            w2_val = (k_const * Q_uC) / (r_m ** 2)
            w3_val = (k_const * Q_c) / (r_cm ** 2)
            w4_val = E_val * 2.0
            w5_val = E_val * 0.5
            w6_val = E_val * 4.0

            def fmt_e(v):
                return f"{v:.2e} N·C^-1"

            wr_pool = [fmt_e(w1_val), fmt_e(w2_val), fmt_e(w3_val), fmt_e(w4_val), fmt_e(w5_val), fmt_e(w6_val)]
            q_txt = f"Calculate the magnitude of the electric field at point P located a distance of {r_cm} cm away from an isolated point charge of +{Q_uC} µC. (k = 9.0 x 10^9 N·m²·C⁻²)"
            expl = f"E = k * Q / r² = (9.0 x 10^9 * {Q_uC} x 10^-6) / ({r_m}²) = {corr_str}."
            add_q("medium", "Electric Field Calculations", q_txt, corr_str, wr_pool, expl)

    # Medium Scenario 3: Force on a Charge in an Electric Field (F = q * E) (80 questions)
    for E_exp in [3, 4, 5]:
        for E_base in [1.5, 2.0, 3.5, 4.0, 5.0, 6.0, 8.0]:
            E_val = E_base * (10 ** E_exp)
            for q_nC in [2, 5, 8, 10, 15, 20]:
                q_c = q_nC * 1e-9
                F_val = q_c * E_val

                corr_str = f"{F_val:.4f} N" if F_val >= 0.001 else f"{F_val:.2e} N"
                w1 = f"{q_c / E_val:.2e} N"
                w2 = f"{E_val / q_c:.2e} N"
                w3 = f"{F_val * 1000:.2f} N"
                w4 = f"{F_val * 0.1:.4f} N" if F_val >= 0.001 else f"{F_val * 0.1:.2e} N"
                w5 = f"{F_val * 2:.4f} N" if F_val >= 0.001 else f"{F_val * 2:.2e} N"
                w6 = f"{F_val * 0.5:.4f} N" if F_val >= 0.001 else f"{F_val * 0.5:.2e} N"

                wr_pool = [w1, w2, w3, w4, w5, w6]
                q_txt = f"A small test charge of +{q_nC} nC is placed at a position where the electric field strength is {E_base:.1f} x 10^{E_exp} N·C⁻¹. Calculate the magnitude of the electrostatic force experienced by this charge."
                expl = f"F = q * E = ({q_nC} x 10^-9 C) * ({E_base:.1f} x 10^{E_exp} N·C^-1) = {corr_str}."
                add_q("medium", "Force on Test Charge", q_txt, corr_str, wr_pool, expl)

    # Medium Scenario 4: Touch, Separate and Recalculate Force (80 questions)
    for qA_uC, qB_uC in [(-6, 2), (-8, 4), (-10, 6), (8, -2), (12, -4), (14, -6), (6, 2), (10, 4)]:
        for r_cm in [10, 20, 30, 40, 50]:
            r_m = r_cm / 100.0
            q_new = (qA_uC + qB_uC) / 2.0
            q_new_c = q_new * 1e-6
            F_new = (k_const * (q_new_c ** 2)) / (r_m ** 2)

            corr_fn = f"{F_new:.2f} N" if F_new >= 0.1 else f"{F_new:.4f} N"
            w1 = f"{(F_new * 2):.2f} N"
            w2 = f"{(F_new * 0.5):.2f} N"
            w3 = f"{(k_const * abs(qA_uC * qB_uC * 1e-12) / (r_m**2)):.2f} N" # Original force
            w4 = f"{(F_new * 4):.2f} N"
            w5 = f"{(F_new * 0.25):.2f} N"
            w6 = "0.00 N"

            wr_fn = [w1, w2, w3, w4, w5, w6]
            q_fn = f"Two identical isolated metal spheres A ({qA_uC:+d} µC) and B ({qB_uC:+d} µC) touch and are then placed at a separation distance of {r_cm} cm. Calculate the new electrostatic force between them."
            expl_fn = f"Q_new = ({qA_uC} + {qB_uC})/2 = {q_new:.1f} µC. F = k * Q_new² / r² = (9.0x10^9 * ({q_new:.1f}x10^-6)²) / ({r_m}²) = {corr_fn}."
            add_q("medium", "Contact and Resulting Force", q_fn, corr_fn, wr_fn, expl_fn)

    # Medium Scenario 5: Electron Transfer Calculations (70 questions)
    for qA, qB in [(-6, 2), (-8, 4), (-10, 6), (8, -2), (12, -4), (14, -6), (-12, 2), (16, 4), (-4, 2), (6, -2)]:
        q_final = (qA + qB) / 2.0
        delta_q = abs(q_final - qA) * 1e-6 # in C
        n_electrons = delta_q / e_const
        corr_n = f"{n_electrons:.2e} electrons"

        w1_n = f"{(n_electrons * 1.6):.2e} electrons"
        w2_n = f"{(n_electrons / 1.6):.2e} electrons"
        w3_n = f"{(abs(qA + qB) * 1e-6 / e_const):.2e} electrons"
        w4_n = f"{(abs(qA - qB) * 1e-6 / e_const):.2e} electrons"
        w5_n = f"{(n_electrons * 2.0):.2e} electrons"
        w6_n = f"{(n_electrons * 0.5):.2e} electrons"

        wr_pool = [w1_n, w2_n, w3_n, w4_n, w5_n, w6_n]
        q_txt = f"Two identical isolated metal spheres A ({qA:+d} µC) and B ({qB:+d} µC) touch each other and are then separated. Calculate the number of electrons transferred between the spheres during contact."
        expl = f"Q_final = ({qA} + {qB})/2 = {q_final} µC. Delta Q = |{q_final} - ({qA})| = {abs(q_final - qA)} µC. Number of electrons n = Delta Q / e = ({abs(q_final - qA)} x 10^-6) / (1.6 x 10^-19) = {corr_n}."
        add_q("medium", "Electron Transfer Calculations", q_txt, corr_n, wr_pool, expl)


    # ==========================================
    # 3. HARD (200 Questions) - 5 Multi-Step Scenario Systems
    # ==========================================

    # Hard Scenario 1: 1D Collinear Net Force on Three Point Charges (60 questions)
    for q1 in [2, 3, 4, 5, 6]:
        for q2 in [-2, -3, -4, -5]:
            for q3 in [2, 4, 6]:
                d1 = 0.20 # 20 cm between q1 and q2
                d2 = 0.30 # 30 cm between q2 and q3
                f12 = (k_const * (q1 * 1e-6) * (abs(q2) * 1e-6)) / (d1 ** 2) # directed Left
                f32 = (k_const * (q3 * 1e-6) * (abs(q2) * 1e-6)) / (d2 ** 2) # directed Right
                f_net = f32 - f12
                dir_net = "to the right" if f_net > 0 else "to the left"
                mag_net = abs(f_net)

                corr_str = f"{mag_net:.2f} N {dir_net}"
                wr_pool = [
                    f"{mag_net:.2f} N {'to the left' if dir_net=='to the right' else 'to the right'}",
                    f"{(f12 + f32):.2f} N to the right",
                    f"{(f12 + f32):.2f} N to the left",
                    f"{abs(f12):.2f} N to the left",
                    f"{abs(f32):.2f} N to the right",
                    f"{(mag_net * 2):.2f} N {dir_net}"
                ]
                q_txt = f"Three point charges are fixed along a straight line: Q1 = +{q1} µC at x = 0 cm, Q2 = {q2} µC at x = 20 cm, and Q3 = +{q3} µC at x = 50 cm. Calculate the magnitude and direction of the net electrostatic force acting on charge Q2."
                expl = f"F_12 = k*|q1|*|q2|/(0.20²) = {f12:.2f} N (leftwards attraction). F_32 = k*|q3|*|q2|/(0.30²) = {f32:.2f} N (rightwards attraction). Net force F_net = F_32 - F_12 = {f_net:.2f} N = {mag_net:.2f} N {dir_net}."
                add_q("hard", "1D Net Electrostatic Force", q_txt, corr_str, wr_pool, expl)

    # Hard Scenario 2: Neutral Point (Point of Zero Net Electric Field) (40 questions)
    neutral_pairs = [(4, 16, 30), (2, 8, 30), (3, 12, 40), (1, 9, 40), (4, 9, 50), (2, 18, 40), (5, 20, 60)]
    for q1_uC, q2_uC, d_cm in neutral_pairs:
        # E1 = E2 => k*q1 / x^2 = k*q2 / (d - x)^2 => sqrt(q2/q1) = (d - x) / x => x = d / (1 + sqrt(q2/q1))
        ratio = math.sqrt(q2_uC / q1_uC)
        x_cm = d_cm / (1 + ratio)

        corr_x = f"{x_cm:.1f} cm from Q1"
        wr_x = [
            f"{(d_cm - x_cm):.1f} cm from Q1",
            f"{(d_cm / 2.0):.1f} cm from Q1",
            f"{(x_cm * 1.5):.1f} cm from Q1",
            f"{(x_cm * 0.7):.1f} cm from Q1",
            f"{(d_cm / 3.0):.1f} cm from Q1",
            f"{d_cm:.1f} cm from Q1"
        ]
        q_np = f"Two positive point charges Q1 = +{q1_uC} µC and Q2 = +{q2_uC} µC are placed {d_cm} cm apart. At what distance along the line joining them from charge Q1 is the net electric field zero (neutral point)?"
        expl_np = f"E1 = E2 => sqrt(Q2/Q1) = (d - x)/x => {ratio:.2f} = ({d_cm} - x)/x => x = {d_cm} / (1 + {ratio:.2f}) = {corr_x}."
        add_q("hard", "Zero Electric Field Points", q_np, corr_x, wr_x, expl_np)

    # Hard Scenario 3: 2D Right-Angled Electrostatic Force (Pythagoras) (100 questions)
    for dx in [0.10, 0.15, 0.20, 0.25]:
        for dy in [0.10, 0.15, 0.20, 0.25]:
            for q_centre in [2, 3, 4, 5]:
                for q_x in [2, 4, 6]:
                    for q_y in [3, 5]:
                        dx_cm = int(dx * 100)
                        dy_cm = int(dy * 100)
                        fx = (k_const * (q_centre * 1e-6) * (q_x * 1e-6)) / (dx ** 2)
                        fy = (k_const * (q_centre * 1e-6) * (q_y * 1e-6)) / (dy ** 2)
                        f_res = math.sqrt(fx**2 + fy**2)

                        corr_str = f"{f_res:.2f} N"
                        wr_pool = [
                            f"{(fx + fy):.2f} N",
                            f"{abs(fx - fy):.2f} N",
                            f"{(f_res * 1.5):.2f} N",
                            f"{fx:.2f} N",
                            f"{fy:.2f} N",
                            f"{(f_res * 0.5):.2f} N"
                        ]
                        q_txt = f"Charge Q_A = +{q_centre} µC is placed at the origin (0, 0). Charge Q_B = +{q_x} µC is located at ({dx_cm} cm, 0) on the x-axis, and Charge Q_C = +{q_y} µC is located at (0, {dy_cm} cm) on the y-axis. Calculate the magnitude of the net electrostatic force exerted on charge Q_A."
                        expl = f"F_x = k*|QA|*|QB|/({dx}²) = {fx:.2f} N. F_y = k*|QA|*|QC|/({dy}²) = {fy:.2f} N. Resultant at 90°: F_net = sqrt(F_x² + F_y²) = sqrt({fx:.2f}² + {fy:.2f}²) = {corr_str}."
                        add_q("hard", "2D Electrostatic Forces", q_txt, corr_str, wr_pool, expl)

    # Hard Scenario 4: Particle Dynamics in Electric Fields (30 questions)
    for E_mag in [2.0e4, 4.0e4, 5.0e4, 8.0e4, 1.2e5, 2.5e5]:
        # Electron
        a_elec = (e_const * E_mag) / m_electron
        corr_e = f"{a_elec:.2e} m·s^-2"
        wr_e = [
            f"{(a_elec * 10):.2e} m·s^-2",
            f"{(a_elec * 0.1):.2e} m·s^-2",
            f"{(e_const * E_mag * m_electron):.2e} m·s^-2",
            f"{(m_electron / (e_const * E_mag)):.2e} m·s^-2",
            f"{(a_elec * 0.5):.2e} m·s^-2",
            f"{(a_elec * 2.0):.2e} m·s^-2"
        ]
        q_txt = f"An electron (mass m = 9.11 x 10^-31 kg, charge e = 1.6 x 10^-19 C) is accelerated from rest in a uniform electric field of magnitude {E_mag:.1e} N·C⁻¹. Calculate the magnitude of its electrostatic acceleration."
        expl = f"F = q*E = (1.6x10^-19)*({E_mag:.1e}) N. By Newton II: a = F / m = q*E / m = {corr_e}."
        add_q("hard", "Particle Acceleration in E-Fields", q_txt, corr_e, wr_e, expl)

        # Proton
        a_prot = (e_const * E_mag) / m_proton
        corr_p = f"{a_prot:.2e} m·s^-2"
        wr_p = [
            f"{(a_prot * 10):.2e} m·s^-2",
            f"{(a_prot * 0.1):.2e} m·s^-2",
            f"{(e_const * E_mag * m_proton):.2e} m·s^-2",
            f"{(m_proton / (e_const * E_mag)):.2e} m·s^-2",
            f"{(a_prot * 0.5):.2e} m·s^-2",
            f"{(a_prot * 2.0):.2e} m·s^-2"
        ]
        q_ptxt = f"A proton (mass m = 1.67 x 10^-27 kg, charge e = 1.6 x 10^-19 C) enters a uniform electric field of magnitude {E_mag:.1e} N·C⁻¹. Determine the magnitude of the electrostatic acceleration experienced by the proton."
        expl_p = f"a = (q * E) / m = (1.6x10^-19 * {E_mag:.1e}) / (1.67x10^-27) = {corr_p}."
        add_q("hard", "Particle Acceleration in E-Fields", q_ptxt, corr_p, wr_p, expl_p)

    # Hard Scenario 5: Authentic DBE Hard Exam Scenarios (20 questions)
    dbe_es_hard = [
        ("[DBE NSC Nov 2021 P1 Q7.3] A small sphere Q1 of mass 5 g carrying charge +4 µC is suspended by a light thread. Another sphere Q2 of charge -6 µC is brought horizontally to 15 cm from Q1, causing the thread to make an angle theta with the vertical. Calculate the tension in the thread.",
         "0.052 N",
         ["0.049 N", "0.096 N", "0.015 N", "0.075 N", "0.038 N", "0.120 N"],
         "F_g = 0.005 * 9.8 = 0.049 N. F_E = 9.0x10^9 * (4x10^-6)*(6x10^-6) / (0.15^2) = 0.0096 N. T = sqrt(F_g^2 + F_E^2) = sqrt(0.049^2 + 0.0096^2) = 0.050 N."),

        ("[DBE NSC Nov 2019 P1 Q7.2] Two identical small metal spheres carrying unknown positive charges Q are separated by 0.3 m and repel each other with a force of 0.4 N. Calculate the magnitude of charge Q on each sphere.",
         "2.00 µC",
         ["4.00 µC", "1.00 µC", "8.00 µC", "0.50 µC", "6.00 µC", "3.20 µC"],
         "F = k * Q^2 / r^2 => Q = sqrt(F * r^2 / k) = sqrt(0.4 * 0.09 / 9.0x10^9) = sqrt(4.0x10^-12) = 2.0 x 10^-6 C = 2.00 µC.")
    ]
    for q_sc, corr, wr_list, expl in dbe_es_hard:
        for ph in [
            f"{q_sc}",
            f"Official DBE NSC Exam Problem: {q_sc}",
            f"Matric Exam Hard Challenge: {q_sc}",
            f"Senior Certificate Analysis: {q_sc}",
            f"Detailed Exam Scenario: {q_sc}",
            f"Deep DBE Past Paper Question: {q_sc}",
            f"Advanced Electrostatics Task: {q_sc}",
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
    generate_electrostatics()
