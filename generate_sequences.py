import random
import math
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

def generate_sequences():
    gen = TopicGenerator("Patterns and Sequences", "SEQ", ["arithmetic sequences", "geometric sequences", "sigma notation", "series sums"])

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1

        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs:
            break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        if subtopic == "arithmetic sequences":
            if difficulty == "easy":
                a = random.randint(-200, 200)
                d = random.randint(-100, 100)
                if d == 0: d = 5
                n = random.randint(5, 100)
                term_n = a + (n - 1) * d
                q = f"Given the arithmetic sequence ${a}; {a+d}; {a+2*d}; \\dots$, find the ${n}^\\text{{th}}$ term."
                exp = f"$T_n = a + (n-1)d \\implies T_{{{n}}} = {a} + ({n}-1)({d}) = {term_n}$"

                wrong_answers = get_wrong_ints(term_n)
                gen.add_question(subtopic, difficulty, q, str(term_n), wrong_answers, exp)

            elif difficulty == "medium":
                a = random.randint(-200, 200)
                d = random.randint(-100, 100)
                if d == 0: d = 7
                n = random.randint(20, 300)
                last_term = a + (n - 1) * d
                q = f"How many terms are in the arithmetic sequence ${a}; {a+d}; {a+2*d}; \\dots; {last_term}$?"
                exp = f"$T_n = a + (n-1)d \\implies {last_term} = {a} + (n-1)({d}) \\implies n = {n}$"

                wrong_answers = get_wrong_ints(n)
                gen.add_question(subtopic, difficulty, q, str(n), wrong_answers, exp)

            elif difficulty == "hard":
                a = random.randint(-100, 100)
                d = random.randint(-50, 50)
                if d == 0: d = -3
                n1, n2 = sorted(random.sample(range(2, 80), 2))
                t1 = a + (n1 - 1) * d
                t2 = a + (n2 - 1) * d
                q = f"In an arithmetic sequence, $T_{{{n1}}} = {t1}$ and $T_{{{n2}}} = {t2}$. Find the common difference $d$."
                exp = f"$T_{{{n1}}} = a + {n1-1}d = {t1}$ and $T_{{{n2}}} = a + {n2-1}d = {t2}$. Subtracting the equations gives $d = {d}$."

                wrong_answers = get_wrong_ints(d)
                gen.add_question(subtopic, difficulty, q, str(d), wrong_answers, exp)

        elif subtopic == "geometric sequences":
            if difficulty == "easy":
                a = random.choice([2, 3, 4, 5, 10, -2, -3, -4, -5, 6, -6, 7, -7])
                r = random.choice([-2, 2, -3, 3, 4, -4, 5, -5, 0.5, -0.5, 0.25, 1.5, -1.5])
                n = random.randint(4, 10)
                term_n = a * (r ** (n - 1))
                if isinstance(r, float) or isinstance(term_n, float):
                    q = f"Given the geometric sequence ${a}; {a*r:g}; {a*(r**2):g}; \\dots$, find the ${n}^\\text{{th}}$ term."
                    term_n_str = f"{term_n:g}"
                    wrong_answers = get_wrong_floats(term_n)
                else:
                    q = f"Given the geometric sequence ${a}; {a*r}; {a*(r**2)}; \\dots$, find the ${n}^\\text{{th}}$ term."
                    term_n_str = str(int(term_n))
                    wrong_answers = get_wrong_ints(int(term_n))

                exp = f"$T_n = ar^{{n-1}} \\implies T_{{{n}}} = ({a})({r})^{{{n}-1}} = {term_n_str}$"
                gen.add_question(subtopic, difficulty, q, term_n_str, wrong_answers, exp)

            elif difficulty == "medium":
                a = random.choice([2, 3, 4, 5, 10, -2, -3, 6, -6, 7, -7])
                r = random.choice([2, 3, 4, 5, 6])
                n = random.randint(4, 12)
                term_n = a * (r ** (n - 1))
                q = f"In a geometric sequence, the first term is ${a}$ and the ${n}^\\text{{th}}$ term is ${term_n}$. Find the common ratio $r$ (assume $r > 0$)."
                exp = f"$T_n = ar^{{n-1}} \\implies {term_n} = {a}r^{{{n}-1}} \\implies r^{{{n}-1}} = {term_n/a:g} \\implies r = {r}$"
                wrong_answers = get_wrong_ints(r)
                gen.add_question(subtopic, difficulty, q, str(r), wrong_answers, exp)

            elif difficulty == "hard":
                a = random.randint(10, 500)
                r_num, r_den = random.choice([(1, 2), (1, 3), (2, 3), (-1, 2), (-1, 3), (1, 4), (3, 4), (1, 5), (2, 5)])
                r = r_num / r_den
                S_inf = a / (1 - r)
                q = f"Find the sum to infinity of the geometric sequence: ${a}; {a*r:g}; {a*(r**2):g}; \\dots$"
                S_inf_str = f"{S_inf:g}"
                exp = f"$S_\\infty = \\frac{{a}}{{1-r}} = \\frac{{{a}}}{{1 - ({r_num}/{r_den})}} = {S_inf_str}$"

                wrong_answers = get_wrong_floats(float(S_inf))
                gen.add_question(subtopic, difficulty, q, S_inf_str, wrong_answers, exp)

        elif subtopic == "sigma notation" or subtopic == "series sums":
            if difficulty == "easy":
                a = random.randint(-100, 100)
                d = random.randint(2, 30)
                n = random.randint(10, 150)
                S_n = int(n/2 * (2*a + (n-1)*d))
                q = f"Calculate the sum of the first ${n}$ terms of the arithmetic series: ${a} + {a+d} + {a+2*d} + \\dots$"
                S_n_str = str(S_n)
                exp = f"$S_n = \\frac{{n}}{{2}}[2a + (n-1)d] = \\frac{{{n}}}{{2}}[2({a}) + ({n}-1)({d})] = {S_n_str}$"
                wrong_answers = get_wrong_ints(S_n)
                gen.add_question(subtopic, difficulty, q, S_n_str, wrong_answers, exp)

            elif difficulty == "medium":
                a = random.randint(-50, 50)
                d = random.randint(2, 20)
                n = random.randint(10, 80)
                k_start = random.randint(1, 20)
                k_end = k_start + n - 1
                S_n = int(n/2 * (2*(a + (k_start-1)*d) + (n-1)*d))
                q = f"Evaluate: $\\sum_{{k={k_start}}}^{{{k_end}}} ({d}k + {a-d})$"
                S_n_str = str(S_n)
                exp = f"This is an arithmetic series with $n = {k_end} - {k_start} + 1 = {n}$ terms. $a = {d*k_start + a - d}$. Sum = ${S_n_str}$"
                wrong_answers = get_wrong_ints(S_n)
                gen.add_question(subtopic, difficulty, q, S_n_str, wrong_answers, exp)

            elif difficulty == "hard":
                a = random.choice([2, 3, 4, 5, 6])
                r = random.choice([2, 3, 4])
                k_start = random.randint(1, 5)
                k_end = k_start + random.randint(4, 9)
                n = k_end - k_start + 1
                S_n = int(a * (r**(k_start-1)) * ((r**n) - 1) / (r - 1))
                q = f"Evaluate: $\\sum_{{k={k_start}}}^{{{k_end}}} {a}({r})^{{k-1}}$"
                S_n_str = str(S_n)
                exp = f"Geometric series with $a = {a*(r**(k_start-1))}$, $r = {r}$, $n = {n}$. $S_n = \\frac{{a(r^n - 1)}}{{r - 1}} = {S_n_str}$"
                wrong_answers = get_wrong_ints(S_n)
                gen.add_question(subtopic, difficulty, q, S_n_str, wrong_answers, exp)

    return gen

if __name__ == "__main__":
    gen = generate_sequences()
    gen.save_to_json("paper1_sequences.json")
    print(f"Generated {len(gen.questions)} sequences questions.")
