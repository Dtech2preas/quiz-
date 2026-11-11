import json
import os
import random
import math
import time

def build_circle_angular_dataset():
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
        q_id = f"TM12_P2_ANG_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Circle Geometry & Angular Movement",
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
                "topic": "Circle Geometry & Angular Movement",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Degrees to Radians Conversions: theta_rad = theta_deg * pi / 180
    deg_cases = [
        (30, "\\frac{\\pi}{6}"), (45, "\\frac{\\pi}{4}"), (60, "\\frac{\\pi}{3}"),
        (90, "\\frac{\\pi}{2}"), (120, "\\frac{2\\pi}{3}"), (135, "\\frac{3\\pi}{4}"),
        (150, "\\frac{5\\pi}{6}"), (180, "\\pi"), (210, "\\frac{7\\pi}{6}"),
        (225, "\\frac{5\\pi}{4}"), (240, "\\frac{4\\pi}{3}"), (270, "\\frac{3\\pi}{2}"),
        (300, "\\frac{5\\pi}{3}"), (315, "\\frac{7\\pi}{4}"), (330, "\\frac{11\\pi}{6}"),
        (360, "2\\pi")
    ]
    for deg_v, rad_ans in deg_cases:
        for idx in range(8):
            q_rad = f"Convert the angle ${deg_v}^\\circ$ into radians in terms of $\\pi$."
            if idx == 1:
                q_rad = f"Express ${deg_v}^\\circ$ in radian measure."
            elif idx == 2:
                q_rad = f"Convert ${deg_v}^\\circ$ to radians (exact value in terms of $\\pi$)."
            elif idx == 3:
                q_rad = f"What is the equivalent radian angle for ${deg_v}^\\circ$?"
            elif idx == 4:
                q_rad = f"Determine the radian measure corresponding to ${deg_v}^\\circ$."
            elif idx == 5:
                q_rad = f"Calculate the radian angle of ${deg_v}^\\circ$."
            elif idx == 6:
                q_rad = f"State ${deg_v}^\\circ$ in radians."
            elif idx == 7:
                q_rad = f"Convert to radians: ${deg_v}^\\circ$."
                
            c_rad = f"${rad_ans}\\text{{ rad}}$"
            d_rad = [
                f"${rad_ans.replace('3', '6')}\\text{{ rad}}$" if "3" in rad_ans else f"${rad_ans.replace('4', '3')}\\text{{ rad}}$",
                f"${rad_ans.replace('2', '4')}\\text{{ rad}}$" if "2" in rad_ans else f"${rad_ans.replace('6', '3')}\\text{{ rad}}$",
                f"${deg_v}\\pi\\text{{ rad}}$",
                f"$\\frac{{{deg_v}}}{{180}}\\text{{ rad}}$",
                f"$\\frac{{\\pi}}{{{deg_v}}}\\text{{ rad}}$",
                f"${round(deg_v * math.pi / 180, 2)}\\text{{ rad}}$",
                f"${rad_ans}\\pi\\text{{ rad}}$"
            ]
            exp_rad = f"Conversion formula: $\\theta_{{\\text{{rad}}}} = \\theta^\\circ \\times \\frac{{\\pi}}{{180^\\circ}} = {deg_v}^\\circ \\times \\frac{{\\pi}}{{180^\\circ}} = {rad_ans}\\text{{ rad}}$."
            add_q("Radian Measure", "easy", q_rad, c_rad, d_rad, exp_rad)

    # 1b. Radians to Degrees Conversions
    for deg_v, rad_ans in deg_cases:
        for idx in range(8):
            q_deg = f"Convert the radian angle ${rad_ans}$ radians into degrees."
            if idx == 1:
                q_deg = f"Express ${rad_ans}$ radians in degrees."
            elif idx == 2:
                q_deg = f"Determine the degree equivalent of ${rad_ans}$ radians."
            elif idx == 3:
                q_deg = f"Calculate the angle in degrees corresponding to ${rad_ans}$ radians."
            elif idx == 4:
                q_deg = f"What is ${rad_ans}$ radians in degrees?"
            elif idx == 5:
                q_deg = f"Convert from radians to degrees: ${rad_ans}$."
            elif idx == 6:
                q_deg = f"Find the degree measure of ${rad_ans}$ radians."
            elif idx == 7:
                q_deg = f"Evaluate in degrees: ${rad_ans}$ rad."
                
            c_deg = f"{deg_v}^\\circ"
            d_deg = [
                f"{deg_v + 30}^\\circ", f"{deg_v - 30 if deg_v > 45 else deg_v + 45}^\\circ",
                f"{round(deg_v / 2, 1)}^\\circ", f"{deg_v * 2}^\\circ",
                f"{180 - deg_v}^\\circ" if deg_v != 90 else "45^\\circ",
                f"{round(deg_v * 1.5, 1)}^\\circ", f"{360 - deg_v}^\\circ"
            ]
            exp_deg = f"Multiply by $\\frac{{180^\\circ}}{{\\pi}}$: ${rad_ans} \\times \\frac{{180^\\circ}}{{\\pi}} = {deg_v}^\\circ$."
            add_q("Radian Measure", "easy", q_deg, c_deg, d_deg, exp_deg)

    # 1c. Circle Theorem Knowledge Statements
    thm_cases = [
        ("The angle subtended by an arc at the centre of a circle is:", "twice the angle subtended by it at the circumference",
         ["equal to the angle subtended at the circumference", "half the angle subtended at the circumference", "always equal to 90 degrees", "equal to 180 degrees", "three times the circumference angle", "four times the circumference angle"]),
        ("The opposite angles of a cyclic quadrilateral are:", "supplementary (add up to 180 degrees)",
         ["complementary (add up to 90 degrees)", "always equal to each other", "alternate angles", "vertically opposite", "always acute", "add up to 360 degrees"]),
        ("An angle subtended by a diameter in a semi-circle is always:", "equal to 90 degrees (a right angle)",
         ["equal to 60 degrees", "equal to 45 degrees", "equal to 180 degrees", "an obtuse angle", "equal to 120 degrees", "an acute angle"]),
        ("According to the Tangent-Chord Theorem, the angle between a tangent to a circle and a chord drawn through the point of contact is equal to:", "the angle subtended by the chord in the alternate segment",
         ["the angle at the centre of the circle", "90 degrees", "half the angle in the alternate segment", "twice the angle at the centre", "the angle opposite the diameter", "the exterior angle of the triangle"]),
        ("The exterior angle of a cyclic quadrilateral is equal to:", "the interior opposite angle",
         ["the interior adjacent angle", "180 degrees", "half the opposite angle", "twice the opposite angle", "90 degrees", "the angle at the centre"])
    ]
    for q_stmt, c_thm, d_thms in thm_cases:
        for idx in range(12):
            q_th = f"In Grade 12 Technical Mathematics circle geometry, complete the theorem statement: {q_stmt}"
            if idx > 0:
                q_th = f"State the official CAPS circle theorem: {q_stmt}"
                if idx > 5:
                    q_th = f"Which statement correctly completes the Euclidean circle theorem: '{q_stmt}'?"
            c_th_ans = c_thm
            d_th_ans = d_thms
            exp_th = f"Official CAPS Euclidean Geometry Theorem: {q_stmt} {c_thm}."
            add_q("Euclidean Circle Geometry Theorems", "easy", q_th, c_th_ans, d_th_ans, exp_th)

    # 1d. Angle at Centre vs Circumference (Basic Calculations)
    for ang_circ in [15, 16, 18, 20, 22, 25, 28, 32, 35, 38, 41, 45, 48, 52, 55, 58, 60, 64, 68, 70, 75, 80]:
        ang_cent = ang_circ * 2
        q_ac = f"An arc of a circle subtends an angle of {ang_circ}$^\\circ$ at the circumference. Calculate the angle subtended by the same arc at the centre."
        c_ac = f"{ang_cent}^\\circ"
        d_ac = [
            f"{ang_circ}^\\circ", f"{round(ang_circ / 2, 1)}^\\circ", f"{180 - ang_circ}^\\circ",
            f"{ang_cent + 10}^\\circ", f"{ang_cent - 10}^\\circ", f"{90 - ang_circ}^\\circ", "90^\\circ"
        ]
        exp_ac = f"Angle at centre theorem: $\\hat{{O}} = 2 \\times \\hat{{A}} = 2 \\times {ang_circ}^\\circ = {ang_cent}^\\circ$."
        add_q("Euclidean Circle Geometry Theorems", "easy", q_ac, c_ac, d_ac, exp_ac)

    # 1e. Cyclic Quad Opposite Angles (Basic Calculations)
    for ang_cq in [55, 60, 65, 70, 72, 75, 80, 85, 90, 95, 100, 105, 110, 115, 118, 120, 125, 130]:
        opp_cq = 180 - ang_cq
        q_cq = f"In cyclic quadrilateral $ABCD$, interior angle $\\hat{{A}} = {ang_cq}^\\circ$. Calculate the magnitude of opposite interior angle $\\hat{{C}}$."
        c_cq = f"{opp_cq}^\\circ"
        d_cq = [
            f"{ang_cq}^\\circ", f"{90 - ang_cq if ang_cq < 90 else ang_cq - 90}^\\circ",
            f"{opp_cq + 10}^\\circ", f"{opp_cq - 10}^\\circ", f"{360 - ang_cq}^\\circ",
            f"{round(ang_cq * 1.5, 1)}^\\circ", "90^\\circ"
        ]
        exp_cq = f"Opposite angles of a cyclic quadrilateral are supplementary: $\\hat{{C}} = 180^\\circ - {ang_cq}^\\circ = {opp_cq}^\\circ$."
        add_q("Euclidean Circle Geometry Theorems", "easy", q_cq, c_cq, d_cq, exp_cq)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Arc Length: s = r * theta (theta in radians)
    for r_arc in [4, 5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 25, 28, 30, 35, 40]:
        for deg_arc in [20, 30, 40, 45, 50, 60, 70, 75, 80, 90, 100, 110, 120, 135, 140, 150, 160]:
            rad_val = deg_arc * math.pi / 180
            s_len = round(r_arc * rad_val, 2)
            
            q_arc = (f"A rotating machine spindle of radius $r = {r_arc}$ cm turns through a central angle of "
                     f"${deg_arc}^\\circ$. Calculate the length of the arc $s$ traversed by a point on the rim. "
                     f"(Round to 2 decimal places).")
            c_arc = f"{s_len} cm"
            d_arc = [
                f"{round(r_arc * deg_arc, 2)} cm",
                f"{round(s_len * 2, 2)} cm",
                f"{round(s_len / 2, 2)} cm",
                f"{round(s_len + 5.5, 2)} cm",
                f"{round(s_len - 5.5 if s_len > 6 else s_len + 10, 2)} cm",
                f"{round(r_arc * math.pi, 2)} cm",
                f"{round(2 * math.pi * r_arc, 2)} cm"
            ]
            exp_arc = (f"Step 1: Convert angle to radians: $\\theta = {deg_arc}^\\circ \\times \\frac{{\\pi}}{{180^\\circ}} = {round(rad_val, 4)}\\text{{ rad}}$.\n"
                       f"Step 2: Calculate arc length: $s = r\\theta = {r_arc} \\times {round(rad_val, 4)} = {s_len}\\text{{ cm}}$.")
            add_q("Arc Length & Sector Area", "medium", q_arc, c_arc, d_arc, exp_arc)

    # 2b. Sector Area: A = 1/2 * r^2 * theta
    for r_sec in [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20]:
        for deg_sec in [25, 30, 35, 45, 50, 60, 70, 75, 80, 90, 100, 110, 120, 135, 140, 150]:
            rad_sec = deg_sec * math.pi / 180
            area_sec = round(0.5 * (r_sec ** 2) * rad_sec, 2)
            
            q_sec = (f"Calculate the area of a circular sector of radius $r = {r_sec}$ cm subtending a central angle "
                     f"of ${deg_sec}^\\circ$. (Round to 2 decimal places).")
            c_sec = f"{area_sec} cm^2"
            d_sec = [
                f"{round(area_sec * 2, 2)} cm^2",
                f"{round(area_sec / 2, 2)} cm^2",
                f"{round(math.pi * r_sec**2, 2)} cm^2",
                f"{round(area_sec + 12.5, 2)} cm^2",
                f"{round(area_sec - 12.5 if area_sec > 15 else area_sec + 25, 2)} cm^2",
                f"{round(r_sec * rad_sec, 2)} cm^2",
                f"{round(0.5 * r_sec * deg_sec, 2)} cm^2"
            ]
            exp_sec = (f"Step 1: Angle in radians: $\\theta = {deg_sec}^\\circ \\times \\frac{{\\pi}}{{180^\\circ}} = {round(rad_sec, 4)}\\text{{ rad}}$.\n"
                       f"Step 2: Area $= \\frac{{1}}{{2}}r^2\\theta = \\frac{{1}}{{2}}({r_sec})^2({round(rad_sec, 4)}) = {area_sec}\\text{{ cm}}^2$.")
            add_q("Arc Length & Sector Area", "medium", q_sec, c_sec, d_sec, exp_sec)

    # 2c. Angular Velocity from Rotational Frequency (rpm to rad/s): omega = 2 * pi * n
    for rpm in [120, 180, 240, 300, 360, 450, 600, 720, 900, 1200, 1500, 1800, 2400, 3000]:
        n_rps = rpm / 60
        omega_exact = round(2 * math.pi * n_rps, 2)
        
        q_om = (f"An electric motor shaft rotates at a speed of {rpm} revolutions per minute (rpm). "
                f"Calculate the angular velocity $\\omega$ in radians per second (rad/s). (Round to 2 decimal places).")
        c_om = f"{omega_exact} rad/s"
        d_om = [
            f"{round(omega_exact * 2, 2)} rad/s",
            f"{round(omega_exact / 2, 2)} rad/s",
            f"{rpm} rad/s",
            f"{round(n_rps, 2)} rad/s",
            f"{round(omega_exact + 15, 2)} rad/s",
            f"{round(omega_exact - 15 if omega_exact > 20 else omega_exact + 30, 2)} rad/s",
            f"{round(rpm * math.pi, 2)} rad/s"
        ]
        exp_om = (f"Step 1: Rotational frequency in rev/s: $n = \\frac{{\\text{{rpm}}}}{{60}} = \\frac{{{rpm}}}{{60}} = {round(n_rps, 2)}\\text{{ r/s}}$.\n"
                  f"Step 2: Angular velocity: $\\omega = 2\\pi n = 2\\pi({round(n_rps, 2)}) = {omega_exact}\\text{{ rad/s}}$.")
        add_q("Angular Movement & Velocities", "medium", q_om, c_om, d_om, exp_om)

    # 2d. Peripheral / Circumferential Velocity: v = r * omega
    for r_wheel in [0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6]:
        for omega_w in [20, 30, 40, 50, 60, 80, 100]:
            v_lin = round(r_wheel * omega_w, 2)
            
            q_v = (f"A flywheel of radius $r = {r_wheel}$ m rotates with an angular velocity of $\\omega = {omega_w}$ rad/s. "
                   f"Calculate the circumferential (linear) velocity $v$ of a point on the outer rim.")
            c_v = f"{v_lin} m/s"
            d_v = [
                f"{round(v_lin * 2, 2)} m/s",
                f"{round(v_lin / 2, 2)} m/s",
                f"{round(omega_w / r_wheel, 2)} m/s",
                f"{round(v_lin + 5, 2)} m/s",
                f"{round(v_lin - 5 if v_lin > 6 else v_lin + 10, 2)} m/s",
                f"{round(2 * math.pi * r_wheel * omega_w, 2)} m/s",
                f"{omega_w} m/s"
            ]
            exp_v = (f"Circumferential velocity formula: $v = r\\omega = {r_wheel} \\times {omega_w} = {v_lin}\\text{{ m/s}}$.")
            add_q("Angular Movement & Velocities", "medium", q_v, c_v, d_v, exp_v)

    # 2e. Tangent-Chord Theorem Numerical Calculations
    for alpha in [34, 42, 48, 53, 58, 62, 67, 71, 75, 82]:
        for var_tc in range(6):
            q_tc = (f"Tangent line $PT$ touches a circle at point $T$. Chord $TC$ subtends an angle $\\hat{{B}}$ "
                    f"in the alternate segment. If the angle between the tangent and the chord is $\\angle PTC = {alpha}^\\circ$, "
                    f"determine the magnitude of $\\hat{{B}}$.")
            if var_tc == 1:
                q_tc = f"In the given circle, tangent $ST$ touches at $T$. If $\\angle STB = {alpha}^\\circ$, calculate the subtended angle in the alternate segment."
            elif var_tc == 2:
                q_tc = f"A tangent touches a circle at $A$. The angle between the tangent and chord $AB$ is {alpha}$^\\circ$. What is the alternate segment angle?"
            elif var_tc == 3:
                q_tc = f"Calculate the alternate segment angle subtended by chord $AB$ given that the tangent-chord angle is {alpha}$^\\circ$."
            elif var_tc == 4:
                q_tc = f"According to the Tangent-Chord Theorem, if the angle between tangent and chord is {alpha}$^\\circ$, determine the angle in the alternate segment."
            elif var_tc == 5:
                q_tc = f"Find the value of the angle subtended by chord $XY$ in the alternate segment if tangent angle $\\theta = {alpha}^\\circ$."
                
            c_tc = f"{alpha}^\\circ"
            d_tc = [
                f"{180 - alpha}^\\circ", f"{90 - alpha}^\\circ", f"{alpha * 2}^\\circ",
                f"{round(alpha / 2, 1)}^\\circ", f"{alpha + 15}^\\circ", f"{alpha - 15}^\\circ", "90^\\circ"
            ]
            exp_tc = f"By the Tangent-Chord Theorem, the angle between tangent and chord equals the angle subtended by the chord in the alternate segment: $\\hat{{B}} = {alpha}^\\circ$."
            add_q("Euclidean Circle Geometry Theorems", "medium", q_tc, c_tc, d_tc, exp_tc)

    # 2f. Peripheral Velocity: v = pi * D * n
    for D_m in [0.4, 0.5, 0.6, 0.75, 0.8, 1.0, 1.2, 1.5]:
        for n_speed in [5, 10, 15, 20, 25, 30]:
            v_peri = round(math.pi * D_m * n_speed, 2)
            q_peri = (f"A grinding wheel has an outer diameter of $D = {D_m}$ m and rotates at $n = {n_speed}$ revolutions per second (r/s). "
                      f"Calculate the peripheral (cutting) speed $v$ in metres per second. (Round to 2 decimal places).")
            c_peri = f"{v_peri} m/s"
            d_peri = [
                f"{round(v_peri * 2, 2)} m/s",
                f"{round(v_peri / 2, 2)} m/s",
                f"{round(D_m * n_speed, 2)} m/s",
                f"{round(v_peri + 8.5, 2)} m/s",
                f"{round(v_peri - 8.5 if v_peri > 10 else v_peri + 15, 2)} m/s",
                f"{round(math.pi * (D_m/2) * n_speed, 2)} m/s",
                f"{n_speed} m/s"
            ]
            exp_peri = (f"Formula for peripheral velocity: $v = \\pi D n = \\pi \\times {D_m} \\times {n_speed} = {v_peri}\\text{{ m/s}}$.")
            add_q("Angular Movement & Velocities", "medium", q_peri, c_peri, d_peri, exp_peri)

    # 2g. Exterior Angle of Cyclic Quad Calculations
    for ext_ang in [74, 82, 88, 96, 104, 112, 120, 128]:
        for var_ext in range(5):
            q_ext = f"In cyclic quadrilateral $PQRS$, side $QR$ is extended to point $T$. If the exterior angle $\\angle SRT = {ext_ang}^\\circ$, calculate the interior opposite angle $\\hat{{P}}$."
            if var_ext == 1:
                q_ext = f"Side $AB$ of cyclic quad $ABCD$ is produced to $E$. If exterior angle $\\angle CBE = {ext_ang}^\\circ$, determine $\\hat{{D}}$."
            elif var_ext == 2:
                q_ext = f"Calculate the interior opposite angle of a cyclic quadrilateral having an exterior angle of {ext_ang}$^\\circ$."
            elif var_ext == 3:
                q_ext = f"Given exterior angle $\\angle X = {ext_ang}^\\circ$ of cyclic quad $WXYZ$, determine the opposite interior angle."
            elif var_ext == 4:
                q_ext = f"Determine the magnitude of the interior opposite angle of a cyclic quad when the exterior angle measures {ext_ang}$^\\circ$."
                
            c_ext = f"{ext_ang}^\\circ"
            d_ext = [
                f"{180 - ext_ang}^\\circ", f"{round(ext_ang / 2, 1)}^\\circ", f"{ext_ang * 2}^\\circ",
                f"{ext_ang + 20}^\\circ", f"{ext_ang - 20}^\\circ", f"{90 - ext_ang if ext_ang < 90 else ext_ang - 90}^\\circ", "90^\\circ"
            ]
            exp_ext = f"The exterior angle of a cyclic quadrilateral equals the interior opposite angle: $\\hat{{P}} = {ext_ang}^\\circ$."
            add_q("Euclidean Circle Geometry Theorems", "medium", q_ext, c_ext, d_ext, exp_ext)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Belt Drive and Pulley Systems: D1 * n1 = D2 * n2
    for D1 in [100, 120, 150, 180, 200, 240, 300]:
        for n1_rpm in [600, 900, 1200, 1440, 1800]:
            for ratio_p in [1.5, 2.0, 2.5, 3.0]:
                D2 = int(D1 * ratio_p)
                # D1 * n1 = D2 * n2 => n2 = (D1 * n1) / D2 = n1 / ratio_p
                n2_rpm = round(n1_rpm / ratio_p, 1)
                
                q_pul = (f"A motor pulley of diameter $D_1 = {D1}$ mm rotating at $n_1 = {n1_rpm}$ rpm is connected via a flat belt "
                         f"to a driven machine pulley of diameter $D_2 = {D2}$ mm. Assuming no belt slippage, calculate the "
                         f"rotational speed $n_2$ of the driven pulley in rpm.")
                c_pul = f"{n2_rpm} rpm"
                d_pul = [
                    f"{round(n1_rpm * ratio_p, 1)} rpm",
                    f"{n1_rpm} rpm",
                    f"{round(n2_rpm * 1.5, 1)} rpm",
                    f"{round(n2_rpm * 0.5, 1)} rpm",
                    f"{round(n2_rpm + 150, 1)} rpm",
                    f"{round(n2_rpm - 150 if n2_rpm > 200 else n2_rpm + 300, 1)} rpm",
                    f"{round((D1 + D2) * 2, 1)} rpm"
                ]
                exp_pul = (f"Since the linear speed of the belt is constant across both pulleys: $v_1 = v_2 \\implies \\pi D_1 n_1 = \\pi D_2 n_2$.\n"
                           f"$D_1 n_1 = D_2 n_2 \\implies n_2 = \\frac{{D_1 \\times n_1}}{{D_2}} = \\frac{{{D1} \\times {n1_rpm}}}{{{D2}}} = {n2_rpm}\\text{{ rpm}}$.")
                add_q("Belt Drives & Pulleys", "hard", q_pul, c_pul, d_pul, exp_pul)

    # 3b. Gear Trains: N1 * T1 = N2 * T2
    for T1 in [16, 18, 20, 24, 30]:
        for T2 in [36, 40, 48, 60, 72]:
            for N1 in [300, 450, 600, 900, 1200]:
                N2 = round((N1 * T1) / T2, 1)
                
                q_gear = (f"A driver gear with $T_1 = {T1}$ teeth rotates at $N_1 = {N1}$ rpm and meshes with a driven gear "
                          f"having $T_2 = {T2}$ teeth. Calculate the rotational speed $N_2$ of the driven gear in rpm.")
                c_gear = f"{N2} rpm"
                d_gear = [
                    f"{round((N1 * T2) / T1, 1)} rpm",
                    f"{N1} rpm",
                    f"{round(N2 * 1.5, 1)} rpm",
                    f"{round(N2 * 0.5, 1)} rpm",
                    f"{round(N2 + 80, 1)} rpm",
                    f"{round(N2 - 80 if N2 > 100 else N2 + 150, 1)} rpm",
                    f"{T1 + T2} rpm"
                ]
                exp_gear = (f"Use the gear ratio formula: $N_1 T_1 = N_2 T_2 \\implies N_2 = \\frac{{N_1 \\times T_1}}{{T_2}} "
                            f"= \\frac{{{N1} \\times {T1}}}{{{T2}}} = {N2}\\text{{ rpm}}$.")
                add_q("Gear Systems", "hard", q_gear, c_gear, d_gear, exp_gear)

    # 3c. Area of Circular Segment: A_seg = 1/2 * r^2 * (theta - sin theta)
    for r_seg in [6, 8, 10, 12, 15]:
        for deg_sg in [60, 90, 120]:
            rad_sg = deg_sg * math.pi / 180
            # A_seg = 0.5 * r^2 * (rad - sin(rad))
            area_seg = round(0.5 * (r_seg ** 2) * (rad_sg - math.sin(rad_sg)), 2)
            
            q_seg = (f"Calculate the area of a circular segment bounded by a chord subtending an angle of ${deg_sg}^\\circ$ "
                     f"at the centre of a circle with radius $r = {r_seg}$ cm. (Round to 2 decimal places).")
            c_seg = f"{area_seg} cm^2"
            d_seg = [
                f"{round(0.5 * (r_seg**2) * rad_sg, 2)} cm^2",
                f"{round(0.5 * (r_seg**2) * math.sin(rad_sg), 2)} cm^2",
                f"{round(area_seg * 2, 2)} cm^2",
                f"{round(area_seg / 2, 2)} cm^2",
                f"{round(area_seg + 8.5, 2)} cm^2",
                f"{round(area_seg - 8.5 if area_seg > 10 else area_seg + 15, 2)} cm^2",
                f"{round(math.pi * r_seg**2, 2)} cm^2"
            ]
            exp_seg = (f"Step 1: Convert central angle to radians: $\\theta = {deg_sg}^\\circ \\times \\frac{{\\pi}}{{180^\\circ}} = {round(rad_sg, 4)}\\text{{ rad}}$.\n"
                       f"Step 2: Area of sector: $A_{{\\text{{sector}}}} = \\frac{{1}}{{2}}r^2\\theta = {round(0.5 * r_seg**2 * rad_sg, 2)}\\text{{ cm}}^2$.\n"
                       f"Step 3: Area of triangle: $A_{{\\triangle}} = \\frac{{1}}{{2}}r^2\\sin\\theta = {round(0.5 * r_seg**2 * math.sin(rad_sg), 2)}\\text{{ cm}}^2$.\n"
                       f"Step 4: Segment area $= A_{{\\text{{sector}}}} - A_{{\\triangle}} = {area_seg}\\text{{ cm}}^2$.")
            add_q("Circle Segments", "hard", q_seg, c_seg, d_seg, exp_seg)

    print(f"Generated Tech Math Circle & Angular: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper2_tech_circle_angular.json")
    dataset = build_circle_angular_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
