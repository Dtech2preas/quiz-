import json
import os

def build_analysis():
    questions = []
    seen_questions = set()
    counts = {"easy": 0, "medium": 0, "hard": 0}

    def add_q(difficulty, subtopic, q_text, correct, wrongs, cognitive, outcome, explanation):
        target = 300 if difficulty == "easy" else 500 if difficulty == "medium" else 200
        if counts[difficulty] >= target:
            return False

        q_clean = q_text.strip()
        if q_clean in seen_questions:
            return False

        c_str = str(correct).strip()
        clean_wrongs = []
        seen_w = set()
        for w in wrongs:
            w_str = str(w).strip()
            if w_str != c_str and w_str not in seen_w:
                seen_w.add(w_str)
                clean_wrongs.append(w_str)

        if len(clean_wrongs) < 6:
            return False

        seen_questions.add(q_clean)
        counts[difficulty] += 1
        qid = f"ACC_P1_ANA_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Financial Indicators & Interpretation",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Financial Indicators",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Ratio Definitions, Purpose, Norms & Direct Level 1 Calculations
    # =========================================================================

    ratio_definitions = [
        ("Current Ratio", "Current Assets : Current Liabilities", "2 : 1 (or 1.5 : 1 depending on trade)",
         "Measures the short-term liquidity of a business; specifically its ability to settle immediate short-term debts maturing within 12 months using its short-term current assets.",
         ["Non-Current Assets : Non-Current Liabilities", "Cost of Sales : Average Stock", "Net Profit : Sales × 100", "Total Assets : Total Liabilities", "Ordinary Shares : Retained Income", "Current Liabilities : Cash"]),

        ("Acid-Test Ratio (Quick Ratio)", "(Current Assets - Inventory) : Current Liabilities", "1 : 1",
         "A rigorous measure of immediate liquidity; tests whether a company can pay off its current liabilities immediately without having to wait to sell trading inventory.",
         ["Current Assets : Current Liabilities", "Total Assets - Fixed Assets : Total Liabilities", "Debtors : Creditors", "Sales - Cost of Sales : Current Assets", "Cash : Bank Overdraft", "Gross Profit : Current Liabilities"]),

        ("Solvency Ratio", "Total Assets : Total Liabilities", "2 : 1 (minimum > 1 : 1)",
         "Measures the long-term solvency of the enterprise; evaluates whether total assets exceed total liabilities so that in the event of liquidation, all outside creditors can be paid in full.",
         ["Current Assets : Current Liabilities", "Operating Profit : Total Capital Employed", "Net Profit after Tax : Shareholders' Equity", "Shareholders' Equity : Non-Current Liabilities", "Sales : Total Assets", "Cash : Long-term Loans"]),

        ("Debt-Equity Ratio (Gearing)", "Non-Current Liabilities : Shareholders' Equity", "Below 0.5 : 1 (Low Gearing)",
         "Measures the financial risk and capital structure (gearing) of the company; evaluates the proportion of borrowed long-term capital compared to contributed owners' equity.",
         ["Total Liabilities : Total Assets", "Current Liabilities : Shareholders' Equity", "Mortgage Loan : Bank Overdraft", "Shareholders' Equity : Retained Income", "Net Profit : Long-term Loan", "Non-Current Assets : Total Equity"]),

        ("Return on Shareholders' Equity (ROSHE)", "(Net Profit after Tax / Average Shareholders' Equity) × 100", "Must exceed alternative returns (e.g. 8-10% fixed deposit rate)",
         "Evaluates the overall profitability of the enterprise from the perspective of the shareholders; measures how effectively directors deployed the owners' capital to generate net earnings.",
         ["(Gross Profit / Sales) × 100", "(Operating Profit / Total Assets) × 100", "(Operating Expenses / Cost of Sales) × 100", "(Dividends Paid / Share Capital) × 100", "(Retained Income / Total Equity) × 100", "(Net Profit before Tax / Sales) × 100"]),

        ("Return on Total Capital Employed (ROTCE)", "(Net Profit before Interest Expense and Tax / Average Capital Employed) × 100", "Must exceed the interest rate on borrowed loans (Positive Gearing)",
         "Evaluates the overall operational efficiency of the business in generating operating returns from all long-term capital invested (both equity and borrowed loans), irrespective of financing structure.",
         ["(Net Profit after Tax / Total Assets) × 100", "(Gross Profit / Average Stock) × 100", "(Operating Expenses / Total Capital) × 100", "(Loan Interest / Total Loan) × 100", "(Retained Income / Capital Employed) × 100", "(Cash Flow / Total Liabilities) × 100"]),

        ("Earnings per Share (EPS)", "(Net Profit after Tax / Number of Issued Ordinary Shares) × 100", "Growth above inflation year-on-year",
         "Calculates the portion of total net company earnings generated per issued ordinary share; used by investors to assess profitability and compare share performance across companies.",
         ["(Dividends Paid / Number of Shares) × 100", "(Sales Revenue / Number of Shares) × 100", "(Gross Profit / Authorised Shares) × 100", "(Shareholders' Equity / Issued Shares) × 100", "(Cash Generated / Number of Shares) × 100", "(Operating Profit / Retained Shares) × 100"]),

        ("Dividends per Share (DPS)", "(Total Dividends declared for the year / Number of Issued Ordinary Shares) × 100", "Consistent annual payout growth",
         "Measures the actual dividend distribution paid or declared per issued ordinary share (interim dividend plus final recommended dividend) received by shareholders.",
         ["(Net Profit / Number of Shares) × 100", "(Retained Income / Issued Shares) × 100", "(Interest Paid / Number of Shares) × 100", "(Taxation Paid / Number of Shares) × 100", "(Capital Employed / Number of Shares) × 100", "(Share Capital / Issued Shares) × 100"]),

        ("Net Asset Value per Share (NAV)", "(Shareholders' Equity / Number of Issued Ordinary Shares) × 100", "Should be compared with the JSE market price of the share",
         "Calculates the book value of net assets belonging to each ordinary share if the company were wound up and all liabilities settled at carrying values.",
         ["(Total Assets / Issued Shares) × 100", "(Net Profit / Issued Shares) × 100", "(Dividends / Issued Shares) × 100", "(Current Assets / Issued Shares) × 100", "(Total Liabilities / Issued Shares) × 100", "(Cash & Cash Equivalents / Issued Shares) × 100"]),

        ("Dividend Payout Rate", "(Dividends per Share / Earnings per Share) × 100", "Typically 40% - 70% (balance retained for growth)",
         "Measures the percentage of annual company net earnings that is distributed to ordinary shareholders as cash dividends versus the percentage retained for reinvestment in the business.",
         ["(EPS / DPS) × 100", "(Dividends / Sales) × 100", "(Dividends / Total Assets) × 100", "(Net Profit / Dividends) × 100", "(DPS / Net Asset Value) × 100", "(Share Capital / Retained Income) × 100"]),

        ("Debtors Collection Period", "(Average Debtors / Total Credit Sales) × 365 days", "30 days (standard credit term)",
         "Measures the average number of days it takes for credit customers (debtors) to settle their outstanding trade accounts; identifies credit control efficiency.",
         ["(Credit Sales / Average Debtors) × 365", "(Average Debtors / Total Sales) × 100", "(Cost of Sales / Debtors) × 365", "(Average Creditors / Credit Purchases) × 365", "(Cash Sales / Debtors) × 365", "(Bad Debts / Total Debtors) × 100"]),

        ("Creditors Payment Period", "(Average Creditors / Total Credit Purchases or Cost of Sales) × 365 days", "60 to 90 days (take full advantage of supplier credit without default)",
         "Calculates the average number of days the business takes to pay its trade suppliers; compared with debtor collection period to ensure working capital equilibrium.",
         ["(Credit Purchases / Average Creditors) × 365", "(Average Debtors / Credit Sales) × 365", "(Total Purchases / Current Liabilities) × 365", "(Cost of Sales / Total Creditors) × 100", "(Creditors / Bank) × 365", "(Trade Payables / Gross Profit) × 100"]),

        ("Stock Turnover Rate", "Cost of Sales / Average Trading Stock", "Higher is better (e.g. 6 to 12 times per year)",
         "Measures how many times per financial year the average trading inventory of the business is completely sold out and replaced.",
         ["Sales / Average Stock", "Average Stock / Cost of Sales", "Gross Profit / Closing Stock", "Cost of Sales / Total Assets", "Net Profit / Average Inventory", "Opening Stock / Closing Stock"]),

        ("Stock Holding Period", "(Average Trading Stock / Cost of Sales) × 365 days (or × 12 months)", "Lower is better (e.g. 30 to 60 days)",
         "Calculates the average duration in days or months that merchandise remains stored on warehouse shelves before being sold to customers.",
         ["(Cost of Sales / Average Stock) × 365", "(Average Stock / Sales) × 100", "(Sales / Cost of Sales) × 365", "(Closing Stock / Average Stock) × 12", "(Trading Stock / Current Assets) × 100", "(Gross Profit / Average Stock) × 365"])
    ]

    for rat_name, rat_form, rat_norm, rat_purpose, rat_wrongs in ratio_definitions:
        for st_r in [
            f"What is the official formula, benchmark norm, and purpose of the **'{rat_name}'**?",
            f"In Grade 12 Accounting financial analysis, how is the **'{rat_name}'** calculated and interpreted?",
            f"Which statement accurately defines the **'{rat_name}'** according to the CAPS curriculum?"
        ]:
            if counts["easy"] >= 300:
                break
            c_r = f"Formula: {rat_form}; Benchmark: {rat_norm}. Purpose: {rat_purpose}"
            w_r = [f"Formula: {w_f}; Benchmark: None. (Incorrect formula)" for w_f in rat_wrongs]
            add_q("easy", "Financial Indicator Definitions", st_r, c_r, w_r, "Remembering", f"Define {rat_name}", c_r)

    # Direct Level 1 Ratio Calculations (Easy)
    direct_ratio_cases = [
        ("Laysano Ltd", 1450000.0, 725000.0, 480000.0, 7850000.0, 2450000.0, 1800000.0, 4800000.0),
        ("Protea Hardware Ltd", 2100000.0, 1050000.0, 750000.0, 11500000.0, 3500000.0, 2500000.0, 6800000.0),
        ("Zulu Fashion Ltd", 880000.0, 440000.0, 310000.0, 4800000.0, 1500000.0, 1000000.0, 3200000.0),
        ("Metro Tech Ltd", 3600000.0, 1800000.0, 1250000.0, 18200000.0, 5200000.0, 3800000.0, 10500000.0),
        ("Apex Auto Ltd", 1750000.0, 875000.0, 580000.0, 8900000.0, 2800000.0, 2100000.0, 5400000.0),
        ("Kairo Furnishers Ltd", 2600000.0, 1300000.0, 890000.0, 12800000.0, 4100000.0, 2800000.0, 7600000.0),
        ("Orchid Boutique Ltd", 720000.0, 360000.0, 260000.0, 3800000.0, 1200000.0, 850000.0, 2500000.0),
        ("Galaxy Appliances Ltd", 4200000.0, 2100000.0, 1450000.0, 22500000.0, 6800000.0, 4900000.0, 13500000.0),
        ("Bakersfield Ltd", 1900000.0, 950000.0, 680000.0, 9600000.0, 3100000.0, 2200000.0, 5800000.0),
        ("Tshwane Traders Ltd", 1600000.0, 800000.0, 550000.0, 8200000.0, 2600000.0, 1900000.0, 5100000.0),
        ("Cape Coast Ltd", 1850000.0, 925000.0, 640000.0, 9400000.0, 3000000.0, 2200000.0, 5600000.0),
        ("Durban Wholesale Ltd", 3800000.0, 1900000.0, 1350000.0, 19500000.0, 5800000.0, 4200000.0, 11800000.0),
        ("Sandton Goods Ltd", 4800000.0, 2400000.0, 1650000.0, 24000000.0, 7500000.0, 5400000.0, 14500000.0),
        ("Bloemfontein Traders Ltd", 1950000.0, 975000.0, 690000.0, 9900000.0, 3200000.0, 2300000.0, 6000000.0),
        ("Polokwane Supply Ltd", 1400000.0, 700000.0, 490000.0, 7200000.0, 2300000.0, 1600000.0, 4400000.0),
        ("Nelspruit Supply Ltd", 1250000.0, 625000.0, 440000.0, 6400000.0, 2100000.0, 1500000.0, 3900000.0),
        ("Kimberley Tools Ltd", 2300000.0, 1150000.0, 810000.0, 11800000.0, 3700000.0, 2700000.0, 7100000.0),
        ("Rustenburg Industrial Ltd", 3200000.0, 1600000.0, 1100000.0, 16500000.0, 5100000.0, 3600000.0, 10200000.0),
        ("Port Elizabeth Logistics Ltd", 3700000.0, 1850000.0, 1300000.0, 18800000.0, 5900000.0, 4100000.0, 11500000.0),
        ("Pietermaritzburg Ltd", 1550000.0, 775000.0, 540000.0, 7900000.0, 2500000.0, 1800000.0, 4800000.0),
        ("Soweto Commercial Ltd", 1850000.0, 925000.0, 650000.0, 9400000.0, 3100000.0, 2100000.0, 5800000.0),
        ("Midrand Tech Ltd", 4400000.0, 2200000.0, 1550000.0, 21800000.0, 6900000.0, 4800000.0, 13200000.0),
        ("Centurion Sports Ltd", 1300000.0, 650000.0, 460000.0, 6800000.0, 2200000.0, 1500000.0, 4100000.0),
        ("East London Timber Ltd", 2150000.0, 1075000.0, 760000.0, 10900000.0, 3500000.0, 2400000.0, 6600000.0),
        ("Stellenbosch Cellars Ltd", 2700000.0, 1350000.0, 950000.0, 13700000.0, 4300000.0, 3000000.0, 8300000.0),
        ("Upington Sun Ltd", 1150000.0, 575000.0, 400000.0, 5900000.0, 1900000.0, 1300000.0, 3600000.0),
        ("Witbank Coal Ltd", 3900000.0, 1950000.0, 1380000.0, 19800000.0, 6300000.0, 4400000.0, 12000000.0),
        ("Paarl Agro Ltd", 1950000.0, 975000.0, 690000.0, 9900000.0, 3200000.0, 2200000.0, 6000000.0),
        ("Potchefstroom Grain Ltd", 1600000.0, 800000.0, 560000.0, 8200000.0, 2600000.0, 1800000.0, 5000000.0),
        ("George Coastal Ltd", 2100000.0, 1050000.0, 740000.0, 10600000.0, 3400000.0, 2300000.0, 6400000.0),
        ("Vereeniging Steel Ltd", 3400000.0, 1700000.0, 1200000.0, 17200000.0, 5500000.0, 3800000.0, 10400000.0),
        ("Welkom Goldfield Ltd", 2800000.0, 1400000.0, 980000.0, 14200000.0, 4500000.0, 3100000.0, 8600000.0),
        ("Klerksdorp Merchants Ltd", 1750000.0, 875000.0, 620000.0, 8900000.0, 2900000.0, 2000000.0, 5400000.0),
        ("Mthatha Wholesale Ltd", 1450000.0, 725000.0, 510000.0, 7400000.0, 2400000.0, 1600000.0, 4500000.0),
        ("Richards Bay Harbour Ltd", 3600000.0, 1800000.0, 1260000.0, 18300000.0, 5800000.0, 4000000.0, 11100000.0),
        ("Ladysmith Textiles Ltd", 1650000.0, 825000.0, 580000.0, 8400000.0, 2700000.0, 1900000.0, 5100000.0),
        ("Mossel Bay Oil Supply Ltd", 4100000.0, 2050000.0, 1440000.0, 20900000.0, 6600000.0, 4600000.0, 12700000.0),
        ("Grahamstown Press Ltd", 1200000.0, 600000.0, 420000.0, 6100000.0, 2000000.0, 1400000.0, 3700000.0),
        ("Krugersdorp Mining Ltd", 3800000.0, 1900000.0, 1330000.0, 19300000.0, 6100000.0, 4200000.0, 11700000.0),
        ("Secunda Petrochem Ltd", 4900000.0, 2450000.0, 1720000.0, 24900000.0, 7900000.0, 5500000.0, 15100000.0),
        ("Bethlehem Grain Silos Ltd", 1550000.0, 775000.0, 540000.0, 7900000.0, 2500000.0, 1700000.0, 4800000.0),
        ("Newcastle Foundry Ltd", 3300000.0, 1650000.0, 1160000.0, 16800000.0, 5300000.0, 3700000.0, 10200000.0),
        ("Vryheid Timber Traders Ltd", 1850000.0, 925000.0, 650000.0, 9400000.0, 3000000.0, 2100000.0, 5700000.0),
        ("Polokwane Freight Ltd", 2250000.0, 1125000.0, 780000.0, 11400000.0, 3600000.0, 2500000.0, 6900000.0),
        ("Tshwane Media Works Ltd", 1700000.0, 850000.0, 590000.0, 8600000.0, 2700000.0, 1900000.0, 5200000.0),
        ("Rustenburg Chrome Ltd", 4200000.0, 2100000.0, 1470000.0, 21300000.0, 6700000.0, 4700000.0, 12900000.0),
        ("Cape Town Logistics Ltd", 3100000.0, 1550000.0, 1080000.0, 15700000.0, 4900000.0, 3400000.0, 9500000.0),
        ("Durban Fresh Produce Ltd", 1400000.0, 700000.0, 490000.0, 7100000.0, 2200000.0, 1500000.0, 4300000.0),
        ("Bloemfontein Milling Ltd", 2600000.0, 1300000.0, 910000.0, 13200000.0, 4100000.0, 2900000.0, 8000000.0),
        ("Kimberley Diamond Tools Ltd", 3500000.0, 1750000.0, 1220000.0, 17800000.0, 5600000.0, 3900000.0, 10800000.0),
        ("Mbombela Citrus Packhouse Ltd", 1900000.0, 950000.0, 660000.0, 9600000.0, 3000000.0, 2100000.0, 5800000.0),
        ("Johannesburg Printers Ltd", 2400000.0, 1200000.0, 840000.0, 12200000.0, 3800000.0, 2700000.0, 7400000.0),
        ("Port Elizabeth Automotives Ltd", 4500000.0, 2250000.0, 1575000.0, 22800000.0, 7200000.0, 5000000.0, 13800000.0),
        ("Saldanha Bulk Terminal Ltd", 3700000.0, 1850000.0, 1295000.0, 18700000.0, 5900000.0, 4100000.0, 11300000.0),
        ("Harrismith Logistics Ltd", 1500000.0, 750000.0, 525000.0, 7600000.0, 2400000.0, 1700000.0, 4600000.0),
        ("Kuruman Ironworks Ltd", 2900000.0, 1450000.0, 1015000.0, 14700000.0, 4600000.0, 3200000.0, 8900000.0),
        ("Plettenberg Hospitality Ltd", 2000000.0, 1000000.0, 700000.0, 10100000.0, 3200000.0, 2200000.0, 6100000.0),
        ("Richards Bay Alloys Ltd", 4800000.0, 2400000.0, 1680000.0, 24300000.0, 7700000.0, 5300000.0, 14700000.0),
        ("Springbok Solar Park Ltd", 3200000.0, 1600000.0, 1120000.0, 16200000.0, 5100000.0, 3500000.0, 9800000.0),
        ("Cradock Wool Exchange Ltd", 1350000.0, 675000.0, 472500.0, 6800000.0, 2100000.0, 1500000.0, 4100000.0),
        ("Oudtshoorn Leather Ltd", 1750000.0, 875000.0, 612500.0, 8800000.0, 2800000.0, 1900000.0, 5300000.0),
        ("Knysna Timber Holdings Ltd", 2300000.0, 1150000.0, 805000.0, 11600000.0, 3700000.0, 2600000.0, 7000000.0),
        ("Thohoyandou Stores Ltd", 1600000.0, 800000.0, 560000.0, 8100000.0, 2500000.0, 1800000.0, 4900000.0),
        ("Makhanda Publishing Ltd", 1250000.0, 625000.0, 437500.0, 6300000.0, 2000000.0, 1400000.0, 3800000.0),
        ("Bredasdorp Grain Agri Ltd", 2150000.0, 1075000.0, 752500.0, 10800000.0, 3400000.0, 2400000.0, 6500000.0),
        ("Standerton Dairy Ltd", 1800000.0, 900000.0, 630000.0, 9100000.0, 2900000.0, 2000000.0, 5500000.0),
        ("Vanderbijl Eng Works Ltd", 3650000.0, 1825000.0, 1277500.0, 18500000.0, 5800000.0, 4100000.0, 11200000.0)
    ]

    for co_dr, ca_v, cl_v, inv_v, ta_v, tl_v, ncl_v, eq_v in direct_ratio_cases:
        # 1. Current Ratio
        if counts["easy"] < 300:
            cr_val = ca_v / cl_v
            c_cr = f"{cr_val:.2f} : 1"
            w_cr = [
                f"{cl_v / ca_v:.2f} : 1 (inverted: CL : CA)",
                f"{(ca_v - inv_v) / cl_v:.2f} : 1 (calculated acid-test ratio instead of current ratio)",
                f"{cr_val * 1.5:.2f} : 1",
                f"{cr_val / 2:.2f} : 1",
                f"{ca_v / (cl_v * 1.5):.2f} : 1",
                f"{cr_val + 1.0:.2f} : 1",
                f"{cr_val - 0.5:.2f} : 1"
            ]
            q_cr = f"**{co_dr}** reports Current Assets of **R{ca_v:,.0f}** and Current Liabilities of **R{cl_v:,.0f}**. Calculate the **Current Ratio**:"
            exp_cr = f"Current Ratio = Current Assets : Current Liabilities = R{ca_v:,.0f} / R{cl_v:,.0f} = {c_cr}."
            add_q("easy", "Direct Ratio Calculations", q_cr, c_cr, w_cr, "Applying", f"Calculate Current Ratio for {co_dr}", exp_cr)

        # 2. Acid-Test Ratio
        if counts["easy"] < 300:
            at_val = (ca_v - inv_v) / cl_v
            c_at = f"{at_val:.2f} : 1"
            w_at = [
                f"{ca_v / cl_v:.2f} : 1 (forgot to deduct inventory: current ratio)",
                f"{cl_v / (ca_v - inv_v):.2f} : 1 (inverted ratio)",
                f"{at_val * 1.5:.2f} : 1",
                f"{at_val / 2:.2f} : 1",
                f"{(ca_v + inv_v) / cl_v:.2f} : 1 (added inventory instead of deducting)",
                f"{at_val + 0.8:.2f} : 1",
                f"{at_val - 0.4:.2f} : 1"
            ]
            q_at = (f"The records of **{co_dr}** show Current Assets of **R{ca_v:,.0f}**, Trading Inventory of **R{inv_v:,.0f}**, "
                    f"and Current Liabilities of **R{cl_v:,.0f}**. Calculate the **Acid-Test Ratio**:")
            exp_at = f"Acid-Test Ratio = (Current Assets - Inventory) : Current Liabilities = (R{ca_v:,.0f} - R{inv_v:,.0f}) / R{cl_v:,.0f} = {c_at}."
            add_q("easy", "Direct Ratio Calculations", q_at, c_at, w_at, "Applying", f"Calculate Acid-Test Ratio for {co_dr}", exp_at)

        # 3. Solvency Ratio
        if counts["easy"] < 300:
            solv_val = ta_v / tl_v
            c_solv = f"{solv_val:.2f} : 1"
            w_solv = [
                f"{tl_v / ta_v:.2f} : 1 (inverted: Total Liabilities : Total Assets)",
                f"{solv_val * 1.5:.2f} : 1",
                f"{solv_val / 2:.2f} : 1",
                f"{eq_v / tl_v:.2f} : 1 (confused equity with total assets)",
                f"{solv_val + 1.2:.2f} : 1",
                f"{solv_val - 0.7:.2f} : 1",
                f"{ca_v / cl_v:.2f} : 1 (calculated current ratio instead of solvency)"
            ]
            q_solv = f"**{co_dr}** has Total Assets of **R{ta_v:,.0f}** and Total Liabilities of **R{tl_v:,.0f}**. Determine the **Solvency Ratio**:"
            exp_solv = f"Solvency Ratio = Total Assets : Total Liabilities = R{ta_v:,.0f} / R{tl_v:,.0f} = {c_solv}."
            add_q("easy", "Direct Ratio Calculations", q_solv, c_solv, w_solv, "Applying", f"Calculate Solvency Ratio for {co_dr}", exp_solv)

        # 4. Debt-Equity Ratio (Gearing)
        if counts["easy"] < 300:
            gearing_val = ncl_v / eq_v
            c_gear = f"{gearing_val:.2f} : 1"
            w_gear = [
                f"{eq_v / ncl_v:.2f} : 1 (inverted: Equity : Debt)",
                f"{tl_v / eq_v:.2f} : 1 (used Total Liabilities instead of Non-Current Liabilities)",
                f"{gearing_val * 2:.2f} : 1",
                f"{gearing_val / 2:.2f} : 1",
                f"{gearing_val + 0.5:.2f} : 1",
                f"{ncl_v / ta_v:.2f} : 1 (divided debt by total assets)",
                f"{gearing_val * 0.8:.2f} : 1"
            ]
            q_gear = (f"The capital structure of **{co_dr}** reflects Non-Current Liabilities (Loan) of **R{ncl_v:,.0f}** and "
                      f"Shareholders' Equity of **R{eq_v:,.0f}**. Calculate the **Debt-Equity Ratio (Gearing)**:")
            exp_gear = f"Debt-Equity Ratio = Non-Current Liabilities : Shareholders' Equity = R{ncl_v:,.0f} / R{eq_v:,.0f} = {c_gear}."
            add_q("easy", "Direct Ratio Calculations", q_gear, c_gear, w_gear, "Applying", f"Calculate Debt-Equity for {co_dr}", exp_gear)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Debtors Collection Period, Creditors Payment Period, Stock Turnover & Holding,
    # ROSHE, ROTCE, EPS, DPS, Dividend Payout, Gearing Evaluation
    # =========================================================================

    debtor_creditor_cases = [
        ("Laysano Ltd", 240000.0, 280000.0, 3120000.0, 180000.0, 220000.0, 1600000.0),
        ("Protea Hardware Ltd", 410000.0, 470000.0, 5350000.0, 310000.0, 370000.0, 2800000.0),
        ("Zulu Fashion Ltd", 150000.0, 190000.0, 2040000.0, 110000.0, 130000.0, 1050000.0),
        ("Metro Tech Ltd", 650000.0, 750000.0, 8500000.0, 480000.0, 560000.0, 4400000.0),
        ("Apex Auto Ltd", 320000.0, 360000.0, 4100000.0, 240000.0, 280000.0, 2150000.0),
        ("Kairo Furnishers Ltd", 480000.0, 540000.0, 6200000.0, 350000.0, 410000.0, 3200000.0),
        ("Orchid Boutique Ltd", 130000.0, 150000.0, 1700000.0, 95000.0, 115000.0, 890000.0),
        ("Galaxy Appliances Ltd", 820000.0, 940000.0, 10700000.0, 620000.0, 720000.0, 5600000.0),
        ("Bakersfield Ltd", 340000.0, 380000.0, 4380000.0, 260000.0, 300000.0, 2300000.0),
        ("Tshwane Traders Ltd", 280000.0, 320000.0, 3650000.0, 210000.0, 250000.0, 1900000.0),
        ("Cape Coast Ltd", 360000.0, 420000.0, 4750000.0, 270000.0, 330000.0, 2500000.0),
        ("Durban Wholesale Ltd", 740000.0, 860000.0, 9750000.0, 550000.0, 650000.0, 5100000.0)
    ]

    for co_dc, open_d, close_d, cr_sales, open_c, close_c, cr_purch in debtor_creditor_cases:
        avg_debtors = (open_d + close_d) / 2.0
        dcp_days = (avg_debtors / cr_sales) * 365.0

        avg_creditors = (open_c + close_c) / 2.0
        cpp_days = (avg_creditors / cr_purch) * 365.0

        # 1. Debtors Collection Period
        if counts["medium"] < 500:
            c_dcp = f"{dcp_days:.1f} days"
            w_dcp = [
                f"{(close_d / cr_sales) * 365:.1f} days (used closing debtors only instead of average debtors)",
                f"{(open_d / cr_sales) * 365:.1f} days (used opening debtors only)",
                f"{dcp_days * 1.5:.1f} days",
                f"{dcp_days / 2:.1f} days",
                f"{(cr_sales / avg_debtors):.1f} times (confused days with turnover times)",
                f"{dcp_days + 15.0:.1f} days",
                f"{dcp_days - 10.0:.1f} days"
            ]
            q_dcp = (f"The records of **{co_dc}** reflect: Trade Debtors on 1 March: **R{open_d:,.0f}**; "
                     f"Trade Debtors on 28 February: **R{close_d:,.0f}**; Total Credit Sales for the year: **R{cr_sales:,.0f}**. "
                     f"Calculate the **Debtors Collection Period in days** (using average debtors):")
            exp_dcp = (f"1. Average Debtors = (R{open_d:,.0f} + R{close_d:,.0f}) / 2 = R{avg_debtors:,.0f}. "
                       f"2. Debtors Collection Period = (Average Debtors / Credit Sales) × 365 = (R{avg_debtors:,.0f} / R{cr_sales:,.0f}) × 365 = {c_dcp}.")
            add_q("medium", "Debtors & Creditors Periods", q_dcp, c_dcp, w_dcp, "Applying", f"Calculate Debtors Collection Period for {co_dc}", exp_dcp)

        # 2. Creditors Payment Period
        if counts["medium"] < 500:
            c_cpp = f"{cpp_days:.1f} days"
            w_cpp = [
                f"{(close_c / cr_purch) * 365:.1f} days (used closing creditors only)",
                f"{cpp_days * 1.5:.1f} days",
                f"{cpp_days / 2:.1f} days",
                f"{(cr_purch / avg_creditors):.1f} times (confused days with times)",
                f"{cpp_days + 20.0:.1f} days",
                f"{cpp_days - 15.0:.1f} days",
                f"{(avg_debtors / cr_sales) * 365:.1f} days (calculated debtors period instead)"
            ]
            q_cpp = (f"In the books of **{co_dc}**, Trade Creditors opened at **R{open_c:,.0f}** and closed at **R{close_c:,.0f}**. "
                     f"Total Credit Purchases for the year amounted to **R{cr_purch:,.0f}**. Calculate the **Creditors Payment Period in days**:")
            exp_cpp = (f"1. Average Creditors = (R{open_c:,.0f} + R{close_c:,.0f}) / 2 = R{avg_creditors:,.0f}. "
                       f"2. Creditors Payment Period = (Average Creditors / Credit Purchases) × 365 = (R{avg_creditors:,.0f} / R{cr_purch:,.0f}) × 365 = {c_cpp}.")
            add_q("medium", "Debtors & Creditors Periods", q_cpp, c_cpp, w_cpp, "Applying", f"Calculate Creditors Payment Period for {co_dc}", exp_cpp)

    # Stock Turnover Rate & Holding Period (Medium)
    stock_turnover_cases = [
        ("Laysano Ltd", 480000.0, 520000.0, 3500000.0),
        ("Protea Hardware Ltd", 720000.0, 800000.0, 5320000.0),
        ("Zulu Fashion Ltd", 280000.0, 320000.0, 2100000.0),
        ("Metro Tech Ltd", 1100000.0, 1300000.0, 8400000.0),
        ("Apex Auto Ltd", 540000.0, 620000.0, 4060000.0),
        ("Kairo Furnishers Ltd", 780000.0, 860000.0, 5740000.0),
        ("Orchid Boutique Ltd", 220000.0, 260000.0, 1680000.0),
        ("Galaxy Appliances Ltd", 1350000.0, 1550000.0, 10150000.0),
        ("Bakersfield Ltd", 560000.0, 640000.0, 4200000.0),
        ("Tshwane Traders Ltd", 460000.0, 540000.0, 3500000.0),
        ("Cape Coast Ltd", 590000.0, 670000.0, 4410000.0),
        ("Durban Wholesale Ltd", 1250000.0, 1450000.0, 9450000.0)
    ]

    for co_st, open_stk, close_stk, cos_stk in stock_turnover_cases:
        avg_stk = (open_stk + close_stk) / 2.0
        stk_rate = cos_stk / avg_stk
        stk_days = (avg_stk / cos_stk) * 365.0

        # Stock Turnover Rate
        if counts["medium"] < 500:
            c_str = f"{stk_rate:.1f} times"
            w_str = [
                f"{cos_stk / close_stk:.1f} times (used closing stock only)",
                f"{cos_stk / open_stk:.1f} times (used opening stock only)",
                f"{avg_stk / cos_stk:.4f} times (inverted formula)",
                f"{stk_rate * 1.5:.1f} times",
                f"{stk_rate / 2:.1f} times",
                f"{stk_days:.1f} days (confused rate with days holding)",
                f"{stk_rate + 2.5:.1f} times"
            ]
            q_str = (f"The trading records of **{co_st}** reflect: Opening Trading Stock: **R{open_stk:,.0f}**; "
                     f"Closing Trading Stock: **R{close_stk:,.0f}**; Cost of Sales for the year: **R{cos_stk:,.0f}**. "
                     f"Calculate the **Stock Turnover Rate** (times per year):")
            exp_str = (f"1. Average Stock = (R{open_stk:,.0f} + R{close_stk:,.0f}) / 2 = R{avg_stk:,.0f}. "
                       f"2. Stock Turnover Rate = Cost of Sales / Average Stock = R{cos_stk:,.0f} / R{avg_stk:,.0f} = {c_str}.")
            add_q("medium", "Stock Turnover Calculations", q_str, c_str, w_str, "Applying", f"Calculate Stock Turnover Rate for {co_st}", exp_str)

        # Stock Holding Period
        if counts["medium"] < 500:
            c_shp = f"{stk_days:.1f} days ({stk_days/30.4167:.1f} months)"
            w_shp = [
                f"{(close_stk / cos_stk) * 365:.1f} days (used closing stock only)",
                f"{stk_days * 1.5:.1f} days",
                f"{stk_days / 2:.1f} days",
                f"{stk_rate:.1f} times (confused holding period with turnover rate)",
                f"{stk_days + 20.0:.1f} days",
                f"{stk_days - 15.0:.1f} days",
                f"{(open_stk / cos_stk) * 365:.1f} days"
            ]
            q_shp = (f"Using the inventory figures for **{co_st}** (Average Stock R{avg_stk:,.0f}, Cost of Sales R{cos_stk:,.0f}), "
                     f"determine the **Stock Holding Period in days**:")
            exp_shp = f"Stock Holding Period = (Average Stock / Cost of Sales) × 365 = (R{avg_stk:,.0f} / R{cos_stk:,.0f}) × 365 = {c_shp}."
            add_q("medium", "Stock Turnover Calculations", q_shp, c_shp, w_shp, "Applying", f"Calculate Stock Holding Period for {co_st}", exp_shp)

    # ROSHE and ROTCE Calculations (Medium)
    roshe_rotce_cases = [
        ("Laysano Ltd", 4800000.0, 5400000.0, 890000.0, 6600000.0, 7200000.0, 1350000.0),
        ("Protea Hardware Ltd", 6800000.0, 7600000.0, 1250000.0, 9200000.0, 10200000.0, 1950000.0),
        ("Zulu Fashion Ltd", 2900000.0, 3300000.0, 520000.0, 4100000.0, 4500000.0, 780000.0),
        ("Metro Tech Ltd", 10200000.0, 11800000.0, 2100000.0, 14500000.0, 16500000.0, 3200000.0),
        ("Apex Auto Ltd", 5100000.0, 5700000.0, 920000.0, 7200000.0, 7800000.0, 1420000.0),
        ("Kairo Furnishers Ltd", 7200000.0, 8000000.0, 1350000.0, 10200000.0, 11200000.0, 2050000.0),
        ("Galaxy Appliances Ltd", 13500000.0, 15500000.0, 2750000.0, 19500000.0, 21500000.0, 4100000.0),
        ("Bakersfield Ltd", 5400000.0, 6000000.0, 980000.0, 7500000.0, 8300000.0, 1500000.0)
    ]

    for co_rr, open_eq, close_eq, npat_val, open_ce, close_ce, op_prof_it in roshe_rotce_cases:
        avg_eq = (open_eq + close_eq) / 2.0
        roshe_pct = (npat_val / avg_eq) * 100.0

        avg_ce = (open_ce + close_ce) / 2.0
        rotce_pct = (op_prof_it / avg_ce) * 100.0

        # ROSHE
        if counts["medium"] < 500:
            c_roshe = f"{roshe_pct:.1f}%"
            w_roshe = [
                f"{(npat_val / close_eq) * 100:.1f}% (used closing equity only instead of average equity)",
                f"{(npat_val / open_eq) * 100:.1f}% (used opening equity only)",
                f"{roshe_pct * 1.5:.1f}%",
                f"{roshe_pct / 2:.1f}%",
                f"{(op_prof_it / avg_eq) * 100:.1f}% (used profit before interest instead of net profit after tax)",
                f"{roshe_pct + 4.0:.1f}%",
                f"{roshe_pct - 3.0:.1f}%"
            ]
            q_roshe = (f"**{co_rr}** generated a Net Profit after Tax of **R{npat_val:,.0f}**. Shareholders' Equity on 1 March was "
                       f"**R{open_eq:,.0f}** and on 28 February was **R{close_eq:,.0f}**. Calculate the **Return on Shareholders' Equity (% ROSHE)**:")
            exp_roshe = (f"1. Average Equity = (R{open_eq:,.0f} + R{close_eq:,.0f}) / 2 = R{avg_eq:,.0f}. "
                         f"2. ROSHE = (Net Profit after Tax / Average Equity) × 100 = (R{npat_val:,.0f} / R{avg_eq:,.0f}) × 100 = {c_roshe}.")
            add_q("medium", "Return Indicators (ROSHE & ROTCE)", q_roshe, c_roshe, w_roshe, "Applying", f"Calculate ROSHE for {co_rr}", exp_roshe)

        # ROTCE
        if counts["medium"] < 500:
            c_rotce = f"{rotce_pct:.1f}%"
            w_rotce = [
                f"{(op_prof_it / close_ce) * 100:.1f}% (used closing capital employed only)",
                f"{rotce_pct * 1.5:.1f}%",
                f"{rotce_pct / 2:.1f}%",
                f"{(npat_val / avg_ce) * 100:.1f}% (used net profit after tax instead of profit before interest & tax)",
                f"{rotce_pct + 5.0:.1f}%",
                f"{rotce_pct - 3.5:.1f}%",
                f"{roshe_pct:.1f}% (confused ROTCE with ROSHE)"
            ]
            q_rotce = (f"The records of **{co_rr}** show: Operating Profit before interest expense and tax: **R{op_prof_it:,.0f}**; "
                       f"Capital Employed on 1 March: **R{open_ce:,.0f}**; Capital Employed on 28 February: **R{close_ce:,.0f}**. "
                       f"Calculate the **Return on Total Capital Employed (% ROTCE)**:")
            exp_rotce = (f"1. Average Capital Employed = (R{open_ce:,.0f} + R{close_ce:,.0f}) / 2 = R{avg_ce:,.0f}. "
                         f"2. ROTCE = (Profit before Interest & Tax / Average Capital Employed) × 100 = (R{op_prof_it:,.0f} / R{avg_ce:,.0f}) × 100 = {c_rotce}.")
            add_q("medium", "Return Indicators (ROSHE & ROTCE)", q_rotce, c_rotce, w_rotce, "Applying", f"Calculate ROTCE for {co_rr}", exp_rotce)

    # EPS, DPS, and Dividend Payout Calculations (Medium)
    investor_metric_cases = [
        ("Laysano Ltd", 890000.0, 600000, 480000.0),
        ("Protea Hardware Ltd", 1250000.0, 800000, 680000.0),
        ("Zulu Fashion Ltd", 520000.0, 400000, 280000.0),
        ("Metro Tech Ltd", 2100000.0, 1200000, 1140000.0),
        ("Apex Auto Ltd", 920000.0, 500000, 500000.0),
        ("Kairo Furnishers Ltd", 1350000.0, 700000, 770000.0),
        ("Galaxy Appliances Ltd", 2750000.0, 1500000, 1500000.0),
        ("Bakersfield Ltd", 980000.0, 650000, 520000.0),
        ("Tshwane Traders Ltd", 810000.0, 550000, 440000.0),
        ("Cape Coast Ltd", 880000.0, 580000, 464000.0),
        ("Durban Wholesale Ltd", 1850000.0, 1100000, 990000.0),
        ("Sandton Goods Ltd", 2300000.0, 1300000, 1170000.0)
    ]

    for co_inv_m, npat_m, shares_m, tot_div_m in investor_metric_cases:
        eps_cents = (npat_m / shares_m) * 100.0
        dps_cents = (tot_div_m / shares_m) * 100.0
        payout_pct = (dps_cents / eps_cents) * 100.0

        # EPS
        if counts["medium"] < 500:
            c_eps = f"{eps_cents:.1f} cents per share"
            w_eps = [
                f"{eps_cents / 100:.2f} cents per share (forgot to convert Rands to cents)",
                f"{dps_cents:.1f} cents per share (confused DPS with EPS)",
                f"{eps_cents * 1.5:.1f} cents per share",
                f"{eps_cents / 2:.1f} cents per share",
                f"{eps_cents + 15.0:.1f} cents per share",
                f"{eps_cents - 12.0:.1f} cents per share",
                f"{(shares_m / npat_m) * 100:.2f} cents per share (inverted)"
            ]
            q_eps = (f"**{co_inv_m}** achieved a Net Profit after Tax of **R{npat_m:,.0f}** for the financial year. The company has "
                     f"**{shares_m:,} issued ordinary shares**. Calculate the **Earnings per Share (EPS) in cents**:")
            exp_eps = f"EPS = (Net Profit after Tax / Number of Issued Shares) × 100 = (R{npat_m:,.0f} / {shares_m:,}) × 100 = {c_eps}."
            add_q("medium", "Investor Financial Indicators", q_eps, c_eps, w_eps, "Applying", f"Calculate EPS for {co_inv_m}", exp_eps)

        # DPS
        if counts["medium"] < 500:
            c_dps = f"{dps_cents:.1f} cents per share"
            w_dps = [
                f"{eps_cents:.1f} cents per share (calculated EPS instead of DPS)",
                f"{dps_cents / 100:.2f} cents per share (forgot to convert to cents)",
                f"{dps_cents * 1.5:.1f} cents per share",
                f"{dps_cents / 2:.1f} cents per share",
                f"{dps_cents + 10.0:.1f} cents per share",
                f"{dps_cents - 8.0:.1f} cents per share",
                f"{(tot_div_m / npat_m) * 100:.1f} cents per share"
            ]
            q_dps = (f"The directors of **{co_inv_m}** declared total dividends (interim + final) of **R{tot_div_m:,.0f}** for the year on "
                     f"**{shares_m:,} issued shares**. Determine the **Dividends per Share (DPS) in cents**:")
            exp_dps = f"DPS = (Total Dividends / Number of Issued Shares) × 100 = (R{tot_div_m:,.0f} / {shares_m:,}) × 100 = {c_dps}."
            add_q("medium", "Investor Financial Indicators", q_dps, c_dps, w_dps, "Applying", f"Calculate DPS for {co_inv_m}", exp_dps)

        # Dividend Payout Rate
        if counts["medium"] < 500:
            c_pay = f"{payout_pct:.1f}%"
            w_pay = [
                f"{(eps_cents / dps_cents) * 100:.1f}% (inverted: EPS / DPS)",
                f"{payout_pct * 1.5:.1f}%",
                f"{payout_pct / 2:.1f}%",
                f"{100.0 - payout_pct:.1f}% (calculated retention rate instead of payout rate)",
                f"{payout_pct + 12.0:.1f}%",
                f"{payout_pct - 10.0:.1f}%",
                f"{dps_cents:.1f}% (confused cents with percentage)"
            ]
            q_pay = (f"For **{co_inv_m}**, Earnings per Share was determined at **{eps_cents:.1f} cents** and Dividends per Share at "
                     f"**{dps_cents:.1f} cents**. Calculate the **Dividend Payout Rate (%)**:")
            exp_pay = f"Dividend Payout Rate = (DPS / EPS) × 100 = ({dps_cents:.1f} cents / {eps_cents:.1f} cents) × 100 = {c_pay}."
            add_q("medium", "Investor Financial Indicators", q_pay, c_pay, w_pay, "Applying", f"Calculate Dividend Payout for {co_inv_m}", exp_pay)

    # Combinatorial additions for Medium:
    # Operating Profit Margin on Sales & Gross Margin on Sales across companies
    company_sales_mix = [
        ("Laysano Ltd", 6500000.0, 2600000.0, 1040000.0),
        ("Protea Hardware Ltd", 9200000.0, 3680000.0, 1472000.0),
        ("Zulu Fashion Ltd", 3800000.0, 1520000.0, 608000.0),
        ("Metro Tech Ltd", 14500000.0, 5800000.0, 2320000.0),
        ("Apex Auto Ltd", 7200000.0, 2880000.0, 1152000.0),
        ("Kairo Furnishers Ltd", 8900000.0, 3560000.0, 1424000.0),
        ("Orchid Boutique Ltd", 2900000.0, 1160000.0, 464000.0),
        ("Galaxy Appliances Ltd", 18500000.0, 7400000.0, 2960000.0),
        ("Bakersfield Ltd", 7600000.0, 3040000.0, 1216000.0),
        ("Tshwane Traders Ltd", 6200000.0, 2480000.0, 992000.0)
    ]

    for co_sm, s_val, gp_val, op_val in company_sales_mix:
        if counts["medium"] >= 500:
            break
        gpm_pct = (gp_val / s_val) * 100.0
        opm_pct = (op_val / s_val) * 100.0

        for mult_factor in [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]:
            if counts["medium"] >= 500:
                break
            cur_s = s_val * mult_factor
            cur_gp = gp_val * mult_factor
            cur_op = op_val * mult_factor

            c_gpm = f"{gpm_pct:.1f}% Gross Margin; {opm_pct:.1f}% Operating Margin"
            w_gpm = [
                f"{opm_pct:.1f}% Gross Margin; {gpm_pct:.1f}% Operating Margin (inverted margins)",
                f"{gpm_pct * 1.5:.1f}% Gross Margin",
                f"{opm_pct / 2:.1f}% Operating Margin",
                f"{100.0 - gpm_pct:.1f}% Cost of Sales Margin",
                f"{gpm_pct + 10.0:.1f}% Gross Margin",
                f"{opm_pct + 8.0:.1f}% Operating Margin",
                f"R{cur_gp:,.0f} Margin"
            ]
            q_gpm = (f"The financial records of **{co_sm}** show Sales of **R{cur_s:,.0f}**, Gross Profit of **R{cur_gp:,.0f}**, "
                     f"and Operating Profit of **R{cur_op:,.0f}**. Calculate the **Gross Profit Margin** and **Operating Profit Margin** on sales:")
            exp_gpm = (f"1. Gross Profit Margin = (Gross Profit / Sales) × 100 = (R{cur_gp:,.0f} / R{cur_s:,.0f}) × 100 = {gpm_pct:.1f}%. "
                       f"2. Operating Profit Margin = (Operating Profit / Sales) × 100 = (R{cur_op:,.0f} / R{cur_s:,.0f}) × 100 = {opm_pct:.1f}%.")
            add_q("medium", "Profitability Margins", q_gpm, c_gpm, w_gpm, "Applying", f"Calculate Profit Margins for {co_sm}", exp_gpm)

    # Additional Medium Profitability Indicators: Operating Expenses % and Net Profit Margin %
    operating_expense_cases = [
        ("Laysano Ltd", 6500000.0, 1560000.0, 624000.0),
        ("Protea Hardware Ltd", 9200000.0, 2208000.0, 883200.0),
        ("Zulu Fashion Ltd", 3800000.0, 912000.0, 364800.0),
        ("Metro Tech Ltd", 14500000.0, 3480000.0, 1392000.0),
        ("Apex Auto Ltd", 7200000.0, 1728000.0, 691200.0),
        ("Kairo Furnishers Ltd", 8900000.0, 2136000.0, 854400.0),
        ("Galaxy Appliances Ltd", 18500000.0, 4440000.0, 1776000.0),
        ("Bakersfield Ltd", 7600000.0, 1824000.0, 729600.0),
        ("Tshwane Traders Ltd", 6200000.0, 1488000.0, 595200.0),
        ("Cape Coast Ltd", 7400000.0, 1776000.0, 710400.0),
        ("Durban Wholesale Ltd", 15000000.0, 3600000.0, 1440000.0),
        ("Sandton Goods Ltd", 19500000.0, 4680000.0, 1872000.0),
        ("Bloemfontein Traders Ltd", 7800000.0, 1872000.0, 748800.0),
        ("Polokwane Supply Ltd", 5400000.0, 1296000.0, 518400.0),
        ("Nelspruit Supply Ltd", 4800000.0, 1152000.0, 460800.0),
        ("Kimberley Tools Ltd", 8400000.0, 2016000.0, 806400.0),
        ("Rustenburg Industrial Ltd", 11500000.0, 2760000.0, 1104000.0),
        ("Port Elizabeth Logistics Ltd", 13200000.0, 3168000.0, 1267200.0),
        ("Pietermaritzburg Ltd", 5900000.0, 1416000.0, 566400.0),
        ("Soweto Commercial Ltd", 6800000.0, 1632000.0, 652800.0)
    ]

    for co_oe, s_oe, opex_oe, np_oe in operating_expense_cases:
        if counts["medium"] >= 500:
            break
        opex_pct = (opex_oe / s_oe) * 100.0
        npm_pct = (np_oe / s_oe) * 100.0

        for scale_oe in [0.75, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.45, 1.55]:
            if counts["medium"] >= 500:
                break
            cur_soe = s_oe * scale_oe
            cur_opex = opex_oe * scale_oe
            cur_npoe = np_oe * scale_oe

            # % Operating expenses on sales
            c_opx = f"{opex_pct:.1f}%"
            w_opx = [
                f"{npm_pct:.1f}% (confused operating expenses percentage with net profit margin)",
                f"{opex_pct * 1.5:.1f}%",
                f"{opex_pct / 2:.1f}%",
                f"{100.0 - opex_pct:.1f}%",
                f"{opex_pct + 8.0:.1f}%",
                f"{opex_pct - 6.0:.1f}%",
                f"R{cur_opex:,.0f}"
            ]
            q_opx = (f"**{co_oe}** recorded Sales of **R{cur_soe:,.0f}** and Operating Expenses of **R{cur_opex:,.0f}**. "
                     f"Calculate the **Operating Expenses as a percentage of Sales** (%):")
            exp_opx = f"% Operating Expenses on Sales = (Operating Expenses / Sales) × 100 = (R{cur_opex:,.0f} / R{cur_soe:,.0f}) × 100 = {c_opx}."
            add_q("medium", "Operating Expenses Analysis", q_opx, c_opx, w_opx, "Applying", f"Calculate Operating Expense % for {co_oe}", exp_opx)

            # % Net Profit Margin on sales
            if counts["medium"] < 500:
                c_npm = f"{npm_pct:.1f}%"
                w_npm = [
                    f"{opex_pct:.1f}% (confused Net Profit Margin with Operating Expenses percentage)",
                    f"{npm_pct * 1.5:.1f}%",
                    f"{npm_pct / 2:.1f}%",
                    f"{npm_pct + 5.0:.1f}%",
                    f"{npm_pct - 4.0:.1f}%",
                    f"{100.0 - npm_pct:.1f}%",
                    f"R{cur_npoe:,.0f}"
                ]
                q_npm = (f"The Income Statement of **{co_oe}** reflects Sales of **R{cur_soe:,.0f}** and Net Profit after Tax of "
                         f"**R{cur_npoe:,.0f}**. Determine the **Net Profit Margin on Sales** (%):")
                exp_npm = f"Net Profit Margin = (Net Profit after Tax / Sales) × 100 = (R{cur_npoe:,.0f} / R{cur_soe:,.0f}) × 100 = {c_npm}."
                add_q("medium", "Operating Expenses Analysis", q_npm, c_npm, w_npm, "Applying", f"Calculate Net Profit Margin for {co_oe}", exp_npm)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Reverse Engineering Balance Sheet Items from Ratios (Inventory, Debtors, Debt, Total Assets),
    # Weighted Average Shares for EPS, Gearing & Financial Risk Decision Making
    # =========================================================================

    reverse_companies = [
        "Laysano Ltd", "Protea Hardware Ltd", "Zulu Fashion Ltd", "Metro Tech Ltd",
        "Apex Auto Ltd", "Kairo Furnishers Ltd", "Orchid Boutique Ltd", "Galaxy Appliances Ltd",
        "Bakersfield Ltd", "Tshwane Traders Ltd", "Cape Coast Ltd", "Durban Wholesale Ltd",
        "Sandton Goods Ltd", "Bloemfontein Traders Ltd", "Polokwane Supply Ltd", "Nelspruit Supply Ltd",
        "Kimberley Tools Ltd", "Rustenburg Industrial Ltd", "Port Elizabeth Logistics Ltd", "Pietermaritzburg Ltd"
    ]
    reverse_param_matrix = [
        (2.2, 1.2, 650000.0, 0.45, 5200000.0, 2.5),
        (2.0, 1.1, 950000.0, 0.35, 7800000.0, 2.8),
        (2.4, 1.4, 380000.0, 0.50, 3200000.0, 2.2),
        (1.8, 0.9, 1800000.0, 0.60, 11500000.0, 2.4),
        (2.1, 1.2, 750000.0, 0.40, 5600000.0, 2.6),
        (2.3, 1.3, 1100000.0, 0.45, 8200000.0, 2.7),
        (2.5, 1.5, 320000.0, 0.30, 2800000.0, 3.1),
        (1.9, 1.0, 2200000.0, 0.55, 14200000.0, 2.3),
        (2.2, 1.2, 820000.0, 0.42, 6100000.0, 2.5),
        (2.0, 1.0, 720000.0, 0.48, 5300000.0, 2.4),
        (2.1, 1.1, 860000.0, 0.38, 5900000.0, 2.8),
        (2.0, 1.1, 1750000.0, 0.45, 11200000.0, 2.6)
    ]

    for co_rev in reverse_companies:
        for cr_r, at_r, cl_r, gear_r, eq_r, solv_r in reverse_param_matrix:
            inv_rev = (cr_r - at_r) * cl_r
            ncl_rev = gear_r * eq_r
            tot_liab_calc = ncl_rev + cl_r
            tot_assets_rev = solv_r * tot_liab_calc

            for q_type_rev in [1, 2, 3]:
                if counts["hard"] >= 200:
                    break

                if q_type_rev == 1:
                    # Reverse calculate Trading Inventory
                    c_ri = f"Trading Inventory = R{inv_rev:,.0f}"
                    w_ri = [
                        f"Trading Inventory = R{cr_r * cl_r:,.0f} (calculated Total Current Assets instead of inventory)",
                        f"Trading Inventory = R{at_r * cl_r:,.0f} (calculated Quick Assets instead of inventory)",
                        f"Trading Inventory = R{inv_rev * 1.5:,.0f}",
                        f"Trading Inventory = R{inv_rev / 2:,.0f}",
                        f"Trading Inventory = R{(cr_r + at_r) * cl_r:,.0f}",
                        f"Trading Inventory = R{cl_r:,.0f}",
                        f"Trading Inventory = R{inv_rev + 100000:,.0f}"
                    ]
                    q_ri = (f"The financial indicators of **{co_rev}** reflect a **Current Ratio of {cr_r:.1f} : 1** and an **Acid-Test Ratio "
                            f"of {at_r:.1f} : 1**. The Balance Sheet discloses Current Liabilities of **R{cl_r:,.0f}**. Reverse-engineer "
                            f"the exact carrying value of **Trading Inventory**:")
                    exp_ri = (f"1. Current Assets = Current Ratio × CL = {cr_r:.1f} × R{cl_r:,.0f} = R{cr_r * cl_r:,.0f}. "
                              f"2. Quick Assets (CA - Inventory) = Acid-Test × CL = {at_r:.1f} × R{cl_r:,.0f} = R{at_r * cl_r:,.0f}. "
                              f"3. Trading Inventory = Current Assets - Quick Assets = (Current Ratio - Acid-Test) × CL "
                              f"= ({cr_r:.1f} - {at_r:.1f}) × R{cl_r:,.0f} = {cr_r - at_r:.1f} × R{cl_r:,.0f} = {c_ri}.")
                    add_q("hard", "Reverse Ratio Engineering", q_ri, c_ri, w_ri, "Evaluating", f"Reverse calculate Inventory for {co_rev}", exp_ri)

                elif q_type_rev == 2:
                    # Reverse calculate Non-Current Liabilities (Loan)
                    c_rn = f"Non-Current Liabilities (Loan) = R{ncl_rev:,.0f}"
                    w_rn = [
                        f"Non-Current Liabilities = R{eq_r / gear_r:,.0f} (inverted: Equity / Gearing)",
                        f"Non-Current Liabilities = R{eq_r:,.0f} (confused debt with equity)",
                        f"Non-Current Liabilities = R{ncl_rev * 1.5:,.0f}",
                        f"Non-Current Liabilities = R{ncl_rev / 2:,.0f}",
                        f"Non-Current Liabilities = R{tot_liab_calc:,.0f} (calculated Total Liabilities instead of loan)",
                        f"Non-Current Liabilities = R{ncl_rev + 250000:,.0f}",
                        f"Non-Current Liabilities = R{eq_r * (1 + gear_r):,.0f}"
                    ]
                    q_rn = (f"**{co_rev}** maintains a **Debt-Equity Ratio of {gear_r:.2f} : 1**. The Statement of Financial Position "
                            f"reports Shareholders' Equity of **R{eq_r:,.0f}**. Calculate the exact balance of **Non-Current Liabilities (Mortgage Loan)**:")
                    exp_rn = f"Debt-Equity = Non-Current Liabilities / Equity. Therefore: Non-Current Liabilities = Gearing × Equity = {gear_r:.2f} × R{eq_r:,.0f} = {c_rn}."
                    add_q("hard", "Reverse Ratio Engineering", q_rn, c_rn, w_rn, "Evaluating", f"Reverse calculate Loan for {co_rev}", exp_rn)

                else:
                    # Reverse calculate Total Assets from Solvency
                    c_rta = f"Total Assets = R{tot_assets_rev:,.0f}"
                    w_rta = [
                        f"Total Assets = R{tot_liab_calc:,.0f} (confused Total Liabilities with Total Assets)",
                        f"Total Assets = R{solv_r * cl_r:,.0f} (only multiplied Current Liabilities)",
                        f"Total Assets = R{tot_assets_rev * 1.2:,.0f}",
                        f"Total Assets = R{tot_assets_rev / 2:,.0f}",
                        f"Total Assets = R{solv_r * eq_r:,.0f} (multiplied equity instead of liabilities)",
                        f"Total Assets = R{tot_assets_rev + 500000:,.0f}",
                        f"Total Assets = R{ncl_rev * solv_r:,.0f}"
                    ]
                    q_rta = (f"In the accounts of **{co_rev}**, the **Solvency Ratio is {solv_r:.1f} : 1**. Non-Current Liabilities are **R{ncl_rev:,.0f}** "
                             f"and Current Liabilities are **R{cl_r:,.0f}**. Calculate the exact value of **Total Assets**:")
                    exp_rta = (f"1. Total Liabilities = Non-Current Liabilities (R{ncl_rev:,.0f}) + Current Liabilities (R{cl_r:,.0f}) = R{tot_liab_calc:,.0f}. "
                               f"2. Total Assets = Solvency Ratio × Total Liabilities = {solv_r:.1f} × R{tot_liab_calc:,.0f} = {c_rta}.")
                    add_q("hard", "Reverse Ratio Engineering", q_rta, c_rta, w_rta, "Evaluating", f"Reverse calculate Assets for {co_rev}", exp_rta)

    # Weighted Average Shares for EPS (Hard)
    weighted_share_cases = [
        ("Laysano Ltd", 500000, 100000, "1 September", 6, 920000.0),
        ("Protea Hardware Ltd", 700000, 150000, "1 December", 3, 1450000.0),
        ("Zulu Fashion Ltd", 350000, 80000, "1 June", 9, 580000.0),
        ("Metro Tech Ltd", 1000000, 240000, "1 September", 6, 2350000.0),
        ("Apex Auto Ltd", 450000, 120000, "1 November", 4, 1050000.0),
        ("Kairo Furnishers Ltd", 600000, 160000, "1 June", 9, 1520000.0),
        ("Galaxy Appliances Ltd", 1200000, 300000, "1 September", 6, 3100000.0),
        ("Bakersfield Ltd", 550000, 140000, "1 December", 3, 1120000.0),
        ("Tshwane Traders Ltd", 480000, 100000, "1 September", 6, 950000.0),
        ("Cape Coast Ltd", 520000, 120000, "1 June", 9, 1080000.0),
        ("Durban Wholesale Ltd", 950000, 200000, "1 November", 4, 2100000.0),
        ("Sandton Goods Ltd", 1100000, 250000, "1 September", 6, 2650000.0)
    ]

    for co_ws, sh_start, sh_new, dt_issued, m_active_sh, npat_ws in weighted_share_cases:
        if counts["hard"] >= 200:
            break
        # Weighted shares = Opening shares + New shares * (m_active / 12)
        weighted_shares = sh_start + (sh_new * (m_active_sh / 12.0))
        eps_weighted = (npat_ws / weighted_shares) * 100.0
        eps_unweighted = (npat_ws / (sh_start + sh_new)) * 100.0

        c_weps = f"Weighted Shares = {weighted_shares:,.0f}; EPS = {eps_weighted:.1f} cents"
        w_weps = [
            f"Weighted Shares = {sh_start + sh_new:,}; EPS = {eps_unweighted:.1f} cents (treated new shares as issued for the entire 12 months)",
            f"Weighted Shares = {sh_start:,}; EPS = {(npat_ws / sh_start) * 100:.1f} cents (ignored new shares completely)",
            f"Weighted Shares = {weighted_shares * 1.2:,.0f}; EPS = {eps_weighted * 0.8:.1f} cents",
            f"Weighted Shares = {weighted_shares / 2:,.0f}; EPS = {eps_weighted * 2:.1f} cents",
            f"Weighted Shares = {weighted_shares:,.0f}; EPS = {eps_weighted / 100:.2f} cents (forgot cents conversion)",
            f"Weighted Shares = {sh_new:,}; EPS = {(npat_ws / sh_new) * 100:.1f} cents",
            f"Weighted Shares = {weighted_shares + 50000:,.0f}; EPS = {eps_weighted - 5.0:.1f} cents"
        ]
        q_weps = (f"**{co_ws}** commenced the financial year on 1 March with **{sh_start:,} issued shares**. On **{dt_issued}** "
                  f"({m_active_sh} months into the financial year), an additional **{sh_new:,} ordinary shares** were issued. "
                  f"Net Profit after Tax for the year amounted to **R{npat_ws:,.0f}**. Calculate the **Weighted Average Number of Shares** "
                  f"and the accurate **Earnings per Share (EPS) in cents**:")
        exp_weps = (f"1. Weighted Average Shares = Opening ({sh_start:,}) + New Shares ({sh_new:,} × {m_active_sh}/12) "
                    f"= {sh_start:,} + {sh_new * (m_active_sh/12.0):,.0f} = {weighted_shares:,.0f} shares. "
                    f"2. EPS = (Net Profit after Tax / Weighted Shares) × 100 = (R{npat_ws:,.0f} / {weighted_shares:,.0f}) × 100 = {c_weps}.")
        add_q("hard", "Weighted Average Shares & EPS", q_weps, c_weps, w_weps, "Evaluating", f"Calculate Weighted EPS for {co_ws}", exp_weps)

    # Gearing & Risk Evaluation Decision Making (Hard)
    gearing_decision_cases = [
        ("Laysano Ltd", 0.40, 14.5, 10.5, "POSITIVE GEARING (ROTCE 14.5% > Interest rate 10.5%): Business benefits from using borrowed capital"),
        ("Protea Hardware Ltd", 0.75, 9.2, 11.5, "NEGATIVE GEARING (ROTCE 9.2% < Interest rate 11.5%): Borrowed capital costs more than it earns, eroding shareholder returns"),
        ("Zulu Fashion Ltd", 0.25, 16.0, 11.0, "POSITIVE GEARING (ROTCE 16.0% > Interest rate 11.0%): Highly favourable borrowing conditions with low financial risk"),
        ("Metro Tech Ltd", 0.85, 8.5, 12.0, "NEGATIVE GEARING (ROTCE 8.5% < Interest rate 12.0%): High financial risk; the company should consider paying down debt or raising equity"),
        ("Apex Auto Ltd", 0.35, 13.8, 10.0, "POSITIVE GEARING (ROTCE 13.8% > Interest rate 10.0%): Effective financial leverage boosting shareholder returns"),
        ("Kairo Furnishers Ltd", 0.65, 10.0, 11.0, "NEGATIVE GEARING (ROTCE 10.0% < Interest rate 11.0%): Unfavourable leverage where loan interest exceeds operating return"),
        ("Galaxy Appliances Ltd", 0.30, 15.5, 10.5, "POSITIVE GEARING (ROTCE 15.5% > Interest rate 10.5%): Low debt risk combined with strong operating returns"),
        ("Bakersfield Ltd", 0.55, 11.2, 11.0, "MARGINAL POSITIVE GEARING (ROTCE 11.2% ≈ Interest rate 11.0%): Thin safety margin against potential interest rate hikes")
    ]

    for co_gd, gear_val, rotce_val, int_rate_val, gd_eval in gearing_decision_cases:
        if counts["hard"] >= 200:
            break
        c_gd = f"Evaluation: {gd_eval}."
        w_gd = [
            f"Evaluation: {'NEGATIVE GEARING' if 'POSITIVE' in gd_eval else 'POSITIVE GEARING'} because any company with a loan is bankrupt.",
            "Evaluation: Zero financial risk because South African banks are non-profit institutions.",
            "Evaluation: Directors must be dismissed immediately under the King IV Code.",
            "Evaluation: The company is legally required to convert all debt into trade creditors within thirty days.",
            "Evaluation: Interest rates have zero mathematical relationship to operating returns.",
            "Evaluation: Gearing is irrelevant because shareholders receive dividends before loan interest is paid."
        ]
        q_gd = (f"The financial indicators of **{co_gd}** show a **Debt-Equity Ratio of {gear_val:.2f} : 1**, a **Return on Total Capital "
                f"Employed (ROTCE) of {rotce_val:.1f}%**, and the business pays an average **borrowing interest rate of {int_rate_val:.1f}%** "
                f"on its bank loans. Critically evaluate the financial gearing and risk of the enterprise:")
        exp_gd = (f"Gearing evaluation: Debt-Equity is {gear_val:.2f} : 1. Compare ROTCE ({rotce_val:.1f}%) with loan interest rate ({int_rate_val:.1f}%): "
                  f"If ROTCE > Interest rate, the business earns more on borrowed money than it costs in interest (Positive Gearing). "
                  f"If ROTCE < Interest rate, borrowing reduces return to shareholders (Negative Gearing). Result: {c_gd}")
        add_q("hard", "Gearing & Risk Decision Making", q_gd, c_gd, w_gd, "Evaluating", f"Evaluate Gearing for {co_gd}", exp_gd)

    return questions

if __name__ == '__main__':
    qs = build_analysis()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_acc_analysis.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
