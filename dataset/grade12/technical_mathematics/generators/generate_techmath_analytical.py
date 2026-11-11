import json
import os
import random
import math
import time

def build_analytical_dataset():
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
        q_id = f"TM12_P2_ANA_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Analytical Geometry",
            "subtopic": subtopic,
            "paper": "paper2",
            "difficulty": difficulty,
            "question": q_text,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_dist[:8],
            "explanation": explanation,
            "tags": {
                "grade": "12",
                "subject": "Technical Mathematics",
                "topic": "Analytical Geometry",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Distance between two points (Pythagorean triples)
    pyth_triples = [
        (3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25),
        (9, 12, 15), (12, 16, 20), (15, 20, 25), (10, 24, 26)
    ]
    for dx, dy, dist in pyth_triples:
        for x1 in [-8, -4, -1, 0, 2, 5, 8]:
            for y1 in [-6, -2, 1, 3, 7]:
                for sgn_x, sgn_y in [(1, 1), (1, -1), (-1, 1)]:
                    x2 = x1 + dx * sgn_x
                    y2 = y1 + dy * sgn_y
                    
                    q_dist = f"Calculate the distance between the points $A({x1}; {y1})$ and $B({x2}; {y2})$."
                    c_dist = str(dist)
                    d_dist = [
                        str(dist + 2), str(dist - 2 if dist > 3 else dist + 4),
                        str(dist**2), str(round(math.sqrt(dist), 2)),
                        str(abs(x2 - x1) + abs(y2 - y1)), str(dist + 5), str(dist * 2)
                    ]
                    exp_dist = (f"Use the distance formula: $d = \\sqrt{{(x_2 - x_1)^2 + (y_2 - y_1)^2}}$\n"
                                f"$d = \\sqrt{{({x2} - ({x1}))^2 + ({y2} - ({y1}))^2}} = \\sqrt{{{dx**2} + {dy**2}}} = \\sqrt{{{dist**2}}} = {dist}$.")
                    add_q("Distance & Midpoint", "easy", q_dist, c_dist, d_dist, exp_dist)

    # 1b. Midpoint of Segment
    for x1_m in range(-8, 9, 2):
        for y1_m in range(-6, 7, 2):
            for x2_m in [-6, -2, 2, 6]:
                y2_m = 4
                xm = (x1_m + x2_m) // 2
                ym = (y1_m + y2_m) // 2
                
                q_mid = f"Determine the midpoint of the line segment joining $P({x1_m}; {y1_m})$ and $Q({x2_m}; {y2_m})$."
                c_mid = f"$({xm}; {ym})$"
                d_mid = [
                    f"$({-xm}; {ym})$", f"$({xm}; {-ym})$", f"$({-xm}; {-ym})$",
                    f"$({ym}; {xm})$", f"$({x1_m + x2_m}; {y1_m + y2_m})$",
                    f"$({xm + 1}; {ym - 1})$", f"$(0; 0)$"
                ]
                exp_mid = (f"Use midpoint formula: $M = \\left( \\frac{{x_1 + x_2}}{{2}}; \\frac{{y_1 + y_2}}{{2}} \\right) "
                           f"= \\left( \\frac{{{x1_m} + ({x2_m})}}{{2}}; \\frac{{{y1_m} + ({y2_m})}}{{2}} \\right) = ({xm}; {ym})$.")
                add_q("Distance & Midpoint", "easy", q_mid, c_mid, d_mid, exp_mid)

    # 1c. Ellipse Semi-axes from Standard Form x^2 / a^2 + y^2 / b^2 = 1
    for a_val in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for b_val in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if a_val == b_val: continue
            a2 = a_val ** 2
            b2 = b_val ** 2
            
            q_el_x = f"Determine the length of the major axis of the ellipse $\\frac{{x^2}}{{{a2}}} + \\frac{{y^2}}{{{b2}}} = 1$."
            major_len = 2 * max(a_val, b_val)
            c_el_x = str(major_len)
            d_el_x = [
                str(max(a_val, b_val)), str(2 * min(a_val, b_val)), str(min(a_val, b_val)),
                str(max(a2, b2)), str(major_len + 4), str(major_len - 2), str(a_val + b_val)
            ]
            exp_el_x = (f"The semi-major axis is $a = \\sqrt{{{max(a2, b2)}}} = {max(a_val, b_val)}$. "
                        f"The total length of the major axis is $2a = 2({max(a_val, b_val)}) = {major_len}$.")
            add_q("Ellipses (Standard Form)", "easy", q_el_x, c_el_x, d_el_x, exp_el_x)

            q_el_y = f"Determine the $y$-intercepts of the ellipse $\\frac{{x^2}}{{{a2}}} + \\frac{{y^2}}{{{b2}}} = 1$."
            c_el_y = f"$(0; {b_val})$ and $(0; {-b_val})$"
            d_el_y = [
                f"$({a_val}; 0)$ and $({-a_val}; 0)$",
                f"$(0; {b2})$ and $(0; {-b2})$",
                f"$(0; {b_val})$ only",
                f"$(0; {b_val + 2})$ and $(0; {-b_val - 2})$",
                f"$({b_val}; 0)$ and $({-b_val}; 0)$",
                f"$(0; {round(math.sqrt(b_val), 2)})$ and $(0; {-round(math.sqrt(b_val), 2)})$",
                f"$(0; 1)$ and $(0; -1)$"
            ]
            exp_el_y = f"Set $x = 0$: $\\frac{{0}}{{a^2}} + \\frac{{y^2}}{{{b2}}} = 1 \\implies y^2 = {b2} \\implies y = \\pm {b_val}$. Intercepts are $(0; {b_val})$ and $(0; {-b_val})$."
            add_q("Ellipses (Standard Form)", "easy", q_el_y, c_el_y, d_el_y, exp_el_y)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Angle of Inclination: tan theta = m
    # Acute angles (m > 0) and Obtuse angles (m < 0)
    angle_cases = [
        (1, 45.0), (math.sqrt(3), 60.0), (1 / math.sqrt(3), 30.0),
        (0.5, 26.57), (0.75, 36.87), (1.5, 56.31), (2.0, 63.43),
        (2.5, 68.20), (3.0, 71.57), (4.0, 75.96)
    ]
    for m_val, theta_deg in angle_cases:
        # Acute angle
        m_r = round(m_val, 2)
        q_inc_ac = f"Calculate the angle of inclination $\\theta$ of a straight line with gradient $m = {m_r}$. (Round to 2 decimal places)."
        c_inc_ac = f"{theta_deg}^\\circ"
        d_inc_ac = [
            f"{round(180 - theta_deg, 2)}^\\circ",
            f"{round(90 - theta_deg, 2)}^\\circ",
            f"{round(theta_deg + 10, 2)}^\\circ",
            f"{round(theta_deg - 10, 2)}^\\circ",
            f"{round(theta_deg * 1.5, 2)}^\\circ",
            f"{round(theta_deg / 2, 2)}^\\circ",
            f"{m_r}^\\circ"
        ]
        exp_inc_ac = f"Use $\\tan \\theta = m$: $\\tan \\theta = {m_r} \\implies \\theta = \\arctan({m_r}) = {theta_deg}^\\circ$."
        add_q("Gradient & Angle of Inclination", "medium", q_inc_ac, c_inc_ac, d_inc_ac, exp_inc_ac)

        # Obtuse angle (m < 0)
        m_neg = -m_r
        obtuse_deg = round(180.0 - theta_deg, 2)
        q_inc_ob = f"Calculate the angle of inclination $\\theta$ of a straight line with negative gradient $m = {m_neg}$. (Round to 2 decimal places)."
        c_inc_ob = f"{obtuse_deg}^\\circ"
        d_inc_ob = [
            f"{theta_deg}^\\circ",
            f"{round(90 + theta_deg, 2)}^\\circ",
            f"{round(obtuse_deg - 10, 2)}^\\circ",
            f"{round(obtuse_deg + 10, 2)}^\\circ",
            f"{round(180 + theta_deg, 2)}^\\circ",
            f"{round(obtuse_deg * 0.9, 2)}^\\circ",
            f"{-theta_deg}^\\circ"
        ]
        exp_inc_ob = (f"Since $m < 0$, the angle is obtuse: $\\theta = 180^\\circ - \\arctan(|{m_neg}|) "
                      f"= 180^\\circ - {theta_deg}^\\circ = {obtuse_deg}^\\circ$.")
        add_q("Gradient & Angle of Inclination", "medium", q_inc_ob, c_inc_ob, d_inc_ob, exp_inc_ob)

    # 2b. Equation of Tangent to Circle Centred at Origin: x^2 + y^2 = r^2 at (x1, y1)
    for a_t, b_t, r_t in [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17)]:
        for sgn_x, sgn_y in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x1 = a_t * sgn_x
            y1 = b_t * sgn_y
            r2 = r_t ** 2
            # Radius gradient: m_rad = y1 / x1
            # Tangent gradient: m_tan = -x1 / y1
            # Tangent equation: x1*x + y1*y = r2 => y = (-x1/y1)*x + r2/y1
            m_tan_val = round(-x1 / y1, 2)
            c_tan_val = round(r2 / y1, 2)
            
            sgn_ctan = f"+ {c_tan_val}" if c_tan_val >= 0 else f"- {abs(c_tan_val)}"
            ans_tan = f"$y = {m_tan_val}x {sgn_ctan}$"
            
            q_tan_c = (f"Determine the equation of the tangent to the circle $x^2 + y^2 = {r2}$ "
                       f"at the point $T({x1}; {y1})$. (Round values to 2 decimal places).")
            d_tan_c = [
                f"$y = {-m_tan_val}x {sgn_ctan}$",
                f"$y = {round(y1/x1, 2)}x {sgn_ctan}$",
                f"$y = {m_tan_val}x {-c_tan_val if c_tan_val < 0 else f'+ {-c_tan_val}'}$",
                f"$y = {round(x1/y1, 2)}x + {r_t}$",
                f"$y = {m_tan_val}x$",
                f"$y = x + {r2}$",
                f"$y = {m_tan_val * 2}x {sgn_ctan}$"
            ]
            exp_tan_c = (f"Step 1: Gradient of radius $OT$: $m_{{OT}} = \\frac{{{y1} - 0}}{{{x1} - 0}} = \\frac{{{y1}}}{{{x1}}}$.\n"
                         f"Step 2: Tangent is perpendicular to radius: $m_{{\\text{{tan}}}} = -\\frac{{1}}{{m_{{OT}}}} = -\\frac{{{x1}}}{{{y1}}} = {m_tan_val}$.\n"
                         f"Step 3: Equation: $y - ({y1}) = {m_tan_val}(x - ({x1})) \\implies {ans_tan}$.")
            add_q("Equation of a Circle & Tangents", "medium", q_tan_c, ans_tan, d_tan_c, exp_tan_c)

    # 2c. Circle Centred at (a, b): (x - a)^2 + (y - b)^2 = r^2
    for a_c in [-4, -2, 1, 3, 5]:
        for b_c in [-5, -1, 2, 4]:
            for r_c in [3, 4, 5, 6, 7]:
                r2_c = r_c ** 2
                a_s = f"- {a_c}" if a_c > 0 else f"+ {abs(a_c)}" if a_c < 0 else ""
                b_s = f"- {b_c}" if b_c > 0 else f"+ {abs(b_c)}" if b_c < 0 else ""
                brk_x = f"(x {a_s})" if a_c != 0 else "x"
                brk_y = f"(y {b_s})" if b_c != 0 else "y"
                eq_circ = f"{brk_x}^2 + {brk_y}^2 = {r2_c}"
                
                q_cc = f"Determine the coordinates of the centre and radius of the circle ${eq_circ}$."
                c_cc = f"Centre $({a_c}; {b_c})$, Radius $r = {r_c}$"
                d_cc = [
                    f"Centre $({-a_c}; {b_c})$, Radius $r = {r_c}$",
                    f"Centre $({a_c}; {-b_c})$, Radius $r = {r_c}$",
                    f"Centre $({-a_c}; {-b_c})$, Radius $r = {r_c}$",
                    f"Centre $({a_c}; {b_c})$, Radius $r = {r2_c}$",
                    f"Centre $({b_c}; {a_c})$, Radius $r = {r_c}$",
                    f"Centre $(0; 0)$, Radius $r = {r_c}$",
                    f"Centre $({a_c}; {b_c})$, Radius $r = {r_c * 2}$"
                ]
                exp_cc = (f"Compare with standard form $(x - a)^2 + (y - b)^2 = r^2$:\n"
                          f"Centre is $(a; b) = ({a_c}; {b_c})$ and radius is $r = \\sqrt{{{r2_c}}} = {r_c}$.")
                add_q("Equation of a Circle & Tangents", "medium", q_cc, c_cc, d_cc, exp_cc)

    # 2d. Determining Equation of Ellipse from Intercepts
    for a_el in [3, 4, 5, 6, 7]:
        for b_el in [2, 3, 5, 8]:
            if a_el == b_el: continue
            a2 = a_el ** 2
            b2 = b_el ** 2
            ans_el = f"$\\frac{{x^2}}{{{a2}}} + \\frac{{y^2}}{{{b2}}} = 1$"
            
            q_eq_el = (f"An ellipse centered at the origin has $x$-intercepts at $(\\pm {a_el}; 0)$ and "
                       f"$y$-intercepts at $(0; \\pm {b_el})$. Determine its equation in standard form.")
            d_eq_el = [
                f"$\\frac{{x^2}}{{{b2}}} + \\frac{{y^2}}{{{a2}}} = 1$",
                f"$\\frac{{x^2}}{{{a_el}}} + \\frac{{y^2}}{{{b_el}}} = 1$",
                f"${a2}x^2 + {b2}y^2 = 1$",
                f"$\\frac{{x^2}}{{{a2}}} - \\frac{{y^2}}{{{b2}}} = 1$",
                f"$\\frac{{x^2}}{{{a2 + b2}}} + \\frac{{y^2}}{{{a2 * b2}}} = 1$",
                f"$x^2 + y^2 = {a2}$",
                f"$\\frac{{x^2}}{{{2*a_el}}} + \\frac{{y^2}}{{{2*b_el}}} = 1$"
            ]
            exp_el = (f"Standard form of an ellipse: $\\frac{{x^2}}{{a^2}} + \\frac{{y^2}}{{b^2}} = 1$.\n"
                      f"Given $x$-intercepts $\\pm {a_el} \\implies a = {a_el} \\implies a^2 = {a2}$.\n"
                      f"Given $y$-intercepts $\\pm {b_el} \\implies b = {b_el} \\implies b^2 = {b2}$.\n"
                      f"Equation: {ans_el}.")
            add_q("Ellipses (Standard Form)", "medium", q_eq_el, ans_el, d_eq_el, exp_el)

    # 2e. Gradient Formula Between Two Points
    for x1_g in [-6, -4, -2, 1, 3, 5]:
        for y1_g in [-5, -2, 0, 3, 6]:
            for dx_g in [-5, -4, -3, -2, 2, 3, 4, 5]:
                for dy_g in [-6, -4, -2, 2, 4, 6]:
                    x2_g = x1_g + dx_g
                    y2_g = y1_g + dy_g
                    m_exact = round(dy_g / dx_g, 2)
                    c_grad = str(int(m_exact)) if m_exact.is_integer() else str(m_exact)
                    
                    q_grad = f"Calculate the gradient $m$ of the line segment joining $A({x1_g}; {y1_g})$ and $B({x2_g}; {y2_g})$."
                    d_grad = [
                        str(-m_exact),
                        str(round(dx_g / dy_g, 2)),
                        str(round(m_exact + 1, 2)),
                        str(round(m_exact - 1, 2)),
                        str(round(m_exact * 2, 2)),
                        str(dy_g),
                        str(dx_g)
                    ]
                    exp_grad = (f"Gradient formula: $m = \\frac{{y_2 - y_1}}{{x_2 - x_1}} = \\frac{{{y2_g} - ({y1_g})}}{{{x2_g} - ({x1_g})}} "
                                f"= \\frac{{{dy_g}}}{{{dx_g}}} = {c_grad}$.")
                    add_q("Gradient & Angle of Inclination", "medium", q_grad, c_grad, d_grad, exp_grad)

    # 2f. Equation of Straight Line: y - y1 = m(x - x1)
    for m_line in [-3, -2, -1, 1, 2, 3]:
        for x1_l in [-4, -2, 0, 1, 3, 5]:
            for y1_l in [-5, -1, 2, 4, 7]:
                c_line = y1_l - m_line * x1_l
                m_str = f"{m_line}x" if m_line != 1 else "x"
                if m_line == -1: m_str = "-x"
                c_str = f"+ {c_line}" if c_line >= 0 else f"- {abs(c_line)}"
                ans_line = f"$y = {m_str} {c_str}$"
                
                q_line = (f"Determine the equation of the straight line with gradient $m = {m_line}$ "
                          f"passing through the point $P({x1_l}; {y1_l})$.")
                d_line = [
                    f"$y = {-m_line}x {c_str}$",
                    f"$y = {m_str} {-c_line if c_line < 0 else f'+ {-c_line}'}$",
                    f"$y = {m_line + 1}x {c_str}$",
                    f"$y = {m_str}$",
                    f"$y = {m_str} + {y1_l}$",
                    f"$y = x + {c_line}$",
                    f"$y = {2*m_line}x {c_str}$"
                ]
                exp_line = (f"Use the point-gradient formula: $y - y_1 = m(x - x_1)$\n"
                            f"$y - ({y1_l}) = {m_line}(x - ({x1_l})) \\implies y = {m_line}x - ({m_line * x1_l}) + ({y1_l}) \\implies {ans_line}$.")
                add_q("Gradient & Angle of Inclination", "medium", q_line, ans_line, d_line, exp_line)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Parallelogram Fourth Vertex via Midpoints
    for xA, yA in [(-2, 3), (1, 4), (-3, 1), (0, 5), (2, -1)]:
        for xB, yB in [(4, 5), (6, 2), (5, 6), (3, 7)]:
            for xC, yC in [(6, 1), (8, -2), (7, 2), (5, 0)]:
                # In parallelogram ABCD, diagonals AC and BD bisect each other:
                # M_AC = ((xA + xC)/2, (yA + yC)/2) = ((xB + xD)/2, (yB + yD)/2)
                # => xD = xA + xC - xB; yD = yA + yC - yB
                xD = xA + xC - xB
                yD = yA + yC - yB
                
                q_pgram = (f"Points $A({xA}; {yA})$, $B({xB}; {yB})$, and $C({xC}; {yC})$ are three consecutive vertices "
                           f"of parallelogram $ABCD$. Determine the coordinates of vertex $D$.")
                c_pgram = f"$({xD}; {yD})$"
                d_pgram = [
                    f"$({-xD}; {yD})$", f"$({xD}; {-yD})$", f"$({yD}; {xD})$",
                    f"$({xD + 2}; {yD - 2})$", f"$({xA + xB - xC}; {yA + yB - yC})$",
                    f"$({xB + xC - xA}; {yB + yC - yA})$", f"$(0; 0)$"
                ]
                exp_pgram = (f"The diagonals of a parallelogram bisect each other, so midpoint of $AC$ = midpoint of $BD$:\n"
                             f"$\\left(\\frac{{{xA} + {xC}}}{{2}}; \\frac{{{yA} + {yC}}}{{2}}\\right) = \\left(\\frac{{{xB} + x_D}}{{2}}; \\frac{{{yB} + y_D}}{{2}}\\right)$.\n"
                             f"$x_D = {xA} + {xC} - {xB} = {xD}$. $y_D = {yA} + {yC} - {yB} = {yD}$. Vertex $D$ is $({xD}; {yD})$." )
                add_q("Properties of Quadrilaterals", "hard", q_pgram, c_pgram, d_pgram, exp_pgram)

    # 3b. Tangent to Circle Not Centred at Origin: (x - a)^2 + (y - b)^2 = r^2
    for a_tc, b_tc in [(1, 2), (2, -1), (-2, 3), (3, 1), (-1, -2)]:
        for dx, dy, r_val in [(3, 4, 5), (4, 3, 5), (-3, 4, 5), (4, -3, 5)]:
            x1 = a_tc + dx
            y1 = b_tc + dy
            r2 = r_val ** 2
            
            # Radius gradient: m_rad = (y1 - b_tc) / (x1 - a_tc) = dy / dx
            # Tangent gradient: m_tan = -dx / dy
            m_tan_val = round(-dx / dy, 2)
            c_tan_val = round(y1 - m_tan_val * x1, 2)
            sgn_c = f"+ {c_tan_val}" if c_tan_val >= 0 else f"- {abs(c_tan_val)}"
            ans_tanc = f"$y = {m_tan_val}x {sgn_c}$"
            
            a_s = f"- {a_tc}" if a_tc > 0 else f"+ {abs(a_tc)}"
            b_s = f"- {b_tc}" if b_tc > 0 else f"+ {abs(b_tc)}"
            q_tanc = (f"Determine the equation of the tangent line to the circle $(x {a_s})^2 + (y {b_s})^2 = {r2}$ "
                      f"at the point of contact $P({x1}; {y1})$. (Round values to 2 decimal places).")
            d_tanc = [
                f"$y = {-m_tan_val}x {sgn_c}$",
                f"$y = {round(dy/dx, 2)}x {sgn_c}$",
                f"$y = {m_tan_val}x {-c_tan_val if c_tan_val < 0 else f'+ {-c_tan_val}'}$",
                f"$y = {round(-dy/dx, 2)}x + {r_val}$",
                f"$y = {m_tan_val}x$",
                f"$y = {m_tan_val * 2}x {sgn_c}$",
                f"$y = x + {r2}$"
            ]
            exp_tanc = (f"Step 1: Centre is $C({a_tc}; {b_tc})$. Gradient of radius $CP$: $m_{{CP}} = \\frac{{{y1} - ({b_tc})}}{{{x1} - ({a_tc})}} = \\frac{{{dy}}}{{{dx}}}$.\n"
                        f"Step 2: Gradient of tangent: $m_{{\\text{{tan}}}} = -\\frac{{{dx}}}{{{dy}}} = {m_tan_val}$.\n"
                        f"Step 3: Equation of tangent: $y - ({y1}) = {m_tan_val}(x - ({x1})) \\implies {ans_tanc}$.")
            add_q("Equation of a Circle & Tangents", "hard", q_tanc, ans_tanc, d_tanc, exp_tanc)

    # 3c. Line Intersecting Ellipse at Standard Coordinates
    for a_ie in [4, 5, 6]:
        for b_ie in [3, 4, 5]:
            if a_ie == b_ie: continue
            a2 = a_ie ** 2
            b2 = b_ie ** 2
            # Let x0 = a_ie * 0.6 => x0^2/a^2 = 0.36 => y0^2/b^2 = 0.64 => y0 = b_ie * 0.8
            x0 = round(a_ie * 0.6, 2)
            y0 = round(b_ie * 0.8, 2)
            
            q_pte = (f"Verify if the point $K({x0}; {y0})$ lies on the ellipse $\\frac{{x^2}}{{{a2}}} + \\frac{{y^2}}{{{b2}}} = 1$. "
                     f"What is the value of $\\frac{{({x0})^2}}{{{a2}}} + \\frac{{({y0})^2}}{{{b2}}}$?")
            c_pte = "1.00 (The point lies on the ellipse)"
            d_pte = [
                "0.64 (The point lies inside the ellipse)",
                "1.36 (The point lies outside the ellipse)",
                "0.50 (The point lies inside the ellipse)",
                "2.00 (The point lies outside the ellipse)",
                "0.00 (The point is at the centre)",
                "1.50 (The point lies outside the ellipse)",
                "0.80 (The point lies inside the ellipse)"
            ]
            exp_pte = (f"Substitute $({x0}; {y0})$ into the left-hand side:\n"
                       f"$\\frac{{({x0})^2}}{{{a2}}} + \\frac{{({y0})^2}}{{{b2}}} = \\frac{{{round(x0**2, 2)}}}{{{a2}}} + \\frac{{{round(y0**2, 2)}}}{{{b2}}} "
                       f"= 0.36 + 0.64 = 1.00$.\n"
                       f"Since $\\text{{LHS}} = \\text{{RHS}} = 1$, the point lies exactly on the ellipse.")
            add_q("Ellipses (Standard Form)", "hard", q_pte, c_pte, d_pte, exp_pte)

    # 3d. Length of Perpendicular Altitude in a Triangle
    for x1_t, y1_t in [(-2, 0), (0, 0), (2, 0)]:
        for x2_t, y2_t in [(4, 0), (6, 0), (8, 0)]:
            for x3_t, y3_t in [(1, 5), (2, 6), (3, 7), (4, 8), (2, 4)]:
                # Base is on y = 0 from (x1_t, 0) to (x2_t, 0), base length = x2_t - x1_t
                # Altitude height is y3_t
                base_len = x2_t - x1_t
                area_tri = round(0.5 * base_len * y3_t, 2)
                
                q_tri = (f"A triangular roof truss has vertices at $A({x1_t}; {y1_t})$, $B({x2_t}; {y2_t})$, and $C({x3_t}; {y3_t})$. "
                         f"Calculate the area of $\\triangle ABC$.")
                c_tri = f"{area_tri} square units"
                d_tri = [
                    f"{round(area_tri * 2, 2)} square units",
                    f"{round(area_tri / 2, 2)} square units",
                    f"{round(base_len * y3_t, 2)} square units",
                    f"{round(area_tri + 4.5, 2)} square units",
                    f"{round(area_tri - 4.5 if area_tri > 5 else area_tri + 8, 2)} square units",
                    f"{base_len} square units",
                    f"{y3_t} square units"
                ]
                exp_tri = (f"Base $AB$ lies on the horizontal axis with length $d = {x2_t} - ({x1_t}) = {base_len}$.\n"
                           f"The perpendicular height from vertex $C$ to base $AB$ is $h = |{y3_t} - 0| = {y3_t}$.\n"
                           f"Area $= \\frac{{1}}{{2}} \\times \\text{{base}} \\times \\text{{height}} = \\frac{{1}}{{2}}({base_len})({y3_t}) = {area_tri}\\text{{ square units}}$.")
                add_q("Properties of Quadrilaterals", "hard", q_tri, c_tri, d_tri, exp_tri)

    # 3e. Collinear Points with Unknown Parameter k
    for m_col in [-2, -1, 1, 2, 3]:
        for x1_c, y1_c in [(-2, 1), (0, 3), (1, -1), (2, 4), (-3, 0)]:
            for dx1 in [2, 3, 4]:
                for dx2 in [2, 3]:
                    x2_c = x1_c + dx1
                    y2_c = y1_c + m_col * dx1
                    x3_c = x2_c + dx2
                    k_val = y2_c + m_col * dx2
                    
                    q_col = (f"Points $A({x1_c}; {y1_c})$, $B({x2_c}; {y2_c})$, and $C({x3_c}; k)$ are collinear. "
                             f"Calculate the value of the unknown coordinate $k$.")
                    c_col = str(k_val)
                    d_col = [
                        str(-k_val),
                        str(k_val + 2),
                        str(k_val - 2),
                        str(k_val + dx2),
                        str(y2_c),
                        str(y1_c),
                        str(k_val * 2)
                    ]
                    exp_col = (f"For collinear points, gradient $m_{{AB}} = m_{{BC}}$:\n"
                               f"$m_{{AB}} = \\frac{{{y2_c} - ({y1_c})}}{{{x2_c} - ({x1_c})}} = {m_col}$.\n"
                               f"Then $\\frac{{k - ({y2_c})}}{{{x3_c} - ({x2_c})}} = {m_col} \\implies k - ({y2_c}) = {m_col}({dx2}) = {m_col * dx2} \\implies k = {k_val}$.")
                    add_q("Gradient & Angle of Inclination", "hard", q_col, c_col, d_col, exp_col)

    # 3f. Perpendicular Bisector of Line Segment
    for xA_pb in [-4, -2, 0, 2]:
        for yA_pb in [-3, -1, 1, 3]:
            for dx_pb in [2, 4]:
                for dy_pb in [2, 4]:
                    xB_pb = xA_pb + dx_pb
                    yB_pb = yA_pb + dy_pb
                    # Midpoint M
                    xM = (xA_pb + xB_pb) // 2
                    yM = (yA_pb + yB_pb) // 2
                    # m_AB = dy / dx
                    m_ab = dy_pb / dx_pb
                    # m_perp = -1 / m_ab = -dx / dy
                    m_perp = round(-dx_pb / dy_pb, 2)
                    c_perp = round(yM - m_perp * xM, 2)
                    
                    m_str = f"{m_perp}x" if m_perp != 1 else "x"
                    c_str = f"+ {c_perp}" if c_perp >= 0 else f"- {abs(c_perp)}"
                    ans_pb = f"$y = {m_str} {c_str}$"
                    
                    q_pb = (f"Determine the equation of the perpendicular bisector of the line segment joining "
                            f"$A({xA_pb}; {yA_pb})$ and $B({xB_pb}; {yB_pb})$.")
                    d_pb = [
                        f"$y = {-m_perp}x {c_str}$",
                        f"$y = {m_str} {-c_perp if c_perp < 0 else f'+ {-c_perp}'}$",
                        f"$y = {round(m_ab, 2)}x + {yM}$",
                        f"$y = {m_str}$",
                        f"$y = {m_perp + 1}x {c_str}$",
                        f"$y = -x + {c_perp}$",
                        f"$y = x + {yM}$"
                    ]
                    exp_pb = (f"Step 1: Calculate midpoint: $M = \\left(\\frac{{{xA_pb} + {xB_pb}}}{{2}}; \\frac{{{yA_pb} + {yB_pb}}}{{2}}\\right) = ({xM}; {yM})$.\n"
                              f"Step 2: Gradient $m_{{AB}} = \\frac{{{yB_pb} - ({yA_pb})}}{{{xB_pb} - ({xA_pb})}} = \\frac{{{dy_pb}}}{{{dx_pb}}} = {m_ab}$.\n"
                              f"Step 3: Perpendicular gradient $m_{{\\perp}} = -\\frac{{1}}{{{m_ab}}} = {m_perp}$.\n"
                              f"Step 4: Equation: $y - {yM} = {m_perp}(x - {xM}) \\implies {ans_pb}$.")
                    add_q("Gradient & Angle of Inclination", "hard", q_pb, ans_pb, d_pb, exp_pb)

    print(f"Generated Tech Math Analytical: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper2_tech_analytical.json")
    dataset = build_analytical_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
