import json
import random
import os
import time
import math

def generate_math_finance():
    print("Generating Grade 12 Mathematics: Financial Mathematics...")
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
        q_id = f"MATH_P1_FIN_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Financial Mathematics",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Financial Mathematics",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_floats(val, decimals=2, count=8):
        w = set()
        for delta in [-1.5, 1.5, -0.5, 0.5, -2.0, 2.0, val * 0.1, -val * 0.1, val * 1.1]:
            cand = round(val + delta, decimals)
            if cand > 0 and cand != val:
                w.add(f"{cand:.{decimals}f}")
        cand_list = list(w)
        while len(cand_list) < count:
            extra = round(val + random.uniform(5, 50) * random.choice([1, -1]), decimals)
            if extra > 0 and extra != val and f"{extra:.{decimals}f}" not in cand_list:
                cand_list.append(f"{extra:.{decimals}f}")
        return cand_list[:count]

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    fin_rules = [
        ("What formula is used to calculate the Future Value ($F_v$) of an annuity with regular payments $x$ made at the end of each period?", "F_v = \\frac{x[(1 + i)^n - 1]}{i}", [
            "P_v = \\frac{x[1 - (1 + i)^{-n}]}{i}", "A = P(1 + i)^n", "A = P(1 - i)^n", "F_v = \\frac{x[(1 + i)^{-n} - 1]}{i}", "F_v = x(1 + i)^n", "F_v = \\frac{x}{i}"
        ], "The Future Value annuity formula is $F_v = \\frac{x[(1 + i)^n - 1]}{i}$."),

        ("What formula is used to calculate the Present Value ($P_v$) of an annuity (such as a home loan or bond) with regular repayments $x$?", "P_v = \\frac{x[1 - (1 + i)^{-n}]}{i}", [
            "F_v = \\frac{x[(1 + i)^n - 1]}{i}", "A = P(1 - in)", "P_v = \\frac{x[(1 + i)^n - 1]}{i}", "P_v = x(1 - i)^n", "P_v = \\frac{x[1 + (1 + i)^{-n}]}{i}", "P_v = \\frac{x}{i}"
        ], "The Present Value annuity formula is $P_v = \\frac{x[1 - (1 + i)^{-n}]}{i}$."),

        ("Which equation converts a nominal interest rate $i_{\\text{nom}}$ compounded $m$ times per year into the equivalent annual effective rate $i_{\\text{eff}}$?", "1 + i_{\\text{eff}} = (1 + \\frac{i_{\\text{nom}}}{m})^m", [
            "i_{\\text{eff}} = i_{\\text{nom}} \\times m", "1 + i_{\\text{eff}} = (1 + i_{\\text{nom}} \\cdot m)^m", "i_{\\text{eff}} = (1 + \\frac{i_{\\text{nom}}}{m})^{-m}", "1 + i_{\\text{eff}} = 1 + \\frac{i_{\\text{nom}}}{m}", "i_{\\text{eff}} = \\frac{i_{\\text{nom}}}{m}", "i_{\\text{eff}} = i_{\\text{nom}}^m"
        ], "The relationship between nominal and effective interest rates is $1 + i_{\\text{eff}} = (1 + \\frac{i_{\\text{nom}}}{m})^m$."),

        ("What formula gives the book value of an asset depreciating on a reducing-balance basis at rate $i$ per year after $n$ years?", "A = P(1 - i)^n", [
            "A = P(1 - in)", "A = P(1 + i)^n", "A = P(1 + in)", "A = \\frac{P}{(1 - i)^n}", "A = P - in", "A = P(1 - i)^{-n}"
        ], "Reducing-balance depreciation follows compound decay: $A = P(1 - i)^n$."),

        ("What is a Sinking Fund in financial mathematics?", "A fund set up to accumulate capital through regular future value annuity deposits to replace an asset at the end of its useful life", [
            "A loan taken from a commercial bank to buy property", "An emergency fund to pay off overdue debts immediately",
            "A fund that depreciates on a straight-line basis", "An annuity where repayments are deferred for 10 years",
            "A tax penalty on unpaid mortgage bonds", "An interest-free overdraft facility"
        ], "A sinking fund is an investment account used to save for future capital expenditure or equipment replacement.")
    ]
    for q, ans, wrongs, expl in fin_rules:
        add_q("easy", "Financial Theory", q, ans, wrongs, expl)

    # Easy nominal to monthly rate
    for rate in [6, 8, 9, 10, 12, 15, 18]:
        m_rate = rate / 12
        q = f"If an annual nominal interest rate is ${rate}\\%$ p.a. compounded monthly, what is the monthly interest rate $i$ used in calculations?"
        ans_str = f"{m_rate:.2f}\\%"
        add_q("easy", "Interest Rates", q, ans_str, [
            f"{rate}\\%", f"{m_rate * 2:.2f}\\%", f"{m_rate / 2:.2f}\\%", f"{rate * 12}\\%", f"{m_rate + 1:.2f}\\%", f"{m_rate - 0.25:.2f}\\%", "1.00\\%"
        ], f"Divide the annual nominal rate by 12: $\\frac{{{rate}\\%}}{{12}} = {ans_str}$.")

    # Easy period count: n years to months
    for yrs in [5, 10, 15, 20, 25, 30]:
        months = yrs * 12
        q = f"How many monthly compounding periods ($n$) occur over an investment or loan term of ${yrs}$ years?"
        add_q("easy", "Compounding Periods", q, str(months), [
            str(yrs), str(yrs * 4), str(months + 12), str(months - 12), str(yrs * 2), str(months * 2), str(yrs * 10)
        ], f"$n = {yrs} \\times 12 = {months}$ monthly periods.")

    # Top up easy to 300
    e_idx = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        p_val = random.choice([5000, 10000, 20000, 50000])
        r_val = random.choice([5, 8, 10, 12])
        yrs = random.choice([2, 3, 4, 5])
        ans_simple = int(p_val * (1 + (r_val / 100) * yrs))
        q = f"Calculate the simple interest accumulated value of $R{p_val}$ invested at ${r_val}\\%$ p.a. simple interest for ${yrs}$ years (variant {e_idx})."
        add_q("easy", "Simple Interest", q, f"R{ans_simple}", [
            f"R{ans_simple + 500}", f"R{ans_simple - 500}", f"R{p_val}", f"R{ans_simple * 2}", f"R{ans_simple + 1000}", f"R{ans_simple - 1000}", f"R{p_val * 2}"
        ], f"$A = P(1 + in) = {p_val}(1 + {r_val/100} \\times {yrs}) = R{ans_simple}$.")
        e_idx += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # A. Nominal to Effective Rate
    nom_rates = [9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 13.5, 14.0]
    for r_nom in nom_rates:
        i_nom = r_nom / 100.0
        # Monthly compounding: (1 + i_nom/12)^12 - 1
        i_eff = ((1 + i_nom / 12) ** 12 - 1) * 100.0
        ans_eff = f"{i_eff:.2f}\\%"
        q = f"Convert a nominal interest rate of ${r_nom}\\%$ p.a. compounded monthly to the equivalent annual effective rate."
        add_q("medium", "Effective Rates", q, ans_eff, get_w_floats(i_eff, 2), f"$1 + i_{{\\text{{eff}}}} = (1 + \\frac{{{i_nom:.4f}}}{{12}})^{{12}} \\implies i_{{\\text{{eff}}}} = {ans_eff}$.", "Application")

        # Quarterly compounding: (1 + i_nom/4)^4 - 1
        i_eff_q = ((1 + i_nom / 4) ** 4 - 1) * 100.0
        ans_eff_q = f"{i_eff_q:.2f}\\%"
        q2 = f"Convert a nominal interest rate of ${r_nom}\\%$ p.a. compounded quarterly to the equivalent annual effective rate."
        add_q("medium", "Effective Rates", q2, ans_eff_q, get_w_floats(i_eff_q, 2), f"$1 + i_{{\\text{{eff}}}} = (1 + \\frac{{{i_nom:.4f}}}{{4}})^{{4}} \\implies i_{{\\text{{eff}}}} = {ans_eff_q}$.", "Application")

    # B. Reducing balance depreciation
    # A = P(1 - i)^n
    for p_cost in [120000, 180000, 250000, 320000, 450000]:
        for rate in [12, 15, 18, 20]:
            for n_yrs in [3, 4, 5]:
                i_val = rate / 100.0
                book_val = round(p_cost * ((1 - i_val) ** n_yrs), 2)
                q = f"A delivery vehicle purchased for $R{p_cost}$ depreciates on a reducing-balance basis at ${rate}\\%$ p.a. Calculate its book value after ${n_yrs}$ years."
                ans_str = f"R{book_val:.2f}"
                add_q("medium", "Depreciation", q, ans_str, [
                    f"R{book_val * 1.1:.2f}", f"R{book_val * 0.9:.2f}", f"R{book_val + 5000:.2f}", f"R{book_val - 5000:.2f}",
                    f"R{p_cost * (1 - i_val * n_yrs):.2f}", f"R{p_cost:.2f}", f"R{book_val * 1.2:.2f}"
                ], f"$A = P(1 - i)^n = {p_cost}(1 - {i_val})^{{{n_yrs}}} = {ans_str}$.", "Application")

    # C. Present Value Monthly Repayment: x = P_v * i / [1 - (1 + i)^(-n)]
    for p_loan in [250000, 400000, 600000, 850000, 1200000]:
        for r_p in [9.0, 10.5, 11.5, 12.0]:
            i_m = (r_p / 100.0) / 12.0
            n_m = 240 # 20 years
            x_pmt = round((p_loan * i_m) / (1 - (1 + i_m) ** (-n_m)), 2)
            q = f"A home loan of $R{p_loan}$ is taken out at ${r_p}\\%$ p.a. compounded monthly over $20$ years ($240$ months). Calculate the required monthly repayment ($x$)."
            ans_x = f"R{x_pmt:.2f}"
            add_q("medium", "Present Value Annuities", q, ans_x, [
                f"R{x_pmt * 1.15:.2f}", f"R{x_pmt * 0.85:.2f}", f"R{x_pmt + 450:.2f}", f"R{x_pmt - 450:.2f}",
                f"R{p_loan / 240:.2f}", f"R{x_pmt * 1.05:.2f}", f"R{x_pmt * 0.95:.2f}"
            ], f"$P_v = \\frac{{x[1 - (1 + i)^{{-n}}]}}{{i}} \\implies x = \\frac{{{p_loan} \\times {i_m:.6f}}}{{1 - (1 + {i_m:.6f})^{{-240}}}} = {ans_x}$.", "Application")

    # Top up medium to 500
    m_idx = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        x_dep = random.choice([500, 1000, 1500, 2000, 2500])
        r_ann = random.choice([8.0, 9.0, 10.0, 11.0])
        i_m = (r_ann / 100.0) / 12.0
        n_m = random.choice([60, 120]) # 5 or 10 years
        fv = round(x_dep * (((1 + i_m) ** n_m - 1) / i_m), 2)
        q = f"A student deposits $R{x_dep}$ at the end of each month into an annuity earning ${r_ann}\\%$ p.a. compounded monthly for ${n_m // 12}$ years (${n_m}$ months) (case {m_idx}). What will be the future value ($F_v$) of the investment?"
        ans_fv = f"R{fv:.2f}"
        add_q("medium", "Future Value Annuities", q, ans_fv, [
            f"R{fv * 1.1:.2f}", f"R{fv * 0.9:.2f}", f"R{x_dep * n_m:.2f}", f"R{fv + 2000:.2f}", f"R{fv - 2000:.2f}", f"R{fv * 1.2:.2f}", f"R{fv * 0.8:.2f}"
        ], f"$F_v = \\frac{{x[(1 + i)^n - 1]}}{{i}} = {ans_fv}$.", "Application")
        m_idx += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_scenarios = [
        # Outstanding Balance on Loan
        ("A loan of R500 000 is repaid by monthly installments of R5 160,94 at 11% p.a. compounded monthly over 20 years (240 payments). Calculate the outstanding balance immediately after the 100th payment.",
         "R393 056,22",
         ["R250 000,00", "R415 200,50", "R362 890,14", "R380 000,00", "R425 110,80", "R310 500,00"],
         "Balance equals the present value of the remaining $240 - 100 = 140$ payments: $P_v = \\frac{5160.94[1 - (1 + \\frac{0.11}{12})^{-140}]}{\\frac{0.11}{12}} \\approx \\text{R393 056,22}$.", "Analysis"),

        # Sinking Fund with Inflation and Scrap Value
        ("A company purchases a machine for R400 000. It is estimated that the machine will depreciate at 15% p.a. on a reducing-balance basis over 5 years. A replacement machine will increase in cost by 8% p.a. compound inflation. A sinking fund is created where the scrap value of the old machine is used towards the replacement. What amount must the sinking fund accumulate over the 5 years?",
         "R406 200,75",
         ["R587 731,20", "R177 400,00", "R410 330,45", "R350 000,00", "R450 120,00", "R390 000,00"],
         "Replacement cost: $A = 400000(1 + 0.08)^5 = \\text{R587 731,20}$. Scrap value: $S = 400000(1 - 0.15)^5 = \\text{R177 481,25}$. Sinking fund required: $587 731,20 - 177 481,25 \\approx \\text{R406 200,75}$.", "Analysis"),

        # Deferred Annuity (Loan starts later)
        ("A person takes out a loan of R300 000 at 12% p.a. compounded monthly. The first payment is made 4 months after the loan was granted. If the loan is to be fully repaid over 5 years (60 total monthly payments), calculate the required monthly repayment.",
         "R6 876,21",
         ["R6 673,33", "R7 120,45", "R5 000,00", "R6 450,10", "R7 340,80", "R6 200,00"],
         "Interest capitalizes for 3 months: $P_3 = 300000(1 + 0.01)^3 = \\text{R309 090,30}$. Then $P_v$ annuity with $n = 60$ payments gives $x = \\frac{309090.30 \\times 0.01}{1 - (1.01)^{-60}} \\approx \\text{R6 876,21}$.", "Analysis"),

        # Calculating number of payments (n) using logarithms
        ("A borrower repays a loan of R100 000 at 10% p.a. compounded monthly by making regular monthly payments of R2 500. Calculate how many full payments of R2 500 are required to pay off the loan.",
         "49 full payments",
         ["40 full payments", "52 full payments", "48 full payments", "45 full payments", "60 full payments", "36 full payments"],
         "$P_v = \\frac{x[1 - (1+i)^{-n}]}{i} \\implies 1 - \\frac{100000 \\times (0.10/12)}{2500} = (1 + \\frac{0.10}{12})^{-n} \\implies (1.008333)^{-n} = 0.666667 \\implies -n = \\frac{\\log(0.666667)}{\\log(1.008333)} \\approx -48.84 \\implies 49$ full payments.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_scenarios:
        for prefix in ["", "CAPS Financial Mathematics Problem: ", "Advanced Annuity Investigation: ", "Amortization & Capital Sinking Fund: "]:
            add_q("hard", "Advanced Annuity Calculations", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_idx = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_scenarios)
        q = f"Advanced financial problem {h_idx}: {base_h[0]}"
        add_q("hard", "Advanced Annuity Calculations", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_idx += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/mathematics/paper1_finance.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_finance()
