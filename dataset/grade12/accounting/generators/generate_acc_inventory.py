import json
import os

def build_inventory():
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
        qid = f"ACC_P2_INV_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Inventory & Asset Control",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Inventory & Asset Control",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Perpetual vs Periodic, FIFO, Weighted Average, Specific Identification, Basic Turnover
    # =========================================================================

    easy_concepts = [
        ("Perpetual Inventory System",
         "An inventory system where stock balances and Cost of Sales are updated continuously at the time of each purchase and sale",
         "An inventory system where Cost of Sales is only calculated at the end of the financial year",
         "An accounting method that values all inventory at historical replacement cost",
         "A system that eliminates the need to perform annual physical stock counts",
         "A stockholding technique used exclusively for raw materials in manufacturing",
         "An inventory policy that forbids the purchase of goods on credit",
         "A system where trading stock is classified as a non-current asset"),

        ("Periodic Inventory System",
         "An inventory system where Cost of Sales is calculated at the end of the accounting period using the formula: Opening Stock + Purchases + Carriage - Closing Stock",
         "A system where Cost of Sales is recorded in the general ledger immediately upon each sale",
         "An inventory valuation method that assigns the most recent purchase prices to units sold",
         "A technique used only by high-end jewelry stores and motor vehicle dealerships",
         "A method where physical stock counts are conducted every hour during trading",
         "A system requiring automated computerized barcode scanners at checkout till points",
         "An accounting system that is prohibited under International Financial Reporting Standards"),

        ("First-In, First-Out (FIFO) Method",
         "A stock valuation method assuming that the oldest stock purchased is sold first, meaning closing inventory is valued at the most recent purchase prices",
         "A method that assumes the newest goods purchased are sold first, leaving oldest stock in closing inventory",
         "A valuation technique that calculates the arithmetic mean of all purchase invoice prices",
         "A method that tracks each specific item using an individual chassis or serial number",
         "A system that values all closing trading stock strictly at original wholesale cost minus 20%",
         "An inventory technique that is strictly illegal under the South African Companies Act",
         "A valuation rule that requires stock to be depreciated over a five-year economic life"),

        ("Weighted Average Cost Method",
         "A stock valuation method that calculates a single average cost per unit by dividing the total cost of available goods by the total number of available units",
         "A valuation method that weights inventory items according to their physical weight in kilograms",
         "A method that values all stock at the highest purchase price paid during the financial year",
         "A technique that values closing inventory at the opening stock unit cost regardless of price changes",
         "An inventory system where stock shrinkage is automatically added to gross sales revenue",
         "A method that assigns zero value to carriage on purchases of trading stock",
         "A valuation standard that requires ordinary shareholder approval at the AGM"),

        ("Specific Identification Method",
         "A stock valuation method that tracks and values each individual unique, high-value item at its actual purchase cost",
         "A method that averages the cost of thousands of identical small items like screws and bolts",
         "A valuation technique that assumes all units in the warehouse were purchased on the same date",
         "A system used exclusively for perishable dairy products and fresh vegetables",
         "An inventory method that values merchandise at the retail selling price minus sales commission",
         "A technique where goods are valued based on the personal discretion of the store manager",
         "An accounting method that ignores import customs duties and freight shipping charges"),

        ("Prohibition of LIFO under IFRS and CAPS",
         "The Last-In, First-Out (LIFO) method is prohibited under IFRS (IAS 2) and CAPS because it distorts inventory valuation on the balance sheet and misrepresents economic reality",
         "LIFO is permitted under CAPS provided the South African Revenue Service grants written exemption",
         "LIFO is mandatory for all listed companies trading on the Johannesburg Stock Exchange",
         "LIFO is prohibited only for companies that experience negative operating cash flows",
         "LIFO was banned because commercial banks refuse to accept it for loan applications",
         "LIFO is allowed under CAPS for manufacturing businesses but prohibited for retail traders",
         "LIFO is permissible if trading stock is insured against fire and flood risks"),

        ("Stock Turnover Rate",
         "The number of times a business sells and replaces its average inventory during a year, calculated as: Cost of Sales / Average Trading Stock",
         "The total cash received from cash sales divided by the closing bank balance",
         "The number of days it takes customers to settle their credit accounts",
         "The percentage markup applied to cost price to establish the retail selling price",
         "The physical speed of delivery vehicles transporting merchandise between retail stores",
         "The ratio of current assets to current liabilities on the statement of financial position",
         "The total units of stock damaged and written off during physical stock counts"),

        ("Stock Holding Period",
         "The average number of days merchandise remains in stock before being sold, calculated as: (Average Stock / Cost of Sales) x 365 days",
         "The statutory period during which a company must retain accounting records under the Companies Act",
         "The maximum credit period granted by suppliers before charging overdue interest",
         "The number of days an external audit firm spends auditing the client storehouse",
         "The time taken to transport imported goods from Durban harbour to Johannesburg",
         "The warranty period granted to retail customers purchasing electronic appliances",
         "The duration of the commercial property lease contract for the central warehouse"),

        ("Lower of Cost or Net Realizable Value (NRV)",
         "Trading stock must be valued at the lower of its historical cost or net realizable value (estimated selling price less completion and selling costs) to prevent overstating assets",
         "Trading stock must always be valued at retail selling price to reflect anticipated profit",
         "Trading stock should be written up to replacement cost during periods of inflation",
         "Stock must be valued at zero if it has been stored in the warehouse for more than 30 days",
         "Trading stock should be valued at cost plus a mandatory 25% markup under IFRS rules",
         "Stock is valued at whichever price the external registered auditor personally chooses",
         "Trading stock must be valued at the average market price of shares on the JSE"),

        ("Carriage on Purchases of Trading Stock",
         "Transport costs incurred to deliver purchased merchandise to the business premises, which must be added to the cost price of inventory",
         "Delivery costs incurred to transport sold goods to retail customers' homes",
         "Maintenance expenses for servicing company administrative executive vehicles",
         "Fuel costs incurred by sales representatives visiting regional retail branches",
         "Storage rent paid for housing excess finished inventory in third-party depots",
         "A non-operating finance expense paid to commercial mortgage lenders",
         "A deductible tax expense that is excluded from the general ledger inventory account")
    ]

    for title_i, corr_i, *wrongs_i in easy_concepts:
        q_i1 = f"In CAPS Grade 12 Accounting Paper 2 (Inventory), what is the correct rule regarding **{title_i}**?"
        exp_i1 = f"**{title_i}**: {corr_i}. This is a fundamental concept in Grade 12 Inventory Valuation."
        add_q("easy", "Inventory Concepts & Systems", q_i1, corr_i, wrongs_i, "Remembering", f"Define rule for {title_i}", exp_i1)

        q_i2 = f"Which inventory accounting term or statutory valuation principle is described as: *\"{corr_i}\"*?"
        clean_terms_i = [
            "Perpetual Inventory Ledger", "Periodic Trading Account",
            "Standard Cost Variance Matrix", "Economic Order Quantity (EOQ)",
            "Safety Stock Buffer Model", "Goods Received Note Verification",
            "Batch Tracking Identification"
        ]
        exp_i2 = f"This describes **{title_i}**. {corr_i}."
        add_q("easy", "Inventory Concepts & Systems", q_i2, title_i, clean_terms_i, "Understanding", f"Identify {title_i}", exp_i2)

    # 65 South African retail businesses for Easy Calculations (65 x 4 = 260 Qs)
    calc_easy_inv = [
        ("Protea Electronics Ltd", 500, 2000, 50, 1800, 4200000.0, 700000.0),
        ("Kavango Traders Ltd", 800, 3500, 100, 3200, 5800000.0, 950000.0),
        ("Algoa Furnishers Ltd", 300, 1200, 30, 1100, 3600000.0, 650000.0),
        ("Soweto Appliance Mart Ltd", 1200, 4800, 150, 4400, 8500000.0, 1400000.0),
        ("Drakensberg Hardware Ltd", 650, 2600, 80, 2400, 4100000.0, 720000.0),
        ("Zululand Wholesalers Ltd", 1500, 6000, 200, 5500, 9800000.0, 1650000.0),
        ("Highveld Computech Ltd", 900, 3800, 120, 3500, 7200000.0, 1200000.0),
        ("Karoo Motors Ltd", 250, 1000, 25, 950, 6800000.0, 1150000.0),
        ("Table Mountain Books Ltd", 2000, 8500, 250, 7800, 3200000.0, 580000.0),
        ("Springbok Sports Mart Ltd", 1100, 4400, 110, 4100, 5200000.0, 880000.0),
        ("Limpopo Farm Store Ltd", 750, 3000, 90, 2800, 4600000.0, 820000.0),
        ("Blyde Timber Merchants Ltd", 400, 1800, 45, 1650, 3900000.0, 680000.0),
        ("Gauteng Health & Beauty Ltd", 1800, 7200, 220, 6800, 6400000.0, 1100000.0),
        ("Free State Grain Mart Ltd", 1300, 5200, 160, 4800, 5500000.0, 920000.0),
        ("Namaqua Diamond Jewelers Ltd", 180, 750, 20, 700, 7800000.0, 1350000.0),
        ("Outeniqua Garden World Ltd", 850, 3400, 95, 3200, 3400000.0, 620000.0),
        ("Mpumalanga Tile Center Ltd", 1400, 5600, 180, 5200, 6100000.0, 1050000.0),
        ("Ezulwini Homeware Ltd", 950, 3900, 130, 3600, 4400000.0, 780000.0),
        ("Vaal Triangle Motors Ltd", 220, 920, 22, 880, 8200000.0, 1450000.0),
        ("Stellenbosch Cellars Ltd", 1600, 6500, 200, 6100, 5900000.0, 1020000.0),
        ("Tshwane Auto Spares Ltd", 1050, 4300, 140, 4000, 6600000.0, 1120000.0),
        ("Richards Bay Tools Ltd", 880, 3600, 110, 3350, 4900000.0, 860000.0),
        ("Polokwane Cash & Carry Ltd", 2200, 9000, 300, 8400, 11200000.0, 1950000.0),
        ("Kimberley Mining Gear Ltd", 680, 2800, 85, 2600, 5400000.0, 940000.0),
        ("Durban Fashion House Ltd", 1250, 5100, 150, 4700, 5700000.0, 980000.0),
        ("Rustenburg Tool Mart Ltd", 1150, 4700, 160, 4400, 7400000.0, 1280000.0),
        ("Witbank Electrical Mart Ltd", 920, 3800, 120, 3550, 5600000.0, 960000.0),
        ("Paarl Fresh Foods Ltd", 1750, 7200, 240, 6800, 6900000.0, 1180000.0),
        ("Midrand IT Direct Ltd", 1350, 5500, 180, 5100, 8800000.0, 1520000.0),
        ("Centurion Sports Emporium Ltd", 980, 4000, 130, 3750, 5300000.0, 920000.0),
        ("Bloemfontein Meats Ltd", 1650, 6800, 210, 6400, 7900000.0, 1360000.0),
        ("East London Marine Spares Ltd", 580, 2400, 75, 2250, 4300000.0, 760000.0),
        ("Klerksdorp Tile Direct Ltd", 1120, 4600, 150, 4300, 6200000.0, 1080000.0),
        ("Potchefstroom Stationery Hub Ltd", 1450, 6000, 190, 5600, 3800000.0, 690000.0),
        ("George Home Living Ltd", 720, 3000, 95, 2800, 4500000.0, 810000.0),
        ("Secunda Safety & Industrial Ltd", 1020, 4200, 140, 3900, 6700000.0, 1160000.0),
        ("Vereeniging Steel Goods Ltd", 840, 3500, 110, 3250, 7800000.0, 1340000.0),
        ("Welkom Mine Supply Ltd", 960, 4000, 130, 3700, 6500000.0, 1140000.0),
        ("Bethlehem Grain Traders Ltd", 1280, 5300, 170, 4950, 5600000.0, 990000.0),
        ("Newcastle Tool Warehouse Ltd", 890, 3700, 120, 3450, 5800000.0, 1020000.0),
        ("Mossel Bay Marine Traders Ltd", 640, 2700, 85, 2500, 4800000.0, 850000.0),
        ("Mthatha Wholesale Hub Ltd", 1180, 4900, 160, 4550, 5900000.0, 1040000.0),
        ("Upington Agro Direct Ltd", 780, 3200, 105, 3000, 4400000.0, 790000.0),
        ("Vryheid Timber Depot Ltd", 820, 3400, 115, 3150, 5100000.0, 910000.0),
        ("Ladysmith Fashion Mart Ltd", 940, 3900, 130, 3650, 4700000.0, 840000.0),
        ("Bredasdorp Grain Store Ltd", 1220, 5100, 165, 4750, 5700000.0, 1010000.0),
        ("Cradock Livestock Hub Ltd", 860, 3600, 120, 3350, 5200000.0, 930000.0),
        ("Makhanda Scholastic Supplies Ltd", 1320, 5500, 180, 5100, 4100000.0, 750000.0),
        ("Oudtshoorn Leathercraft Ltd", 740, 3100, 100, 2900, 4600000.0, 830000.0),
        ("Knysna Marine Woods Ltd", 690, 2900, 95, 2700, 5300000.0, 950000.0),
        ("Standerton Milking Systems Ltd", 810, 3400, 110, 3150, 5500000.0, 980000.0),
        ("Harrismith Logistics Depot Ltd", 950, 4000, 130, 3750, 6300000.0, 1120000.0),
        ("Kuruman Mineral Traders Ltd", 880, 3700, 120, 3450, 7600000.0, 1320000.0),
        ("Thohoyandou Superstore Ltd", 1550, 6500, 210, 6100, 7400000.0, 1300000.0),
        ("Plettenberg Bay Decor Ltd", 680, 2800, 90, 2600, 4900000.0, 870000.0),
        ("Saldanha Marine Freight Ltd", 1150, 4800, 155, 4500, 8900000.0, 1550000.0),
        ("Grahamstown Scholastic Ltd", 1080, 4500, 145, 4200, 4200000.0, 770000.0),
        ("Springbok Wind Parts Ltd", 540, 2300, 75, 2150, 6800000.0, 1190000.0),
        ("Witbank Coal Equipment Ltd", 780, 3300, 105, 3100, 8400000.0, 1460000.0),
        ("Paarl Valley Beverages Ltd", 1420, 5900, 190, 5500, 6600000.0, 1170000.0),
        ("Centurion Office Machines Ltd", 920, 3900, 125, 3650, 6200000.0, 1100000.0),
        ("Bloemfontein Grain Merchants Ltd", 1180, 4900, 160, 4600, 5800000.0, 1030000.0),
        ("East London Fishing Gear Ltd", 610, 2600, 85, 2420, 4400000.0, 790000.0),
        ("Klerksdorp Mining Supplies Ltd", 870, 3700, 120, 3450, 7100000.0, 1240000.0),
        ("Potchefstroom Feeds Mart Ltd", 1250, 5200, 170, 4850, 5600000.0, 990000.0),
        ("Newcastle Heavy Steels Ltd", 940, 3900, 130, 3650, 7300000.0, 1280000.0),
        ("Mossel Bay Offshore Mart Ltd", 520, 2200, 70, 2050, 4900000.0, 860000.0),
        ("Mthatha Timber Supplies Ltd", 780, 3300, 110, 3100, 4500000.0, 810000.0),
        ("Upington Sun Agro Supplies Ltd", 690, 2900, 95, 2720, 4200000.0, 750000.0),
        ("Vryheid Coal Merchants Ltd", 840, 3500, 115, 3280, 5300000.0, 930000.0),
        ("Ladysmith Textiles Mart Ltd", 1100, 4600, 150, 4300, 6100000.0, 1070000.0),
        ("Bredasdorp Wheat Store Ltd", 1350, 5600, 180, 5250, 5900000.0, 1040000.0),
        ("Cradock Merinos Supplies Ltd", 720, 3000, 100, 2800, 4700000.0, 830000.0),
        ("Makhanda Print Supplies Ltd", 1480, 6200, 200, 5800, 4300000.0, 760000.0),
        ("Oudtshoorn Leather Supplies Ltd", 810, 3400, 110, 3180, 4800000.0, 850000.0)
    ]

    for co_i, op_u, pur_u, ret_u, sold_u, cos_val, avg_stk in calc_easy_inv:
        # 1. Total units available for sale
        avail_u = op_u + pur_u - ret_u
        c_au = f"{avail_u:,.0f} units"
        w_au = [
            f"{op_u + pur_u:,.0f} units (forgot to deduct returns to suppliers)",
            f"{pur_u - ret_u:,.0f} units (omitted opening stock)",
            f"{op_u + pur_u + ret_u:,.0f} units (added returns instead of deducting)",
            f"{avail_u * 1.2:,.0f} units",
            f"{avail_u * 0.8:,.0f} units",
            f"{avail_u + 250:,.0f} units",
            f"{avail_u - 200:,.0f} units"
        ]
        q_au = (f"The stock records of **{co_i}** reflect the following trading unit movements for the year:\n"
                f"- Opening stock: **{op_u:,.0f} units**\n"
                f"- Purchases: **{pur_u:,.0f} units**\n"
                f"- Defective units returned to suppliers: **{ret_u:,.0f} units**\n"
                f"Calculate the **total units available for sale** during the year:")
        exp_au = f"Units Available for Sale = Opening Stock + Purchases - Returns to Suppliers = {op_u:,.0f} + {pur_u:,.0f} - {ret_u:,.0f} = {c_au}."
        add_q("easy", "Stock Quantity Calculations", q_au, c_au, w_au, "Applying", f"Calculate available units for {co_i}", exp_au)

        # 2. Closing Stock in Units (Theoretical)
        cl_u = avail_u - sold_u
        c_cu = f"{cl_u:,.0f} units"
        w_cu = [
            f"{avail_u:,.0f} units (omitted units sold)",
            f"{sold_u:,.0f} units (confused with units sold)",
            f"{op_u + pur_u - sold_u:,.0f} units (omitted returns to suppliers)",
            f"{cl_u * 1.25:,.0f} units",
            f"{cl_u * 0.75:,.0f} units",
            f"{cl_u + 120:,.0f} units",
            f"{cl_u - 100:,.0f} units"
        ]
        q_cu = (f"**{co_i}** had **{avail_u:,.0f} units** available for sale and sold **{sold_u:,.0f} units** during the trading year. "
                f"Assuming zero stock shrinkage or theft, how many units should remain in **closing trading stock** at year-end?")
        exp_cu = f"Theoretical Closing Stock = Units Available for Sale - Units Sold = {avail_u:,.0f} - {sold_u:,.0f} = {c_cu}."
        add_q("easy", "Stock Quantity Calculations", q_cu, c_cu, w_cu, "Applying", f"Calculate closing stock units for {co_i}", exp_cu)

        # 3. Stock Turnover Rate
        stor_val = cos_val / avg_stk
        c_stor = f"{stor_val:.2f} times per year"
        w_stor = [
            f"{avg_stk / cos_val:.2f} times per year (inverted: Average Stock / Cost of Sales)",
            f"{stor_val * 1.5:.2f} times per year",
            f"{stor_val * 0.5:.2f} times per year",
            f"{(cos_val / (avg_stk * 1.2)):.2f} times per year",
            f"{stor_val + 2.0:.2f} times per year",
            f"{stor_val - 1.5:.2f} times per year",
            f"{(cos_val * 1.2) / avg_stk:.2f} times per year"
        ]
        q_stor = (f"The financial records of **{co_i}** show Cost of Sales of **R{cos_val:,.2f}** and Average Trading Stock of **R{avg_stk:,.2f}**. "
                  f"Calculate the **Stock Turnover Rate** (times per year, rounded to two decimal places):")
        exp_stor = f"Stock Turnover Rate = Cost of Sales / Average Trading Stock = R{cos_val:,.2f} / R{avg_stk:,.2f} = {c_stor}."
        add_q("easy", "Stock Turnover & Holding Period", q_stor, c_stor, w_stor, "Applying", f"Calculate stock turnover rate for {co_i}", exp_stor)

        # 4. Stock Holding Period (Days)
        shp_val = (avg_stk / cos_val) * 365
        c_shp = f"{shp_val:.1f} days"
        w_shp = [
            f"{(cos_val / avg_stk) * 365:.1f} days (inverted: Cost of Sales / Average Stock)",
            f"{shp_val * 1.5:.1f} days",
            f"{shp_val * 0.5:.1f} days",
            f"{(avg_stk / cos_val) * 30:.1f} days (multiplied by 30 days instead of 365)",
            f"{shp_val + 15.0:.1f} days",
            f"{shp_val - 12.0:.1f} days",
            f"{(cos_val / avg_stk):.1f} days"
        ]
        q_shp = (f"Using the figures for **{co_i}** (Cost of Sales **R{cos_val:,.2f}**, Average Trading Stock **R{avg_stk:,.2f}**), "
                 f"calculate the **Stock Holding Period in days** (using 365 days):")
        exp_shp = f"Stock Holding Period = (Average Trading Stock / Cost of Sales) x 365 = (R{avg_stk:,.2f} / R{cos_val:,.2f}) x 365 = {c_shp}."
        add_q("easy", "Stock Turnover & Holding Period", q_shp, c_shp, w_shp, "Applying", f"Calculate stock holding period for {co_i}", exp_shp)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # FIFO Valuation, Weighted Average Valuation, Cost of Sales, Gross Profit
    # =========================================================================

    # 50 South African commercial retailers with detailed multi-batch purchases
    # (Company, Product, Op_u, Op_p, B1_u, B1_p, B1_carr, B2_u, B2_p, B2_carr, B3_u, B3_p, B3_carr, Sold_u, SP)
    # Total available = Op_u + B1_u + B2_u + B3_u
    # Total available cost = (Op_u * Op_p) + (B1_u * (B1_p + B1_carr)) + (B2_u * (B2_p + B2_carr)) + (B3_u * (B3_p + B3_carr))
    fifo_scenarios = [
        ("Protea Audio Ltd", "Noise-Cancelling Headphones", 200, 850.0, 400, 920.0, 30.0, 500, 980.0, 40.0, 600, 1050.0, 50.0, 1400, 1650.0),
        ("Kavango Outdoors Ltd", "All-Weather Hiking Tents", 150, 1400.0, 300, 1520.0, 50.0, 450, 1600.0, 60.0, 500, 1720.0, 80.0, 1150, 2600.0),
        ("Algoa Furnishers Ltd", "Ergonomic Office Chairs", 120, 1850.0, 250, 1980.0, 70.0, 350, 2100.0, 80.0, 400, 2250.0, 100.0, 920, 3400.0),
        ("Soweto Appliance Mart Ltd", "Microwave Ovens", 300, 1100.0, 600, 1180.0, 40.0, 800, 1260.0, 50.0, 900, 1340.0, 60.0, 2100, 2100.0),
        ("Drakensberg Hardware Ltd", "Cordless Impact Drills", 250, 950.0, 500, 1040.0, 35.0, 700, 1120.0, 45.0, 750, 1200.0, 55.0, 1800, 1950.0),
        ("Zululand Wholesalers Ltd", "LED Floodlights (50W)", 500, 320.0, 1000, 350.0, 15.0, 1200, 380.0, 20.0, 1500, 410.0, 25.0, 3400, 680.0),
        ("Highveld Computech Ltd", "Gaming Monitors (27-inch)", 180, 2800.0, 350, 3000.0, 90.0, 450, 3200.0, 110.0, 520, 3450.0, 130.0, 1220, 5200.0),
        ("Karoo Motors Ltd", "High-Performance Vehicle Batteries", 220, 1650.0, 450, 1780.0, 60.0, 600, 1900.0, 70.0, 650, 2050.0, 85.0, 1580, 3100.0),
        ("Table Mountain Books Ltd", "Medical Reference Atlases", 400, 650.0, 800, 710.0, 25.0, 1100, 760.0, 30.0, 1200, 820.0, 40.0, 2900, 1350.0),
        ("Springbok Sports Mart Ltd", "Professional Tennis Rackets", 280, 1250.0, 550, 1360.0, 45.0, 750, 1450.0, 55.0, 820, 1580.0, 70.0, 1980, 2550.0),
        ("Limpopo Farm Store Ltd", "Electric Fence Energizers", 160, 2100.0, 320, 2280.0, 75.0, 420, 2450.0, 90.0, 500, 2650.0, 110.0, 1140, 4100.0),
        ("Blyde Timber Merchants Ltd", "Hardwood Workbench Units", 100, 3200.0, 220, 3450.0, 120.0, 300, 3700.0, 140.0, 350, 3980.0, 170.0, 810, 6200.0),
        ("Gauteng Health & Beauty Ltd", "Salon Hair Steamers", 240, 1550.0, 480, 1680.0, 55.0, 650, 1800.0, 65.0, 730, 1950.0, 80.0, 1720, 3100.0),
        ("Free State Grain Mart Ltd", "Moisture Meter Kits", 150, 2400.0, 300, 2600.0, 80.0, 400, 2800.0, 100.0, 450, 3050.0, 120.0, 1080, 4800.0),
        ("Namaqua Diamond Jewelers Ltd", "Automatic Watch Winders", 90, 4500.0, 180, 4850.0, 150.0, 240, 5200.0, 180.0, 290, 5600.0, 220.0, 650, 8900.0),
        ("Outeniqua Garden World Ltd", "Petrol Lawn Trimmers", 210, 1350.0, 420, 1480.0, 50.0, 580, 1590.0, 60.0, 640, 1720.0, 75.0, 1510, 2750.0),
        ("Mpumalanga Tile Center Ltd", "Tile Cutting Laser Saws", 140, 2900.0, 280, 3150.0, 100.0, 380, 3380.0, 120.0, 420, 3650.0, 150.0, 1010, 5800.0),
        ("Ezulwini Homeware Ltd", "Espresso Coffee Machines", 190, 2200.0, 380, 2400.0, 80.0, 520, 2580.0, 95.0, 590, 2790.0, 115.0, 1390, 4400.0),
        ("Vaal Triangle Motors Ltd", "Hydraulic Floor Jacks (3-ton)", 170, 1950.0, 350, 2120.0, 70.0, 480, 2280.0, 85.0, 540, 2460.0, 105.0, 1260, 3900.0),
        ("Stellenbosch Cellars Ltd", "Temperature-Controlled Wine Fridges", 110, 4200.0, 220, 4550.0, 140.0, 310, 4880.0, 170.0, 360, 5250.0, 210.0, 830, 8400.0),
        ("Tshwane Auto Spares Ltd", "Diagnostic OBD2 Scanners", 260, 1750.0, 520, 1900.0, 60.0, 700, 2050.0, 75.0, 780, 2220.0, 95.0, 1850, 3500.0),
        ("Richards Bay Tools Ltd", "Heavy Duty Bench Grinders", 230, 1450.0, 460, 1580.0, 50.0, 620, 1710.0, 65.0, 690, 1860.0, 80.0, 1630, 2950.0),
        ("Polokwane Cash & Carry Ltd", "Stainless Steel Urns (20L)", 350, 880.0, 700, 960.0, 35.0, 950, 1040.0, 45.0, 1100, 1130.0, 55.0, 2550, 1850.0),
        ("Kimberley Mining Gear Ltd", "Mining Cap Lamps & Chargers", 320, 1150.0, 640, 1250.0, 45.0, 850, 1360.0, 55.0, 950, 1480.0, 70.0, 2280, 2350.0),
        ("Durban Fashion House Ltd", "Cashmere Overcoats", 160, 2600.0, 320, 2850.0, 90.0, 440, 3080.0, 110.0, 480, 3350.0, 135.0, 1150, 5400.0),
        ("Rustenburg Tool Mart Ltd", "Rotary Hammer Drills", 210, 2300.0, 420, 2500.0, 80.0, 560, 2700.0, 95.0, 610, 2920.0, 120.0, 1480, 4650.0),
        ("Witbank Electrical Mart Ltd", "Solar Inverters (5kW)", 130, 6800.0, 260, 7350.0, 220.0, 350, 7900.0, 260.0, 400, 8500.0, 320.0, 940, 13500.0),
        ("Paarl Fresh Foods Ltd", "Stainless Steel Meat Slicers", 170, 3100.0, 340, 3380.0, 110.0, 460, 3640.0, 130.0, 510, 3940.0, 160.0, 1220, 6200.0),
        ("Midrand IT Direct Ltd", "Laser Printers (Multifunction)", 250, 3400.0, 500, 3700.0, 120.0, 680, 3980.0, 145.0, 750, 4300.0, 180.0, 1780, 6800.0),
        ("Centurion Sports Emporium Ltd", "Elliptical Cross Trainers", 95, 5400.0, 190, 5850.0, 180.0, 260, 6280.0, 220.0, 295, 6750.0, 270.0, 680, 10800.0),
        ("Bloemfontein Meats Ltd", "Vacuum Sealers (Commercial)", 220, 2150.0, 440, 2350.0, 75.0, 590, 2540.0, 90.0, 650, 2750.0, 110.0, 1560, 4400.0),
        ("East London Marine Spares Ltd", "Boat Bilge Pumps (Submersible)", 310, 920.0, 620, 1010.0, 35.0, 840, 1090.0, 45.0, 930, 1180.0, 55.0, 2220, 1950.0),
        ("Klerksdorp Tile Direct Ltd", "Tile Grout Mixers (Electric)", 180, 1850.0, 360, 2020.0, 65.0, 490, 2190.0, 80.0, 540, 2380.0, 95.0, 1290, 3750.0),
        ("Potchefstroom Stationery Hub Ltd", "Heavy Duty Document Shredders", 270, 1400.0, 540, 1530.0, 50.0, 720, 1650.0, 60.0, 810, 1790.0, 75.0, 1920, 2850.0),
        ("George Home Living Ltd", "Ceiling Fans with Remote", 340, 1150.0, 680, 1250.0, 40.0, 910, 1360.0, 50.0, 1020, 1480.0, 65.0, 2450, 2350.0),
        ("Secunda Safety & Industrial Ltd", "Welding Inverters (200A)", 190, 2750.0, 380, 2980.0, 95.0, 510, 3220.0, 115.0, 570, 3480.0, 140.0, 1370, 5500.0),
        ("Vereeniging Steel Goods Ltd", "Angle Grinders (9-inch)", 280, 1650.0, 560, 1800.0, 60.0, 750, 1940.0, 70.0, 840, 2100.0, 85.0, 2010, 3300.0),
        ("Welkom Mine Supply Ltd", "Pneumatic Grease Guns", 240, 1520.0, 480, 1650.0, 55.0, 640, 1780.0, 65.0, 720, 1920.0, 80.0, 1720, 3050.0),
        ("Bethlehem Grain Traders Ltd", "Grain Moisture Probes", 160, 2350.0, 320, 2550.0, 80.0, 430, 2750.0, 95.0, 480, 2980.0, 120.0, 1150, 4700.0),
        ("Newcastle Tool Warehouse Ltd", "Electric Chain Hoists", 120, 4100.0, 240, 4450.0, 140.0, 320, 4780.0, 170.0, 370, 5150.0, 210.0, 860, 8200.0),
        ("Mossel Bay Marine Traders Ltd", "Marine VHF Radios", 210, 1850.0, 420, 2020.0, 65.0, 560, 2180.0, 80.0, 630, 2360.0, 95.0, 1500, 3700.0),
        ("Mthatha Wholesale Hub Ltd", "Commercial Deep Fryers", 175, 2950.0, 350, 3200.0, 105.0, 470, 3450.0, 125.0, 525, 3720.0, 155.0, 1250, 5900.0),
        ("Upington Agro Direct Ltd", "Solar Water Borehole Pumps", 85, 7500.0, 170, 8100.0, 250.0, 230, 8750.0, 300.0, 265, 9400.0, 360.0, 610, 14900.0),
        ("Vryheid Timber Depot Ltd", "Portable Circular Saws", 260, 1580.0, 520, 1720.0, 55.0, 700, 1850.0, 65.0, 780, 2000.0, 80.0, 1860, 3150.0),
        ("Ladysmith Fashion Mart Ltd", "Industrial Sewing Machines", 115, 4800.0, 230, 5200.0, 160.0, 310, 5580.0, 195.0, 350, 6020.0, 240.0, 820, 9600.0),
        ("Bredasdorp Grain Store Ltd", "Digital Platform Scales", 195, 2100.0, 390, 2300.0, 75.0, 520, 2480.0, 90.0, 585, 2690.0, 110.0, 1390, 4250.0),
        ("Cradock Livestock Hub Ltd", "Cattle Weighing Crates", 70, 8800.0, 140, 9500.0, 300.0, 190, 10250.0, 360.0, 215, 11100.0, 440.0, 500, 17500.0),
        ("Makhanda Scholastic Supplies Ltd", "Digital Video Projectors", 155, 3600.0, 310, 3900.0, 125.0, 420, 4220.0, 150.0, 470, 4580.0, 190.0, 1110, 7200.0),
        ("Oudtshoorn Leathercraft Ltd", "Heavy Duty Skiving Machines", 105, 5100.0, 210, 5550.0, 175.0, 280, 5980.0, 210.0, 315, 6450.0, 260.0, 750, 10200.0),
        ("Knysna Marine Woods Ltd", "Electric Planer Thicknessers", 80, 7200.0, 160, 7800.0, 240.0, 220, 8420.0, 290.0, 250, 9100.0, 350.0, 580, 14500.0)
    ]

    for co_s, prod_s, op_u, op_p, b1_u, b1_p, b1_c, b2_u, b2_p, b2_c, b3_u, b3_p, b3_c, sold_u, sp_val in fifo_scenarios:
        # Effective unit cost including carriage
        c_b1 = b1_p + b1_c
        c_b2 = b2_p + b2_c
        c_b3 = b3_p + b3_c

        tot_u_avail = op_u + b1_u + b2_u + b3_u
        tot_cost_avail = (op_u * op_p) + (b1_u * c_b1) + (b2_u * c_b2) + (b3_u * c_b3)

        cl_units = tot_u_avail - sold_u

        # FIFO Closing Stock Valuation:
        # Latest purchases first: take from Batch 3, then Batch 2 if needed
        if cl_units <= b3_u:
            fifo_cl_val = cl_units * c_b3
            fifo_expl_cl = f"{cl_units:,.0f} units from Batch 3 at R{c_b3:.2f} (R{b3_p:.2f} + R{b3_c:.2f} carriage)"
        else:
            rem_after_b3 = cl_units - b3_u
            fifo_cl_val = (b3_u * c_b3) + (rem_after_b3 * c_b2)
            fifo_expl_cl = f"{b3_u:,.0f} units from Batch 3 at R{c_b3:.2f} (R{b3_u * c_b3:,.2f}) + {rem_after_b3:,.0f} units from Batch 2 at R{c_b2:.2f} (R{rem_after_b3 * c_b2:,.2f})"

        fifo_cos = tot_cost_avail - fifo_cl_val
        tot_rev = sold_u * sp_val
        fifo_gp = tot_rev - fifo_cos

        # Weighted Average Cost Method:
        w_avg_cost_u = tot_cost_avail / tot_u_avail
        w_avg_cl_val = cl_units * w_avg_cost_u
        w_avg_cos = tot_cost_avail - w_avg_cl_val
        w_avg_gp = tot_rev - w_avg_cos

        # 1. Medium Q: Closing Stock Valuation under FIFO
        if counts["medium"] < 500:
            c_fcl = f"R{fifo_cl_val:,.2f}"
            w_fcl = [
                f"R{cl_units * op_p:,.2f} (valued closing stock at opening price)",
                f"R{w_avg_cl_val:,.2f} (calculated weighted average closing stock instead of FIFO)",
                f"R{cl_units * b3_p:,.2f} (omitted carriage on purchases in Batch 3)",
                f"R{fifo_cl_val * 1.15:,.2f}",
                f"R{fifo_cl_val * 0.85:,.2f}",
                f"R{(fifo_cl_val + 50000):,.2f}",
                f"R{(fifo_cl_val - 45000):,.2f}"
            ]
            q_fcl = (f"The stock records of **{co_s}** for *{prod_s}* show the following for the year:\n"
                     f"- Opening stock: **{op_u:,.0f} units** at **R{op_p:.2f}**\n"
                     f"- Purchase Batch 1 (May): **{b1_u:,.0f} units** at **R{b1_p:.2f}** (carriage R{b1_c:.2f}/unit)\n"
                     f"- Purchase Batch 2 (August): **{b2_u:,.0f} units** at **R{b2_p:.2f}** (carriage R{b2_c:.2f}/unit)\n"
                     f"- Purchase Batch 3 (November): **{b3_u:,.0f} units** at **R{b3_p:.2f}** (carriage R{b3_c:.2f}/unit)\n"
                     f"Total units sold: **{sold_u:,.0f} units**. The company uses the **FIFO method**.\n"
                     f"Calculate the **value of Closing Inventory** at year-end:")
            exp_fcl = (f"Total Units Available = {tot_u_avail:,.0f} units\n"
                       f"Closing Stock Units = {tot_u_avail:,.0f} - {sold_u:,.0f} = {cl_units:,.0f} units.\n"
                       f"Under FIFO, closing stock comes from the most recent purchases:\n"
                       f"= {fifo_expl_cl} = {c_fcl}.")
            add_q("medium", "FIFO Inventory Valuation", q_fcl, c_fcl, w_fcl, "Applying", f"Calculate FIFO closing stock for {co_s}", exp_fcl)

        # 2. Medium Q: Cost of Sales under FIFO
        if counts["medium"] < 500:
            c_fcos = f"R{fifo_cos:,.2f}"
            w_fcos = [
                f"R{tot_cost_avail:,.2f} (omitted closing inventory deduction: total available cost)",
                f"R{w_avg_cos:,.2f} (calculated Cost of Sales under weighted average method)",
                f"R{sold_u * op_p:,.2f} (multiplied sold units by opening cost price only)",
                f"R{fifo_cos * 1.15:,.2f}",
                f"R{fifo_cos * 0.85:,.2f}",
                f"R{(fifo_cos + 70000):,.2f}",
                f"R{(fifo_cos - 60000):,.2f}"
            ]
            q_fcos = (f"Referring to **{co_s}** (*{prod_s}*): Total cost of goods available for sale was **R{tot_cost_avail:,.2f}** "
                      f"and the FIFO value of closing stock was calculated as **R{fifo_cl_val:,.2f}**. "
                      f"Calculate the **Cost of Sales under FIFO** for the Income Statement:")
            exp_fcos = (f"Cost of Sales = Total Cost of Available Goods - Closing Stock Value (FIFO)\n"
                        f"= R{tot_cost_avail:,.2f} - R{fifo_cl_val:,.2f} = {c_fcos}.")
            add_q("medium", "FIFO Inventory Valuation", q_fcos, c_fcos, w_fcos, "Applying", f"Calculate FIFO cost of sales for {co_s}", exp_fcos)

        # 3. Medium Q: Gross Profit under FIFO
        if counts["medium"] < 500:
            c_fgp = f"R{fifo_gp:,.2f}"
            w_fgp = [
                f"R{tot_rev:,.2f} (sales revenue only: omitted Cost of Sales)",
                f"R{w_avg_gp:,.2f} (calculated Gross Profit under weighted average method)",
                f"R{tot_rev - (sold_u * op_p):,.2f}",
                f"R{fifo_gp * 1.15:,.2f}",
                f"R{fifo_gp * 0.85:,.2f}",
                f"R{(fifo_gp + 80000):,.2f}",
                f"R{(fifo_gp - 70000):,.2f}"
            ]
            q_fgp = (f"**{co_s}** sold **{sold_u:,.0f} units** of *{prod_s}* at **R{sp_val:,.2f}** per unit (Total Sales: **R{tot_rev:,.2f}**). "
                     f"Cost of Sales under FIFO is **R{fifo_cos:,.2f}**. Calculate the **Gross Profit under FIFO**:")
            exp_fgp = (f"Gross Profit = Sales Revenue - Cost of Sales\n"
                       f"= R{tot_rev:,.2f} - R{fifo_cos:,.2f} = {c_fgp}.")
            add_q("medium", "FIFO Inventory Valuation", q_fgp, c_fgp, w_fgp, "Applying", f"Calculate FIFO gross profit for {co_s}", exp_fgp)

        # 4. Medium Q: Weighted Average Cost per Unit
        if counts["medium"] < 500:
            c_wacu = f"R{w_avg_cost_u:.2f}"
            w_wacu = [
                f"R{(op_p + b1_p + b2_p + b3_p) / 4:.2f} (simple average of unit prices: ignored quantities and carriage)",
                f"R{op_p:.2f} (opening price only)",
                f"R{c_b3:.2f} (latest batch price only)",
                f"R{w_avg_cost_u * 1.15:.2f}",
                f"R{w_avg_cost_u * 0.85:.2f}",
                f"R{(w_avg_cost_u + 35.0):.2f}",
                f"R{(w_avg_cost_u - 25.0):.2f}"
            ]
            q_wacu = (f"**{co_s}** uses the **Weighted Average Cost method** for *{prod_s}*. "
                      f"Total cost of available goods (including carriage) is **R{tot_cost_avail:,.2f}** across **{tot_u_avail:,.0f} units**. "
                      f"Calculate the **weighted average cost per unit** (rounded to two decimal places):")
            exp_wacu = (f"Weighted Average Cost per Unit = Total Cost of Goods Available / Total Units Available\n"
                        f"= R{tot_cost_avail:,.2f} / {tot_u_avail:,.0f} = {c_wacu} per unit.")
            add_q("medium", "Weighted Average Inventory Valuation", q_wacu, c_wacu, w_wacu, "Applying", f"Calculate weighted average unit cost for {co_s}", exp_wacu)

        # 5. Medium Q: Closing Stock Valuation under Weighted Average
        if counts["medium"] < 500:
            c_wacl = f"R{w_avg_cl_val:,.2f}"
            w_wacl = [
                f"R{fifo_cl_val:,.2f} (calculated closing stock under FIFO instead of weighted average)",
                f"R{cl_units * op_p:,.2f} (valued closing stock at opening price)",
                f"R{cl_units * c_b3:,.2f} (valued closing stock at latest purchase price)",
                f"R{w_avg_cl_val * 1.15:,.2f}",
                f"R{w_avg_cl_val * 0.85:,.2f}",
                f"R{(w_avg_cl_val + 40000):,.2f}",
                f"R{(w_avg_cl_val - 35000):,.2f}"
            ]
            q_wacl = (f"Referring to **{co_s}**: The weighted average cost per unit is **R{w_avg_cost_u:.2f}** "
                      f"and there are **{cl_units:,.0f} units** on hand at year-end. "
                      f"Calculate the **value of Closing Inventory under the Weighted Average method**:")
            exp_wacl = (f"Closing Stock Value = Closing Units x Weighted Average Cost per Unit\n"
                        f"= {cl_units:,.0f} units x R{w_avg_cost_u:.2f} = {c_wacl}.")
            add_q("medium", "Weighted Average Inventory Valuation", q_wacl, c_wacl, w_wacl, "Applying", f"Calculate weighted average closing stock for {co_s}", exp_wacl)

        # 6. Medium Q: Cost of Sales under Weighted Average
        if counts["medium"] < 500:
            c_wacos = f"R{w_avg_cos:,.2f}"
            w_wacos = [
                f"R{fifo_cos:,.2f} (calculated Cost of Sales under FIFO)",
                f"R{tot_cost_avail:,.2f} (total available cost)",
                f"R{sold_u * op_p:,.2f}",
                f"R{w_avg_cos * 1.15:,.2f}",
                f"R{w_avg_cos * 0.85:,.2f}",
                f"R{(w_avg_cos + 60000):,.2f}",
                f"R{(w_avg_cos - 50000):,.2f}"
            ]
            q_wacos = (f"For **{co_s}** (*{prod_s}*), total available cost is **R{tot_cost_avail:,.2f}** "
                      f"and weighted average closing stock value is **R{w_avg_cl_val:,.2f}**. "
                      f"Calculate the **Cost of Sales under the Weighted Average method**:")
            exp_wacos = (f"Cost of Sales = Total Available Cost - Closing Stock Value (Weighted Average)\n"
                        f"= R{tot_cost_avail:,.2f} - R{w_avg_cl_val:,.2f} = {c_wacos}.")
            add_q("medium", "Weighted Average Inventory Valuation", q_wacos, c_wacos, w_wacos, "Applying", f"Calculate weighted average cost of sales for {co_s}", exp_wacos)

        # 7. Medium Q: Comparison of Gross Profit (FIFO vs Weighted Average)
        diff_gp = fifo_gp - w_avg_gp
        if counts["medium"] < 500:
            c_cgp = f"FIFO Gross Profit is R{abs(diff_gp):,.2f} {'higher' if diff_gp >= 0 else 'lower'} than Weighted Average"
            w_cgp = [
                f"Weighted Average Gross Profit is R{abs(diff_gp):,.2f} higher than FIFO",
                "Both methods produce identical Gross Profit because units sold are equal",
                f"FIFO Gross Profit is R{fifo_gp:,.2f} higher",
                f"Difference is R{abs(diff_gp) * 1.5:,.2f}",
                f"Difference is R{abs(diff_gp) * 0.5:,.2f}",
                f"Weighted Average Gross Profit is R{w_avg_gp:,.2f} lower"
            ]
            q_cgp = (f"Compare the profitability of **{co_s}** under the two stock valuation methods:\n"
                     f"- Gross Profit under FIFO: **R{fifo_gp:,.2f}**\n"
                     f"- Gross Profit under Weighted Average: **R{w_avg_gp:,.2f}**\n"
                     f"Which statement correctly compares the results?")
            exp_cgp = (f"Comparison: {c_cgp}. In times of rising purchase prices (inflation), FIFO assigns older, cheaper costs "
                       f"to Cost of Sales, resulting in higher Gross Profit and higher closing stock on the balance sheet.")
            add_q("medium", "Inventory Method Comparison", q_cgp, c_cgp, w_cgp, "Analyzing", f"Compare FIFO vs weighted average profit for {co_s}", exp_cgp)

        # 8. Medium Q: Total Available Cost of Goods
        if counts["medium"] < 500:
            c_tca = f"R{tot_cost_avail:,.2f}"
            w_tca = [
                f"R{(op_u * op_p) + (b1_u * b1_p) + (b2_u * b2_p) + (b3_u * b3_p):,.2f} (omitted carriage on purchases)",
                f"R{fifo_cos:,.2f} (confused with Cost of Sales)",
                f"R{tot_u_avail * op_p:,.2f}",
                f"R{tot_cost_avail * 1.15:,.2f}",
                f"R{tot_cost_avail * 0.85:,.2f}",
                f"R{(tot_cost_avail + 90000):,.2f}",
                f"R{(tot_cost_avail - 80000):,.2f}"
            ]
            q_tca = (f"Calculate the **Total Cost of Goods Available for Sale** for **{co_s}** (*{prod_s}*) including all purchase batches and carriage on purchases:")
            exp_tca = (f"Total Available Cost = Opening Stock + All Purchases (including carriage)\n"
                       f"= ({op_u:,.0f} x R{op_p:.2f}) + ({b1_u:,.0f} x R{c_b1:.2f}) + ({b2_u:,.0f} x R{c_b2:.2f}) + ({b3_u:,.0f} x R{c_b3:.2f})\n"
                       f"= {c_tca}.")
            add_q("medium", "Inventory Valuation Fundamentals", q_tca, c_tca, w_tca, "Applying", f"Calculate total available cost for {co_s}", exp_tca)

        # 9. Medium Q: Net Realizable Value Adjustment
        # If NRV falls below cost (e.g. damaged batch of 50 units has NRV of R500 vs cost of R1000)
        dam_units = 50
        nrv_unit = c_b3 * 0.60
        write_down_per_u = c_b3 - nrv_unit
        tot_write_down = dam_units * write_down_per_u
        if counts["medium"] < 500:
            c_nrv = f"R{tot_write_down:,.2f} write-down (operating expense in Income Statement)"
            w_nrv = [
                f"R{dam_units * c_b3:,.2f} (wrote off entire cost of damaged units without considering NRV)",
                f"R{dam_units * nrv_unit:,.2f} (used net realizable value as the write-down amount)",
                f"R{tot_write_down * 1.5:,.2f}",
                f"R{tot_write_down * 0.5:,.2f}",
                f"R{(tot_write_down + 15000):,.2f}",
                f"R{(tot_write_down - 10000):,.2f}",
                "Zero write-down because IFRS allows all inventory to remain at historical cost indefinitely"
            ]
            q_nrv = (f"At year-end, **{co_s}** discovered that **{dam_units} units** of *{prod_s}* (from Batch 3, cost **R{c_b3:.2f}** each) "
                     f"suffered water damage. They can only be sold for a Net Realizable Value of **R{nrv_unit:.2f}** each. "
                     f"In terms of IAS 2 (Lower of Cost or Net Realizable Value), calculate the **inventory write-down expense**:")
            exp_nrv = (f"Write-down per unit = Cost (R{c_b3:.2f}) - Net Realizable Value (R{nrv_unit:.2f}) = R{write_down_per_u:.2f}\n"
                       f"Total Inventory Write-Down = {dam_units} units x R{write_down_per_u:.2f} = {c_nrv}.")
            add_q("medium", "Lower of Cost or NRV", q_nrv, c_nrv, w_nrv, "Applying", f"Calculate NRV write-down for {co_s}", exp_nrv)

        # 10. Medium Q: Closing Stock Unit Count Verification
        if counts["medium"] < 500:
            c_csu = f"{cl_units:,.0f} units"
            w_csu = [
                f"{tot_u_avail:,.0f} units (total units available)",
                f"{sold_u:,.0f} units (units sold)",
                f"{op_u:,.0f} units (opening stock units only)",
                f"{cl_units + 100:,.0f} units",
                f"{cl_units - 80:,.0f} units",
                f"{cl_units * 1.2:,.0f} units",
                f"{cl_units * 0.8:,.0f} units"
            ]
            q_csu = (f"**{co_s}** had **{tot_u_avail:,.0f} total units** of *{prod_s}* available for sale during the year and recorded sales of **{sold_u:,.0f} units**. "
                     f"How many units should be counted in **closing trading stock** during the year-end physical inventory audit?")
            exp_csu = f"Closing Stock Units = Total Available Units ({tot_u_avail:,.0f}) - Units Sold ({sold_u:,.0f}) = {c_csu}."
            add_q("medium", "Inventory Quantity Auditing", q_csu, c_csu, w_csu, "Applying", f"Calculate closing stock units for {co_s}", exp_csu)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Stock Shrinkage/Theft Analysis, Internal Control, Ethical Scenarios
    # =========================================================================

    shrinkage_cases = [
        ("Protea Audio Ltd", "Wireless Earbuds", 2200, 1850, 290, 85.0, 920.0, "Security guards bypassed: Warehouse staff smuggling small earbud boxes out in personal lunch bags due to lack of physical bag searches at exit turnstiles"),
        ("Kavango Outdoors Ltd", "LED Camping Lanterns", 1600, 1320, 210, 70.0, 480.0, "Collusion with dispatch drivers: Dispatch clerks loading extra cartons into delivery vans without matching goods dispatch notes"),
        ("Algoa Furnishers Ltd", "Ergonomic Desk Lamps", 1400, 1150, 185, 65.0, 620.0, "Broken storehouse window: Perimeter fence damage allowing trespassers access to ground-floor stock holding area"),
        ("Soweto Appliance Mart Ltd", "Blenders & Food Processors", 2800, 2350, 360, 90.0, 750.0, "Unmonitored returns bay: Defective returned items stolen by temporary staff because returns register was not reconciled with physical bins"),
        ("Drakensberg Hardware Ltd", "Toolboxes with Socket Sets", 2100, 1780, 245, 75.0, 890.0, "Open loading docks: Delivery drivers wandering unattended through the warehouse while storemen were at tea breaks"),
        ("Zululand Wholesalers Ltd", "Industrial Extension Reels", 3800, 3250, 450, 100.0, 520.0, "Fictitious damaged stock write-offs: Supervisor signing off on broken stock vouchers for units that were secretly sold for cash"),
        ("Highveld Computech Ltd", "Solid State Hard Drives (1TB)", 1900, 1620, 215, 65.0, 1450.0, "Pocket theft of high-value compact electronics due to lack of metal detectors and CCTV camera blind spots in the packing aisle"),
        ("Karoo Motors Ltd", "High-Intensity Headlight Bulbs", 2400, 2020, 310, 70.0, 420.0, "Unrecorded technician usage: Mechanics taking replacement bulbs directly from open store bins without completing job card requisitions"),
        ("Table Mountain Books Ltd", "Specialty Medical Dictionaries", 3200, 2750, 380, 70.0, 650.0, "Shoplifting by university students due to malfunctioning security electronic EAS sensor tags at bookstore entrance"),
        ("Springbok Sports Mart Ltd", "Professional Match Soccer Balls", 2600, 2180, 340, 80.0, 680.0, "Display stock shrinkage: Balls placed on outdoor promotional sidewalk bins without tether cables or cashier supervision"),
        ("Limpopo Farm Store Ltd", "Veterinary Antibiotic Drenches", 1500, 1260, 190, 50.0, 550.0, "Poison cabinet unlocked: High-value animal medicines stolen because the dispensary keys were left hanging in the office lock"),
        ("Blyde Timber Merchants Ltd", "Tungsten Tipped Saw Blades", 1300, 1080, 175, 45.0, 780.0, "Tool cage access shared by all workers: Missing logbook for tool checkout allowing workers to keep blades upon shift completion"),
        ("Gauteng Health & Beauty Ltd", "Luxury Fragrance Gift Sets", 2500, 2100, 320, 80.0, 1250.0, "Promotional sample pilferage: Sales assistants distributing retail inventory to friends claiming they were tester units"),
        ("Free State Grain Mart Ltd", "Digital Soil pH Testers", 1200, 1010, 155, 35.0, 850.0, "Delivery shortage: Storeman signed delivery note without counting carton contents; supplier delivered 35 fewer units than invoiced"),
        ("Namaqua Diamond Jewelers Ltd", "Sterling Silver Charm Bracelets", 950, 810, 115, 25.0, 2200.0, "Display showcase left unlocked during customer rush hour; lack of dual control on display cabinet keys"),
        ("Outeniqua Garden World Ltd", "Pruning Shears & Loppers", 1800, 1520, 230, 50.0, 480.0, "Garden center outdoor display theft: Customers concealing gardening tools inside large ceramic plant pots at checkout"),
        ("Mpumalanga Tile Center Ltd", "Diamond Tile Drill Bits", 1600, 1340, 210, 50.0, 620.0, "Checkout scanning errors: Cashiers scanning a single unit while allowing contractors to take boxes of five units"),
        ("Ezulwini Homeware Ltd", "Chef Knife Sets (5-piece)", 1700, 1420, 230, 50.0, 950.0, "Concealment in trash bins: Store workers hiding knife boxes in large cardboard refuse dumpsters to retrieve after hours"),
        ("Vaal Triangle Motors Ltd", "OBD2 Bluetooth Diagnostic Scanners", 1400, 1180, 180, 40.0, 1100.0, "Inventory receiving discrepancy: Warehouse clerk failing to cross-check physical pallet count with supplier packing slip"),
        ("Stellenbosch Cellars Ltd", "Reserve Estate Cabernet Sauvignon", 2200, 1860, 280, 60.0, 750.0, "Staff consumption during private evening tastings: Unrecorded bottles uncorked without event management authorization"),
        ("Centurion Office Machines Ltd", "Laser Toner Cartridges", 2800, 2350, 370, 80.0, 850.0, "Clerks swapping new original toner cartridges for counterfeit generic cartridges and selling original stock to outside traders"),
        ("Bloemfontein Grain Merchants Ltd", "Treated Seed Corn Bags (25kg)", 3500, 2950, 460, 90.0, 420.0, "Loading bay gate left unlocked during night shifts; unauthorized farm bakkies loading seed bags without dispatch documentation"),
        ("East London Fishing Gear Ltd", "Carbon Fiber Fishing Rods", 1600, 1340, 210, 50.0, 1250.0, "Rods taken by weekend charter staff for private angling trips and never returned to inventory bins"),
        ("Klerksdorp Mining Supplies Ltd", "Heavy Duty Safety Harnesses", 1850, 1560, 240, 50.0, 980.0, "Mining contractors walking out of the depot wearing new safety harnesses under their coats due to lack of security gate turnstile body searches"),
        ("Potchefstroom Feeds Mart Ltd", "Mineral Lick Blocks", 4200, 3550, 550, 100.0, 160.0, "Rainwater roof leak dissolving salt blocks in bulk store; storeman discarded residue without completing stock write-off vouchers"),
        ("George Hardwood Depot Ltd", "Electric Planers", 1450, 1220, 190, 40.0, 1450.0, "Apprentices stealing planers from open display shelves due to deactivated electronic security tags"),
        ("Secunda Safety Wear Ltd", "Chemical Resistant Respirators", 2100, 1780, 270, 50.0, 780.0, "Contractors taking extra respirator mask packs from open pallets while storekeeper was processing delivery paperwork"),
        ("Vereeniging Boiler Supplies Ltd", "Pressure Relief Valves", 1300, 1090, 170, 40.0, 1850.0, "High-value brass and stainless steel valves stolen by metal scavengers through a loose corrugated iron warehouse wall sheet"),
        ("Welkom Shaft Merchants Ltd", "Pneumatic Rockdrill Hoses", 1750, 1480, 220, 50.0, 820.0, "Unmeasured hose lengths cut for contractors: Storeman estimating hose lengths by eye, giving out 15% extra rubber hose per sale"),
        ("Bethlehem Farmers Coop Ltd", "Electric Fencing Polywire Rolls", 2600, 2200, 340, 60.0, 360.0, "Rolls loaded onto customer bakkies without requiring signed delivery notes at the dispatch bay"),
        ("Newcastle Heavy Hardware Ltd", "Hydraulic Bottle Jacks (10-ton)", 1500, 1260, 195, 45.0, 1150.0, "Warehouse staff wheeling jacks out through the side emergency fire exit door after hours"),
        ("Mossel Bay Marine Traders Ltd", "GPS Chartplotters", 980, 820, 130, 30.0, 4500.0, "Counter theft during busy boat show expo weekend; display models not secured with security wire locks"),
        ("Mthatha Wholesale Hub Ltd", "Commercial Microwave Ovens", 1650, 1390, 215, 45.0, 1350.0, "Dispatch driver colluding with receiving clerk at a local restaurant, dropping off unmanifested microwaves"),
        ("Upington Agro Direct Ltd", "Drip Irrigation Solenoid Valves", 2400, 2040, 310, 50.0, 520.0, "Farmers taking extra valves directly from open bins in the self-service parts section"),
        ("Vryheid Timber Depot Ltd", "Cordless Circular Saws", 1550, 1310, 195, 45.0, 1650.0, "Store workers packing saw boxes inside empty cardboard rubbish bins to retrieve from outdoor dumpsters"),
        ("Ladysmith Fashion Mart Ltd", "Designer Leather Handbags", 1250, 1050, 160, 40.0, 1850.0, "Shoplifting gang using booster bags lined with aluminum foil to block electronic EAS exit alarm gates"),
        ("Bredasdorp Grain Store Ltd", "Digital Grain Thermometers", 1100, 930, 140, 30.0, 890.0, "Stock received short by 30 units from overseas supplier; receiving clerk failed to open outer shipping crate"),
        ("Cradock Livestock Hub Ltd", "Veterinary Dosing Guns", 1400, 1180, 180, 40.0, 680.0, "Sales staff taking dosing guns for demonstration purposes on farms without logging loan register forms"),
        ("Makhanda Scholastic Supplies Ltd", "Scientific Graphing Calculators", 2300, 1950, 290, 60.0, 950.0, "Calculators stolen from stockroom shelves during annual school textbook collection week"),
        ("Oudtshoorn Leathercraft Ltd", "Ostrich Leather Belts", 1950, 1650, 250, 50.0, 850.0, "Boutique sales clerks failing to ring up belt accessories at checkout till points"),
        ("Knysna Marine Woods Ltd", "Marine Teak Deck Planks", 1200, 1010, 155, 35.0, 1400.0, "Pre-cut teak planks loaded onto unauthorized boat builder trailers without security gate passes"),
        ("Standerton Milking Systems Ltd", "Pulsator Valves", 1650, 1390, 215, 45.0, 1120.0, "Service technicians keeping replacement pulsators in field service vans without job card reconciliation"),
        ("Harrismith Logistics Depot Ltd", "Heavy Duty Ratchet Straps", 3200, 2720, 410, 70.0, 280.0, "Truck drivers borrowing tie-down ratchet straps for long-haul trips without returning them to the equipment depot"),
        ("Kuruman Mineral Traders Ltd", "Geological Rock Picks", 1500, 1270, 190, 40.0, 720.0, "Exploration field workers taking hammers home after geological surveying contracts terminated"),
        ("Thohoyandou Superstore Ltd", "Electric Kettles & Toasters", 2800, 2380, 360, 60.0, 340.0, "Customer returns bay pilferage: Working returned appliances taken by night cleaners in refuse bags"),
        ("Plettenberg Bay Decor Ltd", "Velvet Cushion Covers", 2100, 1780, 270, 50.0, 420.0, "Showroom floor theft: Covers removed from display display lounge suites during peak holiday season"),
        ("Saldanha Marine Freight Ltd", "Heavy Mooring Shackles", 1800, 1520, 235, 45.0, 850.0, "Dock workers throwing steel shackles over the harbour security fence into waiting vehicles at midnight"),
        ("Grahamstown Scholastic Ltd", "Microscope Slide Sets", 1600, 1360, 205, 35.0, 580.0, "Specimen boxes dropped and shattered on warehouse concrete floors; discarded without damage vouchers"),
        ("Springbok Wind Parts Ltd", "Anemometer Wind Sensors", 850, 710, 110, 30.0, 3200.0, "Sensors taken from assembly bay by night technicians for unauthorized testing on private wind turbines"),
        ("Witbank Coal Equipment Ltd", "Excavator Grease Cartridges", 3400, 2850, 440, 110.0, 140.0, "Cartridges loaded onto haul trucks without signed store requisition chits"),
        ("Paarl Valley Beverages Ltd", "Stainless Keg Couplers", 1250, 1050, 160, 40.0, 1250.0, "Couplers removed by event caterers during weekend wine festivals without return documentation"),
        ("Centurion Aerospace Parts Ltd", "Precision Rivet Guns", 750, 620, 95, 35.0, 4800.0, "Pneumatic rivet guns removed from tool cribs without biometric scanning checkout logs"),
        ("Bloemfontein Meats Wholesalers Ltd", "Boning Knives (Serrated)", 2100, 1780, 260, 60.0, 380.0, "Abattoir workers taking boning knives home in protective boot linings"),
        ("East London Marine Spares Ltd", "Brass Marine Propellers", 680, 560, 90, 30.0, 3800.0, "Propellers wheeled out through wharf gate in scrap metal recycling containers"),
        ("Klerksdorp Tile Direct Ltd", "Tile Spacers (Bulk Tubs)", 4500, 3800, 580, 120.0, 120.0, "Cashiers giving free tubs of spacers to preferred contractors without scanning barcodes"),
        ("Potchefstroom Stationery Hub Ltd", "Laminating Film Rolls", 1900, 1610, 240, 50.0, 450.0, "Clerks using commercial laminating rolls for private printing side businesses"),
        ("George Home Living Ltd", "LED Vanity Mirrors", 1150, 960, 150, 40.0, 1850.0, "Unmonitored returns bay: Returned mirrors stolen by night security guards"),
        ("Secunda Safety & Industrial Ltd", "Heavy Duty Fall Arrest Blocks", 820, 680, 105, 35.0, 3900.0, "Contractors swapping old worn blocks for brand new units in the warehouse exchange bay"),
        ("Vereeniging Steel Goods Ltd", "Magnetic Base Drill Units", 640, 530, 85, 25.0, 5600.0, "Drill units hidden in delivery bakkie toolboxes without gate release authorization"),
        ("Welkom Mine Supply Ltd", "Underground Cap Lamp Batteries", 1650, 1390, 210, 50.0, 1150.0, "Batteries removed from battery charging racks without supervisor sign-out forms"),
        ("Bethlehem Grain Traders Ltd", "Grain Moisture Calibration Samples", 950, 790, 125, 35.0, 820.0, "Sealed calibration vials broken during warehouse shelf restacking and swept away"),
        ("Newcastle Tool Warehouse Ltd", "Heavy Duty Bench Vices", 880, 730, 115, 35.0, 2400.0, "Vices loaded onto customer bakkies by warehouse loaders receiving direct cash tips"),
        ("Mossel Bay Marine Traders Ltd", "Marine EPIRB Distress Beacons", 540, 450, 70, 20.0, 6500.0, "Distress beacons stolen from marine electronics glass display case during boat show"),
        ("Mthatha Wholesale Hub Ltd", "Commercial Meat Mincers", 720, 600, 95, 25.0, 4200.0, "Receiving clerk colluding with butchery owner to deliver mincers off-invoice"),
        ("Upington Agro Direct Ltd", "Solar Battery Inverter Cables", 1400, 1180, 180, 40.0, 950.0, "Heavy copper cables cut into short lengths and stolen by perimeter wall trespassers"),
        ("Vryheid Timber Depot Ltd", "Laser Level Measuring Kits", 920, 770, 120, 30.0, 2800.0, "Laser measuring kits pocketed by visiting contractors from open service counters"),
        ("Ladysmith Fashion Mart Ltd", "Silk Evening Scarves", 2600, 2190, 340, 70.0, 420.0, "Scarves concealed under customer jackets during busy weekend seasonal clearance sales"),
        ("Bredasdorp Grain Store Ltd", "Electronic Platform Scales", 680, 560, 90, 30.0, 3400.0, "Scales loaned to local sports clubs for weigh-ins and never returned to inventory bins"),
        ("Cradock Livestock Hub Ltd", "Pneumatic Ear Notch Plier Sets", 1150, 960, 150, 40.0, 1250.0, "Demonstration plier sets taken by field livestock agents without loan forms"),
        ("Makhanda Scholastic Supplies Ltd", "Digital Stopwatches (Sets of 10)", 1350, 1130, 175, 45.0, 850.0, "Stopwatch boxes pilfered from sports stockroom shelves during inter-schools athletics week"),
        ("Oudtshoorn Leathercraft Ltd", "Polished Ostrich Egg Ornaments", 1800, 1510, 230, 60.0, 680.0, "Fragile eggs dropped and smashed during pallet restocking; swept away without loss vouchers"),
        ("Knysna Marine Woods Ltd", "Epoxy Resin Kits (5L)", 1100, 920, 145, 35.0, 1650.0, "Resin tins taken by boatyard workers for private weekend dinghy repairs"),
        ("Standerton Milking Systems Ltd", "Stainless Teat Cups", 1750, 1470, 230, 50.0, 680.0, "Service technicians taking spare cups for unregistered weekend cash jobs"),
        ("Harrismith Logistics Depot Ltd", "Corner Edge Protectors", 3800, 3200, 490, 110.0, 85.0, "Plastic edge protectors crushed by forklift wheels on loading ramps and discarded"),
        ("Kuruman Mineral Traders Ltd", "UV Mineral Inspection Lamps", 620, 510, 85, 25.0, 2450.0, "Field geologists failing to return loan lamps upon field contract completion"),
        ("Thohoyandou Superstore Ltd", "Rechargeable Emergency Lanterns", 2100, 1770, 275, 55.0, 480.0, "Cashiers failing to scan lanterns at checkout during electricity load shedding events"),
        ("Plettenberg Bay Decor Ltd", "Brass Curtain Tie-Backs", 1450, 1220, 190, 40.0, 780.0, "Contractors pocketing tie-backs from unmonitored retail accessory display hooks"),
        ("Saldanha Marine Freight Ltd", "Heavy Duty Rigging Slings", 1300, 1090, 170, 40.0, 1850.0, "Crane operators keeping spare rigging slings in private crane tool compartments"),
        ("Grahamstown Scholastic Ltd", "Electronic Balance Calibrators", 740, 610, 105, 25.0, 3200.0, "Calibration weights dropped and dented on stone floors, rendering them uncertified"),
        ("Springbok Wind Parts Ltd", "Rotor Blade Inspection Drones", 320, 260, 45, 15.0, 12500.0, "Maintenance crew crashing a drone into a turbine pylon and hiding the wreckage in the scrap bin"),
        ("Witbank Coal Equipment Ltd", "Heavy Duty Hydraulic O-Ring Kits", 2400, 2020, 310, 70.0, 580.0, "Diesel mechanics taking o-ring kits home for private farm machinery maintenance")
    ]

    for co_sh, prod_sh, avail_sh, sold_sh, act_count, diff_u, cost_u, cause_sh in shrinkage_cases:
        theor_count = avail_sh - sold_sh
        missing_u = theor_count - act_count
        shrink_val = missing_u * cost_u

        # 1. Hard Q: Calculate Trading Stock Deficit Amount
        if counts["hard"] < 200:
            c_sval = f"R{shrink_val:,.2f} ({missing_u:,.0f} units missing/stolen)"
            w_sval = [
                f"R{theor_count * cost_u:,.2f} (valued total theoretical closing stock)",
                f"R{act_count * cost_u:,.2f} (valued actual physical count)",
                f"R{missing_u:,.2f} (omitted unit cost)",
                f"R{shrink_val * 1.2:,.2f}",
                f"R{shrink_val * 0.8:,.2f}",
                f"R{(shrink_val + 25000):,.2f}",
                f"R{(shrink_val - 20000):,.2f}"
            ]
            q_sval = (f"The stock records of **{co_sh}** for *{prod_sh}* indicate that **{avail_sh:,.0f} units** were available for sale "
                      f"and **{sold_sh:,.0f} units** were sold. The year-end physical inventory count revealed only **{act_count:,.0f} units** on hand. "
                      f"The inventory is valued under FIFO at **R{cost_u:.2f}** per unit. "
                      f"Calculate the **financial value of the Trading Stock Deficit (theft/shrinkage)**:")
            exp_sval = (f"Theoretical Closing Stock = Available ({avail_sh:,.0f}) - Sold ({sold_sh:,.0f}) = {theor_count:,.0f} units\n"
                        f"Actual Physical Count = {act_count:,.0f} units\n"
                        f"Deficit (Missing Units) = {theor_count:,.0f} - {act_count:,.0f} = {missing_u:,.0f} units\n"
                        f"Value of Deficit = {missing_u:,.0f} units x R{cost_u:.2f} = {c_sval}.\n"
                        f"This is debited to Trading Stock Deficit (operating expense in Income Statement).")
            add_q("hard", "Trading Stock Deficit & Shrinkage", q_sval, c_sval, w_sval, "Evaluating", f"Calculate stock deficit for {co_sh}", exp_sval)

        # 2. Hard Q: Internal Control & Security Recommendations
        if counts["hard"] < 200:
            c_shc = f"Internal Control Failure: {cause_sh}. Management must enforce physical access controls, CCTV monitoring, segregation of duties, and unannounced stock audits."
            w_shc = [
                "Ignore the stock loss because inventory theft of 10% to 20% is normal in retail commerce",
                "Increase retail selling prices by 35% immediately to force paying customers to cover the theft",
                "Cease conducting physical stock counts at year-end to prevent detecting future deficits",
                "Dismiss all warehouse workers instantly and close down trading operations permanently",
                "Transfer missing stock balances directly to Ordinary Share Capital as a dividend",
                "Stop buying inventory on credit from commercial suppliers"
            ]
            q_shc = (f"Refer to the stock deficit at **{co_sh}** on *{prod_sh}* ({missing_u:,.0f} units missing, value R{shrink_val:,.2f}). "
                     f"Provide the most professional internal control evaluation and management recommendation under CAPS Accounting:")
            exp_shc = f"Evaluation: **{c_shc}**."
            add_q("hard", "Trading Stock Deficit & Shrinkage", q_shc, c_shc, w_shc, "Evaluating", f"Internal control for stock deficit in {co_sh}", exp_shc)

    # Ethical Dilemmas & Governance in Inventory Management (30 cases)
    inv_ethics = [
        ("The store manager instructed the warehouse clerk to alter physical stock count sheets, artificially inflating closing inventory by R1.8 million to lower Cost of Sales and boost reported Net Profit so that executive bonuses would be triggered.",
         "Fraud and financial statement manipulation: Violates IFRS, the Companies Act, and King IV. Inflating closing stock unlawfully increases profit and deceives shareholders, SARS, and lenders. The manager faces criminal fraud charges and dismissal.",
         ["A legitimate accounting adjustment that protects company stock market value on the JSE",
          "Permissible provided the inflated stock is replaced with actual purchases during the first week of next year",
          "An internal administrative matter that falls strictly outside the mandate of the external auditor",
          "Acceptable practice because optimizing profit to pay executive bonuses motivates leadership",
          "Lawful under King IV as creative commercial presentation of working capital",
          "Permissible if the store manager donates 10% of the bonus to a registered children charity"]),

        ("A supermarket manager discovered that R350,000 worth of frozen chicken had thawed due to a 24-hour power outage. Instead of discarding the health hazard, the manager ordered staff to refreeze and repackage the meat with new expiry date stickers.",
         "Criminal endangerment of public health and gross breach of Consumer Protection Act and King IV: Selling rotten food exposes consumers to severe food poisoning and ruins brand reputation, creating massive civil and criminal liability.",
         ["Smart commercial cost recovery that eliminates the need to record a Trading Stock Deficit",
          "Permissible provided the thawed chicken is sold at a 15% discount on the discount clearance rack",
          "Acceptable practice during electricity load shedding because food spoilage cannot be avoided",
          "A routine operational decision that does not require disclosure to the Board Social and Ethics Committee",
          "Lawful provided customers cook the chicken thoroughly at high heat",
          "Permissible if the savings are used to purchase a backup generator for the executive offices"]),

        ("A car dealership financial manager deliberately omitted R4.2 million of floor-plan vehicle stock from the inventory register and failed to record the corresponding commercial bank liability to artificially reduce debt ratios.",
         "Off-balance sheet fraud and non-disclosure: Violates the fundamental accounting principle of faithful representation and Section 29 of the Companies Act, deliberately misleading bank credit analysts.",
         ["Prudent financial planning that improves the solvency ratio and credit rating of the dealership",
          "Permissible because floor-plan vehicles belong to the bank until sold to retail motorists",
          "A minor bookkeeping oversight that can be corrected whenever the dealership chooses to do so",
          "Fully compliant with King IV because reducing recorded liabilities improves shareholder confidence",
          "Lawful practice recognized by South African automotive dealer associations",
          "Acceptable provided the financial manager reports the transaction in personal tax returns"]),

        ("The receiving clerk at an electronics distributor routinely signs Goods Received Notes (GRN) without opening sealed shipping containers or verifying serial numbers, allowing short-shipments of high-end laptops to pass undetected.",
         "Critical failure of receiving internal controls: Neglecting physical verification exposes the company to massive unrecorded supplier short-shipments and fraud. Management must enforce mandatory carton opening and serial barcode scanning.",
         ["Acceptable practice because shipping container seals guarantee that suppliers never make shipping errors",
          "A time-saving logistical procedure that speeds up inventory receiving turnaround times",
          "Permissible provided the supplier is an established corporate enterprise with a good credit rating",
          "Lawful under CAPS because receiving clerks have no legal duty to inspect delivery contents",
          "A minor administrative delay that has zero impact on Cost of Sales or gross profit",
          "Acceptable provided the receiving clerk receives a monthly productivity bonus from the supplier"]),

        ("The purchasing director awarded all trading stock procurement contracts exclusively to an overseas wholesale supplier owned by the director brother at prices 25% above prevailing open-market prices, receiving annual luxury overseas vacations as kickbacks.",
         "Bribery, corruption, and breach of fiduciary duty: Glaring conflict of interest violating Section 75/76 of the Companies Act and King IV Principle 1. The director breached duties of good faith and enriched family members at company expense.",
         ["Smart commercial networking because doing business with family members guarantees supplier loyalty",
          "Permissible under South African company law provided the brother delivers the merchandise on time",
          "A private family matter that does not require disclosure to the board or audit committee",
          "Acceptable corporate practice because foreign suppliers always provide superior product quality",
          "Lawful provided the director pays personal South African income tax on the luxury vacation kickbacks",
          "Permissible if the purchasing director negotiates a 2% volume rebate for the company"]),

        ("A retail clothing chain financial controller deliberately postponed recording supplier invoices of R3.4 million for winter inventory received in May until August, to conceal trade liabilities and artificially inflate reported gross margin at the June interim report.",
         "Cut-off fraud and deliberate misstatement: Violates the accrual principle and IFRS requirement to record purchases when risk and control transfer. Misleads investors and banks analyzing working capital ratios.",
         ["Standard accounting practice to defer expenses until merchandise has been completely sold to shoppers",
          "Permissible provided the supplier agrees verbally to delay sending formal monthly statements",
          "An immaterial timing difference that has zero effect on annual financial statement credibility",
          "Acceptable under King IV as prudent management of short-term reported debt ratios",
          "Lawful because interim financial reports are unaudited and exempt from Companies Act penalties",
          "Permissible if the controller records the invoices in the subsequent quarter"]),

        ("A timber wholesale manager ordered staff to treat termite-infested structural roof trusses with superficial wood stain to conceal boring holes, selling them to an affordable housing contractor at full price.",
         "Reckless commercial fraud and criminal endangerment: Violates SABS building timber standards and Consumer Protection Act, risking structural building collapse and catastrophic loss of human life.",
         ["Prudent inventory realization that recovers capital invested in biological damaged stock",
          "Permissible under CAPS because timber naturally contains minor insect blemishes",
          "A commercial matter between the contractor and the architect rather than an accounting dilemma",
          "Acceptable practice provided the contractor does not explicitly ask about insect treatments",
          "Lawful because housing construction falls strictly under municipal inspectors rather than accountants",
          "Permissible if the manager provides a 5% discount on the next timber purchase"]),

        ("An automotive spare parts manager discovered that 400 imported brake pad sets were counterfeit and failed SABS friction heat tests. The manager refused to scrap them, ordering counter staff to sell them as genuine OEM components.",
         "Counterfeit goods fraud and criminal negligence: Exposes motorists to fatal brake failure, violates the Counterfeit Goods Act and King IV. The company faces immediate criminal prosecution and reputational destruction.",
         ["Smart trading practice that prevents writing down inventory to net realizable value",
          "Acceptable provided the fake brake pads are fitted only to older commercial delivery vehicles",
          "A minor technical variation that falls strictly outside the jurisdiction of financial accountants",
          "Permissible under IFRS if the profit margin earned on the fake parts exceeds 40%",
          "Lawful practice recognized in informal motor mechanic workshop associations",
          "Acceptable if customers are advised verbally to drive at lower speeds"]),

        ("The storekeeper at a hardware emporium routinely accepts damaged paint tins from delivery trucks without noting the dents on the delivery note in exchange for free personal paint supplies from the truck driver.",
         "Employee corruption and breach of internal control: The company is unable to claim credit notes from suppliers for damaged stock, bearing the full financial loss while the employee receives personal kickbacks.",
         ["Good customer service that fosters cordial relations between storekeepers and transport contractors",
          "An informal workplace perk recognized under South African retail trade custom",
          "A minor logistical detail that should be absorbed into Trading Stock Deficit without investigation",
          "Permissible provided the storekeeper paints company store display fixtures using the free paint",
          "Lawful practice under the Basic Conditions of Employment Act",
          "Acceptable provided the supplier eventually replaces the dented tins when convenient"]),

        ("A pharmaceutical warehouse manager sold R850,000 worth of expired pediatric vaccines to an unaccredited private clinic in an adjacent neighbouring country for cash, keeping the proceeds in an unrecorded slush fund.",
         "Criminal trafficking in expired pharmaceuticals, money laundering, and theft: Gross violation of Medicines and Related Substances Act, King IV, and basic human rights, endangering thousands of children.",
         ["Resourceful revenue generation that converts worthless expired inventory into liquid cash",
          "Permissible because foreign healthcare clinics operate under their own sovereign legal jurisdiction",
          "An off-book transaction that benefits the company by avoiding hazardous medical waste disposal costs",
          "Acceptable practice provided the slush fund is used to purchase staff Christmas party hampers",
          "A commercial marketing strategy actively encouraged by multinational pharmaceutical firms",
          "Lawful provided the cash proceeds are deposited in a commercial bank account within 30 days"]),

        ("During an annual inventory audit, the external auditors selected a sample of 50 high-value power generators for physical counting. The warehouse manager arranged for 20 generators to be counted in Aisle 4, then rapidly moved them to Aisle 12 while the auditors were at lunch so they were counted twice.",
         "Deliberate audit fraud and obstruction: Falsifying inventory quantities to deceive external auditors is a serious criminal offence under Section 214 of the Companies Act, leading to immediate audit qualification or adverse opinion.",
         ["Clever logistical coordination that helps external auditors complete stock counts ahead of schedule",
          "Acceptable audit assistance practice recognized by the South African Institute of Chartered Accountants",
          "A routine operational efficiency that prevents holding up normal commercial warehouse dispatches",
          "Permissible provided the generators are actually owned by the company on the balance sheet date",
          "An administrative issue that should be resolved by buying the audit team coffee and doughnuts",
          "Lawful because double counting balances out other inventory items that might have been missed"]),

        ("A warehouse manager falsified Goods Returned Notes, pretending that R600,000 of obsolete fashion stock was returned to suppliers for full credit, when in reality the goods were dumped in an abandoned quarry.",
         "Fraudulent asset derecognition and illegal dumping: Deliberately conceals inventory obsolescence from the Income Statement, breaches environmental waste bylaws, and misstates Trade Payables.",
         ["Creative stock liquidation that cleans up warehouse storage aisles efficiently",
          "Permissible provided the dumped clothing is eventually covered with topsoil",
          "An informal accounting adjustment recognized under local commercial retail custom",
          "Acceptable under King IV as pragmatic management of slow-moving inventory balances",
          "Lawful because suppliers rarely verify returned goods records older than 60 days",
          "Permissible if the manager donates R5,000 to a local community recycling initiative"]),

        ("A food distribution supervisor relabelled 5,000 tins of canned baby formula that had expired six months prior, selling them to rural crèches at full retail price to avoid recording an inventory write-off.",
         "Heinous criminal endangerment of infant health, gross violation of Foodstuffs, Cosmetics and Disinfectants Act, and utter failure of King IV ethics: Exposes vulnerable infants to malnutrition and disease.",
         ["Resourceful inventory salvage that prevents recording a loss on the trading statement",
          "Permissible provided the formula tins show no external signs of bulging or rust",
          "A minor technical expiration issue that has zero practical health significance",
          "Acceptable practice because rural crèches face severe food budget constraints",
          "Lawful under the Companies Act because baby food is non-perishable canned merchandise",
          "Permissible if the supervisor provides free baby porridge with every ten tins purchased"]),

        ("The logistics director established an undisclosed side transport company registered in his daughter name, charging the main company 40% above market freight rates for carriage on purchases of trading stock.",
         "Undisclosed related-party transaction and self-dealing: Severe breach of Section 75 of the Companies Act and King IV Principle 1. The director siphoned corporate cash into a family entity and inflated inventory costs.",
         ["Commendable family business entrepreneurship that keeps logistics spending within the family circle",
          "Permissible provided the daughter company owns roadworthy transport trucks",
          "An administrative matter that falls strictly outside the jurisdiction of corporate governance",
          "Acceptable because family transport contractors guarantee dedicated delivery schedules",
          "Lawful provided the director reports the income on personal income tax filings",
          "Permissible if the daughter offers a 2% prompt settlement discount to the company"]),

        ("A building supply depot manager secretly swapped 1,000 bags of SABS-certified 42.5N structural cement for uncertified sub-grade 22.5X masonry cement, pocketing the R120,000 price difference in cash.",
         "Theft, substitution fraud, and criminal compromise of structural building safety: High-strength concrete structures built with this sub-grade cement risk catastrophic collapse, leading to multiple manslaughter charges.",
         ["Shrewd inventory arbitrage that maximizes gross margin on building supply merchandise",
          "Acceptable practice provided the cement is used only for single-storey residential walls",
          "A minor quality variation that has zero relevance to financial accounting ledgers",
          "Permissible under IFRS if the cash difference is used to maintain warehouse forklift trucks",
          "Lawful practice recognized among informal building material traders",
          "Acceptable provided the cement bags look physically identical to retail customers"]),

        ("An inventory accountant noticed that R2.5 million of stock was lost to employee theft over the year. To conceal the loss from the Board of Directors, the accountant spread the missing amount across Cost of Sales as an unrecorded price increase.",
         "Falsification of accounting records and concealment of internal control breakdown: Violates Section 28 of the Companies Act and King IV, deliberately hiding severe theft vulnerabilities from the Audit Committee.",
         ["Prudent accounting smoothing that prevents alarming company directors unnecessarily",
          "A professional presentation technique that keeps financial statements looking orderly",
          "Permissible because Cost of Sales absorbs all inventory movements under periodic systems",
          "Acceptable practice because reporting theft causes unnecessary friction with warehouse unions",
          "Lawful under IFRS as general manufacturing overhead absorption",
          "Permissible if the accountant identifies the culprits within the subsequent 12 months"]),

        ("A luxury car dealership manager allowed VIP clients to drive demo vehicle inventory for personal holiday trips over December without insurance cover or hire contracts, resulting in two vehicles being totaled in accidents.",
         "Reckless asset mismanagement and unauthorized asset use: Violates internal asset protection policies and King IV, exposing the business to R3 million in uninsured losses and legal claims.",
         ["Excellent customer relationship marketing that builds VIP brand loyalty",
          "Permissible provided the VIP clients promise to buy a car in the new year",
          "A routine promotional activity that requires no formal documentation or board review",
          "Acceptable practice because demo vehicles are already depreciated on the asset register",
          "Lawful under the Consumer Protection Act as extended test-driving rights",
          "Permissible if the clients pay for their own petrol during the holiday trips"]),

        ("A wholesale wine merchant blended 10,000 litres of cheap box wine into premium cultivar bottled reserve wines, selling them at R450 per bottle to overseas export markets.",
         "Export wine fraud and violation of Wine of Origin (WO) legislation: Damages the international reputation of the South African wine industry and constitutes criminal consumer deceit under King IV.",
         ["Smart product blending that maximizes export revenue and foreign currency earnings",
          "Permissible provided international wine connoisseurs cannot taste the difference",
          "A traditional winemaking blending technique recognized under global trade custom",
          "Acceptable because wine tasting is subjective and has no legal definition under IFRS",
          "Lawful provided the company pays full excise duties to the South African Revenue Service",
          "Permissible if the company donates 5% of export profits to farm worker housing"]),

        ("A chemical distributor storekeeper stored 50 drums of volatile industrial solvent directly next to electrical heating panels in a non-ventilated warehouse to save on outdoor bonded storage rent, resulting in a flash fire that destroyed an entire commercial block.",
         "Criminal negligence and violation of Occupational Health and Safety Act and National Environmental Management Act: Gross failure of risk management and duty of care under King IV Principle 11.",
         ["Unavoidable industrial mishap that has zero connection to managerial responsibility",
          "Smart cost-saving storage optimization that minimized monthly rental overheads",
          "Acceptable practice during winter months to keep solvents at ambient temperature",
          "A municipal fire department issue that does not concern corporate accounting directors",
          "Lawful provided the chemical drums were sealed with plastic screw caps",
          "Permissible if the commercial insurance policy covers fire and smoke damage"])
    ]

    for sc_ie, corr_ie, wrongs_ie in inv_ethics:
        if counts["hard"] < 200:
            q_ie1 = f"**Inventory Control & Corporate Governance Dilemma**:\n\n*\"{sc_ie}\"*\n\nProvide the most professional evaluation under CAPS Accounting standards and the King IV Code:"
            exp_ie1 = f"Evaluation: **{corr_ie}**."
            add_q("hard", "Inventory Internal Control & Governance", q_ie1, corr_ie, wrongs_ie, "Evaluating", "Evaluate inventory governance dilemma", exp_ie1)

        if counts["hard"] < 200:
            q_ie2 = f"Identify the primary internal control measure required to prevent the following inventory malpractice:\n\n*\"{sc_ie}\"*"
            c_ic = "Enforce segregation of duties, mandatory physical verification, independent surprise audits, and strict conflict of interest declarations as required by King IV."
            w_ic = [
                "Abolish all inventory counting procedures and rely solely on supplier invoice estimates",
                "Triple the selling price of goods to ensure all inventory losses are recovered from customers",
                "Prohibit employees from taking annual leave or communicating with external auditors",
                "Cease using pre-numbered Goods Received Notes and purchase requisitions",
                "Allow department managers to destroy accounting records after 30 days",
                "Eliminate internal audit committees and transfer oversight to casual workers"
            ]
            exp_ic = f"Correct Control Measure: **{c_ic}**."
            add_q("hard", "Inventory Internal Control & Governance", q_ie2, c_ic, w_ic, "Evaluating", "Identify internal control measure for inventory", exp_ic)

    print(f"Generated: easy={counts['easy']}, medium={counts['medium']}, hard={counts['hard']}")

    output_path = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting/paper2_acc_inventory.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"SUCCESS: {output_path} created with {len(questions)} questions: {counts}")

if __name__ == "__main__":
    build_inventory()
