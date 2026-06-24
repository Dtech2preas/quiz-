import random
import math
from fractions import Fraction
from generators_common import TopicGenerator

def generate_probability():
    gen = TopicGenerator("Probability", "PROB", ["basic probability", "independent events", "dependent events", "tree diagrams"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        if subtopic == "basic probability":
            if difficulty == "easy":
                total = random.choice([20, 30, 40, 50, 60, 100])
                count = random.randint(5, total - 5)
                color = random.choice(["red", "blue", "green", "black"])
                q = f"A bag contains ${total}$ marbles. ${count}$ of them are {color}. If a marble is drawn at random, what is the probability that it is {color}?"
                prob = Fraction(count, total)
                correct = f"{prob.numerator}/{prob.denominator}" if prob.denominator != 1 else "1"
                # get some wrong fractions
                wrongs = set()
                while len(wrongs) < 8:
                    w_num = random.randint(1, total)
                    w_den = total
                    w_frac = Fraction(w_num, w_den)
                    w_str = f"{w_frac.numerator}/{w_frac.denominator}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Probability = $\\frac{{\\text{{favorable}}}}{{\\text{{total}}}} = \\frac{{{count}}}{{{total}}} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "medium":
                p_A = round(random.uniform(0.1, 0.4), 2)
                p_B = round(random.uniform(0.2, 0.5), 2)
                p_A_or_B = round(p_A + p_B - random.uniform(0.01, min(p_A, p_B)-0.01), 2)
                q = f"Given $P(A) = {p_A}$, $P(B) = {p_B}$, and $P(A \\cup B) = {p_A_or_B}$. Calculate $P(A \\cap B)$."
                ans = round(p_A + p_B - p_A_or_B, 2)
                correct = f"{ans:.2f}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0.01, 0.99), 2)
                    w_str = f"{w:.2f}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"$P(A \\cup B) = P(A) + P(B) - P(A \\cap B) \\implies {p_A_or_B} = {p_A} + {p_B} - P(A \\cap B) \\implies P(A \\cap B) = {ans:.2f}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # mutually exclusive
                p_A = round(random.uniform(0.1, 0.4), 2)
                p_B = round(random.uniform(0.1, 0.5), 2)
                q = f"Events A and B are mutually exclusive. $P(A) = {p_A}$ and $P(B) = {p_B}$. Find $P(A' \\cap B')$, where $A'$ is the complement of A."
                ans = round(1 - (p_A + p_B), 2)
                correct = f"{ans:.2f}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0.01, 0.99), 2)
                    w_str = f"{w:.2f}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Since mutually exclusive, $P(A \\cup B) = {p_A} + {p_B} = {p_A + p_B}$. $P(A' \\cap B') = 1 - P(A \\cup B) = 1 - {p_A + p_B} = {ans:.2f}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

        elif subtopic == "independent events":
            if difficulty == "easy":
                p_A = round(random.uniform(0.2, 0.8), 2)
                p_B = round(random.uniform(0.2, 0.8), 2)
                ans = round(p_A * p_B, 4)
                q = f"A and B are independent events. $P(A) = {p_A}$ and $P(B) = {p_B}$. Find $P(A \\cap B)$."
                correct = f"{ans:.4f}" if not str(ans).endswith('0') else str(ans)
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0.01, 0.99), 4)
                    w_str = f"{w:.4f}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"For independent events, $P(A \\cap B) = P(A) \\cdot P(B) = {p_A} \\times {p_B} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "medium":
                p_A = round(random.uniform(0.2, 0.6), 2)
                p_B = round(random.uniform(0.2, 0.6), 2)
                # find P(A U B)
                ans = round(p_A + p_B - p_A*p_B, 4)
                q = f"A and B are independent events. $P(A) = {p_A}$ and $P(B) = {p_B}$. Find $P(A \\cup B)$."
                correct = f"{ans:.4f}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0.01, 0.99), 4)
                    w_str = f"{w:.4f}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Independent means $P(A \\cap B) = {p_A} \\times {p_B} = {p_A*p_B:.4f}$. $P(A \\cup B) = P(A) + P(B) - P(A \\cap B) = {p_A} + {p_B} - {p_A*p_B:.4f} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # find P(B) given P(A) and P(A U B) for independent events
                p_A = round(random.uniform(0.1, 0.5), 2)
                p_B = round(random.uniform(0.1, 0.5), 2)
                p_A_or_B = round(p_A + p_B - p_A*p_B, 4)
                q = f"A and B are independent events with $P(A) = {p_A}$ and $P(A \\cup B) = {p_A_or_B}$. Find $P(B)$."
                correct = f"{p_B:.2f}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0.01, 0.99), 2)
                    w_str = f"{w:.2f}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"$P(A \\cup B) = P(A) + P(B) - P(A)P(B) \\implies {p_A_or_B} = {p_A} + P(B)(1 - {p_A}) \\implies P(B) = \\frac{{{p_A_or_B} - {p_A}}}{{{round(1-p_A, 2)}}} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

        elif subtopic == "dependent events" or subtopic == "tree diagrams":
            if difficulty == "easy":
                r = random.randint(3, 8)
                b = random.randint(3, 8)
                total = r + b
                q = f"A bag contains ${r}$ red and ${b}$ blue balls. Two balls are drawn WITHOUT replacement. Find the probability that both are red."
                ans_frac = Fraction(r, total) * Fraction(r-1, total-1)
                correct = f"{ans_frac.numerator}/{ans_frac.denominator}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = Fraction(random.randint(1, total*total), total*(total-1))
                    w_str = f"{w.numerator}/{w.denominator}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"P(Both red) = $\\frac{{{r}}}{{{total}}} \\times \\frac{{{r-1}}}{{{total-1}}} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "medium":
                r = random.randint(3, 6)
                b = random.randint(3, 6)
                total = r + b
                q = f"A bag contains ${r}$ red and ${b}$ blue balls. Two balls are drawn WITHOUT replacement. What is the probability of drawing one red and one blue ball in any order?"
                ans_frac = Fraction(r, total) * Fraction(b, total-1) * 2
                correct = f"{ans_frac.numerator}/{ans_frac.denominator}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = Fraction(random.randint(1, total*total), total*(total-1))
                    w_str = f"{w.numerator}/{w.denominator}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"P(RB or BR) = $P(RB) + P(BR) = \\left(\\frac{{{r}}}{{{total}}} \\times \\frac{{{b}}}{{{total-1}}}\\right) + \\left(\\frac{{{b}}}{{{total}}} \\times \\frac{{{r}}}{{{total-1}}}\\right) = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                p_rain = round(random.uniform(0.2, 0.4), 2)
                p_late_if_rain = round(random.uniform(0.6, 0.9), 2)
                p_late_if_not_rain = round(random.uniform(0.1, 0.3), 2)
                p_no_rain = round(1 - p_rain, 2)
                ans = round(p_rain * p_late_if_rain + p_no_rain * p_late_if_not_rain, 4)
                q = f"The probability that it rains is ${p_rain}$. If it rains, the probability a bus is late is ${p_late_if_rain}$. If it does not rain, the probability it is late is ${p_late_if_not_rain}$. Find the total probability that the bus is late."
                correct = f"{ans:.4f}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(0.01, 0.99), 4)
                    w_str = f"{w:.4f}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"P(Late) = P(Rain $\\cap$ Late) + P(No Rain $\\cap$ Late) = $({p_rain} \\times {p_late_if_rain}) + ({p_no_rain} \\times {p_late_if_not_rain}) = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

    return gen

if __name__ == "__main__":
    gen = generate_probability()
    gen.save_to_json("paper1_probability.json")
    print(f"Generated {len(gen.questions)} probability questions.")
