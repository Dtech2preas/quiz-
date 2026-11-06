import json
import random
import os
import time
import math
from fractions import Fraction

def generate_math_probability():
    print("Generating Grade 12 Mathematics: Probability & Counting Principles...")
    t0 = time.time()

    questions = []
    seen_texts = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive="Knowledge"):
        nonlocal questions, seen_texts
        q_text = q_text.strip()
        if q_text in seen_texts:
            return False
        correct = str(correct).strip()
        clean_wrongs = []
        for w in wrongs:
            w = str(w).strip()
            if w != correct and w not in clean_wrongs:
                clean_wrongs.append(w)
        if len(clean_wrongs) < 6:
            return False

        seen_texts.add(q_text)
        q_id = f"MATH_P1_PROB_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Probability",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Probability",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_ints(val, count=8):
        w = set()
        for mult in [2, 3, 4, 5]:
            if val % mult == 0 and val // mult != val and val // mult > 0:
                w.add(str(val // mult))
            w.add(str(val * mult))
        for delta in [-1, 1, -2, 2, -10, 10, -5, 5, -20, 20]:
            if val + delta > 0 and val + delta != val:
                w.add(str(val + delta))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = int(val * random.uniform(0.3, 3.0)) + random.randint(1, 25)
            if extra != val and str(extra) not in cand_list and extra > 0:
                cand_list.append(str(extra))
        return cand_list[:count]

    def get_w_probs(val, count=8):
        w = set()
        for delta in [-0.1, 0.1, -0.05, 0.05, -0.15, 0.15, 0.2, -0.2, 0.08, -0.08]:
            cand = round(val + delta, 2)
            if 0.01 <= cand <= 0.99 and cand != val:
                w.add(f"{cand:.2f}")
        if val != 0.5:
            w.add(f"{round(1 - val, 2):.2f}")
        cand_list = list(w)
        while len(cand_list) < count:
            cand = round(random.uniform(0.02, 0.98), 2)
            s_cand = f"{cand:.2f}"
            if s_cand != f"{val:.2f}" and s_cand not in cand_list:
                cand_list.append(s_cand)
        return cand_list[:count]

    def get_w_fracs(frac, count=8):
        w = set()
        num, den = frac.numerator, frac.denominator
        if num < den:
            w.add(f"{den-num}/{den}")
        if num > 1:
            w.add(f"{num-1}/{den}")
        w.add(f"{num+1}/{den}")
        w.add(f"{num}/{den+1}")
        if den > 2:
            w.add(f"{num}/{den-1}")
        cand_list = list(w)
        while len(cand_list) < count:
            d2 = random.randint(den // 2 if den > 4 else 2, den * 2 + 5)
            n2 = random.randint(1, d2 - 1)
            f2 = Fraction(n2, d2)
            s = f"{f2.numerator}/{f2.denominator}"
            if s != f"{frac.numerator}/{frac.denominator}" and s not in cand_list:
                cand_list.append(s)
        return cand_list[:count]

    # ====================================================
    # EASY QUESTIONS (Target: 300)
    # ====================================================
    easy_count = 0

    # 1. Basic n! arrangements (60)
    items_list = ["books", "trophies", "chairs", "paintings", "certificates", "medals", "plant pots", "family portraits", "learners", "runners", "cars", "bicycles"]
    shelves_list = ["on a shelf", "in a display cabinet", "in a straight row", "on a stage", "along a wall", "on a podium", "in a queue", "in a rack"]
    while easy_count < 60:
        n = random.randint(4, 10)
        item = random.choice(items_list)
        shelf = random.choice(shelves_list)
        ans = math.factorial(n)
        q = f"In how many different ways can ${n}$ unique {item} be arranged {shelf}?"
        wrongs = get_w_ints(ans)
        exp = f"The number of ways to arrange $n$ distinct items in a row is given by $n! = {n}! = {ans}$."
        if add_q("easy", "Counting Principle", q, str(ans), wrongs, exp, "Knowledge"):
            easy_count += 1

    # 2. Multiplication rule (outfits, meals, accessories) (60)
    comb_categories = [
        ("starters", "main courses", "desserts"),
        ("shirts", "pairs of trousers", "pairs of shoes"),
        ("laptops", "printers", "monitors"),
        ("jackets", "ties", "belts"),
        ("sandwiches", "fruit juices", "muffins"),
        ("bicycles", "helmets", "water bottles"),
        ("notebooks", "pens", "highlighters"),
        ("dresses", "handbags", "pairs of heels")
    ]
    while easy_count < 120:
        c1, c2, c3 = random.choice(comb_categories)
        n1 = random.randint(2, 8)
        n2 = random.randint(3, 9)
        n3 = random.randint(2, 7)
        ans = n1 * n2 * n3
        q = f"A shopper chooses from ${n1}$ {c1}, ${n2}$ {c2}, and ${n3}$ {c3}. How many different selections consisting of one of each item are possible?"
        wrongs = get_w_ints(ans)
        exp = f"Using the Fundamental Counting Principle: $N = {n1} \\times {n2} \\times {n3} = {ans}$."
        if add_q("easy", "Counting Principle", q, str(ans), wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 3. Complementary events P(A') = 1 - P(A) (60)
    event_names = [
        "passing a mathematics exam", "it raining tomorrow", "a soccer team winning a match",
        "drawing a red card from a deck", "a train arriving on time", "a learner being selected as prefect",
        "winning a raffle prize", "a light bulb lasting more than 1000 hours"
    ]
    while easy_count < 180:
        p = round(random.uniform(0.08, 0.92), 2)
        ans = round(1 - p, 2)
        ev = random.choice(event_names)
        q = f"If the probability of {ev} is $P(E) = {p:.2f}$, what is the probability of the event NOT occurring, $P(E')$?"
        wrongs = get_w_probs(ans)
        exp = f"According to the rule of complementary events: $P(E') = 1 - P(E) = 1 - {p:.2f} = {ans:.2f}$."
        if add_q("easy", "Complementary Events", q, f"{ans:.2f}", wrongs, exp, "Knowledge"):
            easy_count += 1

    # 4. Mutually exclusive addition rule P(A or B) = P(A) + P(B) (60)
    while easy_count < 240:
        p1 = round(random.uniform(0.10, 0.45), 2)
        p2 = round(random.uniform(0.10, 0.45), 2)
        ans = round(p1 + p2, 2)
        q = f"Events $A$ and $B$ are mutually exclusive (disjoint). If $P(A) = {p1:.2f}$ and $P(B) = {p2:.2f}$, find $P(A \\cup B)$."
        wrongs = get_w_probs(ans)
        exp = f"Because $A$ and $B$ are mutually exclusive, $P(A \\cap B) = 0$. Hence $P(A \\cup B) = P(A) + P(B) = {p1:.2f} + {p2:.2f} = {ans:.2f}$."
        if add_q("easy", "Mutually Exclusive Events", q, f"{ans:.2f}", wrongs, exp, "Routine Procedures"):
            easy_count += 1

    # 5. Simple Independent events P(A and B) = P(A) * P(B) (60)
    while easy_count < 300:
        p1 = round(random.uniform(0.1, 0.8), 2)
        p2 = round(random.uniform(0.1, 0.8), 2)
        ans = round(p1 * p2, 4)
        ans_str = f"{ans:.4f}".rstrip('0').rstrip('.')
        q = f"Given that events $A$ and $B$ are independent with $P(A) = {p1:.2f}$ and $P(B) = {p2:.2f}$, calculate $P(A \\cap B)$."
        wrongs = get_w_probs(ans)
        exp = f"For independent events: $P(A \\cap B) = P(A) \\times P(B) = {p1:.2f} \\times {p2:.2f} = {ans_str}$."
        if add_q("easy", "Independent Events", q, ans_str, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    print(f"Easy questions created: {easy_count}")

    # ====================================================
    # MEDIUM QUESTIONS (Target: 500)
    # ====================================================
    medium_count = 0

    # 1. Permutations of letters with repetition (word anagrams) (100)
    words_data = [
        ("BANANA", 6, [("A", 3), ("N", 2)]),
        ("SUCCESS", 7, [("S", 3), ("C", 2)]),
        ("PARALLEL", 8, [("A", 2), ("L", 3)]),
        ("STATISTICS", 10, [("S", 3), ("T", 3), ("I", 2)]),
        ("ALGEBRA", 7, [("A", 2)]),
        ("EXCELLENT", 9, [("E", 3), ("L", 2)]),
        ("MATHEMATICS", 11, [("M", 2), ("A", 2), ("T", 2)]),
        ("CHOCOLATE", 9, [("C", 2), ("O", 2)]),
        ("BALLOON", 7, [("L", 2), ("O", 2)]),
        ("COFFEE", 6, [("F", 2), ("E", 2)]),
        ("ENGINEERING", 11, [("E", 3), ("N", 3), ("G", 2), ("I", 2)]),
        ("BOOKKEEPER", 10, [("O", 2), ("K", 2), ("E", 3)]),
        ("COMMITTEE", 9, [("M", 2), ("T", 2), ("E", 2)]),
        ("MISSISSIPPI", 11, [("I", 4), ("S", 4), ("P", 2)]),
        ("TENNESSEE", 9, [("E", 4), ("N", 2), ("S", 2)]),
        ("ASSESSMENT", 10, [("S", 4), ("E", 2)]),
        ("INSTITUTION", 11, [("I", 3), ("T", 3), ("N", 2)]),
        ("POSSESSION", 10, [("S", 4), ("O", 2)]),
        ("TRIGONOMETRY", 12, [("T", 2), ("R", 2), ("O", 2)]),
        ("COORDINATE", 10, [("O", 2)])
    ]
    phrasings_word = [
        "How many distinct letter arrangements can be formed using all the letters in the word",
        "Calculate the total number of unique permutations of the letters in the word",
        "Determine the number of different arrangements that can be made using every letter of the word",
        "In how many different orders can all the letters in the word be arranged:",
        "Find the total number of distinct words (with or without meaning) formed by rearranging all the letters of"
    ]
    while medium_count < 100:
        word, total_len, repeats = random.choice(words_data)
        phrase = random.choice(phrasings_word)
        num = math.factorial(total_len)
        denom = 1
        denom_str_parts = []
        for ch, count in repeats:
            denom *= math.factorial(count)
            denom_str_parts.append(f"{count}!")
        ans = num // denom
        denom_str = " \\times ".join(denom_str_parts)
        q = f"{phrase} **\"{word}\"**?"
        wrongs = get_w_ints(ans)
        exp = f"Using the permutation formula with repeated letters: $\\frac{{n!}}{{n_1! n_2! \\dots}} = \\frac{{{total_len}!}}{{{denom_str}}} = \\frac{{{num}}}{{{denom}}} = {ans}$."
        if add_q("medium", "Counting Principle", q, str(ans), wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 2. Block method (Specific items grouped together) (80)
    names_pairs = [
        ("Sipho", "Thabo"), ("Alice", "Bob"), ("Liam", "Noah"), ("Kagiso", "Lindiwe"),
        ("Tshepo", "Bongani"), ("Chloe", "Emma"), ("Sarah", "Leah"), ("Ethan", "Lucas"),
        ("Amina", "Fatima"), ("David", "Samuel"), ("Ayanda", "Naledi"), ("Bandile", "Khaya")
    ]
    locations = ["in a row of chairs", "in a cinema queue", "on a park bench", "for a group photo in a line", "at an executive boardroom table in a row"]
    while medium_count < 180:
        total = random.randint(5, 11)
        p1, p2 = random.choice(names_pairs)
        loc = random.choice(locations)
        ans = math.factorial(total - 1) * 2
        q = f"${total}$ people, including {p1} and {p2}, are seated {loc}. How many arrangements are possible if {p1} and {p2} must always sit next to each other?"
        wrongs = get_w_ints(ans)
        exp = f"Treat {p1} and {p2} as a single unit. There are now $({total} - 1) = {total-1}$ units, which can be arranged in $({total-1})!$ ways. The $2$ people can switch positions in $2!$ ways. Total $= ({total-1})! \\times 2! = {ans}$."
        if add_q("medium", "Counting Principle", q, str(ans), wrongs, exp, "Complex Procedures"):
            medium_count += 1

    # 3. Items NOT seated together (80)
    while medium_count < 260:
        total = random.randint(5, 10)
        p1, p2 = random.choice(names_pairs)
        loc = random.choice(locations)
        tot_fact = math.factorial(total)
        together_fact = math.factorial(total - 1) * 2
        ans = tot_fact - together_fact
        q = f"${total}$ learners line up {loc}. In how many different ways can they be arranged if {p1} and {p2} refuse to stand next to each other?"
        wrongs = get_w_ints(ans)
        exp = f"Total arrangements without restrictions $= {total}! = {tot_fact}$. Arrangements where {p1} and {p2} are together $= ({total}-1)! \\times 2! = {together_fact}$. Arrangements where they are NOT together $= {tot_fact} - {together_fact} = {ans}$."
        if add_q("medium", "Counting Principle", q, str(ans), wrongs, exp, "Complex Procedures"):
            medium_count += 1

    # 4. Inclusion-Exclusion Rule (P(A U B) = P(A) + P(B) - P(A and B)) (80)
    while medium_count < 340:
        p_A = round(random.uniform(0.35, 0.65), 2)
        p_B = round(random.uniform(0.30, 0.60), 2)
        p_inter = round(random.uniform(0.10, min(p_A, p_B) - 0.05), 2)
        p_union = round(p_A + p_B - p_inter, 2)
        
        mode = random.choice(["find_union", "find_inter"])
        if mode == "find_union":
            q = f"Given events $A$ and $B$ where $P(A) = {p_A:.2f}$, $P(B) = {p_B:.2f}$, and $P(A \\cap B) = {p_inter:.2f}$. Calculate $P(A \\cup B)$."
            ans_str = f"{p_union:.2f}"
            wrongs = get_w_probs(p_union)
            exp = f"By the addition rule: $P(A \\cup B) = P(A) + P(B) - P(A \\cap B) = {p_A:.2f} + {p_B:.2f} - {p_inter:.2f} = {ans_str}$."
        else:
            q = f"For events $A$ and $B$, $P(A) = {p_A:.2f}$, $P(B) = {p_B:.2f}$, and $P(A \\cup B) = {p_union:.2f}$. Find $P(A \\cap B)$."
            ans_str = f"{p_inter:.2f}"
            wrongs = get_w_probs(p_inter)
            exp = f"Rearranging the addition rule: $P(A \\cap B) = P(A) + P(B) - P(A \\cup B) = {p_A:.2f} + {p_B:.2f} - {p_union:.2f} = {ans_str}$."
            
        if add_q("medium", "Addition Rule", q, ans_str, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 5. Testing Independence (60)
    while medium_count < 400:
        p_A = round(random.uniform(0.2, 0.6), 2)
        p_B = round(random.uniform(0.2, 0.5), 2)
        is_indep = random.choice([True, False])
        if is_indep:
            p_inter = round(p_A * p_B, 4)
            p_inter_str = f"{p_inter:.4f}".rstrip('0').rstrip('.')
            ans = "Yes, independent because P(A and B) = P(A) * P(B)"
            wrongs = [
                "No, dependent because P(A and B) != P(A) * P(B)",
                "No, because the events are mutually exclusive",
                "Yes, because P(A and B) = 0",
                "Cannot be determined without a Venn diagram",
                "No, because P(A) + P(B) > 1",
                "Yes, because P(A or B) = P(A) + P(B)",
                "No, because P(A) != P(B)"
            ]
        else:
            p_inter = round(p_A * p_B + random.choice([-0.05, 0.05, 0.08, -0.08]), 4)
            if p_inter <= 0 or p_inter >= min(p_A, p_B):
                p_inter = round(p_A * p_B + 0.04, 4)
            p_inter_str = f"{p_inter:.4f}".rstrip('0').rstrip('.')
            ans = "No, dependent because P(A and B) != P(A) * P(B)"
            wrongs = [
                "Yes, independent because P(A and B) = P(A) * P(B)",
                "Yes, because the events are mutually exclusive",
                "Cannot be determined without sample size",
                "No, because P(A and B) is greater than 0",
                "Yes, because P(A or B) = 1",
                "Yes, because P(A) * P(B) is a valid probability",
                "No, because P(A) and P(B) are not complementary"
            ]
        product = round(p_A * p_B, 4)
        product_str = f"{product:.4f}".rstrip('0').rstrip('.')
        q = f"Let $P(A) = {p_A:.2f}$, $P(B) = {p_B:.2f}$, and $P(A \\cap B) = {p_inter_str}$. Are events $A$ and $B$ independent?"
        exp = f"Evaluate $P(A) \\times P(B) = {p_A:.2f} \\times {p_B:.2f} = {product_str}$. Given $P(A \\cap B) = {p_inter_str}$. Since $P(A \\cap B) {'=' if is_indep else '\\neq'} P(A) \\times P(B)$, the events are {'independent' if is_indep else 'dependent'}."
        if add_q("medium", "Independent Events", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 6. Tree Diagrams / Successive draws without replacement (60)
    bag_items = [
        ("red balls", "blue balls"),
        ("green apples", "red apples"),
        ("black marbles", "white marbles"),
        ("gold tokens", "silver tokens"),
        ("blue counters", "yellow counters")
    ]
    while medium_count < 460:
        red = random.randint(3, 9)
        blue = random.randint(4, 10)
        c1, c2 = random.choice(bag_items)
        tot = red + blue
        mode = random.choice(["both_first", "both_second", "one_each"])
        if mode == "both_first":
            frac = Fraction(red, tot) * Fraction(red - 1, tot - 1)
            q = f"A container holds ${red}$ {c1} and ${blue}$ {c2}. Two items are drawn at random without replacement. Find the probability that BOTH drawn items are {c1}."
            exp = f"$P(\\text{{both {c1}}}) = \\frac{{{red}}}{{{tot}}} \\times \\frac{{{red-1}}}{{{tot-1}}} = {frac.numerator}/{frac.denominator}$."
        elif mode == "both_second":
            frac = Fraction(blue, tot) * Fraction(blue - 1, tot - 1)
            q = f"A container holds ${red}$ {c1} and ${blue}$ {c2}. Two items are drawn at random without replacement. Find the probability that BOTH drawn items are {c2}."
            exp = f"$P(\\text{{both {c2}}}) = \\frac{{{blue}}}{{{tot}}} \\times \\frac{{{blue-1}}}{{{tot-1}}} = {frac.numerator}/{frac.denominator}$."
        else:
            frac = Fraction(red, tot) * Fraction(blue, tot - 1) * 2
            q = f"A container holds ${red}$ {c1} and ${blue}$ {c2}. Two items are drawn at random without replacement. Find the probability that ONE is {c1} and the OTHER is {c2} (in any order)."
            exp = f"$P(\\text{{one of each}}) = 2 \\times \\left(\\frac{{{red}}}{{{tot}}} \\times \\frac{{{blue}}}{{{tot-1}}}\\right) = {frac.numerator}/{frac.denominator}$."
        ans_str = f"{frac.numerator}/{frac.denominator}"
        wrongs = get_w_fracs(frac)
        if add_q("medium", "Tree Diagrams", q, ans_str, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 7. Two-circle Venn Diagrams - solving for unknown intersection (40)
    subjects_sets = [
        ("Mathematics", "Physical Sciences"),
        ("History", "Geography"),
        ("Accounting", "Economics"),
        ("Drama", "Visual Arts"),
        ("Rugby", "Cricket"),
        ("French", "German")
    ]
    while medium_count < 500:
        s1, s2 = random.choice(subjects_sets)
        N = random.choice([50, 60, 75, 80, 90, 100, 120, 150])
        n_A = random.randint(int(N * 0.4), int(N * 0.65))
        n_B = random.randint(int(N * 0.4), int(N * 0.65))
        n_neither = random.randint(int(N * 0.05), int(N * 0.15))
        n_union = N - n_neither
        n_inter = (n_A + n_B) - n_union
        if n_inter <= 0 or n_inter >= min(n_A, n_B):
            continue
        q = f"In a group of ${N}$ learners, ${n_A}$ participate in {s1}, ${n_B}$ participate in {s2}, and ${n_neither}$ do neither. How many learners participate in BOTH {s1} and {s2}?"
        wrongs = get_w_ints(n_inter)
        exp = f"Learners taking at least one activity $= {N} - {n_neither} = {n_union}$. Using $n(A \\cup B) = n(A) + n(B) - n(A \\cap B) \\implies {n_union} = {n_A} + {n_B} - n(A \\cap B) \\implies n(A \\cap B) = {n_A + n_B} - {n_union} = {n_inter}$."
        if add_q("medium", "Venn Diagrams", q, str(n_inter), wrongs, exp, "Routine Procedures"):
            medium_count += 1

    print(f"Medium questions created: {medium_count}")

    # ====================================================
    # HARD QUESTIONS (Target: 200)
    # ====================================================
    hard_count = 0

    # 1. Multi-digit PIN codes / Passwords with strict constraints (50)
    pin_types = [
        "ATM security PIN", "smartphone passcode", "bank vault access code",
        "laboratory digital lock code", "server access code", "alarm keypad PIN",
        "safe combination code", "gate intercom passcode"
    ]
    while hard_count < 50:
        p_type = random.choice(pin_types)
        digits_len = random.randint(4, 7)
        mode = random.choice(["even_allowed", "odd_allowed", "greater_not_allowed", "starts_with_not_allowed"])
        
        if mode == "even_allowed":
            # first digit 1-9 (9 options), middle digits_len-2 (10 each), last digit even (0,2,4,6,8 -> 5 options)
            ans = 9 * (10 ** (digits_len - 2)) * 5
            q = f"A ${digits_len}$-digit {p_type} is generated using digits $0-9$. Repetition of digits IS allowed. If the first digit cannot be $0$ and the final digit must be an EVEN number, how many different codes can be created?"
            exp = f"First digit: $9$ possibilities ($1-9$). Intermediate $({digits_len}-2)$ digits: $10$ options each. Last digit: $5$ options ($0, 2, 4, 6, 8$). Total $= 9 \\times 10^{{{digits_len-2}}} \\times 5 = {ans}$."
        elif mode == "odd_allowed":
            ans = 9 * (10 ** (digits_len - 2)) * 5
            q = f"A ${digits_len}$-digit {p_type} is formed from the digits $0$ to $9$ with repetition allowed. How many valid codes exist if the first digit cannot be $0$ and the code must end in an ODD digit?"
            exp = f"First position: $9$ options ($1-9$). Middle $({digits_len}-2)$ positions: $10$ options each. Final position: $5$ options ($1, 3, 5, 7, 9$). Total $= 9 \\times 10^{{{digits_len-2}}} \\times 5 = {ans}$."
        elif mode == "greater_not_allowed":
            # 5-digit number > threshold formed from {1,2,3,4,5,6,7,8,9} without repetition
            first_digit_min = random.choice([4, 5, 6, 7])
            avail_first = 9 - first_digit_min + 1
            threshold = first_digit_min * 10000
            ans = avail_first * 8 * 7 * 6 * 5
            q = f"A $5$-digit number is constructed using digits $\\{{1, 2, 3, 4, 5, 6, 7, 8, 9\\}}$ without repetition. How many unique numbers strictly greater than ${threshold:,}$ can be formed?"
            exp = f"For the number to exceed ${threshold:,}$, the first digit must be one of $\\{{{', '.join(str(d) for d in range(first_digit_min, 10))}\\}}$ (${avail_first}$ choices). The remaining $4$ digits are chosen from the $8$ remaining digits in $8 \\times 7 \\times 6 \\times 5 = 1680$ ways. Total $= {avail_first} \\times 1680 = {ans}$."
        else:
            # 6-digit code from digits {0,1,2,3,4,5,6,7} without repetition, starts with specific digit or pair
            fixed_start = random.choice([7, 8, 9])
            # 6 digits from 9 digits {1..9}
            ans = 1 * 8 * 7 * 6 * 5 * 4
            q = f"A $6$-digit passcode is formed using the digits $\\{{1, 2, 3, 4, 5, 6, 7, 8, 9\\}}$ without repeating any digit. How many passcodes start with the digit ${fixed_start}$?"
            exp = f"The first digit is fixed as ${fixed_start}$ ($1$ choice). The remaining $5$ positions are filled from the remaining $8$ digits in $8 \\times 7 \\times 6 \\times 5 \\times 4 = {ans}$ ways."

        wrongs = get_w_ints(ans)
        if add_q("hard", "Counting Principle", q, str(ans), wrongs, exp, "Complex Procedures"):
            hard_count += 1

    # 2. Probability using counting principle (50)
    seating_contexts = [
        "are seated in a straight row of chairs for a concert",
        "sit together on a long bench for a portrait photo",
        "are allocated adjacent desks in a single row for an examination",
        "stand in a queue at a ticket counter",
        "sit in a row of seats at an auditorium"
    ]
    while hard_count < 100:
        n = random.randint(5, 14)
        p1, p2 = random.choice(names_pairs)
        ctx = random.choice(seating_contexts)
        together = random.choice([True, False])
        if together:
            frac = Fraction(2, n)
            q = f"${n}$ people, including {p1} and {p2}, {ctx}. What is the probability that {p1} and {p2} sit directly adjacent to each other?"
            exp = f"Total arrangements $n(S) = {n}!$. Favorable arrangements $n(E) = ({n}-1)! \\times 2!$. Probability $P = \\frac{{({n}-1)! \\times 2!}}{{{n}!}} = \\frac{{2}}{{{n}}} = {frac.numerator}/{frac.denominator}$."
        else:
            frac = Fraction(n - 2, n)
            q = f"${n}$ people, including {p1} and {p2}, {ctx}. What is the probability that {p1} and {p2} DO NOT sit next to each other?"
            exp = f"Probability of sitting together $= \\frac{{2}}{{{n}}}$. Therefore, probability of NOT sitting together $= 1 - \\frac{{2}}{{{n}}} = \\frac{{{n-2}}}{{{n}}} = {frac.numerator}/{frac.denominator}$."
        ans_str = f"{frac.numerator}/{frac.denominator}"
        wrongs = get_w_fracs(frac)
        if add_q("hard", "Probability with Counting Principle", q, ans_str, wrongs, exp, "Problem Solving"):
            hard_count += 1

    # 3. Three-set Venn diagrams (50)
    while hard_count < 150:
        x_val = random.randint(5, 20)
        a, b, c = random.randint(6, 16), random.randint(6, 16), random.randint(6, 16)
        m_only, p_only, l_only = random.randint(10, 25), random.randint(10, 25), random.randint(10, 25)
        neither = random.randint(4, 15)
        total_students = m_only + p_only + l_only + a + b + c + x_val + neither
        tot_M = m_only + a + b + x_val
        tot_P = p_only + a + c + x_val
        tot_L = l_only + b + c + x_val
        
        q = (f"In a cohort of ${total_students}$ Grade 12 learners: ${tot_M}$ take Mathematics, ${tot_P}$ take Physical Sciences, and ${tot_L}$ take Life Sciences. "
             f"Furthermore, ${a + x_val}$ take Mathematics and Physical Sciences, ${b + x_val}$ take Mathematics and Life Sciences, ${c + x_val}$ take Physical Sciences and Life Sciences, "
             f"while ${neither}$ learners take none of these three subjects. How many learners take ALL THREE subjects?")
        wrongs = get_w_ints(x_val)
        exp = (f"Using the inclusion-exclusion formula: Total learners $= n(M) + n(P) + n(L) - [n(M \\cap P) + n(M \\cap L) + n(P \\cap L)] + x + \\text{{neither}}$. "
               f"${total_students} = {tot_M} + {tot_P} + {tot_L} - ({a+x_val} + {b+x_val} + {c+x_val}) + x + {neither}$. "
               f"Solving for $x$: $x = {x_val}$ learners take all three subjects.")
        if add_q("hard", "Venn Diagrams", q, str(x_val), wrongs, exp, "Problem Solving"):
            hard_count += 1

    # 4. Word permutations with boundary constraints (50)
    constrained_words = [
        ("PROBABILITY", 11, "B", "Y", {"B": 2, "I": 2}, "starts with 'B' and ends with 'Y'"),
        ("ARRANGEMENT", 11, "A", "T", {"A": 2, "R": 2, "E": 2, "N": 2}, "starts with 'A' and ends with 'T'"),
        ("COMBINATION", 11, "C", "N", {"O": 2, "I": 2, "N": 2}, "starts with 'C' and ends with 'N'"),
        ("PERMUTATION", 11, "P", "N", {"T": 2}, "starts with 'P' and ends with 'N'"),
        ("STATISTICS", 10, "S", "S", {"S": 3, "T": 3, "I": 2}, "starts with 'S' and ends with 'S'"),
        ("CALCULATOR", 10, "C", "R", {"C": 2, "A": 2, "L": 2}, "starts with 'C' and ends with 'R'"),
        ("MISSISSIPPI", 11, "M", "I", {"I": 4, "S": 4, "P": 2}, "starts with 'M' and ends with 'I'"),
        ("EXCELLENT", 9, "E", "T", {"E": 3, "L": 2}, "starts with 'E' and ends with 'T'"),
        ("ASSESSMENT", 10, "A", "T", {"S": 4, "E": 2}, "starts with 'A' and ends with 'T'"),
        ("INSTITUTION", 11, "I", "N", {"I": 3, "T": 3, "N": 2}, "starts with 'I' and ends with 'N'"),
        ("MATHEMATICS", 11, "M", "S", {"M": 2, "A": 2, "T": 2}, "starts with 'M' and ends with 'S'"),
        ("ENGINEERING", 11, "E", "G", {"E": 3, "N": 3, "G": 2, "I": 2}, "starts with 'E' and ends with 'G'")
    ]
    while hard_count < 200:
        word, w_len, first_ch, last_ch, repeats, cond_desc = random.choice(constrained_words)
        tot_num = math.factorial(w_len)
        tot_denom = 1
        for count in repeats.values():
            tot_denom *= math.factorial(count)
        total_arr = tot_num // tot_denom
        
        rem_repeats = dict(repeats)
        if first_ch in rem_repeats:
            rem_repeats[first_ch] -= 1
            if rem_repeats[first_ch] <= 1:
                del rem_repeats[first_ch]
        if last_ch in rem_repeats:
            rem_repeats[last_ch] -= 1
            if rem_repeats[last_ch] <= 1:
                del rem_repeats[last_ch]
                
        fav_num = math.factorial(w_len - 2)
        fav_denom = 1
        for count in rem_repeats.values():
            fav_denom *= math.factorial(count)
        fav_arr = fav_num // fav_denom
        
        prob_frac = Fraction(fav_arr, total_arr)
        ans_str = f"{prob_frac.numerator}/{prob_frac.denominator}"
        phr_opts = [
            f"If all letters of the word **\"{word}\"** are randomly arranged, what is the probability that the word {cond_desc}?",
            f"All letters of the word **\"{word}\"** are randomly shuffled in a straight row. Calculate the probability that the arrangement {cond_desc}.",
            f"A word is formed by randomly rearranging all letters of **\"{word}\"**. Determine the probability that the arrangement {cond_desc}.",
            f"Letters from the word **\"{word}\"** are arranged at random without replacement. Find the probability that the resulting word {cond_desc}.",
            f"What is the theoretical probability that a random permutation of all letters in **\"{word}\"** {cond_desc}?"
        ]
        phr = random.choice(phr_opts)
        wrongs = get_w_fracs(prob_frac)
        exp = f"Total arrangements $n(S) = \\frac{{{w_len}!}}{{\\text{{repeats}}}} = {total_arr}$. Fixing '{first_ch}' at the start and '{last_ch}' at the end leaves $({w_len}-2)$ positions, giving $n(E) = {fav_arr}$ favorable arrangements. $P = \\frac{{{fav_arr}}}{{{total_arr}}} = {ans_str}$."
        if add_q("hard", "Probability with Counting Principle", phr, ans_str, wrongs, exp, "Problem Solving"):
            hard_count += 1

    print(f"Final Counts: {{'easy': {easy_count}, 'medium': {medium_count}, 'hard': {hard_count}}}")
    out_dir = "dataset/grade12/mathematics"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_probability.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    t1 = time.time()
    print(f"SUCCESS: {out_file} generated in {t1-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_probability()
