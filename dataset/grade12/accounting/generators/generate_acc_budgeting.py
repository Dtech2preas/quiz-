import json
import os

def build_budgeting():
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
        qid = f"ACC_P2_BUD_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Budgeting",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Budgeting",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Purpose of Budgeting, Cash Budget vs Projected Income Statement, Cash vs Credit Splits
    # =========================================================================

    easy_concepts = [
        ("Purpose of a Cash Budget",
         "To project and monitor expected future cash inflows and outflows to anticipate cash surpluses or deficits and ensure adequate liquidity",
         "To calculate the historical net profit earned during the previous financial trading year",
         "To determine the taxable income payable to the South African Revenue Service (SARS)",
         "To allocate authorized share capital among existing ordinary company shareholders",
         "To record daily cash register till slip shortages and petty cash vouchers",
         "To establish the current replacement cost of factory fixed plant and machinery",
         "To calculate the total depreciation accumulated on commercial delivery vehicles"),

        ("Purpose of a Projected Income Statement",
         "To forecast expected revenues, costs, and operating profit or loss over a future period on an accrual basis",
         "To list physical cash deposits and electronic fund transfers on a daily basis",
         "To verify the reconciliation between the bank statement and cash receipts journal",
         "To track the physical movement of raw materials from the storehouse to the production floor",
         "To calculate the exact customs import tariffs payable on foreign imported goods",
         "To determine the number of ordinary shares to repurchase under Section 48 of the Companies Act",
         "To record the outstanding balances owed by individual credit customers in the debtors ledger"),

        ("Depreciation in Budgeting",
         "Depreciation is a non-cash expense that is included in the Projected Income Statement but completely excluded from the Cash Budget",
         "Depreciation is recorded as a major cash payment in the Cash Budget every month",
         "Depreciation is treated as a cash inflow under cash receipts in the Cash Budget",
         "Depreciation is deducted directly from the opening bank balance in the Cash Budget",
         "Depreciation is added to the collection from debtors in the Cash Budget",
         "Depreciation is classified as an investing cash receipt in the Cash Budget",
         "Depreciation is remitted to commercial banks to reduce the principal loan balance"),

        ("Bad Debts in Budgeting",
         "Bad debts are non-cash write-offs included as an operating expense in the Projected Income Statement but omitted from the Cash Budget",
         "Bad debts are entered as a monthly cash payment to credit customers in the Cash Budget",
         "Bad debts are added to cash receipts to increase projected bank liquidity",
         "Bad debts are paid to SARS as a tax deductible provisional expense in the Cash Budget",
         "Bad debts appear under financing cash outflows in the Cash Budget",
         "Bad debts represent cash discounts granted to prompt paying debtors in the Cash Budget",
         "Bad debts are recorded as cash purchases of trading inventory in the Cash Budget"),

        ("Discount Allowed in Budgeting",
         "Discount allowed reduces the actual cash collected from debtors in the Cash Budget and is recorded as an operating expense in the Projected Income Statement",
         "Discount allowed is entered as a direct cash outflow under cash payments in the Cash Budget",
         "Discount allowed increases the cash collected from debtors in the Debtors Collection Schedule",
         "Discount allowed is paid directly to commercial banks as finance charges",
         "Discount allowed is treated as a non-operating capital receipt in the Cash Budget",
         "Discount allowed is added to gross sales revenue in the Projected Income Statement",
         "Discount allowed is refunded by SARS upon submission of VAT 201 declarations"),

        ("Purchase of Fixed Assets in Budgeting",
         "A cash purchase of equipment is entered in full as a cash outflow in the Cash Budget, while only the annual depreciation appears in the Projected Income Statement",
         "The full cost of purchasing equipment is deducted as an operating expense in the Projected Income Statement",
         "Asset purchases are recorded as cash inflows under cash receipts in the Cash Budget",
         "Asset purchases have zero impact on the Cash Budget if purchased for cash",
         "Equipment purchases are debited directly to the Retained Income Note in the Cash Budget",
         "Equipment purchases are amortized over 20 years as monthly payments in the Cash Budget",
         "Asset purchases are classified under payments to creditors in the Cash Budget"),

        ("Repayment of Long-Term Loan in Budgeting",
         "The capital (principal) portion of the loan repayment is a cash payment in the Cash Budget but is not an expense in the Projected Income Statement",
         "The full capital loan repayment is deducted as an operating expense in the Projected Income Statement",
         "Capital loan repayments are recorded as cash receipts in the Cash Budget",
         "Loan repayments are excluded from the Cash Budget because loans are non-current liabilities",
         "Loan repayments are credited directly to Ordinary Share Capital in the Cash Budget",
         "Loan repayments are treated as trade creditor settlements in the Cash Budget",
         "Loan repayments are refunded by the commercial lender upon loan maturity"),

        ("Interest on Loan in Budgeting",
         "Interest on loan is an expense in the Projected Income Statement and a cash outflow in the Cash Budget in the month it is paid",
         "Interest on loan is an asset that increases projected bank cash balances",
         "Interest on loan is excluded from the Projected Income Statement under IFRS rules",
         "Interest on loan is paid only upon the complete dissolution of the company",
         "Interest on loan is treated as a cash inflow under operating receipts in the Cash Budget",
         "Interest on loan is deducted from the gross invoice total of trade debtors",
         "Interest on loan is an administrative salary expense paid to executive directors"),

        ("Provisional Tax Payments in Budgeting",
         "Provisional income tax payments made to SARS (usually in August and February) are cash outflows in the Cash Budget",
         "Provisional tax payments are spread equally across all twelve months in the Cash Budget",
         "Provisional tax payments are treated as cash receipts from the Department of Trade and Industry",
         "Provisional tax is excluded from the Cash Budget because company taxes are not paid in cash",
         "Provisional tax payments are debited to Trade and Other Receivables in the Cash Budget",
         "Provisional tax payments represent dividends declared to registered shareholders",
         "Provisional tax is refunded automatically by commercial banks every quarter"),

        ("Cash Surplus vs Cash Deficit",
         "A cash surplus occurs when projected cash receipts exceed cash payments; a cash deficit occurs when payments exceed receipts",
         "A cash surplus indicates that the business has zero outstanding trade creditors",
         "A cash deficit means the business is legally insolvent and must immediately liquidate",
         "A cash surplus is identical to net operating profit after tax in the income statement",
         "A cash deficit occurs only when the company pays interim dividends to shareholders",
         "A cash surplus requires the business to double its retail selling prices",
         "A cash deficit means that debtors collection percentage is exactly 100%")
    ]

    for title_b, corr_b, *wrongs_b in easy_concepts:
        q_b1 = f"In Grade 12 Accounting Paper 2 (Budgeting), what is the key accounting rule regarding **{title_b}**?"
        exp_b1 = f"**{title_b}**: {corr_b}. Distinguishing between cash and accrual items is a core requirement under DBE CAPS Accounting."
        add_q("easy", "Budget Concepts & Differences", q_b1, corr_b, wrongs_b, "Remembering", f"Define rule for {title_b}", exp_b1)

        q_b2 = f"Which budgeting principle or transaction treatment is described by: *\"{corr_b}\"*?"
        clean_terms_b = [
            "Fixed Overhead Absorption", "Continuous Rolling Forecast",
            "Zero-Base Budgeting Allocation", "Variance Standard Reconciliation",
            "Capital Redemption Reserve", "Debenture Redemption Portfolio",
            "Working Capital Ratio Analysis"
        ]
        exp_b2 = f"This describes **{title_b}**. {corr_b}."
        add_q("easy", "Budget Concepts & Differences", q_b2, title_b, clean_terms_b, "Understanding", f"Identify {title_b}", exp_b2)

    # Cash vs Credit splits and direct calculations (60 companies)
    calc_easy_bud = [
        ("Protea Outfitters Ltd", 500000.0, 60, 400000.0, 25),
        ("Kavango Electronics Ltd", 800000.0, 40, 600000.0, 30),
        ("Algoa Furnishers Ltd", 650000.0, 30, 500000.0, 20),
        ("Soweto Retail Stores Ltd", 950000.0, 75, 700000.0, 40),
        ("Drakensberg Hardware Ltd", 420000.0, 50, 350000.0, 25),
        ("Zululand Supermarket Ltd", 1200000.0, 80, 900000.0, 50),
        ("Highveld Appliances Ltd", 750000.0, 35, 550000.0, 20),
        ("Karoo Auto Spares Ltd", 380000.0, 45, 280000.0, 30),
        ("Table Mountain Books Ltd", 320000.0, 70, 220000.0, 35),
        ("Springbok Sportswear Ltd", 620000.0, 55, 450000.0, 25),
        ("Limpopo Agri Supplies Ltd", 850000.0, 40, 650000.0, 20),
        ("Blyde Valley Traders Ltd", 480000.0, 50, 360000.0, 30),
        ("Gauteng Pharma Stores Ltd", 1100000.0, 65, 800000.0, 40),
        ("Free State Feeds Ltd", 580000.0, 35, 420000.0, 25),
        ("Namaqua General Store Ltd", 290000.0, 60, 210000.0, 30),
        ("Outeniqua Timber Sales Ltd", 720000.0, 30, 520000.0, 20),
        ("Mpumalanga Builders Ltd", 980000.0, 45, 750000.0, 25),
        ("Ezulwini Homeware Ltd", 460000.0, 55, 340000.0, 35),
        ("Vaal Triangle Motors Ltd", 1400000.0, 25, 1100000.0, 15),
        ("Stellenbosch Cellars Ltd", 540000.0, 60, 380000.0, 30),
        ("Tshwane Computech Ltd", 880000.0, 40, 620000.0, 25),
        ("Richards Bay Marine Ltd", 760000.0, 35, 540000.0, 20),
        ("Polokwane Cash & Carry Ltd", 1350000.0, 85, 1050000.0, 60),
        ("Kimberley Mining Gear Ltd", 920000.0, 30, 680000.0, 20),
        ("Durban Fashion House Ltd", 680000.0, 50, 480000.0, 30),
        ("Rustenburg Industrial Supplies Ltd", 1150000.0, 35, 850000.0, 25),
        ("Witbank Electrical Ltd", 820000.0, 45, 590000.0, 30),
        ("Paarl Fresh Foods Ltd", 640000.0, 70, 460000.0, 40),
        ("Midrand IT Emporium Ltd", 1250000.0, 40, 920000.0, 25),
        ("Centurion Sports Hub Ltd", 590000.0, 60, 410000.0, 35),
        ("Bloemfontein Meat Wholesalers Ltd", 1050000.0, 65, 780000.0, 45),
        ("East London Marine Spares Ltd", 510000.0, 40, 370000.0, 25),
        ("Klerksdorp Building Center Ltd", 870000.0, 35, 630000.0, 20),
        ("Potchefstroom Books Ltd", 360000.0, 75, 250000.0, 40),
        ("George Furniture Emporium Ltd", 740000.0, 30, 530000.0, 20),
        ("Secunda Safety Gear Ltd", 690000.0, 45, 490000.0, 30),
        ("Vereeniging Engineering Supplies Ltd", 1180000.0, 35, 860000.0, 20),
        ("Welkom Mining Merchants Ltd", 960000.0, 40, 710000.0, 25),
        ("Bethlehem Farmers Market Ltd", 630000.0, 60, 440000.0, 35),
        ("Newcastle Hardware Mart Ltd", 840000.0, 50, 610000.0, 30),
        ("Mossel Bay Boating Ltd", 580000.0, 40, 420000.0, 25),
        ("Mthatha General Dealers Ltd", 490000.0, 70, 350000.0, 40),
        ("Upington Sun Trading Ltd", 530000.0, 55, 390000.0, 30),
        ("Vryheid Timber Merchants Ltd", 710000.0, 35, 510000.0, 20),
        ("Ladysmith Drapery Ltd", 450000.0, 60, 320000.0, 35),
        ("Bredasdorp Agri Wholesale Ltd", 780000.0, 40, 560000.0, 25),
        ("Cradock Livestock Supplies Ltd", 660000.0, 45, 470000.0, 30),
        ("Makhanda Stationery Ltd", 340000.0, 65, 240000.0, 35),
        ("Oudtshoorn Leather Mart Ltd", 560000.0, 50, 390000.0, 30),
        ("Knysna Marine Hardware Ltd", 890000.0, 35, 640000.0, 20),
        ("Standerton Dairy Merchants Ltd", 670000.0, 60, 480000.0, 35),
        ("Harrismith Logistics Depot Ltd", 790000.0, 40, 570000.0, 25),
        ("Kuruman Mineral Traders Ltd", 1120000.0, 30, 820000.0, 20),
        ("Thohoyandou Superstore Ltd", 830000.0, 75, 590000.0, 45),
        ("Plettenberg Bay Decor Ltd", 610000.0, 50, 430000.0, 30),
        ("Saldanha Marine Freight Ltd", 1280000.0, 35, 940000.0, 25),
        ("Grahamstown Scholastic Ltd", 420000.0, 60, 300000.0, 35),
        ("Springbok Wind Parts Ltd", 990000.0, 40, 720000.0, 25),
        ("Witbank Coal Equipment Ltd", 1320000.0, 30, 970000.0, 20),
        ("Paarl Valley Beverages Ltd", 730000.0, 65, 520000.0, 35),
        ("Centurion Office Machines Ltd", 840000.0, 45, 620000.0, 25),
        ("Bloemfontein Grain Merchants Ltd", 670000.0, 55, 480000.0, 30),
        ("East London Fishing Gear Ltd", 530000.0, 40, 390000.0, 20),
        ("Klerksdorp Mining Supplies Ltd", 910000.0, 35, 680000.0, 25),
        ("Potchefstroom Feeds Mart Ltd", 620000.0, 60, 450000.0, 35),
        ("George Hardwood Depot Ltd", 760000.0, 30, 550000.0, 20),
        ("Secunda Safety Wear Ltd", 830000.0, 50, 610000.0, 30),
        ("Vereeniging Boiler Supplies Ltd", 1150000.0, 35, 840000.0, 25),
        ("Welkom Shaft Merchants Ltd", 940000.0, 40, 690000.0, 25),
        ("Bethlehem Farmers Coop Ltd", 680000.0, 60, 490000.0, 35),
        ("Newcastle Heavy Hardware Ltd", 890000.0, 45, 650000.0, 30),
        ("Mossel Bay Fuel Traders Ltd", 1250000.0, 70, 950000.0, 40)
    ]

    for co_b, tot_sales, cash_s_pct, tot_purch, cash_p_pct in calc_easy_bud:
        # 1. Cash Sales calculation
        c_sales = tot_sales * (cash_s_pct / 100)
        c_cs = f"R{c_sales:,.2f}"
        credit_s = tot_sales - c_sales
        w_cs = [
            f"R{credit_s:,.2f} (calculated credit sales instead of cash sales)",
            f"R{tot_sales:,.2f} (used total sales without percentage split)",
            f"R{c_sales * 1.15:,.2f}",
            f"R{c_sales * 0.85:,.2f}",
            f"R{(c_sales + 50000):,.2f}",
            f"R{(c_sales - 40000):,.2f}",
            f"R{tot_sales * 0.5:,.2f} (assumed 50% cash split)"
        ]
        q_cs = (f"**{co_b}** budgets total sales of **R{tot_sales:,.2f}** for December. Management anticipates that **{cash_s_pct}%** of all sales will be for cash, "
                f"with the remainder sold on credit. Calculate the budgeted **Cash Sales** to be entered under cash receipts in the December Cash Budget:")
        exp_cs = f"Cash Sales = Total Sales x Cash Sales % = R{tot_sales:,.2f} x {cash_s_pct}% = {c_cs}."
        add_q("easy", "Cash vs Credit Splits", q_cs, c_cs, w_cs, "Applying", f"Calculate cash sales for {co_b}", exp_cs)

        # 2. Credit Sales calculation
        c_crs = f"R{credit_s:,.2f}"
        w_crs = [
            f"R{c_sales:,.2f} (calculated cash sales instead of credit sales)",
            f"R{tot_sales:,.2f} (used total sales)",
            f"R{credit_s * 1.15:,.2f}",
            f"R{credit_s * 0.85:,.2f}",
            f"R{(credit_s + 60000):,.2f}",
            f"R{(credit_s - 50000):,.2f}",
            f"R{tot_sales * 0.5:,.2f}"
        ]
        q_crs = (f"**{co_b}** projects total sales of **R{tot_sales:,.2f}** for November, of which **{cash_s_pct}%** will be cash sales. "
                 f"Calculate the **Credit Sales** that will form the basis of the Debtors Collection Schedule:")
        exp_crs = f"Credit Sales = Total Sales x (100% - Cash Sales %) = R{tot_sales:,.2f} x {100 - cash_s_pct}% = {c_crs}."
        add_q("easy", "Cash vs Credit Splits", q_crs, c_crs, w_crs, "Applying", f"Calculate credit sales for {co_b}", exp_crs)

        # 3. Cash Purchases calculation
        c_purch = tot_purch * (cash_p_pct / 100)
        c_cp = f"R{c_purch:,.2f}"
        credit_p = tot_purch - c_purch
        w_cp = [
            f"R{credit_p:,.2f} (calculated credit purchases instead of cash purchases)",
            f"R{tot_purch:,.2f} (used total purchases)",
            f"R{c_purch * 1.2:,.2f}",
            f"R{c_purch * 0.8:,.2f}",
            f"R{(c_purch + 30000):,.2f}",
            f"R{(c_purch - 25000):,.2f}",
            f"R{tot_purch * 0.5:,.2f}"
        ]
        q_cp = (f"**{co_b}** plans total inventory purchases of **R{tot_purch:,.2f}** for October. The business policy is to pay cash for **{cash_p_pct}%** of purchases "
                f"to obtain trade discounts, with the balance purchased on 30-day credit. Calculate budgeted **Cash Purchases of Stock** for the Cash Budget:")
        exp_cp = f"Cash Purchases = Total Purchases x Cash Purchases % = R{tot_purch:,.2f} x {cash_p_pct}% = {c_cp}."
        add_q("easy", "Cash vs Credit Splits", q_cp, c_cp, w_cp, "Applying", f"Calculate cash purchases for {co_b}", exp_cp)

        # 4. Closing Bank Balance Calculation
        op_bank = 45000.0 + (tot_sales * 0.05)
        tot_receipts = c_sales + 120000.0
        tot_payments = c_purch + 110000.0
        net_cf = tot_receipts - tot_payments
        cl_bank = op_bank + net_cf
        c_cb = f"R{cl_bank:,.2f}"
        w_cb = [
            f"R{net_cf:,.2f} (omitted opening bank balance: net cash flow only)",
            f"R{op_bank - net_cf:,.2f} (deducted net cash flow from opening balance)",
            f"R{tot_receipts:,.2f} (used total receipts only)",
            f"R{cl_bank * 1.15:,.2f}",
            f"R{cl_bank * 0.85:,.2f}",
            f"R{(cl_bank + 40000):,.2f}",
            f"R{(cl_bank - 35000):,.2f}"
        ]
        q_cb = (f"The Cash Budget of **{co_b}** for January shows an opening bank balance of **R{op_bank:,.2f}**. "
                f"Projected cash receipts total **R{tot_receipts:,.2f}** and projected cash payments total **R{tot_payments:,.2f}**. "
                f"Calculate the budgeted **Closing Bank Balance** at the end of January:")
        exp_cb = (f"Net Cash Flow = Receipts (R{tot_receipts:,.2f}) - Payments (R{tot_payments:,.2f}) = R{net_cf:,.2f}\n"
                  f"Closing Bank Balance = Opening Bank Balance + Net Cash Flow = R{op_bank:,.2f} + R{net_cf:,.2f} = {c_cb}.")
        add_q("easy", "Cash Budget Structure", q_cb, c_cb, w_cb, "Applying", f"Calculate closing bank balance for {co_b}", exp_cb)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Debtors Collection Schedules, Creditors Payment Schedules, Rent Escalations, Cash Budgets
    # =========================================================================

    # 50 South African commercial retailers with multi-month sales streams
    # (Company, Aug_credit, Sep_credit, Oct_credit, Nov_credit, Dec_credit, Aug_purch, Sep_purch, Oct_purch, Nov_purch, Dec_purch)
    # Collection Pattern:
    # Month of sale: 20% collected subject to 5% cash discount -> 20% * 0.95 = 19% cash
    # 30 days (month 1): 50% collected
    # 60 days (month 2): 28% collected
    # 90 days (month 3): 2% written off as bad debts
    # Creditors Payment Pattern:
    # 70% paid in the month following purchase subject to 2.5% discount -> 70% * 0.975 = 68.25%
    # 30% paid in the second month following purchase
    budget_scenarios = [
        ("Protea Retailers Ltd", 300000.0, 320000.0, 350000.0, 420000.0, 500000.0, 200000.0, 220000.0, 250000.0, 300000.0, 360000.0),
        ("Kavango Emporium Ltd", 450000.0, 480000.0, 520000.0, 600000.0, 720000.0, 300000.0, 320000.0, 360000.0, 420000.0, 500000.0),
        ("Algoa Furnishers Ltd", 380000.0, 400000.0, 440000.0, 510000.0, 620000.0, 250000.0, 270000.0, 300000.0, 350000.0, 420000.0),
        ("Soweto Megastore Ltd", 600000.0, 640000.0, 700000.0, 820000.0, 980000.0, 400000.0, 430000.0, 480000.0, 560000.0, 680000.0),
        ("Drakensberg Hardware Ltd", 280000.0, 300000.0, 330000.0, 390000.0, 460000.0, 180000.0, 195000.0, 220000.0, 260000.0, 310000.0),
        ("Zululand Wholesalers Ltd", 720000.0, 760000.0, 820000.0, 950000.0, 1150000.0, 480000.0, 510000.0, 560000.0, 650000.0, 780000.0),
        ("Highveld Tech World Ltd", 520000.0, 550000.0, 600000.0, 700000.0, 840000.0, 350000.0, 370000.0, 410000.0, 480000.0, 580000.0),
        ("Karoo Motors Ltd", 850000.0, 900000.0, 980000.0, 1120000.0, 1350000.0, 600000.0, 640000.0, 700000.0, 800000.0, 960000.0),
        ("Table Mountain Books Ltd", 220000.0, 240000.0, 260000.0, 310000.0, 380000.0, 140000.0, 155000.0, 175000.0, 210000.0, 255000.0),
        ("Springbok Sports Mart Ltd", 410000.0, 435000.0, 475000.0, 560000.0, 680000.0, 270000.0, 290000.0, 325000.0, 380000.0, 460000.0),
        ("Limpopo Farm Supplies Ltd", 580000.0, 615000.0, 670000.0, 780000.0, 940000.0, 380000.0, 410000.0, 455000.0, 530000.0, 640000.0),
        ("Blyde Timber Merchants Ltd", 340000.0, 360000.0, 395000.0, 460000.0, 550000.0, 220000.0, 235000.0, 265000.0, 310000.0, 375000.0),
        ("Gauteng Health & Beauty Ltd", 650000.0, 690000.0, 750000.0, 880000.0, 1060000.0, 430000.0, 460000.0, 510000.0, 600000.0, 720000.0),
        ("Free State Grain Mart Ltd", 490000.0, 520000.0, 570000.0, 660000.0, 790000.0, 320000.0, 345000.0, 385000.0, 450000.0, 540000.0),
        ("Namaqua Diamond Jewelers Ltd", 780000.0, 830000.0, 910000.0, 1080000.0, 1300000.0, 520000.0, 555000.0, 620000.0, 730000.0, 880000.0),
        ("Outeniqua Garden World Ltd", 260000.0, 275000.0, 305000.0, 360000.0, 435000.0, 170000.0, 182000.0, 205000.0, 245000.0, 295000.0),
        ("Mpumalanga Tile Center Ltd", 620000.0, 660000.0, 725000.0, 850000.0, 1020000.0, 410000.0, 440000.0, 490000.0, 580000.0, 695000.0),
        ("Ezulwini Furnishing Ltd", 370000.0, 395000.0, 430000.0, 505000.0, 610000.0, 245000.0, 262000.0, 290000.0, 345000.0, 415000.0),
        ("Vaal Triangle Chem Ltd", 810000.0, 860000.0, 940000.0, 1100000.0, 1320000.0, 540000.0, 575000.0, 640000.0, 750000.0, 900000.0),
        ("Stellenbosch Wine Direct Ltd", 440000.0, 470000.0, 515000.0, 610000.0, 735000.0, 290000.0, 310000.0, 345000.0, 410000.0, 495000.0),
        ("Tshwane Auto Parts Ltd", 690000.0, 735000.0, 805000.0, 945000.0, 1140000.0, 460000.0, 492000.0, 545000.0, 640000.0, 775000.0),
        ("Richards Bay Tools Ltd", 540000.0, 575000.0, 630000.0, 740000.0, 890000.0, 360000.0, 385000.0, 425000.0, 500000.0, 605000.0),
        ("Polokwane Cash & Carry Ltd", 920000.0, 980000.0, 1070000.0, 1260000.0, 1510000.0, 620000.0, 660000.0, 730000.0, 860000.0, 1030000.0),
        ("Kimberley Mining Supply Ltd", 670000.0, 715000.0, 785000.0, 920000.0, 1105000.0, 450000.0, 480000.0, 530000.0, 625000.0, 750000.0),
        ("Durban Boutique Ltd", 390000.0, 415000.0, 455000.0, 535000.0, 645000.0, 260000.0, 278000.0, 308000.0, 365000.0, 440000.0),
        ("Rustenburg Industrial Tools Ltd", 880000.0, 935000.0, 1025000.0, 1210000.0, 1450000.0, 590000.0, 630000.0, 695000.0, 820000.0, 985000.0),
        ("Witbank Electrical Mart Ltd", 590000.0, 630000.0, 690000.0, 810000.0, 975000.0, 395000.0, 422000.0, 468000.0, 550000.0, 660000.0),
        ("Paarl Valley Produce Ltd", 480000.0, 510000.0, 560000.0, 655000.0, 790000.0, 320000.0, 342000.0, 378000.0, 445000.0, 535000.0),
        ("Midrand Computer Direct Ltd", 1020000.0, 1085000.0, 1190000.0, 1400000.0, 1680000.0, 680000.0, 725000.0, 805000.0, 950000.0, 1140000.0),
        ("Centurion Sports Emporium Ltd", 510000.0, 545000.0, 595000.0, 700000.0, 840000.0, 340000.0, 365000.0, 405000.0, 475000.0, 570000.0),
        ("Bloemfontein Meats Ltd", 760000.0, 810000.0, 890000.0, 1045000.0, 1260000.0, 510000.0, 545000.0, 605000.0, 710000.0, 855000.0),
        ("East London Marine Works Ltd", 430000.0, 460000.0, 505000.0, 590000.0, 710000.0, 285000.0, 308000.0, 342000.0, 400000.0, 482000.0),
        ("Klerksdorp Tile Direct Ltd", 640000.0, 680000.0, 750000.0, 880000.0, 1060000.0, 425000.0, 455000.0, 508000.0, 595000.0, 720000.0),
        ("Potchefstroom Stationery Hub Ltd", 310000.0, 330000.0, 365000.0, 430000.0, 515000.0, 205000.0, 220000.0, 246000.0, 290000.0, 350000.0),
        ("George Home Living Ltd", 570000.0, 605000.0, 665000.0, 780000.0, 940000.0, 380000.0, 405000.0, 450000.0, 530000.0, 640000.0),
        ("Secunda Safety & Industrial Ltd", 730000.0, 775000.0, 850000.0, 1000000.0, 1200000.0, 490000.0, 520000.0, 575000.0, 680000.0, 815000.0),
        ("Vereeniging Steel Goods Ltd", 950000.0, 1010000.0, 1110000.0, 1300000.0, 1560000.0, 640000.0, 680000.0, 750000.0, 885000.0, 1060000.0),
        ("Welkom Mine Supply Ltd", 790000.0, 840000.0, 920000.0, 1080000.0, 1300000.0, 530000.0, 565000.0, 625000.0, 735000.0, 885000.0),
        ("Bethlehem Grain Traders Ltd", 530000.0, 565000.0, 620000.0, 730000.0, 880000.0, 355000.0, 380000.0, 420000.0, 495000.0, 598000.0),
        ("Newcastle Tool Warehouse Ltd", 680000.0, 725000.0, 795000.0, 935000.0, 1125000.0, 455000.0, 488000.0, 540000.0, 635000.0, 765000.0),
        ("Mossel Bay Marine Traders Ltd", 460000.0, 490000.0, 540000.0, 635000.0, 765000.0, 310000.0, 330000.0, 365000.0, 430000.0, 520000.0),
        ("Mthatha Wholesale Hub Ltd", 550000.0, 585000.0, 645000.0, 760000.0, 915000.0, 370000.0, 395000.0, 438000.0, 515000.0, 620000.0),
        ("Upington Agro Direct Ltd", 420000.0, 450000.0, 495000.0, 580000.0, 700000.0, 280000.0, 302000.0, 335000.0, 395000.0, 475000.0),
        ("Vryheid Timber Depot Ltd", 630000.0, 670000.0, 740000.0, 870000.0, 1045000.0, 420000.0, 450000.0, 500000.0, 590000.0, 710000.0),
        ("Ladysmith Fashion Mart Ltd", 380000.0, 405000.0, 445000.0, 525000.0, 630000.0, 255000.0, 272000.0, 302000.0, 355000.0, 428000.0),
        ("Bredasdorp Grain Store Ltd", 590000.0, 630000.0, 695000.0, 815000.0, 980000.0, 395000.0, 425000.0, 470000.0, 555000.0, 665000.0),
        ("Cradock Livestock Hub Ltd", 510000.0, 545000.0, 600000.0, 705000.0, 850000.0, 340000.0, 368000.0, 408000.0, 480000.0, 578000.0),
        ("Makhanda Scholastic Supplies Ltd", 330000.0, 355000.0, 390000.0, 460000.0, 550000.0, 220000.0, 238000.0, 265000.0, 312000.0, 375000.0),
        ("Oudtshoorn Leathercraft Ltd", 470000.0, 500000.0, 550000.0, 645000.0, 775000.0, 315000.0, 338000.0, 372000.0, 438000.0, 525000.0),
        ("Knysna Marine Woods Ltd", 720000.0, 768000.0, 845000.0, 995000.0, 1195000.0, 485000.0, 518000.0, 575000.0, 675000.0, 810000.0)
    ]

    for co_m, aug_s, sep_s, oct_s, nov_s, dec_s, aug_p, sep_p, oct_p, nov_p, dec_p in budget_scenarios:
        # Debtors collection for November:
        # From November credit sales: 20% collected - 5% discount = 19% * nov_s
        # From October credit sales (30 days): 50% * oct_s
        # From September credit sales (60 days): 28% * sep_s
        col_nov_current = nov_s * 0.20 * 0.95
        col_nov_30 = oct_s * 0.50
        col_nov_60 = sep_s * 0.28
        tot_deb_nov = col_nov_current + col_nov_30 + col_nov_60

        # Debtors collection for December:
        col_dec_current = dec_s * 0.20 * 0.95
        col_dec_30 = nov_s * 0.50
        col_dec_60 = oct_s * 0.28
        tot_deb_dec = col_dec_current + col_dec_30 + col_dec_60

        # Creditors payment for November:
        # From October credit purchases (30 days): 70% paid subject to 2.5% discount -> 70% * 0.975 = 68.25%
        # From September credit purchases (60 days): 30% paid in full
        pay_cred_nov = (oct_p * 0.70 * 0.975) + (sep_p * 0.30)

        # Creditors payment for December:
        pay_cred_dec = (nov_p * 0.70 * 0.975) + (oct_p * 0.30)

        # Rent income escalation: Rent R25,000/month escalates by 8% on 1 November
        base_rent = 25000.0 + (oct_s * 0.02)
        esc_rent = base_rent * 1.08

        # Salaries escalation: Salaries R80,000/month increase by 7% on 1 December
        base_sal = 80000.0 + (oct_s * 0.08)
        inc_sal = base_sal * 1.07

        # 1. Medium Q: Cash Collected from Debtors in November
        if counts["medium"] < 500:
            c_dnov = f"R{tot_deb_nov:,.2f}"
            w_dnov = [
                f"R{nov_s * 0.20 + oct_s * 0.50 + sep_s * 0.28:,.2f} (omitted 5% discount on current month collections)",
                f"R{nov_s:,.2f} (assumed 100% of November sales collected)",
                f"R{col_nov_30 + col_nov_60:,.2f} (omitted collections from November sales)",
                f"R{tot_deb_nov * 1.15:,.2f}",
                f"R{tot_deb_nov * 0.85:,.2f}",
                f"R{(tot_deb_nov + 45000):,.2f}",
                f"R{(tot_deb_nov - 35000):,.2f}"
            ]
            q_dnov = (f"The Debtors Collection Policy of **{co_m}** reveals the following credit collection pattern:\n"
                      f"- 20% collected in the month of sale, subject to a 5% cash settlement discount\n"
                      f"- 50% collected in the month following the month of sale (30 days)\n"
                      f"- 28% collected in the second month following the sale (60 days)\n"
                      f"- 2% written off as irrecoverable bad debts in the third month\n"
                      f"Credit sales: September **R{sep_s:,.2f}**, October **R{oct_s:,.2f}**, November **R{nov_s:,.2f}**.\n"
                      f"Calculate the **total cash expected to be collected from debtors in November**:")
            exp_dnov = (f"November Debtors Collections:\n"
                        f"- From Nov sales: 20% of R{nov_s:,.2f} x 95% = R{col_nov_current:,.2f}\n"
                        f"- From Oct sales: 50% of R{oct_s:,.2f} = R{col_nov_30:,.2f}\n"
                        f"- From Sep sales: 28% of R{sep_s:,.2f} = R{col_nov_60:,.2f}\n"
                        f"Total Collections in November = R{col_nov_current:,.2f} + R{col_nov_30:,.2f} + R{col_nov_60:,.2f} = {c_dnov}.")
            add_q("medium", "Debtors Collection Schedule", q_dnov, c_dnov, w_dnov, "Applying", f"Calculate November debtors collection for {co_m}", exp_dnov)

        # 2. Medium Q: Cash Collected from Debtors in December
        if counts["medium"] < 500:
            c_ddec = f"R{tot_deb_dec:,.2f}"
            w_ddec = [
                f"R{dec_s * 0.20 + nov_s * 0.50 + oct_s * 0.28:,.2f} (omitted 5% discount on December sales)",
                f"R{dec_s:,.2f} (used December credit sales total)",
                f"R{col_dec_30 + col_dec_60:,.2f} (omitted current month collections)",
                f"R{tot_deb_dec * 1.15:,.2f}",
                f"R{tot_deb_dec * 0.85:,.2f}",
                f"R{(tot_deb_dec + 50000):,.2f}",
                f"R{(tot_deb_dec - 40000):,.2f}"
            ]
            q_ddec = (f"Referring to **{co_m}**: Credit sales are: October **R{oct_s:,.2f}**, November **R{nov_s:,.2f}**, December **R{dec_s:,.2f}**.\n"
                      f"Using the collection pattern (20% less 5% discount in month of sale, 50% after 30 days, 28% after 60 days), "
                      f"calculate the **total cash expected from debtors in December**:")
            exp_ddec = (f"December Debtors Collections:\n"
                        f"- From Dec sales: 20% of R{dec_s:,.2f} x 95% = R{col_dec_current:,.2f}\n"
                        f"- From Nov sales: 50% of R{nov_s:,.2f} = R{col_dec_30:,.2f}\n"
                        f"- From Oct sales: 28% of R{oct_s:,.2f} = R{col_dec_60:,.2f}\n"
                        f"Total Collections in December = R{col_dec_current:,.2f} + R{col_dec_30:,.2f} + R{col_dec_60:,.2f} = {c_ddec}.")
            add_q("medium", "Debtors Collection Schedule", q_ddec, c_ddec, w_ddec, "Applying", f"Calculate December debtors collection for {co_m}", exp_ddec)

        # 3. Medium Q: Discount Allowed on Debtors Collections in November
        disc_nov = nov_s * 0.20 * 0.05
        if counts["medium"] < 500:
            c_disc = f"R{disc_nov:,.2f}"
            w_disc = [
                f"R{nov_s * 0.05:,.2f} (calculated 5% on total November sales)",
                f"R{tot_deb_nov * 0.05:,.2f} (calculated 5% on total collections from all months)",
                f"R{disc_nov * 1.5:,.2f}",
                f"R{disc_nov * 0.5:,.2f}",
                f"R{(disc_nov + 5000):,.2f}",
                f"R{(disc_nov - 3000):,.2f}",
                f"R{nov_s * 0.02:,.2f}"
            ]
            q_disc = (f"In **{co_m}**, debtors who settle in the month of sale receive a **5% cash discount**. "
                      f"November credit sales are projected at **R{nov_s:,.2f}**, of which **20%** take advantage of the discount. "
                      f"Calculate the **Discount Allowed** for November to be reflected in the Projected Income Statement:")
            exp_disc = (f"Discount Allowed = Credit Sales x Early Settlement % x Discount %\n"
                        f"= R{nov_s:,.2f} x 20% x 5% = {c_disc}. "
                        f"This is an operating expense in the Projected Income Statement.")
            add_q("medium", "Debtors Collection Schedule", q_disc, c_disc, w_disc, "Applying", f"Calculate discount allowed for {co_m}", exp_disc)

        # 4. Medium Q: Bad Debts Written Off in December
        bad_debt_dec = sep_s * 0.02  # written off 3 months after September
        if counts["medium"] < 500:
            c_bd = f"R{bad_debt_dec:,.2f}"
            w_bd = [
                f"R{dec_s * 0.02:,.2f} (calculated 2% on December sales)",
                f"R{nov_s * 0.02:,.2f} (calculated 2% on November sales)",
                f"R{oct_s * 0.02:,.2f} (calculated 2% on October sales)",
                f"R{bad_debt_dec * 1.5:,.2f}",
                f"R{bad_debt_dec * 0.5:,.2f}",
                f"R{(bad_debt_dec + 4000):,.2f}",
                f"R{(bad_debt_dec - 2000):,.2f}"
            ]
            q_bd = (f"**{co_m}** writes off **2%** of credit sales as irrecoverable bad debts in the third month following the sale. "
                    f"Credit sales were: September **R{sep_s:,.2f}**, October **R{oct_s:,.2f}**, November **R{nov_s:,.2f}**, December **R{dec_s:,.2f}**. "
                    f"Calculate the **Bad Debts to be written off in December**:")
            exp_bd = (f"Bad Debts written off in December relate to credit sales made three months earlier (in September):\n"
                      f"= September Credit Sales x 2% = R{sep_s:,.2f} x 2% = {c_bd}. "
                      f"This appears in the Projected Income Statement but is omitted from the Cash Budget.")
            add_q("medium", "Debtors Collection Schedule", q_bd, c_bd, w_bd, "Applying", f"Calculate bad debts for {co_m}", exp_bd)

        # 5. Medium Q: Cash Paid to Creditors in November
        if counts["medium"] < 500:
            c_pnov = f"R{pay_cred_nov:,.2f}"
            w_pnov = [
                f"R{oct_p * 0.70 + sep_p * 0.30:,.2f} (omitted 2.5% discount on 30-day purchases)",
                f"R{nov_p:,.2f} (used November purchases total)",
                f"R{oct_p:,.2f} (used October purchases total)",
                f"R{pay_cred_nov * 1.15:,.2f}",
                f"R{pay_cred_nov * 0.85:,.2f}",
                f"R{(pay_cred_nov + 30000):,.2f}",
                f"R{(pay_cred_nov - 25000):,.2f}"
            ]
            q_pnov = (f"**{co_m}** settles creditors on the following terms:\n"
                      f"- 70% paid in the month following purchase (30 days), taking advantage of a 2.5% early payment discount\n"
                      f"- 30% paid in the second month following purchase (60 days)\n"
                      f"Credit purchases: September **R{sep_p:,.2f}**, October **R{oct_p:,.2f}**, November **R{nov_p:,.2f}**.\n"
                      f"Calculate the **total cash payments to creditors in November**:")
            exp_pnov = (f"November Payments to Creditors:\n"
                        f"- From Oct purchases: 70% of R{oct_p:,.2f} x 97.5% = R{oct_p * 0.70 * 0.975:,.2f}\n"
                        f"- From Sep purchases: 30% of R{sep_p:,.2f} = R{sep_p * 0.30:,.2f}\n"
                        f"Total Payments in November = R{oct_p * 0.70 * 0.975:,.2f} + R{sep_p * 0.30:,.2f} = {c_pnov}.")
            add_q("medium", "Creditors Payment Schedule", q_pnov, c_pnov, w_pnov, "Applying", f"Calculate November creditors payments for {co_m}", exp_pnov)

        # 6. Medium Q: Cash Paid to Creditors in December
        if counts["medium"] < 500:
            c_pdec = f"R{pay_cred_dec:,.2f}"
            w_pdec = [
                f"R{nov_p * 0.70 + oct_p * 0.30:,.2f} (omitted 2.5% discount)",
                f"R{dec_p:,.2f} (used December purchases)",
                f"R{nov_p:,.2f} (used November purchases)",
                f"R{pay_cred_dec * 1.15:,.2f}",
                f"R{pay_cred_dec * 0.85:,.2f}",
                f"R{(pay_cred_dec + 35000):,.2f}",
                f"R{(pay_cred_dec - 30000):,.2f}"
            ]
            q_pdec = (f"Referring to **{co_m}**: Credit purchases are: October **R{oct_p:,.2f}**, November **R{nov_p:,.2f}**, December **R{dec_p:,.2f}**.\n"
                      f"Creditors are paid: 70% in 30 days less 2.5% discount, and 30% in 60 days. "
                      f"Calculate the **total cash payments to creditors in December**:")
            exp_pdec = (f"December Payments to Creditors:\n"
                        f"- From Nov purchases: 70% of R{nov_p:,.2f} x 97.5% = R{nov_p * 0.70 * 0.975:,.2f}\n"
                        f"- From Oct purchases: 30% of R{oct_p:,.2f} = R{oct_p * 0.30:,.2f}\n"
                        f"Total Payments in December = R{nov_p * 0.70 * 0.975:,.2f} + R{oct_p * 0.30:,.2f} = {c_pdec}.")
            add_q("medium", "Creditors Payment Schedule", q_pdec, c_pdec, w_pdec, "Applying", f"Calculate December creditors payments for {co_m}", exp_pdec)

        # 7. Medium Q: Rent Income Escalation Calculation
        if counts["medium"] < 500:
            c_re = f"R{esc_rent:,.2f}"
            w_re = [
                f"R{base_rent:,.2f} (used unescalated rent)",
                f"R{base_rent * 1.16:,.2f} (applied double escalation)",
                f"R{esc_rent * 1.2:,.2f}",
                f"R{esc_rent * 0.8:,.2f}",
                f"R{(esc_rent + 5000):,.2f}",
                f"R{(esc_rent - 4000):,.2f}",
                f"R{base_rent + 800:,.2f}"
            ]
            q_re = (f"**{co_m}** sublets unused storeroom space at a rental of **R{base_rent:,.2f}** per month until 31 October. "
                    f"The lease agreement stipulates an **8% annual rental escalation** effective from **1 November**. "
                    f"Calculate the budgeted **Rent Income** for the month of **November** in the Cash Budget:")
            exp_re = f"Escalated Rent Income = Current Rent x 108% = R{base_rent:,.2f} x 1.08 = {c_re}."
            add_q("medium", "Rent Income Escalation", q_re, c_re, w_re, "Applying", f"Calculate escalated rent for {co_m}", exp_re)

        # 8. Medium Q: Salaries & Wages Increment Calculation
        if counts["medium"] < 500:
            c_sal = f"R{inc_sal:,.2f}"
            w_sal = [
                f"R{base_sal:,.2f} (omitted annual wage increment)",
                f"R{base_sal * 1.14:,.2f} (applied double increment)",
                f"R{inc_sal * 1.2:,.2f}",
                f"R{inc_sal * 0.8:,.2f}",
                f"R{(inc_sal + 12000):,.2f}",
                f"R{(inc_sal - 10000):,.2f}",
                f"R{base_sal + 7000:,.2f}"
            ]
            q_sal = (f"The monthly salaries and wages budget of **{co_m}** stands at **R{base_sal:,.2f}** up to 30 November. "
                     f"In accordance with the collective bargaining agreement, all staff receive a **7% salary increase** effective from **1 December**. "
                     f"Calculate the budgeted **Salaries and Wages** cash payment for the month of **December**:")
            exp_sal = f"Budgeted Salaries for December = Pre-increase Salaries x 107% = R{base_sal:,.2f} x 1.07 = {c_sal}."
            add_q("medium", "Salaries & Wages Budgeting", q_sal, c_sal, w_sal, "Applying", f"Calculate December salaries for {co_m}", exp_sal)

        # 9. Medium Q: Fixed Loan Repayment and Diminishing Interest
        loan_bal = 360000.0 + (oct_s * 0.5)
        monthly_repay = 15000.0
        annual_int_rate = 12.0  # 12% p.a.
        monthly_int = loan_bal * (annual_int_rate / 100) / 12
        tot_loan_pmt = monthly_repay + monthly_int
        if counts["medium"] < 500:
            c_lp = f"R{tot_loan_pmt:,.2f} (Principal: R{monthly_repay:,.2f}, Interest: R{monthly_int:,.2f})"
            w_lp = [
                f"R{monthly_repay:,.2f} (omitted loan interest: principal repayment only)",
                f"R{monthly_int:,.2f} (omitted principal loan repayment: interest only)",
                f"R{monthly_repay + (loan_bal * 0.12):,.2f} (added full annual interest in one month)",
                f"R{tot_loan_pmt * 1.2:,.2f}",
                f"R{tot_loan_pmt * 0.8:,.2f}",
                f"R{(tot_loan_pmt + 8000):,.2f}",
                f"R{(tot_loan_pmt - 6000):,.2f}"
            ]
            q_lp = (f"**{co_m}** has an outstanding commercial mortgage loan of **R{loan_bal:,.2f}** at **12% interest p.a.** on 1 November. "
                    f"The company repays **R{monthly_repay:,.2f}** of the capital loan principal at the end of each month, plus monthly interest. "
                    f"Calculate the **total cash payment for the loan (capital + interest)** in the November Cash Budget:")
            exp_lp = (f"Monthly Interest = Loan Balance x 12% / 12 months = R{loan_bal:,.2f} x 1% = R{monthly_int:,.2f}\n"
                      f"Total Loan Outflow = Capital Repayment (R{monthly_repay:,.2f}) + Interest (R{monthly_int:,.2f}) = {c_lp}.")
            add_q("medium", "Loan & Interest Repayments", q_lp, c_lp, w_lp, "Applying", f"Calculate loan payment for {co_m}", exp_lp)

        # 10. Medium Q: Cash Budget Net Cash Flow for November
        tot_rec_m = tot_deb_nov + (nov_s * 0.4) + esc_rent
        tot_pay_m = pay_cred_nov + (nov_p * 0.25) + base_sal + tot_loan_pmt
        net_flow_m = tot_rec_m - tot_pay_m
        if counts["medium"] < 500:
            c_nf = f"R{net_flow_m:,.2f} ({'Surplus' if net_flow_m >= 0 else 'Deficit'})"
            w_nf = [
                f"R{tot_rec_m:,.2f} (total receipts only)",
                f"R{tot_pay_m:,.2f} (total payments only)",
                f"R{-net_flow_m:,.2f} (inverted surplus and deficit)",
                f"R{net_flow_m * 1.2:,.2f}",
                f"R{net_flow_m * 0.8:,.2f}",
                f"R{(net_flow_m + 25000):,.2f}",
                f"R{(net_flow_m - 20000):,.2f}"
            ]
            q_nf = (f"The November Cash Budget summary of **{co_m}** reflects total budgeted cash receipts of **R{tot_rec_m:,.2f}** "
                    f"and total budgeted cash payments of **R{tot_pay_m:,.2f}**. Calculate the **Net Cash Flow** for November:")
            exp_nf = f"Net Cash Flow = Total Cash Receipts - Total Cash Payments = R{tot_rec_m:,.2f} - R{tot_pay_m:,.2f} = {c_nf}."
            add_q("medium", "Cash Budget Summary", q_nf, c_nf, w_nf, "Applying", f"Calculate net cash flow for {co_m}", exp_nf)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Variance Analysis (Budgeted vs Actual), Debtors Collection Period, Deficit Remedial Actions
    # =========================================================================

    variance_cases = [
        ("Protea Retailers Ltd", "Advertising", 45000.0, 78000.0, "Aggressive Black Friday radio and social media marketing campaign launched to counter a new competitor; sales grew by 28% as a result, justifying the overspending"),
        ("Kavango Emporium Ltd", "Delivery Vehicle Expenses", 32000.0, 54000.0, "Lack of driver supervision, personal use of delivery vans over weekends, and failure to service vehicles resulting in excessive fuel consumption and unplanned roadside repairs"),
        ("Algoa Furnishers Ltd", "Commission on Sales", 60000.0, 92000.0, "Actual sales exceeded budget by 53%; commission is paid at a fixed 5% of sales, so this is a favourable operational variance reflecting excellent sales performance"),
        ("Soweto Megastore Ltd", "Telephone & Internet", 18000.0, 36000.0, "Uncontrolled personal long-distance calls by clerical staff and unauthorized streaming on corporate uncapped fiber connections without administrative password restrictions"),
        ("Drakensberg Hardware Ltd", "Packing Materials", 25000.0, 44000.0, "Cashiers using double plastic shopping bags and giving uncharged bubble wrap to customers; high material wastage at checkout till points"),
        ("Zululand Wholesalers Ltd", "Maintenance of Equipment", 40000.0, 75000.0, "Major unbudgeted engine overhaul on forklift vehicles due to skipping scheduled 10,000 km preventative maintenance inspections"),
        ("Highveld Tech World Ltd", "Security Services", 28000.0, 48000.0, "Emergency deployment of armed response guards following a series of weekend burglary attempts at the retail shopping complex"),
        ("Karoo Motors Ltd", "Consumable Stores", 22000.0, 39000.0, "Workshop mechanics taking motor oil containers and cleaning sprays home due to unmonitored storehouse access and missing issue requisition slips"),
        ("Table Mountain Books Ltd", "Stationery & Printing", 15000.0, 27000.0, "Printing excessive color promotional brochures that were discarded after a single one-day weekend book fair"),
        ("Springbok Sports Mart Ltd", "Bank Overdraft Charges", 8000.0, 26000.0, "Severe cash flow mismanagement: debtors failed to pay on time, forcing the company to exceed its authorized bank overdraft limit and incur penal interest"),
        ("Limpopo Farm Supplies Ltd", "Water & Electricity", 35000.0, 58000.0, "Unrepaired underground irrigation pipe leaks and municipal tariff hikes of 18.5% that were omitted during annual budget preparation"),
        ("Blyde Timber Merchants Ltd", "Staff Training & Development", 30000.0, 12000.0, "Scheduled health and safety training workshops were cancelled due to heavy production deadlines, saving money short-term but exposing the firm to safety compliance risks"),
        ("Gauteng Health & Beauty Ltd", "Audit Fees", 65000.0, 95000.0, "Significant extra forensic audit testing required after internal auditors discovered unexplained inventory discrepancies in the central cosmetics storehouse"),
        ("Free State Grain Mart Ltd", "Insurance Premiums", 42000.0, 64000.0, "Underwriter increased premium by 50% following two consecutive roof hail damage claims that the risk committee did not anticipate in the budget"),
        ("Namaqua Diamond Jewelers Ltd", "Directors Fees", 120000.0, 180000.0, "Board approved unbudgeted special travel and committee sitting allowances for executive directors without obtaining prior shareholder advisory approval at the AGM"),
        ("Outeniqua Garden World Ltd", "Cleaning Materials", 12000.0, 23000.0, "Cleaners wasting industrial disinfectant concentrates by failing to dilute them with water in accordance with manufacturer instructions"),
        ("Mpumalanga Tile Center Ltd", "Bad Debts Written Off", 20000.0, 68000.0, "Credit manager granted R200,000 credit to two speculative property developers without conducting credit bureau checks or requiring personal surety bonds"),
        ("Ezulwini Furnishing Ltd", "Discount Allowed", 28000.0, 52000.0, "Sales staff offered unauthorized 10% cash settlement discounts to slow-paying debtors who were already 60 days overdue"),
        ("Vaal Triangle Chem Ltd", "Vehicle Fuel & Toll Fees", 55000.0, 96000.0, "Crude oil price surge combined with drivers taking circuitous non-toll bypass routes that added 45% extra mileage per delivery trip"),
        ("Stellenbosch Wine Direct Ltd", "Promotional Tastings & Samples", 38000.0, 71000.0, "Excessive wine bottles uncorked for informal VIP tastings without logging sample requisition vouchers"),
        ("Centurion Office Machines Ltd", "Courier & Freight Charges", 24000.0, 46000.0, "Using express courier overnight air delivery for routine stock orders that could have been transported by standard road freight at one-third of the cost"),
        ("Bloemfontein Grain Merchants Ltd", "Pest Fumigation Services", 36000.0, 62000.0, "Unbudgeted repeated fumigation required due to leaving warehouse loading bay doors open, allowing weevil infestations in grain storage"),
        ("East London Fishing Gear Ltd", "Temporary Casual Wages", 18000.0, 39000.0, "Hiring unauthorized casual labour over long weekends without checking permanent staff attendance or seeking prior branch manager approval"),
        ("Klerksdorp Mining Supplies Ltd", "Protective Clothing & Boots", 42000.0, 78000.0, "Workers claiming replacement boots every three months due to lack of a boot replacement register and failure to return damaged boots"),
        ("Potchefstroom Feeds Mart Ltd", "Forklift Fuel & Maintenance", 26000.0, 48000.0, "Forklifts left idling during staff lunch breaks and unauthorized weekend use moving private pallets"),
        ("George Hardwood Depot Ltd", "Saw Blade Sharpening & Consumables", 19000.0, 35000.0, "Blades dulled prematurely by running timber with embedded nails without using a handheld metal detector"),
        ("Secunda Safety Wear Ltd", "Trade Exhibition Costs", 50000.0, 92000.0, "Executive decision to upgrade to a premier double exhibition stand at the Gallagher Convention Centre without updating the marketing budget"),
        ("Vereeniging Boiler Supplies Ltd", "Water Heating & Gas", 34000.0, 61000.0, "Leaving industrial gas heaters on overnight in unoccupied workshop areas during winter"),
        ("Welkom Shaft Merchants Ltd", "Printing of Catalogs", 28000.0, 52000.0, "Ordering 10,000 full-colour printed product catalogs just three months before the product line was completely discontinued"),
        ("Bethlehem Farmers Coop Ltd", "Software License Upgrades", 45000.0, 79000.0, "Automated auto-renewal of unused cloud user licenses for former employees who left the company over six months ago"),
        ("Newcastle Heavy Hardware Ltd", "Legal Fees on Collections", 30000.0, 68000.0, "Legal litigation costs incurred handing over non-vetted credit customers who proved to have no attachable commercial assets"),
        ("Mossel Bay Fuel Traders Ltd", "Storage Tank Cleaning", 60000.0, 110000.0, "Emergency industrial vacuum tanker service required after sludge accumulated from delaying routine bi-annual drainage"),
        ("Mthatha Wholesale Hub Ltd", "Overtime Meal Allowances", 16000.0, 34000.0, "Cashiers claiming unverified meal vouchers for weekend inventory stocktaking shifts"),
        ("Upington Agro Direct Ltd", "Refrigeration Maintenance", 48000.0, 88000.0, "Cooling condenser coil rupture caused by dust buildup due to postponing scheduled quarterly filter washing"),
        ("Vryheid Timber Depot Ltd", "Loss on Damaged Merchandise", 22000.0, 47000.0, "Stacking timber pallets out in the open during heavy summer rainstorms without waterproof plastic tarp covers"),
        ("Ladysmith Fashion Mart Ltd", "Window Display Mannequins", 14000.0, 29000.0, "Purchasing imported European fashion mannequins at triple the budgeted cost of local SABS-approved display units"),
        ("Bredasdorp Grain Store Ltd", "Moisture Testing Equipment", 25000.0, 48000.0, "Replacing two electronic grain moisture meters dropped on concrete floors due to careless handling by seasonal staff"),
        ("Cradock Livestock Hub Ltd", "Livestock Tagging Supplies", 18000.0, 33000.0, "Ear tag applicator breakages and lost tags during unorganized farm auctions"),
        ("Makhanda Scholastic Supplies Ltd", "Textbook Sample Displays", 20000.0, 38000.0, "Distributing complimentary teacher textbook sample packs without logging school receipt confirmation forms"),
        ("Oudtshoorn Leathercraft Ltd", "Packaging Gift Boxes", 27000.0, 51000.0, "Upgrading packaging to luxury gold-foil embossed gift boxes without adjusting the retail mark-up percentage"),
        ("Knysna Marine Woods Ltd", "Yacht Varnish Brushes & Solvents", 15000.0, 31000.0, "Apprentice carpenters discarding expensive sable hair brushes after a single application instead of cleaning them in mineral turpentine"),
        ("Standerton Milking Systems Ltd", "Stainless Welding Gas", 28000.0, 52000.0, "Argon gas cylinder valve left slightly open over an entire long weekend in the fabrication workshop"),
        ("Harrismith Logistics Depot Ltd", "Fleet Tyre Replacements", 65000.0, 115000.0, "Poor wheel alignment on long-haul transport trucks accelerating tyre shoulder wear and blowout damage"),
        ("Kuruman Mineral Traders Ltd", "Core Sample Bags & Boxes", 22000.0, 41000.0, "Field geologists using heavy-duty mineral sample bags for packing general field camp groceries"),
        ("Thohoyandou Superstore Ltd", "Till Receipt Paper Rolls", 12000.0, 25000.0, "Cashiers printing double till slips and discarding uncollected customer copies into rubbish bins"),
        ("Plettenberg Bay Decor Ltd", "Showroom Air Conditioning", 32000.0, 59000.0, "Keeping showroom sliding glass doors wide open while running industrial air conditioners at minimum temperature"),
        ("Saldanha Marine Freight Ltd", "Harbour Tug Towage Fees", 85000.0, 145000.0, "Vessel arrival delays during rough sea swells requiring two additional standby tugs on hourly demurrage rates"),
        ("Grahamstown Scholastic Ltd", "Book Fair Exhibition Fees", 25000.0, 48000.0, "Upgrading booth space to premium mezzanine level without submitting an adjusted marketing budget"),
        ("Springbok Wind Parts Ltd", "Hydraulic Crane Rental", 70000.0, 125000.0, "Crane kept on site on standby for three extra days due to late arrival of specialized rotor hub bolts"),
        ("Witbank Coal Equipment Ltd", "Overtime Workshop Labour", 55000.0, 98000.0, "Unplanned overtime incurred on emergency excavator repairs because routine hydraulic oil testing was neglected"),
        ("Paarl Valley Beverages Ltd", "Bottling Plant Lubricants", 24000.0, 45000.0, "Excessive grease application by uncertified technicians causing lubricant spillage on conveyor floors"),
        ("Centurion Aerospace Parts Ltd", "Calibrated Gauge Recertification", 38000.0, 68000.0, "Emergency expedited SANAS laboratory calibration required after an uncertified torque wrench was dropped"),
        ("Bloemfontein Meats Wholesalers Ltd", "Cold Storage Power Consumption", 75000.0, 130000.0, "Leaving cold storage blast freezer curtains open during morning pallet loading, forcing compressors to run continuously"),
        ("East London Marine Spares Ltd", "Outboard Motor Testing Fuel", 16000.0, 32000.0, "Technicians running test engines for extended periods without logging engine test serial numbers"),
        ("Klerksdorp Building Center Ltd", "Forklift Hydraulic Hose Repairs", 20000.0, 39000.0, "Drivers dragging pallet forks along abrasive concrete yard surfaces, severing low-hanging hydraulic hoses")
    ]

    for co_v, exp_item, bud_amt, act_amt, expl_v in variance_cases:
        diff_amt = act_amt - bud_amt
        pct_diff = (diff_amt / bud_amt) * 100

        # 1. Hard Q: Calculate Variance Amount and Percentage
        if counts["hard"] < 200:
            c_var = f"R{diff_amt:,.2f} over budget ({pct_diff:.1f}% overspending)"
            w_var = [
                f"R{diff_amt:,.2f} under budget ({pct_diff:.1f}% saving)",
                f"R{bud_amt:,.2f} over budget",
                f"R{act_amt:,.2f} over budget",
                f"R{diff_amt * 1.2:,.2f} over budget",
                f"R{diff_amt * 0.8:,.2f} over budget",
                f"R{(diff_amt + 15000):,.2f} over budget",
                f"R{(diff_amt - 10000):,.2f} over budget"
            ]
            q_var = (f"The Budget Variance Report of **{co_v}** for the quarter indicates the following for **{exp_item}**:\n"
                     f"- Budgeted expenditure: **R{bud_amt:,.2f}**\n"
                     f"- Actual expenditure incurred: **R{act_amt:,.2f}**\n"
                     f"Calculate the **variance amount and percentage variance**:")
            exp_var = (f"Variance = Actual (R{act_amt:,.2f}) - Budget (R{bud_amt:,.2f}) = R{diff_amt:,.2f} overspent.\n"
                       f"Percentage Variance = (R{diff_amt:,.2f} / R{bud_amt:,.2f}) x 100 = {pct_diff:.1f}% over budget.")
            add_q("hard", "Variance Analysis (Budgeted vs Actual)", q_var, c_var, w_var, "Analyzing", f"Calculate variance for {exp_item} in {co_v}", exp_var)

        # 2. Hard Q: Evaluative Feedback & Internal Control Recommendation
        if counts["hard"] < 200:
            c_fdbk = f"Evaluation: {expl_v}. Management must enforce strict budget caps, review authorization thresholds, and require pre-approval for expenditure variances."
            w_fdbk = [
                "Disregard the variance because budget figures are purely decorative estimates that have no operational bearing",
                "Dismiss all accounting personnel immediately and cease preparing future quarterly budgets",
                "Double the selling price of merchandise to ensure all expense variances are absorbed by customers",
                "Transfer the variance to Trade Debtors to conceal the overspending from the external auditors",
                "Borrow R5 million on bank overdraft to cover all future expense overruns without investigation",
                "Eliminate all internal controls and allow department heads to spend company funds without receipts"
            ]
            q_fdbk = (f"Refer to the overspending on **{exp_item}** at **{co_v}** (budget R{bud_amt:,.2f} vs actual R{act_amt:,.2f}). "
                      f"Provide the most accurate professional evaluation and managerial recommendation under CAPS Cost Accounting:")
            exp_fdbk = f"Evaluation: **{c_fdbk}**."
            add_q("hard", "Variance Analysis (Budgeted vs Actual)", q_fdbk, c_fdbk, w_fdbk, "Evaluating", f"Evaluate variance for {exp_item} in {co_v}", exp_fdbk)

    # Debtors Collection Period & Credit Policy Evaluation (25 cases)
    debtors_eval_cases = [
        ("Protea Retailers Ltd", 480000.0, 3200000.0, 30, "Debtors Collection Period is 54.8 days, which exceeds the 30-day credit term by 24.8 days. The business is facing cash flow strain because credit control is ineffective. Measures: Charge interest on overdue accounts, stop credit sales to defaulting debtors, and enforce credit vetting."),
        ("Kavango Emporium Ltd", 650000.0, 4800000.0, 30, "Debtors Collection Period is 49.4 days vs 30 days allowed. Cash is trapped in debtors ledger. Management should offer a 5% early settlement discount and send automated SMS reminders at 21 days."),
        ("Algoa Furnishers Ltd", 520000.0, 3600000.0, 30, "Debtors Collection Period is 52.7 days. Debtors take nearly two months to pay, worsening bank overdraft fees. Action: Refuse further credit purchases until outstanding balances are cleared."),
        ("Soweto Megastore Ltd", 920000.0, 7200000.0, 30, "Debtors Collection Period is 46.6 days vs 30 days allowed. The firm should hire an external debt collection agency for accounts over 90 days and require credit bureau checks on all new accounts."),
        ("Drakensberg Hardware Ltd", 380000.0, 2400000.0, 30, "Debtors Collection Period is 57.8 days. Excessively slow collections endanger supplier payments. Recommendation: Enforce strict credit limits and require bank guarantees on accounts over R50,000."),
        ("Zululand Wholesalers Ltd", 1150000.0, 9500000.0, 30, "Debtors Collection Period is 44.2 days vs 30 days allowed. Liquidity is compromised. Action: Increase credit screening and reward prompt-paying customers with preferred delivery schedules."),
        ("Highveld Tech World Ltd", 780000.0, 5600000.0, 30, "Debtors Collection Period is 50.8 days. Credit policy is too lenient. Immediate remedial step: Charge prime + 2% interest on accounts overdue past 30 days."),
        ("Karoo Motors Ltd", 1250000.0, 8900000.0, 30, "Debtors Collection Period is 51.3 days. Working capital is locked up. Management must demand a 30% upfront cash deposit on all major component orders."),
        ("Table Mountain Books Ltd", 310000.0, 2200000.0, 30, "Debtors Collection Period is 51.4 days. Overdue accounts threaten cash flow. Action: Halt deliveries to bookstores with outstanding balances over 45 days."),
        ("Springbok Sports Mart Ltd", 590000.0, 4100000.0, 30, "Debtors Collection Period is 52.5 days vs 30-day terms. The company must implement monthly account statement reconciliations and telephonic debtor follow-ups."),
        ("Limpopo Farm Supplies Ltd", 840000.0, 5800000.0, 30, "Debtors Collection Period is 52.9 days. Slow collections during post-harvest months. Action: Negotiate seasonal repayment agreements linked to crop delivery dates."),
        ("Blyde Timber Merchants Ltd", 490000.0, 3400000.0, 30, "Debtors Collection Period is 52.6 days. Timber merchants are using the company as an interest-free bank. Remedial step: Hand over defaulting accounts for legal collection."),
        ("Gauteng Health & Beauty Ltd", 950000.0, 6800000.0, 30, "Debtors Collection Period is 51.0 days. High collection period leads to cash shortages. Action: Reduce credit terms from 30 days to 21 days for retail pharmacies."),
        ("Free State Grain Mart Ltd", 710000.0, 4900000.0, 30, "Debtors Collection Period is 52.9 days. Substantial working capital tied up. Strategy: Offer 2.5% discount for EFT payments made within 10 days of invoice."),
        ("Namaqua Diamond Jewelers Ltd", 1100000.0, 7800000.0, 30, "Debtors Collection Period is 51.5 days. High-value debtor defaults risk solvency. Action: Require credit card pre-authorization or bank irrevocable letters of credit."),
        ("Centurion Office Machines Ltd", 680000.0, 4900000.0, 30, "Debtors Collection Period is 50.6 days vs 30 days allowed. Cash is trapped in receivables. Management should introduce biometric signature verification on delivery notes and issue early settlement discounts."),
        ("Bloemfontein Grain Merchants Ltd", 890000.0, 6200000.0, 30, "Debtors Collection Period is 52.4 days. Overdue balances delay seasonal fertilizer purchases. Action: Stop further seed grain deliveries to farmers with balances exceeding 60 days."),
        ("East London Fishing Gear Ltd", 410000.0, 2800000.0, 30, "Debtors Collection Period is 53.4 days. Slow collections increase reliance on bank overdraft. Recommendation: Offer a 3% cash rebate for payments within 7 days."),
        ("Klerksdorp Mining Supplies Ltd", 1050000.0, 7400000.0, 30, "Debtors Collection Period is 51.8 days. Large engineering accounts taking 60+ days to settle. Action: Charge prime + 3% interest on all overdue invoices."),
        ("Potchefstroom Feeds Mart Ltd", 570000.0, 3900000.0, 30, "Debtors Collection Period is 53.3 days. Dairy cooperatives are delaying feed payments. Strategy: Tie credit limits strictly to monthly milk production output."),
        ("George Hardwood Depot Ltd", 720000.0, 5100000.0, 30, "Debtors Collection Period is 51.5 days. Builders delaying settlement until house completion. Action: Require milestone payments rather than 100% end-of-project credit."),
        ("Secunda Safety Wear Ltd", 830000.0, 5900000.0, 30, "Debtors Collection Period is 51.4 days. Mining contractor defaults causing working capital strain. Remedial step: Enforce credit insurance on accounts over R100,000."),
        ("Vereeniging Boiler Supplies Ltd", 1250000.0, 8800000.0, 30, "Debtors Collection Period is 51.8 days. Industrial accounts taking nearly two months. Action: Hire a dedicated credit controller to conduct weekly follow-up visits."),
        ("Welkom Shaft Merchants Ltd", 960000.0, 6700000.0, 30, "Debtors Collection Period is 52.3 days. Gold mine contractors taking excessive credit terms. Recommendation: Enforce mandatory 25% cash deposits on custom equipment orders."),
        ("Bethlehem Farmers Coop Ltd", 640000.0, 4500000.0, 30, "Debtors Collection Period is 51.9 days. Working capital locked in grain producer accounts. Strategy: Provide electronic bank debit order incentives."),
        ("Newcastle Heavy Hardware Ltd", 880000.0, 6100000.0, 30, "Debtors Collection Period is 52.6 days. Construction firms exceeding 30-day limits. Action: Place defaulting accounts on immediate credit stop."),
        ("Mossel Bay Fuel Traders Ltd", 1450000.0, 10500000.0, 30, "Debtors Collection Period is 50.4 days. Commercial shipping fleets taking extended payment terms. Remedial step: Require 50% cash deposit prior to fuel bunkering."),
        ("Mthatha Wholesale Hub Ltd", 620000.0, 4300000.0, 30, "Debtors Collection Period is 52.6 days. Rural trading stores delaying settlement until pension payout days. Strategy: Align credit cycles with regional government pension dates."),
        ("Upington Agro Direct Ltd", 540000.0, 3800000.0, 30, "Debtors Collection Period is 51.9 days. Vineyard owners delaying settlement until harvest export proceeds. Action: Require export crop lien agreements on overdue balances."),
        ("Vryheid Timber Depot Ltd", 780000.0, 5500000.0, 30, "Debtors Collection Period is 51.8 days. Building contractors taking over 50 days. Recommendation: Offer 2% settlement discount within 14 days and halt deliveries on defaulted accounts."),
        ("Ladysmith Fashion Mart Ltd", 460000.0, 3200000.0, 30, "Debtors Collection Period is 52.4 days. Boutique accounts taking nearly two months. Action: Shift retail boutiques to credit card transactions rather than open book credit."),
        ("Bredasdorp Grain Store Ltd", 710000.0, 5000000.0, 30, "Debtors Collection Period is 51.8 days. Agricultural cooperatives taking extended terms. Strategy: Enforce monthly interest charges at prime plus 2.5%."),
        ("Cradock Livestock Hub Ltd", 630000.0, 4400000.0, 30, "Debtors Collection Period is 52.3 days. Farmers delaying livestock feed payments. Action: Demand collateral surety or livestock auction settlement guarantees."),
        ("Makhanda Scholastic Supplies Ltd", 380000.0, 2700000.0, 30, "Debtors Collection Period is 51.4 days. Private school governing bodies delaying payments. Recommendation: Enforce termly pre-payment policies."),
        ("Oudtshoorn Leathercraft Ltd", 590000.0, 4100000.0, 30, "Debtors Collection Period is 52.5 days. Souvenir retailers delaying payments during tourism low season. Action: Require 30-day post-dated cheques upon merchandise dispatch."),
        ("Knysna Marine Woods Ltd", 840000.0, 5900000.0, 30, "Debtors Collection Period is 52.0 days. Boat builders taking nearly two months. Recommendation: Halt timber shipments to boat builders with balances over 45 days."),
        ("Standerton Milking Systems Ltd", 670000.0, 4700000.0, 30, "Debtors Collection Period is 52.0 days. Dairy farms delaying equipment service payments. Strategy: Offer automated monthly debit order discounts of 2.5%.")
    ]

    for co_db, avg_deb, cr_sales_yr, term_days, eval_db in debtors_eval_cases:
        dcp_val = (avg_deb / cr_sales_yr) * 365

        # 1. Hard Q: Calculate Debtors Collection Period in Days
        if counts["hard"] < 200:
            c_dcp = f"{dcp_val:.1f} days"
            w_dcp = [
                f"{dcp_val * 1.5:.1f} days",
                f"{dcp_val * 0.5:.1f} days",
                f"{(avg_deb / cr_sales_yr) * 30:.1f} days (multiplied by 30 days instead of 365)",
                f"{term_days:.1f} days (stated credit term rather than actual period)",
                f"{dcp_val + 15.0:.1f} days",
                f"{dcp_val - 12.0:.1f} days",
                f"{(cr_sales_yr / avg_deb):.1f} days (calculated debtors turnover rate instead of collection period)"
            ]
            q_dcp = (f"The records of **{co_db}** reflect average Debtors of **R{avg_deb:,.2f}** and Total Credit Sales of **R{cr_sales_yr:,.2f}** for the year. "
                     f"The official credit terms granted to customers are **{term_days} days**. "
                     f"Calculate the **Debtors Collection Period** (in days, rounded to one decimal place):")
            exp_dcp = (f"Debtors Collection Period = (Average Debtors / Total Credit Sales) x 365\n"
                       f"= (R{avg_deb:,.2f} / R{cr_sales_yr:,.2f}) x 365 = {c_dcp}.")
            add_q("hard", "Debtors Collection Period Analysis", q_dcp, c_dcp, w_dcp, "Applying", f"Calculate debtors collection period for {co_db}", exp_dcp)

        # 2. Hard Q: Professional Evaluation of Debtors Collection Performance
        if counts["hard"] < 200:
            c_ev_db = eval_db
            w_ev_db = [
                "Exceptional performance: Debtors taking longer to pay proves customer loyalty and satisfaction",
                "Neutral: The collection period has zero impact on company bank liquidity or bad debt risks",
                "The business should immediately cancel all cash sales and sell merchandise 100% on credit",
                "The credit manager should be rewarded with a 50% bonus for keeping money in debtors accounts",
                "Credit terms should be extended to 180 days to encourage debtors to delay payment even further",
                "Debtors collection periods cannot be evaluated without knowing the authorized share capital"
            ]
            q_ev_db = (f"Evaluate the **Debtors Collection Period** of **{co_db}** ({dcp_val:.1f} days vs {term_days}-day terms) "
                       f"and recommend appropriate internal control strategies:")
            exp_ev_db = f"Evaluation: **{c_ev_db}**."
            add_q("hard", "Debtors Collection Period Analysis", q_ev_db, c_ev_db, w_ev_db, "Evaluating", f"Evaluate debtors collection for {co_db}", exp_ev_db)

    # Remedial Strategies for Cash Deficits (15 cases)
    deficit_cases = [
        ("Protea Retailers Ltd", 240000.0, "Postpone non-essential capital equipment purchases, negotiate 60-day terms with suppliers, tighten credit vetting to accelerate debtor collections, and arrange a temporary pre-approved bank overdraft"),
        ("Kavango Emporium Ltd", 380000.0, "Offer a 5% discount for immediate cash settlements, postpone vehicle fleet upgrades, reduce inventory purchase order quantities, and request an extension on the mortgage loan repayment"),
        ("Algoa Furnishers Ltd", 195000.0, "Lease delivery trucks instead of purchasing for cash, introduce strict credit limits, require 20% deposits on custom orders, and curtail executive travel expenses"),
        ("Soweto Megastore Ltd", 450000.0, "Conduct a weekend promotional clearance sale of slow-moving inventory for cash, negotiate a 30-day payment extension with primary creditors, and postpone planned storehouse extensions"),
        ("Highveld Tech World Ltd", 290000.0, "Tighten debtor credit control by charging 2% monthly interest on overdue accounts, halt credit sales to defaulting debtors, and request a temporary increase in overdraft facility"),
        ("Karoo Motors Ltd", 340000.0, "Delay purchase of showroom diagnostic machinery, negotiate 60-day settlement terms with parts importers, and require cash deposits on custom imports"),
        ("Table Mountain Books Ltd", 160000.0, "Hold a cash-only warehouse clearance sale of older book editions and negotiate deferred payment on wholesale publisher invoices"),
        ("Springbok Sports Mart Ltd", 275000.0, "Cancel unessential corporate sponsorship events, accelerate debtor collections through a 5% discount, and postpone store lighting renovations"),
        ("Limpopo Farm Supplies Ltd", 360000.0, "Negotiate structured seasonal repayment terms with major chemical suppliers and offer 3% rebates for farmers paying by EFT upon delivery"),
        ("Blyde Timber Merchants Ltd", 220000.0, "Postpone the cash purchase of a new timber delivery crane and request an increase in temporary working capital overdraft facility"),
        ("Gauteng Health & Beauty Ltd", 410000.0, "Return slow-moving salon equipment to suppliers under consignment clauses and reduce administrative staff overtime hours"),
        ("Free State Grain Mart Ltd", 280000.0, "Accelerate debtor collections by calling in overdue farmer accounts and postpone capital investments in new grain elevators"),
        ("Namaqua Diamond Jewelers Ltd", 520000.0, "Hold an invitation-only private cash sale of antique jewelry collections and defer director travel bonuses until liquidity improves"),
        ("Outeniqua Garden World Ltd", 145000.0, "Lease commercial landscaping equipment instead of purchasing outright and negotiate extended payment terms with seedling nurseries"),
        ("Mpumalanga Tile Center Ltd", 330000.0, "Sell surplus slow-moving ceramic tile stock at cost price for immediate cash and delay new warehouse tile rack installations"),
        ("Newcastle Tool Warehouse Ltd", 285000.0, "Offer a 7.5% cash discount for all overdue trade debtor accounts settled within five days and defer corporate vehicle fleet upgrades"),
        ("Mossel Bay Fuel Traders Ltd", 490000.0, "Arrange a temporary revolving commercial bank trade credit line and postpone scheduled non-essential office renovations"),
        ("Polokwane Cash & Carry Ltd", 360000.0, "Negotiate 45-day credit terms with food manufacturers and hold an emergency clearance sale of bulk canned goods for cash only")
    ]

    for co_df, def_amt, sol_df in deficit_cases:
        if counts["hard"] < 200:
            c_sol = sol_df
            w_sol = [
                "Declare immediate corporate bankruptcy and auction off all inventory for 5% of cost",
                "Stop paying factory and store employee wages for three consecutive months without notice",
                "Alter cash receipts journal entries to falsely show R1 million in non-existent cash sales",
                "Borrow money from unregistered loan sharks at 50% monthly compound interest",
                "Cease keeping accounting records until the bank account returns to a positive balance",
                "Dismiss the external auditors and conceal all financial statements from company directors"
            ]
            q_sol = (f"The Cash Budget of **{co_df}** projects an alarming **cash deficit of R{def_amt:,.2f}** at the end of next month. "
                     f"Which set of remedial management actions represents the most responsible, effective strategy to resolve this cash crisis?")
            exp_sol = f"Strategy: **{c_sol}**. Proactive cash management is essential to prevent business failure."
            add_q("hard", "Cash Deficit Remedial Strategies", q_sol, c_sol, w_sol, "Evaluating", f"Cash deficit strategy for {co_df}", exp_sol)

    print(f"Generated: easy={counts['easy']}, medium={counts['medium']}, hard={counts['hard']}")

    output_path = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting/paper2_acc_budgeting.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"SUCCESS: {output_path} created with {len(questions)} questions: {counts}")

if __name__ == "__main__":
    build_budgeting()
