import os
import sys
import random
import math
import json
import time

def generate_momentum_impulse():
    t0 = time.time()
    print("Generating Grade 12 Physical Sciences: Momentum and Impulse...")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper1_momentum_impulse.json"))

    questions = []
    seen_texts = set()
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    targets = {"easy": 300, "medium": 500, "hard": 200}

    vehicles = ["sports sedan", "minibus taxi", "freight truck", "SUV", "delivery motorcycle", "compact hatchback", "electric car", "pickup truck"]
    sports = ["cricket ball", "tennis ball", "golf ball", "soccer ball", "hockey ball", "baseball", "squash ball"]

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
        q_id = f"PS12_P1_MOM_{len(questions)+1:04d}"

        questions.append({
            "id": q_id,
            "topic": "Momentum and Impulse",
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
                "topic": "Momentum and Impulse",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": diff
            }
        })
        return True

    # 1. EASY (300)
    mom_defs = [
        ("Linear momentum (p)",
         "The product of an object's mass and its velocity",
         ["Force times time", "Mass times acceleration", "Rate of change of kinetic energy", "Work divided by time", "Impulse divided by mass", "Energy per unit mass"],
         "Linear momentum is defined as the product of mass and velocity: p = m * v."),

        ("Impulse (J)",
         "The product of the resultant/net force acting on an object and the time for which the resultant/net force acts",
         ["Rate of change of momentum", "Change in kinetic energy", "Work done per unit time", "Force per unit mass", "Mass times velocity squared", "Total mechanical energy"],
         "Impulse is defined as J = F_net * delta t = delta p."),

        ("Isolated system (Closed system)",
         "A system on which the resultant/net external force is zero",
         ["An open thermodynamic system", "A system without kinetic energy", "A frictionless surface", "A system where all objects are at rest", "A vacuum chamber", "A frame of zero mass"],
         "An isolated system experiences no net external forces, allowing momentum to be conserved."),

        ("Principle of Conservation of Linear Momentum",
         "The total linear momentum of an isolated system remains constant in both magnitude and direction",
         ["Work-Energy Theorem", "Newton's First Law", "Law of Conservation of Mechanical Energy", "Newton's Third Law", "Coulomb's Law", "Hooke's Law"],
         "Total initial linear momentum equals total final linear momentum in an isolated system."),

        ("Elastic collision",
         "A collision in which both total linear momentum and total kinetic energy are conserved",
         ["Inelastic collision", "Completely inelastic collision", "Explosive interaction", "Plastic deformation", "Super-elastic event", "Frictional impact"],
         "In an elastic collision, total kinetic energy is conserved: E_k(initial) = E_k(final)."),

        ("Inelastic collision",
         "A collision in which total linear momentum is conserved, but total kinetic energy is not conserved",
         ["Elastic collision", "Isolated explosion", "Conservative interaction", "Perpetual collision", "Harmonic collision", "Reversible collision"],
         "In an inelastic collision, kinetic energy is converted into heat, sound, and internal deformation energy.")
    ]

    for term, f_def, wrs, expl in mom_defs:
        add_q("easy", "Definitions", f"What term is defined as: '{f_def}'?", term, wrs, expl)
        add_q("easy", "Definitions", f"In classical mechanics, which concept is defined as: '{f_def}'?", term, wrs, expl)
        add_q("easy", "Definitions", f"Identify the physical quantity or principle: '{f_def}'.", term, wrs, expl)

    mom_easy_concepts = [
        ("What is the SI unit of linear momentum?",
         "kg·m/s (or N·s)",
         ["N/s", "J·s", "kg·m/s²", "W·s", "N·m", "kg/m"],
         "The SI unit of momentum is kilogram metre per second (kg·m/s), equivalent to newton second (N·s)."),

        ("Which physical quantity is defined as the rate of change of momentum (delta p / delta t)?",
         "Resultant/net force (F_net)",
         ["Impulse", "Kinetic energy", "Work done", "Power", "Inertia", "Velocity"],
         "Newton's Second Law in terms of momentum states that F_net = delta p / delta t."),

        ("How does a vehicle's crumple zone enhance passenger safety during a severe frontal impact?",
         "It increases collision impact time (delta t), thereby decreasing the net impact force on occupants",
         ["It decreases collision time to stop the car faster", "It eliminates all momentum from the universe", "It converts kinetic energy into electrical charge", "It prevents the seatbelts from locking", "It increases passenger inertia"],
         "Because F_net = delta p / delta t, extending collision duration (delta t) reduces the dangerous peak force (F_net)."),

        ("Why does a wicketkeeper or fielder pull their hands backward when catching a fast-moving cricket ball?",
         "To increase the contact time (delta t), reducing the impact force on the hands",
         ["To increase the ball's final momentum", "To reduce the impulse delivered by the ball", "To decrease the ball's mass", "To violate Newton's Third Law", "To stop the ball instantaneously"],
         "Drawing hands back extends the deceleration time, substantially reducing the impact force.")
    ]

    for q_c, a_c, w_c, expl_c in mom_easy_concepts:
        add_q("easy", "Safety and Concepts", q_c, a_c, w_c, expl_c)

    # Easy Calculations: p = m * v
    while diff_counts["easy"] < targets["easy"]:
        m_car = round(random.uniform(500, 2500), 0)
        v_car = round(random.uniform(10, 35), 1)
        p_val = round(m_car * v_car, 1)
        veh = random.choice(vehicles)
        q_p = f"A {veh} of mass {int(m_car)} kg travels due east at a velocity of {v_car} m/s. Calculate the magnitude of its linear momentum."
        w_p = [f"{round(m_car / v_car, 1)} kg·m/s", f"{round(p_val * 2, 1)} kg·m/s", f"{round(p_val * 0.5, 1)} kg·m/s", f"{round(m_car * 9.8, 1)} kg·m/s", f"{round(p_val + 5000, 1)} kg·m/s", f"{round(v_car * 9.8, 1)} kg·m/s"]
        add_q("easy", "Momentum Calculations", q_p, f"{p_val} kg·m/s", w_p, f"p = m * v = {int(m_car)} * {v_car} = {p_val} kg·m/s east.")

    # 2. MEDIUM (500)
    # Impulse: J = F_net * delta t = delta p = m * (v_f - v_i)
    while diff_counts["medium"] < targets["medium"]:
        if random.choice([True, False]):
            # Rebound scenario (ball hits wall/bat)
            m_ball = round(random.uniform(0.1, 0.6), 2)
            v_i_b = round(random.uniform(15.0, 35.0), 1)
            v_f_b = round(random.uniform(12.0, 30.0), 1)
            # Taking rebound direction as positive => delta v = v_f_b - (-v_i_b) = v_f_b + v_i_b
            delta_p = round(m_ball * (v_f_b + v_i_b), 2)
            sp = random.choice(sports)
            q_reb = f"A {m_ball} kg {sp} moving horizontally to the left at {v_i_b} m/s strikes a rigid vertical wall and rebounds to the right at {v_f_b} m/s. Calculate the magnitude of the impulse delivered to the ball."
            w_reb = [f"{round(m_ball * abs(v_f_b - v_i_b), 2)} N·s", f"{round(delta_p * 2, 2)} N·s", f"{round(delta_p * 0.5, 2)} N·s", f"{round(m_ball * v_i_b, 2)} N·s", f"{round(delta_p + 5.0, 2)} N·s", f"{round(m_ball * 9.8, 2)} N·s"]
            add_q("medium", "Impulse and Rebounds", q_reb, f"{delta_p} N·s", w_reb, f"Taking right as positive: J = delta p = m(v_f - v_i) = {m_ball} * ({v_f_b} - (-{v_i_b})) = {delta_p} N·s.")
        else:
            # 1D Inelastic collision: stick together m1*v1 + m2*v2 = (m1+m2)*v_f
            m1 = random.randint(800, 2000)
            m2 = random.randint(600, 1800)
            v1 = random.randint(15, 30)
            v2 = 0 # stationary target
            v_fin = round((m1 * v1) / (m1 + m2), 2)
            veh1 = random.choice(vehicles)
            veh2 = random.choice([v for v in vehicles if v != veh1])
            q_col = f"A {m1} kg {veh1} travelling at {v1} m/s east collides with a stationary {m2} kg {veh2}. After the collision, the two vehicles lock together. Calculate their common final velocity immediately after collision."
            w_col = [f"{round(v1 * 0.5, 2)} m/s", f"{round(v1 * (m1 / m2), 2)} m/s", f"{round(v_fin * 1.5, 2)} m/s", f"{round(v_fin * 0.5, 2)} m/s", f"{round(v_fin + 4.2, 2)} m/s", f"{v1} m/s"]
            add_q("medium", "Inelastic Collisions", q_col, f"{v_fin} m/s", w_col, f"Total p_initial = Total p_final => ({m1} * {v1}) + 0 = ({m1} + {m2}) * v_f => v_f = {m1 * v1} / {m1 + m2} = {v_fin} m/s.")

    # 3. HARD (200)
    # Average impact force calculation: F_net = m * (v_f - v_i) / delta t
    while diff_counts["hard"] < targets["hard"]:
        if random.choice([True, False]):
            m_imp = round(random.uniform(0.15, 1.2), 2)
            v_in_f = round(random.uniform(20.0, 45.0), 1)
            v_out_f = round(random.uniform(15.0, 40.0), 1)
            dt = round(random.uniform(0.005, 0.030), 4) # milliseconds
            F_impact = round(m_imp * (v_out_f + v_in_f) / dt, 1)
            sp = random.choice(sports)
            q_fnet = f"A {m_imp} kg {sp} travelling at {v_in_f} m/s hits a wall and rebounds in the opposite direction at {v_out_f} m/s. The contact duration is {dt} s. Calculate the magnitude of the average net force exerted on the ball by the wall."
            w_fnet = [f"{round(m_imp * abs(v_out_f - v_in_f) / dt, 1)} N", f"{round(F_impact * 2, 1)} N", f"{round(F_impact * 0.5, 1)} N", f"{round(m_imp * 9.8, 1)} N", f"{round(F_impact + 500, 1)} N", f"{round(m_imp * (v_out_f + v_in_f), 1)} N"]
            add_q("hard", "Impact Forces and Contact Time", q_fnet, f"{F_impact} N", w_fnet, f"F_net = delta p / delta t = {m_imp} * ({v_out_f} - (-{v_in_f})) / {dt} = {F_impact} N.")
        else:
            # Gun/Cannon Recoil: 0 = m_gun * v_gun + m_proj * v_proj
            m_gun = random.randint(300, 1500) # kg cannon
            m_shell = random.randint(5, 25) # kg shell
            v_shell = random.randint(200, 600) # m/s
            v_recoil = round((m_shell * v_shell) / m_gun, 2)
            q_rec = f"A cannon of mass {m_gun} kg fires a {m_shell} kg artillery shell horizontally at a muzzle speed of {v_shell} m/s. Assuming the system is isolated, calculate the recoil speed of the cannon immediately upon firing."
            w_rec = [f"{round(v_shell * 0.5, 2)} m/s", f"{round((m_gun * v_shell) / m_shell, 2)} m/s", f"{round(v_recoil * 1.5, 2)} m/s", f"{round(v_recoil * 0.5, 2)} m/s", f"{round(v_recoil + 3.5, 2)} m/s", f"0.00 m/s"]
            add_q("hard", "Recoil and Explosions", q_rec, f"{v_recoil} m/s", w_rec, f"p_total = 0 => m_gun * v_recoil = m_shell * v_shell => v_recoil = ({m_shell} * {v_shell}) / {m_gun} = {v_recoil} m/s.")

    assert diff_counts == targets, f"Mismatch: {diff_counts} vs {targets}"
    assert len(questions) == 1000, f"Expected 1000, got {len(questions)}"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions ({diff_counts}).")
    return questions

if __name__ == "__main__":
    generate_momentum_impulse()
