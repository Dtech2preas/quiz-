import json
import random
import os
import hashlib
from typing import List, Dict

# Helpers import
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'generators/helpers'))

class AccountingKnowledgeBase:
    def __init__(self, json_path="extracted_topics_accounting.json"):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_topics(self):
        return self.data

class AccountingQuestionEngine:
    def __init__(self, topic_data):
        self.topic = topic_data['topic']
        self.prefix = topic_data['prefix']
        self.file = topic_data['file']
        self.subtopics = topic_data['subtopics']
        self.questions = []
        self.generated_hashes = set()

    def generate_hash(self, question_text, correct_answer):
        hash_input = f"{question_text}|{correct_answer}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

    def add_question(self, question_text, correct_answer, wrong_answers_pool, explanation, difficulty, subtopic_name, l_outcome="Financial Analysis"):
        q_hash = self.generate_hash(question_text, correct_answer)
        if q_hash in self.generated_hashes:
            return False

        self.generated_hashes.add(q_hash)

        q_id = f"{self.prefix}_{len(self.questions) + 1:04d}"

        question = {
            "id": q_id,
            "question": question_text,
            "correct_answer": correct_answer,
            "wrong_answers_pool": wrong_answers_pool,
            "explanation": explanation,
            "tags": {
                "grade": "12",
                "subject": "Accounting",
                "topic": self.topic,
                "subtopic": subtopic_name,
                "cognitive_level": "Knowledge" if difficulty == "easy" else ("Application" if difficulty == "medium" else "Analysis"),
                "difficulty": difficulty,
                "learning_outcome": l_outcome
            }
        }
        self.questions.append(question)
        return True

    def generate_theory_questions(self, target_count=500):
        added = 0
        attempts = 0
        while added < target_count and attempts < target_count * 5:
            attempts += 1
            subtopic = random.choice(self.subtopics)
            if not subtopic['facts']:
                continue
            fact = random.choice(subtopic['facts'])

            q_type = random.choice([1, 2, 3])

            if q_type == 1:
                # Type 1: Definition -> Term
                q_text = f"Which accounting term is defined as: {fact['desc']}?"
                correct = fact['a']
                wrong = random.sample(fact['w'], min(3, len(fact['w'])))
                exp = f"The correct term is {correct}."
            elif q_type == 2:
                # Type 2: Term -> Definition
                q_text = f"What is the correct definition or description for the term '{fact['a']}'?"
                correct = fact['desc']

                # We need plausible distractors for definitions. Let's pull descriptions from other facts in the same subtopic if possible, or general.
                other_facts = [f for f in subtopic['facts'] if f['a'] != fact['a']]
                wrong_desc = []
                for of in other_facts:
                    wrong_desc.append(of['desc'])

                # If we don't have enough, pull from whole KB or use generic ones
                if len(wrong_desc) < 3:
                    wrong_desc.extend([
                        "a metric used solely for internal cost analysis",
                        "a statutory requirement that applies only to close corporations",
                        "the process of reconciling external audit reports with internal budgets",
                        "a financial indicator showing the exact amount of cash on hand"
                    ])
                wrong = random.sample(wrong_desc, min(3, len(wrong_desc)))
                exp = f"'{fact['a']}' means: {correct}."
            else:
                # Type 3: True/False style statement
                is_true = random.choice([True, False])
                if is_true:
                    q_text = f"Which of the following statements about '{fact['a']}' is CORRECT?"
                    correct = fact['desc']
                    other_facts = [f for f in subtopic['facts'] if f['a'] != fact['a']]
                    wrong_desc = [of['desc'] for of in other_facts]
                    if len(wrong_desc) < 3:
                         wrong_desc.extend(["It is only applicable to non-profit organizations.", "It represents a physical asset.", "It is recorded as an expense in the Statement of Comprehensive Income.", "It does not affect the financial statements."])
                    wrong = random.sample(wrong_desc, min(3, len(wrong_desc)))
                    exp = f"The correct statement is that it is {fact['desc']}."
                else:
                    q_text = f"Which of the following terms is INCORRECTLY matched with its description?"
                    correct = f"{fact['a']}: {random.choice(fact['w'])} (Incorrect)" # This is a wrong description matched with the term

                    # The right ones to use as distractors (because we are asking for the INCORRECT one, the distractors must be CORRECT matches)
                    other_facts = [f for f in subtopic['facts'] if f['a'] != fact['a']]
                    if len(other_facts) >= 3:
                        sample_facts = random.sample(other_facts, 3)
                        wrong = [f"{sf['a']}: {sf['desc']}" for sf in sample_facts]
                    else:
                         wrong = [f"{fact['a']}: {fact['desc']}", "Asset: A resource controlled by the entity", "Liability: A present obligation of the entity"]

                    exp = f"The incorrect match is {fact['a']}. Its actual description is: {fact['desc']}."


            if self.add_question(q_text, correct, wrong, exp, "easy", subtopic['name'], "Recall Principles"):
                added += 1

    def generate_procedural_questions(self, target_count=500):
        added = 0
        attempts = 0

        while added < target_count and attempts < target_count * 10:
            attempts += 1

            # Procedural Generation Based on Topic
            if "Analysis" in self.topic:
                added += self._generate_analysis_questions()
            elif "Manufacturing" in self.topic:
                added += self._generate_manufacturing_questions()
            elif "Inventory" in self.topic:
                added += self._generate_inventory_questions()
            elif "Companies" in self.topic or "Financial Statements" in self.topic:
                added += self._generate_financial_statement_questions()
            elif "Budgeting" in self.topic:
                added += self._generate_budgeting_questions()
            elif "Cash Flow" in self.topic:
                added += self._generate_cashflow_questions()
            elif "Reconciliations" in self.topic:
                added += self._generate_reconciliation_questions()
            else:
                self.generate_theory_questions(1)
                added += 1

    def _generate_analysis_questions(self):
        q_type = random.choice(['current_ratio', 'acid_test', 'stock_turnover', 'debt_equity', 'rotce', 'eps', 'nav'])

        if q_type == 'current_ratio':
            current_assets = random.randint(100, 900) * 1000
            current_liabilities = random.randint(50, 400) * 1000
            ratio = current_assets / current_liabilities
            correct_str = f"{ratio:.2f}:1"
            distractor1 = f"{(current_liabilities / current_assets):.2f}:1"
            distractor2 = f"{(ratio + 0.5):.2f}:1"
            distractor3 = f"{(ratio - 0.2):.2f}:1"
            distractor4 = f"{ratio:.1f}:1"
            wrong_pool = [d for d in [distractor1, distractor2, distractor3, distractor4] if d != correct_str]
            q_text = f"A company has current assets of R{current_assets:,} and current liabilities of R{current_liabilities:,}. Calculate the current ratio."
            exp = f"Current Ratio = Current Assets / Current Liabilities = R{current_assets:,} / R{current_liabilities:,} = {ratio:.2f}:1"
            if self.add_question(q_text, correct_str, list(set(wrong_pool)), exp, "medium", "Liquidity Indicators"):
                return 1

        elif q_type == 'acid_test':
            current_assets = random.randint(200, 900) * 1000
            inventory = random.randint(50, int(current_assets * 0.4))
            current_liabilities = random.randint(100, 500) * 1000
            ratio = (current_assets - inventory) / current_liabilities
            correct_str = f"{ratio:.2f}:1"
            distractor1 = f"{(current_assets / current_liabilities):.2f}:1" # Forgot inventory
            distractor2 = f"{((current_assets + inventory) / current_liabilities):.2f}:1" # Added inventory
            distractor3 = f"{(current_liabilities / (current_assets - inventory)):.2f}:1" # Flipped
            wrong_pool = [distractor1, distractor2, distractor3]
            q_text = f"Calculate the acid-test ratio if Current Assets are R{current_assets:,}, Inventory is R{inventory:,}, and Current Liabilities are R{current_liabilities:,}."
            exp = f"Acid-test Ratio = (Current Assets - Inventory) / Current Liabilities = (R{current_assets:,} - R{inventory:,}) / R{current_liabilities:,} = {ratio:.2f}:1"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Liquidity Indicators"):
                return 1

        elif q_type == 'stock_turnover':
            cost_of_sales = random.randint(500, 2000) * 1000
            avg_stock = random.randint(50, 300) * 1000
            rate = cost_of_sales / avg_stock
            correct_str = f"{rate:.1f} times"
            distractor1 = f"{(avg_stock / cost_of_sales * 365):.0f} days" # Did stock days instead
            distractor2 = f"{(rate / 2):.1f} times"
            distractor3 = f"{(rate * 12):.1f} times"
            wrong_pool = [distractor1, distractor2, distractor3]
            q_text = f"Calculate the stock turnover rate if Cost of Sales is R{cost_of_sales:,} and Average Trading Stock is R{avg_stock:,}."
            exp = f"Stock turnover rate = Cost of Sales / Average Stock = R{cost_of_sales:,} / R{avg_stock:,} = {rate:.1f} times."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Liquidity Indicators"):
                return 1

        elif q_type == 'debt_equity':
            ncl = random.randint(500, 2000) * 1000
            sh_equity = random.randint(800, 3000) * 1000
            ratio = ncl / sh_equity
            correct_str = f"{ratio:.2f}:1"
            distractor1 = f"{(sh_equity / ncl):.2f}:1" # Flipped
            distractor2 = f"{(ncl / (sh_equity + ncl)):.2f}:1"
            distractor3 = f"{(ratio + 0.3):.2f}:1"
            wrong_pool = [distractor1, distractor2, distractor3]
            q_text = f"Calculate the debt-equity ratio if Non-Current Liabilities are R{ncl:,} and Shareholders' Equity is R{sh_equity:,}."
            exp = f"Debt-equity Ratio = Non-Current Liabilities / Shareholders' Equity = R{ncl:,} / R{sh_equity:,} = {ratio:.2f}:1"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Solvency & Risk Indicators"):
                return 1

        elif q_type == 'rotce':
            net_profit_before_tax = random.randint(200, 800) * 1000
            interest = random.randint(20, 100) * 1000
            avg_capital = random.randint(1500, 4000) * 1000
            ebit = net_profit_before_tax + interest
            rotce = (ebit / avg_capital) * 100
            correct_str = f"{rotce:.1f}%"
            distractor1 = f"{((net_profit_before_tax / avg_capital) * 100):.1f}%" # Forgot interest
            distractor2 = f"{(((net_profit_before_tax - interest) / avg_capital) * 100):.1f}%" # Subtracted interest
            distractor3 = f"{(rotce + 5):.1f}%"
            wrong_pool = [distractor1, distractor2, distractor3]
            q_text = f"Calculate the Return on Total Capital Employed (ROTCE) if Net Profit Before Tax is R{net_profit_before_tax:,}, Interest Expense is R{interest:,}, and Average Capital Employed is R{avg_capital:,}."
            exp = f"ROTCE = (Net Profit Before Tax + Interest Expense) / Average Capital Employed * 100 = (R{net_profit_before_tax:,} + R{interest:,}) / R{avg_capital:,} * 100 = {rotce:.1f}%"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Profitability Indicators"):
                return 1

        elif q_type == 'eps':
            net_profit_after_tax = random.randint(300, 1200) * 1000
            shares = random.randint(200, 1000) * 1000
            eps = (net_profit_after_tax / shares) * 100
            correct_str = f"{eps:.0f} cents"
            distractor1 = f"{(eps / 100):.2f} cents"
            distractor2 = f"{((net_profit_after_tax / (shares*2)) * 100):.0f} cents"
            distractor3 = f"{(eps + 20):.0f} cents"
            wrong_pool = [distractor1, distractor2, distractor3]
            q_text = f"A company has a Net Profit After Tax of R{net_profit_after_tax:,} and {shares:,} issued ordinary shares. Calculate the Earnings Per Share (EPS)."
            exp = f"EPS = (Net Profit After Tax / Number of Issued Shares) * 100 = (R{net_profit_after_tax:,} / {shares:,}) * 100 = {eps:.0f} cents."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Shareholder Returns"):
                return 1

        elif q_type == 'nav':
            sh_equity = random.randint(1500, 5000) * 1000
            shares = random.randint(200, 800) * 1000
            nav = (sh_equity / shares) * 100
            correct_str = f"{nav:.0f} cents"
            distractor1 = f"{(nav / 100):.2f} cents"
            distractor2 = f"{(nav + 50):.0f} cents"
            distractor3 = f"{(nav * 1.5):.0f} cents"
            wrong_pool = [distractor1, distractor2, distractor3]
            q_text = f"Calculate the Net Asset Value (NAV) per share if Shareholders' Equity is R{sh_equity:,} and there are {shares:,} issued shares."
            exp = f"NAV = (Shareholders' Equity / Number of Issued Shares) * 100 = (R{sh_equity:,} / {shares:,}) * 100 = {nav:.0f} cents."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Shareholder Returns"):
                return 1

        return 0

    def _generate_manufacturing_questions(self):
        q_type = random.choice(['prime_cost', 'factory_overhead', 'total_cost', 'cost_of_production', 'breakeven', 'unit_cost'])

        if q_type == 'prime_cost':
            direct_materials = random.randint(100, 500) * 1000
            direct_labour = random.randint(50, 300) * 1000
            factory_overhead = random.randint(20, 150) * 1000
            prime_cost = direct_materials + direct_labour
            correct_str = f"R{prime_cost:,}"
            wrong_pool = [f"R{(prime_cost + factory_overhead):,}", f"R{(direct_materials + factory_overhead):,}", f"R{(direct_labour + factory_overhead):,}"]
            q_text = f"Calculate the Prime Cost: Direct Materials R{direct_materials:,}, Direct Labour R{direct_labour:,}, Factory Overheads R{factory_overhead:,}."
            exp = f"Prime Cost = Direct Materials + Direct Labour = R{prime_cost:,}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "easy", "Manufacturing Concepts"): return 1

        elif q_type == 'factory_overhead':
            indirect_materials = random.randint(5, 30) * 1000
            indirect_labour = random.randint(10, 50) * 1000
            factory_rent = random.randint(20, 80) * 1000
            direct_materials = random.randint(100, 300) * 1000
            overhead = indirect_materials + indirect_labour + factory_rent
            correct_str = f"R{overhead:,}"
            wrong_pool = [f"R{(overhead + direct_materials):,}", f"R{(indirect_materials + indirect_labour):,}", f"R{(overhead - factory_rent):,}"]
            q_text = f"Calculate Total Factory Overheads: Indirect Materials R{indirect_materials:,}, Indirect Labour R{indirect_labour:,}, Factory Rent R{factory_rent:,}, Direct Materials R{direct_materials:,}."
            exp = f"Factory Overheads = Indirect Materials + Indirect Labour + Factory Rent = R{overhead:,}. Direct materials are a direct cost."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Manufacturing Concepts"): return 1

        elif q_type == 'cost_of_production':
            total_manufacturing_cost = random.randint(500, 1500) * 1000
            wip_start = random.randint(20, 100) * 1000
            wip_end = random.randint(30, 120) * 1000
            cop = total_manufacturing_cost + wip_start - wip_end
            correct_str = f"R{cop:,}"
            wrong_pool = [f"R{(total_manufacturing_cost + wip_start + wip_end):,}", f"R{(total_manufacturing_cost - wip_start + wip_end):,}", f"R{total_manufacturing_cost:,}"]
            q_text = f"Calculate the Cost of Production of Finished Goods if Total Manufacturing Cost is R{total_manufacturing_cost:,}, WIP at start is R{wip_start:,}, and WIP at end is R{wip_end:,}."
            exp = f"Cost of Production = Total Manufacturing Cost (R{total_manufacturing_cost:,}) + WIP Start (R{wip_start:,}) - WIP End (R{wip_end:,}) = R{cop:,}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Manufacturing Concepts"): return 1

        elif q_type == 'breakeven':
            fixed_costs = random.randint(100, 500) * 1000
            selling_price = random.randint(50, 200)
            variable_cost = selling_price - random.randint(10, 40)
            contribution = selling_price - variable_cost
            bep = fixed_costs / contribution
            correct_str = f"{bep:,.0f} units"
            wrong_pool = [f"{(fixed_costs / selling_price):,.0f} units", f"{(fixed_costs / variable_cost):,.0f} units", f"{((fixed_costs + variable_cost) / selling_price):,.0f} units"]
            q_text = f"Calculate the break-even point in units. Total Fixed Costs: R{fixed_costs:,}, Selling Price per unit: R{selling_price}, Variable Cost per unit: R{variable_cost}."
            exp = f"Break-even Point = Fixed Costs / (Selling Price - Variable Cost) = R{fixed_costs:,} / (R{selling_price} - R{variable_cost}) = {bep:,.0f} units."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Break-Even Analysis"): return 1

        elif q_type == 'unit_cost':
            cop = random.randint(500, 2000) * 1000
            units = random.randint(10, 50) * 1000
            unit_cost = cop / units
            correct_str = f"R{unit_cost:.2f}"
            wrong_pool = [f"R{(unit_cost + 5):.2f}", f"R{(unit_cost * 1.5):.2f}", f"R{(unit_cost - 2):.2f}"]
            q_text = f"If the Cost of Production is R{cop:,} and {units:,} units were produced, calculate the unit cost of production."
            exp = f"Unit Cost = Cost of Production / Units Produced = R{cop:,} / {units:,} = R{unit_cost:.2f}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "easy", "Manufacturing Concepts"): return 1

        return 0

    def _generate_inventory_questions(self):
        q_type = random.choice(['fifo', 'weighted_avg', 'missing_stock', 'gross_profit'])

        if q_type == 'weighted_avg':
            units_opening = random.randint(50, 150)
            cost_opening = random.randint(10, 50)
            total_opening = units_opening * cost_opening

            units_purchased = random.randint(100, 300)
            cost_purchased = cost_opening + random.randint(5, 20)
            total_purchased = units_purchased * cost_purchased

            total_units = units_opening + units_purchased
            total_cost = total_opening + total_purchased

            weighted_avg = total_cost / total_units
            correct_str = f"R{weighted_avg:.2f}"
            wrong_pool = [f"R{((cost_opening + cost_purchased)/2):.2f}", f"R{cost_purchased:.2f}", f"R{(total_cost / units_purchased):.2f}"]
            q_text = f"Opening stock is {units_opening} units at R{cost_opening} each. Purchases are {units_purchased} units at R{cost_purchased} each. Calculate the weighted average cost per unit."
            exp = f"Total Cost = R{total_cost}. Total Units = {total_units}. Weighted Average = R{total_cost} / {total_units} = R{weighted_avg:.2f}"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Valuation Methods"): return 1

        elif q_type == 'fifo':
            units_purchased_late = random.randint(100, 200)
            price_late = random.randint(40, 60)
            units_purchased_early = random.randint(150, 250)
            price_early = random.randint(20, 35)
            closing_units = random.randint(50, units_purchased_late - 10)

            val = closing_units * price_late
            correct_str = f"R{val:,}"
            wrong_pool = [f"R{(closing_units * price_early):,}", f"R{(closing_units * ((price_late+price_early)/2)):,.0f}", f"R{(units_purchased_late * price_late):,}"]
            q_text = f"Using FIFO, calculate the value of closing stock of {closing_units} units. The latest purchase was {units_purchased_late} units at R{price_late} each. The previous purchase was {units_purchased_early} units at R{price_early} each."
            exp = f"Under FIFO, closing stock is valued at the latest prices. Closing Stock = {closing_units} units x R{price_late} = R{val:,}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Valuation Methods"): return 1

        elif q_type == 'missing_stock':
            open_stock = random.randint(100, 300)
            purchases = random.randint(500, 1000)
            returns = random.randint(10, 50)
            sales_units = random.randint(400, 800)
            counted = (open_stock + purchases - returns - sales_units) - random.randint(5, 20)

            missing = open_stock + purchases - returns - sales_units - counted
            correct_str = f"{missing} units"
            wrong_pool = [f"{(missing + 10)} units", f"{(open_stock + purchases - counted)} units", f"{(sales_units - counted)} units"]
            q_text = f"Opening stock: {open_stock} units. Purchases: {purchases} units. Returns to suppliers: {returns} units. Sales: {sales_units} units. Stock counted at year end: {counted} units. Calculate the number of missing units."
            exp = f"Expected stock = Opening ({open_stock}) + Purchases ({purchases}) - Returns ({returns}) - Sales ({sales_units}) = {open_stock + purchases - returns - sales_units}. Missing = Expected - Counted ({counted}) = {missing} units."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Inventory Systems"): return 1

        elif q_type == 'gross_profit':
            sales = random.randint(500, 2000) * 1000
            markup = random.choice([20, 25, 33, 50])

            cost_of_sales = sales * (100 / (100 + markup))
            gp = sales - cost_of_sales
            correct_str = f"R{gp:,.0f}"
            wrong_pool = [f"R{(sales * (markup/100)):,.0f}", f"R{cost_of_sales:,.0f}", f"R{(sales - (sales * (markup/100))):,.0f}"]
            q_text = f"Sales are R{sales:,}. The business uses a mark-up of {markup}% on cost. Calculate the Gross Profit."
            exp = f"Cost of Sales = Sales x 100 / (100 + {markup}) = R{cost_of_sales:,.0f}. Gross Profit = Sales - Cost of Sales = R{gp:,.0f}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Inventory Systems"): return 1

        return 0

    def _generate_financial_statement_questions(self):
        q_type = random.choice(['retained_income', 'net_profit', 'ordinary_share_capital', 'depreciation', 'asset_disposal'])

        if q_type == 'retained_income':
            opening_retained = random.randint(100, 500) * 1000
            net_profit_after_tax = random.randint(200, 800) * 1000
            interim_dividend = random.randint(20, 100) * 1000
            final_dividend = random.randint(30, 150) * 1000

            closing_retained = opening_retained + net_profit_after_tax - interim_dividend - final_dividend
            correct_str = f"R{closing_retained:,}"
            wrong_pool = [f"R{(opening_retained + net_profit_after_tax - interim_dividend):,}", f"R{(opening_retained + net_profit_after_tax):,}", f"R{(opening_retained + net_profit_after_tax + interim_dividend + final_dividend):,}"]
            q_text = f"Opening retained income is R{opening_retained:,}. Net profit after tax is R{net_profit_after_tax:,}. Interim dividends paid: R{interim_dividend:,}. Final dividends declared: R{final_dividend:,}. Calculate the closing balance of Retained Income."
            exp = f"Closing Retained Income = Opening Balance (R{opening_retained:,}) + Net Profit after Tax (R{net_profit_after_tax:,}) - Total Dividends (R{interim_dividend + final_dividend:,}) = R{closing_retained:,}"
            sub = "Statement of Financial Position" if "Financial" in self.topic else "Company Concepts"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", sub): return 1

        elif q_type == 'net_profit':
            gross_profit = random.randint(800, 2000) * 1000
            operating_income = random.randint(50, 200) * 1000
            operating_expenses = random.randint(300, 900) * 1000
            operating_profit = gross_profit + operating_income - operating_expenses
            correct_str = f"R{operating_profit:,}"
            wrong_pool = [f"R{(gross_profit - operating_expenses):,}", f"R{(gross_profit + operating_income + operating_expenses):,}", f"R{(operating_expenses - operating_income):,}"]
            q_text = f"Gross profit is R{gross_profit:,}. Operating income is R{operating_income:,}. Operating expenses are R{operating_expenses:,}. Calculate the Operating Profit."
            exp = f"Operating Profit = Gross Profit + Operating Income - Operating Expenses = R{gross_profit:,} + R{operating_income:,} - R{operating_expenses:,} = R{operating_profit:,}."
            sub = "Statement of Comprehensive Income" if "Financial" in self.topic else "Company Concepts"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "easy", sub): return 1

        elif q_type == 'ordinary_share_capital':
            shares_start = random.randint(500, 1000) * 1000
            price_start = random.randint(2, 5)
            shares_issued = random.randint(100, 300) * 1000
            price_issued = price_start + random.randint(1, 3)

            total_capital = (shares_start * price_start) + (shares_issued * price_issued)
            correct_str = f"R{total_capital:,}"
            wrong_pool = [f"R{((shares_start + shares_issued) * price_start):,}", f"R{((shares_start + shares_issued) * price_issued):,}", f"R{(shares_start * price_start):,}"]
            q_text = f"A company started with {shares_start:,} shares issued at R{price_start} each. During the year, they issued another {shares_issued:,} shares at R{price_issued} each. Calculate the total Ordinary Share Capital balance."
            exp = f"Total Capital = (R{shares_start:,} x R{price_start}) + (R{shares_issued:,} x R{price_issued}) = R{shares_start * price_start:,} + R{shares_issued * price_issued:,} = R{total_capital:,}."
            sub = "Statement of Financial Position" if "Financial" in self.topic else "Company Concepts"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", sub): return 1

        elif q_type == 'depreciation':
            cost = random.randint(100, 500) * 1000
            acc_dep = random.randint(20, int(cost*0.4))
            rate = random.choice([10, 15, 20])

            dep = (cost - acc_dep) * (rate / 100)
            correct_str = f"R{dep:,.0f}"
            wrong_pool = [f"R{(cost * (rate/100)):,.0f}", f"R{(acc_dep * (rate/100)):,.0f}", f"R{((cost - acc_dep)):,.0f}"]
            q_text = f"Vehicles cost R{cost:,}. Accumulated depreciation is R{acc_dep:,}. Calculate depreciation for the year at {rate}% p.a. on the diminishing balance method."
            exp = f"Depreciation = (Cost - Accumulated Depreciation) x Rate = (R{cost:,} - R{acc_dep:,}) x {rate}% = R{dep:,.0f}."
            sub = "Notes to Financial Statements" if "Financial" in self.topic else "Company Concepts"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", sub): return 1

        elif q_type == 'asset_disposal':
            cost = random.randint(50, 200) * 1000
            acc_dep = random.randint(10, cost - 10000)
            carrying_value = cost - acc_dep
            sold_for = carrying_value + random.randint(-10000, 15000)

            profit_loss = sold_for - carrying_value
            status = "Profit" if profit_loss > 0 else "Loss"
            correct_str = f"R{abs(profit_loss):,} {status}"
            wrong_pool = [f"R{sold_for:,} {status}", f"R{abs(cost - sold_for):,} Loss", f"R{carrying_value:,} Profit"]
            q_text = f"Equipment costing R{cost:,} with accumulated depreciation of R{acc_dep:,} was sold for R{sold_for:,}. Calculate the profit or loss on sale of the asset."
            exp = f"Carrying Value = R{cost:,} - R{acc_dep:,} = R{carrying_value:,}. Profit/Loss = Sold For - Carrying Value = R{sold_for:,} - R{carrying_value:,} = R{abs(profit_loss):,} {status}."
            sub = "Notes to Financial Statements" if "Financial" in self.topic else "Company Concepts"
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", sub): return 1

        return 0

    def _generate_budgeting_questions(self):
        q_type = random.choice(['debtors_collection', 'creditors_payment', 'cash_vs_income'])

        if q_type == 'debtors_collection':
            credit_sales = random.randint(100, 300) * 1000
            percentage_collected = random.choice([50, 60, 70])
            discount = random.choice([2, 5])
            collected_gross = credit_sales * (percentage_collected / 100)
            discount_amount = collected_gross * (discount / 100)
            actual_cash = collected_gross - discount_amount
            correct_str = f"R{actual_cash:,.0f}"
            wrong_pool = [f"R{collected_gross:,.0f}", f"R{(collected_gross + discount_amount):,.0f}", f"R{(credit_sales * ((percentage_collected - discount)/100)):,.0f}"]
            q_text = f"Credit sales for May are R{credit_sales:,}. The business collects {percentage_collected}% of these sales in June, subject to a {discount}% discount. How much cash will be collected in June from May sales?"
            exp = f"Expected collection gross = R{collected_gross:,.0f}. Discount = {discount}% of R{collected_gross:,.0f} = R{discount_amount:,.0f}. Cash collected = R{actual_cash:,.0f}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Debtors and Creditors Collection"): return 1

        elif q_type == 'creditors_payment':
            purchases = random.randint(150, 400) * 1000
            cash_perc = random.choice([20, 30, 40])
            credit_purchases = purchases * ((100 - cash_perc) / 100)
            pay_perc = random.choice([60, 75, 100])
            paid = credit_purchases * (pay_perc / 100)
            correct_str = f"R{paid:,.0f}"
            wrong_pool = [f"R{credit_purchases:,.0f}", f"R{(purchases * (pay_perc/100)):,.0f}", f"R{(purchases * (cash_perc/100)):,.0f}"]
            q_text = f"Total purchases for July are R{purchases:,}, of which {cash_perc}% is for cash. Creditors are paid {pay_perc}% of the credit purchases in the month following the purchase (August). Calculate the amount paid to creditors in August for July purchases."
            exp = f"Credit Purchases = R{purchases:,} x {(100 - cash_perc)}% = R{credit_purchases:,.0f}. Amount Paid = R{credit_purchases:,.0f} x {pay_perc}% = R{paid:,.0f}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Debtors and Creditors Collection"): return 1

        elif q_type == 'cash_vs_income':
            depreciation = random.randint(20, 50) * 1000
            bad_debts = random.randint(5, 15) * 1000
            loan_repayment = random.randint(30, 100) * 1000
            correct_str = f"Loan repayment (R{loan_repayment:,})"
            wrong_pool = [f"Depreciation (R{depreciation:,})", f"Bad Debts (R{bad_debts:,})", "Cost of Sales"]
            q_text = f"Which of the following items would appear in a Cash Budget but NOT in a Projected Income Statement?"
            exp = f"A loan repayment involves a cash outflow (goes to Cash Budget) but is not an expense (does not go to Income Statement). Depreciation and Bad Debts are non-cash expenses."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Budget Concepts"): return 1

        return 0

    def _generate_cashflow_questions(self):
        q_type = random.choice(['tax_paid', 'dividends_paid', 'fixed_assets_purchased'])

        if q_type == 'tax_paid':
            tax_expense = random.randint(50, 200) * 1000
            open_cr = random.randint(5, 30) * 1000
            expense = random.randint(100, 300) * 1000
            close_cr = random.randint(10, 40) * 1000
            tax_paid = open_cr + expense - close_cr
            correct_str = f"R{tax_paid:,}"
            wrong_pool = [f"R{expense:,}", f"R{(expense + close_cr - open_cr):,}", f"R{(open_cr + close_cr + expense):,}"]
            q_text = f"Income Tax expense is R{expense:,}. SARS (Income Tax) had an opening credit balance of R{open_cr:,} and a closing credit balance of R{close_cr:,}. Calculate Taxation Paid."
            exp = f"Tax Paid = Opening Balance (R{open_cr:,}) + Tax Expense (R{expense:,}) - Closing Balance (R{close_cr:,}) = R{tax_paid:,}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Operating Activities"): return 1

        elif q_type == 'dividends_paid':
            final_prev = random.randint(30, 80) * 1000
            interim_curr = random.randint(40, 90) * 1000
            final_curr = random.randint(50, 100) * 1000
            paid = final_prev + interim_curr
            correct_str = f"R{paid:,}"
            wrong_pool = [f"R{(interim_curr + final_curr):,}", f"R{(final_prev + final_curr):,}", f"R{(final_prev + interim_curr + final_curr):,}"]
            q_text = f"Shareholders for dividends opening balance was R{final_prev:,} (final dividend from last year). During the current year, an interim dividend of R{interim_curr:,} was paid, and a final dividend of R{final_curr:,} was declared. Calculate Dividends Paid for the Cash Flow Statement."
            exp = f"Dividends Paid = Final dividend from previous year (R{final_prev:,}) + Interim dividend paid this year (R{interim_curr:,}) = R{paid:,}. The current year's final dividend is only paid next year."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Operating Activities"): return 1

        elif q_type == 'fixed_assets_purchased':
            carrying_value_start = random.randint(1000, 3000) * 1000
            carrying_value_end = random.randint(1500, 3500) * 1000
            depreciation = random.randint(100, 300) * 1000
            disposals = random.randint(50, 200) * 1000 # carrying value of disposals

            purchases = carrying_value_end - carrying_value_start + depreciation + disposals
            correct_str = f"R{purchases:,}"
            wrong_pool = [f"R{(carrying_value_end - carrying_value_start):,}", f"R{(carrying_value_end - carrying_value_start + depreciation):,}", f"R{(carrying_value_end - carrying_value_start - disposals):,}"]
            q_text = f"Fixed assets carrying value at start: R{carrying_value_start:,}. At end: R{carrying_value_end:,}. Depreciation for the year: R{depreciation:,}. Carrying value of assets sold: R{disposals:,}. Calculate the amount paid to purchase fixed assets."
            exp = f"Purchases = Closing CV (R{carrying_value_end:,}) - Opening CV (R{carrying_value_start:,}) + Depreciation (R{depreciation:,}) + Disposals (R{disposals:,}) = R{purchases:,}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Investing & Financing Activities"): return 1

        return 0

    def _generate_reconciliation_questions(self):
        q_type = random.choice(['bank_recon_balance', 'bank_recon_error', 'debtors_recon'])

        if q_type == 'bank_recon_balance':
            bank_balance = random.randint(10, 50) * 1000 # Debit balance
            outstanding_cheque = random.randint(1, 5) * 1000
            outstanding_deposit = random.randint(2, 8) * 1000
            recon_balance = bank_balance + outstanding_deposit - outstanding_cheque
            correct_str = f"R{recon_balance:,} favourable"
            wrong_pool = [f"R{(bank_balance - outstanding_deposit + outstanding_cheque):,} favourable", f"R{(bank_balance + outstanding_deposit + outstanding_cheque):,} favourable", f"R{recon_balance:,} overdrawn"]
            q_text = f"The Bank Statement shows a favourable balance of R{bank_balance:,}. Outstanding cheques: R{outstanding_cheque:,}. Outstanding deposit: R{outstanding_deposit:,}. Calculate the balance as per the Bank account in the General Ledger."
            exp = f"GL Balance = Bank Statement Balance (R{bank_balance:,}) + Outstanding Deposits (R{outstanding_deposit:,}) - Outstanding Cheques (R{outstanding_cheque:,}) = R{recon_balance:,} favourable."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Bank Reconciliation"): return 1

        elif q_type == 'bank_recon_error':
            error_amt = random.randint(500, 2000)
            correct_str = f"Debit Bank account with R{error_amt:,}"
            wrong_pool = [f"Credit Bank account with R{error_amt:,}", f"Debit Bank account with R{(error_amt*2):,}", f"Credit Bank Statement with R{error_amt:,}"]
            q_text = f"A deposit of R{error_amt:,} was recorded correctly on the Bank Statement but omitted from the Cash Receipts Journal. How must this be corrected?"
            exp = f"If omitted from the CRJ, it must be added to the cash book by debiting the Bank account. It's already on the statement."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "easy", "Bank Reconciliation"): return 1

        elif q_type == 'debtors_recon':
            control_bal = random.randint(50, 150) * 1000
            list_bal = control_bal + random.choice([-2000, 2000, -3000, 3000])
            error_amt = abs(control_bal - list_bal)
            correct_str = f"R{control_bal:,}" if control_bal > list_bal else f"R{list_bal:,}" # Depends on the scenario, let's craft a specific one

            # Scenario: Invoice omitted from Debtors Journal
            control_bal_start = random.randint(50, 150) * 1000
            invoice_omitted = random.randint(1, 5) * 1000
            corrected_control = control_bal_start + invoice_omitted

            correct_str = f"R{corrected_control:,}"
            wrong_pool = [f"R{control_bal_start:,}", f"R{(control_bal_start - invoice_omitted):,}", f"R{(control_bal_start + (invoice_omitted*2)):,}"]
            q_text = f"The Debtors Control account balance is R{control_bal_start:,}. It was discovered that an invoice for R{invoice_omitted:,} was completely omitted from the Debtors Journal. Calculate the corrected Debtors Control balance."
            exp = f"Omitted invoice means credit sales were undercast. We must add the invoice amount to the control account: R{control_bal_start:,} + R{invoice_omitted:,} = R{corrected_control:,}."
            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Debtors & Creditors Reconciliations"): return 1

        return 0


    def build(self, output_dir):
        # Generate target: ~1000 questions per topic
        # Split: 300 theory, 700 procedural calculation variations (to reflect depth of Grade 12 Accounting)
        self.generate_theory_questions(300)
        self.generate_procedural_questions(700)

        filepath = os.path.join(output_dir, self.file)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=4)

        print(f"Generated {len(self.questions)} questions for {self.topic} -> {filepath}")

def main():
    kb = AccountingKnowledgeBase()
    output_dir = "dataset/grade12/accounting"

    os.makedirs(output_dir, exist_ok=True)

    for topic_data in kb.get_topics():
        engine = AccountingQuestionEngine(topic_data)
        engine.build(output_dir)

if __name__ == "__main__":
    main()
