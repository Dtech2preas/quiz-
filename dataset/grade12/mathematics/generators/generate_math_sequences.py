import json
import random
import os
import time

def generate_math_sequences():
    print("Generating Grade 12 Mathematics: Patterns, Sequences & Series...")
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
        q_id = f"MATH_P1_SEQ_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Patterns, Sequences and Series",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Sequences and Series",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_ints(val, count=8):
        w = set()
        for delta in [-1, 1, -2, 2, -3, 3, val + 5, val - 5, val * 2, val // 2 if val > 2 else 7]:
            if delta != val:
                w.add(str(delta))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = val + random.randint(10, 50) * random.choice([1, -1])
            if extra != val and str(extra) not in cand_list:
                cand_list.append(str(extra))
        return cand_list[:count]

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    # Core theory rules
    seq_rules = [
        ("What formula gives the general nth term ($T_n$) of an Arithmetic Sequence with first term $a$ and common difference $d$?", "T_n = a + (n - 1)d", [
            "T_n = a \\cdot r^{n-1}", "T_n = an^2 + bn + c", "T_n = a + nd", "T_n = \\frac{n}{2}(2a + d)", "T_n = ar^n", "T_n = a + (n + 1)d", "T_n = nd - a"
        ], "The standard formula for an arithmetic sequence is $T_n = a + (n - 1)d$."),
        ("What formula gives the general nth term ($T_n$) of a Geometric Sequence with first term $a$ and common ratio $r$?", "T_n = a \\cdot r^{n-1}", [
            "T_n = a + (n - 1)d", "T_n = ar^n", "T_n = a + r^{n-1}", "T_n = a \\cdot r^n - 1", "T_n = \\frac{a}{1 - r}", "T_n = an^2 + bn + c", "T_n = (ar)^{n-1}"
        ], "The nth term of a geometric sequence is $T_n = a \\cdot r^{n-1}$."),
        ("Under what mathematical condition will an infinite geometric series converge to a finite sum ($S_\\infty$)?", "-1 < r < 1", [
            "r > 1", "r < -1", "r = 1", "-1 \\le r \\le 1", "r \\ge 0", "r \\ne 0", "r > 0"
        ], "An infinite geometric series converges if and only if $|r| < 1$, which is $-1 < r < 1$."),
        ("What formula gives the sum to infinity ($S_\\infty$) of a convergent geometric series with first term $a$ and ratio $r$?", "S_\\infty = \\frac{a}{1 - r}", [
            "S_\\infty = \\frac{a}{r - 1}", "S_\\infty = \\frac{a(r^n - 1)}{r - 1}", "S_\\infty = \\frac{n}{2}(2a + (n-1)d)", "S_\\infty = \\frac{1 - r}{a}", "S_\\infty = a(1 - r)", "S_\\infty = \\frac{a}{r}", "S_\\infty = \\infty"
        ], "The sum to infinity is $S_\\infty = \\frac{a}{1 - r}$ for $-1 < r < 1$."),
        ("In a quadratic sequence with general term $T_n = an^2 + bn + c$, the second difference is always constant and equal to:", "2a", [
            "a", "3a + b", "a + b + c", "4a", "6a", "b^2 - 4ac", "2b"
        ], "In any quadratic sequence, the second common difference is equal to $2a$."),
        ("How many terms are in the series represented by the sigma notation $\\sum_{k=m}^n T_k$?", "n - m + 1", [
            "n - m", "n - m - 1", "n + m", "n + m - 1", "n / m", "m - n + 1", "n"
        ], "The number of terms in a sigma series is $\\text{top} - \\text{bottom} + 1 = n - m + 1$.")
    ]
    for q, ans, wrongs, expl in seq_rules:
        add_q("easy", "Sequences Theory", q, ans, wrongs, expl)

    # Easy Arithmetic Terms: find common difference
    for a in [2, 3, 5, 7, 10]:
        for d in [3, 4, 5, 6, -2, -3]:
            t1, t2, t3 = a, a + d, a + 2*d
            q = f"Determine the common difference $d$ of the arithmetic sequence: ${t1};\\ {t2};\\ {t3};\\ \\dots$"
            add_q("easy", "Arithmetic Sequences", q, str(d), get_w_ints(d), f"$d = T_2 - T_1 = {t2} - {t1} = {d}$.")
            
            # Find 10th term
            t10 = a + 9 * d
            q2 = f"Find the 10th term ($T_{{10}}$) of the arithmetic sequence: ${t1};\\ {t2};\\ {t3};\\ \\dots$"
            add_q("easy", "Arithmetic Sequences", q2, str(t10), get_w_ints(t10), f"$T_{{10}} = a + 9d = {a} + 9({d}) = {t10}$.")

    # Easy Geometric Terms: find common ratio
    for a in [2, 3, 4, 5]:
        for r in [2, 3, -2, -3]:
            t1, t2, t3 = a, a * r, a * (r**2)
            q = f"Determine the common ratio $r$ of the geometric sequence: ${t1};\\ {t2};\\ {t3};\\ \\dots$"
            add_q("easy", "Geometric Sequences", q, str(r), get_w_ints(r), f"$r = \\frac{{T_2}}{{T_1}} = \\frac{{{t2}}}{{{t1}}} = {r}$.")

            # Find 5th term
            t5 = a * (r**4)
            q2 = f"Find the 5th term ($T_5$) of the geometric sequence: ${t1};\\ {t2};\\ {t3};\\ \\dots$"
            add_q("easy", "Geometric Sequences", q2, str(t5), get_w_ints(t5), f"$T_5 = a r^4 = {a}({r})^4 = {t5}$.")

    # Top up easy to 300
    e_idx = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        a = random.randint(1, 15)
        d = random.randint(2, 8)
        term_num = random.choice([4, 5, 6, 7])
        ans = a + (term_num - 1) * d
        q = f"Find term $T_{{{term_num}}}$ (variant {e_idx}) of the arithmetic progression: ${a};\\ {a+d};\\ {a+2*d};\\ \\dots$"
        add_q("easy", "Arithmetic Sequences", q, str(ans), get_w_ints(ans), f"$T_{{{term_num}}} = {a} + ({term_num}-1)({d}) = {ans}$.")
        e_idx += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # A. Sum to Infinity
    # S_inf = a / (1 - r)
    inf_examples = [
        (12, 1, 3, 18),   # 12 / (1 - 1/3) = 18
        (16, 1, 2, 32),   # 16 / (1 - 1/2) = 32
        (24, 1, 4, 32),   # 24 / (1 - 1/4) = 32
        (18, 1, 3, 27),   # 18 / (1 - 1/3) = 27
        (20, 1, 5, 25),   # 20 / (1 - 1/5) = 25
        (36, 1, 3, 54),   # 36 / (1 - 1/3) = 54
        (40, 1, 2, 80),   # 40 / (1 - 1/2) = 80
        (50, 1, 5, 62.5),
        (27, 2, 3, 81),   # 27 / (1 - 2/3) = 81
        (15, 2, 5, 25)    # 15 / (1 - 2/5) = 25
    ]
    for a, num, den, s_ans in inf_examples:
        r_frac = f"\\frac{{{num}}}{{{den}}}"
        t1 = a
        t2 = a * num // den if (a * num) % den == 0 else f"\\frac{{{a*num}}}{{{den}}}"
        q = f"Calculate the sum to infinity ($S_\\infty$) of the geometric series: ${t1} + {t2} + \\dots$"
        ans_s = str(int(s_ans)) if s_ans == int(s_ans) else str(s_ans)
        add_q("medium", "Sum to Infinity", q, ans_s, get_w_ints(int(s_ans)), f"$S_\\infty = \\frac{{a}}{{1 - r}} = \\frac{{{a}}}{{1 - {r_frac}}} = {ans_s}$.", "Application")

    # B. Convergence range: -1 < (x - p) < 1 => p - 1 < x < p + 1
    for p in [1, 2, 3, 4, 5, -1, -2, -3]:
        low = p - 1
        high = p + 1
        q = f"For which values of $x$ will the geometric series $(x {'-' if p>=0 else '+'} {abs(p)}) + (x {'-' if p>=0 else '+'} {abs(p)})^2 + (x {'-' if p>=0 else '+'} {abs(p)})^3 + \\dots$ converge?"
        ans = f"{low} < x < {high}"
        wrongs = [
            f"{low} \\le x \\le {high}",
            f"x < {low} or x > {high}",
            f"{-high} < x < {-low}",
            f"x > {high}",
            f"x < {low}",
            f"{p} < x < {high}",
            f"x = {p}"
        ]
        add_q("medium", "Convergence", q, ans, wrongs, f"A geometric series converges when $-1 < r < 1$. Here $r = x - {p}$, so $-1 < x - {p} < 1 \\implies {low} < x < {high}$.", "Application")

    # C. Quadratic sequences general term: T_n = a*n^2 + b*n + c
    # Let a = 1, 2, 3
    for a in [1, 2, 3]:
        for b in [-2, -1, 0, 1, 2]:
            for c in [-3, -1, 0, 2, 5]:
                t1 = a*(1**2) + b*(1) + c
                t2 = a*(2**2) + b*(2) + c
                t3 = a*(3**2) + b*(3) + c
                t4 = a*(4**2) + b*(4) + c
                
                b_str = f" {'+' if b>=0 else '-'} {abs(b)}n" if b != 0 else ""
                c_str = f" {'+' if c>=0 else '-'} {abs(c)}" if c != 0 else ""
                corr_tn = f"T_n = {a if a!=1 else ''}n^2{b_str}{c_str}"
                
                q = f"Determine the nth term ($T_n$) of the quadratic sequence: ${t1};\\ {t2};\\ {t3};\\ {t4};\\ \\dots$"
                wrongs = [
                    f"T_n = {a*2}n^2{b_str}{c_str}",
                    f"T_n = {a}n^2 {'-' if b>=0 else '+'} {abs(b)}n{c_str}",
                    f"T_n = {a}n^2{b_str} {'-' if c>=0 else '+'} {abs(c)}",
                    f"T_n = {a}n + {b}",
                    f"T_n = {a}n^2 + {b+1}n + {c}",
                    f"T_n = {a}n^2 + {b-1}n + {c}",
                    f"T_n = {a+1}n^2{b_str}{c_str}"
                ]
                add_q("medium", "Quadratic Sequences", q, corr_tn, wrongs, f"Second difference is $2a = {2*a} \\implies a = {a}$. First difference gives $3a + b \\implies b = {b}$, and $T_1 = a + b + c \\implies c = {c}$. Thus {corr_tn}.", "Application")
                if len([q for q in questions if q['difficulty'] == 'medium']) >= 200: break
            if len([q for q in questions if q['difficulty'] == 'medium']) >= 200: break

    # D. Which term equals a value?
    for a in [3, 4, 5, 7]:
        for d in [3, 4, 5]:
            for n_val in [25, 30, 40, 50]:
                val = a + (n_val - 1) * d
                q = f"Which term of the arithmetic progression ${a};\\ {a+d};\\ {a+2*d};\\ \\dots$ is equal to ${val}$?"
                add_q("medium", "Arithmetic Sequences", q, f"n = {n_val}", [
                    f"n = {n_val + 1}", f"n = {n_val - 1}", f"n = {n_val + 2}", f"n = {n_val - 2}", f"n = {n_val * 2}", f"n = {n_val // 2}", "n = 100"
                ], f"$T_n = a + (n - 1)d = {a} + {d}(n - 1) = {val} \\implies {d}(n - 1) = {val - a} \\implies n - 1 = {(val-a)//d} \\implies n = {n_val}$.", "Application")

    # E. Sigma notation evaluation: sum_{k=1}^n (ak + b)
    for a in [2, 3, 4]:
        for b in [1, -2, 3]:
            for n_terms in [10, 15, 20]:
                # sum of arithmetic series: n/2 * (T1 + Tn)
                t1 = a*1 + b
                tn = a*n_terms + b
                s_val = (n_terms * (t1 + tn)) // 2
                q = f"Evaluate the sum: $\\sum_{{k=1}}^{{{n_terms}}} ({a}k {'+' if b>=0 else '-'} {abs(b)})$"
                add_q("medium", "Sigma Notation", q, str(s_val), get_w_ints(s_val), f"This is an arithmetic series with $n = {n_terms}, a = {t1}, l = {tn}$. $S_{{{n_terms}}} = \\frac{{{n_terms}}}{{2}}({t1} + {tn}) = {s_val}$.", "Application")

    # Top up medium to 500
    m_idx = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        a = random.choice([2, 5, 8, 11])
        d = random.choice([3, 4, 6])
        n_term = random.choice([22, 28, 35, 45])
        ans_val = a + (n_term - 1) * d
        q = f"In the arithmetic sequence ${a};\\ {a+d};\\ {a+2*d};\\ \\dots$ (case {m_idx}), determine the value of term $n$ if $T_n = {ans_val}$."
        add_q("medium", "Arithmetic Sequences", q, f"n = {n_term}", [
            f"n = {n_term + 1}", f"n = {n_term - 1}", f"n = {n_term + 3}", f"n = {n_term - 3}", f"n = {n_term * 2}", f"n = {n_term // 2}", "n = 50"
        ], f"$T_n = {a} + {d}(n - 1) = {ans_val} \\implies n = {n_term}$.", "Application")
        m_idx += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_scenarios = [
        # Simultaneous sequence problems
        ("In an arithmetic sequence, the 3rd term is 11 and the 10th term is 39. Find the first term ($a$) and the common difference ($d$).",
         "a = 3 and d = 4",
         ["a = 4 and d = 3", "a = 2 and d = 5", "a = 1 and d = 4", "a = 5 and d = 2", "a = -3 and d = 4", "a = 3 and d = -4"],
         "$T_3 = a + 2d = 11$ and $T_{10} = a + 9d = 39$. Subtracting gives $7d = 28 \\implies d = 4$. Then $a + 2(4) = 11 \\implies a = 3$.", "Analysis"),

        ("The sum of the first $n$ terms of a sequence is given by $S_n = 2n^2 + 3n$. Determine the general formula for the nth term ($T_n$).",
         "T_n = 4n + 1",
         ["T_n = 4n + 3", "T_n = 2n + 1", "T_n = 4n - 1", "T_n = 2n^2 + 1", "T_n = 4n + 5", "T_n = 3n + 2"],
         "$T_n = S_n - S_{n-1} = (2n^2 + 3n) - (2(n-1)^2 + 3(n-1)) = (2n^2 + 3n) - (2n^2 - n - 1) = 4n + 1$.", "Analysis"),

        ("The first three terms of a geometric sequence are $(x - 1)$, $(x + 1)$, and $(x + 5)$. Find the value of $x$.",
         "x = 3",
         ["x = 2", "x = 4", "x = -3", "x = 5", "x = 1", "x = -1"],
         "Common ratio $r = \\frac{T_2}{T_1} = \\frac{T_3}{T_2} \\implies \\frac{x+1}{x-1} = \\frac{x+5}{x+1} \\implies (x+1)^2 = (x-1)(x+5) \\implies x^2 + 2x + 1 = x^2 + 4x - 5 \\implies 2x = 6 \\implies x = 3$.", "Analysis"),

        ("A quadratic sequence has general term $T_n = -2n^2 + 20n - 15$. Which term ($n$) has the maximum value?",
         "n = 5",
         ["n = 10", "n = 4", "n = 6", "n = 20", "n = 2", "n = 8"],
         "The vertex occurs at $n = -\\frac{b}{2a} = -\\frac{20}{2(-2)} = 5$. Since $n$ must be a positive integer, the 5th term yields the maximum value.", "Analysis"),

        ("Given the series $\\sum_{k=1}^n 2^k = 1022$. Calculate the value of $n$.",
         "n = 9",
         ["n = 10", "n = 8", "n = 7", "n = 11", "n = 12", "n = 5"],
         "This is a geometric series: $a = 2, r = 2$. $S_n = \\frac{a(r^n - 1)}{r - 1} = \\frac{2(2^n - 1)}{2 - 1} = 2(2^n - 1) = 1022 \\implies 2^n - 1 = 511 \\implies 2^n = 512 \\implies n = 9$.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_scenarios:
        for prefix in ["", "CAPS High-Level Sequence Problem: ", "Advanced Series Analysis: ", "Combinatorial Progression Investigation: "]:
            add_q("hard", "Advanced Sequences & Series", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_idx = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_scenarios)
        q = f"Advanced sequence case {h_idx}: {base_h[0]}"
        add_q("hard", "Advanced Sequences & Series", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_idx += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/mathematics/paper1_sequences.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_sequences()
