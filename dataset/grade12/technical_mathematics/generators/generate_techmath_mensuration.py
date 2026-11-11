import json
import os
import random
import math
import time

def build_mensuration_dataset():
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
        q_id = f"TM12_P2_MEN_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Mensuration & Mid-Ordinate Rule",
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
                "topic": "Mensuration & Mid-Ordinate Rule",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Cylinder Volume & Surface Area
    for r_c in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
        for h_c in [4, 5, 6, 7, 8, 10, 12, 14, 15, 18, 20]:
            vol_c = round(math.pi * (r_c ** 2) * h_c, 2)
            q_vol = f"Calculate the volume of a right circular cylinder with radius $r = {r_c}$ cm and height $h = {h_c}$ cm. (Round to 2 decimal places)."
            c_vol = f"{vol_c} cm^3"
            d_vol = [
                f"{round(vol_c * 2, 2)} cm^3",
                f"{round(vol_c / 2, 2)} cm^3",
                f"{round(2 * math.pi * r_c * h_c, 2)} cm^3",
                f"{round(vol_c + 25.5, 2)} cm^3",
                f"{round(vol_c - 25.5 if vol_c > 30 else vol_c + 50, 2)} cm^3",
                f"{round((r_c**2) * h_c, 2)} cm^3",
                f"{round(math.pi * r_c * (h_c**2), 2)} cm^3"
            ]
            exp_vol = f"Cylinder volume formula: $V = \\pi r^2 h = \\pi({r_c})^2({h_c}) = {r_c**2 * h_c}\\pi = {vol_c}\\text{{ cm}}^3$."
            add_q("Right Circular Cylinders", "easy", q_vol, c_vol, d_vol, exp_vol)

            csa_c = round(2 * math.pi * r_c * h_c, 2)
            q_csa = f"Calculate the curved (lateral) surface area of a right circular cylinder of radius $r = {r_c}$ cm and height $h = {h_c}$ cm. (Round to 2 decimal places)."
            c_csa = f"{csa_c} cm^2"
            d_csa = [
                f"{round(csa_c * 2, 2)} cm^2",
                f"{round(csa_c / 2, 2)} cm^2",
                f"{round(math.pi * (r_c**2) * h_c, 2)} cm^2",
                f"{round(csa_c + 15, 2)} cm^2",
                f"{round(csa_c - 15 if csa_c > 20 else csa_c + 30, 2)} cm^2",
                f"{round(2 * r_c * h_c, 2)} cm^2",
                f"{round(2 * math.pi * (r_c**2), 2)} cm^2"
            ]
            exp_csa = f"Curved surface area formula: $A_{{\\text{{curved}}}} = 2\\pi rh = 2\\pi({r_c})({h_c}) = {2 * r_c * h_c}\\pi = {csa_c}\\text{{ cm}}^2$."
            add_q("Right Circular Cylinders", "easy", q_csa, c_csa, d_csa, exp_csa)

    # 1b. Sphere Volume & Surface Area
    for r_sp in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]:
        vol_sp = round((4 / 3) * math.pi * (r_sp ** 3), 2)
        sa_sp = round(4 * math.pi * (r_sp ** 2), 2)
        
        q_vsp = f"Calculate the volume of an engineering spherical bearing of radius $r = {r_sp}$ cm. (Round to 2 decimal places)."
        c_vsp = f"{vol_sp} cm^3"
        d_vsp = [
            f"{round(vol_sp * 2, 2)} cm^3",
            f"{round(vol_sp / 2, 2)} cm^3",
            f"{round(sa_sp, 2)} cm^3",
            f"{round(vol_sp + 35, 2)} cm^3",
            f"{round(vol_sp - 35 if vol_sp > 40 else vol_sp + 70, 2)} cm^3",
            f"{round(math.pi * r_sp**3, 2)} cm^3",
            f"{round((4/3) * (r_sp**3), 2)} cm^3"
        ]
        exp_vsp = f"Sphere volume formula: $V = \\frac{{4}}{{3}}\\pi r^3 = \\frac{{4}}{{3}}\\pi({r_sp})^3 = {vol_sp}\\text{{ cm}}^3$."
        add_q("Spheres & Hemispheres", "easy", q_vsp, c_vsp, d_vsp, exp_vsp)

        q_sasp = f"Calculate the total surface area of a sphere of radius $r = {r_sp}$ cm. (Round to 2 decimal places)."
        c_sasp = f"{sa_sp} cm^2"
        d_sasp = [
            f"{round(sa_sp * 2, 2)} cm^2",
            f"{round(sa_sp / 2, 2)} cm^2",
            f"{round(vol_sp, 2)} cm^2",
            f"{round(sa_sp + 20, 2)} cm^2",
            f"{round(sa_sp - 20 if sa_sp > 25 else sa_sp + 40, 2)} cm^2",
            f"{round(4 * r_sp**2, 2)} cm^2",
            f"{round(math.pi * r_sp**2, 2)} cm^2"
        ]
        exp_sasp = f"Sphere surface area formula: $A = 4\\pi r^2 = 4\\pi({r_sp})^2 = {4 * r_sp**2}\\pi = {sa_sp}\\text{{ cm}}^2$."
        add_q("Spheres & Hemispheres", "easy", q_sasp, c_sasp, d_sasp, exp_sasp)

    # 1c. Rectangular Prisms (Cuboids)
    for l_rp in [4, 5, 6, 8, 10]:
        for w_rp in [3, 4, 5, 6]:
            for h_rp in [2, 3, 5, 8]:
                vol_rp = l_rp * w_rp * h_rp
                sa_rp = 2 * (l_rp * w_rp + l_rp * h_rp + w_rp * h_rp)
                
                q_vrp = f"Calculate the volume of a rectangular prism with length $l = {l_rp}$ cm, width $w = {w_rp}$ cm, and height $h = {h_rp}$ cm."
                c_vrp = f"{vol_rp} cm^3"
                d_vrp = [
                    f"{vol_rp * 2} cm^3", f"{vol_rp // 2} cm^3", f"{sa_rp} cm^3",
                    f"{vol_rp + 20} cm^3", f"{vol_rp - 20 if vol_rp > 25 else vol_rp + 40} cm^3",
                    f"{(l_rp + w_rp) * h_rp} cm^3", f"{l_rp * w_rp} cm^3"
                ]
                exp_vrp = f"Prism volume: $V = l \\times w \\times h = {l_rp} \\times {w_rp} \\times {h_rp} = {vol_rp}\\text{{ cm}}^3$."
                add_q("Pyramids & Prisms", "easy", q_vrp, c_vrp, d_vrp, exp_vrp)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Mid-Ordinate Rule Calculations with 4 to 8 Ordinates
    base_ords = [
        [3.2, 4.5, 5.1, 4.8, 3.6],
        [2.4, 3.8, 4.2, 4.0, 3.1, 2.0],
        [4.0, 5.2, 6.1, 5.8, 4.6],
        [5.1, 6.4, 7.2, 6.8, 5.5],
        [2.8, 3.5, 4.1, 4.6, 4.2, 3.7],
        [4.2, 5.6, 6.4, 5.9, 4.8, 3.2],
        [3.0, 4.2, 5.0, 4.8, 3.9],
        [3.6, 4.8, 5.5, 5.1, 4.0],
        [2.5, 3.2, 3.8, 4.0, 3.5, 2.8],
        [4.5, 5.8, 6.5, 6.0, 4.9],
        [3.1, 4.0, 4.7, 4.5, 3.8, 2.9],
        [5.0, 6.2, 7.0, 6.5, 5.2],
        [3.4, 4.6, 5.3, 5.0, 4.1, 3.0],
        [2.2, 3.5, 4.4, 4.8, 4.0, 2.8, 1.8],
        [4.8, 6.0, 6.8, 6.3, 5.1, 3.8],
        [3.8, 5.0, 5.9, 5.6, 4.5, 3.2],
        [2.9, 4.1, 4.9, 4.6, 3.7],
        [4.1, 5.4, 6.2, 5.7, 4.6, 3.4],
        [3.5, 4.7, 5.4, 5.0, 4.2],
        [2.7, 3.9, 4.8, 4.4, 3.5, 2.4]
    ]
    for h_strip in [1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.5, 2.8, 3.0, 3.2, 3.5]:
        for o_idx, ordinates in enumerate(base_ords):
            # Scale slightly with h_strip
            scaled_ords = [round(o * (1 + (h_strip - 1) * 0.1), 2) for o in ordinates]
            sum_m = sum(scaled_ords)
            area_calc = round(h_strip * sum_m, 2)
            ords_str = ", ".join([f"{o} m" for o in scaled_ords])
            
            q_mo = (f"The irregular cross-section of an excavation trench has mid-ordinates of: {ords_str}. "
                    f"The distance between consecutive ordinates is $h = {h_strip}$ m. "
                    f"Calculate the cross-sectional area using the Mid-Ordinate Rule.")
            c_mo = f"{area_calc} m^2"
            d_mo = [
                f"{round(area_calc * 2, 2)} m^2",
                f"{round(area_calc / 2, 2)} m^2",
                f"{round(sum_m, 2)} m^2",
                f"{round(area_calc + 8.5, 2)} m^2",
                f"{round(area_calc - 8.5 if area_calc > 10 else area_calc + 15, 2)} m^2",
                f"{round(h_strip * (scaled_ords[0] + scaled_ords[-1]), 2)} m^2",
                f"{round(area_calc * 1.5, 2)} m^2"
            ]
            exp_mo = (f"Apply the Mid-Ordinate Rule: $\\text{{Area}} = h(m_1 + m_2 + \\dots + m_n)$\n"
                      f"Sum of mid-ordinates $= {' + '.join([str(o) for o in scaled_ords])} = {round(sum_m, 2)}\\text{{ m}}$.\n"
                      f"$\\text{{Area}} = {h_strip} \\times {round(sum_m, 2)} = {area_calc}\\text{{ m}}^2$.")
            add_q("Mid-Ordinate Rule", "medium", q_mo, c_mo, d_mo, exp_mo)

    # 2b. Right Circular Cone Volume & Surface Area
    for r_cn, h_cn, l_cn in [
        (3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25),
        (9, 12, 15), (10, 24, 26), (12, 16, 20), (15, 20, 25), (20, 21, 29),
        (12, 35, 37), (16, 30, 34), (18, 24, 30), (14, 48, 50)
    ]:
        vol_cn = round((1 / 3) * math.pi * (r_cn ** 2) * h_cn, 2)
        csa_cn = round(math.pi * r_cn * l_cn, 2)
        tsa_cn = round(math.pi * r_cn * (r_cn + l_cn), 2)
        
        q_vcn = (f"Calculate the volume of a right circular cone with base radius $r = {r_cn}$ cm and perpendicular height "
                 f"$h = {h_cn}$ cm. (Round to 2 decimal places).")
        c_vcn = f"{vol_cn} cm^3"
        d_vcn = [
            f"{round(vol_cn * 3, 2)} cm^3",
            f"{round(vol_cn / 2, 2)} cm^3",
            f"{round(math.pi * (r_cn**2) * h_cn, 2)} cm^3",
            f"{round(vol_cn + 20, 2)} cm^3",
            f"{round(vol_cn - 20 if vol_cn > 25 else vol_cn + 40, 2)} cm^3",
            f"{round(math.pi * r_cn * l_cn, 2)} cm^3",
            f"{round((1/3) * (r_cn**2) * h_cn, 2)} cm^3"
        ]
        exp_vcn = f"Cone volume formula: $V = \\frac{{1}}{{3}}\\pi r^2 h = \\frac{{1}}{{3}}\\pi({r_cn})^2({h_cn}) = {round((r_cn**2 * h_cn)/3, 2)}\\pi = {vol_cn}\\text{{ cm}}^3$."
        add_q("Right Circular Cones", "medium", q_vcn, c_vcn, d_vcn, exp_vcn)

        q_tcn = (f"Calculate the total surface area of a closed right circular cone with radius $r = {r_cn}$ cm and "
                 f"slant height $l = {l_cn}$ cm. (Round to 2 decimal places).")
        c_tcn = f"{tsa_cn} cm^2"
        d_tcn = [
            f"{round(csa_cn, 2)} cm^2",
            f"{round(tsa_cn * 2, 2)} cm^2",
            f"{round(tsa_cn / 2, 2)} cm^2",
            f"{round(tsa_cn + 15, 2)} cm^2",
            f"{round(tsa_cn - 15 if tsa_cn > 20 else tsa_cn + 30, 2)} cm^2",
            f"{round(math.pi * (r_cn**2), 2)} cm^2",
            f"{round(2 * math.pi * r_cn * l_cn, 2)} cm^2"
        ]
        exp_tcn = (f"Total surface area formula: $A = \\pi r^2 + \\pi rl = \\pi r(r + l)$\n"
                   f"$A = \\pi({r_cn})({r_cn} + {l_cn}) = \\pi({r_cn})({r_cn + l_cn}) = {r_cn * (r_cn + l_cn)}\\pi = {tsa_cn}\\text{{ cm}}^2$.")
        add_q("Right Circular Cones", "medium", q_tcn, c_tcn, d_tcn, exp_tcn)

    # 2c. Square-Based Pyramids
    for b_pyr in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
        for h_pyr in [3, 4, 6, 8, 9, 10, 12, 15, 18]:
            vol_pyr = round((1 / 3) * (b_pyr ** 2) * h_pyr, 2)
            s_pyr = round(math.sqrt(h_pyr**2 + (b_pyr / 2)**2), 2)
            sa_pyr = round(b_pyr**2 + 2 * b_pyr * s_pyr, 2)
            
            q_vpyr = (f"A hopper is shaped as an inverted square-based pyramid with base edge $b = {b_pyr}$ cm and "
                      f"perpendicular height $h = {h_pyr}$ cm. Calculate the capacity (volume) of the hopper.")
            c_vpyr = f"{vol_pyr} cm^3"
            d_vpyr = [
                f"{round(vol_pyr * 3, 2)} cm^3",
                f"{round(vol_pyr / 2, 2)} cm^3",
                f"{round(b_pyr * h_pyr, 2)} cm^3",
                f"{round(vol_pyr + 30, 2)} cm^3",
                f"{round(vol_pyr - 30 if vol_pyr > 35 else vol_pyr + 60, 2)} cm^3",
                f"{b_pyr**2} cm^3",
                f"{round(vol_pyr * 1.5, 2)} cm^3"
            ]
            exp_vpyr = f"Pyramid volume: $V = \\frac{{1}}{{3}} \\times \\text{{Base Area}} \\times h = \\frac{{1}}{{3}}({b_pyr})^2({h_pyr}) = {vol_pyr}\\text{{ cm}}^3$."
            add_q("Pyramids & Prisms", "medium", q_vpyr, c_vpyr, d_vpyr, exp_vpyr)

    # 2d. Cylinder Missing Height or Radius Calculation
    for r_cy in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
        for h_cy in [4, 5, 6, 8, 10, 12, 14, 15, 18, 20]:
            v_cy = round(math.pi * (r_cy ** 2) * h_cy, 2)
            q_hcy = (f"A cylindrical rainwater tank has a storage volume of $V = {v_cy}$ cm^3 and a base radius of $r = {r_cy}$ cm. "
                     f"Calculate the height $h$ of the tank. (Round to 2 decimal places).")
            c_hcy = f"{h_cy} cm"
            d_hcy = [
                f"{h_cy + 2} cm", f"{h_cy - 2 if h_cy > 3 else h_cy + 4} cm",
                f"{round(h_cy * 1.5, 2)} cm", f"{round(h_cy / 2, 2)} cm",
                f"{r_cy} cm", f"{round(v_cy / (r_cy**2), 2)} cm", f"{h_cy * 2} cm"
            ]
            exp_hcy = f"Formula: $V = \\pi r^2 h \\implies h = \\frac{{V}}{{\\pi r^2}} = \\frac{{{v_cy}}}{{\\pi({r_cy})^2}} = {h_cy}\\text{{ cm}}$."
            add_q("Right Circular Cylinders", "medium", q_hcy, c_hcy, d_hcy, exp_hcy)

    # 2e. Cone Missing Height Calculation
    for r_co in [3, 4, 5, 6, 8]:
        for h_co in [6, 9, 12, 15, 18]:
            v_co = round((1 / 3) * math.pi * (r_co ** 2) * h_co, 2)
            q_hco = (f"A conical hopper has a capacity of $V = {v_co}$ cm^3 and a circular rim radius of $r = {r_co}$ cm. "
                     f"Calculate the vertical depth (height) $h$ of the hopper. (Round to 2 decimal places).")
            c_hco = f"{h_co} cm"
            d_hco = [
                f"{h_co + 3} cm", f"{h_co - 3 if h_co > 4 else h_co + 6} cm",
                f"{round(h_co * 1.5, 2)} cm", f"{round(h_co / 2, 2)} cm",
                f"{r_co} cm", f"{round(v_co / (math.pi * r_co**2), 2)} cm", f"{h_co * 2} cm"
            ]
            exp_hco = f"Formula: $V = \\frac{{1}}{{3}}\\pi r^2 h \\implies h = \\frac{{3V}}{{\\pi r^2}} = \\frac{{3({v_co})}}{{\\pi({r_co})^2}} = {h_co}\\text{{ cm}}$."
            add_q("Right Circular Cones", "medium", q_hco, c_hco, d_hco, exp_hco)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Frustum of a Right Circular Cone
    frustum_cases = [
        (6, 3, 8), (8, 4, 10), (10, 5, 12), (7, 3, 9), (9, 4, 12),
        (8, 5, 9), (12, 6, 15), (10, 6, 12), (14, 7, 18), (12, 8, 12),
        (15, 9, 16), (16, 8, 20), (18, 10, 24), (20, 10, 25), (11, 5, 14),
        (13, 7, 15), (15, 10, 12), (16, 12, 10), (18, 12, 16), (20, 12, 20)
    ]
    for R_fr, r_fr, h_fr in frustum_cases:
        bracket = R_fr**2 + R_fr * r_fr + r_fr**2
        vol_fr = round((1 / 3) * math.pi * h_fr * bracket, 2)
        l_fr = round(math.sqrt(h_fr**2 + (R_fr - r_fr)**2), 2)
        csa_fr = round(math.pi * (R_fr + r_fr) * l_fr, 2)
        
        q_vfr = (f"A metallurgical casting ladle is in the shape of a frustum of a cone with top radius $R = {R_fr}$ cm, "
                 f"bottom radius $r = {r_fr}$ cm, and perpendicular height $h = {h_fr}$ cm. "
                 f"Calculate the volume of the ladle. (Round to 2 decimal places).")
        c_vfr = f"{vol_fr} cm^3"
        d_vfr = [
            f"{round(vol_fr * 1.5, 2)} cm^3",
            f"{round(vol_fr / 2, 2)} cm^3",
            f"{round(math.pi * h_fr * (R_fr**2), 2)} cm^3",
            f"{round(vol_fr + 50, 2)} cm^3",
            f"{round(vol_fr - 50 if vol_fr > 60 else vol_fr + 100, 2)} cm^3",
            f"{round(math.pi * ((R_fr + r_fr)/2)**2 * h_fr, 2)} cm^3",
            f"{round(vol_fr * 2, 2)} cm^3"
        ]
        exp_vfr = (f"Formula for the volume of a frustum of a cone:\n"
                   f"$V = \\frac{{1}}{{3}}\\pi h(R^2 + Rr + r^2) = \\frac{{1}}{{3}}\\pi({h_fr})[({R_fr})^2 + ({R_fr})({r_fr}) + ({r_fr})^2]$\n"
                   f"$V = \\frac{{{h_fr}\\pi}}{{3}}[{R_fr**2} + {R_fr * r_fr} + {r_fr**2}] = \\frac{{{h_fr}\\pi}}{{3}}({bracket}) = {vol_fr}\\text{{ cm}}^3$.")
        add_q("Frustums of Cones & Pyramids", "hard", q_vfr, c_vfr, d_vfr, exp_vfr)

        q_csafr = (f"For the frustum of a cone with radii $R = {R_fr}$ cm, $r = {r_fr}$ cm, and height $h = {h_fr}$ cm, "
                   f"calculate the curved (lateral) surface area. (Round to 2 decimal places).")
        c_csafr = f"{csa_fr} cm^2"
        d_csafr = [
            f"{round(csa_fr * 1.5, 2)} cm^2",
            f"{round(csa_fr / 2, 2)} cm^2",
            f"{round(math.pi * (R_fr + r_fr) * h_fr, 2)} cm^2",
            f"{round(csa_fr + 30, 2)} cm^2",
            f"{round(csa_fr - 30 if csa_fr > 35 else csa_fr + 60, 2)} cm^2",
            f"{round(2 * math.pi * R_fr * h_fr, 2)} cm^2",
            f"{round(csa_fr * 2, 2)} cm^2"
        ]
        exp_csafr = (f"Step 1: Slant height $l = \\sqrt{{h^2 + (R - r)^2}} = \\sqrt{{{h_fr}^2 + ({R_fr} - {r_fr})^2}} = \\sqrt{{{h_fr**2} + {(R_fr - r_fr)**2}}} = {l_fr}\\text{{ cm}}$.\n"
                     f"Step 2: Curved area $= \\pi(R + r)l = \\pi({R_fr} + {r_fr})({l_fr}) = \\pi({R_fr + r_fr})({l_fr}) = {csa_fr}\\text{{ cm}}^2$.")
        add_q("Frustums of Cones & Pyramids", "hard", q_csafr, c_csafr, d_csafr, exp_csafr)

    # 3b. Earthworks Excavation Trench Volume via Mid-Ordinate Rule
    trench_cases = [
        (2.0, [2.5, 3.8, 4.5, 4.2, 3.0], 50),
        (1.5, [3.0, 4.2, 5.0, 4.6, 3.5, 2.2], 80),
        (2.5, [3.5, 4.8, 5.8, 5.2, 4.0], 60),
        (3.0, [4.5, 5.8, 6.8, 6.2, 5.0], 100),
        (1.8, [2.8, 4.0, 4.9, 4.5, 3.6], 75),
        (2.2, [3.2, 4.5, 5.2, 4.8, 3.8], 90),
        (1.6, [2.6, 3.6, 4.4, 4.1, 3.2], 120),
        (2.4, [3.8, 5.0, 6.0, 5.5, 4.4], 70),
        (2.0, [3.2, 4.4, 5.1, 4.7, 3.5, 2.6], 85),
        (1.5, [2.8, 3.9, 4.6, 4.2, 3.3, 2.0], 110),
        (2.5, [4.2, 5.6, 6.4, 5.9, 4.5], 95),
        (3.0, [5.0, 6.5, 7.5, 7.0, 5.5], 130),
        (1.8, [3.4, 4.6, 5.5, 5.0, 3.9], 65),
        (2.2, [3.7, 5.0, 5.8, 5.3, 4.2], 105),
        (1.6, [3.0, 4.1, 5.0, 4.5, 3.6, 2.5], 140),
        (2.4, [4.0, 5.4, 6.3, 5.8, 4.6], 80)
    ]
    for h_tr, m_list, L_trench in trench_cases:
        sum_m = sum(m_list)
        area_cs = round(h_tr * sum_m, 2)
        vol_earth = round(area_cs * L_trench, 2)
        m_str = ", ".join([f"{m} m" for m in m_list])
        
        q_tr = (f"A stormwater drainage trench of length $L = {L_trench}$ m has an irregular cross-section. "
                f"The cross-section mid-ordinates spaced at $h = {h_tr}$ m are: {m_str}. "
                f"Using the Mid-Ordinate Rule, calculate the total volume of earth excavated.")
        c_tr = f"{vol_earth} m^3"
        d_tr = [
            f"{round(vol_earth * 1.5, 2)} m^3",
            f"{round(vol_earth / 2, 2)} m^3",
            f"{round(area_cs, 2)} m^3",
            f"{round(vol_earth + 250, 2)} m^3",
            f"{round(vol_earth - 250 if vol_earth > 300 else vol_earth + 500, 2)} m^3",
            f"{round(sum_m * L_trench, 2)} m^3",
            f"{round(vol_earth * 2, 2)} m^3"
        ]
        exp_tr = (f"Step 1: Calculate cross-sectional area via Mid-Ordinate Rule:\n"
                  f"$\\text{{Area}} = h \\sum m_i = {h_tr} \\times ({' + '.join([str(m) for m in m_list])}) = {h_tr} \\times {round(sum_m, 2)} = {area_cs}\\text{{ m}}^2$.\n"
                  f"Step 2: Total excavated volume: $V = \\text{{Area}} \\times L = {area_cs} \\times {L_trench} = {vol_earth}\\text{{ m}}^3$.")
        add_q("Mid-Ordinate Rule", "hard", q_tr, c_tr, d_tr, exp_tr)

    # 3c. Composite Engineering Solids: Cylinder topped with Hemisphere
    for r_comp in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for h_cyl in [6, 8, 10, 12, 15, 18, 20]:
            v_cyl_part = math.pi * (r_comp ** 2) * h_cyl
            v_hemi_part = (2 / 3) * math.pi * (r_comp ** 3)
            tot_v_comp = round(v_cyl_part + v_hemi_part, 2)
            
            q_comp = (f"An industrial storage silo consists of a vertical right cylinder of radius $r = {r_comp}$ m and height "
                      f"$h = {h_cyl}$ m, topped with a hemispherical roof of the same radius. "
                      f"Calculate the total storage volume of the silo. (Round to 2 decimal places).")
            c_comp = f"{tot_v_comp} m^3"
            d_comp = [
                f"{round(v_cyl_part, 2)} m^3",
                f"{round(tot_v_comp * 1.5, 2)} m^3",
                f"{round(tot_v_comp / 2, 2)} m^3",
                f"{round(v_cyl_part + (4/3)*math.pi*(r_comp**3), 2)} m^3",
                f"{round(tot_v_comp + 120, 2)} m^3",
                f"{round(tot_v_comp - 120 if tot_v_comp > 150 else tot_v_comp + 200, 2)} m^3",
                f"{round(math.pi * r_comp**2 * (h_cyl + r_comp), 2)} m^3"
            ]
            exp_comp = (f"Step 1: Cylinder volume: $V_{{1}} = \\pi r^2 h = \\pi({r_comp})^2({h_cyl}) = {round(v_cyl_part, 2)}\\text{{ m}}^3$.\n"
                        f"Step 2: Hemisphere volume: $V_{{2}} = \\frac{{2}}{{3}}\\pi r^3 = \\frac{{2}}{{3}}\\pi({r_comp})^3 = {round(v_hemi_part, 2)}\\text{{ m}}^3$.\n"
                        f"Step 3: Total volume $= V_1 + V_2 = {round(v_cyl_part, 2)} + {round(v_hemi_part, 2)} = {tot_v_comp}\\text{{ m}}^3$.")
            add_q("Composite Engineering Solids", "hard", q_comp, c_comp, d_comp, exp_comp)

    # 3d. Hollow Cylindrical Pipe / Sleeve Volume: V = pi * (R^2 - r^2) * h
    for R_pipe in [6, 8, 10, 12, 15]:
        for r_pipe in [3, 4, 6, 8, 10]:
            if r_pipe >= R_pipe: continue
            for h_pipe in [10, 20, 30, 40, 50]:
                vol_pipe = round(math.pi * (R_pipe**2 - r_pipe**2) * h_pipe, 2)
                
                q_pipe = (f"A bronze cylindrical bearing sleeve has an outer radius $R = {R_pipe}$ cm, an inner bore radius "
                          f"$r = {r_pipe}$ cm, and a length $h = {h_pipe}$ cm. "
                          f"Calculate the volume of metal in the sleeve. (Round to 2 decimal places).")
                c_pipe = f"{vol_pipe} cm^3"
                d_pipe = [
                    f"{round(math.pi * (R_pipe**2) * h_pipe, 2)} cm^3",
                    f"{round(math.pi * (r_pipe**2) * h_pipe, 2)} cm^3",
                    f"{round(vol_pipe * 1.5, 2)} cm^3",
                    f"{round(vol_pipe / 2, 2)} cm^3",
                    f"{round(vol_pipe + 100, 2)} cm^3",
                    f"{round(vol_pipe - 100 if vol_pipe > 150 else vol_pipe + 200, 2)} cm^3",
                    f"{round(math.pi * ((R_pipe - r_pipe)**2) * h_pipe, 2)} cm^3"
                ]
                exp_pipe = (f"Volume of hollow cylinder: $V = \\pi(R^2 - r^2)h = \\pi(({R_pipe})^2 - ({r_pipe})^2)({h_pipe}) "
                            f"= \\pi({R_pipe**2} - {r_pipe**2})({h_pipe}) = \\pi({R_pipe**2 - r_pipe**2})({h_pipe}) = {vol_pipe}\\text{{ cm}}^3$.")
                add_q("Composite Engineering Solids", "hard", q_pipe, c_pipe, d_pipe, exp_pipe)

    print(f"Generated Tech Math Mensuration: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper2_tech_mensuration.json")
    dataset = build_mensuration_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
