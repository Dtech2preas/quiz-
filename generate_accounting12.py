import json
import random
import os
import hashlib
import math
from typing import List, Dict

# Helpers import
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'generators/helpers'))
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

class AccountingKnowledgeBase:
    def __init__(self, json_path="extracted_topics_accounting.json"):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_topics(self):
        return self.data

class AdvancedAccountingQuestionEngine:
    def __init__(self, topic_data):
        self.topic = topic_data['topic']
        self.prefix = topic_data['prefix']
        self.file = topic_data['file']

        subtopics_list = [s['name'] for s in topic_data['subtopics']]
        if not subtopics_list:
            subtopics_list = [self.topic]

        self.generator = TopicGenerator(self.topic, self.prefix, subtopics_list)
        self.subtopic_data = topic_data['subtopics']

    def generate_theory_questions(self, target_count=300):
        # We need to extract all descriptions across all topics for good distractors
        all_descs = []
        for s in self.subtopic_data:
            for f in s.get('facts', []):
                all_descs.append(f['desc'])

        all_terms = []
        for s in self.subtopic_data:
            for f in s.get('facts', []):
                all_terms.append(f['a'])

        attempts = 0
        while not self.generator.is_done() and self.generator.difficulty_counts['easy'] < self.generator.difficulty_targets['easy'] and attempts < target_count * 50:
            attempts += 1

            subtopic_obj = random.choice(self.subtopic_data)
            if not subtopic_obj.get('facts'):
                continue

            fact = random.choice(subtopic_obj['facts'])
            subtopic_name = subtopic_obj['name']

            q_type = random.choice([1, 2, 3])

            if q_type == 1:
                # Type 1: Definition -> Term
                q_text = f"Which accounting term is defined as: {fact['desc']}? ({self.topic})"
                correct = fact['a']
                wrong = list(fact['w'])

                # Ensure we have enough wrong answers (at least 6-8)
                extra_wrongs = [t for t in all_terms if t != correct and t not in wrong]
                random.shuffle(extra_wrongs)
                wrong.extend(extra_wrongs[:8])

                exp = f"The correct term is {correct}."

                self.generator.add_question(subtopic_name, "easy", q_text, correct, wrong, exp)

            elif q_type == 2:
                # Type 2: Term -> Definition
                q_text = f"What is the correct definition or description for the term '{fact['a']}'? ({self.topic})"
                correct = fact['desc']

                wrong_desc = [d for d in all_descs if d != correct]
                random.shuffle(wrong_desc)

                # Add some generic fallbacks just in case
                wrong_desc.extend([
                    "a metric used solely for internal cost analysis to determine non-operational variances",
                    "a statutory requirement that applies only to close corporations and not public companies",
                    "the process of reconciling external audit reports with internal zero-based budgets",
                    "a financial indicator showing the exact amount of cash on hand after adjusting for inflation",
                    "the total amount of unauthorized expenditure incurred by the directors",
                    "a method of calculating depreciation based on the prime cost of manufacturing",
                    "an adjustment made at year-end to reflect unrealized profits on inventory",
                    "the legal framework governing the taxation of sole traders"
                ])

                wrong = wrong_desc[:8]
                exp = f"'{fact['a']}' means: {correct}."

                self.generator.add_question(subtopic_name, "easy", q_text, correct, wrong, exp)

            else:
                # Type 3: Identify the INCORRECT statement
                correct_fact = fact

                # Find an incorrect fact (mix and match a term with a wrong desc)
                if len(all_terms) > 1 and len(all_descs) > 1:
                    wrong_term = random.choice([t for t in all_terms if t != fact['a']])
                    wrong_desc_val = random.choice([d for d in all_descs if d != fact['desc']])

                    incorrect_statement = f"{wrong_term}: {wrong_desc_val} (Incorrect)"
                    correct = incorrect_statement

                    # Generate other correct statements for the wrong pool (distractors)
                    wrong_pool_statements = []

                    other_facts = []
                    for s in self.subtopic_data:
                        other_facts.extend(s.get('facts', []))

                    random.shuffle(other_facts)

                    for of in other_facts:
                        if of['a'] != wrong_term:
                            wrong_pool_statements.append(f"{of['a']}: {of['desc']}")

                    if len(wrong_pool_statements) >= 6:
                        q_text = f"Which of the following terms is INCORRECTLY matched with its description? ({self.topic})"
                        exp = f"The statement '{incorrect_statement}' is incorrect because {wrong_term} does not mean {wrong_desc_val}."
                        self.generator.add_question(subtopic_name, "easy", q_text, correct, wrong_pool_statements[:8], exp)


    def _generate_analysis_questions(self):
        # Generate varied ratio questions (profitability, liquidity, solvency, return)
        subtopic_name = "Financial Indicators & Interpretation"
        attempts = 0
        added = 0

        while attempts < 50000 and self.generator.difficulty_counts['medium'] + self.generator.difficulty_counts['hard'] < self.generator.difficulty_targets['medium'] + self.generator.difficulty_targets['hard']:
            attempts += 1

            q_type = random.choice(['gross_margin', 'operating_margin', 'current_ratio', 'acid_test', 'solvency', 'stock_turnover', 'debt_equity', 'nav', 'eps', 'dps', 'ret_equity'])

            difficulty = random.choice(["easy", "easy", "medium", "hard"])

            if q_type == 'gross_margin':
                sales = random.randint(500, 5000) * 1000
                cost_of_sales = int(sales * random.uniform(0.4, 0.8))
                gross_profit = sales - cost_of_sales

                if difficulty == "medium":
                    margin = (gross_profit / sales) * 100
                    correct_str = f"{margin:.1f}%"
                    wrong_pool = get_wrong_floats(margin, count=8, decimals=1)
                    wrong_pool = [f"{w}%" for w in wrong_pool]

                    q_text = f"Calculate the Gross Profit Margin if Sales are R{sales:,} and Cost of Sales is R{cost_of_sales:,}."
                    exp = f"Gross Profit = Sales (R{sales:,}) - COS (R{cost_of_sales:,}) = R{gross_profit:,}. Margin = (R{gross_profit:,} / R{sales:,}) * 100 = {margin:.1f}%."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1
                else:
                    # Hard: given margin and COS, find Sales
                    margin = round(random.uniform(20.0, 60.0), 1)
                    # sales = cos / (1 - margin)
                    sales_calc = cost_of_sales / (1 - (margin / 100))
                    sales_calc = round(sales_calc, 0)
                    correct_str = f"R{sales_calc:,.0f}"

                    wrong_pool_vals = [cost_of_sales * (1 + margin/100), cost_of_sales / (margin/100), cost_of_sales * (margin/100), sales_calc * 1.1, sales_calc * 0.9, cost_of_sales + margin*1000, cost_of_sales - margin*1000, sales_calc * 1.2]
                    wrong_pool = [f"R{w:,.0f}" for w in wrong_pool_vals]

                    q_text = f"A company has a Cost of Sales of R{cost_of_sales:,} and maintains a Gross Profit Margin of {margin}%. Calculate the total Sales."
                    exp = f"Sales = Cost of Sales / (1 - Margin%) = R{cost_of_sales:,} / (1 - {margin/100}) = R{sales_calc:,.0f}."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'current_ratio':
                ca = random.randint(100, 1000) * 1000
                cl = random.randint(50, 800) * 1000

                if difficulty == "medium":
                    ratio = ca / cl
                    correct_str = f"{ratio:.2f} : 1"

                    wrong_pool_vals = [cl/ca if ca != 0 else 0, (ca+cl)/cl, ca/(cl*1.5), (ca*0.8)/cl, ratio*1.2, ratio*0.8, ratio+1, ratio-0.5]
                    wrong_pool = [f"{abs(w):.2f} : 1" for w in wrong_pool_vals]

                    q_text = f"Calculate the Current Ratio if Current Assets are R{ca:,} and Current Liabilities are R{cl:,}."
                    exp = f"Current Ratio = Current Assets : Current Liabilities = R{ca:,} : R{cl:,} = {ratio:.2f} : 1."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1
                else:
                    # Hard: include adjustments
                    inv_adjustment = random.randint(5, 50) * 1000
                    ca_adj = ca - inv_adjustment # e.g. inventory written off
                    ratio = ca_adj / cl
                    correct_str = f"{ratio:.2f} : 1"

                    wrong_ratio_1 = ca / cl
                    wrong_ratio_2 = (ca + inv_adjustment) / cl
                    wrong_ratio_3 = ca_adj / (cl - inv_adjustment)
                    wrong_pool_vals = [wrong_ratio_1, wrong_ratio_2, wrong_ratio_3, ratio*1.5, ratio*0.5, wrong_ratio_1*1.1, cl/ca_adj if ca_adj != 0 else 0, 1.0]
                    wrong_pool = [f"{abs(w):.2f} : 1" for w in wrong_pool_vals]

                    q_text = f"Current Assets are initially R{ca:,} and Current Liabilities are R{cl:,}. It was discovered that obsolete inventory worth R{inv_adjustment:,} must be written off. Calculate the accurate Current Ratio after this adjustment."
                    exp = f"Adjusted Current Assets = R{ca:,} - R{inv_adjustment:,} = R{ca_adj:,}. Current Ratio = R{ca_adj:,} : R{cl:,} = {ratio:.2f} : 1."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'stock_turnover':
                cost_of_sales = random.randint(400, 2000) * 1000
                open_stock = random.randint(50, 300) * 1000
                close_stock = random.randint(40, 350) * 1000
                avg_stock = (open_stock + close_stock) / 2

                rate = cost_of_sales / avg_stock
                correct_str = f"{rate:.1f} times"

                wrong_pool_vals = [cost_of_sales/open_stock, cost_of_sales/close_stock, avg_stock/cost_of_sales, rate*2, rate/2, cost_of_sales/(open_stock+close_stock), rate+2, rate-1.5]
                wrong_pool = [f"{abs(w):.1f} times" for w in wrong_pool_vals]

                q_text = f"Calculate the Stock Turnover Rate if Cost of Sales is R{cost_of_sales:,}, Opening Stock is R{open_stock:,}, and Closing Stock is R{close_stock:,}."
                exp = f"Average Stock = (R{open_stock:,} + R{close_stock:,}) / 2 = R{avg_stock:,}. Stock Turnover Rate = Cost of Sales / Average Stock = R{cost_of_sales:,} / R{avg_stock:,} = {rate:.1f} times."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'eps':
                net_profit = random.randint(200, 2000) * 1000
                shares_issued = random.randint(100, 1000) * 1000

                if difficulty == "medium":
                    eps = (net_profit / shares_issued) * 100
                    correct_str = f"{eps:.0f} cents"

                    wrong_pool_vals = get_wrong_floats(eps, count=8, decimals=0)
                    wrong_pool = [f"{w} cents" for w in wrong_pool_vals]

                    q_text = f"Calculate the Earnings Per Share (EPS) if the Net Profit after tax is R{net_profit:,} and the number of issued shares is {shares_issued:,}."
                    exp = f"EPS = (Net Profit / Number of Shares) * 100 = (R{net_profit:,} / {shares_issued:,}) * 100 = {eps:.0f} cents."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1
                else:
                    # Hard: Weighted average shares
                    shares_start = random.randint(100, 500) * 1000
                    new_shares = random.randint(50, 200) * 1000
                    months_new = random.choice([3, 4, 6, 9])

                    weighted_shares = shares_start + (new_shares * (months_new / 12))
                    eps = (net_profit / weighted_shares) * 100
                    correct_str = f"{eps:.1f} cents"

                    wrong_eps1 = (net_profit / (shares_start + new_shares)) * 100
                    wrong_eps2 = (net_profit / shares_start) * 100
                    wrong_eps3 = (net_profit / (shares_start + new_shares * ((12-months_new)/12))) * 100

                    wrong_pool_vals = [wrong_eps1, wrong_eps2, wrong_eps3, eps*1.2, eps*0.8, eps+15, eps-10, wrong_eps1*1.1]
                    wrong_pool = [f"{w:.1f} cents" for w in wrong_pool_vals]

                    q_text = f"A company started the year with {shares_start:,} issued shares. They issued an additional {new_shares:,} shares with {months_new} months remaining in the financial year. The Net Profit after tax is R{net_profit:,}. Calculate the Earnings Per Share (EPS)."
                    exp = f"Weighted average shares = {shares_start:,} + ({new_shares:,} x {months_new}/12) = {weighted_shares:,.0f}. EPS = (R{net_profit:,} / {weighted_shares:,.0f}) * 100 = {eps:.1f} cents."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

        return added

    def _generate_manufacturing_questions(self):
        subtopic_name = "Cost Accounting & Manufacturing"
        attempts = 0
        added = 0

        while attempts < 50000 and self.generator.difficulty_counts['medium'] + self.generator.difficulty_counts['hard'] < self.generator.difficulty_targets['medium'] + self.generator.difficulty_targets['hard']:
            attempts += 1

            q_type = random.choice(['direct_material', 'factory_overhead', 'cost_of_production', 'break_even'])
            difficulty = random.choice(["easy", "easy", "medium", "hard"])

            if q_type == 'direct_material':
                open_rm = random.randint(50, 500) * 1000
                purchases = random.randint(200, 2000) * 1000
                carriage = random.randint(10, 40) * 1000
                close_rm = random.randint(60, 180) * 1000

                dmc = open_rm + purchases + carriage - close_rm
                correct_str = f"R{dmc:,}"

                wrong_pool_vals = [
                    open_rm + purchases - close_rm,
                    purchases + carriage - close_rm,
                    open_rm + purchases + carriage + close_rm,
                    open_rm + purchases,
                    dmc * 1.1, dmc * 0.9,
                    dmc + carriage, dmc - carriage
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"Calculate the Direct Material Cost issued to the factory. Opening Raw Materials: R{open_rm:,}. Purchases of Raw Materials: R{purchases:,}. Carriage on Purchases: R{carriage:,}. Closing Raw Materials: R{close_rm:,}."
                exp = f"Direct Material Cost = Opening Stock (R{open_rm:,}) + Purchases (R{purchases:,}) + Carriage (R{carriage:,}) - Closing Stock (R{close_rm:,}) = R{dmc:,}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'factory_overhead':
                rent = random.randint(100, 1000) * 1000
                rent_factory_portion = random.choice([0.6, 0.7, 0.75, 0.8])
                factory_rent = rent * rent_factory_portion

                indirect_mat = random.randint(20, 80) * 1000
                depreciation = random.randint(50, 500) * 1000

                fo = factory_rent + indirect_mat + depreciation
                correct_str = f"R{fo:,.0f}"

                wrong_pool_vals = [
                    rent + indirect_mat + depreciation,
                    factory_rent + depreciation,
                    rent * (1 - rent_factory_portion) + indirect_mat + depreciation,
                    fo * 1.1, fo * 0.9,
                    fo + indirect_mat, fo - depreciation,
                    factory_rent + indirect_mat
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"Calculate the Factory Overhead Cost. Total Rent paid is R{rent:,}, of which {rent_factory_portion*100:.0f}% is allocated to the factory. Indirect materials used amount to R{indirect_mat:,}. Depreciation on factory plant is R{depreciation:,}."
                exp = f"Factory Rent = R{rent:,} x {rent_factory_portion*100:.0f}% = R{factory_rent:,.0f}. Factory Overheads = Factory Rent (R{factory_rent:,.0f}) + Indirect Materials (R{indirect_mat:,}) + Depreciation (R{depreciation:,}) = R{fo:,.0f}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'break_even':
                fixed_costs = random.randint(200, 2000) * 1000
                sp_per_unit = random.randint(150, 1500)
                vc_per_unit = int(sp_per_unit * random.uniform(0.4, 0.7))

                contribution = sp_per_unit - vc_per_unit
                bep = math.ceil(fixed_costs / contribution)

                correct_str = f"{bep:,} units"

                wrong_pool_vals = [
                    fixed_costs / sp_per_unit,
                    fixed_costs / vc_per_unit,
                    (fixed_costs + vc_per_unit) / sp_per_unit,
                    bep * 1.1, bep * 0.9,
                    bep + 500, bep - 500,
                    bep * 1.5
                ]
                wrong_pool = [f"{int(w):,} units" for w in wrong_pool_vals]

                q_text = f"Total Fixed Costs are R{fixed_costs:,}. The Selling Price per unit is R{sp_per_unit} and the Variable Cost per unit is R{vc_per_unit}. Calculate the Break-Even Point in units."
                exp = f"Contribution per unit = Selling Price (R{sp_per_unit}) - Variable Cost (R{vc_per_unit}) = R{contribution}. Break-Even Point = Fixed Costs / Contribution = R{fixed_costs:,} / R{contribution} = {bep:,} units."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

        return added

    def _generate_inventory_questions(self):
        subtopic_name = "Inventory Valuation"
        attempts = 0
        added = 0

        while attempts < 50000 and self.generator.difficulty_counts['medium'] + self.generator.difficulty_counts['hard'] < self.generator.difficulty_targets['medium'] + self.generator.difficulty_targets['hard']:
            attempts += 1

            q_type = random.choice(['fifo', 'weighted_average', 'stock_missing'])
            difficulty = random.choice(["easy", "easy", "medium", "hard"])

            if q_type == 'fifo':
                units_open = random.randint(100, 1000)
                price_open = random.randint(50, 100)

                units_p1 = random.randint(200, 500)
                price_p1 = price_open + random.randint(5, 15)

                units_p2 = random.randint(300, 600)
                price_p2 = price_p1 + random.randint(5, 15)

                units_sold = random.randint(400, 800)
                units_closing = (units_open + units_p1 + units_p2) - units_sold

                if difficulty == "medium":
                    # Simple closing stock value using FIFO
                    # Assuming units_closing is less than units_p2 for simplicity, or splits
                    if units_closing <= units_p2:
                        val = units_closing * price_p2
                        exp = f"Closing units = {units_closing}. Under FIFO, these come from the latest batch (Batch 2). Value = {units_closing} x R{price_p2} = R{val:,}."
                    else:
                        rem = units_closing - units_p2
                        val = (units_p2 * price_p2) + (rem * price_p1)
                        exp = f"Closing units = {units_closing}. Under FIFO, {units_p2} come from Batch 2 (R{price_p2}) and {rem} from Batch 1 (R{price_p1}). Value = (R{units_p2*price_p2:,}) + (R{rem*price_p1:,}) = R{val:,}."

                    correct_str = f"R{val:,}"
                    wrong_pool_vals = [
                        units_closing * price_open,
                        units_closing * price_p1,
                        units_closing * ((price_open + price_p1 + price_p2)/3),
                        val * 1.1, val * 0.9,
                        val + price_p2*10, val - price_p2*10,
                        units_closing * (price_p2 + 5)
                    ]
                    wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                    q_text = f"Calculate the value of Closing Stock using the FIFO method. Opening Stock: {units_open} units @ R{price_open}. Batch 1 Purchases: {units_p1} units @ R{price_p1}. Batch 2 Purchases: {units_p2} units @ R{price_p2}. Total units sold: {units_sold}."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1
                else:
                    # Hard: Carriage or returns included
                    returns = random.randint(10, 30) # from Batch 2
                    carriage_p1_total = random.randint(500, 2000)

                    units_closing_adj = (units_open + units_p1 + (units_p2 - returns)) - units_sold

                    price_p1_adj = price_p1 + (carriage_p1_total / units_p1)

                    if units_closing_adj <= (units_p2 - returns):
                        val = units_closing_adj * price_p2
                        exp = f"Closing units = {units_open} + {units_p1} + ({units_p2} - {returns}) - {units_sold} = {units_closing_adj}. From latest batch (Batch 2): {units_closing_adj} x R{price_p2} = R{val:,.2f}."
                    else:
                        rem = units_closing_adj - (units_p2 - returns)
                        val = ((units_p2 - returns) * price_p2) + (rem * price_p1_adj)
                        exp = f"Closing units = {units_closing_adj}. Batch 1 adjusted price = R{price_p1} + (R{carriage_p1_total} / {units_p1}) = R{price_p1_adj:.2f}. Value = (({units_p2} - {returns}) x R{price_p2}) + ({rem} x R{price_p1_adj:.2f}) = R{val:,.2f}."

                    correct_str = f"R{val:,.2f}"
                    wrong_pool_vals = [
                        units_closing_adj * price_p2,
                        units_closing_adj * price_p1_adj,
                        units_closing * price_p2, # ignoring returns
                        val * 1.1, val * 0.9,
                        val + 500, val - 500,
                        units_closing_adj * price_open
                    ]
                    wrong_pool = [f"R{w:,.2f}" for w in wrong_pool_vals]

                    q_text = f"Calculate Closing Stock value using FIFO. Opening: {units_open} units @ R{price_open}. Batch 1: {units_p1} units @ R{price_p1} (Total carriage for Batch 1: R{carriage_p1_total}). Batch 2: {units_p2} units @ R{price_p2}. Returns: {returns} units from Batch 2. Total sold: {units_sold}."

                    if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'weighted_average':
                units_open = random.randint(100, 1000)
                price_open = random.randint(50, 100)

                units_p = random.randint(500, 1000)
                price_p = price_open + random.randint(10, 20)
                carriage = random.randint(1000, 5000)

                total_val = (units_open * price_open) + (units_p * price_p) + carriage
                total_units = units_open + units_p

                wap = total_val / total_units

                units_sold = random.randint(400, 800)
                units_closing = total_units - units_sold

                val = units_closing * wap

                correct_str = f"R{val:,.2f}"
                wrong_pool_vals = [
                    units_closing * price_p,
                    units_closing * price_open,
                    units_closing * ((total_val - carriage) / total_units),
                    val * 1.1, val * 0.9,
                    val + 1000, val - 1000,
                    units_closing * (price_p + price_open)/2
                ]
                wrong_pool = [f"R{w:,.2f}" for w in wrong_pool_vals]

                q_text = f"Calculate Closing Stock value using the Weighted Average method. Opening Stock: {units_open} units @ R{price_open}. Purchases: {units_p} units @ R{price_p}. Carriage on purchases: R{carriage}. Total units sold: {units_sold}."
                exp = f"Total Value = (R{units_open * price_open:,}) + (R{units_p * price_p:,}) + Carriage(R{carriage}) = R{total_val:,}. Total Units = {total_units}. WAP = R{total_val:,} / {total_units} = R{wap:.2f}. Closing Stock Value = {units_closing} units x R{wap:.2f} = R{val:,.2f}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

        return added

    def _generate_financial_statement_questions(self):
        subtopic_name = "Financial Statements"
        attempts = 0
        added = 0

        while attempts < 50000 and self.generator.difficulty_counts['medium'] + self.generator.difficulty_counts['hard'] < self.generator.difficulty_targets['medium'] + self.generator.difficulty_targets['hard']:
            attempts += 1

            q_type = random.choice(['retained_income', 'ordinary_share_capital', 'trade_other_receivables', 'audit_fees'])
            difficulty = random.choice(["easy", "easy", "medium", "hard"])

            if q_type == 'retained_income':
                open_bal = random.randint(100, 500) * 1000
                net_profit = random.randint(400, 4000) * 1000
                shares_repurchased = random.randint(20, 100) * 1000
                repurchase_premium = random.randint(2, 10) # above average price
                buyback_cost_ri = shares_repurchased * repurchase_premium

                interim_div = random.randint(50, 500) * 1000
                final_div = random.randint(80, 200) * 1000

                close_bal = open_bal + net_profit - buyback_cost_ri - interim_div - final_div

                correct_str = f"R{close_bal:,}"
                wrong_pool_vals = [
                    open_bal + net_profit - interim_div - final_div,
                    open_bal + net_profit - buyback_cost_ri - final_div,
                    open_bal + net_profit,
                    close_bal + buyback_cost_ri,
                    close_bal - interim_div,
                    close_bal * 1.1, close_bal * 0.9,
                    close_bal + 50000
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"Calculate the Retained Income balance at year-end. Opening balance: R{open_bal:,}. Net profit after tax: R{net_profit:,}. {shares_repurchased:,} shares were repurchased at R{repurchase_premium} above the average share price. Interim dividends paid: R{interim_div:,}. Final dividends declared: R{final_div:,}."
                exp = f"Closing Balance = Opening (R{open_bal:,}) + Net Profit (R{net_profit:,}) - Buyback Premium (R{buyback_cost_ri:,}) - Interim Div (R{interim_div:,}) - Final Div (R{final_div:,}) = R{close_bal:,}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'ordinary_share_capital':
                auth_shares = random.randint(1000, 5000) * 1000
                issued_start = int(auth_shares * random.uniform(0.4, 0.7))
                avg_price_start = random.uniform(5.0, 15.0)

                cap_start = issued_start * avg_price_start

                new_shares = random.randint(50, 200) * 1000
                new_price = avg_price_start + random.uniform(1.0, 5.0)

                repurchased = random.randint(10, 200) * 1000

                # The repurchased shares decrease OSC by the NEW average price (or old if before issue, assume after)
                total_issued_before_buyback = issued_start + new_shares
                total_cap_before_buyback = cap_start + (new_shares * new_price)
                new_avg = total_cap_before_buyback / total_issued_before_buyback

                cap_end = total_cap_before_buyback - (repurchased * new_avg)

                correct_str = f"R{cap_end:,.0f}"

                wrong_pool_vals = [
                    total_cap_before_buyback,
                    cap_start + (new_shares * new_price) - (repurchased * new_price), # wrong buyback deduction
                    cap_start + (new_shares * new_price) - (repurchased * avg_price_start),
                    cap_end * 1.1, cap_end * 0.9,
                    cap_end + 100000, cap_end - 100000,
                    cap_start + (new_shares * new_avg)
                ]
                wrong_pool = [f"R{int(w):,.0f}" for w in wrong_pool_vals]

                q_text = f"Opening Share Capital: {issued_start:,} shares valued at R{cap_start:,.0f}. During the year, {new_shares:,} new shares were issued at R{new_price:.2f} each. Later, {repurchased:,} shares were repurchased. Calculate the Ordinary Share Capital balance at year-end."
                exp = f"Value before buyback = R{cap_start:,.0f} + (R{new_price:.2f} x {new_shares:,}) = R{total_cap_before_buyback:,.0f}. New Average Price = R{total_cap_before_buyback:,.0f} / {total_issued_before_buyback:,} = R{new_avg:.2f}. Buyback deduction = {repurchased:,} x R{new_avg:.2f} = R{repurchased * new_avg:,.0f}. Final Capital = R{cap_end:,.0f}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'trade_other_receivables':
                debtors_control = random.randint(150, 1500) * 1000
                prov_bad_debts = random.randint(5, 15) * 1000
                prepaid_exp = random.randint(2, 10) * 1000
                accrued_inc = random.randint(3, 12) * 1000
                sars_income_tax_dr = random.choice([0, random.randint(10, 30) * 1000])

                total = debtors_control - prov_bad_debts + prepaid_exp + accrued_inc + sars_income_tax_dr

                correct_str = f"R{total:,}"

                wrong_pool_vals = [
                    debtors_control + prov_bad_debts + prepaid_exp + accrued_inc + sars_income_tax_dr,
                    debtors_control - prov_bad_debts - prepaid_exp + accrued_inc,
                    debtors_control + prepaid_exp + accrued_inc,
                    total - sars_income_tax_dr * 2,
                    total * 1.1, total * 0.9,
                    total + 5000, total - 5000
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"Calculate Trade and Other Receivables. Debtors Control: R{debtors_control:,}. Provision for Bad Debts: R{prov_bad_debts:,}. Prepaid Expenses: R{prepaid_exp:,}. Accrued Income: R{accrued_inc:,}. SARS (Income Tax) Debit balance: R{sars_income_tax_dr:,}."
                exp = f"Trade & Other Receivables = Debtors (R{debtors_control:,}) - Provision (R{prov_bad_debts:,}) + Prepaid Exp (R{prepaid_exp:,}) + Accrued Inc (R{accrued_inc:,}) + SARS Debit (R{sars_income_tax_dr:,}) = R{total:,}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

        return added

    def _generate_budgeting_questions(self):
        subtopic_name = "Budgeting"
        attempts = 0
        added = 0

        while attempts < 50000 and self.generator.difficulty_counts['medium'] + self.generator.difficulty_counts['hard'] < self.generator.difficulty_targets['medium'] + self.generator.difficulty_targets['hard']:
            attempts += 1

            q_type = random.choice(['debtors_collection', 'creditors_payment', 'cash_vs_income'])
            difficulty = random.choice(["easy", "easy", "medium", "hard"])

            if q_type == 'debtors_collection':
                credit_sales_1 = random.randint(100, 1000) * 1000 # 2 months ago
                credit_sales_2 = random.randint(150, 350) * 1000 # 1 month ago
                credit_sales_3 = random.randint(200, 400) * 1000 # current month

                col_curr = random.choice([20, 30])
                col_1 = random.choice([40, 50])
                col_2 = random.choice([15, 20])
                discount = random.choice([0, 5])

                curr_collected = credit_sales_3 * (col_curr/100)
                if discount > 0:
                    # Discount usually applied in month of sale
                    curr_collected = curr_collected * (1 - (discount/100))

                prev1_collected = credit_sales_2 * (col_1/100)
                prev2_collected = credit_sales_1 * (col_2/100)

                total = curr_collected + prev1_collected + prev2_collected

                correct_str = f"R{total:,.0f}"

                wrong_pool_vals = [
                    (credit_sales_3 * (col_curr/100)) + prev1_collected + prev2_collected, # no discount
                    credit_sales_3 * (col_1/100) + credit_sales_2 * (col_2/100), # shifted months
                    total * 1.1, total * 0.9,
                    total + 10000, total - 10000,
                    total + 5000, total - 5000
                ]
                wrong_pool = [f"R{int(w):,.0f}" for w in wrong_pool_vals]

                q_text = f"Credit sales: May R{credit_sales_1:,}, June R{credit_sales_2:,}, July R{credit_sales_3:,}. Collection pattern: {col_curr}% in month of sale (subject to {discount}% discount), {col_1}% in the 1st month after sale, {col_2}% in the 2nd month after. Calculate the cash collected from debtors in July."
                exp = f"July sales collected = R{credit_sales_3:,} x {col_curr}% x {(100-discount)}% = R{curr_collected:,.0f}. June sales collected = R{credit_sales_2:,} x {col_1}% = R{prev1_collected:,.0f}. May sales collected = R{credit_sales_1:,} x {col_2}% = R{prev2_collected:,.0f}. Total = R{total:,.0f}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'creditors_payment':
                purchases = random.randint(150, 1500) * 1000
                cash_perc = random.choice([20, 30, 40])
                credit_purchases = purchases * ((100 - cash_perc) / 100)

                pay_perc = random.choice([60, 75, 100])
                paid = credit_purchases * (pay_perc / 100)

                correct_str = f"R{paid:,.0f}"

                wrong_pool_vals = [
                    credit_purchases,
                    purchases * (pay_perc/100),
                    purchases * (cash_perc/100),
                    paid * 1.1, paid * 0.9,
                    paid + 5000, paid - 5000,
                    purchases * ((100 - cash_perc) / 100) * 1.5
                ]
                wrong_pool = [f"R{int(w):,.0f}" for w in wrong_pool_vals]

                q_text = f"Total purchases for July are R{purchases:,}, of which {cash_perc}% is for cash. Creditors are paid {pay_perc}% of the credit purchases in the month following the purchase (August). Calculate the amount paid to creditors in August for July purchases."
                exp = f"Credit Purchases = R{purchases:,} x {(100 - cash_perc)}% = R{credit_purchases:,.0f}. Amount Paid = R{credit_purchases:,.0f} x {pay_perc}% = R{paid:,.0f}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

        return added

    def _generate_cashflow_questions(self):
        subtopic_name = "Cash Flow Statements"
        attempts = 0
        added = 0

        while attempts < 50000 and self.generator.difficulty_counts['medium'] + self.generator.difficulty_counts['hard'] < self.generator.difficulty_targets['medium'] + self.generator.difficulty_targets['hard']:
            attempts += 1

            q_type = random.choice(['tax_paid', 'dividends_paid', 'fixed_assets_purchased'])
            difficulty = random.choice(["easy", "easy", "medium", "hard"])

            if q_type == 'tax_paid':
                tax_expense = random.randint(50, 200) * 1000
                open_cr = random.randint(5, 30) * 1000
                expense = random.randint(100, 1000) * 1000
                close_cr = random.randint(10, 40) * 1000

                tax_paid = open_cr + expense - close_cr
                correct_str = f"R{tax_paid:,}"

                wrong_pool_vals = [
                    expense,
                    expense + close_cr - open_cr,
                    open_cr + close_cr + expense,
                    tax_paid * 1.1, tax_paid * 0.9,
                    tax_paid + 2000, tax_paid - 2000,
                    close_cr + open_cr
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"Income Tax expense for the year is R{expense:,}. SARS (Income Tax) had an opening credit balance of R{open_cr:,} and a closing credit balance of R{close_cr:,}. Calculate Taxation Paid for the Cash Flow Statement."
                exp = f"Tax Paid = Opening Balance (R{open_cr:,}) + Tax Expense (R{expense:,}) - Closing Balance (R{close_cr:,}) = R{tax_paid:,}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'dividends_paid':
                final_prev = random.randint(30, 80) * 1000
                interim_curr = random.randint(40, 90) * 1000
                final_curr = random.randint(50, 100) * 1000

                paid = final_prev + interim_curr
                correct_str = f"R{paid:,}"

                wrong_pool_vals = [
                    interim_curr + final_curr,
                    final_prev + final_curr,
                    final_prev + interim_curr + final_curr,
                    paid * 1.1, paid * 0.9,
                    paid + 5000, paid - 5000,
                    final_curr
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"Shareholders for dividends opening balance was R{final_prev:,} (final dividend from last year). During the current year, an interim dividend of R{interim_curr:,} was paid, and a final dividend of R{final_curr:,} was declared. Calculate Dividends Paid for the Cash Flow Statement."
                exp = f"Dividends Paid = Final dividend from previous year (R{final_prev:,}) + Interim dividend paid this year (R{interim_curr:,}) = R{paid:,}. The current year's final dividend is only paid next year."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'fixed_assets_purchased':
                carrying_value_start = random.randint(1000, 10000) * 1000
                carrying_value_end = random.randint(1500, 15000) * 1000
                depreciation = random.randint(100, 1000) * 1000
                disposals = random.randint(50, 200) * 1000

                purchases = carrying_value_end - carrying_value_start + depreciation + disposals

                correct_str = f"R{purchases:,}"

                wrong_pool_vals = [
                    carrying_value_end - carrying_value_start,
                    carrying_value_end - carrying_value_start + depreciation,
                    carrying_value_end - carrying_value_start - disposals,
                    carrying_value_end - carrying_value_start - depreciation + disposals,
                    purchases * 1.1, purchases * 0.9,
                    purchases + 20000, purchases - 20000
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"Fixed assets carrying value at start: R{carrying_value_start:,}. At end: R{carrying_value_end:,}. Depreciation for the year: R{depreciation:,}. Carrying value of assets sold: R{disposals:,}. Calculate the amount paid to purchase fixed assets."
                exp = f"Purchases = Closing CV (R{carrying_value_end:,}) - Opening CV (R{carrying_value_start:,}) + Depreciation (R{depreciation:,}) + Disposals (R{disposals:,}) = R{purchases:,}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

        return added

    def _generate_reconciliation_questions(self):
        subtopic_name = "Reconciliations"
        attempts = 0
        added = 0

        while attempts < 50000 and self.generator.difficulty_counts['medium'] + self.generator.difficulty_counts['hard'] < self.generator.difficulty_targets['medium'] + self.generator.difficulty_targets['hard']:
            attempts += 1

            q_type = random.choice(['bank_recon_balance', 'bank_recon_error', 'debtors_recon'])
            difficulty = random.choice(["easy", "easy", "medium", "hard"])

            if q_type == 'bank_recon_balance':
                bank_balance = random.randint(10, 200) * 1000
                outstanding_cheque = random.randint(1, 30) * 1000
                outstanding_deposit = random.randint(2, 40) * 1000

                recon_balance = bank_balance + outstanding_deposit - outstanding_cheque
                correct_str = f"R{recon_balance:,} favourable"

                wrong_pool_vals = [
                    f"R{bank_balance - outstanding_deposit + outstanding_cheque:,} favourable",
                    f"R{bank_balance + outstanding_deposit + outstanding_cheque:,} favourable",
                    f"R{recon_balance:,} overdrawn",
                    f"R{bank_balance:,} favourable",
                    f"R{bank_balance + outstanding_deposit:,} favourable",
                    f"R{bank_balance - outstanding_cheque:,} favourable",
                    f"R{recon_balance + 1000:,} favourable",
                    f"R{abs(recon_balance - 1000):,} favourable"
                ]
                wrong_pool = list(wrong_pool_vals)

                q_text = f"The Bank Statement shows a favourable balance of R{bank_balance:,}. Outstanding cheques: R{outstanding_cheque:,}. Outstanding deposit: R{outstanding_deposit:,}. Calculate the balance as per the Bank account in the General Ledger."
                exp = f"GL Balance = Bank Statement Balance (R{bank_balance:,}) + Outstanding Deposits (R{outstanding_deposit:,}) - Outstanding Cheques (R{outstanding_cheque:,}) = R{recon_balance:,} favourable."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

            elif q_type == 'debtors_recon':
                control_bal_start = random.randint(50, 500) * 1000
                invoice_omitted = random.randint(1, 30) * 1000

                corrected_control = control_bal_start + invoice_omitted
                correct_str = f"R{corrected_control:,}"

                wrong_pool_vals = [
                    control_bal_start,
                    control_bal_start - invoice_omitted,
                    control_bal_start + (invoice_omitted*2),
                    corrected_control * 1.1, corrected_control * 0.9,
                    corrected_control + 500, corrected_control - 500,
                    invoice_omitted
                ]
                wrong_pool = [f"R{int(w):,}" for w in wrong_pool_vals]

                q_text = f"The Debtors Control account balance is R{control_bal_start:,}. It was discovered that an invoice for R{invoice_omitted:,} was completely omitted from the Debtors Journal. Calculate the corrected Debtors Control balance."
                exp = f"Omitted invoice means credit sales were undercast. We must add the invoice amount to the control account: R{control_bal_start:,} + R{invoice_omitted:,} = R{corrected_control:,}."

                if self.generator.add_question(subtopic_name, difficulty, q_text, correct_str, wrong_pool, exp): added += 1

        return added


    def build(self, output_dir):
        # We need 1000 questions in total: 300 easy, 500 medium, 200 hard
        self.generate_theory_questions(300)

        # Procedural questions for the remaining 700
        if "Analysis" in self.topic:
            self._generate_analysis_questions()
        elif "Manufacturing" in self.topic:
            self._generate_manufacturing_questions()
        elif "Inventory" in self.topic:
            self._generate_inventory_questions()
        elif "Companies" in self.topic or "Financial Statements" in self.topic:
            self._generate_financial_statement_questions()
        elif "Budgeting" in self.topic:
            self._generate_budgeting_questions()
        elif "Cash Flow" in self.topic:
            self._generate_cashflow_questions()
        elif "Reconciliations" in self.topic:
            self._generate_reconciliation_questions()

        # Fallback to make up numbers if we somehow missed the targets
        # We will loop through the available procedural methods and keep calling them until done
        attempts = 0
        while not self.generator.is_done() and attempts < 50000:
            attempts += 1
            if "Analysis" in self.topic: self._generate_analysis_questions()
            elif "Manufacturing" in self.topic: self._generate_manufacturing_questions()
            elif "Inventory" in self.topic: self._generate_inventory_questions()
            elif "Companies" in self.topic or "Financial Statements" in self.topic: self._generate_financial_statement_questions()
            elif "Budgeting" in self.topic: self._generate_budgeting_questions()
            elif "Cash Flow" in self.topic: self._generate_cashflow_questions()
            elif "Reconciliations" in self.topic: self._generate_reconciliation_questions()

        filepath = os.path.join(output_dir, self.file)
        self.generator.save_to_json(filepath)
        print(f"Generated {len(self.generator.questions)} questions for {self.topic} -> {filepath}")

def main():
    kb = AccountingKnowledgeBase()
    output_dir = "dataset/grade12/accounting"
    os.makedirs(output_dir, exist_ok=True)

    for topic_data in kb.get_topics():
        engine = AdvancedAccountingQuestionEngine(topic_data)
        engine.build(output_dir)

if __name__ == "__main__":
    main()
