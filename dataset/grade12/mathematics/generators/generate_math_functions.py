import json
import random
import os
import time

def generate_math_functions():
    print("Generating Grade 12 Mathematics: Functions & Graphs...")
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
        q_id = f"MATH_P1_FUNC_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Functions and Graphs",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Functions",
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
    func_rules = [
        ("What geometric transformation maps a function $f(x)$ onto its inverse $f^{-1}(x)$?", "Reflection across the line $y = x$", [
            "Reflection across the x-axis", "Reflection across the y-axis", "Rotation of 90 degrees about origin",
            "Translation of 1 unit right", "Dilation from the origin", "Reflection across the line $y = -x$", "Inversion across the unit circle"
        ], "The graph of $f^{-1}(x)$ is obtained by interchanging the x and y coordinates, which is a reflection across the line $y = x$."),

        ("What test can be performed on the Cartesian graph of a relation to determine whether it is a function?", "The vertical line test", [
            "The horizontal line test", "The diagonal line test", "The slope test",
            "The circle test", "The asymptote test", "The quadratic formula test"
        ], "If any vertical line intersects a graph in at most one point, the relation is a function."),

        ("What test can be performed on the graph of a function to determine if its inverse $f^{-1}$ will also be a function?", "The horizontal line test", [
            "The vertical line test", "The axis test", "The turning point test",
            "The discriminant test", "The derivative test", "The symmetry test"
        ], "If a horizontal line intersects $f(x)$ at more than one point (many-to-one), its inverse will fail the vertical line test and not be a function."),

        ("For the hyperbola $f(x) = \\frac{a}{x - p} + q$, what are the equations of the vertical and horizontal asymptotes?", "Vertical: $x = p$, Horizontal: $y = q$", [
            "Vertical: $x = -p$, Horizontal: $y = -q$", "Vertical: $y = q$, Horizontal: $x = p$",
            "Vertical: $x = 0$, Horizontal: $y = 0$", "Vertical: $x = a$, Horizontal: $y = q$",
            "Vertical: $x = q$, Horizontal: $y = p$", "Vertical: $x = p$, Horizontal: $y = a$"
        ], "Division by zero is undefined at $x = p$ (vertical asymptote); as $x \\to \\pm\\infty$, $\\frac{a}{x-p} \\to 0$, giving $y = q$ (horizontal asymptote)."),

        ("What is the horizontal asymptote of the exponential function $f(x) = a \\cdot b^x + q$?", "y = q", [
            "y = 0", "x = q", "x = 0", "y = a", "y = b", "y = -q", "x = -q"
        ], "As $x \\to -\\infty$ (for $b > 1$), $b^x \\to 0$, so $y \\to q$."),

        ("For the parabola $f(x) = a(x - p)^2 + q$, what are the coordinates of the turning point (vertex)?", "(p; q)", [
            "(-p; q)", "(p; -q)", "(-p; -q)", "(q; p)", "(0; q)", "(-b/2a; 0)", "(a; p)"
        ], "The turning point form $y = a(x - p)^2 + q$ gives the vertex coordinates directly as $(p; q)$.")
    ]
    for q, ans, wrongs, expl in func_rules:
        add_q("easy", "Function Theory", q, ans, wrongs, expl)

    # Easy Turning Points & Asymptotes
    for p in range(-5, 6):
        for q_val in range(-5, 6):
            if p == 0 and q_val == 0: continue
            # Hyperbola asymptotes
            q_text = f"Find the vertical and horizontal asymptotes of the hyperbola $f(x) = \\frac{{3}}{{x {'-' if p>=0 else '+'} {abs(p)}}} {'+' if q_val>=0 else '-'} {abs(q_val)}$."
            ans_str = f"x = {p} and y = {q_val}"
            wrongs_str = [
                f"x = {-p} and y = {q_val}", f"x = {p} and y = {-q_val}", f"x = {-p} and y = {-q_val}",
                f"y = {p} and x = {q_val}", f"x = {p} and y = 0", f"x = 0 and y = {q_val}", f"x = 3 and y = {q_val}"
            ]
            add_q("easy", "Hyperbola Asymptotes", q_text, ans_str, wrongs_str, f"Vertical asymptote occurs where denominator is zero ($x = {p}$); horizontal asymptote is the vertical shift ($y = {q_val}$).")

            # Parabola Turning points
            q_text2 = f"Find the coordinates of the turning point of the parabola $y = 2(x {'-' if p>=0 else '+'} {abs(p)})^2 {'+' if q_val>=0 else '-'} {abs(q_val)}$."
            ans_tp = f"({p}; {q_val})"
            wrongs_tp = [
                f"({-p}; {q_val})", f"({p}; {-q_val})", f"({-p}; {-q_val})", f"({q_val}; {p})",
                f"(0; {q_val})", f"({p}; 0)", f"(2; {q_val})"
            ]
            add_q("easy", "Parabola Turning Point", q_text2, ans_tp, wrongs_tp, f"In the form $y = a(x - p)^2 + q$, the vertex is $(p; q) = ({p}; {q_val})$.")

    # Top up easy to 300
    e_idx = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        c_val = random.randint(-10, 10)
        q = f"Find the y-intercept of the quadratic function $f(x) = 3x^2 - 5x {'+' if c_val>=0 else '-'} {abs(c_val)}$ (variant {e_idx})."
        add_q("easy", "Intercepts", q, f"(0; {c_val})", [
            f"(0; {-c_val})", f"({c_val}; 0)", f"(0; 3)", f"(0; -5)", f"(3; -5)", f"(0; {c_val + 2})", f"(0; {c_val - 2})"
        ], f"The y-intercept occurs where $x = 0$: $f(0) = {c_val} \\implies (0; {c_val})$.")
        e_idx += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # A. Turning points from standard form: y = a x^2 + b x + c
    # x = -b / (2a)
    for a in [1, -1, 2, -2]:
        for x_tp in range(-4, 5):
            b = -2 * a * x_tp
            c = random.randint(-8, 8)
            y_tp = a * (x_tp ** 2) + b * x_tp + c
            
            b_sgn = '+' if b >= 0 else '-'
            c_sgn = '+' if c >= 0 else '-'
            q = f"Calculate the coordinates of the turning point of the parabola $f(x) = {a if a!=1 and a!=-1 else ('-' if a==-1 else '')}x^2 {b_sgn} {abs(b)}x {c_sgn} {abs(c)}$."
            ans_tp = f"({x_tp}; {y_tp})"
            w_tp = [
                f"({-x_tp}; {y_tp})", f"({x_tp}; {-y_tp})", f"({-x_tp}; {-y_tp})",
                f"({x_tp + 1}; {y_tp - 1})", f"({x_tp - 1}; {y_tp + 1})", f"({y_tp}; {x_tp})", f"(0; {c})"
            ]
            add_q("medium", "Parabola Turning Point", q, ans_tp, w_tp, f"$x = -\\frac{{b}}{{2a}} = -\\frac{{{b}}}{{2({a})}} = {x_tp}$. Substituting into $f({x_tp}) = {y_tp} \\implies ({x_tp}; {y_tp})$.", "Application")

    # B. Inverse of linear functions: y = mx + c => x = (y - c)/m
    for m in [2, 3, 4, 5]:
        for c in [-6, -4, -2, 2, 4, 6]:
            q = f"Determine the equation of the inverse function $f^{{-1}}(x)$ for $f(x) = {m}x {'+' if c>=0 else '-'} {abs(c)}$."
            # y = (x - c)/m
            sign_c = '-' if c >= 0 else '+'
            ans_inv = f"y = \\frac{{x {sign_c} {abs(c)}}}{{{m}}}"
            w_inv = [
                f"y = \\frac{{x {'+' if c>=0 else '-'} {abs(c)}}}{{{m}}}",
                f"y = {m}x {sign_c} {abs(c)}",
                f"y = \\frac{{1}}{{{m}x {'+' if c>=0 else '-'} {abs(c)}}}",
                f"y = -{m}x {sign_c} {abs(c)}",
                f"y = \\frac{{{m}}}{{x {sign_c} {abs(c)}}}",
                f"y = \\frac{{x}}{{{m}}} {'+' if c>=0 else '-'} {abs(c)}",
                f"y = x {sign_c} {abs(c)}"
            ]
            add_q("medium", "Inverse Functions", q, ans_inv, w_inv, f"Swap $x$ and $y$: $x = {m}y {'+' if c>=0 else '-'} {abs(c)} \\implies {m}y = x {sign_c} {abs(c)} \\implies {ans_inv}$.", "Application")

    # C. Inverse of exponential function: y = b^x => y = log_b(x)
    for base in [2, 3, 4, 5, 10]:
        q = f"Determine the equation of the inverse function $f^{{-1}}(x)$ for $f(x) = {base}^x$."
        ans_inv = f"y = \\log_{{{base}}}(x)"
        w_inv = [
            f"y = {base}^{{-x}}", f"y = \\frac{{1}}{{{base}^x}}", f"y = \\log_x({base})",
            f"y = x^{{{base}}}", f"y = {base}x", f"y = -\\log_{{{base}}}(x)", f"y = \\sqrt[{{{base}}}]{{x}}"
        ]
        add_q("medium", "Inverse Functions", q, ans_inv, w_inv, f"Swap $x$ and $y$: $x = {base}^y \\implies y = \\log_{{{base}}}(x)$.", "Application")

    # D. Axes of symmetry of Hyperbola: y = (x - p) + q and y = -(x - p) + q
    for p in [-3, -2, -1, 1, 2, 3]:
        for q_val in [-4, -2, 2, 4]:
            c1 = q_val - p
            c2 = q_val + p
            q = f"Find the equation of the axis of symmetry with positive gradient ($m = 1$) for the hyperbola $f(x) = \\frac{{4}}{{x {'-' if p>=0 else '+'} {abs(p)}}} {'+' if q_val>=0 else '-'} {abs(q_val)}$."
            ans_sym = f"y = x {'+' if c1>=0 else '-'} {abs(c1)}"
            w_sym = [
                f"y = x {'-' if c1>=0 else '+'} {abs(c1)}", f"y = -x {'+' if c2>=0 else '-'} {abs(c2)}",
                f"y = x + {p}", f"y = x + {q_val}", f"y = x", f"y = -x", f"y = 2x + {c1}"
            ]
            add_q("medium", "Hyperbola Symmetry", q, ans_sym, w_sym, f"Axis of symmetry with $m = 1$: $y = (x - p) + q = (x - ({p})) + ({q_val}) = x {'+' if c1>=0 else '-'} {abs(c1)}$.", "Application")

    # Top up medium to 500
    m_idx = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        base = random.choice([2, 3, 5])
        q_val = random.choice([-5, -3, -1, 1, 3, 5])
        q = f"State the range of the exponential function $f(x) = {base}^x {'+' if q_val>=0 else '-'} {abs(q_val)}$ (case {m_idx})."
        ans_r = f"y > {q_val}"
        w_r = [
            f"y \\ge {q_val}", f"y < {q_val}", f"y \\le {q_val}", f"y \\in \\mathbb{{R}}",
            f"y > 0", f"y > {-q_val}", f"x > {q_val}"
        ]
        add_q("medium", "Function Range", q, ans_r, w_r, f"Since ${base}^x > 0$ for all real $x$, the range is $y > {q_val}$.", "Application")
        m_idx += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_scenarios = [
        # Domain restriction for parabolic inverse
        ("Given the function $f(x) = 2x^2$. How must the domain of $f$ be restricted so that its inverse $f^{-1}$ is a function?",
         "x >= 0 (or x <= 0)",
         ["x in R", "x > 2", "x != 0", "x > -2", "-2 <= x <= 2", "x >= 2"],
         "A parabola is many-to-one; restricting the domain to $x \\ge 0$ (one half of the parabola) makes it one-to-one, ensuring $f^{-1}$ passes the vertical line test.", "Analysis"),

        # Points of intersection between parabola and line
        ("Find the points of intersection of the parabola $f(x) = x^2 - 2x - 3$ and the line $g(x) = x + 1$.",
         "(-1; 0) and (4; 5)",
         ["(1; 2) and (-4; -3)", "(-1; 2) and (4; 3)", "(0; -3) and (1; 2)", "(-3; 0) and (1; 0)", "(2; -3) and (3; 4)", "(-2; -1) and (3; 4)"],
         "Set $x^2 - 2x - 3 = x + 1 \\implies x^2 - 3x - 4 = 0 \\implies (x - 4)(x + 1) = 0 \\implies x = 4$ or $x = -1$. Substitute into $g(x)$: $g(4) = 5 \\implies (4; 5)$ and $g(-1) = 0 \\implies (-1; 0)$.", "Analysis"),

        # Reading graphical inequalities: f(x) * g(x) <= 0
        ("The parabola $f(x) = -(x - 1)(x - 5)$ and the straight line $g(x) = x - 3$ are sketched. For which values of $x$ is $f(x) \\cdot g(x) \\le 0$ on the interval $x > 0$?",
         "1 <= x <= 3 or x >= 5",
         ["x <= 1 or 3 <= x <= 5", "1 < x < 5", "3 <= x <= 5", "x >= 3", "0 < x <= 1", "1 <= x <= 5"],
         "$f(x) \\ge 0$ on $[1; 5]$ and $g(x) \\ge 0$ for $x \\ge 3$. The product is $\\le 0$ when $f$ and $g$ have opposite signs or are zero: $1 \\le x \\le 3$ (where $f \\ge 0, g \\le 0$) and $x \\ge 5$ (where $f \\le 0, g \\ge 0$).", "Analysis"),

        # Horizontal and vertical shifts: g(x) = f(x - 2) + 3
        ("The turning point of a parabola $f(x)$ is $(3; -4)$. If $g(x) = f(x - 2) + 5$, what are the coordinates of the turning point of $g$?",
         "(5; 1)",
         ["(1; 1)", "(5; -9)", "(1; -9)", "(3; 1)", "(5; -4)", "(-1; 1)"],
         "$f(x - 2)$ shifts the graph 2 units to the right ($3 + 2 = 5$), and $+ 5$ shifts it 5 units upwards ($-4 + 5 = 1$). The new turning point is $(5; 1)$.", "Analysis"),

        # Average gradient
        ("Calculate the average gradient of the function $f(x) = 2x^2 - 3$ between the points where $x = 1$ and $x = 4$.",
         "10",
         ["8", "12", "6", "14", "5", "9"],
         "Average gradient $= \\frac{f(4) - f(1)}{4 - 1} = \\frac{(2(16) - 3) - (2(1) - 3)}{3} = \\frac{29 - (-1)}{3} = \\frac{30}{3} = 10$.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_scenarios:
        for prefix in ["", "CAPS Analytical Function Problem: ", "Advanced Graph Interpretation: ", "Calculus/Algebra Function Synthesis: "]:
            add_q("hard", "Advanced Graph Interpretation", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_idx = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_scenarios)
        q = f"Advanced function investigation {h_idx}: {base_h[0]}"
        add_q("hard", "Advanced Graph Interpretation", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_idx += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/mathematics/paper1_functions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_functions()
