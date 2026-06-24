import random
import math
import sympy as sp
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats, get_wrong_exprs

def generate_algebra():
    gen = TopicGenerator("Algebra, Equations and Inequalities", "ALG", ["linear equations", "quadratic equations", "inequalities", "logarithmic equations"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        x = sp.Symbol('x')

        if subtopic == "linear equations":
            if difficulty == "easy":
                a = random.randint(2, 9)
                b = random.randint(-20, 20)
                ans = random.randint(-10, 10)
                c = a * ans - b
                q = f"Solve for $x$: ${a}x + {b} = {a * ans}$"
                correct = str(ans)
                wrongs = get_wrong_ints(ans)
                exp = f"${a}x = {a * ans} - {b} \\implies {a}x = {a * ans - b} \\implies x = {ans}$"

                # To make it prettier, generate eq carefully
                c = random.randint(1, 20)
                b = random.randint(1, 10)
                ans = random.randint(-10, 10)
                if ans == 0: ans = 2
                a = random.choice([2, 3, 4, 5])
                rhs = a * ans + b
                q = f"Solve for $x$: ${a}x + {b} = {rhs}$"
                exp = f"${a}x + {b} = {rhs} \\implies {a}x = {rhs - b} \\implies x = {ans}$"
                gen.add_question(subtopic, difficulty, q, str(ans), get_wrong_ints(ans), exp)

            elif difficulty == "medium":
                a1 = random.choice([2, 3, 4])
                b1 = random.randint(-5, 5)
                a2 = random.choice([1, 2, 3])
                b2 = random.randint(-5, 5)
                ans = random.randint(-5, 5)
                # a1(x + b1) = a2(x + b2) + c
                c = a1*(ans + b1) - a2*(ans + b2)
                q = f"Solve for $x$: ${a1}(x {'+' if b1>=0 else ''}{b1}) = {a2}(x {'+' if b2>=0 else ''}{b2}) {'+' if c>=0 else ''}{c}$"
                exp = f"Expand both sides: ${a1}x {'+' if a1*b1>=0 else ''}{a1*b1} = {a2}x {'+' if a2*b2>=0 else ''}{a2*b2} {'+' if c>=0 else ''}{c}$. Then simplify to find $x = {ans}$."
                gen.add_question(subtopic, difficulty, q, str(ans), get_wrong_ints(ans), exp)

            elif difficulty == "hard":
                # Linear simultaneous
                x_val = random.randint(-5, 5)
                y_val = random.randint(-5, 5)
                a1, b1 = random.randint(1, 4), random.randint(-4, -1)
                a2, b2 = random.randint(2, 5), random.randint(1, 3)
                c1 = a1*x_val + b1*y_val
                c2 = a2*x_val + b2*y_val
                q = f"Solve the system of equations for $x$: \n$ {a1}x {b1}y = {c1} $ \n$ {a2}x + {b2}y = {c2} $"
                exp = f"Using substitution or elimination, we find $x = {x_val}$ and $y = {y_val}$."
                gen.add_question(subtopic, difficulty, q, str(x_val), get_wrong_ints(x_val), exp)

        elif subtopic == "quadratic equations":
            if difficulty == "easy":
                r1 = random.randint(-5, 5)
                r2 = random.randint(-5, 5)
                expr = (x - r1) * (x - r2)
                expanded = sp.expand(expr)
                q = f"Solve for $x$: ${sp.latex(expanded)} = 0$"
                roots = sorted(list(set([r1, r2])))
                correct = ", ".join(map(str, roots))
                exp = f"Factorizing gives $(x - {r1})(x - {r2}) = 0$, so $x = {r1}$ or $x = {r2}$."

                wrongs = set()
                while len(wrongs) < 8:
                    w1 = random.randint(-7, 7)
                    w2 = random.randint(-7, 7)
                    w_roots = sorted(list(set([w1, w2])))
                    w_str = ", ".join(map(str, w_roots))
                    if w_str != correct:
                        wrongs.add(w_str)
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "medium":
                # Quadratic formula
                a = random.choice([2, 3, 4])
                r1 = random.randint(-3, 3)
                r2 = random.randint(-3, 3)
                expr = a * (x - r1) * (x - r2) + random.choice([-1, 1]) * random.randint(1, 3)
                expanded = sp.expand(expr)
                # Actually, let's just make sure roots are real
                a = random.choice([1, 2, 3])
                b = random.randint(4, 10)
                c = random.randint(-10, 0)
                expr = a*x**2 + b*x + c
                q = f"Solve for $x$ (correct to 2 decimal places): ${sp.latex(expr)} = 0$"
                disc = b**2 - 4*a*c
                if disc >= 0:
                    ans1 = (-b + math.sqrt(disc)) / (2*a)
                    ans2 = (-b - math.sqrt(disc)) / (2*a)
                    ans1, ans2 = min(ans1, ans2), max(ans1, ans2)
                    correct = f"{ans1:.2f}, {ans2:.2f}"
                    exp = f"Using the quadratic formula $x = \\frac{{-b \\pm \\sqrt{{b^2 - 4ac}}}}{{2a}}$, we get $x = {ans1:.2f}$ or $x = {ans2:.2f}$."

                    wrongs = set()
                    while len(wrongs) < 8:
                        w1 = ans1 + random.choice([-1, 1]) * random.uniform(0.1, 2)
                        w2 = ans2 + random.choice([-1, 1]) * random.uniform(0.1, 2)
                        w1, w2 = min(w1, w2), max(w1, w2)
                        w_str = f"{w1:.2f}, {w2:.2f}"
                        if w_str != correct: wrongs.add(w_str)
                    gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # Equations leading to quadratic (e.g. rational or substitution)
                a = random.randint(1, 3)
                # x + a/x = b
                # x^2 - bx + a = 0
                r1 = random.randint(1, 5)
                r2 = random.randint(1, 5)
                b = r1 + r2
                a_val = r1 * r2
                q = f"Solve for $x$: $x + \\frac{{{a_val}}}{{x}} = {b}$"
                roots = sorted(list(set([r1, r2])))
                correct = ", ".join(map(str, roots))
                exp = f"Multiply by $x$: $x^2 + {a_val} = {b}x \\implies x^2 - {b}x + {a_val} = 0 \\implies (x - {r1})(x - {r2}) = 0$. So $x = {r1}$ or $x = {r2}$."

                wrongs = set()
                while len(wrongs) < 8:
                    w1 = random.randint(-5, 10)
                    w2 = random.randint(-5, 10)
                    w_roots = sorted(list(set([w1, w2])))
                    w_str = ", ".join(map(str, w_roots))
                    if w_str != correct: wrongs.add(w_str)
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

        elif subtopic == "inequalities":
            if difficulty == "easy":
                a = random.choice([2, 3, 4])
                b = random.randint(-10, 10)
                ans = random.randint(-5, 5)
                c = a * ans - b
                q = f"Solve for $x$: ${a}x + {b} > {a * ans}$"
                correct = f"x > {ans}"
                wrongs = [f"x < {ans}", f"x \\geq {ans}", f"x \\leq {ans}", f"x > {-ans}", f"x < {-ans}", f"x > {ans*2}", f"x < {ans*2}", f"x > {ans-1}"]
                exp = f"${a}x > {a * ans} - {b} \\implies {a}x > {a * ans - b} \\implies x > {ans}$"
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                r1 = random.randint(-5, 0)
                r2 = random.randint(1, 5)
                expr = (x - r1) * (x - r2)
                expanded = sp.expand(expr)
                q = f"Solve for $x$: ${sp.latex(expanded)} \\leq 0$"
                correct = f"{r1} \\leq x \\leq {r2}"
                wrongs = [
                    f"x \\leq {r1} \\text{{ or }} x \\geq {r2}",
                    f"{r1} < x < {r2}",
                    f"{-r2} \\leq x \\leq {-r1}",
                    f"x \\leq {-r2} \\text{{ or }} x \\geq {-r1}",
                    f"{r2} \\leq x \\leq {r1}",
                    f"{r1-1} \\leq x \\leq {r2+1}",
                    f"x \\leq {r1}"
                ]
                exp = f"Critical values are $x = {r1}$ and $x = {r2}$. Since the parabola opens upwards, it is $\\leq 0$ between the roots: ${correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                r1 = random.randint(-3, -1)
                r2 = random.randint(1, 3)
                r3 = random.randint(4, 6)
                # x(x-r2)/(x-r3) >= 0 -> simplified
                q = f"Solve for $x$: $\\frac{{(x - {r1})(x - {r2})}}{{x - {r3}}} \\geq 0$"
                correct = f"{r1} \\leq x \\leq {r2} \\text{{ or }} x > {r3}"
                wrongs = [
                    f"x \\leq {r1} \\text{{ or }} {r2} \\leq x < {r3}",
                    f"{r1} \\leq x \\leq {r2} \\text{{ or }} x \\geq {r3}",
                    f"{r1} < x < {r2} \\text{{ or }} x > {r3}",
                    f"x < {r1} \\text{{ or }} x > {r3}",
                    f"x \\geq {r3}",
                    f"{r1} \\leq x < {r3}",
                    f"x \\leq {r1} \\text{{ or }} x \\geq {r2}"
                ]
                exp = f"Critical values are ${r1}, {r2}, {r3}$. Checking regions with a sign table gives ${correct}$. Note $x \\neq {r3}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "logarithmic equations":
            if difficulty == "easy":
                base = random.choice([2, 3, 5])
                ans = random.randint(1, 4)
                val = base ** ans
                q = f"Solve for $x$: $\\log_{{{base}}}(x) = {ans}$"
                correct = str(val)
                wrongs = get_wrong_ints(val)
                exp = f"By definition of logarithms, $x = {base}^{{{ans}}} = {val}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                base = random.choice([2, 3])
                x_val = random.randint(2, 10)
                val = base ** x_val
                # log(x+a) + log(x) = log(val) etc, let's keep it solvable
                a = random.randint(1, 5)
                val = random.randint(1, 4)
                x_ans = base**val - a
                if x_ans > 0:
                    q = f"Solve for $x$: $\\log_{{{base}}}(x + {a}) = {val}$"
                    correct = str(x_ans)
                    wrongs = get_wrong_ints(x_ans)
                    exp = f"Rewrite in exponential form: $x + {a} = {base}^{{{val}}} \\implies x + {a} = {base**val} \\implies x = {x_ans}$."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                base = random.choice([2, 3])
                r = random.randint(2, 5)
                # log(x) + log(x - a) = b
                a = r - 1
                b = r * (r - a)
                # Ensure it's a valid power
                if b == base or b == base**2 or b == base**3:
                    pass
                else:
                    r = random.choice([2, 4])
                    a = r - 1
                    b_val = 1 if r*(r-a) == base else 2 if r*(r-a) == base**2 else 3
                    x_ans = r
                    q = f"Solve for $x$: $\\log_{{{base}}}(x) + \\log_{{{base}}}(x - {a}) = {b_val}$"
                    correct = str(x_ans)
                    wrongs = get_wrong_ints(x_ans)
                    exp = f"$\\log_{{{base}}}(x(x - {a})) = {b_val} \\implies x^2 - {a}x = {base}^{{{b_val}}}$. Solve the quadratic to find $x = {x_ans}$ (rejecting the negative root)."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

    return gen

if __name__ == "__main__":
    gen = generate_algebra()
    gen.save_to_json("paper1_algebra.json")
    print(f"Generated {len(gen.questions)} algebra questions.")
