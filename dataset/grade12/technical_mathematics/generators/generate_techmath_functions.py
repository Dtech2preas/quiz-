import json
import os
import random
import math
import time

def build_functions_dataset():
    questions = []
    seen_questions = set()
    
    target_easy = 300
    target_med = 500
    target_hard = 200
    counts = {"easy": 0, "medium": 0, "hard": 0}
    
    def add_q(subtopic, difficulty, q_text, correct_ans, distractors, explanation):
        if counts[difficulty] >= (target_easy if difficulty == "easy" else target_med if difficulty == "medium" else target_hard):
            return False
        if q_text in seen_questions:
            return False
            
        c_str = str(correct_ans).strip()
        clean_dist = []
        seen_d = {c_str}
        for d in distractors:
            d_str = str(d).strip()
            if d_str and d_str not in seen_d:
                seen_d.add(d_str)
                clean_dist.append(d_str)
                
        if len(clean_dist) < 6:
            return False
            
        seen_questions.add(q_text)
        counts[difficulty] += 1
        q_id = f"TM12_P1_FUN_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Functions & Graphs",
            "subtopic": subtopic,
            "paper": "paper1",
            "difficulty": difficulty,
            "question": q_text,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_dist[:8],
            "explanation": explanation,
            "tags": {
                "grade": "12",
                "subject": "Technical Mathematics",
                "topic": "Functions & Graphs",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Hyperbola Asymptotes
    for p in range(-9, 10):
        for q in range(-9, 10):
            if p == 0 and q == 0: continue
            a_val = random.choice([-6, -4, -3, -2, 2, 3, 4, 6])
            p_sign = f"- {p}" if p > 0 else f"+ {abs(p)}" if p < 0 else ""
            denom = f"x {p_sign}" if p != 0 else "x"
            q_sign = f"+ {q}" if q > 0 else f"- {abs(q)}" if q < 0 else ""
            eq_str = f"y = \\frac{{{a_val}}}{{{denom}}} {q_sign}".strip()
            
            q_va = f"Determine the equation of the vertical asymptote of the hyperbola ${eq_str}$."
            c_va = f"$x = {p}$"
            d_va = [
                f"$x = {-p}$", f"$y = {q}$", f"$y = {-q}$", f"$x = {q}$",
                f"$y = {p}$", f"$x = {a_val}$", f"$y = 0$"
            ]
            exp_va = f"The vertical asymptote occurs where the denominator equals zero: ${denom} = 0 \\implies x = {p}$."
            add_q("Hyperbolic Functions", "easy", q_va, c_va, d_va, exp_va)

            q_ha = f"Determine the equation of the horizontal asymptote of the hyperbola ${eq_str}$."
            c_ha = f"$y = {q}$"
            d_ha = [
                f"$y = {-q}$", f"$x = {p}$", f"$x = {-p}$", f"$y = {p}$",
                f"$x = {q}$", f"$y = {a_val}$", f"$x = 0$"
            ]
            exp_ha = f"As $x \\to \\pm\\infty$, the fraction $\\frac{{{a_val}}}{{{denom}}} \\to 0$, giving horizontal asymptote $y = {q}$."
            add_q("Hyperbolic Functions", "easy", q_ha, c_ha, d_ha, exp_ha)

    # 1b. Semi-circle Domain and Range
    for r in range(2, 16):
        r_sq = r * r
        # Upper semi-circle: y = sqrt(r^2 - x^2)
        q_sc_dom = f"Determine the domain of the semi-circle function $f(x) = \\sqrt{{{r_sq} - x^2}}$."
        c_sc_dom = f"${-r} \\le x \\le {r}$"
        d_sc_dom = [
            f"$0 \\le x \\le {r}$", f"${-r_sq} \\le x \\le {r_sq}$", f"$x \\ge {-r}$",
            f"$x \\le {r}$", f"${-r} < x < {r}$", f"$x \\in \\mathbb{{R}}$", f"${-r} \\le y \\le {r}$"
        ]
        exp_sc_dom = f"For the square root to be real: ${r_sq} - x^2 \\ge 0 \\implies x^2 \\le {r_sq} \\implies {-r} \\le x \\le {r}$."
        add_q("Semi-circles", "easy", q_sc_dom, c_sc_dom, d_sc_dom, exp_sc_dom)

        q_sc_rng = f"Determine the range of the upper semi-circle function $f(x) = \\sqrt{{{r_sq} - x^2}}$."
        c_sc_rng = f"$0 \\le y \\le {r}$"
        d_sc_rng = [
            f"${-r} \\le y \\le {r}$", f"$y \\ge 0$", f"$0 \\le y \\le {r_sq}$",
            f"$0 < y < {r}$", f"${-r} \\le x \\le {r}$", f"$y \\le {r}$", f"$y \\in \\mathbb{{R}}$"
        ]
        exp_sc_rng = f"The principal square root is non-negative, with minimum $y = 0$ at $x = \\pm {r}$ and maximum $y = {r}$ at $x = 0$. Range: $0 \\le y \\le {r}$."
        add_q("Semi-circles", "easy", q_sc_rng, c_sc_rng, d_sc_rng, exp_sc_rng)

        # Lower semi-circle: y = -sqrt(r^2 - x^2)
        q_lsc_rng = f"Determine the range of the lower semi-circle function $g(x) = -\\sqrt{{{r_sq} - x^2}}$."
        c_lsc_rng = f"${-r} \\le y \\le 0$"
        d_lsc_rng = [
            f"$0 \\le y \\le {r}$", f"${-r} \\le y \\le {r}$", f"$y \\le 0$",
            f"${-r_sq} \\le y \\le 0$", f"${-r} < y < 0$", f"${-r} \\le x \\le {r}$", f"$y \\in \\mathbb{{R}}$"
        ]
        exp_lsc_rng = f"The negative square root has maximum $y = 0$ at $x = \\pm {r}$ and minimum $y = -{r}$ at $x = 0$. Range: ${-r} \\le y \\le 0$."
        add_q("Semi-circles", "easy", q_lsc_rng, c_lsc_rng, d_lsc_rng, exp_lsc_rng)

    # 1c. Trigonometric Graphs: Amplitude and Period
    for a_tr in [1, 2, 3, 4, 5]:
        for b_tr in [1, 2, 3, 4]:
            period_sin = 360 // b_tr
            period_tan = 180 // b_tr
            b_str = f"{b_tr}x" if b_tr != 1 else "x"
            
            q_amp = f"Determine the amplitude of the trigonometric function $f(x) = {a_tr}\\sin({b_str})$."
            c_amp = str(a_tr)
            d_amp = [str(a_tr * 2), str(period_sin), str(b_tr), str(-a_tr), str(round(a_tr / 2, 1)), "1", "360"]
            exp_amp = f"Amplitude is the absolute value of the leading coefficient: $|a| = |{a_tr}| = {a_tr}$."
            add_q("Trigonometric Graphs", "easy", q_amp, c_amp, d_amp, exp_amp)

            q_per = f"Determine the period of the trigonometric function $g(x) = {a_tr}\\cos({b_str})$."
            c_per = f"{period_sin}^\\circ"
            d_per = [
                f"{period_sin * 2}^\\circ", f"{period_sin // 2 if period_sin > 60 else period_sin + 60}^\\circ",
                "360^\\circ", "180^\\circ", f"{a_tr}^\\circ", f"{b_tr}^\\circ", "720^\\circ"
            ]
            exp_per = f"The period of $y = \\cos(bx)$ is $\\frac{{360^\\circ}}{{b}} = \\frac{{360^\\circ}}{{{b_tr}}} = {period_sin}^\\circ$."
            add_q("Trigonometric Graphs", "easy", q_per, c_per, d_per, exp_per)

    # 1d. Parabola Axis of Symmetry
    for p_sym in range(-8, 9):
        for q_sym in [-5, -2, 1, 3, 7]:
            p_s = f"- {p_sym}" if p_sym > 0 else f"+ {abs(p_sym)}" if p_sym < 0 else ""
            q_s = f"+ {q_sym}" if q_sym > 0 else f"- {abs(q_sym)}"
            inner = f"(x {p_s})" if p_sym != 0 else "x"
            
            q_sym_axis = f"State the equation of the axis of symmetry for the parabola $f(x) = 2{inner}^2 {q_s}$."
            c_sym_axis = f"$x = {p_sym}$"
            d_sym_axis = [
                f"$x = {-p_sym}$", f"$y = {q_sym}$", f"$y = {-q_sym}$",
                f"$x = {q_sym}$", f"$y = {p_sym}$", f"$x = 2$", f"$y = 0$"
            ]
            exp_sym_axis = f"The axis of symmetry of $f(x) = a(x - p)^2 + q$ is given by $x = p$. Here, $x = {p_sym}$."
            add_q("Quadratic Functions (Parabolas)", "easy", q_sym_axis, c_sym_axis, d_sym_axis, exp_sym_axis)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Parabola Turning Point and Range
    for a_pb in [-2, -1, 1, 2, 3]:
        for p_pb in range(-5, 6):
            for q_pb in range(-6, 7):
                p_str = f"- {p_pb}" if p_pb > 0 else f"+ {abs(p_pb)}" if p_pb < 0 else ""
                q_str = f"+ {q_pb}" if q_pb > 0 else f"- {abs(q_pb)}" if q_pb < 0 else ""
                brk = f"(x {p_str})" if p_pb != 0 else "x"
                a_str = f"{a_pb}" if a_pb != 1 else ""
                if a_pb == -1: a_str = "-"
                
                # Turning Point
                q_tp = f"Determine the coordinates of the turning point of the parabola $f(x) = {a_str}{brk}^2 {q_str}$."
                c_tp = f"$({p_pb}; {q_pb})$"
                d_tp = [
                    f"$({-p_pb}; {q_pb})$", f"$({p_pb}; {-q_pb})$", f"$({-p_pb}; {-q_pb})$",
                    f"$({q_pb}; {p_pb})$", f"$(0; {q_pb})$", f"$({p_pb}; 0)$", f"$(0; 0)$"
                ]
                exp_tp = f"In vertex form $y = a(x - p)^2 + q$, the turning point is $(p; q) = ({p_pb}; {q_pb})$."
                add_q("Quadratic Functions (Parabolas)", "medium", q_tp, c_tp, d_tp, exp_tp)

                # Range
                rng_sym = "\\ge" if a_pb > 0 else "\\le"
                q_rng = f"Determine the range of the parabolic function $f(x) = {a_str}{brk}^2 {q_str}$."
                c_rng = f"$y {rng_sym} {q_pb}$"
                d_rng = [
                    f"$y {('\\le' if a_pb > 0 else '\\ge')} {q_pb}$",
                    f"$y {rng_sym} {-q_pb}$",
                    f"$x {rng_sym} {p_pb}$",
                    f"$y \\in \\mathbb{{R}}$",
                    f"$y {rng_sym} {p_pb}$",
                    f"$y {rng_sym} 0$",
                    f"${min(p_pb, q_pb)} \\le y \\le {max(p_pb, q_pb)}$"
                ]
                exp_rng = f"Since $a = {a_pb}$ ({'opens upward' if a_pb > 0 else 'opens downward'}), the extreme value is $y = {q_pb}$, giving range $y {rng_sym} {q_pb}$."
                add_q("Quadratic Functions (Parabolas)", "medium", q_rng, c_rng, d_rng, exp_rng)

    # 2b. Exponential Graphs: Horizontal Asymptote & y-intercept
    for base in [2, 3, 5]:
        for q_exp in range(-7, 8):
            if q_exp == 0: continue
            for a_exp in [1, 2, -1]:
                q_sign = f"+ {q_exp}" if q_exp > 0 else f"- {abs(q_exp)}"
                a_str = f"{a_exp} \\cdot " if a_exp not in [1, -1] else ("-" if a_exp == -1 else "")
                
                # y-intercept (x = 0)
                y_int_val = a_exp * (base ** 0) + q_exp
                q_yint = f"Calculate the $y$-intercept of the exponential function $h(x) = {a_str}{base}^x {q_sign}$."
                c_yint = f"$(0; {y_int_val})$"
                d_yint = [
                    f"$(0; {q_exp})$", f"$(0; {-y_int_val})$", f"$({y_int_val}; 0)$",
                    f"$(0; {a_exp + q_exp + 1})$", f"$(0; {base + q_exp})$", f"$(0; 0)$", f"$(0; 1)$"
                ]
                exp_yint = f"Substitute $x = 0$: $h(0) = {a_str}{base}^0 {q_sign} = {a_exp}(1) + ({q_exp}) = {y_int_val}$. The $y$-intercept is $(0; {y_int_val})$."
                add_q("Exponential Functions", "medium", q_yint, c_yint, d_yint, exp_yint)

    # 2c. Hyperbola: Finding Equation given point and asymptotes
    for p_h in [-3, -2, -1, 1, 2, 3]:
        for q_h in [-4, -2, 2, 4]:
            for a_cand in [-6, -4, 2, 4, 6]:
                # pick x0 such that x0 != p_h and (x0 - p_h) divides a_cand
                x0 = p_h + (2 if a_cand % 2 == 0 else 1)
                y0 = (a_cand // (x0 - p_h)) + q_h
                
                q_find_a = (f"The hyperbola $y = \\frac{{a}}{{x - ({p_h})}} + ({q_h})$ passes through the point $({x0}; {y0})$. "
                            f"Calculate the value of $a$.")
                c_find_a = str(a_cand)
                d_find_a = [
                    str(-a_cand), str(a_cand * 2), str(a_cand + 2), str(a_cand - 2),
                    str(y0), str(x0), str(q_h)
                ]
                exp_find_a = (f"Substitute $({x0}; {y0})$ into the equation: "
                              f"${y0} = \\frac{{a}}{{{x0} - ({p_h})}} + ({q_h}) \\implies {y0 - q_h} = \\frac{{a}}{{{x0 - p_h}}} "
                              f"\\implies a = ({y0 - q_h}) \\times ({x0 - p_h}) = {a_cand}$.")
                add_q("Hyperbolic Functions", "medium", q_find_a, c_find_a, d_find_a, exp_find_a)

    # 2d. Trigonometric Graphs: Phase Shift & Vertical Translation
    for trig_fn in ["\\sin", "\\cos"]:
        for p_deg in [30, 45, 60, 90]:
            for v_shift in [-2, -1, 1, 2, 3]:
                v_s = f"+ {v_shift}" if v_shift > 0 else f"- {abs(v_shift)}"
                
                q_max = f"Determine the maximum value of $f(x) = 2{trig_fn}(x - {p_deg}^\\circ) {v_s}$."
                c_max = str(2 + v_shift)
                d_max = [
                    str(2 - v_shift), str(v_shift), str(2), str(-2 + v_shift),
                    str(4 + v_shift), str(1 + v_shift), "0"
                ]
                exp_max = f"The maximum of ${trig_fn}(\\dots)$ is $1$. Maximum $f(x) = 2(1) + ({v_shift}) = {2 + v_shift}$."
                add_q("Trigonometric Graphs", "medium", q_max, c_max, d_max, exp_max)

                q_min = f"Determine the minimum value of $f(x) = 2{trig_fn}(x - {p_deg}^\\circ) {v_s}$."
                c_min = str(-2 + v_shift)
                d_min = [
                    str(2 + v_shift), str(-2 - v_shift), str(-v_shift), str(-2),
                    str(v_shift - 1), str(-4 + v_shift), "0"
                ]
                exp_min = f"The minimum of ${trig_fn}(\\dots)$ is $-1$. Minimum $f(x) = 2(-1) + ({v_shift}) = {-2 + v_shift}$."
                add_q("Trigonometric Graphs", "medium", q_min, c_min, d_min, exp_min)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Graphical Inequalities: f(x) * g(x) <= 0 or f(x) >= g(x)
    for r1 in [-4, -3, -2]:
        for r2 in [2, 3, 4]:
            for m_line in [1, 2]:
                c_line = 0
                # Parabola f(x) = (x - r1)(x - r2) = x^2 - (r1+r2)x + r1*r2
                # Line g(x) = m*x
                # f(x) <= 0 between r1 and r2
                q_ginq = (f"The sketch shows a parabola $f(x) = (x - ({r1}))(x - {r2})$ and the $x$-axis. "
                          f"For which values of $x$ is $f(x) \\le 0$?")
                c_ginq = f"${r1} \\le x \\le {r2}$"
                d_ginq = [
                    f"$x \\le {r1}$ or $x \\ge {r2}$",
                    f"$x < {r1}$ or $x > {r2}$",
                    f"${r1} < x < {r2}$",
                    f"$x \\le {r2}$",
                    f"$x \\ge {r1}$",
                    f"${-r2} \\le x \\le {-r1}$",
                    f"$x = {r1}$ or $x = {r2}$"
                ]
                exp_ginq = f"The parabola opens upward with $x$-intercepts at $x = {r1}$ and $x = {r2}$. It lies on or below the $x$-axis for ${r1} \\le x \\le {r2}$."
                add_q("Interpretation of Graphs", "hard", q_ginq, c_ginq, d_ginq, exp_ginq)

                q_ginq_pos = (f"Given the parabola $f(x) = (x - ({r1}))(x - {r2})$. "
                              f"For which values of $x$ is $f(x) > 0$?")
                c_ginq_pos = f"$x < {r1}$ or $x > {r2}$"
                d_ginq_pos = [
                    f"${r1} < x < {r2}$",
                    f"${r1} \\le x \\le {r2}$",
                    f"$x \\le {r1}$ or $x \\ge {r2}$",
                    f"$x > {r2}$ only",
                    f"$x < {r1}$ only",
                    f"$x < {-r2}$ or $x > {-r1}$",
                    f"$x \\in \\mathbb{{R}}$"
                ]
                exp_ginq_pos = f"The graph is strictly above the $x$-axis outside the roots: $x < {r1}$ or $x > {r2}$."
                add_q("Interpretation of Graphs", "hard", q_ginq_pos, c_ginq_pos, d_ginq_pos, exp_ginq_pos)

    # 3b. Semi-circle and Straight Line Intersections
    for rad in [3, 4, 5, 6, 8, 10]:
        # y = sqrt(rad^2 - x^2) intersects y = m*x at origin? No, at x = rad / sqrt(1 + m^2)
        # Test line y = x: x^2 + x^2 = rad^2 => 2x^2 = rad^2 => x = rad / sqrt(2)
        # Or horizontal line y = k
        for k_val in [1, 2, 3, 4]:
            if k_val >= rad: continue
            x_int = round(math.sqrt(rad**2 - k_val**2), 2)
            q_sc_line = (f"Determine the coordinates of the points of intersection between the upper semi-circle "
                         f"$f(x) = \\sqrt{{{rad**2} - x^2}}$ and the horizontal line $y = {k_val}$.")
            c_sc_line = f"$({-x_int}; {k_val})$ and $({x_int}; {k_val})$"
            d_sc_line = [
                f"$({x_int}; {k_val})$ only",
                f"$({-x_int}; {-k_val})$ and $({x_int}; {-k_val})$",
                f"$(0; {k_val})$ and $({rad}; {k_val})$",
                f"$({-rad}; {k_val})$ and $({rad}; {k_val})$",
                f"$({-k_val}; {x_int})$ and $({k_val}; {x_int})$",
                f"$({round(x_int*1.5, 2)}; {k_val})$ and $({-round(x_int*1.5, 2)}; {k_val})$",
                "No intersection points"
            ]
            exp_sc_line = (f"Set $\\sqrt{{{rad**2} - x^2}} = {k_val} \\implies {rad**2} - x^2 = {k_val**2} "
                           f"\\implies x^2 = {rad**2 - k_val**2} \\implies x = \\pm {x_int}$. "
                           f"Intersection points: $({-x_int}; {k_val})$ and $({x_int}; {k_val})$.")
            add_q("Semi-circles", "hard", q_sc_line, c_sc_line, d_sc_line, exp_sc_line)

    # 3c. Function Transformations and Reflections
    for a_tf in [2, 3, 4]:
        for p_tf in [1, 2, 3]:
            for q_tf in [1, 2, 4]:
                q_refl_x = (f"The function $f(x) = {a_tf}(x - {p_tf})^2 + {q_tf}$ is reflected across the $x$-axis to form $g(x)$. "
                            f"Determine the equation of $g(x)$.")
                c_refl_x = f"$g(x) = -{a_tf}(x - {p_tf})^2 - {q_tf}$"
                d_refl_x = [
                    f"$g(x) = -{a_tf}(x + {p_tf})^2 + {q_tf}$",
                    f"$g(x) = {a_tf}(x + {p_tf})^2 - {q_tf}$",
                    f"$g(x) = {a_tf}(x - {p_tf})^2 - {q_tf}$",
                    f"$g(x) = -{a_tf}(x - {p_tf})^2 + {q_tf}$",
                    f"$g(x) = {a_tf}(x + {p_tf})^2 + {q_tf}$",
                    f"$g(x) = \\frac{{1}}{{{a_tf}}}(x - {p_tf})^2 + {q_tf}$",
                    f"$g(x) = -{a_tf}x^2 - {q_tf}$"
                ]
                exp_refl_x = f"Reflection across the $x$-axis transforms $y = f(x)$ into $y = -f(x) = -[{a_tf}(x - {p_tf})^2 + {q_tf}] = -{a_tf}(x - {p_tf})^2 - {q_tf}$."
                add_q("Transformation of Functions", "hard", q_refl_x, c_refl_x, d_refl_x, exp_refl_x)

                q_refl_y = (f"The function $f(x) = {a_tf}(x - {p_tf})^2 + {q_tf}$ is reflected across the $y$-axis to form $h(x)$. "
                            f"Determine the equation of $h(x)$.")
                c_refl_y = f"$h(x) = {a_tf}(x + {p_tf})^2 + {q_tf}$"
                d_refl_y = [
                    f"$h(x) = -{a_tf}(x - {p_tf})^2 + {q_tf}$",
                    f"$h(x) = -{a_tf}(x + {p_tf})^2 - {q_tf}$",
                    f"$h(x) = {a_tf}(x - {p_tf})^2 - {q_tf}$",
                    f"$h(x) = {a_tf}(-x - {p_tf})^2 - {q_tf}$",
                    f"$h(x) = -{a_tf}(x + {p_tf})^2 + {q_tf}$",
                    f"$h(x) = {a_tf}x^2 + {q_tf}$",
                    f"$h(x) = 2{a_tf}(x + {p_tf})^2 + {q_tf}$"
                ]
                exp_refl_y = f"Reflection across the $y$-axis replaces $x$ with $-x$: $h(x) = f(-x) = {a_tf}(-x - {p_tf})^2 + {q_tf} = {a_tf}(-(x + {p_tf}))^2 + {q_tf} = {a_tf}(x + {p_tf})^2 + {q_tf}$."
                add_q("Transformation of Functions", "hard", q_refl_y, c_refl_y, d_refl_y, exp_refl_y)

    # 3d. Intersections of Horizontal Line y = k with Parabola
    for a_k in [-2, -1, 1, 2]:
        for p_k in [-3, -1, 2, 4]:
            for q_k in [-5, -2, 1, 3, 6]:
                # y = a_k*(x - p_k)^2 + q_k
                p_str = f"- {p_k}" if p_k > 0 else f"+ {abs(p_k)}" if p_k < 0 else ""
                q_str = f"+ {q_k}" if q_k > 0 else f"- {abs(q_k)}"
                brk = f"(x {p_str})" if p_k != 0 else "x"
                a_str = f"{a_k}" if a_k != 1 else ""
                if a_k == -1: a_str = "-"
                
                # Condition for 2 distinct real roots:
                # If a > 0, k > q_k; if a < 0, k < q_k
                c_2pts = f"$k > {q_k}$" if a_k > 0 else f"$k < {q_k}$"
                d_2pts = [
                    f"$k < {q_k}$" if a_k > 0 else f"$k > {q_k}$",
                    f"$k \\ge {q_k}$",
                    f"$k = {q_k}$",
                    f"$k > {p_k}$",
                    f"$k < {p_k}$",
                    f"$k \\le 0$",
                    f"$k > 0$"
                ]
                q_2pts = (f"Given the parabola $f(x) = {a_str}{brk}^2 {q_str}$, determine the values of $k$ "
                          f"for which the horizontal line $y = k$ intersects the curve at two distinct points.")
                exp_2pts = (f"The turning point has $y$-coordinate $y = {q_k}$. Since the parabola opens "
                            f"{'upwards ($a > 0$)' if a_k > 0 else 'downwards ($a < 0$)'}, $y = k$ intersects in two points when {c_2pts}.")
                add_q("Quadratic Functions (Parabolas)", "hard", q_2pts, c_2pts, d_2pts, exp_2pts)

                # Condition for no real roots:
                c_0pts = f"$k < {q_k}$" if a_k > 0 else f"$k > {q_k}$"
                d_0pts = [
                    f"$k > {q_k}$" if a_k > 0 else f"$k < {q_k}$",
                    f"$k = {q_k}$",
                    f"$k \\le {q_k}$",
                    f"$k < {p_k}$",
                    f"$k > {p_k}$",
                    f"$k < 0$",
                    f"$k = 0$"
                ]
                q_0pts = (f"For the parabola $f(x) = {a_str}{brk}^2 {q_str}$, determine the values of $k$ "
                          f"such that the line $y = k$ does not intersect the curve at any point.")
                exp_0pts = f"Since the minimum/maximum is at $y = {q_k}$, the line $y = k$ will have no intersections when {c_0pts}."
                add_q("Quadratic Functions (Parabolas)", "hard", q_0pts, c_0pts, d_0pts, exp_0pts)

    # 3e. Finding Equation of Parabola given Intercepts and Third Point
    for r1_p in [-4, -3, -2, -1]:
        for r2_p in [1, 2, 3, 4]:
            for a_fac in [1, 2, -1, -2]:
                # y = a_fac*(x - r1_p)*(x - r2_p)
                # y-intercept: (0, c_val) where c_val = a_fac * (-r1_p) * (-r2_p) = a_fac * r1_p * r2_p
                c_val = a_fac * r1_p * r2_p
                # expanded: a_fac*x^2 - a_fac*(r1_p + r2_p)x + c_val
                b_val = -a_fac * (r1_p + r2_p)
                sgn_b = f"+ {b_val}" if b_val >= 0 else f"- {abs(b_val)}"
                sgn_c = f"+ {c_val}" if c_val >= 0 else f"- {abs(c_val)}"
                a_coef = f"{a_fac}" if a_fac not in [1, -1] else ("-" if a_fac == -1 else "")
                ans_eq = f"$y = {a_coef}x^2 {sgn_b}x {sgn_c}$"
                
                q_eq_p = (f"A parabola has $x$-intercepts at $({r1_p}; 0)$ and $({r2_p}; 0)$, and a $y$-intercept at $(0; {c_val})$. "
                          f"Determine the standard equation of the parabola.")
                d_eq_p = [
                    f"$y = {-a_fac}x^2 {sgn_b}x {sgn_c}$",
                    f"$y = {a_coef}x^2 {-b_val if b_val < 0 else f'+ {-b_val}'}x {sgn_c}$",
                    f"$y = {a_coef}x^2 {sgn_b}x {-c_val if c_val < 0 else f'+ {-c_val}'}$",
                    f"$y = x^2 - {r1_p + r2_p}x + {r1_p * r2_p}$",
                    f"$y = 2x^2 + {b_val}x + {c_val}$",
                    f"$y = {a_coef}(x + {r1_p})(x - {r2_p})$",
                    f"$y = {a_coef}x^2 + {c_val}$"
                ]
                exp_eq_p = (f"Start with intercept form: $y = a(x - ({r1_p}))(x - {r2_p}) = a(x - {r1_p})(x - {r2_p})$. "
                            f"Substitute $(0; {c_val})$: ${c_val} = a(0 - {r1_p})(0 - {r2_p}) = a({r1_p * r2_p}) \\implies a = {a_fac}$. "
                            f"Expanding gives ${ans_eq}$." )
                add_q("Quadratic Functions (Parabolas)", "hard", q_eq_p, ans_eq, d_eq_p, exp_eq_p)

    print(f"Generated Tech Math Functions: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper1_tech_functions.json")
    dataset = build_functions_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
