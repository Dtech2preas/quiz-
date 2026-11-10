import json
import os

def build_manufacturing():
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
        qid = f"ACC_P2_MFG_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Cost Accounting (Manufacturing)",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": "Cost Accounting (Manufacturing)",
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

    core_definitions = [
        ("Direct Materials",
         "Raw materials that become an integral part of the finished product and can be directly and conveniently traced to each unit produced",
         "Cleaning chemicals and lubricants used on factory machinery",
         "Office stationery used by accounting personnel in administration",
         "Delivery packaging materials used in the finished goods sales dispatch bay",
         "Protective clothing and overalls worn by factory safety supervisors",
         "Maintenance spare parts stored for emergency conveyor belt repairs",
         "Printer cartridges used in the marketing director's office"),

        ("Direct Labour",
         "The wages and employer contributions paid to production line workers who physically manufacture or assemble the finished goods",
         "The salary paid to the factory general manager and safety inspector",
         "The commission paid to sales representatives travelling across provinces",
         "The fee paid to external registered auditors at the financial year-end",
         "The wages paid to head office cleaners and boardroom caterers",
         "The wages paid to forklift drivers operating in the finished goods warehouse",
         "The monthly retainer fee paid to legal consultants on labour disputes"),

        ("Factory Overheads",
         "All indirect manufacturing costs incurred inside the factory building other than direct material and direct labour",
         "All operating expenses incurred in the head office administration building",
         "The advertising and delivery expenses incurred to sell finished products to retailers",
         "The total interest paid on long-term bank loans and mortgage debentures",
         "The dividends declared and paid to registered ordinary company shareholders",
         "The corporate income tax paid directly to the South African Revenue Service",
         "The direct raw materials issued from the storehouse to the cutting department"),

        ("Prime Cost",
         "The sum of Direct Material Cost and Direct Labour Cost",
         "The sum of Factory Overheads and Administration Costs",
         "The Total Cost of Production divided by total units produced",
         "The difference between total sales revenue and total variable costs",
         "The sum of Direct Labour Cost and Factory Overhead Cost",
         "The total selling and distribution expenses incurred during the financial period",
         "The opening balance of work-in-process plus carriage on purchases"),

        ("Work-in-Process (WIP)",
         "Partially manufactured goods that are still on the production line undergoing processing at the beginning or end of an accounting period",
         "Completed finished goods stored in the showroom waiting for customer collection",
         "Raw materials delivered by suppliers that have not yet been inspected or unpacked",
         "Damaged and unsellable goods written off as manufacturing scrap",
         "Office furniture and computers installed in the administrative boardroom",
         "Delivery vehicles in transit transporting merchandise between regional warehouses",
         "Advertising brochures printed by commercial marketing agencies"),

        ("Fixed Costs",
         "Operating costs that remain unchanged in total within a relevant range of production regardless of fluctuations in production volume",
         "Costs that increase or decrease in direct proportion to changes in production output",
         "Costs that vary unpredictably depending on daily currency exchange rate fluctuations",
         "Costs that are incurred only when factory workers work overtime on public holidays",
         "Expenses paid exclusively in cash on the first day of every trading month",
         "Costs that are refunded by the South African Revenue Service upon submission of VAT returns",
         "Expenses that must be approved directly by ordinary shareholders at the AGM"),

        ("Variable Costs",
         "Costs that change in total in direct proportion to the volume of units produced or manufactured",
         "Costs that stay exactly constant in total amount no matter how many units are produced",
         "Administrative salaries paid to permanent corporate office executives",
         "Annual factory building insurance premiums fixed by commercial insurance underwriters",
         "Municipal property rates and taxes levied on the factory land and buildings",
         "Depreciation on factory machinery calculated on the straight-line method",
         "Fixed monthly rental paid for leasing the factory premises"),

        ("Break-Even Point (BEP)",
         "The production and sales volume at which total revenue equals total costs, resulting in neither profit nor loss",
         "The maximum production capacity that factory machinery can physically achieve in 24 hours",
         "The point where variable cost per unit equals fixed cost per unit",
         "The minimum selling price at which goods must be sold to cover administrative salaries",
         "The level of inventory at which a new purchase order must be placed with suppliers",
         "The volume of sales required to pay a 15% dividend return to ordinary shareholders",
         "The point where total assets equal total liabilities in the balance sheet"),

        ("Margin of Safety",
         "The excess of actual or budgeted production/sales volume over the break-even volume, showing how far sales can drop before incurring a loss",
         "The percentage markup applied to total cost of production to establish selling price",
         "The mandatory cash reserve required by commercial banks before approving overdrafts",
         "The minimum raw material stock maintained in the warehouse to prevent factory shutdowns",
         "The statutory insurance coverage required under the Occupational Health and Safety Act",
         "The difference between authorized share capital and issued ordinary share capital",
         "The total depreciation accumulated on factory plant and equipment since purchase"),

        ("Carriage on Purchases of Raw Materials",
         "Transport costs incurred to deliver raw materials from the supplier's warehouse to the factory, which form part of Direct Material Cost",
         "Delivery costs to transport completed finished goods to retail customers",
         "Fuel expenses incurred by administrative sales representatives visiting trade expos",
         "Maintenance charges for servicing factory forklift vehicles",
         "Storage rent paid for housing excess finished inventory in regional depots",
         "Import duties paid on importing administrative executive office desks",
         "Demurrage fees paid to shipping lines for delayed container dispatch")
    ]

    for title_d, corr_d, *wrongs_d in core_definitions:
        q_def = f"In Grade 12 Cost and Management Accounting (Paper 2), what is the correct definition of **{title_d}**?"
        exp_def = f"**{title_d}**: {corr_d}. This is a fundamental concept in CAPS Grade 12 Manufacturing Accounting."
        add_q("easy", "Cost Concepts & Classifications", q_def, corr_d, wrongs_d, "Remembering", f"Define {title_d}", exp_def)

        q_rev = f"Which manufacturing accounting term is defined as: *\"{corr_d}\"*?"
        clean_terms = [
            "Indirect Manufacturing Consumables", "Finished Goods Inventory",
            "Opportunity Cost", "Sunk Cost Allocation", "Administrative Overhead",
            "Debtors Allowance Factor", "Operating Leverage Coefficient"
        ]
        exp_rev = f"The definition describes **{title_d}**. {corr_d}."
        add_q("easy", "Cost Concepts & Classifications", q_rev, title_d, clean_terms, "Understanding", f"Identify {title_d}", exp_rev)

    class_items = [
        ("Fabric used in manufacturing school uniforms", "Direct Material Cost", ["Factory Overhead Cost", "Administration Cost", "Selling and Distribution Cost", "Indirect Material Cost", "Financial Cost", "Non-operating Cost"]),
        ("Wages paid to machine operators sewing uniforms", "Direct Labour Cost", ["Factory Overhead Cost", "Administration Cost", "Selling and Distribution Cost", "Indirect Labour Cost", "Fixed Period Cost", "Administrative Expense"]),
        ("Salary of the factory cleaning supervisor", "Factory Overhead Cost", ["Direct Labour Cost", "Direct Material Cost", "Selling and Distribution Cost", "Administration Cost", "Prime Cost", "Distribution Expense"]),
        ("Thread and buttons used in clothing manufacturing where tracing per garment is not practical", "Factory Overhead Cost (Indirect Material)", ["Direct Material Cost", "Prime Cost", "Selling and Distribution Cost", "Administration Cost", "Direct Labour Cost", "Capital Expenditure"]),
        ("Depreciation on factory sewing machines", "Factory Overhead Cost", ["Direct Material Cost", "Administration Cost", "Selling and Distribution Cost", "Direct Labour Cost", "Prime Cost", "Current Asset"]),
        ("Electricity bill for factory production machinery", "Factory Overhead Cost", ["Administration Cost", "Selling and Distribution Cost", "Direct Material Cost", "Direct Labour Cost", "Prime Cost", "Capital Asset"]),
        ("Commission paid to sales representatives on uniform sales", "Selling and Distribution Cost", ["Factory Overhead Cost", "Direct Labour Cost", "Direct Material Cost", "Administration Cost", "Prime Cost", "Work-in-Process"]),
        ("Salary of the Managing Director in the head office", "Administration Cost", ["Factory Overhead Cost", "Direct Labour Cost", "Selling and Distribution Cost", "Prime Cost", "Direct Material Cost", "Work-in-Process"]),
        ("Timber and pine wood used to manufacture dining tables", "Direct Material Cost", ["Factory Overhead Cost", "Selling and Distribution Cost", "Administration Cost", "Indirect Material Cost", "Capital Asset", "Finished Goods"]),
        ("Wages of carpenters assembling dining tables", "Direct Labour Cost", ["Factory Overhead Cost", "Administration Cost", "Selling and Distribution Cost", "Indirect Labour Cost", "Administration Expense", "Fixed Overhead"]),
        ("Glue and sandpaper used in furniture manufacturing", "Factory Overhead Cost (Indirect Material)", ["Direct Material Cost", "Direct Labour Cost", "Prime Cost", "Selling and Distribution Cost", "Administration Cost", "Finished Goods"]),
        ("Delivery vehicle fuel delivering furniture to buyers", "Selling and Distribution Cost", ["Factory Overhead Cost", "Direct Material Cost", "Administration Cost", "Direct Labour Cost", "Prime Cost", "Work-in-Process"]),
        ("Leather used to manufacture safety boots", "Direct Material Cost", ["Factory Overhead Cost", "Selling and Distribution Cost", "Administration Cost", "Indirect Material Cost", "Prime Cost", "Finished Goods"]),
        ("Wages of shoemakers cutting and stitching leather boots", "Direct Labour Cost", ["Factory Overhead Cost", "Administration Cost", "Selling and Distribution Cost", "Indirect Labour Cost", "Administration Expense", "Fixed Overhead"]),
        ("Rent of the factory building", "Factory Overhead Cost", ["Administration Cost", "Selling and Distribution Cost", "Direct Material Cost", "Direct Labour Cost", "Prime Cost", "Current Asset"]),
        ("Audit fees paid to external auditors", "Administration Cost", ["Factory Overhead Cost", "Selling and Distribution Cost", "Direct Labour Cost", "Direct Material Cost", "Prime Cost", "Work-in-Process"]),
        ("Advertising campaign on regional radio stations", "Selling and Distribution Cost", ["Factory Overhead Cost", "Administration Cost", "Direct Labour Cost", "Direct Material Cost", "Prime Cost", "Work-in-Process"]),
        ("Oranges and sugar used to manufacture fruit juice", "Direct Material Cost", ["Factory Overhead Cost", "Selling and Distribution Cost", "Administration Cost", "Indirect Material Cost", "Finished Goods", "Capital Expenditure"]),
        ("Wages of bottling plant operators", "Direct Labour Cost", ["Factory Overhead Cost", "Administration Cost", "Selling and Distribution Cost", "Indirect Labour Cost", "Prime Cost", "Work-in-Process"]),
        ("Lubricants and grease for juice packaging machines", "Factory Overhead Cost (Indirect Material)", ["Direct Material Cost", "Direct Labour Cost", "Selling and Distribution Cost", "Administration Cost", "Prime Cost", "Finished Goods"])
    ]

    for item_desc, correct_cat, wrong_cats in class_items:
        q_cl = f"How should the cost of **'{item_desc}'** be classified in a manufacturing business?"
        exp_cl = f"**{item_desc}** is classified as **{correct_cat}**. In CAPS manufacturing accounting, costs incurred on the factory floor are split into direct materials, direct labour, and factory overheads."
        add_q("easy", "Cost Concepts & Classifications", q_cl, correct_cat, wrong_cats, "Understanding", "Classify manufacturing cost items", exp_cl)

    # 70 South African manufacturing enterprises for Easy Calculations (70 x 4 = 280 Qs)
    calc_easy_mfg = [
        ("Mzansi Footwear Ltd", 650000.0, 420000.0, 280000.0, 10000),
        ("Kavango Apparel Ltd", 880000.0, 560000.0, 340000.0, 15000),
        ("Protea Furniture Ltd", 1250000.0, 780000.0, 520000.0, 8000),
        ("Soweto Bakeries Ltd", 450000.0, 310000.0, 190000.0, 50000),
        ("Algoa Solar Panels Ltd", 1850000.0, 920000.0, 680000.0, 4000),
        ("Drakensberg Juices Ltd", 720000.0, 410000.0, 260000.0, 20000),
        ("Zululand Paper Mills Ltd", 1400000.0, 850000.0, 590000.0, 12000),
        ("Highveld Steel Doors Ltd", 960000.0, 640000.0, 430000.0, 6000),
        ("Karoo Leather Goods Ltd", 580000.0, 390000.0, 240000.0, 7500),
        ("Table Mountain Teas Ltd", 510000.0, 320000.0, 210000.0, 25000),
        ("Springbok Sports Gear Ltd", 820000.0, 530000.0, 350000.0, 14000),
        ("Limpopo Brickworks Ltd", 690000.0, 470000.0, 310000.0, 30000),
        ("Blyde Valley Packaging Ltd", 740000.0, 460000.0, 290000.0, 18000),
        ("Gauteng Medical Supplies Ltd", 1600000.0, 980000.0, 640000.0, 9000),
        ("Free State Grain Mills Ltd", 1100000.0, 620000.0, 410000.0, 22000),
        ("Namaqua Ceramics Ltd", 490000.0, 340000.0, 220000.0, 11000),
        ("Outeniqua Timber Crafts Ltd", 890000.0, 580000.0, 380000.0, 8500),
        ("Mpumalanga Fertilizer Ltd", 1750000.0, 950000.0, 670000.0, 16000),
        ("Ezulwini Glassware Ltd", 630000.0, 420000.0, 270000.0, 13000),
        ("Vaal Triangle Plastics Ltd", 1350000.0, 790000.0, 530000.0, 17500),
        ("Stellenbosch Barrels Ltd", 780000.0, 490000.0, 320000.0, 5500),
        ("Tshwane Auto Components Ltd", 1950000.0, 1150000.0, 760000.0, 7000),
        ("Richards Bay Wire Ltd", 1220000.0, 730000.0, 490000.0, 9500),
        ("Polokwane Feeds Ltd", 870000.0, 540000.0, 360000.0, 21000),
        ("Kimberley Tools Ltd", 1050000.0, 680000.0, 440000.0, 8200),
        ("Durban Detergents Ltd", 920000.0, 580000.0, 370000.0, 24000),
        ("Rustenburg Foundry Ltd", 2100000.0, 1280000.0, 840000.0, 6500),
        ("Witbank Cables Ltd", 1480000.0, 890000.0, 580000.0, 11500),
        ("Paarl Canneries Ltd", 990000.0, 610000.0, 400000.0, 19000),
        ("Midrand Electronics Ltd", 2300000.0, 1350000.0, 890000.0, 5000),
        ("Centurion Composites Ltd", 1550000.0, 910000.0, 600000.0, 6200),
        ("Bloemfontein Meat Packers Ltd", 1680000.0, 990000.0, 660000.0, 14500),
        ("East London Marine Eng Ltd", 1820000.0, 1080000.0, 710000.0, 4800),
        ("Klerksdorp Cement Works Ltd", 1190000.0, 740000.0, 480000.0, 28000),
        ("Potchefstroom Dairy Ltd", 810000.0, 510000.0, 330000.0, 26000),
        ("George Woodworks Ltd", 940000.0, 590000.0, 390000.0, 9200),
        ("Secunda Polymers Ltd", 2250000.0, 1320000.0, 880000.0, 13500),
        ("Vereeniging Boiler Works Ltd", 2050000.0, 1210000.0, 810000.0, 3800),
        ("Welkom Rockdrills Ltd", 1390000.0, 830000.0, 540000.0, 7200),
        ("Bethlehem Dairy Co Ltd", 760000.0, 480000.0, 310000.0, 23000),
        ("Newcastle Heavy Steels Ltd", 1980000.0, 1180000.0, 790000.0, 8200),
        ("Mossel Bay Nets Ltd", 1250000.0, 760000.0, 510000.0, 1800),
        ("Mthatha Timber Supplies Ltd", 830000.0, 510000.0, 340000.0, 5200),
        ("Upington Sun Agro Ltd", 1090000.0, 670000.0, 430000.0, 26000),
        ("Vryheid Coal Pellets Ltd", 1320000.0, 780000.0, 510000.0, 34000),
        ("Ladysmith Textiles Ltd", 1140000.0, 680000.0, 440000.0, 15500),
        ("Bredasdorp Wheat Mills Ltd", 1220000.0, 710000.0, 470000.0, 31000),
        ("Cradock Merinos Ltd", 910000.0, 560000.0, 360000.0, 12500),
        ("Makhanda Print Works Ltd", 950000.0, 580000.0, 380000.0, 44000),
        ("Oudtshoorn Leathers Ltd", 1120000.0, 670000.0, 440000.0, 6200),
        ("Knysna Fine Yachts Ltd", 1450000.0, 890000.0, 580000.0, 850),
        ("Standerton Dairy Co Ltd", 840000.0, 520000.0, 340000.0, 25000),
        ("Harrismith Logistics Pack Ltd", 1020000.0, 630000.0, 410000.0, 16000),
        ("Kuruman Foundry Ltd", 1750000.0, 1050000.0, 690000.0, 7200),
        ("Thohoyandou Mills Ltd", 790000.0, 490000.0, 320000.0, 22000),
        ("Plettenberg Bay Timber Ltd", 1160000.0, 710000.0, 460000.0, 6400),
        ("Saldanha Shiprepair Ltd", 2150000.0, 1290000.0, 850000.0, 2800),
        ("Grahamstown Pottery Ltd", 680000.0, 430000.0, 280000.0, 12000),
        ("Springbok Solar Inverters Ltd", 1650000.0, 990000.0, 650000.0, 4500),
        ("Witbank Refractory Ltd", 1520000.0, 920000.0, 610000.0, 8800),
        ("Paarl Wine Oak Ltd", 1040000.0, 640000.0, 420000.0, 3800),
        ("Durban Container Depot Ltd", 1380000.0, 840000.0, 550000.0, 9200),
        ("Rustenburg Smelter Spares Ltd", 1880000.0, 1140000.0, 750000.0, 5400),
        ("Cape West Fish Processors Ltd", 980000.0, 610000.0, 390000.0, 21000),
        ("Highveld Industrial Gases Ltd", 1420000.0, 860000.0, 570000.0, 11000),
        ("Zululand Timber Poles Ltd", 1260000.0, 770000.0, 500000.0, 14000),
        ("Algoa Marine Paints Ltd", 890000.0, 550000.0, 360000.0, 19500),
        ("Karoo Renewable Equipment Ltd", 1720000.0, 1040000.0, 680000.0, 5100),
        ("Tshwane Electric Motors Ltd", 1920000.0, 1160000.0, 770000.0, 6800),
        ("Midrand Data Cabinets Ltd", 1460000.0, 880000.0, 580000.0, 7600)
    ]

    for co_m, dm_v, dl_v, foh_v, units_v in calc_easy_mfg:
        # 1. Prime Cost
        prime_c = dm_v + dl_v
        c_p = f"R{prime_c:,.2f}"
        w_p = [
            f"R{dm_v + foh_v:,.2f} (added direct material and factory overheads)",
            f"R{dl_v + foh_v:,.2f} (added direct labour and factory overheads)",
            f"R{dm_v + dl_v + foh_v:,.2f} (calculated total cost of production instead of prime cost)",
            f"R{prime_c * 1.15:,.2f}",
            f"R{prime_c * 0.85:,.2f}",
            f"R{dm_v:,.2f} (omitted direct labour)",
            f"R{(prime_c + 150000):,.2f}"
        ]
        q_p = (f"The records of **{co_m}** indicate Direct Material Cost of **R{dm_v:,.2f}** and Direct Labour Cost of **R{dl_v:,.2f}**. "
               f"Calculate the **Prime Cost**:")
        exp_p = f"Prime Cost = Direct Material Cost + Direct Labour Cost = R{dm_v:,.2f} + R{dl_v:,.2f} = {c_p}."
        add_q("easy", "Prime Cost & Cost of Production", q_p, c_p, w_p, "Applying", f"Calculate prime cost for {co_m}", exp_p)

        # 2. Total Cost of Production
        tot_cop = dm_v + dl_v + foh_v
        c_tcp = f"R{tot_cop:,.2f}"
        w_tcp = [
            f"R{prime_c:,.2f} (omitted factory overheads: prime cost only)",
            f"R{tot_cop * 1.2:,.2f}",
            f"R{tot_cop * 0.8:,.2f}",
            f"R{dm_v + foh_v:,.2f}",
            f"R{dl_v + foh_v:,.2f}",
            f"R{(tot_cop + 200000):,.2f}",
            f"R{(tot_cop - 180000):,.2f}"
        ]
        q_tcp = (f"For the financial year ended 28 February, **{co_m}** incurred Direct Materials of **R{dm_v:,.2f}**, Direct Labour of **R{dl_v:,.2f}**, "
                 f"and Factory Overheads of **R{foh_v:,.2f}**. There were no work-in-process balances. Calculate the **Total Cost of Production**:")
        exp_tcp = f"Total Cost of Production = Prime Cost + Factory Overheads = (R{dm_v:,.2f} + R{dl_v:,.2f}) + R{foh_v:,.2f} = {c_tcp}."
        add_q("easy", "Prime Cost & Cost of Production", q_tcp, c_tcp, w_tcp, "Applying", f"Calculate total cost of production for {co_m}", exp_tcp)

        # 3. Unit Cost of Production
        unit_c = tot_cop / units_v
        c_uc = f"R{unit_c:.2f}"
        w_uc = [
            f"R{prime_c / units_v:.2f} (calculated unit prime cost: omitted factory overheads)",
            f"R{dm_v / units_v:.2f} (unit direct material cost only)",
            f"R{dl_v / units_v:.2f} (unit direct labour cost only)",
            f"R{unit_c * 1.25:.2f}",
            f"R{unit_c * 0.75:.2f}",
            f"R{(unit_c + 15.00):.2f}",
            f"R{(unit_c - 10.00):.2f}"
        ]
        q_uc = (f"**{co_m}** produced **{units_v:,.0f} units** during the financial year. The Total Cost of Production was **R{tot_cop:,.2f}**. "
                f"Calculate the **Unit Cost of Production** per unit:")
        exp_uc = f"Unit Cost of Production = Total Cost of Production / Units Produced = R{tot_cop:,.2f} / {units_v:,.0f} = {c_uc} per unit."
        add_q("easy", "Unit Cost of Production", q_uc, c_uc, w_uc, "Applying", f"Calculate unit cost of production for {co_m}", exp_uc)

        # 4. Direct Material Issued to Production
        op_mat = dm_v * 0.15
        cl_mat = dm_v * 0.20
        carr = dm_v * 0.05
        purch = dm_v - op_mat - carr + cl_mat
        c_dmiss = f"R{dm_v:,.2f}"
        w_dmiss = [
            f"R{purch:,.2f} (used net purchases only: omitted opening and closing inventory adjustments)",
            f"R{op_mat + purch + carr:,.2f} (forgot to deduct closing inventory of raw materials)",
            f"R{op_mat + purch + cl_mat:,.2f} (omitted carriage on purchases)",
            f"R{dm_v * 1.15:,.2f}",
            f"R{dm_v * 0.85:,.2f}",
            f"R{(dm_v + 60000):,.2f}",
            f"R{(dm_v - 50000):,.2f}"
        ]
        q_dmiss = (f"Calculate the **Direct Material Cost issued to production** for **{co_m}** from the following data:\n"
                   f"- Opening stock of raw materials: **R{op_mat:,.2f}**\n"
                   f"- Purchases of raw materials: **R{purch:,.2f}**\n"
                   f"- Carriage on purchases: **R{carr:,.2f}**\n"
                   f"- Closing stock of raw materials: **R{cl_mat:,.2f}**")
        exp_dmiss = (f"Direct Material Cost = Opening Stock + Purchases + Carriage on Purchases - Closing Stock\n"
                     f"= R{op_mat:,.2f} + R{purch:,.2f} + R{carr:,.2f} - R{cl_mat:,.2f} = {c_dmiss}.")
        add_q("easy", "Direct Material Cost Note", q_dmiss, c_dmiss, w_dmiss, "Applying", f"Calculate direct materials issued for {co_m}", exp_dmiss)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # =========================================================================

    mfg_scenarios = [
        ("Protea Footwear Ltd", "Leather School Shoes", 12000, 720000.0, 480000.0, 360000.0, 45000.0, 35000.0, 220.0, 420000.0, 110.0),
        ("Kavango Garments Ltd", "Protective Overalls", 18000, 1080000.0, 630000.0, 450000.0, 60000.0, 48000.0, 180.0, 520000.0, 95.0),
        ("Algoa Furniture Ltd", "Office Desks", 6500, 1430000.0, 780000.0, 520000.0, 85000.0, 65000.0, 650.0, 680000.0, 360.0),
        ("Soweto Bakery Ltd", "Specialty Bread Loaves", 60000, 540000.0, 360000.0, 240000.0, 25000.0, 15000.0, 28.0, 310000.0, 16.0),
        ("Drakensberg Beverages Ltd", "Bottled Fruit Juices", 35000, 840000.0, 490000.0, 350000.0, 40000.0, 30000.0, 65.0, 450000.0, 38.0),
        ("Zululand Paper Works Ltd", "Cardboard Packaging Boxes", 25000, 1250000.0, 750000.0, 500000.0, 70000.0, 55000.0, 140.0, 620000.0, 85.0),
        ("Highveld Steel Doors Ltd", "Security Gate Units", 4500, 1125000.0, 675000.0, 450000.0, 90000.0, 72000.0, 850.0, 580000.0, 440.0),
        ("Karoo Leathercraft Ltd", "Saddle Bags", 5000, 650000.0, 400000.0, 280000.0, 35000.0, 25000.0, 420.0, 360000.0, 230.0),
        ("Table Mountain Teas Ltd", "Herbal Tea Cartons", 40000, 640000.0, 380000.0, 260000.0, 30000.0, 22000.0, 50.0, 340000.0, 28.0),
        ("Springbok Sports Ltd", "Rugby Balls", 15000, 900000.0, 540000.0, 360000.0, 50000.0, 38000.0, 185.0, 460000.0, 105.0),
        ("Limpopo Brickworks Ltd", "Facing Bricks (Packs of 100)", 22000, 880000.0, 550000.0, 380000.0, 45000.0, 35000.0, 130.0, 480000.0, 72.0),
        ("Blyde Timber Mills Ltd", "Pine Dining Tables", 4000, 1200000.0, 680000.0, 460000.0, 80000.0, 60000.0, 950.0, 590000.0, 510.0),
        ("Gauteng Meditech Ltd", "Surgical Gauze Rolls", 30000, 1500000.0, 840000.0, 570000.0, 65000.0, 50000.0, 125.0, 720000.0, 82.0),
        ("Free State Grain Mills Ltd", "Maize Flour Bags (10kg)", 28000, 1260000.0, 672000.0, 448000.0, 55000.0, 42000.0, 115.0, 560000.0, 74.0),
        ("Namaqua Pottery Ltd", "Ceramic Floor Tiles (Boxes)", 16000, 720000.0, 448000.0, 304000.0, 40000.0, 32000.0, 145.0, 390000.0, 80.0),
        ("Outeniqua Crafts Ltd", "Garden Benches", 3500, 945000.0, 560000.0, 385000.0, 60000.0, 45000.0, 880.0, 490000.0, 470.0),
        ("Mpumalanga Fertilizers Ltd", "Crop Nutrition Bags (50kg)", 20000, 1800000.0, 960000.0, 640000.0, 85000.0, 65000.0, 240.0, 780000.0, 145.0),
        ("Ezulwini Ceramics Ltd", "Dinnerware Sets", 7000, 840000.0, 525000.0, 350000.0, 48000.0, 36000.0, 360.0, 440000.0, 210.0),
        ("Vaal Polymer Pipes Ltd", "Irrigation Piping (Coils)", 11000, 1430000.0, 792000.0, 528000.0, 75000.0, 58000.0, 340.0, 660000.0, 215.0),
        ("Stellenbosch Oak Ltd", "Wine Storage Casks", 2800, 1120000.0, 672000.0, 448000.0, 95000.0, 75000.0, 1250.0, 570000.0, 710.0),
        ("Tshwane Radiators Ltd", "Automotive Radiators", 8500, 1870000.0, 1020000.0, 680000.0, 90000.0, 70000.0, 580.0, 840000.0, 380.0),
        ("Richards Bay Alloys Ltd", "Aluminum Window Frames", 9000, 1350000.0, 765000.0, 510000.0, 65000.0, 50000.0, 390.0, 640000.0, 245.0),
        ("Polokwane Feeds Ltd", "Poultry Feed Bags (25kg)", 32000, 1120000.0, 640000.0, 416000.0, 50000.0, 38000.0, 95.0, 520000.0, 60.0),
        ("Kimberley Tools Ltd", "Mining Shovels", 14000, 1190000.0, 714000.0, 476000.0, 60000.0, 46000.0, 240.0, 580000.0, 150.0),
        ("Durban Soaps Ltd", "Hygiene Soap Bars (Cartons)", 45000, 1125000.0, 675000.0, 450000.0, 55000.0, 40000.0, 75.0, 540000.0, 46.0),
        ("Rustenburg Foundry Ltd", "Cast Iron Manhole Covers", 5500, 1925000.0, 1100000.0, 742500.0, 110000.0, 85000.0, 980.0, 890000.0, 600.0),
        ("Witbank Electrics Ltd", "Industrial Extension Cables", 13000, 1560000.0, 884000.0, 585000.0, 75000.0, 58000.0, 320.0, 710000.0, 210.0),
        ("Paarl Preserves Ltd", "Canned Peaches (Cartons)", 24000, 1080000.0, 624000.0, 408000.0, 48000.0, 36000.0, 120.0, 490000.0, 76.0),
        ("Midrand Circuits Ltd", "Electronic Power Supplies", 8000, 2160000.0, 1200000.0, 800000.0, 105000.0, 80000.0, 780.0, 960000.0, 465.0),
        ("Centurion Composites Ltd", "Fiberglass Boat Hulls", 1200, 1800000.0, 1020000.0, 696000.0, 140000.0, 110000.0, 4500.0, 850000.0, 2650.0),
        ("Bloemfontein Meats Ltd", "Vacuum-Packed Biltong (Packs)", 38000, 1710000.0, 950000.0, 627000.0, 65000.0, 50000.0, 110.0, 750000.0, 74.0),
        ("East London Boatcraft Ltd", "Kayak Canoes", 2200, 1210000.0, 704000.0, 473000.0, 70000.0, 52000.0, 1650.0, 560000.0, 1050.0),
        ("Klerksdorp Cement Works Ltd", "Cement Bags (50kg)", 42000, 1470000.0, 840000.0, 546000.0, 60000.0, 45000.0, 92.0, 640000.0, 60.0),
        ("Potchefstroom Dairy Ltd", "Cheddar Cheese Blocks (kg)", 19000, 988000.0, 589000.0, 389500.0, 45000.0, 34000.0, 145.0, 470000.0, 96.0),
        ("George Furniture Ltd", "Oak Coffee Tables", 4800, 1152000.0, 672000.0, 456000.0, 72000.0, 55000.0, 720.0, 540000.0, 435.0),
        ("Secunda Polymers Ltd", "Heavy-Duty Plastic Crates", 17000, 2210000.0, 1241000.0, 816000.0, 95000.0, 72000.0, 380.0, 980000.0, 245.0),
        ("Vereeniging Boilers Ltd", "Pressure Vessels", 1500, 1875000.0, 1080000.0, 720000.0, 125000.0, 95000.0, 3400.0, 870000.0, 2250.0),
        ("Welkom Drills Ltd", "Jackhammer Drill Bits", 9500, 1425000.0, 807500.0, 541500.0, 68000.0, 52000.0, 410.0, 650000.0, 260.0),
        ("Bethlehem Dairy Co Ltd", "Full Cream Milk (6x2L packs)", 36000, 864000.0, 504000.0, 331200.0, 40000.0, 30000.0, 70.0, 410000.0, 45.0),
        ("Newcastle Forge Ltd", "Railway Sleepers & Spikes", 8200, 1722000.0, 984000.0, 656000.0, 88000.0, 68000.0, 560.0, 790000.0, 370.0),
        ("Mossel Bay Nets Ltd", "Commercial Trawler Nets", 1800, 1350000.0, 774000.0, 522000.0, 80000.0, 62000.0, 2100.0, 610000.0, 1350.0),
        ("Mthatha Timber Supplies Ltd", "School Study Desks", 5200, 780000.0, 468000.0, 312000.0, 45000.0, 34000.0, 440.0, 380000.0, 280.0),
        ("Upington Sun Agro Ltd", "Dried Sultanas (Cartons)", 26000, 1170000.0, 676000.0, 442000.0, 52000.0, 39000.0, 115.0, 530000.0, 75.0),
        ("Vryheid Coal Pellets Ltd", "Smokeless Fuel Briquettes (Bags)", 34000, 1360000.0, 782000.0, 510000.0, 62000.0, 46000.0, 98.0, 610000.0, 63.0),
        ("Ladysmith Textiles Ltd", "Hospital Bed Sheets (Sets)", 15500, 1085000.0, 635500.0, 418500.0, 54000.0, 40000.0, 195.0, 510000.0, 118.0),
        ("Bredasdorp Wheat Mills Ltd", "Cake Flour (12.5kg)", 31000, 1240000.0, 713000.0, 465000.0, 58000.0, 44000.0, 105.0, 560000.0, 68.0),
        ("Cradock Merinos Ltd", "Spun Knitting Yarn (Hanks)", 12500, 937500.0, 550000.0, 362500.0, 46000.0, 35000.0, 210.0, 440000.0, 135.0),
        ("Makhanda Print Works Ltd", "Standard Exercise Books (Packs)", 44000, 968000.0, 572000.0, 374000.0, 42000.0, 32000.0, 62.0, 450000.0, 41.0),
        ("Oudtshoorn Leathers Ltd", "Ostrich Leather Wallets", 6200, 1178000.0, 682000.0, 452600.0, 64000.0, 48000.0, 520.0, 530000.0, 335.0),
        ("Knysna Fine Yachts Ltd", "Rowing Skiffs", 850, 1530000.0, 884000.0, 595000.0, 120000.0, 92000.0, 5200.0, 710000.0, 3100.0)
    ]

    for co_s, prod, units_s, dm_s, dl_s, foh_s, wip_b, wip_e, sp_s, tfc_s, vc_s in mfg_scenarios:
        prime_s = dm_s + dl_s
        tot_mfg_costs = prime_s + foh_s
        cop_fg = tot_mfg_costs + wip_b - wip_e
        unit_cop = cop_fg / units_s

        marg_inc = sp_s - vc_s
        bep_units = tfc_s / marg_inc
        mos_units = units_s - bep_units

        # 1. Medium Q: Total Cost of Production of Finished Goods
        if counts["medium"] < 500:
            c_cop_fg = f"R{cop_fg:,.2f}"
            w_cop_fg = [
                f"R{tot_mfg_costs:,.2f} (omitted work-in-process adjustments)",
                f"R{tot_mfg_costs - wip_b + wip_e:,.2f} (deducted opening WIP and added closing WIP)",
                f"R{prime_s + wip_b - wip_e:,.2f} (omitted factory overheads)",
                f"R{cop_fg * 1.15:,.2f}",
                f"R{cop_fg * 0.85:,.2f}",
                f"R{(cop_fg + 100000):,.2f}",
                f"R{(cop_fg - 100000):,.2f}"
            ]
            q_cop_fg = (f"The following manufacturing costs relate to **{co_s}** for the production of *{prod}*:\n"
                        f"- Direct Material Cost: **R{dm_s:,.2f}**\n"
                        f"- Direct Labour Cost: **R{dl_s:,.2f}**\n"
                        f"- Factory Overheads: **R{foh_s:,.2f}**\n"
                        f"- Work-in-Process at beginning of year: **R{wip_b:,.2f}**\n"
                        f"- Work-in-Process at end of year: **R{wip_e:,.2f}**\n"
                        f"Calculate the **Cost of Production of Finished Goods** to be transferred to the Trading Statement:")
            exp_cop_fg = (f"Cost of Production of Finished Goods = Prime Cost (R{prime_s:,.2f}) + Factory Overheads (R{foh_s:,.2f}) "
                          f"+ Opening WIP (R{wip_b:,.2f}) - Closing WIP (R{wip_e:,.2f})\n"
                          f"= R{tot_mfg_costs:,.2f} + R{wip_b:,.2f} - R{wip_e:,.2f} = {c_cop_fg}.")
            add_q("medium", "Production Cost Statement", q_cop_fg, c_cop_fg, w_cop_fg, "Applying", f"Calculate cost of finished goods for {co_s}", exp_cop_fg)

        # 2. Medium Q: Unit Cost of Finished Goods Produced
        if counts["medium"] < 500:
            c_uc_fg = f"R{unit_cop:.2f}"
            w_uc_fg = [
                f"R{tot_mfg_costs / units_s:.2f} (calculated without WIP adjustment)",
                f"R{prime_s / units_s:.2f} (unit prime cost only)",
                f"R{dm_s / units_s:.2f} (unit direct materials only)",
                f"R{unit_cop * 1.25:.2f}",
                f"R{unit_cop * 0.75:.2f}",
                f"R{(unit_cop + 25.00):.2f}",
                f"R{(unit_cop - 18.00):.2f}"
            ]
            q_uc_fg = (f"**{co_s}** completed **{units_s:,.0f} units** of *{prod}*. The Cost of Production of Finished Goods was **R{cop_fg:,.2f}**. "
                       f"Calculate the **unit cost of production** per finished unit:")
            exp_uc_fg = f"Unit Cost of Production = Cost of Production of Finished Goods / Units Produced = R{cop_fg:,.2f} / {units_s:,.0f} = {c_uc_fg} per unit."
            add_q("medium", "Production Cost Statement", q_uc_fg, c_uc_fg, w_uc_fg, "Applying", f"Calculate unit cost of finished goods for {co_s}", exp_uc_fg)

        # 3. Medium Q: Break-Even Point in Units
        if counts["medium"] < 500:
            c_bep = f"{bep_units:,.0f} units"
            w_bep = [
                f"{tfc_s / sp_s:,.0f} units (divided fixed costs by selling price only: omitted variable costs)",
                f"{tfc_s / vc_s:,.0f} units (divided fixed costs by variable costs only)",
                f"{(tfc_s + (vc_s * units_s)) / sp_s:,.0f} units",
                f"{bep_units * 1.2:,.0f} units",
                f"{bep_units * 0.8:,.0f} units",
                f"{bep_units + 1200:,.0f} units",
                f"{bep_units - 800:,.0f} units"
            ]
            q_bep = (f"**{co_s}** sells *{prod}* at a selling price of **R{sp_s:.2f}** per unit. "
                     f"Variable costs are **R{vc_s:.2f}** per unit and Total Fixed Costs amount to **R{tfc_s:,.2f}**. "
                     f"Calculate the **Break-Even Point in units**:")
            exp_bep = (f"Break-Even Point = Total Fixed Costs / (Selling Price - Variable Cost per unit)\n"
                       f"= R{tfc_s:,.2f} / (R{sp_s:.2f} - R{vc_s:.2f})\n"
                       f"= R{tfc_s:,.2f} / R{marg_inc:.2f} = {c_bep}.")
            add_q("medium", "Break-Even Analysis", q_bep, c_bep, w_bep, "Applying", f"Calculate break-even units for {co_s}", exp_bep)

        # 4. Medium Q: Margin of Safety in Units
        if counts["medium"] < 500:
            c_mos = f"{mos_units:,.0f} units"
            w_mos = [
                f"{bep_units:,.0f} units (confused with break-even point)",
                f"{units_s:,.0f} units (used actual production volume)",
                f"{units_s + bep_units:,.0f} units (added actual units and BEP units)",
                f"{mos_units * 1.2:,.0f} units",
                f"{mos_units * 0.8:,.0f} units",
                f"{mos_units + 1500:,.0f} units",
                f"{mos_units - 1200:,.0f} units"
            ]
            q_mos = (f"**{co_s}** produced and sold **{units_s:,.0f} units** of *{prod}*. The calculated break-even point is **{bep_units:,.0f} units**. "
                     f"Calculate the **Margin of Safety in units**:")
            exp_mos = (f"Margin of Safety = Actual/Budgeted Sales Units - Break-Even Units\n"
                       f"= {units_s:,.0f} - {bep_units:,.0f} = {c_mos}. "
                       f"This represents the cushion of safety before the firm begins to make a trading loss.")
            add_q("medium", "Break-Even Analysis", q_mos, c_mos, w_mos, "Applying", f"Calculate margin of safety for {co_s}", exp_mos)

        # 5. Medium Q: Factory Overhead Allocation by Floor Space
        tot_rent = 160000.0 + (foh_s * 0.2)
        fact_pct = 75
        fact_rent = tot_rent * (fact_pct / 100)
        if counts["medium"] < 500:
            c_fr = f"R{fact_rent:,.2f}"
            w_fr = [
                f"R{tot_rent:,.2f} (allocated 100% of rent to factory)",
                f"R{tot_rent * 0.15:,.2f} (allocated administrative share of rent)",
                f"R{tot_rent * 0.10:,.2f} (allocated sales share of rent)",
                f"R{fact_rent * 1.2:,.2f}",
                f"R{fact_rent * 0.8:,.2f}",
                f"R{(fact_rent + 25000):,.2f}",
                f"R{(fact_rent - 20000):,.2f}"
            ]
            q_fr = (f"**{co_s}** pays total rent of **R{tot_rent:,.2f}** for the combined business premises. "
                    f"The premises have a total floor area of 2,000 square metres, occupied as follows:\n"
                    f"- Factory production floor: 1,500 m² (75%)\n"
                    f"- Administrative offices: 300 m² (15%)\n"
                    f"- Sales showroom: 200 m² (10%)\n"
                    f"Calculate the amount of rent to be allocated to **Factory Overheads** (Note 3):")
            exp_fr = (f"Factory Overhead Rent = Total Rent x (Factory Area / Total Area) = R{tot_rent:,.2f} x 75% = {c_fr}.\n"
                      f"Only costs incurred directly in the manufacturing section form part of factory overheads.")
            add_q("medium", "Factory Overhead Allocation", q_fr, c_fr, w_fr, "Applying", f"Calculate factory rent allocation for {co_s}", exp_fr)

        # 6. Medium Q: Cost of Finished Goods Sold
        op_fg = cop_fg * 0.12
        cl_fg = cop_fg * 0.15
        cogs = op_fg + cop_fg - cl_fg
        if counts["medium"] < 500:
            c_cogs = f"R{cogs:,.2f}"
            w_cogs = [
                f"R{cop_fg:,.2f} (used cost of production without finished goods inventory adjustments)",
                f"R{op_fg + cop_fg + cl_fg:,.2f} (added closing finished goods instead of deducting)",
                f"R{cop_fg - op_fg + cl_fg:,.2f}",
                f"R{cogs * 1.15:,.2f}",
                f"R{cogs * 0.85:,.2f}",
                f"R{(cogs + 80000):,.2f}",
                f"R{(cogs - 70000):,.2f}"
            ]
            q_cogs = (f"Calculate the **Cost of Finished Goods Sold** for **{co_s}**:\n"
                      f"- Finished Goods at beginning: **R{op_fg:,.2f}**\n"
                      f"- Cost of Production of Finished Goods for the year: **R{cop_fg:,.2f}**\n"
                      f"- Finished Goods at end of year: **R{cl_fg:,.2f}**")
            exp_cogs = (f"Cost of Finished Goods Sold = Opening Finished Goods + Cost of Production - Closing Finished Goods\n"
                        f"= R{op_fg:,.2f} + R{cop_fg:,.2f} - R{cl_fg:,.2f} = {c_cogs}.")
            add_q("medium", "Cost of Finished Goods Sold", q_cogs, c_cogs, w_cogs, "Applying", f"Calculate cost of finished goods sold for {co_s}", exp_cogs)

        # 7. Medium Q: Direct Labour Cost with Contributions
        basic_wages = dl_s / 1.08
        uif_c = basic_wages * 0.01
        sdl_c = basic_wages * 0.01
        pension_c = basic_wages * 0.06
        if counts["medium"] < 500:
            c_dl_tot = f"R{dl_s:,.2f}"
            w_dl_tot = [
                f"R{basic_wages:,.2f} (basic wages only: omitted employer contributions)",
                f"R{basic_wages + uif_c:,.2f} (included UIF only)",
                f"R{basic_wages + pension_c:,.2f} (included pension only)",
                f"R{dl_s * 1.2:,.2f}",
                f"R{dl_s * 0.8:,.2f}",
                f"R{(dl_s + 45000):,.2f}",
                f"R{(dl_s - 35000):,.2f}"
            ]
            q_dl_tot = (f"The factory wage records of **{co_s}** show the following for machine operators:\n"
                        f"- Gross Basic Wages: **R{basic_wages:,.2f}**\n"
                        f"- Employer UIF contribution (1%): **R{uif_c:,.2f}**\n"
                        f"- Employer Skills Development Levy (1%): **R{sdl_c:,.2f}**\n"
                        f"- Employer Pension Fund contribution (6%): **R{pension_c:,.2f}**\n"
                        f"Calculate the total **Direct Labour Cost** to be entered into the Production Cost Statement:")
            exp_dl_tot = (f"Total Direct Labour Cost = Gross Wages + Employer Contributions (UIF + SDL + Pension)\n"
                          f"= R{basic_wages:,.2f} + R{uif_c:,.2f} + R{sdl_c:,.2f} + R{pension_c:,.2f} = {c_dl_tot}.\n"
                          f"Under CAPS, all direct factory labour employment costs incurred by the employer form part of Direct Labour Cost.")
            add_q("medium", "Direct Labour Cost Note", q_dl_tot, c_dl_tot, w_dl_tot, "Applying", f"Calculate direct labour total for {co_s}", exp_dl_tot)

        # 8. Medium Q: Contribution Margin per unit
        if counts["medium"] < 500:
            c_cm = f"R{marg_inc:.2f}"
            w_cm = [
                f"R{sp_s:.2f} (selling price only)",
                f"R{vc_s:.2f} (variable cost only)",
                f"R{sp_s + vc_s:.2f} (added selling price and variable cost)",
                f"R{marg_inc * 1.2:.2f}",
                f"R{marg_inc * 0.8:.2f}",
                f"R{(marg_inc + 10.00):.2f}",
                f"R{(marg_inc - 8.00):.2f}"
            ]
            q_cm = (f"**{co_s}** sells *{prod}* for **R{sp_s:.2f}** each, incurring variable manufacturing and selling costs of **R{vc_s:.2f}** per unit. "
                    f"Calculate the **Marginal Income (Contribution Margin) per unit**:")
            exp_cm = f"Marginal Income per unit = Selling Price per unit - Variable Cost per unit = R{sp_s:.2f} - R{vc_s:.2f} = {c_cm}."
            add_q("medium", "Break-Even Analysis", q_cm, c_cm, w_cm, "Applying", f"Calculate contribution margin for {co_s}", exp_cm)

        # 9. Medium Q: Break-Even Point Evaluation
        if counts["medium"] < 500:
            bep_eval = "The business is operating profitably and safely because actual production exceeds the break-even point" if units_s > bep_units else "The business is operating at a net loss because production is below break-even"
            c_be_ev = bep_eval
            w_be_ev = [
                "The business should immediately cease operations because the break-even point is greater than zero",
                "The business should reduce selling price by 50% to increase production volume",
                "Break-even analysis has no relevance to operational viability under King IV",
                "The business is breaking even exactly with zero margin of safety",
                "Fixed costs should be transferred to trade debtors to artificially increase profitability",
                "The business must double variable cost per unit to achieve financial equilibrium"
            ]
            q_be_ev = (f"**{co_s}** produced and sold **{units_s:,.0f} units** of *{prod}*, while its break-even point was calculated as **{bep_units:,.0f} units**. "
                       f"Which statement best evaluates the **operational viability** of the enterprise?")
            exp_be_ev = f"Evaluation: **{c_be_ev}**. With actual production of {units_s:,.0f} units vs BEP of {bep_units:,.0f} units, Margin of Safety is {mos_units:,.0f} units."
            add_q("medium", "Break-Even Analysis", q_be_ev, c_be_ev, w_be_ev, "Analyzing", f"Evaluate break-even viability for {co_s}", exp_be_ev)

        # 10. Medium Q: Factory Indirect Materials Consumed
        op_ind = foh_s * 0.08
        cl_ind = foh_s * 0.06
        purch_ind = foh_s * 0.20
        used_ind = op_ind + purch_ind - cl_ind
        if counts["medium"] < 500:
            c_ind = f"R{used_ind:,.2f}"
            w_ind = [
                f"R{purch_ind:,.2f} (used purchases only without inventory adjustments)",
                f"R{op_ind + purch_ind + cl_ind:,.2f} (added closing stock)",
                f"R{used_ind * 1.2:,.2f}",
                f"R{used_ind * 0.8:,.2f}",
                f"R{(used_ind + 15000):,.2f}",
                f"R{(used_ind - 12000):,.2f}",
                f"R{op_ind + purch_ind:,.2f}"
            ]
            q_ind = (f"Calculate the **Indirect Materials (Factory Consumables) consumed** for **{co_s}**:\n"
                     f"- Opening stock of consumables: **R{op_ind:,.2f}**\n"
                     f"- Purchases of factory consumables: **R{purch_ind:,.2f}**\n"
                     f"- Closing stock of consumables: **R{cl_ind:,.2f}**")
            exp_ind = (f"Factory Consumables Used = Opening Stock + Purchases - Closing Stock\n"
                       f"= R{op_ind:,.2f} + R{purch_ind:,.2f} - R{cl_ind:,.2f} = {c_ind}. "
                       f"This forms part of Factory Overhead Cost.")
            add_q("medium", "Factory Overhead Allocation", q_ind, c_ind, w_ind, "Applying", f"Calculate consumables used for {co_s}", exp_ind)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Wastage Analysis, Labour Productivity, Make-or-Buy Decisions
    # =========================================================================

    wastage_cases = [
        ("Protea Clothing Ltd", "School Blazers", 8000, 2.5, 3.1, 95.0, "Machinists lack training in computer-assisted cutting, resulting in excessive off-cut fabric scraps and poor layout efficiency"),
        ("Kavango Leather Ltd", "Executive Briefcases", 4500, 1.8, 2.3, 160.0, "Substandard leather hides with numerous natural blemishes and knife cuts received from the tannery supplier"),
        ("Algoa Woodworks Ltd", "Wooden Dining Chairs", 6000, 4.0, 4.8, 85.0, "Faulty saw blade calibration and improper wood seasoning causing extensive splitting and timber wastage"),
        ("Soweto Pastries Ltd", "Commercial Wedding Cakes", 3500, 3.5, 4.2, 55.0, "Over-mixing ingredients and defective temperature sensors on commercial ovens leading to burnt batches"),
        ("Drakensberg Solar Ltd", "Solar Collector Panels", 2800, 6.0, 7.2, 220.0, "Manual soldering errors cracking photovoltaic wafer cells during shift changes"),
        ("Zululand Pack Ltd", "Corrugated Shipping Cartons", 18000, 1.2, 1.5, 30.0, "Outdated die-cutting machine shearing carton edges inaccurately without automated tension sensors"),
        ("Highveld Gates Ltd", "Security Fencing Panels", 5000, 8.5, 10.0, 110.0, "Excessive steel off-cuts due to standard 6m pipe lengths not aligning with panel dimensions"),
        ("Karoo Footwear Ltd", "Veldskoen Boots", 7500, 1.5, 1.9, 140.0, "Inexperienced casual workers cutting leather without standardized pattern templates"),
        ("Table Mountain Teas Ltd", "Herbal Infusion Pouches", 25000, 0.25, 0.32, 45.0, "Poor seal temperature calibration on high-speed tea bagging machinery causing powder spillage"),
        ("Springbok Balls Ltd", "Match Soccer Balls", 12000, 0.8, 1.05, 90.0, "Defective synthetic polyurethane panels tearing during machine stitching"),
        ("Limpopo Pottery Ltd", "Architectural Clay Urns", 4200, 5.0, 6.2, 65.0, "Inadequate drying time before kiln firing causing thermal shock and structural cracking"),
        ("Blyde Valley Timber Ltd", "Hardwood Doors", 3600, 7.0, 8.5, 150.0, "Operator error during computerized routing leading to misaligned lock mortise cavities"),
        ("Gauteng Textiles Ltd", "Hospital Scrub Uniforms", 14000, 2.2, 2.7, 75.0, "Fabric flaws and colour shading inconsistencies requiring whole roll rejections"),
        ("Free State Feeds Ltd", "Mineral Lick Blocks", 15000, 10.0, 11.5, 35.0, "High humidity in storage warehouse causing salt block crumbling prior to automated packaging"),
        ("Namaqua Tiles Ltd", "Porcelain Wall Tiles", 9000, 3.0, 3.6, 70.0, "Inconsistent hydraulic press pressure creating hairline cracks during conveyor transport"),
        ("Outeniqua Woodcraft Ltd", "Picnic Table Sets", 2400, 12.0, 14.5, 95.0, "Unseasoned damp timber warping after cross-cutting, rendering planks unusable"),
        ("Mpumalanga Chem Ltd", "Industrial Disinfectant Drums", 8500, 25.0, 29.0, 40.0, "Pipe leakage and valve weeping during chemical mixing and tank transfer"),
        ("Ezulwini Glass Ltd", "Tumbler Glass Sets", 11000, 1.4, 1.8, 50.0, "Molten glass viscosity fluctuations causing uneven wall thickness and shatter rejections"),
        ("Vaal Pipes Ltd", "Drainage Pipes", 6500, 15.0, 18.0, 80.0, "Extrusion temperature overheating causing plastic deformation and wall blistering"),
        ("Stellenbosch Cooperage Ltd", "Wine Barrels", 1600, 20.0, 24.5, 210.0, "Oak stave cracking during steam bending due to rushing the cooperage heating cycle"),
        ("Tshwane Auto Ltd", "Exhaust Silencers", 5800, 6.5, 7.8, 130.0, "Robotic welding head misalignment piercing sheet metal tubes"),
        ("Richards Bay Wire Ltd", "Diamond Mesh Fencing", 7200, 18.0, 21.5, 48.0, "Wire tensile strength failure during high-speed automated weaving loom cycles"),
        ("Polokwane Agri Feeds Ltd", "Dairy Cattle Feed (Bags)", 21000, 50.0, 54.0, 22.0, "Sack tearing on loading ramps due to sharp conveyor protrusions"),
        ("Kimberley Mining Gear Ltd", "Safety Hardhats", 16000, 0.45, 0.58, 60.0, "Polycarbonate pellet moisture contamination causing bubble formation in injection mould cavities"),
        ("Durban Detergent Works Ltd", "Liquid Bleach Bottles", 32000, 1.05, 1.25, 25.0, "Bottle capping machine overtightening and splitting plastic container necks"),
        ("Centurion Aerospace Parts Ltd", "Carbon Fiber Winglets", 1500, 4.2, 5.1, 380.0, "Autoclave temperature vacuum bag leakage causing resin voids and structural scrapping"),
        ("Bloemfontein Milling Hub Ltd", "Semolina Flour Packs", 26000, 1.0, 1.18, 18.0, "Vibrating sifter screen tear spilling bran particles into refined flour hoppers"),
        ("East London Shipchandlers Ltd", "Nylon Mooring Hawsers", 3200, 15.0, 17.8, 85.0, "Twisting machine bobbin friction burn severing high-tensile core filaments"),
        ("Klerksdorp Lime Ltd", "Agricultural Lime (Bags)", 38000, 25.0, 27.5, 14.0, "Paper sack burst during automated robotic pallet wrapping"),
        ("Potchefstroom Yoghurt Ltd", "Cultured Milk Tubs", 45000, 0.50, 0.62, 16.0, "Foil heat-sealing head misalignment causing dairy batch contamination rejections"),
        ("George Cedarcraft Ltd", "Garden Loungers", 2900, 8.5, 10.2, 115.0, "Cross-grain tearout on four-sided planer due to blunt cutter knives"),
        ("Secunda Resins Ltd", "Polyethylene Pallets", 8400, 12.0, 14.2, 65.0, "Purging waste during polymer colour changeovers without recovery granulators"),
        ("Vereeniging Castings Ltd", "Impeller Pumps", 2200, 16.0, 19.5, 145.0, "Sand mould collapse during grey iron pouring creating surface porosity defects"),
        ("Welkom Core Bits Ltd", "Diamond Core Drill Tips", 6800, 0.35, 0.46, 260.0, "Induction brazing overheating oxidizing synthetic diamond segments"),
        ("Bethlehem Cheese Co Ltd", "Gouda Rounds (5kg)", 7500, 50.0, 58.0, 32.0, "Whey drainage failure causing high moisture acidity and rind splitting"),
        ("Newcastle Heavy Barrels Ltd", "Steel Shipping Drums", 9200, 14.0, 16.5, 75.0, "Seam-rolling wheel wear leading to hydraulic pressure leak rejections"),
        ("Mossel Bay Fish Meal Ltd", "High-Protein Pellets", 28000, 20.0, 22.8, 26.0, "Steam dryer scorching causing charred particle rejections"),
        ("Mthatha School Furniture Ltd", "Steel Desk Frames", 6400, 5.5, 6.7, 68.0, "Bending machine clamp slippage causing angle distortion and tubing buckling"),
        ("Upington Sun Raisins Ltd", "Seedless Golden Raisins", 31000, 1.0, 1.20, 35.0, "Optical laser sorter air jet misfire ejecting premium sound fruit with stems"),
        ("Vryheid Briquettes Ltd", "Charcoal Logs (5kg)", 42000, 5.0, 5.8, 12.0, "Binder mixture inconsistency causing briquette crumbling in packaging bins"),
        ("Ladysmith Curtains Ltd", "Blackout Drapes", 8600, 6.0, 7.3, 85.0, "Pattern repeat mismatch during manual cutting requiring fabric panel replacement"),
        ("Bredasdorp Barley Works Ltd", "Malted Barley (Sacks)", 24000, 25.0, 27.6, 22.0, "Kiln air duct blockage causing uneven grain germination and malt scorching"),
        ("Cradock Leather Saddles Ltd", "Riding Saddles", 1400, 12.0, 15.0, 240.0, "Irregular hide thickness and brand scarring causing leather piece rejection"),
        ("Makhanda Bookbinding Ltd", "Hardcover School Atlases", 18500, 0.90, 1.12, 42.0, "Guillotine blade dulling tearing coated paper folios during three-knife trimming"),
        ("Oudtshoorn Feathercraft Ltd", "Feather Dusters", 12500, 0.20, 0.27, 55.0, "Handle socket splitting during automated wooden dowel insertion"),
        ("Knysna Timber Floors Ltd", "Engineered Oak Planks", 5400, 3.5, 4.3, 135.0, "Adhesive press cold spots causing top veneer delamination"),
        ("Standerton Milking Systems Ltd", "Stainless Steel Pails", 4800, 4.5, 5.4, 110.0, "Deep-drawing hydraulic press wrinkle formation due to inadequate lubrication"),
        ("Harrismith Tarpaulins Ltd", "PVC Truck Covers", 3600, 22.0, 26.2, 78.0, "High-frequency plastic welder dielectric breakdown burning PVC fabric sheets"),
        ("Kuruman Crushers Ltd", "Manganese Screen Liners", 3100, 30.0, 35.5, 160.0, "Gas cutting torch nozzle clogging creating irregular slag edges requiring grinding"),
        ("Thohoyandou Oilseed Ltd", "Pressed Sunflower Oil", 23000, 3.2, 3.9, 28.0, "Screw press filter cloth tearing allowing meal solids to pollute clarified oil tanks")
    ]

    for co_w, prod_w, units_w, std_m, act_m, cost_m, cause_w in wastage_cases:
        tot_std_mat = units_w * std_m
        tot_act_mat = units_w * act_m
        wastage_units = tot_act_mat - tot_std_mat
        wastage_cost = wastage_units * cost_m

        # 1. Hard Q: Calculate Raw Material Wastage Cost
        if counts["hard"] < 200:
            c_wcost = f"R{wastage_cost:,.2f} ({wastage_units:,.1f} units of material wasted)"
            w_wcost = [
                f"R{tot_act_mat * cost_m:,.2f} (calculated total actual material cost)",
                f"R{tot_std_mat * cost_m:,.2f} (calculated standard material cost)",
                f"R{wastage_units:,.2f} (omitted cost per unit of material)",
                f"R{wastage_cost * 1.2:,.2f}",
                f"R{wastage_cost * 0.8:,.2f}",
                f"R{(wastage_cost + 40000):,.2f}",
                f"R{(wastage_cost - 30000):,.2f}"
            ]
            q_wcost = (f"The standard specification for **{co_w}** indicates that each unit of *{prod_w}* requires **{std_m:.2f} metres/kg** of raw material "
                       f"at a standard cost of **R{cost_m:.2f}** per metre/kg. During the year, the factory produced **{units_w:,.0f} units** "
                       f"and actually used **{tot_act_mat:,.1f} metres/kg** (an average of **{act_m:.2f} metres/kg** per unit). "
                       f"Calculate the **financial cost of raw material wastage**:")
            exp_wcost = (f"Standard Material Required = {units_w:,.0f} x {std_m:.2f} = {tot_std_mat:,.1f}\n"
                         f"Actual Material Used = {tot_act_mat:,.1f}\n"
                         f"Material Wastage = {tot_act_mat:,.1f} - {tot_std_mat:,.1f} = {wastage_units:,.1f}\n"
                         f"Cost of Wastage = {wastage_units:,.1f} x R{cost_m:.2f} = {c_wcost}.")
            add_q("hard", "Material Wastage & Variance Analysis", q_wcost, c_wcost, w_wcost, "Evaluating", f"Calculate material wastage cost for {co_w}", exp_wcost)

        # 2. Hard Q: Internal Control and Management Remedial Action
        if counts["hard"] < 200:
            c_rec = f"Investigate root cause: {cause_w}. Provide operator retraining, recalibrate machinery, and enforce strict material requisition slips."
            w_rec = [
                "Increase selling price by 40% immediately to transfer all wastage losses onto retail customers",
                "Dismiss all factory workers instantly without labour hearings and cease production",
                "Transfer the cost of wasted material directly to administrative advertising expenses",
                "Discontinue recording raw material inventory balances in the general ledger",
                "Reduce the quality of raw materials purchased to the cheapest grade available on the market",
                "Ignore the variance because material wastage of 20% to 30% is standard and unavoidable under King IV"
            ]
            q_rec = (f"Referring to the raw material wastage at **{co_w}** on *{prod_w}*: "
                     f"Which internal control recommendation and corrective managerial action should the Cost Accountant advise?")
            exp_rec = f"Correct Internal Control Action: **{c_rec}**. CAPS Cost Accounting requires identification of causes and practical control measures."
            add_q("hard", "Internal Control in Manufacturing", q_rec, c_rec, w_rec, "Evaluating", f"Internal control for wastage in {co_w}", exp_rec)

    labour_cases = [
        ("Protea Clothing Ltd", 8000, 1.5, 2.1, 85.0, "Frequent Stage 6 load shedding without industrial backup generator and conveyor breakdown causing 4,800 hours of idle time"),
        ("Kavango Leather Ltd", 4500, 2.0, 2.8, 95.0, "High absenteeism on Monday mornings and lack of supervisory oversight on the stitching line"),
        ("Algoa Woodworks Ltd", 6000, 3.0, 3.9, 90.0, "Bottlenecks at the spray-painting booth and inadequate drying space slowing down assembly"),
        ("Soweto Bakery Ltd", 60000, 0.10, 0.16, 70.0, "Flour delivery delays and breakdown of automated dough kneading machinery"),
        ("Drakensberg Solar Ltd", 2800, 4.0, 5.2, 110.0, "Power voltage dips disrupting robotic laser soldering machines and requiring manual rework"),
        ("Zululand Pack Ltd", 18000, 0.40, 0.55, 65.0, "Shortage of forklift operators in raw material storage causing machine waiting time"),
        ("Highveld Gates Ltd", 5000, 2.5, 3.4, 95.0, "Arc welding gas cylinder shortages and unorganized tool workstations"),
        ("Karoo Footwear Ltd", 7500, 1.2, 1.7, 75.0, "Worker go-slow protest over overtime bonus calculation disputes"),
        ("Table Mountain Teas Ltd", 25000, 0.15, 0.22, 60.0, "Frequent carton packaging machine jams due to uncalibrated feeding rollers"),
        ("Springbok Balls Ltd", 12000, 0.50, 0.72, 80.0, "Inadequate training of newly hired casual workers during peak tournament demand"),
        ("Limpopo Pottery Ltd", 4200, 1.8, 2.5, 70.0, "Excessive manual handling between glazing stations and firing kilns"),
        ("Blyde Valley Timber Ltd", 3600, 3.5, 4.6, 100.0, "Power outages causing restart delays on high-voltage timber seasoning kilns"),
        ("Gauteng Textiles Ltd", 14000, 1.0, 1.45, 80.0, "Poor lighting and ergonomics in the sewing hall leading to worker fatigue and slower stitch rates"),
        ("Free State Feeds Ltd", 15000, 0.30, 0.45, 65.0, "Unplanned conveyor motor burnouts and delayed maintenance response"),
        ("Namaqua Tiles Ltd", 9000, 0.80, 1.15, 75.0, "Pallet truck shortages causing finished goods congestion on the factory floor"),
        ("Outeniqua Woodcraft Ltd", 2400, 5.0, 6.8, 95.0, "Hand-sanding bottlenecks due to defective electric orbital sanders"),
        ("Mpumalanga Chem Ltd", 8500, 0.90, 1.30, 90.0, "Manual drum handling rather than automated palletizing systems"),
        ("Ezulwini Glass Ltd", 11000, 0.60, 0.88, 85.0, "Cooling lehr conveyor belt breakdowns leading to glass batch thermal shock"),
        ("Vaal Pipes Ltd", 6500, 1.6, 2.3, 95.0, "Raw plastic granule drying delays before extrusion injection"),
        ("Stellenbosch Cooperage Ltd", 1600, 8.0, 10.8, 120.0, "Shortage of skilled master coopers requiring extensive rework on leaky oak casks"),
        ("Tshwane Radiators Ltd", 8500, 1.4, 1.95, 92.0, "Copper tube brazing leak reworks and flux station clutter"),
        ("Richards Bay Wire Works Ltd", 7200, 1.1, 1.55, 78.0, "Wire galvanizing bath heating element failure causing line shutdowns"),
        ("Polokwane Feeds Hub Ltd", 21000, 0.25, 0.38, 62.0, "Bagging scale calibration drift requiring manual re-weighing"),
        ("Kimberley Tools Mfg Ltd", 14000, 0.65, 0.92, 84.0, "Drop-hammer die alignment checks causing operator standing time"),
        ("Durban Soaps Plant Ltd", 45000, 0.08, 0.13, 68.0, "Soap plodder cooling jacket water leak halting extrusion line")
    ]

    for co_l, units_l, std_h, act_h, rate_h, cause_l in labour_cases:
        tot_std_hours = units_l * std_h
        tot_act_hours = units_l * act_h
        excess_hours = tot_act_hours - tot_std_hours
        excess_cost = excess_hours * rate_h

        # 1. Hard Q: Labour Inefficiency Cost
        if counts["hard"] < 200:
            c_lcost = f"R{excess_cost:,.2f} ({excess_hours:,.1f} excess hours worked)"
            w_lcost = [
                f"R{tot_act_hours * rate_h:,.2f} (total direct labour cost)",
                f"R{tot_std_hours * rate_h:,.2f} (standard labour cost)",
                f"R{excess_hours:,.2f} (omitted hourly labour rate)",
                f"R{excess_cost * 1.25:,.2f}",
                f"R{excess_cost * 0.75:,.2f}",
                f"R{(excess_cost + 35000):,.2f}",
                f"R{(excess_cost - 25000):,.2f}"
            ]
            q_lcost = (f"In **{co_l}**, the direct labour standard for *producing one unit* is **{std_h:.2f} hours** at **R{rate_h:.2f}** per hour. "
                       f"During the year, the factory produced **{units_l:,.0f} units** but logged **{tot_act_hours:,.1f} actual labour hours** "
                       f"(averaging **{act_h:.2f} hours** per unit). Calculate the **financial cost of direct labour inefficiency (idle time/excess hours)**:")
            exp_lcost = (f"Standard Labour Hours = {units_l:,.0f} x {std_h:.2f} = {tot_std_hours:,.1f} hours\n"
                         f"Actual Labour Hours = {tot_act_hours:,.1f} hours\n"
                         f"Excess Hours = {tot_act_hours:,.1f} - {tot_std_hours:,.1f} = {excess_hours:,.1f} hours\n"
                         f"Labour Inefficiency Cost = {excess_hours:,.1f} hours x R{rate_h:.2f} = {c_lcost}.")
            add_q("hard", "Labour Efficiency & Productivity", q_lcost, c_lcost, w_lcost, "Evaluating", f"Calculate labour inefficiency cost for {co_l}", exp_lcost)

        # 2. Hard Q: Managerial Evaluation of Productivity
        if counts["hard"] < 200:
            c_lev = f"Unfavourable labour variance: {cause_l}. Management must install backup generators, implement biometric attendance, and introduce production incentive bonuses."
            w_lev = [
                "Favourable labour variance because employees were paid more hours than budgeted",
                "Dismiss the production manager and replace all machinery with manual hand tools",
                "Cease all operations during electricity load shedding and pay workers zero wages",
                "Transfer excess labour hours to Trade and Other Receivables as an asset",
                "Direct labour productivity has zero impact on cost of production in modern manufacturing",
                "Increase standard hours to match actual hours to conceal the inefficiency"
            ]
            q_lev = (f"Evaluate the **labour productivity performance** at **{co_l}** and provide the most sound managerial conclusion:")
            exp_lev = f"Evaluation: **{c_lev}**. Direct labour productivity and management response to idle time are key exam evaluation topics."
            add_q("hard", "Labour Efficiency & Productivity", q_lev, c_lev, w_lev, "Evaluating", f"Evaluate labour productivity for {co_l}", exp_lev)

    # Make-or-Buy Decision Cases (20 cases)
    make_buy_cases = [
        ("Protea Footwear Ltd", "Shoe Soles", 12000, 35.0, 20.0, 15.0, 58.0),
        ("Algoa Furniture Ltd", "Pre-cut Table Legs", 6500, 75.0, 45.0, 30.0, 125.0),
        ("Drakensberg Beverages Ltd", "Plastic Bottle Preforms", 35000, 8.50, 4.20, 3.80, 14.50),
        ("Zululand Paper Works Ltd", "Die-Cut Handles", 25000, 15.0, 9.0, 6.0, 26.0),
        ("Highveld Steel Doors Ltd", "Lock Mechanisms", 4500, 120.0, 80.0, 40.0, 210.0),
        ("Karoo Leathercraft Ltd", "Brass Buckles", 5000, 45.0, 25.0, 18.0, 78.0),
        ("Springbok Sports Ltd", "Inflatable Bladders", 15000, 28.0, 16.0, 12.0, 48.0),
        ("Gauteng Meditech Ltd", "Sterile Packaging Pouches", 30000, 12.0, 7.5, 4.5, 21.0),
        ("Vaal Polymer Pipes Ltd", "Coupling Joints", 11000, 42.0, 26.0, 16.0, 72.0),
        ("Tshwane Auto Components Ltd", "Brake Pad Shims", 8500, 68.0, 42.0, 26.0, 115.0),
        ("Centurion Aerospace Parts Ltd", "Titanium Fasteners", 4000, 110.0, 65.0, 40.0, 185.0),
        ("Bloemfontein Milling Hub Ltd", "Polypropylene Grain Sacks", 28000, 6.50, 3.80, 2.20, 11.20),
        ("East London Shipchandlers Ltd", "Galvanized Thimbles", 5500, 32.0, 18.0, 12.0, 54.0),
        ("Klerksdorp Lime Ltd", "Paper Valve Sacks", 35000, 4.20, 2.50, 1.50, 7.20),
        ("Potchefstroom Yoghurt Ltd", "Plastic Spoons & Lids", 42000, 1.80, 1.10, 0.70, 3.20),
        ("George Cedarcraft Ltd", "Turned Finial Knobs", 3200, 48.0, 28.0, 18.0, 82.0),
        ("Secunda Resins Ltd", "Reinforced Corner Brackets", 9500, 22.0, 14.0, 8.0, 38.0),
        ("Vereeniging Castings Ltd", "Brass Bushings", 3800, 85.0, 50.0, 32.0, 148.0),
        ("Welkom Core Bits Ltd", "Steel Mandrel Shanks", 7500, 95.0, 55.0, 35.0, 165.0),
        ("Bethlehem Cheese Co Ltd", "Wax Coating Blend", 12000, 18.0, 10.5, 6.5, 31.0),
        ("Newcastle Heavy Barrels Ltd", "Drum Locking Rings", 9200, 24.0, 15.0, 9.0, 42.0),
        ("Mossel Bay Fish Meal Ltd", "Antioxidant Preservative", 28000, 5.0, 3.2, 1.8, 8.8),
        ("Mthatha School Furniture Ltd", "Moulded Plastic Seats", 6400, 45.0, 26.0, 16.0, 78.0),
        ("Upington Sun Raisins Ltd", "Sulfur Fumigation Strips", 31000, 2.5, 1.5, 0.8, 4.4),
        ("Vryheid Briquettes Ltd", "Cornstarch Binder", 42000, 1.2, 0.7, 0.4, 2.1),
        ("Ladysmith Curtains Ltd", "Brass Curtain Eyelets", 8600, 8.5, 5.2, 3.1, 14.8),
        ("Bredasdorp Barley Works Ltd", "Hessian Grain Bags", 24000, 7.8, 4.8, 2.8, 13.5),
        ("Cradock Leather Saddles Ltd", "Steel Stirrup Irons", 1400, 130.0, 75.0, 45.0, 220.0),
        ("Makhanda Bookbinding Ltd", "Book Spine Calico Cloth", 18500, 4.2, 2.6, 1.6, 7.5),
        ("Oudtshoorn Feathercraft Ltd", "Turned Wood Handles", 12500, 12.0, 7.5, 4.5, 21.0),
        ("Knysna Timber Floors Ltd", "Moisture Barrier Underlay", 5400, 28.0, 16.0, 10.0, 48.0),
        ("Standerton Milking Systems Ltd", "Rubber Liner Teatcups", 4800, 35.0, 22.0, 14.0, 62.0),
        ("Harrismith Tarpaulins Ltd", "Reinforced Eyelet Rings", 3600, 16.0, 10.0, 6.0, 28.0),
        ("Kuruman Crushers Ltd", "Cast Manganese Teeth", 3100, 145.0, 85.0, 55.0, 250.0),
        ("Thohoyandou Oilseed Ltd", "Filter Cloth Sleeves", 23000, 8.5, 5.2, 3.2, 15.0),
        ("Plettenberg Bay Timber Ltd", "Stainless Decking Screws", 6400, 12.0, 7.5, 4.5, 21.0),
        ("Saldanha Shiprepair Ltd", "Zinc Sacrificial Anodes", 2800, 95.0, 55.0, 35.0, 165.0),
        ("Grahamstown Pottery Ltd", "High-Temperature Kiln Props", 12000, 22.0, 13.0, 8.0, 38.0),
        ("Springbok Solar Inverters Ltd", "Aluminum Heatsinks", 4500, 85.0, 50.0, 30.0, 145.0),
        ("Witbank Refractory Ltd", "Ceramic Insulating Bricks", 8800, 38.0, 22.0, 14.0, 66.0),
        ("Paarl Wine Oak Ltd", "Galvanized Hoop Steel", 3800, 52.0, 30.0, 18.0, 88.0)
    ]

    for co_mb, comp_name, req_units, dm_mb, dl_mb, foh_v_mb, quote_mb in make_buy_cases:
        var_cost_make = dm_mb + dl_mb + foh_v_mb
        tot_make_cost = req_units * var_cost_make
        tot_buy_cost = req_units * quote_mb

        if counts["hard"] < 200:
            if var_cost_make < quote_mb:
                c_mb = f"Make in-house: Variable cost is R{var_cost_make:.2f} per unit vs buy price of R{quote_mb:.2f}, saving R{tot_buy_cost - tot_make_cost:,.2f}"
                w_mb = [
                    f"Buy from external supplier: Supplier price of R{quote_mb:.2f} is cheaper than total manufacturing cost",
                    f"Make in-house only if fixed factory overheads are completely eliminated",
                    f"Outsource immediately because buying always guarantees superior product quality",
                    f"Make in-house: Marginal cost is R{dm_mb + dl_mb:.2f} (omitted variable overheads)",
                    f"Buy from supplier: Total saving is R{(tot_buy_cost - tot_make_cost) * 1.5:,.2f}",
                    f"Decision cannot be evaluated without knowing the company authorized share capital"
                ]
            else:
                c_mb = f"Buy from supplier: External quote of R{quote_mb:.2f} is cheaper than internal variable cost of R{var_cost_make:.2f}, saving R{tot_make_cost - tot_buy_cost:,.2f}"
                w_mb = [
                    f"Make in-house regardless of cost to keep factory workers busy",
                    f"Buy from supplier only if external supplier purchases company shares",
                    f"Outsourcing is strictly illegal under the South African Companies Act",
                    f"Make in-house: Internal variable cost of R{var_cost_make:.2f} is superior to external supply",
                    f"Buy from supplier: Cost saving is R{(tot_make_cost - tot_buy_cost) * 1.2:,.2f}",
                    f"Decision should be made solely based on the managing director personal preference"
                ]

            q_mb = (f"**Decision-Making Analysis — Make vs Buy for {co_mb}**:\n"
                    f"The factory requires **{req_units:,.0f} units** of *{comp_name}* annually. "
                    f"Internal variable costs per unit are: Direct Materials R{dm_mb:.2f}, Direct Labour R{dl_mb:.2f}, Variable Factory Overheads R{foh_v_mb:.2f}. "
                    f"Fixed factory overheads will continue unchanged whether made or bought. An outside supplier offers to supply the component at **R{quote_mb:.2f}** per unit. "
                    f"Evaluate the **financial wisdom** of whether {co_mb} should **make or buy** the component:")
            exp_mb = (f"Internal Variable Cost to Make = DM (R{dm_mb:.2f}) + DL (R{dl_mb:.2f}) + Variable FOH (R{foh_v_mb:.2f}) = R{var_cost_make:.2f} per unit.\n"
                      f"Outside Supplier Price = R{quote_mb:.2f} per unit.\n"
                      f"Decision: {c_mb}. Fixed overheads are unavoidable and sunk.")
            add_q("hard", "Make-or-Buy Decision Analysis", q_mb, c_mb, w_mb, "Evaluating", f"Make or buy evaluation for {co_mb}", exp_mb)

    # Ethical & Internal Control Dilemmas in Manufacturing (30 cases)
    mfg_ethics = [
        ("The factory production manager secretly substituted standard grade flame-retardant fabric with cheap, highly flammable synthetic polyester to reduce Direct Material Cost by R450,000 and earn an annual executive cost-saving bonus.",
         "Unethical and unlawful: Endangers customer life and safety, violates the Consumer Protection Act and SABS standards, and breaches King IV ethical leadership principles.",
         ["Fully ethical because minimizing Direct Material Cost maximizes gross profit and dividend payouts",
          "Acceptable practice provided the safety risk is not detected by provincial labour inspectors",
          "A legitimate accounting cost-saving technique actively encouraged by the Johannesburg Stock Exchange",
          "Permissible if the production manager donates 10% of the bonus to the factory employee sports club",
          "A minor operational detail that does not concern executive directors or the audit committee",
          "Lawful under the Companies Act because blazers are consumer clothing rather than industrial equipment"]),

        ("A supervisor routinely clocks in time-cards for absent factory friends using unauthorized duplicate RFID cards, allowing them to collect full direct labour wages without performing any production work.",
         "Fraud and payroll theft: Severe breakdown of internal control over Direct Labour. The supervisor and accomplices face criminal charges and dismissal. Management must install biometric facial scanners.",
         ["Acceptable solidarity among factory workers during economic hardship",
          "A minor human resource issue that only requires an informal verbal reminder",
          "Permissible provided the total units produced by the remaining workers meets weekly targets",
          "Lawful because overtime wage allocations cover unworked shifts automatically",
          "A legitimate labour flexi-time practice recognized under the Basic Conditions of Employment Act",
          "Acceptable provided the absent workers repay the wages upon retirement"]),

        ("A timber furniture factory dumps sawdust, toxic varnish waste, and chemical solvents into an adjacent municipal storm drain at midnight to avoid paying hazardous waste disposal contractors.",
         "Severe violation of National Environmental Management Act and King IV: Compromises public health, exposes the company to hefty fines, environmental cleanup liability, and reputational collapse.",
         ["Smart commercial waste management that reduces Factory Overhead expenses significantly",
          "Permissible because municipal stormwater systems are designed to wash away all chemical industrial waste",
          "Acceptable practice provided dumping is performed outside normal business trading hours",
          "A routine matter that falls strictly outside the scope of the Board Social and Ethics Committee",
          "Lawful provided the factory plants three indigenous trees on Arbor Day to offset the pollution",
          "Permissible if the chemical waste is diluted with 50% tap water prior to discharge"]),

        ("Factory storehouse security guards allow trucks to leave with unrecorded excess rolls of fabric in exchange for cash kickbacks, claiming the inventory was lost to manufacturing scrap.",
         "Stock theft and corruption: Critical failure of physical gate controls and inventory dispatch documentation. Management must enforce independent gate pass verifications and security camera audits.",
         ["Normal inventory shrinkage that should be absorbed into Factory Overhead without investigation",
          "Acceptable practice because factory scrap has zero economic value under IFRS standards",
          "Permissible provided the security guards report the kickbacks on their personal SARS tax returns",
          "A minor logistical delay that will self-correct when new raw materials are purchased",
          "Lawful under King IV as informal employee performance incentives",
          "An administrative issue to be resolved by increasing the selling price of finished goods"]),

        ("The factory engineer falsified machinery maintenance logbooks, postponing safety overhauls on high-speed metal stamping presses for 18 months to cut maintenance overhead costs, resulting in a worker losing two fingers.",
         "Criminal negligence and gross breach of Occupational Health and Safety Act and King IV: Neglecting preventive maintenance for short-term cost savings creates catastrophic safety hazards and personal director liability.",
         ["Exemplary cost-cutting because postponing maintenance improves short-term operating profit margin",
          "Unavoidable manufacturing casualty that has zero bearing on management ethics or corporate governance",
          "Acceptable because the worker can be easily replaced by hiring an entry-level casual labourer",
          "Permissible provided the worker receives a one-time company gift hamper and continues working",
          "A routine factory incident that requires no reporting to the Department of Employment and Labour",
          "Lawful practice provided factory overheads were kept strictly below budgeted targets"])
    ]

    for sc_eth, corr_eth, wrongs_eth in mfg_ethics:
        if counts["hard"] < 200:
            q_eth_m = f"**Manufacturing Internal Control & Ethics Scenario**:\n\n*\"{sc_eth}\"*\n\nProvide the most professional evaluation under CAPS Cost Accounting and King IV governance:"
            exp_eth_m = f"Evaluation: **{corr_eth}**."
            add_q("hard", "Manufacturing Internal Control & Ethics", q_eth_m, corr_eth, wrongs_eth, "Evaluating", "Evaluate manufacturing ethics scenario", exp_eth_m)

        if counts["hard"] < 200:
            q_eth_m2 = f"Identify the primary internal control measure required to prevent the following manufacturing malpractice:\n\n*\"{sc_eth}\"*"
            c_ctrl = f"Enforce strict segregation of duties, physical access controls, periodic unannounced audits, and independent oversight as outlined in King IV and CAPS standards."
            w_ctrl = [
                "Increase worker wages by 50% without asking questions",
                "Abolish all factory supervision and allow workers to self-regulate completely",
                "Cease keeping cost accounting records and Production Cost Statements",
                "Outsource all factory management to overseas remote freelancers",
                "Order commercial banks to monitor daily worker lunch breaks",
                "Replace general ledgers with single-entry cash registers"
            ]
            exp_ctrl = f"Control Measure: **{c_ctrl}**."
            add_q("hard", "Manufacturing Internal Control & Ethics", q_eth_m2, c_ctrl, w_ctrl, "Evaluating", "Internal control measure for manufacturing", exp_ctrl)

    print(f"Generated: easy={counts['easy']}, medium={counts['medium']}, hard={counts['hard']}")

    output_path = "/data/data/com.termux/files/home/quiz-/dataset/grade12/accounting/paper2_acc_manufacturing.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"SUCCESS: {output_path} created with {len(questions)} questions: {counts}")

if __name__ == "__main__":
    build_manufacturing()
