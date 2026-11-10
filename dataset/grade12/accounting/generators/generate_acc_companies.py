import json
import os

def build_companies():
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
        qid = f"ACC_P1_COMP_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Companies & Corporate Governance",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Companies & Corporate Governance",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # =========================================================================

    easy_concepts = [
        ("Memorandum of Incorporation (MOI)",
         "The statutory founding document setting out the rights, duties, and responsibilities of shareholders, directors, and other stakeholders in a South African company",
         "The prospectus issued to invite members of the public to subscribe for shares",
         "The annual contract signed between the company and its external registered auditors",
         "The agreement between the company and commercial banks regarding overdraft facilities",
         "The internal policy manual governing daily staff attendance and disciplinary procedures",
         "The certificate issued by SARS authorizing the company to deduct PAYE from salaries",
         "The register of fixed assets maintained by the financial manager"),

        ("Authorized Share Capital",
         "The maximum number of shares that a company is legally permitted to issue as stated in its Memorandum of Incorporation (MOI)",
         "The actual number of shares that have been sold and issued to registered shareholders",
         "The market value of all shares trading on the Johannesburg Stock Exchange (JSE)",
         "The total cash received from issuing shares since the date of incorporation",
         "The minimum number of shares directors must purchase before taking office",
         "The total profit retained by the company since its founding date",
         "The number of shares repurchased by the company during the financial year"),

        ("Issued Share Capital",
         "The portion of authorized share capital that has actually been allocated and issued to shareholders",
         "The total pool of shares authorized in the Memorandum of Incorporation that can never be exceeded",
         "The reserves set aside by the directors for future asset replacements",
         "The net asset value per share multiplied by the current inflation rate",
         "The total borrowed capital obtained through long-term mortgage loans and debentures",
         "The number of unissued shares kept in reserve for employee share incentive schemes",
         "The total interim and final dividends paid out to shareholders during the year"),

        ("Limited Liability of Shareholders",
         "Shareholders cannot be held personally liable for the debts of the company; their loss is limited to the amount they invested in shares",
         "Shareholders have limited rights to vote at the Annual General Meeting (AGM)",
         "The company is only allowed to incur debt up to the par value of its issued shares",
         "Directors are personally liable for all bank loans incurred during normal trading",
         "The company can only operate for a limited period before mandatory liquidation",
         "Shareholders are not entitled to receive dividends during periods of economic recession",
         "The maximum dividend payable per share is strictly capped by the Companies Act"),

        ("Legal Entity (Separate Juridical Persona)",
         "A registered company exists as a separate legal entity distinct from its owners, capable of owning assets, entering contracts, and suing or being sued in its own name",
         "A legal doctrine meaning directors are the sole owners of all company property",
         "A rule stating that a company must dissolve automatically when a major shareholder passes away",
         "A requirement that every shareholder must be registered as a legal practitioner with the High Court",
         "An agreement where commercial banks assume ownership of all company assets",
         "A provision allowing shareholders to access company bank accounts for personal use",
         "A regulation stating that profits must be taxed directly in the personal tax returns of shareholders"),

        ("Public Company ((Ltd)) vs Private Company (((Pty) Ltd))",
         "A public company may offer its shares to the public and list on the JSE, whereas a private company restricts share transfers and cannot offer shares to the public",
         "A private company must have at least three directors while a public company needs only one director",
         "A public company is exempt from preparing annual financial statements and external audits",
         "A private company's name must end with 'Ltd' while a public company's name ends with '(Pty) Ltd'",
         "A public company has unlimited liability while a private company has limited liability",
         "A private company must hold an open Annual General Meeting broadcast to the general public",
         "A public company cannot obtain commercial loans from South African financial institutions"),

        ("Role of the Audit Committee",
         "An independent committee of at least three non-executive directors responsible for overseeing financial reporting, internal controls, and auditor independence",
         "A group of executive directors tasked with daily bookkeeping and authorizing petty cash vouchers",
         "A panel of external shareholders appointed to manage advertising and sales campaigns",
         "A government oversight committee appointed by SARS to collect provisional company taxes",
         "A board subcommittee responsible solely for setting retail selling prices and product discounts",
         "An internal staff union committee negotiating annual wage increases for factory workers",
         "A committee formed by commercial banks to monitor compliance with bank overdraft covenants"),

        ("Fiduciary Duty of Directors",
         "The legal duty of directors to act in good faith, with honesty, integrity, and always in the best economic interest of the company rather than personal gain",
         "The obligation of directors to guarantee an annual minimum return on investment of 15% to shareholders",
         "The duty of directors to personally settle all unpaid creditors if the company experiences cash flow shortages",
         "The right of directors to borrow company funds interest-free without disclosing it to shareholders",
         "The authority of directors to alter the Memorandum of Incorporation without shareholder approval",
         "The obligation of directors to award corporate procurement contracts exclusively to close relatives",
         "The requirement that directors must hold an undergraduate degree in chartered accountancy"),

        ("King IV Code: Ethical Culture",
         "A core corporate governance outcome ensuring leadership demonstrates integrity, competence, responsibility, accountability, fairness, and transparency",
         "A requirement that all company advertising must feature religious messages and endorsements",
         "A financial rule stating that 50% of annual profits must be donated to registered charitable trusts",
         "A regulation preventing South African companies from engaging in international import and export trade",
         "An accounting standard mandating the replacement of historical cost accounting with inflation accounting",
         "A legal clause exempting corporate directors from paying personal income tax on director fees",
         "A policy prohibiting companies from operating multiple branches across different provinces"),

        ("External Auditor Independence",
         "The external auditor must have no financial or operational interest in the client company to ensure an unbiased, objective opinion on the financial statements",
         "The external auditor must be an employee of the company reporting directly to the Chief Executive Officer",
         "The external auditor is permitted to own up to 25% of the ordinary share capital of the audited firm",
         "The external auditor must guarantee that no fraud or theft has occurred within the client organization",
         "The external auditor prepares and enters the month-end closing journal entries into the general ledger",
         "The external auditor is appointed by the Chief Financial Officer without shareholder involvement",
         "The external auditor is legally responsible for paying the company's provisional tax liabilities"),

        ("Unqualified Audit Report ('Clean Report')",
         "The auditor concludes that the financial statements fairly present, in all material respects, the financial position and performance in accordance with IFRS and Companies Act",
         "The auditor is unable to express an opinion due to severe limitations in obtaining audit evidence",
         "The auditor identifies widespread, pervasive misstatements that render the financial statements completely misleading",
         "The auditor states that financial statements are fair except for a specific, isolated disagreement regarding one item",
         "The auditor refuses to sign the financial statements because the company made an operating loss",
         "The auditor certifies that the company will remain profitable and liquid for the next twenty years",
         "The auditor confirms that zero errors, omissions, or minor irregularities exist in the books"),

        ("Qualified Audit Report",
         "The auditor finds that the financial statements are fairly presented except for a specific, material matter that is not pervasive",
         "The auditor confirms that the financial records are completely free from any misstatement or error",
         "The auditor declines to express any opinion because company management destroyed accounting records",
         "The auditor issues a declaration of bankruptcy against the company and orders asset liquidation",
         "The auditor certifies that the company's internal control system is the best in the industry",
         "The auditor finds that the entire financial statements are thoroughly fraudulent and unreliable",
         "The auditor confirms that directors have fulfilled all ethical duties under King IV without exception"),

        ("Adverse Audit Opinion",
         "The auditor concludes that misstatements are both material and pervasive, rendering the financial statements as a whole misleading and unreliable",
         "The auditor issues a clean opinion confirming total compliance with International Financial Reporting Standards",
         "The auditor finds an isolated, minor arithmetic error on a petty cash voucher",
         "The auditor approves the financial statements subject only to an immaterial depreciation adjustment",
         "The auditor resigns because the company failed to meet its budgeted sales target for the year",
         "The auditor expresses confidence that the company's share price will increase significantly on the JSE",
         "The auditor confirms that external confirmation letters were received from all commercial banks"),

        ("Disclaimer of Audit Opinion",
         "The auditor was unable to obtain sufficient appropriate audit evidence and cannot express an opinion on the financial statements",
         "The auditor certifies that the financial statements are completely accurate and without fault",
         "The auditor confirms that only minor typographical errors were detected during field testing",
         "The auditor recommends that shareholders immediately re-elect the current board of directors",
         "The auditor endorses the company's creditworthiness for a multi-million rand commercial bank loan",
         "The auditor guarantees that company inventories are valued strictly at net realizable value",
         "The auditor confirms that all board resolutions complied fully with JSE Listings Requirements"),

        ("Ordinary Shares vs Preference Shares",
         "Ordinary shareholders are equity owners with voting rights and variable dividends, whereas preference shareholders enjoy a fixed dividend rate and priority in asset liquidation",
         "Ordinary shareholders receive a fixed guaranteed dividend every quarter regardless of company profitability",
         "Preference shareholders have the exclusive right to vote for the election of board directors at the AGM",
         "Ordinary shares cannot be traded on the open market, while preference shares are freely negotiable",
         "Preference shareholders are personally liable for company debts if operating cash flow turns negative",
         "Ordinary shareholders are repaid their capital before preference shareholders upon company dissolution",
         "Preference shareholders are entitled to retain all undistributed profits upon company winding-up"),

        ("Dividends Tax in South Africa",
         "A 20% withholding tax deducted by the company from dividends payable to individual shareholders and remitted directly to SARS",
         "A 27% direct company income tax levied on net profit before tax",
         "A 15% value-added tax charged on the sale of new ordinary shares to the general public",
         "A penalty tax levied on companies that fail to distribute at least 80% of net profits as dividends",
         "A personal transfer tax paid by directors when buying back shares on the open market",
         "A municipal property rate levied on factory buildings owned by public listed corporations",
         "An import customs surcharge levied on foreign investors purchasing shares on the JSE"),

        ("Interim Dividend",
         "A dividend declared and paid halfway through the financial year based on interim six-month operating results",
         "A dividend payable only upon the complete liquidation and dissolution of the company",
         "A dividend declared at the end of the financial year and confirmed at the Annual General Meeting",
         "A mandatory interest payment made to long-term commercial bank mortgage lenders",
         "A bonus payment distributed exclusively to executive directors for hitting annual sales targets",
         "A cash refund paid to customers who return damaged goods within thirty days of purchase",
         "An advance payment made to raw material suppliers prior to delivery of inventory"),

        ("Final Dividend",
         "A dividend recommended by directors at year-end and declared to shareholders of record at the end of the financial year",
         "A dividend paid during the first week of the financial year prior to any commercial trading",
         "A refund of share capital paid to founding shareholders when new ordinary shares are issued",
         "A fixed interest coupon paid semi-annually to holders of registered corporate debentures",
         "A tax rebate received from SARS due to overpayment of provisional corporate income taxes",
         "A special distribution funded entirely by obtaining short-term commercial bank overdrafts",
         "A distribution of company manufacturing equipment directly to institutional investors"),

        ("Section 46 Solvency and Liquidity Test",
         "A statutory requirement under the Companies Act ensuring that assets exceed liabilities (solvency) and the company can pay debts as they become due for 12 months (liquidity) after a distribution",
         "A test requiring a company to hold at least R10 million in physical cash in its primary cheque account",
         "A rule stating that current assets must be exactly double current liabilities at all times",
         "A regulation prohibiting companies from issuing shares if the debt-equity ratio exceeds 2:1",
         "A test conducted by commercial banks before approving any business credit card application",
         "A mandatory audit procedure verifying that factory machinery has been maintained properly",
         "An evaluation conducted by SARS to verify whether employee PAYE deductions were remitted on time"),

        ("Social and Ethics Committee Mandate",
         "A board committee tasked with monitoring company activities regarding social and economic development, good corporate citizenship, environment, health, and public safety",
         "A committee responsible for auditing daily cashier cash drawers and bank deposit slips",
         "A panel of shareholders authorized to determine retail selling prices for consumer goods",
         "A legal team appointed to defend the company against copyright infringement lawsuits",
         "An executive committee tasked with selecting commercial advertising agencies and slogans",
         "A supervisory board overseeing the installation of factory solar panel electrical wiring",
         "A working group formed to negotiate transport freight tariffs with logistics contractors")
    ]

    for title, corr, *wrongs in easy_concepts:
        q1 = f"In terms of the South African Companies Act No. 71 of 2008 and CAPS curriculum, what is the meaning of **{title}**?"
        exp1 = f"**{title}**: {corr}. This is an essential corporate governance and Companies Act concept under CAPS Grade 12 Accounting."
        add_q("easy", "Company Concepts & Legislation", q1, corr, wrongs, "Remembering", f"Define {title}", exp1)

        q2 = f"Which corporate accounting concept or statutory provision is defined as: *\"{corr}\"*?"
        wr_names_clean = [
            "Internal Audit Mandate", "Debenture Trust Deed", "Memorandum of Understanding",
            "Broad-Based Black Economic Empowerment Charter", "JSE Advisory Circular",
            "SARS Customs and Excise Act", "Basic Conditions of Employment Act"
        ]
        exp2 = f"The definition describes **{title}**. Under South African company law and CAPS Accounting, {corr}."
        add_q("easy", "Company Concepts & Legislation", q2, title, wr_names_clean, "Understanding", f"Identify {title}", exp2)

    # Easy Calculations: 60 realistic South African company cases
    calc_easy_cases = [
        ("Naledi Gold Ltd", 5000000, 3200000, 8.50, 0.40, 0.65),
        ("Protea Valley Ltd", 2000000, 1400000, 6.00, 0.25, 0.45),
        ("Kalahari Solar Ltd", 4000000, 2500000, 12.00, 0.50, 0.80),
        ("Drakensberg Dairy Ltd", 1500000, 900000, 4.50, 0.20, 0.35),
        ("Algoa Bay Fisheries Ltd", 3000000, 2100000, 7.20, 0.30, 0.55),
        ("Ubuntu Logistics Ltd", 6000000, 4500000, 10.00, 0.60, 0.90),
        ("Zululand Sugar Ltd", 2500000, 1800000, 5.50, 0.25, 0.40),
        ("Highveld Steelworks Ltd", 8000000, 5600000, 15.00, 0.75, 1.10),
        ("Karoo Agro Holdings Ltd", 1200000, 850000, 9.00, 0.35, 0.60),
        ("Table Mountain Retail Ltd", 10000000, 7500000, 18.00, 0.80, 1.25),
        ("Springbok Pharma Ltd", 3500000, 2400000, 11.50, 0.45, 0.70),
        ("Limpopo Citrus Ltd", 1800000, 1250000, 6.80, 0.30, 0.50),
        ("Blyde River Timber Ltd", 2200000, 1600000, 8.20, 0.35, 0.55),
        ("Gauteng Tech Solutions Ltd", 5500000, 4000000, 22.00, 1.00, 1.60),
        ("Free State Grain Silos Ltd", 2800000, 1950000, 7.00, 0.28, 0.42),
        ("Namaqua Copper Ltd", 4500000, 3100000, 14.50, 0.65, 0.95),
        ("Outeniqua Transport Ltd", 1600000, 1100000, 5.00, 0.20, 0.35),
        ("Mpumalanga Coal Ltd", 7000000, 5200000, 13.00, 0.55, 0.85),
        ("Ezulwini Hospitality Ltd", 1400000, 950000, 8.00, 0.40, 0.60),
        ("Vaal Triangle Chem Ltd", 3800000, 2700000, 9.50, 0.45, 0.75),
        ("Stellenbosch Vineyards Ltd", 2600000, 1750000, 16.00, 0.70, 1.05),
        ("Tshwane Auto Spares Ltd", 4200000, 3000000, 8.80, 0.38, 0.58),
        ("Richards Bay Terminals Ltd", 6500000, 4800000, 17.50, 0.85, 1.30),
        ("Soweto Retail Hub Ltd", 1900000, 1300000, 6.50, 0.25, 0.45),
        ("Polokwane Milling Ltd", 2400000, 1700000, 7.50, 0.32, 0.52),
        ("Kimberley Mining Supply Ltd", 3200000, 2250000, 12.50, 0.50, 0.80),
        ("Durban Container Depot Ltd", 5800000, 4100000, 19.00, 0.90, 1.40),
        ("Rustenburg Platinum Ltd", 9000000, 6800000, 25.00, 1.20, 1.80),
        ("Witbank Energy Corp Ltd", 4800000, 3400000, 10.50, 0.48, 0.72),
        ("Paarl Bottling Works Ltd", 1700000, 1150000, 9.20, 0.42, 0.68),
        ("Centurion Aerospace Ltd", 3600000, 2500000, 14.00, 0.60, 0.90),
        ("Bloemfontein Food Ltd", 2100000, 1500000, 7.80, 0.32, 0.48),
        ("Midrand Data Corp Ltd", 4600000, 3300000, 18.50, 0.80, 1.20),
        ("East London Marine Ltd", 1850000, 1300000, 6.20, 0.28, 0.44),
        ("Klerksdorp Gold Ltd", 5200000, 3800000, 11.00, 0.50, 0.75),
        ("Potchefstroom Grain Ltd", 2300000, 1600000, 8.40, 0.36, 0.54),
        ("George Timberworks Ltd", 1750000, 1200000, 9.60, 0.40, 0.62),
        ("Secunda Chemical Plant Ltd", 6200000, 4400000, 16.00, 0.70, 1.05),
        ("Vereeniging Steel Ltd", 4100000, 2900000, 12.20, 0.55, 0.82),
        ("Welkom Mine Works Ltd", 3300000, 2350000, 10.20, 0.45, 0.68),
        ("Bethlehem Flour Ltd", 1650000, 1150000, 7.40, 0.30, 0.46),
        ("Newcastle Heavy Forge Ltd", 3900000, 2750000, 13.50, 0.58, 0.88),
        ("Mossel Bay Petroleum Ltd", 5400000, 3900000, 17.00, 0.75, 1.15),
        ("Mthatha Wholesale Ltd", 1550000, 1050000, 6.40, 0.26, 0.40),
        ("Upington Solar Farms Ltd", 2900000, 2050000, 13.00, 0.56, 0.84),
        ("Vryheid Coal Traders Ltd", 2450000, 1750000, 8.60, 0.38, 0.58),
        ("Ladysmith Textiles Ltd", 1950000, 1350000, 7.10, 0.30, 0.45),
        ("Bredasdorp Agri Corp Ltd", 2050000, 1450000, 9.40, 0.40, 0.60),
        ("Cradock Livestock Hub Ltd", 1450000, 1000000, 8.50, 0.35, 0.55),
        ("Makhanda Media Works Ltd", 1350000, 920000, 10.00, 0.42, 0.65),
        ("Oudtshoorn Leathercraft Ltd", 1600000, 1100000, 11.20, 0.48, 0.72),
        ("Knysna Fine Woods Ltd", 2250000, 1550000, 12.80, 0.52, 0.80),
        ("Standerton Dairy Co Ltd", 1900000, 1300000, 7.60, 0.32, 0.50),
        ("Harrismith Freight Ltd", 2700000, 1900000, 10.80, 0.46, 0.70),
        ("Kuruman Manganese Ltd", 4800000, 3450000, 15.50, 0.68, 1.02),
        ("Thohoyandou Trading Ltd", 1700000, 1180000, 6.90, 0.28, 0.44),
        ("Plettenberg Leisure Ltd", 2150000, 1500000, 14.50, 0.62, 0.95),
        ("Saldanha Iron Terminal Ltd", 5100000, 3650000, 16.50, 0.72, 1.10),
        ("Grahamstown Books Ltd", 1250000, 860000, 9.80, 0.40, 0.62),
        ("Springbok Wind Energy Ltd", 3150000, 2200000, 13.80, 0.58, 0.88)
    ]

    for co_name, auth_s, iss_s, avg_p, int_d, fin_d in calc_easy_cases:
        # 1. Unissued Shares
        uniss_s = auth_s - iss_s
        c_uniss = f"{uniss_s:,.0f} shares"
        w_uniss = [
            f"{auth_s:,.0f} shares (used total authorized shares)",
            f"{iss_s:,.0f} shares (confused with issued shares)",
            f"{auth_s + iss_s:,.0f} shares (added authorized and issued)",
            f"{uniss_s * 1.2:,.0f} shares",
            f"{uniss_s * 0.8:,.0f} shares",
            f"{uniss_s + 200000:,.0f} shares",
            f"{uniss_s - 150000:,.0f} shares"
        ]
        q_uniss = (f"The Memorandum of Incorporation of **{co_name}** authorizes the issue of **{auth_s:,.0f}** ordinary shares. "
                   f"To date, the company has issued **{iss_s:,.0f}** ordinary shares. How many ordinary shares remain **unissued**?")
        exp_uniss = (f"Unissued Shares = Authorized Shares - Issued Shares = {auth_s:,.0f} - {iss_s:,.0f} = {c_uniss}. "
                     f"Unissued shares remain in reserve and may be issued in future by resolution of the directors subject to the MOI.")
        add_q("easy", "Ordinary Share Capital Note", q_uniss, c_uniss, w_uniss, "Applying", f"Calculate unissued shares for {co_name}", exp_uniss)

        # 2. Total Share Capital Issued Value
        total_sc = iss_s * avg_p
        c_sc = f"R{total_sc:,.2f}"
        w_sc = [
            f"R{auth_s * avg_p:,.2f} (multiplied by authorized shares instead of issued)",
            f"R{(iss_s * avg_p) * 1.15:,.2f}",
            f"R{(iss_s * avg_p) * 0.85:,.2f}",
            f"R{uniss_s * avg_p:,.2f} (multiplied unissued shares by issue price)",
            f"R{(total_sc + 500000):,.2f}",
            f"R{(total_sc - 400000):,.2f}",
            f"R{iss_s:,.2f} (omitted issue price per share)"
        ]
        q_sc = (f"**{co_name}** has **{iss_s:,.0f}** ordinary shares in issue, which were issued at an average price of **R{avg_p:.2f}** per share. "
                f"Calculate the total value of **Ordinary Share Capital** to be reflected in the Balance Sheet (Statement of Financial Position):")
        exp_sc = (f"Ordinary Share Capital = Issued Shares x Average Issue Price = {iss_s:,.0f} x R{avg_p:.2f} = {c_sc}.")
        add_q("easy", "Ordinary Share Capital Note", q_sc, c_sc, w_sc, "Applying", f"Calculate ordinary share capital for {co_name}", exp_sc)

        # 3. Total Interim Dividends Paid
        tot_int = iss_s * int_d
        c_int = f"R{tot_int:,.2f}"
        w_int = [
            f"R{auth_s * int_d:,.2f} (multiplied by authorized shares)",
            f"R{iss_s * fin_d:,.2f} (calculated final dividend instead of interim dividend)",
            f"R{iss_s * (int_d + fin_d):,.2f} (calculated total annual dividends)",
            f"R{tot_int * 1.2:,.2f}",
            f"R{tot_int * 0.8:,.2f}",
            f"R{tot_int * 0.80:,.2f} (deducted 20% dividends tax from company payment)",
            f"R{(tot_int + 100000):,.2f}"
        ]
        q_int = (f"During the financial year, the directors of **{co_name}** declared and paid an interim dividend of **{int_d * 100:.0f} cents** (R{int_d:.2f}) "
                 f"per share on all **{iss_s:,.0f}** issued ordinary shares. Calculate the total **interim dividend** paid:")
        exp_int = (f"Total Interim Dividend = Number of Issued Shares x Interim Dividend per Share = {iss_s:,.0f} x R{int_d:.2f} = {c_int}. "
                   f"This amount is recorded in the Retained Income Note and Cash Flow Statement (operating activities).")
        add_q("easy", "Retained Income Note", q_int, c_int, w_int, "Applying", f"Calculate interim dividend for {co_name}", exp_int)

        # 4. Total Final Recommended Dividends
        tot_fin = iss_s * fin_d
        c_fin = f"R{tot_fin:,.2f}"
        w_fin = [
            f"R{auth_s * fin_d:,.2f} (calculated on authorized shares)",
            f"R{tot_int:,.2f} (confused with interim dividend)",
            f"R{iss_s * (int_d + fin_d):,.2f} (combined interim and final dividends)",
            f"R{tot_fin * 1.2:,.2f}",
            f"R{tot_fin * 0.8:,.2f}",
            f"R{tot_fin * 0.80:,.2f} (deducted 20% dividends tax)",
            f"R{(tot_fin + 150000):,.2f}"
        ]
        q_fin = (f"At the financial year-end, the directors of **{co_name}** recommended a final dividend of **{fin_d * 100:.0f} cents** (R{fin_d:.2f}) "
                 f"per share on the **{iss_s:,.0f}** ordinary shares in issue. Calculate the total **final dividend**:")
        exp_fin = (f"Total Final Dividend = Number of Issued Shares x Final Dividend per Share = {iss_s:,.0f} x R{fin_d:.2f} = {c_fin}. "
                   f"This appears in the Retained Income Note as part of Dividends on Ordinary Shares and in the Balance Sheet under Trade and Other Payables (Shareholders for Dividends).")
        add_q("easy", "Retained Income Note", q_fin, c_fin, w_fin, "Applying", f"Calculate final dividend for {co_name}", exp_fin)

        # 5. Total Annual Dividends (Interim + Final)
        tot_div = tot_int + tot_fin
        c_div = f"R{tot_div:,.2f}"
        w_div = [
            f"R{tot_int:,.2f} (included only interim dividend)",
            f"R{tot_fin:,.2f} (included only final dividend)",
            f"R{tot_div * 1.2:,.2f}",
            f"R{tot_div * 0.8:,.2f}",
            f"R{auth_s * (int_d + fin_d):,.2f} (calculated on authorized shares)",
            f"R{tot_div * 0.80:,.2f} (deducted dividends withholding tax)",
            f"R{(tot_div + 250000):,.2f}"
        ]
        q_div = (f"For the financial year ended 28 February, **{co_name}** paid an interim dividend of **R{int_d:.2f}** per share and declared a final "
                 f"dividend of **R{fin_d:.2f}** per share on **{iss_s:,.0f}** issued ordinary shares. Calculate the **total dividends on ordinary shares** for the Retained Income Note:")
        exp_div = (f"Total Dividends on Ordinary Shares = Interim Dividends (R{tot_int:,.2f}) + Final Dividends (R{tot_fin:,.2f}) = {c_div}. "
                   f"Both interim and final dividends declared for the year are deducted in the Retained Income Note.")
        add_q("easy", "Retained Income Note", q_div, c_div, w_div, "Applying", f"Calculate total dividends for {co_name}", exp_div)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # =========================================================================

    company_scenarios = [
        ("Laysano Ltd", 800000, 6.00, 200000, 7.50, 50000, 8.20, 1450000.0, 0.35, 0.55),
        ("Kavango Mining Ltd", 1200000, 10.00, 300000, 12.50, 80000, 14.00, 2800000.0, 0.50, 0.80),
        ("Protea Chem Ltd", 600000, 8.50, 150000, 10.00, 40000, 11.20, 1100000.0, 0.40, 0.65),
        ("Soweto Retail Holdings Ltd", 1500000, 5.00, 500000, 6.20, 100000, 7.00, 1950000.0, 0.25, 0.45),
        ("Blyde Valley Timber Ltd", 500000, 7.20, 100000, 9.00, 30000, 9.80, 820000.0, 0.30, 0.50),
        ("Drakensberg Energy Ltd", 2000000, 15.00, 400000, 18.00, 120000, 20.00, 5400000.0, 0.75, 1.15),
        ("Algoa Auto Spares Ltd", 900000, 9.00, 250000, 11.00, 60000, 12.50, 1680000.0, 0.45, 0.70),
        ("Zululand Agro Ltd", 750000, 4.80, 200000, 6.00, 45000, 6.80, 920000.0, 0.22, 0.38),
        ("Cape Floral Extracts Ltd", 400000, 12.00, 100000, 14.50, 25000, 16.00, 1050000.0, 0.60, 0.95),
        ("Highveld Brick & Tile Ltd", 1100000, 6.50, 300000, 8.00, 70000, 9.10, 1580000.0, 0.32, 0.52),
        ("Namaqua Diamonds Ltd", 1800000, 20.00, 450000, 24.00, 90000, 26.50, 6200000.0, 0.90, 1.45),
        ("Ezulwini Safari Lodges Ltd", 650000, 11.50, 150000, 13.50, 35000, 15.00, 1320000.0, 0.55, 0.85),
        ("Vaal Triangle Plastics Ltd", 850000, 7.80, 200000, 9.50, 55000, 10.60, 1400000.0, 0.38, 0.62),
        ("Limpopo Valley Citrus Ltd", 1300000, 5.50, 350000, 7.00, 75000, 7.90, 1750000.0, 0.28, 0.46),
        ("Tshwane Telecoms Ltd", 2500000, 14.00, 500000, 16.80, 150000, 18.50, 5900000.0, 0.70, 1.10),
        ("Outeniqua Paper Mills Ltd", 700000, 8.00, 180000, 9.80, 42000, 10.90, 1220000.0, 0.40, 0.60),
        ("Richards Bay Coal Ltd", 1600000, 16.50, 400000, 19.50, 85000, 22.00, 4800000.0, 0.80, 1.25),
        ("Karoo Renewable Power Ltd", 1000000, 13.00, 250000, 15.20, 50000, 17.00, 2400000.0, 0.65, 1.00),
        ("Stellenbosch Cellars Ltd", 550000, 18.00, 120000, 21.00, 28000, 23.50, 1780000.0, 0.85, 1.35),
        ("Polokwane Milling Ltd", 950000, 6.20, 220000, 7.60, 60000, 8.50, 1350000.0, 0.30, 0.48),
        ("Durban Container Logistics Ltd", 2200000, 11.00, 450000, 13.20, 110000, 14.80, 4200000.0, 0.55, 0.88),
        ("Rustenburg Smelters Ltd", 1750000, 22.00, 350000, 26.00, 80000, 29.00, 6800000.0, 1.05, 1.65),
        ("Witbank Foundry Ltd", 820000, 9.40, 180000, 11.20, 45000, 12.40, 1520000.0, 0.44, 0.70),
        ("Paarl Packaging Ltd", 620000, 7.50, 140000, 9.00, 32000, 10.20, 1040000.0, 0.36, 0.58),
        ("Midrand Software Systems Ltd", 1400000, 25.00, 300000, 30.00, 70000, 33.00, 5600000.0, 1.15, 1.85),
        ("Springbok Agri Holdings Ltd", 1050000, 8.20, 250000, 10.00, 52000, 11.40, 1620000.0, 0.42, 0.66),
        ("Kimberley Diamond Tools Ltd", 880000, 15.50, 200000, 18.50, 44000, 20.50, 2350000.0, 0.72, 1.12),
        ("Bloemfontein Cold Storage Ltd", 720000, 6.80, 160000, 8.40, 38000, 9.50, 1180000.0, 0.34, 0.54),
        ("Mbombela Fruit Packers Ltd", 1150000, 5.80, 280000, 7.20, 65000, 8.10, 1540000.0, 0.28, 0.48),
        ("Port Elizabeth Assembly Ltd", 1950000, 12.50, 400000, 15.00, 95000, 16.80, 3950000.0, 0.62, 0.98),
        ("Secunda Synthetic Fuels Ltd", 2800000, 17.00, 550000, 20.50, 130000, 23.00, 7500000.0, 0.85, 1.35),
        ("Makhanda Educational Media Ltd", 480000, 9.50, 120000, 11.50, 26000, 13.00, 960000.0, 0.46, 0.74),
        ("Cradock Livestock Trading Ltd", 680000, 8.40, 150000, 10.20, 36000, 11.50, 1140000.0, 0.40, 0.64),
        ("Vanderbijlpark Engineering Ltd", 1650000, 13.50, 350000, 16.00, 85000, 18.00, 3700000.0, 0.68, 1.05),
        ("Bredasdorp Wheat Mills Ltd", 920000, 7.00, 200000, 8.60, 50000, 9.70, 1380000.0, 0.35, 0.56),
        ("Upington Solar Grid Ltd", 1250000, 14.50, 280000, 17.20, 65000, 19.00, 2900000.0, 0.60, 0.92),
        ("Ladysmith Cotton Mills Ltd", 780000, 6.40, 170000, 7.80, 40000, 8.90, 1120000.0, 0.30, 0.46),
        ("Vryheid Coking Coal Ltd", 1350000, 11.80, 320000, 14.00, 75000, 15.60, 2600000.0, 0.52, 0.82),
        ("Newcastle Heavy Steels Ltd", 2100000, 15.80, 420000, 18.50, 105000, 20.80, 4600000.0, 0.78, 1.20),
        ("Bethlehem Grain Elevator Ltd", 840000, 8.20, 190000, 10.00, 48000, 11.20, 1340000.0, 0.38, 0.60),
        ("Potchefstroom Feeds Ltd", 1020000, 7.40, 240000, 9.00, 55000, 10.20, 1460000.0, 0.34, 0.55),
        ("Mossel Bay Offshore Ltd", 2400000, 19.00, 480000, 22.50, 115000, 25.00, 5800000.0, 0.92, 1.45),
        ("East London Harbour Services Ltd", 1180000, 10.40, 260000, 12.60, 62000, 14.00, 2150000.0, 0.48, 0.76),
        ("Klerksdorp Goldfields Ltd", 2900000, 13.20, 580000, 15.80, 140000, 17.50, 5100000.0, 0.65, 1.05),
        ("George Fine Timber Ltd", 640000, 9.80, 150000, 12.00, 35000, 13.50, 1160000.0, 0.44, 0.70),
        ("Welkom Mining Supplies Ltd", 1480000, 11.20, 330000, 13.40, 78000, 15.00, 2750000.0, 0.54, 0.84),
        ("Knysna Luxury Boats Ltd", 520000, 21.00, 110000, 25.00, 26000, 28.00, 1650000.0, 0.95, 1.50),
        ("Standerton Agri Holdings Ltd", 860000, 8.60, 190000, 10.50, 46000, 11.80, 1380000.0, 0.38, 0.62),
        ("Kuruman Iron Ore Ltd", 3100000, 16.00, 620000, 19.00, 150000, 21.50, 6400000.0, 0.82, 1.30),
        ("Saldanha Deepwater Terminal Ltd", 2650000, 18.20, 520000, 21.50, 125000, 24.00, 6100000.0, 0.88, 1.40)
    ]

    for co, beg_s, beg_p, new_s, new_p, buy_s, buy_p, npat, int_d, fin_d in company_scenarios:
        beg_val = beg_s * beg_p
        new_val = new_s * new_p
        tot_s_before_buy = beg_s + new_s
        tot_val_before_buy = beg_val + new_val
        avg_price = tot_val_before_buy / tot_s_before_buy

        buy_sc_deduct = buy_s * avg_price
        buy_ri_deduct = buy_s * (buy_p - avg_price)
        end_s = tot_s_before_buy - buy_s
        end_sc = end_s * avg_price

        tot_int_div = tot_s_before_buy * int_d
        tot_fin_div = end_s * fin_d
        tot_div = tot_int_div + tot_fin_div

        # 1. Medium Q: Weighted Average Issue Price per Share
        if counts["medium"] < 500:
            c_avg = f"R{avg_price:.2f}"
            w_avg = [
                f"R{beg_p:.2f} (used opening price only)",
                f"R{new_p:.2f} (used new issue price only)",
                f"R{(beg_p + new_p) / 2:.2f} (simple average without weighting by shares)",
                f"R{buy_p:.2f} (used repurchase price)",
                f"R{avg_price * 1.15:.2f}",
                f"R{avg_price * 0.85:.2f}",
                f"R{(avg_price + 1.20):.2f}"
            ]
            q_avg = (f"The Ordinary Share Capital records of **{co}** reveal the following:\n"
                     f"- Balance at beginning of financial year: **{beg_s:,.0f}** ordinary shares valued at **R{beg_val:,.0f}** (R{beg_p:.2f} each)\n"
                     f"- Shares issued during the year: **{new_s:,.0f}** ordinary shares at **R{new_p:.2f}** each\n"
                     f"Calculate the **weighted average issue price per share** prior to any share repurchase:")
            exp_avg = (f"Weighted Average Price = (Opening Value + New Issue Value) / (Opening Shares + New Shares)\n"
                       f"= (R{beg_val:,.0f} + R{new_val:,.0f}) / ({beg_s:,.0f} + {new_s:,.0f})\n"
                       f"= R{tot_val_before_buy:,.0f} / {tot_s_before_buy:,.0f} = {c_avg} per share.")
            add_q("medium", "Ordinary Share Capital Note", q_avg, c_avg, w_avg, "Applying", f"Calculate weighted average share price for {co}", exp_avg)

        # 2. Medium Q: Amount Debited to Ordinary Share Capital for Share Buyback
        if counts["medium"] < 500:
            c_sc_buy = f"R{buy_sc_deduct:,.2f}"
            w_sc_buy = [
                f"R{buy_s * buy_p:,.2f} (debited entire repurchase price to share capital)",
                f"R{buy_ri_deduct:,.2f} (confused with amount debited to retained income)",
                f"R{buy_s * beg_p:,.2f} (used opening price instead of weighted average)",
                f"R{buy_s * new_p:,.2f} (used new issue price instead of weighted average)",
                f"R{buy_sc_deduct * 1.2:,.2f}",
                f"R{buy_sc_deduct * 0.8:,.2f}",
                f"R{(buy_sc_deduct + 50000):,.2f}"
            ]
            q_sc_buy = (f"**{co}** repurchased **{buy_s:,.0f}** ordinary shares from an existing shareholder at **R{buy_p:.2f}** per share. "
                        f"The weighted average issue price of all shares in issue prior to the buyback was **R{avg_price:.2f}**. "
                        f"Calculate the amount by which **Ordinary Share Capital** will be reduced (debited) in Note 7:")
            exp_sc_buy = (f"Reduction in Share Capital = Shares Repurchased x Weighted Average Issue Price\n"
                          f"= {buy_s:,.0f} x R{avg_price:.2f} = {c_sc_buy}.\n"
                          f"Under CAPS and the Companies Act, the ordinary share capital account can only be reduced by the average issue price. Any excess paid is debited to Retained Income.")
            add_q("medium", "Ordinary Share Capital Note", q_sc_buy, c_sc_buy, w_sc_buy, "Applying", f"Calculate share capital buyback reduction for {co}", exp_sc_buy)

        # 3. Medium Q: Amount Debited to Retained Income for Share Buyback
        if counts["medium"] < 500:
            c_ri_buy = f"R{buy_ri_deduct:,.2f}"
            w_ri_buy = [
                f"R{buy_sc_deduct:,.2f} (confused with amount debited to share capital)",
                f"R{buy_s * buy_p:,.2f} (debited total repurchase consideration to retained income)",
                f"R{buy_s * (buy_p - beg_p):,.2f} (used opening price instead of weighted average price)",
                f"R{buy_ri_deduct * 1.25:,.2f}",
                f"R{buy_ri_deduct * 0.75:,.2f}",
                f"R{(buy_ri_deduct + 30000):,.2f}",
                f"R{(buy_ri_deduct - 20000):,.2f}"
            ]
            q_ri_buy = (f"**{co}** bought back **{buy_s:,.0f}** ordinary shares at **R{buy_p:.2f}** each. "
                        f"The weighted average issue price on the date of repurchase was **R{avg_price:.2f}**. "
                        f"Calculate the amount debited to **Retained Income** (Note 8) in respect of this share repurchase:")
            exp_ri_buy = (f"Amount Debited to Retained Income = Shares Repurchased x (Repurchase Price - Weighted Average Issue Price)\n"
                          f"= {buy_s:,.0f} x (R{buy_p:.2f} - R{avg_price:.2f})\n"
                          f"= {buy_s:,.0f} x R{buy_p - avg_price:.2f} = {c_ri_buy}.\n"
                          f"This represents the premium paid over the average issue price, which reduces accumulated retained earnings.")
            add_q("medium", "Retained Income Note", q_ri_buy, c_ri_buy, w_ri_buy, "Applying", f"Calculate retained income buyback debit for {co}", exp_ri_buy)

        # 4. Medium Q: Final Year-End Balance of Ordinary Share Capital
        if counts["medium"] < 500:
            c_end_sc = f"R{end_sc:,.2f}"
            w_end_sc = [
                f"R{tot_val_before_buy - (buy_s * buy_p):,.2f} (deducted full buyback price from share capital)",
                f"R{tot_val_before_buy:,.2f} (omitted the share repurchase)",
                f"R{end_s * beg_p:,.2f} (valued closing shares at opening issue price)",
                f"R{end_sc * 1.1:,.2f}",
                f"R{end_sc * 0.9:,.2f}",
                f"R{(end_sc + 200000):,.2f}",
                f"R{(end_sc - 180000):,.2f}"
            ]
            q_end_sc = (f"**{co}** started the year with **{beg_s:,.0f}** shares valued at **R{beg_val:,.0f}**. "
                        f"They issued **{new_s:,.0f}** shares for **R{new_val:,.0f}** and subsequently repurchased **{buy_s:,.0f}** shares at **R{buy_p:.2f}** per share. "
                        f"Calculate the closing balance of **Ordinary Share Capital** to be shown in the Balance Sheet at year-end:")
            exp_end_sc = (f"Closing Share Capital Balance = Remaining Shares x Weighted Average Price\n"
                          f"= ({tot_s_before_buy:,.0f} - {buy_s:,.0f}) x R{avg_price:.2f}\n"
                          f"= {end_s:,.0f} shares x R{avg_price:.2f} = {c_end_sc}.")
            add_q("medium", "Ordinary Share Capital Note", q_end_sc, c_end_sc, w_end_sc, "Applying", f"Calculate closing share capital for {co}", exp_end_sc)

        # 5. Medium Q: Total Dividends Recommended and Paid
        if counts["medium"] < 500:
            c_tot_div = f"R{tot_div:,.2f}"
            w_tot_div = [
                f"R{tot_int_div:,.2f} (omitted final recommended dividend)",
                f"R{tot_fin_div:,.2f} (omitted interim dividend)",
                f"R{end_s * (int_d + fin_d):,.2f} (calculated interim dividend on closing shares after buyback)",
                f"R{tot_s_before_buy * (int_d + fin_d):,.2f} (calculated final dividend on shares before buyback)",
                f"R{tot_div * 1.2:,.2f}",
                f"R{tot_div * 0.8:,.2f}",
                f"R{(tot_div + 120000):,.2f}"
            ]
            q_tot_div = (f"During the year, **{co}** paid an interim dividend of **{int_d * 100:.0f} cents** per share on **{tot_s_before_buy:,.0f}** issued shares. "
                         f"Later, **{buy_s:,.0f}** shares were repurchased. At year-end, a final dividend of **{fin_d * 100:.0f} cents** per share was declared on the remaining **{end_s:,.0f}** shares. "
                         f"Calculate the **Total Dividends on Ordinary Shares** for the Retained Income Note:")
            exp_tot_div = (f"Interim Dividend Paid = {tot_s_before_buy:,.0f} x R{int_d:.2f} = R{tot_int_div:,.2f}\n"
                           f"Final Dividend Declared = {end_s:,.0f} x R{fin_d:.2f} = R{tot_fin_div:,.2f}\n"
                           f"Total Dividends = R{tot_int_div:,.2f} + R{tot_fin_div:,.2f} = {c_tot_div}.")
            add_q("medium", "Retained Income Note", q_tot_div, c_tot_div, w_tot_div, "Applying", f"Calculate total dividends for {co}", exp_tot_div)

        # 6. Medium Q: Retained Income Balance at Year-End
        beg_ri = 450000.0 + (beg_s * 0.5)
        end_ri = beg_ri + npat - buy_ri_deduct - tot_div
        if counts["medium"] < 500:
            c_end_ri = f"R{end_ri:,.2f}"
            w_end_ri = [
                f"R{beg_ri + npat - tot_div:,.2f} (omitted share buyback deduction from retained income)",
                f"R{beg_ri + npat - (buy_s * buy_p) - tot_div:,.2f} (deducted full buyback price instead of premium)",
                f"R{end_ri + tot_fin_div:,.2f} (omitted final dividend deduction)",
                f"R{end_ri * 1.15:,.2f}",
                f"R{end_ri * 0.85:,.2f}",
                f"R{(end_ri + 150000):,.2f}",
                f"R{(end_ri - 120000):,.2f}"
            ]
            q_end_ri = (f"The following details relate to **{co}** for the financial year:\n"
                        f"- Retained Income balance at beginning: **R{beg_ri:,.2f}**\n"
                        f"- Net Profit after Tax: **R{npat:,.2f}**\n"
                        f"- Share buyback premium debited to retained income: **R{buy_ri_deduct:,.2f}**\n"
                        f"- Total dividends on ordinary shares (interim R{tot_int_div:,.2f} + final R{tot_fin_div:,.2f}): **R{tot_div:,.2f}**\n"
                        f"Calculate the **Retained Income balance** at the end of the financial year:")
            exp_end_ri = (f"Retained Income at End = Opening Balance + Net Profit after Tax - Buyback Premium - Total Dividends\n"
                          f"= R{beg_ri:,.2f} + R{npat:,.2f} - R{buy_ri_deduct:,.2f} - R{tot_div:,.2f}\n"
                          f"= {c_end_ri}.")
            add_q("medium", "Retained Income Note", q_end_ri, c_end_ri, w_end_ri, "Applying", f"Calculate closing retained income for {co}", exp_end_ri)

        # 7. Medium Q: Closing Share Count
        if counts["medium"] < 500:
            c_end_s = f"{end_s:,.0f} shares"
            w_end_s = [
                f"{tot_s_before_buy:,.0f} shares (forgot to deduct repurchased shares)",
                f"{beg_s:,.0f} shares (used beginning shares only)",
                f"{beg_s - buy_s:,.0f} shares (deducted buyback from opening shares without adding new issue)",
                f"{tot_s_before_buy + buy_s:,.0f} shares (added repurchased shares)",
                f"{end_s + 50000:,.0f} shares",
                f"{end_s - 50000:,.0f} shares",
                f"{end_s * 1.1:,.0f} shares"
            ]
            q_end_s = (f"At the start of the year, **{co}** had **{beg_s:,.0f}** shares. During the year, they issued **{new_s:,.0f}** new shares "
                       f"and later bought back **{buy_s:,.0f}** shares. How many ordinary shares are in issue at the **end of the financial year**?")
            exp_end_s = (f"Closing Issued Shares = Opening Shares + New Shares Issued - Shares Repurchased\n"
                         f"= {beg_s:,.0f} + {new_s:,.0f} - {buy_s:,.0f} = {c_end_s}.")
            add_q("medium", "Ordinary Share Capital Note", q_end_s, c_end_s, w_end_s, "Applying", f"Calculate closing share count for {co}", exp_end_s)

        # 8. Medium Q: Audit Opinion Identification
        audit_types = [
            ("The external auditors of **" + co + "** discovered that inventory was overstated by R3.5 million. The directors refused to adjust the books. The misstatement is material but restricted only to inventory and cost of sales, not affecting the rest of the accounts pervasively.",
             "Qualified audit opinion",
             ["Unqualified audit opinion ('clean report')", "Adverse audit opinion", "Disclaimer of audit opinion", "Notice of immediate commercial liquidation", "SARS provisional tax compliance certificate", "Internal audit management inquiry"]),

            ("The external auditors of **" + co + "** completed all audit testing and confirmed that the financial statements fairly present, in all material respects, the financial position and performance in compliance with IFRS.",
             "Unqualified audit opinion ('clean report')",
             ["Qualified audit opinion", "Adverse audit opinion", "Disclaimer of audit opinion", "Forensic criminal investigation", "JSE immediate delisting notice", "Creditors reconciliation variance report"]),

            ("A major fire destroyed **" + co + "**'s head office, obliterating 80% of accounting documentation, general ledgers, and backup servers. The auditors were unable to obtain sufficient appropriate audit evidence.",
             "Disclaimer of audit opinion",
             ["Unqualified audit opinion ('clean report')", "Qualified audit opinion", "Adverse audit opinion", "Voluntary shareholder distribution certificate", "B-BBEE level 1 compliance rating", "King IV corporate governance excellence award"]),

            ("The directors of **" + co + "** deliberately omitted R45 million in bank loans and fabricated R30 million in fictitious sales. The financial statements are overwhelmingly, pervasively misleading.",
             "Adverse audit opinion",
             ["Unqualified audit opinion ('clean report')", "Qualified audit opinion", "Disclaimer of audit opinion", "Interim distribution approval notice", "Provisional tax assessment clearance", "Companies and Intellectual Property Commission (CIPC) routine certificate"])
        ]

        for desc, corr_aud, wrongs_aud in audit_types:
            if counts["medium"] < 500:
                q_aud = f"Read the audit finding below for **{co}** and identify the correct audit opinion:\n\n*\"{desc}\"*"
                exp_aud = f"Correct Opinion: **{corr_aud}**. Under SAICA and DBE CAPS guidelines, {desc.split('.')[1].strip()}."
                add_q("medium", "Audit Reports & Corporate Governance", q_aud, corr_aud, wrongs_aud, "Analyzing", f"Identify audit opinion for {co}", exp_aud)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Advanced Shareholding shifts, NAV vs Buyback, King IV Governance
    # =========================================================================

    control_cases = [
        ("Protea Holdings Ltd", "Mahlangu", 450000, 1000000, 100000, 12.50, 15.00),
        ("Kavango Resources Ltd", "Naidoo", 580000, 1200000, 150000, 18.00, 22.00),
        ("Ubuntu Commercial Ltd", "Van der Merwe", 480000, 1000000, 120000, 8.00, 10.50),
        ("Highveld Tech Ltd", "Sithole", 720000, 1500000, 200000, 25.00, 30.00),
        ("Cape Horizon Ltd", "Pillay", 390000, 800000, 100000, 14.00, 17.50),
        ("Limpopo Platinum Ltd", "Baloyi", 950000, 2000000, 250000, 20.00, 24.50),
        ("Drakensberg Dairy Ltd", "Du Plessis", 460000, 950000, 110000, 7.50, 9.20),
        ("Zululand Sugar Ltd", "Dlamini", 850000, 1800000, 220000, 11.00, 13.80),
        ("Algoa Marine Ltd", "Williams", 520000, 1100000, 140000, 16.00, 19.50),
        ("Karoo Power Ltd", "Botha", 630000, 1300000, 160000, 22.00, 27.00),
        ("Tshwane Media Ltd", "Molefe", 420000, 900000, 110000, 13.50, 16.00),
        ("Ezulwini Hotels Ltd", "Khumalo", 380000, 800000, 95000, 15.00, 18.50),
        ("Namaqua Gold Ltd", "Coetzee", 760000, 1600000, 200000, 28.00, 34.00),
        ("Outeniqua Timber Ltd", "Meyer", 490000, 1050000, 130000, 9.50, 12.00),
        ("Richards Bay Logistics Ltd", "Govender", 880000, 1850000, 230000, 19.00, 23.50),
        ("Free State Grain Ltd", "Nel", 540000, 1150000, 145000, 8.80, 11.20),
        ("Midrand Systems Ltd", "Chauke", 680000, 1400000, 175000, 32.00, 38.00),
        ("Stellenbosch Agri Ltd", "De Villiers", 410000, 850000, 105000, 17.00, 21.00),
        ("Polokwane Freight Ltd", "Mabaso", 470000, 1000000, 125000, 10.50, 13.00),
        ("Soweto Retail Hub Ltd", "Ndlovu", 590000, 1250000, 155000, 6.50, 8.20),
        ("Kimberley Mining Ltd", "Jacobs", 510000, 1080000, 135000, 21.00, 25.50),
        ("Durban Port Terminal Ltd", "Moodley", 920000, 1900000, 240000, 18.50, 23.00),
        ("Rustenburg Chrome Ltd", "Mokoena", 840000, 1750000, 215000, 26.00, 31.50),
        ("Vaal Eng Works Ltd", "Fourie", 610000, 1280000, 160000, 14.50, 17.80),
        ("Mbombela Citrus Ltd", "Mathebula", 530000, 1120000, 140000, 7.80, 9.80),
        ("Centurion Tech Ltd", "Mthembu", 475000, 1020000, 120000, 24.00, 29.00),
        ("Bloemfontein Milling Ltd", "Steyn", 360000, 780000, 90000, 11.50, 14.00),
        ("Paarl Agrochem Ltd", "Louw", 425000, 920000, 115000, 16.00, 19.50),
        ("East London Automotive Ltd", "Jansen", 670000, 1450000, 180000, 13.00, 16.20),
        ("Klerksdorp Ore Ltd", "Venter", 515000, 1100000, 135000, 20.00, 24.00),
        ("Potchefstroom Grain Trading Ltd", "Swanepoel", 395000, 850000, 105000, 9.20, 11.50),
        ("George Coastal Timber Ltd", "Ferreira", 440000, 950000, 120000, 12.00, 15.00),
        ("Secunda Fuel Processing Ltd", "Maseko", 890000, 1920000, 240000, 27.00, 32.50),
        ("Vereeniging Castings Ltd", "Pretorius", 580000, 1250000, 150000, 15.50, 18.80),
        ("Welkom Shaft Supplies Ltd", "Kruger", 460000, 980000, 125000, 14.00, 17.00),
        ("Bethlehem Roller Mills Ltd", "Oosthuizen", 350000, 750000, 95000, 10.00, 12.20),
        ("Newcastle Heavy Steels Ltd", "Radebe", 740000, 1600000, 200000, 18.00, 22.00),
        ("Mossel Bay Deepsea Ltd", "Pienaar", 810000, 1750000, 220000, 21.00, 25.50),
        ("Mthatha General Trading Ltd", "Mnguni", 330000, 720000, 90000, 8.50, 10.40),
        ("Upington Sun Agro Ltd", "Bester", 410000, 880000, 110000, 13.20, 16.00),
        ("Vryheid Coal Supply Ltd", "Sibiya", 620000, 1340000, 165000, 16.80, 20.50),
        ("Ladysmith Textile Mills Ltd", "Cele", 370000, 800000, 100000, 9.80, 12.00),
        ("Bredasdorp Wheatlands Ltd", "Lombard", 430000, 930000, 115000, 11.00, 13.50),
        ("Cradock Merinos Ltd", "Erasmus", 340000, 740000, 92000, 12.50, 15.20),
        ("Makhanda Print Corp Ltd", "Zuma", 310000, 670000, 85000, 14.20, 17.50),
        ("Oudtshoorn Ostrich Ltd", "Nortje", 450000, 970000, 120000, 15.00, 18.20),
        ("Knysna Marine Craft Ltd", "Potgieter", 380000, 820000, 105000, 23.00, 28.00),
        ("Standerton Dairy Co Ltd", "Van Zyl", 490000, 1060000, 130000, 10.20, 12.60),
        ("Harrismith Transit Ltd", "Makhanya", 560000, 1210000, 150000, 13.80, 16.80),
        ("Kuruman Iron Mining Ltd", "Snyman", 790000, 1700000, 210000, 22.50, 27.50),
        ("Thohoyandou Stores Ltd", "Netshitenzhe", 320000, 700000, 88000, 8.00, 10.00),
        ("Plettenberg Bay Estates Ltd", "Basson", 400000, 860000, 110000, 19.50, 24.00),
        ("Saldanha Bulk Shipments Ltd", "Myburgh", 870000, 1880000, 235000, 20.50, 25.00),
        ("Grahamstown Media Ltd", "Gxilishe", 360000, 770000, 96000, 12.80, 15.50),
        ("Springbok Renewables Ltd", "Agenbag", 650000, 1400000, 175000, 17.20, 21.00),
        ("Witbank Petrochemicals Ltd", "Mabuza", 730000, 1580000, 195000, 18.50, 22.80),
        ("Paarl Valley Vineyards Ltd", "Theron", 480000, 1040000, 130000, 25.00, 31.00),
        ("Durban Container Ports Ltd", "Chetty", 910000, 1960000, 245000, 16.50, 20.20),
        ("Rustenburg PGM Metals Ltd", "Lekota", 820000, 1780000, 225000, 29.00, 35.50),
        ("Cape West Coast Fisheries Ltd", "Stander", 540000, 1170000, 145000, 11.20, 13.80),
        ("Highveld Industrial Park Ltd", "Tshabalala", 690000, 1490000, 185000, 14.80, 18.00),
        ("Zululand Forestry Co Ltd", "Zulu", 710000, 1530000, 190000, 13.50, 16.50),
        ("Algoa Commercial Wharves Ltd", "Daniels", 600000, 1300000, 160000, 17.50, 21.50),
        ("Karoo Sun Power Ltd", "Viviers", 570000, 1230000, 155000, 24.50, 29.80),
        ("Tshwane City Logistics Ltd", "Kekana", 640000, 1380000, 170000, 15.00, 18.40)
    ]

    for co_c, founder, founder_shares, orig_total, buy_shares, mkt_p, buy_p in control_cases:
        orig_pct = (founder_shares / orig_total) * 100
        new_total = orig_total - buy_shares
        new_pct = (founder_shares / new_total) * 100
        pct_change = new_pct - orig_pct

        # 1. Hard Q: Calculate Change in Percentage Shareholding
        if counts["hard"] < 200:
            c_pct = f"Increased by {pct_change:.2f}% (from {orig_pct:.2f}% to {new_pct:.2f}%)"
            w_pct = [
                f"Decreased by {pct_change:.2f}% (from {new_pct:.2f}% to {orig_pct:.2f}%)",
                f"Remained unchanged at {orig_pct:.2f}% because {founder} bought no shares",
                f"Increased by {(buy_shares / orig_total) * 100:.2f}%",
                f"Increased by {pct_change * 1.5:.2f}%",
                f"Increased by {pct_change * 0.5:.2f}%",
                f"Decreased by {(buy_shares / new_total) * 100:.2f}%",
                f"Increased by 10.00% exactly"
            ]
            q_pct = (f"In **{co_c}**, director **{founder}** owned **{founder_shares:,.0f}** shares out of **{orig_total:,.0f}** total issued shares. "
                     f"The company repurchased **{buy_shares:,.0f}** shares from other discontented shareholders and cancelled them. "
                     f"{founder} did not participate in the repurchase. Calculate the change in **{founder}'s percentage shareholding**:")
            exp_pct = (f"Original Shareholding % = ({founder_shares:,.0f} / {orig_total:,.0f}) x 100 = {orig_pct:.2f}%\n"
                       f"New Total Shares = {orig_total:,.0f} - {buy_shares:,.0f} = {new_total:,.0f} shares\n"
                       f"New Shareholding % = ({founder_shares:,.0f} / {new_total:,.0f}) x 100 = {new_pct:.2f}%\n"
                       f"Net Change = {new_pct:.2f}% - {orig_pct:.2f}% = {c_pct}. "
                       f"Notice: Without investing a single cent of personal money, {founder}'s voting power increased significantly!")
            add_q("hard", "Share Repurchase & Corporate Control", q_pct, c_pct, w_pct, "Evaluating", f"Evaluate change in shareholding for {founder} in {co_c}", exp_pct)

        # 2. Hard Q: Ethical Evaluation under King IV
        if counts["hard"] < 200:
            c_eth = (f"Unethical conflict of interest: {founder} used company cash resources to buy back shares at an inflated price (R{buy_p:.2f} vs market R{mkt_p:.2f}), "
                     f"effectively consolidating personal voting power ({new_pct:.2f}%) at the expense of company liquidity")
            w_eth = [
                f"Completely ethical and commendable: {founder} sacrificed personal wealth to assist other shareholders",
                f"Neutral: Share buybacks have zero impact on voting control or corporate liquidity under King IV",
                f"Illegal under Companies Act: Companies are strictly prohibited from repurchasing shares under any circumstances",
                f"Ethical because all commercial banks require directors to hold over 50% equity before approving overdrafts",
                f"Unethical solely because dividends tax of 20% was not remitted to the Johannesburg Stock Exchange",
                f"Ethical because the Companies Act mandates that founding directors must always gain absolute voting control"
            ]
            q_eth = (f"Referring to **{co_c}**: The company paid **R{buy_p:.2f}** per share for the buyback when the prevailing market price was only **R{mkt_p:.2f}**. "
                     f"As a result, director {founder}'s stake grew from **{orig_pct:.2f}%** to **{new_pct:.2f}%**. "
                     f"Provide the most accurate professional evaluation of this transaction under the **King IV Code of Corporate Governance**:")
            exp_eth = (f"Evaluation: {c_eth}. "
                       f"Under King IV and Section 75/76 of the Companies Act, directors have a fiduciary duty not to abuse corporate funds for personal control or pay prices well above fair value without independent valuation.")
            add_q("hard", "Share Repurchase & Corporate Control", q_eth, c_eth, w_eth, "Evaluating", f"Evaluate ethics of share buyback in {co_c}", exp_eth)

        # 3. Hard Q: NAV per share vs Buyback Price
        tot_eq = new_total * (buy_p * 0.85)
        nav_per_share = tot_eq / new_total
        if counts["hard"] < 200:
            c_nav = f"NAV per share is R{nav_per_share:.2f}. Paying R{buy_p:.2f} per share diluted the net wealth of remaining shareholders because the repurchase price exceeded NAV by R{buy_p - nav_per_share:.2f} per share"
            w_nav = [
                f"NAV per share is R{nav_per_share:.2f}. The repurchase increased shareholder wealth because NAV was higher than buyback price",
                f"NAV per share is R{tot_eq / orig_total:.2f}. The buyback had no effect on net asset value per share",
                f"NAV per share cannot be calculated without knowing the company's gross profit margin percentage",
                f"NAV per share is R{buy_p:.2f}. The repurchase was conducted at exact book parity with net assets",
                f"NAV per share is R{nav_per_share * 1.5:.2f}. The company made a capital profit on the repurchase",
                f"NAV per share is R{nav_per_share * 0.5:.2f}. The repurchase violated Section 46 solvency requirements automatically"
            ]
            q_nav = (f"Following the share repurchase, the total Ordinary Shareholders' Equity of **{co_c}** stands at **R{tot_eq:,.2f}** "
                     f"across **{new_total:,.0f}** remaining shares. The buyback price was **R{buy_p:.2f}** per share. "
                     f"Evaluate the **financial wisdom** of the buyback price in relation to the company's **Net Asset Value (NAV) per share**:")
            exp_nav = (f"NAV per share = Total Equity / Number of Shares in Issue = R{tot_eq:,.2f} / {new_total:,.0f} = R{nav_per_share:.2f}.\n"
                       f"Since the repurchase price of R{buy_p:.2f} exceeded NAV (R{nav_per_share:.2f}), the remaining shareholders suffered a dilution in net asset backing per share.")
            add_q("hard", "Financial Evaluation & NAV", q_nav, c_nav, w_nav, "Evaluating", f"Evaluate NAV vs buyback price for {co_c}", exp_nav)

    # King IV Ethical Case Studies
    king_iv_cases = [
        ("Conflict of Interest & Tenders",
         "The Chief Executive Officer of a listed company awarded a multi-million rand security and logistics contract to an enterprise owned by his spouse without competitive bidding or declaring his interest to the Board.",
         "Violation of Section 75 of Companies Act and King IV: The CEO failed to disclose a material personal financial interest, did not recuse himself from deliberations, and compromised competitive procurement and board integrity.",
         "Permissible provided the spouse offered a 5% discount below standard industry rates",
         "Fully compliant with King IV because executive directors have unilateral authority to select preferred family vendors",
         "A minor administrative oversight that only requires an informal email to the company secretary",
         "Permissible if the spouse donates 10% of contract profits to the company's employee social fund",
         "A matter falling strictly under the jurisdiction of the Department of Labour rather than corporate governance",
         "Acceptable corporate practice as long as the internal audit manager is a personal friend of the CEO"),

        ("Whistleblower Protection & Fraud",
         "An internal cost accountant noticed that factory overhead invoices for R8.4 million were paid to a fictitious shell corporation linked to the Financial Director. After reporting this to the Audit Committee, the accountant was demoted and threatened with dismissal.",
         "Severe breach of Protected Disclosures Act and King IV: The company failed to provide an effective, confidential whistleblowing hotline and unlawfully victimized an employee acting in good faith to protect company assets.",
         "Proper management action because internal accountants owe absolute secrecy and obedience to executive directors",
         "Lawful under the Companies Act because reporting financial irregularities damages corporate reputation and share price",
         "Permissible provided the Financial Director replaces the misappropriated funds prior to the external audit visit",
         "A labour issue that should be resolved by transferring the accountant to an outdoor landscaping department",
         "Fully compliant because King IV does not apply to transactions involving amounts below R10 million",
         "Acceptable practice because internal audit committees have no legal duty to investigate anonymous complaints"),

        ("Director Remuneration vs Worker Wage Gap",
         "During a financial year where the company retrenched 400 factory workers due to declining operating profits, the Board of Directors awarded themselves performance bonuses of R15 million each, which shareholders voted against at the AGM.",
         "Breach of King IV Principle 14: Remuneration should be fair, responsible, and transparent, promoting the achievement of strategic objectives in the medium and long term without rewarding failure amid worker retrenchments.",
         "Exemplary corporate leadership because executive bonuses must always take precedence over factory operational costs",
         "A mandatory requirement under JSE Listings Rules to pay top-quartile executive bonuses regardless of profitability",
         "Acceptable because shareholder advisory votes on remuneration policy are purely decorative and can be completely disregarded",
         "Fully compliant because the Companies Act strictly forbids trade unions from questioning director remuneration packages",
         "A routine human resource matter that does not require disclosure in the published Annual Financial Statements",
         "Lawful because executive directors are personally entitled to 20% of gross company revenue every year"),

        ("Environmental Responsibility & CSR",
         "A chemical manufacturing company secretly dumped untreated toxic industrial effluent into an adjacent river system to save R6 million in waste treatment costs, contaminating municipal water supplies.",
         "Gross violation of King IV (Ethical Corporate Citizenship) and National Environmental Management Act: The board failed in its social and environmental responsibility, exposing the firm to severe legal penalties and reputational devastation.",
         "Smart commercial cost-saving strategy that maximizes short-term dividend yields for institutional shareholders",
         "Permissible under South African law provided the chemical dumping is conducted late at night during rainy weather",
         "A legitimate manufacturing technique as long as factory production quotas were successfully achieved for the quarter",
         "Acceptable practice provided the company sponsors a local soccer tournament to compensate the local community",
         "An operational matter that falls strictly outside the mandate of the Board's Social and Ethics Committee",
         "Permissible if the savings of R6 million are distributed directly to executive directors as safety bonuses"),

        ("External Audit Quality & Rotation",
         "An external audit firm has served as the sole auditor of a listed commercial group for 28 consecutive years. The senior audit partner is the godfather of the client Chief Financial Officer's children and regularly joins family vacations.",
         "Compromise of Auditor Independence under IRBA Mandatory Audit Firm Rotation rules: Familiarity and personal relationships severely impair auditor objectivity and public trust in the credibility of the financial statements.",
         "Ideal audit continuity because three decades of personal friendship guarantees superior accounting accuracy",
         "Fully compliant with King IV because long-standing personal relationships eliminate the need for substantive audit testing",
         "Permissible provided the audit fee is discounted by at least 15% to compensate for the close friendship",
         "A standard practice actively encouraged by the Johannesburg Stock Exchange to minimize audit transition friction",
         "Acceptable because independence rules apply only to internal bookkeepers rather than registered external auditors",
         "Lawful because the Companies Act prohibits companies from ever changing their appointed external audit firm")
    ]

    for title_k, sc_k, corr_k, *wrongs_k in king_iv_cases:
        if counts["hard"] < 200:
            q_k = (f"**Corporate Governance Case Study — {title_k}**:\n\n"
                   f"Scenario: *\"{sc_k}\"*\n\n"
                   f"Evaluate this scenario in terms of the **King IV Report on Corporate Governance** and South African legislation:")
            exp_k = f"Evaluation: **{corr_k}**. Ethical governance, transparency, and accountability are non-negotiable standards tested extensively in Grade 12 Accounting Paper 1."
            add_q("hard", "Corporate Governance & Ethics", q_k, corr_k, wrongs_k, "Evaluating", f"Evaluate {title_k}", exp_k)

    print(f"Generated: easy={counts['easy']}, medium={counts['medium']}, hard={counts['hard']}")

    output_path = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting/paper1_acc_companies.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"SUCCESS: {output_path} created with {len(questions)} questions: {counts}")

if __name__ == "__main__":
    build_companies()
