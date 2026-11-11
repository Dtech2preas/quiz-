import json
import os
import random
import time

def build_finance_dataset():
    questions = []
    seen_questions = set()
    
    # Counts
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
        q_id = f"ML12_P1_FIN_{len(questions) + 1:04d}"
        
        questions.append({
            "id": q_id,
            "topic": "Finance",
            "subtopic": subtopic,
            "paper": "paper1",
            "difficulty": difficulty,
            "question": q_text,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_dist[:8],
            "explanation": explanation
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # Context arrays
    sa_names = ["Sipho", "Lerato", "Kagiso", "Fatima", "Thabo", "Aisha", "Mpho", "Bongani", "Zanele", "Devan", "Nolwazi", "Johan", "Khanyisile", "Riaan", "Nomsa", "Pieter", "Precious", "Tshepo", "Keitumetse", "Sbusiso"]
    goods = [
        ("laptop", 8500), ("refrigerator", 6500), ("smart TV", 7200), ("microwave oven", 1800),
        ("washing machine", 5400), ("dining table", 4200), ("gas stove", 3600), ("smartphone", 9500),
        ("generator", 11000), ("office desk", 2500), ("lawnmower", 3200), ("solar inverter", 14500)
    ]
    currencies = [
        ("US Dollar (USD)", "$", 18.50), ("British Pound (GBP)", "£", 23.40),
        ("Euro (EUR)", "€", 20.10), ("Botswana Pula (BWP)", "P", 1.35),
        ("Australian Dollar (AUD)", "A$", 12.20)
    ]
    
    # 1a. Direct VAT exclusive to inclusive and VAT amount (easy)
    for name in sa_names:
        for item, base_p in goods:
            for mult in [0.8, 0.9, 1.0, 1.1, 1.25, 1.5, 1.75]:
                price_ex = round(base_p * mult, 2)
                vat_amt = round(price_ex * 0.15, 2)
                price_inc = round(price_ex + vat_amt, 2)
                
                # Question 1: Calculate 15% VAT amount
                q1 = f"{name} purchases a {item} priced at R{price_ex:,.2f} excluding VAT. Calculate the VAT amount payable at the standard rate of 15%."
                c1 = f"R{vat_amt:,.2f}"
                d1 = [
                    f"R{round(price_ex * 0.14, 2):,.2f}",
                    f"R{round(price_ex * 0.10, 2):,.2f}",
                    f"R{round(price_ex / 1.15, 2):,.2f}",
                    f"R{round(price_ex * 1.15, 2):,.2f}",
                    f"R{round(vat_amt * 1.15, 2):,.2f}",
                    f"R{round(vat_amt * 0.85, 2):,.2f}",
                    f"R{round(price_ex * 0.16, 2):,.2f}"
                ]
                exp1 = f"VAT Amount = Price excluding VAT × 15% = R{price_ex:,.2f} × 0.15 = R{vat_amt:,.2f}."
                add_q("Value Added Tax (VAT)", "easy", q1, c1, d1, exp1)
                
                # Question 2: Price including VAT
                q2 = f"A retail store displays a {item} at R{price_ex:,.2f} excluding VAT. Determine the total selling price of the {item} including 15% VAT."
                c2 = f"R{price_inc:,.2f}"
                d2 = [
                    f"R{price_ex:,.2f}",
                    f"R{vat_amt:,.2f}",
                    f"R{round(price_ex * 1.14, 2):,.2f}",
                    f"R{round(price_ex + (price_ex * 0.10), 2):,.2f}",
                    f"R{round(price_ex * 1.20, 2):,.2f}",
                    f"R{round(price_inc + 100, 2):,.2f}",
                    f"R{round(price_inc - 100, 2):,.2f}"
                ]
                exp2 = f"Selling Price including VAT = Price excluding VAT × 1.15 = R{price_ex:,.2f} × 1.15 = R{price_inc:,.2f}."
                add_q("Value Added Tax (VAT)", "easy", q2, c2, d2, exp2)
                
                # Question 3: Simple interest calculation
                rate = random.choice([6.0, 7.5, 8.0, 9.0, 10.5])
                years = random.choice([2, 3, 4, 5])
                p_inv = round(base_p * 2 * mult, 2)
                si = round(p_inv * (rate / 100.0) * years, 2)
                tot_si = round(p_inv + si, 2)
                
                q3 = f"{name} deposits R{p_inv:,.2f} into a fixed notice bank account earning simple interest at {rate}% per annum for {years} years. Calculate the total interest earned."
                c3 = f"R{si:,.2f}"
                d3 = [
                    f"R{tot_si:,.2f}",
                    f"R{round(p_inv * (rate / 100.0), 2):,.2f}",
                    f"R{round(si * 1.15, 2):,.2f}",
                    f"R{round(p_inv * (1 + rate/100.0)**years - p_inv, 2):,.2f}",
                    f"R{round(si * 0.85, 2):,.2f}",
                    f"R{round(si + 250, 2):,.2f}",
                    f"R{round(si - 250, 2):,.2f}"
                ]
                exp3 = f"Simple Interest (I) = P × i × n = R{p_inv:,.2f} × {rate/100.0} × {years} = R{si:,.2f}."
                add_q("Simple & Compound Interest", "easy", q3, c3, d3, exp3)

    # 1b. Definitions & terminology (easy)
    vocab = [
        ("Gross salary", "The total earnings of an employee before any compulsory or voluntary deductions are made.", 
         ["The final take-home salary after all deductions have been subtracted.", "The basic salary excluding housing allowance and travel allowance.", "The total income tax paid to SARS for the financial year.", "The net amount deposited into the employee bank account.", "The salary remaining after deducting pension fund only.", "The employer's annual contribution to the employee's retirement annuity."]),
        ("Net salary", "The actual take-home pay received by an employee after all statutory and voluntary deductions.",
         ["The total income of the employee before any taxes or deductions are subtracted.", "The total taxable fringe benefits received by an employee.", "The total amount of PAYE deducted from the salary.", "The employer's total contribution to UIF and pension.", "The gross salary plus all overtime payments before tax.", "The annual bonus paid during December."]),
        ("UIF (Unemployment Insurance Fund)", "A statutory deduction of 1% from employee salary, matched by 1% from the employer, providing short-term relief during unemployment.",
         ["A voluntary medical aid insurance payment deducted monthly.", "A 15% value added tax deducted on goods and services.", "An annual SARS tax rebate for citizens over 65 years.", "A compulsory company pension contribution of 7.5%.", "A credit life insurance premium charged on hire purchase agreements.", "A municipality levy charged for sewage and sanitation."]),
        ("Medical Scheme Fees Tax Credit (MTC)", "A fixed, non-refundable monthly rebate deducted directly from calculated tax payable for belonging to a registered medical scheme.",
         ["A deduction from gross salary that reduces taxable income before tax calculation.", "A cash refund sent directly by SARS into the taxpayer's bank account every month.", "A percentage discount on prescription medicine at local pharmacies.", "An exemption from paying Unemployment Insurance Fund (UIF).", "A medical subsidy paid exclusively by government employers.", "An additional surcharge added to taxpayers earning above R1,000,000."]),
        ("Break-even point", "The level of sales or production where total revenue exactly equals total costs, resulting in zero profit and zero loss.",
         ["The point where profit is at its maximum possible value.", "The minimum selling price allowed by South African trade regulations.", "The level of output where variable costs equal fixed costs.", "The point where a business ceases all trading activities due to insolvency.", "The total capital invested by the owner at the start of operations.", "The monthly installment required to pay off a commercial bank loan."]),
        ("Inflation", "The general and sustained increase in the prices of goods and services over time, leading to a decrease in the purchasing power of money.",
         ["The interest rate charged by commercial banks on home loans.", "The fee charged by municipal councils for refuse removal and electricity.", "The total depreciation in the value of fixed assets over their useful life.", "The percentage discount offered to customers who pay in cash.", "The difference between gross profit and net profit in a business.", "The rate of exchange between the South African Rand and the US Dollar."]),
        ("Hire Purchase", "A credit agreement where the buyer pays a deposit and takes possession of the good, paying the balance plus interest in monthly installments while ownership remains with the seller until paid in full.",
         ["A cash transaction where the full price is paid immediately with a 10% discount.", "A commercial lease agreement where the equipment is returned to the store after one year.", "A municipal tariff system based on stepped consumption blocks.", "A life insurance policy taken out to secure a 20-year mortgage bond.", "A lay-bye agreement where the buyer only receives the item after paying all installments.", "An investment in government retail bonds earning compound interest."])
    ]
    for term, correct_def, wrong_defs in vocab:
        q_text = f"In Mathematical Literacy and South African financial contexts, define the term '{term}'."
        add_q("Financial Terminology", "easy", q_text, correct_def, wrong_defs, f"Official CAPS definition: {term} is defined as: {correct_def}")

    # 1c. UIF deductions (1% capped at R177.12)
    salaries = [8500, 11200, 14500, 17712, 22000, 28500, 35000, 42000]
    for sal in salaries:
        for name in sa_names[:8]:
            uif_expected = min(round(sal * 0.01, 2), 177.12)
            q_uif = f"{name} earns a gross monthly salary of R{sal:,.2f}. If the UIF contribution rate is 1% of gross earnings capped at a maximum of R177.12 per month, calculate {name}'s monthly UIF deduction."
            c_uif = f"R{uif_expected:,.2f}"
            d_uif = [
                f"R{sal * 0.01:,.2f}" if sal > 17712 else f"R177.12",
                f"R{round(sal * 0.02, 2):,.2f}",
                f"R{round(sal * 0.005, 2):,.2f}",
                f"R{round(sal * 0.075, 2):,.2f}",
                f"R{round(uif_expected + 25.0, 2):,.2f}",
                f"R{round(uif_expected - 25.0, 2):,.2f}",
                f"R{round(uif_expected * 12, 2):,.2f}"
            ]
            exp_uif = f"UIF = 1% of R{sal:,.2f} = R{sal * 0.01:,.2f}. Since the maximum cap is R177.12, the deduction is R{uif_expected:,.2f}."
            add_q("Payslips & Salary Structure", "easy", q_uif, c_uif, d_uif, exp_uif)

    # 1d. Basic Currency conversions (easy)
    for curr_name, sym, rate in currencies:
        for zar_amt in [1500, 2500, 4800, 6000, 8500, 12000]:
            foreign = round(zar_amt / rate, 2)
            q_curr = f"A traveler exchanges R{zar_amt:,.2f} for {curr_name} at an exchange rate of 1 {curr_name.split()[0]} = R{rate:.2f}. How much foreign currency will the traveler receive?"
            c_curr = f"{sym}{foreign:,.2f}"
            d_curr = [
                f"{sym}{round(zar_amt * rate, 2):,.2f}",
                f"{sym}{round(foreign * 1.15, 2):,.2f}",
                f"{sym}{round(foreign * 0.85, 2):,.2f}",
                f"{sym}{round(zar_amt / (rate * 1.1), 2):,.2f}",
                f"{sym}{round(foreign + 50, 2):,.2f}",
                f"{sym}{round(foreign - 50, 2):,.2f}",
                f"{sym}{round(foreign * 1.05, 2):,.2f}"
            ]
            exp_curr = f"Foreign Currency = Amount in ZAR ÷ Exchange Rate = R{zar_amt:,.2f} ÷ {rate:.2f} = {sym}{foreign:,.2f}."
            add_q("Exchange Rates & Budgets", "easy", q_curr, c_curr, d_curr, exp_curr)

    # Fill remaining easy if needed
    for i in range(100):
        if counts["easy"] >= target_easy:
            break
        cost_p = random.randint(120, 850)
        mark_perc = random.choice([20, 25, 30, 40, 50, 60])
        profit = round(cost_p * (mark_perc / 100.0), 2)
        sp = round(cost_p + profit, 2)
        q_mark = f"A school tuckshop buys a case of fruit juices for R{cost_p:,.2f} and applies a mark-up of {mark_perc}% on cost price. Calculate the selling price of the case of fruit juices."
        c_mark = f"R{sp:,.2f}"
        d_mark = [
            f"R{profit:,.2f}",
            f"R{round(cost_p * 1.15, 2):,.2f}",
            f"R{round(cost_p + mark_perc, 2):,.2f}",
            f"R{round(sp * 1.15, 2):,.2f}",
            f"R{round(cost_p / (mark_perc / 100.0), 2):,.2f}",
            f"R{round(sp + 35, 2):,.2f}",
            f"R{round(sp - 35, 2):,.2f}"
        ]
        exp_mark = f"Mark-up = {mark_perc}% of R{cost_p:,.2f} = R{profit:,.2f}. Selling Price = Cost + Mark-up = R{cost_p:,.2f} + R{profit:,.2f} = R{sp:,.2f}."
        add_q("Profit & Mark-up", "easy", q_mark, c_mark, d_mark, exp_mark)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    # 2a. Real SARS Personal Income Tax (2023/2024 Tax Brackets & Rebates)
    # Brackets:
    # 1: 0 - 237,100 (18%)
    # 2: 237,101 - 370,500 (42,678 + 26% above 237,100)
    # 3: 370,501 - 512,800 (77,362 + 31% above 370,500)
    # 4: 512,801 - 673,000 (121,475 + 36% above 512,800)
    # 5: 673,001 - 857,900 (179,147 + 39% above 673,000)
    # Rebates: Primary (under 65): 17,235. Secondary (65-74): 9,444. Tertiary (75+): 3,145.
    tax_scenarios = [
        # (taxable_income, age, bracket_num, bracket_desc, base_tax, rate, threshold, dependents)
        (210000, 34, 1, "18% of taxable income", 0, 0.18, 0, 0),
        (225000, 42, 1, "18% of taxable income", 0, 0.18, 0, 1),
        (280000, 29, 2, "R42,678 + 26% of taxable income above R237,100", 42678, 0.26, 237100, 0),
        (315000, 45, 2, "R42,678 + 26% of taxable income above R237,100", 42678, 0.26, 237100, 2),
        (350000, 52, 2, "R42,678 + 26% of taxable income above R237,100", 42678, 0.26, 237100, 1),
        (395000, 38, 3, "R77,362 + 31% of taxable income above R370,500", 77362, 0.31, 370500, 0),
        (440000, 67, 3, "R77,362 + 31% of taxable income above R370,500", 77362, 0.31, 370500, 1),
        (480000, 40, 3, "R77,362 + 31% of taxable income above R370,500", 77362, 0.31, 370500, 3),
        (540000, 49, 4, "R121,475 + 36% of taxable income above R512,800", 121475, 0.36, 512800, 2),
        (610000, 76, 4, "R121,475 + 36% of taxable income above R512,800", 121475, 0.36, 512800, 0),
        (720000, 55, 5, "R179,147 + 39% of taxable income above R673,000", 179147, 0.39, 673000, 2)
    ]
    
    for ti_base, age, br_num, br_str, base_tax, rate, thresh, deps in tax_scenarios:
        for delta in [-15000, -8000, 0, 6000, 14000, 22000]:
            ti = ti_base + delta
            # Ensure within bracket
            if br_num == 1 and ti > 237100: continue
            if br_num == 2 and (ti <= 237100 or ti > 370500): continue
            if br_num == 3 and (ti <= 370500 or ti > 512800): continue
            if br_num == 4 and (ti <= 512800 or ti > 673000): continue
            if br_num == 5 and (ti <= 673000 or ti > 857900): continue
            
            tax_before_rebate = base_tax + (ti - thresh) * rate
            
            # Rebates
            rebate = 17235
            rebate_str = "Primary rebate of R17,235"
            if age >= 65 and age < 75:
                rebate += 9444
                rebate_str = "Primary (R17,235) and Secondary rebate (R9,444) totaling R26,679"
            elif age >= 75:
                rebate += 9444 + 3145
                rebate_str = "Primary (R17,235), Secondary (R9,444), and Tertiary rebate (R3,145) totaling R29,824"
                
            # Medical tax credit (monthly: R364 main, R364 1st dep, R246 add)
            annual_mtc = 0
            mtc_str = ""
            if deps > 0:
                monthly_mtc = 364 # main
                if deps >= 1: monthly_mtc += 364
                if deps > 1: monthly_mtc += (deps - 1) * 246
                annual_mtc = monthly_mtc * 12
                mtc_str = f" They belong to a registered medical aid scheme with {deps} dependent(s), qualifying for an annual Medical Scheme Fees Tax Credit of R{annual_mtc:,.2f}."
                
            tax_payable = max(0.0, tax_before_rebate - rebate - annual_mtc)
            monthly_tax = round(tax_payable / 12.0, 2)
            
            name = random.choice(sa_names)
            # Question A: Annual tax payable
            q_tax1 = (f"{name}, aged {age}, has an annual taxable income of R{ti:,.2f} for the 2023/2024 tax year. "
                      f"According to the SARS tax table, Bracket {br_num} applies: '{br_str}'. "
                      f"Eligible rebates: {rebate_str}.{mtc_str} "
                      f"Calculate {name}'s total annual income tax payable.")
            c_tax1 = f"R{tax_payable:,.2f}"
            d_tax1 = [
                f"R{tax_before_rebate:,.2f}",
                f"R{tax_before_rebate - rebate:,.2f}" if annual_mtc > 0 else f"R{tax_before_rebate - 17235:,.2f}",
                f"R{tax_payable + 5000:,.2f}",
                f"R{tax_payable - 5000:,.2f}",
                f"R{round(tax_payable * 1.10, 2):,.2f}",
                f"R{round(tax_payable * 0.90, 2):,.2f}",
                f"R{monthly_tax:,.2f}"
            ]
            exp_tax1 = (f"Step 1: Tax before rebate = R{base_tax:,.2f} + ({rate*100:.0f}% × (R{ti:,.2f} - R{thresh:,.2f})) = R{tax_before_rebate:,.2f}. "
                        f"Step 2: Total rebates = R{rebate:,.2f}. "
                        f"Step 3: Annual MTC = R{annual_mtc:,.2f}. "
                        f"Step 4: Tax payable = R{tax_before_rebate:,.2f} - R{rebate:,.2f} - R{annual_mtc:,.2f} = R{tax_payable:,.2f}.")
            add_q("Personal Income Tax & Rebates", "medium", q_tax1, c_tax1, d_tax1, exp_tax1)
            
            # Question B: Monthly PAYE
            q_tax2 = (f"From the tax calculation where {name}'s total annual tax payable is R{tax_payable:,.2f}, "
                      f"determine the monthly PAYE (Pay-As-You-Earn) deduction that must be reflected on {name}'s monthly payslip.")
            c_tax2 = f"R{monthly_tax:,.2f}"
            d_tax2 = [
                f"R{round(tax_before_rebate / 12.0, 2):,.2f}",
                f"R{round((tax_payable + rebate) / 12.0, 2):,.2f}",
                f"R{round(monthly_tax * 1.15, 2):,.2f}",
                f"R{round(monthly_tax * 0.85, 2):,.2f}",
                f"R{round(monthly_tax + 250, 2):,.2f}",
                f"R{round(monthly_tax - 250, 2):,.2f}",
                f"R{round(tax_payable / 10.0, 2):,.2f}"
            ]
            exp_tax2 = f"Monthly PAYE = Annual Tax Payable ÷ 12 = R{tax_payable:,.2f} ÷ 12 = R{monthly_tax:,.2f}."
            add_q("Personal Income Tax & Rebates", "medium", q_tax2, c_tax2, d_tax2, exp_tax2)

    # 2b. Stepped Municipal Water Tariffs (Sliding scale)
    # Authentic sliding scale:
    # Block 1: 0 - 6 kl @ R15.50/kl
    # Block 2: >6 - 15 kl @ R22.40/kl
    # Block 3: >15 - 30 kl @ R31.80/kl
    # Block 4: >30 - 45 kl @ R42.50/kl
    # All tariffs exclude 15% VAT.
    water_usages = [12, 14, 18, 22, 25, 28, 32, 35, 40]
    for kl in water_usages:
        for municipality in ["City of Johannesburg", "eThekwini Municipality", "City of Cape Town", "Mangaung Metropolitan Municipality"]:
            # Cost calculation
            cost_ex = 0.0
            breakdown = []
            if kl <= 6:
                cost_ex = kl * 15.50
                breakdown.append(f"Block 1 (0-6 kl): {kl} kl × R15.50 = R{kl*15.50:.2f}")
            elif kl <= 15:
                cost_ex = (6 * 15.50) + ((kl - 6) * 22.40)
                breakdown.append("Block 1 (0-6 kl): 6 kl × R15.50 = R93.00")
                breakdown.append(f"Block 2 (>6-15 kl): {kl-6} kl × R22.40 = R{(kl-6)*22.40:.2f}")
            elif kl <= 30:
                cost_ex = (6 * 15.50) + (9 * 22.40) + ((kl - 15) * 31.80)
                breakdown.append("Block 1: 6 kl × R15.50 = R93.00")
                breakdown.append("Block 2: 9 kl × R22.40 = R201.60")
                breakdown.append(f"Block 3 (>15-30 kl): {kl-15} kl × R31.80 = R{(kl-15)*31.80:.2f}")
            else:
                cost_ex = (6 * 15.50) + (9 * 22.40) + (15 * 31.80) + ((kl - 30) * 42.50)
                breakdown.append("Block 1: 6 × R15.50 = R93.00")
                breakdown.append("Block 2: 9 × R22.40 = R201.60")
                breakdown.append("Block 3: 15 × R31.80 = R477.00")
                breakdown.append(f"Block 4 (>30 kl): {kl-30} kl × R42.50 = R{(kl-30)*42.50:.2f}")
                
            cost_inc = round(cost_ex * 1.15, 2)
            cost_ex = round(cost_ex, 2)
            
            q_w = (f"A household in {municipality} consumes {kl} kℓ of domestic water in a 30-day billing cycle. "
                   f"The stepped tariff table (excluding VAT) is:\n"
                   f"• Block 1 (0 – 6 kℓ): R15.50 per kℓ\n"
                   f"• Block 2 (>6 – 15 kℓ): R22.40 per kℓ\n"
                   f"• Block 3 (>15 – 30 kℓ): R31.80 per kℓ\n"
                   f"• Block 4 (>30 – 45 kℓ): R42.50 per kℓ\n"
                   f"Calculate the total water bill payable including 15% VAT.")
            c_w = f"R{cost_inc:,.2f}"
            d_w = [
                f"R{cost_ex:,.2f}",
                f"R{round(kl * 31.80 * 1.15, 2):,.2f}",
                f"R{round(kl * 42.50 * 1.15, 2):,.2f}",
                f"R{round(kl * 22.40 * 1.15, 2):,.2f}",
                f"R{round(cost_inc * 1.10, 2):,.2f}",
                f"R{round(cost_inc * 0.90, 2):,.2f}",
                f"R{round(cost_ex + (kl * 15.50), 2):,.2f}"
            ]
            exp_w = f"Calculations:\n" + "\n".join(breakdown) + f"\nTotal excluding VAT = R{cost_ex:,.2f}. Adding 15% VAT: R{cost_ex:,.2f} × 1.15 = R{cost_inc:,.2f}."
            add_q("Municipal Tariffs (Water & Electricity)", "medium", q_w, c_w, d_w, exp_w)

    # 2c. Stepped Electricity Tariffs
    # Block 1: 0 - 50 kWh @ R1.65/kWh
    # Block 2: 51 - 350 kWh @ R2.15/kWh
    # Block 3: 351 - 600 kWh @ R2.85/kWh
    elec_usages = [180, 240, 320, 380, 420, 480, 550]
    for kwh in elec_usages:
        cost_ex = 0.0
        if kwh <= 50:
            cost_ex = kwh * 1.65
        elif kwh <= 350:
            cost_ex = (50 * 1.65) + ((kwh - 50) * 2.15)
        else:
            cost_ex = (50 * 1.65) + (300 * 2.15) + ((kwh - 350) * 2.85)
        cost_inc = round(cost_ex * 1.15, 2)
        cost_ex = round(cost_ex, 2)
        
        q_e = (f"A domestic prepaid electricity meter records a monthly consumption of {kwh} kWh. "
               f"Tariffs (excl. VAT):\n"
               f"• Block 1 (0 – 50 kWh): R1.65 per kWh\n"
               f"• Block 2 (51 – 350 kWh): R2.15 per kWh\n"
               f"• Block 3 (351 – 600 kWh): R2.85 per kWh\n"
               f"Calculate the total amount paid by the consumer including 15% VAT.")
        c_e = f"R{cost_inc:,.2f}"
        d_e = [
            f"R{cost_ex:,.2f}",
            f"R{round(kwh * 2.15 * 1.15, 2):,.2f}",
            f"R{round(kwh * 2.85 * 1.15, 2):,.2f}",
            f"R{round(kwh * 1.65 * 1.15, 2):,.2f}",
            f"R{round(cost_inc + 50, 2):,.2f}",
            f"R{round(cost_inc - 50, 2):,.2f}",
            f"R{round(cost_inc * 1.05, 2):,.2f}"
        ]
        exp_e = f"Cost excl. VAT = Block 1 (50 × 1.65 = R82.50) + remaining blocks = R{cost_ex:,.2f}. Adding 15% VAT = R{cost_ex:,.2f} × 1.15 = R{cost_inc:,.2f}."
        add_q("Municipal Tariffs (Water & Electricity)", "medium", q_e, c_e, d_e, exp_e)

    # 2d. Hire Purchase Agreements
    hp_items = [
        ("double-door refrigerator", 14999, 10, 24, 18.5, 45.00),
        ("lounge suite", 18500, 15, 36, 19.0, 52.00),
        ("high-end gaming computer", 22999, 10, 24, 17.5, 48.00),
        ("bedroom furniture set", 16800, 10, 36, 18.0, 42.00),
        ("solar power backup system", 34500, 20, 36, 16.5, 65.00),
        ("commercial ride-on lawnmower", 28000, 15, 24, 19.5, 55.00)
    ]
    for item_name, cash_p, dep_pct, term_m, hp_rate, m_fee in hp_items:
        dep_amt = round(cash_p * (dep_pct / 100.0), 2)
        balance = round(cash_p - dep_amt, 2)
        term_y = term_m / 12.0
        tot_interest = round(balance * (hp_rate / 100.0) * term_y, 2)
        tot_repaid = round(balance + tot_interest, 2)
        monthly_inst = round(tot_repaid / term_m, 2)
        tot_monthly = round(monthly_inst + m_fee, 2)
        tot_hp_cost = round(dep_amt + (tot_monthly * term_m), 2)
        diff_from_cash = round(tot_hp_cost - cash_p, 2)
        
        for name in sa_names[:6]:
            q_hp1 = (f"{name} buys a {item_name} on a Hire Purchase (HP) agreement. "
                     f"Cash price: R{cash_p:,.2f}. Required deposit: {dep_pct}%. "
                     f"The remaining balance attracts simple interest at {hp_rate}% per annum over {term_m} months. "
                     f"A monthly insurance/admin fee of R{m_fee:,.2f} is added to each payment. "
                     f"Calculate the total monthly payment ({name}'s total monthly installment).")
            c_hp1 = f"R{tot_monthly:,.2f}"
            d_hp1 = [
                f"R{monthly_inst:,.2f}",
                f"R{round(cash_p / term_m, 2):,.2f}",
                f"R{round(tot_repaid / term_m + (cash_p * 0.15 / term_m), 2):,.2f}",
                f"R{round(tot_monthly * 1.15, 2):,.2f}",
                f"R{round(tot_monthly * 0.85, 2):,.2f}",
                f"R{round(tot_monthly + 100, 2):,.2f}",
                f"R{round(tot_monthly - 100, 2):,.2f}"
            ]
            exp_hp1 = (f"Deposit = {dep_pct}% of R{cash_p:,.2f} = R{dep_amt:,.2f}. "
                       f"Balance = R{cash_p:,.2f} - R{dep_amt:,.2f} = R{balance:,.2f}. "
                       f"Interest = R{balance:,.2f} × {hp_rate/100.0} × {term_y} years = R{tot_interest:,.2f}. "
                       f"Amount to repay = R{tot_repaid:,.2f}. Monthly loan payment = R{tot_repaid:,.2f} ÷ {term_m} = R{monthly_inst:,.2f}. "
                       f"Total monthly installment = R{monthly_inst:,.2f} + R{m_fee:,.2f} = R{tot_monthly:,.2f}.")
            add_q("Hire Purchase & Loans", "medium", q_hp1, c_hp1, d_hp1, exp_hp1)
            
            q_hp2 = (f"Using the Hire Purchase details for the {item_name} (Cash price: R{cash_p:,.2f}, Deposit: R{dep_amt:,.2f}, "
                     f"and {term_m} monthly payments of R{tot_monthly:,.2f}), "
                     f"calculate how much more {name} will pay in total on HP compared to paying the cash price upfront.")
            c_hp2 = f"R{diff_from_cash:,.2f}"
            d_hp2 = [
                f"R{tot_interest:,.2f}",
                f"R{tot_hp_cost:,.2f}",
                f"R{round(tot_monthly * term_m, 2):,.2f}",
                f"R{round(diff_from_cash * 1.10, 2):,.2f}",
                f"R{round(diff_from_cash * 0.90, 2):,.2f}",
                f"R{round(cash_p * 0.15, 2):,.2f}",
                f"R{round(diff_from_cash + 500, 2):,.2f}"
            ]
            exp_hp2 = (f"Total cost on HP = Deposit + (Monthly payment × {term_m}) = R{dep_amt:,.2f} + (R{tot_monthly:,.2f} × {term_m}) = R{tot_hp_cost:,.2f}. "
                       f"Difference = Total HP cost - Cash price = R{tot_hp_cost:,.2f} - R{cash_p:,.2f} = R{diff_from_cash:,.2f}.")
            add_q("Hire Purchase & Loans", "medium", q_hp2, c_hp2, d_hp2, exp_hp2)

    # 2e. Compound Interest vs Simple Interest (medium)
    for p_val in [25000, 45000, 60000, 85000, 120000]:
        for r_val in [7.0, 8.5, 9.25, 10.0]:
            for t_val in [3, 4, 5]:
                # Annually
                ci_ann = round(p_val * ((1 + r_val / 100.0) ** t_val), 2)
                # Monthly
                ci_m = round(p_val * ((1 + (r_val / 100.0) / 12.0) ** (t_val * 12)), 2)
                si_val = round(p_val * (1 + (r_val / 100.0) * t_val), 2)
                
                name = random.choice(sa_names)
                q_ci = (f"{name} invests R{p_val:,.2f} in a bank fixed deposit for {t_val} years at {r_val}% per annum compound interest, compounded annually. "
                        f"Calculate the accumulated maturity value at the end of the investment term.")
                c_ci = f"R{ci_ann:,.2f}"
                d_ci = [
                    f"R{si_val:,.2f}",
                    f"R{ci_m:,.2f}",
                    f"R{round(ci_ann - p_val, 2):,.2f}",
                    f"R{round(ci_ann * 1.10, 2):,.2f}",
                    f"R{round(ci_ann * 0.90, 2):,.2f}",
                    f"R{round(ci_ann + 1500, 2):,.2f}",
                    f"R{round(ci_ann - 1500, 2):,.2f}"
                ]
                exp_ci = f"A = P(1 + i)^n = R{p_val:,.2f}(1 + {r_val/100.0})^{t_val} = R{ci_ann:,.2f}."
                add_q("Simple & Compound Interest", "medium", q_ci, c_ci, d_ci, exp_ci)

    # Fill remaining medium
    while counts["medium"] < target_med:
        p_val = random.randint(30000, 95000)
        r_val = random.choice([6.5, 7.25, 8.0, 8.75, 9.5])
        t_val = random.choice([2, 3, 4])
        ci_ann = round(p_val * ((1 + r_val / 100.0) ** t_val), 2)
        interest_earned = round(ci_ann - p_val, 2)
        name = random.choice(sa_names)
        q_fill = f"{name} deposits R{p_val:,.2f} into an investment fund earning {r_val}% compound interest compounded annually. Calculate the total interest earned over {t_val} years."
        c_fill = f"R{interest_earned:,.2f}"
        d_fill = [
            f"R{ci_ann:,.2f}",
            f"R{round(p_val * (r_val/100.0) * t_val, 2):,.2f}",
            f"R{round(interest_earned * 1.15, 2):,.2f}",
            f"R{round(interest_earned * 0.85, 2):,.2f}",
            f"R{round(interest_earned + 800, 2):,.2f}",
            f"R{round(interest_earned - 800, 2):,.2f}",
            f"R{round(interest_earned * 1.08, 2):,.2f}"
        ]
        exp_fill = f"A = R{p_val:,.2f}(1 + {r_val/100.0})^{t_val} = R{ci_ann:,.2f}. Total Interest = A - P = R{ci_ann:,.2f} - R{p_val:,.2f} = R{interest_earned:,.2f}."
        add_q("Simple & Compound Interest", "medium", q_fill, c_fill, d_fill, exp_fill)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Home Loan Bond Amortization & Repayments
    # Bond factor table: monthly repayment per R1,000 for 20-year bond:
    # 9.0% -> R9.00; 9.5% -> R9.32; 10.0% -> R9.65; 10.5% -> R9.98; 11.0% -> R10.32; 11.5% -> R10.66
    factors = [
        (9.0, 9.00), (9.5, 9.32), (10.0, 9.65), (10.5, 9.98), (11.0, 10.32), (11.5, 10.66)
    ]
    bond_amounts = [650000, 850000, 1050000, 1250000, 1500000, 1850000]
    for p_bond in bond_amounts:
        for rate, factor in factors:
            monthly_bond = round((p_bond / 1000.0) * factor, 2)
            tot_20y = round(monthly_bond * 240, 2)
            interest_20y = round(tot_20y - p_bond, 2)
            name = random.choice(sa_names)
            
            # Question 1: Total interest over 20 years
            q_bond1 = (f"{name} purchases a residential house by securing a 20-year mortgage bond of R{p_bond:,.2f} from a commercial bank at an interest rate of {rate}% per annum. "
                       f"The bank loan factor table specifies a monthly installment of R{factor:.2f} per R1,000 borrowed. "
                       f"Calculate the total interest {name} will pay to the bank over the entire 20-year loan term.")
            c_bond1 = f"R{interest_20y:,.2f}"
            d_bond1 = [
                f"R{tot_20y:,.2f}",
                f"R{round(p_bond * (rate / 100.0) * 20, 2):,.2f}",
                f"R{round(monthly_bond * 12, 2):,.2f}",
                f"R{round(interest_20y * 1.10, 2):,.2f}",
                f"R{round(interest_20y * 0.90, 2):,.2f}",
                f"R{round(interest_20y + 50000, 2):,.2f}",
                f"R{round(interest_20y - 50000, 2):,.2f}"
            ]
            exp_bond1 = (f"Step 1: Monthly repayment = (R{p_bond:,.2f} ÷ 1,000) × R{factor:.2f} = R{monthly_bond:,.2f}. "
                         f"Step 2: Total paid over 20 years (240 months) = R{monthly_bond:,.2f} × 240 = R{tot_20y:,.2f}. "
                         f"Step 3: Total Interest = Total Paid - Capital Loan = R{tot_20y:,.2f} - R{p_bond:,.2f} = R{interest_20y:,.2f}.")
            add_q("Hire Purchase & Loans", "hard", q_bond1, c_bond1, d_bond1, exp_bond1)

            # Question 2: Monthly statement interest vs capital reduction
            # First month interest = P * (rate / 100) / 12
            month1_int = round(p_bond * (rate / 100.0) / 12.0, 2)
            month1_cap = round(monthly_bond - month1_int, 2)
            balance_m1 = round(p_bond - month1_cap, 2)
            
            q_bond2 = (f"Continuing with {name}'s home loan of R{p_bond:,.2f} at {rate}% per annum with a monthly payment of R{monthly_bond:,.2f}: "
                       f"In Month 1, simple monthly interest is charged on the full opening balance. "
                       f"Calculate the amount of the first monthly installment that goes towards reducing the actual loan capital balance.")
            c_bond2 = f"R{month1_cap:,.2f}"
            d_bond2 = [
                f"R{month1_int:,.2f}",
                f"R{monthly_bond:,.2f}",
                f"R{round(monthly_bond / 2.0, 2):,.2f}",
                f"R{round(month1_cap * 1.20, 2):,.2f}",
                f"R{round(month1_cap * 0.80, 2):,.2f}",
                f"R{round(p_bond / 240.0, 2):,.2f}",
                f"R{balance_m1:,.2f}"
            ]
            exp_bond2 = (f"Month 1 Interest = R{p_bond:,.2f} × ({rate}% ÷ 12) = R{month1_int:,.2f}. "
                         f"Capital reduction = Monthly Payment - Interest = R{monthly_bond:,.2f} - R{month1_int:,.2f} = R{month1_cap:,.2f}.")
            add_q("Hire Purchase & Loans", "hard", q_bond2, c_bond2, d_bond2, exp_bond2)

    # 3b. Inflation & Multi-Year Purchasing Power
    # Real CPI scenarios
    cpi_scenarios = [
        ("loaf of white bread", 14.50, 5.8, 4),
        ("2-litre fresh milk", 28.00, 6.2, 5),
        ("10 kg bag of maize meal", 98.00, 7.1, 3),
        ("500g brick of butter", 64.00, 6.5, 4),
        ("private school tuition", 45000.00, 7.5, 6),
        ("medical aid monthly premium", 3800.00, 8.2, 5)
    ]
    for item_name, init_price, inf_rate, yrs in cpi_scenarios:
        future_price = round(init_price * ((1 + inf_rate / 100.0) ** yrs), 2)
        total_increase = round(future_price - init_price, 2)
        perc_tot = round((total_increase / init_price) * 100.0, 2)
        
        q_inf = (f"According to Statistics South Africa (Stats SA), the average annual inflation rate for {item_name} was recorded at {inf_rate}% per annum compounded. "
                 f"If the base price was R{init_price:,.2f}, determine the projected price of this item after {yrs} years due to inflation.")
        c_inf = f"R{future_price:,.2f}"
        d_inf = [
            f"R{round(init_price * (1 + (inf_rate/100.0) * yrs), 2):,.2f}",
            f"R{total_increase:,.2f}",
            f"R{round(future_price * 1.15, 2):,.2f}",
            f"R{round(future_price * 0.85, 2):,.2f}",
            f"R{round(future_price + 25, 2):,.2f}",
            f"R{round(future_price - 25, 2):,.2f}",
            f"R{round(init_price * (1 + inf_rate/100.0), 2):,.2f}"
        ]
        exp_inf = f"Compound Inflation Formula: A = P(1 + r)^n = R{init_price:,.2f}(1 + {inf_rate/100.0})^{yrs} = R{future_price:,.2f}."
        add_q("Inflation & CPI", "hard", q_inf, c_inf, d_inf, exp_inf)

    # 3c. Business Break-Even Analysis with Target Profit
    be_scenarios = [
        ("custom t-shirt printing enterprise", 8500, 65.00, 140.00, 12000),
        ("mobile car detailing service", 12000, 45.00, 160.00, 15000),
        ("artisan bakery producing sourdough loaves", 9800, 18.00, 48.00, 14000),
        ("school stationery packs distributor", 7200, 85.00, 155.00, 9500),
        ("organic fruit jam producer", 6400, 22.00, 58.00, 8000)
    ]
    for biz_name, fc, vc, sp, target_profit in be_scenarios:
        cm = sp - vc
        be_units = int(-(-fc // cm)) # ceiling division
        target_units = int(-(-(fc + target_profit) // cm))
        target_revenue = round(target_units * sp, 2)
        
        # Q1: Break-even units
        q_be1 = (f"A small entrepreneur runs a {biz_name}. "
                 f"Monthly fixed operating costs (rent, machine lease, insurance) are R{fc:,.2f}. "
                 f"The variable production cost per unit is R{vc:,.2f}, and each unit is sold for R{sp:,.2f}. "
                 f"Calculate the minimum number of units that must be sold each month to break even.")
        c_be1 = f"{be_units} units"
        d_be1 = [
            f"{int(fc // sp)} units",
            f"{int(fc // vc)} units",
            f"{be_units + 25} units",
            f"{be_units - 25} units",
            f"{int(be_units * 1.15)} units",
            f"{int(be_units * 0.85)} units",
            f"{be_units + 50} units"
        ]
        exp_be1 = (f"Contribution Margin per unit = Selling Price - Variable Cost = R{sp:,.2f} - R{vc:,.2f} = R{cm:,.2f}. "
                   f"Break-even quantity = Fixed Costs ÷ Contribution Margin = R{fc:,.2f} ÷ R{cm:,.2f} = {fc / cm:.2f} ≈ {be_units} units.")
        add_q("Break-Even Analysis", "hard", q_be1, c_be1, d_be1, exp_be1)
        
        # Q2: Target profit units
        q_be2 = (f"Using the same cost structure for the {biz_name} (Fixed costs: R{fc:,.2f}, Variable cost: R{vc:,.2f}, Selling price: R{sp:,.2f}): "
                 f"Determine the number of units the entrepreneur must sell in a month to achieve a targeted net monthly profit of R{target_profit:,.2f}.")
        c_be2 = f"{target_units} units"
        d_be2 = [
            f"{be_units} units",
            f"{int(target_profit // cm)} units",
            f"{int((fc + target_profit) // sp)} units",
            f"{target_units + 30} units",
            f"{target_units - 30} units",
            f"{int(target_units * 1.10)} units",
            f"{int(target_units * 0.90)} units"
        ]
        exp_be2 = (f"Required Units = (Fixed Costs + Target Profit) ÷ Contribution Margin "
                   f"= (R{fc:,.2f} + R{target_profit:,.2f}) ÷ R{cm:,.2f} = R{fc + target_profit:,.2f} ÷ R{cm:,.2f} = {(fc + target_profit) / cm:.2f} ≈ {target_units} units.")
        add_q("Break-Even Analysis", "hard", q_be2, c_be2, d_be2, exp_be2)

    # Fill remaining hard
    while counts["hard"] < target_hard:
        fc = random.randint(7000, 25000)
        vc = random.randint(30, 150)
        sp = vc + random.randint(40, 120)
        cm = sp - vc
        be_units = int(-(-fc // cm))
        q_fill_h = f"An enterprise incurs fixed monthly overheads of R{fc:,.2f}. Direct variable costs per item are R{vc:,.2f} and each item sells for R{sp:,.2f}. Calculate the break-even sales volume."
        c_fill_h = f"{be_units} units"
        d_fill_h = [
            f"{int(fc // sp)} units",
            f"{int(fc // vc)} units",
            f"{be_units + 15} units",
            f"{be_units - 15} units",
            f"{int(be_units * 1.12)} units",
            f"{int(be_units * 0.88)} units",
            f"{be_units + 30} units"
        ]
        exp_fill_h = f"Contribution margin = R{sp:,.2f} - R{vc:,.2f} = R{cm:,.2f}. Break-even volume = R{fc:,.2f} ÷ R{cm:,.2f} = {fc/cm:.2f} ≈ {be_units} units."
        add_q("Break-Even Analysis", "hard", q_fill_h, c_fill_h, d_fill_h, exp_fill_h)

    print(f"Generated Finance: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/mathematical_literacy"
    out_file = os.path.join(out_dir, "paper1_mathlit12_finance.json")
    dataset = build_finance_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
