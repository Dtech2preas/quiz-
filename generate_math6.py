import json
import random
import math
import os
from typing import List
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

# We will need to define a generator class similar to Math10Generator
class Math6Generator(TopicGenerator):
    def __init__(self, topic_name: str, topic_prefix: str, subtopics: List[str]):
        super().__init__(topic_name, topic_prefix, subtopics)

    def add_question(self, subtopic: str, difficulty: str, question: str, correct_answer: str, wrong_answers: List[str], explanation: str):
        if self.difficulty_counts[difficulty] >= self.difficulty_targets[difficulty]:
            return False

        if question in self.generated_questions:
            return False

        correct_str = str(correct_answer)
        wrong_answers = [str(w) for w in wrong_answers if str(w) != correct_str]

        unique_wrong_answers = []
        seen = set()
        for w in wrong_answers:
            if w not in seen:
                seen.add(w)
                unique_wrong_answers.append(w)

        if len(unique_wrong_answers) < 6:
            # try to fill to 6 if it's not enough
            while len(unique_wrong_answers) < 6:
                if correct_str.isdigit():
                    new_val = int(correct_str) + random.randint(-100, 100)
                    if new_val != int(correct_str) and str(new_val) not in unique_wrong_answers:
                        unique_wrong_answers.append(str(new_val))
                else:
                    break

            if len(unique_wrong_answers) < 6:
                return False

        self.generated_questions.add(question)

        question_id = f"{self.topic_prefix}_{len(self.questions) + 1:03d}"

        q_dict = {
            "id": question_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": correct_str,
            "wrong_answers_pool": unique_wrong_answers[:8],
            "explanation": explanation
        }
        self.questions.append(q_dict)
        self.difficulty_counts[difficulty] += 1
        return True


def generate_numbers_operations() -> Math6Generator:
    subtopics = [
        "Place value",
        "Addition and Subtraction",
        "Multiplication",
        "Division",
        "Properties of numbers"
    ]
    gen = Math6Generator("Numbers, Operations and Relationships", "G6_MATH_NUM", subtopics)

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

        if subtopic == "Place value":
            if difficulty == "easy":
                # Value of a digit
                number = random.randint(10000, 999999)
                num_str = f"{number:,}".replace(",", " ")
                num_str_nospace = str(number)
                idx = random.randint(0, len(num_str_nospace)-1)
                digit = int(num_str_nospace[idx])
                place = len(num_str_nospace) - idx - 1
                if digit == 0:
                    continue
                ans_val = digit * (10**place)
                q = f"What is the value of the digit {digit} in {num_str}?"
                ans = f"{ans_val:,}".replace(",", " ")
                places = ["units", "tens", "hundreds", "thousands", "ten-thousands", "hundred-thousands"]
                exp = f"The digit {digit} is in the {places[place]} place, so its value is {ans}."
                wrongs = []
                for w_place in range(6):
                    w_ans = digit * (10**w_place)
                    w_str = f"{w_ans:,}".replace(",", " ")
                    if w_str != ans:
                        wrongs.append(w_str)
                wrongs.append(str(digit))
                wrongs.append(f"{digit} 000 000")
                wrongs.append(f"{digit} 0")
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Expanded notation
                number = random.randint(100000, 999999)
                num_str = f"{number:,}".replace(",", " ")
                q = f"Write {num_str} in expanded form."
                parts = []
                for i, d in enumerate(str(number)):
                    if d != '0':
                        parts.append(str(int(d) * (10**(5-i))))
                ans = " + ".join(parts)
                exp = f"Each digit is multiplied by its place value: {ans}."
                wrongs = []
                for _ in range(6):
                    w_parts = parts.copy()
                    idx_w = random.randint(0, len(w_parts)-1)
                    if "0" in w_parts[idx_w]:
                        w_parts[idx_w] = w_parts[idx_w][:-1]
                    else:
                        w_parts[idx_w] = w_parts[idx_w] + "0"
                    wrongs.append(" + ".join(w_parts))
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Ordering numbers
                nums = [random.randint(100000, 999999) for _ in range(4)]
                q = f"Arrange these numbers in descending order: {', '.join([f'{n:,}'.replace(',', ' ') for n in nums])}."
                nums_sorted = sorted(nums, reverse=True)
                ans = ", ".join([f"{n:,}".replace(",", " ") for n in nums_sorted])
                exp = "Compare the numbers starting from the largest place value (hundred thousands) to find the largest."
                wrongs = [
                    ", ".join([f"{n:,}".replace(",", " ") for n in sorted(nums)]), # ascending
                    ", ".join([f"{n:,}".replace(",", " ") for n in [nums_sorted[0], nums_sorted[2], nums_sorted[1], nums_sorted[3]]]),
                    ", ".join([f"{n:,}".replace(",", " ") for n in [nums_sorted[1], nums_sorted[0], nums_sorted[2], nums_sorted[3]]]),
                    ", ".join([f"{n:,}".replace(",", " ") for n in [nums_sorted[3], nums_sorted[2], nums_sorted[1], nums_sorted[0]]]),
                    ", ".join([f"{n:,}".replace(",", " ") for n in [nums_sorted[0], nums_sorted[1], nums_sorted[3], nums_sorted[2]]]),
                    ", ".join([f"{n:,}".replace(",", " ") for n in [nums_sorted[2], nums_sorted[3], nums_sorted[0], nums_sorted[1]]])
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Addition and Subtraction":
            if difficulty == "easy":
                a = random.randint(1000, 9999)
                b = random.randint(1000, 9999)
                op = random.choice(["+", "-"])
                if op == "-":
                    if a < b:
                        a, b = b, a
                    ans_val = a - b
                    q = f"Calculate: {a} - {b}"
                    exp = f"Subtract {b} from {a} to get {ans_val}."
                else:
                    ans_val = a + b
                    q = f"Calculate: {a} + {b}"
                    exp = f"Add {a} and {b} to get {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                a = random.randint(10000, 99999)
                b = random.randint(10000, 99999)
                op = random.choice(["+", "-"])
                if op == "-":
                    if a < b:
                        a, b = b, a
                    ans_val = a - b
                    q = f"Calculate: {a} - {b}"
                    exp = f"Subtract {b} from {a} to get {ans_val}."
                else:
                    ans_val = a + b
                    q = f"Calculate: {a} + {b}"
                    exp = f"Add {a} and {b} to get {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                a = random.randint(10000, 99999)
                b = random.randint(10000, 99999)
                c = random.randint(10000, 99999)
                ans_val = a + b - c
                q = f"Calculate: {a} + {b} - {c}"
                exp = f"First add {a} and {b} to get {a+b}, then subtract {c} to get {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Multiplication":
            if difficulty == "easy":
                a = random.randint(10, 99)
                b = random.randint(2, 9)
                ans_val = a * b
                q = f"Calculate: {a} × {b}"
                exp = f"Multiply {a} by {b} to get {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                a = random.randint(100, 999)
                b = random.randint(10, 99)
                ans_val = a * b
                q = f"Calculate: {a} × {b}"
                exp = f"Multiply {a} by {b} to get {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                a = random.randint(1000, 9999)
                b = random.randint(10, 99)
                ans_val = a * b
                q = f"A factory produces {a} items every day. How many items will it produce in {b} days?"
                exp = f"Multiply the daily production ({a}) by the number of days ({b}): {a} × {b} = {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Division":
            if difficulty == "easy":
                b = random.randint(2, 9)
                ans_val = random.randint(10, 99)
                a = ans_val * b
                q = f"Calculate: {a} ÷ {b}"
                exp = f"Divide {a} by {b} to get {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                b = random.randint(10, 99)
                ans_val = random.randint(10, 99)
                a = ans_val * b
                q = f"Calculate: {a} ÷ {b}"
                exp = f"Divide {a} by {b} to get {ans_val}."
                ans = str(ans_val)
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                b = random.randint(10, 50)
                ans_val = random.randint(100, 999)
                rem = random.randint(1, b-1)
                a = ans_val * b + rem
                q = f"Calculate: {a} ÷ {b}. What is the quotient and remainder?"
                ans = f"{ans_val} remainder {rem}"
                exp = f"{b} goes into {a} {ans_val} times. {ans_val} × {b} = {ans_val*b}. The remainder is {a} - {ans_val*b} = {rem}."
                wrongs = [
                    f"{ans_val} remainder {rem+1}",
                    f"{ans_val+1} remainder {rem}",
                    f"{ans_val} remainder {rem-1}" if rem > 1 else f"{ans_val} remainder 2",
                    f"{ans_val-1} remainder {rem}",
                    f"{rem} remainder {ans_val}",
                    f"{ans_val} remainder 0"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Properties of numbers":
            if difficulty == "easy":
                num = random.randint(2, 50)
                q = f"Which of the following is a multiple of {num}?"
                ans_val = num * random.randint(2, 10)
                ans = str(ans_val)
                exp = f"{ans_val} is a multiple of {num} because {num} × {ans_val//num} = {ans_val}."
                wrongs = [str(ans_val + random.randint(1, num-1)) for _ in range(6)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                num = random.choice([12, 18, 20, 24, 30, 36, 40, 48, 50])
                factors = [i for i in range(1, num + 1) if num % i == 0]
                q = f"Which of the following lists all the factors of {num}?"
                ans = ", ".join(map(str, factors))
                exp = f"The factors of {num} are the numbers that divide exactly into {num}: {ans}."
                wrongs = [
                    ", ".join(map(str, factors[1:])), # Missing 1
                    ", ".join(map(str, factors[:-1])), # Missing num
                    ", ".join(map(str, factors)) + f", {num*2}", # Extra
                    ", ".join(map(str, factors[1:-1])), # Missing 1 and num
                    ", ".join(map(str, [f for f in factors if f%2==0])), # Only evens
                    ", ".join(map(str, factors)) + f", {factors[-1]+1}"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                a = random.choice([2, 3, 5])
                b = random.choice([7, 11, 13])
                num = a * b * a
                q = f"What is the prime factorisation of {num}?"
                if a == 2 and b == 7:
                    ans = "2 × 2 × 7"
                elif a == 3 and b == 7:
                    ans = "3 × 3 × 7"
                else:
                    ans = f"{a} × {a} × {b}"

                exp = f"{num} can be written as a product of its prime factors: {ans}."
                wrongs = [
                    f"{a*a} × {b}",
                    f"{a} × {a*b}",
                    f"{a*2} × {b}",
                    f"{a} × {b} × {b}",
                    f"{a+1} × {a-1} × {b}",
                    f"{a} × {b}"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen


def generate_fractions_decimals_percentages() -> Math6Generator:
    subtopics = [
        "Common Fractions",
        "Decimal Fractions",
        "Percentages"
    ]
    gen = Math6Generator("Fractions, Decimals and Percentages", "G6_MATH_FDP", subtopics)

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

        if subtopic == "Common Fractions":
            if difficulty == "easy":
                # Equivalent fractions
                num = random.randint(1, 9)
                den = random.randint(num+1, 10)
                factor = random.randint(2, 5)
                ans_num = num * factor
                ans_den = den * factor
                q = f"Which fraction is equivalent to {num}/{den}?"
                ans = f"{ans_num}/{ans_den}"
                exp = f"Multiply the numerator and denominator by {factor}: {num}×{factor} = {ans_num} and {den}×{factor} = {ans_den}."
                wrongs = [
                    f"{ans_num+1}/{ans_den}",
                    f"{ans_num}/{ans_den+1}",
                    f"{ans_den}/{ans_num}",
                    f"{num+1}/{den+factor}",
                    f"{num*factor}/{den+factor}",
                    f"{num+factor}/{den*factor}"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Addition with same denominator
                den = random.randint(3, 12)
                num1 = random.randint(1, den-1)
                num2 = random.randint(1, den-1)
                ans_num = num1 + num2
                q = f"Calculate: {num1}/{den} + {num2}/{den}"
                if ans_num > den:
                    whole = ans_num // den
                    rem = ans_num % den
                    if rem == 0:
                        ans = str(whole)
                    else:
                        ans = f"{whole} {rem}/{den}"
                else:
                    ans = f"{ans_num}/{den}"
                exp = f"Add the numerators: {num1} + {num2} = {ans_num}. The result is {ans}."
                wrongs = [
                    f"{ans_num}/{den+den}",
                    f"{num1+1}/{den}",
                    f"{num2+1}/{den}",
                    f"{num1}/{den}",
                    f"{ans_num+1}/{den}",
                    f"{ans_num-1}/{den}" if ans_num > 1 else f"{ans_num+2}/{den}"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Addition with different denominators
                den1 = random.choice([2, 3, 4, 5])
                den2 = den1 * random.randint(2, 3)
                num1 = random.randint(1, den1-1)
                num2 = random.randint(1, den2-1)
                factor = den2 // den1
                ans_num = num1 * factor + num2
                q = f"Calculate: {num1}/{den1} + {num2}/{den2}"
                if ans_num > den2:
                    whole = ans_num // den2
                    rem = ans_num % den2
                    if rem == 0:
                        ans = str(whole)
                    else:
                        ans = f"{whole} {rem}/{den2}"
                else:
                    ans = f"{ans_num}/{den2}"
                exp = f"First find a common denominator ({den2}). {num1}/{den1} = {num1*factor}/{den2}. Then add: {num1*factor} + {num2} = {ans_num}."
                wrongs = [
                    f"{num1+num2}/{den1+den2}",
                    f"{num1+num2}/{den2}",
                    f"{num1*num2}/{den1*den2}",
                    f"{ans_num+1}/{den2}",
                    f"{ans_num-1}/{den2}" if ans_num > 1 else f"{ans_num+2}/{den2}",
                    f"{num1*factor + num2 + 1}/{den2}"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Decimal Fractions":
            if difficulty == "easy":
                # Place value
                num = round(random.uniform(0.1, 9.99), 2)
                q = f"What is the place value of the digit {str(num).split('.')[1][0]} in {num:.2f}?"
                ans = "tenths"
                exp = f"The first digit after the decimal point represents tenths."
                wrongs = ["hundredths", "units", "tens", "thousandths", "ones", "hundreds"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Addition
                a = round(random.uniform(1.0, 9.99), 2)
                b = round(random.uniform(1.0, 9.99), 2)
                ans_val = a + b
                q = f"Calculate: {a:.2f} + {b:.2f}"
                ans = f"{ans_val:.2f}"
                exp = f"Align the decimal points and add to get {ans}."
                wrongs = get_wrong_floats(ans_val, count=6, decimals=2)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Subtraction with borrowing
                a = round(random.uniform(10.0, 20.0), 2)
                b = round(random.uniform(1.0, 9.99), 2)
                ans_val = a - b
                q = f"Calculate: {a:.2f} - {b:.2f}"
                ans = f"{ans_val:.2f}"
                exp = f"Align the decimal points and subtract to get {ans}."
                wrongs = get_wrong_floats(ans_val, count=6, decimals=2)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Percentages":
            if difficulty == "easy":
                # Percentage of 100
                perc = random.randint(1, 99)
                q = f"Write {perc}% as a fraction in its simplest form."
                gcd = math.gcd(perc, 100)
                ans = f"{perc//gcd}/{100//gcd}"
                exp = f"Percentage means 'out of 100'. {perc}% = {perc}/100. Simplify to get {ans}."
                wrongs = [
                    f"{perc}/10",
                    f"{perc+1}/100",
                    f"{perc}/1000",
                    f"{perc-1}/100",
                    f"{100//gcd}/{perc//gcd}" if perc > 0 else "0",
                    f"{perc}/50"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Percentage of an amount
                perc = random.choice([10, 20, 25, 50, 75])
                amount = random.randint(1, 10) * 100
                ans_val = (perc * amount) // 100
                q = f"Calculate {perc}% of R{amount}"
                ans = f"R{ans_val}"
                exp = f"{perc}% is {perc}/100. Multiply by {amount}: ({perc}/100) × {amount} = {ans_val}."
                wrongs = [f"R{w}" for w in get_wrong_ints(ans_val, count=6)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Convert fraction to percentage
                num = random.choice([1, 3, 7, 9, 11, 13, 17, 19])
                den = 20
                perc = (num * 100) // den
                q = f"Write {num}/{den} as a percentage."
                ans = f"{perc}%"
                exp = f"Multiply the fraction by 100 to convert to a percentage: ({num}/{den}) × 100 = {perc}%."
                wrongs = [f"{perc+5}%", f"{perc-5}%", f"{num}%", f"{den}%", f"{perc*2}%", f"{perc//2}%"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen


def generate_patterns_algebra() -> Math6Generator:
    subtopics = [
        "Numeric patterns",
        "Geometric patterns",
        "Number sentences"
    ]
    gen = Math6Generator("Patterns, Functions and Algebra", "G6_MATH_PFA", subtopics)

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

        if subtopic == "Numeric patterns":
            if difficulty == "easy":
                # Find the next term (constant difference)
                start = random.randint(1, 50)
                diff = random.choice([2, 3, 4, 5, 10, 20])
                seq = [start + i*diff for i in range(4)]
                ans_val = seq[-1] + diff
                q = f"What is the next number in the pattern: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ...?"
                ans = str(ans_val)
                exp = f"The pattern increases by {diff} each time. {seq[3]} + {diff} = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Find the rule
                start = random.randint(1, 20)
                diff = random.choice([3, 4, 6, 7, 8, 9])
                seq = [start + i*diff for i in range(3)]
                q = f"What is the constant difference in the pattern: {seq[0]}, {seq[1]}, {seq[2]}, ...?"
                ans = str(diff)
                exp = f"Subtract consecutive terms: {seq[1]} - {seq[0]} = {diff}."
                wrongs = get_wrong_ints(diff)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Find the missing term (multiplication)
                start = random.randint(2, 5)
                factor = random.choice([2, 3])
                seq = [start * (factor**i) for i in range(4)]
                missing_idx = random.choice([1, 2])
                ans_val = seq[missing_idx]
                q_seq = seq.copy()
                q_seq[missing_idx] = "__"
                q = f"Find the missing number in the pattern: {q_seq[0]}, {q_seq[1]}, {q_seq[2]}, {q_seq[3]}."
                ans = str(ans_val)
                exp = f"The pattern multiplies by {factor} each time. {seq[missing_idx-1]} × {factor} = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Geometric patterns":
            if difficulty == "easy":
                # Matchsticks pattern
                n1 = random.randint(3, 6) # e.g. a triangle is 3, square is 4
                diff = n1 - 1 # typical connected pattern difference
                q = f"A pattern of shapes is made with matchsticks. Shape 1 needs {n1} matches. Each new shape needs {diff} more matches. How many matches for Shape 2?"
                ans_val = n1 + diff
                ans = str(ans_val)
                exp = f"Add the difference to the first term: {n1} + {diff} = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                n1 = random.randint(3, 6)
                diff = n1 - 1
                term = random.randint(4, 6)
                ans_val = n1 + diff * (term - 1)
                q = f"A pattern uses {n1} sticks for figure 1, {n1+diff} for figure 2, and {n1+diff*2} for figure 3. How many sticks for figure {term}?"
                ans = str(ans_val)
                exp = f"The rule is to add {diff} each time. Figure {term} is {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                n1 = random.randint(3, 6)
                diff = n1 - 1
                term = random.randint(10, 20)
                ans_val = n1 + diff * (term - 1)
                q = f"A pattern follows the rule: number of sticks = {diff} × figure number + 1. How many sticks are in figure {term}?"
                ans = str(ans_val)
                exp = f"Substitute {term} into the rule: {diff} × {term} + 1 = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Number sentences":
            if difficulty == "easy":
                a = random.randint(10, 50)
                b = random.randint(10, 50)
                ans_val = a + b
                q = f"Find the value of the square (□) to make the sentence true: □ = {a} + {b}"
                ans = str(ans_val)
                exp = f"Add the numbers together: {a} + {b} = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                ans_val = random.randint(10, 50)
                a = random.randint(10, 50)
                b = ans_val + a
                q = f"Find the value of the square (□): □ + {a} = {b}"
                ans = str(ans_val)
                exp = f"Subtract {a} from both sides: □ = {b} - {a} = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                ans_val = random.randint(2, 12)
                a = random.choice([2, 3, 4, 5])
                b = ans_val * a
                q = f"Find the value of the square (□): {a} × □ = {b}"
                ans = str(ans_val)
                exp = f"Divide both sides by {a}: □ = {b} ÷ {a} = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen


def generate_geometry() -> Math6Generator:
    subtopics = [
        "Properties of 2D shapes",
        "Properties of 3D objects",
        "Symmetry",
        "Transformations"
    ]
    gen = Math6Generator("Space and Shape (Geometry)", "G6_MATH_GEO", subtopics)

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

        if subtopic == "Properties of 2D shapes":
            if difficulty == "easy":
                # Polygon angles
                n = random.randint(3, 12)
                poly_names = {3:"triangle", 4:"quadrilateral", 5:"pentagon", 6:"hexagon", 7:"heptagon", 8:"octagon", 9:"nonagon", 10:"decagon", 11:"hendecagon", 12:"dodecagon"}
                name = poly_names[n]
                side_len = random.randint(2, 20)
                q = f"If a regular {name} has a side length of {side_len} cm, what is its perimeter?"
                ans_val = n * side_len
                ans = str(ans_val)
                exp = f"A {name} has {n} sides. Perimeter = {n} × {side_len} = {ans_val} cm."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Find missing angle in triangle
                a = random.randint(20, 100)
                b = random.randint(20, 150 - a)
                c = 180 - a - b
                q = f"Two angles of a triangle are {a}° and {b}°. What is the size of the third angle?"
                ans = str(c)
                exp = f"The angles of a triangle add up to 180°. {180} - ({a} + {b}) = {c}°."
                wrongs = get_wrong_ints(c)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Find missing angle in quadrilateral
                a = random.randint(40, 130)
                b = random.randint(40, 130)
                c = random.randint(40, 130)
                while a+b+c >= 350:
                    c = random.randint(40, 130)
                d = 360 - (a + b + c)
                q = f"Three angles of a quadrilateral are {a}°, {b}°, and {c}°. What is the size of the fourth angle?"
                ans = str(d)
                exp = f"The angles of a quadrilateral add up to 360°. {360} - ({a} + {b} + {c}) = {d}°."
                wrongs = get_wrong_ints(d)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Properties of 3D objects":
            if difficulty == "easy":
                # Prism properties parametrised
                n = random.randint(3, 12)
                base_names = {3:"triangular", 4:"rectangular", 5:"pentagonal", 6:"hexagonal", 7:"heptagonal", 8:"octagonal", 9:"nonagonal", 10:"decagonal", 11:"hendecagonal", 12:"dodecagonal"}
                name = base_names[n]
                prop = random.choice(["faces", "edges", "vertices"])
                if prop == "faces":
                    ans_val = n + 2
                elif prop == "edges":
                    ans_val = n * 3
                else: # vertices
                    ans_val = n * 2
                q = f"How many {prop} does a {name} prism have?"
                ans = str(ans_val)
                exp = f"A prism with an {n}-sided base has {ans_val} {prop}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Pyramid properties parametrised
                n = random.randint(3, 12)
                base_names = {3:"triangular", 4:"square", 5:"pentagonal", 6:"hexagonal", 7:"heptagonal", 8:"octagonal", 9:"nonagonal", 10:"decagonal", 11:"hendecagonal", 12:"dodecagonal"}
                name = base_names[n]
                prop = random.choice(["faces", "edges", "vertices"])
                if prop == "faces":
                    ans_val = n + 1
                elif prop == "edges":
                    ans_val = n * 2
                else: # vertices
                    ans_val = n + 1
                q = f"How many {prop} does a {name}-based pyramid have?"
                ans = str(ans_val)
                exp = f"A pyramid with an {n}-sided base has {ans_val} {prop}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Euler's formula
                v = random.randint(4, 20)
                f = random.randint(4, 20)
                e = v + f - 2
                q = f"A certain 3D object has {v} vertices and {f} faces. According to Euler's formula (V + F - E = 2), how many edges does it have?"
                ans = str(e)
                exp = f"Substitute the values into the formula: {v} + {f} - E = 2. {v+f} - E = 2, so E = {e}."
                wrongs = get_wrong_ints(e)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Symmetry":
            if difficulty == "easy":
                # Regular polygon symmetry
                n = random.randint(3, 20)
                poly_names = {3:"triangle", 4:"quadrilateral", 5:"pentagon", 6:"hexagon", 7:"heptagon", 8:"octagon", 9:"nonagon", 10:"decagon", 11:"hendecagon", 12:"dodecagon"}
                if n in poly_names:
                    name = poly_names[n]
                else:
                    name = f"{n}-gon"

                if n == 4:
                    name = "square"
                elif n == 3:
                    name = "equilateral triangle"
                elif n > 4:
                    name = f"regular {name}"

                q = f"How many lines of symmetry does a {name} have?"
                ans = str(n)
                exp = f"A regular polygon with {n} sides has {n} lines of symmetry."
                wrongs = get_wrong_ints(n)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Rotational symmetry
                n = random.randint(3, 12)
                poly_names = {3:"equilateral triangle", 4:"square", 5:"regular pentagon", 6:"regular hexagon", 8:"regular octagon", 10:"regular decagon", 12:"regular dodecagon"}
                if n not in poly_names:
                    n = random.choice(list(poly_names.keys()))
                name = poly_names[n]
                ans_val = 360 // n
                q = f"What is the angle of rotational symmetry for a {name}?"
                ans = f"{ans_val}°"
                exp = f"A {name} has order of rotational symmetry {n}. Angle = 360° ÷ {n} = {ans_val}°."
                wrongs = [f"{w}°" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Coordinate symmetry
                x = random.randint(1, 10)
                y = random.randint(1, 10)
                axis = random.choice(["x-axis", "y-axis"])
                if axis == "x-axis":
                    ans_x = x
                    ans_y = -y
                else:
                    ans_x = -x
                    ans_y = y
                q = f"If the point ({x}, {y}) is reflected across the {axis}, what are the coordinates of the new point?"
                ans = f"({ans_x}, {ans_y})"
                exp = f"Reflecting across the {axis} changes the sign of the {'y' if axis=='x-axis' else 'x'}-coordinate."
                wrongs = [
                    f"({-x}, {-y})",
                    f"({y}, {x})",
                    f"({-y}, {-x})",
                    f"({x}, {y})",
                    f"({ans_y}, {ans_x})",
                    f"({-ans_x}, {-ans_y})"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Transformations":
            if difficulty == "easy":
                # Translation of a point
                x = random.randint(1, 10)
                y = random.randint(1, 10)
                dx = random.randint(1, 5) * random.choice([1, -1])
                dy = random.randint(1, 5) * random.choice([1, -1])
                ans_x = x + dx
                ans_y = y + dy
                dx_str = f"{abs(dx)} units {'right' if dx > 0 else 'left'}"
                dy_str = f"{abs(dy)} units {'up' if dy > 0 else 'down'}"
                q = f"Point A is at ({x}, {y}). It is translated {dx_str} and {dy_str}. What are the new coordinates?"
                ans = f"({ans_x}, {ans_y})"
                exp = f"Add {dx} to the x-coordinate and {dy} to the y-coordinate: ({x}+{dx}, {y}+{dy}) = {ans}."
                wrongs = [
                    f"({x-dx}, {y-dy})",
                    f"({ans_y}, {ans_x})",
                    f"({x+dy}, {y+dx})",
                    f"({x-dy}, {y-dx})",
                    f"({ans_x+1}, {ans_y})",
                    f"({ans_x}, {ans_y-1})"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Enlargement scale factor
                side = random.randint(2, 10)
                sf = random.randint(2, 5)
                new_side = side * sf
                q = f"A shape with a side length of {side} cm is enlarged by a scale factor of {sf}. What is the new side length?"
                ans = str(new_side)
                exp = f"Multiply the side length by the scale factor: {side} × {sf} = {new_side} cm."
                wrongs = get_wrong_ints(new_side)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Rotation of a point
                x = random.randint(1, 10) * random.choice([1, -1])
                y = random.randint(1, 10) * random.choice([1, -1])
                angle = random.choice(["90° clockwise", "90° anti-clockwise", "180°"])
                if angle == "180°":
                    ans_x = -x
                    ans_y = -y
                elif angle == "90° clockwise":
                    ans_x = y
                    ans_y = -x
                else: # 90° anti-clockwise
                    ans_x = -y
                    ans_y = x
                q = f"Rotate the point ({x}, {y}) about the origin (0,0) by {angle}. What are the new coordinates?"
                ans = f"({ans_x}, {ans_y})"
                exp = f"Following the rules for rotation by {angle} around the origin, the new point is {ans}."
                wrongs = [
                    f"({-x}, {y})",
                    f"({x}, {-y})",
                    f"({y}, {x})",
                    f"({-y}, {-x})",
                    f"({x}, {y})",
                    f"({ans_y}, {ans_x})"
                ]
                # filter duplicates
                unique_wrongs = list(set([w for w in wrongs if w != ans]))
                while len(unique_wrongs) < 6:
                    unique_wrongs.append(f"({ans_x + random.randint(1,3)}, {ans_y - random.randint(1,3)})")
                gen.add_question(subtopic, difficulty, q, ans, unique_wrongs, exp)

    return gen


def generate_measurement() -> Math6Generator:
    subtopics = [
        "Length",
        "Mass",
        "Capacity and Volume",
        "Time",
        "Area and Perimeter"
    ]
    gen = Math6Generator("Measurement", "G6_MATH_MEA", subtopics)

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

        if subtopic == "Length":
            if difficulty == "easy":
                # Convert mm to cm
                val = random.randint(10, 500) * 10
                q = f"Convert {val} mm to cm."
                ans_val = val // 10
                ans = f"{ans_val} cm"
                exp = f"Divide by 10 because there are 10 mm in 1 cm: {val} ÷ 10 = {ans_val} cm."
                wrongs = [f"{w} cm" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Convert m to km
                val = random.randint(1, 50) * 100
                q = f"Convert {val} m to km."
                ans_val = val / 1000
                ans = f"{ans_val:g} km"
                exp = f"Divide by 1000 because there are 1000 m in 1 km: {val} ÷ 1000 = {ans_val:g} km."
                wrongs = [f"{w} km" for w in get_wrong_floats(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Word problem
                len1 = round(random.uniform(1.0, 5.0), 1)
                len2 = round(random.uniform(50, 200), 1)
                q = f"A ribbon is {len1} m long. If I cut off {len2} cm, how much ribbon is left? Give the answer in cm."
                ans_val = int(len1 * 100 - len2)
                ans = f"{ans_val} cm"
                exp = f"Convert {len1} m to cm: {len1} × 100 = {int(len1*100)} cm. Subtract the cut piece: {int(len1*100)} - {len2} = {ans_val} cm."
                wrongs = [f"{w} cm" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Mass":
            if difficulty == "easy":
                # Convert g to kg
                val = random.randint(1, 10) * 1000
                q = f"Convert {val} g to kg."
                ans_val = val // 1000
                ans = f"{ans_val} kg"
                exp = f"Divide by 1000 because there are 1000 g in 1 kg: {val} ÷ 1000 = {ans_val} kg."
                wrongs = [f"{w} kg" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Convert kg to g
                val = round(random.uniform(0.5, 5.5), 1)
                q = f"Convert {val} kg to g."
                ans_val = int(val * 1000)
                ans = f"{ans_val} g"
                exp = f"Multiply by 1000 because there are 1000 g in 1 kg: {val} × 1000 = {ans_val} g."
                wrongs = [f"{w} g" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Word problem
                bags = random.randint(3, 8)
                mass = random.randint(250, 750)
                q = f"If {bags} identical bags of flour have a total mass of {bags * mass} g, what is the mass of one bag?"
                ans_val = mass
                ans = f"{ans_val} g"
                exp = f"Divide the total mass by the number of bags: {bags * mass} ÷ {bags} = {ans_val} g."
                wrongs = [f"{w} g" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Capacity and Volume":
            if difficulty == "easy":
                # Convert ml to l
                val = random.randint(1, 10) * 1000
                q = f"Convert {val} ml to liters (l)."
                ans_val = val // 1000
                ans = f"{ans_val} l"
                exp = f"Divide by 1000 because there are 1000 ml in 1 l: {val} ÷ 1000 = {ans_val} l."
                wrongs = [f"{w} l" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Convert l to ml
                val = round(random.uniform(0.5, 5.5), 1)
                q = f"Convert {val} l to ml."
                ans_val = int(val * 1000)
                ans = f"{ans_val} ml"
                exp = f"Multiply by 1000 because there are 1000 ml in 1 l: {val} × 1000 = {ans_val} ml."
                wrongs = [f"{w} ml" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Word problem
                jugs = random.randint(3, 8)
                cap = random.randint(200, 500)
                q = f"A large container holds {jugs} jugs of water. If each jug holds {cap} ml, what is the total capacity of the container in liters (l)?"
                ans_val = (jugs * cap) / 1000
                ans = f"{ans_val:g} l"
                exp = f"Multiply the capacity of one jug by the number of jugs: {cap} × {jugs} = {jugs * cap} ml. Then divide by 1000 to convert to liters: {jugs * cap} ÷ 1000 = {ans_val:g} l."
                wrongs = [f"{w} l" for w in get_wrong_floats(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Time":
            if difficulty == "easy":
                # Convert hours to minutes
                val = random.randint(2, 6)
                q = f"Convert {val} hours to minutes."
                ans_val = val * 60
                ans = f"{ans_val} minutes"
                exp = f"Multiply by 60 because there are 60 minutes in 1 hour: {val} × 60 = {ans_val} minutes."
                wrongs = [f"{w} minutes" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Convert days to hours
                val = random.randint(2, 6)
                q = f"Convert {val} days to hours."
                ans_val = val * 24
                ans = f"{ans_val} hours"
                exp = f"Multiply by 24 because there are 24 hours in 1 day: {val} × 24 = {ans_val} hours."
                wrongs = [f"{w} hours" for w in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Time duration
                h1 = random.randint(8, 10)
                m1 = random.randint(10, 40)
                h2 = random.randint(11, 14)
                m2 = random.randint(10, 40)
                dur_h = h2 - h1
                dur_m = m2 - m1
                if dur_m < 0:
                    dur_h -= 1
                    dur_m += 60
                q = f"A bus departs at {h1:02d}:{m1:02d} and arrives at {h2:02d}:{m2:02d}. How long was the journey?"
                ans = f"{dur_h} hours {dur_m} minutes"
                exp = f"Calculate the difference in hours and minutes from {h1:02d}:{m1:02d} to {h2:02d}:{m2:02d}."
                wrongs = [
                    f"{dur_h} hours {dur_m+5} minutes",
                    f"{dur_h} hours {dur_m-5} minutes",
                    f"{dur_h+1} hours {dur_m} minutes",
                    f"{dur_h-1} hours {dur_m} minutes",
                    f"{dur_h} hours {dur_m+10} minutes",
                    f"{dur_h} hours {dur_m-10} minutes",
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Area and Perimeter":
            if difficulty == "easy":
                # Perimeter of rectangle
                l = random.randint(5, 15)
                w = random.randint(2, l-1)
                q = f"A rectangle has a length of {l} cm and a width of {w} cm. What is its perimeter?"
                ans_val = 2 * (l + w)
                ans = f"{ans_val} cm"
                exp = f"Perimeter = 2 × (Length + Width) = 2 × ({l} + {w}) = 2 × {l+w} = {ans_val} cm."
                wrongs = [f"{w_val} cm" for w_val in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Area of rectangle
                l = random.randint(5, 15)
                w = random.randint(2, l-1)
                q = f"A rectangle has a length of {l} cm and a width of {w} cm. What is its area?"
                ans_val = l * w
                ans = f"{ans_val} cm²"
                exp = f"Area = Length × Width = {l} × {w} = {ans_val} cm²."
                wrongs = [f"{w_val} cm²" for w_val in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Missing side given perimeter
                l = random.randint(5, 15)
                w = random.randint(2, l-1)
                p = 2 * (l + w)
                q = f"The perimeter of a rectangle is {p} cm. If its length is {l} cm, what is its width?"
                ans_val = w
                ans = f"{ans_val} cm"
                exp = f"Perimeter = 2 × (Length + Width). {p} = 2 × ({l} + Width). {p} ÷ 2 = {l} + Width. {p//2} - {l} = {ans_val} cm."
                wrongs = [f"{w_val} cm" for w_val in get_wrong_ints(ans_val)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen


def generate_data_probability() -> Math6Generator:
    subtopics = [
        "Collecting and organising data",
        "Representing data",
        "Interpreting and analysing data",
        "Probability"
    ]
    gen = Math6Generator("Data Handling and Probability", "G6_MATH_DHP", subtopics)

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

        if subtopic == "Collecting and organising data":
            if difficulty == "easy":
                # Tally marks
                count = random.randint(11, 29)
                groups = count // 5
                rem = count % 5
                q = f"In a tally chart, there are {groups} full groups of five and {rem} single marks. What is the total frequency?"
                ans = str(count)
                exp = f"Each group represents 5. So, {groups} × 5 = {groups*5}. Plus {rem} single marks = {count}."
                wrongs = get_wrong_ints(count)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Missing total
                freqs = [random.randint(5, 20) for _ in range(4)]
                missing = random.randint(5, 20)
                total = sum(freqs) + missing
                q = f"A survey asked {total} people for their favourite colour. Red was chosen by {freqs[0]}, Blue by {freqs[1]}, Green by {freqs[2]}, and Yellow by {freqs[3]}. How many chose Pink, the only other option?"
                ans = str(missing)
                exp = f"Subtract the known frequencies from the total: {total} - ({freqs[0]} + {freqs[1]} + {freqs[2]} + {freqs[3]}) = {missing}."
                wrongs = get_wrong_ints(missing)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Two-way table / organizing
                boys_total = random.randint(20, 30)
                girls_total = random.randint(20, 30)
                boys_soccer = random.randint(10, boys_total-5)
                girls_soccer = random.randint(5, girls_total-5)
                boys_rugby = boys_total - boys_soccer
                girls_rugby = girls_total - girls_soccer
                q = f"In a class of {boys_total+girls_total} students, there are {boys_total} boys. {boys_soccer} boys and {girls_soccer} girls play soccer, the rest play rugby. How many girls play rugby?"
                ans = str(girls_rugby)
                exp = f"Total girls = {girls_total}. Girls playing rugby = Total girls - Girls playing soccer = {girls_total} - {girls_soccer} = {girls_rugby}."
                wrongs = get_wrong_ints(girls_rugby)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Representing data":
            if difficulty == "easy":
                # Bar graph interpretation
                scale = random.choice([2, 5, 10, 20])
                bars = random.randint(4, 10)
                val = bars * scale
                q = f"On a bar graph, the vertical axis goes up in steps of {scale}. A bar is exactly {bars} steps high. What value does it represent?"
                ans = str(val)
                exp = f"Multiply the number of steps by the scale: {bars} × {scale} = {val}."
                wrongs = get_wrong_ints(val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Pictograph
                symbol_val = random.choice([5, 10, 20, 50])
                symbols = random.randint(2, 6)
                half = random.choice([True, False])
                val = symbols * symbol_val
                if half:
                    val += symbol_val // 2
                q = f"In a pictograph, one symbol represents {symbol_val} cars. A row has {symbols} full symbols"
                if half:
                    q += " and one half symbol. "
                else:
                    q += ". "
                q += "How many cars does this row represent?"
                ans = str(val)
                exp = f"{symbols} full symbols × {symbol_val} = {symbols * symbol_val}."
                if half:
                    exp += f" Half a symbol = {symbol_val // 2}. Total = {val}."
                wrongs = get_wrong_ints(val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Pie chart degrees/percentages
                perc = random.choice([10, 20, 25, 30, 40, 50])
                total = random.randint(10, 50) * 10
                ans_val = (perc * total) // 100
                q = f"A pie chart shows the favourite sports of {total} students. If the slice for tennis is {perc}%, how many students chose tennis?"
                ans = str(ans_val)
                exp = f"{perc}% of {total} = ({perc}/100) × {total} = {ans_val}."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Interpreting and analysing data":
            if difficulty == "easy":
                # Mode
                data = [random.randint(1, 10) for _ in range(5)]
                mode = random.randint(1, 10)
                data.extend([mode, mode])
                random.shuffle(data)
                q = f"What is the mode of this data set: {', '.join(map(str, data))}?"
                ans = str(mode)
                exp = f"The mode is the number that appears most often, which is {mode}."
                wrongs = get_wrong_ints(mode)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Median
                data = [random.randint(10, 50) for _ in range(5)]
                data.sort()
                median = data[2]
                random.shuffle(data)
                q = f"Find the median of this data set: {', '.join(map(str, data))}."
                ans = str(median)
                exp = f"First, order the data from smallest to largest: {', '.join(map(str, sorted(data)))}. The middle number is {median}."
                wrongs = get_wrong_ints(median)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Mean
                mean = random.randint(10, 40)
                data = [random.randint(mean-5, mean+5) for _ in range(4)]
                last_val = mean * 5 - sum(data)
                data.append(last_val)
                random.shuffle(data)
                q = f"Calculate the mean (average) of these numbers: {', '.join(map(str, data))}."
                ans = str(mean)
                exp = f"Add all the numbers: sum = {sum(data)}. Divide by the number of values (5): {sum(data)} ÷ 5 = {mean}."
                wrongs = get_wrong_ints(mean)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Probability":
            if difficulty == "easy":
                # Probability terms
                events = [
                    ("The sun will rise tomorrow.", "certain"),
                    ("You will roll a 7 on a standard 6-sided die.", "impossible"),
                    ("If you flip a coin, it will land on heads.", "even chance"),
                    ("A fish will walk on land tomorrow.", "impossible"),
                    ("Tomorrow will be a Tuesday if today is Monday.", "certain")
                ]
                event = random.choice(events)
                q = f"What is the likelihood of the following event? '{event[0]}'"
                ans = event[1]
                exp = f"This event is {event[1]} to happen."
                wrongs = [w for w in ["certain", "impossible", "even chance", "likely", "unlikely"] if w != ans]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Simple probability as fraction
                colors = ["red", "blue", "green", "yellow"]
                chosen = random.choice(colors)
                counts = {c: random.randint(2, 6) for c in colors}
                total = sum(counts.values())
                q = f"A bag contains {counts['red']} red, {counts['blue']} blue, {counts['green']} green, and {counts['yellow']} yellow marbles. What is the probability of randomly picking a {chosen} marble?"
                ans = f"{counts[chosen]}/{total}"
                exp = f"There are {counts[chosen]} {chosen} marbles out of a total of {total}. Probability = {counts[chosen]}/{total}."
                wrongs = [f"{c}/{total}" for c in counts.values() if f"{c}/{total}" != ans]
                wrongs.append(f"{total}/{counts[chosen]}")
                wrongs.append(f"1/{total}")
                wrongs.append(f"1/{counts[chosen]}")
                wrongs.append(f"0/{total}")
                wrongs.append(f"{counts[chosen]+1}/{total}")
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Coin flips / Dice
                q = "If you roll a standard 6-sided die, what is the probability of rolling a prime number? Give the answer as a fraction in simplest form."
                ans = "1/2"
                exp = "The prime numbers on a die are 2, 3, and 5. There are 3 prime numbers out of 6 possible outcomes. 3/6 simplifies to 1/2."
                wrongs = ["1/6", "1/3", "2/3", "5/6", "3/6", "1/4"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen


if __name__ == "__main__":
    random.seed(42)

    print("Generating Numbers, Operations and Relationships...")
    gen_num = generate_numbers_operations()
    gen_num.save_to_json("dataset/grade6/mathematics/grade6_math_numbers_operations.json")

    print("Generating Fractions, Decimals and Percentages...")
    gen_frac = generate_fractions_decimals_percentages()
    gen_frac.save_to_json("dataset/grade6/mathematics/grade6_math_fractions_decimals_percentages.json")

    print("Generating Patterns, Functions and Algebra...")
    gen_pat = generate_patterns_algebra()
    gen_pat.save_to_json("dataset/grade6/mathematics/grade6_math_patterns_algebra.json")

    print("Generating Geometry...")
    gen_geo = generate_geometry()
    gen_geo.save_to_json("dataset/grade6/mathematics/grade6_math_geometry.json")

    print("Generating Measurement...")
    gen_mea = generate_measurement()
    gen_mea.save_to_json("dataset/grade6/mathematics/grade6_math_measurement.json")

    print("Generating Data Handling and Probability...")
    gen_dhp = generate_data_probability()
    gen_dhp.save_to_json("dataset/grade6/mathematics/grade6_math_data_probability.json")

    print("All Grade 6 Mathematics datasets generated successfully.")
