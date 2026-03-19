import json
import random
import math
import os
from typing import List
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

class MathLit12Generator(TopicGenerator):
    def __init__(self, topic_name: str, topic_prefix: str, subtopics: List[str], paper: str):
        super().__init__(topic_name, topic_prefix, subtopics)
        self.paper = paper

    def add_question(self, subtopic: str, difficulty: str, question: str, correct_answer: str, wrong_answers: List[str], explanation: str):
        # We override add_question to include the paper field in the dictionary.
        # Check if we still need more questions of this difficulty
        if self.difficulty_counts[difficulty] >= self.difficulty_targets[difficulty]:
            return False

        # Check for duplication (exact question text)
        if question in self.generated_questions:
            return False

        # Ensure correct answer is not in wrong answers
        correct_str = str(correct_answer)
        wrong_answers = [str(w) for w in wrong_answers if str(w) != correct_str]

        # Deduplicate wrong answers
        unique_wrong_answers = []
        seen = set()
        for w in wrong_answers:
            if w not in seen:
                seen.add(w)
                unique_wrong_answers.append(w)

        # We need at least 6 wrong answers
        if len(unique_wrong_answers) < 6:
            return False

        self.generated_questions.add(question)
        self.difficulty_counts[difficulty] += 1

        question_id = f"{self.topic_prefix}_{len(self.questions) + 1:03d}"

        q_dict = {
            "id": question_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "paper": self.paper,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": correct_str,
            "wrong_answers_pool": unique_wrong_answers[:8],
            "explanation": explanation
        }
        self.questions.append(q_dict)
        return True

def generate_p1_finance() -> MathLit12Generator:
    subtopics = ["Income and Expenditure", "Budgets", "Profit and Loss", "Tax", "Interest"]
    gen = MathLit12Generator("Finance", "ML12_P1_FIN", subtopics, "paper1")

    names = ["Kagiso", "Lebo", "Mandla", "Noxolo", "Tshepo", "Buhle", "Lerato", "Sipho", "Zanele", "Thabo", "Mpho", "Fatima", "Aisha", "John", "Sarah"]
    items = ["jacket", "laptop", "phone", "bicycle", "fridge", "microwave", "tv", "sneakers", "desk", "sofa"]

    attempts = 0
    while not gen.is_done() and attempts < 100000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        name = random.choice(names)
        item = random.choice(items)

        if subtopic == "Tax":
            if difficulty == "easy":
                price = random.randint(100, 2000)
                vat_amount = price * 0.15
                q = f"A {item} costs R{price} before VAT. If VAT is 15%, calculate the amount of VAT to be added."
                ans_str = f"R{vat_amount:.2f}"
                wrong = get_wrong_floats(vat_amount, 8, 2)
                wrong = [f"R{w}" for w in wrong]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"VAT = 15% of R{price} = 0.15 × {price} = R{vat_amount:.2f}.")
            elif difficulty == "medium":
                price_inc = random.randint(200, 5000)
                price_exc = price_inc / 1.15
                q = f"A {item} costs R{price_inc} including VAT (15%). What is the price excluding VAT? (Round to 2 decimal places)."
                ans_str = f"R{price_exc:.2f}"
                wrong_vals = [price_inc - (price_inc * 0.15), price_inc / 0.15, price_inc * 1.15, price_exc + 10, price_exc - 10, price_inc - 15, price_inc * 0.85]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(price_exc, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Price excluding VAT = R{price_inc} ÷ 1.15 = R{price_exc:.2f}.")
            else:
                salary = random.randint(100000, 400000)
                tax_rate = random.choice([18, 26, 31])
                rebate = random.randint(10000, 15000)
                tax = (salary * tax_rate / 100) - rebate
                tax = max(0, tax)
                q = f"{name} earns an annual taxable income of R{salary}. According to the tax tables, their tax is calculated at {tax_rate}% of taxable income. If they receive a primary tax rebate of R{rebate}, calculate the final tax payable for the year."
                ans_str = f"R{tax:.2f}"
                wrong_vals = [salary * tax_rate / 100, (salary - rebate) * tax_rate / 100, (salary * tax_rate / 100) + rebate, tax + 1000, tax - 1000, tax * 12, tax / 12]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(tax, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Tax before rebate = {tax_rate}% of R{salary} = R{salary * tax_rate / 100:.2f}. Final tax = R{salary * tax_rate / 100:.2f} - R{rebate} = R{tax:.2f}.")

        elif subtopic == "Interest":
            if difficulty == "easy":
                p = random.randint(1000, 10000)
                r = random.randint(5, 12)
                t = random.randint(2, 5)
                interest = p * (r / 100) * t
                q = f"{name} invests R{p} at a simple interest rate of {r}% per annum for {t} years. Calculate the total interest earned."
                ans_str = f"R{interest:.2f}"
                wrong_vals = [p + interest, p * (r/100), p * (r/100)**t, interest + 100, interest - 100, interest * 12, interest / t]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(interest, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Simple Interest = P × r × t = R{p} × {r/100} × {t} = R{interest:.2f}.")
            elif difficulty == "medium":
                p = random.randint(5000, 20000)
                r = random.randint(5, 15)
                t = random.randint(2, 6)
                a = p * (1 + r/100)**t
                q = f"{name} invests R{p} at a compound interest rate of {r}% per annum. Calculate the total amount accumulated after {t} years. (Round to 2 decimal places)."
                ans_str = f"R{a:.2f}"
                wrong_vals = [p * (1 + r/100 * t), p + (p * r/100 * t), a - p, a + 1000, a - 1000, p * (r/100)**t]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(a, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Compound Amount A = P(1 + r/100)^t = R{p}(1 + {r/100})^{t} = R{a:.2f}.")
            else:
                p = random.randint(10000, 50000)
                r = random.choice([6.5, 7.5, 8.5, 9.5, 10.5])
                t = random.randint(3, 8)
                a = p * (1 + (r/100)/12)**(t*12)
                q = f"{name} takes a loan of R{p} over {t} years. The interest rate is {r}% per annum compounded monthly. What is the total amount to be repaid at the end of the loan period? (Round to 2 decimal places)."
                ans_str = f"R{a:.2f}"
                wrong_vals = [p * (1 + r/100)**t, p * (1 + r/100 * t), a - p, p * (1 + (r/100)/12)**t, p * (1 + r/100)**(t*12), a * 1.1]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(a, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"A = P(1 + r/n)^(nt). A = R{p}(1 + {r/100}/12)^({t}×12) = R{p}(1 + {r/1200})^{t*12} = R{a:.2f}.")

        elif subtopic == "Profit and Loss":
            if difficulty == "easy":
                cp = random.randint(100, 500)
                sp = cp + random.randint(50, 200)
                profit = sp - cp
                q = f"{name} buys a {item} for R{cp} and sells it for R{sp}. Calculate the profit made."
                ans_str = f"R{profit}"
                wrong = [f"R{w}" for w in get_wrong_ints(profit)] + [f"R{cp}", f"R{sp}", f"R{profit + 50}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Profit = Selling Price - Cost Price = R{sp} - R{cp} = R{profit}.")
            elif difficulty == "medium":
                cp = random.randint(500, 2000)
                markup_perc = random.randint(15, 60)
                profit = cp * (markup_perc / 100)
                sp = cp + profit
                q = f"A store buys a {item} for R{cp} and marks up the price by {markup_perc}%. What is the selling price of the {item}?"
                ans_str = f"R{sp:.2f}"
                wrong_vals = [cp + markup_perc, cp * (markup_perc/100), sp - 100, sp + 100, cp / (markup_perc/100), sp * 1.1]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(sp, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Markup = {markup_perc}% of R{cp} = R{profit:.2f}. Selling Price = Cost + Markup = R{cp} + R{profit:.2f} = R{sp:.2f}.")
            else:
                sp = random.randint(800, 4000)
                markup_perc = random.choice([20, 25, 30, 40, 50])
                cp = sp / (1 + markup_perc/100)
                q = f"{name} sells a {item} for R{sp}, which includes a profit markup of {markup_perc}% on the cost price. Calculate the original cost price of the {item}. (Round to 2 decimal places)."
                ans_str = f"R{cp:.2f}"
                wrong_vals = [sp - (sp * markup_perc/100), sp * (1 - markup_perc/100), sp / (markup_perc/100), cp + 100, cp - 100, sp * 1.2]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(cp, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Selling Price = Cost Price × (1 + markup%). R{sp} = Cost × (1 + {markup_perc/100}). Cost = R{sp} ÷ {1 + markup_perc/100} = R{cp:.2f}.")

        elif subtopic == "Income and Expenditure":
            if difficulty == "easy":
                wage = random.randint(150, 300)
                hours = random.randint(5, 12)
                income = wage * hours
                q = f"{name} works for {hours} hours and is paid R{wage} per hour. What is their total income for the day?"
                ans_str = f"R{income}"
                wrong = [f"R{w}" for w in get_wrong_ints(income)] + [f"R{wage + hours}", f"R{wage * (hours+1)}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total Income = Hourly Rate × Hours Worked = R{wage} × {hours} = R{income}.")
            elif difficulty == "medium":
                basic = random.randint(5000, 15000)
                comm_rate = random.randint(3, 10)
                sales = random.randint(20000, 80000)
                commission = sales * (comm_rate / 100)
                total = basic + commission
                q = f"{name} earns a basic salary of R{basic} per month plus a {comm_rate}% commission on total sales. If their sales for the month amounted to R{sales}, calculate their total gross income."
                ans_str = f"R{total:.2f}"
                wrong_vals = [commission, basic + sales, total - basic, total + 1000, basic + (sales / (comm_rate/100)), basic * (comm_rate/100)]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(total, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Commission = {comm_rate}% of R{sales} = R{commission:.2f}. Total Income = Basic + Commission = R{basic} + R{commission:.2f} = R{total:.2f}.")
            else:
                gross = random.randint(15000, 35000)
                tax = random.randint(2000, 6000)
                med = random.randint(1000, 3000)
                uif = gross * 0.01
                net = gross - tax - med - uif
                q = f"{name}'s gross monthly salary is R{gross}. The following deductions are made: PAYE Tax of R{tax}, Medical Aid of R{med}, and UIF contribution of 1% of gross salary. Calculate {name}'s net salary."
                ans_str = f"R{net:.2f}"
                wrong_vals = [gross - tax - med, net + uif, gross - uif, net - uif, gross * 0.99, net + 1000]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(net, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"UIF = 1% of R{gross} = R{uif:.2f}. Total Deductions = R{tax} + R{med} + R{uif:.2f} = R{tax+med+uif:.2f}. Net Salary = Gross - Deductions = R{gross} - R{tax+med+uif:.2f} = R{net:.2f}.")

        elif subtopic == "Budgets":
            if difficulty == "easy":
                income = random.randint(3000, 8000)
                expense = random.randint(2000, 5000)
                surplus = income - expense
                q = f"{name} has a monthly income of R{income} and total monthly expenses of R{expense}. What is their surplus or deficit?"
                ans_str = f"Surplus of R{surplus}" if surplus >= 0 else f"Deficit of R{-surplus}"
                wrong = [f"Surplus of R{surplus + 500}", f"Deficit of R{abs(surplus)}", f"Deficit of R{surplus + 100}", f"Surplus of R{-surplus if surplus < 0 else surplus + 200}", f"Surplus of R{income}", f"Deficit of R{expense}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Income - Expenses = R{income} - R{expense} = R{surplus}. Since income is greater than expenses, it is a surplus.")
            elif difficulty == "medium":
                rent = random.randint(3000, 8000)
                food = random.randint(1500, 4000)
                transport = random.randint(800, 2500)
                total_exp = rent + food + transport
                income = random.randint(6000, 16000)
                balance = income - total_exp
                q = f"In a monthly budget, {name} allocates R{rent} for rent, R{food} for groceries, and R{transport} for transport. If {name}'s total income is R{income}, how much money is left for other expenses?"
                ans_str = f"R{balance}"
                wrong_vals = [total_exp, balance + 500, balance - 500, income + total_exp, income - rent, income - food]
                wrong = [f"R{w}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_ints(balance, 4)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total specified expenses = R{rent} + R{food} + R{transport} = R{total_exp}. Money left = Income - Expenses = R{income} - R{total_exp} = R{balance}.")
            else:
                income = random.randint(12000, 25000)
                rent_perc = random.choice([25, 30, 35])
                food_perc = random.choice([15, 20, 25])
                save_perc = random.choice([10, 15])
                other_perc = 100 - rent_perc - food_perc - save_perc
                other_amt = income * (other_perc / 100)
                q = f"{name} earns R{income} per month. They budget {rent_perc}% for rent, {food_perc}% for groceries, and {save_perc}% for savings. The rest of the money is for entertainment and other expenses. How much money is allocated for entertainment and other expenses?"
                ans_str = f"R{other_amt:.2f}"
                wrong_vals = [income * (rent_perc/100), income * (food_perc/100), income * ((100-other_perc)/100), other_amt + 500, other_amt - 500, other_amt * 1.1]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(other_amt, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total allocated percentage = {rent_perc}% + {food_perc}% + {save_perc}% = {rent_perc+food_perc+save_perc}%. Remaining percentage = 100% - {rent_perc+food_perc+save_perc}% = {other_perc}%. Amount = {other_perc}% of R{income} = R{other_amt:.2f}.")

    return gen

def generate_p1_data_handling() -> MathLit12Generator:
    subtopics = ["Statistics", "Interpreting Graphs", "Quartiles and Percentiles"]
    gen = MathLit12Generator("Data Handling", "ML12_P1_DATA", subtopics, "paper1")

    names = ["A group of learners", "A small business", "A taxi rank", "A local municipality", "A survey team"]

    attempts = 0
    while not gen.is_done() and attempts < 100000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        name = random.choice(names)

        if subtopic == "Statistics":
            if difficulty == "easy":
                vals = [random.randint(10, 50) for _ in range(5)]
                vals.sort()
                mean = sum(vals) / len(vals)
                q = f"{name} collected the following data: {', '.join(map(str, vals))}. What is the mean (average) of this data set? (Round to 1 decimal place)."
                ans_str = f"{mean:.1f}"
                wrong = get_wrong_floats(mean, 8, 1)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Sum = {sum(vals)}. N = 5. Mean = {sum(vals)} ÷ 5 = {mean:.1f}.")
            elif difficulty == "medium":
                vals = [random.randint(20, 100) for _ in range(6)]
                vals.sort()
                median = (vals[2] + vals[3]) / 2
                q = f"The test scores for 6 learners are: {', '.join(map(str, vals))}. What is the median score? (Round to 1 decimal place)."
                ans_str = f"{median:.1f}"
                wrong = get_wrong_floats(median, 8, 1)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"The data is ordered. N=6 (even). The middle values are {vals[2]} and {vals[3]}. Median = ({vals[2]} + {vals[3]}) ÷ 2 = {median:.1f}.")
            else:
                vals = [random.randint(5, 50) for _ in range(8)]
                mode = vals[0]
                vals[1] = mode
                vals[2] = mode
                vals.sort()
                q = f"Identify the mode in the following set of data collected during a survey: {', '.join(map(str, vals))}."
                ans_str = f"{mode}"
                wrong = get_wrong_ints(mode, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"The mode is the value that appears most frequently. The number {mode} appears 3 times.")

        elif subtopic == "Interpreting Graphs":
            if difficulty == "easy":
                sales = random.randint(150, 400)
                q = f"A bar graph shows the number of cars sold by a dealership. If the bar for 'Toyota' reaches {sales} on the vertical axis, how many Toyotas were sold?"
                ans_str = f"{sales}"
                wrong = get_wrong_ints(sales, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Read the value directly from the vertical axis. The bar reaches {sales}.")
            elif difficulty == "medium":
                total = random.randint(1000, 5000)
                perc = random.choice([15, 20, 25, 30, 35, 40, 45, 50])
                amount = total * (perc / 100)
                q = f"A pie chart represents the budget of a municipality. The total budget is R{total}. If the 'Housing' sector takes up {perc}% of the pie chart, how much money is allocated to Housing?"
                ans_str = f"R{amount:.2f}"
                wrong_vals = [total - amount, amount + 500, amount - 500, total * (100 - perc)/100, amount * 1.1]
                wrong = [f"R{w:.2f}" for w in wrong_vals] + [f"R{w}" for w in get_wrong_floats(amount, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Housing Budget = {perc}% of R{total} = 0.{perc} × R{total} = R{amount:.2f}.")
            else:
                year1 = random.randint(2010, 2015)
                year2 = year1 + random.randint(3, 5)
                val1 = random.randint(50, 150)
                val2 = val1 + random.randint(30, 80)
                diff = val2 - val1
                q = f"A line graph shows a company's profit over several years. In {year1}, the profit was R{val1} million. In {year2}, the profit was R{val2} million. What was the average annual increase in profit between {year1} and {year2}?"
                years = year2 - year1
                avg_inc = diff / years
                ans_str = f"R{avg_inc:.2f} million"
                wrong_vals = [diff, val2, diff/2, avg_inc + 5, avg_inc - 5]
                wrong = [f"R{w:.2f} million" for w in wrong_vals] + [f"R{w} million" for w in get_wrong_floats(avg_inc, 4, 2)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total Increase = R{val2} - R{val1} = R{diff} million. Number of years = {year2} - {year1} = {years}. Average annual increase = R{diff} ÷ {years} = R{avg_inc:.2f} million.")

        elif subtopic == "Quartiles and Percentiles":
            if difficulty == "easy":
                min_v = random.randint(10, 30)
                q1 = min_v + random.randint(5, 15)
                med = q1 + random.randint(5, 15)
                q3 = med + random.randint(5, 15)
                max_v = q3 + random.randint(5, 15)
                iqr = q3 - q1
                q = f"Given the five-number summary of a dataset: Minimum = {min_v}, Lower Quartile (Q1) = {q1}, Median = {med}, Upper Quartile (Q3) = {q3}, Maximum = {max_v}. Calculate the Interquartile Range (IQR)."
                ans_str = f"{iqr}"
                wrong = get_wrong_ints(iqr, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"IQR = Q3 - Q1 = {q3} - {q1} = {iqr}.")
            elif difficulty == "medium":
                min_v = random.randint(20, 50)
                q1 = min_v + random.randint(10, 20)
                med = q1 + random.randint(10, 20)
                q3 = med + random.randint(10, 20)
                max_v = q3 + random.randint(10, 20)
                range_v = max_v - min_v
                q = f"A box and whisker plot shows the distribution of test marks. The plot indicates: Min={min_v}, Q1={q1}, Median={med}, Q3={q3}, and Max={max_v}. What is the range of the test marks?"
                ans_str = f"{range_v}"
                wrong = get_wrong_ints(range_v, 8) + [str(q3 - q1)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Range = Maximum - Minimum = {max_v} - {min_v} = {range_v}.")
            else:
                total_learners = random.randint(80, 200)
                percentile = random.choice([25, 50, 75, 90])
                below = int(total_learners * (percentile / 100))
                q = f"In a grade of {total_learners} learners, Thabo scored in the {percentile}th percentile for his Math Lit exam. Approximately how many learners scored lower than Thabo?"
                ans_str = f"{below}"
                wrong = get_wrong_ints(below, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"The {percentile}th percentile means {percentile}% of the learners scored lower. {percentile}% of {total_learners} = 0.{percentile} × {total_learners} = {below} learners.")

    return gen


def generate_p1_probability() -> MathLit12Generator:
    subtopics = ["Theoretical Probability", "Relative Frequency", "Tree Diagrams"]
    gen = MathLit12Generator("Probability (P1)", "ML12_P1_PROB", subtopics, "paper1")

    attempts = 0
    while not gen.is_done() and attempts < 250000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Theoretical Probability":
            if difficulty == "easy":
                colors = ["red", "blue", "green", "yellow", "black", "white", "purple", "orange", "pink", "brown", "grey", "silver"]
                c1, c2 = random.sample(colors, 2)
                n1 = random.randint(3, 50)
                n2 = random.randint(4, 50)
                total = n1 + n2
                q = f"A bag contains {n1} {c1} marbles and {n2} {c2} marbles. If one marble is drawn at random, what is the theoretical probability of drawing a {c1} marble? (Give your answer as a fraction)."
                ans_str = f"{n1}/{total}"
                wrong = [f"{n2}/{total}", f"{n1}/{n2}", f"{n2}/{n1}", f"1/{total}", f"{n1}/{n1+n2+2}", f"{n1-1}/{total}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total marbles = {n1} + {n2} = {total}. Probability of {c1} = Favorable outcomes / Total outcomes = {n1}/{total}.")
            elif difficulty == "medium":
                faces = random.choice([6, 8, 12])
                q = f"A fair {faces}-sided die is rolled. What is the probability of rolling a number greater than 4? (Give your answer as a fraction in simplest form)."
                favorable = faces - 4
                if favorable <= 0:
                    favorable = 0
                    ans_str = "0"
                    wrong = ["1/2", "1/4", "1/6", "1/3", "2/3", "3/4"]
                else:
                    gcd = math.gcd(favorable, faces)
                    ans_str = f"{favorable//gcd}/{faces//gcd}"
                    wrong = [f"{(favorable-1)//math.gcd(favorable-1, faces)}/{faces//math.gcd(favorable-1, faces)}" if math.gcd(favorable-1, faces) > 0 else "0",
                             f"4/{faces}", f"{favorable}/{faces+1}"]
                    wrong += [f"1/{faces}", f"2/{faces}", f"3/{faces}", f"{faces-1}/{faces}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Numbers greater than 4: 5, 6... up to {faces}. There are {favorable} such numbers. Probability = {favorable}/{faces} = {ans_str}.")
            else:
                n_red = random.randint(2, 5)
                n_blue = random.randint(3, 7)
                total = n_red + n_blue
                prob = (n_red/total) * ((n_red-1)/(total-1))
                q = f"A jar contains {n_red} red sweets and {n_blue} blue sweets. Two sweets are drawn at random without replacement. What is the probability that both sweets are red? (Give your answer as a decimal rounded to 3 decimal places)."
                ans_str = f"{prob:.3f}"
                wrong = get_wrong_floats(prob, 8, 3)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"P(1st Red) = {n_red}/{total}. P(2nd Red | 1st Red) = {n_red-1}/{total-1}. P(Both Red) = ({n_red}/{total}) × ({n_red-1}/{total-1}) = {prob:.3f}.")

        elif subtopic == "Relative Frequency":
            if difficulty == "easy":
                trials = random.randint(50, 500)
                successes = random.randint(10, trials-10)
                rf = successes / trials
                q = f"A coin was flipped {trials} times and landed on 'Heads' {successes} times. What is the relative frequency of getting 'Heads'? (Give your answer as a decimal rounded to 2 decimal places)."
                ans_str = f"{rf:.2f}"
                wrong = get_wrong_floats(rf, 8, 2)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Relative Frequency = Number of successful trials / Total number of trials = {successes} / {trials} = {rf:.2f}.")
            elif difficulty == "medium":
                trials = random.randint(150, 800)
                successes = random.randint(30, 120)
                rf_perc = (successes / trials) * 100
                q = f"A survey of {trials} people found that {successes} of them use public transport. What is the relative frequency, expressed as a percentage, of people using public transport? (Round to 1 decimal place)."
                ans_str = f"{rf_perc:.1f}%"
                wrong = [f"{w}%" for w in get_wrong_floats(rf_perc, 8, 1)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Relative Frequency = ({successes} / {trials}) × 100 = {rf_perc:.1f}%.")
            else:
                expected_prob = 1/6
                trials = random.choice([300, 600, 1200, 900, 1500, 1800, 2400])
                actual = random.randint(int(trials*expected_prob) - 40, int(trials*expected_prob) + 40)
                diff = abs(actual - (trials/6))
                q = f"A 6-sided die is rolled {trials} times. It lands on a '3' exactly {actual} times. What is the difference between the expected number of 3s (based on theoretical probability) and the actual experimental results? (Round to nearest whole number)."
                ans_str = f"{int(round(diff))}"
                wrong = get_wrong_ints(int(round(diff)), 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Expected number of 3s = (1/6) × {trials} = {trials/6}. Actual = {actual}. Difference = |{trials/6} - {actual}| = {int(round(diff))}.")

        elif subtopic == "Tree Diagrams":
            if difficulty == "easy":
                s_types = random.randint(2, 6)
                d_types = random.randint(2, 5)
                ans_str = str(s_types * d_types)
                q = f"A student has to choose 1 sandwich and 1 drink for lunch. There are {s_types} types of sandwiches and {d_types} types of drinks. By drawing a tree diagram, how many possible lunch combinations are there?"
                wrong = get_wrong_ints(s_types * d_types, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total combinations = Number of sandwiches × Number of drinks = {s_types} × {d_types} = {s_types * d_types}.")
            elif difficulty == "medium":
                p1 = random.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
                p2 = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
                ans = p1 * p2
                q = f"On a tree diagram, the probability of Event A happening is {p1}. If Event A happens, the probability of Event B happening is {p2}. What is the probability that BOTH Event A and Event B happen? (Give answer as a decimal rounded to 2 decimal places)."
                ans_str = f"{ans:.2f}"
                wrong = get_wrong_floats(ans, 8, 2)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Multiply along the branches: P(A and B) = P(A) × P(B|A) = {p1} × {p2} = {ans:.2f}.")
            else:
                p1 = random.choice([0.1, 0.2, 0.3, 0.4, 0.5])
                p2 = random.choice([0.6, 0.7, 0.8, 0.9])
                p_success_A = p1 * p2
                p_fail_A = (1 - p1) * random.choice([0.1, 0.2, 0.3, 0.4])
                ans = p_success_A + p_fail_A
                q = f"A weather model uses a tree diagram. The probability of Rain is {p1}. If it rains, the probability of a traffic jam is {p2}. If it does not rain, the probability of a traffic jam is {p_fail_A / (1 - p1):.2f}. What is the overall probability of a traffic jam? (Give answer as a decimal rounded to 2 decimal places)."
                ans_str = f"{ans:.2f}"
                wrong = get_wrong_floats(ans, 8, 2)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"P(Jam) = P(Rain and Jam) + P(No Rain and Jam). P(Rain and Jam) = {p1} × {p2} = {p_success_A:.2f}. P(No Rain and Jam) = (1 - {p1}) × {p_fail_A / (1 - p1):.2f} = {p_fail_A:.2f}. Total = {ans:.2f}.")

    return gen


def generate_p2_measurement() -> MathLit12Generator:
    subtopics = ["Conversions", "Perimeter and Area", "Volume and Surface Area", "Time", "Temperature"]
    gen = MathLit12Generator("Measurement", "ML12_P2_MEAS", subtopics, "paper2")

    names = ["Kagiso", "Lebo", "Mandla", "Noxolo", "Tshepo", "Buhle", "Lerato", "Sipho", "Zanele", "Thabo", "Mpho", "Fatima", "Aisha", "John", "Sarah"]
    items = ["garden", "swimming pool", "floor", "box", "tank", "roof", "field"]

    attempts = 0
    while not gen.is_done() and attempts < 100000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        name = random.choice(names)
        item = random.choice(items)

        if subtopic == "Conversions":
            if difficulty == "easy":
                km = random.randint(2, 50)
                m = km * 1000
                q = f"Convert {km} km to meters (m)."
                ans_str = f"{m}"
                wrong = get_wrong_ints(m, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 km = 1000 m. {km} km × 1000 = {m} m.")
            elif difficulty == "medium":
                cm = random.randint(150, 950)
                m = cm / 100
                q = f"{name} measures a piece of wood as {cm} cm long. Convert this length to meters (m)."
                ans_str = f"{m:.2f}"
                wrong = get_wrong_floats(m, 8, 2)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 m = 100 cm. {cm} cm ÷ 100 = {m:.2f} m.")
            else:
                liters = random.uniform(1.5, 15.5)
                ml = liters * 1000
                q = f"A recipe requires {liters:.1f} liters of milk. How many milliliters (ml) is this?"
                ans_str = f"{int(ml)}"
                wrong = get_wrong_ints(int(ml), 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 Liter = 1000 ml. {liters:.1f} L × 1000 = {int(ml)} ml.")

        elif subtopic == "Perimeter and Area":
            if difficulty == "easy":
                l = random.randint(5, 20)
                w = random.randint(2, 10)
                area = l * w
                q = f"Calculate the area of a rectangular {item} with length {l}m and width {w}m. (Give only the numerical value in m²)."
                ans_str = f"{area}"
                wrong = get_wrong_ints(area, 8) + [str(2*(l+w))]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Area of a rectangle = length × width = {l} × {w} = {area} m².")
            elif difficulty == "medium":
                r = random.randint(3, 15)
                circumference = 2 * math.pi * r
                q = f"A circular {item} has a radius of {r}m. Calculate the circumference. (Use π ≈ 3.142 and round to 2 decimal places)."
                ans_str = f"{2 * 3.142 * r:.2f}"
                wrong = get_wrong_floats(2 * 3.142 * r, 8, 2)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Circumference = 2πr = 2 × 3.142 × {r} = {2 * 3.142 * r:.2f} m.")
            else:
                l = random.randint(8, 25)
                w = random.randint(4, 12)
                cost_per_m2 = random.randint(150, 400)
                area = l * w
                total_cost = area * cost_per_m2
                q = f"{name} wants to tile a rectangular room measuring {l}m by {w}m. If the tiles cost R{cost_per_m2} per square meter, calculate the total cost of the tiles."
                ans_str = f"R{total_cost}"
                wrong = [f"R{w}" for w in get_wrong_ints(total_cost, 8)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Area = {l} × {w} = {area} m². Total Cost = Area × Cost per m² = {area} × R{cost_per_m2} = R{total_cost}.")

        elif subtopic == "Volume and Surface Area":
            if difficulty == "easy":
                l = random.randint(2, 10)
                w = random.randint(2, 8)
                h = random.randint(2, 6)
                vol = l * w * h
                q = f"Calculate the volume of a rectangular {item} with length {l}m, width {w}m, and height {h}m. (Give only the numerical value in m³)."
                ans_str = f"{vol}"
                wrong = get_wrong_ints(vol, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Volume = length × width × height = {l} × {w} × {h} = {vol} m³.")
            elif difficulty == "medium":
                r = random.randint(2, 8)
                h = random.randint(4, 15)
                vol = math.pi * r**2 * h
                q = f"A cylindrical {item} has a radius of {r}m and a height of {h}m. Calculate its volume. (Use π ≈ 3.142 and round to 2 decimal places)."
                ans_str = f"{3.142 * r**2 * h:.2f}"
                wrong = get_wrong_floats(3.142 * r**2 * h, 8, 2)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Volume of a cylinder = πr²h = 3.142 × {r}² × {h} = {3.142 * r**2 * h:.2f} m³.")
            else:
                l = random.randint(5, 12)
                w = random.randint(4, 10)
                h = random.randint(2, 5)
                sa = 2*(l*w) + 2*(l*h) + 2*(w*h)
                q = f"{name} wants to paint the outside of a closed rectangular {item} (including top and bottom) with dimensions {l}m × {w}m × {h}m. Calculate the total surface area to be painted. (Give only the numerical value in m²)."
                ans_str = f"{sa}"
                wrong = get_wrong_ints(sa, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Surface Area = 2(lw + lh + wh) = 2({l*w} + {l*h} + {w*h}) = {sa} m².")

        elif subtopic == "Time":
            if difficulty == "easy":
                hrs = random.randint(2, 10)
                mins = hrs * 60
                q = f"Convert {hrs} hours into minutes."
                ans_str = f"{mins}"
                wrong = get_wrong_ints(mins, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 hour = 60 minutes. {hrs} hours × 60 = {mins} minutes.")
            elif difficulty == "medium":
                start_h = random.randint(6, 10)
                start_m = random.choice([0, 15, 30, 45])
                dur_h = random.randint(2, 5)
                dur_m = random.choice([20, 35, 50])
                total_m = start_m + dur_m
                end_h = start_h + dur_h + (total_m // 60)
                end_m = total_m % 60
                q = f"A bus departs at {start_h:02d}:{start_m:02d} and the journey takes {dur_h} hours and {dur_m} minutes. At what time will the bus arrive? (Format as HH:MM)."
                ans_str = f"{end_h:02d}:{end_m:02d}"
                wrong_vals = [f"{(end_h+1)%24:02d}:{end_m:02d}", f"{end_h:02d}:{(end_m+10)%60:02d}", f"{end_h-1:02d}:{end_m:02d}", f"{end_h:02d}:{(end_m-10)%60:02d}", f"{end_h+2:02d}:{end_m:02d}", f"{end_h:02d}:30", f"{end_h:02d}:00", f"{(end_h-2)%24:02d}:{end_m:02d}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong_vals, f"Add {dur_h} hours and {dur_m} minutes to {start_h:02d}:{start_m:02d}. Minutes = {start_m} + {dur_m} = {total_m}. {total_m} mins = {total_m//60} hr and {total_m%60} mins. Hours = {start_h} + {dur_h} + {total_m//60} = {end_h}. Arrival time is {end_h:02d}:{end_m:02d}.")
            else:
                dist = random.randint(150, 400)
                speed = random.randint(60, 100)
                time_h = dist / speed
                hrs = int(time_h)
                mins = int(round((time_h - hrs) * 60))
                q = f"{name} drives a distance of {dist} km at an average speed of {speed} km/h. How long does the journey take? (Give answer in hours and minutes, e.g., '2 hours 30 minutes')."
                ans_str = f"{hrs} hours {mins} minutes"
                wrong_vals = [f"{hrs} hours {mins+10} minutes", f"{hrs+1} hours {mins} minutes", f"{hrs} hours {mins-10} minutes", f"{hrs-1} hours {mins} minutes", f"{hrs} hours {int(time_h*100)%100} minutes", f"{mins} hours {hrs} minutes", f"2 hours 15 minutes", f"3 hours 45 minutes"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong_vals, f"Time = Distance ÷ Speed = {dist} ÷ {speed} = {time_h:.2f} hours. {hrs} hours. {time_h - hrs:.2f} × 60 = {mins} minutes. Total time = {hrs} hours {mins} minutes.")

        elif subtopic == "Temperature":
            if difficulty == "easy":
                c = random.randint(10, 35)
                f = (c * 9/5) + 32
                q = f"Convert a temperature of {c}°C to degrees Fahrenheit using the formula: °F = (°C × 1.8) + 32. (Round to 1 decimal place)."
                ans_str = f"{f:.1f}"
                wrong = get_wrong_floats(f, 8, 1)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"°F = ({c} × 1.8) + 32 = {c*1.8} + 32 = {f:.1f}°F.")
            elif difficulty == "medium":
                f = random.randint(50, 100)
                c = (f - 32) * 5/9
                q = f"Convert a temperature of {f}°F to degrees Celsius using the formula: °C = (°F - 32) ÷ 1.8. (Round to 1 decimal place)."
                ans_str = f"{c:.1f}"
                wrong = get_wrong_floats(c, 8, 1)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"°C = ({f} - 32) ÷ 1.8 = {f-32} ÷ 1.8 = {c:.1f}°C.")
            else:
                c1 = random.randint(-10, 5)
                c2 = c1 + random.randint(15, 30)
                diff = c2 - c1
                q = f"The temperature in a freezer is {c1}°C. During a power cut, the temperature rises to {c2}°C. What was the increase in temperature?"
                ans_str = f"{diff}°C"
                wrong = [f"{w}°C" for w in get_wrong_ints(diff, 8)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Increase = Final temp - Initial temp = {c2} - ({c1}) = {c2} + {abs(c1)} = {diff}°C.")

    return gen


def generate_p2_maps_plans() -> MathLit12Generator:
    subtopics = ["Scale", "Maps and Directions", "Models and Packaging", "Seating Plans"]
    gen = MathLit12Generator("Maps and Plans", "ML12_P2_MAPS", subtopics, "paper2")

    attempts = 0
    while not gen.is_done() and attempts < 100000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Scale":
            if difficulty == "easy":
                map_dist = random.randint(2, 15)
                scale = random.randint(500, 2000)
                real_dist = map_dist * scale
                q = f"A map has a number scale of 1:{scale}. If the distance between two towns on the map is {map_dist} cm, what is the real distance in cm?"
                ans_str = f"{real_dist}"
                wrong = get_wrong_ints(real_dist, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Real distance = Map distance × Scale factor = {map_dist} × {scale} = {real_dist} cm.")
            elif difficulty == "medium":
                map_dist = random.randint(5, 20)
                scale = random.choice([10000, 50000, 100000])
                real_cm = map_dist * scale
                real_km = real_cm / 100000
                q = f"On a map with a scale of 1:{scale}, the distance between a school and a library is {map_dist} cm. Calculate the actual distance in kilometres (km)."
                ans_str = f"{real_km:.2f}"
                wrong = get_wrong_floats(real_km, 8, 2)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Actual distance = {map_dist} × {scale} = {real_cm} cm. Convert to km: {real_cm} ÷ 100,000 = {real_km:.2f} km.")
            else:
                real_km = random.randint(10, 50)
                map_cm = random.randint(2, 10)
                real_cm = real_km * 100000
                scale_ratio = real_cm / map_cm
                q = f"The actual distance between City A and City B is {real_km} km. On a map, this distance is represented by {map_cm} cm. Determine the number scale of the map in the form 1:..."
                ans_str = f"1:{int(scale_ratio)}"
                wrong_vals = [int(scale_ratio*10), int(scale_ratio/10), int(scale_ratio+1000), int(scale_ratio-1000), int(real_km/map_cm), int(real_cm)]
                wrong = [f"1:{w}" for w in wrong_vals] + [f"1:{w}" for w in get_wrong_ints(int(scale_ratio), 4)]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"{real_km} km = {real_cm} cm. Scale = {map_cm}:{real_cm} = 1:{int(scale_ratio)}.")

        elif subtopic == "Maps and Directions":
            if difficulty == "easy":
                q = "If you are facing North and you turn 90° clockwise, which direction are you now facing?"
                ans_str = "East"
                wrong = ["South", "West", "North-East", "South-East", "North-West", "South-West"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Turning 90° clockwise from North points you East.")
            elif difficulty == "medium":
                q = "A tourist is walking South along Main Street, then takes the first left turn into First Avenue. Which direction is the tourist now walking?"
                ans_str = "East"
                wrong = ["North", "South", "West", "North-East", "South-East", "North-West", "South-West"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Walking South means facing down on a map. Turning left (from the perspective of someone facing South) points you East.")
            else:
                q = "On a street map, Hospital Road runs parallel to Station Road, and both are intersected by Church Street at a 90° angle. If you are travelling North on Church Street and turn right onto Station Road, which direction are you now travelling?"
                ans_str = "East"
                wrong = ["North", "South", "West", "North-East", "South-East", "North-West", "South-West"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Travelling North and turning right means you turn 90° clockwise. You are now travelling East.")

        elif subtopic == "Models and Packaging":
            if difficulty == "easy":
                side = random.randint(2, 8)
                vol = side**3
                q = f"Calculate the volume of a cubic packaging box with a side length of {side} cm. (Give only the numerical value in cm³)."
                ans_str = f"{vol}"
                wrong = get_wrong_ints(vol, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Volume of a cube = side × side × side = {side} × {side} × {side} = {vol} cm³.")
            elif difficulty == "medium":
                small_side = random.randint(2, 5)
                large_l = random.randint(10, 20)
                large_w = random.randint(10, 20)
                large_h = random.randint(5, 15)
                fit_l = large_l // small_side
                fit_w = large_w // small_side
                fit_h = large_h // small_side
                total_fit = fit_l * fit_w * fit_h
                q = f"A company packs small cubic boxes of side {small_side} cm into a larger container measuring {large_l} cm by {large_w} cm by {large_h} cm. Assuming all boxes must be packed upright and squarely, how many small boxes can fit into the large container?"
                ans_str = f"{total_fit}"
                wrong = get_wrong_ints(total_fit, 8) + [str((large_l*large_w*large_h)//(small_side**3))]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Lengthways: {large_l} ÷ {small_side} = {fit_l}. Widthways: {large_w} ÷ {small_side} = {fit_w}. Heightways: {large_h} ÷ {small_side} = {fit_h}. Total = {fit_l} × {fit_w} × {fit_h} = {total_fit}.")
            else:
                r = random.randint(3, 8)
                h = random.randint(10, 25)
                diam = r * 2
                box_l = diam * random.randint(2, 5)
                box_w = diam * random.randint(2, 4)
                box_h = h
                fit_l = box_l // diam
                fit_w = box_w // diam
                total_cans = fit_l * fit_w
                q = f"Cylindrical cans of radius {r} cm and height {h} cm are to be packed upright into a rectangular box of dimensions {box_l} cm × {box_w} cm × {box_h} cm. How many cans will fit into the box?"
                ans_str = f"{total_cans}"
                wrong = get_wrong_ints(total_cans, 8) + [str((box_l*box_w*box_h)//int(math.pi*r**2*h))]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Diameter of can = {r} × 2 = {diam} cm. Fit lengthways = {box_l} ÷ {diam} = {fit_l}. Fit widthways = {box_w} ÷ {diam} = {fit_w}. Total cans = {fit_l} × {fit_w} = {total_cans}.")

        elif subtopic == "Seating Plans":
            if difficulty == "easy":
                rows = random.randint(10, 20)
                seats_per_row = random.randint(15, 30)
                total_seats = rows * seats_per_row
                q = f"A cinema has {rows} rows of seats, and each row has {seats_per_row} seats. How many seats are there in total?"
                ans_str = f"{total_seats}"
                wrong = get_wrong_ints(total_seats, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total seats = {rows} × {seats_per_row} = {total_seats}.")
            elif difficulty == "medium":
                rows = random.randint(12, 25)
                seats_per_row = random.randint(15, 35)
                vip = random.randint(20, 50)
                standard = (rows * seats_per_row) - vip
                q = f"A theatre seating plan has {rows} rows with {seats_per_row} seats each. If the first {vip} seats are reserved for VIPs, how many standard seats are available?"
                ans_str = f"{standard}"
                wrong = get_wrong_ints(standard, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total seats = {rows} × {seats_per_row} = {rows * seats_per_row}. Standard = {rows * seats_per_row} - {vip} = {standard}.")
            else:
                total_seats = random.randint(300, 800)
                blocks = random.randint(3, 5)
                aisle = blocks - 1
                q = f"A hall has {total_seats} seats arranged uniformly across {blocks} seating blocks separated by {aisle} aisles. If each block has 10 rows, how many seats are there in a single row of one block?"
                seats_per_block = total_seats // blocks
                seats_per_row_in_block = seats_per_block // 10
                ans_str = f"{seats_per_row_in_block}"
                wrong = get_wrong_ints(seats_per_row_in_block, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Seats per block = {total_seats} ÷ {blocks} = {seats_per_block}. Seats per row in one block = {seats_per_block} ÷ 10 = {seats_per_row_in_block}.")

    return gen


def generate_p2_probability() -> MathLit12Generator:
    subtopics = ["Contextual Probability", "Combined Events", "Two-way Tables"]
    gen = MathLit12Generator("Probability (P2)", "ML12_P2_PROB", subtopics, "paper2")

    attempts = 0
    while not gen.is_done() and attempts < 100000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Contextual Probability":
            if difficulty == "easy":
                faulty = random.randint(2, 10)
                total = random.randint(50, 200)
                q = f"A factory produces {total} lightbulbs in an hour, and quality control finds that {faulty} of them are faulty. What is the probability that a lightbulb chosen at random is faulty? (Give as a fraction)."
                ans_str = f"{faulty}/{total}"
                wrong = [f"{total-faulty}/{total}", f"{faulty}/{total-faulty}", f"1/{total}", f"{faulty+1}/{total}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Probability = Favorable outcomes / Total = {faulty}/{total}.")
            elif difficulty == "medium":
                total = random.randint(500, 1500)
                won = random.randint(100, 300)
                q = f"In a scratch-card competition, {total} cards were printed and {won} contain a winning prize. If you buy one card, what is the probability that you DO NOT win a prize? (Give as a percentage, rounded to 1 decimal place)."
                prob_not_win = ((total - won) / total) * 100
                ans_str = f"{prob_not_win:.1f}%"
                wrong = [f"{w}%" for w in get_wrong_floats(prob_not_win, 8, 1)] + [f"{(won/total)*100:.1f}%"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Cards without a prize = {total} - {won} = {total - won}. Probability = ({total - won} / {total}) × 100 = {prob_not_win:.1f}%.")
            else:
                rain_prob = random.choice([0.15, 0.25, 0.35, 0.45])
                q = f"A weather forecast predicts a {rain_prob*100:.0f}% chance of rain on Saturday and a {(rain_prob+0.1)*100:.0f}% chance of rain on Sunday. Assuming these events are independent, what is the probability that it rains on BOTH days? (Give as a decimal)."
                ans = rain_prob * (rain_prob + 0.1)
                ans_str = f"{ans:.4f}"
                wrong = get_wrong_floats(ans, 8, 4)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"P(Sat and Sun) = P(Sat) × P(Sun) = {rain_prob} × {rain_prob+0.1} = {ans:.4f}.")

        elif subtopic == "Combined Events":
            if difficulty == "easy":
                q = "A coin is flipped and a 6-sided die is rolled. How many possible combined outcomes are there?"
                ans_str = "12"
                wrong = ["8", "6", "2", "36", "10", "14", "18"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Coin outcomes = 2. Die outcomes = 6. Total combined outcomes = 2 × 6 = 12.")
            elif difficulty == "medium":
                q = "Two fair 6-sided dice are rolled simultaneously. What is the probability that the sum of the numbers rolled is exactly 7? (Give as a fraction in simplest form)."
                ans_str = "1/6"
                wrong = ["7/36", "1/12", "1/36", "1/4", "1/3", "1/2", "5/36"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total outcomes = 36. Outcomes giving sum of 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 outcomes. Probability = 6/36 = 1/6.")
            else:
                q = "A standard deck of 52 playing cards contains 4 suits (Hearts, Diamonds, Clubs, Spades) of 13 cards each. What is the probability of drawing a Heart OR a 'Queen'? (Give as a fraction)."
                ans_str = "16/52"
                wrong = ["13/52", "4/52", "17/52", "1/52", "12/52", "14/52"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Hearts = 13. Queens = 4. Queens of Hearts = 1. P(Heart or Queen) = P(Heart) + P(Queen) - P(Queen of Hearts) = 13/52 + 4/52 - 1/52 = 16/52.")

        elif subtopic == "Two-way Tables":
            if difficulty == "easy":
                boys_math = random.randint(10, 25)
                boys_lit = random.randint(10, 25)
                girls_math = random.randint(10, 25)
                girls_lit = random.randint(10, 25)
                total = boys_math + boys_lit + girls_math + girls_lit
                q = f"A school survey on subject choices showed: Boys taking Math= {boys_math}, Boys taking Math Lit= {boys_lit}, Girls taking Math= {girls_math}, Girls taking Math Lit= {girls_lit}. How many learners participated in total?"
                ans_str = f"{total}"
                wrong = get_wrong_ints(total, 8)
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total = {boys_math} + {boys_lit} + {girls_math} + {girls_lit} = {total}.")
            elif difficulty == "medium":
                b_m = random.randint(15, 30)
                b_l = random.randint(15, 30)
                g_m = random.randint(15, 30)
                g_l = random.randint(15, 30)
                total_boys = b_m + b_l
                total = b_m + b_l + g_m + g_l
                q = f"A two-way table shows subject choices: Boys taking Math= {b_m}, Boys taking Math Lit= {b_l}, Girls taking Math= {g_m}, Girls taking Math Lit= {g_l}. If a learner is chosen at random, what is the probability that the learner is a Boy? (Give as a fraction)."
                ans_str = f"{total_boys}/{total}"
                wrong = [f"{b_m}/{total}", f"{b_l}/{total}", f"{(g_m+g_l)}/{total}", f"{total_boys}/100", f"{b_m}/{total_boys}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total Boys = {b_m} + {b_l} = {total_boys}. Total Learners = {total}. Probability = {total_boys}/{total}.")
            else:
                b_m = random.randint(10, 20)
                b_l = random.randint(10, 20)
                g_m = random.randint(10, 20)
                g_l = random.randint(10, 20)
                total_math = b_m + g_m
                total = b_m + b_l + g_m + g_l
                q = f"Data: Boys taking Math= {b_m}, Boys taking Math Lit= {b_l}, Girls taking Math= {g_m}, Girls taking Math Lit= {g_l}. A learner is selected at random and it is known that they take Math. What is the probability that this learner is a Girl? (Give as a decimal rounded to 2 decimal places)."
                ans = g_m / total_math
                ans_str = f"{ans:.2f}"
                wrong = get_wrong_floats(ans, 8, 2) + [f"{(g_m/total):.2f}"]
                gen.add_question(subtopic, difficulty, q, ans_str, wrong, f"This is conditional probability. Total taking Math = {b_m} + {g_m} = {total_math}. Number of Girls taking Math = {g_m}. P(Girl | Math) = {g_m} / {total_math} = {ans:.2f}.")

    return gen

if __name__ == "__main__":
    random.seed(42)
    os.makedirs("dataset/mathematical_literacy", exist_ok=True)

    print("Generating Paper 1 Finance...")
    p1_finance = generate_p1_finance()
    p1_finance.save_to_json("dataset/mathematical_literacy/paper1_mathlit12_finance.json")

    print("Generating Paper 1 Data Handling...")
    p1_data = generate_p1_data_handling()
    p1_data.save_to_json("dataset/mathematical_literacy/paper1_mathlit12_data_handling.json")

    print("Generating Paper 1 Probability...")
    p1_prob = generate_p1_probability()
    p1_prob.save_to_json("dataset/mathematical_literacy/paper1_mathlit12_probability.json")

    print("Generating Paper 2 Measurement...")
    p2_meas = generate_p2_measurement()
    p2_meas.save_to_json("dataset/mathematical_literacy/paper2_mathlit12_measurement.json")

    print("Generating Paper 2 Maps and Plans...")
    p2_maps = generate_p2_maps_plans()
    p2_maps.save_to_json("dataset/mathematical_literacy/paper2_mathlit12_maps_plans.json")

    print("Generating Paper 2 Probability...")
    p2_prob = generate_p2_probability()
    p2_prob.save_to_json("dataset/mathematical_literacy/paper2_mathlit12_probability.json")

    print("Done! All 6 Grade 12 Math Lit files generated in dataset/mathematical_literacy/")
