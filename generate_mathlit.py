import os
import random
import math
from generator_base import TopicGenerator

def generate_wrong_answers(correct_answer, answer_type="currency", num_wrong=8):
    """
    Generate plausible wrong answers based on the type.
    We return strings.
    """
    wrong = set()
    try:
        if answer_type == "currency":
            # Extract number
            val_str = str(correct_answer).replace("R", "").replace(",", "").strip()
            val = float(val_str)

            # Common mistakes
            mistakes = [
                val * 12, # months instead of years or vice versa
                val / 12,
                val * 10,
                val / 10,
                val * 1.15, # adding VAT incorrectly
                val * 0.85, # subtracting VAT incorrectly
                val * 2,
                val / 2,
                val + 100,
                val - 100,
                val * 100,
                val / 100
            ]
            for m in mistakes:
                if m > 0:
                    if m.is_integer():
                        wrong.add(f"R{int(m)}")
                    else:
                        wrong.add(f"R{m:.2f}")

            # Random tweaks
            while len(wrong) < num_wrong * 2:
                r = val * random.uniform(0.5, 1.5)
                if r > 0:
                    if r.is_integer():
                        wrong.add(f"R{int(r)}")
                    else:
                        wrong.add(f"R{r:.2f}")

        elif answer_type == "percentage":
            val_str = str(correct_answer).replace("%", "").strip()
            val = float(val_str)

            mistakes = [
                val * 100,
                val / 100,
                100 - val,
                val + 10,
                val - 10,
                val * 2,
                val / 2
            ]
            for m in mistakes:
                if m >= 0 and m <= 100:
                    if m.is_integer():
                        wrong.add(f"{int(m)}%")
                    else:
                        wrong.add(f"{m:.1f}%")

            while len(wrong) < num_wrong * 2:
                r = val + random.uniform(-20, 20)
                if r >= 0 and r <= 100:
                    if r.is_integer():
                        wrong.add(f"{int(r)}%")
                    else:
                        wrong.add(f"{r:.1f}%")

        elif answer_type == "number":
            val = float(str(correct_answer).split()[0])
            unit = " ".join(str(correct_answer).split()[1:])

            mistakes = [
                val * 10,
                val / 10,
                val * 100,
                val / 100,
                val * 1000,
                val / 1000,
                val * 2,
                val / 2
            ]

            for m in mistakes:
                if m > 0:
                    if m.is_integer() or m == int(m):
                        res = f"{int(m)}"
                    else:
                        res = f"{m:.2f}"

                    if unit:
                        res += f" {unit}"
                    wrong.add(res)

            while len(wrong) < num_wrong * 2:
                r = val * random.uniform(0.1, 5.0)
                if r > 0:
                    if r.is_integer():
                        res = f"{int(r)}"
                    else:
                        res = f"{r:.2f}"
                    if unit:
                        res += f" {unit}"
                    wrong.add(res)

        elif answer_type == "time":
             val = float(str(correct_answer).split()[0])
             unit = " ".join(str(correct_answer).split()[1:])
             mistakes = [
                 val * 60,
                 val / 60,
                 val * 24,
                 val / 24,
                 val * 7,
                 val / 7,
                 val * 12,
                 val / 12
             ]
             for m in mistakes:
                if m > 0:
                    if m.is_integer():
                        res = f"{int(m)}"
                    else:
                        res = f"{m:.2f}"

                    if unit:
                        res += f" {unit}"
                    wrong.add(res)

             while len(wrong) < num_wrong * 2:
                r = val * random.uniform(0.5, 2.0)
                if r > 0:
                    if r.is_integer():
                        res = f"{int(r)}"
                    else:
                        res = f"{r:.2f}"
                    if unit:
                        res += f" {unit}"
                    wrong.add(res)
    except Exception as e:
        # Fallback to simple numeric randomizing
        pass

    # Ensure correct answer is not in wrong pool
    wrong.discard(str(correct_answer))

    wrong_list = list(wrong)
    random.shuffle(wrong_list)
    return wrong_list[:num_wrong]

def generate_finance_questions():
    generator = TopicGenerator(
        topic_name="Finance",
        topic_prefix="ML_FIN",
        subtopics=["Income", "Expenses", "Budgets", "Tax", "Interest"]
    )

    names = ["Thabo", "Sipho", "Lerato", "Zanele", "Johan", "Fatima", "Kabelo", "Naledi", "Lindiwe", "Tariq"]
    jobs = ["teacher", "nurse", "electrician", "cashier", "manager", "plumber"]

    while not generator.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(generator.subtopics)
        name = random.choice(names)

        if subtopic == "Income":
            if difficulty == "easy":
                wage = random.randint(30, 80)
                hours = random.randint(5, 12)
                ans = wage * hours
                q = f"{name} earns R{wage} per hour. If they work for {hours} hours, calculate their total income."
                ans_str = f"R{ans}"
                wrong = [f"R{wage + hours}", f"R{ans * 2}", f"R{ans / 2}", f"R{ans + 100}", f"R{ans - 50}", f"R{wage * (hours + 1)}", f"R{wage * (hours - 1)}", f"R{ans + wage}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total Income = Hourly Wage × Hours Worked = {wage} × {hours} = R{ans}.")
            elif difficulty == "medium":
                monthly = random.randint(5000, 15000)
                bonus_pct = random.randint(5, 15)
                bonus = monthly * (bonus_pct / 100)
                ans = monthly + bonus
                q = f"{name} earns a basic monthly salary of R{monthly}. This month, they receive a {bonus_pct}% bonus. Calculate their total income for the month."
                ans_str = f"R{int(ans)}"
                wrong = [f"R{int(monthly + bonus_pct)}", f"R{int(monthly - bonus)}", f"R{int(monthly + (bonus*2))}", f"R{int(ans + 1000)}", f"R{int(bonus)}", f"R{int(monthly * bonus_pct)}", f"R{int(monthly / (bonus_pct/100))}", f"R{int(ans - 500)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Bonus = {bonus_pct}% of R{monthly} = R{int(bonus)}. Total Income = R{monthly} + R{int(bonus)} = R{int(ans)}.")
            else:
                annual = random.randint(120000, 300000)
                deductions = random.randint(1500, 4000)
                monthly_gross = annual / 12
                ans = monthly_gross - deductions
                q = f"{name}'s annual gross salary is R{annual}. Each month, R{deductions} is deducted for UIF and pension. Calculate their net monthly income."
                ans_str = f"R{int(ans)}"
                wrong = [f"R{int((annual - deductions) / 12)}", f"R{int(annual - deductions)}", f"R{int(monthly_gross + deductions)}", f"R{int(ans * 12)}", f"R{int(monthly_gross)}", f"R{int((annual/12) - (deductions*12))}", f"R{int(ans + 2000)}", f"R{int(ans - 1000)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Monthly Gross = R{annual} ÷ 12 = R{int(monthly_gross)}. Net Monthly Income = R{int(monthly_gross)} - R{deductions} = R{int(ans)}.")

        elif subtopic == "Expenses":
            if difficulty == "easy":
                bread = random.randint(15, 20)
                milk = random.randint(25, 35)
                ans = bread + milk
                q = f"{name} buys a loaf of bread for R{bread} and milk for R{milk}. What is their total expense?"
                ans_str = f"R{ans}"
                wrong = [f"R{abs(bread - milk)}", f"R{bread * milk}", f"R{ans + 10}", f"R{ans - 5}", f"R{bread}", f"R{milk}", f"R{ans + 20}", f"R{ans - 10}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total Expense = R{bread} + R{milk} = R{ans}.")
            elif difficulty == "medium":
                rent = random.randint(3000, 6000)
                groceries = random.randint(1500, 3000)
                transport = random.randint(500, 1500)
                ans = rent + groceries + transport
                q = f"{name}'s monthly expenses are: Rent R{rent}, Groceries R{groceries}, and Transport R{transport}. Calculate their total monthly expenses."
                ans_str = f"R{ans}"
                wrong = [f"R{rent + groceries}", f"R{rent + transport}", f"R{ans * 12}", f"R{ans + 1000}", f"R{ans - 500}", f"R{rent}", f"R{int(ans * 1.15)}", f"R{int(ans * 0.85)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total = R{rent} + R{groceries} + R{transport} = R{ans}.")
            else:
                total_budget = random.randint(10000, 20000)
                rent_pct = random.randint(25, 40)
                ans = total_budget * (rent_pct / 100)
                q = f"{name} has a monthly budget of R{total_budget}. They spend {rent_pct}% of their budget on rent. How much do they spend on rent?"
                ans_str = f"R{int(ans)}"
                wrong = [f"R{int(total_budget - ans)}", f"R{int(ans * 12)}", f"R{int(total_budget / (rent_pct/100))}", f"R{rent_pct}", f"R{int(total_budget + ans)}", f"R{int(ans / 2)}", f"R{int(ans * 2)}", f"R{int(ans + 500)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Rent Expense = {rent_pct}% of R{total_budget} = ( {rent_pct} ÷ 100 ) × {total_budget} = R{int(ans)}.")

        elif subtopic == "Budgets":
            if difficulty == "easy":
                income = random.randint(3000, 8000)
                expenses = random.randint(2000, income - 500)
                ans = income - expenses
                q = f"{name}'s income is R{income} and expenses are R{expenses}. Calculate their surplus (savings)."
                ans_str = f"R{ans}"
                wrong = [f"R{income + expenses}", f"R{expenses - income}", f"R{ans + 500}", f"R{ans - 200}", f"R{income}", f"R{expenses}", f"R{ans * 12}", f"R{ans * 2}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Surplus = Income - Expenses = R{income} - R{expenses} = R{ans}.")
            elif difficulty == "medium":
                income = random.randint(10000, 25000)
                rent = random.randint(3000, 7000)
                food = random.randint(2000, 5000)
                ans = income - (rent + food)
                q = f"{name} earns R{income} per month. They budget R{rent} for rent and R{food} for food. How much money is left for other expenses?"
                ans_str = f"R{ans}"
                wrong = [f"R{income + rent + food}", f"R{rent + food}", f"R{income - rent + food}", f"R{ans + 1000}", f"R{ans - 500}", f"R{int(ans * 1.15)}", f"R{income - food}", f"R{income - rent}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total budgeted = R{rent} + R{food} = R{rent + food}. Remaining = R{income} - R{rent + food} = R{ans}.")
            else:
                income = random.randint(15000, 30000)
                savings_pct = random.randint(10, 20)
                ans = income * (savings_pct / 100)
                q = f"{name} plans to save {savings_pct}% of their monthly income of R{income}. How much money should they put into savings?"
                ans_str = f"R{int(ans)}"
                wrong = [f"R{int(income - ans)}", f"R{int(income + ans)}", f"R{int(ans * 12)}", f"R{int(income / (savings_pct/100))}", f"R{savings_pct}", f"R{int(ans / 2)}", f"R{int(ans * 2)}", f"R{int(ans + 1000)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Savings = {savings_pct}% of R{income} = ( {savings_pct} ÷ 100 ) × {income} = R{int(ans)}.")

        elif subtopic == "Tax":
            if difficulty == "easy":
                price = random.randint(100, 500)
                vat = price * 0.15
                ans = price + vat
                q = f"An item costs R{price} before VAT. If VAT is 15%, calculate the total price including VAT."
                ans_str = f"R{ans:.2f}"
                wrong = [f"R{price - vat:.2f}", f"R{price:.2f}", f"R{vat:.2f}", f"R{(price * 1.14):.2f}", f"R{(price * 1.20):.2f}", f"R{price + 15:.2f}", f"R{price - 15:.2f}", f"R{ans + 50:.2f}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"VAT = 15% of R{price} = R{vat:.2f}. Total Price = R{price} + R{vat:.2f} = R{ans:.2f}.")
            elif difficulty == "medium":
                total_price = random.randint(230, 1150) # Multiple of 1.15
                price_excl = total_price / 1.15
                ans = total_price - price_excl
                q = f"A TV costs R{total_price} including 15% VAT. Calculate the amount of VAT included in the price."
                ans_str = f"R{ans:.2f}"
                wrong = [f"R{(total_price * 0.15):.2f}", f"R{price_excl:.2f}", f"R{total_price:.2f}", f"R{(total_price * 0.85):.2f}", f"R{(total_price / 1.14):.2f}", f"R{(total_price / 1.20):.2f}", f"R{ans * 2:.2f}", f"R{ans + 50:.2f}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Price Excluding VAT = R{total_price} ÷ 1.15 = R{price_excl:.2f}. VAT Amount = R{total_price} - R{price_excl:.2f} = R{ans:.2f}.")
            else:
                taxable = random.randint(200000, 300000)
                base_tax = random.randint(30000, 45000)
                rate = random.randint(20, 30)
                threshold = 200000
                tax = base_tax + ((taxable - threshold) * (rate / 100))
                q = f"{name} has a taxable income of R{taxable}. According to the tax tables, they must pay R{base_tax} plus {rate}% of the amount over R{threshold}. Calculate their total tax payable."
                ans_str = f"R{int(tax)}"
                wrong = [f"R{int(base_tax)}", f"R{int(taxable * (rate/100))}", f"R{int(base_tax + (taxable * (rate/100)))}", f"R{int((taxable - threshold) * (rate/100))}", f"R{int(tax + 5000)}", f"R{int(tax - 5000)}", f"R{int(taxable - tax)}", f"R{int(taxable * 0.15)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Amount over threshold = R{taxable} - R{threshold} = R{taxable - threshold}. {rate}% of R{taxable - threshold} = R{int((taxable - threshold) * (rate/100))}. Total Tax = R{base_tax} + R{int((taxable - threshold) * (rate/100))} = R{int(tax)}.")

        elif subtopic == "Interest":
            if difficulty == "easy":
                P = random.randint(1000, 5000)
                r = random.randint(5, 12)
                t = random.randint(2, 5)
                ans = P * (r / 100) * t
                q = f"Calculate the simple interest on R{P} invested at {r}% per year for {t} years."
                ans_str = f"R{int(ans)}"
                wrong = [f"R{int(P + ans)}", f"R{int(P * (r/100))}", f"R{int(ans / t)}", f"R{int(P * r * t)}", f"R{int(ans * 12)}", f"R{int(ans + 100)}", f"R{int(ans - 50)}", f"R{int(P * ((1 + r/100)**t) - P)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Simple Interest = P × r × t = {P} × {r/100} × {t} = R{int(ans)}.")
            elif difficulty == "medium":
                P = random.randint(2000, 10000)
                r = random.randint(5, 12)
                t = random.randint(2, 5)
                ans = P * ((1 + (r / 100)) ** t)
                q = f"{name} invests R{P} in a bank that pays {r}% compound interest per year. Calculate the final amount after {t} years. (Round to 2 decimal places)."
                ans_str = f"R{ans:.2f}"
                wrong = [f"R{P + (P * (r/100) * t):.2f}", f"R{ans - P:.2f}", f"R{P * (r/100) * t:.2f}", f"R{ans * 1.15:.2f}", f"R{P * ((1 + r/100)**(t*12)):.2f}", f"R{P * ((1 + (r/100)/12)**(t*12)):.2f}", f"R{ans + 500:.2f}", f"R{ans - 200:.2f}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"A = P(1 + r)ⁿ = {P}(1 + {r/100})^{t} = R{ans:.2f}.")
            else:
                A = random.randint(15000, 30000)
                r = random.randint(6, 10)
                t = random.randint(3, 6)
                P = A / (1 + (r/100)*t)
                q = f"{name} wants to have R{A} in {t} years' time. If an account offers {r}% simple interest per year, how much must they invest now? (Round to nearest Rand)."
                ans_str = f"R{int(P)}"
                wrong = [f"R{int(A - (A * (r/100) * t))}", f"R{int(A / ((1 + r/100)**t))}", f"R{int(A * (r/100) * t)}", f"R{int(A)}", f"R{int(P + 1000)}", f"R{int(P - 500)}", f"R{int(A * (1 + (r/100)*t))}", f"R{int(A / (r/100) / t)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"A = P(1 + rt) ⇒ {A} = P(1 + {r/100} × {t}) ⇒ P = {A} ÷ {1 + (r/100)*t} = R{int(P)}.")

    return generator

def generate_measurement_questions():
    generator = TopicGenerator(
        topic_name="Measurement",
        topic_prefix="ML_MEAS",
        subtopics=["Length", "Area", "Volume", "Time"]
    )

    names = ["Kagiso", "Lebo", "Mandla", "Noxolo", "Tshepo", "Buhle"]

    while not generator.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(generator.subtopics)
        name = random.choice(names)

        if subtopic == "Length":
            if difficulty == "easy":
                cm = random.randint(150, 500)
                m = cm / 100
                q = f"Convert {cm} cm to metres (m)."
                ans_str = f"{m} m"
                wrong = [f"{cm * 100} m", f"{cm * 10} m", f"{cm / 10} m", f"{cm / 1000} m", f"{cm} m", f"{m + 1} m", f"{m * 2} m", f"{m / 2} m"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 m = 100 cm. So, {cm} ÷ 100 = {m} m.")
            elif difficulty == "medium":
                km = random.randint(5, 50)
                m_add = random.randint(100, 900)
                total_m = (km * 1000) + m_add
                q = f"{name} runs {km} km and walks {m_add} m. Calculate the total distance covered in metres (m)."
                ans_str = f"{total_m} m"
                wrong = [f"{km + m_add} m", f"{(km * 100) + m_add} m", f"{km * 1000} m", f"{(km * 1000) - m_add} m", f"{m_add / 1000} m", f"{total_m * 10} m", f"{total_m / 10} m", f"{km * 1000 + m_add * 1000} m"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"{km} km = {km * 1000} m. Total = {km * 1000} m + {m_add} m = {total_m} m.")
            else:
                length = random.randint(10, 30)
                width = random.randint(5, 15)
                perimeter = 2 * (length + width)
                q = f"A rectangular garden has a length of {length} m and a width of {width} m. Calculate the perimeter of the garden."
                ans_str = f"{perimeter} m"
                wrong = [f"{length * width} m", f"{length + width} m", f"{perimeter * 2} m", f"{perimeter / 2} m", f"{(2 * length) + width} m", f"{length + (2 * width)} m", f"{length * 2 * width * 2} m", f"{perimeter + 10} m"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Perimeter = 2 × (Length + Width) = 2 × ({length} + {width}) = 2 × {length + width} = {perimeter} m.")

        elif subtopic == "Area":
            if difficulty == "easy":
                side = random.randint(4, 15)
                area = side * side
                q = f"Calculate the area of a square room with a side length of {side} m."
                ans_str = f"{area} m²"
                wrong = [f"{side * 4} m²", f"{side * 2} m²", f"{area * 2} m²", f"{area / 2} m²", f"{side + side} m²", f"{side ** 3} m²", f"{area + 10} m²", f"{area - 5} m²"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Area of a square = side × side = {side} × {side} = {area} m².")
            elif difficulty == "medium":
                length = random.randint(10, 25)
                width = random.randint(5, 15)
                area = length * width
                q = f"A rectangular swimming pool is {length} m long and {width} m wide. Calculate the area of the pool."
                ans_str = f"{area} m²"
                wrong = [f"{2 * (length + width)} m²", f"{length + width} m²", f"{area * 2} m²", f"{area / 2} m²", f"{(length * width) * 2} m²", f"{(length * width) + 10} m²", f"{length * length} m²", f"{width * width} m²"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Area = Length × Width = {length} × {width} = {area} m².")
            else:
                radius = random.randint(3, 12)
                area = math.pi * (radius ** 2)
                q = f"Calculate the area of a circular patio with a radius of {radius} m. (Use π = 3.14, round to 2 decimal places)."
                ans_round = round(3.14 * (radius ** 2), 2)
                ans_str = f"{ans_round} m²"
                wrong = [f"{round(2 * 3.14 * radius, 2)} m²", f"{round(3.14 * radius, 2)} m²", f"{round(3.14 * (radius ** 2) * 2, 2)} m²", f"{round(3.14 * ((radius * 2) ** 2), 2)} m²", f"{round(3.14 * (radius ** 3), 2)} m²", f"{round((3.14 * radius) ** 2, 2)} m²", f"{round(ans_round + 10, 2)} m²", f"{round(ans_round / 2, 2)} m²"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Area = π × r² = 3.14 × {radius}² = 3.14 × {radius ** 2} = {ans_round} m².")

        elif subtopic == "Volume":
            if difficulty == "easy":
                litres = random.randint(2, 10)
                ml = litres * 1000
                q = f"Convert {litres} litres to millilitres (ml)."
                ans_str = f"{ml} ml"
                wrong = [f"{litres * 100} ml", f"{litres * 10} ml", f"{litres / 1000} ml", f"{litres} ml", f"{ml * 10} ml", f"{ml / 10} ml", f"{ml + 1000} ml", f"{ml - 500} ml"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 litre = 1000 ml. So, {litres} × 1000 = {ml} ml.")
            elif difficulty == "medium":
                length = random.randint(4, 10)
                width = random.randint(3, 8)
                height = random.randint(2, 6)
                vol = length * width * height
                q = f"A rectangular water tank has a length of {length} m, a width of {width} m, and a height of {height} m. Calculate its volume."
                ans_str = f"{vol} m³"
                wrong = [f"{(length * width) + height} m³", f"{length + width + height} m³", f"{2 * (length + width + height)} m³", f"{vol * 1000} m³", f"{vol / 2} m³", f"{vol * 2} m³", f"{(length * width) * 2} m³", f"{vol + 10} m³"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Volume = Length × Width × Height = {length} × {width} × {height} = {vol} m³.")
            else:
                radius = random.randint(2, 6)
                height = random.randint(5, 15)
                vol = 3.14 * (radius ** 2) * height
                ans_round = round(vol, 2)
                q = f"Calculate the volume of a cylindrical container with a radius of {radius} m and a height of {height} m. (Use π = 3.14, round to 2 decimal places)."
                ans_str = f"{ans_round} m³"
                wrong = [f"{round(3.14 * radius * height, 2)} m³", f"{round(2 * 3.14 * radius * height, 2)} m³", f"{round(3.14 * ((radius * 2) ** 2) * height, 2)} m³", f"{round(3.14 * (radius ** 2) * (height ** 2), 2)} m³", f"{round(ans_round * 1000, 2)} m³", f"{round(ans_round / 2, 2)} m³", f"{round(ans_round * 2, 2)} m³", f"{round(3.14 * (radius ** 3) * height, 2)} m³"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Volume = π × r² × h = 3.14 × {radius}² × {height} = 3.14 × {radius ** 2} × {height} = {ans_round} m³.")

        elif subtopic == "Time":
            if difficulty == "easy":
                mins = random.randint(120, 300)
                hours = mins // 60
                rem_mins = mins % 60
                q = f"Convert {mins} minutes into hours and minutes."
                ans_str = f"{hours} hours {rem_mins} minutes" if rem_mins > 0 else f"{hours} hours"
                wrong = [f"{mins / 100} hours", f"{mins * 60} hours", f"{hours} hours {rem_mins + 10} minutes", f"{hours + 1} hours {rem_mins} minutes", f"{hours} hours {mins} minutes", f"{hours * 2} hours", f"{mins / 24} hours", f"{hours} hours {rem_mins - 10} minutes" if rem_mins > 10 else f"{hours - 1} hours {rem_mins + 20} minutes"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 hour = 60 minutes. {mins} ÷ 60 = {hours} with a remainder of {rem_mins}. So, {ans_str}.")
            elif difficulty == "medium":
                start_h = random.randint(8, 11)
                start_m = random.randint(10, 50)
                dur_h = random.randint(2, 4)
                dur_m = random.randint(15, 45)
                end_m = (start_m + dur_m) % 60
                end_h = start_h + dur_h + ((start_m + dur_m) // 60)
                q = f"A bus departs at {start_h:02d}:{start_m:02d} and the journey takes {dur_h} hours and {dur_m} minutes. At what time does the bus arrive?"
                ans_str = f"{end_h:02d}:{end_m:02d}"
                wrong = [f"{start_h + dur_h:02d}:{start_m + dur_m:02d}" if start_m + dur_m < 60 else f"{start_h + dur_h:02d}:{(start_m + dur_m) % 100:02d}", f"{end_h + 1:02d}:{end_m:02d}", f"{end_h - 1:02d}:{end_m:02d}", f"{end_h:02d}:{end_m + 10:02d}", f"{end_h:02d}:{end_m - 10:02d}", f"{start_h + dur_h:02d}:{end_m:02d}", f"{end_h + 12:02d}:{end_m:02d}", f"{start_h + dur_h:02d}:{start_m:02d}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"{start_h:02d}:{start_m:02d} + {dur_h}h {dur_m}m = {end_h:02d}:{end_m:02d}.")
            else:
                days = random.randint(3, 7)
                hours = random.randint(5, 20)
                total_hours = (days * 24) + hours
                q = f"A project takes {days} days and {hours} hours to complete. Convert the total time taken into hours."
                ans_str = f"{total_hours} hours"
                wrong = [f"{(days * 12) + hours} hours", f"{days + hours} hours", f"{(days * 10) + hours} hours", f"{(days * 60) + hours} hours", f"{total_hours * 60} hours", f"{total_hours * 2} hours", f"{total_hours + 24} hours", f"{(days * 24) * hours} hours"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"1 day = 24 hours. ({days} × 24) + {hours} = {days * 24} + {hours} = {total_hours} hours.")

    return generator

def generate_maps_questions():
    generator = TopicGenerator(
        topic_name="Maps and Plans",
        topic_prefix="ML_MAPS",
        subtopics=["Scale", "Distance", "Directions", "Speed"]
    )

    names = ["Kagiso", "Lebo", "Mandla", "Noxolo", "Tshepo", "Buhle"]
    places = ["Cape Town", "Johannesburg", "Durban", "Pretoria", "Polokwane", "Bloemfontein"]

    while not generator.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(generator.subtopics)
        name = random.choice(names)

        if subtopic == "Scale":
            if difficulty == "easy":
                map_dist = random.randint(2, 10)
                scale = random.choice([100, 200, 500])
                real_dist = map_dist * scale
                q = f"A map has a scale of 1:{scale}. If the distance on the map is {map_dist} cm, calculate the real-world distance in cm."
                ans_str = f"{real_dist} cm"
                wrong = [f"{map_dist + scale} cm", f"{scale / map_dist} cm", f"{real_dist / 100} cm", f"{real_dist * 10} cm", f"{real_dist / 10} cm", f"{map_dist * 100} cm", f"{scale} cm", f"{real_dist + 500} cm"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Real Distance = Map Distance × Scale Factor = {map_dist} × {scale} = {real_dist} cm.")
            elif difficulty == "medium":
                map_cm = random.randint(3, 15)
                scale_km = random.choice([50, 100, 200, 500]) # 1cm = 50km
                real_km = map_cm * scale_km
                q = f"On a map, 1 cm represents {scale_km} km. If two towns are {map_cm} cm apart on the map, what is the actual distance between them in km?"
                ans_str = f"{real_km} km"
                wrong = [f"{map_cm + scale_km} km", f"{scale_km / map_cm} km", f"{real_km * 10} km", f"{real_km / 10} km", f"{real_km * 1000} km", f"{real_km / 1000} km", f"{map_cm * 10} km", f"{real_km + 100} km"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Real Distance = Map Distance × Scale = {map_cm} × {scale_km} = {real_km} km.")
            else:
                real_km = random.randint(20, 100)
                map_cm = random.randint(2, 10)
                scale = (real_km * 100000) // map_cm # 1km = 100000cm
                q = f"The actual distance between two cities is {real_km} km. On a map, this distance is represented as {map_cm} cm. Calculate the map's scale in the form 1:..."
                ans_str = f"1:{scale}"
                wrong = [f"1:{real_km * 100}", f"1:{real_km * 1000}", f"1:{scale // 10}", f"1:{scale * 10}", f"1:{real_km // map_cm}", f"1:{(real_km * 1000) // map_cm}", f"1:{scale + 1000}", f"1:{scale // 100}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"{real_km} km = {real_km * 100000} cm. Scale = {map_cm}:{real_km * 100000} = 1:{scale}.")

        elif subtopic == "Distance":
            if difficulty == "easy":
                km1 = random.randint(10, 50)
                km2 = random.randint(20, 80)
                total = km1 + km2
                q = f"{name} drives {km1} km to work and {km2} km back home via a different route. What is the total distance traveled?"
                ans_str = f"{total} km"
                wrong = [f"{abs(km1 - km2)} km", f"{km1 * km2} km", f"{total * 2} km", f"{total * 1000} km", f"{km1} km", f"{km2} km", f"{total + 10} km", f"{total - 5} km"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total Distance = {km1} + {km2} = {total} km.")
            elif difficulty == "medium":
                total_dist = random.randint(300, 800)
                driven = random.randint(100, total_dist - 50)
                rem = total_dist - driven
                q = f"The distance from {random.choice(places)} to {random.choice(places)} is {total_dist} km. If {name} has already driven {driven} km, how far do they still need to travel?"
                ans_str = f"{rem} km"
                wrong = [f"{total_dist + driven} km", f"{driven - total_dist} km", f"{rem * 1000} km", f"{total_dist} km", f"{driven} km", f"{rem + 50} km", f"{rem - 20} km", f"{total_dist * driven} km"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Remaining = Total - Driven = {total_dist} - {driven} = {rem} km.")
            else:
                dist1 = random.randint(15, 45)
                dist2 = random.randint(25, 60)
                dist3 = random.randint(10, 30)
                total = dist1 + dist2 + dist3
                q = f"A delivery driver makes three stops. The distances between the stops are {dist1} km, {dist2} km, and {dist3} km. What is the total distance covered?"
                ans_str = f"{total} km"
                wrong = [f"{dist1 + dist2} km", f"{dist2 + dist3} km", f"{total * 2} km", f"{total + 10} km", f"{total - 10} km", f"{(dist1 * dist2) + dist3} km", f"{total * 1000} km", f"{total / 2} km"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total = {dist1} + {dist2} + {dist3} = {total} km.")

        elif subtopic == "Directions":
            if difficulty == "easy":
                dirs = ["North", "South", "East", "West"]
                d = random.choice(dirs)
                opp = {"North":"South", "South":"North", "East":"West", "West":"East"}[d]
                q = f"If you are facing {d} and you turn 180 degrees, which direction will you be facing?"
                ans_str = opp
                wrong = [d_ for d_ in dirs + ["North-East", "South-West", "North-West", "South-East"] if d_ != opp]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong[:8], f"180 degrees means facing the opposite direction. The opposite of {d} is {opp}.")
            elif difficulty == "medium":
                start_d = "North"
                turns = random.choice([("left", "West"), ("right", "East")])
                q = f"{name} is facing {start_d}. They make a 90-degree turn to the {turns[0]}. Which direction are they facing now?"
                ans_str = turns[1]
                wrong = ["North", "South", "East", "West", "North-East", "South-West", "North-West", "South-East"]
                wrong.remove(ans_str)
                generator.add_question(subtopic, difficulty, q, ans_str, wrong[:8], f"A 90-degree {turns[0]} turn from North points {turns[1]}.")
            else:
                q = f"If {name} travels North-East from point A to point B, what direction must they travel to return from point B directly back to point A?"
                ans_str = "South-West"
                wrong = ["North-East", "North-West", "South-East", "North", "South", "East", "West", "South-South-West"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"The opposite direction of North-East is South-West.")

        elif subtopic == "Speed":
            if difficulty == "easy":
                speed = random.choice([60, 80, 100, 120])
                time = random.randint(2, 5)
                dist = speed * time
                q = f"A car travels at a constant speed of {speed} km/h for {time} hours. Calculate the distance traveled."
                ans_str = f"{dist} km"
                wrong = [f"{speed + time} km", f"{speed / time} km", f"{time / speed} km", f"{dist * 2} km", f"{dist / 2} km", f"{speed * (time + 1)} km", f"{speed * (time - 1)} km", f"{dist + 10} km"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Distance = Speed × Time = {speed} × {time} = {dist} km.")
            elif difficulty == "medium":
                dist = random.choice([100, 200, 300, 400])
                time = random.randint(2, 5)
                speed = dist / time
                q = f"{name} travels {dist} km in {time} hours. Calculate their average speed in km/h."
                ans_str = f"{speed:.0f} km/h"
                wrong = [f"{dist * time} km/h", f"{dist + time} km/h", f"{time / dist} km/h", f"{speed * 2:.0f} km/h", f"{speed / 2:.0f} km/h", f"{dist / (time + 1):.0f} km/h", f"{dist / (time - 1):.0f} km/h" if time > 1 else f"{speed + 10:.0f} km/h", f"{speed - 10:.0f} km/h"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Speed = Distance ÷ Time = {dist} ÷ {time} = {speed:.0f} km/h.")
            else:
                dist = random.randint(150, 450)
                speed = random.choice([60, 80, 100])
                time = dist / speed
                h = int(time)
                m = int((time - h) * 60)
                ans_str = f"{h} hours and {m} minutes" if m > 0 else f"{h} hours"
                q = f"A taxi travels a distance of {dist} km at an average speed of {speed} km/h. Calculate the total time taken."
                wrong = [f"{dist * speed} hours", f"{dist + speed} hours", f"{speed / dist} hours", f"{h} hours and {m + 10} minutes", f"{h + 1} hours", f"{h} hours and {int(m/2)} minutes", f"{time:.2f} hours", f"{h * 60 + m} hours"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Time = Distance ÷ Speed = {dist} ÷ {speed} = {time:.2f} hours. 0.{(time-h)*100:.0f} hours × 60 = {m} minutes. Total = {ans_str}.")

    return generator

def generate_data_questions():
    generator = TopicGenerator(
        topic_name="Data Handling",
        topic_prefix="ML_DATA",
        subtopics=["Tables", "Graphs", "Statistics"]
    )

    names = ["Kagiso", "Lebo", "Mandla", "Noxolo", "Tshepo", "Buhle"]
    items = ["apples", "books", "pens", "shirts", "phones", "tickets"]

    while not generator.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(generator.subtopics)
        name = random.choice(names)
        item = random.choice(items)

        if subtopic == "Tables":
            if difficulty == "easy":
                col1 = random.randint(10, 30)
                col2 = random.randint(15, 40)
                col3 = random.randint(5, 20)
                total = col1 + col2 + col3
                q = f"A table shows the number of {item} sold over three days: Monday = {col1}, Tuesday = {col2}, Wednesday = {col3}. Calculate the total number sold."
                ans_str = str(total)
                wrong = [str(col1 + col2), str(col2 + col3), str(total * 2), str(col1 + col2 - col3), str(total + 10), str(total - 5), str(col1 * 3), str(col2 * 3)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total = {col1} + {col2} + {col3} = {total}.")
            elif difficulty == "medium":
                total = random.randint(100, 200)
                mon = random.randint(20, 50)
                tue = random.randint(30, 60)
                wed = total - (mon + tue)
                q = f"A shop sold a total of {total} {item} from Monday to Wednesday. The table shows {mon} sold on Monday and {tue} on Tuesday. How many were sold on Wednesday?"
                ans_str = str(wed)
                wrong = [str(mon + tue), str(total - mon), str(total - tue), str(wed + 10), str(wed - 10), str(abs(mon - tue)), str(total + wed), str(wed * 2)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Wednesday = Total - (Monday + Tuesday) = {total} - ({mon} + {tue}) = {wed}.")
            else:
                price = random.randint(15, 50)
                qty = random.randint(5, 20)
                discount = random.randint(5, 15)
                ans = (price * qty) - discount
                q = f"An invoice table shows {qty} {item} bought at R{price} each. A discount of R{discount} is applied to the total. Calculate the final amount due."
                ans_str = f"R{ans}"
                wrong = [f"R{price * qty}", f"R{(price * qty) + discount}", f"R{price * (qty - discount)}", f"R{(price - discount) * qty}", f"R{ans + 20}", f"R{ans - 10}", f"R{price + qty - discount}", f"R{price * qty * discount}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total before discount = {qty} × R{price} = R{price * qty}. Final Amount = R{price * qty} - R{discount} = R{ans}.")

        elif subtopic == "Graphs":
            if difficulty == "easy":
                val1 = random.randint(20, 50)
                val2 = random.randint(60, 100)
                diff = val2 - val1
                q = f"A bar graph shows {val1} {item} in Group A and {val2} {item} in Group B. How many more {item} are in Group B than Group A?"
                ans_str = str(diff)
                wrong = [str(val1 + val2), str(val2 * val1), str(val1), str(val2), str(diff + 10), str(diff - 5), str(val2 + 10), str(diff * 2)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Difference = Group B - Group A = {val2} - {val1} = {diff}.")
            elif difficulty == "medium":
                total = random.choice([100, 200, 300, 400])
                pct = random.choice([10, 20, 25, 30, 40, 50])
                ans = int(total * (pct / 100))
                q = f"A pie chart represents a total of {total} people. If the slice for '{item}' is {pct}%, how many people chose '{item}'?"
                ans_str = str(ans)
                wrong = [str(pct), str(total - ans), str(total + ans), str(int(total / (pct/100))), str(ans * 2), str(int(ans / 2)), str(ans + 10), str(ans - 10)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"{pct}% of {total} = ({pct} ÷ 100) × {total} = {ans}.")
            else:
                y1 = random.randint(10, 30)
                y2 = random.randint(50, 90)
                rate = (y2 - y1) / 2
                ans = y2 + int(rate)
                q = f"A line graph shows a steady increase. At Day 1 the value is {y1}, and at Day 3 the value is {y2}. Assuming the same constant rate of change, what will the value be at Day 4?"
                ans_str = str(ans)
                wrong = [str(y2 + (y2 - y1)), str(ans + 10), str(ans - 5), str(int(y2 * 1.5)), str(y2 + y1), str(int(y2 + (rate*2))), str(ans * 2), str(y2 + 5)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Rate of change = ({y2} - {y1}) ÷ (3 - 1) = {y2 - y1} ÷ 2 = {rate}. Day 4 value = Day 3 + Rate = {y2} + {rate} = {ans}.")

        elif subtopic == "Statistics":
            if difficulty == "easy":
                nums = [random.randint(5, 20) for _ in range(5)]
                ans = max(nums) - min(nums)
                q = f"Calculate the range of the following data set: {', '.join(map(str, nums))}."
                ans_str = str(ans)
                wrong = [str(max(nums)), str(min(nums)), str(sum(nums)), str(int(sum(nums)/5)), str(ans + 2), str(ans - 1), str(max(nums) + min(nums)), str(ans * 2)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Range = Maximum - Minimum = {max(nums)} - {min(nums)} = {ans}.")
            elif difficulty == "medium":
                nums = [random.randint(10, 50) for _ in range(4)]
                avg = sum(nums) / 4
                ans_str = f"{avg:.2f}" if not avg.is_integer() else f"{int(avg)}"
                q = f"Calculate the mean (average) of the following numbers: {', '.join(map(str, nums))}."
                wrong = [str(sum(nums)), str(max(nums) - min(nums)), str(sorted(nums)[1]), f"{avg + 5:.2f}", f"{avg - 5:.2f}", f"{(sum(nums)/3):.2f}", f"{(sum(nums)/5):.2f}", str(int(avg*2))]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Mean = Sum of values ÷ Number of values = {sum(nums)} ÷ 4 = {ans_str}.")
            else:
                nums = [random.randint(10, 40) for _ in range(5)]
                median = sorted(nums)[2]
                mean = sum(nums) / 5
                diff = abs(mean - median)
                ans_str = f"{diff:.1f}" if not diff.is_integer() else f"{int(diff)}"
                q = f"For the data set {', '.join(map(str, nums))}, calculate the positive difference between the mean and the median."
                wrong = [str(int(mean)), str(median), f"{mean + median:.1f}", f"{diff + 2:.1f}", f"{diff - 1:.1f}" if diff > 1 else f"{diff + 5:.1f}", str(max(nums) - min(nums)), f"{abs(mean - max(nums)):.1f}", f"{mean * median:.1f}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Ordered set: {', '.join(map(str, sorted(nums)))}. Median = {median}. Mean = {sum(nums)} ÷ 5 = {mean}. Difference = |{mean} - {median}| = {ans_str}.")

    return generator

def generate_probability_questions():
    generator = TopicGenerator(
        topic_name="Probability",
        topic_prefix="ML_PROB",
        subtopics=["Simple Events", "Relative Frequency", "Theoretical Probability"]
    )

    names = ["Kagiso", "Lebo", "Mandla", "Noxolo", "Tshepo", "Buhle"]
    colors = ["red", "blue", "green", "yellow", "black", "white"]

    while not generator.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(generator.subtopics)
        name = random.choice(names)

        if subtopic == "Simple Events":
            if difficulty == "easy":
                color1, color2 = random.sample(colors, 2)
                num1 = random.randint(2, 6)
                num2 = random.randint(2, 6)
                total = num1 + num2
                q = f"A bag contains {num1} {color1} balls and {num2} {color2} balls. What is the probability of randomly picking a {color1} ball? (Format as fraction)."
                ans_str = f"{num1}/{total}"
                wrong = [f"{num2}/{total}", f"{num1}/{num2}", f"{num2}/{num1}", f"1/{total}", f"{num1}/{total+1}", f"{num1-1}/{total}", f"{num1+1}/{total}", f"1/{num1}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Probability = Favorable outcomes ÷ Total outcomes = {num1} ÷ {total} = {ans_str}.")
            elif difficulty == "medium":
                target = random.choice([2, 3, 4, 5, 6])
                q = f"A standard fair 6-sided die is rolled. What is the probability of rolling a number greater than {target}?"
                ans = 6 - target
                ans_str = f"{ans}/6"
                wrong = [f"{target}/6", f"{ans-1}/6" if ans > 1 else f"{ans+2}/6", f"{ans+1}/6" if ans < 5 else f"{ans-2}/6", f"1/6", f"5/6", f"2/6", f"3/6", f"4/6"]
                wrong = [w for w in wrong if w != ans_str]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong[:8], f"Numbers greater than {target} are {', '.join([str(i) for i in range(target+1, 7)])}. There are {ans} such numbers. Probability = {ans_str}.")
            else:
                q = f"A card is drawn at random from a standard deck of 52 playing cards. What is the probability of drawing a face card (Jack, Queen, or King)? (Format as fraction)."
                ans_str = "12/52"
                wrong = ["3/52", "4/52", "1/52", "13/52", "16/52", "26/52", "10/52", "8/52"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"There are 3 face cards per suit, and 4 suits. Total face cards = 12. Probability = 12/52.")

        elif subtopic == "Relative Frequency":
            if difficulty == "easy":
                trials = random.choice([50, 100, 200])
                success = random.randint(10, trials // 2)
                q = f"{name} flips a coin {trials} times and gets 'Heads' {success} times. Calculate the relative frequency of getting 'Heads' as a decimal."
                ans_str = f"{success/trials:.2f}"
                wrong = [f"{trials/success:.2f}", f"{(trials-success)/trials:.2f}", f"{success/100:.2f}", f"0.50", f"{(success+10)/trials:.2f}", f"{(success-5)/trials:.2f}", f"{success/(trials*2):.2f}", f"{(trials-success)/100:.2f}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Relative Frequency = Successful trials ÷ Total trials = {success} ÷ {trials} = {ans_str}.")
            elif difficulty == "medium":
                total = random.randint(100, 300)
                faulty = random.randint(5, 15)
                q = f"In a batch of {total} lightbulbs, {faulty} are found to be faulty. What is the relative frequency of finding a working lightbulb? (Format as fraction)."
                ans_str = f"{total - faulty}/{total}"
                wrong = [f"{faulty}/{total}", f"{total - faulty}/{faulty}", f"{faulty}/{total - faulty}", f"1/{total}", f"{total - faulty + 1}/{total}", f"{total - faulty - 1}/{total}", f"{total}/{faulty}", f"{total - faulty}/100"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Working bulbs = {total} - {faulty} = {total - faulty}. Relative Frequency = {total - faulty}/{total}.")
            else:
                total_spins = random.choice([200, 400, 500])
                red_freq = random.randint(40, 80)
                blue_freq = random.randint(60, 100)
                green_freq = total_spins - red_freq - blue_freq
                q = f"A spinner landed on Red {red_freq} times, Blue {blue_freq} times, and Green {green_freq} times out of {total_spins} spins. What is the percentage relative frequency of landing on Green?"
                ans = (green_freq / total_spins) * 100
                ans_str = f"{ans:.1f}%" if not ans.is_integer() else f"{int(ans)}%"
                wrong = [f"{(red_freq/total_spins)*100:.1f}%", f"{(blue_freq/total_spins)*100:.1f}%", f"{green_freq}%", f"{total_spins}%", f"{ans + 5:.1f}%", f"{ans - 5:.1f}%", f"{(green_freq/100):.1f}%", f"{(total_spins/green_freq):.1f}%"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Green Frequency = {green_freq}. Relative Frequency = ({green_freq} ÷ {total_spins}) × 100 = {ans_str}.")

        elif subtopic == "Theoretical Probability":
            if difficulty == "easy":
                q = f"What is the theoretical probability of rolling an even number on a fair 6-sided die? (Format as percentage)."
                ans_str = "50%"
                wrong = ["33%", "16.7%", "66.7%", "25%", "60%", "100%", "5%", "40%"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Even numbers = 2, 4, 6 (3 outcomes). Total = 6. Probability = 3/6 = 1/2 = 50%.")
            elif difficulty == "medium":
                num_boys = random.randint(12, 18)
                num_girls = random.randint(14, 20)
                total = num_boys + num_girls
                q = f"A class has {num_boys} boys and {num_girls} girls. If a student is chosen at random, what is the theoretical probability that it is a girl? (Format as fraction)."
                ans_str = f"{num_girls}/{total}"
                wrong = [f"{num_boys}/{total}", f"{num_girls}/{num_boys}", f"{num_boys}/{num_girls}", f"1/{total}", f"{num_girls-1}/{total}", f"{num_girls+1}/{total}", f"{num_girls}/100", f"{num_boys}/100"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total students = {num_boys} + {num_girls} = {total}. Probability of girl = {num_girls}/{total}.")
            else:
                q = f"Two fair coins are flipped at the same time. What is the theoretical probability of getting exactly one Head and one Tail? (Format as fraction)."
                ans_str = "2/4"
                wrong = ["1/4", "3/4", "4/4", "1/2", "1/3", "2/3", "1/8", "2/8"]
                # remove 1/2 if ans is 2/4
                wrong = [w for w in wrong if w != "1/2" and w != "2/4"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong[:8], f"Possible outcomes: HH, HT, TH, TT. Outcomes with one Head and one Tail: HT, TH (2 outcomes). Probability = 2/4.")

    return generator

def generate_algebra_questions():
    generator = TopicGenerator(
        topic_name="Basic Algebra",
        topic_prefix="ML_ALG",
        subtopics=["Patterns", "Relationships", "Equations"]
    )

    names = ["Kagiso", "Lebo", "Mandla", "Noxolo", "Tshepo", "Buhle"]
    items = ["books", "chairs", "tickets", "boxes"]

    while not generator.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(generator.subtopics)
        name = random.choice(names)
        item = random.choice(items)

        if subtopic == "Patterns":
            if difficulty == "easy":
                start = random.randint(2, 10)
                diff = random.randint(2, 5)
                seq = [start, start+diff, start+(2*diff)]
                ans = start + (3*diff)
                q = f"Consider the number pattern: {seq[0]}, {seq[1]}, {seq[2]}, ... What is the next number in the pattern?"
                ans_str = str(ans)
                wrong = [str(ans + diff), str(ans - diff), str(seq[-1] * diff), str(ans + 1), str(ans - 1), str(seq[-1] + diff + 1), str(start + (4*diff)), str(seq[0] * 3)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"The pattern increases by {diff} each time. Next number = {seq[-1]} + {diff} = {ans}.")
            elif difficulty == "medium":
                start = random.randint(5, 20)
                diff = random.randint(3, 8)
                n = random.randint(8, 15)
                ans = start + (n - 1) * diff
                q = f"A pattern follows the rule: Term = {diff} × n + {start - diff}. Calculate the value of term number {n}."
                ans_str = str(ans)
                wrong = [str(start + n * diff), str(diff * n), str(start + diff), str(ans + diff), str(ans - diff), str(n + diff + start), str(n * start), str(ans + 10)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Substitute n = {n} into the rule: Term = {diff}({n}) + {start - diff} = {diff * n} + {start - diff} = {ans}.")
            else:
                start = random.randint(10, 50)
                diff = random.randint(4, 12)
                target = start + (random.randint(15, 30) - 1) * diff
                # find n: target = diff*n + (start-diff)  => diff*n = target - start + diff => n = (target - start + diff)/diff
                n = (target - start + diff) // diff
                q = f"The general rule for a number pattern is Term = {diff}n + {start - diff}. Which term number has a value of {target}?"
                ans_str = str(n)
                diff_safe = start - diff if start - diff != 0 else 1
                wrong = [str(n + 1), str(n - 1), str(n * 2), str(int(target/diff)), str(int(target/diff_safe)), str(n + diff), str(n + 5), str(int(n/2))]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Set {diff}n + {start - diff} = {target}. Then {diff}n = {target - (start - diff)}. n = {target - (start - diff)} ÷ {diff} = {n}.")

        elif subtopic == "Relationships":
            if difficulty == "easy":
                rate = random.randint(15, 40)
                qty = random.randint(3, 8)
                ans = rate * qty
                q = f"If 1 {item[:-1]} costs R{rate}, how much will {qty} {item} cost?"
                ans_str = f"R{ans}"
                wrong = [f"R{rate + qty}", f"R{ans + rate}", f"R{ans - rate}", f"R{rate * (qty + 1)}", f"R{rate * (qty - 1)}", f"R{qty}", f"R{ans * 2}", f"R{ans / 2}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Cost = Rate × Quantity = R{rate} × {qty} = R{ans}.")
            elif difficulty == "medium":
                fixed = random.randint(100, 300)
                rate = random.randint(20, 50)
                hours = random.randint(4, 10)
                ans = fixed + (rate * hours)
                q = f"A plumber charges a fixed call-out fee of R{fixed} and R{rate} per hour of work. How much will it cost if the plumber works for {hours} hours?"
                ans_str = f"R{ans}"
                wrong = [f"R{fixed * hours}", f"R{rate * hours}", f"R{(fixed + rate) * hours}", f"R{ans + rate}", f"R{ans - rate}", f"R{fixed + hours}", f"R{ans + fixed}", f"R{ans * 2}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Cost = Call-out fee + (Rate × Hours) = {fixed} + ({rate} × {hours}) = {fixed} + {rate * hours} = R{ans}.")
            else:
                rate = random.randint(150, 400)
                time = random.choice([2.5, 3.5, 4.5])
                ans = rate * time
                q = f"{name} earns R{rate} per day. If they work for {time} days, calculate their total pay."
                ans_str = f"R{int(ans)}" if ans.is_integer() else f"R{ans:.2f}"
                wrong = [f"R{int(rate * int(time))}", f"R{int(rate * math.ceil(time))}", f"R{int(ans + rate)}", f"R{int(ans - rate/2)}", f"R{int(rate + time)}", f"R{int(rate / time)}", f"R{int(ans * 2)}", f"R{int(ans + 100)}"]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Total Pay = Rate × Time = {rate} × {time} = R{ans}.")

        elif subtopic == "Equations":
            if difficulty == "easy":
                x = random.randint(5, 20)
                add = random.randint(2, 10)
                total = x + add
                q = f"Solve for x: x + {add} = {total}"
                ans_str = str(x)
                wrong = [str(total + add), str(x * 2), str(total), str(add), str(x + 1), str(x - 1), str(total * add), str(int(total/add))]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Subtract {add} from both sides: x = {total} - {add} = {x}.")
            elif difficulty == "medium":
                x = random.randint(4, 15)
                mult = random.randint(2, 6)
                add = random.randint(5, 20)
                total = (mult * x) + add
                q = f"Solve for y: {mult}y + {add} = {total}"
                ans_str = str(x)
                wrong = [str(x + 1), str(x - 1), str(total - add), str(int((total + add)/mult)), str(total), str(mult * total), str(int(total/mult)), str(x * 2)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"{mult}y = {total} - {add} = {total - add}. y = {total - add} ÷ {mult} = {x}.")
            else:
                x = random.randint(5, 20)
                c1 = random.randint(2, 5)
                c2 = random.randint(6, 12)
                # Equation: C1(x + C2) = Total
                total = c1 * (x + c2)
                q = f"Solve for p: {c1}(p + {c2}) = {total}"
                ans_str = str(x)
                wrong = [str(x + c2), str(int(total/c1)), str(int((total - c2)/c1)), str(x + 1), str(x - 1), str(total - c1 - c2), str(int((total + c1*c2)/c1)), str(x * 2)]
                generator.add_question(subtopic, difficulty, q, ans_str, wrong, f"Divide by {c1}: p + {c2} = {total//c1}. Subtract {c2}: p = {total//c1} - {c2} = {x}.")

    return generator

if __name__ == "__main__":
    os.makedirs("dataset/grade10", exist_ok=True)

    print("Generating Finance...")
    fin_gen = generate_finance_questions()
    fin_gen.save_to_json("dataset/grade10/mathlit_finance.json")

    print("Generating Measurement...")
    meas_gen = generate_measurement_questions()
    meas_gen.save_to_json("dataset/grade10/mathlit_measurement.json")

    print("Generating Maps and Plans...")
    maps_gen = generate_maps_questions()
    maps_gen.save_to_json("dataset/grade10/mathlit_maps_plans.json")

    print("Generating Data Handling...")
    data_gen = generate_data_questions()
    data_gen.save_to_json("dataset/grade10/mathlit_data_handling.json")

    print("Generating Probability...")
    prob_gen = generate_probability_questions()
    prob_gen.save_to_json("dataset/grade10/mathlit_probability.json")

    print("Generating Basic Algebra...")
    alg_gen = generate_algebra_questions()
    alg_gen.save_to_json("dataset/grade10/mathlit_algebra.json")

    print("Done!")
