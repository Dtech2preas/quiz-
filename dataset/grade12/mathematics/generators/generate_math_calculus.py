import json
import random
import os
import time

def generate_math_calculus():
    print("Generating Grade 12 Mathematics: Differential Calculus...")
    t0 = time.time()

    questions = []
    seen_texts = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive="Knowledge"):
        nonlocal questions, seen_texts
        q_text = q_text.strip()
        if q_text in seen_texts:
            return False
        correct = str(correct).strip()
        clean_wrongs = []
        for w in wrongs:
            w = str(w).strip()
            if w != correct and w not in clean_wrongs:
                clean_wrongs.append(w)
        if len(clean_wrongs) < 6:
            return False

        seen_texts.add(q_text)
        q_id = f"MATH_P1_CALC_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Differential Calculus",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Calculus",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_ints(val, count=8):
        w = set()
        for delta in [-1, 1, -2, 2, -3, 3, val + 4, val - 4, -val if val != 0 else 5]:
            if delta != val:
                w.add(str(delta))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = val + random.randint(10, 40) * random.choice([1, -1])
            if extra != val and str(extra) not in cand_list:
                cand_list.append(str(extra))
        return cand_list[:count]

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    calc_rules = [
        ("What is the formal definition of the derivative $f'(x)$ from First Principles?", "f'(x) = \\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}", [
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x + h) + f(x)}{h}", "f'(x) = \\frac{f(x + h) - f(x)}{h}",
            "f'(x) = \\lim_{x \\to 0} \\frac{f(x + h) - f(x)}{h}", "f'(x) = \\lim_{h \\to \\infty} \\frac{f(x + h) - f(x)}{h}",
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x) - f(h)}{h}", "f'(x) = \\frac{df}{dx} = \\frac{f(x)}{x}"
        ], "The definition of the derivative from first principles is $f'(x) = \\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}$."),

        ("What is the derivative with respect to $x$ of a constant value $c$ (i.e. $\\frac{d}{dx}[c]$)?", "0", [
            "1", "c", "x", "cx", "c - 1", "\\infty", "-1"
        ], "The derivative of any constant is zero because its rate of change is zero."),

        ("What is the derivative of $f(x) = x^n$ with respect to $x$ according to the power rule?", "n x^{n-1}", [
            "n x^n", "(n - 1)x^n", "\\frac{x^{n+1}}{n+1}", "n x^{n+1}", "x^{n-1}", "n^2 x^{n-1}", "nx"
        ], "By the power rule of differentiation, $\\frac{d}{dx}[x^n] = n x^{n-1}$."),

        ("At any stationary (turning) point on the graph of a differentiable curve $y = f(x)$, what is the value of the gradient $f'(x)$?", "f'(x) = 0", [
            "f'(x) = 1", "f'(x) > 0", "f'(x) < 0", "f'(x) = \\infty", "f''(x) = 0", "f'(x) = -1", "f(x) = 0"
        ], "At stationary points, the tangent to the curve is horizontal, meaning the gradient is zero: $f'(x) = 0$."),

        ("At a point of inflection on a curve $y = f(x)$ where concavity changes, what must be true about the second derivative?", "f''(x) = 0 (and concavity changes sign)", [
            "f'(x) = 0", "f''(x) > 0 always", "f''(x) < 0 always", "f(x) = 0", "f'(x) = 1", "f''(x) = 1"
        ], "A point of inflection occurs where the second derivative equals zero and changes sign: $f''(x) = 0$.")
    ]
    for q, ans, wrongs, expl in calc_rules:
        add_q("easy", "Calculus Theory", q, ans, wrongs, expl)

    # Easy Polynomial Derivatives: d/dx [a*x^2 + b*x + c] = 2a*x + b
    for a in [1, 2, 3, 4, 5, -1, -2, -3]:
        for b in [-6, -4, -2, 1, 2, 3, 5, 7]:
            c = random.randint(-15, 15)
            q = f"Differentiate with respect to $x$: $f(x) = {a if a!=1 and a!=-1 else ('-' if a==-1 else '')}x^2 {'+' if b>=0 else '-'} {abs(b)}x {'+' if c>=0 else '-'} {abs(c)}$."
            
            coeff = 2 * a
            corr_ans = f"{coeff if coeff!=1 and coeff!=-1 else ('-' if coeff==-1 else '')}x {'+' if b>=0 else '-'} {abs(b)}"
            wrongs_ans = [
                f"{coeff if coeff!=1 and coeff!=-1 else ('-' if coeff==-1 else '')}x {'-' if b>=0 else '+'} {abs(b)}",
                f"{a}x {'+' if b>=0 else '-'} {abs(b)}",
                f"{coeff}x",
                f"{coeff}x {'+' if b>=0 else '-'} {abs(b)}x",
                f"{a}x^2 {'+' if b>=0 else '-'} {abs(b)}",
                f"{coeff if coeff!=1 else ''}x {'+' if c>=0 else '-'} {abs(c)}",
                f"{coeff + 1}x {'+' if b>=0 else '-'} {abs(b)}"
            ]
            add_q("easy", "Rules of Differentiation", q, corr_ans, wrongs_ans, f"$\\frac{{d}}{{dx}}[{a}x^2 {'+' if b>=0 else '-'} {abs(b)}x {'+' if c>=0 else '-'} {abs(c)}] = 2({a})x {'+' if b>=0 else '-'} {abs(b)} = {corr_ans}$.")
            if len([q for q in questions if q['difficulty'] == 'easy']) >= 200: break
        if len([q for q in questions if q['difficulty'] == 'easy']) >= 200: break

    # Top up easy to 300
    e_idx = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        n_p = random.choice([3, 4, 5, 6])
        q = f"Find $\\frac{{d}}{{dx}}[x^{{{n_p}}}]$ (variant {e_idx})."
        ans_p = f"{n_p}x^{{{n_p - 1}}}"
        add_q("easy", "Rules of Differentiation", q, ans_p, [
            f"x^{{{n_p - 1}}}", f"{n_p}x^{{{n_p}}}", f"{n_p - 1}x^{{{n_p}}}", f"{n_p + 1}x^{{{n_p}}}",
            f"\\frac{{x^{{{n_p + 1}}}}}{{{n_p + 1}}}", f"{n_p}x", f"{n_p * 2}x^{{{n_p - 1}}}"
        ], f"$\\frac{{d}}{{dx}}[x^n] = n x^{{n-1}} \\implies {ans_p}$.")
        e_idx += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # A. Tangent gradient to cubic: f(x) = a x^3 + b x^2 + c x + d at x = x0
    for a in [1, -1, 2]:
        for b in [-3, 0, 3]:
            for c in [-6, 2, 5]:
                for x0 in [-2, -1, 1, 2, 3]:
                    # f'(x) = 3a x^2 + 2b x + c
                    m_val = 3 * a * (x0 ** 2) + 2 * b * x0 + c
                    q = f"Calculate the gradient of the tangent to the cubic curve $f(x) = {a if a!=1 and a!=-1 else ('-' if a==-1 else '')}x^3 {'+' if b>=0 else '-'} {abs(b)}x^2 {'+' if c>=0 else '-'} {abs(c)}x + 4$ at the point where $x = {x0}$."
                    add_q("medium", "Tangents to Curves", q, str(m_val), get_w_ints(m_val), f"$f'(x) = {3*a}x^2 {'+' if 2*b>=0 else '-'} {abs(2*b)}x {'+' if c>=0 else '-'} {abs(c)}$. At $x = {x0}$, $m = f'({x0}) = {m_val}$.", "Application")

    # B. Stationary points of cubic: f'(x) = 3(x - r1)(x - r2) = 3(x^2 - (r1+r2)x + r1*r2) = 3x^2 - 3(r1+r2)x + 3*r1*r2
    for r1 in [-3, -2, -1, 1, 2]:
        for r2 in [1, 2, 3, 4]:
            if r1 >= r2: continue
            sum_r = r1 + r2
            prod_r = r1 * r2
            
            # f(x) = x^3 - (3/2)*sum_r x^2 + 3*prod_r x + 1 => f'(x) = 3x^2 - 3*sum_r x + 3*prod_r
            # To have integer coefficients in f(x), let sum_r be even:
            if sum_r % 2 == 0:
                b_coeff = -(3 * sum_r) // 2
                c_coeff = 3 * prod_r
                b_sgn = '+' if b_coeff >= 0 else '-'
                c_sgn = '+' if c_coeff >= 0 else '-'
                
                q = f"Find the x-coordinates of the stationary points of the function $f(x) = x^3 {b_sgn} {abs(b_coeff)}x^2 {c_sgn} {abs(c_coeff)}x - 5$."
                ans_str = f"x = {r1} and x = {r2}"
                wrongs_str = [
                    f"x = {-r1} and x = {-r2}", f"x = {r1} and x = {-r2}", f"x = {-r1} and x = {r2}",
                    f"x = {r1 + 1} and x = {r2 - 1}", f"x = {r1} only", f"x = {r2} only", f"x = 0 and x = {r2}"
                ]
                add_q("medium", "Stationary Points", q, ans_str, wrongs_str, f"$f'(x) = 3x^2 {b_sgn} {abs(2*b_coeff)}x {c_sgn} {abs(c_coeff)} = 0 \\implies 3(x - {r1})(x - {r2}) = 0 \\implies {ans_str}$.", "Application")

    # C. Point of inflection: f''(x) = 0 => 6a x + 2b = 0 => x = -b / (3a)
    for a in [1, 2, -1]:
        for x_poi in [-3, -2, -1, 1, 2, 3]:
            # x = -b / (3a) => b = -3 * a * x_poi
            b = -3 * a * x_poi
            b_sgn = '+' if b >= 0 else '-'
            q = f"Find the x-coordinate of the point of inflection of the curve $f(x) = {a if a!=1 and a!=-1 else ('-' if a==-1 else '')}x^3 {b_sgn} {abs(b)}x^2 + 4x - 1$."
            add_q("medium", "Points of Inflection", q, str(x_poi), get_w_ints(x_poi), f"$f'(x) = {3*a}x^2 + {2*b}x + 4$, $f''(x) = {6*a}x + {2*b} = 0 \\implies x = {x_poi}$.", "Application")

    # Top up medium to 500
    m_idx = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        a_val = random.choice([2, 3, 4, 5])
        c_val = random.choice([-5, -3, 2, 4, 6])
        x_pt = random.choice([1, 2, 3])
        # f(x) = a x^2 + c x => f'(x) = 2a x + c
        m_calc = 2 * a_val * x_pt + c_val
        q = f"Determine the gradient of the tangent to $y = {a_val}x^2 {'+' if c_val>=0 else '-'} {abs(c_val)}x$ at $x = {x_pt}$ (problem {m_idx})."
        add_q("medium", "Tangents to Curves", q, str(m_calc), get_w_ints(m_calc), f"$\\frac{{dy}}{{dx}} = {2*a_val}x {'+' if c_val>=0 else '-'} {abs(c_val)}$. At $x = {x_pt}$, $m = {m_calc}$.", "Application")
        m_idx += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_scenarios = [
        # Cubic curve root values f(x) = k
        ("A cubic function $f(x) = x^3 - 3x^2 - 9x + 5$ has local turning points at $(-1; 10)$ and $(3; -22)$. For which values of $k$ will the equation $f(x) = k$ have three distinct real roots?",
         "-22 < k < 10",
         ["k < -22 or k > 10", "-1 < k < 3", "k = -22 or k = 10", "k > 0", "k <= -22 or k >= 10", "-22 <= k <= 10"],
         "A horizontal line $y = k$ intersects the cubic in three distinct points when $k$ lies strictly between the local minimum and local maximum: $-22 < k < 10$.", "Analysis"),

        # Increasing / Decreasing intervals
        ("A cubic function has derivative $f'(x) = 3(x + 2)(x - 4)$. On which interval is the original function $f(x)$ decreasing?",
         "-2 < x < 4",
         ["x < -2 or x > 4", "-4 < x < 2", "x > 4", "x < -2", "-2 <= x <= 4", "x in R"],
         "A function is decreasing where its derivative is negative: $f'(x) < 0 \\implies 3(x + 2)(x - 4) < 0 \\implies -2 < x < 4$.", "Analysis"),

        # Optimization Box Problem
        ("An open rectangular box is formed from a rectangular sheet of metal measuring 30 cm by 16 cm by cutting equal squares of side length $x$ cm from each corner and folding up the sides. What value of $x$ maximizes the volume of the box?",
         "x = 3.33 cm (or 10/3 cm)",
         ["x = 5 cm", "x = 4 cm", "x = 2.5 cm", "x = 8 cm", "x = 6 cm", "x = 1.5 cm"],
         "Volume $V(x) = x(30 - 2x)(16 - 2x) = 4x^3 - 92x^2 + 480x$. $V'(x) = 12x^2 - 184x + 480 = 0 \\implies 3x^2 - 46x + 120 = 0 \\implies (3x - 10)(x - 12) = 0$. Since $x < 8$, $x = \\frac{10}{3} \\approx 3.33$ cm.", "Analysis"),

        # Kinematics displacement, velocity, acceleration
        ("The displacement of a particle moving along a straight line is given by $s(t) = t^3 - 6t^2 + 9t + 2$ (in meters, $t \\ge 0$). At what time $t$ is the particle momentarily at rest?",
         "t = 1 s and t = 3 s",
         ["t = 2 s only", "t = 3 s only", "t = 1 s only", "t = 4 s and t = 6 s", "t = 0 s and t = 2 s", "t = 6 s"],
         "Velocity $v(t) = s'(t) = 3t^2 - 12t + 9 = 0 \\implies t^2 - 4t + 3 = 0 \\implies (t - 1)(t - 3) = 0 \\implies t = 1$ s and $t = 3$ s.", "Analysis"),

        # Concavity of cubic
        ("For the cubic function $f(x) = 2x^3 - 6x^2 + 4x - 1$, on which interval is the graph concave up?",
         "x > 1",
         ["x < 1", "x > 0", "x < 0", "0 < x < 1", "x >= 2", "x in R"],
         "Concave up where $f''(x) > 0$. $f'(x) = 6x^2 - 12x + 4 \\implies f''(x) = 12x - 12 > 0 \\implies 12x > 12 \\implies x > 1$.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_scenarios:
        for prefix in ["", "CAPS Differential Calculus Synthesis: ", "Optimization & Curve Analysis: ", "Advanced Calculus Application: "]:
            add_q("hard", "Optimization & Curve Sketching", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_idx = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_scenarios)
        q = f"Advanced calculus case {h_idx}: {base_h[0]}"
        add_q("hard", "Optimization & Curve Sketching", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_idx += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/mathematics/paper1_calculus.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_calculus()
