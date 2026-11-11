import json
import os
import random
import math
import time

def build_calculus_dataset():
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
        q_id = f"TM12_P1_CALC_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Differential Calculus & Integration",
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
                "topic": "Differential Calculus & Integration",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Power Rule Differentiation: d/dx [a*x^n + b*x]
    for a in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for n in [2, 3, 4, 5, 6]:
            for b in [-8, -6, -4, -2, 2, 4, 6, 8]:
                an = a * n
                nm1 = n - 1
                nm1_str = f"x^{{{nm1}}}" if nm1 > 1 else "x" if nm1 == 1 else ""
                n_str = f"x^{{{n}}}"
                b_sgn = f"+ {b}" if b >= 0 else f"- {abs(b)}"
                b_deriv_sgn = f"+ {b}" if b >= 0 else f"- {abs(b)}"
                
                q_diff = f"Determine the derivative $\\frac{{dy}}{{dx}}$ if $y = {a}{n_str} {b_sgn}x$."
                c_diff = f"${an}{nm1_str} {b_deriv_sgn}$"
                d_diff = [
                    f"${a}{nm1_str} {b_deriv_sgn}$",
                    f"${an}x^{{{n}}} {b_deriv_sgn}x$",
                    f"${an}{nm1_str}$",
                    f"${an + 1}{nm1_str} {b_deriv_sgn}$",
                    f"${a*n*2}{nm1_str} {b_deriv_sgn}$",
                    f"${an}{nm1_str} - {b}$",
                    f"${a}{n_str} + {b}$"
                ]
                exp_diff = (f"Apply the power rule $\\frac{{d}}{{dx}}[k x^n] = k n x^{{n-1}}$:\n"
                            f"$\\frac{{d}}{{dx}}[{a}{n_str}] = {a} \\times {n} x^{{{n}-1}} = {an}{nm1_str}$.\n"
                            f"$\\frac{{d}}{{dx}}[{b}x] = {b}$.\n"
                            f"Therefore, $\\frac{{dy}}{{dx}} = {c_diff}$.")
                add_q("Rules of Differentiation", "easy", q_diff, c_diff, d_diff, exp_diff)

    # 1b. Basic Indefinite Integrals: int (k*x^p) dx
    for k in [2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 18, 20]:
        for p in [1, 2, 3, 4]:
            np1 = p + 1
            p_str = f"x^{{{p}}}" if p > 1 else "x"
            if k % np1 == 0:
                coef_str = f"{k // np1}" if (k // np1) != 1 else ""
                ans_int = f"${coef_str}x^{{{np1}}} + C$"
            else:
                ans_int = f"$\\frac{{{k}}}{{{np1}}}x^{{{np1}}} + C$"
                
            q_int = f"Evaluate the indefinite integral: $\\int ({k}{p_str}) \\, dx$."
            d_int = [
                f"${k * p}x^{{{p - 1}}} + C$" if p > 1 else f"${k} + C$",
                f"${k}x^{{{np1}}} + C$",
                f"$\\frac{{{k}}}{{{p}}}x^{{{p}}} + C$",
                f"${k + 1}x^{{{np1}}} + C$",
                f"${k}x^{{{p}}} + C$",
                f"$\\frac{{{k}}}{{{np1 + 1}}}x^{{{np1 + 1}}} + C$",
                f"${k * np1}x^{{{np1}}} + C$"
            ]
            exp_int = (f"Apply the power rule of integration: $\\int x^n \\, dx = \\frac{{x^{{n+1}}}}{{n+1}} + C$.\n"
                       f"$\\int {k}{p_str} \\, dx = {k} \\left(\\frac{{x^{{{p}+1}}}}{{{p}+1}}\\right) + C = {ans_int}$.")
            add_q("Integration (Indefinite)", "easy", q_int, ans_int, d_int, exp_int)

    # 1c. Derivative of Reciprocals d/dx [a / x]
    for a_rec in [-8, -6, -4, -2, 2, 3, 4, 5, 6, 7, 8]:
        q_rec = f"Determine the derivative $\\frac{{dy}}{{dx}}$ if $y = \\frac{{{a_rec}}}{{x}}$."
        c_rec = f"$-\\frac{{{a_rec}}}{{x^2}}$" if a_rec > 0 else f"$\\frac{{{abs(a_rec)}}}{{x^2}}$"
        d_rec = [
            f"$\\frac{{{a_rec}}}{{x}}$",
            f"$\\frac{{{a_rec}}}{{x^2}}$" if a_rec > 0 else f"$-\\frac{{{abs(a_rec)}}}{{x^2}}$",
            f"${a_rec}\\ln|x|$",
            f"$-\\frac{{{a_rec}}}{{x}}$",
            f"${-a_rec}x$",
            f"$\\frac{{{a_rec}}}{{2x}}$",
            "0"
        ]
        exp_rec = f"Rewrite $y = {a_rec}x^{{-1}}$. Then $\\frac{{dy}}{{dx}} = {a_rec}(-1)x^{{-2}} = {c_rec}$."
        add_q("Rules of Differentiation", "easy", q_rec, c_rec, d_rec, exp_rec)

    # 1d. Evaluating Derivative at a Point
    for a_ev in [1, 2, 3]:
        for b_ev in [-4, -2, 2, 4]:
            for x_ev in [1, 2, 3, 4, 5]:
                # f(x) = a_ev*x^2 + b_ev*x => f'(x) = 2*a_ev*x + b_ev
                deriv_val = 2 * a_ev * x_ev + b_ev
                b_s = f"+ {b_ev}x" if b_ev >= 0 else f"- {abs(b_ev)}x"
                a_s = f"{a_ev}" if a_ev != 1 else ""
                
                q_ev = f"Given $f(x) = {a_s}x^2 {b_s}$, calculate the value of $f'({x_ev})$."
                c_ev = str(deriv_val)
                d_ev = [
                    str(deriv_val + 2), str(deriv_val - 2), str(deriv_val * 2),
                    str(deriv_val + 4), str(-deriv_val), str(a_ev * x_ev**2 + b_ev * x_ev),
                    str(2 * a_ev * x_ev)
                ]
                exp_ev = (f"First, differentiate: $f'(x) = {2*a_ev}x + ({b_ev})$.\n"
                          f"Then substitute $x = {x_ev}$: $f'({x_ev}) = {2*a_ev}({x_ev}) + ({b_ev}) = {deriv_val}$.")
                add_q("Rules of Differentiation", "easy", q_ev, c_ev, d_ev, exp_ev)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. First Principles Differentiation: f'(x) = lim h->0 [f(x+h) - f(x)] / h
    for a_fp in [-3, -2, -1, 1, 2, 3, 4]:
        for b_fp in [-5, -3, -1, 0, 2, 4, 6]:
            for c_fp in [-4, 2, 5, 8]:
                b_s = f"+ {b_fp}x" if b_fp > 0 else f"- {abs(b_fp)}x" if b_fp < 0 else ""
                c_s = f"+ {c_fp}" if c_fp >= 0 else f"- {abs(c_fp)}"
                a_s = f"{a_fp}" if a_fp not in [1, -1] else ("-" if a_fp == -1 else "")
                fn_str = f"f(x) = {a_s}x^2 {b_s} {c_s}"
                
                deriv_a = 2 * a_fp
                deriv_b = b_fp
                da_s = f"{deriv_a}x"
                db_s = f"+ {deriv_b}" if deriv_b > 0 else f"- {abs(deriv_b)}" if deriv_b < 0 else ""
                c_fp_ans = f"$f'(x) = {da_s} {db_s}$".strip()
                
                q_fp = f"Determine $f'(x)$ from first principles for the function ${fn_str}$."
                d_fp = [
                    f"$f'(x) = {a_fp}x {db_s}$",
                    f"$f'(x) = {deriv_a}x^2 {db_s}$",
                    f"$f'(x) = {deriv_a}x {c_s}$",
                    f"$f'(x) = {deriv_a + 1}x {db_s}$",
                    f"$f'(x) = {-deriv_a}x {db_s}$",
                    f"$f'(x) = {da_s}$",
                    f"$f'(x) = {da_s} + 2h$"
                ]
                exp_fp = (f"Definition of first principles: $f'(x) = \\lim_{{h \\to 0}} \\frac{{f(x+h) - f(x)}}{{h}}$.\n"
                          f"$f(x+h) = {a_s}(x+h)^2 {b_s.replace('x', '(x+h)')} {c_s} = {a_s}(x^2 + 2xh + h^2) + {b_fp}(x+h) {c_s}$.\n"
                          f"$f(x+h) - f(x) = {deriv_a}xh + {a_fp}h^2 + {b_fp}h = h({deriv_a}x + {a_fp}h + {b_fp})$.\n"
                          f"Dividing by $h$ and letting $h \\to 0$ yields $f'(x) = {c_fp_ans}$.")
                add_q("First Principles Differentiation", "medium", q_fp, c_fp_ans, d_fp, exp_fp)

    # 2b. Tangent Lines to Curves: y - y1 = m(x - x1)
    for a_t in [1, 2, -1]:
        for b_t in [-3, -1, 2, 4]:
            for x0_t in [-2, -1, 1, 2, 3]:
                c_t = 3
                y0_t = a_t * (x0_t**2) + b_t * x0_t + c_t
                m_t = 2 * a_t * x0_t + b_t
                c_tan = y0_t - m_t * x0_t
                m_str = f"{m_t}x" if m_t != 1 else "x"
                c_tan_str = f"+ {c_tan}" if c_tan >= 0 else f"- {abs(c_tan)}"
                ans_tan = f"$y = {m_str} {c_tan_str}$"
                
                a_s = f"{a_t}" if a_t not in [1, -1] else ("-" if a_t == -1 else "")
                b_s = f"+ {b_t}x" if b_t >= 0 else f"- {abs(b_t)}x"
                curve_s = f"y = {a_s}x^2 {b_s} + {c_t}"
                
                q_tan = f"Determine the equation of the tangent to the curve ${curve_s}$ at the point where $x = {x0_t}$."
                d_tan = [
                    f"$y = {-m_t}x {c_tan_str}$",
                    f"$y = {m_str} {-c_tan if c_tan < 0 else f'+ {-c_tan}'}$",
                    f"$y = {m_t + 1}x {c_tan_str}$",
                    f"$y = {m_t - 1}x {c_tan_str}$",
                    f"$y = {m_str}$",
                    f"$y = {2*a_t}x + {y0_t}$",
                    f"$y = {m_str} + {y0_t}$"
                ]
                exp_tan = (f"Step 1: Calculate $y$-coordinate: $y_1 = {a_t}({x0_t})^2 + ({b_t})({x0_t}) + {c_t} = {y0_t}$. Point is $({x0_t}; {y0_t})$.\n"
                           f"Step 2: Calculate gradient $m = \\frac{{dy}}{{dx}} = {2*a_t}x + ({b_t})$. At $x = {x0_t}$: $m = {2*a_t}({x0_t}) + ({b_t}) = {m_t}$.\n"
                           f"Step 3: Equation: $y - y_1 = m(x - x_1) \\implies y - ({y0_t}) = {m_t}(x - ({x0_t})) \\implies {ans_tan}$.")
                add_q("Tangents to Curves", "medium", q_tan, ans_tan, d_tan, exp_tan)

    # 2c. Definite Integrals: int_a^b f(x) dx
    for p_di in [1, 2]:
        for k_di in [2, 3, 4, 6]:
            for lower in [0, 1, 2]:
                for upper in [lower + 1, lower + 2, lower + 3]:
                    val_upper = (k_di / (p_di + 1)) * (upper ** (p_di + 1))
                    val_lower = (k_di / (p_di + 1)) * (lower ** (p_di + 1))
                    res_def = round(val_upper - val_lower, 2)
                    
                    p_s = f"x^{{{p_di}}}" if p_di > 1 else "x"
                    q_def = f"Evaluate the definite integral: $\\int_{{{lower}}}^{{{upper}}} ({k_di}{p_s}) \\, dx$."
                    c_def = str(int(res_def)) if res_def.is_integer() else str(res_def)
                    d_def = [
                        str(round(res_def + 2, 2)),
                        str(round(res_def - 2 if res_def > 3 else res_def + 4, 2)),
                        str(round(res_def * 1.5, 2)),
                        str(round(res_def * 0.5, 2)),
                        str(round(k_di * (upper - lower), 2)),
                        str(round(val_upper, 2)),
                        str(round(res_def + 10, 2))
                    ]
                    exp_def = (f"Step 1: Find antiderivative: $F(x) = \\int {k_di}{p_s} \\, dx = \\frac{{{k_di}}}{{{p_di + 1}}}x^{{{p_di + 1}}}$.\n"
                               f"Step 2: Apply fundamental theorem of calculus: $[F(x)]_{{{lower}}}^{{{upper}}} = F({upper}) - F({lower}) "
                               f"= {val_upper} - {val_lower} = {c_def}$.")
                    add_q("Integration (Definite)", "medium", q_def, c_def, d_def, exp_def)

    # 2d. Kinematics: Velocity and Acceleration
    for a_kin in [-5, -4.9, -2]:
        for v0_kin in [20, 25, 30, 40, 50]:
            for t_eval in [1, 2, 3, 4]:
                v_res = round(2 * a_kin * t_eval + v0_kin, 2)
                acc_res = round(2 * a_kin, 2)
                
                q_kin = (f"The displacement of a mechanical piston is given by $s(t) = {a_kin}t^2 + {v0_kin}t$ (in metres). "
                         f"Calculate the instantaneous velocity of the piston at $t = {t_eval}$ seconds.")
                c_kin = f"{v_res} m/s"
                d_kin = [
                    f"{round(v_res + 10, 2)} m/s",
                    f"{round(v_res - 10, 2)} m/s",
                    f"{round(v0_kin, 2)} m/s",
                    f"{round(acc_res, 2)} m/s",
                    f"{round(a_kin * t_eval**2 + v0_kin * t_eval, 2)} m/s",
                    f"{round(v_res * 1.5, 2)} m/s",
                    f"{round(v_res * 0.5, 2)} m/s"
                ]
                exp_kin = (f"Velocity is the first derivative of displacement: $v(t) = s'(t) = \\frac{{ds}}{{dt}} = {2*a_kin}t + {v0_kin}$.\n"
                           f"At $t = {t_eval}\\text{{ s}}$: $v({t_eval}) = {2*a_kin}({t_eval}) + {v0_kin} = {v_res}\\text{{ m/s}}$.")
                add_q("Practical Applications of Calculus", "medium", q_kin, c_kin, d_kin, exp_kin)

    # 2e. Polynomial Integration: int (a*x^2 + b*x + c) dx
    for a_pi in [3, 6]:
        for b_pi in [-4, -2, 2, 4]:
            for c_pi in [1, 3, 5, 7]:
                # int (a_pi*x^2 + b_pi*x + c_pi) dx = (a_pi/3)*x^3 + (b_pi/2)*x^2 + c_pi*x + C
                term1 = f"{a_pi // 3}x^3" if (a_pi // 3) != 1 else "x^3"
                coef2 = b_pi // 2
                term2 = f"+ {coef2}x^2" if coef2 > 0 else f"- {abs(coef2)}x^2"
                term3 = f"+ {c_pi}x"
                ans_pi = f"${term1} {term2} {term3} + C$"
                
                b_sgn = f"+ {b_pi}x" if b_pi >= 0 else f"- {abs(b_pi)}x"
                q_pi = f"Determine the indefinite integral: $\\int ({a_pi}x^2 {b_sgn} + {c_pi}) \\, dx$."
                d_pi = [
                    f"${2*a_pi}x + {b_pi}$",
                    f"${term1} - {abs(coef2)}x^2 {term3} + C$" if coef2 > 0 else f"${term1} + {abs(coef2)}x^2 {term3} + C$",
                    f"${a_pi}x^3 {term2} {term3} + C$",
                    f"${term1} {term2} + {c_pi} + C$",
                    f"${term1} {term2} {term3}$",
                    f"${a_pi // 3}x^3 + {b_pi}x^2 + {c_pi}x + C$",
                    f"$\\frac{{{a_pi}}}{{2}}x^2 + {b_pi}x + C$"
                ]
                exp_pi = (f"Integrate term by term:\n"
                          f"$\\int {a_pi}x^2 \\, dx = \\frac{{{a_pi}}}{{3}}x^3 = {term1}$.\n"
                          f"$\\int {b_pi}x \\, dx = \\frac{{{b_pi}}}{{2}}x^2 = {term2}$.\n"
                          f"$\\int {c_pi} \\, dx = {c_pi}x$.\n"
                          f"Adding constant of integration $C$ gives {ans_pi}.")
                add_q("Integration (Indefinite)", "medium", q_pi, ans_pi, d_pi, exp_pi)

    # 2f. Stationary Points of Parabola via Calculus
    for a_sp in [-3, -2, -1, 1, 2, 3]:
        for b_sp in [-12, -8, -6, -4, 4, 6, 8, 12]:
            c_sp = 5
            # f'(x) = 2*a_sp*x + b_sp = 0 => x = -b_sp / (2*a_sp)
            x_sp = round(-b_sp / (2 * a_sp), 2)
            y_sp = round(a_sp * (x_sp ** 2) + b_sp * x_sp + c_sp, 2)
            
            a_s = f"{a_sp}" if a_sp not in [1, -1] else ("-" if a_sp == -1 else "")
            b_s = f"+ {b_sp}x" if b_sp >= 0 else f"- {abs(b_sp)}x"
            q_sp = f"Use differentiation to determine the coordinates of the stationary point of $f(x) = {a_s}x^2 {b_s} + {c_sp}$."
            c_sp_ans = f"$({x_sp}; {y_sp})$"
            d_sp = [
                f"$({-x_sp}; {y_sp})$",
                f"$({x_sp}; {-y_sp})$",
                f"$({-x_sp}; {-y_sp})$",
                f"$(0; {c_sp})$",
                f"$({y_sp}; {x_sp})$",
                f"$({2*x_sp}; {y_sp})$",
                f"$({x_sp}; 0)$"
            ]
            exp_sp = (f"Step 1: Set first derivative to zero: $f'(x) = {2*a_sp}x + ({b_sp}) = 0 \\implies x = {x_sp}$.\n"
                      f"Step 2: Substitute $x = {x_sp}$ into $f(x)$: $f({x_sp}) = {a_sp}({x_sp})^2 + ({b_sp})({x_sp}) + {c_sp} = {y_sp}$.\n"
                      f"Stationary point is $({x_sp}; {y_sp})$.")
            add_q("Rules of Differentiation", "medium", q_sp, c_sp_ans, d_sp, exp_sp)

    # 2g. Second Derivative Evaluation
    for a_sd in [1, 2, 3, 4]:
        for b_sd in [-6, -3, 3, 6]:
            for x_sd in [-2, -1, 1, 2, 3]:
                # f(x) = a_sd*x^3 + b_sd*x^2 => f'(x) = 3*a_sd*x^2 + 2*b_sd*x => f''(x) = 6*a_sd*x + 2*b_sd
                sd_val = 6 * a_sd * x_sd + 2 * b_sd
                b_s = f"+ {b_sd}x^2" if b_sd >= 0 else f"- {abs(b_sd)}x^2"
                a_s = f"{a_sd}" if a_sd != 1 else ""
                
                q_sd = f"Given $f(x) = {a_s}x^3 {b_s}$, calculate the value of the second derivative $f''({x_sd})$."
                c_sd = str(sd_val)
                d_sd = [
                    str(sd_val + 6), str(sd_val - 6), str(-sd_val),
                    str(sd_val * 2), str(3 * a_sd * x_sd**2 + 2 * b_sd * x_sd),
                    str(6 * a_sd * x_sd), str(2 * b_sd)
                ]
                exp_sd = (f"First derivative: $f'(x) = {3*a_sd}x^2 + ({2*b_sd})x$.\n"
                          f"Second derivative: $f''(x) = {6*a_sd}x + ({2*b_sd})$.\n"
                          f"At $x = {x_sd}$: $f''({x_sd}) = {6*a_sd}({x_sd}) + ({2*b_sd}) = {sd_val}$.")
                add_q("Rules of Differentiation", "medium", q_sd, c_sd, d_sd, exp_sd)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Area Between Curve and x-axis using Definite Integrals
    for r_area in [2, 3, 4, 5, 6, 7, 8]:
        r_sq = r_area ** 2
        area_exact = round((2 / 3) * (r_area ** 3), 2)
        
        q_area = (f"Calculate the area enclosed by the parabola $y = {r_sq} - x^2$ and the $x$-axis in the first quadrant "
                  f"(from $x = 0$ to the positive $x$-intercept). (Round to 2 decimal places).")
        c_area = f"{area_exact} square units"
        d_area = [
            f"{round(r_area**3, 2)} square units",
            f"{round(r_sq * r_area, 2)} square units",
            f"{round(area_exact * 2, 2)} square units",
            f"{round(area_exact / 2, 2)} square units",
            f"{round(area_exact + 4.5, 2)} square units",
            f"{round(area_exact - 4.5 if area_exact > 6 else area_exact + 8, 2)} square units",
            f"{r_sq} square units"
        ]
        exp_area = (f"Step 1: Positive $x$-intercept occurs where ${r_sq} - x^2 = 0 \\implies x = {r_area}$.\n"
                    f"Step 2: Area $= \\int_0^{{{r_area}}} ({r_sq} - x^2) \\, dx = \\left[ {r_sq}x - \\frac{{x^3}}{{3}} \\right]_0^{{{r_area}}}$.\n"
                    f"Step 3: Evaluate limits: $\\left({r_sq}({r_area}) - \\frac{{{r_area}^3}}{{3}}\\right) - 0 "
                    f"= {r_area**3} - \\frac{{{r_area**3}}}{{3}} = \\frac{{2}}{3}({r_area**3}) = {area_exact}\\text{{ square units}}$.")
        add_q("Area under Curve & Definite Integrals", "hard", q_area, c_area, d_area, exp_area)

    # 3b. Engineering Optimization (Maximum Volume)
    for side in [12, 18, 24, 30, 36, 42, 48, 54, 60]:
        x_opt = side / 6
        max_vol = round(x_opt * ((side - 2 * x_opt) ** 2), 2)
        
        q_opt = (f"An open rectangular container is formed by cutting equal squares of side length $x$ cm from each corner "
                 f"of a square metal sheet of side {side} cm, and folding up the edges. "
                 f"Calculate the value of $x$ that maximizes the volume of the container.")
        c_opt = f"x = {round(x_opt, 2)} cm"
        d_opt = [
            f"x = {round(side / 4, 2)} cm",
            f"x = {round(side / 2, 2)} cm",
            f"x = {round(x_opt * 1.5, 2)} cm",
            f"x = {round(x_opt * 0.5, 2)} cm",
            f"x = {round(x_opt + 2, 2)} cm",
            f"x = {round(side / 8, 2)} cm",
            f"x = {side} cm"
        ]
        exp_opt = (f"Step 1: Volume function: $V(x) = x({side} - 2x)^2 = 4x^3 - {4*side}x^2 + {side**2}x$.\n"
                   f"Step 2: Differentiate and set to zero: $V'(x) = 12x^2 - {8*side}x + {side**2} = 0$.\n"
                   f"Factorising: $(2x - {side})(6x - {side}) = 0 \\implies x = \\frac{{{side}}}{{6}} = {round(x_opt, 2)}\\text{{ cm}}$.")
        add_q("Optimization Problems", "hard", q_opt, c_opt, d_opt, exp_opt)

    # 3c. Cubic Functions: Turning Points and Inflection Points
    for p_cb in [1, 2, 3, 4, 5, 6]:
        p3 = 3 * (p_cb ** 2)
        local_max = 2 * (p_cb ** 3)
        local_min = -2 * (p_cb ** 3)
        
        q_cb = (f"For the cubic function $f(x) = x^3 - {p3}x$, determine the coordinates of the local maximum turning point.")
        c_cb = f"$({-p_cb}; {local_max})$"
        d_cb = [
            f"$({p_cb}; {local_min})$",
            f"$(0; 0)$",
            f"$({-p_cb}; {-local_max})$",
            f"$({p_cb}; {local_max})$",
            f"$({-p_cb}; {p3})$",
            f"$(1; {1 - p3})$",
            f"$({p_cb * 2}; {8 * p_cb**3})$"
        ]
        exp_cb = (f"Step 1: $f'(x) = 3x^2 - {p3} = 0 \\implies 3(x^2 - {p_cb**2}) = 0 \\implies x = \\pm {p_cb}$.\n"
                  f"Step 2: Second derivative $f''(x) = 6x$. For $x = -{p_cb}$, $f''(-{p_cb}) = -{6*p_cb} < 0$, which is a local maximum.\n"
                  f"Step 3: $f(-{p_cb}) = (-{p_cb})^3 - {p3}(-{p_cb}) = {local_max}$. Local max is $({-p_cb}; {local_max})$.")
        add_q("Cubic Functions & Optimization", "hard", q_cb, c_cb, d_cb, exp_cb)

        q_infl = (f"Determine the coordinates of the point of inflection for the cubic function $f(x) = x^3 - {p3}x + 10$.")
        c_infl = "$(0; 10)$"
        d_infl = [
            f"$({p_cb}; {-local_min + 10})$",
            f"$({-p_cb}; {local_max + 10})$",
            "$(0; 0)$",
            "$(1; 10)$",
            "$(-1; 10)$",
            f"$(0; {p3})$",
            f"$({p_cb}; 10)$"
        ]
        exp_infl = (f"Step 1: Point of inflection occurs where $f''(x) = 0$.\n"
                    f"Step 2: $f'(x) = 3x^2 - {p3}$ and $f''(x) = 6x = 0 \\implies x = 0$.\n"
                    f"Step 3: $f(0) = 0^3 - {p3}(0) + 10 = 10$. Point of inflection is $(0; 10)$.")
        add_q("Cubic Functions & Optimization", "hard", q_infl, c_infl, d_infl, exp_infl)

    # 3d. Additional Integration: Definite Area Between Curve and Line
    for a_int in [1, 2, 3]:
        for b_int in [2, 3, 4, 5, 6]:
            val_exact = round((a_int / 3) * (b_int ** 3), 2)
            q_par_area = (f"Evaluate the total area under the curve $y = {a_int}x^2$ bounded by the $x$-axis, "
                          f"$x = 0$, and $x = {b_int}$. (Round to 2 decimal places).")
            c_par_area = f"{val_exact} square units"
            d_par_area = [
                f"{round(a_int * b_int**2, 2)} square units",
                f"{round(val_exact * 2, 2)} square units",
                f"{round(val_exact / 2, 2)} square units",
                f"{round(val_exact + 3.2, 2)} square units",
                f"{round(val_exact - 3.2 if val_exact > 4 else val_exact + 6, 2)} square units",
                f"{round(a_int * b_int, 2)} square units",
                f"{b_int**2} square units"
            ]
            exp_par_area = (f"Area $= \\int_0^{{{b_int}}} {a_int}x^2 \\, dx = \\left[ \\frac{{{a_int}x^3}}{{3}} \\right]_0^{{{b_int}}} "
                            f"= \\frac{{{a_int}({b_int}^3)}}{{3}} - 0 = {val_exact}\\text{{ square units}}$.")
            add_q("Area under Curve & Definite Integrals", "hard", q_par_area, c_par_area, d_par_area, exp_par_area)

    # 3e. Projectile Maximum Height and Airtime
    for v0_p in [20, 30, 40, 50, 60, 70, 80]:
        for g_p in [5, 10]:  # g = 10 m/s^2 => s(t) = - (g/2)*t^2 + v0*t = -g_p/2 * t^2 + v0*t
            # Let s(t) = -g_p * t^2 + v0_p * t
            # v(t) = -2*g_p*t + v0_p = 0 => t_max = v0_p / (2*g_p)
            t_max = round(v0_p / (2 * g_p), 2)
            s_max = round(-g_p * (t_max ** 2) + v0_p * t_max, 2)
            
            q_proj = (f"A rocket is fired vertically into the air such that its height in metres after $t$ seconds is given by "
                      f"$h(t) = -{g_p}t^2 + {v0_p}t$. Calculate the maximum height reached by the rocket.")
            c_proj = f"{s_max} m"
            d_proj = [
                f"{round(s_max * 1.5, 2)} m",
                f"{round(s_max * 0.5, 2)} m",
                f"{round(v0_p * t_max, 2)} m",
                f"{round(s_max + 15, 2)} m",
                f"{round(s_max - 15 if s_max > 20 else s_max + 25, 2)} m",
                f"{v0_p} m",
                f"{round(s_max * 2, 2)} m"
            ]
            exp_proj = (f"Step 1: Set velocity to zero to find time of maximum height: $v(t) = h'(t) = -{2*g_p}t + {v0_p} = 0 \\implies t = {t_max}\\text{{ s}}$.\n"
                        f"Step 2: Substitute $t = {t_max}$ into $h(t)$: $h({t_max}) = -{g_p}({t_max})^2 + {v0_p}({t_max}) = {s_max}\\text{{ m}}$.")
            add_q("Practical Applications of Calculus", "hard", q_proj, c_proj, d_proj, exp_proj)

    # 3f. Area Between Two Curves (Parabola and Line)
    # y = m*x and y = a*x^2
    for a_cv in [1, 2]:
        for m_cv in [2, 3, 4, 6]:
            # Intersection: a*x^2 = m*x => x = 0 or x = m/a
            x_int = m_cv / a_cv
            # Area = int_0^(m/a) (m*x - a*x^2) dx = [m/2 * x^2 - a/3 * x^3]_0^(m/a)
            # = (m/2)*(m/a)^2 - (a/3)*(m/a)^3 = m^3/(2a^2) - m^3/(3a^2) = m^3 / (6 a^2)
            area_2c = round((m_cv ** 3) / (6 * (a_cv ** 2)), 2)
            
            a_s = f"{a_cv}" if a_cv != 1 else ""
            q_2c = (f"Calculate the area enclosed between the line $y = {m_cv}x$ and the parabola $y = {a_s}x^2$. (Round to 2 decimal places).")
            c_2c = f"{area_2c} square units"
            d_2c = [
                f"{round(area_2c * 2, 2)} square units",
                f"{round(area_2c / 2, 2)} square units",
                f"{round(area_2c * 1.5, 2)} square units",
                f"{round(area_2c + 2.5, 2)} square units",
                f"{round(area_2c - 2.5 if area_2c > 3 else area_2c + 5, 2)} square units",
                f"{round(m_cv * x_int, 2)} square units",
                f"{round(x_int**2, 2)} square units"
            ]
            exp_2c = (f"Step 1: Find points of intersection: ${a_s}x^2 = {m_cv}x \\implies x({a_cv}x - {m_cv}) = 0 \\implies x = 0$ or $x = {round(x_int, 2)}$.\n"
                      f"Step 2: Area $= \\int_0^{{{round(x_int, 2)}}} ({m_cv}x - {a_s}x^2) \\, dx = \\left[ \\frac{{{m_cv}x^2}}{{2}} - \\frac{{{a_cv}x^3}}{{3}} \\right]_0^{{{round(x_int, 2)}}}$.\n"
                      f"Step 3: Evaluating at upper limit yields ${area_2c}\\text{{ square units}}$.")
            add_q("Area under Curve & Definite Integrals", "hard", q_2c, c_2c, d_2c, exp_2c)

    # 3g. Rate of Change of Volume of Cylindrical Tank
    # V = pi * r^2 * h
    for r_tank in [2, 3, 4, 5, 6, 8]:
        for dh_dt in [0.2, 0.4, 0.5, 0.8, 1.2]:
            # dV/dt = pi * r^2 * dh/dt
            r2 = r_tank ** 2
            dv_dt_coef = round(r2 * dh_dt, 2)
            ans_dv = f"{dv_dt_coef}\\pi m^3/min"
            
            q_rt = (f"Water is pumped into a cylindrical storage tank of constant radius $r = {r_tank}$ m. "
                    f"If the water level rises at a rate of $\\frac{{dh}}{{dt}} = {dh_dt}$ m/min, "
                    f"determine the rate of change of the volume of water $\\frac{{dV}}{{dt}}$ in terms of $\\pi$.")
            c_rt = ans_dv
            d_rt = [
                f"{round(dv_dt_coef * 2, 2)}\\pi m^3/min",
                f"{round(dv_dt_coef / 2, 2)}\\pi m^3/min",
                f"{round(r_tank * dh_dt, 2)}\\pi m^3/min",
                f"{round(dv_dt_coef + 5, 2)}\\pi m^3/min",
                f"{round(dv_dt_coef - 5 if dv_dt_coef > 6 else dv_dt_coef + 8, 2)}\\pi m^3/min",
                f"{r2}\\pi m^3/min",
                f"{dh_dt}\\pi m^3/min"
            ]
            exp_rt = (f"Formula for cylinder volume: $V = \\pi r^2 h = \\pi ({r_tank})^2 h = {r2}\\pi h$.\n"
                      f"Differentiating with respect to time $t$: $\\frac{{dV}}{{dt}} = {r2}\\pi \\frac{{dh}}{{dt}} "
                      f"= {r2}\\pi ({dh_dt}) = {dv_dt_coef}\\pi\\text{{ m}}^3/\\text{{min}}$.")
            add_q("Practical Applications of Calculus", "hard", q_rt, c_rt, d_rt, exp_rt)

    # 3h. Work Done as Definite Integral of Force (W = int F dx)
    for k_spring in [150, 200, 250, 300, 400, 500]:
        for dist_cm in [4, 6, 8, 10, 12, 15]:
            dist_m = dist_cm / 100
            # W = int_0^d k*x dx = 1/2 * k * d^2
            work_j = round(0.5 * k_spring * (dist_m ** 2), 2)
            
            q_work = (f"According to Hooke's Law, the restoring force of a spring is $F(x) = {k_spring}x$ (in N). "
                      f"Calculate the work done in stretching the spring from $x = 0$ to $x = {dist_m}$ m "
                      f"using the work integral $W = \\int_0^d F(x) \\, dx$.")
            c_work = f"{work_j} J"
            d_work = [
                f"{round(k_spring * dist_m, 2)} J",
                f"{round(work_j * 2, 2)} J",
                f"{round(work_j / 2, 2)} J",
                f"{round(work_j + 1.5, 2)} J",
                f"{round(work_j - 1.5 if work_j > 2 else work_j + 3, 2)} J",
                f"{round(k_spring * (dist_m**2), 2)} J",
                f"{k_spring} J"
            ]
            exp_work = (f"Apply the definite work integral: $W = \\int_0^{{{dist_m}}} {k_spring}x \\, dx "
                        f"= \\left[ \\frac{{{k_spring}x^2}}{{2}} \\right]_0^{{{dist_m}}} "
                        f"= \\frac{{{k_spring}}}{{2}}({dist_m})^2 = {work_j}\\text{{ J}}$.")
            add_q("Practical Applications of Calculus", "hard", q_work, c_work, d_work, exp_work)

    # 3i. Distance Travelled by Integrating Velocity Function
    for a_vel in [2, 3, 4]:
        for v0_v in [10, 15, 20, 25]:
            for t_end in [2, 3, 4, 5]:
                # s(T) = int_0^T (a_vel*t + v0_v) dt = a_vel/2 * T^2 + v0_v * T
                tot_dist = round((a_vel / 2) * (t_end ** 2) + v0_v * t_end, 2)
                
                q_dist = (f"The velocity of an electric locomotive is given by $v(t) = {a_vel}t + {v0_v}$ m/s. "
                          f"Calculate the total distance travelled from $t = 0$ to $t = {t_end}$ seconds "
                          f"by evaluating the definite integral $\\int_0^{{{t_end}}} v(t) \\, dt$.")
                c_dist = f"{tot_dist} m"
                d_dist = [
                    f"{round(a_vel * t_end + v0_v, 2)} m",
                    f"{round(tot_dist * 1.5, 2)} m",
                    f"{round(tot_dist * 0.5, 2)} m",
                    f"{round(tot_dist + 15, 2)} m",
                    f"{round(tot_dist - 15 if tot_dist > 20 else tot_dist + 25, 2)} m",
                    f"{round(a_vel * (t_end**2) + v0_v * t_end, 2)} m",
                    f"{round(v0_v * t_end, 2)} m"
                ]
                exp_dist = (f"Distance is the integral of velocity: $s = \\int_0^{{{t_end}}} ({a_vel}t + {v0_v}) \\, dt "
                            f"= \\left[ \\frac{{{a_vel}t^2}}{{2}} + {v0_v}t \\right]_0^{{{t_end}}} "
                            f"= \\frac{{{a_vel}({t_end}^2)}}{{2}} + {v0_v}({t_end}) = {tot_dist}\\text{{ m}}$.")
                add_q("Practical Applications of Calculus", "hard", q_dist, c_dist, d_dist, exp_dist)

    # 3j. Tangent to Cubic Curve at Point of Inflection
    for p_ti in [1, 2, 3, 4, 5]:
        for c_ti in [-8, -5, -2, 2, 5, 8, 12, 15]:
            # f(x) = x^3 - 3*p^2*x + c_ti
            # inflection at x = 0, y = c_ti
            # f'(0) = -3*p^2
            # tangent: y - c_ti = -3*p^2*(x - 0) => y = -3*p^2*x + c_ti
            p3 = 3 * (p_ti ** 2)
            c_ti_s = f"+ {c_ti}" if c_ti >= 0 else f"- {abs(c_ti)}"
            ans_ti = f"$y = -{p3}x {c_ti_s}$"
            
            q_ti = (f"Determine the equation of the tangent line to the cubic function $f(x) = x^3 - {p3}x {c_ti_s}$ "
                    f"at its point of inflection.")
            d_ti = [
                f"$y = {p3}x {c_ti_s}$",
                f"$y = -{p3}x {-c_ti if c_ti < 0 else f'+ {-c_ti}'}$",
                f"$y = -{p3}x$",
                f"$y = {c_ti}$",
                f"$y = -{p3 + 2}x {c_ti_s}$",
                f"$y = 3x^2 - {p3}$",
                f"$y = -{p3}x + {p_ti}$"
            ]
            exp_ti = (f"Step 1: Point of inflection: $f''(x) = 6x = 0 \\implies x = 0$. $y = f(0) = {c_ti}$. Point is $(0; {c_ti})$.\n"
                      f"Step 2: Gradient at $x = 0$: $m = f'(0) = 3(0)^2 - {p3} = -{p3}$.\n"
                      f"Step 3: Tangent line equation: $y - {c_ti} = -{p3}(x - 0) \\implies {ans_ti}$.")
            add_q("Cubic Functions & Optimization", "hard", q_ti, ans_ti, d_ti, exp_ti)

    print(f"Generated Tech Math Calculus: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper1_tech_calculus.json")
    dataset = build_calculus_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
