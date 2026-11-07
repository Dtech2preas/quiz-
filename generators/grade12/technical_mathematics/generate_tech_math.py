import random
import math
import json
import os
import sys

# Ensure helpers are accessible
sys.path.append(os.path.join(os.getcwd(), 'generators', 'helpers'))
sys.path.append(os.path.join(os.getcwd(), 'generators'))
sys.path.append(os.path.join(os.getcwd()))
try:
    from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats, get_wrong_exprs
except ImportError:
    print("Could not find generators_common!")
    sys.exit(1)

# --- PAPER 1 GENERATORS ---

def gen_p1_algebra():
    gen = TopicGenerator(
        "Algebra, Equations & Inequalities (Technical)", "ALG",
        ["Linear Equations", "Quadratic Equations", "Simultaneous Equations", "Complex Numbers", "Binary Conversions"]
    )

    attempts = 0
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Linear Equations":
            if diff == "easy":
                a = random.randint(2, 9)
                b = random.randint(1, 20)
                ans = random.randint(-10, 10)
                c = a * ans + b
                q = f"Solve for $x$: ${a}x + {b} = {c}$"
                correct = str(ans)
                wrongs = get_wrong_ints(ans, 6)
                exp = f"${a}x = {c} - {b} \\implies {a}x = {c-b} \\implies x = {ans}$"
            elif diff == "medium":
                a = random.randint(2, 6)
                b = random.randint(-10, 10)
                c = random.randint(2, 5)
                d = random.randint(-10, 10)
                ans = random.randint(-5, 5)
                if a == c: c += 1
                val1 = a * (ans + b)
                val2 = c * ans + d
                const2 = val1 - c * ans
                q = f"Solve for $x$: ${a}(x + {b}) = {c}x + {const2}$"
                correct = str(ans)
                wrongs = get_wrong_ints(ans, 6)
                exp = f"${a}x + {a*b} = {c}x + {const2} \\implies {a-c}x = {const2 - a*b} \\implies x = {ans}$"
            else:
                ans = random.randint(-4, 4)
                if ans == 0: ans = 2
                den = random.randint(2, 5)
                a = random.randint(2, 5)
                num = a * ans
                b = random.randint(1, 10)
                c = (num + b) / den
                if c != int(c): continue
                c = int(c)
                q = f"Solve for $x$: $\\frac{{{a}x + {b}}}{{{den}}} = {c}$"
                correct = str(ans)
                wrongs = get_wrong_ints(ans, 6)
                exp = f"${a}x + {b} = {c * den} \\implies {a}x = {c*den - b} \\implies x = {ans}$"

        elif sub == "Quadratic Equations":
            if diff == "easy":
                r1 = random.randint(-5, 5)
                r2 = random.randint(-5, 5)
                if r1 == r2: r2 += 1
                b = -(r1 + r2)
                c = r1 * r2
                b_str = f"+ {b}x" if b > 0 else (f"- {-b}x" if b < 0 else "")
                if b == 1: b_str = "+ x"
                if b == -1: b_str = "- x"
                c_str = f"+ {c}" if c > 0 else (f"- {-c}" if c < 0 else "")
                q = f"Solve for $x$: $x^2 {b_str} {c_str} = 0$"
                r_min, r_max = min(r1, r2), max(r1, r2)
                correct = f"$x = {r_min}$ or $x = {r_max}$"
                wrongs = []
                for _ in range(20):
                    w1 = r_min + random.randint(-3, 3)
                    w2 = r_max + random.randint(-3, 3)
                    if w1 == w2: w2 += 1
                    w_min, w_max = min(w1, w2), max(w1, w2)
                    w_str = f"$x = {w_min}$ or $x = {w_max}$"
                    if w_str != correct and w_str not in wrongs:
                        wrongs.append(w_str)
                    if len(wrongs) == 6: break
                exp = f"Factorise: $(x - {r1})(x - {r2}) = 0 \\implies x = {r1}$ or $x = {r2}$."
            elif diff == "medium":
                a = random.randint(2, 5)
                b = random.randint(2, 8)
                c = random.randint(-10, -1)
                disc = b**2 - 4*a*c
                q = f"Solve for $x$ (correct to two decimal places): ${a}x^2 + {b}x + {c} = 0$"
                ans1 = round((-b + math.sqrt(disc)) / (2*a), 2)
                ans2 = round((-b - math.sqrt(disc)) / (2*a), 2)
                r_min, r_max = min(ans1, ans2), max(ans1, ans2)
                correct = f"$x = {r_min}$ or $x = {r_max}$"
                wrongs = []
                for _ in range(30):
                    w1 = round(r_min + random.uniform(-2, 2), 2)
                    w2 = round(r_max + random.uniform(-2, 2), 2)
                    w_min, w_max = min(w1, w2), max(w1, w2)
                    w_str = f"$x = {w_min}$ or $x = {w_max}$"
                    if w_str != correct and w_str not in wrongs:
                        wrongs.append(w_str)
                    if len(wrongs) == 6: break
                exp = f"Use quadratic formula: $x = \\frac{{-({b}) \\pm \\sqrt{{{b}^2 - 4({a})({c})}}}}{{2({a})}} = \\frac{{{-b} \\pm \\sqrt{{{disc}}}}}{{{2*a}}}$"
            else:
                r1 = random.randint(-4, 0)
                r2 = random.randint(1, 5)
                b = -(r1 + r2)
                c = r1 * r2
                q = f"Solve for $x$: $x^2 + {b}x + {c} \\le 0$"
                correct = f"${r1} \\le x \\le {r2}$"
                wrongs = [
                    f"$x \\le {r1}$ or $x \\ge {r2}$",
                    f"${r1} < x < {r2}$",
                    f"$x < {r1}$ or $x > {r2}$",
                    f"${-r2} \\le x \\le {-r1}$",
                    f"$x \\le {-r2}$ or $x \\ge {-r1}$",
                    f"${r1-1} \\le x \\le {r2+1}$"
                ]
                exp = f"Roots are {r1} and {r2}. The parabola opens upwards, so it is $\\le 0$ between the roots."

        elif sub == "Simultaneous Equations":
            if diff in ["easy", "medium"]:
                x = random.randint(-3, 3)
                y = random.randint(-3, 3)
                a1, b1 = random.randint(1, 3), random.randint(1, 3)
                c1 = a1*x + b1*y
                a2, b2 = random.randint(1, 3), random.randint(-3, -1)
                c2 = a2*x + b2*y
                q = f"Solve for $x$ and $y$: \\\\ ${a1}x + {b1}y = {c1}$ \\\\ ${a2}x {b2}y = {c2}$"
                correct = f"$x = {x}; y = {y}$"
                wrongs = []
                for _ in range(20):
                    wx = x + random.randint(-2, 2)
                    wy = y + random.randint(-2, 2)
                    w = f"$x = {wx}; y = {wy}$"
                    if w != correct and w not in wrongs: wrongs.append(w)
                    if len(wrongs) == 6: break
                exp = "Use elimination or substitution to find the intersection of the two lines."
            else:
                x = random.randint(1, 3)
                y = random.randint(1, 3)
                q = f"Solve for $x$ and $y$: $y = x + {y-x}$ and $x^2 + y^2 = {x**2 + y**2}$"
                correct = f"$x = {x}; y = {y}$"
                wrongs = [f"$x = {x+1}; y = {y}$", f"$x = {x}; y = {y+1}$", f"$x = {-x}; y = {-y}$", f"$x = {y}; y = {x}$", f"$x = {x-1}; y = {y+1}$", f"$x = {x+2}; y = {y-1}$"]
                exp = "Substitute the linear equation into the quadratic one and solve."

        elif sub == "Complex Numbers":
            a = random.randint(1, 5)
            b = random.randint(2, 6)
            c = random.randint(1, 5)
            d = random.randint(2, 6)
            if diff == "easy":
                q = f"Simplify the complex number expression: $( {a} + {b}i ) + ( {c} - {d}i )$"
                ans_r = a + c
                ans_i = b - d
                correct = f"${ans_r} {'+' if ans_i >= 0 else '-'} {abs(ans_i)}i$"
                wrongs = [
                    f"${ans_r + 1} {'+' if ans_i >= 0 else '-'} {abs(ans_i)}i$",
                    f"${ans_r} {'+' if ans_i+1 >= 0 else '-'} {abs(ans_i+1)}i$",
                    f"${ans_r - 1} {'+' if ans_i >= 0 else '-'} {abs(ans_i)}i$",
                    f"${ans_r} {'+' if ans_i-1 >= 0 else '-'} {abs(ans_i-1)}i$",
                    f"${ans_r + 2} {'+' if ans_i >= 0 else '-'} {abs(ans_i)}i$",
                    f"${ans_r} {'+' if ans_i+2 >= 0 else '-'} {abs(ans_i+2)}i$"
                ]
                exp = f"Add real parts: ${a} + {c} = {ans_r}$. Add imaginary parts: ${b}i - {d}i = {ans_i}i$."
            elif diff == "medium":
                q = f"Multiply the complex numbers: $( {a} + {b}i )( {c} + {d}i )$"
                ans_r = a*c - b*d
                ans_i = a*d + b*c
                correct = f"${ans_r} {'+' if ans_i >= 0 else '-'} {abs(ans_i)}i$"
                wrongs = []
                for _ in range(20):
                    wr = ans_r + random.randint(-5, 5)
                    wi = ans_i + random.randint(-5, 5)
                    w = f"${wr} {'+' if wi >= 0 else '-'} {abs(wi)}i$"
                    if w != correct and w not in wrongs: wrongs.append(w)
                    if len(wrongs) == 6: break
                exp = f"Expand: $({a})({c}) + ({a})({d}i) + ({b}i)({c}) + ({b}i)({d}i)$. Note $i^2 = -1$. ${a*c} + {a*d}i + {b*c}i - {b*d} = {ans_r} + {ans_i}i$"
            else:
                q = f"Determine the modulus of the complex number $z = {a} + {b}i$"
                correct = f"$\\sqrt{{{a**2 + b**2}}}$"
                wrongs = [f"$\\sqrt{{{a**2 + b**2 + random.randint(1, 5)}}}$" for _ in range(6)]
                exp = f"Modulus $|z| = \\sqrt{{a^2 + b^2}} = \\sqrt{{{a}^2 + {b}^2}} = \\sqrt{{{a**2 + b**2}}}$"

        elif sub == "Binary Conversions":
            num = random.randint(10, 50) if diff == "easy" else random.randint(50, 150)
            if random.choice([True, False]):
                q = f"Convert the decimal number ${num}$ to binary."
                correct = bin(num)[2:]
                wrongs = [bin(num + i)[2:] for i in [-3, -2, -1, 1, 2, 3]]
                exp = "Repeatedly divide by 2 and read remainders upwards."
            else:
                b_str = bin(num)[2:]
                q = f"Convert the binary number ${b_str}_2$ to decimal."
                correct = str(num)
                wrongs = get_wrong_ints(num, 6)
                exp = "Multiply each bit by increasing powers of 2 from right to left."

        if q and correct and len(wrongs) >= 6:
            # Need to pass to TopicGenerator correctly as expected by common:
            # TopicGenerator.add_question(self, question, correct_answer, wrong_answers, explanation, difficulty=None, subtopic=None)
            # wait, TopicGenerator in generators_common might not take difficulty and subtopic in some versions. Wait, let's check it.
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                try:
                    # Maybe arguments are in different order? Let's check common logic.
                    # Usually: q, correct, wrongs, exp, sub, diff
                    gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
                except Exception as e:
                    print("Error in add_question", e)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper1_tech_algebra.json")


def gen_p1_functions():
    gen = TopicGenerator(
        "Functions & Graphs (Technical)", "FUN",
        ["Linear Graphs", "Parabolas", "Hyperbolas", "Exponential Graphs", "Circles (Semi-circles)"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Linear Graphs":
            m = random.randint(-5, 5)
            if m == 0: m = 2
            c = random.randint(-10, 10)
            q = f"Given the linear function $f(x) = {m}x {'+' if c>=0 else '-'} {abs(c)}$. Determine the $x$-intercept."
            ans = round(-c/m, 2)
            correct = str(ans)
            wrongs = get_wrong_floats(ans, 6)
            exp = f"Set $f(x) = 0 \\implies {m}x = {-c} \\implies x = {-c/m}$"

        elif sub == "Parabolas":
            a = random.choice([-2, -1, 1, 2])
            p = random.randint(-4, 4)
            q_val = random.randint(-5, 5)
            if diff == "easy":
                q = f"Given the parabola $g(x) = {a}(x - {p})^2 + {q_val}$. Write down the coordinates of the turning point."
                correct = f"$({p}; {q_val})$"
                wrongs = [f"$({-p}; {q_val})$", f"$({p}; {-q_val})$", f"$({-p}; {-q_val})$", f"$({q_val}; {p})$", f"$({-q_val}; {-p})$", f"$({p+1}; {q_val-1})$"]
                exp = f"For $y = a(x-p)^2 + q$, the turning point is $(p; q)$."
            elif diff == "medium":
                c = p**2 * a + q_val
                q = f"Determine the $y$-intercept of $g(x) = {a}(x - {p})^2 + {q_val}$."
                correct = str(c)
                wrongs = get_wrong_ints(c, 6)
                exp = f"Set $x = 0$: $g(0) = {a}(0 - {p})^2 + {q_val} = {a}({p**2}) + {q_val} = {c}$."
            else:
                q = f"Determine the maximum/minimum value of $f(x) = {a}(x - {p})^2 + {q_val}$."
                correct = f"{'Minimum' if a > 0 else 'Maximum'} value is {q_val}"
                wrongs = [
                    f"{'Maximum' if a > 0 else 'Minimum'} value is {q_val}",
                    f"{'Minimum' if a > 0 else 'Maximum'} value is {-q_val}",
                    f"{'Maximum' if a > 0 else 'Minimum'} value is {-q_val}",
                    f"{'Minimum' if a > 0 else 'Maximum'} value is {p}",
                    f"{'Maximum' if a > 0 else 'Minimum'} value is {p}",
                    f"{'Minimum' if a > 0 else 'Maximum'} value is {-p}"
                ]
                exp = f"Since $a={a}$ (which is {'positive' if a>0 else 'negative'}), the parabola opens {'upwards' if a>0 else 'downwards'}, giving a {'minimum' if a>0 else 'maximum'} value at $y = {q_val}$."

        elif sub == "Hyperbolas":
            a = random.randint(1, 5) * random.choice([1, -1])
            p = random.randint(-3, 3)
            q_val = random.randint(-4, 4)
            q = f"Given the hyperbola $h(x) = \\frac{{{a}}}{{x - {p}}} + {q_val}$. Determine the equations of the asymptotes."
            correct = f"$x = {p}$ and $y = {q_val}$"
            wrongs = [
                f"$x = {-p}$ and $y = {q_val}$",
                f"$x = {p}$ and $y = {-q_val}$",
                f"$x = {-p}$ and $y = {-q_val}$",
                f"$x = {q_val}$ and $y = {p}$",
                f"$x = {-q_val}$ and $y = {-p}$",
                f"$x = 0$ and $y = 0$"
            ]
            exp = f"Vertical asymptote where denominator is zero: $x - {p} = 0 \\implies x = {p}$. Horizontal asymptote is the constant term: $y = {q_val}$."

        elif sub == "Exponential Graphs":
            b = random.randint(2, 4)
            q_val = random.randint(-5, 5)
            q = f"Given $k(x) = {b}^x + {q_val}$. Write down the equation of the horizontal asymptote."
            correct = f"$y = {q_val}$"
            wrongs = [f"$y = {-q_val}$", f"$y = 0$", f"$x = {q_val}$", f"$x = 0$", f"$y = {b}$", f"$y = {-b}$"]
            exp = f"The horizontal asymptote is $y = q$, so $y = {q_val}$."

        elif sub == "Circles (Semi-circles)":
            r_sq = random.choice([4, 9, 16, 25, 36])
            r = int(math.sqrt(r_sq))
            q = f"Given the semi-circle function $y = \\sqrt{{{r_sq} - x^2}}$. Determine the domain."
            correct = f"${-r} \\le x \\le {r}$"
            wrongs = [
                f"${-r_sq} \\le x \\le {r_sq}$",
                f"$0 \\le x \\le {r}$",
                f"$x \\ge 0$",
                f"${-r} < x < {r}$",
                f"$-{r} \\le y \\le {r}$",
                f"$0 \\le y \\le {r}$"
            ]
            exp = f"The value inside the square root must be non-negative: ${r_sq} - x^2 \\ge 0 \\implies x^2 \\le {r_sq} \\implies {-r} \\le x \\le {r}$."

        if q and correct and len(wrongs) >= 6:
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper1_tech_functions.json")


def gen_p1_finance():
    gen = TopicGenerator(
        "Financial Mathematics (Technical)", "FIN",
        ["Interest Rates", "Depreciation", "Future Value Annuities", "Present Value Annuities"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Interest Rates":
            P = random.randint(5, 50) * 1000
            i = random.uniform(5.0, 12.0)
            n = random.randint(2, 10)
            if diff == "easy":
                q = f"Calculate the simple interest accumulated if R{P} is invested at {i:.1f}% p.a. simple interest for {n} years."
                ans = P * (i/100) * n
                correct = f"R{ans:.2f}"
                wrongs = [f"R{(ans + random.randint(100, 1000)):.2f}" for _ in range(6)]
                exp = f"$I = P \\times i \\times n = {P} \\times {i/100} \\times {n}$"
            else:
                q = f"Calculate the total amount if R{P} is invested at {i:.1f}% p.a. compounded monthly for {n} years."
                ans = P * (1 + (i/100)/12)**(n*12)
                correct = f"R{ans:.2f}"
                wrongs = [f"R{(ans * random.uniform(0.9, 1.1)):.2f}" for _ in range(6)]
                exp = f"$A = P(1 + i/m)^{{n \\times m}} = {P}(1 + {(i/100)}/12)^{{{n*12}}}$"

        elif sub == "Depreciation":
            P = random.randint(100, 500) * 1000
            i = random.uniform(8.0, 20.0)
            n = random.randint(3, 7)
            if diff == "easy":
                q = f"A machine costing R{P} depreciates on a straight-line basis at {i:.1f}% p.a. What is its book value after {n} years?"
                ans = P * (1 - (i/100) * n)
                correct = f"R{ans:.2f}"
                wrongs = [f"R{(ans * random.uniform(0.8, 1.2)):.2f}" for _ in range(6)]
                exp = f"$A = P(1 - in) = {P}(1 - {i/100} \\times {n})$"
            else:
                q = f"A vehicle costing R{P} depreciates on a reducing balance method at {i:.1f}% p.a. What is its book value after {n} years?"
                ans = P * (1 - i/100)**n
                correct = f"R{ans:.2f}"
                wrongs = [f"R{(ans * random.uniform(0.8, 1.2)):.2f}" for _ in range(6)]
                exp = f"$A = P(1 - i)^n = {P}(1 - {i/100})^{n}$"

        elif sub == "Future Value Annuities":
            x = random.randint(5, 30) * 100
            i = random.uniform(6.0, 10.0)
            n = random.randint(3, 8)
            q = f"A company deposits R{x} at the end of each month into a sinking fund. The interest rate is {i:.1f}% p.a. compounded monthly. Calculate the future value after {n} years."
            i_m = (i/100)/12
            n_m = n * 12
            ans = x * (((1 + i_m)**n_m - 1) / i_m)
            correct = f"R{ans:.2f}"
            wrongs = [f"R{(ans * random.uniform(0.8, 1.2)):.2f}" for _ in range(6)]
            exp = "Use $F = \\frac{x[(1+i)^n - 1]}{i}$ where $i$ is the monthly rate and $n$ is total months."

        elif sub == "Present Value Annuities":
            P = random.randint(100, 800) * 1000
            i = random.uniform(7.0, 12.0)
            n = random.randint(10, 20)
            q = f"A loan of R{P} is repaid with equal monthly instalments over {n} years at an interest rate of {i:.1f}% p.a. compounded monthly. Calculate the monthly instalment."
            i_m = (i/100)/12
            n_m = n * 12
            x = (P * i_m) / (1 - (1 + i_m)**(-n_m))
            correct = f"R{x:.2f}"
            wrongs = [f"R{(x * random.uniform(0.8, 1.2)):.2f}" for _ in range(6)]
            exp = "Use $P = \\frac{x[1 - (1+i)^{-n}]}{i}$ rearranged to solve for $x$."

        if q and correct and len(wrongs) >= 6:
            wrongs = list(set(wrongs))
            while len(wrongs) < 6:
                wrongs.append(f"R{(float(correct[1:]) * random.uniform(0.5, 1.5)):.2f}")
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper1_tech_finance.json")


def gen_p1_calculus():
    gen = TopicGenerator(
        "Differential Calculus & Integration", "CALC",
        ["Limits", "First Principles", "Differentiation Rules", "Tangents & Turning Points", "Integration"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 60000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break
        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)
        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Limits":
            if diff == "easy":
                a = random.randint(1, 9)
                b = random.randint(-15, 15)
                c = random.randint(-5, 5)
                val = a * c + b
                q = f"Evaluate the limit: $\\lim_{{x \\to {c}}} ({a}x {b:+d})$"
                correct = str(val)
                wrongs = get_wrong_ints(val, 8)
                exp = f"Substitute $x={c}$: ${a}({c}) {b:+d} = {val}$."
            elif diff == "medium":
                l_type = random.choice([1, 2, 3])
                if l_type == 1:
                    c = random.randint(-15, 15)
                    if c == 0: c = 2
                    q = f"Evaluate the limit: $\\lim_{{x \\to {c}}} \\frac{{x^2 - {c**2}}}{{x - {c}}}$"
                    val = 2 * c
                    correct = str(val)
                    wrongs = get_wrong_ints(val, 8)
                    exp = f"Factorise: $\\lim_{{x \\to {c}}} (x + {c}) = {val}$."
                elif l_type == 2:
                    a = random.randint(1, 9)
                    b = random.randint(-20, 20)
                    if b == 0: b = 3
                    q = f"Evaluate the limit: $\\lim_{{x \\to 0}} \\frac{{{a}x^2 {b:+d}x}}{{x}}$"
                    val = b
                    correct = str(val)
                    wrongs = get_wrong_ints(val, 8)
                    exp = f"Factorise $x$: $\\lim_{{x \\to 0}} ({a}x {b:+d}) = {val}$."
                else:
                    a = random.randint(1, 4)
                    b = random.randint(-5, 5)
                    c = random.randint(-3, 3)
                    d = random.randint(-10, 10)
                    val = a*(c**2) + b*c + d
                    q = f"Evaluate the limit: $\\lim_{{x \\to {c}}} ({a}x^2 {b:+d}x {d:+d})$"
                    correct = str(val)
                    wrongs = get_wrong_ints(val, 8)
                    exp = f"Substitute $x={c}$: {val}."
            else: # hard
                a = random.randint(1, 8)
                b = random.randint(1, 8)
                c = random.randint(1, 5)
                q = f"Evaluate the limit: $\\lim_{{x \\to {c}}} \\frac{{x^2 {a-c:+d}x - {a*c}}}{{x - {c}}}$"
                val = c + a
                correct = str(val)
                wrongs = get_wrong_ints(val, 8)
                exp = f"Factorise into $(x-{c})(x+{a})/(x-{c}) = x + {a} \\to {c} + {a} = {val}$."

        elif sub == "First Principles":
            if diff == "easy":
                m = random.choice([2, 3, 4, 5, 6, 7, 8, 9, -2, -3, -4, -5])
                c_val = random.randint(-10, 10)
                q = f"Use first principles to find $f'(x)$ for $f(x) = {m}x {c_val:+d}$."
                correct = str(m)
                wrongs = get_wrong_ints(m, 8)
                exp = f"Derivative is {m}."
            elif diff == "medium":
                a = random.randint(-10, 10)
                if a == 0: a = 2
                b = random.randint(-20, 20)
                q = f"Use first principles to determine the derivative of $f(x) = {a}x^2 {b:+d}$."
                correct = f"${2*a}x$"
                wrongs = [f"${a}x$", f"${2*a}x^2$", f"${a}x^2$", f"${2*a}$", f"${a}$", f"${-2*a}x$", f"${4*a}x$", f"${2*a}x^3$"]
                exp = f"Derivative of ${a}x^2 {b:+d}$ is ${2*a}x$."
            else: # hard
                a = random.choice([2, 3, 4, -2, -3])
                b = random.choice([1, 2, 3, 4, 5, -1, -2, -3, -4])
                q = f"Determine the derivative of $f(x) = {a}x^2 {b:+d}x$ from first principles."
                correct = f"${2*a}x {b:+d}$"
                wrongs = [f"${2*a}x - {b}$", f"${a}x {b:+d}$", f"${2*a}x^2 {b:+d}$", f"${2*a}x$", f"${a*2}x {b*2:+d}$", f"${2*a+1}x {b:+d}$", f"${2*a}x {b-1:+d}$", f"${2*a}x {b+1:+d}$"]
                exp = f"$f'(x) = {2*a}x {b:+d}$."

        elif sub == "Differentiation Rules":
            if diff == "easy":
                a = random.randint(2, 9)
                n = random.randint(2, 6)
                q = f"Determine $\\frac{{dy}}{{dx}}$ if $y = {a}x^{{{n}}}$."
                correct = f"${a*n}x^{{{n-1}}}$"
                wrongs = [f"${a*n}x^{{{n}}}$", f"${a}x^{{{n-1}}}$", f"${a*n}x^{{{n+1}}}$", f"${a*n*2}x^{{{n-1}}}$", f"${a*n}x$", f"${a}x^{{{n-2}}}$", f"${a*n+1}x^{{{n-1}}}$", f"${a*n-1}x^{{{n-1}}}$"]
                exp = f"Power rule: {a*n}x^{n-1}."
            elif diff == "medium":
                m_type = random.choice([1, 2])
                if m_type == 1:
                    a = random.randint(2, 8)
                    n = random.randint(2, 5)
                    c_val = random.randint(1, 9)
                    q = f"Differentiate $y = {a}x^{{{n}}} + \\frac{{{c_val}}}{{x}}$ with respect to $x$."
                    correct = f"${a*n}x^{{{n-1}}} - \\frac{{{c_val}}}{{x^2}}$"
                    wrongs = [
                        f"${a*n}x^{{{n-1}}} + \\frac{{{c_val}}}{{x^2}}$",
                        f"${a*n}x^{{{n}}} - \\frac{{{c_val}}}{{x^2}}$",
                        f"${a}x^{{{n-1}}} - \\frac{{{c_val}}}{{x^2}}$",
                        f"${a*n}x^{{{n-1}}} - {c_val}x$",
                        f"${a*n}x^{{{n-1}}} + {c_val}\\ln x$",
                        f"${a*n}x^{{{n+1}}} - \\frac{{{c_val}}}{{x^2}}$",
                        f"${a*n}x^{{{n-1}}} - \\frac{{{c_val*2}}}{{x^2}}$",
                        f"${a*n*2}x^{{{n-1}}} - \\frac{{{c_val}}}{{x^2}}$"
                    ]
                    exp = f"Derivative is {a*n}x^{n-1} - {c_val}/x^2."
                else:
                    a = random.randint(2, 6)
                    b = random.randint(2, 6)
                    n = random.randint(2, 5)
                    m = random.randint(2, 4)
                    if n == m: m = n + 1
                    q = f"Determine $\\frac{{dy}}{{dx}}$ if $y = {a}x^{{{n}}} + {b}x^{{{m}}}$."
                    correct = f"${a*n}x^{{{n-1}}} + {b*m}x^{{{m-1}}}$"
                    wrongs = [
                        f"${a*n}x^{{{n}}} + {b*m}x^{{{m}}}$",
                        f"${a}x^{{{n-1}}} + {b}x^{{{m-1}}}$",
                        f"${a*n}x^{{{n-1}}} - {b*m}x^{{{m-1}}}$",
                        f"${a*n*2}x^{{{n-1}}} + {b*m}x^{{{m-1}}}$",
                        f"${a*n}x^{{{n+1}}} + {b*m}x^{{{m+1}}}$",
                        f"${a*n}x^{{{n-1}}} + {b}x^{{{m}}}$",
                        f"${a}x^{{{n}}} + {b*m}x^{{{m-1}}}$",
                        f"${a*n+1}x^{{{n-1}}} + {b*m}x^{{{m-1}}}$"
                    ]
                    exp = f"Differentiate term-by-term."
            else: # hard
                a = random.randint(2, 6)
                b = random.randint(1, 8)
                q = f"Determine $\\frac{{dy}}{{dx}}$ if $y = \\sqrt{{{a}x}} + {b}x^{{-2}}$."
                correct = f"$\\frac{{\\sqrt{{{a}}}}}{{2\\sqrt{{x}}}} - {2*b}x^{{-3}}$"
                wrongs = [
                    f"$\\frac{{\\sqrt{{{a}}}}}{{2\\sqrt{{x}}}} + {2*b}x^{{-3}}$",
                    f"$\\frac{{{a}}}{{2\\sqrt{{x}}}} - {2*b}x^{{-3}}$",
                    f"$\\frac{{\\sqrt{{{a}}}}}{{\\sqrt{{x}}}} - {2*b}x^{{-3}}$",
                    f"$\\frac{{\\sqrt{{{a}}}}}{{2\\sqrt{{x}}}} - {b}x^{{-3}}$",
                    f"$\\frac{{\\sqrt{{{a}}}}}{{2\\sqrt{{x}}}} - {2*b}x^{{-1}}$",
                    f"$\\frac{{\\sqrt{{{a}}}}}{{2x}} - {2*b}x^{{-3}}$",
                    f"$\\sqrt{{{a}x}} - {2*b}x^{{-3}}$",
                    f"$\\frac{{1}}{{2\\sqrt{{{a}x}}}} - {2*b}x^{{-3}}$"
                ]
                exp = f"Derivative is \\frac{{\\sqrt{{{a}}}}}{{2\\sqrt{{x}}}} - {2*b}x^{{-3}}."

        elif sub == "Tangents & Turning Points":
            if diff == "easy":
                m = random.choice([2, 3, 4, 5, -2, -3, -4, -5])
                q = f"Determine the gradient of the tangent to the curve where $\\frac{{dy}}{{dx}} = {m}$."
                correct = str(m)
                wrongs = get_wrong_ints(m, 8)
                exp = f"Gradient $m = {m}$."
            elif diff == "medium":
                a = random.choice([1, 2, 3])
                b = random.choice([-6, -4, -2, 2, 4, 6])
                x0 = random.randint(-5, 5)
                m = 2 * a * x0 + b
                q = f"Determine the gradient of the tangent to the parabola $y = {a}x^2 {b:+d}x$ at $x = {x0}$."
                correct = str(m)
                wrongs = get_wrong_ints(m, 8)
                exp = f"Gradient $m = {m}$."
            else: # hard
                k = random.choice([1, 2, 3, 4, 5, 6])
                c_val = random.randint(-20, 20)
                q = f"Find the $x$-coordinates of the stationary points of $f(x) = x^3 - {3*k**2}x {c_val:+d}$."
                correct = f"$x = {k}$ and $x = {-k}$"
                wrongs = [
                    f"$x = {k+1}$ and $x = {-k-1}$",
                    f"$x = {k}$ and $x = 0$",
                    f"$x = {-k}$ and $x = 0$",
                    f"$x = {k**2}$ and $x = {-k**2}$",
                    f"$x = {3*k}$ and $x = {-3*k}$",
                    f"$x = {k*2}$ and $x = {-k*2}$",
                    f"$x = 1$ and $x = -1$",
                    f"$x = {k+2}$ and $x = {-k+2}$"
                ]
                exp = f"Stationary points: x = {k} and x = {-k}."

        elif sub == "Integration":
            if diff == "easy":
                a = random.randint(2, 9)
                n = random.randint(2, 5)
                n1 = n + 1
                q = f"Determine the indefinite integral: $\\int {a*n1}x^{{{n}}} dx$."
                correct = f"${a}x^{{{n1}}} + C$"
                wrongs = [f"${a*n1}x^{{{n1}}} + C$", f"${a}x^{{{n}}} + C$", f"${a*n}x^{{{n-1}}} + C$", f"${a*2}x^{{{n1}}} + C$", f"${a}x^{{{n1}}}$", f"${a*n1}x^{{{n-1}}} + C$", f"${a+1}x^{{{n1}}} + C$", f"${a-1}x^{{{n1}}} + C$"]
                exp = f"Integral is {a}x^{n1} + C."
            elif diff == "medium":
                m_int_type = random.choice([1, 2])
                if m_int_type == 1:
                    k = random.randint(2, 25)
                    q = f"Determine the integral: $\\int \\frac{{{k}}}{{x}} dx$."
                    correct = f"${k}\\ln|x| + C$"
                    wrongs = [
                        f"$\\frac{{{k}}}{{x^2}} + C$",
                        f"${k}x + C$",
                        f"$-{k}x^{{-2}} + C$",
                        f"$\\frac{{{k}}}{{2}}x^2 + C$",
                        f"${k}\\ln(x)$",
                        f"$-{k}\\ln|x| + C$",
                        f"$\\frac{{{1}}}{{{k}}}\\ln|x| + C$",
                        f"${k+1}\\ln|x| + C$"
                    ]
                    exp = f"Integral is {k}ln|x| + C."
                else:
                    a = random.choice([2, 4, 6])
                    b = random.randint(1, 10)
                    q = f"Determine the indefinite integral: $\\int ({a}x {b:+d}) dx$."
                    correct = f"${a//2}x^2 {b:+d}x + C$"
                    wrongs = [
                        f"${a}x^2 {b:+d}x + C$",
                        f"${a//2}x^2 {b:+d} + C$",
                        f"${a*2}x^2 {b:+d}x + C$",
                        f"${a//2}x^2 - {b}x + C$",
                        f"${a//2}x^2 + C$",
                        f"${a}x + {b} + C$",
                        f"${a//2}x^3 {b:+d}x + C$",
                        f"${a+1}x^2 {b:+d}x + C$"
                    ]
                    exp = f"Integral is {a//2}x^2 {b:+d}x + C."
            else: # hard
                a = random.choice([2, 4, 6, 8])
                b = random.randint(1, 6)
                val = int((a // 2) * (b ** 2))
                q = f"Evaluate the definite integral: $\\int_{{0}}^{{{b}}} {a}x \\, dx$."
                correct = str(val)
                wrongs = get_wrong_ints(val, 8)
                exp = f"Definite integral value is {val}."

        if q and correct and len(wrongs) >= 6:
            gen.add_question(sub, diff, q, correct, wrongs[:8], exp)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper1_tech_calculus.json")


# --- PAPER 2 GENERATORS ---

def gen_p2_analytical():
    gen = TopicGenerator(
        "Analytical Geometry (Technical)", "ANALYT",
        ["Distance", "Midpoint", "Gradient & Inclination", "Equation of a Line", "Circles"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
        x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
        if x1 == x2 and y1 == y2: x2 += 1
        if x1 == x2: x2 += 1

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Distance":
            q = f"Determine the distance between $A({x1}; {y1})$ and $B({x2}; {y2})$. (Leave answer in surd form if necessary)"
            dist_sq = (x2-x1)**2 + (y2-y1)**2
            correct = f"$\\sqrt{{{dist_sq}}}$"
            wrongs = [f"$\\sqrt{{{dist_sq + random.randint(1, 10)}}}$" for _ in range(6)]
            exp = f"$d = \\sqrt{{(x_2-x_1)^2 + (y_2-y_1)^2}} = \\sqrt{{({x2}-({x1}))^2 + ({y2}-({y1}))^2}} = \\sqrt{{{dist_sq}}}$"

        elif sub == "Midpoint":
            q = f"Determine the coordinates of the midpoint of the line segment joining $C({x1}; {y1})$ and $D({x2}; {y2})$."
            mx, my = (x1+x2)/2, (y1+y2)/2
            correct = f"$({mx:g}; {my:g})$"
            wrongs = [
                f"$({(x1-x2)/2:g}; {(y1-y2)/2:g})$",
                f"$({mx+1:g}; {my:g})$",
                f"$({mx:g}; {my-1:g})$",
                f"$({my:g}; {mx:g})$",
                f"$({(x2-x1)/2:g}; {(y2-y1)/2:g})$",
                f"$({mx*2:g}; {my*2:g})$"
            ]
            exp = f"$M(\\frac{{x_1+x_2}}{{2}}; \\frac{{y_1+y_2}}{{2}}) = M(\\frac{{{x1}+{x2}}}{{2}}; \\frac{{{y1}+{y2}}}{{2}})$"

        elif sub == "Gradient & Inclination":
            q = f"Determine the gradient of the line passing through $E({x1}; {y1})$ and $F({x2}; {y2})$."
            dy, dx = y2-y1, x2-x1
            m = dy/dx
            correct = f"${m:g}$" if m.is_integer() else f"${dy}/{dx}$"
            wrongs = [f"${dx}/{dy}$" if dy!=0 else "Undefined", f"${-m:g}$", f"${m+1:g}$", f"${(y2+y1)/(x2+x1) if x2+x1!=0 else 0:g}$", f"${m-1:g}$", f"${m*2:g}$"]
            exp = f"$m = \\frac{{y_2-y_1}}{{x_2-x_1}} = \\frac{{{y2}-({y1})}}{{{x2}-({x1})}}$"

        elif sub == "Equation of a Line":
            m_int = random.randint(-4, 4)
            if m_int == 0: m_int = 2
            c_int = y1 - m_int*x1
            q = f"Determine the equation of the line passing through $G({x1}; {y1})$ with a gradient of ${m_int}$."
            correct = f"$y = {m_int}x {'+' if c_int>=0 else '-'} {abs(c_int)}$"
            wrongs = [
                f"$y = {m_int}x {'+' if c_int-1>=0 else '-'} {abs(c_int-1)}$",
                f"$y = {-m_int}x {'+' if c_int>=0 else '-'} {abs(c_int)}$",
                f"$y = {c_int}x {'+' if m_int>=0 else '-'} {abs(m_int)}$",
                f"$y = {m_int}x {'+' if c_int+2>=0 else '-'} {abs(c_int+2)}$",
                f"$x = {m_int}y {'+' if c_int>=0 else '-'} {abs(c_int)}$",
                f"$y = {m_int}x$"
            ]
            exp = f"Use $y - y_1 = m(x - x_1) \\implies y - {y1} = {m_int}(x - {x1})$."

        elif sub == "Circles":
            r_sq = random.choice([9, 16, 25, 36, 49])
            q = f"Give the radius of the circle defined by $x^2 + y^2 = {r_sq}$."
            r = int(math.sqrt(r_sq))
            correct = str(r)
            wrongs = get_wrong_ints(r, 6)
            exp = f"Equation of circle at origin is $x^2 + y^2 = r^2$, so $r = \\sqrt{{{r_sq}}} = {r}$."

        if q and correct and len(wrongs) >= 6:
            wrongs = list(set(wrongs))
            while len(wrongs) < 6: wrongs.append(f"Rand{random.randint(100, 999)}")
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper2_tech_analytical.json")


def gen_p2_trig():
    gen = TopicGenerator(
        "Trigonometry (Technical)", "TRIG",
        ["Identities", "Reduction Formulae", "Solving Equations", "2D/3D Problems"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 60000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break
        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)
        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Identities":
            var = random.choice(["x", "\\theta", "\\alpha", "\\beta", "A", "B"])
            if diff == "easy":
                id_type = random.choice([1, 2, 3, 4, 5, 6])
                if id_type == 1:
                    q = f"Which of the following is equivalent to $\\sec {var}$?"
                    correct = f"$\\frac{{1}}{{\\cos {var}}}$"
                    wrongs = [f"$\\frac{{1}}{{\\sin {var}}}$", f"$\\frac{{1}}{{\\tan {var}}}$", f"$\\cos {var}$", f"$\\frac{{\\sin {var}}}{{\\cos {var}}}$", f"$1 - \\cos {var}$", f"$\\frac{{1}}{{\\cot {var}}}$", f"$\\tan^2 {var}$", f"$-\\cos {var}$"]
                    exp = f"By definition, secant is the reciprocal of cosine: $\\sec {var} = \\frac{{1}}{{\\cos {var}}}$."
                elif id_type == 2:
                    q = f"Which of the following is equivalent to $\\csc {var}$?"
                    correct = f"$\\frac{{1}}{{\\sin {var}}}$"
                    wrongs = [f"$\\frac{{1}}{{\\cos {var}}}$", f"$\\frac{{1}}{{\\tan {var}}}$", f"$\\sin {var}$", f"$\\frac{{\\cos {var}}}{{\\sin {var}}}$", f"$1 - \\sin {var}$", f"$\\frac{{1}}{{\\sec {var}}}$", f"$\\cot^2 {var}$", f"$-\\sin {var}$"]
                    exp = f"Cosecant is the reciprocal of sine: $\\csc {var} = \\frac{{1}}{{\\sin {var}}}$."
                elif id_type == 3:
                    q = f"Which of the following is equivalent to $\\cot {var}$?"
                    correct = f"$\\frac{{1}}{{\\tan {var}}}$"
                    wrongs = [f"$\\frac{{1}}{{\\sin {var}}}$", f"$\\frac{{1}}{{\\cos {var}}}$", f"$\\tan {var}$", f"$\\sin {var} \\cos {var}$", f"$1 + \\tan {var}$", f"$\\sec {var}$", f"$\\csc {var}$", f"$-\\tan {var}$"]
                    exp = f"Cotangent is the reciprocal of tangent: $\\cot {var} = \\frac{{1}}{{\\tan {var}}}$."
                elif id_type == 4:
                    q = f"Simplify the trigonometric expression: $\\sin^2 {var} + \\cos^2 {var}$."
                    correct = "$1$"
                    wrongs = ["$0$", "$2$", "$\\tan {var}$", "$\\sec {var}$", "$-1$", "$\\sin {var}$", "$\\cos {var}$", "$2\\sin {var}$"]
                    exp = "The fundamental Pythagorean identity states $\\sin^2 \\theta + \\cos^2 \\theta = 1$."
                elif id_type == 5:
                    q = f"Simplify: $\\tan {var} \\cdot \\cot {var}$."
                    correct = "$1$"
                    wrongs = ["$0$", "$\\tan^2 {var}$", "$\\cot^2 {var}$", "$-1$", "$\\sec {var}$", "$\\sin {var}$", "$2$", "$\\cos {var}$"]
                    exp = f"$\\tan {var} \\cdot \\cot {var} = \\tan {var} \\cdot \\frac{{1}}{{\\tan {var}}} = 1$."
                else:
                    q = f"Simplify: $\\cos {var} \\cdot \\sec {var}$."
                    correct = "$1$"
                    wrongs = ["$0$", "$\\cos^2 {var}$", "$\\sec^2 {var}$", "$-1$", "$\\sin {var}$", "$\\tan {var}$", "$2$", "$\\csc {var}$"]
                    exp = f"$\\cos {var} \\cdot \\sec {var} = \\cos {var} \\cdot \\frac{{1}}{{\\cos {var}}} = 1$."
            elif diff == "medium":
                m_type = random.choice([1, 2, 3, 4, 5])
                if m_type == 1:
                    q = f"Simplify the expression: $\\frac{{\\sin {var}}}{{\\cos {var}}} \\cdot \\cos {var}$."
                    correct = f"$\\sin {var}$"
                    wrongs = [f"$\\cos {var}$", "$1$", f"$\\tan {var}$", f"$\\sec {var}$", f"$\\cot {var}$", f"$\\sin^2 {var}$", f"$\\csc {var}$", "$0$"]
                    exp = f"$\\frac{{\\sin {var}}}{{\\cos {var}}} \\cdot \\cos {var} = \\sin {var}$."
                elif m_type == 2:
                    q = f"Simplify: $1 - \\cos^2 {var}$."
                    correct = f"$\\sin^2 {var}$"
                    wrongs = [f"$\\cos^2 {var}$", f"$\\sin {var}$", "$1$", f"-\\sin^2 {var}", f"$\\tan^2 {var}$", f"$\\sec^2 {var}$", "$0$", f"$1 + \\cos {var}$"]
                    exp = f"From $\\sin^2 {var} + \\cos^2 {var} = 1$, $1 - \\cos^2 {var} = \\sin^2 {var}$."
                elif m_type == 3:
                    q = f"Simplify: $\\sec^2 {var} - \\tan^2 {var}$."
                    correct = "$1$"
                    wrongs = ["$0$", "$-1$", f"$\\sec^2 {var}$", f"$\\tan^2 {var}$", f"$\\sin^2 {var}$", "$2$", f"$\\cos^2 {var}$", f"$\\cot^2 {var}$"]
                    exp = f"Identity $1 + \\tan^2 {var} = \\sec^2 {var} \\implies \\sec^2 {var} - \\tan^2 {var} = 1$."
                elif m_type == 4:
                    q = f"Simplify: $(1 - \\sin {var})(1 + \\sin {var})$."
                    correct = f"$\\cos^2 {var}$"
                    wrongs = [f"$\\sin^2 {var}$", f"$1 - \\sin {var}$", "$1$", f"$-\\cos^2 {var}$", f"$\\cos {var}$", f"$\\tan^2 {var}$", "$0$", f"$\\sec^2 {var}$"]
                    exp = f"$(1 - \\sin {var})(1 + \\sin {var}) = 1 - \\sin^2 {var} = \\cos^2 {var}$."
                else:
                    q = f"Simplify: $\\frac{{\\tan {var}}}{{\\sec {var}}}$."
                    correct = f"$\\sin {var}$"
                    wrongs = [f"$\\cos {var}$", f"$\\cot {var}$", "$1$", f"$\\csc {var}$", f"$\\sin^2 {var}$", f"$\\tan^2 {var}$", "$0$", f"$\\sec {var}$"]
                    exp = f"$\\frac{{\\tan {var}}}{{\\sec {var}}} = \\frac{{\\sin {var}/\\cos {var}}}{{1/\\cos {var}}} = \\sin {var}$."
            else: # hard
                q = f"Simplify: $\\frac{{1 - \\cos^2 {var}}}{{\\sin {var}}}$."
                correct = f"$\\sin {var}$"
                wrongs = [f"$\\cos {var}$", "$1$", f"$\\sin^2 {var}$", f"$\\tan {var}$", f"$\\csc {var}$", f"-\\sin {var}", "$0$", f"$\\sec {var}$"]
                exp = f"$\\frac{{1 - \\cos^2 {var}}}{{\\sin {var}}} = \\frac{{\\sin^2 {var}}}{{\\sin {var}}} = \\sin {var}$."

        elif sub == "Reduction Formulae":
            var = "\\theta"
            if diff == "easy":
                r_type = random.choice([1, 2, 3, 4, 5, 6])
                if r_type == 1:
                    q = f"Reduce to a single ratio: $\\sin(180^\\circ - {var})$."
                    correct = f"$\\sin {var}$"
                    wrongs = [f"$-\\sin {var}$", f"$\\cos {var}$", f"$-\\cos {var}$", f"$\\tan {var}$", f"$1$", f"$0$", f"$\\csc {var}$", f"-\\tan {var}"]
                    exp = f"In the second quadrant, sine is positive: $\\sin(180^\\circ - {var}) = \\sin {var}$."
                elif r_type == 2:
                    q = f"Reduce to a single ratio: $\\cos(180^\\circ - {var})$."
                    correct = f"$-\\cos {var}$"
                    wrongs = [f"$\\cos {var}$", f"$\\sin {var}$", f"$-\\sin {var}$", f"$\\tan {var}$", f"$1$", f"$-1$", f"$\\sec {var}$", f"-\\sec {var}"]
                    exp = f"In the second quadrant, cosine is negative: $\\cos(180^\\circ - {var}) = -\\cos {var}$."
                elif r_type == 3:
                    q = f"Reduce to a single ratio: $\\tan(180^\\circ + {var})$."
                    correct = f"$\\tan {var}$"
                    wrongs = [f"$-\\tan {var}$", f"$\\cot {var}$", f"$-\\cot {var}$", f"$\\sin {var}$", f"$\\cos {var}$", f"$1$", f"$0$", f"-\\sin {var}"]
                    exp = f"In the third quadrant, tangent is positive: $\\tan(180^\\circ + {var}) = \\tan {var}$."
                elif r_type == 4:
                    q = f"Reduce to a single ratio: $\\cos(360^\\circ - {var})$."
                    correct = f"$\\cos {var}$"
                    wrongs = [f"$-\\cos {var}$", f"$\\sin {var}$", f"$-\\sin {var}$", f"$\\tan {var}$", f"$1$", f"$-1$", f"$\\sec {var}$", f"-\\tan {var}"]
                    exp = f"In the fourth quadrant, cosine is positive: $\\cos(360^\\circ - {var}) = \\cos {var}$."
                elif r_type == 5:
                    q = f"Simplify the negative angle: $\\sin(-{var})$."
                    correct = f"$-\\sin {var}$"
                    wrongs = [f"$\\sin {var}$", f"$\\cos {var}$", f"$-\\cos {var}$", f"$\\tan {var}$", f"$1$", f"$-1$", f"$\\csc {var}$", f"-\\csc {var}"]
                    exp = f"Sine is an odd function: $\\sin(-{var}) = -\\sin {var}$."
                else:
                    q = f"Simplify the negative angle: $\\cos(-{var})$."
                    correct = f"$\\cos {var}$"
                    wrongs = [f"$-\\cos {var}$", f"$\\sin {var}$", f"$-\\sin {var}$", f"$\\tan {var}$", f"$1$", f"$-1$", f"$\\sec {var}$", f"-\\sec {var}"]
                    exp = f"Cosine is an even function: $\\cos(-{var}) = \\cos {var}$."
            elif diff == "medium":
                angle = random.choice([120, 135, 150, 210, 225, 240, 300, 315, 330])
                fn = random.choice(["sin", "cos", "tan"])
                if fn == "sin":
                    rad = math.radians(angle)
                    val = round(math.sin(rad), 3)
                elif fn == "cos":
                    rad = math.radians(angle)
                    val = round(math.cos(rad), 3)
                else:
                    rad = math.radians(angle)
                    val = round(math.tan(rad), 3)
                q = f"Determine the exact value of $\\{fn}({angle}^\\circ)$ (to 3 decimal places)."
                correct = f"{val:.3f}"
                wrongs = [f"{(val + offset):.3f}" for offset in [0.2, -0.2, 0.5, -0.5, 0.866, -0.866, 0.707, -0.707] if round(val+offset, 3) != val][:8]
                while len(wrongs) < 6: wrongs.append(f"{val + random.uniform(0.1, 0.9):.3f}")
                exp = f"Reduce ${angle}^\\circ$ using CAST diagram to find reference angle."
            else: # hard
                angle = random.choice([120, 150, 210, 240, 300, 330])
                q = f"Simplify: $\\frac{{\\sin(180^\\circ - {var}) \\cdot \\cos({angle}^\\circ)}}{{\\sin {var}}}$."
                val = round(math.cos(math.radians(angle)), 3)
                correct = f"{val:.3f}"
                wrongs = [f"{(val + off):.3f}" for off in [0.5, -0.5, 1.0, -1.0, 0.866, -0.866, 0.707, -0.707] if round(val+off, 3) != val][:8]
                while len(wrongs) < 6: wrongs.append(f"{val + random.uniform(0.1, 0.9):.3f}")
                exp = f"$\\sin(180^\\circ - {var}) = \\sin {var}$, which cancels with denominator, leaving $\\cos({angle}^\\circ) = {val:.3f}$."

        elif sub == "Solving Equations":
            if diff == "easy":
                fn = random.choice(["sin", "cos", "tan"])
                if fn == "sin":
                    q = "Solve for $\\theta \\in [0^\\circ, 90^\\circ]$: $\\sin \\theta = 0.5$."
                    correct = "$30^\\circ$"
                    wrongs = ["$45^\\circ$", "$60^\\circ$", "$90^\\circ$", "$15^\\circ$", "$75^\\circ$", "$120^\\circ$", "$150^\\circ$", "$0^\\circ$"]
                    exp = "$\\sin^{-1}(0.5) = 30^\\circ$."
                elif fn == "cos":
                    q = "Solve for $\\theta \\in [0^\\circ, 90^\\circ]$: $\\cos \\theta = 0.5$."
                    correct = "$60^\\circ$"
                    wrongs = ["$30^\\circ$", "$45^\\circ$", "$90^\\circ$", "$15^\\circ$", "$75^\\circ$", "$120^\\circ$", "$150^\\circ$", "$0^\\circ$"]
                    exp = "$\\cos^{-1}(0.5) = 60^\\circ$."
                else:
                    q = "Solve for $\\theta \\in [0^\\circ, 90^\\circ]$: $\\tan \\theta = 1$."
                    correct = "$45^\\circ$"
                    wrongs = ["$30^\\circ$", "$60^\\circ$", "$90^\\circ$", "$15^\\circ$", "$75^\\circ$", "$120^\\circ$", "$135^\\circ$", "$0^\\circ$"]
                    exp = "$\\tan^{-1}(1) = 45^\\circ$."
            elif diff == "medium":
                c_val = random.randint(2, 6)
                ans = round(math.degrees(math.asin(1.0 / c_val)), 1)
                q = f"Solve for $\\theta \\in [0^\\circ, 90^\\circ]$: ${c_val}\\sin \\theta = 1$."
                correct = f"{ans}^\\circ"
                wrongs = [f"{round(ans + off, 1)}^\\circ" for off in [10, -10, 15, -15, 20, -20, 25, 30] if round(ans+off, 1) != ans][:8]
                while len(wrongs) < 6: wrongs.append(f"{ans + random.randint(5, 40):.1f}^\\circ")
                exp = f"$\\sin \\theta = \\frac{{1}}{{{c_val}}} \\implies \\theta = \\sin^{{-1}}(1/{c_val}) = {ans}^\\circ$."
            else: # hard
                ans = random.choice([15.0, 22.5, 30.0, 45.0, 60.0])
                if ans == 15.0:
                    q = "Solve for $\\theta \\in [0^\\circ, 90^\\circ]$: $\\sin(2\\theta) = 0.5$."
                    correct = "$15^\\circ$"
                    wrongs = ["$30^\\circ$", "$45^\\circ$", "$60^\\circ$", "$10^\\circ$", "$20^\\circ$", "$25^\\circ$", "$75^\\circ$", "$90^\\circ$"]
                    exp = "$2\\theta = 30^\\circ \\implies \\theta = 15^\\circ$."
                elif ans == 30.0:
                    q = "Solve for $\\theta \\in [0^\\circ, 90^\\circ]$: $\\cos(2\\theta) = 0.5$."
                    correct = "$30^\\circ$"
                    wrongs = ["$15^\\circ$", "$45^\\circ$", "$60^\\circ$", "$20^\\circ$", "$25^\\circ$", "$50^\\circ$", "$75^\\circ$", "$90^\\circ$"]
                    exp = "$2\\theta = 60^\\circ \\implies \\theta = 30^\\circ$."
                else:
                    q = "Solve for $\\theta \\in [0^\\circ, 90^\\circ]$: $\\tan(2\\theta) = 1$."
                    correct = "$22.5^\\circ$"
                    wrongs = ["$45^\\circ$", "$30^\\circ$", "$15^\\circ$", "$20^\\circ$", "$25^\\circ$", "$35^\\circ$", "$40^\\circ$", "$12.5^\\circ$"]
                    exp = "$2\\theta = 45^\\circ \\implies \\theta = 22.5^\\circ$."

        elif sub == "2D/3D Problems":
            a = random.randint(4, 30)
            b = random.randint(4, 30)
            if diff == "easy":
                angle = random.choice([30, 90, 150])
                sin_val = math.sin(math.radians(angle))
                area = round(0.5 * a * b * sin_val, 2)
                q = f"In $\\Delta ABC$, $a = {a}$ cm, $b = {b}$ cm and $\\angle C = {angle}^\\circ$. Calculate the area of $\\Delta ABC$."
                correct = f"{area:.2f} cm²"
                wrongs = [f"{(area * m):.2f} cm²" for m in [0.5, 1.5, 0.8, 1.2, 2.0, 0.7, 1.3, 1.8] if round(area*m, 2) != area][:8]
                while len(wrongs) < 6: wrongs.append(f"{area + random.randint(5, 50):.2f} cm²")
                exp = f"Area = $\\frac{{1}}{{2}}ab\\sin C = 0.5 \\times {a} \\times {b} \\times \\sin({angle}^\\circ) = {area:.2f}$ cm²."
            elif diff == "medium":
                angle = random.choice([45, 60, 120, 135])
                sin_val = math.sin(math.radians(angle))
                area = round(0.5 * a * b * sin_val, 2)
                q = f"In $\\Delta PQR$, $p = {a}$ m, $q = {b}$ m and $\\angle R = {angle}^\\circ$. Calculate the area of the triangle."
                correct = f"{area:.2f} m²"
                wrongs = [f"{(area * m):.2f} m²" for m in [0.5, 1.5, 0.8, 1.2, 2.0, 0.7, 1.3, 1.8] if round(area*m, 2) != area][:8]
                while len(wrongs) < 6: wrongs.append(f"{area + random.randint(5, 50):.2f} m²")
                exp = f"Area = $\\frac{{1}}{{2}}pq\\sin R = 0.5 \\times {a} \\times {b} \\times \\sin({angle}^\\circ) = {area:.2f}$ m²."
            else: # hard (cosine rule)
                angle = random.choice([60, 90, 120])
                cos_val = math.cos(math.radians(angle))
                c_sq = a**2 + b**2 - 2 * a * b * cos_val
                c_len = round(math.sqrt(c_sq), 2)
                q = f"In $\\Delta ABC$, $a = {a}$ cm, $b = {b}$ cm and $\\angle C = {angle}^\\circ$. Calculate the length of side $c$ using the Cosine Rule."
                correct = f"{c_len:.2f} cm"
                wrongs = [f"{(c_len * m):.2f} cm" for m in [0.8, 1.2, 0.9, 1.1, 1.5, 0.7, 1.3, 0.6] if round(c_len*m, 2) != c_len][:8]
                while len(wrongs) < 6: wrongs.append(f"{c_len + random.randint(2, 20):.2f} cm")
                exp = f"$c^2 = a^2 + b^2 - 2ab\\cos C = {a}^2 + {b}^2 - 2({a})({b})\\cos({angle}^\\circ) = {c_sq:.2f} \\implies c = {c_len:.2f}$ cm."

        if q and correct and len(wrongs) >= 6:
            gen.add_question(sub, diff, q, correct, wrongs[:8], exp)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper2_tech_trig.json")


def gen_p2_circle_angular():
    gen = TopicGenerator(
        "Circle Geometry & Angular Movement", "CIRC",
        ["Circle Theorems", "Angular Velocity", "Circumferential Velocity"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Circle Theorems":
            ang = random.randint(30, 80)
            q = f"In a circle, an angle at the circumference subtended by an arc is ${ang}^\\circ$. What is the angle at the centre subtended by the same arc?"
            ans = 2 * ang
            correct = f"${ans}^\\circ$"
            wrongs = [f"${ang}^\\circ$", f"${ang/2}^\\circ$", f"${180-ang}^\\circ$", f"${90-ang}^\\circ$", f"${180-2*ang}^\\circ$", f"${360-ang}^\\circ$"]
            exp = "The angle at the centre is twice the angle at the circumference."

        elif sub == "Angular Velocity":
            rpm = random.randint(20, 100)
            q = f"A wheel rotates at {rpm} revolutions per minute (rpm). Convert this to radians per second."
            ans = (rpm * 2 * math.pi) / 60
            correct = f"{ans:.2f} rad/s"
            wrongs = [f"{(ans * random.uniform(0.5, 1.5)):.2f} rad/s" for _ in range(6)]
            exp = f"$\\omega = 2\\pi \\times \\frac{{{rpm}}}{{60}}$"

        elif sub == "Circumferential Velocity":
            rpm = random.randint(30, 120)
            r = random.randint(10, 50)
            q = f"A gear of radius {r} cm rotates at {rpm} rpm. Calculate its circumferential (linear) velocity in m/s."
            v = (r/100) * ((rpm * 2 * math.pi) / 60)
            correct = f"{v:.2f} m/s"
            wrongs = [f"{(v * random.uniform(0.5, 1.5)):.2f} m/s" for _ in range(6)]
            exp = f"$v = \\omega r = (2\\pi \\times \\frac{{{rpm}}}{{60}}) \\times \\frac{{{r}}}{{100}}$"

        if q and correct and len(wrongs) >= 6:
            wrongs = list(set(wrongs))
            while len(wrongs) < 6: wrongs.append(f"{random.randint(1, 99)}")
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper2_tech_circle_angular.json")


def gen_p2_mensuration():
    gen = TopicGenerator(
        "Mensuration (Technical)", "MENS",
        ["Surface Area of 3D Shapes", "Volume of 3D Shapes", "Composite Shapes"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Surface Area of 3D Shapes":
            r = random.randint(2, 10)
            h = random.randint(5, 20)
            q = f"Calculate the total surface area of a closed cylinder with radius {r} cm and height {h} cm."
            ans = 2 * math.pi * r**2 + 2 * math.pi * r * h
            correct = f"{ans:.2f} cm²"
            wrongs = [f"{(ans * random.uniform(0.7, 1.3)):.2f} cm²" for _ in range(6)]
            exp = f"SA = $2\\pi r^2 + 2\\pi rh = 2\\pi({r})^2 + 2\\pi({r})({h})$"

        elif sub == "Volume of 3D Shapes":
            r = random.randint(3, 12)
            q = f"Calculate the volume of a sphere with radius {r} cm."
            ans = (4/3) * math.pi * r**3
            correct = f"{ans:.2f} cm³"
            wrongs = [f"{(ans * random.uniform(0.7, 1.3)):.2f} cm³" for _ in range(6)]
            exp = f"V = $\\frac{{4}}{{3}}\\pi r^3 = \\frac{{4}}{{3}}\\pi({r})^3$"

        elif sub == "Composite Shapes":
            l, w, h = random.randint(5, 15), random.randint(5, 15), random.randint(5, 15)
            q = f"A rectangular prism has dimensions {l}m by {w}m by {h}m. A cylindrical hole of radius 1m is drilled straight through its height ({h}m). Calculate the remaining volume."
            vol_prism = l * w * h
            vol_cyl = math.pi * (1**2) * h
            ans = vol_prism - vol_cyl
            correct = f"{ans:.2f} m³"
            wrongs = [f"{(ans * random.uniform(0.7, 1.3)):.2f} m³" for _ in range(6)]
            exp = f"V_remaining = V_prism - V_cylinder = ({l}\\times{w}\\times{h}) - (\\pi(1)^2({h}))"

        if q and correct and len(wrongs) >= 6:
            wrongs = list(set(wrongs))
            while len(wrongs) < 6: wrongs.append(f"{random.randint(1, 99)}")
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)

    gen.save_to_json("dataset/grade12/technical_mathematics/paper2_tech_mensuration.json")


if __name__ == '__main__':
    print("Generating Paper 1...")
    gen_p1_algebra()
    gen_p1_functions()
    gen_p1_finance()
    gen_p1_calculus()

    print("Generating Paper 2...")
    gen_p2_analytical()
    gen_p2_trig()
    gen_p2_circle_angular()
    gen_p2_mensuration()
    print("Done!")
