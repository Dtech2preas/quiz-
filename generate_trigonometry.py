import random
import math
import sympy as sp
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

def generate_trigonometry():
    gen = TopicGenerator("Trigonometry", "TRIG", ["trig identities", "solving trig equations", "sine rule", "cosine rule"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        if subtopic == "trig identities":
            # Just test basic values or reductions
            # e.g., cos(180 - x), sin(90 - x), exact values
            angles_exact = [(30, "1/2", "\\sqrt{3}/2", "1/\\sqrt{3}"),
                            (45, "1/\\sqrt{2}", "1/\\sqrt{2}", "1"),
                            (60, "\\sqrt{3}/2", "1/2", "\\sqrt{3}")]
            if difficulty == "easy":
                ang, s_val, c_val, t_val = random.choice(angles_exact)
                func = random.choice(["\\sin", "\\cos", "\\tan"])
                q = f"What is the exact value of ${func}({ang}^\\circ)$?"
                correct = s_val if func == "\\sin" else (c_val if func == "\\cos" else t_val)
                wrongs = [w for _, s, c, t in angles_exact for w in (s, c, t)]
                wrongs = list(set([w for w in wrongs if w != correct])) + ["0", "1", "-1"]
                exp = f"From special triangles, ${func}({ang}^\\circ) = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Reduction formula
                angle = random.choice([120, 135, 150, 210, 225, 240, 300, 315, 330])
                func = random.choice(["\\sin", "\\cos", "\\tan"])
                q = f"Evaluate without a calculator: ${func}({angle}^\\circ)$."
                # use math to find val
                rad = math.radians(angle)
                if func == "\\sin": v = math.sin(rad)
                elif func == "\\cos": v = math.cos(rad)
                else: v = math.tan(rad)

                # Check quadrant
                sign = "" if v > 0 else "-"
                # Reference angle
                ref = angle % 90 if angle % 90 <= 45 else 90 - (angle % 90)
                if ref == 0: ref = 90 # for 180, 270...
                for a, s, c, t in angles_exact:
                    if a == ref:
                        v_str = s if func == "\\sin" else (c if func == "\\cos" else t)
                        break
                correct = f"{sign}{v_str}" if v_str != "0" else "0"
                # Some wrongs
                wrongs = []
                for a, s, c, t in angles_exact:
                    wrongs.extend([s, f"-{s}", c, f"-{c}", t, f"-{t}"])
                wrongs = list(set([w for w in wrongs if w != correct]))
                exp = f"Reference angle is ${ref}^\\circ$. Based on the CAST diagram, ${func}({angle}^\\circ) = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # Compound / double angle value
                # e.g. 2sin15cos15
                q = f"Evaluate: $2\\sin(15^\\circ)\\cos(15^\\circ)$"
                correct = "1/2"
                wrongs = ["1", "\\sqrt{3}/2", "1/\\sqrt{2}", "\\sqrt{3}", "0", "-1/2", "-\\sqrt{3}/2", "2"]
                exp = f"Using double angle identity: $2\\sin(x)\\cos(x) = \\sin(2x) \\implies 2\\sin(15^\\circ)\\cos(15^\\circ) = \\sin(30^\\circ) = 1/2$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "solving trig equations":
            if difficulty == "easy":
                # Basic
                v = random.choice(["0.5", "\\frac{1}{2}", "0.707", "0.866", "1"])
                angle = random.randint(10, 80)
                val = round(math.sin(math.radians(angle)), 2)
                q = f"Solve for $\\theta \\in [0^\\circ; 90^\\circ]$: $\\sin(\\theta) = {val}$ (correct to 1 decimal place)."
                correct = f"{angle}.0^\\circ" if float(angle).is_integer() else f"{angle}^\\circ"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0, 90), 1)
                    w_str = f"{w}^\\circ"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"$\\theta = \\sin^{{-1}}({val}) \\approx {angle}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "medium":
                # General solution or interval
                # tan(x) = a
                a = random.randint(1, 5)
                q = f"Find the reference angle for the equation $\\tan(x) = {-a}$ (correct to 1 decimal place)."
                ref = math.degrees(math.atan(a))
                correct = f"{ref:.1f}^\\circ"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0, 90), 1)
                    w_str = f"{w}^\\circ"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Reference angle is always positive. $\\tan^{{-1}}({a}) = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # Quadratic trig eq
                # 2cos^2 x - cos x - 1 = 0
                # (2cos x + 1)(cos x - 1) = 0 => cos x = -1/2 or cos x = 1
                q = f"Solve for $x \\in [0^\\circ; 180^\\circ]$: $2\\cos^2(x) - \\cos(x) - 1 = 0$."
                correct = "0^\\circ, 120^\\circ"
                wrongs = ["60^\\circ, 180^\\circ", "30^\\circ, 150^\\circ", "90^\\circ, 180^\\circ", "0^\\circ, 60^\\circ", "120^\\circ, 180^\\circ", "45^\\circ, 135^\\circ", "0^\\circ, 90^\\circ"]
                exp = f"Let $k = \\cos(x)$. $2k^2 - k - 1 = 0 \\implies (2k + 1)(k - 1) = 0$. So $\\cos(x) = -1/2$ or $\\cos(x) = 1$. In $[0^\\circ; 180^\\circ]$, $x = 120^\\circ$ or $x = 0^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "sine rule":
            if difficulty == "easy":
                # Find side
                a = random.randint(5, 20)
                A = random.randint(30, 80)
                B = random.randint(30, 80)
                # a/sinA = b/sinB -> b = a * sinB / sinA
                b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))
                b_round = round(b, 1)
                q = f"In $\\Delta ABC$, $a = {a}$, $\\angle A = {A}^\\circ$, and $\\angle B = {B}^\\circ$. Find the length of side $b$ (to 1 decimal place)."
                correct = f"{b_round:.1f}"
                wrongs = get_wrong_floats(b_round, decimals=1)
                exp = f"$\\frac{{b}}{{\\sin B}} = \\frac{{a}}{{\\sin A}} \\implies b = \\frac{{{a} \\cdot \\sin {B}^\\circ}}{{\\sin {A}^\\circ}} \\approx {b_round:.1f}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Find angle
                a = random.randint(10, 20)
                b = random.randint(5, 15)
                A = random.randint(60, 100) # Ensure a valid triangle without ambiguous case if possible
                if b > a: a, b = b, a # make a > b, so angle A > angle B, no ambiguity
                sinB = b * math.sin(math.radians(A)) / a
                B = math.degrees(math.asin(sinB))
                B_round = round(B, 1)
                q = f"In $\\Delta ABC$, $a = {a}$, $b = {b}$, and $\\angle A = {A}^\\circ$. Find the size of acute $\\angle B$ (to 1 decimal place)."
                correct = f"{B_round:.1f}^\\circ"
                wrongs = [f"{w}^\\circ" for w in get_wrong_floats(B_round, decimals=1)]
                exp = f"$\\frac{{\\sin B}}{{b}} = \\frac{{\\sin A}}{{a}} \\implies \\sin B = \\frac{{{b} \\cdot \\sin {A}^\\circ}}{{{a}}} \\approx {sinB:.4f} \\implies B \\approx {B_round:.1f}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # Area rule
                a = random.randint(5, 15)
                b = random.randint(5, 15)
                C = random.randint(30, 150)
                area = 0.5 * a * b * math.sin(math.radians(C))
                area_round = round(area, 2)
                q = f"In $\\Delta ABC$, $a = {a}$, $b = {b}$, and $\\angle C = {C}^\\circ$. Calculate the area of the triangle (to 2 decimal places)."
                correct = f"{area_round:.2f}"
                wrongs = get_wrong_floats(area_round, decimals=2)
                exp = f"$\\text{{Area}} = \\frac{{1}}{{2}}ab\\sin C = 0.5({a})({b})\\sin({C}^\\circ) \\approx {area_round:.2f}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "cosine rule":
            if difficulty == "easy":
                # Find side c
                a = random.randint(5, 15)
                b = random.randint(5, 15)
                C = random.randint(40, 120)
                c_sq = a**2 + b**2 - 2*a*b*math.cos(math.radians(C))
                c = math.sqrt(c_sq)
                c_round = round(c, 1)
                q = f"In $\\Delta ABC$, $a = {a}$, $b = {b}$, and $\\angle C = {C}^\\circ$. Find the length of side $c$ (to 1 decimal place)."
                correct = f"{c_round:.1f}"
                wrongs = get_wrong_floats(c_round, decimals=1)
                exp = f"$c^2 = a^2 + b^2 - 2ab\\cos C = {a}^2 + {b}^2 - 2({a})({b})\\cos {C}^\\circ \\approx {c_sq:.2f} \\implies c \\approx {c_round:.1f}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Find angle
                a = random.randint(5, 15)
                b = random.randint(5, 15)
                c = random.randint(abs(a-b)+2, a+b-2) # Ensure valid triangle
                cosC = (a**2 + b**2 - c**2) / (2 * a * b)
                C = math.degrees(math.acos(cosC))
                C_round = round(C, 1)
                q = f"In $\\Delta ABC$, $a = {a}$, $b = {b}$, and $c = {c}$. Find the size of $\\angle C$ (to 1 decimal place)."
                correct = f"{C_round:.1f}^\\circ"
                wrongs = [f"{w}^\\circ" for w in get_wrong_floats(C_round, decimals=1)]
                exp = f"$\\cos C = \\frac{{a^2 + b^2 - c^2}}{{2ab}} = \\frac{{{a}^2 + {b}^2 - {c}^2}}{{2({a})({b})}} = {cosC:.4f} \\implies C \\approx {C_round:.1f}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # Combine rules
                a = random.randint(8, 20)
                B = random.randint(30, 60)
                C = random.randint(30, 80)
                A = 180 - B - C
                # Given a, B, C. Find c using sine rule, then area using 1/2 ac sinB. Or just find area using 1/2 a c sinB.
                # Just find c first to make it a multi-step.
                c = a * math.sin(math.radians(C)) / math.sin(math.radians(A))
                area = 0.5 * a * c * math.sin(math.radians(B))
                area_round = round(area, 1)
                q = f"In $\\Delta ABC$, $a = {a}$, $\\angle B = {B}^\\circ$, and $\\angle C = {C}^\\circ$. Calculate the area of the triangle (to 1 decimal place)."
                correct = f"{area_round:.1f}"
                wrongs = get_wrong_floats(area_round, decimals=1)
                exp = f"$\\angle A = 180^\\circ - ({B}^\\circ + {C}^\\circ) = {A}^\\circ$. By Sine Rule, $c = \\frac{{{a}\\sin {C}^\\circ}}{{\\sin {A}^\\circ}} \\approx {c:.2f}$. Area = $\\frac{{1}}{{2}}ac\\sin B \\approx {area_round:.1f}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

    return gen

if __name__ == "__main__":
    gen = generate_trigonometry()
    gen.save_to_json("paper2_trigonometry.json")
    print(f"Generated {len(gen.questions)} trigonometry questions.")
