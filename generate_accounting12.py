import json
import random
import os
import hashlib
from typing import List, Dict

# Helpers import
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'generators/helpers'))
# If helper files exist we can use them, but we will write a self-contained engine for accounting here
# just to be safe and specific to its procedural calculation needs.

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

    def generate_theory_questions(self, target_count=50):
        added = 0
        attempts = 0
        while added < target_count and attempts < target_count * 5:
            attempts += 1
            subtopic = random.choice(self.subtopics)
            fact = random.choice(subtopic['facts'])

            # Type 1: Definition -> Term
            q_text = f"Which accounting term is defined as: {fact['desc']}?"
            correct = fact['a']
            wrong = random.sample(fact['w'], min(3, len(fact['w'])))

            if self.add_question(q_text, correct, wrong, f"The correct term is {correct}.", "easy", subtopic['name'], "Recall Principles"):
                added += 1

    def generate_procedural_questions(self, target_count=50):
        added = 0
        attempts = 0

        while added < target_count and attempts < target_count * 5:
            attempts += 1

            # Procedural Generation Based on Topic
            if "Analysis" in self.topic:
                added += self._generate_ratio_question()
            elif "Manufacturing" in self.topic:
                added += self._generate_manufacturing_question()
            elif "Inventory" in self.topic:
                added += self._generate_inventory_question()
            elif "Companies" in self.topic or "Financial Statements" in self.topic:
                added += self._generate_financial_statement_question()
            elif "Budgeting" in self.topic:
                added += self._generate_budgeting_question()
            elif "Cash Flow" in self.topic:
                added += self._generate_cashflow_question()
            elif "Reconciliations" in self.topic:
                added += self._generate_reconciliation_question()
            else:
                # Fallback to more theory if no procedural logic
                self.generate_theory_questions(1)
                added += 1

    def _generate_ratio_question(self):
        # Example: Current Ratio
        if random.choice([True, False]):
            current_assets = random.randint(100, 900) * 1000
            current_liabilities = random.randint(50, 400) * 1000

            ratio = current_assets / current_liabilities
            correct_str = f"{ratio:.2f}:1"

            # Plausible distractors
            distractor1 = f"{(current_liabilities / current_assets):.2f}:1" # inverted
            distractor2 = f"{(ratio + 0.5):.2f}:1"
            distractor3 = f"{(ratio - 0.2):.2f}:1"
            distractor4 = f"{ratio:.1f}:1" # rounding issue

            pool = list(set([distractor1, distractor2, distractor3, distractor4]))
            wrong_pool = []
            for d in pool:
                if d != correct_str:
                    wrong_pool.append(d)

            q_text = f"A company has current assets of R{current_assets:,} and current liabilities of R{current_liabilities:,}. Calculate the current ratio."
            exp = f"Current Ratio = Current Assets / Current Liabilities = R{current_assets:,} / R{current_liabilities:,} = {ratio:.2f}:1"

            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Liquidity Indicators"):
                return 1
        else:
            # Gross Profit Margin
            sales = random.randint(500, 2000) * 1000
            cost_of_sales = int(sales * random.uniform(0.4, 0.8))
            gross_profit = sales - cost_of_sales

            margin = (gross_profit / sales) * 100
            correct_str = f"{margin:.1f}%"

            distractor1 = f"{((gross_profit / cost_of_sales) * 100):.1f}%" # Mark-up on cost instead
            distractor2 = f"{((cost_of_sales / sales) * 100):.1f}%" # Cost of sales percentage
            distractor3 = f"{(margin + 5):.1f}%"

            wrong_pool = [distractor1, distractor2, distractor3]

            q_text = f"A business has sales of R{sales:,} and cost of sales of R{cost_of_sales:,}. Calculate the gross profit margin."
            exp = f"Gross Profit = Sales - Cost of Sales = R{sales:,} - R{cost_of_sales:,} = R{gross_profit:,}. Margin = (Gross Profit / Sales) * 100 = {margin:.1f}%"

            if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Profitability Indicators"):
                return 1
        return 0

    def _generate_manufacturing_question(self):
        # Prime Cost
        direct_materials = random.randint(100, 500) * 1000
        direct_labour = random.randint(50, 300) * 1000
        factory_overhead = random.randint(20, 150) * 1000

        prime_cost = direct_materials + direct_labour
        correct_str = f"R{prime_cost:,}"

        distractor1 = f"R{(prime_cost + factory_overhead):,}" # Included overheads (Total Manufacturing Cost)
        distractor2 = f"R{(direct_materials + factory_overhead):,}" # Missed labour
        distractor3 = f"R{(direct_labour + factory_overhead):,}" # Missed materials

        wrong_pool = [distractor1, distractor2, distractor3]

        q_text = f"Calculate the Prime Cost given the following: Direct Materials R{direct_materials:,}, Direct Labour R{direct_labour:,}, and Factory Overheads R{factory_overhead:,}."
        exp = f"Prime Cost = Direct Materials + Direct Labour = R{direct_materials:,} + R{direct_labour:,} = R{prime_cost:,}. (Factory overheads are not included in prime cost)."

        if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Manufacturing Concepts"):
            return 1
        return 0

    def _generate_inventory_question(self):
        # Weighted Average
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

        distractor1 = f"R{((cost_opening + cost_purchased)/2):.2f}" # Simple average of unit prices
        distractor2 = f"R{cost_purchased:.2f}" # Used latest price
        distractor3 = f"R{(total_cost / units_purchased):.2f}" # Divided by wrong units

        wrong_pool = [distractor1, distractor2, distractor3]

        q_text = f"Opening stock is {units_opening} units at R{cost_opening} each. Purchases during the year are {units_purchased} units at R{cost_purchased} each. Calculate the weighted average cost per unit."
        exp = f"Total Cost = (R{total_opening}) + (R{total_purchased}) = R{total_cost}. Total Units = {total_units}. Weighted Average = R{total_cost} / {total_units} = R{weighted_avg:.2f}"

        if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Valuation Methods"):
            return 1
        return 0

    def _generate_financial_statement_question(self):
        # Retained Income
        opening_retained = random.randint(100, 500) * 1000
        net_profit_after_tax = random.randint(200, 800) * 1000
        interim_dividend = random.randint(20, 100) * 1000
        final_dividend = random.randint(30, 150) * 1000

        closing_retained = opening_retained + net_profit_after_tax - interim_dividend - final_dividend
        correct_str = f"R{closing_retained:,}"

        distractor1 = f"R{(opening_retained + net_profit_after_tax - interim_dividend):,}" # Forgot final dividend
        distractor2 = f"R{(opening_retained + net_profit_after_tax):,}" # Forgot all dividends
        distractor3 = f"R{(opening_retained + net_profit_after_tax + interim_dividend + final_dividend):,}" # Added dividends instead of subtracting

        wrong_pool = [distractor1, distractor2, distractor3]

        q_text = f"A company has an opening retained income of R{opening_retained:,}. The net profit after tax is R{net_profit_after_tax:,}. Interim dividends paid were R{interim_dividend:,} and final dividends declared were R{final_dividend:,}. Calculate the closing balance of the Retained Income account."
        exp = f"Closing Retained Income = Opening Balance (R{opening_retained:,}) + Net Profit after Tax (R{net_profit_after_tax:,}) - Total Dividends (R{interim_dividend + final_dividend:,}) = R{closing_retained:,}"

        sub = "Statement of Financial Position" if "Financial" in self.topic else "Company Concepts"
        if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", sub):
            return 1
        return 0

    def _generate_budgeting_question(self):
        # Debtors Collection
        credit_sales = random.randint(100, 300) * 1000
        percentage_collected = random.choice([50, 60, 70])
        discount = random.choice([2, 5])

        collected_gross = credit_sales * (percentage_collected / 100)
        discount_amount = collected_gross * (discount / 100)
        actual_cash = collected_gross - discount_amount

        correct_str = f"R{actual_cash:,.0f}"
        distractor1 = f"R{collected_gross:,.0f}" # Forgot to deduct discount
        distractor2 = f"R{(collected_gross + discount_amount):,.0f}" # Added discount
        distractor3 = f"R{(credit_sales * ((percentage_collected - discount)/100)):,.0f}" # Incorrect percentage logic

        wrong_pool = [distractor1, distractor2, distractor3]

        q_text = f"Credit sales for May are R{credit_sales:,}. The business expects to collect {percentage_collected}% of these sales in June, subject to a {discount}% discount for prompt payment. How much cash will be collected in June from May sales?"
        exp = f"Expected collection gross = {percentage_collected}% of R{credit_sales:,} = R{collected_gross:,.0f}. Discount = {discount}% of R{collected_gross:,.0f} = R{discount_amount:,.0f}. Cash collected = R{collected_gross:,.0f} - R{discount_amount:,.0f} = R{actual_cash:,.0f}"

        if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Debtors and Creditors Collection"):
            return 1
        return 0

    def _generate_cashflow_question(self):
        # Tax Paid Calculation
        tax_expense = random.randint(50, 200) * 1000
        opening_sars = random.choice([-20, -10, 10, 20]) * 1000 # Negative means debit balance (SARS owes company)
        closing_sars = random.choice([-15, -5, 15, 25]) * 1000

        # Calculation: Opening Balance (Cr is +, Dr is -) + Income Statement Expense - Closing Balance (Cr is +, Dr is -) = Amount Paid
        # Let's frame it simpler:
        # Opening balance Cr (owe SARS), Expense (adds to owe), Closing balance Cr (still owe)
        open_cr = random.randint(5, 30) * 1000
        expense = random.randint(100, 300) * 1000
        close_cr = random.randint(10, 40) * 1000

        tax_paid = open_cr + expense - close_cr

        correct_str = f"R{tax_paid:,}"
        distractor1 = f"R{expense:,}" # Used income statement figure only
        distractor2 = f"R{(expense + close_cr - open_cr):,}" # Reversed opening and closing
        distractor3 = f"R{(open_cr + close_cr + expense):,}" # Added everything

        wrong_pool = [distractor1, distractor2, distractor3]

        q_text = f"The Income Tax expense for the year is R{expense:,}. The SARS (Income Tax) account had an opening credit balance of R{open_cr:,} and a closing credit balance of R{close_cr:,}. Calculate the actual Taxation Paid during the year."
        exp = f"Tax Paid = Opening Balance (R{open_cr:,}) + Tax Expense (R{expense:,}) - Closing Balance (R{close_cr:,}) = R{tax_paid:,}"

        if self.add_question(q_text, correct_str, wrong_pool, exp, "hard", "Operating Activities"):
            return 1
        return 0

    def _generate_reconciliation_question(self):
        bank_balance = random.randint(10, 50) * 1000 # Debit balance
        outstanding_cheque = random.randint(1, 5) * 1000
        outstanding_deposit = random.randint(2, 8) * 1000

        # Bank reconciliation statement balance
        recon_balance = bank_balance + outstanding_deposit - outstanding_cheque

        correct_str = f"R{recon_balance:,} favourable"
        distractor1 = f"R{(bank_balance - outstanding_deposit + outstanding_cheque):,} favourable" # Signs reversed
        distractor2 = f"R{(bank_balance + outstanding_deposit + outstanding_cheque):,} favourable" # Added both
        distractor3 = f"R{recon_balance:,} overdrawn" # Wrong sign interpretation

        wrong_pool = [distractor1, distractor2, distractor3]

        q_text = f"The Bank Statement shows a favourable (credit) balance of R{bank_balance:,}. Outstanding cheques amount to R{outstanding_cheque:,} and an outstanding deposit is R{outstanding_deposit:,}. Calculate the balance as per the Bank account in the General Ledger (assuming no other errors)."
        exp = f"Balance per General Ledger = Bank Statement Balance (R{bank_balance:,}) + Outstanding Deposits (R{outstanding_deposit:,}) - Outstanding Cheques (R{outstanding_cheque:,}) = R{recon_balance:,} favourable (debit balance in GL)."

        if self.add_question(q_text, correct_str, wrong_pool, exp, "medium", "Bank Reconciliation"):
            return 1
        return 0


    def build(self, output_dir):
        # Generate 20 theory and 30 procedural questions
        self.generate_theory_questions(20)
        self.generate_procedural_questions(30)

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
