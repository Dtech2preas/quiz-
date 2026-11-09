import os
import sys
import random
import math
import json
import time

def generate_vertical_projectile():
    t0 = time.time()
    print("Generating Grade 12 Physical Sciences: Vertical Projectile Motion in 1D...")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../paper1_vertical_projectile.json"))

    questions = []
    seen_texts = set()
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    targets = {"easy": 300, "medium": 500, "hard": 200}

    objects = ["cricket ball", "tennis ball", "stone", "metal sphere", "golf ball", "pebble", "arrow", "lead weight", "baseball", "hockey ball"]
    settings = ["on an athletic field", "during a physics practical", "at a sports stadium", "in a laboratory demonstration", "at ground level", "on an open field", "in an outdoor test", "during a training drill"]
    structures = ["balcony", "cliff", "rooftop", "observation deck", "construction crane", "bridge", "fire tower", "vertical scaffold"]

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
        q_id = f"PS12_P1_VP_{len(questions)+1:04d}"

        questions.append({
            "id": q_id,
            "topic": "Vertical Projectile Motion",
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
                "topic": "Vertical Projectile Motion",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": diff
            }
        })
        return True

    # 1. EASY (300)
    vp_defs = [
        ("Projectile",
         "An object upon which the only force acting is the force of gravity",
         ["Satellite", "Rocket under thrust", "Glider", "Parachutist", "Aircraft", "Hovercraft"],
         "A projectile is an object in free fall moving purely under the influence of gravity."),

        ("Free fall",
         "Motion during which the only force acting on an object is the gravitational force",
         ["Terminal velocity", "Inertial motion", "Linear deceleration", "Frictional drag", "Orbital decay", "Levitation"],
         "Free fall occurs when gravitational force is the sole force acting on an object."),

        ("Gravitational acceleration (g)",
         "The constant acceleration of an object in free fall towards the centre of the Earth, equal to 9.8 m/s² downward near Earth's surface",
         ["9.8 m/s² upward", "0 m/s² at the apex", "Variable acceleration", "Terminal velocity", "Gravitational potential", "Specific gravity"],
         "Gravitational acceleration near Earth is a constant vector: 9.8 m/s² downward."),

        ("Terminal velocity",
         "The constant maximum velocity reached by an object falling through a fluid when upward drag force equals downward weight",
         ["Free fall velocity", "Initial velocity", "Escape velocity", "Instantaneous velocity", "Orbital speed", "Apex speed"],
         "Terminal velocity occurs when air resistance balances the object's weight (F_net = 0).")
    ]

    for term, f_def, wrs, expl in vp_defs:
        add_q("easy", "Definitions", f"What term is defined as: '{f_def}'?", term, wrs, expl)
        add_q("easy", "Definitions", f"In 1D kinematics, which concept is defined as '{f_def}'?", term, wrs, expl)
        add_q("easy", "Definitions", f"Identify the physical concept: '{f_def}'.", term, wrs, expl)

    vp_easy_concepts = [
        ("What is the magnitude and direction of the acceleration of a ball at the very top (highest point) of its upward trajectory in free fall?",
         "9.8 m/s² downwards",
         ["0 m/s²", "9.8 m/s² upwards", "4.9 m/s² downwards", "Depends on launch speed", "Infinite", "9.8 m/s² horizontally"],
         "Acceleration remains constant at 9.8 m/s² downward throughout the entire trajectory, even when instantaneous velocity is zero at the apex."),

        ("A tennis ball is thrown vertically upwards and caught at the same launch height. How does the time taken to rise compare to the time taken to fall back down (neglecting air resistance)?",
         "Time to rise equals time to fall (time_up = time_down)",
         ["Time to rise is twice the time to fall", "Time to rise is half the time to fall", "Time to fall is always longer", "Time to rise depends on mass", "Time to fall is zero"],
         "In symmetric free fall without air resistance, the upward and downward times are strictly equal."),

        ("A stone is projected vertically upwards with a velocity of 25 m/s. Neglecting air friction, with what speed will it return to the exact same launch position?",
         "25 m/s downwards",
         ["0 m/s", "12.5 m/s downwards", "50 m/s downwards", "9.8 m/s downwards", "Depends on stone mass"],
         "By conservation of mechanical energy, return speed equals launch speed (direction is reversed)."),

        ("What is the instantaneous velocity of a projectile at its maximum height?",
         "0 m/s",
         ["9.8 m/s downwards", "9.8 m/s upwards", "Equal to initial velocity", "Half the initial velocity", "Undefined"],
         "At the apex of vertical flight, the projectile momentarily halts before reversing direction: v = 0 m/s."),

        ("On a position vs time (y vs t) graph for a projectile launched upwards, what shape does the trajectory curve represent?",
         "A parabolic curve curving downwards (concave downward)",
         ["A straight line with negative slope", "A horizontal line", "An exponential curve", "A sinusoidal wave", "A circle"],
         "Because position y = v_i*t - 0.5*g*t², the position-time graph is a concave-downward parabola."),

        ("On a velocity vs time (v vs t) graph for vertical projectile motion (taking upward as positive), what is represented by the gradient (slope) of the line?",
         "Gravitational acceleration (-9.8 m/s²)",
         ["Displacement", "Maximum height", "Initial velocity", "Air resistance", "Force of launch"],
         "The gradient of a velocity-time graph represents acceleration: slope = delta v / delta t = -9.8 m/s².")
    ]

    for q_c, a_c, w_c, expl_c in vp_easy_concepts:
        add_q("easy", "Kinematic Concepts", q_c, a_c, w_c, expl_c)

    # Easy Calculations with large combination space
    while diff_counts["easy"] < targets["easy"]:
        v_rand = round(random.uniform(10.0, 90.0), 1)
        t_rand = round(v_rand / 9.8, 2)
        obj = random.choice(objects)
        st = random.choice(settings)
        q_r = f"A {obj} is projected vertically upwards {st} with an initial speed of {v_rand} m/s. Calculate the time required to reach its maximum height (g = 9.8 m/s²)."
        w_r = [f"{round(t_rand * 2, 2)} s", f"{round(t_rand * 0.5, 2)} s", f"{round(v_rand / 4.9, 2)} s", f"{round(t_rand + 1.5, 2)} s", f"{round(t_rand - 0.8, 2)} s", f"{round(t_rand * 1.3, 2)} s"]
        add_q("easy", "Apex Calculations", q_r, f"{t_rand} s", w_r, f"t = v_i / g = {v_rand} / 9.8 = {t_rand} s.")

    # 2. MEDIUM (500)
    # Dropped objects from structures: v_f = sqrt(2gh), t = sqrt(2h/g)
    for h_drop in [10, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80, 100, 120, 125]:
        v_strike = round(math.sqrt(2 * 9.8 * h_drop), 2)
        t_fall = round(math.sqrt(2 * h_drop / 9.8), 2)
        for obj in objects[:5]:
            struc = random.choice(structures)
            q_drop_v = f"A {obj} is released from rest from a {struc} {h_drop} m above the ground. Calculate its speed immediately before hitting the ground."
            w_drop_v = [f"{round(v_strike * 0.5, 2)} m/s", f"{round(v_strike * 1.5, 2)} m/s", f"{round(2 * 9.8 * h_drop, 2)} m/s", f"{round(h_drop / 9.8, 2)} m/s", f"{round(v_strike + 8.5, 2)} m/s", f"{round(h_drop * 9.8, 2)} m/s"]
            add_q("medium", "Dropped Objects", q_drop_v, f"{v_strike} m/s", w_drop_v, f"v_f = sqrt(2 * g * h) = sqrt(2 * 9.8 * {h_drop}) = {v_strike} m/s.")

            q_drop_t = f"How long does it take for a {obj} dropped from rest from a {struc} {h_drop} m tall to hit the ground below?"
            w_drop_t = [f"{round(t_fall * 2, 2)} s", f"{round(t_fall * 0.5, 2)} s", f"{round(h_drop / 9.8, 2)} s", f"{round(t_fall + 1.5, 2)} s", f"{round(2 * h_drop / 9.8, 2)} s", f"{round(t_fall * 1.25, 2)} s"]
            add_q("medium", "Dropped Objects", q_drop_t, f"{t_fall} s", w_drop_t, f"t = sqrt(2 * h / g) = sqrt(2 * {h_drop} / 9.8) = {t_fall} s.")

    # Top up medium with maximum height and thrown downwards
    while diff_counts["medium"] < targets["medium"]:
        if random.choice([True, False]):
            v_t = round(random.uniform(12.0, 55.0), 1)
            h_t = round((v_t ** 2) / (2 * 9.8), 2)
            obj = random.choice(objects)
            st = random.choice(settings)
            q_h_rand = f"A {obj} is launched vertically upwards {st} with an initial velocity of {v_t} m/s. Determine the maximum height reached above the launch position."
            w_h_rand = [f"{round(h_t * 0.5, 2)} m", f"{round(h_t * 2, 2)} m", f"{round(v_t * 9.8, 2)} m", f"{round((v_t**2)/9.8, 2)} m", f"{round(h_t + 14.5, 2)} m", f"{round(h_t - 9.2, 2)} m"]
            add_q("medium", "Maximum Height", q_h_rand, f"{h_t} m", w_h_rand, f"h = v_i^2 / (2g) = {v_t}^2 / (2 * 9.8) = {h_t} m.")
        else:
            v_down = round(random.uniform(4.0, 20.0), 1)
            h_cliff = round(random.uniform(15.0, 80.0), 1)
            v_fin_down = round(math.sqrt(v_down**2 + 2 * 9.8 * h_cliff), 2)
            obj = random.choice(objects)
            struc = random.choice(structures)
            q_down_r = f"A {obj} is thrown vertically downwards from a {struc} {h_cliff} m high at an initial speed of {v_down} m/s. What is its velocity upon impact?"
            w_down_r = [f"{round(math.sqrt(2 * 9.8 * h_cliff), 2)} m/s", f"{round(v_fin_down * 1.3, 2)} m/s", f"{round(v_fin_down * 0.7, 2)} m/s", f"{round(v_down + 9.8, 2)} m/s", f"{round(v_fin_down + 11.2, 2)} m/s", f"{round(v_fin_down - 8.5, 2)} m/s"]
            add_q("medium", "Thrown Downwards", q_down_r, f"{v_fin_down} m/s", w_down_r, f"v_f = sqrt(v_i^2 + 2gh) = sqrt({v_down}^2 + 2*9.8*{h_cliff}) = {v_fin_down} m/s.")

    # 3. HARD (200)
    while diff_counts["hard"] < targets["hard"]:
        h_cliff_r = round(random.uniform(20.0, 90.0), 1)
        v_launch_r = round(random.uniform(10.0, 40.0), 1)
        disc_r = (v_launch_r ** 2) - (4 * 4.9 * (-h_cliff_r))
        t_sol = round((v_launch_r + math.sqrt(disc_r)) / (2 * 4.9), 2)
        v_strike_hard = round(math.sqrt(v_launch_r**2 + 2 * 9.8 * h_cliff_r), 2)
        obj = random.choice(objects)
        struc = random.choice(structures)

        if random.choice([True, False]):
            q_hard = f"A {obj} is projected vertically upwards from the edge of a {struc} {h_cliff_r} m high at an initial velocity of {v_launch_r} m/s. It travels upward, misses the edge on its descent, and strikes the ground below. Calculate the total time of flight."
            w_hard = [f"{round(v_launch_r / 9.8, 2)} s", f"{round(math.sqrt(2 * h_cliff_r / 9.8), 2)} s", f"{round(t_sol * 1.4, 2)} s", f"{round(t_sol * 0.6, 2)} s", f"{round(t_sol + 2.5, 2)} s", f"{round(t_sol - 1.8, 2)} s"]
            add_q("hard", "Cliff Projection and Quadratic Kinematics", q_hard, f"{t_sol} s", w_hard, f"Using Delta y = v_i*t - 0.5*g*t^2: -{h_cliff_r} = {v_launch_r}*t - 4.9*t^2. Solving quadratic yields t = {t_sol} s.")
        else:
            q_hard_v = f"A {obj} is thrown vertically upwards from a {struc} {h_cliff_r} m above the ground with an initial speed of {v_launch_r} m/s. Calculate the magnitude of its velocity as it strikes the ground at the bottom."
            w_hard_v = [f"{v_launch_r} m/s", f"{round(math.sqrt(2 * 9.8 * h_cliff_r), 2)} m/s", f"{round(v_strike_hard * 1.25, 2)} m/s", f"{round(v_strike_hard * 0.75, 2)} m/s", f"{round(v_strike_hard + 14.2, 2)} m/s", f"{round(v_strike_hard - 9.6, 2)} m/s"]
            add_q("hard", "Cliff Projection and Quadratic Kinematics", q_hard_v, f"{v_strike_hard} m/s", w_hard_v, f"v_f = sqrt(v_i^2 + 2gh) = sqrt({v_launch_r}^2 + 2*9.8*{h_cliff_r}) = {v_strike_hard} m/s.")

    assert diff_counts == targets, f"Mismatch: {diff_counts} vs {targets}"
    assert len(questions) == 1000, f"Expected 1000, got {len(questions)}"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions ({diff_counts}).")
    return questions

if __name__ == "__main__":
    generate_vertical_projectile()
