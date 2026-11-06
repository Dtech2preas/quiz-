import json
import random
import os
import time
import math

def generate_math_analytical():
    print("Generating Grade 12 Mathematics: Analytical Geometry (Circles & Lines)...")
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
        q_id = f"MATH_P2_ANAG_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Analytical Geometry",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Analytical Geometry",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_ints(val, count=8):
        w = set()
        for delta in [-1, 1, -2, 2, -3, 3, -4, 4, 5, -5, 10, -10]:
            if val + delta != val:
                w.add(str(val + delta))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = val + random.randint(11, 40) * random.choice([1, -1])
            if extra != val and str(extra) not in cand_list:
                cand_list.append(str(extra))
        return cand_list[:count]

    def get_w_coords(x, y, count=8):
        w = set()
        # Common sign errors, transpositions, shifts
        deltas = [(-x, y), (x, -y), (-x, -y), (y, x), (x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+2, y-2), (-y, -x)]
        for wx, wy in deltas:
            if (wx, wy) != (x, y):
                w.add(f"({wx}; {wy})")
        cand_list = list(w)
        while len(cand_list) < count:
            wx = x + random.randint(-6, 6)
            wy = y + random.randint(-6, 6)
            s_cand = f"({wx}; {wy})"
            if (wx, wy) != (x, y) and s_cand not in cand_list:
                cand_list.append(s_cand)
        return cand_list[:count]

    def get_w_angles(deg, count=8):
        w = set()
        for delta in [180 - deg, 90 - deg if deg < 90 else deg - 90, 360 - deg, deg + 45, deg - 45, 90 + deg if deg < 90 else deg]:
            cand = round(delta, 2)
            if 0 < cand < 180 and cand != deg:
                w.add(f"{cand:.2f}°" if not cand.is_integer() else f"{int(cand)}°")
        cand_list = list(w)
        while len(cand_list) < count:
            cand = round(random.uniform(5.0, 175.0), 2)
            s_cand = f"{cand:.2f}°"
            if cand != deg and s_cand not in cand_list:
                cand_list.append(s_cand)
        return cand_list[:count]

    def get_w_lines(m, c, count=8):
        w = set()
        m_str = f"{m}x" if m != 1 and m != -1 else ("x" if m == 1 else "-x")
        for dm in [-1, 1, -2, 2]:
            new_m = m + dm
            nm_str = f"{new_m}x" if new_m != 1 and new_m != -1 else ("x" if new_m == 1 else "-x")
            for dc in [-2, 2, -1, 1]:
                new_c = c + dc
                cop = "+" if new_c >= 0 else "-"
                w.add(f"y = {nm_str} {cop} {abs(new_c)}")
        cand_list = [item for item in w if item != f"y = {m_str} {'+' if c>=0 else '-'} {abs(c)}"]
        while len(cand_list) < count:
            rm = m + random.choice([-3, 3, -4, 4])
            rc = c + random.randint(-8, 8)
            rm_str = f"{rm}x" if rm != 1 and rm != -1 else ("x" if rm == 1 else "-x")
            cand_list.append(f"y = {rm_str} {'+' if rc>=0 else '-'} {abs(rc)}")
        return cand_list[:count]

    # ====================================================
    # EASY QUESTIONS (Target: 300)
    # ====================================================
    easy_count = 0

    # 1. Circle center and radius from standard form (x - a)^2 + (y - b)^2 = r^2 (75)
    while easy_count < 75:
        a = random.randint(-8, 8)
        b = random.randint(-8, 8)
        r = random.randint(2, 12)
        r_sq = r ** 2
        sgn_a = f"- {a}" if a > 0 else (f"+ {abs(a)}" if a < 0 else "")
        sgn_b = f"- {b}" if b > 0 else (f"+ {abs(b)}" if b < 0 else "")
        term_x = f"(x {sgn_a})^2" if a != 0 else "x^2"
        term_y = f"(y {sgn_b})^2" if b != 0 else "y^2"
        
        mode = random.choice(["center", "radius"])
        if mode == "center":
            q = f"Determine the coordinates of the centre of the circle defined by ${term_x} + {term_y} = {r_sq}$."
            ans = f"({a}; {b})"
            wrongs = get_w_coords(a, b)
            exp = f"Comparing with the standard circle equation $(x - a)^2 + (y - b)^2 = r^2$, the centre is $(a; b) = ({a}; {b})$."
        else:
            q = f"Find the radius ($r$) of the circle defined by ${term_x} + {term_y} = {r_sq}$."
            ans = str(r)
            wrongs = get_w_ints(r)
            exp = f"Comparing with $(x - a)^2 + (y - b)^2 = r^2$, we have $r^2 = {r_sq} \\implies r = \\sqrt{{{r_sq}}} = {r}$."
            
        if add_q("easy", "Circle Equation", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 2. Gradient between two points (75)
    while easy_count < 150:
        x1 = random.randint(-8, 8)
        y1 = random.randint(-8, 8)
        dx = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        m_int = random.randint(-4, 4)
        if m_int == 0: m_int = 1
        dy = m_int * dx
        x2 = x1 + dx
        y2 = y1 + dy
        q = f"Calculate the gradient of the line passing through points A$({x1}; {y1})$ and B$({x2}; {y2})$."
        ans = str(m_int)
        wrongs = get_w_ints(m_int)
        exp = f"Using the gradient formula: $m = \\frac{{y_2 - y_1}}{{x_2 - x_1}} = \\frac{{{y2} - ({y1})}}{{{x2} - ({x1})}} = \\frac{{{dy}}}{{{dx}}} = {m_int}$."
        if add_q("easy", "Gradient", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 3. Midpoint of a line segment (75)
    while easy_count < 225:
        # Choose even sums for clean integer midpoints
        mx = random.randint(-8, 8)
        my = random.randint(-8, 8)
        dx = random.randint(-9, 9)
        dy = random.randint(-9, 9)
        x1 = mx - dx
        y1 = my - dy
        x2 = mx + dx
        y2 = my + dy
        if (x1, y1) == (x2, y2): continue
        q = f"Find the coordinates of the midpoint $M$ of the segment connecting $P({x1}; {y1})$ and $Q({x2}; {y2})$."
        ans = f"({mx}; {my})"
        wrongs = get_w_coords(mx, my)
        exp = f"$M = \\left(\\frac{{x_1 + x_2}}{{2}}; \\frac{{y_1 + y_2}}{{2}}\\right) = \\left(\\frac{{{x1} + {x2}}}{{2}}; \\frac{{{y1} + {y2}}}{{2}}\\right) = ({mx}; {my})$."
        if add_q("easy", "Midpoint", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 4. Distance between two points (Pythagorean triples) (75)
    pyth_triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25), (9, 12, 15)]
    while easy_count < 300:
        a_dx, b_dy, dist = random.choice(pyth_triples)
        # Random signs
        sx = random.choice([1, -1])
        sy = random.choice([1, -1])
        dx = a_dx * sx
        dy = b_dy * sy
        x1 = random.randint(-10, 10)
        y1 = random.randint(-10, 10)
        x2 = x1 + dx
        y2 = y1 + dy
        q = f"Calculate the exact distance between points $A({x1}; {y1})$ and $B({x2}; {y2})$."
        ans = str(dist)
        wrongs = get_w_ints(dist)
        exp = f"$d = \\sqrt{{(x_2 - x_1)^2 + (y_2 - y_1)^2}} = \\sqrt{{({dx})^2 + ({dy})^2}} = \\sqrt{{{dx**2 + dy**2}}} = {dist}$."
        if add_q("easy", "Distance Formula", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    print(f"Easy questions created: {easy_count}")

    # ====================================================
    # MEDIUM QUESTIONS (Target: 500)
    # ====================================================
    medium_count = 0

    # 1. Angle of inclination θ (tan θ = m) (125)
    while medium_count < 125:
        mode = random.choice(["acute", "obtuse"])
        if mode == "acute":
            deg = round(random.uniform(15.0, 75.0), 1)
            m_val = round(math.tan(math.radians(deg)), 2)
            q = f"A straight line has a gradient of $m = {m_val:.2f}$. Calculate its angle of inclination $\\theta$ (correct to one decimal place)."
            ans = f"{deg:.1f}°"
            wrongs = get_w_angles(deg)
            exp = f"$\\tan \\theta = m = {m_val:.2f} \\implies \\theta = \\tan^{{-1}}({m_val:.2f}) \\approx {ans}$."
        else:
            ref_deg = round(random.uniform(15.0, 75.0), 1)
            deg = round(180.0 - ref_deg, 1)
            m_val = round(math.tan(math.radians(deg)), 2) # negative
            q = f"A line has a negative gradient of $m = {m_val:.2f}$. Determine its angle of inclination $\\theta$ (correct to one decimal place)."
            ans = f"{deg:.1f}°"
            wrongs = get_w_angles(deg)
            exp = f"Since $m < 0$, $\\theta = 180^\\circ - \\tan^{{-1}}(|{m_val:.2f}|) = 180^\\circ - {ref_deg:.1f}^\\circ = {ans}$."
            
        if add_q("medium", "Angle of Inclination", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 2. Completing the square for circle equation (125)
    # x^2 + y^2 - 2ax - 2by + c = 0
    while medium_count < 250:
        a = random.randint(-6, 6)
        b = random.randint(-6, 6)
        r = random.randint(3, 9)
        if a == 0 and b == 0: continue
        # (x - a)^2 + (y - b)^2 = r^2
        # x^2 - 2ax + a^2 + y^2 - 2by + b^2 = r^2
        # x^2 + y^2 - 2ax - 2by + (a^2 + b^2 - r^2) = 0
        c_const = a**2 + b**2 - r**2
        
        term_x = f"{'-' if 2*a > 0 else '+'} {abs(2*a)}x" if a != 0 else ""
        term_y = f"{'-' if 2*b > 0 else '+'} {abs(2*b)}y" if b != 0 else ""
        term_c = f"{'+' if c_const >= 0 else '-'} {abs(c_const)}"
        
        circle_expanded = f"x^2 + y^2 {term_x} {term_y} {term_c} = 0"
        
        mode = random.choice(["center", "radius"])
        if mode == "center":
            q = f"Find the coordinates of the centre of the circle defined by ${circle_expanded}$."
            ans = f"({a}; {b})"
            wrongs = get_w_coords(a, b)
            exp = f"Complete the square: $(x - {a})^2 + (y - {b})^2 = {r}^2$. Thus the centre is $(a; b) = ({a}; {b})$."
        else:
            q = f"Determine the length of the radius of the circle defined by ${circle_expanded}$."
            ans = str(r)
            wrongs = get_w_ints(r)
            exp = f"Completing the square gives $(x - {a})^2 + (y - {b})^2 = {r**2} \\implies r = \\sqrt{{{r**2}}} = {r}$."
            
        if add_q("medium", "Circle Geometry", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 3. Equation of tangent to a circle at a point on circumference (125)
    # Use clean integer gradients: m_tan in {-3, -2, -1, 1, 2, 3}
    # m_tan = -(x1 - a) / (y1 - b)
    # If m_tan = -1: dy = dx
    # If m_tan = -2: dy = 1, dx = 2  (r^2 = 5) or dy = 2, dx = 4 (r^2 = 20)
    # If m_tan = 2: dy = -1, dx = 2
    # If m_tan = -3: dy = 1, dx = 3  (r^2 = 10)
    # If m_tan = 3: dy = -1, dx = 3
    tan_configs = [
        (1, 1, 2, -1), (-1, 1, 2, 1), (1, -1, 2, 1), (-1, -1, 2, -1),
        (2, 1, 5, -2), (-2, 1, 5, 2), (2, -1, 5, 2), (-2, -1, 5, -2),
        (3, 1, 10, -3), (-3, 1, 10, 3), (3, -1, 10, 3), (-3, -1, 10, -3),
        (4, 2, 20, -2), (-4, 2, 20, 2), (4, -2, 20, 2), (-4, -2, 20, -2),
        (2, 2, 8, -1), (-2, 2, 8, 1), (3, 3, 18, -1), (-3, 3, 18, 1)
    ]
    while medium_count < 375:
        a = random.randint(-7, 7)
        b = random.randint(-7, 7)
        dx_val, dy_val, r_sq, m_tan = random.choice(tan_configs)
        x1 = a + dx_val
        y1 = b + dy_val
        c_tan = y1 - m_tan * x1
        
        sgn_a = f"- {a}" if a > 0 else (f"+ {abs(a)}" if a < 0 else "")
        sgn_b = f"- {b}" if b > 0 else (f"+ {abs(b)}" if b < 0 else "")
        circ_eq = f"(x {sgn_a})^2 + (y {sgn_b})^2 = {r_sq}" if (a != 0 or b != 0) else f"x^2 + y^2 = {r_sq}"
        
        m_str = f"{m_tan}x" if m_tan != 1 and m_tan != -1 else ("x" if m_tan == 1 else "-x")
        ans = f"y = {m_str} {'+' if c_tan>=0 else '-'} {abs(c_tan)}"
        wrongs = get_w_lines(m_tan, c_tan)
        exp = f"Radius connects centre $C({a}; {b})$ to $P({x1}; {y1})$. Gradient of radius $m_{{rad}} = \\frac{{{y1} - {b}}}{{{x1} - {a}}} = \\frac{{{dy_val}}}{{{dx_val}}}$. Since tangent is perpendicular to radius, $m_{{tan}} = -\\frac{{1}}{{m_{{rad}}}} = {m_tan}$. Using $y - {y1} = {m_tan}(x - {x1}) \\implies {ans}$."
        if add_q("medium", "Tangents to Circles", f"Determine the equation of the tangent to the circle ${circ_eq}$ at the point $P({x1}; {y1})$.", ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 4. Unknown endpoint from midpoint / Parallelogram 4th vertex (125)
    while medium_count < 500:
        mode = random.choice(["endpoint", "parallelogram"])
        if mode == "endpoint":
            x1 = random.randint(-8, 8)
            y1 = random.randint(-8, 8)
            mx = random.randint(-8, 8)
            my = random.randint(-8, 8)
            x2 = 2 * mx - x1
            y2 = 2 * my - y1
            q = f"The midpoint of line segment $AB$ is $M({mx}; {my})$. If $A$ has coordinates $({x1}; {y1})$, determine the coordinates of point $B$."
            ans = f"({x2}; {y2})"
            wrongs = get_w_coords(x2, y2)
            exp = f"$\\frac{{{x1} + x_B}}{{2}} = {mx} \\implies x_B = 2({mx}) - ({x1}) = {x2}$. $\\frac{{{y1} + y_B}}{{2}} = {my} \\implies y_B = 2({my}) - ({y1}) = {y2}$. Thus $B({x2}; {y2})$."
        else:
            x1, y1 = random.randint(-6, 6), random.randint(-6, 6)
            x2, y2 = random.randint(-6, 6), random.randint(-6, 6)
            x3, y3 = random.randint(-6, 6), random.randint(-6, 6)
            # Diagonals AC and BD bisect each other:
            # Midpoint AC = ((x1+x3)/2, (y1+y3)/2)
            # D = (x1 + x3 - x2, y1 + y3 - y2)
            x4 = x1 + x3 - x2
            y4 = y1 + y3 - y2
            q = f"Points $A({x1}; {y1})$, $B({x2}; {y2})$, $C({x3}; {y3})$, and $D(x; y)$ form a parallelogram $ABCD$ in order. Find the coordinates of vertex $D$."
            ans = f"({x4}; {y4})"
            wrongs = get_w_coords(x4, y4)
            exp = f"The diagonals of a parallelogram bisect each other. Midpoint $AC =$ Midpoint $BD$. $\\frac{{{x1} + {x3}}}{{2}} = \\frac{{{x2} + x_D}}{{2}} \\implies x_D = {x1} + {x3} - {x2} = {x4}$. Similarly, $y_D = {y1} + {y3} - {y2} = {y4}$."
            
        if add_q("medium", "Coordinate Geometry", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    print(f"Medium questions created: {medium_count}")

    # ====================================================
    # HARD QUESTIONS (Target: 200)
    # ====================================================
    hard_count = 0

    # 1. Relationship between two circles (intersect, touch externally, touch internally, disjoint) (50)
    while hard_count < 50:
        c1_x, c1_y = random.randint(-5, 5), random.randint(-5, 5)
        # Distance between centers using 3-4-5 or 6-8-10
        dx_c, dy_c, d_val = random.choice([(3, 4, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13)])
        c2_x = c1_x + dx_c
        c2_y = c1_y + dy_c
        
        rel_type = random.choice(["touch_ext", "touch_int", "intersect", "disjoint"])
        if rel_type == "touch_ext":
            r1 = random.randint(2, d_val - 2)
            r2 = d_val - r1
            ans = "Touch externally"
            exp = f"Distance between centres $d = \\sqrt{{({c2_x}-{c1_x})^2 + ({c2_y}-{c1_y})^2}} = {d_val}$. Sum of radii $r_1 + r_2 = {r1} + {r2} = {d_val}$. Since $d = r_1 + r_2$, the circles touch externally."
        elif rel_type == "touch_int":
            r2 = random.randint(2, 5)
            r1 = d_val + r2
            ans = "Touch internally"
            exp = f"Distance between centres $d = {d_val}$. Difference between radii $|r_1 - r_2| = {r1} - {r2} = {d_val}$. Since $d = |r_1 - r_2|$, the circles touch internally."
        elif rel_type == "intersect":
            r1 = d_val - 1
            r2 = d_val - 2
            ans = "Intersect at two distinct points"
            exp = f"Distance between centres $d = {d_val}$. Here $|r_1 - r_2| < d < r_1 + r_2$, which confirms the circles intersect at two distinct points."
        else:
            r1 = 1
            r2 = 1
            ans = "Do not intersect (disjoint and separate)"
            exp = f"Distance between centres $d = {d_val}$. Sum of radii $r_1 + r_2 = {r1 + r2} < {d_val}$. Since $d > r_1 + r_2$, the circles are entirely separate."

        all_rels = [
            "Touch externally", "Touch internally", "Intersect at two distinct points",
            "Do not intersect (disjoint and separate)", "Concentric with identical centres",
            "Coincident circles", "Orthogonal at origin"
        ]
        wrongs = [r for r in all_rels if r != ans]
        q = f"Circle $C_1$ has centre $({c1_x}; {c1_y})$ and radius $r_1 = {r1}$. Circle $C_2$ has centre $({c2_x}; {c2_y})$ and radius $r_2 = {r2}$. What is the geometric relationship between the two circles?"
        if add_q("hard", "Intersecting Circles", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    # 2. Length of tangent from external point to circle (50)
    while hard_count < 100:
        # Tangent length L = sqrt(d^2 - r^2)
        # Use Pythagorean triples: (r, L, d)
        r, L, d_val = random.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (6, 8, 10), (8, 6, 10)])
        c_x, c_y = random.randint(-4, 4), random.randint(-4, 4)
        # External point P at distance d_val from centre
        # We can align horizontally or vertically:
        p_x = c_x + d_val
        p_y = c_y
        circ_eq = f"(x - {c_x})^2 + (y - {c_y})^2 = {r**2}" if (c_x != 0 or c_y != 0) else f"x^2 + y^2 = {r**2}"
        q = f"Determine the length of the tangent drawn from the external point $P({p_x}; {p_y})$ to the circle ${circ_eq}$."
        ans = str(L)
        wrongs = get_w_ints(L)
        exp = f"The distance from $P({p_x}; {p_y})$ to centre $C({c_x}; {c_y})$ is $d = {d_val}$. The radius is $r = {r}$. By the Pythagorean theorem on the right triangle formed by the radius and tangent: $L = \\sqrt{{d^2 - r^2}} = \\sqrt{{{d_val}^2 - {r}^2}} = \\sqrt{{{d_val**2 - r**2}}} = {L}$."
        if add_q("hard", "Tangents to Circles", q, ans, wrongs, exp, "Problem Solving"):
            hard_count += 1

    # 3. Horizontal and vertical tangents to circle (50)
    while hard_count < 150:
        a = random.randint(-8, 8)
        b = random.randint(-8, 8)
        r = random.randint(2, 15)
        orient = random.choice(["horizontal", "vertical"])
        sgn_a = f"- {a}" if a > 0 else (f"+ {abs(a)}" if a < 0 else "")
        sgn_b = f"- {b}" if b > 0 else (f"+ {abs(b)}" if b < 0 else "")
        circ_eq = f"(x {sgn_a})^2 + (y {sgn_b})^2 = {r**2}" if (a != 0 or b != 0) else f"x^2 + y^2 = {r**2}"
        
        if orient == "horizontal":
            y_high = b + r
            y_low = b - r
            q = f"Find the equations of the two HORIZONTAL tangents to the circle defined by ${circ_eq}$."
            ans = f"y = {y_high} and y = {y_low}"
            wrongs = [
                f"x = {a+r} and x = {a-r}",
                f"y = {y_high+1} and y = {y_low-1}",
                f"y = {b+r**2} and y = {b-r**2}",
                f"x = {y_high} and x = {y_low}",
                f"y = {r} and y = -{r}",
                f"y = {b} and x = {a}",
                f"y = {2*r} and y = {-2*r}"
            ]
            exp = f"Horizontal tangents are perpendicular to the vertical diameter. The vertical bounds of the circle are $y = b \\pm r = {b} \\pm {r}$, giving $y = {y_high}$ and $y = {y_low}$."
        else:
            x_right = a + r
            x_left = a - r
            q = f"Find the equations of the two VERTICAL tangents to the circle defined by ${circ_eq}$."
            ans = f"x = {x_right} and x = {x_left}"
            wrongs = [
                f"y = {b+r} and y = {b-r}",
                f"x = {x_right+1} and x = {x_left-1}",
                f"x = {a+r**2} and x = {a-r**2}",
                f"y = {x_right} and y = {x_left}",
                f"x = {r} and x = -{r}",
                f"x = {a} and y = {b}",
                f"x = {2*r} and x = {-2*r}"
            ]
            exp = f"Vertical tangents are perpendicular to the horizontal diameter. The horizontal bounds of the circle are $x = a \\pm r = {a} \\pm {r}$, giving $x = {x_right}$ and $x = {x_left}$."
            
        if add_q("hard", "Tangents to Circles", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    # 4. Collinear points with unknown variable (50)
    while hard_count < 200:
        x1, y1 = random.randint(-6, 6), random.randint(-6, 6)
        m = random.choice([-3, -2, -1, 1, 2, 3])
        dx2 = random.choice([-3, -2, -1, 1, 2, 3])
        dx3 = dx2 + random.choice([2, 3, 4])
        x2 = x1 + dx2
        y2 = y1 + m * dx2
        x3 = x1 + dx3
        y3 = y1 + m * dx3
        
        q = f"The three points $A({x1}; {y1})$, $B({x2}; {y2})$, and $C({x3}; k)$ are collinear. Find the value of $k$."
        ans = str(y3)
        wrongs = get_w_ints(y3)
        exp = f"Collinear points have equal gradients: $m_{{AB}} = m_{{BC}} = {m}$. Thus $\\frac{{k - ({y2})}}{{{x3} - ({x2})}} = {m} \\implies k - {y2} = {m * (x3 - x2)} \\implies k = {y3}$."
        if add_q("hard", "Collinear Points", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    print(f"Final Counts: {{'easy': {easy_count}, 'medium': {medium_count}, 'hard': {hard_count}}}")
    out_dir = "dataset/grade12/mathematics"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_analytical_geometry.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    t1 = time.time()
    print(f"SUCCESS: {out_file} generated in {t1-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_analytical()
