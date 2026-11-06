import json
import random
import os
import time
import math

def generate_math_trigonometry():
    print("Generating Grade 12 Mathematics: Trigonometry (Paper 2)...")
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
        q_id = f"MATH_P2_TRIG_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Trigonometry",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Trigonometry",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_ints(val, count=8):
        w = set()
        for delta in [-1, 1, -2, 2, -3, 3, 4, -4, 5, -5]:
            if val + delta != val:
                w.add(str(val + delta))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = val + random.randint(6, 25) * random.choice([1, -1])
            if extra != val and str(extra) not in cand_list:
                cand_list.append(str(extra))
        return cand_list[:count]

    def get_w_floats(val, decimals=2, count=8):
        w = set()
        for delta in [-0.5, 0.5, -0.2, 0.2, -1.0, 1.0, -0.1, 0.1]:
            cand = round(val + delta, decimals)
            if cand != val:
                w.add(f"{cand:.{decimals}f}")
        cand_list = list(w)
        while len(cand_list) < count:
            extra = round(val + random.uniform(-4.0, 4.0), decimals)
            s_cand = f"{extra:.{decimals}f}"
            if extra != val and s_cand not in cand_list:
                cand_list.append(s_cand)
        return cand_list[:count]

    def get_w_trig_vals(ans, count=8):
        common_vals = [
            "0", "1", "-1", "1/2", "-1/2", "√3/2", "-√3/2",
            "√2/2", "-√2/2", "√3", "-√3", "1/√3", "-1/√3", "2", "-2"
        ]
        pool = [v for v in common_vals if v != ans]
        random.shuffle(pool)
        return pool[:count]

    # ====================================================
    # EASY QUESTIONS (Target: 300)
    # ====================================================
    easy_count = 0

    # 1. Special Angles exact values (60)
    spec_data = [
        (30, "\\sin", "1/2", "sin(30°) = 1/2"),
        (30, "\\cos", "√3/2", "cos(30°) = √3/2"),
        (30, "\\tan", "1/√3", "tan(30°) = 1/√3"),
        (45, "\\sin", "√2/2", "sin(45°) = √2/2"),
        (45, "\\cos", "√2/2", "cos(45°) = √2/2"),
        (45, "\\tan", "1", "tan(45°) = 1"),
        (60, "\\sin", "√3/2", "sin(60°) = √3/2"),
        (60, "\\cos", "1/2", "cos(60°) = 1/2"),
        (60, "\\tan", "√3", "tan(60°) = √3"),
        (90, "\\sin", "1", "sin(90°) = 1"),
        (90, "\\cos", "0", "cos(90°) = 0"),
        (0, "\\sin", "0", "sin(0°) = 0"),
        (0, "\\cos", "1", "cos(0°) = 1"),
        (0, "\\tan", "0", "tan(0°) = 0"),
        (180, "\\cos", "-1", "cos(180°) = -1"),
        (180, "\\sin", "0", "sin(180°) = 0")
    ]
    phrases_spec = [
        "Without using a calculator, determine the exact value of",
        "What is the exact numerical value of",
        "Evaluate using special angle ratios:",
        "State the exact value of the trigonometric ratio:"
    ]
    while easy_count < 60:
        ang, fn, ans, exp_reason = random.choice(spec_data)
        phr = random.choice(phrases_spec)
        q = f"{phr} ${fn}({ang}^\\circ)$."
        wrongs = get_w_trig_vals(ans)
        exp = f"From special angles: ${fn}({ang}^\\circ) = {ans}$. ({exp_reason})."
        if add_q("easy", "Special Angles", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 2. Fundamental identities with varied angles and coefficients (60)
    while easy_count < 120:
        mode = random.choice(["pyth_num", "pyth_scaled", "quotient_num"])
        if mode == "pyth_num":
            theta = random.randint(11, 88)
            q = f"Simplify without a calculator: $\\sin^2({theta}^\\circ) + \\cos^2({theta}^\\circ)$."
            ans = "1"
            wrongs = ["0", "-1", "2", f"{theta}", f"sin({2*theta}°)", f"cos({2*theta}°)", "1/2"]
            exp = f"By the Pythagorean identity, $\\sin^2(\\theta) + \\cos^2(\\theta) = 1$ for any angle $\\theta$. Here $\\theta = {theta}^\\circ$, so the value is $1$."
        elif mode == "pyth_scaled":
            k = random.randint(2, 9)
            theta = random.randint(11, 88)
            q = f"Calculate the exact value of ${k}\\sin^2({theta}^\\circ) + {k}\\cos^2({theta}^\\circ)$."
            ans = str(k)
            wrongs = get_w_ints(k)
            exp = f"Factor out ${k}$: ${k}(\\sin^2({theta}^\\circ) + \\cos^2({theta}^\\circ)) = {k}(1) = {k}$."
        else:
            theta = random.randint(12, 78)
            q = f"Express $\\frac{{\\sin({theta}^\\circ)}}{{\\cos({theta}^\\circ)}}$ as a single trigonometric ratio."
            ans = f"tan({theta}°)"
            wrongs = [f"cot({theta}°)", f"sin({theta}°)", f"cos({theta}°)", "1", f"tan({2*theta}°)", f"-tan({theta}°)", f"tan({90-theta}°)"]
            exp = f"Using the quotient identity: $\\frac{{\\sin(\\theta)}}{{\\cos(\\theta)}} = \\tan(\\theta) = \\tan({theta}^\\circ)$."
            
        if add_q("easy", "Identities", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 3. Reduction formulas & co-functions with numerical/variable angles (60)
    red_rules = [
        ("180 - theta", "sin", "sin", False),
        ("180 - theta", "cos", "cos", True),
        ("180 - theta", "tan", "tan", True),
        ("180 + theta", "sin", "sin", True),
        ("180 + theta", "cos", "cos", True),
        ("180 + theta", "tan", "tan", False),
        ("360 - theta", "cos", "cos", False),
        ("360 - theta", "sin", "sin", True),
        ("90 - theta", "sin", "cos", False),
        ("90 - theta", "cos", "sin", False),
        ("neg_theta", "sin", "sin", True),
        ("neg_theta", "cos", "cos", False)
    ]
    var_symbols = ["x", "\\theta", "\\alpha", "\\beta", "A"]
    while easy_count < 180:
        rule_type, in_fn, out_fn, is_neg = random.choice(red_rules)
        var = random.choice(var_symbols)
        if rule_type == "180 - theta":
            expr = f"\\{in_fn}(180^\\circ - {var})"
            reason = f"In Quadrant II, {in_fn} is {'negative' if is_neg else 'positive'}"
        elif rule_type == "180 + theta":
            expr = f"\\{in_fn}(180^\\circ + {var})"
            reason = f"In Quadrant III, {in_fn} is {'negative' if is_neg else 'positive'}"
        elif rule_type == "360 - theta":
            expr = f"\\{in_fn}(360^\\circ - {var})"
            reason = f"In Quadrant IV, {in_fn} is {'negative' if is_neg else 'positive'}"
        elif rule_type == "90 - theta":
            expr = f"\\{in_fn}(90^\\circ - {var})"
            reason = "By co-function complementary identity"
        else:
            expr = f"\\{in_fn}(-{var})"
            reason = f"{in_fn} is an {'odd' if is_neg else 'even'} function"
            
        sign_str = "-" if is_neg else ""
        ans = f"{sign_str}{out_fn}({var.replace('\\', '')})"
        
        all_alts = [
            f"{out_fn}({var.replace('\\', '')})",
            f"-{out_fn}({var.replace('\\', '')})",
            f"{in_fn}({var.replace('\\', '')})",
            f"-{in_fn}({var.replace('\\', '')})",
            f"tan({var.replace('\\', '')})",
            f"-tan({var.replace('\\', '')})",
            "1", "-1", "0"
        ]
        wrongs = [a for a in all_alts if a != ans]
        phr = random.choice(["Apply reduction formulas to simplify:", "Express as a single trigonometric ratio:", "Simplify the reduction expression:"])
        q = f"{phr} ${expr}$."
        exp = f"${expr} = {ans}$. ({reason})."
        if add_q("easy", "Reduction Formulas", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 4. Trig graphs amplitude and period (60)
    while easy_count < 240:
        a = random.randint(2, 9)
        b = random.choice([1, 2, 3, 4, 6])
        fn = random.choice(["\\sin", "\\cos"])
        var = random.choice(["x", "\\theta"])
        mode = random.choice(["amplitude", "period"])
        if mode == "amplitude":
            q = f"Determine the amplitude of the trigonometric function $y = {a}{fn}({b}{var})$."
            ans = str(a)
            wrongs = get_w_ints(a)
            exp = f"For $y = a{fn}(bx)$, the amplitude is $|a| = |{a}| = {ans}$."
        else:
            period_val = 360 // b
            q = f"Determine the period of the trigonometric function $y = {a}{fn}({b}{var})$."
            ans = f"{period_val}°"
            wrongs = [f"{w}°" for w in [360, 180, 720, 90, 120, 60, 540, 270] if w != period_val]
            exp = f"The period is $\\frac{{360^\\circ}}{{b}} = \\frac{{360^\\circ}}{{{b}}} = {ans}$."
            
        if add_q("easy", "Trig Graphs", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 5. Area Rule simple calculation (60)
    while easy_count < 300:
        a_side = random.randint(4, 16)
        b_side = random.randint(4, 16)
        ang_C = random.choice([30, 90, 150])
        sin_val = 0.5 if ang_C in [30, 150] else 1.0
        area = 0.5 * a_side * b_side * sin_val
        ans = f"{area:.1f}" if not float(area).is_integer() else str(int(area))
        q = f"In $\\triangle ABC$, side $a = {a_side}$ cm, side $b = {b_side}$ cm, and $\\hat{{C}} = {ang_C}^\\circ$. Calculate the area of $\\triangle ABC$."
        wrongs = get_w_floats(area, 1) if not float(area).is_integer() else get_w_ints(int(area))
        exp = f"$\\text{{Area}} = \\frac{{1}}{{2}}ab\\sin C = \\frac{{1}}{{2}}({a_side})({b_side})\\sin({ang_C}^\\circ) = {ans}\\text{{ cm}}^2$."
        if add_q("easy", "Area Rule", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    print(f"Easy questions created: {easy_count}")

    # ====================================================
    # MEDIUM QUESTIONS (Target: 500)
    # ====================================================
    medium_count = 0

    # 1. Compound angle simplifications with huge parameter space (125)
    phrases_comp = [
        "Evaluate without using a calculator:",
        "Simplify using compound angle formulas:",
        "Calculate the exact numerical value of the expression:",
        "Reduce using compound angle expansions:"
    ]
    while medium_count < 125:
        target_diff = random.choice([30, 45, 60])
        B = random.randint(12, 68)
        A = B + target_diff
        mode = random.choice(["cos_minus", "sin_minus", "cos_plus", "sin_plus"])
        
        if mode == "cos_minus":
            expr = f"\\cos({A}^\\circ)\\cos({B}^\\circ) + \\sin({A}^\\circ)\\sin({B}^\\circ)"
            ans = "1/2" if target_diff == 60 else ("√3/2" if target_diff == 30 else "√2/2")
            formula = f"\\cos({A}^\\circ - {B}^\\circ) = \\cos({target_diff}^\\circ)"
        elif mode == "sin_minus":
            expr = f"\\sin({A}^\\circ)\\cos({B}^\\circ) - \\cos({A}^\\circ)\\sin({B}^\\circ)"
            ans = "1/2" if target_diff == 30 else ("√3/2" if target_diff == 60 else "√2/2")
            formula = f"\\sin({A}^\\circ - {B}^\\circ) = \\sin({target_diff}^\\circ)"
        elif mode == "cos_plus":
            target_sum = random.choice([60, 90])
            B = random.randint(10, target_sum - 10)
            A = target_sum - B
            expr = f"\\cos({A}^\\circ)\\cos({B}^\\circ) - \\sin({A}^\\circ)\\sin({B}^\\circ)"
            ans = "1/2" if target_sum == 60 else "0"
            formula = f"\\cos({A}^\\circ + {B}^\\circ) = \\cos({target_sum}^\\circ)"
        else:
            target_sum = random.choice([30, 90, 150])
            B = random.randint(10, target_sum - 10)
            A = target_sum - B
            expr = f"\\sin({A}^\\circ)\\cos({B}^\\circ) + \\cos({A}^\\circ)\\sin({B}^\\circ)"
            ans = "1/2" if target_sum in [30, 150] else "1"
            formula = f"\\sin({A}^\\circ + {B}^\\circ) = \\sin({target_sum}^\\circ)"

        phr = random.choice(phrases_comp)
        q = f"{phr} ${expr}$."
        wrongs = get_w_trig_vals(ans)
        exp = f"Apply the compound angle identity: ${expr} = {formula} = {ans}$."
        if add_q("medium", "Compound Angles", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 2. Double angle reductions to a single ratio (125)
    phrases_dbl = [
        "Express as a single trigonometric ratio using double angle formulas:",
        "Simplify the trigonometric expression to a single term:",
        "Reduce using double angle identities:",
        "State as a single trigonometric function:"
    ]
    while medium_count < 250:
        theta = random.randint(11, 79)
        dbl = 2 * theta
        mode = random.choice(["2sincos", "cos2_minus_sin2", "1_minus_2sin2", "2cos2_minus_1"])
        if mode == "2sincos":
            expr = f"2\\sin({theta}^\\circ)\\cos({theta}^\\circ)"
            ans = f"sin({dbl}°)"
            wrongs = [f"cos({dbl}°)", f"sin({theta}°)", f"2sin({dbl}°)", f"cos({theta}°)", f"tan({dbl}°)", f"sin({theta//2}°)", "1"]
            exp = f"Using $2\\sin(x)\\cos(x) = \\sin(2x)$, we have $2\\sin({theta}^\\circ)\\cos({theta}^\\circ) = \\sin({dbl}^\\circ)$."
        elif mode == "cos2_minus_sin2":
            expr = f"\\cos^2({theta}^\\circ) - \\sin^2({theta}^\\circ)"
            ans = f"cos({dbl}°)"
            wrongs = [f"sin({dbl}°)", "1", f"cos({theta}°)", f"-cos({dbl}°)", f"tan({dbl}°)", f"2cos({dbl}°)", "0"]
            exp = f"Using $\\cos^2(x) - \\sin^2(x) = \\cos(2x)$, we have $\\cos^2({theta}^\\circ) - \\sin^2({theta}^\\circ) = \\cos({dbl}^\\circ)$."
        elif mode == "1_minus_2sin2":
            expr = f"1 - 2\\sin^2({theta}^\\circ)"
            ans = f"cos({dbl}°)"
            wrongs = [f"sin({dbl}°)", f"-cos({dbl}°)", f"cos({theta}°)", "1", f"2cos({dbl}°)", f"tan({dbl}°)", "0"]
            exp = f"Using $1 - 2\\sin^2(x) = \\cos(2x)$, we have $1 - 2\\sin^2({theta}^\\circ) = \\cos({dbl}^\\circ)$."
        else:
            expr = f"2\\cos^2({theta}^\\circ) - 1"
            ans = f"cos({dbl}°)"
            wrongs = [f"sin({dbl}°)", f"-cos({dbl}°)", f"cos({theta}°)", "1", f"2cos({dbl}°)", f"tan({dbl}°)", "0"]
            exp = f"Using $2\\cos^2(x) - 1 = \\cos(2x)$, we have $2\\cos^2({theta}^\\circ) - 1 = \\cos({dbl}^\\circ)$."

        phr = random.choice(phrases_dbl)
        q = f"{phr} ${expr}$."
        if add_q("medium", "Double Angles", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 3. Sine Rule and Cosine Rule calculations (125)
    while medium_count < 375:
        rule_type = random.choice(["sine_rule", "cosine_rule"])
        if rule_type == "sine_rule":
            a_side = random.randint(6, 25)
            ang_A = 30
            ang_B = random.randint(35, 85)
            sin_B = math.sin(math.radians(ang_B))
            b_val = round(2 * a_side * sin_B, 2)
            ans = f"{b_val:.2f}"
            q = f"In $\\triangle ABC$, $\\hat{{A}} = {ang_A}^\\circ$, $\\hat{{B}} = {ang_B}^\\circ$, and side $a = {a_side}$ cm. Calculate the length of side $b$ (correct to 2 decimal places)."
            wrongs = get_w_floats(b_val)
            exp = f"$\\frac{{b}}{{\\sin B}} = \\frac{{a}}{{\\sin A}} \\implies b = \\frac{{{a_side} \\cdot \\sin({ang_B}^\\circ)}}{{\\sin({ang_A}^\\circ)}} = \\frac{{{a_side} \\cdot {sin_B:.4f}}}{{0.5}} \\approx {ans}\\text{{ cm}}$."
        else:
            a_side = random.randint(5, 18)
            b_side = random.randint(5, 18)
            ang_C = random.randint(35, 125)
            cos_C = math.cos(math.radians(ang_C))
            c_sq = a_side**2 + b_side**2 - 2 * a_side * b_side * cos_C
            c_val = round(math.sqrt(c_sq), 2)
            ans = f"{c_val:.2f}"
            q = f"In $\\triangle ABC$, $a = {a_side}$ cm, $b = {b_side}$ cm, and $\\hat{{C}} = {ang_C}^\\circ$. Use the Cosine Rule to calculate side $c$ (correct to 2 decimal places)."
            wrongs = get_w_floats(c_val)
            exp = f"$c^2 = a^2 + b^2 - 2ab\\cos C = {a_side}^2 + {b_side}^2 - 2({a_side})({b_side})\\cos({ang_C}^\\circ) = {c_sq:.2f} \\implies c = \\sqrt{{{c_sq:.2f}}} \\approx {ans}\\text{{ cm}}$."
            
        if add_q("medium", "Triangle Rules", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 4. General solutions for single trig ratio across 70 angles (125)
    while medium_count < 500:
        func = random.choice(["sin", "cos", "tan"])
        ref = random.randint(12, 78)
        if func == "sin":
            q = f"Determine the general solution for $\\sin(x) = \\sin({ref}^\\circ)$."
            ans = f"x = {ref}° + k·360° or x = {180-ref}° + k·360°, k ∈ Z"
            wrongs = [
                f"x = {ref}° + k·180° or x = {180-ref}° + k·180°, k ∈ Z",
                f"x = ±{ref}° + k·360°, k ∈ Z",
                f"x = {ref}° + k·360°, k ∈ Z",
                f"x = {90-ref}° + k·360° or x = {90+ref}° + k·360°, k ∈ Z",
                f"x = {ref}° + k·180°, k ∈ Z",
                f"x = ±{180-ref}° + k·360°, k ∈ Z",
                f"x = {ref}° + k·720°, k ∈ Z"
            ]
            exp = f"Reference angle is ${ref}^\\circ$. Sine is positive in Quadrants I and II: $x = {ref}^\\circ + k \\cdot 360^\\circ$ or $x = 180^\\circ - {ref}^\\circ + k \\cdot 360^\\circ = {180-ref}^\\circ + k \\cdot 360^\\circ$ ($k \\in \\mathbb{{Z}}$)."
        elif func == "cos":
            q = f"Determine the general solution for $\\cos(x) = \\cos({ref}^\\circ)$."
            ans = f"x = ±{ref}° + k·360°, k ∈ Z"
            wrongs = [
                f"x = {ref}° + k·360° or x = {180-ref}° + k·360°, k ∈ Z",
                f"x = {ref}° + k·180°, k ∈ Z",
                f"x = ±{ref}° + k·180°, k ∈ Z",
                f"x = {ref}° + k·360°, k ∈ Z",
                f"x = ±{90-ref}° + k·360°, k ∈ Z",
                f"x = {180-ref}° + k·360°, k ∈ Z",
                f"x = ±{ref}° + k·720°, k ∈ Z"
            ]
            exp = f"Reference angle is ${ref}^\\circ$. Cosine is positive in Quadrants I and IV: $x = \\pm {ref}^\\circ + k \\cdot 360^\\circ$ ($k \\in \\mathbb{{Z}}$)."
        else:
            q = f"Determine the general solution for $\\tan(x) = \\tan({ref}^\\circ)$."
            ans = f"x = {ref}° + k·180°, k ∈ Z"
            wrongs = [
                f"x = ±{ref}° + k·360°, k ∈ Z",
                f"x = {ref}° + k·360° or x = {180+ref}° + k·360°, k ∈ Z",
                f"x = {ref}° + k·360°, k ∈ Z",
                f"x = {180-ref}° + k·180°, k ∈ Z",
                f"x = ±{ref}° + k·180°, k ∈ Z",
                f"x = {ref}° + k·90°, k ∈ Z",
                f"x = {90-ref}° + k·180°, k ∈ Z"
            ]
            exp = f"Reference angle is ${ref}^\\circ$. Tangent has period $180^\\circ$: $x = {ref}^\\circ + k \\cdot 180^\\circ$ ($k \\in \\mathbb{{Z}}$)."
            
        if add_q("medium", "General Solutions", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    print(f"Medium questions created: {medium_count}")

    # ====================================================
    # HARD QUESTIONS (Target: 200)
    # ====================================================
    hard_count = 0

    # 1. Quadratic trigonometric factorizations (50)
    while hard_count < 50:
        fn_name = random.choice(["cos", "sin"])
        a = random.choice([2, 3, 4])
        b = random.choice([-3, -2, -1, 1, 2, 3])
        c = 1
        d = random.choice([-3, -2, -1, 1, 2, 3])
        quad_a = a * c
        quad_b = a * d + b * c
        quad_c = b * d
        
        r1_str = f"{-b}/{a}" if abs(b) % a != 0 else str(-b // a)
        r2_str = str(-d)
        
        sb = "+" if quad_b >= 0 else "-"
        sc = "+" if quad_c >= 0 else "-"
        term_b = f"{sb} {abs(quad_b)}" if quad_b != 0 else ""
        term_c = f"{sc} {abs(quad_c)}"
        fn_latex = f"\\{fn_name}"
        eq = f"{quad_a}{fn_latex}^2(x) {term_b}{fn_latex}(x) {term_c} = 0"
        
        ans = f"{fn_name}(x) = {r1_str} or {fn_name}(x) = {r2_str}"
        wrongs = [
            f"{fn_name}(x) = {-b} or {fn_name}(x) = {-d}",
            f"{fn_name}(x) = {b}/{a} or {fn_name}(x) = {d}",
            f"{fn_name}(x) = 0 or {fn_name}(x) = 1",
            f"{fn_name}(x) = 1 or {fn_name}(x) = -1",
            f"{fn_name}(x) = √2/2 or {fn_name}(x) = -1",
            f"{fn_name}(x) = {r1_str} or {fn_name}(x) = 0",
            f"{fn_name}(x) = {-d} or {fn_name}(x) = {d}",
            f"{fn_name}(x) = 1/2 or {fn_name}(x) = -1/2"
        ]
        q = f"Solve the quadratic trigonometric equation for ${fn_latex}(x)$: ${eq}$."
        exp = f"Factorizing: $({a}{fn_latex}(x) {'+' if b>0 else '-'} {abs(b)})({fn_latex}(x) {'+' if d>0 else '-'} {abs(d)}) = 0 \\implies {ans}$."
        if add_q("hard", "Trig Equations", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    # 2. Maximum and minimum values of trigonometric functions (50)
    while hard_count < 100:
        a = random.randint(2, 9)
        c = random.randint(-8, 8)
        func = random.choice(["\\sin", "\\cos"])
        b = random.choice([1, 2, 3, 4])
        mode = random.choice(["maximum", "minimum", "range"])
        if mode == "maximum":
            ans_val = a + c
            q = f"Determine the MAXIMUM value of the function $f(x) = {a}{func}({b}x) {'+' if c>=0 else '-'} {abs(c)}$."
            ans = str(ans_val)
            wrongs = get_w_ints(ans_val)
            exp = f"Since the maximum of ${func}({b}x)$ is $1$, $f_{{\\text{{max}}}} = {a}(1) + ({c}) = {ans}$."
        elif mode == "minimum":
            ans_val = -a + c
            q = f"Determine the MINIMUM value of the function $f(x) = {a}{func}({b}x) {'+' if c>=0 else '-'} {abs(c)}$."
            ans = str(ans_val)
            wrongs = get_w_ints(ans_val)
            exp = f"Since the minimum of ${func}({b}x)$ is $-1$, $f_{{\\text{{min}}}} = {a}(-1) + ({c}) = {ans}$."
        else:
            min_v = -a + c
            max_v = a + c
            q = f"Find the range of the function $f(x) = {a}{func}({b}x) {'+' if c>=0 else '-'} {abs(c)}$."
            ans = f"[{min_v}; {max_v}]"
            wrongs = [
                f"[{-a}; {a}]", f"[{min_v-1}; {max_v+1}]", f"[{min_v}; {max_v-1}]",
                f"({min_v}; {max_v})", f"[{-c}; {c}]", f"[{min_v+2}; {max_v+2}]", f"[0; {max_v}]"
            ]
            exp = f"Amplitude is $|{a}| = {a}$. Vertical shift is ${c}$. The range is $[{-a} + ({c}); {a} + ({c})] = {ans}$."
            
        if add_q("hard", "Trig Functions", q, ans, wrongs, exp, "Problem Solving"):
            hard_count += 1

    # 3. Co-function trigonometric equations (50)
    while hard_count < 150:
        eq_type = random.choice(["sin2_cos", "cos2_sin", "sin2_sin", "cos2_cos"])
        if eq_type == "sin2_cos":
            offset = random.choice([6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72])
            base_x = (90 - offset) // 3
            q = f"Find an acute angle solution ($x \\in [0^\\circ; 90^\\circ]$) for: $\\sin(2x) = \\cos(x + {offset}^\\circ)$."
            ans = f"{base_x}°"
            exp = f"$\\sin(2x) = \\sin(90^\\circ - (x + {offset}^\\circ)) = \\sin({90 - offset}^\\circ - x) \\implies 2x = {90 - offset}^\\circ - x \\implies 3x = {90 - offset}^\\circ \\implies x = {ans}$."
        elif eq_type == "cos2_sin":
            offset = random.choice([6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72])
            base_x = (90 - offset) // 3
            q = f"Find an acute angle solution ($x \\in [0^\\circ; 90^\\circ]$) for: $\\cos(2x) = \\sin(x + {offset}^\\circ)$."
            ans = f"{base_x}°"
            exp = f"$\\cos(2x) = \\cos(90^\\circ - (x + {offset}^\\circ)) = \\cos({90 - offset}^\\circ - x) \\implies 2x = {90 - offset}^\\circ - x \\implies 3x = {90 - offset}^\\circ \\implies x = {ans}$."
        elif eq_type == "sin2_sin":
            offset = random.randint(12, 78)
            q = f"Find an acute angle solution ($x \\in [0^\\circ; 90^\\circ]$) for: $\\sin(2x) = \\sin(x + {offset}^\\circ)$."
            ans = f"{offset}°"
            exp = f"Equating arguments: $2x = x + {offset}^\\circ \\implies x = {ans}$."
        else:
            offset = random.randint(12, 78)
            q = f"Find an acute angle solution ($x \\in [0^\\circ; 90^\\circ]$) for: $\\cos(2x) = \\cos(x + {offset}^\\circ)$."
            ans = f"{offset}°"
            exp = f"Equating arguments: $2x = x + {offset}^\\circ \\implies x = {ans}$."

        wrongs = [f"{w}°" for w in [int(ans.replace('°','')) + 10, int(ans.replace('°','')) - 10, int(ans.replace('°','')) + 15, int(ans.replace('°','')) - 15, int(ans.replace('°','')) + 20, 90 - int(ans.replace('°','')), int(ans.replace('°','')) + 30, int(ans.replace('°','')) + 5] if w > 0 and w != int(ans.replace('°',''))]
        while len(wrongs) < 8:
            wrongs.append(f"{random.randint(1, 89)}°")
        if add_q("hard", "Co-function Equations", q, ans, wrongs, exp, "Problem Solving"):
            hard_count += 1

    # 4. Identity simplifications (50)
    ident_list = [
        ("\\frac{\\sin(2{v})}{2\\cos({v})}", "sin({v})", ["cos({v})", "tan({v})", "1", "2sin({v})", "-sin({v})", "cos(2{v})", "2tan({v})"], "$\\frac{2\\sin({v})\\cos({v})}{2\\cos({v})} = \\sin({v})$."),
        ("\\frac{\\sin(2{v})}{\\sin({v})}", "2cos({v})", ["2sin({v})", "cos({v})", "2", "tan({v})", "-cos({v})", "cos(2{v})", "2tan({v})"], "$\\frac{2\\sin({v})\\cos({v})}{\\sin({v})} = 2\\cos({v})$."),
        ("\\frac{1 - \\cos(2{v})}{2}", "sin^2({v})", ["cos^2({v})", "sin({v})", "cos({v})", "1", "tan^2({v})", "-sin^2({v})", "2sin^2({v})"], "$\\frac{2\\sin^2({v})}{2} = \\sin^2({v})$."),
        ("\\frac{1 + \\cos(2{v})}{2}", "cos^2({v})", ["sin^2({v})", "cos({v})", "sin({v})", "1", "tan^2({v})", "-cos^2({v})", "2cos^2({v})"], "$\\frac{2\\cos^2({v})}{2} = \\cos^2({v})$."),
        ("\\frac{\\sin(2{v})}{1 + \\cos(2{v})}", "tan({v})", ["cot({v})", "sin({v})", "cos({v})", "1", "2tan({v})", "-tan({v})", "tan(2{v})"], "$\\frac{2\\sin({v})\\cos({v})}{2\\cos^2({v})} = \\frac{\\sin({v})}{\\cos({v})} = \\tan({v})$."),
        ("\\frac{1 - \\cos(2{v})}{\\sin(2{v})}", "tan({v})", ["cot({v})", "sin({v})", "cos({v})", "1", "sin^2({v})", "-tan({v})", "tan(2{v})"], "$\\frac{2\\sin^2({v})}{2\\sin({v})\\cos({v})} = \\frac{\\sin({v})}{\\cos({v})} = \\tan({v})$."),
        ("(\\sin({v}) + \\cos({v}))^2 - 1", "sin(2{v})", ["cos(2{v})", "0", "1", "2sin({v})", "2cos({v})", "-sin(2{v})", "tan(2{v})"], "$\\sin^2({v}) + \\cos^2({v}) + 2\\sin({v})\\cos({var}) - 1 = 1 + \\sin(2{v}) - 1 = \\sin(2{v})$."),
        ("\\cos^4({v}) - \\sin^4({v})", "cos(2{v})", ["sin(2{v})", "1", "0", "cos^2({v})", "sin^2({v})", "-cos(2{v})", "tan(2{v})"], "$(\\cos^2({v}) - \\sin^2({v}))(\\cos^2({v}) + \\sin^2({v})) = \\cos(2{v}) \\cdot 1 = \\cos(2{v})$."),
        ("\\frac{\\cos(2{v})}{\\cos({v}) - \\sin({v})}", "cos({v}) + sin({v})", ["cos({v}) - sin({v})", "1", "sin(2{v})", "2cos({v})", "tan({v})", "0", "cos(2{v})"], "$\\frac{(\\cos({v})-\\sin({v}))(\\cos({v})+\\sin({v}))}{\\cos({v})-\\sin({v})} = \\cos({v})+\\sin({v})$."),
        ("\\frac{\\cos(2{v})}{\\cos({v}) + \\sin({v})}", "cos({v}) - sin({v})", ["cos({v}) + sin({v})", "1", "sin(2{v})", "2sin({v})", "tan({v})", "0", "cos(2{v})"], "$\\frac{(\\cos({v})-\\sin({v}))(\\cos({v})+\\sin({v}))}{\\cos({v})+\\sin({v})} = \\cos({v})-\\sin({v})$.")
    ]
    phrases = ["Simplify: ", "Reduce to simplest form: ", "Determine the identity: ", "State the simplest equivalent expression for: "]
    while hard_count < 200:
        tmpl, a_tmpl, w_tmpl, exp_tmpl = random.choice(ident_list)
        v = random.choice(["x", "\\theta", "\\alpha", "\\beta", "A", "y"])
        raw_v = v.replace("\\", "")
        phr = random.choice(phrases)
        expr = tmpl.replace("{v}", v)
        ans = a_tmpl.replace("{v}", raw_v)
        wrongs = [w.replace("{v}", raw_v) for w in w_tmpl]
        exp = exp_tmpl.replace("{v}", v)
        q = f"{phr}${expr}$"
        if add_q("hard", "Identities", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    print(f"Final Counts: {{'easy': {easy_count}, 'medium': {medium_count}, 'hard': {hard_count}}}")
    out_dir = "dataset/grade12/mathematics"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_trigonometry.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    t1 = time.time()
    print(f"SUCCESS: {out_file} generated in {t1-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_trigonometry()
