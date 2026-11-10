import json
import os

def build_momentum():
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
        qid = f"TS_P1_MOM_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Momentum & Impulse",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Momentum & Impulse",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Conservation Principles, Safety Devices, Elastic vs Inelastic
    # =========================================================================

    core_definitions = [
        ("Linear Momentum (p)",
         "The product of an object's mass and its velocity (p = m * v, a vector quantity pointing in the same direction as velocity, measured in kg·m·s⁻¹).",
         ["The product of an object's mass and its acceleration",
          "The work done in moving an object over a distance",
          "The rate of change of kinetic energy with respect to time",
          "The ratio of force applied to contact area",
          "The gravitational potential energy divided by displacement",
          "The scalar quantity of total matter inside a moving body"],
         "Linear momentum is defined as the product of mass and velocity: p = m * v. Its SI unit is kg·m·s⁻¹ (equivalent to N·s)."),

        ("Newton's Second Law in terms of Momentum",
         "The resultant (net) force acting on an object is equal to the rate of change of momentum of the object (F_net = Δp / Δt).",
         ["The net force equals mass divided by change in velocity",
          "The total momentum of an isolated system always increases with force",
          "Action and reaction forces act on the same object during impact",
          "The impulse experienced by an object is inversely proportional to momentum",
          "Force equals kinetic energy divided by stopping time squared",
          "The acceleration of an object is independent of the net force"],
         "Newton's Second Law expressed in terms of momentum states: F_net = Δp / Δt."),

        ("Impulse (J)",
         "The product of the resultant (net) force acting on an object and the time the net force acts on the object (Impulse = F_net * Δt = Δp, measured in N·s or kg·m·s⁻¹).",
         ["The total kinetic energy lost during a non-elastic collision",
          "The maximum velocity an object attains under constant acceleration",
          "The rate of change of power delivered by a vehicle engine",
          "The resistance of a solid body to angular rotation",
          "The force exerted divided by the impact duration",
          "The mechanical work done per unit time during braking"],
         "Impulse is defined as F_net * Δt. By the Impulse-Momentum Theorem, Impulse equals change in momentum: F_net * Δt = Δp."),

        ("Principle of Conservation of Linear Momentum",
         "The total linear momentum in an isolated (closed) system remains constant (is conserved) in both magnitude and direction.",
         ["The total kinetic energy of all colliding objects is always conserved",
          "The momentum of every individual colliding object remains constant",
          "The velocity of objects before collision equals velocity after collision",
          "Momentum is conserved only when external friction acts on the bodies",
          "Momentum is destroyed when two vehicles stick together upon impact",
          "The sum of forces in an isolated system equals total momentum"],
         "The Principle of Conservation of Linear Momentum states that the total momentum of an isolated system before collision equals the total momentum after collision: Σp_initial = Σp_final."),

        ("Isolated (Closed) System",
         "A physical system on which no external resultant forces (such as friction or air resistance) act.",
         ["A container completely sealed against thermal heat exchange",
          "A system where kinetic energy is conserved in all collisions",
          "An apparatus operating under standard atmospheric conditions",
          "A system containing only one solitary stationary mass",
          "A vacuum chamber where gravitational force is zero",
          "An electrical circuit with infinite internal resistance"],
         "An isolated system in mechanics is one free from net external forces, allowing internal momentum to be strictly conserved."),

        ("Elastic Collision",
         "A collision in which both total linear momentum AND total kinetic energy are completely conserved.",
         ["A collision in which kinetic energy is converted into thermal heat",
          "A collision where the colliding objects stick together permanently",
          "A collision where momentum decreases by 50%",
          "A collision involving only deformable rubber materials",
          "A collision where one object comes to a permanent halt",
          "A collision where the final velocity is greater than the speed of light"],
         "An elastic collision conserves both linear momentum (Σp_i = Σp_f) and kinetic energy (ΣE_ki = ΣE_kf)."),

        ("Inelastic Collision",
         "A collision in which linear momentum is conserved, but total kinetic energy is NOT conserved (some kinetic energy is converted into heat, sound, or permanent deformation).",
         ["A collision in which neither momentum nor kinetic energy is conserved",
          "A collision in which kinetic energy increases spontaneously",
          "A collision that occurs only between subatomic electrons",
          "A collision where no sound or heat is generated",
          "A collision in which external forces must act continuously",
          "A collision where the two objects repel without touching"],
         "In an inelastic collision, momentum is conserved, but kinetic energy is lost as internal energy, heat, sound, and structural crumpling.")
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

    # Automotive Safety Features & Physics of Impulse
    safety_features = [
        ("Airbags in motor vehicles",
         "During a crash, the rapidly inflating airbag increases the time of contact (Δt) for the occupant to come to rest, which significantly reduces the net impact force (F_net = Δp / Δt) experienced by the head and chest.",
         ["Airbags decrease the time of impact to stop the occupant faster",
          "Airbags eliminate the momentum of the car before collision begins",
          "Airbags convert the passenger's kinetic energy into potential energy",
          "Airbags create a vacuum that pulls the passenger away from the wheel",
          "Airbags ensure that the collision is 100% perfectly elastic",
          "Airbags increase the net force to overcome passenger inertia"]),

        ("Crumple zones at the front and rear of motor vehicles",
         "The engineered controlled collapse of the vehicle bodywork increases the duration of the impact (Δt), thereby decreasing the average net impact force (F_net = Δp / Δt) transmitted to the passenger cabin.",
         ["Crumple zones make the car bounce off colliding obstacles elastically",
          "Crumple zones make the vehicle body as rigid as solid cast iron",
          "Crumple zones reduce the total mass of the car to zero during impact",
          "Crumple zones accelerate the vehicle in reverse to cancel momentum",
          "Crumple zones ensure that passenger kinetic energy is multiplied",
          "Crumple zones prevent the tires from skidding on asphalt"]),

        ("Seatbelts with inertial locking reels",
         "They apply a restraining force over an extended stopping distance and time, preventing the occupant from continuing forward at high speed (inertia) and colliding with the windscreen or steering column.",
         ["They increase the passenger's momentum to match the engine speed",
          "They compress the passenger into the seat cushion to increase mass",
          "They eliminate the need for friction between tires and the road",
          "They convert the vehicle into an isolated mechanical system",
          "They make the collision perfectly elastic between passenger and glass",
          "They pull the passenger backward with ten times the collision force"]),

        ("Arrester beds on steep downhill mountain passes",
         "A long bed of deep loose sand or gravel that decelerates runaway heavy trucks over an extended stopping distance and time (Δt), reducing the deceleration force to safe levels while absorbing vehicle momentum safely.",
         ["They accelerate the truck into an emergency runaway ramp",
          "They lubricate the truck tires with low-viscosity oil",
          "They provide an elastic barrier that bounces the truck backward",
          "They decrease the impact time to stop the truck in one millisecond",
          "They increase the truck's gravitational potential energy to infinity",
          "They eliminate the truck's mass via aerodynamic drag"])
    ]

    for feat_name, feat_expl, wr_feats in safety_features:
        add_q("easy", "Safety Devices",
              f"From the perspective of Newton's Second Law in terms of momentum (F_net = Δp / Δt), how do **{feat_name}** protect human life?",
              feat_expl, wr_feats, "Understanding", f"Explain safety mechanism of {feat_name}", feat_expl)

    # Fill easy to exactly 300 with diverse qualitative momentum and collision comparisons
    vehicles = [
        ("freight train locomotive", 80000.0, 15.0),
        ("heavy haulage mining truck", 45000.0, 18.0),
        ("fully loaded cargo lorry", 20000.0, 22.0),
        ("passenger bus", 12000.0, 25.0),
        ("delivery van", 3500.0, 30.0),
        ("sports utility vehicle (SUV)", 2200.0, 32.0),
        ("compact family sedan", 1300.0, 35.0),
        ("electric hatchback", 1600.0, 30.0),
        ("racing motorcycle", 220.0, 50.0),
        ("cyclist on road bicycle", 85.0, 12.0),
        ("cricket ball bowled fast", 0.16, 38.0),
        ("rugby player sprinting", 105.0, 8.5),
        ("golf ball struck by driver", 0.045, 70.0),
        ("tennis ball served at pace", 0.058, 55.0),
        ("cargo aircraft landing", 150000.0, 70.0),
        ("bullet from target rifle", 0.020, 350.0)
    ]

    for veh_name, m_kg, v_ms in vehicles:
        for factor_v in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.2, 2.5, 3.0]:
            if counts["easy"] >= 300:
                break
            v_curr = v_ms * factor_v
            q_text_p = f"A **{veh_name}** of mass {m_kg:.0f} kg travels eastward at a constant velocity of {v_curr:.1f} m·s⁻¹. What is the direction of its linear momentum vector?"
            c_p = "Eastward (the linear momentum vector always points in the exact same direction as the velocity vector)."
            w_p = [
                "Westward (momentum always opposes the direction of motion)",
                "Vertically downward towards the center of the Earth",
                "Perpendicular to the direction of motion towards the North",
                "Momentum is a scalar quantity and has no physical direction",
                "Directly opposite to the direction of vehicle acceleration",
                "Upward away from the road surface"
            ]
            add_q("easy", "Momentum Vectors", q_text_p, c_p, w_p, "Understanding", f"Identify momentum vector direction for {veh_name}", c_p)

            if counts["easy"] < 300:
                q_text_mag = f"If the speed of the {veh_name} is DOUBLED while its mass remains {m_kg:.0f} kg, what happens to the magnitude of its linear momentum?"
                c_mag = "The linear momentum DOUBLES, because linear momentum is directly proportional to velocity (p ∝ v)."
                w_mag = [
                    "The linear momentum quadruples (increases by 4 times).",
                    "The linear momentum remains completely unchanged.",
                    "The linear momentum is halved (decreases by 1/2).",
                    "The linear momentum drops to zero.",
                    "The kinetic energy doubles while momentum quadruples.",
                    "The mass of the vehicle doubles automatically."
                ]
                add_q("easy", "Momentum Proportionality", q_text_mag, c_mag, w_mag, "Understanding", "Apply momentum direct proportionality to velocity", c_mag)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Direct Calculations: p = mv, Δp = m(vf - vi), F_net = Δp / Δt, 1D Inelastic Collisions
    # =========================================================================

    # 1. Momentum & Impulse Calculations: p = m * v and J = F_net * Δt = Δp
    mass_items = [0.15, 0.20, 0.40, 0.45, 0.50, 0.80, 1.0, 1.2, 1.5, 2.0, 5.0, 10.0, 25.0, 50.0, 100.0] # kg (balls, projectiles, crates)
    velocities_ms = [4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 18.0, 20.0, 25.0, 30.0, 35.0, 40.0]

    for m_obj in mass_items:
        for v_obj in velocities_ms:
            if counts["medium"] >= 500:
                break
            p_val = m_obj * v_obj
            corr_p = f"{p_val:.2f} kg·m·s⁻¹ eastward"
            wrs_p = [
                f"{m_obj * (v_obj ** 2):.2f} kg·m·s⁻¹ eastward (used v² instead of v)",
                f"{0.5 * m_obj * (v_obj ** 2):.2f} J (calculated kinetic energy instead of momentum)",
                f"{p_val * 2:.2f} kg·m·s⁻¹ eastward",
                f"{p_val / 2:.2f} kg·m·s⁻¹ eastward",
                f"{v_obj / m_obj:.2f} kg·m·s⁻¹ eastward",
                f"{p_val + 10.0:.2f} kg·m·s⁻¹ eastward",
                f"{p_val * 1.5:.2f} kg·m·s⁻¹ eastward"
            ]
            q_text_p = f"A technical object of mass {m_obj:.2f} kg travels at a constant velocity of {v_obj:.1f} m·s⁻¹ eastwards. Calculate its linear momentum:"
            expl_p = f"Linear momentum: p = m × v = {m_obj:.2f} kg × {v_obj:.1f} m·s⁻¹ = {corr_p}."
            add_q("medium", "Momentum Calculations", q_text_p, corr_p, wrs_p, "Applying", "Calculate linear momentum from mass and velocity", expl_p)

            # Impact force from change in momentum: F_net = m * (v_f - v_i) / Δt
            if counts["medium"] < 500:
                dt_contact = 0.05 # 50 ms contact time
                # Carries out a complete stop: v_i = v_obj, v_f = 0
                f_stop = (m_obj * v_obj) / dt_contact
                corr_fstop = f"{f_stop:.1f} N"
                wrs_fstop = [
                    f"{(m_obj * v_obj * dt_contact):.3f} N (multiplied by time instead of dividing)",
                    f"{f_stop * 2:.1f} N",
                    f"{f_stop / 2:.1f} N",
                    f"{m_obj * v_obj:.2f} N (omitted impact time factor)",
                    f"{f_stop + 120.0:.1f} N",
                    f"{(f_stop / 9.8):.1f} N",
                    f"{f_stop * 1.4:.1f} N"
                ]
                q_text_stop = f"An object of mass {m_obj:.2f} kg moving eastward at {v_obj:.1f} m·s⁻¹ collides with a barrier and is brought to rest in a time of {dt_contact:.2f} s. Calculate the magnitude of the average net force exerted on the object to stop it:"
                expl_stop = f"F_net = Δp / Δt = m × (v_f - v_i) / Δt = {m_obj:.2f} × (0 - {v_obj:.1f}) / {dt_contact:.2f} = -{m_obj * v_obj:.2f} / {dt_contact:.2f} = -{f_stop:.1f} N (magnitude is {corr_fstop})."
                add_q("medium", "Impulse Calculations", q_text_stop, corr_fstop, wrs_fstop, "Applying", "Calculate average impact force using impulse theorem", expl_stop)

    # 2. Conservation of Linear Momentum: Inelastic collision where two objects stick together
    # m1 * v1i + m2 * v2i = (m1 + m2) * vf
    # Object 1 moving into stationary Object 2 (v2i = 0): vf = (m1 * v1i) / (m1 + m2)
    trolley_1_masses = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 50.0]
    trolley_2_masses = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0]
    initial_speeds = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0]

    for m1 in trolley_1_masses:
        for m2 in trolley_2_masses:
            for v1i in initial_speeds:
                if counts["medium"] >= 500:
                    break
                p_tot_i = m1 * v1i
                m_tot = m1 + m2
                vf_stick = p_tot_i / m_tot
                corr_vf = f"{vf_stick:.2f} m·s⁻¹ eastwards"
                wrs_vf = [
                    f"{v1i:.2f} m·s⁻¹ eastwards (assumed speed unchanged)",
                    f"{(v1i / 2):.2f} m·s⁻¹ eastwards (halved speed regardless of mass ratio)",
                    f"{vf_stick * 2:.2f} m·s⁻¹ eastwards",
                    f"{vf_stick / 2:.2f} m·s⁻¹ eastwards",
                    f"{(p_tot_i / m2):.2f} m·s⁻¹ eastwards (omitted m1 from final combined mass)",
                    f"{vf_stick + 1.5:.2f} m·s⁻¹ eastwards",
                    f"{vf_stick * 1.4:.2f} m·s⁻¹ eastwards"
                ]
                q_text_stick = f"Trolley A of mass {m1:.1f} kg moves eastwards across a frictionless track at {v1i:.1f} m·s⁻¹ and collides with stationary Trolley B of mass {m2:.1f} kg. Upon impact, the two trolleys lock together. Calculate the common velocity (v_f) of the combined system immediately after collision:"
                expl_stick = f"Conservation of linear momentum: Σp_initial = Σp_final => (m1 × v1i) + (m2 × v2i) = (m1 + m2) × v_f => ({m1:.1f} × {v1i:.1f}) + 0 = ({m1:.1f} + {m2:.1f}) × v_f => {p_tot_i:.2f} = {m_tot:.1f} × v_f => v_f = {p_tot_i:.2f} / {m_tot:.1f} = {corr_vf}."
                add_q("medium", "Inelastic Collisions", q_text_stick, corr_vf, wrs_vf, "Applying", "Calculate final velocity for completely inelastic collision", expl_stick)

    # Fill medium to exactly 500 with recoil / explosion problems
    # (m1 + m2) at rest initially: m1 * v1f = -m2 * v2f => v2f = -(m1 * v1f) / m2
    step = 1
    while counts["medium"] < 500:
        m_rifle = 4.0 + (step * 0.1)
        m_bullet = 0.02 # 20 grams
        v_bullet = 400.0 + (step * 5.0)
        v_recoil = (m_bullet * v_bullet) / m_rifle
        corr_rec = f"{v_recoil:.2f} m·s⁻¹ backwards"
        wrs_rec = [
            f"{v_bullet:.2f} m·s⁻¹ (assumed equal velocity)",
            f"{v_recoil * 2:.2f} m·s⁻¹ backwards",
            f"{v_recoil / 2:.2f} m·s⁻¹ backwards",
            f"{(m_rifle * v_bullet) / m_bullet:.2f} m·s⁻¹",
            f"{v_recoil + 1.2:.2f} m·s⁻¹ backwards",
            f"{v_recoil * 1.5:.2f} m·s⁻¹ backwards",
            f"0.00 m·s⁻²"
        ]
        q_text_rec = f"A rifle of mass {m_rifle:.2f} kg fires a bullet of mass {m_bullet * 1000:.0f} g ({m_bullet:.3f} kg) horizontally forward at a muzzle velocity of {v_bullet:.1f} m·s⁻¹. Assuming an isolated system, calculate the recoil velocity of the rifle:"
        expl_rec = f"Conservation of linear momentum: Σp_initial = Σp_final => 0 = (m_rifle × v_recoil) + (m_bullet × v_bullet) => v_recoil = -(m_bullet × v_bullet) / m_rifle = -({m_bullet:.3f} × {v_bullet:.1f}) / {m_rifle:.2f} = -{m_bullet * v_bullet:.2f} / {m_rifle:.2f} = {corr_rec}."
        add_q("medium", "Recoil Dynamics", q_text_rec, corr_rec, wrs_rec, "Applying", "Calculate recoil velocity using momentum conservation", expl_rec)
        step += 1

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Rebounding Vectors (sign conventions), Kinetic Energy Loss Verification, Multi-Body Collisions
    # =========================================================================

    # 1. Bouncing / Rebound Vectors: Ball strikes wall horizontally at +vi and rebounds at -vf
    # Δp = m * (-vf - vi) = -m * (vf + vi)
    ball_masses = [0.15, 0.25, 0.30, 0.40, 0.45, 0.50, 0.60, 0.80, 1.0, 1.5] # kg
    approach_speeds = [10.0, 12.0, 15.0, 18.0, 20.0, 25.0, 30.0] # m/s
    rebound_fractions = [0.60, 0.70, 0.75, 0.80, 0.85] # restitution

    for m_b in ball_masses:
        for vi in approach_speeds:
            for r_frac in rebound_fractions:
                if counts["hard"] >= 200:
                    break
                vf = vi * r_frac
                # Taking right (initial) as positive: vi = +vi, vf = -vf
                # Δp = m * (vf - vi) = m * (-vf - vi) = -m * (vf + vi)
                mag_dp = m_b * (vf + vi)
                corr_dp = f"{mag_dp:.2f} N·s away from the wall (opposite to initial motion)"
                # Common student error: Δp = m * (vf - vi) = m * (vf - vi) (forgetting negative sign on rebound velocity)
                wrong_dp = m_b * abs(vf - vi)
                wrs_dp = [
                    f"{wrong_dp:.2f} N·s (failed to treat rebound velocity as a negative vector: vf - vi)",
                    f"{m_b * vi:.2f} N·s (calculated initial momentum only)",
                    f"{m_b * vf:.2f} N·s (calculated rebound momentum only)",
                    f"{mag_dp * 2:.2f} N·s",
                    f"{mag_dp / 2:.2f} N·s",
                    f"{mag_dp + 5.0:.2f} N·s",
                    f"{mag_dp * 1.4:.2f} N·s"
                ]
                q_text_b = f"A ball of mass {m_b:.2f} kg moves horizontally rightwards at {vi:.1f} m·s⁻¹ and strikes a vertical concrete wall. It rebounds horizontally to the left at a speed of {vf:.1f} m·s⁻¹. Taking rightwards as the positive direction, calculate the magnitude and direction of the change in momentum (Δp) of the ball:"
                expl_b = f"Assign directions: Right = (+), Left = (-). v_i = +{vi:.1f} m·s⁻¹, v_f = -{vf:.1f} m·s⁻¹. Δp = m × (v_f - v_i) = {m_b:.2f} × [(-{vf:.1f}) - (+{vi:.1f})] = {m_b:.2f} × (-{vf + vi:.1f}) = -{mag_dp:.2f} kg·m·s⁻¹ (magnitude = {corr_dp})."
                add_q("hard", "Rebounding Vectors", q_text_b, corr_dp, wrs_dp, "Evaluating", "Calculate change in momentum for rebounding object using vector signs", expl_b)

    # 2. Kinetic Energy Loss Verification (Proving Inelasticity quantitatively)
    # E_ki = 1/2 m1 v1i^2 + 1/2 m2 v2i^2; E_kf = 1/2 (m1 + m2) vf^2; ΔE_k = E_kf - E_ki
    for m1 in [1000.0, 1200.0, 1500.0, 2000.0]:
        for m2 in [800.0, 1000.0, 1200.0, 1500.0]:
            for v1i in [15.0, 20.0, 25.0, 30.0]:
                if counts["hard"] >= 200:
                    break
                v2i = 0.0 # Car 2 stationary
                # Combined final velocity: vf = (m1 * v1i) / (m1 + m2)
                vf = (m1 * v1i) / (m1 + m2)
                eki = 0.5 * m1 * (v1i ** 2)
                ekf = 0.5 * (m1 + m2) * (vf ** 2)
                ek_lost = eki - ekf
                corr_ekloss = f"{ek_lost:.1f} J (proving the collision is INELASTIC)"
                wrs_ekloss = [
                    "0.00 J (the collision is perfectly elastic)",
                    f"{eki:.1f} J (100% of kinetic energy was lost)",
                    f"{ekf:.1f} J",
                    f"{ek_lost * 2:.1f} J",
                    f"{ek_lost / 2:.1f} J",
                    f"{ek_lost + 25000.0:.1f} J",
                    f"{ek_lost * 1.5:.1f} J"
                ]
                q_text_ek = f"Car A of mass {m1:.0f} kg travelling at {v1i:.1f} m·s⁻¹ collides with stationary Car B of mass {m2:.0f} kg. The two vehicles lock together upon impact and slide forward. Quantitatively determine the total kinetic energy LOST during this collision and classify the collision type:"
                expl_ek = f"1. Conservation of momentum: v_f = (m1 × v1i) / (m1 + m2) = ({m1:.0f} × {v1i:.1f}) / ({m1 + m2:.0f}) = {vf:.2f} m·s⁻¹. 2. Initial kinetic energy: E_ki = 0.5 × {m1:.0f} × ({v1i:.1f})² = {eki:.1f} J. 3. Final kinetic energy: E_kf = 0.5 × {m1 + m2:.0f} × ({vf:.2f})² = {ekf:.1f} J. 4. Loss: ΔE_k = E_ki - E_kf = {eki:.1f} - {ekf:.1f} = {corr_ekloss}."
                add_q("hard", "Kinetic Energy Loss", q_text_ek, corr_ekloss, wrs_ekloss, "Evaluating", "Calculate kinetic energy lost to prove collision is inelastic", expl_ek)

    # 3. Two Moving Vehicles Head-on Collision: m1*v1i + m2*v2i = (m1+m2)*vf
    # v1i = +v1, v2i = -v2
    for m1 in [1000.0, 1500.0, 2000.0]:
        for m2 in [1200.0, 1800.0, 2500.0]:
            for v1 in [15.0, 20.0, 25.0]:
                for v2 in [10.0, 15.0, 20.0]:
                    if counts["hard"] >= 200:
                        break
                    p_net = (m1 * v1) - (m2 * v2)
                    tot_m = m1 + m2
                    vf_head = p_net / tot_m
                    dir_str = "eastwards" if vf_head >= 0 else "westwards"
                    corr_head = f"{abs(vf_head):.2f} m·s⁻¹ {dir_str}"
                    wrs_head = [
                        f"{((m1 * v1) + (m2 * v2)) / tot_m:.2f} m·s⁻¹ eastwards (added momentums as scalars without vector direction)",
                        f"{abs(v1 - v2):.2f} m·s⁻¹ {dir_str}",
                        f"{abs(vf_head) * 2:.2f} m·s⁻¹ {dir_str}",
                        f"{abs(vf_head) / 2:.2f} m·s⁻¹ {dir_str}",
                        f"{(abs(p_net) / m1):.2f} m·s⁻¹ {dir_str}",
                        f"{abs(vf_head) + 2.5:.2f} m·s⁻¹ {dir_str}",
                        f"0.00 m·s⁻¹"
                    ]
                    q_text_head = f"Vehicle 1 of mass {m1:.0f} kg travelling eastwards at {v1:.1f} m·s⁻¹ collides head-on with Vehicle 2 of mass {m2:.0f} kg travelling westwards at {v2:.1f} m·s⁻¹. The two vehicles crumple and stick together. Taking eastwards as positive, calculate the final velocity of the wreckage:"
                    expl_head = f"Vector momentum: East = (+), West = (-). p_initial = (m1 × +v1) + (m2 × -v2) = ({m1:.0f} × {v1:.1f}) - ({m2:.0f} × {v2:.1f}) = {m1*v1:.0f} - {m2*v2:.0f} = {p_net:.1f} kg·m·s⁻¹. Final velocity v_f = p_net / (m1 + m2) = {p_net:.1f} / {tot_m:.0f} = {vf_head:.2f} m·s⁻¹ (magnitude = {corr_head})."
                    add_q("hard", "Head-on Collisions", q_text_head, corr_head, wrs_head, "Evaluating", "Calculate final velocity in head-on collision using vector signs", expl_head)

    return questions

if __name__ == '__main__':
    qs = build_momentum()
    out_dir = "dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_momentum.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
