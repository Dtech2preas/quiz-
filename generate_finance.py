import random
import math
import sympy as sp
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats, get_wrong_exprs

def generate_sequences():
    # ... we'll reuse the one from generate_sequences.py
    pass

def generate_finance():
    gen = TopicGenerator("Finance, Growth and Decay", "FIN", ["compound interest", "depreciation", "exponential growth"])

    attempts = 0
    while not gen.is_done() and attempts < 10000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        if subtopic == "compound interest":
            P = random.randint(100, 10000) * 10
            i = random.randint(2, 15)
            n = random.randint(2, 20)

            if difficulty == "easy":
                A = P * (1 + i/100)**n
                q = f"Calculate the final amount if R${P}$ is invested at ${i}\\%$ p.a. compound interest for ${n}$ years."
                A_str = f"{A:.2f}"
                exp = f"$A = P(1+i)^n = {P}(1 + {i/100})^{n} = {A_str}$"
                gen.add_question(subtopic, difficulty, q, A_str, get_wrong_floats(A, decimals=2), exp)

            elif difficulty == "medium":
                # Find n
                A = int(P * (1 + i/100)**n)
                q = f"An investment of R${P}$ grows to R${A}$ at an interest rate of ${i}\\%$ p.a. compounded annually. Find the number of years $n$."
                exp = f"$A = P(1+i)^n \\implies {A} = {P}(1 + {i/100})^n \\implies ({1 + i/100})^n = {A/P:.4f} \\implies n = \\log_{{{1 + i/100}}}({A/P:.4f}) \\approx {n}$"
                gen.add_question(subtopic, difficulty, q, str(n), get_wrong_ints(n), exp)

            elif difficulty == "hard":
                # Find P or i with different compounding periods
                k = random.choice([2, 4, 12]) # semi-annually, quarterly, monthly
                period_name = {2: "semi-annually", 4: "quarterly", 12: "monthly"}[k]
                A = P * (1 + i/(100*k))**(n*k)
                A_round = round(A, 2)
                q = f"An amount grows to R${A_round:.2f}$ after ${n}$ years at an interest rate of ${i}\\%$ p.a. compounded {period_name}. Calculate the original principal amount $P$."
                exp = f"$A = P(1+\\frac{{i}}{{k}})^{{nk}} \\implies {A_round:.2f} = P(1 + \\frac{{{i/100}}}{{{k}}})^{{{n*k}}} \\implies P = \\frac{{{A_round:.2f}}}{{(1 + {i/(100*k):.4f})^{{{n*k}}}}} \\approx {P}$"
                gen.add_question(subtopic, difficulty, q, str(P), get_wrong_ints(P), exp)

        elif subtopic == "depreciation":
            P = random.randint(50, 500) * 1000
            i = random.randint(5, 20)
            n = random.randint(2, 10)

            if difficulty == "easy":
                # Straight line
                A = P * (1 - n*i/100)
                if A < 0: A = 0
                A_round = round(A, 2)
                q = f"A car valued at R${P}$ depreciates on a straight-line basis at ${i}\\%$ p.a. What is its book value after ${n}$ years?"
                exp = f"$A = P(1 - in) = {P}(1 - ({i/100})({n})) = {A_round:.2f}$"
                gen.add_question(subtopic, difficulty, q, f"{A_round:.2f}", get_wrong_floats(A_round, decimals=2), exp)

            elif difficulty == "medium":
                # Reducing balance
                A = P * (1 - i/100)**n
                A_round = round(A, 2)
                q = f"Equipment bought for R${P}$ depreciates on a reducing-balance basis at ${i}\\%$ p.a. Find its value after ${n}$ years."
                exp = f"$A = P(1 - i)^n = {P}(1 - {i/100})^{n} \\approx {A_round:.2f}$"
                gen.add_question(subtopic, difficulty, q, f"{A_round:.2f}", get_wrong_floats(A_round, decimals=2), exp)

            elif difficulty == "hard":
                # Find n or i on reducing balance
                A = P * (1 - i/100)**n
                A_round = int(A)
                q = f"A machine bought for R${P}$ has a book value of R${A_round}$ after ${n}$ years on the reducing-balance method. Calculate the annual rate of depreciation $r$ (as a percentage)."
                i_calc = (1 - (A_round/P)**(1/n)) * 100
                i_round = round(i_calc, 2)
                exp = f"$A = P(1 - i)^n \\implies {A_round} = {P}(1 - i)^{n} \\implies 1 - i = \\sqrt[{n}]{{\\frac{{{A_round}}}{{{P}}}}} \\implies i \\approx {i_round}\\%$"
                gen.add_question(subtopic, difficulty, q, f"{i_round:.2f}", get_wrong_floats(i_round, decimals=2), exp)

        elif subtopic == "exponential growth":
            P = random.randint(1000, 50000)
            i = random.randint(1, 8)
            n = random.randint(5, 50)

            if difficulty == "easy":
                A = P * math.exp(i/100 * n)
                A_round = int(A)
                q = f"A population of ${P}$ bacteria grows exponentially at a continuous rate of ${i}\\%$ per hour. Estimate the population after ${n}$ hours."
                exp = f"$A = Pe^{{rt}} = {P}e^{{({i/100})({n})}} \\approx {A_round}$"
                gen.add_question(subtopic, difficulty, q, str(A_round), get_wrong_ints(A_round), exp)

            elif difficulty == "medium":
                A = P * (1 + i/100)**n
                A_round = int(A)
                q = f"The population of a town is currently ${P}$ and grows at ${i}\\%$ per year. What will the population be in ${n}$ years?"
                exp = f"$A = P(1+i)^n = {P}(1 + {i/100})^{n} \\approx {A_round}$"
                gen.add_question(subtopic, difficulty, q, str(A_round), get_wrong_ints(A_round), exp)

            elif difficulty == "hard":
                # Time to double
                q = f"A population grows continuously at a rate of ${i}\\%$ per year. How many years will it take for the population to double? (Round to 2 decimal places)."
                n_calc = math.log(2) / (i/100)
                n_round = round(n_calc, 2)
                exp = f"$2P = Pe^{{{i/100}t}} \\implies e^{{{i/100}t}} = 2 \\implies {i/100}t = \\ln(2) \\implies t = \\frac{{\\ln(2)}}{{{i/100}}} \\approx {n_round}$"
                gen.add_question(subtopic, difficulty, q, f"{n_round:.2f}", get_wrong_floats(n_round, decimals=2), exp)

    return gen

if __name__ == "__main__":
    gen = generate_finance()
    gen.save_to_json("paper1_finance.json")
    print(f"Generated {len(gen.questions)} finance questions.")
