import json
import os

def build_reconciliations():
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
        qid = f"ACC_P2_REC_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Reconciliations & Internal Control",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Reconciliations & Internal Control",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Bank Reconciliation Concepts, CRJ vs CPJ, Bank Statement vs Bank Account, Creditors Reconciliation
    # =========================================================================

    easy_concepts = [
        ("Purpose of a Bank Reconciliation Statement",
         "To explain and reconcile the difference between the balance in the Bank Account in the general ledger and the balance on the Bank Statement received from the commercial bank",
         "To calculate the total interest earned on long-term fixed deposit investments",
         "To determine the amount of provisional corporate tax payable to SARS",
         "To calculate the depreciation on company delivery vehicles",
         "To record the number of ordinary shares issued during the financial year",
         "To approve annual salary increments for factory production workers",
         "To verify the physical stock count of trading inventory at year-end"),

        ("Favourable vs Unfavourable Bank Balances",
         "In the business Bank Account, a debit balance is favourable (asset) and a credit balance is unfavourable (overdraft liability); on the Bank Statement, a credit balance is favourable and a debit balance is unfavourable",
         "A debit balance on both records always represents an asset",
         "A credit balance in the business ledger is favourable while a debit balance on the bank statement is favourable",
         "An unfavourable bank balance means the business has zero trade debtors",
         "A favourable bank balance requires the business to immediately declare dividends",
         "Bank balances have zero connection to cash and cash equivalents on the balance sheet",
         "An overdraft is recorded as a non-current asset on the statement of financial position"),

        ("Treatment of Bank Charges in Journals",
         "Bank charges appearing on the Bank Statement must be recorded in the Cash Payments Journal (CPJ) to update the business Bank Account",
         "Bank charges are recorded in the Cash Receipts Journal (CRJ)",
         "Bank charges are entered on the credit side of the Bank Reconciliation Statement",
         "Bank charges are deducted directly from trade debtors in the Debtors Ledger",
         "Bank charges are debited to Ordinary Share Capital as a dividend distribution",
         "Bank charges are refunded by the commercial bank at the end of every quarter",
         "Bank charges are ignored because they are non-operating capital expenses"),

        ("Treatment of Direct Deposits by Debtors",
         "Direct electronic transfers (EFTs) by debtors shown on the Bank Statement must be entered in the Cash Receipts Journal (CRJ)",
         "Direct deposits are recorded in the Cash Payments Journal (CPJ)",
         "Direct deposits are entered on the debit side of the Bank Reconciliation Statement",
         "Direct deposits are credited to Trading Stock in the General Ledger",
         "Direct deposits are ignored until the debtor sends a physical written letter",
         "Direct deposits are refunded automatically by commercial banks",
         "Direct deposits are classified under investing cash outflows"),

        ("Treatment of Stop Orders and Debit Orders",
         "Pre-authorized monthly stop orders (e.g. insurance) and debit orders appearing on the Bank Statement are recorded in the Cash Payments Journal (CPJ)",
         "Stop orders are entered in the Cash Receipts Journal (CRJ)",
         "Stop orders are entered on the credit side of the Bank Reconciliation Statement",
         "Stop orders are deducted from gross sales revenue in the trading statement",
         "Stop orders are treated as loans from commercial banks",
         "Stop orders are excluded from the general ledger because they are automated",
         "Stop orders are credited to Trade and Other Receivables"),

        ("Dishonoured Cheques (RD Cheques) Treatment",
         "A cheque returned unpaid by the bank due to insufficient funds (Refer to Drawer) must be recorded in the Cash Payments Journal (CPJ) and debited to the debtor's account",
         "An RD cheque is recorded in the Cash Receipts Journal (CRJ)",
         "An RD cheque is entered as an outstanding deposit on the Bank Reconciliation Statement",
         "An RD cheque is written off immediately as a bad debt without contacting the customer",
         "An RD cheque is credited directly to Bank in the Cash Receipts Journal",
         "An RD cheque is paid by the commercial bank on behalf of the customer",
         "An RD cheque has zero impact on the debtor's outstanding balance"),

        ("Outstanding Deposits on Bank Reconciliation",
         "Cash received and entered in the CRJ but not yet credited on the Bank Statement by the bank is listed on the credit side of the Bank Reconciliation Statement",
         "Outstanding deposits are entered on the debit side of the Bank Reconciliation Statement",
         "Outstanding deposits are entered in the Cash Payments Journal to cancel them",
         "Outstanding deposits are written off to Trading Stock Deficit",
         "Outstanding deposits are treated as commercial bank overdrafts",
         "Outstanding deposits are refunded by the South African Reserve Bank",
         "Outstanding deposits are deducted from trade creditors in the general ledger"),

        ("Unpresented Cheques / Outstanding EFTs",
         "Cheques issued and entered in the CPJ that have not yet been presented to the bank for payment are listed on the debit side of the Bank Reconciliation Statement",
         "Unpresented cheques are entered on the credit side of the Bank Reconciliation Statement",
         "Unpresented cheques are entered in the Cash Receipts Journal as income",
         "Unpresented cheques are added to the Bank Account balance in the general ledger",
         "Unpresented cheques are cancelled immediately after 3 days",
         "Unpresented cheques are paid out of petty cash vouchers",
         "Unpresented cheques are classified under non-current liabilities"),

        ("Stale Cheques",
         "Under South African banking practice, a cheque that has not been presented for payment within six months from the date of issue is stale and must be cancelled by recording it in the CRJ",
         "A cheque becomes stale after exactly 14 days from the date of issue",
         "Stale cheques must be handed over to the South African Police Service for fraud investigation",
         "A stale cheque can still be cashed at any commercial bank indefinitely",
         "A stale cheque is deducted from the bank overdraft facility automatically",
         "Stale cheques are debited to Retained Income as an extraordinary dividend",
         "A stale cheque is recorded in the Cash Payments Journal a second time"),

        ("Purpose of Creditors Reconciliation",
         "To compare the monthly Statement of Account received from a supplier (creditor) with the supplier's account in the Creditors Ledger to ensure accuracy and prevent overpayments",
         "To ensure that all retail customers settle their store accounts within 30 days",
         "To reconcile the petty cash box balance with cash register till slips",
         "To calculate the total interest charged by SARS on late provisional tax submissions",
         "To verify that ordinary shareholders have received their final dividend payments",
         "To record the number of factory machine hours worked during night shifts",
         "To inspect the physical condition of motor vehicles in the company garage")
    ]

    for title_r, corr_r, *wrongs_r in easy_concepts:
        q_r1 = f"In Grade 12 Accounting Paper 2 (Reconciliations), what is the correct rule regarding **{title_r}**?"
        exp_r1 = f"**{title_r}**: {corr_r}. Understanding the dual perspective of the bank and the business is a core CAPS requirement."
        add_q("easy", "Reconciliation Fundamentals", q_r1, corr_r, wrongs_r, "Remembering", f"Define rule for {title_r}", exp_r1)

        q_r2 = f"Which reconciliation accounting concept or internal control procedure is defined as: *\"{corr_r}\"*?"
        clean_terms_r = [
            "Petty Cash Imprest Reconciliation", "Debtors Age Analysis Verification",
            "Fixed Asset Register Audit", "Inventory Shrinkage Matrix",
            "VAT Input Output Clearance", "Consolidated Cash Flow Schedule",
            "Audit Committee Mandate"
        ]
        exp_r2 = f"This describes **{title_r}**. {corr_r}."
        add_q("easy", "Reconciliation Fundamentals", q_r2, title_r, clean_terms_r, "Understanding", f"Identify {title_r}", exp_r2)

    # Journal Classification & Easy Direct Calculation cases (70 companies)
    calc_easy_rec = [
        ("Protea Hardware Ltd", 45000.0, 1800.0, 12500.0, 2400.0, 3500.0),
        ("Kavango Auto Spares Ltd", 68000.0, 2400.0, 16800.0, 3100.0, 4200.0),
        ("Algoa Furnishers Ltd", 38000.0, 1500.0, 9500.0, 1900.0, 2800.0),
        ("Soweto Retail Mart Ltd", 95000.0, 3600.0, 24000.0, 4500.0, 6200.0),
        ("Drakensberg Tools Ltd", 52000.0, 1900.0, 14200.0, 2600.0, 3400.0),
        ("Zululand Wholesalers Ltd", 110000.0, 4200.0, 28500.0, 5200.0, 7500.0),
        ("Highveld Computech Ltd", 74000.0, 2800.0, 19000.0, 3600.0, 4800.0),
        ("Karoo Motors Ltd", 88000.0, 3200.0, 22500.0, 4100.0, 5900.0),
        ("Table Mountain Books Ltd", 32000.0, 1300.0, 8400.0, 1600.0, 2200.0),
        ("Springbok Sports Mart Ltd", 61000.0, 2200.0, 15800.0, 2900.0, 3900.0),
        ("Limpopo Farm Supplies Ltd", 82000.0, 3100.0, 21000.0, 3900.0, 5400.0),
        ("Blyde Timber Merchants Ltd", 46000.0, 1700.0, 11800.0, 2200.0, 3100.0),
        ("Gauteng Health Stores Ltd", 105000.0, 3900.0, 27000.0, 4900.0, 6800.0),
        ("Free State Grain Mart Ltd", 59000.0, 2300.0, 15200.0, 2800.0, 3900.0),
        ("Namaqua Diamond Jewelers Ltd", 125000.0, 4800.0, 32000.0, 5800.0, 8200.0),
        ("Outeniqua Garden World Ltd", 41000.0, 1600.0, 10500.0, 2000.0, 2700.0),
        ("Mpumalanga Tile Center Ltd", 78000.0, 2900.0, 20500.0, 3700.0, 5100.0),
        ("Ezulwini Homeware Ltd", 49000.0, 1850.0, 12600.0, 2350.0, 3250.0),
        ("Vaal Triangle Motors Ltd", 135000.0, 5100.0, 35000.0, 6400.0, 8900.0),
        ("Stellenbosch Cellars Ltd", 64000.0, 2500.0, 17000.0, 3100.0, 4300.0),
        ("Tshwane Auto Spares Ltd", 84000.0, 3150.0, 22000.0, 4000.0, 5600.0),
        ("Richards Bay Tools Ltd", 56000.0, 2100.0, 14800.0, 2700.0, 3700.0),
        ("Polokwane Cash & Carry Ltd", 145000.0, 5500.0, 38000.0, 6900.0, 9600.0),
        ("Kimberley Mining Gear Ltd", 72000.0, 2700.0, 18500.0, 3400.0, 4700.0),
        ("Durban Fashion House Ltd", 63000.0, 2400.0, 16200.0, 3000.0, 4100.0),
        ("Rustenburg Tool Mart Ltd", 92000.0, 3500.0, 24000.0, 4400.0, 6100.0),
        ("Witbank Electrical Mart Ltd", 69000.0, 2600.0, 17800.0, 3300.0, 4500.0),
        ("Paarl Fresh Foods Ltd", 81000.0, 3050.0, 21200.0, 3850.0, 5350.0),
        ("Midrand IT Direct Ltd", 118000.0, 4400.0, 30500.0, 5600.0, 7800.0),
        ("Centurion Sports Emporium Ltd", 57000.0, 2150.0, 14900.0, 2750.0, 3800.0),
        ("Bloemfontein Meats Ltd", 99000.0, 3750.0, 26000.0, 4750.0, 6550.0),
        ("East London Marine Spares Ltd", 48000.0, 1800.0, 12400.0, 2300.0, 3150.0),
        ("Klerksdorp Tile Direct Ltd", 76000.0, 2850.0, 19800.0, 3650.0, 5050.0),
        ("Potchefstroom Stationery Hub Ltd", 43000.0, 1650.0, 11200.0, 2100.0, 2850.0),
        ("George Home Living Ltd", 65000.0, 2450.0, 16900.0, 3100.0, 4300.0),
        ("Secunda Safety & Industrial Ltd", 86000.0, 3250.0, 22600.0, 4150.0, 5750.0),
        ("Vereeniging Steel Goods Ltd", 112000.0, 4200.0, 29200.0, 5350.0, 7450.0),
        ("Welkom Mine Supply Ltd", 79000.0, 2950.0, 20600.0, 3800.0, 5250.0),
        ("Bethlehem Grain Traders Ltd", 62000.0, 2350.0, 16200.0, 3000.0, 4100.0),
        ("Newcastle Tool Warehouse Ltd", 83000.0, 3100.0, 21800.0, 4000.0, 5500.0),
        ("Mossel Bay Marine Traders Ltd", 54000.0, 2050.0, 14100.0, 2600.0, 3600.0),
        ("Mthatha Wholesale Hub Ltd", 71000.0, 2700.0, 18600.0, 3400.0, 4700.0),
        ("Upington Agro Direct Ltd", 47000.0, 1750.0, 12200.0, 2250.0, 3100.0),
        ("Vryheid Timber Depot Ltd", 67000.0, 2500.0, 17500.0, 3200.0, 4450.0),
        ("Ladysmith Fashion Mart Ltd", 51000.0, 1950.0, 13300.0, 2450.0, 3400.0),
        ("Bredasdorp Grain Store Ltd", 74000.0, 2800.0, 19400.0, 3550.0, 4900.0),
        ("Cradock Livestock Hub Ltd", 58000.0, 2200.0, 15100.0, 2800.0, 3850.0),
        ("Makhanda Scholastic Supplies Ltd", 44000.0, 1650.0, 11500.0, 2100.0, 2900.0),
        ("Oudtshoorn Leathercraft Ltd", 60000.0, 2250.0, 15700.0, 2900.0, 4000.0),
        ("Knysna Marine Woods Ltd", 87000.0, 3300.0, 22800.0, 4200.0, 5800.0),
        ("Standerton Milking Systems Ltd", 66000.0, 2500.0, 17200.0, 3150.0, 4350.0),
        ("Harrismith Logistics Depot Ltd", 75000.0, 2850.0, 19600.0, 3600.0, 5000.0),
        ("Kuruman Mineral Traders Ltd", 108000.0, 4100.0, 28200.0, 5200.0, 7200.0),
        ("Thohoyandou Superstore Ltd", 93000.0, 3500.0, 24300.0, 4450.0, 6150.0),
        ("Plettenberg Bay Decor Ltd", 53000.0, 2000.0, 13800.0, 2550.0, 3500.0),
        ("Saldanha Marine Freight Ltd", 132000.0, 5000.0, 34500.0, 6300.0, 8700.0),
        ("Grahamstown Scholastic Ltd", 49000.0, 1850.0, 12800.0, 2350.0, 3250.0),
        ("Springbok Wind Parts Ltd", 96000.0, 3600.0, 25100.0, 4600.0, 6350.0),
        ("Witbank Coal Equipment Ltd", 122000.0, 4600.0, 31800.0, 5800.0, 8050.0),
        ("Paarl Valley Beverages Ltd", 85000.0, 3200.0, 22200.0, 4050.0, 5600.0),
        ("Centurion Office Machines Ltd", 77000.0, 2900.0, 20100.0, 3700.0, 5100.0),
        ("Bloemfontein Grain Merchants Ltd", 68000.0, 2550.0, 17800.0, 3250.0, 4500.0),
        ("East London Fishing Gear Ltd", 55000.0, 2100.0, 14400.0, 2650.0, 3650.0),
        ("Klerksdorp Mining Supplies Ltd", 91000.0, 3450.0, 23800.0, 4350.0, 6050.0),
        ("Potchefstroom Feeds Mart Ltd", 73000.0, 2750.0, 19100.0, 3500.0, 4850.0),
        ("Newcastle Heavy Steels Ltd", 115000.0, 4350.0, 30100.0, 5500.0, 7650.0),
        ("Mossel Bay Offshore Mart Ltd", 64000.0, 2400.0, 16700.0, 3050.0, 4250.0),
        ("Mthatha Timber Supplies Ltd", 58000.0, 2200.0, 15200.0, 2750.0, 3850.0),
        ("Upington Sun Agro Supplies Ltd", 52000.0, 1950.0, 13600.0, 2500.0, 3450.0),
        ("Vryheid Coal Merchants Ltd", 84000.0, 3150.0, 22000.0, 4000.0, 5550.0)
    ]

    for co_r, unadj_bank, b_charges, dir_dep, stop_ord, rd_chk in calc_easy_rec:
        # Journal adjustments:
        # CRJ addition: Direct deposit by debtor
        # CPJ additions: Bank charges + Stop order + RD cheque
        tot_cpj = b_charges + stop_ord + rd_chk
        adj_bank = unadj_bank + dir_dep - tot_cpj

        # 1. Adjusted Bank Account Balance
        c_ab = f"R{adj_bank:,.2f} ({'Debit/Favourable' if adj_bank >= 0 else 'Credit/Overdraft'})"
        w_ab = [
            f"R{unadj_bank + dir_dep:,.2f} (omitted CPJ deductions: bank charges, stop orders, RD cheques)",
            f"R{unadj_bank - tot_cpj:,.2f} (omitted direct deposit from debtor)",
            f"R{unadj_bank + tot_cpj - dir_dep:,.2f} (added payments and deducted receipts)",
            f"R{adj_bank * 1.15:,.2f}",
            f"R{adj_bank * 0.85:,.2f}",
            f"R{(adj_bank + 25000):,.2f}",
            f"R{(adj_bank - 20000):,.2f}"
        ]
        q_ab = (f"The Bank Account of **{co_r}** showed a debit balance of **R{unadj_bank:,.2f}** before reconciling. "
                f"The Bank Statement showed the following items not yet entered in the journals:\n"
                f"- Direct deposit by a debtor: **R{dir_dep:,.2f}**\n"
                f"- Bank charges: **R{b_charges:,.2f}**\n"
                f"- Stop order for insurance: **R{stop_ord:,.2f}**\n"
                f"- Dishonoured (RD) cheque from customer: **R{rd_chk:,.2f}**\n"
                f"Calculate the **Adjusted Bank Account balance** to be reflected in the General Ledger:")
        exp_ab = (f"CRJ additions = Direct deposit (R{dir_dep:,.2f})\n"
                  f"CPJ deductions = Bank charges (R{b_charges:,.2f}) + Stop order (R{stop_ord:,.2f}) + RD cheque (R{rd_chk:,.2f}) = R{tot_cpj:,.2f}\n"
                  f"Adjusted Bank Balance = Opening Balance (R{unadj_bank:,.2f}) + R{dir_dep:,.2f} - R{tot_cpj:,.2f} = {c_ab}.")
        add_q("easy", "Bank Account Adjustments", q_ab, c_ab, w_ab, "Applying", f"Calculate adjusted bank balance for {co_r}", exp_ab)

        # 2. Total Additional CPJ Entries
        c_tcpj = f"R{tot_cpj:,.2f}"
        w_tcpj = [
            f"R{b_charges + stop_ord:,.2f} (omitted RD cheque)",
            f"R{b_charges:,.2f} (bank charges only)",
            f"R{tot_cpj + dir_dep:,.2f} (added direct deposit to CPJ)",
            f"R{tot_cpj * 1.2:,.2f}",
            f"R{tot_cpj * 0.8:,.2f}",
            f"R{(tot_cpj + 3000):,.2f}",
            f"R{(tot_cpj - 2500):,.2f}"
        ]
        q_tcpj = (f"For **{co_r}**, calculate the **total amount to be entered in the Cash Payments Journal (CPJ)** "
                  f"from the Bank Statement entries (Bank charges **R{b_charges:,.2f}**, Stop order **R{stop_ord:,.2f}**, RD cheque **R{rd_chk:,.2f}**):")
        exp_tcpj = f"Total CPJ Entries = Bank Charges + Stop Order + RD Cheque = R{b_charges:,.2f} + R{stop_ord:,.2f} + R{rd_chk:,.2f} = {c_tcpj}."
        add_q("easy", "Bank Account Adjustments", q_tcpj, c_tcpj, w_tcpj, "Applying", f"Calculate total CPJ entries for {co_r}", exp_tcpj)

        # 3. Journal Classification Question
        q_jc = f"In which journal should the **dishonoured (RD) cheque of R{rd_chk:,.2f}** for **{co_r}** be entered, and how is it posted to the ledger?"
        c_jc = "Cash Payments Journal (CPJ); posted to credit of Bank Account and debit of Debtor's Account (Accounts Receivable)"
        w_jc = [
            "Cash Receipts Journal (CRJ); credited to Bank Account and debited to Bad Debts",
            "General Journal (GJ); debited to Bank and credited to Sales Revenue",
            "Cash Payments Journal (CPJ); debited to Bank Account and credited to Bank Charges",
            "Creditors Journal (CJ); credited to Accounts Payable",
            "Bank Reconciliation Statement directly without entering any journal",
            "Cash Receipts Journal (CRJ); debited to Drawings and credited to Trading Stock"
        ]
        exp_jc = f"Correct Journal: {c_jc}. When a debtor's cheque bounces, the cash receipt is cancelled in the CPJ and the debt is reinstated."
        add_q("easy", "Journal Recording Rules", q_jc, c_jc, w_jc, "Understanding", f"Journal classification of RD cheque for {co_r}", exp_jc)

        # 4. Bank Reconciliation: Balance as per Bank Statement
        # Bank Reconciliation Statement:
        # Balance as per Bank Statement (credit) + Outstanding Deposit - Unpresented Cheques = Adjusted Bank Balance
        # Let's assign outstanding deposit and unpresented cheques
        out_dep = dir_dep * 1.5
        unpres_chk = tot_cpj * 1.8
        bank_stmt_bal = adj_bank - out_dep + unpres_chk
        c_bsb = f"R{bank_stmt_bal:,.2f} ({'Credit/Favourable' if bank_stmt_bal >= 0 else 'Debit/Overdraft'})"
        w_bsb = [
            f"R{adj_bank:,.2f} (used adjusted bank account balance)",
            f"R{adj_bank + out_dep - unpres_chk:,.2f} (added deposit and deducted cheques from bank account)",
            f"R{bank_stmt_bal * 1.15:,.2f}",
            f"R{bank_stmt_bal * 0.85:,.2f}",
            f"R{(bank_stmt_bal + 15000):,.2f}",
            f"R{(bank_stmt_bal - 12000):,.2f}",
            f"R{out_dep - unpres_chk:,.2f}"
        ]
        q_bsb = (f"The Bank Reconciliation Statement of **{co_r}** at month-end shows:\n"
                 f"- Outstanding deposit: **R{out_dep:,.2f}**\n"
                 f"- Unpresented cheques: **R{unpres_chk:,.2f}**\n"
                 f"- Adjusted Bank Account balance: **R{adj_bank:,.2f}** (favourable)\n"
                 f"Calculate the **Balance as per Bank Statement** before reconciliation:")
        exp_bsb = (f"Bank Statement Balance + Outstanding Deposit (R{out_dep:,.2f}) - Unpresented Cheques (R{unpres_chk:,.2f}) = Adjusted Bank Balance (R{adj_bank:,.2f})\n"
                   f"Bank Statement Balance = R{adj_bank:,.2f} - R{out_dep:,.2f} + R{unpres_chk:,.2f} = {c_bsb}.")
        add_q("easy", "Bank Reconciliation Structure", q_bsb, c_bsb, w_bsb, "Applying", f"Calculate bank statement balance for {co_r}", exp_bsb)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Full Bank Reconciliations with Error Corrections, Creditors Reconciliations
    # =========================================================================

    # 50 South African commercial scenarios with multi-error adjustments
    # (Company, Unadj_bank, Bank_stmt_bal, Out_dep, Unpres_chk, Bank_error_deb, Book_error_cpj, Cred_ledger_bal, Cred_stmt_bal, Inv_omitted, Disc_disallowed, Return_omitted)
    rec_scenarios = [
        ("Protea Hardware Ltd", 54000.0, 48200.0, 28000.0, 22500.0, 1500.0, 900.0, 68000.0, 74500.0, 4200.0, 850.0, 2850.0),
        ("Kavango Auto Spares Ltd", 82000.0, 76500.0, 36000.0, 31200.0, 2200.0, 1200.0, 94000.0, 102800.0, 5800.0, 1150.0, 3950.0),
        ("Algoa Furnishers Ltd", 46000.0, 41200.0, 22000.0, 17800.0, 1200.0, 750.0, 52000.0, 57400.0, 3400.0, 680.0, 2320.0),
        ("Soweto Retail Mart Ltd", 115000.0, 106800.0, 48000.0, 41500.0, 2800.0, 1600.0, 138000.0, 150500.0, 8500.0, 1650.0, 5650.0),
        ("Drakensberg Tools Ltd", 62000.0, 55800.0, 31000.0, 25600.0, 1800.0, 950.0, 75000.0, 82200.0, 4600.0, 920.0, 3120.0),
        ("Zululand Wholesalers Ltd", 132000.0, 121500.0, 56000.0, 47800.0, 3200.0, 1800.0, 162000.0, 176800.0, 9800.0, 1950.0, 6550.0),
        ("Highveld Computech Ltd", 89000.0, 81400.0, 42000.0, 35600.0, 2400.0, 1300.0, 108000.0, 117900.0, 6700.0, 1350.0, 4450.0),
        ("Karoo Motors Ltd", 104000.0, 96200.0, 49000.0, 42500.0, 2700.0, 1500.0, 125000.0, 136200.0, 7800.0, 1550.0, 5150.0),
        ("Table Mountain Books Ltd", 38000.0, 33500.0, 18000.0, 14200.0, 950.0, 550.0, 44000.0, 48500.0, 2800.0, 560.0, 1860.0),
        ("Springbok Sports Mart Ltd", 73000.0, 66400.0, 34000.0, 28500.0, 1950.0, 1100.0, 86000.0, 94100.0, 5400.0, 1080.0, 3580.0),
        ("Limpopo Farm Supplies Ltd", 98000.0, 89800.0, 45000.0, 38200.0, 2600.0, 1450.0, 119000.0, 129800.0, 7400.0, 1480.0, 4920.0),
        ("Blyde Timber Merchants Ltd", 55000.0, 49500.0, 26000.0, 21800.0, 1450.0, 820.0, 64000.0, 70200.0, 4100.0, 820.0, 2720.0),
        ("Gauteng Health Stores Ltd", 126000.0, 116200.0, 54000.0, 46500.0, 3100.0, 1750.0, 152000.0, 165800.0, 9400.0, 1850.0, 6250.0),
        ("Free State Grain Mart Ltd", 71000.0, 64200.0, 33000.0, 27500.0, 1850.0, 1050.0, 84000.0, 91800.0, 5200.0, 1040.0, 3440.0),
        ("Namaqua Diamond Jewelers Ltd", 148000.0, 136500.0, 62000.0, 53200.0, 3600.0, 2100.0, 185000.0, 201800.0, 11500.0, 2250.0, 7550.0),
        ("Outeniqua Garden World Ltd", 49000.0, 43800.0, 23000.0, 18900.0, 1300.0, 720.0, 58000.0, 63600.0, 3700.0, 740.0, 2440.0),
        ("Mpumalanga Tile Center Ltd", 93000.0, 84800.0, 43000.0, 36200.0, 2450.0, 1380.0, 112000.0, 122400.0, 7100.0, 1420.0, 4720.0),
        ("Ezulwini Homeware Ltd", 58000.0, 52100.0, 27000.0, 22400.0, 1500.0, 860.0, 69000.0, 75600.0, 4300.0, 860.0, 2860.0),
        ("Vaal Triangle Motors Ltd", 162000.0, 149500.0, 68000.0, 58200.0, 4000.0, 2300.0, 198000.0, 216200.0, 12400.0, 2450.0, 8250.0),
        ("Stellenbosch Cellars Ltd", 77000.0, 70100.0, 37000.0, 31200.0, 2050.0, 1150.0, 92000.0, 100600.0, 5800.0, 1160.0, 3860.0),
        ("Tshwane Auto Spares Ltd", 101000.0, 92400.0, 47000.0, 39800.0, 2700.0, 1520.0, 122000.0, 133200.0, 7600.0, 1520.0, 5080.0),
        ("Richards Bay Tools Ltd", 67000.0, 60800.0, 32000.0, 26900.0, 1750.0, 980.0, 79000.0, 86500.0, 4900.0, 980.0, 3280.0),
        ("Polokwane Cash & Carry Ltd", 175000.0, 161800.0, 74000.0, 63500.0, 4300.0, 2500.0, 215000.0, 234800.0, 13500.0, 2650.0, 8950.0),
        ("Kimberley Mining Gear Ltd", 86000.0, 78400.0, 40000.0, 33800.0, 2250.0, 1280.0, 104000.0, 113600.0, 6500.0, 1300.0, 4300.0),
        ("Durban Fashion House Ltd", 75000.0, 68200.0, 35000.0, 29400.0, 1980.0, 1120.0, 89000.0, 97400.0, 5600.0, 1120.0, 3720.0),
        ("Rustenburg Tool Mart Ltd", 110000.0, 100800.0, 51000.0, 43200.0, 2900.0, 1650.0, 134000.0, 146500.0, 8400.0, 1680.0, 5580.0),
        ("Witbank Electrical Mart Ltd", 83000.0, 75600.0, 39000.0, 32800.0, 2180.0, 1220.0, 99000.0, 108200.0, 6200.0, 1240.0, 4120.0),
        ("Paarl Fresh Foods Ltd", 97000.0, 88500.0, 44000.0, 37400.0, 2550.0, 1420.0, 117000.0, 127900.0, 7300.0, 1460.0, 4860.0),
        ("Midrand IT Direct Ltd", 142000.0, 130800.0, 61000.0, 52200.0, 3500.0, 2020.0, 172000.0, 187800.0, 10800.0, 2150.0, 7150.0),
        ("Centurion Sports Emporium Ltd", 68000.0, 61800.0, 33000.0, 27600.0, 1800.0, 1020.0, 81000.0, 88600.0, 5100.0, 1020.0, 3380.0),
        ("Bloemfontein Meats Ltd", 118000.0, 108200.0, 53000.0, 45200.0, 3050.0, 1720.0, 144000.0, 157200.0, 9000.0, 1800.0, 5980.0),
        ("East London Marine Spares Ltd", 57000.0, 51400.0, 28000.0, 23400.0, 1520.0, 850.0, 68000.0, 74600.0, 4300.0, 860.0, 2860.0),
        ("Klerksdorp Tile Direct Ltd", 91000.0, 83100.0, 42000.0, 35500.0, 2380.0, 1340.0, 110000.0, 120200.0, 6900.0, 1380.0, 4580.0),
        ("Potchefstroom Stationery Hub Ltd", 51000.0, 45900.0, 25000.0, 20800.0, 1380.0, 760.0, 61000.0, 66800.0, 3900.0, 780.0, 2580.0),
        ("George Home Living Ltd", 78000.0, 70900.0, 37000.0, 31000.0, 2050.0, 1160.0, 94000.0, 102800.0, 5900.0, 1180.0, 3920.0),
        ("Secunda Safety & Industrial Ltd", 103000.0, 94200.0, 48000.0, 40800.0, 2750.0, 1540.0, 126000.0, 137800.0, 7900.0, 1580.0, 5260.0),
        ("Vereeniging Steel Goods Ltd", 135000.0, 124100.0, 58000.0, 49600.0, 3350.0, 1920.0, 164000.0, 179200.0, 10200.0, 2040.0, 6820.0),
        ("Welkom Mine Supply Ltd", 95000.0, 86900.0, 44000.0, 37200.0, 2480.0, 1400.0, 116000.0, 126800.0, 7300.0, 1460.0, 4860.0),
        ("Bethlehem Grain Traders Ltd", 74000.0, 67200.0, 35000.0, 29500.0, 1950.0, 1100.0, 88000.0, 96400.0, 5500.0, 1100.0, 3680.0),
        ("Newcastle Tool Warehouse Ltd", 100000.0, 91500.0, 46000.0, 39100.0, 2650.0, 1480.0, 121000.0, 132400.0, 7600.0, 1520.0, 5060.0),
        ("Mossel Bay Marine Traders Ltd", 65000.0, 58900.0, 31000.0, 26200.0, 1720.0, 960.0, 78000.0, 85400.0, 4900.0, 980.0, 3260.0),
        ("Mthatha Wholesale Hub Ltd", 85000.0, 77500.0, 40000.0, 33800.0, 2240.0, 1260.0, 103000.0, 112800.0, 6500.0, 1300.0, 4320.0),
        ("Upington Agro Direct Ltd", 56000.0, 50600.0, 27000.0, 22600.0, 1490.0, 840.0, 67000.0, 73400.0, 4200.0, 840.0, 2800.0),
        ("Vryheid Timber Depot Ltd", 80000.0, 72800.0, 38000.0, 32100.0, 2120.0, 1180.0, 97000.0, 106200.0, 6100.0, 1220.0, 4060.0),
        ("Ladysmith Fashion Mart Ltd", 61000.0, 55200.0, 29000.0, 24500.0, 1620.0, 910.0, 74000.0, 81000.0, 4700.0, 940.0, 3120.0),
        ("Bredasdorp Grain Store Ltd", 89000.0, 81100.0, 42000.0, 35600.0, 2360.0, 1320.0, 108000.0, 118200.0, 6800.0, 1360.0, 4520.0),
        ("Cradock Livestock Hub Ltd", 70000.0, 63500.0, 34000.0, 28600.0, 1860.0, 1040.0, 85000.0, 93000.0, 5300.0, 1060.0, 3540.0),
        ("Makhanda Scholastic Supplies Ltd", 53000.0, 47800.0, 26000.0, 21700.0, 1420.0, 790.0, 63000.0, 69000.0, 4000.0, 800.0, 2660.0),
        ("Oudtshoorn Leathercraft Ltd", 72000.0, 65200.0, 35000.0, 29400.0, 1920.0, 1070.0, 87000.0, 95200.0, 5500.0, 1100.0, 3660.0),
        ("Knysna Marine Woods Ltd", 105000.0, 95800.0, 49000.0, 41500.0, 2780.0, 1560.0, 127000.0, 139000.0, 8000.0, 1600.0, 5320.0)
    ]

    for co_m, unadj_b, bs_bal, out_d, unpres_c, b_err_deb, bk_err_cpj, cr_ledg, cr_stmt, inv_omit, disc_disall, ret_omit in rec_scenarios:
        # Bank Reconciliation calculation:
        # Bank Account error: cheque was entered in CPJ as R5,400 instead of R4,500 (overstated by bk_err_cpj)
        # -> Corrected by adding bk_err_cpj to CRJ (increases Bank Account)
        adj_bank_m = unadj_b + bk_err_cpj

        # Bank Statement error: Bank erroneously debited business account with another client's cheque of b_err_deb
        # -> Corrected on Bank Reconciliation Statement by crediting the amount (adding to bank balance)
        reconciled_stmt_bal = bs_bal + out_d - unpres_c + b_err_deb

        # Creditors Reconciliation calculation:
        # In Creditors Ledger:
        # Invoice omitted: add inv_omit
        # Discount disallowed: add disc_disall (reversing discount)
        adj_cred_ledg = cr_ledg + inv_omit + disc_disall

        # In Creditors Reconciliation Statement (adjusting supplier statement):
        # Return omitted by supplier: deduct ret_omit
        adj_cred_stmt = cr_stmt - ret_omit

        # 1. Medium Q: Correcting Bookkeeping Error in Journal
        if counts["medium"] < 500:
            c_err_b = f"Enter R{bk_err_cpj:,.2f} in Cash Receipts Journal (CRJ) to reverse the overpayment"
            w_err_b = [
                f"Enter R{bk_err_cpj:,.2f} in Cash Payments Journal (CPJ) a second time",
                f"Enter on the debit side of the Bank Reconciliation Statement without journal entry",
                f"Deduct R{bk_err_cpj:,.2f} from Trade Debtors in the general ledger",
                f"Cancel the cheque and issue a new cheque for R{bk_err_cpj:,.2f}",
                f"Deduct R{bk_err_cpj:,.2f} from Ordinary Share Capital",
                f"Leave the error uncorrected because bank reconciliation fixes it automatically"
            ]
            q_err_b = (f"In **{co_m}**, cheque No. 412 was correctly drawn for payment to a supplier, but the bookkeeper entered it "
                       f"in the Cash Payments Journal (CPJ) with an overstatement of **R{bk_err_cpj:,.2f}**. "
                       f"How should this bookkeeping error be corrected in the accounting records?")
            exp_err_b = (f"Correction: {c_err_b}. Since the CPJ was overstated, cash payments were inflated. "
                         f"Entering the difference in the CRJ restores the Bank Account to its correct balance.")
            add_q("medium", "Bank Account Error Corrections", q_err_b, c_err_b, w_err_b, "Applying", f"Correct CPJ error for {co_m}", exp_err_b)

        # 2. Medium Q: Correcting Bank Error on Reconciliation Statement
        if counts["medium"] < 500:
            c_err_bank = f"Credit R{b_err_deb:,.2f} on the Bank Reconciliation Statement"
            w_err_bank = [
                f"Debit R{b_err_deb:,.2f} on the Bank Reconciliation Statement",
                f"Enter R{b_err_deb:,.2f} in the Cash Payments Journal (CPJ)",
                f"Enter R{b_err_deb:,.2f} in the Cash Receipts Journal (CRJ)",
                f"Deduct R{b_err_deb:,.2f} from Trade Creditors",
                f"Write off R{b_err_deb:,.2f} as a Bad Debt in the Income Statement",
                f"Do nothing because banks never make mistakes on bank statements"
            ]
            q_err_bank = (f"The Bank Statement of **{co_m}** reflects a debit of **R{b_err_deb:,.2f}** for a cheque drawn by another business. "
                          f"The bank acknowledged the error and promised to correct it next month. "
                          f"How must this bank error be reflected in the **Bank Reconciliation Statement** at month-end?")
            exp_err_bank = (f"Correction: {c_err_bank}. Because the bank erroneously subtracted (debited) money from the business account, "
                            f"the Bank Reconciliation Statement must credit the amount to show what the bank balance should be.")
            add_q("medium", "Bank Reconciliation Structure", q_err_bank, c_err_bank, w_err_bank, "Applying", f"Correct bank error for {co_m}", exp_err_bank)

        # 3. Medium Q: Adjusted Bank Account Balance after journal corrections
        if counts["medium"] < 500:
            c_adj_b = f"R{adj_bank_m:,.2f}"
            w_adj_b = [
                f"R{unadj_b - bk_err_cpj:,.2f} (deducted error instead of adding)",
                f"R{unadj_b:,.2f} (unadjusted balance)",
                f"R{adj_bank_m * 1.15:,.2f}",
                f"R{adj_bank_m * 0.85:,.2f}",
                f"R{(adj_bank_m + 15000):,.2f}",
                f"R{(adj_bank_m - 12000):,.2f}",
                f"R{unadj_b + b_err_deb:,.2f} (added bank error to cash journals)"
            ]
            q_adj_b = (f"Before reconciliation, the Bank Account of **{co_r}** showed a balance of **R{unadj_b:,.2f}**. "
                       f"The only unrecorded item was a CPJ overstatement error of **R{bk_err_cpj:,.2f}** which must be added in the CRJ. "
                       f"Calculate the **Adjusted Bank Account balance**:")
            exp_adj_b = f"Adjusted Bank Balance = Unadjusted Balance (R{unadj_b:,.2f}) + CRJ correction (R{bk_err_cpj:,.2f}) = {c_adj_b}."
            add_q("medium", "Bank Account Adjustments", q_adj_b, c_adj_b, w_adj_b, "Applying", f"Calculate adjusted bank balance for {co_m}", exp_adj_b)

        # 4. Medium Q: Bank Reconciliation Reconciled Balance
        if counts["medium"] < 500:
            c_rec_b = f"R{reconciled_stmt_bal:,.2f}"
            w_rec_b = [
                f"R{bs_bal:,.2f} (unadjusted statement balance)",
                f"R{bs_bal + out_d + unpres_c:,.2f} (added unpresented cheques instead of deducting)",
                f"R{bs_bal - out_d + unpres_c:,.2f} (deducted deposit and added cheques)",
                f"R{reconciled_stmt_bal * 1.15:,.2f}",
                f"R{reconciled_stmt_bal * 0.85:,.2f}",
                f"R{(reconciled_stmt_bal + 20000):,.2f}",
                f"R{(reconciled_stmt_bal - 18000):,.2f}"
            ]
            q_rec_b = (f"Calculate the **Reconciled Bank Statement Balance** for **{co_m}** from the following Bank Reconciliation figures:\n"
                       f"- Balance as per Bank Statement (credit): **R{bs_bal:,.2f}**\n"
                       f"- Credit: Outstanding deposit: **R{out_d:,.2f}**\n"
                       f"- Debit: Unpresented cheques: **R{unpres_c:,.2f}**\n"
                       f"- Credit: Bank error (cheque incorrectly debited): **R{b_err_deb:,.2f}**")
            exp_rec_b = (f"Reconciled Balance = Bank Statement Balance (R{bs_bal:,.2f}) + Outstanding Deposit (R{out_d:,.2f}) "
                         f"- Unpresented Cheques (R{unpres_c:,.2f}) + Bank Error Credit (R{b_err_deb:,.2f})\n"
                         f"= {c_rec_b}.")
            add_q("medium", "Bank Reconciliation Structure", q_rec_b, c_rec_b, w_rec_b, "Applying", f"Calculate reconciled balance for {co_m}", exp_rec_b)

        # 5. Medium Q: Creditors Ledger Adjustment for Omitted Invoice
        if counts["medium"] < 500:
            c_cl_inv = f"Credit the Creditors Ledger account with R{inv_omit:,.2f} (increases liability)"
            w_cl_inv = [
                f"Debit the Creditors Ledger account with R{inv_omit:,.2f} (decreases liability)",
                f"Enter on the Creditors Reconciliation Statement as an outstanding debit note",
                f"Deduct R{inv_omit:,.2f} from Cash Payments Journal",
                f"Ignore the invoice until the creditor sends a final demand letter",
                f"Credit the Debtors Ledger account with R{inv_omit:,.2f}",
                f"Write off R{inv_omit:,.2f} to Bad Debts Recovered"
            ]
            q_cl_inv = (f"The monthly statement from supplier Protea Wholesalers received by **{co_m}** includes an invoice for **R{inv_omit:,.2f}** "
                        f"which was correctly delivered but omitted from the company's Creditors Journal. "
                        f"How must this omission be corrected in the accounting records?")
            exp_cl_inv = f"Correction: {c_cl_inv}. The business owes the money, so the purchase must be credited to the supplier's account in the Creditors Ledger."
            add_q("medium", "Creditors Reconciliation Adjustments", q_cl_inv, c_cl_inv, w_cl_inv, "Applying", f"Correct omitted invoice for {co_m}", exp_cl_inv)

        # 6. Medium Q: Creditors Ledger Adjustment for Disallowed Discount
        if counts["medium"] < 500:
            c_cl_disc = f"Credit the Creditors Ledger account with R{disc_disall:,.2f} to reverse the discount"
            w_cl_disc = [
                f"Debit the Creditors Ledger account with R{disc_disall:,.2f}",
                f"Enter on the Creditors Reconciliation Statement as a credit note",
                f"Deduct R{disc_disall:,.2f} from the opening bank balance in the Cash Budget",
                f"Transfer R{disc_disall:,.2f} to Discount Received income",
                f"Ignore the creditor's refusal and maintain the deduction",
                f"Deduct R{disc_disall:,.2f} from Value-Added Tax payable to SARS"
            ]
            q_cl_disc = (f"**{co_m}** deducted an early settlement discount of **R{disc_disall:,.2f}** in the CPJ when paying supplier Kavango Supplies. "
                         f"However, the payment was made after the 30-day deadline, and the creditor disallowed the discount on the monthly statement. "
                         f"How must this disallowed discount be recorded in the Creditors Ledger?")
            exp_cl_disc = f"Correction: {c_cl_disc}. When a discount is cancelled by a supplier, the liability must be reinstated by crediting the Creditors Ledger."
            add_q("medium", "Creditors Reconciliation Adjustments", q_cl_disc, c_cl_disc, w_cl_disc, "Applying", f"Correct disallowed discount for {co_m}", exp_cl_disc)

        # 7. Medium Q: Adjusted Creditors Ledger Balance
        if counts["medium"] < 500:
            c_acl = f"R{adj_cred_ledg:,.2f}"
            w_acl = [
                f"R{cr_ledg:,.2f} (unadjusted creditors balance)",
                f"R{cr_ledg - inv_omit - disc_disall:,.2f} (deducted omitted invoice and discount)",
                f"R{cr_ledg + inv_omit - disc_disall:,.2f} (deducted disallowed discount)",
                f"R{adj_cred_ledg * 1.15:,.2f}",
                f"R{adj_cred_ledg * 0.85:,.2f}",
                f"R{(adj_cred_ledg + 18000):,.2f}",
                f"R{(adj_cred_ledg - 15000):,.2f}"
            ]
            q_acl = (f"The Creditors Ledger balance of **{co_m}** for supplier Algoa Traders was **R{cr_ledg:,.2f}**. "
                     f"Adjustments required in the ledger are:\n"
                     f"- Omitted purchase invoice: **R{inv_omit:,.2f}**\n"
                     f"- Disallowed early settlement discount: **R{disc_disall:,.2f}**\n"
                     f"Calculate the **Adjusted Creditors Ledger balance**:")
            exp_acl = f"Adjusted Balance = Ledger Balance (R{cr_ledg:,.2f}) + Omitted Invoice (R{inv_omit:,.2f}) + Disallowed Discount (R{disc_disall:,.2f}) = {c_acl}."
            add_q("medium", "Creditors Reconciliation Adjustments", q_acl, c_acl, w_acl, "Applying", f"Calculate adjusted creditors balance for {co_m}", exp_acl)

        # 8. Medium Q: Adjusted Statement of Account Balance (Creditors Reconciliation Statement)
        if counts["medium"] < 500:
            c_acs = f"R{adj_cred_stmt:,.2f}"
            w_acs = [
                f"R{cr_stmt:,.2f} (unadjusted statement balance)",
                f"R{cr_stmt + ret_omit:,.2f} (added return instead of deducting)",
                f"R{adj_cred_stmt * 1.15:,.2f}",
                f"R{adj_cred_stmt * 0.85:,.2f}",
                f"R{(adj_cred_stmt + 12000):,.2f}",
                f"R{(adj_cred_stmt - 10000):,.2f}",
                f"R{cr_stmt - inv_omit:,.2f}"
            ]
            q_acs = (f"The Statement of Account received from supplier Soweto Traders by **{co_m}** shows a closing balance of **R{cr_stmt:,.2f}**. "
                     f"A debit note of **R{ret_omit:,.2f}** issued by {co_m} for returned damaged goods does not appear on the supplier's statement. "
                     f"Calculate the **Adjusted Statement Balance** on the Creditors Reconciliation Statement:")
            exp_acs = f"Adjusted Statement Balance = Statement Balance (R{cr_stmt:,.2f}) - Goods Returned (R{ret_omit:,.2f}) = {c_acs}."
            add_q("medium", "Creditors Reconciliation Adjustments", q_acs, c_acs, w_acs, "Applying", f"Calculate adjusted statement balance for {co_m}", exp_acs)

        # 9. Medium Q: Reconciled Settlement Amount for Creditor
        if counts["medium"] < 500:
            settle_amt = adj_cred_stmt  # Both balances should reconcile!
            c_set = f"R{settle_amt:,.2f}"
            w_set = [
                f"R{cr_stmt:,.2f} (paid full unadjusted supplier statement balance)",
                f"R{cr_ledg:,.2f} (paid unadjusted internal ledger balance)",
                f"R{settle_amt * 1.15:,.2f}",
                f"R{settle_amt * 0.85:,.2f}",
                f"R{(settle_amt + 15000):,.2f}",
                f"R{(settle_amt - 12000):,.2f}",
                f"R{settle_amt - 5000:,.2f}"
            ]
            q_set = (f"Following reconciliation between the Creditors Ledger and the supplier statement for **{co_m}**, "
                     f"both adjusted records reflect an agreed reconciled balance of **R{settle_amt:,.2f}**. "
                     f"What is the **exact settlement amount** that {co_m} should pay to clear the supplier's account?")
            exp_set = f"Settlement Amount: **{c_set}**. Payment must be made strictly on the reconciled agreed balance."
            add_q("medium", "Creditors Reconciliation Adjustments", q_set, c_set, w_set, "Applying", f"Calculate supplier settlement for {co_m}", exp_set)

        # 10. Medium Q: Reason for Creditors Reconciliation
        if counts["medium"] < 500:
            c_reas = "To verify external supplier claims, prevent overpayments, detect unrecorded credit notes, and maintain good supplier credit ratings"
            w_reas = [
                "To calculate corporate income tax deductions for the South African Revenue Service",
                "To determine how many ordinary shares the company should issue to suppliers",
                "To calculate annual factory machinery depreciation on the diminishing balance method",
                "To evaluate whether retail selling prices of consumer goods should be increased by 20%",
                "To replace the need for conducting annual physical inventory counts in the warehouse",
                "To enable company directors to borrow corporate cash without paying interest"
            ]
            q_reas = f"What is the primary internal control and business governance reason for preparing a **Creditors Reconciliation** in **{co_m}**?"
            exp_reas = f"Reason: **{c_reas}**. Reconciliations are essential internal control checks in financial accounting."
            add_q("medium", "Creditors Reconciliation Adjustments", q_reas, c_reas, w_reas, "Understanding", f"Explain reason for creditors reconciliation in {co_m}", exp_reas)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Fraud Detection, Teeming & Lading, Stale Cheques, Internal Control Deficiencies
    # =========================================================================

    fraud_scenarios = [
        ("The Bank Reconciliation Statement of **Protea Hardware Ltd** shows an outstanding deposit of **R85,000** entered on 18 September that has appeared as an outstanding deposit for three consecutive months (September, October, November). The cashier claims the bank delayed processing.",
         "Cash embezzlement and theft: A legitimate commercial bank deposit takes 24 to 48 hours to clear. The cashier stole the cash before banking and concealed the theft on the Bank Reconciliation Statement. Management must audit daily deposit slips and suspend the cashier pending criminal charges.",
         ["Normal commercial banking delay caused by inter-bank clearance queues",
          "Acceptable practice during electricity load shedding and national banking system maintenance",
          "A minor administrative delay that will self-correct when the bank issues its annual report",
          "Permissible provided the cashier replaces the cash when receiving an annual bonus",
          "Lawful under the Companies Act because deposits remain valid assets for up to three years",
          "An operational matter that falls strictly outside the jurisdiction of financial management"]),

        ("The internal auditor discovered that cashier **Sipho** was practicing 'teeming and lading' (cheque rolling): using today's cash receipts from debtor B to deposit into the bank to cover yesterday's cash stolen from debtor A's payment.",
         "Teeming and lading fraud (lapping): Severe breakdown of internal control caused by a single person collecting cash, issuing receipts, making bank deposits, and posting to debtors ledgers. Management must immediately separate cash handling from ledger bookkeeping.",
         ["Smart short-term cash flow smoothing that assists the company in maintaining liquidity",
          "Permissible under South African retail trade custom during difficult economic recessions",
          "A minor human resource issue that only requires an informal verbal counseling session",
          "Acceptable practice provided the total debtors ledger balance equals the general ledger control account",
          "Lawful under King IV as flexible daily working capital management",
          "Permissible if Sipho pays 10% interest to the company on the rolled funds"]),

        ("The bookkeeper of **Kavango Auto Spares Ltd** issued cheque No. 814 for **R42,000** payable to 'Cash' signed by only one director, while the company's internal mandate requires dual signatures for all payments exceeding R10,000.",
         "Gross violation of internal control and banking mandates: Single signature on a cash cheque exposes the firm to unauthorized misappropriation. The commercial bank should have rejected the cheque, and the company must enforce electronic dual-authorization EFTs.",
         ["Exemplary administrative efficiency that reduces paperwork delays in paying urgent suppliers",
          "Permissible under the Companies Act because executive directors have unilateral signing authority",
          "A minor technical banking formality that has zero bearing on corporate asset protection",
          "Acceptable practice provided the bookkeeper obtains verbal approval over the telephone",
          "Lawful provided the cash cheque is cashed during normal commercial banking trading hours",
          "Permissible if the director uses the cash to purchase company factory equipment"]),

        ("An examination of the Creditors Ledger of **Algoa Furnishers Ltd** reveals that payments totaling **R450,000** were made to a supplier named 'Apex Timber Ltd'. Investigation reveals that Apex Timber is a fictitious shell corporation registered to the purchasing manager's brother with no physical business premises.",
         "Procurement fraud and criminal theft: Fictitious supplier fraud. The purchasing manager fabricated purchase orders, goods received notes, and invoices to siphon company funds. Management must file criminal charges, freeze accounts, and institute forensic asset recovery.",
         ["Legitimate related-party trade diversification encouraged by the Department of Trade and Industry",
          "Permissible provided the fictitious entity pays corporate tax to SARS on the payments received",
          "A private family business arrangement that does not concern executive board members",
          "Acceptable corporate practice because all businesses use intermediary procurement brokers",
          "Lawful provided the purchasing manager negotiates a 5% trade discount on future orders",
          "An administrative issue to be resolved by transferring the manager to human resources"]),

        ("The bank reconciliation of **Soweto Retail Mart Ltd** includes an unpresented cheque of **R18,500** issued seven months ago to 'Quality Printers'. The cheque has never cleared the bank account.",
         "Stale cheque: Under South African law, cheques older than six months are legally void and stale. The bookkeeper must cancel the cheque by debiting Bank and crediting Quality Printers (or Creditors Control) in the Cash Receipts Journal (CRJ).",
         ["The cheque remains fully valid and must continue to be listed on the Bank Reconciliation indefinitely",
          "The bank should be sued in the High Court for failing to pay a seven-month-old cheque",
          "The bookkeeper must record the payment in the Cash Payments Journal a second time",
          "The R18,500 should be transferred directly to the managing director's personal savings account",
          "The amount must be written off immediately to Bad Debts in the Income Statement",
          "The company should issue a second cheque without cancelling the first cheque"]),

        ("The Financial Director of **Highveld Computech Ltd** instructed the bookkeeper not to prepare monthly bank reconciliations for six consecutive months, claiming that daily online internet banking balances make reconciliations unnecessary.",
         "Dangerous abandonment of internal control and breach of King IV: Online balances only show what has cleared the bank, completely missing unrecorded direct debits, banking errors, outstanding deposits, and employee fraud. Monthly reconciliations are mandatory.",
         ["Progressive, paperless modern financial management that saves time and administrative overhead",
          "Fully compliant with IFRS because real-time internet banking replaces general ledger accounts",
          "Acceptable practice because commercial banks are legally responsible for all accounting errors",
          "Permissible provided the company maintains a favourable bank balance above R500,000",
          "Lawful under the Companies Act because bank reconciliations are purely optional recommendations",
          "Permissible if the bookkeeper conducts a verbal check with the bank call center once a year"]),

        ("During an unannounced internal audit at **Karoo Motors Ltd**, the auditor found that the storekeeper responsible for receiving spare parts is also the sole person who authorizes supplier invoices and signs electronic EFT payment releases.",
         "Critical failure of segregation of duties: Allowing one individual to receive goods, approve invoices, and release payments creates massive opportunity for fictitious purchases and unrecorded theft without detection.",
         ["Optimal operational efficiency that streamlines the procurement and payment workflow",
          "Permissible provided the storekeeper has more than ten years of loyal service to the company",
          "An informal workplace practice recognized in South African motor workshop trade unions",
          "Acceptable because dividing duties among multiple employees increases administrative wage expenses",
          "Lawful provided the storekeeper signs an annual declaration of personal honesty",
          "A minor human resource matter that has zero impact on financial statement accuracy"]),

        ("Supplier **Vaal Steel Ltd** charged **Protea Hardware Ltd** an unbudgeted interest penalty of **R28,000** at 24% p.a. on an overdue account. The credit manager approved and paid the interest without querying it, even though the delay was caused by Vaal Steel delivering the wrong invoice address.",
         "Unjustified loss and lack of internal control: The credit manager failed to protect company funds by disputing an illegitimate penalty caused by supplier error. Management must reverse the interest and enforce invoice verification protocols.",
         ["Completely justified because commercial suppliers are legally entitled to charge any interest rate they choose",
          "Permissible provided the interest is deducted as an operating expense in the corporate tax return",
          "A routine supplier charge that should be absorbed into general manufacturing overhead without dispute",
          "Acceptable practice because disputing interest penalties damages commercial goodwill with suppliers",
          "Lawful under King IV as fair compensation to suppliers for late payment friction",
          "An immaterial amount that does not require investigation by internal auditors"]),

        ("The bank statement of **Blyde Timber Merchants Ltd** showed a debit of **R95,000** with the description 'EFT Outward: Unapproved'. Investigation revealed that hackers accessed the financial manager's unencrypted computer through phishing and initiated an unauthorized transfer.",
         "Cyber fraud and data security breach: Severe violation of cyber risk governance under King IV Principle 11. Management must immediately report the fraud to the bank's fraud unit, lay criminal charges, isolate servers, and implement two-factor authentication.",
         ["A routine commercial risk that should be written off as an ordinary bank charge in the CPJ",
          "Permissible because commercial banks guarantee automatic full reimbursement for all cyber theft",
          "A minor computer glitch that should be resolved by deleting the manager's email inbox",
          "Acceptable practice because all modern businesses experience quarterly cyber theft losses",
          "Lawful provided the financial manager changes the computer desktop wallpaper password",
          "An administrative issue that should be concealed from the Board Audit Committee to avoid panic"]),

        ("A cashier at **Gauteng Health Stores Ltd** routinely holds back physical cash received from weekend cash sales, depositing it into the bank on Thursday of the following week so that he can use the cash for personal sports betting over the weekend.",
         "Unauthorized borrowing, fraud, and breach of trust: Using company funds for personal gain, even temporarily, is criminal theft and embezzlement. The cashier must be dismissed, and management must mandate daily banking of all cash takings.",
         ["Resourceful personal initiative provided the cashier deposits the exact original cash total on Thursday",
          "Permissible under South African labour law because the company suffered zero permanent financial loss",
          "An informal short-term interest-free staff loan recognized under retail trade custom",
          "Acceptable practice provided the cashier wins the bets and donates 10% of winnings to the staff tea fund",
          "Lawful under the Basic Conditions of Employment Act as flexible cash custody",
          "A minor disciplinary infraction that only requires a friendly verbal reminder from the manager"]),

        ("The accountant of **Polokwane Cash & Carry Ltd** noticed an unpresented cheque of **R34,000** issued 8 months ago to a supplier. The accountant created a fake creditor account and transferred the cancelled cheque proceeds to his personal bank account.",
         "Fraud and embezzlement: Cancelling a stale cheque requires debiting Bank and crediting the legitimate supplier in the Creditors Ledger. Diverting funds to a personal account constitutes criminal theft.",
         ["Clever accounting recovery that converts forgotten cheques into personal executive bonuses",
          "Permissible because cheques older than six months become the legal property of the bookkeeper",
          "A routine bookkeeping write-off that does not require disclosure to the external auditors",
          "Acceptable under King IV as informal performance remuneration for diligent accountants",
          "Lawful provided the accountant pays personal SARS income tax on the transferred proceeds",
          "An administrative issue to be resolved by issuing a verbal warning"]),

        ("The credit controller of **Durban Fashion House Ltd** allowed her brother-in-law to purchase R250,000 of boutique merchandise on 30-day credit without a credit application, credit check, or signed surety bond.",
         "Nepotism, conflict of interest, and breach of internal credit policy: Violates King IV Principle 1. When the relative defaulted, the company suffered a complete loss. Management must enforce independent credit committee vetting.",
         ["Commendable family support that promotes local entrepreneurship and retail trade growth",
          "Permissible under South African company law provided the relative promises to pay eventually",
          "A private family arrangement that falls strictly outside corporate governance oversight",
          "Acceptable practice because doing business with relatives always guarantees customer loyalty",
          "Lawful provided the credit controller offers the same credit terms to other retail clients",
          "A minor sales issue that should be absorbed into general bad debts without investigation"]),

        ("A receiving clerk at **Kimberley Mining Gear Ltd** signed a supplier delivery note for 50 hydraulic drill pumps, but only 35 pumps were physically delivered. The clerk accepted a R15,000 cash bribe from the delivery driver to overlook the shortage.",
         "Bribery, corruption, and collusion: Critical failure of receiving controls. The company paid for 50 pumps while receiving only 35, suffering a R120,000 loss. Both the clerk and driver face criminal fraud charges.",
         ["Standard commercial expediting fee that speeds up logistics turnaround times",
          "An informal workplace perk recognized in the mining supplies wholesale industry",
          "A minor logistical delivery discrepancy that will balance out on future purchase orders",
          "Permissible provided the clerk shares the cash bribe with other warehouse staff",
          "Lawful under the Basic Conditions of Employment Act as informal tip income",
          "Acceptable provided the supplier delivers the remaining 15 pumps within six months"]),

        ("The financial manager of **Rustenburg Tool Mart Ltd** deliberately entered an unpresented cheque of **R120,000** in the Bank Reconciliation Statement on 28 February, even though the cheque was only drawn and signed on 5 March.",
         "Window dressing and cut-off fraud: Artificially backdating payments to reduce reported bank balances or manipulate working capital ratios violates IFRS and Section 29 of the Companies Act.",
         ["Prudent year-end balance sheet presentation that reflects upcoming financial commitments",
          "Permissible provided the cheque is delivered to the supplier during the first week of March",
          "A standard accounting practice actively encouraged by commercial banks to minimize overdrafts",
          "Acceptable under King IV as forward-looking financial management",
          "Lawful because a difference of five days is considered an immaterial accounting timing difference",
          "An administrative convenience that does not affect financial statement credibility"]),

        ("The cashier at **Witbank Electrical Mart Ltd** routinely deposits cash takings two days late, leaving daily cash bags overnight in an unlocked wooden desk drawer in the sales office.",
         "Gross negligence and failure of physical asset protection: Exposes company cash to opportunistic burglary and internal theft. Cash takings must be locked in a certified drop-safe and banked daily by an armed transit service.",
         ["Acceptable practice provided the sales office door is locked with a standard cylinder key",
          "A minor operational convenience that saves cashier time traveling to commercial banks",
          "Permissible because commercial property insurance covers all cash left in desk drawers",
          "A routine retail procedure that falls strictly outside corporate internal audit scope",
          "Lawful under King IV as flexible daily cashier workflow",
          "Acceptable provided the cashier counts the cash again on the following morning"])
    ]

    for title_f, sc_f, corr_f, *wrongs_f in fraud_scenarios:
        # 1. Hard Q: Evaluation of Fraud / Irregularity Scenario
        if counts["hard"] < 200:
            q_f1 = f"**Internal Control & Fraud Scenario — {title_f}**:\n\n*\"{sc_f}\"*\n\nProvide the most professional evaluation under CAPS Accounting standards and the King IV Code of Governance:"
            exp_f1 = f"Evaluation: **{corr_f}**."
            add_q("hard", "Fraud Detection & Internal Control", q_f1, corr_f, wrongs_f, "Evaluating", f"Evaluate fraud scenario for {title_f}", exp_f1)

        # 2. Hard Q: Internal Control Remedy
        if counts["hard"] < 200:
            q_f2 = f"Identify the primary internal control measure required to prevent the malpractice described in: *\"{title_f}\"*"
            c_frem = f"Implement strict segregation of duties, daily independent banking verifications, dual electronic authorization on EFTs, and surprise internal audits as required by King IV."
            w_frem = [
                "Abolish all cash sales and force all customers to pay with physical post-dated cheques",
                "Cease preparing Bank Reconciliation Statements and allow commercial banks to manage all ledgers",
                "Permit department managers to approve payments to their own family enterprises without disclosure",
                "Prohibit external registered auditors from inspecting bank statements or cash journals",
                "Increase retail markups by 30% to cover all internal embezzlement losses",
                "Destroy all cash register till rolls and receipt books after 14 days"
            ]
            exp_f2 = f"Correct Internal Control Remedy: **{c_frem}**."
            add_q("hard", "Fraud Detection & Internal Control", q_f2, c_frem, w_frem, "Evaluating", f"Identify internal control remedy for {title_f}", exp_f2)

    # Multi-step complex reconciliation calculations (25 cases)
    complex_rec_cases = [
        ("Protea Hardware Ltd", 65000.0, 72500.0, 32000.0, 24500.0, 1800.0, 1200.0, 4500.0, 1500.0),
        ("Kavango Auto Spares Ltd", 95000.0, 106000.0, 44000.0, 36200.0, 2600.0, 1800.0, 6200.0, 2100.0),
        ("Algoa Furnishers Ltd", 54000.0, 60500.0, 27000.0, 21800.0, 1500.0, 950.0, 3800.0, 1300.0),
        ("Soweto Retail Mart Ltd", 135000.0, 151200.0, 58000.0, 48500.0, 3500.0, 2400.0, 8900.0, 3000.0),
        ("Drakensberg Tools Ltd", 72000.0, 80400.0, 36000.0, 29800.0, 2100.0, 1400.0, 5100.0, 1700.0),
        ("Zululand Wholesalers Ltd", 155000.0, 173500.0, 68000.0, 56800.0, 4100.0, 2800.0, 10500.0, 3500.0),
        ("Highveld Computech Ltd", 105000.0, 117500.0, 49000.0, 41200.0, 2900.0, 2000.0, 7200.0, 2400.0),
        ("Karoo Motors Ltd", 122000.0, 136800.0, 56000.0, 47200.0, 3300.0, 2300.0, 8400.0, 2800.0),
        ("Table Mountain Books Ltd", 45000.0, 50200.0, 22000.0, 18200.0, 1250.0, 850.0, 3100.0, 1050.0),
        ("Springbok Sports Mart Ltd", 86000.0, 96200.0, 41000.0, 34500.0, 2400.0, 1650.0, 5900.0, 1950.0),
        ("Limpopo Farm Supplies Ltd", 115000.0, 128800.0, 53000.0, 44800.0, 3150.0, 2200.0, 7900.0, 2650.0),
        ("Blyde Timber Merchants Ltd", 64000.0, 71500.0, 31000.0, 26000.0, 1800.0, 1250.0, 4400.0, 1500.0),
        ("Gauteng Health Stores Ltd", 148000.0, 165800.0, 65000.0, 54500.0, 3900.0, 2700.0, 10200.0, 3400.0),
        ("Free State Grain Mart Ltd", 84000.0, 93800.0, 40000.0, 33500.0, 2350.0, 1600.0, 5800.0, 1950.0),
        ("Namaqua Diamond Jewelers Ltd", 175000.0, 196200.0, 76000.0, 63800.0, 4600.0, 3200.0, 12100.0, 4050.0),
        ("Outeniqua Garden World Ltd", 58000.0, 64800.0, 28000.0, 23400.0, 1600.0, 1100.0, 4000.0, 1350.0),
        ("Mpumalanga Tile Center Ltd", 110000.0, 123200.0, 51000.0, 42800.0, 3050.0, 2100.0, 7600.0, 2550.0),
        ("Ezulwini Homeware Ltd", 68000.0, 76000.0, 33000.0, 27600.0, 1900.0, 1300.0, 4700.0, 1600.0),
        ("Vaal Triangle Motors Ltd", 192000.0, 215000.0, 85000.0, 71500.0, 5100.0, 3600.0, 13200.0, 4400.0),
        ("Stellenbosch Cellars Ltd", 91000.0, 101800.0, 43000.0, 36200.0, 2550.0, 1750.0, 6300.0, 2100.0),
        ("Tshwane Auto Spares Ltd", 119000.0, 133200.0, 55000.0, 46200.0, 3250.0, 2250.0, 8200.0, 2750.0),
        ("Richards Bay Tools Ltd", 79000.0, 88400.0, 38000.0, 31800.0, 2200.0, 1500.0, 5500.0, 1850.0),
        ("Polokwane Cash & Carry Ltd", 205000.0, 229800.0, 92000.0, 77500.0, 5500.0, 3850.0, 14200.0, 4750.0),
        ("Kimberley Mining Gear Ltd", 102000.0, 114200.0, 48000.0, 40400.0, 2850.0, 1950.0, 7000.0, 2350.0),
        ("Durban Fashion House Ltd", 88000.0, 98500.0, 42000.0, 35200.0, 2450.0, 1700.0, 6100.0, 2050.0),
        ("Paarl Fresh Foods Ltd", 112000.0, 125400.0, 52000.0, 43600.0, 3100.0, 2150.0, 7700.0, 2600.0),
        ("Midrand IT Direct Ltd", 165000.0, 184800.0, 72000.0, 60400.0, 4400.0, 3050.0, 11400.0, 3850.0),
        ("Centurion Sports Emporium Ltd", 78000.0, 87400.0, 39000.0, 32700.0, 2250.0, 1550.0, 5400.0, 1820.0),
        ("Bloemfontein Meats Ltd", 136000.0, 152300.0, 59000.0, 49500.0, 3600.0, 2500.0, 9400.0, 3180.0),
        ("East London Marine Spares Ltd", 66000.0, 73900.0, 33000.0, 27700.0, 1900.0, 1320.0, 4600.0, 1550.0),
        ("Klerksdorp Tile Direct Ltd", 104000.0, 116500.0, 49000.0, 41100.0, 2900.0, 2020.0, 7200.0, 2440.0),
        ("Potchefstroom Stationery Hub Ltd", 59000.0, 66100.0, 29000.0, 24300.0, 1700.0, 1180.0, 4100.0, 1390.0),
        ("George Home Living Ltd", 89000.0, 99700.0, 43000.0, 36100.0, 2500.0, 1740.0, 6200.0, 2090.0),
        ("Secunda Safety & Industrial Ltd", 118000.0, 132200.0, 55000.0, 46200.0, 3250.0, 2260.0, 8200.0, 2770.0),
        ("Vereeniging Steel Goods Ltd", 154000.0, 172500.0, 67000.0, 56300.0, 4100.0, 2850.0, 10700.0, 3620.0),
        ("Welkom Mine Supply Ltd", 108000.0, 121000.0, 51000.0, 42800.0, 3050.0, 2120.0, 7500.0, 2540.0),
        ("Bethlehem Grain Traders Ltd", 85000.0, 95200.0, 41000.0, 34400.0, 2400.0, 1670.0, 5900.0, 2000.0),
        ("Newcastle Tool Warehouse Ltd", 114000.0, 127700.0, 53000.0, 44500.0, 3150.0, 2190.0, 7900.0, 2680.0),
        ("Mossel Bay Marine Traders Ltd", 74000.0, 82900.0, 36000.0, 30200.0, 2100.0, 1460.0, 5100.0, 1740.0),
        ("Mthatha Wholesale Hub Ltd", 97000.0, 108600.0, 46000.0, 38600.0, 2700.0, 1880.0, 6700.0, 2280.0),
        ("Upington Agro Direct Ltd", 64000.0, 71700.0, 32000.0, 26900.0, 1850.0, 1290.0, 4400.0, 1500.0),
        ("Vryheid Timber Depot Ltd", 91000.0, 101900.0, 44000.0, 36900.0, 2550.0, 1780.0, 6300.0, 2140.0),
        ("Ladysmith Fashion Mart Ltd", 70000.0, 78400.0, 35000.0, 29400.0, 2000.0, 1390.0, 4900.0, 1660.0),
        ("Bredasdorp Grain Store Ltd", 102000.0, 114200.0, 48000.0, 40300.0, 2850.0, 1980.0, 7100.0, 2400.0),
        ("Cradock Livestock Hub Ltd", 80000.0, 89600.0, 39000.0, 32700.0, 2300.0, 1600.0, 5600.0, 1900.0),
        ("Makhanda Scholastic Supplies Ltd", 61000.0, 68300.0, 30000.0, 25200.0, 1750.0, 1220.0, 4200.0, 1430.0),
        ("Oudtshoorn Leathercraft Ltd", 82000.0, 91800.0, 40000.0, 33600.0, 2350.0, 1640.0, 5700.0, 1940.0),
        ("Knysna Marine Woods Ltd", 120000.0, 134400.0, 56000.0, 47000.0, 3350.0, 2330.0, 8300.0, 2820.0),
        ("Standerton Milking Systems Ltd", 76000.0, 85100.0, 37000.0, 31100.0, 2150.0, 1500.0, 5300.0, 1800.0),
        ("Harrismith Logistics Depot Ltd", 86000.0, 96300.0, 41000.0, 34400.0, 2450.0, 1710.0, 6000.0, 2040.0),
        ("Kuruman Mineral Traders Ltd", 124000.0, 138900.0, 57000.0, 47900.0, 3450.0, 2410.0, 8600.0, 2920.0),
        ("Thohoyandou Superstore Ltd", 106000.0, 118700.0, 50000.0, 42000.0, 2950.0, 2060.0, 7400.0, 2510.0),
        ("Plettenberg Bay Decor Ltd", 61000.0, 68300.0, 30000.0, 25200.0, 1750.0, 1220.0, 4200.0, 1430.0),
        ("Saldanha Marine Freight Ltd", 151000.0, 169100.0, 66000.0, 55400.0, 4050.0, 2820.0, 10500.0, 3570.0),
        ("Grahamstown Scholastic Ltd", 56000.0, 62700.0, 28000.0, 23500.0, 1600.0, 1120.0, 3900.0, 1320.0),
        ("Springbok Wind Parts Ltd", 110000.0, 123200.0, 51000.0, 42800.0, 3050.0, 2130.0, 7600.0, 2580.0),
        ("Witbank Coal Equipment Ltd", 140000.0, 156800.0, 61000.0, 51200.0, 3800.0, 2650.0, 9700.0, 3300.0),
        ("Paarl Valley Beverages Ltd", 97000.0, 108600.0, 45000.0, 37800.0, 2700.0, 1880.0, 6700.0, 2280.0),
        ("Centurion Office Machines Ltd", 88000.0, 98600.0, 42000.0, 35300.0, 2500.0, 1740.0, 6100.0, 2070.0),
        ("Bloemfontein Grain Merchants Ltd", 78000.0, 87400.0, 38000.0, 31900.0, 2250.0, 1570.0, 5400.0, 1840.0),
        ("East London Fishing Gear Ltd", 63000.0, 70600.0, 31000.0, 26000.0, 1800.0, 1260.0, 4400.0, 1500.0),
        ("Klerksdorp Mining Supplies Ltd", 104000.0, 116500.0, 48000.0, 40300.0, 2900.0, 2020.0, 7200.0, 2450.0),
        ("Potchefstroom Feeds Mart Ltd", 84000.0, 94100.0, 40000.0, 33600.0, 2350.0, 1640.0, 5800.0, 1970.0),
        ("Newcastle Heavy Steels Ltd", 132000.0, 147800.0, 58000.0, 48700.0, 3650.0, 2550.0, 9200.0, 3120.0),
        ("Mossel Bay Offshore Mart Ltd", 72000.0, 80600.0, 35000.0, 29400.0, 2000.0, 1400.0, 5000.0, 1700.0),
        ("Mthatha Timber Supplies Ltd", 65000.0, 72800.0, 32000.0, 26900.0, 1800.0, 1260.0, 4500.0, 1530.0),
        ("Upington Sun Agro Supplies Ltd", 59000.0, 66100.0, 29000.0, 24400.0, 1650.0, 1150.0, 4100.0, 1390.0),
        ("Vryheid Coal Merchants Ltd", 95000.0, 106400.0, 43000.0, 36100.0, 2650.0, 1850.0, 6600.0, 2240.0),
        ("Ladysmith Textiles Mart Ltd", 125000.0, 140000.0, 55000.0, 46200.0, 3450.0, 2410.0, 8700.0, 2950.0),
        ("Bredasdorp Wheat Store Ltd", 152000.0, 170200.0, 66000.0, 55400.0, 4200.0, 2940.0, 10600.0, 3600.0),
        ("Cradock Merinos Supplies Ltd", 81000.0, 90700.0, 38000.0, 31900.0, 2250.0, 1570.0, 5600.0, 1900.0),
        ("Makhanda Print Supplies Ltd", 168000.0, 188100.0, 72000.0, 60500.0, 4650.0, 3250.0, 11700.0, 3970.0),
        ("Oudtshoorn Leather Supplies Ltd", 92000.0, 103000.0, 42000.0, 35300.0, 2550.0, 1780.0, 6400.0, 2180.0),
        ("Centurion Office Machines Ltd", 88000.0, 98600.0, 41000.0, 34500.0, 2450.0, 1710.0, 6100.0, 2070.0),
        ("Bloemfontein Grain Merchants Ltd", 78000.0, 87400.0, 37000.0, 31100.0, 2150.0, 1500.0, 5400.0, 1840.0),
        ("East London Fishing Gear Ltd", 63000.0, 70600.0, 30000.0, 25200.0, 1750.0, 1220.0, 4400.0, 1500.0),
        ("Klerksdorp Mining Supplies Ltd", 104000.0, 116500.0, 47000.0, 39500.0, 2900.0, 2020.0, 7200.0, 2450.0),
        ("Potchefstroom Feeds Mart Ltd", 84000.0, 94100.0, 39000.0, 32800.0, 2350.0, 1640.0, 5800.0, 1970.0),
        ("George Hardwood Depot Ltd", 89000.0, 99700.0, 42000.0, 35300.0, 2500.0, 1740.0, 6200.0, 2090.0),
        ("Secunda Safety Wear Ltd", 118000.0, 132200.0, 54000.0, 45400.0, 3250.0, 2260.0, 8200.0, 2770.0),
        ("Vereeniging Boiler Supplies Ltd", 154000.0, 172500.0, 66000.0, 55400.0, 4100.0, 2850.0, 10700.0, 3620.0),
        ("Welkom Shaft Merchants Ltd", 108000.0, 121000.0, 50000.0, 42000.0, 3050.0, 2120.0, 7500.0, 2540.0),
        ("Bethlehem Farmers Coop Ltd", 85000.0, 95200.0, 40000.0, 33600.0, 2400.0, 1670.0, 5900.0, 2000.0),
        ("Newcastle Heavy Hardware Ltd", 114000.0, 127700.0, 52000.0, 43700.0, 3150.0, 2190.0, 7900.0, 2680.0),
        ("Mossel Bay Fuel Traders Ltd", 145000.0, 162400.0, 63000.0, 52900.0, 4000.0, 2800.0, 10100.0, 3430.0),
        ("Mthatha General Dealers Ltd", 71000.0, 79500.0, 35000.0, 29400.0, 1980.0, 1380.0, 4900.0, 1670.0),
        ("Upington Sun Trading Ltd", 62000.0, 69400.0, 31000.0, 26000.0, 1720.0, 1200.0, 4300.0, 1460.0),
        ("Vryheid Timber Merchants Ltd", 88000.0, 98600.0, 41000.0, 34400.0, 2450.0, 1710.0, 6100.0, 2070.0),
        ("Ladysmith Drapery Ltd", 57000.0, 63800.0, 28000.0, 23500.0, 1600.0, 1120.0, 4000.0, 1350.0),
        ("Bredasdorp Agri Wholesale Ltd", 96000.0, 107500.0, 44000.0, 37000.0, 2650.0, 1850.0, 6700.0, 2270.0),
        ("Cradock Livestock Supplies Ltd", 75000.0, 84000.0, 37000.0, 31100.0, 2100.0, 1460.0, 5200.0, 1770.0),
        ("Makhanda Stationery Ltd", 52000.0, 58200.0, 26000.0, 21800.0, 1450.0, 1010.0, 3600.0, 1220.0),
        ("Oudtshoorn Leather Mart Ltd", 68000.0, 76100.0, 32000.0, 26900.0, 1850.0, 1300.0, 4700.0, 1600.0),
        ("Knysna Marine Hardware Ltd", 112000.0, 125400.0, 51000.0, 42800.0, 3100.0, 2170.0, 7800.0, 2650.0)
    ]

    for co_c, open_b, close_bs, dep_out, chk_unpres, b_fee, b_int, b_err_add, b_err_sub in complex_rec_cases:
        # Full multi-step reconciliation solving for adjusted bank balance and verification
        crj_tot = b_int + b_err_add
        cpj_tot = b_fee + b_err_sub
        adj_bank_c = open_b + crj_tot - cpj_tot

        # 1. Hard Q: Calculate Reconciled Adjusted Bank Account Balance
        if counts["hard"] < 200:
            c_abc = f"R{adj_bank_c:,.2f}"
            w_abc = [
                f"R{open_b:,.2f} (unadjusted opening balance)",
                f"R{open_b + crj_tot:,.2f} (omitted CPJ deductions)",
                f"R{open_b - cpj_tot:,.2f} (omitted CRJ additions)",
                f"R{adj_bank_c * 1.15:,.2f}",
                f"R{adj_bank_c * 0.85:,.2f}",
                f"R{(adj_bank_c + 18000):,.2f}",
                f"R{(adj_bank_c - 15000):,.2f}"
            ]
            q_abc = (f"The Bank Account of **{co_c}** had an unadjusted debit balance of **R{open_b:,.2f}** on 30 November. "
                     f"The Bank Statement showed the following:\n"
                     f"- Interest on favourable balance: **R{b_int:,.2f}**\n"
                     f"- Direct credit transfer from debtor: **R{b_err_add:,.2f}**\n"
                     f"- Bank service fees and transaction charges: **R{b_fee:,.2f}**\n"
                     f"- Debit order for monthly insurance: **R{b_err_sub:,.2f}**\n"
                     f"Calculate the **Adjusted Bank Account balance** to be reflected in the Balance Sheet:")
            exp_abc = (f"CRJ Additions = Bank Interest (R{b_int:,.2f}) + Direct Deposit (R{b_err_add:,.2f}) = R{crj_tot:,.2f}\n"
                       f"CPJ Deductions = Bank Fees (R{b_fee:,.2f}) + Debit Order (R{b_err_sub:,.2f}) = R{cpj_tot:,.2f}\n"
                       f"Adjusted Bank Balance = R{open_b:,.2f} + R{crj_tot:,.2f} - R{cpj_tot:,.2f} = {c_abc}.")
            add_q("hard", "Complex Bank Reconciliation Calculations", q_abc, c_abc, w_abc, "Applying", f"Calculate adjusted balance for {co_c}", exp_abc)

        # 2. Hard Q: Reverse-engineering the Bank Statement Closing Balance
        # Bank Statement Balance + Outstanding Deposit - Unpresented Cheques = Adjusted Bank Balance
        # Bank Statement Balance = Adjusted Bank Balance - Outstanding Deposit + Unpresented Cheques
        rev_bs_bal = adj_bank_c - dep_out + chk_unpres
        if counts["hard"] < 200:
            c_rbs = f"R{rev_bs_bal:,.2f} ({'Credit/Favourable' if rev_bs_bal >= 0 else 'Debit/Overdraft'})"
            w_rbs = [
                f"R{adj_bank_c + dep_out - chk_unpres:,.2f} (added deposit and deducted cheques)",
                f"R{adj_bank_c:,.2f} (used adjusted bank account balance)",
                f"R{rev_bs_bal * 1.15:,.2f}",
                f"R{rev_bs_bal * 0.85:,.2f}",
                f"R{(rev_bs_bal + 22000):,.2f}",
                f"R{(rev_bs_bal - 18000):,.2f}",
                f"R{dep_out - chk_unpres:,.2f}"
            ]
            q_rbs = (f"The adjusted Bank Account of **{co_c}** reflects a favourable balance of **R{adj_bank_c:,.2f}**. "
                     f"The Bank Reconciliation Statement lists an outstanding deposit of **R{dep_out:,.2f}** "
                     f"and unpresented cheques totaling **R{chk_unpres:,.2f}**. There were no bank errors. "
                     f"Reverse-engineer and calculate the **Balance as per Bank Statement** at month-end:")
            exp_rbs = (f"Reconciliation Formula: Bank Statement Balance + Outstanding Deposit - Unpresented Cheques = Adjusted Bank Balance\n"
                       f"Bank Statement Balance = Adjusted Bank Balance (R{adj_bank_c:,.2f}) - Outstanding Deposit (R{dep_out:,.2f}) + Unpresented Cheques (R{chk_unpres:,.2f})\n"
                       f"= {c_rbs}.")
            add_q("hard", "Complex Bank Reconciliation Calculations", q_rbs, c_rbs, w_rbs, "Applying", f"Reverse engineer bank statement for {co_c}", exp_rbs)

    print(f"Generated: easy={counts['easy']}, medium={counts['medium']}, hard={counts['hard']}")

    output_path = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting/paper2_acc_reconciliations.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"SUCCESS: {output_path} created with {len(questions)} questions: {counts}")

if __name__ == "__main__":
    build_reconciliations()
