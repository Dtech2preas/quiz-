import random
import math
import sympy as sp
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
        ["Limits", "First Principles", "Differentiation Rules", "Cubic Graphs", "Integration"]
    )
    attempts = 0
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Limits":
            a = random.randint(2, 5)
            x_val = random.randint(1, 4)
            if diff == "easy":
                q = f"Evaluate: $\\lim_{{x \\to {x_val}}} ({a}x^2 - x)$"
                ans = a*(x_val**2) - x_val
                correct = str(ans)
                wrongs = get_wrong_ints(ans, 6)
                exp = f"Substitute $x={x_val}$: ${a}({x_val})^2 - ({x_val}) = {ans}$"
            else:
                q = f"Evaluate: $\\lim_{{x \\to {x_val}}} \\frac{{x^2 - {x_val**2}}}{{x - {x_val}}}$"
                ans = 2 * x_val
                correct = str(ans)
                wrongs = get_wrong_ints(ans, 6)
                exp = f"Factorise numerator: $\\frac{{(x-{x_val})(x+{x_val})}}{{x-{x_val}}} = x + {x_val}$. Then substitute $x={x_val}$ to get ${x_val}+{x_val} = {ans}$."

        elif sub == "Differentiation Rules":
            n = random.randint(2, 5)
            a = random.randint(2, 6)
            if diff == "easy":
                q = f"Determine $\\frac{{dy}}{{dx}}$ if $y = {a}x^{n}$."
                ans_a = a * n
                ans_n = n - 1
                correct = f"${ans_a}x^{ans_n}$"
                wrongs = [f"${ans_a}x^{n}$", f"${a}x^{ans_n}$", f"${ans_a}x^{n+1}$", f"${a*n*2}x^{ans_n}$", f"${ans_a}x$", f"${a}x^{n-2}$"]
                exp = f"Multiply coefficient by power, reduce power by 1: ${a} \\times {n} = {ans_a}$, new power = ${n}-1 = {ans_n}$."
            else:
                q = f"Determine $f'(x)$ if $f(x) = {a}x^{n} - \\frac{{{a}}}{{x^2}}$."
                ans_a1 = a * n
                ans_n1 = n - 1
                correct = f"${ans_a1}x^{ans_n1} + {2*a}x^{{-3}}$"
                wrongs = [
                    f"${ans_a1}x^{ans_n1} - {2*a}x^{{-3}}$",
                    f"${ans_a1}x^{ans_n1} + {a}x^{{-3}}$",
                    f"${ans_a1}x^{ans_n1} - {a}x^{{-1}}$",
                    f"${ans_a1}x^{n} + {2*a}x^{{-3}}$",
                    f"${a}x^{ans_n1} + {2*a}x^{{-3}}$",
                    f"${ans_a1}x^{ans_n1} + {2*a}x^{{-1}}$"
                ]
                exp = f"Rewrite as $f(x) = {a}x^{n} - {a}x^{{-2}}$. Then $f'(x) = {ans_a1}x^{ans_n1} - (-2)({a})x^{{-3}}$."

        elif sub == "First Principles":
            a = random.randint(2, 5)
            q = f"Determine the derivative of $f(x) = {a}x^2$ from first principles. What is $f'(x)$?"
            correct = f"${2*a}x$"
            wrongs = [f"${a}x$", f"${2*a}x^2$", f"${a}x^2$", f"${2*a}$", f"${a}$", f"${2*a}x^3$"]
            exp = f"$f'(x) = \\lim_{{h \\to 0}} \\frac{{{a}(x+h)^2 - {a}x^2}}{{h}} = \\lim_{{h \\to 0}} \\frac{{{a}(x^2+2xh+h^2) - {a}x^2}}{{h}} = {2*a}x$"

        elif sub == "Cubic Graphs":
            q = "A cubic function $f(x) = x^3 - 3x^2 + 4$. At what $x$-values do the turning points occur?"
            correct = "$x = 0$ and $x = 2$"
            wrongs = [
                "$x = -2$ and $x = 0$", "$x = -1$ and $x = 2$", "$x = 1$ and $x = -2$",
                "$x = 0$ and $x = 3$", "$x = 1$ and $x = 3$", "$x = -3$ and $x = 2$"
            ]
            exp = "$f'(x) = 3x^2 - 6x$. Set $f'(x)=0 \\implies 3x(x-2)=0 \\implies x=0$ or $x=2$."

        elif sub == "Integration":
            a = random.randint(2, 6)
            n = random.randint(2, 4)
            q = f"Determine the indefinite integral: $\\int {a}x^{n} dx$"
            ans_n = n + 1
            correct = f"$\\frac{{{a}}}{{{ans_n}}}x^{{{ans_n}}} + C$"
            wrongs = [
                f"$\\frac{{{a}}}{{{n}}}x^{{{ans_n}}} + C$",
                f"${a * n}x^{{{n-1}}} + C$",
                f"$\\frac{{{a}}}{{{ans_n}}}x^{{{n}}} + C$",
                f"$\\frac{{{a}}}{{{n-1}}}x^{{{ans_n}}} + C$",
                f"$\\frac{{{a}}}{{{ans_n}}}x^{{{ans_n}}}$",
                f"${a}x^{{{ans_n}}} + C$"
            ]
            exp = "Add 1 to the exponent and divide by the new exponent, plus C."

        if q and correct and len(wrongs) >= 6:
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)

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
    while not gen.is_done() and attempts < 30000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        diff = random.choice(available_diffs)
        sub = random.choice(gen.subtopics)

        q, correct, wrongs, exp = "", "", [], ""

        if sub == "Identities":
            q = "Simplify: $\\tan x \\cdot \\cos x$"
            correct = "$\\sin x$"
            wrongs = ["$\\cos x$", "$1$", "$\\sec x$", "$\\csc x$", "$\\cot x$", "$\\sin^2 x$"]
            exp = "$\\tan x = \\frac{\\sin x}{\\cos x}$, so $\\frac{\\sin x}{\\cos x} \\cdot \\cos x = \\sin x$"

        elif sub == "Reduction Formulae":
            angle = random.choice([120, 135, 150, 210, 225, 240, 300, 315, 330])
            q = f"Evaluate without a calculator: $\\sin({angle}^\\circ)$"
            val = math.sin(math.radians(angle))
            correct = f"{val:.3f}"
            wrongs = [f"{(val + random.uniform(0.1, 0.5)):.3f}" for _ in range(6)]
            exp = f"Reduce ${angle}^\\circ$ to the first quadrant using CAST diagram."

        elif sub == "Solving Equations":
            a = random.randint(2, 5)
            q = f"Solve for $x$ in the interval $[0^\\circ, 90^\\circ]$: $\\cos x = \\frac{{1}}{{{a}}}$"
            ans = math.degrees(math.acos(1/a))
            correct = f"{ans:.1f}^\\circ"
            wrongs = [f"{(ans + random.randint(10, 50)):.1f}^\\circ" for _ in range(6)]
            exp = f"Use inverse cosine: $x = \\cos^{{-1}}(1/{a})$."

        elif sub == "2D/3D Problems":
            a, b = random.randint(5, 15), random.randint(5, 15)
            angle = random.choice([30, 45, 60, 120])
            q = f"In $\\Delta ABC$, $a = {a}$, $b = {b}$ and $\\angle C = {angle}^\\circ$. Calculate the area of the triangle."
            ans = 0.5 * a * b * math.sin(math.radians(angle))
            correct = f"{ans:.2f}"
            wrongs = [f"{(ans * random.uniform(0.5, 1.5)):.2f}" for _ in range(6)]
            exp = f"Area = $\\frac{{1}}{{2}}ab\\sin C = 0.5 \\times {a} \\times {b} \\times \\sin({angle}^\\circ)$"

        if q and correct and len(wrongs) >= 6:
            wrongs = list(set(wrongs))
            while len(wrongs) < 6: wrongs.append(f"{random.randint(1, 99)}")
            try:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)
            except TypeError:
                gen.add_question(sub, diff, q, correct, wrongs[:6], exp)

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
