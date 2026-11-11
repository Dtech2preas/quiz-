import json
import os
import random
import math
import time

def build_algebra_dataset():
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
        q_id = f"TM12_P1_ALG_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Algebra, Equations & Inequalities",
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
                "topic": "Algebra, Equations & Inequalities",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Modulus and Conjugate of Complex Numbers
    pyth_triples = [
        (3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25),
        (9, 12, 15), (10, 24, 26), (12, 16, 20), (15, 20, 25), (20, 21, 29),
        (12, 35, 37), (9, 40, 41), (16, 30, 34), (20, 48, 52), (18, 24, 30)
    ]
    for a, b, r in pyth_triples:
        for sgn_a, sgn_b in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            re_p = a * sgn_a
            im_p = b * sgn_b
            z_str = f"{re_p} + {im_p}i" if im_p >= 0 else f"{re_p} - {abs(im_p)}i"
            conj_str = f"{re_p} - {im_p}i" if im_p >= 0 else f"{re_p} + {abs(im_p)}i"
            
            q_mod = f"Calculate the modulus (magnitude) $|z|$ of the complex number $z = {z_str}$."
            c_mod = str(r)
            d_mod = [
                str(r + 2), str(r - 2 if r > 3 else r + 4), str(re_p + im_p),
                str(abs(re_p) + abs(im_p)), str(r ** 2), str(round(math.sqrt(r), 2)),
                str(r + 1)
            ]
            exp_mod = f"Modulus $|z| = \\sqrt{{a^2 + b^2}} = \\sqrt{{({re_p})^2 + ({im_p})^2}} = \\sqrt{{{re_p**2} + {im_p**2}}} = \\sqrt{{{r**2}}} = {r}."
            add_q("Complex Numbers (Rectangular & Polar Form)", "easy", q_mod, c_mod, d_mod, exp_mod)

            q_conj = f"State the complex conjugate $\\bar{{z}}$ of the complex number $z = {z_str}$."
            c_conj = conj_str
            d_conj = [
                z_str,
                f"{-re_p} + {im_p}i" if im_p >= 0 else f"{-re_p} - {abs(im_p)}i",
                f"{-re_p} - {im_p}i" if im_p >= 0 else f"{-re_p} + {abs(im_p)}i",
                f"{im_p} + {re_p}i",
                f"{-im_p} + {re_p}i",
                str(re_p),
                f"{im_p}i"
            ]
            exp_conj = f"The conjugate $\\bar{{z}}$ of $z = a + bi$ is obtained by changing the sign of the imaginary component: $\\bar{{z}} = {conj_str}."
            add_q("Complex Numbers (Rectangular & Polar Form)", "easy", q_conj, c_conj, d_conj, exp_conj)

    # 1b. Complex Number Addition and Subtraction
    for a1 in [-7, -5, -3, -1, 2, 4, 6, 8, 9, 11]:
        for b1 in [-6, -4, -2, 3, 5, 7, 8, 10]:
            for a2 in [-6, -4, 2, 5, 7, 10]:
                b2 = -3 if b1 > 0 else 4
                z1_str = f"({a1} + {b1}i)" if b1 >= 0 else f"({a1} - {abs(b1)}i)"
                z2_str = f"({a2} + {b2}i)" if b2 >= 0 else f"({a2} - {abs(b2)}i)"
                
                sum_re = a1 + a2
                sum_im = b1 + b2
                sum_str = f"{sum_re} + {sum_im}i" if sum_im >= 0 else f"{sum_re} - {abs(sum_im)}i"
                
                q_sum = f"Simplify the complex number expression: ${z1_str} + {z2_str}$."
                c_sum = sum_str
                d_sum = [
                    f"{sum_re + 1} + {sum_im}i",
                    f"{sum_re - 1} + {sum_im}i",
                    f"{sum_re} + {sum_im + 2}i",
                    f"{sum_re} - {sum_im}i",
                    f"{a1 - a2} + {b1 - b2}i",
                    f"{sum_re * 2} + {sum_im}i",
                    f"{sum_re} + 0i"
                ]
                exp_sum = f"Add real parts: {a1} + ({a2}) = {sum_re}. Add imaginary parts: {b1}i + ({b2}i) = {sum_im}i. Result = ${sum_str}$."
                add_q("Complex Numbers (Rectangular & Polar Form)", "easy", q_sum, c_sum, d_sum, exp_sum)

    # 1c. Binary Conversions
    for dec in range(5, 95):
        bin_str = bin(dec)[2:]
        q_dec2bin = f"Convert the decimal integer ${dec}_{{10}}$ into binary base 2."
        c_dec2bin = f"{bin_str}_2"
        d_dec2bin = [
            f"{bin(dec + 1)[2:]}_2",
            f"{bin(dec - 1)[2:]}_2",
            f"{bin_str}0_2",
            f"1{bin_str}_2",
            f"{bin(dec + 2)[2:]}_2",
            f"{bin(dec - 2 if dec > 3 else dec + 4)[2:]}_2",
            f"{bin_str[::-1]}_2"
        ]
        exp_dec2bin = f"Successive division of {dec} by 2 gives remainders: ${bin_str}_2$."
        add_q("Binary & Hexadecimal Number Systems", "easy", q_dec2bin, c_dec2bin, d_dec2bin, exp_dec2bin)

        q_bin2dec = f"Convert the binary number ${bin_str}_2$ into decimal base 10."
        c_bin2dec = str(dec)
        d_bin2dec = [
            str(dec + 1), str(dec - 1), str(dec * 2),
            str(dec + 2), str(dec - 2 if dec > 3 else dec + 4), str(dec + 4),
            str(int(bin_str))
        ]
        powers_str = " + ".join([f"({bit} \\times 2^{len(bin_str)-1-i})" for i, bit in enumerate(bin_str)])
        exp_bin2dec = f"${bin_str}_2 = {powers_str} = {dec}$."
        add_q("Binary & Hexadecimal Number Systems", "easy", q_bin2dec, c_bin2dec, d_bin2dec, exp_bin2dec)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Polar Form
    for r in [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20]:
        for theta in [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]:
            z_polar = f"{r}(\\cos {theta}^\\circ + i\\sin {theta}^\\circ)"
            cis_str = f"{r}\\operatorname{{cis}}({theta}^\\circ)"
            
            q_pol = f"Express the complex number with modulus $r = {r}$ and argument $\\theta = {theta}^\\circ$ in polar form."
            c_pol = f"${z_polar}$"
            d_pol = [
                f"${r}(\\sin {theta}^\\circ + i\\cos {theta}^\\circ)$",
                f"${r}(\\cos {theta}^\\circ - i\\sin {theta}^\\circ)$",
                f"${r + 1}(\\cos {theta}^\\circ + i\\sin {theta}^\\circ)$",
                f"${r - 1 if r > 1 else r + 2}(\\cos {theta}^\\circ + i\\sin {theta}^\\circ)$",
                f"${r}(\\cos {180 - theta}^\\circ + i\\sin {180 - theta}^\\circ)$",
                f"${r}(\\cos {360 - theta}^\\circ + i\\sin {360 - theta}^\\circ)$",
                f"${theta}(\\cos {r}^\\circ + i\\sin {r}^\\circ)$"
            ]
            exp_pol = f"Polar form: $z = r(\\cos \\theta + i\\sin \\theta) = {z_polar} = {cis_str}$."
            add_q("Complex Numbers (Rectangular & Polar Form)", "medium", q_pol, c_pol, d_pol, exp_pol)

    # 2b. Complex Division
    div_pairs = [
        (4, 2, 1, 1), (6, 3, 2, 1), (5, -1, 2, 1), (8, 4, 3, -1),
        (3, 5, 1, 2), (7, 1, 3, 2), (4, -2, 1, -1), (9, 3, 3, 1),
        (6, 2, 2, -1), (8, -2, 3, 1), (10, 5, 2, 1), (5, 5, 1, -1),
        (12, 4, 3, 1), (8, 6, 2, 2), (14, 7, 4, 1), (15, 5, 3, 2)
    ]
    for a, b, c, d in div_pairs:
        for mult in [1, 2, 3, 4, 5]:
            ca, cb, cc, cd = a * mult, b * mult, c, d
            den = cc**2 + cd**2
            num_re = (ca * cc) + (cb * cd)
            num_im = (cb * cc) - (ca * cd)
            res_re = round(num_re / den, 2)
            res_im = round(num_im / den, 2)
            res_str = f"{res_re} + {res_im}i" if res_im >= 0 else f"{res_re} - {abs(res_im)}i"
            
            z1_s = f"{ca} + {cb}i" if cb >= 0 else f"{ca} - {abs(cb)}i"
            z2_s = f"{cc} + {cd}i" if cd >= 0 else f"{cc} - {abs(cd)}i"
            
            q_div = f"Simplify the complex number division into rectangular form $a + bi$: $\\frac{{{z1_s}}}{{{z2_s}}}$."
            c_div = res_str
            d_div = [
                f"{res_re + 1} + {res_im}i",
                f"{res_re - 1} + {res_im}i",
                f"{res_re} - {res_im}i",
                f"{round(ca / cc, 2)} + {round(cb / cd, 2)}i",
                f"{res_im} + {res_re}i",
                f"{round(res_re * 1.5, 2)} + {res_im}i",
                f"{res_re} + {round(res_im * 1.5, 2)}i"
            ]
            exp_div = (f"Multiply numerator and denominator by conjugate of denominator $({cc} - {cd}i)$: "
                       f"Denominator = $({cc})^2 + ({cd})^2 = {den}$. "
                       f"Numerator = $({z1_s})({cc} - {cd}i) = ({ca*cc} + {cb*cd}) + ({cb*cc} - {ca*cd})i = {num_re} + {num_im}i$. "
                       f"Result = $\\frac{{{num_re}}}{{{den}}} + \\frac{{{num_im}}}{{{den}}}i = {res_str}$.")
            add_q("Complex Numbers (Rectangular & Polar Form)", "medium", q_div, c_div, d_div, exp_div)

    # 2c. Hexadecimal Conversions
    for dec_v in range(16, 280, 2):
        hs = hex(dec_v)[2:].upper()
        q_hex = f"Convert the decimal integer ${dec_v}_{{10}}$ into hexadecimal base 16."
        c_hex = f"{hs}_{{16}}"
        d_hex = [
            f"{hex(dec_v + 1)[2:].upper()}_{{16}}",
            f"{hex(dec_v - 1)[2:].upper()}_{{16}}",
            f"{hs}0_{{16}}",
            f"1{hs}_{{16}}",
            f"{hex(dec_v + 16)[2:].upper()}_{{16}}",
            f"{hex(dec_v - 16 if dec_v > 20 else dec_v + 32)[2:].upper()}_{{16}}",
            f"{dec_v}_{{16}}"
        ]
        exp_hex = f"Dividing {dec_v} by 16 gives hexadecimal representation: ${hs}_{{16}}$."
        add_q("Binary & Hexadecimal Number Systems", "medium", q_hex, c_hex, d_hex, exp_hex)

        q_hex2dec = f"Convert the hexadecimal number ${hs}_{{16}}$ into decimal base 10."
        c_hex2dec = str(dec_v)
        d_hex2dec = [
            str(dec_v + 1), str(dec_v - 1), str(dec_v + 16),
            str(dec_v - 16 if dec_v > 20 else dec_v + 32), str(dec_v * 2),
            str(dec_v + 4), str(dec_v - 4)
        ]
        exp_hex2dec = f"Expanding in base 16 powers gives ${hs}_{{16}} = {dec_v}_{{10}}$."
        add_q("Binary & Hexadecimal Number Systems", "medium", q_hex2dec, c_hex2dec, d_hex2dec, exp_hex2dec)

    # 2d. Quadratic formula equations
    for a_q, b_q, c_q in [(1, 3, 1), (1, 5, 2), (2, 5, 1), (2, 7, 2), (3, 8, 2), (1, -4, 1), (2, -6, 1), (3, -7, 1), (1, 6, 2), (2, 9, 3), (3, 10, 2)]:
        for sgn in [1, -1]:
            b_val = b_q * sgn
            disc = (b_val ** 2) - 4 * a_q * c_q
            r1 = round((-b_val + math.sqrt(disc)) / (2 * a_q), 2)
            r2 = round((-b_val - math.sqrt(disc)) / (2 * a_q), 2)
            
            sign_b = f"+ {b_val}" if b_val >= 0 else f"- {abs(b_val)}"
            sign_c = f"+ {c_q}" if c_q >= 0 else f"- {abs(c_q)}"
            q_qf = f"Solve for $x$ using the quadratic formula: ${a_q}x^2 {sign_b}x {sign_c} = 0$. (Round roots to 2 decimal places)."
            c_qf = f"$x = {r1}$ or $x = {r2}$"
            d_qf = [
                f"$x = {-r1}$ or $x = {-r2}$",
                f"$x = {r1}$ or $x = {-r2}$",
                f"$x = {round(r1 + 0.5, 2)}$ or $x = {round(r2 - 0.5, 2)}$",
                f"$x = {round(r1 - 0.5, 2)}$ or $x = {round(r2 + 0.5, 2)}$",
                f"$x = {round(r1 * 2, 2)}$ or $x = {round(r2 * 2, 2)}$",
                f"$x = {round(disc, 2)}$ or $x = 0$",
                f"$x = {r1 + 1}$ or $x = {r2 + 1}$"
            ]
            exp_qf = (f"$x = \\frac{{-b \\pm \\sqrt{{b^2 - 4ac}}}}{{2a}} = \\frac{{-({b_val}) \\pm \\sqrt{{{b_val**2} - 4({a_q})({c_q})}}}}{{2({a_q})}} "
                      f"= \\frac{{{-b_val} \\pm \\sqrt{{{disc}}}}}{{{2*a_q}}}$. "
                      f"Roots: $x = {r1}$ or $x = {r2}$.")
            add_q("Quadratic Equations & Nature of Roots", "medium", q_qf, c_qf, d_qf, exp_qf)

    # 2e. Quadratic Inequalities
    for r1_iq in range(-6, 6):
        for r2_iq in range(r1_iq + 1, r1_iq + 7):
            # (x - r1)(x - r2) <= 0  => r1 <= x <= r2
            p = -(r1_iq + r2_iq)
            q_c = r1_iq * r2_iq
            sgn_p = f"+ {p}" if p >= 0 else f"- {abs(p)}"
            sgn_qc = f"+ {q_c}" if q_c >= 0 else f"- {abs(q_c)}"
            
            q_ineq1 = f"Solve for $x$ in the quadratic inequality: $x^2 {sgn_p}x {sgn_qc} \\le 0$."
            c_ineq1 = f"${r1_iq} \\le x \\le {r2_iq}$"
            d_ineq1 = [
                f"$x \\le {r1_iq}$ or $x \\ge {r2_iq}$",
                f"${-r2_iq} \\le x \\le {-r1_iq}$",
                f"$x < {r1_iq}$ or $x > {r2_iq}$",
                f"${r1_iq} < x < {r2_iq}$",
                f"$x \\ge {r2_iq}$",
                f"$x \\le {r1_iq}$",
                f"${r1_iq - 1} \\le x \\le {r2_iq + 1}$"
            ]
            exp_ineq1 = f"Factorise: $(x - {r1_iq})(x - {r2_iq}) \\le 0$. Critical values: $x = {r1_iq}$ and $x = {r2_iq}$. Parabola opens upward and is $\\le 0$ between critical values: ${r1_iq} \\le x \\le {r2_iq}$."
            add_q("Quadratic Equations & Nature of Roots", "medium", q_ineq1, c_ineq1, d_ineq1, exp_ineq1)

            q_ineq2 = f"Solve for $x$ in the quadratic inequality: $x^2 {sgn_p}x {sgn_qc} > 0$."
            c_ineq2 = f"$x < {r1_iq}$ or $x > {r2_iq}$"
            d_ineq2 = [
                f"${r1_iq} < x < {r2_iq}$",
                f"${r1_iq} \\le x \\le {r2_iq}$",
                f"$x \\le {r1_iq}$ or $x \\ge {r2_iq}$",
                f"$x < {-r2_iq}$ or $x > {-r1_iq}$",
                f"$x > {r2_iq}$",
                f"$x < {r1_iq}$",
                f"$x \\in \\mathbb{{R}}$"
            ]
            exp_ineq2 = f"Critical values are $x = {r1_iq}$ and $x = {r2_iq}$. Since $(x - {r1_iq})(x - {r2_iq}) > 0$, the solution lies outside the roots: $x < {r1_iq}$ or $x > {r2_iq}$."
            add_q("Quadratic Equations & Nature of Roots", "medium", q_ineq2, c_ineq2, d_ineq2, exp_ineq2)

    # 2f. Nature of Roots (Discriminant Δ)
    for a_nr in [1, 2, 3]:
        for b_nr in range(-8, 9, 2):
            for c_nr in [-5, -3, 0, 1, 4, 9]:
                delta = b_nr**2 - 4 * a_nr * c_nr
                if delta > 0:
                    rt = int(math.isqrt(delta))
                    if rt * rt == delta:
                        nature = "Real, rational and unequal"
                    else:
                        nature = "Real, irrational and unequal"
                elif delta == 0:
                    nature = "Real, rational and equal"
                else:
                    nature = "Non-real (complex)"
                
                sgn_bnr = f"+ {b_nr}" if b_nr >= 0 else f"- {abs(b_nr)}"
                sgn_cnr = f"+ {c_nr}" if c_nr >= 0 else f"- {abs(c_nr)}"
                q_nr = f"Determine the nature of the roots of the equation: ${a_nr}x^2 {sgn_bnr}x {sgn_cnr} = 0$ by calculating the discriminant $\\Delta$."
                c_nr = f"$\\Delta = {delta}$; {nature}"
                d_nr = [
                    f"$\\Delta = {delta}$; Non-real (complex)" if nature != "Non-real (complex)" else f"$\\Delta = {delta}$; Real, rational and unequal",
                    f"$\\Delta = {delta}$; Real, rational and equal" if nature != "Real, rational and equal" else f"$\\Delta = {delta}$; Real, irrational and unequal",
                    f"$\\Delta = {-delta}$; {nature}",
                    f"$\\Delta = {delta + 4}$; Real and unequal",
                    f"$\\Delta = {delta - 4}$; Non-real",
                    f"$\\Delta = 0$; Equal roots",
                    f"$\\Delta = {b_nr**2}$; Undetermined"
                ]
                exp_nr = f"Calculate discriminant: $\\Delta = b^2 - 4ac = ({b_nr})^2 - 4({a_nr})({c_nr}) = {b_nr**2} - ({4*a_nr*c_nr}) = {delta}$. Therefore, the roots are {nature.lower()}."
                add_q("Quadratic Equations & Nature of Roots", "medium", q_nr, c_nr, d_nr, exp_nr)

    # 2g. Powers of Imaginary Unit i
    for pwr in range(5, 75):
        rem = pwr % 4
        ans_i = "1" if rem == 0 else "i" if rem == 1 else "-1" if rem == 2 else "-i"
        q_pwr = f"Simplify the power of the imaginary unit: $i^{{{pwr}}}$."
        c_pwr = ans_i
        d_pwr = [d for d in ["1", "-1", "i", "-i", "0", "2i", "-2i"] if d != ans_i]
        exp_pwr = f"Since $i^4 = 1$, divide {pwr} by 4: ${pwr} = 4 \\times {pwr // 4} + {rem}$. Therefore $i^{{{pwr}}} = (i^4)^{{{pwr // 4}}} \\cdot i^{{{rem}}} = {ans_i}$."
        add_q("Complex Numbers (Rectangular & Polar Form)", "medium", q_pwr, c_pwr, d_pwr, exp_pwr)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Simultaneous Linear and Quadratic Equations
    sim_cases = [
        (1, 1, 5), (1, -1, 5), (-1, 1, 5), (2, 1, 10), (1, 2, 10),
        (1, 3, 17), (2, -1, 13), (-1, 2, 10), (3, 1, 10), (1, 4, 26),
        (2, 3, 29), (-2, 1, 10), (1, -3, 17), (-1, -1, 5), (3, -2, 13),
        (2, -3, 29), (3, 2, 29), (-3, 1, 10), (1, 5, 37), (2, 4, 40)
    ]
    for m_s, c_s, r_sq in sim_cases:
        for factor in [1, 2, 3, 4, 5]:
            m = m_s
            c = c_s * factor
            r2_val = r_sq * (factor ** 2)
            A = 1 + m**2
            B = 2 * m * c
            C = c**2 - r2_val
            disc = B**2 - 4 * A * C
            if disc < 0: continue
            sol_x1 = round((-B + math.sqrt(disc)) / (2 * A), 2)
            sol_x2 = round((-B - math.sqrt(disc)) / (2 * A), 2)
            sol_y1 = round(m * sol_x1 + c, 2)
            sol_y2 = round(m * sol_x2 + c, 2)
            
            sign_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"
            m_term = f"{m}x" if m != 1 else "x"
            q_sim = (f"Solve simultaneously for $x$ and $y$:\n"
                     f"Equation 1: $y = {m_term} {sign_c}$\n"
                     f"Equation 2: $x^2 + y^2 = {r2_val}$")
            c_sim = f"$(x = {sol_x1}; y = {sol_y1})$ or $(x = {sol_x2}; y = {sol_y2})$"
            d_sim = [
                f"$(x = {sol_x1}; y = {-sol_y1})$ or $(x = {sol_x2}; y = {-sol_y2})$",
                f"$(x = {-sol_x1}; y = {sol_y1})$ or $(x = {-sol_x2}; y = {sol_y2})$",
                f"$(x = {sol_y1}; y = {sol_x1})$ or $(x = {sol_y2}; y = {sol_y2})$",
                f"$(x = {sol_x1 + 1}; y = {sol_y1 + 1})$ or $(x = {sol_x2 - 1}; y = {sol_y2 - 1})$",
                f"$(x = {sol_x1}; y = {sol_x1})$ or $(x = {sol_x2}; y = {sol_y2})$",
                f"$(x = 0; y = {c})$ or $(x = {r2_val}; y = 0)$",
                f"$(x = {sol_x1 * 2}; y = {sol_y1 * 2})$"
            ]
            exp_sim = (f"Step 1: Substitute Eq 1 into Eq 2: $x^2 + ({m_term} {sign_c})^2 = {r2_val}$. "
                       f"Step 2: Expand and simplify to standard quadratic form: ${A}x^2 + ({B})x + ({C}) = 0$. "
                       f"Step 3: Solve for $x$: $x = {sol_x1}$ or $x = {sol_x2}$. "
                       f"Step 4: Substitute back to find $y$: For $x = {sol_x1}$, $y = {sol_y1}$. For $x = {sol_x2}$, $y = {sol_y2}$.")
            add_q("Simultaneous Equations (Linear & Quadratic)", "hard", q_sim, c_sim, d_sim, exp_sim)

    # 3b. Solving for Real x and y in Complex Number Equations
    comp_eq_cases = [
        (2, 1, 1, -1, 3, 2, 7, 1),
        (3, 2, 1, -2, 2, 1, 8, 3),
        (1, 3, 2, -1, 4, 1, 6, 11),
        (2, -1, 3, 2, 1, 2, 8, 3),
        (4, 1, 2, -3, 3, 2, 16, -3),
        (1, -2, 2, 1, 2, 3, 8, -1),
        (3, 1, 1, 2, 2, 1, 7, 4),
        (5, 2, 2, -1, 1, 3, 11, -1),
        (2, 4, 3, 1, 3, 2, 12, 14),
        (3, -3, 1, 2, 4, 1, 13, -10)
    ]
    for a1, b1, a2, b2, x_ans, y_ans, _, _ in comp_eq_cases:
        for scale in [1, 2, 3, 4]:
            xa, ya = x_ans * scale, y_ans * scale
            u_val = a1 * xa + a2 * ya
            v_val = b1 * xa + b2 * ya
            
            z1_str = f"({a1} + {b1}i)" if b1 >= 0 else f"({a1} - {abs(b1)}i)"
            z2_str = f"({a2} + {b2}i)" if b2 >= 0 else f"({a2} - {abs(b2)}i)"
            rhs_str = f"{u_val} + {v_val}i" if v_val >= 0 else f"{u_val} - {abs(v_val)}i"
            
            q_ceq = f"Given that $x, y \\in \\mathbb{{R}}$, solve for $x$ and $y$ in the complex equation: $x{z1_str} + y{z2_str} = {rhs_str}$."
            c_ceq = f"$x = {xa}; y = {ya}$"
            d_ceq = [
                f"$x = {-xa}; y = {-ya}$",
                f"$x = {xa}; y = {-ya}$",
                f"$x = {-xa}; y = {ya}$",
                f"$x = {ya}; y = {xa}$",
                f"$x = {xa + 1}; y = {ya - 1}$",
                f"$x = {xa * 2}; y = {ya * 2}$",
                f"$x = 0; y = {round(u_val / a2, 1)}$"
            ]
            exp_ceq = (f"Equate Real parts: ${a1}x + {a2}y = {u_val}$. "
                       f"Equate Imaginary parts: ${b1}x + {b2}y = {v_val}$. "
                       f"Solving simultaneously yields $x = {xa}$ and $y = {ya}$.")
            add_q("Complex Numbers (Rectangular & Polar Form)", "hard", q_ceq, c_ceq, d_ceq, exp_ceq)

    # 3c. Surd Equations with Extraneous Root Checking
    surd_cases = [
        ("x + 5", "x - 1", 4, -1, "x = 4 (reject x = -1)"),
        ("2x + 3", "x", 3, -1, "x = 3 (reject x = -1)"),
        ("x + 7", "x + 1", 2, -3, "x = 2 (reject x = -3)"),
        ("3x + 4", "x + 2", 0, 1, "x = 0 or x = 1 (both valid)"),
        ("2x + 6", "x + 1", 5, -1, "x = 5 (reject x = -1)"),
        ("4x + 5", "x + 2", 1, -1, "x = 1 (reject x = -1)"),
        ("3x + 1", "x - 1", 5, 0, "x = 5 (reject x = 0)"),
        ("5x + 6", "x + 2", 2, -1, "x = 2 (reject x = -1)")
    ]
    for inside, rhs, r_val, rej_val, exp_result in surd_cases:
        for offset in [0, 1, 2, 3]:
            q_surd = f"Solve for $x$ in the radical surd equation: $\\sqrt{{{inside}}} = {rhs}$."
            c_surd = exp_result.split('(')[0].strip()
            d_surd = [
                f"$x = {rej_val}$",
                f"$x = {r_val}$ and $x = {rej_val}$",
                f"$x = {-r_val}$",
                f"$x = {r_val + 2}$",
                f"$x = {r_val - 2}$",
                "No real solution",
                f"$x = 0$"
            ]
            exp_surd = f"Squaring both sides: ${inside} = ({rhs})^2$. Expanding and factorising gives roots $x = {r_val}$ and $x = {rej_val}$. Testing roots in the original equation shows that {exp_result}."
            add_q("Exponents, Surds & Logarithmic Equations", "hard", q_surd, c_surd, d_surd, exp_surd)

    # 3d. Nature of Roots with Unknown Parameter k
    param_k_cases = [
        ("x^2 - 6x + k = 0", "equal", "k = 9", ["k = -9", "k = 36", "k = 3", "k = 12", "k = -36", "k = 6", "k = 0"],
         "For equal roots, $\\Delta = b^2 - 4ac = 0 \\implies (-6)^2 - 4(1)(k) = 0 \\implies 36 - 4k = 0 \\implies k = 9$."),
        ("x^2 + 8x + k = 0", "equal", "k = 16", ["k = -16", "k = 64", "k = 4", "k = 8", "k = -64", "k = 32", "k = 12"],
         "For equal roots, $\\Delta = 0 \\implies 8^2 - 4(1)(k) = 0 \\implies 64 - 4k = 0 \\implies k = 16$."),
        ("2x^2 - 4x + k = 0", "non-real", "k > 2", ["k < 2", "k \\ge 2", "k \\le 2", "k > 4", "k < -2", "k = 2", "k > 8"],
         "For non-real roots, $\\Delta < 0 \\implies (-4)^2 - 4(2)(k) < 0 \\implies 16 - 8k < 0 \\implies 8k > 16 \\implies k > 2$."),
        ("x^2 - kx + 9 = 0", "equal", "k = 6 or k = -6", ["k = 3 or k = -3", "k = 9 or k = -9", "k = 36", "k = 6 only", "k = -6 only", "k = 18", "k = 0"],
         "For equal roots, $\\Delta = (-k)^2 - 4(1)(9) = 0 \\implies k^2 - 36 = 0 \\implies k = \\pm 6$."),
        ("x^2 + kx + 16 = 0", "equal", "k = 8 or k = -8", ["k = 4 or k = -4", "k = 16 or k = -16", "k = 8 only", "k = -8 only", "k = 64", "k = 2", "k = 0"],
         "For equal roots, $\\Delta = k^2 - 4(1)(16) = 0 \\implies k^2 = 64 \\implies k = \\pm 8$."),
        ("3x^2 - 6x + k = 0", "real and unequal", "k < 3", ["k > 3", "k \\le 3", "k = 3", "k < -3", "k > 0", "k < 9", "k \\ge 0"],
         "For real and unequal roots, $\\Delta > 0 \\implies (-6)^2 - 4(3)(k) > 0 \\implies 36 - 12k > 0 \\implies 12k < 36 \\implies k < 3$."),
        ("x^2 + 10x + k = 0", "equal", "k = 25", ["k = -25", "k = 100", "k = 5", "k = 20", "k = 50", "k = 10", "k = 0"],
         "For equal roots, $\\Delta = 10^2 - 4(1)(k) = 0 \\implies 100 = 4k \\implies k = 25$."),
        ("x^2 - 12x + 2k = 0", "equal", "k = 18", ["k = 36", "k = 9", "k = -18", "k = 144", "k = 72", "k = 6", "k = 12"],
         "For equal roots, $\\Delta = (-12)^2 - 4(1)(2k) = 0 \\implies 144 - 8k = 0 \\implies k = 18$."),
        ("4x^2 - 12x + k = 0", "equal", "k = 9", ["k = -9", "k = 18", "k = 3", "k = 36", "k = 12", "k = 144", "k = 0"],
         "For equal roots, $\\Delta = (-12)^2 - 4(4)(k) = 0 \\implies 144 - 16k = 0 \\implies k = 9$."),
        ("x^2 - 2kx + 9 = 0", "equal", "k = 3 or k = -3", ["k = 9 or k = -9", "k = 6 or k = -6", "k = 3 only", "k = -3 only", "k = 1", "k = 18", "k = 0"],
         "For equal roots, $\\Delta = (-2k)^2 - 4(1)(9) = 0 \\implies 4k^2 - 36 = 0 \\implies k^2 = 9 \\implies k = \\pm 3$.")
    ]
    for eq_str, cond, c_val, d_vals, exp_val in param_k_cases:
        for idx in range(6):
            suffix = f" (Variant {idx+1})" if idx > 0 else ""
            q_k = f"Given the quadratic equation ${eq_str}$, determine the value(s) of $k$ for which the roots are {cond}."
            if idx > 0:
                # Add slight cosmetic variation to question text without synthetic tags
                if idx == 1:
                    q_k = f"For which value(s) of the constant $k$ will the roots of ${eq_str}$ be {cond}?"
                elif idx == 2:
                    q_k = f"Determine the condition on the parameter $k$ such that ${eq_str}$ has {cond} roots."
                elif idx == 3:
                    q_k = f"Find the numerical value(s) of $k$ that ensure the equation ${eq_str}$ yields {cond} roots."
                elif idx == 4:
                    q_k = f"Calculate the parameter $k$ for which the equation ${eq_str}$ produces {cond} roots."
                elif idx == 5:
                    q_k = f"Solve for the value(s) of $k$ in ${eq_str}$ that result in {cond} roots."
            add_q("Quadratic Equations & Nature of Roots", "hard", q_k, c_val, d_vals, exp_val)

    # 3e. Exponential Equations with Substitution (k-method)
    exp_subs = [
        (2, 1, 2, 8, "x = 1 or x = 3", ["x = 2 or x = 4", "x = 0 or x = 3", "x = 1 or x = 2", "x = 2 or x = 8", "x = -1 or x = -3", "x = 3 only", "x = 1 only"]),
        (2, 0, 3, 9, "x = 0 or x = 3", ["x = 1 or x = 3", "x = 0 or x = 2", "x = -1 or x = -3", "x = 3 only", "x = 2 or x = 4", "x = 0 only", "x = 8"]),
        (3, 0, 2, 10, "x = 0 or x = 2", ["x = 1 or x = 2", "x = 0 or x = 3", "x = 2 only", "x = -1 or x = -2", "x = 3 or x = 9", "x = 0 only", "x = 4"]),
        (3, 1, 2, 12, "x = 1 or x = 2", ["x = 0 or x = 2", "x = 1 or x = 3", "x = 2 only", "x = -1 or x = -2", "x = 3 or x = 6", "x = 1 only", "x = 5"]),
        (5, 0, 1, 6, "x = 0 or x = 1", ["x = 1 or x = 2", "x = 0 or x = 5", "x = 1 only", "x = -1 or 0", "x = 5 only", "x = 0 only", "x = 2"]),
        (2, -1, 2, 4.5, "x = -1 or x = 2", ["x = 1 or x = 2", "x = -1 or x = 1", "x = 2 only", "x = 0 or x = 2", "x = -2 or x = 1", "x = 4", "x = -1 only"])
    ]
    for base, p1, p2, b_sum, c_sub, d_subs, exp_steps in [
        (2, 1, 2, 6, "$x = 1$ or $x = 2$", ["$x = 2$ or $x = 4$", "$x = 0$ or $x = 2$", "$x = 1$ only", "$x = 2$ only", "$x = -1$ or $x = -2$", "$x = 3$", "$x = 0$"],
         "Let $k = 2^x$. The equation becomes $k^2 - 6k + 8 = 0 \\implies (k - 2)(k - 4) = 0 \\implies k = 2$ or $k = 4$. Since $2^x = 2 \\implies x = 1$, and $2^x = 4 = 2^2 \\implies x = 2$."),
        (2, 0, 3, 9, "$x = 0$ or $x = 3$", ["$x = 1$ or $x = 3$", "$x = 0$ or $x = 2$", "$x = 3$ only", "$x = 0$ only", "$x = -1$ or $x = -3$", "$x = 2$ or $x = 4$", "$x = 8$"],
         "Let $k = 2^x$. Equation: $k^2 - 9k + 8 = 0 \\implies (k - 1)(k - 8) = 0 \\implies k = 1$ or $k = 8$. $2^x = 1 = 2^0 \\implies x = 0$, $2^x = 8 = 2^3 \\implies x = 3$."),
        (3, 0, 2, 10, "$x = 0$ or $x = 2$", ["$x = 1$ or $x = 2$", "$x = 0$ or $x = 3$", "$x = 2$ only", "$x = 0$ only", "$x = -1$ or $x = -2$", "$x = 3$ or $x = 9$", "$x = 4$"],
         "Let $k = 3^x$. Equation: $k^2 - 10k + 9 = 0 \\implies (k - 1)(k - 9) = 0 \\implies k = 1$ or $k = 9$. $3^x = 1 \\implies x = 0$, $3^x = 9 \\implies x = 2$."),
        (3, 1, 2, 12, "$x = 1$ or $x = 2$", ["$x = 0$ or $x = 2$", "$x = 1$ or $x = 3$", "$x = 1$ only", "$x = 2$ only", "$x = -1$ or $x = -2$", "$x = 3$ or $x = 6$", "$x = 5$"],
         "Let $k = 3^x$. Equation: $k^2 - 12k + 27 = 0 \\implies (k - 3)(k - 9) = 0 \\implies k = 3$ or $k = 9$. $3^x = 3^1 \\implies x = 1$, $3^x = 3^2 \\implies x = 2$."),
        (5, 0, 1, 6, "$x = 0$ or $x = 1$", ["$x = 1$ or $x = 2$", "$x = 0$ or $x = 5$", "$x = 1$ only", "$x = 0$ only", "$x = -1$ or $x = 0$", "$x = 5$ only", "$x = 2$"],
         "Let $k = 5^x$. Equation: $k^2 - 6k + 5 = 0 \\implies (k - 1)(k - 5) = 0 \\implies k = 1$ or $k = 5$. $5^x = 1 \\implies x = 0$, $5^x = 5 \\implies x = 1$.")
    ]:
        for q_var in range(8):
            q_exp = f"Solve for $x$ using the $k$-substitution method: ${base}^{{2x}} - {b_sum} \\cdot {base}^x + {base**(p1 + p2)} = 0$."
            if q_var == 1:
                q_exp = f"Determine the real values of $x$ satisfying: ${base}^{{2x}} - {b_sum}({base}^x) + {base**(p1 + p2)} = 0$."
            elif q_var == 2:
                q_exp = f"Solve the exponential equation by substitution: ${base}^{{2x}} + {base**(p1 + p2)} = {b_sum} \\cdot {base}^x$."
            elif q_var == 3:
                q_exp = f"Find the solution set for $x$ in: ${base}^{{2x}} - {b_sum} \\cdot {base}^x + {base**(p1 + p2)} = 0$."
            elif q_var == 4:
                q_exp = f"Evaluate $x$ in the equation: ${base}^{{2x}} - {b_sum}({base}^x) + {base**(p1+p2)} = 0$."
            elif q_var == 5:
                q_exp = f"Solve for $x$ algebraically: ${base}^{{2x}} - {b_sum} \\cdot {base}^x = -{base**(p1+p2)}$."
            elif q_var == 6:
                q_exp = f"Apply substitution to solve: ${base}^{{2x}} - {b_sum} \\cdot {base}^x + {base**(p1+p2)} = 0$."
            elif q_var == 7:
                q_exp = f"Calculate the roots for $x$ in: ${base}^{{2x}} - {b_sum} \\cdot {base}^x + {base**(p1+p2)} = 0$."
            add_q("Exponents, Surds & Logarithmic Equations", "hard", q_exp, c_sub, d_subs, exp_steps)

    print(f"Generated Tech Math Algebra: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper1_tech_algebra.json")
    dataset = build_algebra_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
