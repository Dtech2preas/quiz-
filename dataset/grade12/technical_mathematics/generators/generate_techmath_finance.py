import json
import os
import random
import math
import time

def build_finance_dataset():
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
        q_id = f"TM12_P1_FIN_{len(questions) + 1:04d}"
        
        cog_level = "Knowledge" if difficulty == "easy" else "Routine Procedures" if difficulty == "medium" else "Complex Procedures"
        
        questions.append({
            "id": q_id,
            "topic": "Financial Mathematics",
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
                "topic": "Financial Mathematics",
                "subtopic": subtopic,
                "cognitive_level": cog_level,
                "difficulty": difficulty
            }
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Simple Interest A = P(1 + in)
    p_vals = [2000, 3500, 5000, 7500, 10000, 12000, 15000, 18000, 20000, 25000, 30000, 40000, 50000]
    r_vals = [4.5, 5.0, 6.0, 7.5, 8.0, 8.5, 9.0, 10.0, 11.5, 12.0]
    n_vals = [2, 3, 4, 5, 6, 7, 8]
    for P in p_vals:
        for r in r_vals:
            for n in n_vals:
                i = r / 100
                A = round(P * (1 + i * n), 2)
                interest = round(A - P, 2)
                
                q_si = (f"A technical workshop deposits R{P:,} into a savings account earning {r}% per annum simple interest. "
                        f"Calculate the total accumulated amount after {n} years.")
                c_si = f"R{A:,.2f}"
                d_si = [
                    f"R{P * (1 + i)**n:,.2f}",
                    f"R{P + (P * i):,.2f}",
                    f"R{A + 500:,.2f}",
                    f"R{A - 500:,.2f}",
                    f"R{P * 2:,.2f}",
                    f"R{interest:,.2f}",
                    f"R{A * 1.1:,.2f}"
                ]
                exp_si = (f"Use the simple interest formula: $A = P(1 + in) = {P}(1 + {i} \\times {n}) "
                          f"= {P}(1 + {round(i*n, 4)}) = \\text{{R}}{A:,.2f}$.")
                add_q("Simple Interest & Depreciation", "easy", q_si, c_si, d_si, exp_si)

                # 1b. Straight-line Depreciation A = P(1 - in)
                if i * n < 1:
                    A_dep = round(P * (1 - i * n), 2)
                    q_sld = (f"A piece of industrial equipment with an initial cost of R{P:,} depreciates at a rate of {r}% per annum "
                             f"on a straight-line basis. Determine its book value after {n} years.")
                    c_sld = f"R{A_dep:,.2f}"
                    d_sld = [
                        f"R{P * (1 - i)**n:,.2f}",
                        f"R{P - (P * i):,.2f}",
                        f"R{A_dep + 400:,.2f}",
                        f"R{A_dep - 400:,.2f}",
                        f"R{P * i * n:,.2f}",
                        f"R{P * 0.5:,.2f}",
                        f"R{A_dep * 0.9:,.2f}"
                    ]
                    exp_sld = (f"Use the straight-line depreciation formula: $A = P(1 - in) = {P}(1 - {i} \\times {n}) "
                               f"= {P}(1 - {round(i*n, 4)}) = \\text{{R}}{A_dep:,.2f}$.")
                    add_q("Simple Interest & Depreciation", "easy", q_sld, c_sld, d_sld, exp_sld)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Nominal to Effective Interest Rate: (1 + i_eff) = (1 + i_nom / m)^m
    comp_types = [
        ("monthly", 12),
        ("quarterly", 4),
        ("semi-annually", 2),
        ("daily", 365)
    ]
    for r_nom in [6.5, 7.25, 8.0, 8.5, 9.0, 9.75, 10.25, 11.0, 11.5, 12.0, 12.5, 13.25, 14.0]:
        for comp_name, m in comp_types:
            i_nom = r_nom / 100
            i_eff = (1 + i_nom / m)**m - 1
            r_eff = round(i_eff * 100, 2)
            
            q_eff = (f"Convert an annual nominal interest rate of {r_nom}% per annum compounded {comp_name} "
                     f"to the equivalent effective annual interest rate. (Round to 2 decimal places).")
            c_eff = f"{r_eff}%"
            d_eff = [
                f"{r_nom}%",
                f"{round(r_eff + 0.5, 2)}%",
                f"{round(r_eff - 0.5, 2)}%",
                f"{round(r_nom + (r_nom / m), 2)}%",
                f"{round(r_eff * 1.1, 2)}%",
                f"{round(r_eff * 0.9, 2)}%",
                f"{round(r_nom * 1.05, 2)}%"
            ]
            exp_eff = (f"Use the formula: $1 + i_{{\\text{{eff}}}} = \\left(1 + \\frac{{i_{{\\text{{nom}}}}}}{{m}}\\right)^m$\n"
                       f"$1 + i_{{\\text{{eff}}}} = \\left(1 + \\frac{{{i_nom}}}{{{m}}}\\right)^{{{m}}} = \\left({round(1 + i_nom/m, 6)}\\right)^{{{m}}} "
                       f"= {round(1 + i_eff, 6)}$\n"
                       f"$i_{{\\text{{eff}}}} = {round(i_eff, 4)} \\implies {r_eff}\\%$.")
            add_q("Nominal and Effective Interest Rates", "medium", q_eff, c_eff, d_eff, exp_eff)

    # 2b. Reducing-Balance Depreciation A = P(1 - i)^n
    p_rb_list = [15000, 25000, 45000, 60000, 85000, 120000, 180000, 250000, 320000, 450000, 600000]
    rate_rb_list = [8, 10, 12, 14, 15, 16, 18, 20]
    years_rb = [3, 4, 5, 6, 7]
    for P_rb in p_rb_list:
        for r_rb in rate_rb_list:
            for n_rb in years_rb:
                i_rb = r_rb / 100
                A_rb = round(P_rb * ((1 - i_rb) ** n_rb), 2)
                
                q_rb = (f"A CNC milling machine is purchased for R{P_rb:,}. It depreciates at a rate of {r_rb}% per annum "
                        f"on the reducing-balance method. Calculate its salvage (scrap) value after {n_rb} years.")
                c_rb = f"R{A_rb:,.2f}"
                d_rb = [
                    f"R{P_rb * (1 - i_rb * n_rb):,.2f}",
                    f"R{P_rb * ((1 + i_rb) ** n_rb):,.2f}",
                    f"R{round(A_rb * 1.15, 2):,.2f}",
                    f"R{round(A_rb * 0.85, 2):,.2f}",
                    f"R{P_rb * (1 - i_rb):,.2f}",
                    f"R{round(P_rb - A_rb, 2):,.2f}",
                    f"R{round(A_rb + 1200, 2):,.2f}"
                ]
                exp_rb = (f"Use the reducing-balance depreciation formula: $A = P(1 - i)^n$\n"
                          f"$A = {P_rb}(1 - {i_rb})^{{{n_rb}}} = {P_rb}({round(1 - i_rb, 4)})^{{{n_rb}}} = \\text{{R}}{A_rb:,.2f}$.")
                add_q("Compound Interest & Depreciation", "medium", q_rb, c_rb, d_rb, exp_rb)

    # 2c. Compound Interest with Compounding Periods
    for P_c in [10000, 20000, 35000, 50000, 75000, 100000]:
        for r_c in [7.5, 9.0, 10.5, 12.0]:
            for n_c in [3, 4, 5]:
                for comp_name, m_c in [("monthly", 12), ("quarterly", 4), ("semi-annually", 2)]:
                    i_per = (r_c / 100) / m_c
                    tot_periods = n_c * m_c
                    A_c = round(P_c * ((1 + i_per) ** tot_periods), 2)
                    
                    q_comp = (f"An engineering firm invests R{P_c:,} at {r_c}% per annum compounded {comp_name}. "
                              f"Calculate the accumulated future value of the investment after {n_c} years.")
                    c_comp = f"R{A_c:,.2f}"
                    d_comp = [
                        f"R{P_c * (1 + (r_c/100)*n_c):,.2f}",
                        f"R{P_c * (1 + (r_c/100))**n_c:,.2f}",
                        f"R{round(A_c * 1.08, 2):,.2f}",
                        f"R{round(A_c * 0.92, 2):,.2f}",
                        f"R{round(A_c + 2500, 2):,.2f}",
                        f"R{round(A_c - 2500, 2):,.2f}",
                        f"R{P_c * 2:,.2f}"
                    ]
                    exp_comp = (f"Use compound formula: $A = P\\left(1 + \\frac{{i}}{{m}}\\right)^{{n \\times m}}$\n"
                                f"$A = {P_c}\\left(1 + \\frac{{{r_c/100}}}{{{m_c}}}\\right)^{{{n_c} \\times {m_c}}} "
                                f"= {P_c}({round(1 + i_per, 6)})^{{{tot_periods}}} = \\text{{R}}{A_c:,.2f}$.")
                    add_q("Compound Interest & Depreciation", "medium", q_comp, c_comp, d_comp, exp_comp)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Multi-Stage Timeline Investments (Deposit + Withdrawal)
    timeline_cases = [
        (50000, 8.5, 6, 20000, 3, "withdrawal"),
        (40000, 9.0, 5, 15000, 2, "withdrawal"),
        (60000, 10.0, 7, 25000, 4, "withdrawal"),
        (30000, 8.0, 6, 12000, 3, "withdrawal"),
        (75000, 9.5, 8, 30000, 5, "withdrawal"),
        (45000, 10.5, 5, 18000, 2, "withdrawal"),
        (50000, 9.0, 6, 20000, 3, "deposit"),
        (35000, 8.5, 5, 15000, 2, "deposit"),
        (65000, 10.0, 7, 25000, 4, "deposit"),
        (40000, 9.5, 6, 15000, 3, "deposit"),
        (80000, 8.0, 8, 35000, 4, "deposit"),
        (55000, 11.0, 5, 20000, 2, "deposit")
    ]
    for P_init, r_t, tot_yrs, flow_amt, flow_yr, flow_type in timeline_cases:
        for comp_name, m_t in [("monthly", 12), ("quarterly", 4)]:
            i_p = (r_t / 100) / m_t
            # FV of P_init for tot_yrs
            fv_init = P_init * ((1 + i_p) ** (tot_yrs * m_t))
            # FV of flow_amt from flow_yr to tot_yrs
            rem_yrs = tot_yrs - flow_yr
            fv_flow = flow_amt * ((1 + i_p) ** (rem_yrs * m_t))
            
            if flow_type == "withdrawal":
                A_net = round(fv_init - fv_flow, 2)
                action_str = f"withdraws R{flow_amt:,} from the account"
                sign_str = "-"
            else:
                A_net = round(fv_init + fv_flow, 2)
                action_str = f"makes an additional deposit of R{flow_amt:,}"
                sign_str = "+"
                
            q_tl = (f"A contractor opens a savings account with an initial deposit of R{P_init:,} at an interest rate of {r_t}% "
                    f"per annum compounded {comp_name}. At the end of year {flow_yr}, the contractor {action_str}. "
                    f"Calculate the total balance in the account at the end of {tot_yrs} years.")
            c_tl = f"R{A_net:,.2f}"
            d_tl = [
                f"R{round(fv_init, 2):,.2f}",
                f"R{round(fv_init + (fv_flow if flow_type == 'withdrawal' else -fv_flow), 2):,.2f}",
                f"R{round(A_net * 1.1, 2):,.2f}",
                f"R{round(A_net * 0.9, 2):,.2f}",
                f"R{round((P_init + (flow_amt if flow_type == 'deposit' else -flow_amt)) * ((1 + i_p)**(tot_yrs * m_t)), 2):,.2f}",
                f"R{round(A_net + 5000, 2):,.2f}",
                f"R{round(A_net - 5000, 2):,.2f}"
            ]
            exp_tl = (f"Use the timeline method:\n"
                      f"1. Accumulate initial principal for {tot_yrs} years: $\\text{{FV}}_1 = {P_init}\\left(1 + \\frac{{{r_t/100}}}{{{m_t}}}\\right)^{{{tot_yrs * m_t}}} = \\text{{R}}{fv_init:,.2f}$.\n"
                      f"2. Accumulate the year {flow_yr} flow for remaining {rem_yrs} years: $\\text{{FV}}_2 = {flow_amt}\\left(1 + \\frac{{{r_t/100}}}{{{m_t}}}\\right)^{{{rem_yrs * m_t}}} = \\text{{R}}{fv_flow:,.2f}$.\n"
                      f"3. Net balance = $\\text{{FV}}_1 {sign_str} \\text{{FV}}_2 = \\text{{R}}{A_net:,.2f}$.")
            add_q("Multi-stage Timelines", "hard", q_tl, c_tl, d_tl, exp_tl)

    # 3b. Interest Rate Fluctuations on an Investment
    rate_chg_cases = [
        (60000, 8.0, 3, 10.0, 4),
        (50000, 7.5, 2, 9.5, 3),
        (80000, 9.0, 4, 11.0, 3),
        (40000, 8.5, 3, 10.5, 3),
        (70000, 9.0, 2, 11.5, 4),
        (100000, 8.0, 3, 10.0, 3),
        (90000, 7.0, 4, 9.0, 4),
        (45000, 8.5, 2, 10.5, 5)
    ]
    for P_rc, r1_c, n1_c, r2_c, n2_c in rate_chg_cases:
        for comp_name, m_rc in [("monthly", 12), ("quarterly", 4)]:
            i1 = (r1_c / 100) / m_rc
            i2 = (r2_c / 100) / m_rc
            A_mid = P_rc * ((1 + i1) ** (n1_c * m_rc))
            A_final = round(A_mid * ((1 + i2) ** (n2_c * m_rc)), 2)
            tot_n = n1_c + n2_c
            
            q_rc = (f"A manufacturing company invests R{P_rc:,} for {tot_n} years. For the first {n1_c} years, "
                    f"the interest rate is {r1_c}% per annum compounded {comp_name}. The interest rate then changes to "
                    f"{r2_c}% per annum compounded {comp_name} for the remaining {n2_c} years. "
                    f"Calculate the accumulated balance at the end of the {tot_n}-year investment period.")
            c_rc = f"R{A_final:,.2f}"
            d_rc = [
                f"R{round(P_rc * ((1 + (r1_c/100)/m_rc)**(tot_n * m_rc)), 2):,.2f}",
                f"R{round(P_rc * ((1 + (r2_c/100)/m_rc)**(tot_n * m_rc)), 2):,.2f}",
                f"R{round(A_final * 1.08, 2):,.2f}",
                f"R{round(A_final * 0.92, 2):,.2f}",
                f"R{round(A_mid, 2):,.2f}",
                f"R{round(A_final + 8000, 2):,.2f}",
                f"R{round(A_final - 8000, 2):,.2f}"
            ]
            exp_rc = (f"Use the multi-period compound formula:\n"
                      f"$A = P\\left(1 + \\frac{{i_1}}{{m}}\\right)^{{n_1 \\times m}} \\times \\left(1 + \\frac{{i_2}}{{m}}\\right)^{{n_2 \\times m}}$\n"
                      f"$A = {P_rc}\\left(1 + \\frac{{{r1_c/100}}}{{{m_rc}}}\\right)^{{{n1_c * m_rc}}} \\times \\left(1 + \\frac{{{r2_c/100}}}{{{m_rc}}}\\right)^{{{n2_c * m_rc}}} = \\text{{R}}{A_final:,.2f}$.")
            add_q("Multi-stage Timelines", "hard", q_rc, c_rc, d_rc, exp_rc)

    # 3c. Solving for Time n or Depreciation Rate i using Logarithms
    for P_log in [50000, 80000, 120000, 200000, 300000]:
        for rate_log in [10, 12, 15, 18, 20]:
            # Halving time (half-life of asset under reducing-balance depreciation)
            i_l = rate_log / 100
            # A = P * (1 - i)^n => 0.5 = (1 - i)^n => n = log(0.5) / log(1 - i)
            n_exact = math.log(0.5) / math.log(1 - i_l)
            n_rounded = round(n_exact, 2)
            
            q_log = (f"A factory machine depreciates at a rate of {rate_log}% per annum on the reducing-balance method. "
                     f"How many years will it take for the machine's book value to reduce to exactly half (50%) of its original cost price? "
                     f"(Round to 2 decimal places).")
            c_log = f"{n_rounded} years"
            d_log = [
                f"{round(100 / rate_log, 2)} years",
                f"{round(n_rounded + 1.2, 2)} years",
                f"{round(n_rounded - 1.2 if n_rounded > 2 else n_rounded + 2.5, 2)} years",
                f"{round(n_rounded * 1.5, 2)} years",
                f"{round(n_rounded * 0.7, 2)} years",
                f"{rate_log} years",
                f"{round(50 / rate_log, 2)} years"
            ]
            exp_log = (f"Set $A = 0.5P$ in the reducing-balance equation: $0.5P = P(1 - {i_l})^n \\implies 0.5 = ({round(1 - i_l, 4)})^n$.\n"
                       f"Take logarithms on both sides: $n = \\frac{{\\log(0.5)}}{{\\log({round(1 - i_l, 4)})}} = {n_rounded}\\text{{ years}}$.")
            add_q("Compound Interest & Depreciation", "hard", q_log, c_log, d_log, exp_log)

    # 3d. Sinking Fund & Equipment Replacement Deficit
    rep_cases = [
        (250000, 6.5, 14.0, 5),
        (350000, 7.0, 15.0, 4),
        (500000, 6.0, 16.0, 5),
        (400000, 7.5, 18.0, 4),
        (600000, 5.5, 12.0, 6),
        (300000, 8.0, 15.0, 5),
        (750000, 6.5, 16.0, 5),
        (450000, 7.0, 14.0, 4),
        (800000, 6.0, 15.0, 6),
        (550000, 7.5, 18.0, 5),
        (900000, 5.5, 13.0, 5),
        (650000, 6.5, 16.0, 4)
    ]
    for C_0, r_inf, r_dep, n_rep in rep_cases:
        i_inf = r_inf / 100
        i_dep = r_dep / 100
        cost_new = round(C_0 * ((1 + i_inf) ** n_rep), 2)
        scrap_val = round(C_0 * ((1 - i_dep) ** n_rep), 2)
        deficit = round(cost_new - scrap_val, 2)
        
        q_rep = (f"A manufacturing company buys a hydraulic press for R{C_0:,}. The machine will be replaced in {n_rep} years. "
                 f"The price of a new machine increases by {r_inf}% per annum compound inflation, while the current machine "
                 f"depreciates at {r_dep}% per annum on the reducing-balance method. Calculate the net sinking fund deficit "
                 f"(the difference between the cost of the new machine and the scrap value of the old machine).")
        c_rep = f"R{deficit:,.2f}"
        d_rep = [
            f"R{cost_new:,.2f}",
            f"R{scrap_val:,.2f}",
            f"R{cost_new + scrap_val:,.2f}",
            f"R{round(deficit * 1.1, 2):,.2f}",
            f"R{round(deficit * 0.9, 2):,.2f}",
            f"R{round(C_0 * (1 + i_inf * n_rep) - C_0 * (1 - i_dep * n_rep), 2):,.2f}",
            f"R{round(deficit + 20000, 2):,.2f}"
        ]
        exp_rep = (f"Step 1: Future replacement cost of new machine: $C_{{{n_rep}}} = {C_0}(1 + {i_inf})^{{{n_rep}}} = \\text{{R}}{cost_new:,.2f}$.\n"
                   f"Step 2: Scrap value of existing machine: $S_{{{n_rep}}} = {C_0}(1 - {i_dep})^{{{n_rep}}} = \\text{{R}}{scrap_val:,.2f}$.\n"
                   f"Step 3: Sinking fund deficit = $C_{{{n_rep}}} - S_{{{n_rep}}} = {cost_new:,.2f} - {scrap_val:,.2f} = \\text{{R}}{deficit:,.2f}$.")
        add_q("Multi-stage Timelines", "hard", q_rep, c_rep, d_rep, exp_rep)

    # 3e. Solving for Reducing-Balance Depreciation Rate i
    dep_rate_cases = [
        (120000, 52000, 5),
        (180000, 75000, 5),
        (250000, 95000, 6),
        (300000, 110000, 6),
        (400000, 140000, 5),
        (150000, 60000, 4),
        (220000, 85000, 5),
        (350000, 125000, 6),
        (500000, 160000, 6),
        (280000, 105000, 5),
        (450000, 155000, 5),
        (320000, 115000, 5)
    ]
    for P_dr, A_dr, n_dr in dep_rate_cases:
        ratio = A_dr / P_dr
        i_exact = 1 - (ratio ** (1 / n_dr))
        r_exact = round(i_exact * 100, 2)
        
        q_dr = (f"An industrial generator costing R{P_dr:,} has a book value of R{A_dr:,} after {n_dr} years. "
                f"Calculate the annual rate of depreciation on the reducing-balance method. (Round to 2 decimal places).")
        c_dr = f"{r_exact}%"
        d_dr = [
            f"{round(r_exact + 1.5, 2)}%",
            f"{round(r_exact - 1.5, 2)}%",
            f"{round(((P_dr - A_dr) / (P_dr * n_dr)) * 100, 2)}%",
            f"{round(r_exact * 1.15, 2)}%",
            f"{round(r_exact * 0.85, 2)}%",
            f"{round((1 - ratio) * 100, 2)}%",
            f"{round(r_exact + 3.0, 2)}%"
        ]
        exp_dr = (f"Use the reducing-balance formula: $A = P(1 - i)^n \\implies \\frac{{{A_dr}}}{{{P_dr}}} = (1 - i)^{{{n_dr}}}$.\n"
                  f"$1 - i = \\left(\\frac{{{A_dr}}}{{{P_dr}}}\\right)^{{1/{n_dr}}} = ({round(ratio, 4)})^{{1/{n_dr}}} = {round(1 - i_exact, 4)}$.\n"
                  f"$i = 1 - {round(1 - i_exact, 4)} = {round(i_exact, 4)} \\implies {r_exact}\\%$.")
        add_q("Compound Interest & Depreciation", "hard", q_dr, c_dr, d_dr, exp_dr)

    # 3f. Present Value: Calculating Required Initial Investment P
    for A_pv in [100000, 150000, 200000, 250000, 300000, 400000, 500000]:
        for r_pv in [8.0, 9.0, 10.0, 11.0, 12.0]:
            for n_pv in [3, 4, 5]:
                for comp_name, m_pv in [("monthly", 12), ("quarterly", 4)]:
                    i_pv = (r_pv / 100) / m_pv
                    tot_m = n_pv * m_pv
                    P_req = round(A_pv / ((1 + i_pv) ** tot_m), 2)
                    
                    q_pv = (f"How much money must an engineering technician invest now into an account paying {r_pv}% per annum "
                            f"compounded {comp_name} to accumulate a total of R{A_pv:,} in {n_pv} years' time?")
                    c_pv = f"R{P_req:,.2f}"
                    d_pv = [
                        f"R{round(A_pv * ((1 + i_pv)**tot_m), 2):,.2f}",
                        f"R{round(A_pv / (1 + (r_pv/100)*n_pv), 2):,.2f}",
                        f"R{round(P_req * 1.1, 2):,.2f}",
                        f"R{round(P_req * 0.9, 2):,.2f}",
                        f"R{round(P_req + 4000, 2):,.2f}",
                        f"R{round(P_req - 4000, 2):,.2f}",
                        f"R{A_pv / 2:,.2f}"
                    ]
                    exp_pv = (f"Rearrange compound formula for principal $P$: $P = \\frac{{A}}{{\\left(1 + \\frac{{i}}{{m}}\\right)^{{n \\times m}}}}$\n"
                              f"$P = \\frac{{{A_pv}}}{{\\left(1 + \\frac{{{r_pv/100}}}{{{m_pv}}}\\right)^{{{tot_m}}}}} "
                              f"= \\frac{{{A_pv}}}{{{round((1 + i_pv)**tot_m, 6)}}} = \\text{{R}}{P_req:,.2f}$.")
                    add_q("Compound Interest & Depreciation", "hard", q_pv, c_pv, d_pv, exp_pv)

    print(f"Generated Tech Math Finance: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_mathematics"
    out_file = os.path.join(out_dir, "paper1_tech_finance.json")
    dataset = build_finance_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
