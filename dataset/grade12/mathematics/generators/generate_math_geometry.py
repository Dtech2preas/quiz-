import json
import random
import os
import time
import math

def generate_math_geometry():
    print("Generating Grade 12 Mathematics: Euclidean Geometry (Circles & Similarity)...")
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
        q_id = f"MATH_P2_GEOM_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Euclidean Geometry",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Euclidean Geometry",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_ints(val, count=8):
        w = set()
        for delta in [-1, 1, -2, 2, -5, 5, -10, 10, -15, 15]:
            if val + delta > 0 and val + delta != val:
                w.add(str(val + delta))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = val + random.randint(3, 40) * random.choice([1, -1])
            if extra > 0 and extra != val and str(extra) not in cand_list:
                cand_list.append(str(extra))
        return cand_list[:count]

    def get_w_angles(deg, count=8):
        w = set()
        for delta in [180 - deg, deg // 2, 2 * deg if 2 * deg < 180 else deg - 20, 90 - deg if deg < 90 else deg - 90, deg + 10, deg - 10, deg + 20, deg - 20]:
            if 0 < delta < 180 and delta != deg:
                w.add(f"{delta}°")
        cand_list = list(w)
        while len(cand_list) < count:
            cand = random.randint(15, 165)
            s_cand = f"{cand}°"
            if cand != deg and s_cand not in cand_list:
                cand_list.append(s_cand)
        return cand_list[:count]

    def get_w_floats(val, decimals=2, count=8):
        w = set()
        for delta in [-0.5, 0.5, -0.2, 0.2, -1.0, 1.0, -0.25, 0.25]:
            cand = round(val + delta, decimals)
            if cand > 0 and cand != val:
                w.add(f"{cand:.{decimals}f}")
        cand_list = list(w)
        while len(cand_list) < count:
            extra = round(val + random.uniform(-4.0, 4.0), decimals)
            s_cand = f"{extra:.{decimals}f}"
            if extra > 0 and extra != val and s_cand not in cand_list:
                cand_list.append(s_cand)
        return cand_list[:count]

    # ====================================================
    # EASY QUESTIONS (Target: 300)
    # ====================================================
    easy_count = 0

    # 1. Angle at centre is twice angle at circumference (60)
    while easy_count < 60:
        circumf_ang = random.randint(25, 80)
        centre_ang = 2 * circumf_ang
        mode = random.choice(["find_centre", "find_circumf"])
        if mode == "find_centre":
            q = f"In a circle with centre $O$, chord $AB$ subtends an angle of $\\hat{{C}} = {circumf_ang}^\\circ$ at the circumference. Calculate the size of the angle subtended at the centre, $A\\hat{{O}}B$."
            ans = f"{centre_ang}°"
            wrongs = get_w_angles(centre_ang)
            exp = f"Theorem: The angle subtended by an arc at the centre is twice the angle subtended at the circumference. $A\\hat{{O}}B = 2 \\times \\hat{{C}} = 2 \\times {circumf_ang}^\\circ = {ans}$."
        else:
            q = f"In a circle with centre $O$, chord $AB$ subtends an angle of $A\\hat{{O}}B = {centre_ang}^\\circ$ at the centre. Determine the size of the angle $\\hat{{C}}$ subtended by $AB$ at the circumference."
            ans = f"{circumf_ang}°"
            wrongs = get_w_angles(circumf_ang)
            exp = f"Theorem: $\\hat{{C}} = \\frac{{1}}{{2}} A\\hat{{O}}B = \\frac{{{centre_ang}^\\circ}}{{2}} = {ans}$."
            
        if add_q("easy", "Angle at Centre", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 2. Angle in a semi-circle (60)
    while easy_count < 120:
        ang_A = random.randint(18, 72)
        ang_B = 90 - ang_A
        diameter_names = ["AB", "PQ", "KL", "XY", "CD"]
        d_name = random.choice(diameter_names)
        other_pt = "C" if d_name != "CD" else "E"
        q = f"In a circle with diameter ${d_name}$, point ${other_pt}$ lies on the circumference. If $\\angle {d_name[0]}{other_pt}{d_name[1]} = 90^\\circ$ and $\\angle {other_pt}{d_name[0]}{d_name[1]} = {ang_A}^\\circ$, calculate the size of $\\angle {other_pt}{d_name[1]}{d_name[0]}$."
        ans = f"{ang_B}°"
        wrongs = get_w_angles(ang_B)
        exp = f"Angle in a semi-circle is $90^\\circ$ ($\\angle {d_name[0]}{other_pt}{d_name[1]} = 90^\\circ$). The sum of angles in $\\triangle {d_name[0]}{other_pt}{d_name[1]}$ is $180^\\circ \\implies 90^\\circ - {ang_A}^\\circ = {ans}$."
        if add_q("easy", "Angle in Semi-circle", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 3. Opposite angles of a cyclic quad (60)
    quad_letters = [("A", "B", "C", "D"), ("P", "Q", "R", "S"), ("K", "L", "M", "N"), ("W", "X", "Y", "Z")]
    while easy_count < 180:
        p1, p2, p3, p4 = random.choice(quad_letters)
        ang1 = random.randint(45, 135)
        ang_opp = 180 - ang1
        q = f"${p1}{p2}{p3}{p4}$ is a cyclic quadrilateral. If $\\hat{{{p1}}} = {ang1}^\\circ$, calculate the size of the opposite interior angle $\\hat{{{p3}}}$."
        ans = f"{ang_opp}°"
        wrongs = get_w_angles(ang_opp)
        exp = f"Theorem: The opposite angles of a cyclic quadrilateral are supplementary. $\\hat{{{p1}}} + \\hat{{{p3}}} = 180^\\circ \\implies \\hat{{{p3}}} = 180^\\circ - {ang1}^\\circ = {ans}$."
        if add_q("easy", "Cyclic Quadrilateral", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 4. Exterior angle of a cyclic quad (60)
    while easy_count < 240:
        p1, p2, p3, p4 = random.choice(quad_letters)
        ang_val = random.randint(55, 125)
        q = f"${p1}{p2}{p3}{p4}$ is a cyclic quadrilateral with side ${p1}{p2}$ produced to $E$. If the exterior angle $\\angle {p4}{p1}E = {ang_val}^\\circ$, determine the size of the interior opposite angle $\\hat{{{p3}}}$."
        ans = f"{ang_val}°"
        wrongs = get_w_angles(ang_val)
        exp = f"Theorem: The exterior angle of a cyclic quadrilateral equals the interior opposite angle. $\\hat{{{p3}}} = \\angle {p4}{p1}E = {ans}$."
        if add_q("easy", "Cyclic Quadrilateral", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 5. Tangent perpendicular to radius at point of contact (60)
    while easy_count < 300:
        pt = random.choice(["T", "P", "A", "B"])
        ang_offset = random.randint(15, 65)
        ang_rem = 90 - ang_offset
        q = f"In a circle with centre $O$, line $ST$ is a tangent to the circle at point ${pt}$, and $O{pt}$ is a radius. If a chord ${pt}Q$ is drawn such that $\\angle O{pt}Q = {ang_offset}^\\circ$, calculate the size of the angle between the tangent $S{pt}$ and the chord ${pt}Q$ ($\\angle S{pt}Q$)."
        ans = f"{ang_rem}°"
        wrongs = get_w_angles(ang_rem)
        exp = f"Theorem: A tangent to a circle is perpendicular to the radius at the point of contact ($O{pt} \\perp S{pt} \\implies \\angle O{pt}S = 90^\\circ$). Therefore $\\angle S{pt}Q = 90^\\circ - {ang_offset}^\\circ = {ans}$."
        if add_q("easy", "Tangents", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    print(f"Easy questions created: {easy_count}")

    # ====================================================
    # MEDIUM QUESTIONS (Target: 500)
    # ====================================================
    medium_count = 0

    # 1. Tan-Chord Theorem calculations (125)
    tangent_lines = [
        ("PQ", "A", "B", "C"),
        ("ST", "K", "L", "M"),
        ("MN", "X", "Y", "Z"),
        ("DE", "P", "Q", "R"),
        ("XY", "E", "F", "G"),
        ("AB", "C", "D", "E")
    ]
    while medium_count < 125:
        t_line, pt, ch, opp = random.choice(tangent_lines)
        subtended_ang = random.randint(25, 85)
        q = f"Line ${t_line}$ is tangent to a circle at point ${pt}$. Chord ${pt}{ch}$ is drawn. Point ${opp}$ lies on the major arc such that $\\angle {pt}{opp}{ch} = {subtended_ang}^\\circ$. Determine the size of the angle between the tangent ${t_line}$ and chord ${pt}{ch}$ ($\\angle {t_line[1]}{pt}{ch}$)."
        ans = f"{subtended_ang}°"
        wrongs = get_w_angles(subtended_ang)
        exp = f"Theorem (Tan-Chord Theorem): The angle between a tangent to a circle and a chord drawn through the point of contact is equal to the angle in the alternate segment. Thus $\\angle {t_line[1]}{pt}{ch} = \\angle {pt}{opp}{ch} = {ans}$."
        if add_q("medium", "Tan-Chord Theorem", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 2. Proportionality Theorem in Triangles (line parallel to one side) (125)
    while medium_count < 250:
        mult = random.choice([2, 3, 4, 5])
        db = random.randint(3, 15)
        ad = mult * db
        ec = random.randint(3, 15)
        ae = mult * ec
        
        mode = random.choice(["find_ae", "find_ec", "find_ad", "find_db"])
        if mode == "find_ae":
            q = f"In $\\triangle ABC$, line segment $DE$ is drawn parallel to base $BC$, with $D$ on $AB$ and $E$ on $AC$. If $AD = {ad}$ cm, $DB = {db}$ cm, and $EC = {ec}$ cm, calculate the length of $AE$."
            ans = f"{ae} cm"
            wrongs = [f"{w} cm" for w in get_w_ints(ae)]
            exp = f"Theorem (Proportionality theorem, $DE \\parallel BC$): $\\frac{{AE}}{{EC}} = \\frac{{AD}}{{DB}} \\implies \\frac{{AE}}{{{ec}}} = \\frac{{{ad}}}{{{db}}} = {mult} \\implies AE = {mult} \\times {ec} = {ans}$."
        elif mode == "find_ec":
            q = f"In $\\triangle ABC$, $DE \\parallel BC$. If $AD = {ad}$ cm, $DB = {db}$ cm, and $AE = {ae}$ cm, calculate the length of $EC$."
            ans = f"{ec} cm"
            wrongs = [f"{w} cm" for w in get_w_ints(ec)]
            exp = f"Theorem ($DE \\parallel BC$): $\\frac{{AE}}{{EC}} = \\frac{{AD}}{{DB}} \\implies \\frac{{{ae}}}{{EC}} = \\frac{{{ad}}}{{{db}}} = {mult} \\implies EC = \\frac{{{ae}}}{{{mult}}} = {ans}$."
        elif mode == "find_ad":
            q = f"In $\\triangle ABC$, $DE \\parallel BC$. If $DB = {db}$ cm, $AE = {ae}$ cm, and $EC = {ec}$ cm, calculate the length of $AD$."
            ans = f"{ad} cm"
            wrongs = [f"{w} cm" for w in get_w_ints(ad)]
            exp = f"Theorem ($DE \\parallel BC$): $\\frac{{AD}}{{DB}} = \\frac{{AE}}{{EC}} \\implies \\frac{{AD}}{{{db}}} = \\frac{{{ae}}}{{{ec}}} = {mult} \\implies AD = {mult} \\times {db} = {ans}$."
        else:
            q = f"In $\\triangle ABC$, $DE \\parallel BC$. If $AD = {ad}$ cm, $AE = {ae}$ cm, and $EC = {ec}$ cm, calculate the length of $DB$."
            ans = f"{db} cm"
            wrongs = [f"{w} cm" for w in get_w_ints(db)]
            exp = f"Theorem ($DE \\parallel BC$): $\\frac{{AD}}{{DB}} = \\frac{{AE}}{{EC}} \\implies \\frac{{{ad}}}{{DB}} = \\frac{{{ae}}}{{{ec}}} = {mult} \\implies DB = \\frac{{{ad}}}{{{mult}}} = {ans}$."
            
        if add_q("medium", "Proportionality Theorem", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 3. Angles in the same segment with algebra (125)
    while medium_count < 375:
        x_val = random.randint(5, 30)
        a_coef = random.randint(3, 6)
        c_coef = random.randint(1, a_coef - 1)
        b_const = random.randint(5, 35)
        d_const = (a_coef - c_coef) * x_val + b_const
        angle_size = a_coef * x_val + b_const
        if angle_size >= 90: continue
        
        mode = random.choice(["solve_x", "solve_angle"])
        if mode == "solve_x":
            q = f"Points $A, B, C,$ and $D$ lie on the circumference of a circle. Subtended by the same chord $AB$, $\\angle ADB = ({a_coef}x + {b_const})^\\circ$ and $\\angle ACB = ({c_coef}x + {d_const})^\\circ$. Determine the value of $x$."
            ans = str(x_val)
            wrongs = get_w_ints(x_val)
            exp = f"Angles in the same segment are equal: ${a_coef}x + {b_const} = {c_coef}x + {d_const} \\implies {a_coef - c_coef}x = {d_const - b_const} \\implies x = {ans}$."
        else:
            q = f"Points $A, B, C,$ and $D$ lie in order on a circle. $\\angle ADB = ({a_coef}x + {b_const})^\\circ$ and $\\angle ACB = ({c_coef}x + {d_const})^\\circ$. Determine the actual size of $\\angle ADB$."
            ans = f"{angle_size}°"
            wrongs = get_w_angles(angle_size)
            exp = f"Equating angles in the same segment: ${a_coef}x + {b_const} = {c_coef}x + {d_const} \\implies x = {x_val}$. Thus $\\angle ADB = {a_coef}({x_val}) + {b_const} = {ans}$."
            
        if add_q("medium", "Angles in Same Segment", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 4. Line from centre perpendicular to chord (Pythagoras) (125)
    while medium_count < 500:
        half_ch = random.randint(4, 24)
        dist_c = random.randint(3, 20)
        rad_val = round((dist_c**2 + half_ch**2)**0.5, 2)
        rad_str = str(int(rad_val)) if float(rad_val).is_integer() else f"{rad_val:.2f}"
        chord_len = 2 * half_ch
        mode = random.choice(["find_radius", "find_chord", "find_dist"])
        if mode == "find_radius":
            q = f"In a circle with centre $O$, a chord of length ${chord_len}$ cm is at a perpendicular distance of ${dist_c}$ cm from the centre. Calculate the radius of the circle (correct to 2 decimal places)."
            ans = f"{rad_str} cm"
            wrongs = [f"{w} cm" for w in get_w_floats(rad_val, 2)]
            exp = f"The perpendicular from centre bisects the chord: half-chord $= \\frac{{{chord_len}}}{{2}} = {half_ch}$ cm. By Pythagoras: $r^2 = {dist_c}^2 + {half_ch}^2 = {dist_c**2 + half_ch**2} \\implies r \\approx {ans}$."
        elif mode == "find_chord":
            q = f"A circle has a radius of ${rad_str}$ cm. A chord is drawn at a perpendicular distance of ${dist_c}$ cm from the centre. What is the total length of the chord?"
            ans = f"{chord_len} cm"
            wrongs = [f"{w} cm" for w in get_w_ints(chord_len)]
            exp = f"Half-chord length $= \\sqrt{{r^2 - d^2}} = \\sqrt{{{rad_val}^2 - {dist_c}^2}} = {half_ch}$ cm. Total chord length $= 2 \\times {half_ch} = {ans}$."
        else:
            q = f"In a circle of radius ${rad_str}$ cm, a chord of length ${chord_len}$ cm is drawn. Determine the perpendicular distance from the centre of the circle to the chord."
            ans = f"{dist_c} cm"
            wrongs = [f"{w} cm" for w in get_w_ints(dist_c)]
            exp = f"Half-chord $= {half_ch}$ cm. By Pythagoras, distance $= \\sqrt{{r^2 - (\\text{{half-chord}})^2}} = {ans}$."
            
        if add_q("medium", "Chord and Radius", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    print(f"Medium questions created: {medium_count}")

    # ====================================================
    # HARD QUESTIONS (Target: 200)
    # ====================================================
    hard_count = 0

    # 1. Similar Triangles and Ratio of Sides (50)
    while hard_count < 50:
        scale = random.choice([1.5, 2.0, 2.5, 3.0, 4.0])
        ab = random.randint(4, 12)
        bc = random.randint(5, 14)
        de = round(ab * scale, 1)
        ef = round(bc * scale, 1)
        de_str = str(int(de)) if float(de).is_integer() else f"{de:.1f}"
        ef_str = str(int(ef)) if float(ef).is_integer() else f"{ef:.1f}"
        
        q = f"Given that $\\triangle ABC \\,\\|\\|\\, \\triangle DEF$. If $AB = {ab}$ cm, $BC = {bc}$ cm, and $DE = {de_str}$ cm, calculate the length of side $EF$."
        ans = f"{ef_str} cm"
        wrongs = [f"{w} cm" for w in get_w_floats(ef, 1)]
        exp = f"Since $\\triangle ABC \\,\\|\\|\\, \\triangle DEF$, corresponding sides are in proportion: $\\frac{{EF}}{{BC}} = \\frac{{DE}}{{AB}} \\implies \\frac{{EF}}{{{bc}}} = \\frac{{{de_str}}}{{{ab}}} = {scale} \\implies EF = {scale} \\times {bc} = {ans}$."
        if add_q("hard", "Similarity", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    # 2. Geometric Mean / Altitude to Hypotenuse in Right Triangle (50)
    trig_names = [
        ("ABC", "B", "AC", "BD", "AD", "DC"),
        ("PQR", "Q", "PR", "QS", "PS", "SR"),
        ("KLM", "L", "KM", "LN", "KN", "NM"),
        ("XYZ", "Y", "XZ", "YW", "XW", "WZ"),
        ("DEF", "E", "DF", "EG", "DG", "GF")
    ]
    while hard_count < 100:
        t_name, right_ang, hyp, alt, seg1, seg2 = random.choice(trig_names)
        ad_v = random.randint(2, 25)
        dc_v = random.randint(2, 25)
        bd_val = round((ad_v * dc_v)**0.5, 2)
        bd_str = str(int(bd_val)) if float(bd_val).is_integer() else f"{bd_val:.2f}"
        q = f"In $\\triangle {t_name}$, right-angled at $\\hat{{{right_ang}}}$, altitude ${alt}$ is drawn perpendicular to hypotenuse ${hyp}$. If ${seg1} = {ad_v}$ cm and ${seg2} = {dc_v}$ cm, calculate the length of altitude ${alt}$."
        ans = f"{bd_str} cm"
        wrongs = [f"{w} cm" for w in get_w_floats(bd_val, 2)]
        exp = f"By the geometric mean theorem for right-angled triangles: ${alt}^2 = {seg1} \\times {seg2} = {ad_v} \\times {dc_v} = {ad_v * dc_v} \\implies {alt} = \\sqrt{{{ad_v * dc_v}}} \\approx {ans}$."
        if add_q("hard", "Similarity", q, ans, wrongs, exp, "Problem Solving"):
            hard_count += 1

    # 3. Two tangents from common external point (50)
    ext_pts = [("P", "A", "B"), ("Q", "C", "D"), ("T", "X", "Y"), ("S", "K", "L"), ("R", "M", "N"), ("W", "E", "F")]
    while hard_count < 150:
        p, a, b = random.choice(ext_pts)
        angle_p = random.randint(25, 85)
        base_ang = (180 - angle_p) / 2
        base_str = str(int(base_ang)) if float(base_ang).is_integer() else f"{base_ang:.1f}"
        q = f"Tangents ${p}{a}$ and ${p}{b}$ are drawn from an external point ${p}$ to touch a circle at ${a}$ and ${b}$. If $\\angle {a}{p}{b} = {angle_p}^\\circ$, calculate the size of $\\angle {p}{a}{b}$."
        ans = f"{base_str}°"
        wrongs = get_w_angles(int(base_ang))
        exp = f"Theorem: Tangents drawn from a common external point are equal in length (${p}{a} = {p}{b}$). Thus $\\triangle {p}{a}{b}$ is isosceles with $\\angle {p}{a}{b} = \\angle {p}{b}{a} = \\frac{{180^\\circ - {angle_p}^\\circ}}{{2}} = {ans}$."
        if add_q("hard", "Tangents", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    # 4. Proving a quadrilateral is cyclic (Converse Theorems) (50)
    quad_names = ["ABCD", "PQRS", "KLMN", "WXYZ", "EFGH"]
    while hard_count < 200:
        q_name = random.choice(quad_names)
        ang_a = random.randint(45, 135)
        is_cyclic = random.choice([True, False])
        if is_cyclic:
            ang_c = 180 - ang_a
            ans = "Yes, because opposite angles are supplementary (sum to 180°)"
            exp = f"In quad ${q_name}$, opposite angles sum to $\\hat{{{q_name[0]}}} + \\hat{{{q_name[2]}}} = {ang_a}^\\circ + {ang_c}^\\circ = 180^\\circ$. By the converse of opposite angles of a cyclic quad, ${q_name}$ is cyclic."
        else:
            diff = random.choice([-15, -10, -5, 5, 10, 15])
            ang_c = 180 - ang_a + diff
            ans = "No, because opposite angles are not supplementary"
            exp = f"$\\hat{{{q_name[0]}}} + \\hat{{{q_name[2]}}} = {ang_a}^\\circ + {ang_c}^\\circ = {ang_a + ang_c}^\\circ \\neq 180^\\circ$. Therefore ${q_name}$ is not cyclic."

        q = f"In quadrilateral ${q_name}$, $\\hat{{{q_name[0]}}} = {ang_a}^\\circ$ and the opposite angle $\\hat{{{q_name[2]}}} = {ang_c}^\\circ$. Is ${q_name}$ a cyclic quadrilateral?"
        wrongs = [
            "Yes, because opposite angles are supplementary (sum to 180°)" if not is_cyclic else "No, because opposite angles are not supplementary",
            "Yes, because adjacent angles are complementary",
            "No, because opposite angles are equal",
            "Cannot be determined without circle radius",
            "Yes, by the tan-chord theorem",
            "No, because exterior angle is undefined",
            "Yes, because all four sides are equal"
        ]
        if add_q("hard", "Cyclic Quad Proofs", q, ans, wrongs, exp, "Problem Solving"):
            hard_count += 1

    print(f"Final Counts: {{'easy': {easy_count}, 'medium': {medium_count}, 'hard': {hard_count}}}")
    out_dir = "dataset/grade12/mathematics"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_geometry.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    t1 = time.time()
    print(f"SUCCESS: {out_file} generated in {t1-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_geometry()
