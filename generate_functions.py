import random
import math
import sympy as sp
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats, get_wrong_exprs

def generate_functions():
    gen = TopicGenerator("Functions and Graphs", "FUN", ["quadratic functions", "cubic functions", "transformations", "intercepts and turning points"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        if subtopic == "quadratic functions":
            if difficulty == "easy":
                a = random.choice([-3, -2, -1, 1, 2, 3])
                p = random.randint(-5, 5)
                q = random.randint(-10, 10)
                expr = a * (sp.Symbol('x') - p)**2 + q
                expanded = sp.expand(expr)
                question = f"Given the quadratic function $f(x) = {sp.latex(expanded)}$, find the coordinates of the turning point."
                exp = f"Completing the square or using $x = -b/(2a)$: $f(x) = {a}(x - {p})^2 + {q}$. Turning point is $({p}; {q})$."
                correct = f"({p}; {q})"
                wrongs = [f"({-p}; {q})", f"({p}; {-q})", f"({-p}; {-q})", f"({q}; {p})", f"({-q}; {p})", f"({q}; {-p})", f"({-q}; {-p})", f"({p}; 0)"]
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

            elif difficulty == "medium":
                r1 = random.randint(-5, 5)
                r2 = random.randint(-5, 5)
                a = random.choice([-2, -1, 1, 2])
                expr = a * (sp.Symbol('x') - r1) * (sp.Symbol('x') - r2)
                expanded = sp.expand(expr)
                question = f"Find the x-intercepts of the function $f(x) = {sp.latex(expanded)}$."
                exp = f"$f(x) = 0 \\implies {a}(x - {r1})(x - {r2}) = 0$. The x-intercepts are $x = {r1}$ and $x = {r2}$."
                correct = f"{min(r1, r2)} and {max(r1, r2)}"
                wrongs = [f"{-r1} and {-r2}", f"{r1} and {-r2}", f"{-r1} and {r2}", f"{min(r1-1, r2-1)} and {max(r1-1, r2-1)}", f"{min(r1+1, r2+1)} and {max(r1+1, r2+1)}", f"{r1*2} and {r2*2}", f"0 and {r1+r2}"]
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

            elif difficulty == "hard":
                # Find equation from points
                r1 = random.randint(-3, 3)
                r2 = random.randint(r1+1, 6)
                a = random.choice([-2, -1, 2, 3])
                x3 = random.choice([x for x in range(-5, 5) if x != r1 and x != r2])
                y3 = a * (x3 - r1) * (x3 - r2)
                expr = a * (sp.Symbol('x') - r1) * (sp.Symbol('x') - r2)
                expanded = sp.expand(expr)
                question = f"A parabola has x-intercepts at $({r1}; 0)$ and $({r2}; 0)$ and passes through the point $({x3}; {y3})$. Find its equation in the form $y = ax^2 + bx + c$."
                exp = f"$y = a(x - {r1})(x - {r2})$. Substitute $({x3}; {y3})$: ${y3} = a({x3} - {r1})({x3} - {r2}) \\implies a = {a}$. Equation: $y = {sp.latex(expanded)}$."
                correct = f"y = {sp.latex(expanded)}"
                wrongs = get_wrong_exprs(expanded, count=8)
                wrongs = [f"y = {w}" for w in wrongs]
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

        elif subtopic == "cubic functions":
            x = sp.Symbol('x')
            if difficulty == "easy":
                a = random.choice([-1, 1, 2, -2])
                c = random.randint(-5, 5)
                expr = a*x**3 + c*x
                question = f"Find the y-intercept of the cubic function $f(x) = {sp.latex(expr)} + {random.randint(1, 10)}$."
                # It's better to just build it directly
                y_int = random.randint(-10, 10)
                expr = a*x**3 + random.randint(-5, 5)*x**2 + random.randint(-5, 5)*x + y_int
                question = f"Find the y-intercept of $f(x) = {sp.latex(expr)}$."
                exp = f"The y-intercept occurs when $x = 0$. $f(0) = {y_int}$."
                correct = str(y_int)
                wrongs = get_wrong_ints(y_int)
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

            elif difficulty == "medium":
                # Roots
                r1 = random.randint(-3, 3)
                r2 = random.randint(-3, 3)
                r3 = random.randint(-3, 3)
                expr = (x - r1) * (x - r2) * (x - r3)
                expanded = sp.expand(expr)
                question = f"Given $f(x) = {sp.latex(expanded)}$, find the x-intercepts."
                exp = f"$f(x) = (x - {r1})(x - {r2})(x - {r3}) = 0$. The intercepts are $x = {r1}$, $x = {r2}$, $x = {r3}$."
                roots = sorted(list(set([r1, r2, r3])))
                correct = ", ".join(map(str, roots))
                # generate wrong roots
                wrongs = set()
                while len(wrongs) < 8:
                    w1 = random.randint(-5, 5)
                    w2 = random.randint(-5, 5)
                    w3 = random.randint(-5, 5)
                    w_roots = sorted(list(set([w1, w2, w3])))
                    w_str = ", ".join(map(str, w_roots))
                    if w_str != correct:
                        wrongs.add(w_str)
                gen.add_question(subtopic, difficulty, question, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # Turning points via calculus (moved to calculus, but here for intercepts and tp)
                r1 = random.randint(-2, 2)
                r2 = random.randint(-3, 3)
                if r1 == r2: r2 += 1
                expr = (x - r1)**2 * (x - r2)
                expanded = sp.expand(expr)
                question = f"The function $f(x) = {sp.latex(expanded)}$ has a local turning point on the x-axis. Find the coordinates of this turning point."
                exp = f"Since $(x - {r1})^2$ is a factor, the graph touches the x-axis at $x = {r1}$. Turning point: $({r1}; 0)$."
                correct = f"({r1}; 0)"
                wrongs = [f"({-r1}; 0)", f"(0; {r1})", f"({r2}; 0)", f"({-r2}; 0)", f"(0; {-r1})", f"({r1}; {r2})", f"({r2}; {r1})", f"({-r1}; {-r2})"]
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

        elif subtopic == "transformations":
            if difficulty == "easy":
                a = random.randint(2, 5)
                h = random.randint(1, 5)
                q = f"The graph of $f(x) = x^2$ is translated ${h}$ units to the right. Write the equation of the new graph $g(x)$."
                correct = f"g(x) = (x - {h})^2"
                wrongs = [f"g(x) = (x + {h})^2", f"g(x) = x^2 - {h}", f"g(x) = x^2 + {h}", f"g(x) = {h}x^2", f"g(x) = (x - {h*2})^2", f"g(x) = (x + {h*2})^2", f"g(x) = x^2 - {h**2}"]
                exp = f"A translation ${h}$ units right means replacing $x$ with $(x - {h})$. Thus, $g(x) = (x - {h})^2$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                p = random.randint(1, 4)
                q_val = random.randint(1, 4)
                q = f"The graph of $f(x) = \\frac{{1}}{{x}}$ is translated ${p}$ units left and ${q_val}$ units down. Write the equation of the new graph."
                correct = f"y = \\frac{{1}}{{x + {p}}} - {q_val}"
                wrongs = [f"y = \\frac{{1}}{{x - {p}}} - {q_val}", f"y = \\frac{{1}}{{x + {p}}} + {q_val}", f"y = \\frac{{1}}{{x - {p}}} + {q_val}", f"y = \\frac{{1}}{{x}} - {p}", f"y = \\frac{{1}}{{x + {q_val}}} - {p}", f"y = \\frac{{1}}{{x - {q_val}}} + {p}", f"y = \\frac{{{p}}}{{x}} - {q_val}"]
                exp = f"Left by ${p}$ means $x \\mapsto x + {p}$. Down by ${q_val}$ means subtracting ${q_val}$. Equation: $y = \\frac{{1}}{{x + {p}}} - {q_val}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                a = random.choice([2, 3])
                p = random.choice([-2, -1, 1, 2])
                q_val = random.choice([-3, -2, 2, 3])
                q = f"Describe the transformation from $f(x) = {a}^x$ to $g(x) = {a}^{{x - {p}}} + {q_val}$."
                dir_x = "right" if p > 0 else "left"
                dir_y = "up" if q_val > 0 else "down"
                correct = f"Translated {abs(p)} units {dir_x} and {abs(q_val)} units {dir_y}"
                wrongs = [
                    f"Translated {abs(p)} units {'left' if p > 0 else 'right'} and {abs(q_val)} units {dir_y}",
                    f"Translated {abs(p)} units {dir_x} and {abs(q_val)} units {'down' if q_val > 0 else 'up'}",
                    f"Translated {abs(p)} units {'left' if p > 0 else 'right'} and {abs(q_val)} units {'down' if q_val > 0 else 'up'}",
                    f"Translated {abs(q_val)} units {dir_x} and {abs(p)} units {dir_y}",
                    f"Translated {abs(q_val)} units {'left' if p > 0 else 'right'} and {abs(p)} units {'down' if q_val > 0 else 'up'}",
                    f"Scaled by {abs(p)} and translated {abs(q_val)} units {dir_y}",
                    f"Reflected and translated {abs(p)} units {dir_x}"
                ]
                exp = f"$x \\mapsto x - {p}$ is a shift of {abs(p)} units {dir_x}. Adding ${q_val}$ is a shift of {abs(q_val)} units {dir_y}."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "intercepts and turning points":
            x = sp.Symbol('x')
            if difficulty == "easy":
                a = random.choice([-2, -1, 1, 2])
                b = random.randint(-6, 6)
                if b == 0: b = 2
                c = random.randint(-10, 10)
                expr = a*x**2 + b*x + c
                question = f"Find the x-coordinate of the turning point of the parabola $y = {sp.latex(expr)}$."
                x_tp = sp.Rational(-b, 2*a)
                correct = sp.latex(x_tp)
                wrongs = [sp.latex(w) for w in [x_tp * -1, x_tp + 1, x_tp - 1, sp.Rational(b, a), sp.Rational(-b, a), x_tp * 2, c, -c]]
                exp = f"$x = \\frac{{-b}}{{2a}} = \\frac{{-({b})}}{{2({a})}} = {correct}$"
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

            elif difficulty == "medium":
                a = random.choice([-1, 1])
                p = random.randint(-4, 4)
                q_val = random.randint(-9, 9)
                expr = a*(x - p)**2 + q_val
                expanded = sp.expand(expr)
                question = f"What is the range of the function $f(x) = {sp.latex(expanded)}$?"
                if a > 0:
                    correct = f"y \\geq {q_val}"
                    wrongs = [f"y \\leq {q_val}", f"y \\geq {-q_val}", f"y \\leq {-q_val}", f"y \\geq {p}", f"y \\leq {p}", f"y \\in \\mathbb{{R}}", f"y > {q_val}"]
                    exp = f"The minimum value is $y = {q_val}$. Therefore, range is $y \\geq {q_val}$."
                else:
                    correct = f"y \\leq {q_val}"
                    wrongs = [f"y \\geq {q_val}", f"y \\leq {-q_val}", f"y \\geq {-q_val}", f"y \\leq {p}", f"y \\geq {p}", f"y \\in \\mathbb{{R}}", f"y < {q_val}"]
                    exp = f"The maximum value is $y = {q_val}$. Therefore, range is $y \\leq {q_val}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

            elif difficulty == "hard":
                # hyperbola asymptotes
                p = random.randint(-5, 5)
                if p == 0: p = 2
                q_val = random.randint(-5, 5)
                a = random.choice([-3, -2, -1, 1, 2, 3])
                expr = a / (x + p) + q_val
                # formatting the equation
                p_str = f"+ {p}" if p > 0 else f"- {abs(p)}"
                q_str = f"+ {q_val}" if q_val > 0 else f"- {abs(q_val)}"
                question = f"State the equations of the asymptotes for the hyperbola $y = \\frac{{{a}}}{{x {p_str}}} {q_str}$."
                correct = f"x = {-p}, y = {q_val}"
                wrongs = [
                    f"x = {p}, y = {q_val}", f"x = {-p}, y = {-q_val}", f"x = {p}, y = {-q_val}",
                    f"x = {q_val}, y = {-p}", f"x = {-q_val}, y = {p}", f"x = {a}, y = {q_val}",
                    f"x = {-p}, y = {a}"
                ]
                exp = f"The vertical asymptote is where the denominator is zero: $x {p_str} = 0 \\implies x = {-p}$. The horizontal asymptote is the vertical shift: $y = {q_val}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, exp)

    return gen

if __name__ == "__main__":
    gen = generate_functions()
    gen.save_to_json("paper1_functions.json")
    print(f"Generated {len(gen.questions)} functions questions.")
