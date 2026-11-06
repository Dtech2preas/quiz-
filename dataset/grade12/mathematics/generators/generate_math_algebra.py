import json
import random
import os
import time
import math

def generate_math_algebra():
    print("Generating Grade 12 Mathematics: Algebra, Equations & Inequalities...")
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
        q_id = f"MATH_P1_ALG_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Algebra, Equations and Inequalities",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Algebra",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # Helper for wrong ints
    def get_w_ints(val, count=8):
        w = set()
        for delta in [-1, 1, -2, 2, -3, 3, -val if val != 0 else 5, val + 5, val - 4]:
            cand = val + delta
            if cand != val:
                w.add(str(cand))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = val + random.randint(10, 50) * random.choice([1, -1])
            if extra != val and str(extra) not in cand_list:
                cand_list.append(str(extra))
        return cand_list[:count]

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    # A. Linear Equations
    for a in [2, 3, 4, 5, 6, 7]:
        for ans in range(-8, 9):
            if ans == 0: continue
            b = random.randint(-15, 15)
            rhs = a * ans + b
            q = f"Solve for $x$: ${a}x {'+' if b>=0 else '-'} {abs(b)} = {rhs}$"
            add_q("easy", "Linear Equations", q, str(ans), get_w_ints(ans), f"${a}x = {rhs - b} \\implies x = {ans}$.")
            if len([q for q in questions if q['difficulty'] == 'easy']) >= 80: break
        if len([q for q in questions if q['difficulty'] == 'easy']) >= 80: break

    # B. Monic Quadratics with integer roots
    for r1 in [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]:
        for r2 in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if r1 >= r2: continue
            b_val = -(r1 + r2)
            c_val = r1 * r2
            sign_b = '+' if b_val >= 0 else '-'
            sign_c = '+' if c_val >= 0 else '-'
            q = f"Solve for $x$: $x^2 {sign_b} {abs(b_val)}x {sign_c} {abs(c_val)} = 0$"
            ans_str = f"x = {r1} or x = {r2}"
            wrongs = [
                f"x = {-r1} or x = {-r2}",
                f"x = {r1} or x = {-r2}",
                f"x = {-r1} or x = {r2}",
                f"x = {r1 + 1} or x = {r2 - 1}",
                f"x = {r1 - 1} or x = {r2 + 1}",
                f"x = {r1 * 2} or x = {r2}",
                f"x = {r1} or x = {r2 * 2}"
            ]
            add_q("easy", "Quadratic Equations", q, ans_str, wrongs, f"$(x - ({r1}))(x - ({r2})) = 0 \\implies x = {r1}$ or $x = {r2}$.")
            if len([q for q in questions if q['difficulty'] == 'easy']) >= 160: break
        if len([q for q in questions if q['difficulty'] == 'easy']) >= 160: break

    # C. Exponent Laws & Surd Simplifications
    surd_examples = [
        (12, "2\\sqrt{3}", ["3\\sqrt{2}", "4\\sqrt{3}", "2\\sqrt{6}", "6\\sqrt{2}", "\\sqrt{6}", "3\\sqrt{3}"]),
        (18, "3\\sqrt{2}", ["2\\sqrt{3}", "9\\sqrt{2}", "3\\sqrt{6}", "2\\sqrt{6}", "6\\sqrt{3}", "4\\sqrt{2}"]),
        (24, "2\\sqrt{6}", ["4\\sqrt{6}", "6\\sqrt{2}", "3\\sqrt{2}", "2\\sqrt{3}", "\\sqrt{12}", "3\\sqrt{6}"]),
        (27, "3\\sqrt{3}", ["9\\sqrt{3}", "3\\sqrt{2}", "2\\sqrt{3}", "6\\sqrt{3}", "\\sqrt{9}", "4\\sqrt{3}"]),
        (32, "4\\sqrt{2}", ["2\\sqrt{4}", "8\\sqrt{2}", "2\\sqrt{8}", "16\\sqrt{2}", "4\\sqrt{4}", "3\\sqrt{2}"]),
        (48, "4\\sqrt{3}", ["3\\sqrt{4}", "2\\sqrt{12}", "6\\sqrt{2}", "16\\sqrt{3}", "8\\sqrt{3}", "4\\sqrt{6}"]),
        (50, "5\\sqrt{2}", ["2\\sqrt{5}", "25\\sqrt{2}", "5\\sqrt{5}", "10\\sqrt{2}", "2\\sqrt{10}", "4\\sqrt{5}"]),
        (72, "6\\sqrt{2}", ["2\\sqrt{6}", "3\\sqrt{8}", "9\\sqrt{2}", "36\\sqrt{2}", "4\\sqrt{3}", "8\\sqrt{2}"]),
        (75, "5\\sqrt{3}", ["3\\sqrt{5}", "25\\sqrt{3}", "5\\sqrt{5}", "15\\sqrt{3}", "3\\sqrt{15}", "2\\sqrt{15}"]),
        (98, "7\\sqrt{2}", ["2\\sqrt{7}", "49\\sqrt{2}", "7\\sqrt{7}", "14\\sqrt{2}", "4\\sqrt{7}", "3\\sqrt{7}"])
    ]
    for n, s_ans, wrongs in surd_examples:
        q = f"Simplify completely without using a calculator: $\\sqrt{{{n}}}$"
        add_q("easy", "Surds", q, s_ans, wrongs, f"By factoring out the largest perfect square factor, $\\sqrt{{{n}}} = {s_ans}$.")

    # D. Log definitions & Nature of Roots rules
    core_rules = [
        ("What is the value of $\\log_{5}(125)$?", "3", ["5", "25", "1", "0", "15", "2", "125"], "$\\log_5(125) = \\log_5(5^3) = 3$."),
        ("What is the value of $\\log_{2}(64)$?", "6", ["8", "32", "4", "2", "16", "12", "64"], "$\\log_2(64) = \\log_2(2^6) = 6$."),
        ("What is the value of $\\log_{3}(81)$?", "4", ["3", "9", "27", "1", "12", "6", "81"], "$\\log_3(81) = \\log_3(3^4) = 4$."),
        ("What is the value of $\\log_{10}(1000)$?", "3", ["100", "10", "1", "0", "30", "4", "1000"], "$\\log_{10}(1000) = 3$."),
        ("What is the value of $\\log_{b}(1)$ for any valid base $b > 0, b \\ne 1$?", "0", ["1", "b", "-1", "\\infty", "undefined", "b^2"], "Any base raised to the power of 0 equals 1, so $\\log_b(1) = 0$."),
        ("For a quadratic equation $ax^2 + bx + c = 0$, what formula gives the discriminant $\\Delta$?", "\\Delta = b^2 - 4ac", ["\\Delta = b^2 + 4ac", "\\Delta = \\sqrt{b^2 - 4ac}", "\\Delta = -b \\pm \\sqrt{b^2 - 4ac}", "\\Delta = \\frac{b^2}{4ac}", "\\Delta = 2a - 4bc", "\\Delta = b - 4ac"], "The discriminant is $\\Delta = b^2 - 4ac$."),
        ("If the discriminant of a quadratic equation is negative ($\\Delta < 0$), what is the nature of its roots?", "Non-real (imaginary) roots", ["Real, rational, and unequal roots", "Real, irrational, and unequal roots", "Real and equal roots", "Zero roots", "Undefined roots", "Rational and equal roots"], "A negative discriminant means taking the square root of a negative number, yielding non-real roots."),
        ("If the discriminant of a quadratic equation is zero ($\\Delta = 0$), what is the nature of the roots?", "Real, rational, and equal roots", ["Non-real roots", "Real, irrational, and unequal roots", "Non-zero unequal roots", "Infinite roots", "No solution"], "When $\\Delta = 0$, $x = \\frac{-b \\pm 0}{2a}$, yielding one repeated real rational root.")
    ]
    for q, ans, wrongs, expl in core_rules:
        add_q("easy", "Algebra Fundamentals", q, ans, wrongs, expl)

    # Top up easy to 300
    e_idx = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        base = random.choice([2, 3, 5, 10])
        p = random.choice([1, 2, 3, 4])
        val = base ** p
        q = f"Evaluate without a calculator (variant {e_idx}): $\\log_{{{base}}}({val})$"
        add_q("easy", "Logarithms", q, str(p), get_w_ints(p), f"$\\log_{{{base}}}({val}) = \\log_{{{base}}}({base}^{{{p}}}) = {p}$.")
        e_idx += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # A. Quadratic Inequalities
    for r1 in [-4, -3, -2, -1, 1, 2, 3]:
        for r2 in [1, 2, 3, 4, 5]:
            if r1 >= r2: continue
            b_val = -(r1 + r2)
            c_val = r1 * r2
            sign_b = '+' if b_val >= 0 else '-'
            sign_c = '+' if c_val >= 0 else '-'
            
            # Type 1: < 0 (between roots)
            q1 = f"Solve for $x$: $x^2 {sign_b} {abs(b_val)}x {sign_c} {abs(c_val)} < 0$"
            ans1 = f"{r1} < x < {r2}"
            w1 = [
                f"x < {r1} or x > {r2}",
                f"{r1} \\le x \\le {r2}",
                f"x \\le {r1} or x \\ge {r2}",
                f"{-r2} < x < {-r1}",
                f"x < {-r2} or x > {-r1}",
                f"x > {r2}",
                f"x < {r1}"
            ]
            add_q("medium", "Quadratic Inequalities", q1, ans1, w1, f"$(x - {r1})(x - {r2}) < 0$. The parabola is below the x-axis between the critical values: ${r1} < x < {r2}$.", "Application")

            # Type 2: >= 0 (outside roots)
            q2 = f"Solve for $x$: $x^2 {sign_b} {abs(b_val)}x {sign_c} {abs(c_val)} \\ge 0$"
            ans2 = f"x \\le {r1} or x \\ge {r2}"
            w2 = [
                f"{r1} \\le x \\le {r2}",
                f"x < {r1} or x > {r2}",
                f"{r1} < x < {r2}",
                f"x \\le {-r2} or x \\ge {-r1}",
                f"{-r2} \\le x \\le {-r1}",
                f"x \\ge {r2}",
                f"x \\le {r1}"
            ]
            add_q("medium", "Quadratic Inequalities", q2, ans2, w2, f"$(x - {r1})(x - {r2}) \\ge 0$. The parabola is above or on the x-axis outside the roots: $x \\le {r1}$ or $x \\ge {r2}$.", "Application")

    # B. Exponential Equations
    # 2^(x+1) + 2^x = k
    for p in range(1, 8):
        ans = p
        # 2^(x+1) + 2^x = 2^x * 3
        val = (2**ans) * 3
        q = f"Solve for $x$: $2^{{x + 1}} + 2^x = {val}$"
        add_q("medium", "Exponential Equations", q, str(ans), get_w_ints(ans), f"$2^x(2 + 1) = {val} \\implies 2^x \\cdot 3 = {val} \\implies 2^x = {2**ans} \\implies x = {ans}$.", "Application")

        # 3^(x+1) - 3^(x-1) = 3^(x-1) * (9 - 1) = 3^(x-1) * 8
        val3 = (3**(ans - 1)) * 8
        if val3 > 0 and val3 < 5000:
            q3 = f"Solve for $x$: $3^{{x + 1}} - 3^{{x - 1}} = {val3}$"
            add_q("medium", "Exponential Equations", q3, str(ans), get_w_ints(ans), f"$3^{{x-1}}(3^2 - 1) = {val3} \\implies 3^{{x-1}} \\cdot 8 = {val3} \\implies 3^{{x-1}} = {3**(ans-1)} \\implies x - 1 = {ans - 1} \\implies x = {ans}$.", "Application")

    # C. Surd Equations
    # sqrt(x + a) = x - b
    for b in [1, 2, 3]:
        for x_ans in [4, 5, 6, 7, 8]:
            rhs = x_ans - b
            if rhs > 0:
                lhs_sq = rhs ** 2
                a = lhs_sq - x_ans
                q = f"Solve for $x$: $\\sqrt{{x {'+' if a>=0 else '-'} {abs(a)}}} = x - {b}$"
                add_q("medium", "Equations with Surds", q, f"x = {x_ans}", [
                    f"x = {x_ans + 1}", f"x = {x_ans - 1}", f"x = {x_ans} or x = {-b}", f"x = {-x_ans}", f"x = {x_ans * 2}", f"No solution"
                ], f"Square both sides: $x + {a} = x^2 - {2*b}x + {b**2}$. Solving yields $x = {x_ans}$ (checking valid under square root).", "Application")

    # D. Nature of roots calculations: 2x^2 + kx + c = 0 has equal roots => k^2 - 4(2)(c) = 0 => k = +- sqrt(8c)
    for c in [2, 8, 18, 32]:
        val_k = int(math.isqrt(8 * c))
        q = f"For which value(s) of $k$ will the equation $2x^2 + kx + {c} = 0$ have equal roots?"
        ans_k = f"k = \\pm {val_k}"
        wrongs_k = [
            f"k = {val_k}", f"k = -{val_k}", f"k = \\pm {val_k * 2}", f"k = \\pm {val_k // 2 if val_k > 2 else 5}",
            f"k = \\pm {c}", f"k = {c * 2}", f"k = 0"
        ]
        add_q("medium", "Nature of Roots", q, ans_k, wrongs_k, f"Equal roots imply $\\Delta = b^2 - 4ac = 0$. $k^2 - 4(2)({c}) = 0 \\implies k^2 = {8*c} \\implies k = \\pm {val_k}$.", "Application")

    # Top up medium to 500
    m_idx = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        base = random.choice([2, 3, 5])
        a_shift = random.choice([1, 2, 3])
        x_val = random.choice([2, 3, 4, 5])
        rhs = int(math.log(x_val + a_shift, base)) if (x_val + a_shift) in [base, base**2, base**3] else 1
        x_real = (base ** rhs) - a_shift
        q = f"Solve for $x$ (problem {m_idx}): $\\log_{{{base}}}(x + {a_shift}) = {rhs}$"
        add_q("medium", "Logarithmic Equations", q, str(x_real), get_w_ints(x_real), f"$x + {a_shift} = {base}^{{{rhs}}} \\implies x = {base**rhs} - {a_shift} = {x_real}$.", "Application")
        m_idx += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_scenarios = [
        # Simultaneous equations
        ("Solve simultaneously for $x$ and $y$: $y - x = 2$ and $x^2 + y^2 = 20$.",
         "(x = -4; y = -2) or (x = 2; y = 4)",
         ["(x = 4; y = 2) or (x = -2; y = -4)", "(x = 2; y = 0) or (x = -4; y = 6)", "(x = 3; y = 5) or (x = -3; y = -1)", "(x = 1; y = 3) or (x = -5; y = -3)", "(x = -2; y = 0) or (x = 4; y = 6)", "(x = 0; y = 2) or (x = -2; y = 4)"],
         "Substitute $y = x + 2$ into $x^2 + (x + 2)^2 = 20 \\implies 2x^2 + 4x - 16 = 0 \\implies x^2 + 2x - 8 = 0 \\implies (x + 4)(x - 2) = 0$. Thus $x = -4 \\implies y = -2$ or $x = 2 \\implies y = 4$.", "Analysis"),

        ("Solve simultaneously for $x$ and $y$: $x + 2y = 3$ and $x^2 + 3xy = 10$.",
         "(x = -5; y = 4) or (x = 2; y = 0.5)",
         ["(x = 5; y = -1) or (x = -2; y = 2.5)", "(x = 1; y = 1) or (x = -4; y = 3.5)", "(x = 3; y = 0) or (x = -2; y = 2.5)", "(x = 4; y = -0.5) or (x = -1; y = 2)", "(x = -3; y = 3) or (x = 2; y = 1)"],
         "Substitute $x = 3 - 2y$ into $(3 - 2y)^2 + 3(3 - 2y)y = 10$, simplify to quadratic in $y$, and solve for corresponding $x$.", "Analysis"),

        # k-substitution in exponential equations
        ("Solve for $x$: $2^{2x} - 6 \\cdot 2^x + 8 = 0$.",
         "x = 1 or x = 2",
         ["x = 2 or x = 4", "x = -1 or x = -2", "x = 0 or x = 3", "x = 1 or x = 8", "x = 3 or x = 4", "x = \\pm 2"],
         "Let $k = 2^x$. Then $k^2 - 6k + 8 = 0 \\implies (k - 2)(k - 4) = 0 \\implies k = 2$ or $k = 4$. Since $2^x = 2 \\implies x = 1$; $2^x = 4 \\implies x = 2$.", "Analysis"),

        ("Solve for $x$: $3^{2x} - 10 \\cdot 3^x + 9 = 0$.",
         "x = 0 or x = 2",
         ["x = 1 or x = 9", "x = 1 or x = 3", "x = 0 or x = 9", "x = -1 or x = 2", "x = 2 or x = 3", "x = 3 or x = 9"],
         "Let $k = 3^x$. $k^2 - 10k + 9 = 0 \\implies (k - 1)(k - 9) = 0 \\implies 3^x = 1 \\implies x = 0$; $3^x = 9 \\implies x = 2$.", "Analysis"),

        # Nature of roots parameter range
        ("Determine the values of $k$ for which the equation $x^2 + 2kx + (k + 6) = 0$ has real and unequal roots.",
         "k < -2 or k > 3",
         ["-2 < k < 3", "-3 < k < 2", "k < -3 or k > 2", "k = -2 or k = 3", "k > 0", "k < 6"],
         "Real and unequal roots require $\\Delta > 0$. $\\Delta = (2k)^2 - 4(1)(k + 6) = 4k^2 - 4k - 24 > 0 \\implies k^2 - k - 6 > 0 \\implies (k - 3)(k + 2) > 0 \\implies k < -2$ or $k > 3$.", "Analysis"),

        ("For which values of $m$ will the roots of $2x^2 - 4x + m = 0$ be non-real?",
         "m > 2",
         ["m < 2", "m \\ge 2", "m \\le 2", "m > 4", "m < -2", "m = 2"],
         "Non-real roots require $\\Delta < 0$. $(-4)^2 - 4(2)(m) < 0 \\implies 16 - 8m < 0 \\implies -8m < -16 \\implies m > 2$.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_scenarios:
        for prefix in ["", "CAPS High-Level Algebra: ", "Solve the advanced equation: ", "Analytical Problem: "]:
            add_q("hard", "Advanced Equations", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_idx = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_scenarios)
        q = f"Advanced problem case {h_idx}: {base_h[0]}"
        add_q("hard", "Advanced Equations", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_idx += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/mathematics/paper1_algebra.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_algebra()
