import json
import os

def build_cash_flow():
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
        qid = f"ACC_P1_CF_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Cash Flow Statement",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Cash Flow Statement",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Purpose of Cash Flow, Three Main Activities, Cash & Cash Equivalents, Direct Changes
    # =========================================================================

    core_concepts = [
        ("Purpose of the Cash Flow Statement",
         "To provide information about the actual cash inflows and cash outflows of an enterprise over a financial period, categorized into operating, investing, and financing activities, enabling users to evaluate the company's liquidity, solvency, and ability to generate future cash flows.",
         ["To calculate the taxable net profit for the year on an accrual basis",
          "To list the physical inventory items stored in the warehouse at cost price",
          "To determine the replacement market value of non-current tangible assets",
          "To record the personal drawings and salary advances of the managing director",
          "To reconcile credit customer accounts with the monthly sales journal",
          "To calculate the total depreciation expense for the next ten financial years"],
         "The Cash Flow Statement reports historical cash movements to assess liquidity and financial viability."),

        ("Why a Profitable Company Can Face Liquidity Crisis (Cash vs Profit)",
         "Profit is calculated on the accrual basis (including credit sales not yet collected and deducting non-cash expenses like depreciation), whereas cash flow reflects actual liquid funds; a company may report high paper profits while its cash is trapped in uncollected debtors or slow-moving inventory, leaving it unable to pay immediate debts.",
         ["Profit and cash flow are always mathematically identical in corporate accounting",
          "Companies are legally forbidden from paying debts if they make a positive profit",
          "Profits are immediately transferred to the Department of Basic Education as tax",
          "Banks automatically seize all cash balances as soon as a company reports profit",
          "Profits only exist if the company has zero non-current liabilities",
          "Cash flow is measured exclusively by the physical weight of inventory in the store"],
         "Profit differs from cash due to credit transactions and non-cash items; profits tied up in working capital cause cash crises."),

        ("Operating Activities",
         "Cash flows derived from the principal revenue-generating operations and day-to-day trading activities of the business (e.g. cash generated from operations, interest paid, taxation paid, and dividends paid).",
         ["Cash spent on purchasing delivery vehicles and manufacturing equipment",
          "Cash received from issuing new ordinary shares to the general public",
          "Cash proceeds received from raising a mortgage loan from a commercial bank",
          "Cash outflows used to repurchase company shares above the average issue price",
          "Cash paid to acquire long-term government bonds and fixed deposits",
          "Cash received from selling company land and office buildings"],
         "Operating activities encompass the core trading cycle and statutory tax/dividend payments."),

        ("Investing Activities",
         "Cash flows resulting from the acquisition and disposal of long-term non-current assets (such as land, buildings, equipment, and vehicles) as well as long-term financial investments (fixed deposits).",
         ["Cash received from daily cash sales and customer account payments",
          "Cash paid to SARS for provisional and annual company income tax",
          "Cash paid to suppliers for monthly deliveries of trading stock",
          "Cash outflows for monthly salaries, wages, and factory electricity",
          "Cash received from taking out a five-year bank loan facility",
          "Cash paid as interim dividends to registered company shareholders"],
         "Investing activities reflect capital investments in and disposals of long-term productive assets."),

        ("Financing Activities",
         "Cash flows that result in changes in the size and composition of the contributed equity capital and borrowings of the enterprise (e.g. proceeds from issuing shares, share buybacks, and borrowing or repaying long-term loans).",
         ["Cash received from renting out surplus office space to commercial tenants",
          "Cash paid to repair and service factory delivery vehicles",
          "Cash spent on purchasing consumable office stationery and tea supplies",
          "Cash paid to external auditors for conducting the statutory annual audit",
          "Cash generated from customer collections in the debtors schedule",
          "Cash spent on purchasing specialized production machinery for the factory"],
         "Financing activities involve equity capital and long-term debt transactions."),

        ("Cash and Cash Equivalents Components",
         "Comprises highly liquid short-term financial holdings: positive bank current account balances, petty cash floats, cash on hand in till registers, and short-term fixed deposits maturing within 3 months, less short-term bank overdrafts.",
         ["Comprises heavy industrial machinery, land, and factory buildings",
          "Comprises trading inventory, raw materials, and work-in-progress stock",
          "Comprises trade debtors, prepayments, and accrued commission income",
          "Comprises long-term mortgage loans repayable over twenty years",
          "Comprises authorized ordinary share capital not yet issued to investors",
          "Comprises intangible assets such as patents, goodwill, and trademarks"],
         "Cash and cash equivalents are short-term, highly liquid holdings ready for immediate use.")
    ]

    for cc_title, cc_corr, cc_wrongs, cc_expl in core_concepts:
        for st_cc in [
            f"In Grade 12 Accounting, what is the official definition and significance of **'{cc_title}'**?",
            f"Under CAPS curriculum standards, which statement accurately explains **'{cc_title}'**?",
            f"In the analysis of company financial performance, **'{cc_title}'** refers to:",
            f"Which evaluation correctly describes **'{cc_title}'** on the Cash Flow Statement?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Cash Flow Concepts", st_cc, cc_corr, cc_wrongs, "Remembering", f"Define {cc_title}", cc_expl)

    # Activity Classification of Specific Transactions (Easy)
    transaction_classifications = [
        ("Proceeds from the issue of 100,000 ordinary shares", "Cash Flow from Financing Activities (Inflow)"),
        ("Repurchase of 50,000 shares from a retired shareholder", "Cash Flow from Financing Activities (Outflow)"),
        ("Repayment of R200,000 on the mortgage loan", "Cash Flow from Financing Activities (Outflow)"),
        ("Raising a new long-term bank loan of R500,000", "Cash Flow from Financing Activities (Inflow)"),
        ("Purchase of a new delivery truck for R450,000", "Cash Flow from Investing Activities (Outflow)"),
        ("Proceeds from the sale of an old office copier for R35,000", "Cash Flow from Investing Activities (Inflow)"),
        ("Erection of a new factory warehouse extension for R1,200,000", "Cash Flow from Investing Activities (Outflow)"),
        ("Maturity and cashing in of a 2-year fixed deposit of R300,000", "Cash Flow from Investing Activities (Inflow)"),
        ("Payment of provisional company income tax to SARS", "Cash Flow from Operating Activities (Outflow)"),
        ("Payment of interim dividends to shareholders", "Cash Flow from Operating Activities (Outflow)"),
        ("Payment of interest on a mortgage bond", "Cash Flow from Operating Activities (Outflow)"),
        ("Cash generated from customers and operations", "Cash Flow from Operating Activities (Inflow)"),
        ("Increase in the fixed deposit held at Nedbank", "Cash Flow from Investing Activities (Outflow)"),
        ("Payment of final dividends declared in the previous financial year", "Cash Flow from Operating Activities (Outflow)")
    ]

    for tx_desc, tx_class in transaction_classifications:
        for st_tx in [
            f"How is the transaction **'{tx_desc}'** classified on the Cash Flow Statement?",
            f"In which section of the Cash Flow Statement does **'{tx_desc}'** appear?",
            f"Identify the correct cash flow categorization for: **'{tx_desc}'**"
        ]:
            if counts["easy"] >= 300:
                break
            w_tx = [
                f"{'Cash Flow from Investing Activities' if 'Financing' in tx_class or 'Operating' in tx_class else 'Cash Flow from Financing Activities'} (Outflow)",
                f"{'Cash Flow from Operating Activities' if 'Investing' in tx_class or 'Financing' in tx_class else 'Cash Flow from Investing Activities'} (Inflow)",
                "Non-Cash Adjustment: Excluded completely from the Cash Flow Statement",
                "Retained Income Note item: Deducted directly from opening accumulated reserves",
                "Trading Account deduction: Subtracted from Gross Cost of Sales",
                "Contingent Liability: Disclosed only as an unquantified audit footnote"
            ]
            expl_tx = f"'{tx_desc}' is classified under {tx_class}."
            add_q("easy", "Transaction Classification", st_tx, tx_class, w_tx, "Understanding", f"Classify {tx_desc[:30]}", expl_tx)

    # Net Change in Cash and Cash Equivalents Calculations (Easy)
    cash_eq_scenarios = [
        ("Laysano Ltd", 125000.0, 310000.0, 5000.0, 8000.0),
        ("Protea Hardware Ltd", 240000.0, 480000.0, 10000.0, 15000.0),
        ("Zulu Fashion Ltd", 95000.0, 160000.0, 3000.0, 5000.0),
        ("Metro Tech Ltd", 410000.0, 690000.0, 12000.0, 20000.0),
        ("Apex Auto Ltd", 180000.0, 275000.0, 6000.0, 10000.0),
        ("Kairo Furnishers Ltd", 290000.0, 430000.0, 8000.0, 12000.0),
        ("Orchid Boutique Ltd", 85000.0, 140000.0, 4000.0, 6000.0),
        ("Galaxy Appliances Ltd", 520000.0, 850000.0, 15000.0, 25000.0),
        ("Bakersfield Ltd", 160000.0, 295000.0, 5000.0, 9000.0),
        ("Tshwane Traders Ltd", 140000.0, 230000.0, 6000.0, 8000.0),
        ("Cape Coast Ltd", 175000.0, 320000.0, 7000.0, 11000.0),
        ("Durban Wholesale Ltd", 360000.0, 580000.0, 14000.0, 18000.0),
        ("Sandton Goods Ltd", 450000.0, 780000.0, 16000.0, 22000.0),
        ("Bloemfontein Traders Ltd", 190000.0, 310000.0, 8000.0, 12000.0),
        ("Polokwane Supply Ltd", 130000.0, 215000.0, 5000.0, 7000.0),
        ("Nelspruit Supply Ltd", 115000.0, 195000.0, 4000.0, 6000.0),
        ("Kimberley Tools Ltd", 220000.0, 370000.0, 9000.0, 14000.0),
        ("Rustenburg Industrial Ltd", 310000.0, 540000.0, 11000.0, 17000.0),
        ("Port Elizabeth Logistics Ltd", 380000.0, 620000.0, 13000.0, 19000.0),
        ("Pietermaritzburg Ltd", 155000.0, 260000.0, 6000.0, 9000.0)
    ]

    for co_c, open_b, close_b, open_p, close_p in cash_eq_scenarios:
        tot_open = open_b + open_p
        tot_close = close_b + close_p
        net_change = tot_close - tot_open

        # 1. Net change in cash and cash equivalents
        if counts["easy"] < 300:
            c_nc = f"Net Increase of R{net_change:,.0f}" if net_change > 0 else f"Net Decrease of R{abs(net_change):,.0f}"
            w_nc = [
                f"Net Decrease of R{net_change:,.0f}" if net_change > 0 else f"Net Increase of R{abs(net_change):,.0f}",
                f"Net Increase of R{tot_close:,.0f} (confused closing balance with net change)",
                f"Net Increase of R{tot_open:,.0f} (confused opening balance with net change)",
                f"Net Increase of R{net_change * 1.5:,.0f}",
                f"Net Increase of R{net_change / 2:,.0f}",
                f"Net Increase of R{tot_close + tot_open:,.0f}",
                f"Net Increase of R{close_b - open_b:,.0f} (forgot petty cash float)"
            ]
            q_nc = (f"The records of **{co_c}** reflect the following cash balances: At beginning of year: Bank **R{open_b:,.0f}**, "
                    f"Petty Cash **R{open_p:,.0f}**; At end of year: Bank **R{close_b:,.0f}**, Petty Cash **R{close_p:,.0f}**. "
                    f"Calculate the **Net Change in Cash and Cash Equivalents** for the year:")
            exp_nc = (f"1. Total opening cash: R{open_b:,.0f} + R{open_p:,.0f} = R{tot_open:,.0f}. "
                      f"2. Total closing cash: R{close_b:,.0f} + R{close_p:,.0f} = R{tot_close:,.0f}. "
                      f"3. Net change = R{tot_close:,.0f} - R{tot_open:,.0f} = {c_nc}.")
            add_q("easy", "Cash Equivalents Calculations", q_nc, c_nc, w_nc, "Applying", f"Calculate Net Change in Cash for {co_c}", exp_nc)

    # Three-Activity Summation: Net Change = Operating + Investing + Financing (Easy)
    activity_totals = [
        ("Laysano Ltd", 850000.0, -420000.0, -180000.0),
        ("Protea Hardware Ltd", 1200000.0, -650000.0, -250000.0),
        ("Zulu Fashion Ltd", 540000.0, -280000.0, -110000.0),
        ("Metro Tech Ltd", 1650000.0, -980000.0, -320000.0),
        ("Apex Auto Ltd", 720000.0, -410000.0, -150000.0),
        ("Kairo Furnishers Ltd", 980000.0, -560000.0, -220000.0),
        ("Orchid Boutique Ltd", 380000.0, -210000.0, -85000.0),
        ("Galaxy Appliances Ltd", 1950000.0, -1100000.0, -450000.0),
        ("Bakersfield Ltd", 680000.0, -390000.0, -140000.0),
        ("Tshwane Traders Ltd", 610000.0, -340000.0, -130000.0),
        ("Cape Coast Ltd", 750000.0, -420000.0, -160000.0),
        ("Durban Wholesale Ltd", 1420000.0, -810000.0, -290000.0),
        ("Sandton Goods Ltd", 1850000.0, -1050000.0, -380000.0),
        ("Bloemfontein Traders Ltd", 780000.0, -440000.0, -170000.0),
        ("Polokwane Supply Ltd", 520000.0, -290000.0, -120000.0),
        ("Nelspruit Supply Ltd", 640000.0, -360000.0, -145000.0),
        ("Kimberley Tools Ltd", 890000.0, -510000.0, -210000.0),
        ("Rustenburg Industrial Ltd", 1350000.0, -780000.0, -310000.0),
        ("Port Elizabeth Logistics Ltd", 1520000.0, -890000.0, -350000.0),
        ("Pietermaritzburg Ltd", 710000.0, -410000.0, -165000.0),
        ("Soweto Commercial Ltd", 940000.0, -530000.0, -215000.0),
        ("Midrand Tech Ltd", 2100000.0, -1250000.0, -490000.0),
        ("Centurion Sports Ltd", 580000.0, -320000.0, -135000.0),
        ("East London Timber Ltd", 820000.0, -470000.0, -190000.0),
        ("Stellenbosch Cellars Ltd", 1150000.0, -660000.0, -270000.0),
        ("Upington Sun Ltd", 490000.0, -275000.0, -115000.0),
        ("Witbank Coal Supplies Ltd", 1680000.0, -970000.0, -390000.0),
        ("Paarl Agro Ltd", 760000.0, -430000.0, -175000.0),
        ("Potchefstroom Traders Ltd", 630000.0, -355000.0, -145000.0),
        ("George Coastal Ltd", 840000.0, -485000.0, -195000.0)
    ]

    for co_act, op_f, inv_f, fin_f in activity_totals:
        if counts["easy"] < 300:
            net_act = op_f + inv_f + fin_f
            c_act = f"Net Increase of R{net_act:,.0f}" if net_act > 0 else f"Net Decrease of R{abs(net_act):,.0f}"
            w_act = [
                f"Net Increase of R{op_f:,.0f} (ignored investing and financing flows)",
                f"Net Increase of R{op_f + abs(inv_f) + abs(fin_f):,.0f} (added outflows instead of subtracting)",
                f"Net Decrease of R{net_act:,.0f}" if net_act > 0 else f"Net Increase of R{abs(net_act):,.0f}",
                f"Net Increase of R{net_act * 1.5:,.0f}",
                f"Net Increase of R{net_act / 2:,.0f}",
                f"Net Increase of R{abs(inv_f) + abs(fin_f):,.0f}",
                f"Net Increase of R{net_act + 50000:,.0f}"
            ]
            q_act = (f"The completed sections of the Cash Flow Statement for **{co_act}** reflect: "
                     f"Cash flow from operating activities: **R{op_f:,.0f}**; "
                     f"Cash flow from investing activities: **(R{abs(inv_f):,.0f})**; "
                     f"Cash flow from financing activities: **(R{abs(fin_f):,.0f})**. "
                     f"Calculate the resulting **Net Change in Cash and Cash Equivalents**:")
            exp_act = f"Net Change = Operating (R{op_f:,.0f}) + Investing ((R{abs(inv_f):,.0f})) + Financing ((R{abs(fin_f):,.0f})) = {c_act}."
            add_q("easy", "Cash Flow Summation", q_act, c_act, w_act, "Applying", f"Calculate Net Change for {co_act}", exp_act)

    # Bank Overdraft Impact on Cash & Cash Equivalents (Easy)
    overdraft_scenarios = [
        ("Laysano Ltd", -45000.0, 5000.0, 3000.0),
        ("Protea Hardware Ltd", -82000.0, 8000.0, 4000.0),
        ("Zulu Fashion Ltd", -28000.0, 3000.0, 2000.0),
        ("Metro Tech Ltd", -120000.0, 15000.0, 8000.0),
        ("Apex Auto Ltd", -52000.0, 6000.0, 3500.0),
        ("Kairo Furnishers Ltd", -64000.0, 7500.0, 4500.0),
        ("Orchid Boutique Ltd", -18000.0, 2500.0, 1500.0),
        ("Galaxy Appliances Ltd", -150000.0, 18000.0, 9000.0),
        ("Bakersfield Ltd", -42000.0, 5000.0, 3000.0),
        ("Tshwane Traders Ltd", -38000.0, 4500.0, 2500.0),
        ("Cape Coast Ltd", -49000.0, 6000.0, 3000.0),
        ("Durban Wholesale Ltd", -95000.0, 12000.0, 6000.0),
        ("Sandton Goods Ltd", -110000.0, 14000.0, 7000.0),
        ("Bloemfontein Traders Ltd", -35000.0, 4000.0, 2000.0),
        ("Polokwane Supply Ltd", -25000.0, 3000.0, 1800.0),
        ("Nelspruit Supply Ltd", -31000.0, 3500.0, 2200.0),
        ("Kimberley Tools Ltd", -58000.0, 7000.0, 3800.0),
        ("Rustenburg Industrial Ltd", -76000.0, 9000.0, 4600.0),
        ("Port Elizabeth Logistics Ltd", -88000.0, 10500.0, 5200.0),
        ("Pietermaritzburg Ltd", -39000.0, 4200.0, 2100.0)
    ]

    for co_od, b_od, p_od, f_od in overdraft_scenarios:
        if counts["easy"] < 300:
            net_cce = b_od + p_od + f_od
            c_od = f"Net Overdraft of R{abs(net_cce):,.0f} ((R{abs(net_cce):,.0f}))" if net_cce < 0 else f"Net Positive Cash of R{net_cce:,.0f}"
            w_od = [
                f"Net Positive Cash of R{abs(b_od) + p_od + f_od:,.0f} (treated overdraft as positive cash)",
                f"Net Overdraft of R{abs(b_od):,.0f} (ignored petty cash and float)",
                f"R{p_od + f_od:,.0f} Positive Cash",
                f"Net Overdraft of R{abs(net_cce) * 1.5:,.0f}",
                f"Net Overdraft of R{abs(net_cce) / 2:,.0f}",
                f"Net Overdraft of R{abs(b_od) - p_od + f_od:,.0f}",
                f"R0"
            ]
            q_od = (f"The year-end Trial Balance of **{co_od}** reflects: Bank overdraft of **R{abs(b_od):,.0f}**; Petty cash float of "
                    f"**R{p_od:,.0f}**; Cash float in till registers of **R{f_od:,.0f}**. Calculate the net **Cash and Cash Equivalents** "
                    f"to be shown on the Balance Sheet / Cash Flow Statement:")
            exp_od = (f"Cash & Cash Equivalents = Bank (Overdraft: -R{abs(b_od):,.0f}) + Petty Cash (R{p_od:,.0f}) + Float (R{f_od:,.0f}) "
                      f"= -R{abs(b_od):,.0f} + R{p_od + f_od:,.0f} = {c_od}.")
            add_q("easy", "Cash Equivalents & Overdraft", q_od, c_od, w_od, "Applying", f"Calculate Overdraft CCE for {co_od}", exp_od)

    # Inflow vs Outflow vs Non-Cash Identification (Easy)
    cash_identification_items = [
        ("Depreciation written off on plant and machinery", "NON-CASH ITEM: Added back to profit in working capital reconciliation", "it represents an internal cost allocation with zero physical movement of cash funds"),
        ("Bad debts written off during the financial year", "NON-CASH ITEM: Added back or reconciled through debtors control", "it is an accounting adjustment for irrecoverable credit and involves zero cash outflow"),
        ("Loss on sale of delivery vehicle", "NON-CASH ITEM: Added back to profit in Cash Flow reconciliation", "it is an accounting adjustment; the actual cash proceeds appear separately under Investing Activities"),
        ("Profit on sale of surplus warehouse equipment", "NON-CASH ITEM: Deducted from profit in Cash Flow reconciliation", "it is an accounting gain; total cash proceeds are recognized under Investing Activities"),
        ("Discount allowed to debtors for early settlement", "NON-CASH ITEM: Bookkeeping discount reducing credit receivables", "it represents revenue foregone rather than a physical outflow of money from the bank"),
        ("Discount received from creditors for prompt payment", "NON-CASH ITEM: Bookkeeping discount reducing accounts payable", "it represents a cost reduction rather than a physical inflow of cash into the bank"),
        ("Cash received from credit customers in settlement of accounts", "CASH INFLOW: Operating Activities", "it represents liquid funds entering the business bank account from trading operations"),
        ("Cash paid to acquire additional delivery vehicles", "CASH OUTFLOW: Investing Activities", "it represents capital expenditure paid from company liquid reserves to acquire non-current assets"),
        ("Repurchase of ordinary shares from existing shareholders", "CASH OUTFLOW: Financing Activities", "it represents company cash paid to reacquire equity shares from investors"),
        ("Receipt of cash from issuing new ordinary share capital", "CASH INFLOW: Financing Activities", "it represents new equity funds deposited into the company bank account by shareholders"),
        ("Payment of provisional company tax to SARS", "CASH OUTFLOW: Operating Activities", "it represents mandatory statutory taxation disbursed from liquid cash reserves"),
        ("Payment of interim dividends to company shareholders", "CASH OUTFLOW: Operating Activities", "it represents profit distribution paid out in cash to registered shareholders"),
        ("Cash proceeds from selling an unneeded forklift", "CASH INFLOW: Investing Activities", "it represents liquid capital generated from disposing of a productive fixed asset"),
        ("Repayment of the principal balance on a mortgage bond", "CASH OUTFLOW: Financing Activities", "it represents cash disbursed to reduce long-term loan liabilities owed to financial institutions")
    ]

    for id_item, id_cat, id_rsn in cash_identification_items:
        for st_id in [
            f"How is **'{id_item}'** classified and treated in the Cash Flow Statement?",
            f"In cash flow accounting, **'{id_item}'** is defined as:",
            f"Identify the verified cash flow categorization of: **'{id_item}'**"
        ]:
            if counts["easy"] >= 300:
                break
            c_id = f"{id_cat} because {id_rsn}."
            w_id = [
                f"{'CASH INFLOW: Operating Activities' if 'NON-CASH' in id_cat or 'OUTFLOW' in id_cat else 'CASH OUTFLOW: Investing Activities'} because all ledger entries involve physical cash.",
                "Tax Exemption Allowance recognized exclusively by the South African Reserve Bank.",
                "Retained Income adjustment with zero disclosure on any financial statement.",
                "Fictitious asset created by double-entry bookkeeping rules.",
                "Contingent Liability recorded only in the Directors' Report Chairman address.",
                "Trading account deduction subtracted directly from raw material stock."
            ]
            add_q("easy", "Cash Flow Item Identification", st_id, c_id, w_id, "Understanding", f"Identify cash nature of {id_item[:25]}", c_id)

    # Bank Balance Shift Calculations (Favourable to Overdrawn & Vice Versa) (Easy)
    bank_transition_cases = [
        ("Laysano Ltd", 65000.0, -38000.0, "favourable R65,000", "overdrawn by (R38,000)"),
        ("Protea Hardware Ltd", 110000.0, -55000.0, "favourable R110,000", "overdrawn by (R55,000)"),
        ("Zulu Fashion Ltd", 45000.0, -22000.0, "favourable R45,000", "overdrawn by (R22,000)"),
        ("Metro Tech Ltd", 180000.0, -85000.0, "favourable R180,000", "overdrawn by (R85,000)"),
        ("Apex Auto Ltd", 80000.0, -42000.0, "favourable R80,000", "overdrawn by (R42,000)"),
        ("Kairo Furnishers Ltd", 95000.0, -48000.0, "favourable R95,000", "overdrawn by (R48,000)"),
        ("Galaxy Appliances Ltd", 240000.0, -115000.0, "favourable R240,000", "overdrawn by (R115,000)"),
        ("Bakersfield Ltd", 72000.0, -35000.0, "favourable R72,000", "overdrawn by (R35,000)"),
        ("Tshwane Traders Ltd", 60000.0, -29000.0, "favourable R60,000", "overdrawn by (R29,000)"),
        ("Cape Coast Ltd", 78000.0, -39000.0, "favourable R78,000", "overdrawn by (R39,000)"),
        # Reverse transitions: Overdrawn to Favourable
        ("Durban Wholesale Ltd", -65000.0, 95000.0, "overdrawn by (R65,000)", "favourable R95,000"),
        ("Sandton Goods Ltd", -120000.0, 160000.0, "overdrawn by (R120,000)", "favourable R160,000"),
        ("Bloemfontein Traders Ltd", -45000.0, 70000.0, "overdrawn by (R45,000)", "favourable R70,000"),
        ("Polokwane Supply Ltd", -32000.0, 48000.0, "overdrawn by (R32,000)", "favourable R48,000"),
        ("Nelspruit Supply Ltd", -38000.0, 56000.0, "overdrawn by (R38,000)", "favourable R56,000"),
        ("Kimberley Tools Ltd", -70000.0, 105000.0, "overdrawn by (R70,000)", "favourable R105,000"),
        ("Rustenburg Industrial Ltd", -85000.0, 130000.0, "overdrawn by (R85,000)", "favourable R130,000"),
        ("Port Elizabeth Logistics Ltd", -95000.0, 145000.0, "overdrawn by (R95,000)", "favourable R145,000"),
        ("Pietermaritzburg Ltd", -42000.0, 68000.0, "overdrawn by (R42,000)", "favourable R68,000"),
        ("Soweto Commercial Ltd", -52000.0, 82000.0, "overdrawn by (R52,000)", "favourable R82,000")
    ]

    for co_bt, b_start, b_end, desc_start, desc_end in bank_transition_cases:
        if counts["easy"] < 300:
            diff_bank = b_end - b_start
            is_inc = diff_bank > 0
            c_bt = f"Net {'Increase' if is_inc else 'Decrease'} of R{abs(diff_bank):,.0f}"
            w_bt = [
                f"Net {'Decrease' if is_inc else 'Increase'} of R{abs(diff_bank):,.0f}",
                f"Net Increase of R{abs(b_end) - abs(b_start):,.0f} (subtracted absolute values without directional signs)",
                f"Net Decrease of R{abs(b_start):,.0f} (only counted opening balance)",
                f"Net Increase of R{abs(b_end):,.0f} (only counted closing balance)",
                f"Net {'Increase' if is_inc else 'Decrease'} of R{abs(diff_bank) * 1.5:,.0f}",
                f"Net {'Increase' if is_inc else 'Decrease'} of R{abs(diff_bank) / 2:,.0f}",
                f"R0 (no change in cash)"
            ]
            q_bt = (f"In the records of **{co_bt}**, the Bank account balance on 1 March was **{desc_start}**. On 28 February, the Bank "
                    f"account was **{desc_end}**. Calculate the exact **Net Change in the Bank balance** for the Cash Flow Statement:")
            exp_bt = (f"Net Change in Bank = Closing Balance ({desc_end}) - Opening Balance ({desc_start}) "
                      f"= R{b_end:,.0f} - (R{b_start:,.0f}) = {c_bt}.")
            add_q("easy", "Bank Balance Shifts", q_bt, c_bt, w_bt, "Applying", f"Calculate Bank shift for {co_bt}", exp_bt)

    # Loan Inflow vs Repayment Determinations (Easy)
    loan_easy_cases = [
        ("Laysano Ltd", 1500000.0, 1200000.0, 300000.0, "repayment"),
        ("Protea Hardware Ltd", 2000000.0, 1600000.0, 400000.0, "repayment"),
        ("Zulu Fashion Ltd", 900000.0, 750000.0, 150000.0, "repayment"),
        ("Metro Tech Ltd", 3500000.0, 2800000.0, 700000.0, "repayment"),
        ("Apex Auto Ltd", 1800000.0, 1450000.0, 350000.0, "repayment"),
        ("Kairo Furnishers Ltd", 2200000.0, 1850000.0, 350000.0, "repayment"),
        ("Galaxy Appliances Ltd", 4000000.0, 3200000.0, 800000.0, "repayment"),
        ("Bakersfield Ltd", 1600000.0, 1300000.0, 300000.0, "repayment"),
        ("Tshwane Traders Ltd", 1400000.0, 1150000.0, 250000.0, "repayment"),
        ("Cape Coast Ltd", 1700000.0, 1400000.0, 300000.0, "repayment"),
        # Additional loan borrowed (inflow)
        ("Durban Wholesale Ltd", 2500000.0, 3200000.0, 700000.0, "inflow"),
        ("Sandton Goods Ltd", 3000000.0, 4200000.0, 1200000.0, "inflow"),
        ("Bloemfontein Traders Ltd", 1200000.0, 1650000.0, 450000.0, "inflow"),
        ("Polokwane Supply Ltd", 950000.0, 1300000.0, 350000.0, "inflow"),
        ("Nelspruit Supply Ltd", 1100000.0, 1500000.0, 400000.0, "inflow"),
        ("Kimberley Tools Ltd", 1800000.0, 2350000.0, 550000.0, "inflow"),
        ("Rustenburg Industrial Ltd", 2400000.0, 3100000.0, 700000.0, "inflow"),
        ("Port Elizabeth Logistics Ltd", 2800000.0, 3600000.0, 800000.0, "inflow"),
        ("Pietermaritzburg Ltd", 1300000.0, 1750000.0, 450000.0, "inflow"),
        ("Soweto Commercial Ltd", 1500000.0, 2050000.0, 550000.0, "inflow")
    ]

    for co_ln, ln_open, ln_close, ln_diff, ln_dir in loan_easy_cases:
        if counts["easy"] < 300:
            if ln_dir == "repayment":
                c_ln = f"R{ln_diff:,.0f} Repayment of Loan (Financing Cash Outflow)"
            else:
                c_ln = f"R{ln_diff:,.0f} Additional Loan Raised (Financing Cash Inflow)"

            w_ln = [
                f"R{ln_diff:,.0f} {'Inflow' if ln_dir == 'repayment' else 'Outflow'} (inverted cash flow direction)",
                f"R{ln_close:,.0f} (confused closing loan balance with the cash flow)",
                f"R{ln_open:,.0f} (confused opening balance with the cash flow)",
                f"R{ln_diff * 1.5:,.0f}",
                f"R{ln_diff / 2:,.0f}",
                f"R{ln_open + ln_close:,.0f}",
                f"R{ln_diff + 50000:,.0f}"
            ]
            q_ln = (f"The Non-Current Liabilities section of **{co_ln}** reflects a mortgage loan from Standard Bank with an opening "
                    f"balance of **R{ln_open:,.0f}** and a closing balance of **R{ln_close:,.0f}**. Determine the cash flow figure and "
                    f"its classification on the Cash Flow Statement:")
            exp_ln = (f"Change in Loan = Closing (R{ln_close:,.0f}) - Opening (R{ln_open:,.0f}) = R{ln_diff:,.0f} ({ln_dir}). "
                      f"Classified under Cash Flows from Financing Activities: {c_ln}.")
            add_q("easy", "Loan Financing Determinations", q_ln, c_ln, w_ln, "Applying", f"Determine Loan change for {co_ln}", exp_ln)

    # Detailed Cash Flow Scenarios (Easy)
    more_cf_scenarios = [
        ("Acquisition of a vacant commercial plot for future warehouse expansion", "Cash Flow from Investing Activities (Outflow)", "it involves purchasing a non-current tangible capital asset"),
        ("Receipt of annual dividend payments from listed company investments", "Cash Flow from Operating Activities (Inflow)", "it represents investment return generated from income-earning financial holdings"),
        ("Payment of annual interest on a 15-year commercial mortgage loan", "Cash Flow from Operating Activities (Outflow)", "financing costs/interest on borrowings are statutory operating cash outflows"),
        ("Collection of outstanding credit balances from debtors via EFT deposits", "Cash Flow from Operating Activities (Inflow)", "it represents liquid funds received from trading revenue operations"),
        ("Capitalized interest added directly to a long-term loan account balance", "NON-CASH ITEM: Excluded from Cash Flow Statement", "it increases the loan balance via bookkeeping entry with zero physical cash movement"),
        ("Payment of statutory Unemployment Insurance Fund (UIF) contributions to SARS", "Cash Flow from Operating Activities (Outflow)", "it represents employee compensation and statutory operating disbursements"),
        ("Receipt of a state manufacturing grant deposited into the current account", "Cash Flow from Operating Activities (Inflow)", "it represents liquid funds received to subsidize operational manufacturing activities"),
        ("Cash paid to acquire high-speed automated packaging machinery", "Cash Flow from Investing Activities (Outflow)", "it is capital expenditure disbursed to purchase non-current productive equipment"),
        ("Cash received from an insurance claim payout for a written-off company van", "Cash Flow from Investing Activities (Inflow)", "it represents capital compensation received for a destroyed non-current tangible asset"),
        ("Repurchase of 25,000 ordinary shares from the estate of a deceased director", "Cash Flow from Financing Activities (Outflow)", "it is a cash disbursement made to buy back company equity from shareholders"),
        ("Issue of 50,000 new ordinary shares at R15.00 each through a private placement", "Cash Flow from Financing Activities (Inflow)", "it represents fresh equity capital injected into the company bank account"),
        ("Settlement of monthly municipal water and electricity utility bills", "Cash Flow from Operating Activities (Outflow)", "it is a regular operational expense paid in cash to maintain trading facilities"),
        ("Writing off irrecoverable credit sales after a debtor absconded overseas", "NON-CASH ITEM: Excluded from Cash Flow Statement", "it is an accounting journal write-off that involves no physical cash movement"),
        ("Transfer of R100,000 from the Bank account into a 6-month Fixed Deposit", "Cash Flow from Investing Activities (Outflow)", "it represents cash deployed to acquire a medium-term financial investment asset"),
        ("Redemption and receipt of capital from a matured Nedbank Fixed Deposit", "Cash Flow from Investing Activities (Inflow)", "it represents liquid funds returning from a liquidated financial asset"),
        ("Settlement of outstanding trade creditors accounts by electronic funds transfer", "Cash Flow from Operating Activities (Outflow)", "it represents cash disbursed in the normal trading cycle to pay suppliers of trading goods"),
        ("Cash sales of merchandise to retail walk-in customers", "Cash Flow from Operating Activities (Inflow)", "it represents immediate liquid cash generated from direct revenue trading operations"),
        ("Purchase of packaging materials for immediate factory production use", "Cash Flow from Operating Activities (Outflow)", "it is an operational expense paid in cash to support manufacturing processes"),
        ("Payment of monthly warehouse security guarding services", "Cash Flow from Operating Activities (Outflow)", "it represents an operational cash outflow incurred to protect company inventory"),
        ("Payment of annual audit fees to external chartered accountants", "Cash Flow from Operating Activities (Outflow)", "it is a statutory operational expense paid in cash to independent auditing professionals"),
        ("Cash paid to construct an employee canteen extension", "Cash Flow from Investing Activities (Outflow)", "it represents capital expenditure disbursed to expand company fixed property assets"),
        ("Cash proceeds from the sale of redundant office desks and chairs", "Cash Flow from Investing Activities (Inflow)", "it represents liquid recovery from disposing of surplus non-current office furniture"),
        ("Repurchase of ordinary shares from an institutional investor", "Cash Flow from Financing Activities (Outflow)", "it represents cash paid to buy back company equity shares from the market"),
        ("Taking out an 8-year industrial vehicle lease financing loan", "Cash Flow from Financing Activities (Inflow)", "it is long-term borrowed capital received to finance commercial transport capacity"),
        ("Annual payment of municipal property assessment rates", "Cash Flow from Operating Activities (Outflow)", "it is an operational property expense paid to local government authorities"),
        ("Receipt of interest earned on an investment in RSA Government Retail Bonds", "Cash Flow from Operating Activities (Inflow)", "it represents operational investment income generated from cash investments"),
        ("Cash paid to acquire commercial delivery scooters", "Cash Flow from Investing Activities (Outflow)", "it is capital expenditure disbursed to purchase non-current delivery assets"),
        ("Capital injection from issuing 50,000 preference shares", "Cash Flow from Financing Activities (Inflow)", "it is fresh contributed equity capital injected into company bank reserves"),
        ("Repayment of 5-year debenture bonds at maturity", "Cash Flow from Financing Activities (Outflow)", "it represents cash disbursed to settle and retire long-term debt liabilities"),
        ("Settlement of annual factory insurance premiums", "Cash Flow from Operating Activities (Outflow)", "it is an operational disbursement paid in cash to insure factory assets against fire and theft")
    ]

    for m_item, m_class, m_rsn in more_cf_scenarios:
        for st_m in [
            f"Under which section of the Cash Flow Statement is **'{m_item}'** presented, and why?",
            f"What is the accounting classification and cash effect of **'{m_item}'**?",
            f"Identify the verified Cash Flow Statement classification for: **'{m_item}'**"
        ]:
            if counts["easy"] >= 300:
                break
            c_m = f"Classified under {m_class} because {m_rsn}."
            w_m = [
                f"Classified under {'Cash Flow from Investing Activities' if 'Financing' in m_class or 'Operating' in m_class else 'Cash Flow from Financing Activities'} (Outflow) because all ledger accounts affect equity.",
                f"Classified under {'Cash Flow from Operating Activities' if 'Investing' in m_class or 'Financing' in m_class else 'Cash Flow from Investing Activities'} (Inflow) because it reduces operating profit.",
                "Non-Cash Adjustment disclosed exclusively in the Corporate Governance Chairman note.",
                "Tax Allowance that bypasses the general ledger completely.",
                "Trading Account deduction subtracted directly from raw material stock.",
                "Contingent Liability recorded only in an off-balance sheet footnote."
            ]
            add_q("easy", "Detailed Cash Flow Scenarios", st_m, c_m, w_m, "Understanding", f"Classify {m_item[:25]}", c_m)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Reconciliation of Profit to Cash Generated, Taxation Paid, Dividends Paid,
    # Additions to Tangible Assets, Share Capital & Loan Inflows/Outflows
    # =========================================================================

    # 1. Taxation Paid Note (Medium)
    # Tax Paid = Open SARS (Credit +) + Income Tax Expense - Close SARS (Credit -)
    tax_paid_cases = [
        ("Laysano Ltd", 45000.0, "credit", 540000.0, 32000.0, "credit"),
        ("Protea Hardware Ltd", 68000.0, "credit", 780000.0, 51000.0, "credit"),
        ("Zulu Fashion Ltd", 24000.0, "credit", 390000.0, 18000.0, "credit"),
        ("Metro Tech Ltd", 82000.0, "credit", 980000.0, 64000.0, "credit"),
        ("Apex Auto Ltd", 38000.0, "credit", 460000.0, 27000.0, "credit"),
        ("Kairo Furnishers Ltd", 55000.0, "credit", 680000.0, 42000.0, "credit"),
        ("Orchid Boutique Ltd", 19000.0, "credit", 240000.0, 14000.0, "credit"),
        ("Galaxy Appliances Ltd", 95000.0, "credit", 1150000.0, 78000.0, "credit"),
        ("Bakersfield Ltd", 41000.0, "credit", 510000.0, 33000.0, "credit"),
        ("Tshwane Traders Ltd", 34000.0, "credit", 430000.0, 26000.0, "credit"),
        # Cases with debit opening/closing balances (SARS refundable):
        ("Cape Coast Ltd", 28000.0, "debit", 490000.0, 35000.0, "credit"),
        ("Durban Wholesale Ltd", 48000.0, "credit", 850000.0, 22000.0, "debit"),
        ("Sandton Goods Ltd", 35000.0, "debit", 1250000.0, 45000.0, "credit"),
        ("Bloemfontein Traders Ltd", 22000.0, "credit", 580000.0, 15000.0, "debit"),
        ("Polokwane Supply Ltd", 18000.0, "debit", 390000.0, 25000.0, "credit")
    ]

    for co_tx_p, open_sars, open_st, tax_exp, close_sars, close_st in tax_paid_cases:
        # SARS Ledger Account formulation:
        # Bank payment (Tax Paid) is on the DEBIT side of the SARS Account.
        # Debit side = Bank (Tax Paid) + (Opening Debit if debit) + (Closing Credit if credit) -> wait:
        # SARS Account:
        # Balance b/d: Credit (Liability) or Debit (Asset)
        # Income Tax (Expense): Credit side
        # Bank (Payment): Debit side
        # Balance c/d: Closing balance
        # Therefore:
        # Total Credits = (Open if credit else 0) + Income Tax Expense
        # Total Debits = (Open if debit else 0) + Bank (Tax Paid) + (Close if credit else 0)
        # If closing is debit, it goes to credit side as Balance c/d.
        # Let's use strict ledger balancing:
        credits_sars = tax_exp + (open_sars if open_st == "credit" else 0.0) + (close_sars if close_st == "debit" else 0.0)
        debits_non_bank = (open_sars if open_st == "debit" else 0.0) + (close_sars if close_st == "credit" else 0.0)
        tax_paid = credits_sars - debits_non_bank

        c_tp = f"R{tax_paid:,.0f} (Cash Outflow)"
        w_tp = [
            f"R{tax_exp:,.0f} (assumed Income Tax expense equals tax paid without adjustments)",
            f"R{tax_paid + open_sars:,.0f}",
            f"R{tax_paid - close_sars:,.0f}",
            f"R{tax_paid * 1.2:,.0f}",
            f"R{tax_paid / 2:,.0f}",
            f"R{open_sars + tax_exp + close_sars:,.0f}",
            f"R{tax_exp - open_sars:,.0f}"
        ]
        q_tp = (f"The financial records of **{co_tx_p}** reflect: Opening SARS (Income Tax) balance: **R{open_sars:,.0f} ({open_st})**; "
                f"Income Tax expense for the year per Income Statement: **R{tax_exp:,.0f}**; Closing SARS (Income Tax) balance: "
                f"**R{close_sars:,.0f} ({close_st})**. Calculate the **Taxation Paid** figure for the Cash Flow Statement:")
        exp_tp = (f"SARS Account Ledger: Total tax owed = Opening ({open_st} R{open_sars:,.0f}) + Current Tax (R{tax_exp:,.0f}) = R{credits_sars:,.0f}. "
                  f"Subtracting non-bank debits and closing ({close_st} R{close_sars:,.0f}) yields: Taxation Paid = {c_tp}.")
        add_q("medium", "Taxation Paid Calculations", q_tp, c_tp, w_tp, "Applying", f"Calculate Taxation Paid for {co_tx_p}", exp_tp)

    # 2. Dividends Paid Note (Medium)
    # Dividends Paid = Opening Shareholders for Dividends + Interim Dividends Paid
    dividends_paid_cases = [
        ("Laysano Ltd", 180000.0, 120000.0, 210000.0),
        ("Protea Hardware Ltd", 260000.0, 180000.0, 310000.0),
        ("Zulu Fashion Ltd", 95000.0, 65000.0, 115000.0),
        ("Metro Tech Ltd", 380000.0, 240000.0, 450000.0),
        ("Apex Auto Ltd", 150000.0, 95000.0, 180000.0),
        ("Kairo Furnishers Ltd", 220000.0, 140000.0, 260000.0),
        ("Orchid Boutique Ltd", 75000.0, 48000.0, 90000.0),
        ("Galaxy Appliances Ltd", 440000.0, 290000.0, 520000.0),
        ("Bakersfield Ltd", 170000.0, 110000.0, 205000.0),
        ("Tshwane Traders Ltd", 145000.0, 90000.0, 175000.0),
        ("Cape Coast Ltd", 165000.0, 105000.0, 195000.0),
        ("Durban Wholesale Ltd", 320000.0, 210000.0, 390000.0),
        ("Sandton Goods Ltd", 410000.0, 270000.0, 480000.0),
        ("Bloemfontein Traders Ltd", 185000.0, 115000.0, 225000.0),
        ("Polokwane Supply Ltd", 130000.0, 80000.0, 155000.0)
    ]

    for co_div, open_div, interim_div, final_div in dividends_paid_cases:
        div_paid = open_div + interim_div
        c_dp = f"R{div_paid:,.0f} (Cash Outflow)"
        w_dp = [
            f"R{interim_div + final_div:,.0f} (calculated total dividends declared for the year instead of dividends paid)",
            f"R{open_div:,.0f} (only paid opening dividends without interim dividends)",
            f"R{interim_div:,.0f} (only counted interim dividends)",
            f"R{final_div:,.0f} (confused final dividend declared with dividends paid)",
            f"R{open_div + interim_div + final_div:,.0f}",
            f"R{div_paid * 1.5:,.0f}",
            f"R{div_paid / 2:,.0f}"
        ]
        q_dp = (f"The records of **{co_div}** show: Shareholders for Dividends on 1 March (opening): **R{open_div:,.0f}**; "
                f"Interim dividends paid during the year: **R{interim_div:,.0f}**; Final dividends recommended at year-end (closing): "
                f"**R{final_div:,.0f}**. Calculate the **Dividends Paid** to be presented in the Cash Flow Statement:")
        exp_dp = (f"Dividends Paid = Opening Shareholders for Dividends (last year's final dividend paid this year) + Interim Dividends paid "
                  f"= R{open_div:,.0f} + R{interim_div:,.0f} = {c_dp}. (The final dividend of R{final_div:,.0f} is a year-end liability paid next year).")
        add_q("medium", "Dividends Paid Calculations", q_dp, c_dp, w_dp, "Applying", f"Calculate Dividends Paid for {co_div}", exp_dp)

    # 3. Additions to Tangible Assets (Purchases) (Medium)
    # Additions = Close CV - Open CV + Depreciation + CV of Disposals
    asset_additions_cases = [
        ("Laysano Ltd", 3800000.0, 4450000.0, 320000.0, 140000.0),
        ("Protea Hardware Ltd", 5200000.0, 6100000.0, 450000.0, 180000.0),
        ("Zulu Fashion Ltd", 2400000.0, 2750000.0, 190000.0, 95000.0),
        ("Metro Tech Ltd", 7500000.0, 8900000.0, 620000.0, 240000.0),
        ("Apex Auto Ltd", 3600000.0, 4200000.0, 280000.0, 130000.0),
        ("Kairo Furnishers Ltd", 4800000.0, 5650000.0, 390000.0, 160000.0),
        ("Orchid Boutique Ltd", 1600000.0, 1920000.0, 140000.0, 60000.0),
        ("Galaxy Appliances Ltd", 8900000.0, 10500000.0, 750000.0, 310000.0),
        ("Bakersfield Ltd", 3700000.0, 4350000.0, 310000.0, 125000.0),
        ("Tshwane Traders Ltd", 3100000.0, 3680000.0, 260000.0, 110000.0),
        ("Cape Coast Ltd", 3500000.0, 4150000.0, 290000.0, 120000.0),
        ("Durban Wholesale Ltd", 6800000.0, 7950000.0, 560000.0, 220000.0)
    ]

    for co_add, open_cv, close_cv, dep_yr, disp_cv in asset_additions_cases:
        # Additions = Close CV - Open CV + Depreciation + Disposals CV
        additions_val = close_cv - open_cv + dep_yr + disp_cv
        c_add = f"R{additions_val:,.0f} (Investing Outflow)"
        w_add = [
            f"R{close_cv - open_cv:,.0f} (simply took the net difference without accounting for depreciation or disposals)",
            f"R{close_cv - open_cv + dep_yr:,.0f} (forgot to add back disposals carrying value)",
            f"R{additions_val * 1.2:,.0f}",
            f"R{additions_val / 2:,.0f}",
            f"R{additions_val + 150000:,.0f}",
            f"R{close_cv + dep_yr:,.0f}",
            f"R{open_cv + dep_yr:,.0f}"
        ]
        q_add = (f"The Tangible Asset records of **{co_add}** show: Carrying Value at 1 March (opening): **R{open_cv:,.0f}**; "
                 f"Carrying Value at 28 February (closing): **R{close_cv:,.0f}**. During the year, depreciation amounted to **R{dep_yr:,.0f}** "
                 f"and an old asset with a carrying value of **R{disp_cv:,.0f}** was sold. Calculate the **Cost of Tangible Assets Purchased (Additions)**:")
        exp_add = (f"Asset Note reconstruction: Closing CV (R{close_cv:,.0f}) = Opening CV (R{open_cv:,.0f}) + Additions - Depreciation (R{dep_yr:,.0f}) - Disposals (R{disp_cv:,.0f}). "
                   f"Additions = R{close_cv:,.0f} - R{open_cv:,.0f} + R{dep_yr:,.0f} + R{disp_cv:,.0f} = {c_add}.")
        add_q("medium", "Tangible Asset Additions", q_add, c_add, w_add, "Applying", f"Calculate Asset Additions for {co_add}", exp_add)

    # 4. Changes in Working Capital Components (Inventory, Receivables, Payables) (Medium)
    wc_changes_grid = [
        ("Trading Inventory", 450000.0, 520000.0, "increase", "Outflow of R70,000", -70000.0),
        ("Trading Inventory", 680000.0, 590000.0, "decrease", "Inflow of R90,000", 90000.0),
        ("Trade and Other Receivables", 380000.0, 440000.0, "increase", "Outflow of R60,000", -60000.0),
        ("Trade and Other Receivables", 510000.0, 430000.0, "decrease", "Inflow of R80,000", 80000.0),
        ("Trade and Other Payables", 290000.0, 360000.0, "increase", "Inflow of R70,000", 70000.0),
        ("Trade and Other Payables", 420000.0, 350000.0, "decrease", "Outflow of R70,000", -70000.0)
    ]

    for co_name_wc in ["Laysano Ltd", "Protea Ltd", "Zulu Ltd", "Metro Ltd", "Apex Ltd", "Kairo Ltd", "Orchid Ltd", "Galaxy Ltd", "Bakersfield Ltd", "Tshwane Ltd"]:
        for item_wc, open_wcv, close_wcv, dir_wcv, cash_impact, num_impact in wc_changes_grid:
            if counts["medium"] >= 500:
                break
            diff_wcv = abs(close_wcv - open_wcv)
            c_cw = f"({dir_wcv.capitalize()} of R{diff_wcv:,.0f}): {cash_impact}"
            w_cw = [
                f"({dir_wcv.capitalize()} of R{diff_wcv:,.0f}): {'Inflow' if 'Outflow' in cash_impact else 'Outflow'} of R{diff_wcv:,.0f} (inverted cash flow direction)",
                f"No effect on cash flow because {item_wc} is a non-cash balance sheet item",
                f"Investing Activity: Outflow of R{diff_wcv:,.0f}",
                f"Financing Activity: Inflow of R{diff_wcv:,.0f}",
                f"R{close_wcv:,.0f} (confused closing balance with cash change)",
                f"R{open_wcv + close_wcv:,.0f}",
                f"Outflow of R{diff_wcv * 2:,.0f}"
            ]
            q_cw = (f"In the records of **{co_name_wc}**, **{item_wc}** had an opening balance of **R{open_wcv:,.0f}** and a closing "
                    f"balance of **R{close_wcv:,.0f}**. Determine the change and its effect on the Cash Flow Statement under Changes in Working Capital:")
            exp_cw = (f"{item_wc} changed by R{diff_wcv:,.0f} ({dir_wcv}). In working capital: For assets (inventory/debtors), an increase consumes cash (outflow) "
                      f"and a decrease frees cash (inflow); for liabilities (creditors), an increase delays cash payment (inflow) and a decrease consumes cash (outflow). Result: {c_cw}.")
            add_q("medium", "Working Capital Changes", q_cw, c_cw, w_cw, "Applying", f"Determine WC change for {co_name_wc}", exp_cw)

    # Combinatorial additions for Medium to reach 500:
    # Operating Profit Before Changes in Working Capital
    # = Net Profit Before Tax + Depreciation + Interest Expense
    npbt_list = [750000.0, 920000.0, 1100000.0, 1350000.0, 1600000.0, 1850000.0, 2100000.0, 2450000.0]
    dep_list = [120000.0, 150000.0, 180000.0, 220000.0, 260000.0, 310000.0]
    int_list = [35000.0, 48000.0, 62000.0, 75000.0, 90000.0]

    for co_op in ["Laysano Ltd", "Protea Ltd", "Zulu Ltd", "Metro Ltd", "Apex Ltd", "Kairo Ltd", "Galaxy Ltd", "Bakersfield Ltd"]:
        for np_val in npbt_list:
            for dep_val in dep_list:
                for int_val in int_list:
                    if counts["medium"] >= 500:
                        break
                    op_before_wc = np_val + dep_val + int_val
                    c_opwc = f"R{op_before_wc:,.0f}"
                    w_opwc = [
                        f"R{np_val - dep_val - int_val:,.0f} (subtracted depreciation and interest instead of adding back)",
                        f"R{np_val + dep_val:,.0f} (forgot to add back interest expense)",
                        f"R{np_val + int_val:,.0f} (forgot to add back non-cash depreciation)",
                        f"R{op_before_wc * 1.2:,.0f}",
                        f"R{op_before_wc / 2:,.0f}",
                        f"R{np_val:,.0f}",
                        f"R{op_before_wc + 100000:,.0f}"
                    ]
                    q_opwc = (f"In the Cash Flow reconciliation note of **{co_op}**, Net Profit before tax is **R{np_val:,.0f}**. "
                              f"Depreciation for the year is **R{dep_val:,.0f}** and Interest expense on loan is **R{int_val:,.0f}**. "
                              f"Calculate the **Operating Profit before Changes in Working Capital**:")
                    exp_opwc = f"Operating Profit before Working Capital = Net Profit before Tax (R{np_val:,.0f}) + Depreciation (R{dep_val:,.0f}) + Interest Expense (R{int_val:,.0f}) = {c_opwc}."
                    add_q("medium", "Working Capital Reconciliation", q_opwc, c_opwc, w_opwc, "Applying", f"Calculate Operating Profit before WC for {co_op}", exp_opwc)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Complete Cash Generated from Operations Reconciliation, Ordinary Share Capital
    # and Share Buybacks at Average Issue Price, Total Investing Activities
    # =========================================================================

    share_buyback_cases = [
        ("Laysano Ltd", 600000, 4800000.0, 50000, 11.50, 150000, 12.00),
        ("Protea Hardware Ltd", 800000, 7200000.0, 60000, 12.80, 200000, 13.50),
        ("Zulu Fashion Ltd", 400000, 2800000.0, 40000, 9.20, 100000, 9.50),
        ("Metro Tech Ltd", 1200000, 14400000.0, 100000, 15.00, 300000, 16.00),
        ("Apex Auto Ltd", 500000, 4500000.0, 45000, 11.20, 120000, 11.80),
        ("Kairo Furnishers Ltd", 700000, 6300000.0, 50000, 12.00, 180000, 12.50),
        ("Galaxy Appliances Ltd", 1500000, 18000000.0, 120000, 16.50, 400000, 17.00),
        ("Bakersfield Ltd", 650000, 5850000.0, 55000, 11.80, 160000, 12.20)
    ]

    for co_sb, open_shares, open_cap, buy_shares, buy_price, new_shares, new_price in share_buyback_cases:
        avg_issue_price = open_cap / open_shares
        cap_outflow_buyback = buy_shares * avg_issue_price
        ret_income_buyback = buy_shares * (buy_price - avg_issue_price)
        total_cash_buyback = buy_shares * buy_price
        new_shares_proceeds = new_shares * new_price
        net_financing_shares = new_shares_proceeds - total_cash_buyback

        for q_type_h in [1, 2]:
            if counts["hard"] >= 200:
                break

            if q_type_h == 1:
                # Calculate Share Buyback Split (Share Capital vs Retained Income)
                c_sbs = f"Share Capital deduction = R{cap_outflow_buyback:,.0f} (at average price R{avg_issue_price:.2f}); Retained Income deduction = R{ret_income_buyback:,.0f}"
                w_sbs = [
                    f"Share Capital deduction = R{total_cash_buyback:,.0f}; Retained Income deduction = R0 (deducted entire repurchase from share capital)",
                    f"Share Capital deduction = R0; Retained Income deduction = R{total_cash_buyback:,.0f} (deducted entire repurchase from retained income)",
                    f"Share Capital deduction = R{ret_income_buyback:,.0f}; Retained Income deduction = R{cap_outflow_buyback:,.0f} (inverted share capital and retained income)",
                    f"Share Capital deduction = R{cap_outflow_buyback * 1.2:,.0f}; Retained Income = R{ret_income_buyback * 1.5:,.0f}",
                    f"Share Capital deduction = R{cap_outflow_buyback / 2:,.0f}; Retained Income = R{ret_income_buyback / 2:,.0f}",
                    f"Share Capital deduction = R{buy_shares * buy_price:,.0f}; Zero deduction from retained income",
                    f"Share Capital deduction = R{open_cap - total_cash_buyback:,.0f}"
                ]
                q_sbs = (f"**{co_sb}** had **{open_shares:,} issued shares** with a stated capital balance of **R{open_cap:,.0f}** on 1 March. "
                         f"On 31 August, the company repurchased **{buy_shares:,} shares** at **R{buy_price:.2f} per share** from a dissatisfied shareholder. "
                         f"Calculate the average issue price per share and determine the separate deductions to be made from **Ordinary Share Capital** and **Retained Income**:")
                exp_sbs = (f"1. Average issue price = Opening Share Capital (R{open_cap:,.0f}) / Opening Shares ({open_shares:,}) = R{avg_issue_price:.2f} per share. "
                           f"2. Deduction from Share Capital = {buy_shares:,} shares × R{avg_issue_price:.2f} = R{cap_outflow_buyback:,.0f}. "
                           f"3. Excess paid above average price = R{buy_price:.2f} - R{avg_issue_price:.2f} = R{buy_price - avg_issue_price:.2f} per share. "
                           f"4. Deduction from Retained Income = {buy_shares:,} shares × R{buy_price - avg_issue_price:.2f} = R{ret_income_buyback:,.0f}.")
                add_q("hard", "Share Buyback Calculations", q_sbs, c_sbs, w_sbs, "Evaluating", f"Calculate Share Buyback split for {co_sb}", exp_sbs)

            else:
                # Calculate Net Proceeds from Share Financing Activities
                c_sfn = f"Proceeds from new shares = R{new_shares_proceeds:,.0f}; Repurchase outflow = (R{total_cash_buyback:,.0f}); Net Share Financing = R{net_financing_shares:,.0f}"
                w_sfn = [
                    f"Proceeds = R{new_shares_proceeds:,.0f}; Repurchase outflow = (R{cap_outflow_buyback:,.0f}) (used only capital portion instead of total cash paid)",
                    f"Proceeds = R{new_shares_proceeds - total_cash_buyback:,.0f}; Net = R0",
                    f"Proceeds = R{new_shares_proceeds * 1.2:,.0f}; Net = R{net_financing_shares * 1.5:,.0f}",
                    f"Proceeds = R{total_cash_buyback:,.0f}; Net = (R{total_cash_buyback:,.0f})",
                    f"Proceeds = R{new_shares_proceeds:,.0f}; Net = R{new_shares_proceeds + total_cash_buyback:,.0f} (added repurchase outflow instead of subtracting)",
                    f"Proceeds = R{open_cap + new_shares_proceeds:,.0f}",
                    f"Net Share Financing = R{net_financing_shares / 2:,.0f}"
                ]
                q_sfn = (f"During the financial year, **{co_sb}** issued **{new_shares:,} new ordinary shares** at **R{new_price:.2f} each**, and "
                         f"repurchased **{buy_shares:,} shares** at **R{buy_price:.2f} each**. "
                         f"Calculate the total cash inflow from share issues, the total cash outflow for share buybacks, and the **Net Cash Flow from Share Financing**:")
                exp_sfn = (f"1. Cash inflow from issue of shares = {new_shares:,} × R{new_price:.2f} = R{new_shares_proceeds:,.0f}. "
                           f"2. Total cash outflow for share buyback = {buy_shares:,} × R{buy_price:.2f} = R{total_cash_buyback:,.0f}. "
                           f"3. Net Cash Flow from shares = R{new_shares_proceeds:,.0f} - R{total_cash_buyback:,.0f} = {c_sfn}.")
                add_q("hard", "Share Capital Financing", q_sfn, c_sfn, w_sfn, "Evaluating", f"Calculate Net Share Financing for {co_sb}", exp_sfn)

    # Complete Cash Generated from Operations Reconciliation (Hard)
    cgo_companies = [
        "Laysano Ltd", "Protea Hardware Ltd", "Zulu Fashion Ltd", "Metro Tech Ltd",
        "Apex Auto Ltd", "Kairo Furnishers Ltd", "Galaxy Appliances Ltd", "Bakersfield Ltd",
        "Tshwane Traders Ltd", "Cape Coast Ltd", "Durban Wholesale Ltd", "Sandton Goods Ltd",
        "Bloemfontein Traders Ltd", "Polokwane Supply Ltd", "Nelspruit Supply Ltd"
    ]
    cgo_financial_data = [
        (1250000.0, 240000.0, 65000.0, -35000.0, -45000.0, 60000.0),
        (1450000.0, 280000.0, 75000.0, -45000.0, -60000.0, 80000.0),
        (1650000.0, 310000.0, 85000.0, -50000.0, -70000.0, 95000.0),
        (1850000.0, 340000.0, 95000.0, -60000.0, -75000.0, 110000.0),
        (2100000.0, 390000.0, 110000.0, -85000.0, -95000.0, 120000.0),
        (2400000.0, 420000.0, 125000.0, -90000.0, -110000.0, 140000.0),
        (2750000.0, 480000.0, 145000.0, -110000.0, -130000.0, 175000.0),
        (3200000.0, 580000.0, 180000.0, -120000.0, -140000.0, 210000.0),
        (3600000.0, 640000.0, 200000.0, -150000.0, -170000.0, 240000.0),
        (4100000.0, 720000.0, 220000.0, -180000.0, -210000.0, 290000.0),
        (950000.0, 180000.0, 48000.0, 25000.0, -35000.0, -40000.0),
        (880000.0, 160000.0, 42000.0, 35000.0, -40000.0, -50000.0),
        (1100000.0, 210000.0, 55000.0, -30000.0, -42000.0, 52000.0),
        (1350000.0, 260000.0, 70000.0, -40000.0, -55000.0, 72000.0)
    ]

    for co_cgo in cgo_companies:
        for npbt_c, dep_c, int_c, d_inv, d_rec, d_pay in cgo_financial_data:
            if counts["hard"] >= 200:
                break
            op_prof_wc = npbt_c + dep_c + int_c
            net_wc_change = d_inv + d_rec + d_pay
            final_cgo = op_prof_wc + net_wc_change

            c_cgo = f"R{final_cgo:,.0f}"
            w_cgo = [
                f"R{op_prof_wc:,.0f} (stopped before applying working capital changes)",
                f"R{npbt_c:,.0f} (confused net profit before tax with cash generated)",
                f"R{final_cgo * 1.2:,.0f}",
                f"R{final_cgo / 2:,.0f}",
                f"R{op_prof_wc - net_wc_change:,.0f} (inverted working capital signs)",
                f"R{final_cgo + 250000:,.0f}",
                f"R{npbt_c + net_wc_change:,.0f} (omitted non-cash adjustments)"
            ]
            q_cgo = (f"The financial records of **{co_cgo}** reflect: "
                     f"Net Profit before tax: **R{npbt_c:,.0f}**; Depreciation: **R{dep_c:,.0f}**; Interest expense: **R{int_c:,.0f}**. "
                     f"Working capital changes: Inventory change: **R{d_inv:,.0f}**; Debtors/Receivables change: **R{d_rec:,.0f}**; "
                     f"Creditors/Payables change: **R{d_pay:,.0f}**. Calculate the finalized **Cash Generated from Operations**:")
            exp_cgo = (f"1. Operating Profit before WC changes = Net Profit before Tax (R{npbt_c:,.0f}) + Depreciation (R{dep_c:,.0f}) + Interest (R{int_c:,.0f}) = R{op_prof_wc:,.0f}. "
                       f"2. Working Capital changes = R{d_inv:,.0f} + R{d_rec:,.0f} + R{d_pay:,.0f} = R{net_wc_change:,.0f}. "
                       f"3. Cash Generated from Operations = R{op_prof_wc:,.0f} + (R{net_wc_change:,.0f}) = {c_cgo}.")
            add_q("hard", "Cash Generated from Operations Reconciliation", q_cgo, c_cgo, w_cgo, "Evaluating", f"Calculate CGO for {co_cgo}", exp_cgo)

    # Multi-Asset Investing Activities Calculations (Hard)
    investing_cases = [
        ("Laysano Ltd", 850000.0, 320000.0, 140000.0, 15000.0, 100000.0),
        ("Protea Hardware Ltd", 1200000.0, 450000.0, 180000.0, -25000.0, 150000.0),
        ("Zulu Fashion Ltd", 500000.0, 190000.0, 95000.0, 10000.0, 50000.0),
        ("Metro Tech Ltd", 1800000.0, 620000.0, 240000.0, 30000.0, 200000.0),
        ("Apex Auto Ltd", 750000.0, 280000.0, 130000.0, -15000.0, 80000.0),
        ("Kairo Furnishers Ltd", 950000.0, 390000.0, 160000.0, 20000.0, 120000.0),
        ("Galaxy Appliances Ltd", 2200000.0, 750000.0, 310000.0, 45000.0, 250000.0),
        ("Bakersfield Ltd", 880000.0, 310000.0, 125000.0, -18000.0, 90000.0)
    ]

    for co_inv, bldg_add, equip_add, veh_cv_sold, veh_prof_loss, fix_dep_inc in investing_cases:
        if counts["hard"] >= 200:
            break
        # Proceeds from vehicle sold = CV + profit (or - loss)
        veh_proceeds = veh_cv_sold + veh_prof_loss
        total_investing_outflow = -(bldg_add + equip_add + fix_dep_inc) + veh_proceeds

        c_inv = f"(R{abs(total_investing_outflow):,.0f}) (Net Investing Cash Outflow)"
        w_inv = [
            f"(R{bldg_add + equip_add:,.0f}) (forgot proceeds from vehicle sale)",
            f"(R{abs(total_investing_outflow) + veh_proceeds:,.0f}) (subtracted proceeds instead of adding to cash)",
            f"(R{abs(total_investing_outflow) * 1.2:,.0f})",
            f"(R{abs(total_investing_outflow) / 2:,.0f})",
            f"R{abs(total_investing_outflow):,.0f} (treated net outflow as net inflow)",
            f"(R{bldg_add + equip_add + fix_dep_inc:,.0f})",
            f"(R{abs(total_investing_outflow) + 50000:,.0f})"
        ]
        q_inv = (f"During the financial year, **{co_inv}** incurred the following capital transactions: "
                 f"Additions to buildings: **R{bldg_add:,.0f}**; Purchase of new equipment: **R{equip_add:,.0f}**; "
                 f"Increase in fixed deposit: **R{fix_dep_inc:,.0f}**. An old delivery van with a carrying value of "
                 f"**R{veh_cv_sold:,.0f}** was sold at a **{'profit' if veh_prof_loss >= 0 else 'loss'} of R{abs(veh_prof_loss):,.0f}**. "
                 f"Calculate the **Net Cash Flow from Investing Activities**:")
        exp_inv = (f"1. Cash paid for asset purchases = Buildings (R{bldg_add:,.0f}) + Equipment (R{equip_add:,.0f}) + Fixed Deposit (R{fix_dep_inc:,.0f}) = R{bldg_add + equip_add + fix_dep_inc:,.0f} (Outflow). "
                   f"2. Cash proceeds from vehicle disposal = Carrying Value (R{veh_cv_sold:,.0f}) + Profit/Loss (R{veh_prof_loss:,.0f}) = R{veh_proceeds:,.0f} (Inflow). "
                   f"3. Net Cash Flow from Investing Activities = -R{bldg_add + equip_add + fix_dep_inc:,.0f} + R{veh_proceeds:,.0f} = {c_inv}.")
        add_q("hard", "Comprehensive Investing Activities", q_inv, c_inv, w_inv, "Evaluating", f"Calculate Net Investing Flow for {co_inv}", exp_inv)

    return questions

if __name__ == '__main__':
    qs = build_cash_flow()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_acc_cash_flow.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
