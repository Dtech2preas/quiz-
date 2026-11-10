import json
import os

def build_financial_statements():
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
        qid = f"ACC_P1_FIN_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Financial Statements & Adjustments",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Financial Statements",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # GAAP/IFRS Principles, Format & Structure of Income Statement and Balance Sheet
    # =========================================================================

    gaap_principles = [
        ("Matching Principle",
         "Expenses incurred to generate revenue during a specific financial period must be recorded in the same period as the related revenue, regardless of when cash is physically paid or received.",
         ["Assets must always be recorded at their original historical acquisition cost regardless of market value changes",
          "The personal financial affairs of the business owner must be strictly separated from the business transactions",
          "Anticipate no future profits but provide for all possible probable losses immediately",
          "Financial statements are prepared under the assumption that the enterprise will continue operating indefinitely",
          "Only financial events that can be expressed in terms of currency are recorded in the accounting books",
          "All insignificant immaterial expenses must be listed on the face of the Balance Sheet"],
         "The matching principle requires that incomes and the expenses incurred to produce them are matched in the same accounting period."),

        ("Prudence (Conservatism) Principle",
         "When preparing financial statements, accountants must exercise caution: revenue and profits are recognized only when realized, whereas liabilities and potential losses are provided for as soon as they are anticipated (e.g. Provision for Bad Debts, Inventory at lower of cost and net realizable value).",
         ["Every business transaction must affect at least two ledger accounts with equal debits and credits",
          "Financial statements assume the company will be liquidated within the next six months",
          "Revenue is recognized only when cash has been deposited directly into the bank account",
          "Expenses are deferred indefinitely until the business produces a positive gross profit",
          "All assets must be revalued to their maximum optimistic replacement value each year",
          "The owner's personal mortgage is recorded as a long-term liability of the company"],
         "Prudence requires that profits are not anticipated and provision is made for all known liabilities and expected losses."),

        ("Historical Cost Principle",
         "Assets must be originally recorded in the accounting books at their actual purchase acquisition cost price, including all costs incurred in bringing the asset to its working condition, rather than at subjective estimated market values.",
         ["Assets are revalued weekly based on current inflation indexes published by Statistics SA",
          "Expenses are matched with revenues earned in the following financial year",
          "All fixed assets are written off as immediate operating expenses in the year of purchase",
          "Liabilities must be recorded at double their actual value to maintain conservative reserves",
          "Financial statements are prepared assuming the company is currently bankrupt",
          "Debtors are recorded at the full selling price plus the expected future interest"],
         "Historical cost principle dictates that assets enter the ledger at their original transaction price."),

        ("Going Concern Assumption",
         "Financial statements are prepared on the fundamental assumption that the business entity will continue operating and meeting its legal obligations in the foreseeable future (at least 12 months) and has neither the intention nor the necessity of liquidation.",
         ["The business must close its doors and liquidate all assets at the end of each financial year",
          "Assets must immediately be written down to their distress liquidation auction values",
          "All profits made by the company must be distributed to directors within twenty-four hours",
          "The business is treated as an indivisible extension of the sole owner's private life",
          "Only cash sales may be recorded in the general ledger journals",
          "The enterprise is legally exempt from paying corporate income tax to SARS"],
         "The going concern principle assumes that the business will remain in operational existence for the foreseeable future."),

        ("Business Entity Rule",
         "The economic and financial transactions of the business must be kept completely separate from the personal financial affairs of the owners, shareholders, or directors.",
         ["The personal grocery purchases of directors must be recorded as company operating expenses",
          "The business and the owner are legally and financially identical in corporate accounting",
          "Company bank accounts may be freely used for private household utility bill payments",
          "Shareholders must лично pay all trade creditor invoices using their private credit cards",
          "All private assets of shareholders must be included on the company Statement of Financial Position",
          "The company does not require its own dedicated bank account or tax registration"],
         "The business entity rule strictly isolates business finances from personal financial activities."),

        ("Materiality Principle",
         "Information is material and must be separately disclosed in financial reports if its omission, misstatement, or obscurity could reasonably be expected to influence the economic decisions of users taken on the basis of those financial statements.",
         ["Every small box of paperclips purchased must be listed as a separate non-current tangible asset",
          "Materiality requires that only transactions exceeding ten million Rand are recorded",
          "Financial statements must only disclose cash transactions and omit all credit transactions",
          "All assets must be rounded to the nearest billion Rand regardless of company size",
          "Auditors are prohibited from examining any transaction with a value below R100,000",
          "Materiality dictates that all expenses are combined into a single undisclosed figure"],
         "Materiality ensures that significant financial information capable of affecting users' decisions is disclosed."),

        ("Consistency Principle",
         "Accounting policies, procedures, and valuation methods (such as depreciation methods and inventory valuation methods like FIFO or Weighted Average) must be applied consistently from one financial period to the next to enable meaningful comparison over time.",
         ["A company must change its inventory valuation method every month",
          "Financial statements must be compiled using different currencies each quarter",
          "All fixed assets must be written off in full every second year",
          "Companies are prohibited from presenting comparative figures from the previous year",
          "Depreciation rates must be altered weekly depending on rainfall",
          "The company may choose arbitrary accounting rules for each separate ledger account"],
         "Consistency requires that accounting methods are applied uniformly from year to year to allow valid financial comparisons."),

        ("Accrual Principle",
         "Transactions and economic events are recognized when they occur (when goods are delivered or services rendered) rather than when cash or its equivalent is actually received or paid.",
         ["Revenues can only be recorded when physical banknotes are received in the cash register",
          "Credit sales are never recognized in corporate financial statements",
          "Expenses are only recognized after an auditor signs the annual report",
          "Transactions are recorded exclusively on the date the supplier issues a receipt",
          "All liabilities are ignored until legal summons are served by a magistrate",
          "Cash accounting is the mandatory system for all listed public companies in SA"],
         "The accrual principle dictates that revenues and expenses are recorded in the period they occur, not when cash moves."),

        ("Prudence applied to Trading Stock (Lower of Cost and Net Realisable Value)",
         "Trading stock must be valued at the lower of its historical cost price or its net realizable value (estimated selling price less completion and selling costs) to prevent overstating current assets and profits.",
         ["Trading stock must always be valued at its highest optimistic future selling price",
          "Damaged and obsolete stock must be doubled in value on the balance sheet",
          "Inventory is recorded at zero on the balance sheet at all times",
          "Trading stock is valued based on the original invoice price plus 100% markup",
          "Stock is revalued upwards whenever competitor prices increase",
          "The value of trading stock is determined exclusively by the store floor manager"],
         "Under prudence, trading stock is carried at the lower of historical cost or net realizable value."),

        ("Capital Expenditure vs Revenue Expenditure",
         "Capital expenditure is spending incurred to acquire, replace, or enhance non-current assets and generate long-term benefits (capitalized on Balance Sheet); Revenue expenditure is spending incurred for routine operation, repair, and maintenance (expensed in Income Statement).",
         ["Capital expenditure is recorded as an operating expense in the Income Statement",
          "Purchasing a delivery truck is classified as routine revenue expenditure",
          "Servicing an engine and changing engine oil is capitalized as a fixed asset",
          "Revenue expenditure increases the carrying value of tangible assets on the Balance Sheet",
          "Both capital and revenue expenditures are deducted directly from Retained Income",
          "Capital expenditure is strictly illegal under the South African Companies Act"],
         "Capital expenditure creates long-term assets (Balance Sheet); Revenue expenditure covers day-to-day running costs (Income Statement)."),

        ("Division / Separation of Duties",
         "An internal control principle where key operational responsibilities—such as authorization, execution, custody of assets, and recording of transactions—are allocated to separate individuals to minimize fraud, collusion, and errors.",
         ["One single accountant should write cheques, sign cheques, and perform the bank reconciliation alone",
          "The cashier who receives cash should also be the sole person to write off bad debts",
          "All employees in the firm should have administrative password access to the general ledger",
          "Internal controls require that all tasks are performed by outside contractors only",
          "No documentation or audit trail should ever be retained in the accounting office",
          "The warehouse receiver should also authorize purchase orders and approve supplier invoices"],
         "Separation of duties ensures no single person controls all phases of a transaction, reducing risk of fraud and error.")
    ]

    for princ_name, princ_corr, princ_wrongs, princ_expl in gaap_principles:
        for st_p in [
            f"In Grade 12 Accounting, what is the core meaning and application of the **'{princ_name}'**?",
            f"Which statement accurately explains the **'{princ_name}'** in corporate financial reporting?",
            f"Under South African CAPS Accounting standards, the **'{princ_name}'** states that:",
            f"When compiling company financial statements, the **'{princ_name}'** requires that:"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "GAAP & IFRS Principles", st_p, princ_corr, princ_wrongs, "Remembering", f"Define {princ_name}", princ_expl)

    # Classification of Accounts in Financial Statements (Easy)
    account_classifications = [
        ("Trading Stock Deficit", "Operating Expense", "Statement of Comprehensive Income (Operating Expenses)"),
        ("Provision for Bad Debts Adjustment (increase)", "Operating Expense", "Statement of Comprehensive Income (Operating Expenses)"),
        ("Provision for Bad Debts Adjustment (decrease)", "Other Operating Income", "Statement of Comprehensive Income (Other Operating Income)"),
        ("Bad Debts Recovered", "Other Operating Income", "Statement of Comprehensive Income (Other Operating Income)"),
        ("Rent Income (adjusted for prepaid/accrued)", "Other Operating Income", "Statement of Comprehensive Income (Other Operating Income)"),
        ("Directors' Fees", "Operating Expense", "Statement of Comprehensive Income (Operating Expenses)"),
        ("Audit Fees", "Operating Expense", "Statement of Comprehensive Income (Operating Expenses)"),
        ("Consumable Stores on Hand (at year-end)", "Current Asset", "Statement of Financial Position under Trade and Other Receivables"),
        ("Accrued Income (Income receivable)", "Current Asset", "Statement of Financial Position under Trade and Other Receivables"),
        ("Prepaid Expenses (Expenses paid in advance)", "Current Asset", "Statement of Financial Position under Trade and Other Receivables"),
        ("Income Received in Advance (Deferred Revenue)", "Current Liability", "Statement of Financial Position under Trade and Other Payables"),
        ("Accrued Expenses (Expenses payable)", "Current Liability", "Statement of Financial Position under Trade and Other Payables"),
        ("Shareholders for Dividends", "Current Liability", "Statement of Financial Position under Trade and Other Payables"),
        ("SARS: Income Tax (Credit balance)", "Current Liability", "Statement of Financial Position under Trade and Other Payables"),
        ("SARS: Income Tax (Debit balance)", "Current Asset", "Statement of Financial Position under Trade and Other Receivables"),
        ("Fixed Deposit maturing in 6 months", "Current Asset", "Statement of Financial Position under Cash and Cash Equivalents"),
        ("Fixed Deposit maturing in 3 years", "Non-Current Asset", "Statement of Financial Position under Financial Assets"),
        ("Bank Overdraft", "Current Liability", "Statement of Financial Position under Cash and Cash Equivalents (or Trade & Other Payables)"),
        ("Mortgage Loan (portion repayable within 12 months)", "Current Liability", "Statement of Financial Position under Short-term portion of loan / Current Liabilities"),
        ("Mortgage Loan (portion repayable after 12 months)", "Non-Current Liability", "Statement of Financial Position under Non-Current Liabilities")
    ]

    for acc_name, acc_type, acc_location in account_classifications:
        for st_ac in [
            f"How is the account **'{acc_name}'** classified and presented in the financial statements?",
            f"In which section of the financial statements does **'{acc_name}'** appear?",
            f"Identify the correct accounting classification for **'{acc_name}'**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_ac = f"{acc_type}: Presented in the {acc_location}."
            w_ac = [
                f"{'Current Liability' if acc_type != 'Current Liability' else 'Non-Current Asset'}: Presented in the Statement of Changes in Equity.",
                f"{'Operating Expense' if acc_type != 'Operating Expense' else 'Other Operating Income'}: Deducted directly from Ordinary Share Capital.",
                "Non-Operating Capital Reserve: Disclosed solely in the Director's Chairman Report.",
                "Tax Exemption Allowance: Credited directly to the General Reserve.",
                "Contingent Liability: Recorded as an off-balance sheet narrative footnote only.",
                "Fictitious Asset: Written off against preliminary incorporation expenses."
            ]
            expl_ac = f"{acc_name} is classified as a {acc_type} and is shown in the {acc_location}."
            add_q("easy", "Financial Statement Classification", st_ac, c_ac, w_ac, "Understanding", f"Classify {acc_name}", expl_ac)

    # Basic Direct Level 1 Income Statement Calculations (Easy)
    # Markup, Gross profit, Income tax, Net profit
    basic_calc_scenarios = [
        ("Lindiwe Retailers Ltd", 2000000.0, 50.0),
        ("Protea Hardware Ltd", 4500000.0, 60.0),
        ("Kairo Furnishers Ltd", 3600000.0, 50.0),
        ("Zulu Fashion Ltd", 1800000.0, 80.0),
        ("Metro Tech Ltd", 5000000.0, 25.0),
        ("Apex Auto Spares Ltd", 2400000.0, 60.0),
        ("Orchid Boutique Ltd", 1500000.0, 100.0),
        ("Galaxy Appliances Ltd", 6000000.0, 50.0),
        ("Oasis General Dealers Ltd", 3000000.0, 75.0),
        ("Bakersfield Ltd", 4000000.0, 60.0),
        ("Tshwane Traders Ltd", 2800000.0, 40.0),
        ("Durban Wholesale Ltd", 7200000.0, 50.0),
        ("Cape Coast Ltd", 3500000.0, 75.0),
        ("Limpopo Merchants Ltd", 1600000.0, 60.0),
        ("Highveld Stores Ltd", 4800000.0, 50.0),
        ("Sandton Luxury Goods Ltd", 9000000.0, 100.0),
        ("Bloemfontein Traders Ltd", 3200000.0, 60.0),
        ("Polokwane Distributors Ltd", 2100000.0, 40.0),
        ("Nelspruit Fruit Supply Ltd", 1750000.0, 25.0),
        ("Kimberley Diamond Tools Ltd", 4200000.0, 50.0),
        ("Rustenburg Industrial Supplies Ltd", 5400000.0, 80.0),
        ("Port Elizabeth Logistics Ltd", 6300000.0, 50.0),
        ("Pietermaritzburg Textiles Ltd", 2600000.0, 60.0),
        ("Soweto Commercial Ltd", 3800000.0, 50.0),
        ("Midrand Electronics Ltd", 8400000.0, 75.0),
        ("Centurion Sports Ltd", 1950000.0, 50.0),
        ("East London Timber Ltd", 2900000.0, 45.0),
        ("George Garden Supplies Ltd", 1350000.0, 50.0),
        ("Kroonstad Grain Merchants Ltd", 4600000.0, 25.0),
        ("Stellenbosch Wine Cellars Ltd", 5800000.0, 100.0),
        ("Upington Sun Trading Ltd", 2250000.0, 50.0)
    ]

    for co_name, sales_amt, markup_pct in basic_calc_scenarios:
        if counts["easy"] >= 300:
            break
        # Cost of sales = Sales / (1 + markup/100)
        cos_amt = sales_amt / (1.0 + (markup_pct / 100.0))
        gp_amt = sales_amt - cos_amt

        # 1. Calculate Cost of Sales
        c_cos = f"R{cos_amt:,.0f}"
        w_cos = [
            f"R{sales_amt * (1.0 + markup_pct/100.0):,.0f} (multiplied instead of dividing by 1 + markup)",
            f"R{sales_amt * (markup_pct/100.0):,.0f} (calculated gross profit instead of cost of sales)",
            f"R{sales_amt - (sales_amt * markup_pct/100.0):,.0f}",
            f"R{cos_amt * 1.5:,.0f}",
            f"R{cos_amt * 0.8:,.0f}",
            f"R{cos_amt + 200000:,.0f}",
            f"R{sales_amt:,.0f}"
        ]
        q_cos = (f"**{co_name}** achieved total sales of **R{sales_amt:,.0f}** for the financial year. The company applies a consistent "
                 f"mark-up of **{markup_pct:.0f}% on cost**. Calculate the **Cost of Sales**:")
        exp_cos = f"Cost of Sales = Sales / (1 + Markup%) = R{sales_amt:,.0f} / (1 + {markup_pct/100:.2f}) = {c_cos}."
        add_q("easy", "Basic Trading Calculations", q_cos, c_cos, w_cos, "Applying", f"Calculate Cost of Sales for {co_name}", exp_cos)

        # 2. Calculate Gross Profit
        if counts["easy"] < 300:
            c_gp = f"R{gp_amt:,.0f}"
            w_gp = [
                f"R{cos_amt:,.0f} (confused Cost of Sales with Gross Profit)",
                f"R{sales_amt * 0.10:,.0f}",
                f"R{gp_amt * 1.2:,.0f}",
                f"R{gp_amt / 2:,.0f}",
                f"R{sales_amt + gp_amt:,.0f}",
                f"R{gp_amt - 150000:,.0f}",
                f"R{sales_amt * (markup_pct/100.0) * 1.5:,.0f}"
            ]
            q_gp = (f"**{co_name}** recorded Sales of **R{sales_amt:,.0f}** with a mark-up of **{markup_pct:.0f}% on cost** "
                    f"(Cost of Sales = R{cos_amt:,.0f}). Determine the **Gross Profit**:")
            exp_gp = f"Gross Profit = Sales - Cost of Sales = R{sales_amt:,.0f} - R{cos_amt:,.0f} = {c_gp}."
            add_q("easy", "Basic Trading Calculations", q_gp, c_gp, w_gp, "Applying", f"Calculate Gross Profit for {co_name}", exp_gp)

        # 3. Calculate Company Income Tax at 27%
        if counts["easy"] < 300:
            pbt_sample = round(gp_amt * 0.45, -3)
            tax_27 = pbt_sample * 0.27
            np_after_tax = pbt_sample - tax_27
            c_tax = f"R{tax_27:,.0f}"
            w_tax = [
                f"R{pbt_sample * 0.28:,.0f} (used obsolete 28% tax rate instead of 27%)",
                f"R{pbt_sample * 0.15:,.0f} (confused 27% income tax with 15% VAT rate)",
                f"R{np_after_tax:,.0f} (confused tax with net profit after tax)",
                f"R{tax_27 * 1.5:,.0f}",
                f"R{tax_27 / 2:,.0f}",
                f"R{pbt_sample:,.0f}",
                f"R{tax_27 + 50000:,.0f}"
            ]
            q_tax = (f"**{co_name}** generated a Net Profit before tax of **R{pbt_sample:,.0f}**. Given that corporate income tax is levied "
                     f"at the standard rate of **27%**, calculate the Income Tax expense for the year:")
            exp_tax = f"Income Tax = Net Profit before Tax × 27% = R{pbt_sample:,.0f} × 0.27 = {c_tax}."
            add_q("easy", "Income Tax Calculation", q_tax, c_tax, w_tax, "Applying", f"Calculate Income Tax for {co_name}", exp_tax)

    # Markup on Cost vs Gross Margin on Sales Conversions (Easy)
    markup_margin_pairs = [
        (25.0, 20.0),
        (33.333333, 25.0),
        (50.0, 33.333333),
        (60.0, 37.5),
        (66.666667, 40.0),
        (75.0, 42.857143),
        (100.0, 50.0),
        (150.0, 60.0),
        (200.0, 66.666667)
    ]
    for mk_c, mg_s in markup_margin_pairs:
        # Type 1: Markup on cost -> Gross margin on sales
        if counts["easy"] < 300:
            c_m1 = f"{mg_s:.1f}% on sales"
            w_m1 = [
                f"{mk_c:.1f}% on sales (assumed markup on cost equals margin on sales)",
                f"{mg_s * 1.5:.1f}% on sales",
                f"{mg_s / 2:.1f}% on sales",
                f"{100.0 - mg_s:.1f}% on sales",
                f"{mg_s + 10.0:.1f}% on sales",
                f"{mk_c / 2:.1f}% on sales",
                f"{mg_s * 2:.1f}% on sales"
            ]
            q_m1 = f"If a business applies a mark-up of **{mk_c:.1f}% on cost**, calculate the equivalent **Gross Margin percentage on Sales**:"
            exp_m1 = f"Margin on Sales = [Markup / (100 + Markup)] × 100 = [{mk_c:.1f} / {100 + mk_c:.1f}] × 100 = {c_m1}."
            add_q("easy", "Markup & Margin Conversions", q_m1, c_m1, w_m1, "Applying", "Convert Markup on Cost to Margin on Sales", exp_m1)

        # Type 2: Margin on sales -> Markup on cost
        if counts["easy"] < 300:
            c_m2 = f"{mk_c:.1f}% on cost"
            w_m2 = [
                f"{mg_s:.1f}% on cost (assumed margin on sales equals markup on cost)",
                f"{mk_c * 1.5:.1f}% on cost",
                f"{mk_c / 2:.1f}% on cost",
                f"{100.0 - mk_c if mk_c < 100 else 45.0:.1f}% on cost",
                f"{mk_c + 15.0:.1f}% on cost",
                f"{mg_s * 2:.1f}% on cost",
                f"{mk_c * 0.8:.1f}% on cost"
            ]
            q_m2 = f"A retail enterprise achieves a **Gross Profit Margin of {mg_s:.1f}% on Sales**. Calculate the business's **Mark-up percentage on Cost**:"
            exp_m2 = f"Markup on Cost = [Margin / (100 - Margin)] × 100 = [{mg_s:.1f} / {100 - mg_s:.1f}] × 100 = {c_m2}."
            add_q("easy", "Markup & Margin Conversions", q_m2, c_m2, w_m2, "Applying", "Convert Margin on Sales to Markup on Cost", exp_m2)

    # Working Capital & Capital Employed Fundamentals (Easy)
    working_cap_cases = [
        ("Laysano Ltd", 1450000.0, 620000.0, 4800000.0, 1500000.0),
        ("Protea Hardware Ltd", 2100000.0, 950000.0, 6500000.0, 2000000.0),
        ("Zulu Fashion Ltd", 880000.0, 390000.0, 3200000.0, 1000000.0),
        ("Metro Tech Ltd", 3400000.0, 1600000.0, 9800000.0, 3500000.0),
        ("Apex Auto Ltd", 1750000.0, 780000.0, 5200000.0, 1800000.0),
        ("Kairo Furnishers Ltd", 2600000.0, 1150000.0, 7400000.0, 2200000.0),
        ("Orchid Boutique Ltd", 720000.0, 310000.0, 2400000.0, 800000.0),
        ("Galaxy Appliances Ltd", 4100000.0, 1900000.0, 11500000.0, 4000000.0),
        ("Bakersfield Ltd", 1900000.0, 820000.0, 5600000.0, 1600000.0),
        ("Tshwane Traders Ltd", 1600000.0, 740000.0, 4900000.0, 1500000.0),
        ("Cape Coast Ltd", 1850000.0, 860000.0, 5400000.0, 1700000.0),
        ("Durban Wholesale Ltd", 3800000.0, 1750000.0, 10500000.0, 3200000.0),
        ("Sandton Goods Ltd", 4500000.0, 2100000.0, 12800000.0, 4500000.0),
        ("Bloemfontein Traders Ltd", 1950000.0, 880000.0, 5700000.0, 1800000.0),
        ("Polokwane Supply Ltd", 1400000.0, 610000.0, 4200000.0, 1200000.0)
    ]

    for co_wc, ca_val, cl_val, eq_val, ncl_val in working_cap_cases:
        # 1. Working Capital = CA - CL
        if counts["easy"] < 300:
            net_wc = ca_val - cl_val
            c_wc = f"R{net_wc:,.0f}"
            w_wc = [
                f"R{ca_val + cl_val:,.0f} (added Current Liabilities instead of subtracting)",
                f"R{ca_val:,.0f} (confused Total Current Assets with Working Capital)",
                f"R{cl_val:,.0f}",
                f"R{net_wc * 1.5:,.0f}",
                f"R{net_wc / 2:,.0f}",
                f"R{net_wc + 100000:,.0f}",
                f"R{ca_val / cl_val:.2f}"
            ]
            q_wc = (f"The Balance Sheet records of **{co_wc}** show Current Assets of **R{ca_val:,.0f}** and Current Liabilities of "
                    f"**R{cl_val:,.0f}**. Calculate the **Net Working Capital** of the enterprise:")
            exp_wc = f"Working Capital = Current Assets - Current Liabilities = R{ca_val:,.0f} - R{cl_val:,.0f} = {c_wc}."
            add_q("easy", "Working Capital Fundamentals", q_wc, c_wc, w_wc, "Applying", f"Calculate Working Capital for {co_wc}", exp_wc)

        # 2. Capital Employed = Equity + Non-Current Liabilities
        if counts["easy"] < 300:
            cap_emp = eq_val + ncl_val
            c_ce = f"R{cap_emp:,.0f}"
            w_ce = [
                f"R{eq_val - ncl_val:,.0f} (subtracted loan instead of adding to equity)",
                f"R{eq_val:,.0f} (only counted Shareholders' Equity)",
                f"R{ncl_val:,.0f} (only counted Non-Current Liabilities)",
                f"R{cap_emp * 1.2:,.0f}",
                f"R{cap_emp / 2:,.0f}",
                f"R{cap_emp + 250000:,.0f}",
                f"R{eq_val + ncl_val + cl_val:,.0f}"
            ]
            q_ce = (f"**{co_wc}** reports Shareholders' Equity of **R{eq_val:,.0f}** and a Non-Current Mortgage Loan of **R{ncl_val:,.0f}**. "
                    f"Calculate the **Total Capital Employed** in the business:")
            exp_ce = f"Capital Employed = Shareholders' Equity + Non-Current Liabilities = R{eq_val:,.0f} + R{ncl_val:,.0f} = {c_ce}."
            add_q("easy", "Capital Employed Fundamentals", q_ce, c_ce, w_ce, "Applying", f"Calculate Capital Employed for {co_wc}", exp_ce)

    # Accounting Equation Determinations: Assets = Equity + Liabilities (Easy)
    accounting_equation_cases = [
        ("Laysano Ltd", 6850000.0, 4800000.0, 2050000.0),
        ("Protea Hardware Ltd", 9450000.0, 6500000.0, 2950000.0),
        ("Zulu Fashion Ltd", 4590000.0, 3200000.0, 1390000.0),
        ("Metro Tech Ltd", 14900000.0, 9800000.0, 5100000.0),
        ("Apex Auto Ltd", 7780000.0, 5200000.0, 2580000.0),
        ("Kairo Furnishers Ltd", 10750000.0, 7400000.0, 3350000.0),
        ("Orchid Boutique Ltd", 3510000.0, 2400000.0, 1110000.0),
        ("Galaxy Appliances Ltd", 17400000.0, 11500000.0, 5900000.0),
        ("Bakersfield Ltd", 8020000.0, 5600000.0, 2420000.0),
        ("Tshwane Traders Ltd", 7140000.0, 4900000.0, 2240000.0),
        ("Cape Coast Ltd", 7960000.0, 5400000.0, 2560000.0),
        ("Durban Wholesale Ltd", 15450000.0, 10500000.0, 4950000.0),
        ("Sandton Goods Ltd", 19400000.0, 12800000.0, 6600000.0),
        ("Bloemfontein Traders Ltd", 8380000.0, 5700000.0, 2680000.0),
        ("Polokwane Supply Ltd", 6010000.0, 4200000.0, 1810000.0),
        ("Nelspruit Supply Ltd", 5250000.0, 3700000.0, 1550000.0),
        ("Kimberley Tools Ltd", 8900000.0, 6100000.0, 2800000.0),
        ("Rustenburg Industrial Ltd", 11200000.0, 7900000.0, 3300000.0),
        ("Port Elizabeth Logistics Ltd", 13500000.0, 9200000.0, 4300000.0),
        ("Pietermaritzburg Ltd", 6900000.0, 4800000.0, 2100000.0)
    ]

    for co_eq, tot_assets, tot_equity, tot_liab in accounting_equation_cases:
        # Determine Liabilities = Assets - Equity
        if counts["easy"] < 300:
            c_eq_l = f"R{tot_liab:,.0f}"
            w_eq_l = [
                f"R{tot_assets + tot_equity:,.0f}",
                f"R{tot_assets:,.0f}",
                f"R{tot_equity:,.0f}",
                f"R{tot_liab * 1.5:,.0f}",
                f"R{tot_liab / 2:,.0f}",
                f"R{tot_liab + 200000:,.0f}",
                f"R{tot_equity - tot_liab:,.0f}"
            ]
            q_eq_l = (f"According to the basic accounting equation (Assets = Equity + Liabilities), if **{co_eq}** has Total Assets of "
                      f"**R{tot_assets:,.0f}** and Shareholders' Equity of **R{tot_equity:,.0f}**, determine **Total Liabilities**:")
            exp_eq_l = f"Liabilities = Total Assets - Shareholders' Equity = R{tot_assets:,.0f} - R{tot_equity:,.0f} = {c_eq_l}."
            add_q("easy", "Accounting Equation Determinations", q_eq_l, c_eq_l, w_eq_l, "Applying", f"Calculate Liabilities for {co_eq}", exp_eq_l)

        # Determine Equity = Assets - Liabilities
        if counts["easy"] < 300:
            c_eq_e = f"R{tot_equity:,.0f}"
            w_eq_e = [
                f"R{tot_assets + tot_liab:,.0f}",
                f"R{tot_assets:,.0f}",
                f"R{tot_liab:,.0f}",
                f"R{tot_equity * 1.2:,.0f}",
                f"R{tot_equity / 2:,.0f}",
                f"R{tot_equity + 300000:,.0f}",
                f"R{tot_assets - (tot_liab / 2):,.0f}"
            ]
            q_eq_e = (f"If **{co_eq}** reflects Total Assets of **R{tot_assets:,.0f}** and Total Liabilities of **R{tot_liab:,.0f}**, "
                      f"calculate **Shareholders' Equity** using the fundamental accounting equation:")
            exp_eq_e = f"Equity = Total Assets - Total Liabilities = R{tot_assets:,.0f} - R{tot_liab:,.0f} = {c_eq_e}."
            add_q("easy", "Accounting Equation Determinations", q_eq_e, c_eq_e, w_eq_e, "Applying", f"Calculate Equity for {co_eq}", exp_eq_e)

        # Determine Total Assets = Equity + Liabilities
        if counts["easy"] < 300:
            c_eq_a = f"R{tot_assets:,.0f}"
            w_eq_a = [
                f"R{tot_equity - tot_liab:,.0f}",
                f"R{tot_equity:,.0f}",
                f"R{tot_liab:,.0f}",
                f"R{tot_assets * 1.2:,.0f}",
                f"R{tot_assets / 2:,.0f}",
                f"R{tot_assets + 250000:,.0f}",
                f"R{tot_equity * 2:,.0f}"
            ]
            q_eq_a = (f"In the records of **{co_eq}**, Shareholders' Equity stands at **R{tot_equity:,.0f}** and Total Liabilities "
                      f"equal **R{tot_liab:,.0f}**. Calculate **Total Assets** using the basic accounting equation:")
            exp_eq_a = f"Total Assets = Shareholders' Equity + Total Liabilities = R{tot_equity:,.0f} + R{tot_liab:,.0f} = {c_eq_a}."
            add_q("easy", "Accounting Equation Determinations", q_eq_a, c_eq_a, w_eq_a, "Applying", f"Calculate Assets for {co_eq}", exp_eq_a)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Real DBE Year-End Adjustments (Trading Stock Deficit, Provision for Bad Debts,
    # Rent Prepaid/Accrued, Depreciation Straight-Line vs Diminishing Balance, Working Capital Notes)
    # =========================================================================

    # 1. Trading Stock Deficit / Surplus Adjustments (Medium)
    stock_deficit_scenarios = [
        ("Laysano Ltd", 480000.0, 462500.0, "physical stock count revealed missing units due to shoplifting"),
        ("Protea Hardware Ltd", 850000.0, 836000.0, "periodic physical inventory count at year-end"),
        ("Zulu Fashion Ltd", 320000.0, 311500.0, "stocktake revealed damaged and unaccounted stock"),
        ("Metro Tech Ltd", 1250000.0, 1238000.0, "physical count on 28 February"),
        ("Apex Auto Ltd", 640000.0, 629000.0, "physical verification of replacement auto parts"),
        ("Kairo Furnishers Ltd", 910000.0, 895000.0, "damaged furniture items discarded without journal entry"),
        ("Orchid Boutique Ltd", 275000.0, 269200.0, "physical inventory count completed by external checkers"),
        ("Galaxy Electronics Ltd", 1480000.0, 1461000.0, "audit stocktake discrepancy at year-end"),
        ("Bakersfield Ltd", 530000.0, 521400.0, "annual physical stock inspection"),
        ("Tshwane Traders Ltd", 720000.0, 708500.0, "routine annual stock count on 30 June"),
        ("Cape Coast Ltd", 390000.0, 384200.0, "inventory audit discrepancy"),
        ("Durban Wholesale Ltd", 1650000.0, 1632000.0, "warehouse physical verification"),
        ("Highveld Stores Ltd", 810000.0, 799000.0, "stock count on the final day of the financial year"),
        ("Limpopo Merchants Ltd", 440000.0, 432500.0, "inventory recount following minor flooding"),
        ("Oasis Dealers Ltd", 590000.0, 581800.0, "year-end stocktaking count")
    ]

    for co_stk, ledger_val, count_val, rsn_stk in stock_deficit_scenarios:
        deficit_amt = ledger_val - count_val
        c_def = f"R{deficit_amt:,.0f} Trading Stock Deficit (Operating Expense)"
        w_def = [
            f"R{deficit_amt:,.0f} Trading Stock Surplus (Operating Income)",
            f"R{count_val:,.0f} (confused physical count with the deficit)",
            f"R{ledger_val:,.0f} (confused ledger balance with the deficit)",
            f"R{ledger_val + count_val:,.0f}",
            f"R{deficit_amt * 2:,.0f}",
            f"R{deficit_amt / 2:,.0f}",
            f"R{deficit_amt + 5000:,.0f}"
        ]
        q_stk = (f"The Trial Balance of **{co_stk}** at year-end shows Trading Stock of **R{ledger_val:,.0f}**. A {rsn_stk} "
                 f"valued the trading stock on hand at **R{count_val:,.0f}**. Determine the required year-end adjustment and its presentation:")
        exp_stk = (f"Trading Stock Deficit = Ledger Balance - Physical Count = R{ledger_val:,.0f} - R{count_val:,.0f} = R{deficit_amt:,.0f}. "
                   f"This deficit is recognized as an Operating Expense in the Statement of Comprehensive Income, reducing stock in the Balance Sheet.")
        add_q("medium", "Trading Stock Adjustments", q_stk, c_def, w_def, "Applying", f"Calculate Trading Stock Deficit for {co_stk}", exp_stk)

    # 2. Provision for Bad Debts Adjustment (Medium)
    pbd_scenarios = [
        ("Laysano Ltd", 240000.0, 8000.0, 0.05, 10500.0),
        ("Protea Hardware Ltd", 450000.0, 15000.0, 0.05, 23000.0),
        ("Zulu Fashion Ltd", 180000.0, 5000.0, 0.05, 7800.0),
        ("Metro Tech Ltd", 620000.0, 20000.0, 0.05, 32500.0),
        ("Apex Auto Ltd", 310000.0, 10000.0, 0.05, 13800.0),
        ("Kairo Furnishers Ltd", 520000.0, 25000.0, 0.05, 26000.0),
        ("Orchid Boutique Ltd", 140000.0, 4000.0, 0.05, 6200.0),
        ("Galaxy Appliances Ltd", 800000.0, 30000.0, 0.05, 41000.0),
        ("Bakersfield Ltd", 360000.0, 12000.0, 0.05, 16500.0),
        ("Tshwane Traders Ltd", 290000.0, 10000.0, 0.05, 15400.0),
        ("Cape Coast Ltd", 410000.0, 14000.0, 0.05, 18500.0),
        ("Durban Wholesale Ltd", 750000.0, 26000.0, 0.05, 38000.0)
    ]

    for co_pbd, debt_ctrl, add_bad, target_pct, old_pbd in pbd_scenarios:
        good_debtors = debt_ctrl - add_bad
        new_pbd = good_debtors * target_pct
        diff_pbd = new_pbd - old_pbd

        if diff_pbd > 0:
            c_pbd = f"Increase of R{diff_pbd:,.0f} (Operating Expense)"
            expl_pbd = (f"1. Adjusted Debtors = R{debt_ctrl:,.0f} - R{add_bad:,.0f} = R{good_debtors:,.0f}. "
                        f"2. New Provision = R{good_debtors:,.0f} × {target_pct*100:.0f}% = R{new_pbd:,.0f}. "
                        f"3. Adjustment = R{new_pbd:,.0f} - R{old_pbd:,.0f} = Increase of R{diff_pbd:,.0f} (Operating Expense).")
        else:
            diff_abs = abs(diff_pbd)
            c_pbd = f"Decrease of R{diff_abs:,.0f} (Other Operating Income)"
            expl_pbd = (f"1. Adjusted Debtors = R{debt_ctrl:,.0f} - R{add_bad:,.0f} = R{good_debtors:,.0f}. "
                        f"2. New Provision = R{good_debtors:,.0f} × {target_pct*100:.0f}% = R{new_pbd:,.0f}. "
                        f"3. Adjustment = R{old_pbd:,.0f} - R{new_pbd:,.0f} = Decrease of R{diff_abs:,.0f} (Other Operating Income).")

        w_pbd = [
            f"Increase of R{debt_ctrl * target_pct:,.0f} (forgot to deduct additional bad debts)",
            f"R{new_pbd:,.0f} (confused the new balance with the adjustment amount)",
            f"Decrease of R{abs(diff_pbd) + 2000:,.0f}",
            f"Increase of R{abs(diff_pbd) + 3500:,.0f}",
            f"R{good_debtors:,.0f} (treated entire net debtors as provision)",
            f"Decrease of R{add_bad:,.0f} (confused bad debt write-off with provision adjustment)",
            f"Increase of R{diff_pbd * 2:,.0f}"
        ]
        q_pbd = (f"The records of **{co_pbd}** show Debtors Control of **R{debt_ctrl:,.0f}** and Provision for Bad Debts of **R{old_pbd:,.0f}**. "
                 f"An insolvent debtor who owes **R{add_bad:,.0f}** must be written off as irrecoverable. The provision must then be adjusted "
                 f"to **{target_pct*100:.0f}% of good debtors**. Calculate the Provision for Bad Debts adjustment and state its presentation:")
        add_q("medium", "Provision for Bad Debts Adjustments", q_pbd, c_pbd, w_pbd, "Applying", f"Calculate Provision for Bad Debts adjustment for {co_pbd}", expl_pbd)

    # 3. Rent Income Adjustments with Mid-Year Rent Increases (Medium)
    # E.g. Rent increased by 10% on 1 Dec; FY ends 28 Feb (12 months = 9 months old rent, 3 months new rent + prepaid/accrued)
    rent_increase_scenarios = [
        ("Laysano Ltd", 183600.0, 10.0, "1 December", 1), # 1 month prepaid (received for March)
        ("Protea Hardware Ltd", 243800.0, 10.0, "1 November", 1),
        ("Zulu Fashion Ltd", 146400.0, 15.0, "1 December", 1),
        ("Metro Tech Ltd", 312000.0, 10.0, "1 January", 1),
        ("Apex Auto Ltd", 195500.0, 15.0, "1 November", 1),
        ("Kairo Furnishers Ltd", 224400.0, 10.0, "1 December", 1),
        ("Orchid Boutique Ltd", 126500.0, 10.0, "1 December", 1),
        ("Galaxy Appliances Ltd", 374000.0, 10.0, "1 November", 1),
        ("Bakersfield Ltd", 168300.0, 10.0, "1 December", 1),
        ("Tshwane Traders Ltd", 217800.0, 10.0, "1 January", 1)
    ]

    for co_r, tot_rent_rec, inc_pct, inc_date, prep_months in rent_increase_scenarios:
        # Let's say financial year ends 28 February (12 months).
        # If inc_date == "1 December", there are 9 months at original rent R, and (3 + prep_months) months at (1 + inc_pct/100)*R
        if "December" in inc_date:
            m_old = 9
            m_new = 3 + prep_months
        elif "November" in inc_date:
            m_old = 8
            m_new = 4 + prep_months
        else: # January
            m_old = 10
            m_new = 2 + prep_months

        mult_new = 1.0 + (inc_pct / 100.0)
        # tot_rent_rec = m_old * R + m_new * (R * mult_new) = R * (m_old + m_new * mult_new)
        eq_months = m_old + (m_new * mult_new)
        r_base = tot_rent_rec / eq_months
        r_new = r_base * mult_new
        prepaid_amt = prep_months * r_new
        earned_rent = tot_rent_rec - prepaid_amt

        c_rent = f"R{prepaid_amt:,.0f} Prepaid Income (Current Liability); Earned Rent = R{earned_rent:,.0f}"
        w_rent = [
            f"R{prepaid_amt:,.0f} Accrued Income (Current Asset); Earned Rent = R{tot_rent_rec + prepaid_amt:,.0f}",
            f"R{tot_rent_rec / 12:,.0f} (divided total rent evenly by 12 without accounting for the {inc_pct:.0f}% increase)",
            f"R{prepaid_amt * 2:,.0f} Prepaid Income",
            f"R{prepaid_amt / 2:,.0f} Accrued Income",
            f"R{r_base:,.0f} Prepaid Income (used old rent rate instead of new rent rate)",
            f"R{prepaid_amt + 3000:,.0f} Prepaid Income",
            f"R{earned_rent:,.0f} Prepaid Income (confused earned rent with prepaid portion)"
        ]
        q_rent = (f"The financial year of **{co_r}** ends on **28 February**. Total Rent Income received according to the Trial Balance "
                 f"is **R{tot_rent_rec:,.0f}**. Rent was increased by **{inc_pct:.0f}% on {inc_date}**. Rent for **March (one month prepaid)** "
                 f"has already been received and deposited. Calculate the amount received in advance (prepaid rent) and the true rent earned:")
        exp_rent = (f"1. Let base monthly rent = R. Total months equivalent = {m_old} + ({m_new} × {mult_new:.2f}) = {eq_months:.2f} months. "
                    f"2. Base rent: R = R{tot_rent_rec:,.0f} / {eq_months:.2f} = R{r_base:,.0f}. "
                    f"3. New increased rent = R{r_base:,.0f} × {mult_new:.2f} = R{r_new:,.0f} per month. "
                    f"4. Prepaid rent (March) = 1 month × R{r_new:,.0f} = R{prepaid_amt:,.0f} (Deferred Revenue under Trade & Other Payables). "
                    f"5. Rent earned = R{tot_rent_rec:,.0f} - R{prepaid_amt:,.0f} = R{earned_rent:,.0f}.")
        add_q("medium", "Rent Income Adjustments", q_rent, c_rent, w_rent, "Applying", f"Calculate Rent adjustment for {co_r}", exp_rent)

    # 4. Tangible Assets Depreciation (Straight-Line & Diminishing Balance) (Medium)
    deprec_scenarios = [
        ("Equipment", 180000.0, 36000.0, 15.0, "diminishing balance", 12, "full year"),
        ("Vehicles", 450000.0, 150000.0, 20.0, "diminishing balance", 12, "full year"),
        ("Machinery", 600000.0, 180000.0, 15.0, "straight-line", 12, "full year"),
        ("Office Furniture", 120000.0, 30000.0, 10.0, "straight-line", 12, "full year"),
        ("Delivery Truck", 380000.0, 114000.0, 20.0, "diminishing balance", 12, "full year"),
        ("Computer Equipment", 90000.0, 35000.0, 33.333333, "straight-line", 12, "full year"),
        ("Heavy Plant", 850000.0, 255000.0, 10.0, "diminishing balance", 12, "full year"),
        ("Security System", 160000.0, 48000.0, 15.0, "straight-line", 12, "full year"),
        ("Fleet Vans", 520000.0, 182000.0, 20.0, "diminishing balance", 12, "full year"),
        ("Store Fittings", 210000.0, 63000.0, 10.0, "straight-line", 12, "full year"),
        # New additions bought partway through year:
        ("New Delivery Van bought on 1 Sept (6 months)", 240000.0, 0.0, 20.0, "diminishing balance", 6, "pro-rata 6 months"),
        ("New Manufacturing Press bought on 1 Dec (3 months)", 300000.0, 0.0, 15.0, "straight-line", 3, "pro-rata 3 months"),
        ("New Forklift bought on 1 June (9 months)", 160000.0, 0.0, 15.0, "diminishing balance", 9, "pro-rata 9 months"),
        ("New Generator bought on 1 Nov (4 months)", 120000.0, 0.0, 20.0, "straight-line", 4, "pro-rata 4 months")
    ]

    for asset_type, cost_val, accum_dep_start, dep_rate, dep_method, m_active, dur_desc in deprec_scenarios:
        if counts["medium"] >= 500:
            break
        if "diminishing" in dep_method:
            carrying_val = cost_val - accum_dep_start
            deprec_val = carrying_val * (dep_rate / 100.0) * (m_active / 12.0)
            base_desc = f"Carrying Value (Cost R{cost_val:,.0f} - Accum Dep R{accum_dep_start:,.0f} = R{carrying_val:,.0f})"
        else: # straight-line
            deprec_val = cost_val * (dep_rate / 100.0) * (m_active / 12.0)
            base_desc = f"Cost Price (R{cost_val:,.0f})"

        c_dep = f"R{deprec_val:,.0f}"
        w_dep = [
            f"R{cost_val * (dep_rate/100.0):,.0f} (calculated full-year depreciation on cost ignoring {'diminishing balance' if 'diminishing' in dep_method else 'pro-rata months'})",
            f"R{deprec_val * 2:,.0f}",
            f"R{deprec_val / 2:,.0f}",
            f"R{deprec_val * 1.5:,.0f}",
            f"R{(cost_val - accum_dep_start):,.0f} (confused carrying value with depreciation)",
            f"R{deprec_val + 5000:,.0f}",
            f"R{deprec_val * 0.8:,.0f}"
        ]
        q_dep = (f"Calculate the depreciation on **{asset_type}** for the financial year ended 28 February. "
                 f"Cost price: **R{cost_val:,.0f}**; Accumulated depreciation at start of year: **R{accum_dep_start:,.0f}**. "
                 f"Depreciation policy: **{dep_rate:.1f}% p.a. on {dep_method}** ({dur_desc}):")
        exp_dep = (f"Depreciation calculation ({dep_method}): Depreciation = {base_desc} × {dep_rate:.1f}% × ({m_active}/12) = {c_dep}.")
        add_q("medium", "Tangible Assets Depreciation", q_dep, c_dep, w_dep, "Applying", f"Calculate Depreciation on {asset_type}", exp_dep)

    # 5. Combinatorial Direct Adjustments to reach 500 in Medium:
    # Adjusting pre-tax profit for multiple simultaneous year-end items
    companies_batch = [
        "Laysano Ltd", "Protea Ltd", "Kairo Ltd", "Zulu Ltd", "Metro Ltd",
        "Apex Ltd", "Orchid Ltd", "Galaxy Ltd", "Oasis Ltd", "Bakersfield Ltd",
        "Tshwane Ltd", "Durban Ltd", "Cape Ltd", "Limpopo Ltd", "Highveld Ltd"
    ]
    prelim_profits = [
        850000.0, 920000.0, 1100000.0, 1250000.0, 1400000.0,
        1600000.0, 1850000.0, 2100000.0, 2400000.0, 2800000.0
    ]
    adj_expense_pairs = [
        (12000.0, "trading stock deficit", 8500.0, "increase in provision for bad debts"),
        (15000.0, "depreciation omission", 6200.0, "bad debt written off"),
        (9400.0, "audit fee adjustment", 11500.0, "directors fees owed"),
        (14000.0, "insurance prepaid reversed", 7800.0, "trading stock loss"),
        (8200.0, "additional interest on loan", 5500.0, "provision for bad debts increase"),
        (18000.0, "depreciation on new vehicle", 9200.0, "repairs incorrectly capitalized")
    ]

    for c_name in companies_batch:
        for p_prof in prelim_profits:
            for exp1, desc1, exp2, desc2 in adj_expense_pairs:
                if counts["medium"] >= 500:
                    break
                total_deduct = exp1 + exp2
                final_prof = p_prof - total_deduct
                c_fp = f"R{final_prof:,.0f}"
                w_fp = [
                    f"R{p_prof + total_deduct:,.0f} (added expenses to profit instead of subtracting)",
                    f"R{p_prof - exp1:,.0f} (omitted the second adjustment of R{exp2:,.0f})",
                    f"R{p_prof - exp2:,.0f} (omitted the first adjustment of R{exp1:,.0f})",
                    f"R{final_prof * 1.1:,.0f}",
                    f"R{final_prof * 0.9:,.0f}",
                    f"R{final_prof + 25000:,.0f}",
                    f"R{p_prof:,.0f}"
                ]
                q_fp = (f"The preliminary Net Profit before tax for **{c_name}** was determined to be **R{p_prof:,.0f}**. "
                        f"Before closing the books, the following two year-end adjustments were omitted: (1) {desc1} of **R{exp1:,.0f}**, "
                        f"and (2) {desc2} of **R{exp2:,.0f}**. Calculate the finalized, corrected Net Profit before tax:")
                exp_fp = f"Corrected Profit = Preliminary Profit (R{p_prof:,.0f}) - {desc1} (R{exp1:,.0f}) - {desc2} (R{exp2:,.0f}) = {c_fp}."
                add_q("medium", "Net Profit Adjustments", q_fp, c_fp, w_fp, "Applying", f"Adjust Net Profit for {c_name}", exp_fp)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Multi-Step Tangible Asset Disposal (Profit/Loss + Carrying Value),
    # Comprehensive Balance Sheet Notes (Retained Income & Share Buybacks, SARS Income Tax)
    # =========================================================================

    disposal_cases = [
        ("Delivery Van", 280000.0, 112000.0, 20.0, "diminishing balance", "31 August", 6, 155000.0, "sold for cash"),
        ("Delivery Truck", 420000.0, 168000.0, 20.0, "diminishing balance", "30 November", 9, 210000.0, "sold on credit to a dealer"),
        ("Executive Sedan", 350000.0, 140000.0, 20.0, "diminishing balance", "31 October", 8, 175000.0, "sold for cash"),
        ("Forklift", 180000.0, 54000.0, 15.0, "straight-line", "31 August", 6, 120000.0, "traded in on a new model"),
        ("CNC Lathe Machine", 500000.0, 200000.0, 10.0, "straight-line", "31 December", 10, 240000.0, "sold for cash"),
        ("Printing Press", 600000.0, 240000.0, 15.0, "diminishing balance", "31 October", 8, 310000.0, "sold on credit"),
        ("Company Bakkie", 240000.0, 96000.0, 20.0, "diminishing balance", "31 May", 3, 142000.0, "sold for cash"),
        ("Office Copier System", 120000.0, 48000.0, 20.0, "straight-line", "30 November", 9, 65000.0, "traded in")
    ]

    for asset_name, cost_disp, acc_dep_start_disp, dep_rate_d, dep_method_d, date_sold, m_sold, sell_price, disp_term in disposal_cases:
        # Step 1: Depreciation for current year up to sale
        if "diminishing" in dep_method_d:
            cv_start = cost_disp - acc_dep_start_disp
            current_dep = cv_start * (dep_rate_d / 100.0) * (m_sold / 12.0)
        else:
            current_dep = cost_disp * (dep_rate_d / 100.0) * (m_sold / 12.0)

        # Step 2: Accumulated depreciation at date of sale
        total_acc_dep_at_sale = acc_dep_start_disp + current_dep

        # Step 3: Carrying value at date of sale
        cv_at_sale = cost_disp - total_acc_dep_at_sale

        # Step 4: Profit or Loss on sale
        profit_or_loss = sell_price - cv_at_sale
        is_profit = profit_or_loss >= 0
        status_pl = "PROFIT" if is_profit else "LOSS"

        for co_h in companies_batch:
            if counts["hard"] >= 200:
                break

            c_disp = f"Carrying Value = R{cv_at_sale:,.0f}; {status_pl} on sale = R{abs(profit_or_loss):,.0f}"
            w_disp = [
                f"Carrying Value = R{cost_disp - acc_dep_start_disp:,.0f}; {'LOSS' if is_profit else 'PROFIT'} on sale = R{abs(sell_price - (cost_disp - acc_dep_start_disp)):,.0f} (forgot current year depreciation)",
                f"Carrying Value = R{cost_disp:,.0f}; LOSS on sale = R{cost_disp - sell_price:,.0f}",
                f"Carrying Value = R{cv_at_sale:,.0f}; {'LOSS' if is_profit else 'PROFIT'} on sale = R{abs(profit_or_loss):,.0f} (inverted profit and loss)",
                f"Carrying Value = R{cv_at_sale * 1.1:,.0f}; Profit on sale = R{abs(profit_or_loss) * 1.5:,.0f}",
                f"Carrying Value = R{total_acc_dep_at_sale:,.0f}; Loss on sale = R{abs(sell_price - total_acc_dep_at_sale):,.0f}",
                f"Carrying Value = R{cv_at_sale:,.0f}; Zero profit or loss",
                f"Carrying Value = R{sell_price:,.0f}; Profit on sale = R{current_dep:,.0f}"
            ]
            q_disp = (f"**{co_h}** disposed of a **{asset_name}** on **{date_sold}** ({m_sold} months into the financial year ending 28 February). "
                      f"Original cost price: **R{cost_disp:,.0f}**; Accumulated depreciation at the start of the year (1 March): **R{acc_dep_start_disp:,.0f}**. "
                      f"Depreciation rate: **{dep_rate_d:.0f}% p.a. on {dep_method_d}**. The asset was {disp_term} for **R{sell_price:,.0f}**. "
                      f"Calculate the carrying value on the date of disposal and the resulting profit or loss on sale:")
            exp_disp = (f"1. Current year depreciation up to sale ({date_sold}, {m_sold} months): R{current_dep:,.0f}. "
                        f"2. Total accumulated depreciation at date of disposal: R{acc_dep_start_disp:,.0f} + R{current_dep:,.0f} = R{total_acc_dep_at_sale:,.0f}. "
                        f"3. Carrying value at date of disposal: Cost (R{cost_disp:,.0f}) - Accumulated Depreciation (R{total_acc_dep_at_sale:,.0f}) = R{cv_at_sale:,.0f}. "
                        f"4. Profit/Loss on disposal: Selling price (R{sell_price:,.0f}) - Carrying value (R{cv_at_sale:,.0f}) = {c_disp}.")
            add_q("hard", "Tangible Asset Disposal Calculations", q_disp, c_disp, w_disp, "Evaluating", f"Calculate Asset Disposal for {co_h}", exp_disp)

            # Secondary Question: Total Accumulated Depreciation at Disposal
            if counts["hard"] < 200:
                c_ad = f"R{total_acc_dep_at_sale:,.0f}"
                w_ad = [
                    f"R{acc_dep_start_disp:,.0f} (forgot current year depreciation)",
                    f"R{current_dep:,.0f} (only stated current year depreciation)",
                    f"R{cost_disp:,.0f}",
                    f"R{total_acc_dep_at_sale * 1.2:,.0f}",
                    f"R{total_acc_dep_at_sale / 2:,.0f}",
                    f"R{cv_at_sale:,.0f}",
                    f"R{total_acc_dep_at_sale + 15000:,.0f}"
                ]
                q_ad = (f"In the records of **{co_h}**, determine the **Accumulated Depreciation** to be written off and debited to the "
                        f"Asset Disposal Account for the **{asset_name}** sold on **{date_sold}** (Cost R{cost_disp:,.0f}, starting accumulated dep R{acc_dep_start_disp:,.0f}, "
                        f"{dep_rate_d:.0f}% {dep_method_d}):")
                exp_ad = f"Total Accumulated Depreciation at disposal = Opening Acc Dep (R{acc_dep_start_disp:,.0f}) + Current year dep (R{current_dep:,.0f}) = {c_ad}."
                add_q("hard", "Tangible Asset Disposal Calculations", q_ad, c_ad, w_ad, "Evaluating", f"Calculate Accumulated Depreciation for {co_h}", exp_ad)

    # SARS (Income Tax) and Net Profit Reverse Engineering (Hard)
    sars_tax_cases = [
        ("Laysano Ltd", 48000.0, "debit", 450000.0, 520000.0, 27.0),
        ("Protea Ltd", 35000.0, "credit", 680000.0, 710000.0, 27.0),
        ("Kairo Ltd", 62000.0, "debit", 540000.0, 580000.0, 27.0),
        ("Zulu Ltd", 24000.0, "credit", 390000.0, 420000.0, 27.0),
        ("Metro Ltd", 85000.0, "debit", 890000.0, 950000.0, 27.0)
    ]

    for co_tx, sars_open, sars_side, prov_paid, final_tax_assessed, tx_rate in sars_tax_cases:
        if counts["hard"] >= 200:
            break
        # SARS Ledger Account:
        # Debit side: Payments to SARS (Provisional tax paid) + Opening balance if debit
        # Credit side: Income tax expense for the year (final assessment) + Opening balance if credit
        # Balance = (Credits) - (Debits). If Credits > Debits => Credit balance (Payable / Liability)
        # If Debits > Credits => Debit balance (Receivable / Asset)
        total_debits = prov_paid + (sars_open if sars_side == "debit" else 0.0)
        total_credits = final_tax_assessed + (sars_open if sars_side == "credit" else 0.0)

        diff_sars = total_credits - total_debits
        if diff_sars > 0:
            c_sars = f"R{diff_sars:,.0f} Credit Balance (Amount Payable to SARS under Trade & Other Payables)"
            expl_sars = (f"1. Total debited to SARS (payments + open debit): R{total_debits:,.0f}. "
                         f"2. Total credited to SARS (tax expense + open credit): R{total_credits:,.0f}. "
                         f"3. Balance owed to SARS: R{total_credits:,.0f} - R{total_debits:,.0f} = R{diff_sars:,.0f} Credit Balance (Current Liability).")
        else:
            diff_abs = abs(diff_sars)
            c_sars = f"R{diff_abs:,.0f} Debit Balance (Amount Receivable from SARS under Trade & Other Receivables)"
            expl_sars = (f"1. Total debited to SARS (payments + open debit): R{total_debits:,.0f}. "
                         f"2. Total credited to SARS (tax expense + open credit): R{total_credits:,.0f}. "
                         f"3. Balance refundable from SARS: R{total_debits:,.0f} - R{total_credits:,.0f} = R{diff_abs:,.0f} Debit Balance (Current Asset).")

        w_sars = [
            f"R{final_tax_assessed - prov_paid:,.0f} (ignored opening SARS balance)",
            f"R{total_credits:,.0f} (treated entire tax assessment as balance owed)",
            f"R{total_debits:,.0f} (treated total provisional payments as balance)",
            f"R{abs(diff_sars) * 2:,.0f}",
            f"R{abs(diff_sars) + 15000:,.0f}",
            f"R{final_tax_assessed:,.0f}",
            f"R{prov_paid:,.0f}"
        ]
        q_sars = (f"At the end of the financial year, the accounting records of **{co_tx}** reflect the following concerning SARS (Income Tax): "
                  f"Opening balance on 1 March: **R{sars_open:,.0f} ({sars_side})**; Provisional tax payments made during the year: **R{prov_paid:,.0f}**; "
                  f"Total Income Tax expense for the year assessed at **R{final_tax_assessed:,.0f}**. "
                  f"Calculate the closing balance of the SARS (Income Tax) account and identify its financial statement presentation:")
        add_q("hard", "SARS Income Tax Calculations", q_sars, c_sars, w_sars, "Evaluating", f"Calculate SARS balance for {co_tx}", expl_sars)

    return questions

if __name__ == '__main__':
    qs = build_financial_statements()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_acc_financial_statements.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
