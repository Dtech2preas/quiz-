import json
import os
import random
import math
import time

def build_trig_dataset():
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
        q_id = f"TM12_P2_TRIG_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Trigonometry",
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
                "topic": "Trigonometry",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Reciprocal Ratios Definitions
    recip_defs = [
        ("\\sec \\theta", "\\frac{1}{\\cos \\theta}", ["\\frac{1}{\\sin \\theta}", "\\frac{1}{\\tan \\theta}", "\\frac{\\sin \\theta}{\\cos \\theta}", "1 - \\cos \\theta", "\\cos(-\\theta)", "\\frac{1}{\\cot \\theta}", "\\tan \\theta"]),
        ("\\operatorname{cosec} \\theta", "\\frac{1}{\\sin \\theta}", ["\\frac{1}{\\cos \\theta}", "\\frac{1}{\\tan \\theta}", "\\frac{\\cos \\theta}{\\sin \\theta}", "1 - \\sin \\theta", "\\sin(-\\theta)", "\\frac{1}{\\sec \\theta}", "\\cos \\theta"]),
        ("\\cot \\theta", "\\frac{1}{\\tan \\theta}", ["\\frac{1}{\\sin \\theta}", "\\frac{1}{\\cos \\theta}", "\\tan(-\\theta)", "1 - \\tan \\theta", "\\frac{\\sin \\theta}{\\cos \\theta}", "\\sec \\theta", "\\operatorname{cosec} \\theta"]),
        ("\\cot \\theta", "\\frac{\\cos \\theta}{\\sin \\theta}", ["\\frac{\\sin \\theta}{\\cos \\theta}", "\\frac{1}{\\cos \\theta}", "\\frac{1}{\\sin \\theta}", "\\sin \\theta \\cos \\theta", "1 + \\tan \\theta", "\\sec^2 \\theta", "\\tan \\theta"])
    ]
    for expr, ans_def, wrongs in recip_defs:
        for var_i in range(12):
            q_def = f"In Technical Mathematics, which expression is strictly equivalent to the reciprocal ratio ${expr}$?"
            if var_i == 1:
                q_def = f"State the primary ratio definition of the reciprocal trigonometric ratio ${expr}$."
            elif var_i == 2:
                q_def = f"By definition of reciprocal trigonometric ratios, ${expr}$ is identical to:"
            elif var_i == 3:
                q_def = f"Which of the following identities correctly defines ${expr}$?"
            elif var_i == 4:
                q_def = f"Express the reciprocal function ${expr}$ in terms of basic trigonometric ratios."
            elif var_i == 5:
                q_def = f"According to CAPS examination standards, ${expr}$ simplifies directly to:"
            elif var_i == 6:
                q_def = f"Simplify the trigonometric expression into fundamental ratios: ${expr}$."
            elif var_i == 7:
                q_def = f"Identify the correct formula that defines ${expr}$."
            elif var_i == 8:
                q_def = f"What is the mathematical equivalent of the reciprocal ratio ${expr}$?"
            elif var_i == 9:
                q_def = f"Convert the reciprocal ratio ${expr}$ to its quotient definition."
            elif var_i == 10:
                q_def = f"Select the true trigonometric identity corresponding to ${expr}$."
            elif var_i == 11:
                q_def = f"In terms of sine and cosine, the ratio ${expr}$ equals:"
                
            c_def = f"${ans_def}$"
            d_def = [f"${w}$" for w in wrongs]
            exp_def = f"The reciprocal trigonometric ratio ${expr}$ is defined as ${ans_def}$."
            add_q("Reciprocal Ratios", "easy", q_def, c_def, d_def, exp_def)

    # 1b. Special Angles with Reciprocal Ratios
    special_cases = [
        ("\\sec 60^\\circ", "2", ["\\frac{1}{2}", "\\sqrt{3}", "\\frac{2}{\\sqrt{3}}", "1", "\\sqrt{2}", "0", "\\frac{\\sqrt{3}}{2}"]),
        ("\\sec 30^\\circ", "\\frac{2}{\\sqrt{3}}", ["\\frac{\\sqrt{3}}{2}", "2", "\\frac{1}{2}", "\\sqrt{3}", "1", "\\sqrt{2}", "0"]),
        ("\\sec 45^\\circ", "\\sqrt{2}", ["\\frac{1}{\\sqrt{2}}", "\\frac{\\sqrt{2}}{2}", "2", "1", "\\sqrt{3}", "\\frac{2}{\\sqrt{3}}", "0"]),
        ("\\operatorname{cosec} 30^\\circ", "2", ["\\frac{1}{2}", "\\sqrt{3}", "\\frac{2}{\\sqrt{3}}", "1", "\\sqrt{2}", "0", "\\frac{\\sqrt{3}}{2}"]),
        ("\\operatorname{cosec} 60^\\circ", "\\frac{2}{\\sqrt{3}}", ["\\frac{\\sqrt{3}}{2}", "2", "\\frac{1}{2}", "\\sqrt{3}", "1", "\\sqrt{2}", "0"]),
        ("\\operatorname{cosec} 45^\\circ", "\\sqrt{2}", ["\\frac{1}{\\sqrt{2}}", "2", "1", "\\frac{\\sqrt{2}}{2}", "\\sqrt{3}", "0", "\\frac{1}{2}"]),
        ("\\cot 45^\\circ", "1", ["0", "\\sqrt{3}", "\\frac{1}{\\sqrt{3}}", "2", "\\sqrt{2}", "-1", "\\frac{1}{2}"]),
        ("\\cot 60^\\circ", "\\frac{1}{\\sqrt{3}}", ["\\sqrt{3}", "1", "0", "2", "\\frac{2}{\\sqrt{3}}", "\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}"]),
        ("\\cot 30^\\circ", "\\sqrt{3}", ["\\frac{1}{\\sqrt{3}}", "1", "0", "2", "\\frac{2}{\\sqrt{3}}", "\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}"])
    ]
    for fn_str, c_val, d_vals in special_cases:
        for idx in range(12):
            q_sp = f"Without using a calculator, evaluate the exact value of ${fn_str}$."
            if idx == 1:
                q_sp = f"Determine the exact value of ${fn_str}$ using special angles."
            elif idx == 2:
                q_sp = f"Calculate the precise numerical value of ${fn_str}$ without a calculator."
            elif idx == 3:
                q_sp = f"Evaluate the special angle ratio: ${fn_str}$."
            elif idx == 4:
                q_sp = f"Find the exact surd value of ${fn_str}$."
            elif idx == 5:
                q_sp = f"What is the exact value of the expression ${fn_str}$?"
            elif idx == 6:
                q_sp = f"State the exact value of ${fn_str}$ derived from standard special triangles."
            elif idx == 7:
                q_sp = f"Without a calculator, determine ${fn_str}$."
            elif idx == 8:
                q_sp = f"Calculate the exact trigonometric value: ${fn_str}$."
            elif idx == 9:
                q_sp = f"Simplify the exact ratio: ${fn_str}$."
            elif idx == 10:
                q_sp = f"Express ${fn_str}$ as an exact rational or surd number."
            elif idx == 11:
                q_sp = f"Find the value of ${fn_str}$ using special angle ratios."
                
            c_ans = f"${c_val}$"
            d_ans = [f"${d}$" for d in d_vals]
            exp_sp = f"Evaluate using special angles: ${fn_str} = {c_val}$."
            add_q("Special Angles", "easy", q_sp, c_ans, d_ans, exp_sp)

    # 1c. Signs in Quadrants (CAST rule)
    quad_cases = [
        ("In the third quadrant ($180^\\circ < \\theta < 270^\\circ$), which reciprocal ratio is positive?", "\\cot \\theta", ["\\sec \\theta", "\\operatorname{cosec} \\theta", "\\sin \\theta", "\\cos \\theta", "None", "\\sec^2 \\theta"]),
        ("In the fourth quadrant ($270^\\circ < \\theta < 360^\\circ$), which reciprocal ratio is positive?", "\\sec \\theta", ["\\cot \\theta", "\\operatorname{cosec} \\theta", "\\sin \\theta", "\\tan \\theta", "None", "\\cot^2 \\theta"]),
        ("In the second quadrant ($90^\\circ < \\theta < 180^\\circ$), which reciprocal ratio is positive?", "\\operatorname{cosec} \\theta", ["\\sec \\theta", "\\cot \\theta", "\\cos \\theta", "\\tan \\theta", "None", "\\sec \\theta \\cot \\theta"])
    ]
    for q_txt, c_quad, d_quads in quad_cases:
        for idx in range(16):
            q_q = q_txt if idx == 0 else f"{q_txt.replace('?', '')} according to the CAST rule (Variation {idx+1})?"
            q_q_clean = q_q.replace(f" (Variation {idx+1})", "")
            if idx > 0:
                q_q_clean = f"Applying the CAST diagram, {q_txt.lower()}"
                if idx > 8:
                    q_q_clean = f"Determine which reciprocal ratio is positive: {q_txt.split(',')[0]}."
            c_q_ans = f"${c_quad}$"
            d_q_ans = [f"${d}$" for d in d_quads]
            exp_q = f"According to the CAST rule, tangent and cotangent are positive in Q3, cosine and secant in Q4, and sine and cosecant in Q2."
            add_q("CAST Diagram & Quadrants", "easy", q_q_clean, c_q_ans, d_q_ans, exp_q)

    # 1d. Reciprocal Values from Given Ratios (Pythagorean Triples)
    pyth_cases_easy = [
        (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
        (9, 40, 41), (20, 21, 29), (12, 35, 37), (10, 24, 26),
        (6, 8, 10), (9, 12, 15), (15, 20, 25), (16, 30, 34)
    ]
    for x_p, y_p, r_p in pyth_cases_easy:
        # sec theta = r / x
        q_sec = f"If $\\theta$ is an acute angle and $\\cos \\theta = \\frac{{{x_p}}}{{{r_p}}}$, determine the value of $\\sec \\theta$."
        c_sec = f"\\frac{{{r_p}}}{{{x_p}}}"
        d_sec = [
            f"\\frac{{{x_p}}}{{{r_p}}}", f"\\frac{{{y_p}}}{{{r_p}}}", f"\\frac{{{r_p}}}{{{y_p}}}",
            f"\\frac{{{y_p}}}{{{x_p}}}", f"\\frac{{{x_p}}}{{{y_p}}}", "1", f"\\frac{{{r_p + 1}}}{{{x_p}}}"
        ]
        exp_sec = f"By definition of the reciprocal ratio: $\\sec \\theta = \\frac{{1}}{{\\cos \\theta}} = \\frac{{1}}{{{x_p}/{r_p}}} = \\frac{{{r_p}}}{{{x_p}}}$."
        add_q("Reciprocal Ratios", "easy", q_sec, f"${c_sec}$", [f"${d}$" for d in d_sec], exp_sec)

        # cosec theta = r / y
        q_csc = f"If $\\theta$ is an acute angle and $\\sin \\theta = \\frac{{{y_p}}}{{{r_p}}}$, determine the value of $\\operatorname{{cosec}} \\theta$."
        c_csc = f"\\frac{{{r_p}}}{{{y_p}}}"
        d_csc = [
            f"\\frac{{{y_p}}}{{{r_p}}}", f"\\frac{{{x_p}}}{{{r_p}}}", f"\\frac{{{r_p}}}{{{x_p}}}",
            f"\\frac{{{x_p}}}{{{y_p}}}", f"\\frac{{{y_p}}}{{{x_p}}}", "1", f"\\frac{{{r_p + 2}}}{{{y_p}}}"
        ]
        exp_csc = f"By definition of the cosecant ratio: $\\operatorname{{cosec}} \\theta = \\frac{{1}}{{\\sin \\theta}} = \\frac{{1}}{{{y_p}/{r_p}}} = \\frac{{{r_p}}}{{{y_p}}}$."
        add_q("Reciprocal Ratios", "easy", q_csc, f"${c_csc}$", [f"${d}$" for d in d_csc], exp_csc)

        # cot theta = x / y
        q_cot = f"If $\\theta$ is an acute angle and $\\tan \\theta = \\frac{{{y_p}}}{{{x_p}}}$, determine the value of $\\cot \\theta$."
        c_cot = f"\\frac{{{x_p}}}{{{y_p}}}"
        d_cot = [
            f"\\frac{{{y_p}}}{{{x_p}}}", f"\\frac{{{r_p}}}{{{x_p}}}", f"\\frac{{{x_p}}}{{{r_p}}}",
            f"\\frac{{{r_p}}}{{{y_p}}}", f"\\frac{{{y_p}}}{{{r_p}}}", "1", f"\\frac{{{x_p + 1}}}{{{y_p}}}"
        ]
        exp_cot = f"By definition of cotangent: $\\cot \\theta = \\frac{{1}}{{\\tan \\theta}} = \\frac{{1}}{{{y_p}/{x_p}}} = \\frac{{{x_p}}}{{{y_p}}}$."
        add_q("Reciprocal Ratios", "easy", q_cot, f"${c_cot}$", [f"${d}$" for d in d_cot], exp_cot)

    # 1e. Standard Quadrantal Angles & Co-ratio Identities
    quadrantal_cases = [
        ("\\sin 0^\\circ", "0", ["1", "-1", "\\frac{1}{2}", "\\sqrt{2}", "\\text{undefined}", "\\frac{\\sqrt{3}}{2}"]),
        ("\\sin 90^\\circ", "1", ["0", "-1", "\\frac{1}{2}", "\\text{undefined}", "\\sqrt{2}", "2"]),
        ("\\cos 0^\\circ", "1", ["0", "-1", "\\frac{1}{2}", "\\text{undefined}", "2", "\\frac{\\sqrt{3}}{2}"]),
        ("\\cos 90^\\circ", "0", ["1", "-1", "\\frac{1}{2}", "\\text{undefined}", "\\sqrt{3}", "2"]),
        ("\\cos 180^\\circ", "-1", ["1", "0", "\\frac{1}{2}", "-\\frac{1}{2}", "\\text{undefined}", "2"]),
        ("\\sin 270^\\circ", "-1", ["1", "0", "-\\frac{1}{2}", "\\frac{1}{2}", "\\text{undefined}", "-2"]),
        ("\\tan 0^\\circ", "0", ["1", "-1", "\\text{undefined}", "\\frac{1}{\\sqrt{3}}", "\\sqrt{3}", "2"]),
        ("\\tan 45^\\circ", "1", ["0", "-1", "\\sqrt{3}", "\\frac{1}{\\sqrt{3}}", "2", "\\frac{1}{2}"])
    ]
    for fn_str, c_val, d_vals in quadrantal_cases:
        for idx in range(15):
            q_qd = f"Evaluate the exact trigonometric value: ${fn_str}$."
            if idx == 1:
                q_qd = f"Determine the exact value of ${fn_str}$."
            elif idx == 2:
                q_qd = f"Without using a calculator, what is the value of ${fn_str}$?"
            elif idx == 3:
                q_qd = f"State the exact numerical value of ${fn_str}$."
            elif idx == 4:
                q_qd = f"Evaluate: ${fn_str}$."
            elif idx == 5:
                q_qd = f"Calculate: ${fn_str}$."
            elif idx == 6:
                q_qd = f"What is ${fn_str}$ equal to?"
            elif idx == 7:
                q_qd = f"Find the value of the quadrantal ratio: ${fn_str}$."
            elif idx == 8:
                q_qd = f"Determine ${fn_str}$ from the unit circle."
            elif idx == 9:
                q_qd = f"Express the exact value of ${fn_str}$."
            elif idx == 10:
                q_qd = f"What is the exact value of ${fn_str}$?"
            elif idx == 11:
                q_qd = f"Simplify the trigonometric term: ${fn_str}$."
            elif idx == 12:
                q_qd = f"Find the numerical result of: ${fn_str}$."
            elif idx == 13:
                q_qd = f"Evaluate the angle ratio: ${fn_str}$."
            elif idx == 14:
                q_qd = f"State the value of: ${fn_str}$."
                
            c_ans = f"${c_val}$"
            d_ans = [f"${d}$" for d in d_vals]
            exp_qd = f"By definition of the unit circle: ${fn_str} = {c_val}$."
            add_q("Special Angles", "easy", q_qd, c_ans, d_ans, exp_qd)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Reduction Formulas
    red_cases = [
        ("\\sin(180^\\circ - x)", "\\sin x", ["-\\sin x", "\\cos x", "-\\cos x", "\\sec x", "\\tan x", "1"]),
        ("\\cos(180^\\circ - x)", "-\\cos x", ["\\cos x", "\\sin x", "-\\sin x", "-\\sec x", "0", "1"]),
        ("\\tan(180^\\circ - x)", "-\\tan x", ["\\tan x", "\\cot x", "-\\cot x", "\\sin x", "0", "1"]),
        ("\\sin(180^\\circ + x)", "-\\sin x", ["\\sin x", "\\cos x", "-\\cos x", "-\\operatorname{cosec} x", "0", "1"]),
        ("\\cos(180^\\circ + x)", "-\\cos x", ["\\cos x", "\\sin x", "-\\sin x", "-\\sec x", "0", "1"]),
        ("\\tan(180^\\circ + x)", "\\tan x", ["-\\tan x", "\\cot x", "-\\cot x", "\\cos x", "0", "1"]),
        ("\\sin(360^\\circ - x)", "-\\sin x", ["\\sin x", "\\cos x", "-\\cos x", "-\\operatorname{cosec} x", "0", "1"]),
        ("\\cos(360^\\circ - x)", "\\cos x", ["-\\cos x", "\\sin x", "-\\sin x", "\\sec x", "0", "1"]),
        ("\\tan(360^\\circ - x)", "-\\tan x", ["\\tan x", "\\cot x", "-\\cot x", "-\\sin x", "0", "1"]),
        ("\\sin(90^\\circ + x)", "\\cos x", ["-\\cos x", "\\sin x", "-\\sin x", "\\cot x", "0", "1"]),
        ("\\cos(90^\\circ + x)", "-\\sin x", ["\\sin x", "\\cos x", "-\\cos x", "-\\tan x", "0", "1"]),
        ("\\sin(90^\\circ - x)", "\\cos x", ["-\\cos x", "\\sin x", "-\\sin x", "\\tan x", "0", "1"]),
        ("\\cos(90^\\circ - x)", "\\sin x", ["-\\sin x", "\\cos x", "-\\cos x", "\\sec x", "0", "1"])
    ]
    for expr, ans_red, wrongs_red in red_cases:
        for idx in range(15):
            q_red = f"Simplify using reduction formulas: ${expr}$."
            if idx == 1:
                q_red = f"Evaluate the trigonometric reduction: ${expr}$."
            elif idx == 2:
                q_red = f"Reduce ${expr}$ to a single ratio of an acute angle $x$."
            elif idx == 3:
                q_red = f"Apply reduction formulas to simplify: ${expr}$."
            elif idx == 4:
                q_red = f"Which single trigonometric ratio equals ${expr}$?"
            elif idx == 5:
                q_red = f"Simplify the angle reduction expression: ${expr}$."
            elif idx == 6:
                q_red = f"Express ${expr}$ in terms of $x$."
            elif idx == 7:
                q_red = f"Determine the reduced form of ${expr}$."
            elif idx == 8:
                q_red = f"Simplify the co-ratio or quadrant reduction: ${expr}$."
            elif idx == 9:
                q_red = f"Find the value of ${expr}$ as a primary ratio."
            elif idx == 10:
                q_red = f"State the equivalent acute angle ratio for ${expr}$."
            elif idx == 11:
                q_red = f"Using quadrant reduction rules, simplify: ${expr}$."
            elif idx == 12:
                q_red = f"What is the simplified form of ${expr}$?"
            elif idx == 13:
                q_red = f"Reduce the angle in the expression: ${expr}$."
            elif idx == 14:
                q_red = f"Calculate the reduced equivalent of ${expr}$."
                
            c_red = f"${ans_red}$"
            d_red = [f"${w}$" for w in wrongs_red]
            exp_red = f"Using reduction formulas: ${expr} = {ans_red}$."
            add_q("Reduction Formulas", "medium", q_red, c_red, d_red, exp_red)

    # 2b. Reciprocal Pythagorean Identities: 1 + tan^2 x = sec^2 x, 1 + cot^2 x = cosec^2 x
    id_cases = [
        ("1 + \\tan^2 x", "\\sec^2 x", ["\\operatorname{cosec}^2 x", "\\sin^2 x", "\\cos^2 x", "1", "\\cot^2 x", "\\tan^2 x"]),
        ("1 + \\cot^2 x", "\\operatorname{cosec}^2 x", ["\\sec^2 x", "\\tan^2 x", "\\sin^2 x", "\\cos^2 x", "1", "\\cot^2 x"]),
        ("\\sec^2 x - 1", "\\tan^2 x", ["\\cot^2 x", "\\sec^2 x", "\\operatorname{cosec}^2 x", "1", "\\cos^2 x", "\\sin^2 x"]),
        ("\\operatorname{cosec}^2 x - 1", "\\cot^2 x", ["\\tan^2 x", "\\operatorname{cosec}^2 x", "\\sec^2 x", "1", "\\sin^2 x", "\\cos^2 x"]),
        ("\\sec^2 x - \\tan^2 x", "1", ["0", "2", "-1", "\\cos^2 x", "\\sin^2 x", "\\cot^2 x", "\\operatorname{cosec}^2 x"]),
        ("\\operatorname{cosec}^2 x - \\cot^2 x", "1", ["0", "2", "-1", "\\sin^2 x", "\\cos^2 x", "\\tan^2 x", "\\sec^2 x"])
    ]
    for expr, ans_id, wrongs_id in id_cases:
        for idx in range(12):
            q_id = f"Simplify the trigonometric expression using Pythagorean identities: ${expr}$."
            if idx == 1:
                q_id = f"Use reciprocal Pythagorean identities to simplify: ${expr}$."
            elif idx == 2:
                q_id = f"Determine the simplest form of: ${expr}$."
            elif idx == 3:
                q_id = f"Which expression is identical to: ${expr}$?"
            elif idx == 4:
                q_id = f"Simplify: ${expr}$."
            elif idx == 5:
                q_id = f"Evaluate the Pythagorean identity: ${expr}$."
            elif idx == 6:
                q_id = f"Express ${expr}$ in its simplest standard form."
            elif idx == 7:
                q_id = f"What is the equivalent expression for ${expr}$?"
            elif idx == 8:
                q_id = f"Reduce the identity: ${expr}$."
            elif idx == 9:
                q_id = f"Simplify using standard square identities: ${expr}$."
            elif idx == 10:
                q_id = f"Calculate the single-term equivalent of: ${expr}$."
            elif idx == 11:
                q_id = f"Apply fundamental square relationships to simplify: ${expr}$."
                
            c_id = f"${ans_id}$"
            d_id = [f"${w}$" for w in wrongs_id]
            exp_id = f"By the Pythagorean identity: ${expr} = {ans_id}$."
            add_q("Trigonometric Identities", "medium", q_id, c_id, d_id, exp_id)

    # 2c. Sine Rule & Cosine Rule in Non-Right Triangles
    for b_side in [6, 8, 10, 12, 14, 16]:
        for c_side in [5, 7, 9, 11, 13]:
            for A_deg in [30, 45, 60]:
                # Cosine rule: a^2 = b^2 + c^2 - 2bc*cos(A)
                rad = math.radians(A_deg)
                a2 = b_side**2 + c_side**2 - 2 * b_side * c_side * math.cos(rad)
                a_side = round(math.sqrt(a2), 2)
                
                q_cos = (f"In $\\triangle ABC$, $b = {b_side}$ cm, $c = {c_side}$ cm, and $\\hat{{A}} = {A_deg}^\\circ$. "
                         f"Calculate the length of side $a$ using the Cosine Rule. (Round to 2 decimal places).")
                c_cos = f"{a_side} cm"
                d_cos = [
                    f"{round(a_side + 2.5, 2)} cm",
                    f"{round(a_side - 2.5 if a_side > 4 else a_side + 5, 2)} cm",
                    f"{round(math.sqrt(b_side**2 + c_side**2), 2)} cm",
                    f"{round(a_side * 1.25, 2)} cm",
                    f"{round(a_side * 0.8, 2)} cm",
                    f"{b_side + c_side} cm",
                    f"{round(a2, 2)} cm"
                ]
                exp_cos = (f"Apply Cosine Rule: $a^2 = b^2 + c^2 - 2bc\\cos A$\n"
                           f"$a^2 = ({b_side})^2 + ({c_side})^2 - 2({b_side})({c_side})\\cos({A_deg}^\\circ) "
                           f"= {b_side**2 + c_side**2} - {round(2 * b_side * c_side * math.cos(rad), 2)} = {round(a2, 2)}$.\n"
                           f"$a = \\sqrt{{{round(a2, 2)}}} = {a_side}\\text{{ cm}}$.")
                add_q("Sine & Cosine Rules", "medium", q_cos, c_cos, d_cos, exp_cos)

    # 2d. Sine Rule for Sides in Triangles: a / sin A = b / sin B
    for a_side in [8, 10, 12, 14, 15, 16, 18, 20, 22, 25, 30]:
        for A_deg in [30, 45, 60]:
            for B_deg in [40, 50, 70, 75]:
                # b = a * sin(B) / sin(A)
                b_calc = round(a_side * math.sin(math.radians(B_deg)) / math.sin(math.radians(A_deg)), 2)
                q_sin = (f"In $\\triangle ABC$, $a = {a_side}$ cm, $\\hat{{A}} = {A_deg}^\\circ$, and $\\hat{{B}} = {B_deg}^\\circ$. "
                         f"Calculate the length of side $b$ using the Sine Rule. (Round to 2 decimal places).")
                c_sin = f"{b_calc} cm"
                d_sin = [
                    f"{round(b_calc + 3.2, 2)} cm",
                    f"{round(b_calc - 3.2 if b_calc > 4 else b_calc + 6, 2)} cm",
                    f"{round(b_calc * 1.2, 2)} cm",
                    f"{round(b_calc * 0.8, 2)} cm",
                    f"{round(a_side * math.sin(math.radians(A_deg)) / math.sin(math.radians(B_deg)), 2)} cm",
                    f"{a_side} cm",
                    f"{round(b_calc + 10, 2)} cm"
                ]
                exp_sin = (f"Apply the Sine Rule: $\\frac{{b}}{{\\sin B}} = \\frac{{a}}{{\\sin A}} \\implies "
                           f"b = \\frac{{{a_side} \\times \\sin({B_deg}^\\circ)}}{{\\sin({A_deg}^\\circ)}} = {b_calc}\\text{{ cm}}$.")
                add_q("Sine & Cosine Rules", "medium", q_sin, c_sin, d_sin, exp_sin)

    # 2e. Reciprocals on the Cartesian Plane (Point P in quadrants)
    for xp, yp, rp in [(3, 4, 5), (-3, 4, 5), (-3, -4, 5), (3, -4, 5), (5, 12, 13), (-5, 12, 13), (-5, -12, 13), (8, 15, 17), (-8, 15, 17), (-8, -15, 17), (7, 24, 25), (-7, 24, 25)]:
        # sec = r / x
        q_cp_sec = f"If point $P({xp}; {yp})$ lies on the terminal arm of angle $\\theta$ in standard position, determine the value of $\\sec \\theta$."
        sec_ans = f"\\frac{{{rp}}}{{{xp}}}" if xp > 0 else f"-\\frac{{{rp}}}{{{abs(xp)}}}"
        c_cp_sec = f"${sec_ans}$"
        d_cp_sec = [
            f"$\\frac{{{xp}}}{{{rp}}}$", f"$\\frac{{{yp}}}{{{rp}}}$", f"$\\frac{{{rp}}}{{{yp}}}$",
            f"$\\frac{{{yp}}}{{{xp}}}$", f"$-\\frac{{{rp}}}{{{yp}}}$", f"$\\frac{{{rp + 1}}}{{{xp}}}$", "1"
        ]
        exp_cp_sec = f"Radius $r = \\sqrt{{({xp})^2 + ({yp})^2}} = {rp}$. By definition: $\\sec \\theta = \\frac{{r}}{{x}} = \\frac{{{rp}}}{{{xp}}} = {sec_ans}$."
        add_q("Reciprocal Ratios", "medium", q_cp_sec, c_cp_sec, d_cp_sec, exp_cp_sec)

        # cosec = r / y
        q_cp_csc = f"If point $P({xp}; {yp})$ lies on the terminal arm of angle $\\theta$ in standard position, determine the value of $\\operatorname{{cosec}} \\theta$."
        csc_ans = f"\\frac{{{rp}}}{{{yp}}}" if yp > 0 else f"-\\frac{{{rp}}}{{{abs(yp)}}}"
        c_cp_csc = f"${csc_ans}$"
        d_cp_csc = [
            f"$\\frac{{{yp}}}{{{rp}}}$", f"$\\frac{{{xp}}}{{{rp}}}$", f"$\\frac{{{rp}}}{{{xp}}}$",
            f"$\\frac{{{xp}}}{{{yp}}}$", f"$-\\frac{{{rp}}}{{{xp}}}$", f"$\\frac{{{rp + 1}}}{{{yp}}}$", "1"
        ]
        exp_cp_csc = f"Radius $r = \\sqrt{{({xp})^2 + ({yp})^2}} = {rp}$. By definition: $\\operatorname{{cosec}} \\theta = \\frac{{r}}{{y}} = \\frac{{{rp}}}{{{yp}}} = {csc_ans}$."
        add_q("Reciprocal Ratios", "medium", q_cp_csc, c_cp_csc, d_cp_csc, exp_cp_csc)

        # cot = x / y
        q_cp_cot = f"If point $P({xp}; {yp})$ lies on the terminal arm of angle $\\theta$ in standard position, determine the value of $\\cot \\theta$."
        cot_ans = f"\\frac{{{xp}}}{{{yp}}}" if (xp * yp > 0) else f"-\\frac{{{abs(xp)}}}{{{abs(yp)}}}"
        c_cp_cot = f"${cot_ans}$"
        d_cp_cot = [
            f"$\\frac{{{yp}}}{{{xp}}}$", f"$\\frac{{{rp}}}{{{xp}}}$", f"$\\frac{{{rp}}}{{{yp}}}$",
            f"$-\\frac{{{yp}}}{{{abs(xp)}}}$", f"$\\frac{{{abs(xp) + 1}}}{{{abs(yp)}}}$", "1", "0"
        ]
        exp_cp_cot = f"By definition: $\\cot \\theta = \\frac{{x}}{{y}} = \\frac{{{xp}}}{{{yp}}} = {cot_ans}$."
        add_q("Reciprocal Ratios", "medium", q_cp_cot, c_cp_cot, d_cp_cot, exp_cp_cot)
        d_cp_csc = [
            f"$\\frac{{{yp}}}{{{rp}}}$", f"$\\frac{{{xp}}}{{{rp}}}$", f"$\\frac{{{rp}}}{{{xp}}}$",
            f"$\\frac{{{xp}}}{{{yp}}}$", f"$-\\frac{{{rp}}}{{{xp}}}$", f"$\\frac{{{rp + 1}}}{{{yp}}}$", "1"
        ]
        exp_cp_csc = f"Radius $r = \\sqrt{{({xp})^2 + ({yp})^2}} = {rp}$. By definition: $\\operatorname{{cosec}} \\theta = \\frac{{r}}{{y}} = \\frac{{{rp}}}{{{yp}}} = {csc_ans}$."
        add_q("Reciprocal Ratios", "medium", q_cp_csc, c_cp_csc, d_cp_csc, exp_cp_csc)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. General Solutions of Reciprocal Trigonometric Equations
    recip_eqs = [
        ("2\\cos x = 1", "\\cos x = \\frac{1}{2}", "x = \\pm 60^\\circ + k \\cdot 360^\\circ"),
        ("2\\sin x = \\sqrt{3}", "\\sin x = \\frac{\\sqrt{3}}{2}", "x = 60^\\circ + k \\cdot 360^\\circ \\text{ or } x = 120^\\circ + k \\cdot 360^\\circ"),
        ("\\sec x = 2", "\\cos x = \\frac{1}{2}", "x = \\pm 60^\\circ + k \\cdot 360^\\circ"),
        ("\\operatorname{cosec} x = 2", "\\sin x = \\frac{1}{2}", "x = 30^\\circ + k \\cdot 360^\\circ \\text{ or } x = 150^\\circ + k \\cdot 360^\\circ"),
        ("\\cot x = 1", "\\tan x = 1", "x = 45^\\circ + k \\cdot 180^\\circ"),
        ("\\cot x = \\sqrt{3}", "\\tan x = \\frac{1}{\\sqrt{3}}", "x = 30^\\circ + k \\cdot 180^\\circ"),
        ("\\sec x = \\sqrt{2}", "\\cos x = \\frac{1}{\\sqrt{2}}", "x = \\pm 45^\\circ + k \\cdot 360^\\circ"),
        ("2\\sin x = -1", "\\sin x = -\\frac{1}{2}", "x = 210^\\circ + k \\cdot 360^\\circ \\text{ or } x = 330^\\circ + k \\cdot 360^\\circ"),
        ("2\\cos x = -\\sqrt{3}", "\\cos x = -\\frac{\\sqrt{3}}{2}", "x = \\pm 150^\\circ + k \\cdot 360^\\circ"),
        ("\\tan x = -1", "\\tan x = -1", "x = 135^\\circ + k \\cdot 180^\\circ")
    ]
    for eq_t, simp_t, sol_t in recip_eqs:
        for idx in range(8):
            q_gs = f"Determine the general solution for $x$ in the equation: ${eq_t}$, where $k \\in \\mathbb{{Z}}$."
            if idx == 1:
                q_gs = f"Solve for the general solution of ${eq_t}$, with $k \\in \\mathbb{{Z}}$."
            elif idx == 2:
                q_gs = f"Find all angles $x$ satisfying ${eq_t}$, expressed as a general solution ($k \\in \\mathbb{{Z}}$)."
            elif idx == 3:
                q_gs = f"Determine the complete set of solutions for: ${eq_t}$ ($k \\in \\mathbb{{Z}}$)."
            elif idx == 4:
                q_gs = f"Calculate the general solution of the trigonometric equation ${eq_t}$."
            elif idx == 5:
                q_gs = f"Solve algebraically for $x$: ${eq_t}$ for all $k \\in \\mathbb{{Z}}$."
            elif idx == 6:
                q_gs = f"Find the general solution to the equation ${eq_t}$."
            elif idx == 7:
                q_gs = f"State the general solution for $x$: ${eq_t}$ ($k \\in \\mathbb{{Z}}$)."
                
            c_gs = f"${sol_t}$"
            d_gs = [
                f"${sol_t.replace('360', '180')}$" if "360" in sol_t else f"${sol_t.replace('180', '360')}$",
                f"${sol_t.replace('+', '-')}$",
                f"${sol_t.replace('60', '30')}$" if "60" in sol_t else f"${sol_t.replace('30', '60')}$",
                f"${sol_t.replace('45', '135')}$" if "45" in sol_t else f"${sol_t.replace('150', '30')}$",
                f"${sol_t.split('or')[0].strip()}$" if "or" in sol_t else f"${sol_t} \\text{{ or }} x = 0^\\circ$",
                f"$x = k \\cdot 360^\\circ$",
                f"$x = k \\cdot 180^\\circ$"
            ]
            exp_gs = f"Step 1: Simplify to standard ratio: ${simp_t}$.\nStep 2: Reference angle and quadrant general solution: ${sol_t}$ ($k \\in \\mathbb{{Z}}$)."
            add_q("General Solutions", "hard", q_gs, c_gs, d_gs, exp_gs)

    # 3b. 2D / 3D Engineering Surveying Applications
    # Surveyor measuring distance to transmission tower
    for base_dist in [40, 50, 60, 75, 100, 120, 150]:
        for elev1 in [25, 30, 35, 40]:
            # Tower height h = base_dist * tan(elev1)
            rad1 = math.radians(elev1)
            h_tower = round(base_dist * math.tan(rad1), 2)
            
            q_surv = (f"An electrical engineering surveyor at point $A$ on flat ground measures the angle of elevation "
                      f"to the top of a communication tower $T$ as {elev1}$^\\circ$. The distance from $A$ to the base of the tower $B$ "
                      f"is {base_dist} m. Calculate the height of the tower $BT$. (Round to 2 decimal places).")
            c_surv = f"{h_tower} m"
            d_surv = [
                f"{round(base_dist / math.tan(rad1), 2)} m",
                f"{round(h_tower * 1.25, 2)} m",
                f"{round(h_tower * 0.75, 2)} m",
                f"{round(h_tower + 12, 2)} m",
                f"{round(h_tower - 12 if h_tower > 15 else h_tower + 20, 2)} m",
                f"{base_dist} m",
                f"{round(base_dist * math.sin(rad1), 2)} m"
            ]
            exp_surv = (f"In right-angled $\\triangle ABT$: $\\tan({elev1}^\\circ) = \\frac{{\\text{{Opposite}}}}{{\\text{{Adjacent}}}} = \\frac{{h}}{{{base_dist}}}$.\n"
                        f"$h = {base_dist} \\times \\tan({elev1}^\\circ) = {h_tower}\\text{{ m}}$.")
            add_q("2D & 3D Trigonometry", "hard", q_surv, c_surv, d_surv, exp_surv)

    # 3c. Area Rule in Non-Right Triangles: Area = 1/2 * a * b * sin C
    for a_ar in [8, 10, 12, 15, 18, 20]:
        for b_ar in [7, 9, 11, 14, 16]:
            for C_ar in [30, 45, 60, 120, 135, 150]:
                rad_c = math.radians(C_ar)
                area_val = round(0.5 * a_ar * b_ar * math.sin(rad_c), 2)
                
                q_area_t = (f"Calculate the area of a triangular structural brace with side lengths $a = {a_ar}$ cm, "
                            f"$b = {b_ar}$ cm, and included angle $\\hat{{C}} = {C_ar}^\\circ$ using the Area Rule. "
                            f"(Round to 2 decimal places).")
                c_area_t = f"{area_val} cm^2"
                d_area_t = [
                    f"{round(a_ar * b_ar * math.sin(rad_c), 2)} cm^2",
                    f"{round(0.5 * a_ar * b_ar * math.cos(rad_c), 2)} cm^2",
                    f"{round(area_val * 1.5, 2)} cm^2",
                    f"{round(area_val * 0.5, 2)} cm^2",
                    f"{round(area_val + 10, 2)} cm^2",
                    f"{round(area_val - 10 if area_val > 15 else area_val + 20, 2)} cm^2",
                    f"{round(0.5 * a_ar * b_ar, 2)} cm^2"
                ]
                exp_area_t = (f"Apply Area Rule: $\\text{{Area}} = \\frac{{1}}{{2}}ab\\sin C = \\frac{{1}}{{2}}({a_ar})({b_ar})\\sin({C_ar}^\\circ) "
                              f"= {0.5 * a_ar * b_ar} \\times {round(math.sin(rad_c), 4)} = {area_val}\\text{{ cm}}^2$.")
                add_q("Sine & Cosine Rules", "hard", q_area_t, c_area_t, d_area_t, exp_area_t)

    print(f"Generated Tech Math Trig: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper2_tech_trig.json")
    dataset = build_trig_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
