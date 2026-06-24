import random
import math
import sympy as sp
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats, get_wrong_exprs

def generate_calculus():
    gen = TopicGenerator("Differential Calculus", "CALC", ["derivative rules", "gradients of curves", "turning points", "optimization problems"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        x = sp.Symbol('x')

        if subtopic == "derivative rules":
            if difficulty == "easy":
                a = random.randint(2, 6)
                b = random.randint(-5, 5)
                if b == 0: b = 3
                c = random.randint(-10, 10)
                expr = a*x**2 + b*x + c
                q = f"Determine $f'(x)$ if $f(x) = {sp.latex(expr)}$."
                deriv = sp.diff(expr, x)
                correct = sp.latex(deriv)
                wrongs = get_wrong_exprs(deriv, count=8)
                exp = f"Using the power rule: $f'(x) = 2({a})x + {b} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # f(x) = x^3 - 4x^2 + 2x^-1 etc
                a = random.choice([-2, -1, 1, 2])
                b = random.randint(-3, 3)
                p = random.choice([-2, -1, 3, 4])
                expr = a*x**p + b*x**2
                # write clearly
                q = f"Find $\\frac{{dy}}{{dx}}$ if $y = {sp.latex(expr)}$."
                deriv = sp.diff(expr, x)
                correct = sp.latex(deriv)
                wrongs = get_wrong_exprs(deriv, count=8)
                exp = f"Apply the power rule to each term: $\\frac{{dy}}{{dx}} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # Quotient / expanding first
                a = random.randint(1, 4)
                b = random.randint(-4, 4)
                if b == 0: b = 2
                expr = (x**2 + a*x + b) / x
                # We need it simplified before latex
                q = f"Determine $D_x \\left[ \\frac{{x^2 {'+' if a>=0 else ''}{a}x {'+' if b>=0 else ''}{b}}}{{x}} \\right]$."
                deriv = sp.diff(x + a + b/x, x)
                correct = sp.latex(deriv)
                wrongs = get_wrong_exprs(deriv, count=8)
                exp = f"First simplify the expression to $x + {a} + {b}x^{{-1}}$. Then differentiate: $1 - {b}x^{{-2}} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "gradients of curves":
            if difficulty == "easy":
                a = random.choice([-2, -1, 1, 2])
                b = random.randint(-5, 5)
                expr = a*x**2 + b*x
                x_val = random.randint(-3, 3)
                q = f"Determine the gradient of the curve $f(x) = {sp.latex(expr)}$ at the point where $x = {x_val}$."
                deriv = sp.diff(expr, x)
                grad = int(deriv.subs(x, x_val))
                correct = str(grad)
                wrongs = get_wrong_ints(grad)
                exp = f"$f'(x) = {sp.latex(deriv)}$. Substitute $x = {x_val}$: $f'({x_val}) = {grad}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                a = random.choice([-1, 1, 2])
                b = random.randint(-3, 3)
                expr = a*x**3 + b*x**2
                m = random.randint(-10, 10)
                # Ensure rational solutions
                # Let's just find points where gradient is m
                # 3ax^2 + 2bx = m
                r1 = random.randint(-3, 3)
                r2 = random.randint(-3, 3)
                a_val = random.choice([1, 2])
                b_val = -(r1 + r2) * 3 * a_val / 2
                if b_val.is_integer():
                    b_val = int(b_val)
                    expr = a_val*x**3 + b_val*x**2
                    deriv = sp.diff(expr, x)
                    m = int(deriv.subs(x, r1))
                    q = f"Find the x-coordinates of the points on the curve $f(x) = {sp.latex(expr)}$ where the gradient is ${m}$."
                    roots = sorted(list(set([r1, r2])))
                    correct = ", ".join(map(str, roots))
                    exp = f"$f'(x) = {sp.latex(deriv)}$. Set $f'(x) = {m}$: ${sp.latex(deriv)} = {m}$. Solving this quadratic gives $x = {correct}$."

                    wrongs = set()
                    while len(wrongs) < 8:
                        w1 = random.randint(-5, 5)
                        w2 = random.randint(-5, 5)
                        w_roots = sorted(list(set([w1, w2])))
                        w_str = ", ".join(map(str, w_roots))
                        if w_str != correct: wrongs.add(w_str)
                    gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # Find equation of tangent
                a = random.choice([-2, -1, 1, 2])
                b = random.randint(-5, 5)
                expr = a*x**2 + b*x
                x_val = random.randint(-2, 2)
                y_val = int(expr.subs(x, x_val))
                deriv = sp.diff(expr, x)
                m = int(deriv.subs(x, x_val))
                c = y_val - m*x_val
                q = f"Find the equation of the tangent to the curve $y = {sp.latex(expr)}$ at the point $({x_val}; {y_val})$."
                tangent = m*x + c
                correct = f"y = {sp.latex(tangent)}"
                wrongs = get_wrong_exprs(tangent, count=8)
                wrongs = [f"y = {w}" for w in wrongs]
                exp = f"Gradient $m = \\frac{{dy}}{{dx}}$ at $x={x_val}$ is ${m}$. Using $y - y_1 = m(x - x_1)$, we get $y - {y_val} = {m}(x - {x_val}) \\implies y = {sp.latex(tangent)}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "turning points":
            if difficulty == "easy":
                a = random.choice([-2, -1, 1, 2])
                r1 = random.randint(-3, 3)
                r2 = random.randint(-3, 3)
                expr = a*(x - r1)**2 + r2
                expanded = sp.expand(expr)
                q = f"Find the coordinates of the turning point of $f(x) = {sp.latex(expanded)}$."
                correct = f"({r1}; {r2})"
                wrongs = [f"({-r1}; {r2})", f"({r1}; {-r2})", f"({-r1}; {-r2})", f"({r2}; {r1})", f"({-r2}; {r1})", f"({r2}; {-r1})", f"({-r2}; {-r1})", f"({r1}; 0)"]
                exp = f"$f'(x) = {sp.latex(sp.diff(expanded, x))} = 0 \\implies x = {r1}$. Substitute into $f(x)$ to get $y = {r2}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Cubic with nice integer turning points
                r1 = random.randint(-3, 3)
                r2 = random.randint(-3, 3)
                if r1 != r2:
                    # To have integer turning points at r1 and r2, the derivative must be k(x-r1)(x-r2)
                    k = random.choice([-3, 3, 6, -6])
                    deriv = k * (x - r1) * (x - r2)
                    expr = sp.integrate(deriv, x) + random.randint(-5, 5)
                    q = f"Find the x-coordinates of the turning points of $f(x) = {sp.latex(expr)}$."
                    roots = sorted([r1, r2])
                    correct = f"{roots[0]} and {roots[1]}"
                    exp = f"$f'(x) = {sp.latex(deriv)} = 0$. So $x = {roots[0]}$ or $x = {roots[1]}$."

                    wrongs = set()
                    while len(wrongs) < 8:
                        w1 = random.randint(-5, 5)
                        w2 = random.randint(-5, 5)
                        if w1 != w2:
                            w_roots = sorted([w1, w2])
                            w_str = f"{w_roots[0]} and {w_roots[1]}"
                            if w_str != correct: wrongs.add(w_str)
                    gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # Determine if local max or min
                r1 = random.randint(-2, 2)
                r2 = random.randint(-2, 2)
                if r1 != r2:
                    k = random.choice([-3, 3, 6, -6])
                    deriv = k * (x - r1) * (x - r2)
                    expr = sp.integrate(deriv, x) + random.randint(-5, 5)
                    second_deriv = sp.diff(deriv, x)
                    # Let's ask for the x-coordinate of the local maximum
                    val1 = second_deriv.subs(x, r1)
                    val2 = second_deriv.subs(x, r2)
                    max_x = r1 if val1 < 0 else r2
                    q = f"Determine the x-coordinate of the local MAXIMUM of $f(x) = {sp.latex(expr)}$."
                    correct = str(max_x)
                    wrongs = get_wrong_ints(max_x)
                    exp = f"$f'(x) = {sp.latex(deriv)} = 0 \\implies x = {r1}$ or $x = {r2}$. $f''(x) = {sp.latex(second_deriv)}$. Substituting the critical values, $f''({max_x}) < 0$, so $x = {max_x}$ is a local maximum."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "optimization problems":
            # Area/volume max/min
            if difficulty == "easy":
                P = random.choice([20, 40, 60, 80, 100])
                q = f"A rectangular garden is to be fenced using ${P}$ meters of fencing. What is the maximum possible area of the garden?"
                # max area is a square
                side = P / 4
                max_A = side * side
                correct = str(int(max_A))
                wrongs = get_wrong_ints(int(max_A))
                exp = f"Let length be $x$, width be $y$. $2x+2y={P} \\implies y={P/2}-x$. Area $A = x({P/2}-x) = {P/2}x - x^2$. $A' = {P/2} - 2x = 0 \\implies x = {P/4}$. Max area is $({P/4})^2 = {int(max_A)}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Box with square base, given volume, minimize surface area
                V = random.choice([8, 27, 64, 125, 216]) # perfect cubes
                q = f"A closed rectangular box has a square base and a volume of ${V} \\text{{ cm}}^3$. Find the side length of the square base that minimizes the total surface area."
                side = int(round(V**(1/3)))
                correct = str(side)
                wrongs = get_wrong_ints(side)
                exp = f"Let base side be $x$ and height $h$. $x^2 h = {V} \\implies h = {V}/x^2$. Surface Area $S = 2x^2 + 4xh = 2x^2 + 4x({V}/x^2) = 2x^2 + {4*V}/x$. $S' = 4x - {4*V}/x^2 = 0 \\implies 4x^3 = {4*V} \\implies x = {side}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # Maximize profit
                a = random.randint(10, 50)
                b = random.choice([1, 2, 3])
                q = f"The profit of selling $x$ items is given by $P(x) = {a}x - {b}x^2 - 10$. How many items must be sold to maximize profit?"
                x_max = a / (2 * b)
                if x_max.is_integer():
                    correct = str(int(x_max))
                    wrongs = get_wrong_ints(int(x_max))
                    exp = f"$P'(x) = {a} - {2*b}x = 0 \\implies x = {int(x_max)}$."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

    return gen

if __name__ == "__main__":
    gen = generate_calculus()
    gen.save_to_json("paper1_calculus.json")
    print(f"Generated {len(gen.questions)} calculus questions.")
