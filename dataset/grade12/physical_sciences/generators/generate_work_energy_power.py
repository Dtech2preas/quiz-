import os
import sys
import random
import math
import json
import time

def generate_work_energy_power():
    t0 = time.time()
    print("Generating Grade 12 Physical Sciences: Work, Energy and Power...")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper1_work_energy_power.json"))

    questions = []
    seen_texts = set()
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    targets = {"easy": 300, "medium": 500, "hard": 200}

    objects = ["crate", "trolley", "sled", "mining cart", "block", "box", "luggage case", "cargo container"]
    surfaces = ["horizontal floor", "inclined ramp", "level conveyor", "rough surface", "frictionless plane", "warehouse deck"]

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
        q_id = f"PS12_P1_WEP_{len(questions)+1:04d}"

        questions.append({
            "id": q_id,
            "topic": "Work, Energy and Power",
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
                "topic": "Work, Energy and Power",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": diff
            }
        })
        return True

    # 1. EASY (300)
    wep_defs = [
        ("Work done by a constant force",
         "The product of the magnitude of the force, the magnitude of the displacement, and the cosine of the angle between the force and the displacement (W = F * Delta x * cos(theta))",
         ["The rate at which work is performed", "The change in momentum over time", "The product of mass and acceleration", "The total mechanical energy in a closed system", "The force applied per unit area", "The kinetic energy per unit time"],
         "Work is defined as W = F * Delta x * cos(theta)."),

        ("Work-Energy Theorem",
         "The total/net work done on an object is equal to the change in the object's kinetic energy (W_net = Delta E_k)",
         ["Total mechanical energy is strictly conserved", "Energy cannot be transformed into non-mechanical forms", "Work done equals the change in momentum", "Power is inversely proportional to net work", "Potential energy equals kinetic energy", "Force equals rate of change of work"],
         "Work-Energy Theorem states that W_net = Delta E_k = 0.5*m*v_f^2 - 0.5*m*v_i^2."),

        ("Conservative force",
         "A force for which the work done in moving an object between two points is independent of the path taken",
         ["Non-conservative force", "Frictional force", "Tension force", "Air resistance", "Applied pushing force", "Viscous drag force"],
         "Gravitational force and elastic spring force are classic examples of conservative forces."),

        ("Non-conservative force",
         "A force for which the work done in moving an object between two points depends on the path taken",
         ["Conservative force", "Gravitational force", "Electrostatic force", "Nuclear force", "Centripetal force", "Weight"],
         "Frictional force, air resistance, and tension are non-conservative forces."),

        ("Principle of Conservation of Mechanical Energy",
         "The total mechanical energy (sum of gravitational potential energy and kinetic energy) in an isolated system remains constant",
         ["Work-Energy Theorem", "Newton's First Law", "Law of Conservation of Linear Momentum", "Coulomb's Law", "First Law of Thermodynamics", "Hooke's Law"],
         "Mechanical energy is conserved when only conservative forces do work: E_mech = E_k + E_p = constant."),

        ("Power (P)",
         "The rate at which work is done or the rate at which energy is expended/transferred (P = W / Delta t)",
         ["The total work done by a net force", "The change in kinetic energy per metre", "The product of force and mass", "The force exerted per unit distance", "The total electrical potential", "The rate of change of momentum"],
         "Power is defined as P = W / Delta t, measured in watts (W).")
    ]

    for term, f_def, wrs, expl in wep_defs:
        add_q("easy", "Definitions", f"What term or principle is defined as: '{f_def}'?", term, wrs, expl)
        add_q("easy", "Definitions", f"In physics, which concept corresponds to: '{f_def}'?", term, wrs, expl)
        add_q("easy", "Definitions", f"Identify the physical concept: '{f_def}'.", term, wrs, expl)

    # Conceptual Easy
    wep_easy_concepts = [
        ("What is the SI unit of work and energy?",
         "Joule (J) [equivalent to N·m or kg·m²/s²]",
         ["Watt (W)", "Newton (N)", "Pascal (Pa)", "kg·m/s", "N/s", "Coulomb (C)"],
         "Work and energy are measured in joules (J)."),

        ("What is the SI unit of power?",
         "Watt (W) [equivalent to J/s]",
         ["Joule (J)", "Newton (N)", "Volt (V)", "Ampere (A)", "Ohm", "Farad"],
         "Power is measured in watts (W), where 1 W = 1 J/s."),

        ("A student carries a 10 kg backpack while walking horizontally at constant velocity across a level room. What is the work done by the vertical lifting force exerted by the student's shoulders on the backpack?",
         "0 J (zero work)",
         ["98 J", "980 J", "Depends on walking speed", "Negative 98 J", "Infinite"],
         "Because the lifting force is vertical (theta = 90°) and displacement is horizontal, W = F * Delta x * cos(90°) = 0 J."),

        ("What type of work is done by kinetic friction on a sliding object moving across a rough surface?",
         "Negative work (theta = 180°, cos(180°) = -1)",
         ["Positive work", "Zero work", "Conservative work", "Potential work", "Infinite work"],
         "Friction opposes the direction of displacement, so cos(180°) = -1, meaning friction does negative work.")
    ]

    for q_c, a_c, w_c, expl_c in wep_easy_concepts:
        add_q("easy", "Work and Power Fundamentals", q_c, a_c, w_c, expl_c)

    # Easy Calculations: W = F * d
    while diff_counts["easy"] < targets["easy"]:
        f_rand = random.randint(15, 120) * 10
        d_rand = random.randint(2, 45)
        w_rand = f_rand * d_rand
        obj = random.choice(objects)
        surf = random.choice(surfaces)
        q_calc = f"A horizontal force of {f_rand} N pushes a {obj} across a {surf} through a distance of {d_rand} m in the direction of the force. Calculate the work done by the applied force."
        w_calc = [f"{round(f_rand / d_rand, 1)} J", f"{w_rand * 2} J", f"{round(w_rand * 0.5, 1)} J", f"{round(f_rand * 9.8, 1)} J", f"{w_rand + 250} J", f"{round(d_rand * 9.8, 1)} J"]
        add_q("easy", "Work Calculations", q_calc, f"{w_rand} J", w_calc, f"W = F * Delta x * cos(0°) = {f_rand} * {d_rand} * 1 = {w_rand} J.")

    # 2. MEDIUM (500)
    # Work done at an angle: W = F * d * cos(theta)
    angles_w = [20, 25, 30, 35, 40, 45, 60]
    for ang in angles_w:
        rad = math.radians(ang)
        for f_pull in [40, 60, 80, 100, 120, 150, 200]:
            for dist in [5, 10, 15, 20, 25]:
                w_ang = round(f_pull * dist * math.cos(rad), 1)
                obj = random.choice(objects)
                q_wang = f"A worker pulls a {obj} with a force of {f_pull} N directed at an angle of {ang}° above the horizontal. The {obj} moves a horizontal distance of {dist} m. Calculate the work done by the pulling force."
                w_wang = [f"{round(f_pull * dist, 1)} J", f"{round(f_pull * dist * math.sin(rad), 1)} J", f"{round(w_ang * 1.5, 1)} J", f"{round(w_ang * 0.5, 1)} J", f"{round(w_ang + 80, 1)} J", f"{round(f_pull * 9.8, 1)} J"]
                add_q("medium", "Work at an Angle", q_wang, f"{w_ang} J", w_wang, f"W = F * Delta x * cos({ang}°) = {f_pull} * {dist} * cos({ang}°) = {w_ang} J.")

    # Average Power: P = W / Delta t or P = F * v
    for f_p in [200, 350, 500, 800, 1200, 1500, 2000]:
        for v_p in [5, 10, 15, 20, 25, 30]:
            p_watt = f_p * v_p
            p_kw = round(p_watt / 1000, 2)
            q_pow = f"A motor vehicle engine delivers a driving force of {f_p} N to propel a car at a constant cruising speed of {v_p} m/s along a flat freeway. What is the power output of the engine in kilowatts (kW)?"
            w_pow = [f"{round(f_p / v_p, 2)} kW", f"{round(p_kw * 2, 2)} kW", f"{round(p_kw * 0.5, 2)} kW", f"{round(p_watt / 100, 2)} kW", f"{round(p_kw + 12, 2)} kW", f"{round(f_p * 9.8 / 1000, 2)} kW"]
            add_q("medium", "Power and Constant Velocity", q_pow, f"{p_kw} kW", w_pow, f"P = F * v = {f_p} N * {v_p} m/s = {p_watt} W = {p_kw} kW.")

    # Top up medium with work done by gravity & friction
    while diff_counts["medium"] < targets["medium"]:
        m_med = random.randint(10, 80)
        h_med = round(random.uniform(3.0, 25.0), 1)
        wg_val = round(m_med * 9.8 * h_med, 1)
        obj = random.choice(objects)
        q_wg = f"A {m_med} kg {obj} falls vertically from rest through a height of {h_med} m. Calculate the work done by the gravitational force on the {obj}."
        w_wg = [f"{round(m_med * h_med, 1)} J", f"{round(wg_val * 1.5, 1)} J", f"{round(wg_val * 0.5, 1)} J", f"{round(wg_val + 200, 1)} J", f"{round(m_med * 9.8, 1)} J", f"0.0 J"]
        add_q("medium", "Work done by Gravity", q_wg, f"{wg_val} J", w_wg, f"W_g = m * g * h = {m_med} * 9.8 * {h_med} = {wg_val} J.")

    # 3. HARD (200)
    # Work-Energy Theorem: W_net = Delta E_k => F_net * d = 0.5 * m * (v_f^2 - v_i^2)
    while diff_counts["hard"] < targets["hard"]:
        if random.choice([True, False]):
            m_h = random.randint(800, 2200) # car
            v_i_kmh = random.randint(15, 35) # m/s
            v_f_kmh = random.randint(0, 10) # m/s
            d_stop = round(random.uniform(20, 60), 1)
            # Delta E_k = 0.5 * m * (v_f^2 - v_i^2)
            delta_ek = 0.5 * m_h * (v_f_kmh**2 - v_i_kmh**2)
            f_brake = round(abs(delta_ek) / d_stop, 1)
            q_brake = f"A vehicle of mass {m_h} kg travelling at {v_i_kmh} m/s applies its brakes and slows down to {v_f_kmh} m/s over a stopping distance of {d_stop} m on a level road. Calculate the magnitude of the average net braking force acting on the vehicle."
            w_brake = [f"{round(f_brake * 1.5, 1)} N", f"{round(f_brake * 0.5, 1)} N", f"{round(m_h * (v_i_kmh - v_f_kmh), 1)} N", f"{round(abs(delta_ek) / 9.8, 1)} N", f"{round(f_brake + 1200, 1)} N", f"{round(m_h * 9.8, 1)} N"]
            add_q("hard", "Work-Energy Theorem Applications", q_brake, f"{f_brake} N", w_brake, f"W_net = Delta E_k => F_net * d = 0.5 * {m_h} * ({v_i_kmh}^2 - {v_f_kmh}^2) = {abs(delta_ek):.1f} J. F_net = {abs(delta_ek):.1f} / {d_stop} = {f_brake} N.")
        else:
            # Mechanical energy conservation with roller coaster / pendulum: v = sqrt(2 * g * h)
            h_pend = round(random.uniform(2.0, 15.0), 2)
            v_pend = round(math.sqrt(2 * 9.8 * h_pend), 2)
            m_cart = random.randint(50, 500)
            q_pend = f"A {m_cart} kg roller coaster cart starts from rest at the top of a frictionless track at height h = {h_pend} m above ground level. Using the principle of conservation of mechanical energy, calculate the speed of the cart at the bottom of the track."
            w_pend = [f"{round(math.sqrt(9.8 * h_pend), 2)} m/s", f"{round(v_pend * 1.4, 2)} m/s", f"{round(v_pend * 0.6, 2)} m/s", f"{round(2 * 9.8 * h_pend, 2)} m/s", f"{round(v_pend + 4.5, 2)} m/s", f"{round(h_pend * 9.8, 2)} m/s"]
            add_q("hard", "Conservation of Mechanical Energy", q_pend, f"{v_pend} m/s", w_pend, f"E_mech(top) = E_mech(bottom) => m*g*h = 0.5*m*v^2 => v = sqrt(2 * g * h) = sqrt(2 * 9.8 * {h_pend}) = {v_pend} m/s.")

    assert diff_counts == targets, f"Mismatch: {diff_counts} vs {targets}"
    assert len(questions) == 1000, f"Expected 1000, got {len(questions)}"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions ({diff_counts}).")
    return questions

if __name__ == "__main__":
    generate_work_energy_power()
