import json
import math
import os

def build_newtons_laws():
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
        qid = f"TS_P1_NEWT_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Newton's Laws",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Newton's Laws",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Force Types, Inertia, Action-Reaction Pairs, Gravitation Concepts
    # =========================================================================

    core_definitions = [
        ("Newton's First Law of Motion",
         "A body will remain in its state of rest or uniform motion at constant velocity in a straight line, unless acted upon by a non-zero resultant (net) force.",
         ["Force equals the rate of change of momentum of an accelerating object",
          "For every action force there is an equal and opposite reaction force acting on the same object",
          "Acceleration is inversely proportional to the applied net force",
          "An object in motion will naturally slow down and stop even if no friction exists",
          "The gravitational force between two masses is inversely proportional to distance",
          "Energy cannot be created or destroyed, only transformed between states"],
         "Newton's First Law describes inertia: a body continues in its state of rest or constant velocity unless an unbalanced net force acts on it."),

        ("Newton's Second Law of Motion",
         "When a resultant (net) force acts on an object, the object will accelerate in the direction of the force with an acceleration that is directly proportional to the force and inversely proportional to the mass of the object (F_net = m * a).",
         ["A body maintains constant velocity only when an external force is applied continuously",
          "Action and reaction forces cancel each other out so no acceleration occurs",
          "The momentum of an isolated system remains constant in all collisions",
          "Frictional force is independent of the normal force between surfaces",
          "The gravitational acceleration on any planet is independent of its mass",
          "The mechanical advantage of an inclined plane equals the sine of the angle"],
         "Newton's Second Law defines acceleration in terms of net force and mass: a = F_net / m, or F_net = m * a."),

        ("Newton's Third Law of Motion",
         "When object A exerts a force on object B, object B simultaneously exerts an oppositely directed force of equal magnitude on object A.",
         ["Action and reaction forces act on the same object to produce static equilibrium",
          "The reaction force occurs only after the action force has finished acting",
          "Heavier objects exert greater forces on lighter objects than vice versa",
          "Action and reaction forces add vectorially to zero on a single free-body diagram",
          "Newton's third law applies only when objects are moving at constant velocity",
          "Friction is the reaction force to applied normal force"],
         "Newton's Third Law states that forces always occur in matched pairs acting on DIFFERENT bodies with equal magnitude and opposite direction."),

        ("Newton's Law of Universal Gravitation",
         "Each particle in the universe attracts every other particle with a gravitational force that is directly proportional to the product of their masses and inversely proportional to the square of the distance between their centres (F = G * m1 * m2 / r²).",
         ["Gravitational force is directly proportional to the distance between two masses",
          "The force of gravity between two objects becomes zero in the vacuum of space",
          "Every object attracts all other objects with a force independent of their masses",
          "Gravitational field strength increases as an object moves further away from Earth",
          "The universal gravitational constant G varies depending on which planet you are on",
          "The weight of an object remains constant everywhere in the universe"],
         "Newton's Law of Universal Gravitation gives the mutual attraction between two masses: F = G * m1 * m2 / r²."),

        ("Normal Force (N or F_N)",
         "The force or the component of a force which a surface exerts on an object with which it is in contact, and which acts perpendicular to the surface.",
         ["The gravitational force exerted by the Earth pulling an object downward",
          "The force that always acts parallel to the contact surface opposing motion",
          "The force exerted by a stretched rope or cable attached to an object",
          "The net resultant force acting on an accelerating body",
          "The buoyant upward force exerted exclusively by liquid fluids",
          "The force that always equals mass times 9.8 m·s⁻² regardless of angle"],
         "The normal force is the contact force exerted by a surface perpendicular (at 90°) to the surface plane."),

        ("Frictional Force (f)",
         "The contact force that opposes the motion of an object and which acts parallel to the surface.",
         ["The contact force acting perpendicular to the supporting surface",
          "The force of gravity pulling objects down an inclined plane",
          "The force required to keep an object moving at constant speed in a vacuum",
          "The attractive electrostatic force between neutral atoms",
          "The tension force in a flexible string connecting two masses",
          "The force that always increases when a surface is lubricated with oil"],
         "Frictional force acts parallel to the surface of contact in the direction opposing actual or attempted relative motion."),

        ("Static Frictional Force (f_s)",
         "The frictional force that opposes the tendency of motion of a stationary object relative to a surface, up to a maximum value (f_s(max) = μ_s * N).",
         ["The constant friction acting on an object while it is sliding at high speed",
          "The force that causes stationary objects to accelerate spontaneously",
          "The friction experienced by aircraft moving through atmospheric air",
          "The internal shear resistance between layers of motor oil",
          "The force that drops to zero when an external horizontal force is applied",
          "The force that is always smaller than kinetic friction"],
         "Static friction matches applied force to keep an object at rest, reaching its peak just before slip: f_s(max) = μ_s * N."),

        ("Kinetic Frictional Force (f_k)",
         "The frictional force that opposes the motion of an object that is sliding across a surface (f_k = μ_k * N).",
         ["The variable friction that prevents a stationary object from beginning to move",
          "The friction force that increases linearly with sliding speed indefinitely",
          "The force acting perpendicular to the incline supporting an object",
          "The friction that is always greater than maximum static friction",
          "The force required to overcome inertia in outer space",
          "The upward contact force exerted by a horizontal floor"],
         "Kinetic friction acts when surfaces slide relative to each other: f_k = μ_k * N, where μ_k is the coefficient of kinetic friction."),

        ("Inertia",
         "The property of an object that causes it to resist any change in its state of rest or uniform motion in a straight line.",
         ["The force that propels rockets forward in outer space",
          "The rate of change of velocity of an accelerating body",
          "The product of mass multiplied by acceleration",
          "The total mechanical energy stored in a moving body",
          "The resistance of a liquid to shear deformation",
          "The gravitational attraction between an object and the Earth"],
         "Inertia is the natural tendency of an object to resist changes in its motion; mass is the quantitative measure of inertia.")
    ]

    stems = [
        "In Grade 12 Technical Sciences, what is the precise CAPS definition of **'{}'**?",
        "According to the examination guidelines, **'{}'** refers to:",
        "Which statement provides the exact scientific definition for **'{}'**?",
        "Identify the correct CAPS-approved definition for **'{}'**:",
        "When an examiner asks for the definition of **'{}'**, which statement receives full marks?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Conceptual Scenarios: Newton's Laws in Daily Life & Engineering
    newton_concepts = [
        ("Why does a passenger in a motor car jerk forward when the driver suddenly applies the brakes?",
         "Because of inertia (Newton's First Law): the passenger's body continues moving forward at the car's initial velocity until an external unbalanced force (the seatbelt) stops it.",
         ["Because a forward force is generated by the car's brake pads.",
          "Because the friction of the road pushes the passenger forward.",
          "Because the car loses its gravitational mass when stopping.",
          "Because of Newton's Third Law pulling the passenger toward the windscreen.",
          "Because air resistance inside the cabin increases dramatically.",
          "Because normal force tilts forward at 45 degrees."],
         "Inertia causes the passenger to maintain their state of forward motion until restrained by seatbelts."),

        ("Why do heavy commercial trucks take much longer to stop than lightweight passenger cars travelling at the same speed?",
         "According to Newton's Second Law (a = F_net / m), a larger mass requires a much greater braking force to achieve the same deceleration, or takes a longer distance and time under the same braking force.",
         ["Heavy trucks experience zero friction with the asphalt road surface.",
          "Lightweight cars have a higher universal gravitational constant G.",
          "Heavy trucks violate Newton's first law because of their length.",
          "Braking force is inversely proportional to vehicle weight.",
          "Heavy trucks have lower inertia than small cars.",
          "The normal force on heavy trucks points downward."],
         "Greater mass means greater inertia; for a given maximum braking friction, acceleration a = F_net / m is smaller, requiring longer stopping distance."),

        ("A book rests stationary on a flat horizontal table. Which force represents the true Newton's Third Law REACTION force to the Earth's gravitational downward pull on the book?",
         "The upward gravitational force exerted by the book on the Earth.",
         ["The upward normal contact force exerted by the table on the book.",
          "The downward contact force exerted by the book on the table.",
          "The static frictional force between the book cover and the table.",
          "The air pressure pushing down on the top surface of the book.",
          "The tension force inside the wooden table legs.",
          "There is no reaction force because the book is at rest."],
         "Newton's Third Law pairs must be of the same physical nature and act on different bodies: Earth pulls book down (gravity) <-> Book pulls Earth up (gravity). Normal force is an electrostatic contact force from the table, not the gravitational reaction!"),

        ("Why does a rocket accelerate upward in the vacuum of space where there is no air to push against?",
         "According to Newton's Third Law, the rocket engine exerts a backward force on the expelled exhaust gases (action), and the escaping exhaust gases exert an equal and opposite forward thrust force on the rocket (reaction).",
         ["The rocket pushes against the atmospheric air left behind on Earth.",
          "The rocket pushes against the gravitational field of distant stars.",
          "Space vacuum creates suction that pulls the rocket forward.",
          "The mass of the rocket drops to zero allowing infinite speed.",
          "The rocket bounces off cosmic dust particles in the vacuum.",
          "Newton's Third Law does not apply in outer space."],
         "Rockets propel themselves via internal momentum exchange: expelling high-speed exhaust gas backward pushes the rocket forward.")
    ]

    for q_nc, c_nc, w_nc, exp_nc in newton_concepts:
        add_q("easy", "Conceptual Mechanics", q_nc, c_nc, w_nc, "Understanding", "Explain real-world scenario using Newton's laws", exp_nc)

    # Gravitation Proportionality Questions
    grav_props = [
        ("If the distance (r) between two spherical masses is DOUBLED, what happens to the gravitational force between them?",
         "The gravitational force decreases to ONE-QUARTER (1/4) of its original value, because F ∝ 1 / r² (inverse-square law).",
         ["The gravitational force is halved (decreases to 1/2).",
          "The gravitational force doubles (increases by factor of 2).",
          "The gravitational force quadruples (increases by factor of 4).",
          "The gravitational force remains completely unchanged.",
          "The gravitational force drops to exactly zero.",
          "The gravitational force reverses and becomes repulsive."]),

        ("If the mass of one of the two objects is TRIPLED while distance remains constant, what happens to the gravitational force?",
         "The gravitational force TRIPLES (increases by a factor of 3), because F ∝ m1.",
         ["The gravitational force increases by a factor of 9 (tripled squared).",
          "The gravitational force decreases to 1/3 of its original value.",
          "The gravitational force remains constant because distance didn't change.",
          "The universal gravitational constant G triples in value.",
          "The gravitational force increases by 1.5 times.",
          "The object becomes weightless."]),

        ("If the distance between two masses is HALVED (reduced to r / 2), how does the gravitational force change?",
         "The gravitational force increases by a factor of FOUR (4 times greater), because F ∝ 1 / (r/2)² = 4 / r².",
         ["The gravitational force doubles (2 times greater).",
          "The gravitational force is halved (1/2).",
          "The gravitational force is reduced to one-quarter (1/4).",
          "The gravitational force drops to zero.",
          "The universal constant G quadruples.",
          "The masses merge into a single black hole immediately."])
    ]

    for q_gp, c_gp, w_gp in grav_props:
        add_q("easy", "Gravitation Proportionalities", q_gp, c_gp, w_gp, "Understanding", "Apply universal gravitation inverse-square proportionality", c_gp)

    # Fill easy to exactly 300 with diverse, authentic friction and normal force identification questions
    surfaces = [
        ("rubber tire on dry concrete", 0.85, 0.65),
        ("rubber tire on wet asphalt", 0.50, 0.35),
        ("steel skate on smooth ice", 0.05, 0.02),
        ("wood block on polished steel table", 0.40, 0.30),
        ("teflon slider on teflon surface", 0.04, 0.04),
        ("leather boot sole on dry timber floor", 0.60, 0.45),
        ("cast iron brake shoe on steel train wheel", 0.45, 0.30),
        ("oiled steel bearing on bronze sleeve", 0.10, 0.05),
        ("copper block on steel guide rail", 0.53, 0.36),
        ("aluminium block on dry steel base", 0.61, 0.47)
    ]

    for surf_name, mu_s, mu_k in surfaces:
        for mass_kg in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80, 90, 100, 120, 150, 200, 250, 300, 400, 500, 750, 1000]:
            if counts["easy"] >= 300:
                break
            norm_f = mass_kg * 9.8
            q_text_n = f"A stationary equipment box of mass {mass_kg} kg rests on a flat horizontal floor ({surf_name}). Taking g = 9.8 m·s⁻², what is the magnitude of the NORMAL FORCE exerted by the floor on the box?"
            corr_n = f"{norm_f:.1f} N"
            wrs_n = [
                f"{mass_kg:.1f} N (confused mass in kg with force in N)",
                f"{norm_f * 2:.1f} N",
                f"{norm_f / 2:.1f} N",
                f"{norm_f * mu_s:.1f} N (calculated static friction instead of normal force)",
                f"{norm_f * mu_k:.1f} N (calculated kinetic friction)",
                f"{norm_f + 50.0:.1f} N",
                f"0.00 N (assumed weightlessness on floor)"
            ]
            add_q("easy", "Normal Force", q_text_n, corr_n, wrs_n, "Applying", f"Calculate normal force for {mass_kg} kg on horizontal floor",
                  f"On a level horizontal surface with no vertical applied forces, Normal Force N = F_g = m × g = {mass_kg} kg × 9.8 m·s⁻² = {corr_n}.")

            if counts["easy"] < 300:
                q_text_rel = f"For {surf_name}, the coefficient of static friction is μ_s = {mu_s} and the coefficient of kinetic friction is μ_k = {mu_k}. Why is μ_s generally greater than μ_k in mechanical systems?"
                corr_rel = "At rest, microscopic surface asperities settle deeply into each other and form cold-welded contact junctions; once sliding begins, there is less time for junctions to form."
                wrs_rel = [
                    "Because kinetic friction acts perpendicular to the contact surface.",
                    "Because static friction increases the mass of the object while at rest.",
                    "Because moving objects experience zero gravitational downward pull.",
                    "Because normal force disappears once an object begins sliding.",
                    "Because kinetic friction is independent of surface roughness.",
                    "Because speed always eliminates all molecular attractive forces."
                ]
                add_q("easy", "Friction Principles", q_text_rel, corr_rel, wrs_rel, "Understanding", f"Explain why static friction exceeds kinetic friction for {surf_name}", corr_rel)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Direct Calculations: F_net = m*a, f_k = μ_k*N, F_app - f_k = m*a, F_g = G*m1*m2/r²
    # =========================================================================

    # 1. Horizontal acceleration with applied force and friction
    masses_med = [5.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 75.0, 80.0, 100.0]
    mu_k_vals = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50]
    acc_targets = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]

    for m_val in masses_med:
        for muk in mu_k_vals:
            for a_req in acc_targets:
                if counts["medium"] >= 500:
                    break
                norm_f = m_val * 9.8
                fk_val = muk * norm_f
                f_net = m_val * a_req
                f_app = f_net + fk_val
                corr_app = f"{f_app:.1f} N"
                wrs_app = [
                    f"{f_net:.1f} N (neglected kinetic friction fk)",
                    f"{fk_val:.1f} N (applied force equals friction, zero acceleration)",
                    f"{f_app * 2:.1f} N",
                    f"{f_app / 2:.1f} N",
                    f"{f_app + 45.0:.1f} N",
                    f"{(f_net - fk_val):.1f} N (subtracted friction from net force)",
                    f"{f_app * 1.5:.1f} N"
                ]
                q_text_app = f"A mechanical crate of mass {m_val:.1f} kg is pulled across a rough horizontal concrete floor where the coefficient of kinetic friction is μ_k = {muk:.2f}. What horizontal applied force (F_app) is required to accelerate the crate at {a_req:.1f} m·s⁻² (g = 9.8 m·s⁻²)?"
                expl_app = f"1. Normal force: N = m × g = {m_val:.1f} × 9.8 = {norm_f:.1f} N. 2. Friction: f_k = μ_k × N = {muk:.2f} × {norm_f:.1f} = {fk_val:.1f} N. 3. Newton's 2nd Law: F_net = F_app - f_k = m × a => F_app = m × a + f_k = ({m_val:.1f} × {a_req:.1f}) + {fk_val:.1f} = {f_net:.1f} + {fk_val:.1f} = {corr_app}."
                add_q("medium", "Newton Second Law Calculations", q_text_app, corr_app, wrs_app, "Applying", "Calculate horizontal applied force with friction", expl_app)

                # Acceleration calculation: a = (F_app - f_k) / m
                if counts["medium"] < 500:
                    corr_acc = f"{a_req:.2f} m·s⁻²"
                    wrs_acc = [
                        f"{f_app / m_val:.2f} m·s⁻² (ignored friction force fk)",
                        f"{a_req * 2:.2f} m·s⁻²",
                        f"{a_req / 2:.2f} m·s⁻²",
                        f"{fk_val / m_val:.2f} m·s⁻²",
                        f"{a_req + 1.25:.2f} m·s⁻²",
                        f"{a_req * 1.4:.2f} m·s⁻²",
                        f"0.00 m·s⁻² (assumed constant velocity)"
                    ]
                    q_text_acc = f"A horizontal pulling force of {f_app:.1f} N acts on a {m_val:.1f} kg trolley resting on a horizontal track. A constant kinetic friction force of {fk_val:.1f} N opposes the motion. Determine the acceleration (a) of the trolley:"
                    expl_acc = f"F_net = F_app - f_k = {f_app:.1f} N - {fk_val:.1f} N = {f_net:.1f} N. a = F_net / m = {f_net:.1f} N / {m_val:.1f} kg = {corr_acc}."
                    add_q("medium", "Acceleration Calculations", q_text_acc, corr_acc, wrs_acc, "Applying", "Calculate acceleration from applied force and friction", expl_acc)

    # 2. Universal Gravitation Calculations: F = G * m1 * m2 / r²
    G_const = 6.67e-11 # N m^2 / kg^2
    masses_1 = [500.0, 1000.0, 2000.0, 5000.0, 10000.0, 50000.0] # kg
    masses_2 = [1000.0, 2500.0, 5000.0, 10000.0, 20000.0, 100000.0] # kg
    distances_m = [2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 20.0, 50.0] # m

    for m1 in masses_1:
        for m2 in masses_2:
            for r_dist in distances_m:
                if counts["medium"] >= 500:
                    break
                f_grav = (G_const * m1 * m2) / (r_dist ** 2)
                corr_fg = f"{f_grav:.3e} N"
                wrs_fg = [
                    f"{(G_const * m1 * m2) / r_dist:.3e} N (forgot to square distance r)",
                    f"{((m1 * m2) / (r_dist ** 2)):.3e} N (omitted gravitational constant G)",
                    f"{f_grav * 2:.3e} N",
                    f"{f_grav / 2:.3e} N",
                    f"{f_grav * 4:.3e} N",
                    f"{f_grav * 1e6:.3e} N",
                    f"{f_grav * 1.5:.3e} N"
                ]
                q_text_g = f"Two industrial machinery components of masses {m1:.0f} kg and {m2:.0f} kg are separated by a center-to-center distance of {r_dist:.1f} m. Calculate the mutual gravitational force of attraction between them (G = 6.67 × 10⁻¹¹ N·m²·kg⁻²):"
                expl_g = f"F = G × (m1 × m2) / r² = (6.67 × 10⁻¹¹) × ({m1:.0f} × {m2:.0f}) / ({r_dist:.1f})² = (6.67 × 10⁻¹¹ × {m1 * m2:.1e}) / {r_dist ** 2:.1f} = {corr_fg}."
                add_q("medium", "Universal Gravitation Calculations", q_text_g, corr_fg, wrs_g, "Applying", "Calculate mutual gravitational force between two masses", expl_g)

    # Fill medium to exactly 500 with weight on different celestial bodies
    planets = [
        ("the Moon", 1.62),
        ("Mars", 3.71),
        ("Venus", 8.87),
        ("Jupiter", 24.79),
        ("Mercury", 3.70),
        ("Saturn", 10.44),
        ("Neptune", 11.15)
    ]

    for p_name, g_surf in planets:
        for mass_probe in [50, 75, 100, 120, 150, 200, 250, 300, 400, 500, 750, 1000]:
            if counts["medium"] >= 500:
                break
            w_planet = mass_probe * g_surf
            w_earth = mass_probe * 9.8
            corr_wp = f"{w_planet:.1f} N"
            wrs_wp = [
                f"{w_earth:.1f} N (used Earth gravity g = 9.8 instead of {p_name})",
                f"{mass_probe:.1f} N (confused mass with weight)",
                f"{w_planet * 2:.1f} N",
                f"{w_planet / 2:.1f} N",
                f"{w_planet + 80.0:.1f} N",
                f"{mass_probe / g_surf:.1f} N",
                f"{w_planet * 1.4:.1f} N"
            ]
            q_text_p = f"A robotic space exploration rover has a mass of {mass_probe} kg on Earth. If the gravitational acceleration on the surface of {p_name} is g = {g_surf:.2f} m·s⁻², calculate the WEIGHT of the rover on {p_name}:"
            expl_p = f"Weight w = m × g = {mass_probe} kg × {g_surf:.2f} m·s⁻² = {corr_wp}. (Note: Mass remains {mass_probe} kg everywhere)."
            add_q("medium", "Weight on Celestial Bodies", q_text_p, corr_wp, wrs_wp, "Applying", f"Calculate weight on {p_name}", expl_p)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Inclined Planes (F_g|| = mg sinθ, N = mg cosθ), Connected Bodies (Tension & Accel), Pulley Systems
    # =========================================================================

    # 1. Motion on an Inclined Plane:
    # m, θ, μ_k. Component parallel: F_g|| = mg sin θ. Normal: N = mg cos θ. Friction: f_k = μ_k mg cos θ.
    # Case A: Object sliding down an incline under gravity and friction: a = g(sin θ - μ_k cos θ)
    incline_angles = [15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0]
    incline_masses = [10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0]
    incline_muks = [0.10, 0.15, 0.20, 0.25, 0.30]

    for theta in incline_angles:
        rad = math.radians(theta)
        sin_t = math.sin(rad)
        cos_t = math.cos(rad)
        for m_obj in incline_masses:
            for muk in incline_muks:
                if counts["hard"] >= 200:
                    break
                fg_par = m_obj * 9.8 * sin_t
                norm_inc = m_obj * 9.8 * cos_t
                fk_inc = muk * norm_inc
                f_net_down = fg_par - fk_inc
                if f_net_down <= 0.1:
                    continue # does not slide down
                a_down = f_net_down / m_obj
                corr_adown = f"{a_down:.2f} m·s⁻²"
                wrs_adown = [
                    f"{9.8 * sin_t:.2f} m·s⁻² (ignored friction on incline)",
                    f"{9.8 * cos_t:.2f} m·s⁻² (used cosine instead of sine for parallel component)",
                    f"{a_down * 2:.2f} m·s⁻²",
                    f"{a_down / 2:.2f} m·s⁻²",
                    f"{(fg_par + fk_inc) / m_obj:.2f} m·s⁻² (added friction instead of opposing motion)",
                    f"{a_down + 1.5:.2f} m·s⁻²",
                    f"{a_down * 1.5:.2f} m·s⁻²"
                ]
                q_text_inc = f"A block of mass {m_obj:.0f} kg slides down an incline angled at {theta:.0f}° to the horizontal. The coefficient of kinetic friction between the block and the incline is μ_k = {muk:.2f}. Taking g = 9.8 m·s⁻², calculate the acceleration of the block down the incline:"
                expl_inc = f"1. Parallel weight component: F_g∥ = m × g × sin({theta:.0f}°) = {m_obj:.0f} × 9.8 × {sin_t:.4f} = {fg_par:.1f} N. 2. Normal force: N = m × g × cos({theta:.0f}°) = {m_obj:.0f} × 9.8 × {cos_t:.4f} = {norm_inc:.1f} N. 3. Kinetic friction: f_k = μ_k × N = {muk:.2f} × {norm_inc:.1f} = {fk_inc:.1f} N. 4. F_net = F_g∥ - f_k = {fg_par:.1f} - {fk_inc:.1f} = {f_net_down:.1f} N. a = F_net / m = {f_net_down:.1f} / {m_obj:.0f} = {corr_adown}."
                add_q("hard", "Inclined Plane Calculations", q_text_inc, corr_adown, wrs_adown, "Evaluating", "Calculate acceleration down a rough inclined plane", expl_inc)

    # 2. Connected Two-Body System: Car pulling trailer on horizontal road
    # Car (m1) exerts driving force F_engine, pulling trailer (m2) via towbar (Tension T). Friction f1 and f2.
    # System: F_engine - (f1 + f2) = (m1 + m2) * a => a = [F_engine - (f1 + f2)] / (m1 + m2)
    # Trailer: T - f2 = m2 * a => T = m2 * a + f2
    for m1_car in [1000.0, 1200.0, 1500.0]:
        for m2_trailer in [400.0, 500.0, 600.0, 800.0]:
            for f_engine in [3000.0, 4000.0, 5000.0, 6000.0]:
                if counts["hard"] >= 200:
                    break
                f1_fric = 0.10 * m1_car * 9.8
                f2_fric = 0.10 * m2_trailer * 9.8
                tot_mass = m1_car + m2_trailer
                tot_fric = f1_fric + f2_fric
                net_sys = f_engine - tot_fric
                if net_sys <= 100:
                    continue
                a_sys = net_sys / tot_mass
                t_towbar = (m2_trailer * a_sys) + f2_fric
                corr_t = f"{t_towbar:.1f} N"
                wrs_t = [
                    f"{f_engine:.1f} N (assumed towbar transmits full engine force)",
                    f"{m2_trailer * a_sys:.1f} N (neglected trailer friction f2)",
                    f"{t_towbar * 2:.1f} N",
                    f"{t_towbar / 2:.1f} N",
                    f"{(m1_car * a_sys) + f1_fric:.1f} N (calculated net force on car instead of towbar tension)",
                    f"{t_towbar + 250.0:.1f} N",
                    f"{t_towbar * 1.4:.1f} N"
                ]
                q_text_tow = f"A motor vehicle of mass {m1_car:.0f} kg tows a trailer of mass {m2_trailer:.0f} kg along a level road using a rigid horizontal towbar. The vehicle engine exerts a forward driving force of {f_engine:.0f} N. The friction opposing the car is {f1_fric:.1f} N and the friction opposing the trailer is {f2_fric:.1f} N. Calculate the TENSION (T) in the towbar:"
                expl_tow = f"1. System acceleration: a = [F_engine - (f1 + f2)] / (m1 + m2) = [{f_engine:.0f} - ({f1_fric:.1f} + {f2_fric:.1f})] / ({m1_car:.0f} + {m2_trailer:.0f}) = {net_sys:.1f} N / {tot_mass:.0f} kg = {a_sys:.3f} m·s⁻². 2. Trailer equation: T - f2 = m2 × a => T = ({m2_trailer:.0f} × {a_sys:.3f}) + {f2_fric:.1f} = {corr_t}."
                add_q("hard", "Connected Bodies", q_text_tow, corr_t, wrs_t, "Evaluating", "Calculate tension in towbar of connected vehicle system", expl_tow)

    # 3. Pulley System (Modified Atwood Machine): Block on table connected to hanging mass
    # Block m_table on horizontal table (friction f_k = μ_k * m_table * g) connected via light frictionless pulley to hanging mass m_hang.
    # m_hang * g - T = m_hang * a; T - f_k = m_table * a
    # a = (m_hang * g - f_k) / (m_table + m_hang); T = m_hang * (g - a)
    for m_tab in [2.0, 3.0, 4.0, 5.0, 6.0, 8.0]:
        for m_h in [1.0, 1.5, 2.0, 3.0, 4.0, 5.0]:
            for mu_tab in [0.10, 0.15, 0.20]:
                if counts["hard"] >= 200:
                    break
                fk_tab = mu_tab * m_tab * 9.8
                fg_hang = m_h * 9.8
                if fg_hang <= fk_tab + 0.5:
                    continue # does not move
                a_pull = (fg_hang - fk_tab) / (m_tab + m_h)
                t_pull = m_h * (9.8 - a_pull)
                corr_tpull = f"{t_pull:.2f} N"
                wrs_tpull = [
                    f"{fg_hang:.2f} N (assumed tension equals hanging weight, zero acceleration)",
                    f"{m_tab * a_pull:.2f} N (neglected table friction fk)",
                    f"{t_pull * 2:.2f} N",
                    f"{t_pull / 2:.2f} N",
                    f"{m_h * (9.8 + a_pull):.2f} N (added acceleration to g)",
                    f"{t_pull + 4.5:.2f} N",
                    f"{t_pull * 1.5:.2f} N"
                ]
                q_text_pull = f"A {m_tab:.1f} kg block resting on a horizontal table (μ_k = {mu_tab:.2f}) is connected by a light inextensible cord passing over a frictionless pulley to a hanging mass of {m_h:.1f} kg. Taking g = 9.8 m·s⁻², calculate the TENSION in the cord while the masses are in motion:"
                expl_pull = f"1. Table friction: f_k = {mu_tab:.2f} × {m_tab:.1f} × 9.8 = {fk_tab:.2f} N. 2. System acceleration: a = (m_hang × g - f_k) / (m_table + m_hang) = ({fg_hang:.2f} - {fk_tab:.2f}) / ({m_tab:.1f} + {m_h:.1f}) = {a_pull:.3f} m·s⁻². 3. Tension: T = m_hang × (g - a) = {m_h:.1f} × (9.8 - {a_pull:.3f}) = {corr_tpull}."
                add_q("hard", "Pulley Dynamics", q_text_pull, corr_tpull, wrs_tpull, "Evaluating", "Calculate cord tension in pulley system with friction", expl_pull)

    return questions

if __name__ == '__main__':
    qs = build_newtons_laws()
    out_dir = "dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_newtons_laws.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
