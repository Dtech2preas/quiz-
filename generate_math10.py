import json
import random
import math
import sympy as sp
import os
from typing import List
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats, get_wrong_exprs

class Math10Generator(TopicGenerator):
    def __init__(self, topic_name: str, topic_prefix: str, subtopics: List[str], paper: str):
        super().__init__(topic_name, topic_prefix, subtopics)
        self.paper = paper

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
            return False

        self.generated_questions.add(question)

        question_id = f"{self.topic_prefix}_{len(self.questions) + 1:03d}"

        q_dict = {
            "id": question_id,
            "topic": self.topic_name,
            "subtopic": subtopic,
            "paper": self.paper,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": correct_str,
            "wrong_answers_pool": unique_wrong_answers[:8],
            "explanation": explanation
        }
        self.questions.append(q_dict)
        self.difficulty_counts[difficulty] += 1
        return True

def generate_algebra() -> Math10Generator:
    subtopics = [
        "Algebraic Expressions",
        "Equations and Inequalities",
        "Factorisation",
        "Exponents"
    ]
    gen = Math10Generator("Algebra", "M10_P1_ALG", subtopics, "paper1")

    x, y = sp.symbols('x y')

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Algebraic Expressions":
            if difficulty == "easy":
                # Simplification
                a, b, c = random.randint(2, 20), random.randint(2, 20), random.randint(1, 15)
                expr = a*x + b*y - c*x + y
                q = f"Simplify the expression: ${a}x + {b}y - {c}x + y$"
                ans_expr = sp.simplify(expr)
                ans = sp.latex(ans_expr)
                exp = f"Group like terms: $({a} - {c})x + ({b} + 1)y = {ans}$"
                wrongs = get_wrong_exprs(ans_expr)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Expansion
                a = random.randint(2, 15)
                b = random.randint(1, 15)
                expr = (x + a) * (x - b)
                expanded = sp.expand(expr)
                q = f"Expand and simplify: $(x + {a})(x - {b})$"
                ans = sp.latex(expanded)
                exp = f"Multiply out using FOIL: $x^2 - {b}x + {a}x - {a*b} = {ans}$"
                wrongs = get_wrong_exprs(expanded)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else: # hard
                # Expand binomial squared + term
                a = random.randint(2, 12)
                b = random.randint(1, 20)
                expr = (x - a)**2 + b*x
                expanded = sp.expand(expr)
                q = f"Expand and simplify: $(x - {a})^2 + {b}x$"
                ans = sp.latex(expanded)
                exp = f"Expand the square: $x^2 - {2*a}x + {a**2} + {b}x = {ans}$"
                wrongs = get_wrong_exprs(expanded)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Factorisation":
            if difficulty == "easy":
                # Common factor
                a = random.randint(2, 20)
                b = a * random.randint(2, 15)
                q = f"Factorise completely: ${a}x^2 + {b}x$"
                ans = f"{a}x(x + {b//a})"
                exp = f"Take out the highest common factor ${a}x$."
                wrongs = [f"x({a}x + {b})", f"{a}(x^2 + {b//a}x)", f"{a}x^2(1 + {b//a})", f"{a}x(x - {b//a})", f"x^2({a} + {b}/x)", f"{b}x(x + {a})"]
                # Additional random wrongs if needed to make 6
                while len(wrongs) < 6:
                     wrongs.append(f"{a+random.randint(1,3)}x(x + {b//a})")
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Difference of squares
                a = random.randint(1, 15)
                sq = a**2
                q = f"Factorise: $x^2 - {sq}$"
                ans = f"(x - {a})(x + {a})"
                exp = f"This is a difference of squares: $x^2 - {a}^2 = (x - {a})(x + {a})$"
                wrongs = [f"(x - {sq})(x + 1)", f"(x - {a})(x - {a})", f"(x + {a})(x + {a})", f"x(x - {sq})", f"x^2 - {a}", f"(x - {sq})(x - 1)"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else: # hard
                # Trinomials
                r1 = random.randint(1, 15)
                r2 = random.randint(-15, -1)
                b = -(r1 + r2)
                c = r1 * r2
                sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
                sign_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"
                q = f"Factorise the trinomial: $x^2 {sign_b}x {sign_c}$"
                ans = sp.latex(sp.factor(x**2 + b*x + c))
                exp = f"Find factors of ${c}$ that sum to ${b}$, which are ${-r1}$ and ${-r2}$. Hence $(x - {r1})(x - {r2})$."
                wrongs = [
                    sp.latex(sp.factor(x**2 - b*x + c)),
                    sp.latex(sp.factor(x**2 + b*x - c)),
                    f"(x + {r1})(x + {abs(r2)})",
                    f"(x - {r1})(x - {abs(r2)})",
                    f"(x + {abs(r1*r2)})(x - 1)",
                    f"(x - {abs(r1*r2)})(x + 1)"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Equations and Inequalities":
            if difficulty == "easy":
                # Linear eq
                a = random.randint(2, 20)
                ans_val = random.randint(-40, 40)
                b = a * ans_val
                q = f"Solve for $x$: ${a}x = {b}$"
                ans = str(ans_val)
                exp = f"Divide by ${a}$ on both sides to get $x = {ans_val}$."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Linear inequality
                a = random.randint(2, 15)
                b = random.randint(1, 20)
                ans_val = random.randint(1, 15)
                c = a * ans_val - b
                q = f"Solve for $x$: ${a}x + {b} < {a*ans_val}$"
                ans = f"x < {ans_val - b/a:.2f}".rstrip('0').rstrip('.') if b%a!=0 else f"x < {ans_val - b//a}"
                exp = f"Subtract ${b}$ from both sides and divide by ${a}$."
                # We need a proper wrong answer pool. Let's make it simple integer-based.
                ans_val = random.randint(1, 15)
                c = a * ans_val
                q = f"Solve for $x$: ${a}x - {a} < {c}$"
                ans = f"x < {ans_val + 1}"
                wrongs = [f"x > {ans_val + 1}", f"x < {ans_val}", f"x \\leq {ans_val + 1}", f"x > {ans_val}", f"x < {-ans_val-1}", f"x > {-ans_val-1}"]
                exp = f"Add ${a}$ to both sides: ${a}x < {c+a}$. Divide by ${a}$: $x < {ans_val+1}$."
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else: # hard
                # Simultaneous equations
                x_val = random.randint(-20, 20)
                y_val = random.randint(-20, 20)
                q = f"Solve for $x$ in the system: \n$x + y = {x_val+y_val}$\n$x - y = {x_val-y_val}$"
                ans = str(x_val)
                exp = f"Add the two equations: $2x = {(x_val+y_val)+(x_val-y_val)} \\implies x = {x_val}$."
                wrongs = get_wrong_ints(x_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Exponents":
            if difficulty == "easy":
                base = random.choice([2, 3, 5, 7, 'x', 'y', 'z', 'a', 'b'])
                a, b = random.randint(2, 15), random.randint(2, 15)
                q = f"Simplify: ${base}^{a} \\times {base}^{b}$"
                ans = f"{base}^{{{a+b}}}"
                exp = f"When multiplying with the same base, add the exponents: ${a} + {b} = {a+b}$."
                wrongs = [f"{base}^{{{a*b}}}", f"{base}^{{{abs(a-b)}}}", f"{base}^{{{a+b+1}}}", f"(2{base})^{{{a+b}}}", f"{base}^{{{a}}}", f"{base}^{{{b}}}"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                base = random.choice(['x', 'y', 'z', 'a', 'b', 'c', 'p', 'q'])
                a, b = random.randint(3, 30), random.randint(1, 20)
                q = f"Simplify: $\\frac{{{base}^{a}}}{{{base}^{b}}}$"
                ans = f"{base}^{{{a-b}}}" if a!=b else "1"
                exp = f"When dividing with the same base, subtract the exponents: ${a} - {b} = {a-b}$."
                wrongs = [f"{base}^{{{a+b}}}", f"{base}^{{{a*b}}}", f"{base}^{{{b-a}}}", f"1", f"{base}^{{{a}}}", f"{base}^{{{b}}}"]
                # make unique
                wrongs = list(set([w for w in wrongs if w != ans]))
                while len(wrongs) < 6: wrongs.append(f"{base}^{{{random.randint(10, 20)}}}")
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else: # hard
                x_val = random.randint(1, 20)
                base = random.choice([2, 3, 4, 5, 6, 7])
                val = base**x_val
                q = f"Solve for $x$: ${base}^{{x+1}} = {val*base}$"
                ans = str(x_val)
                exp = f"${val*base}$ is ${base}^{{{x_val+1}}}$. Thus $x+1 = {x_val+1} \\implies x = {x_val}$."
                wrongs = get_wrong_ints(x_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen

def generate_sequences() -> Math10Generator:
    subtopics = ["Linear Number Patterns"]
    gen = Math10Generator("Number Patterns", "M10_P1_SEQ", subtopics, "paper1")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if difficulty == "easy":
            # Next terms
            d = random.randint(2, 8) * random.choice([1, -1])
            a = random.randint(-20, 20)
            seq = [a, a+d, a+2*d, a+3*d]
            q = f"Find the next term in the sequence: ${seq[0]}; {seq[1]}; {seq[2]}; {seq[3]}; \\dots$"
            ans = str(a + 4*d)
            exp = f"The constant difference is ${d}$. Add ${d}$ to ${seq[3]}$ to get ${ans}$."
            wrongs = get_wrong_ints(a + 4*d)
            gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
        elif difficulty == "medium":
            # General term
            d = random.randint(2, 20) * random.choice([1, -1])
            a = random.randint(-40, 40)
            seq = [a, a+d, a+2*d]
            q = f"Determine the general term $T_n$ for the sequence: ${seq[0]}; {seq[1]}; {seq[2]}; \\dots$"
            ans = f"{d}n {'+' if a-d >= 0 else '-'} {abs(a-d)}"
            exp = f"The constant difference is $d = {d}$. Using $T_n = dn + c$, $T_1 = {d}(1) + c = {a} \\implies c = {a-d}$. Thus $T_n = {ans}$."
            wrongs = [
                f"{a}n {'+' if d >= 0 else '-'} {abs(d)}",
                f"{d}n {'+' if a >= 0 else '-'} {abs(a)}",
                f"{-d}n {'+' if a-d >= 0 else '-'} {abs(a-d)}",
                f"n {'+' if d >= 0 else '-'} {abs(d)}",
                f"{d}n",
                f"{d}n {'+' if a+d >= 0 else '-'} {abs(a+d)}"
            ]
            gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
        else: # hard
            # Find n given Tn
            d = random.randint(2, 15) * random.choice([1, -1])
            a = random.randint(1, 20)
            n = random.randint(15, 30)
            Tn = a + (n-1)*d
            seq = [a, a+d, a+2*d]
            q = f"Which term in the sequence ${seq[0]}; {seq[1]}; {seq[2]}; \\dots$ is equal to ${Tn}$?"
            ans = str(n)
            exp = f"$T_n = {d}n {'+' if a-d >= 0 else '-'} {abs(a-d)}$. Set $T_n = {Tn}$ and solve for $n$: ${d}n = {Tn - (a-d)} \\implies n = {n}$."
            wrongs = get_wrong_ints(n)
            gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen

def generate_functions() -> Math10Generator:
    subtopics = ["Linear Functions", "Quadratic Functions", "Exponential Functions", "Hyperbolic Functions"]
    gen = Math10Generator("Functions and Graphs", "M10_P1_FUN", subtopics, "paper1")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Linear Functions":
            if difficulty == "easy":
                m = random.randint(2, 15) * random.choice([1, -1])
                c = random.randint(-40, 40)
                q = f"What is the y-intercept of the function $f(x) = {m}x {'+' if c>=0 else '-'} {abs(c)}$?"
                ans = str(c)
                exp = f"The y-intercept occurs where $x = 0$. $f(0) = {c}$."
                wrongs = get_wrong_ints(c)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                m = random.randint(2, 15) * random.choice([1, -1])
                c = m * random.randint(-20, 20)
                q = f"What is the x-intercept of the function $f(x) = {m}x {'+' if c>=0 else '-'} {abs(c)}$?"
                ans = str(-c//m)
                exp = f"The x-intercept occurs where $y = 0$. $0 = {m}x {'+' if c>=0 else '-'} {abs(c)} \\implies x = {-c//m}$."
                wrongs = get_wrong_ints(-c//m)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                m = random.randint(2, 15)
                x1, y1 = random.randint(1, 20), random.randint(1, 15)
                c = y1 - m*x1
                q = f"Find the equation of the straight line with gradient ${m}$ passing through $({x1}; {y1})$."
                ans = f"y = {m}x {'+' if c>=0 else '-'} {abs(c)}"
                exp = f"Use $y = mx + c$. Substitute $m={m}, x={x1}, y={y1}$: ${y1} = {m}({x1}) + c \\implies c = {c}$. Thus ${ans}$."
                wrongs = [
                    f"y = {m}x {'+' if y1>=0 else '-'} {abs(y1)}",
                    f"y = {x1}x {'+' if c>=0 else '-'} {abs(c)}",
                    f"y = {-m}x {'+' if c>=0 else '-'} {abs(c)}",
                    f"y = {m}x {'+' if -c>=0 else '-'} {abs(-c)}",
                    f"y = {m}x",
                    f"y = {c}x {'+' if m>=0 else '-'} {abs(m)}"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Quadratic Functions":
            if difficulty == "easy":
                a = random.randint(1, 20) * random.choice([1, -1])
                q = f"What is the turning point of the parabola $g(x) = {a}x^2$?"
                ans = "(0; 0)"
                exp = "A parabola in the form $y = ax^2$ has its turning point at the origin $(0; 0)$."
                wrongs = ["(1; 1)", "(0; 1)", "(1; 0)", f"(0; {a})", f"({a}; 0)", "(-1; -1)"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                a = random.choice([1, -1])
                q = f"What is the range of $h(x) = {a}x^2$?"
                ans = "y \\geq 0" if a > 0 else "y \\leq 0"
                exp = f"Since $a {' > ' if a>0 else ' < '} 0$, the parabola opens {'upwards' if a>0 else 'downwards'}. The minimum/maximum is $0$, so ${ans}$."
                wrongs = ["y \\leq 0" if a > 0 else "y \\geq 0", "y > 0", "y < 0", "All real numbers", "x \\geq 0", "x \\leq 0"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                a = random.choice([1, 2])
                qVal = random.randint(-40, -1)
                q = f"Find the x-intercepts of $f(x) = {a}x^2 {'+' if qVal>=0 else '-'} {abs(qVal)}$ (give answers as $\\pm$ value if applicable, correct to 2 decimal places)."
                val = math.sqrt(abs(qVal)/a)
                ans = f"\\pm {val:.2f}"
                exp = f"Set $y = 0$: ${a}x^2 = {abs(qVal)} \\implies x^2 = {abs(qVal)/a:.2f} \\implies x = {ans}$."
                wrongs = [f"\\pm {(val+1):.2f}", f"\\pm {(val-0.5):.2f}", f"\\pm {abs(qVal):.2f}", f"{val:.2f}", f"{-val:.2f}", f"\\pm {(val*2):.2f}"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Exponential Functions":
            if difficulty == "easy":
                b = random.choice([2, 3, 4, 5, 6, 7, 8])
                q = f"What is the y-intercept of $k(x) = {b}^x$?"
                ans = "1"
                exp = f"Set $x = 0$: $k(0) = {b}^0 = 1$."
                wrongs = ["0", str(b), "-1", "Cannot be determined", f"1/{b}", "2"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                b = random.choice([2, 3, 4, 5, 6, 7])
                qVal = random.randint(1, 15)
                q = f"What is the equation of the asymptote of $f(x) = {b}^x + {qVal}$?"
                ans = f"y = {qVal}"
                exp = f"The exponential function $y = b^x + q$ has a horizontal asymptote at $y = q$. Here, $q = {qVal}$."
                wrongs = [f"y = 0", f"x = {qVal}", f"x = 0", f"y = {-qVal}", f"y = {b}", f"x = {b}"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                b = random.choice([2, 3, 4, 5, 6, 7])
                qVal = random.randint(-15, -1)
                q = f"Does the graph of $g(x) = {b}^x {'+' if qVal>=0 else '-'} {abs(qVal)}$ intersect the x-axis? Answer 'Yes' or 'No'."
                ans = "Yes"
                exp = f"The range is $y > {qVal}$. Since ${qVal}$ is negative, the graph crosses $y=0$ (the x-axis)."
                wrongs = ["No", "Only at the origin", "Cannot be determined", "It is an asymptote", "Yes, at two points", "Yes, at y-intercept"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Hyperbolic Functions":
            if difficulty == "easy":
                a = random.randint(2, 20)
                q = f"What are the equations of the asymptotes of $f(x) = \\frac{{{a}}}{{x}}$?"
                ans = "x = 0 and y = 0"
                exp = "The basic hyperbola $y = a/x$ has asymptotes at the axes: $x=0$ and $y=0$."
                wrongs = ["x = 1 and y = 1", f"x = {a} and y = 0", f"x = 0 and y = {a}", "x = -1 and y = 1", f"x = {a} and y = {a}", "There are no asymptotes"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                a = random.choice([2, 4, 6]) * random.choice([1, -1])
                x_val = random.choice([1, 2, 3, 4, 5, 6, 7])
                y_val = a / x_val
                q = f"If $f(x) = \\frac{{{a}}}{{x}}$, calculate $f({x_val})$."
                ans = f"{y_val:.2f}".rstrip('0').rstrip('.')
                exp = f"Substitute $x={x_val}$: $f({x_val}) = \\frac{{{a}}}{{{x_val}}} = {ans}$."
                wrongs = get_wrong_floats(y_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                a = random.randint(-15, -1)
                q = f"In which quadrants does the graph of $y = \\frac{{{a}}}{{x}}$ lie?"
                ans = "Quadrant 2 and 4"
                exp = f"Since $a = {a} < 0$, the graph lies in the second and fourth quadrants."
                wrongs = ["Quadrant 1 and 3", "Quadrant 1 and 2", "Quadrant 3 and 4", "Quadrant 1 and 4", "Quadrant 2 and 3", "All quadrants"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen

def generate_finance() -> Math10Generator:
    subtopics = ["Simple Interest", "Compound Interest", "Exchange Rates", "Hire Purchase"]
    gen = Math10Generator("Finance, Growth and Decay", "M10_P1_FIN", subtopics, "paper1")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        P = random.randint(10, 200) * 100
        r = random.uniform(5.0, 15.0)
        n = random.randint(2, 8)

        if subtopic == "Simple Interest":
            if difficulty == "easy":
                A = P * (1 + (r/100) * n)
                q = f"Calculate the accumulated amount if R{P} is invested for {n} years at {r:.1f}% p.a. simple interest."
                ans = f"R{A:.2f}"
                exp = f"A = P(1 + in) = {P}(1 + ({r/100})({n})) = {A:.2f}"
                wrongs = [f"R{w}" for w in get_wrong_floats(A)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                A = P * (1 + (r/100) * n)
                q = f"An investment grows to R{A:.2f} over {n} years at {r:.1f}% p.a. simple interest. Calculate the original investment amount."
                ans = f"R{P:.2f}"
                exp = f"P = A / (1 + in) = {A:.2f} / (1 + ({r/100})({n})) = {P:.2f}"
                wrongs = [f"R{w}" for w in get_wrong_floats(P)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                I = P * (r/100) * n
                q = f"How many years will it take for an investment of R{P} to earn R{I:.2f} in interest at {r:.1f}% p.a. simple interest?"
                ans = str(n)
                exp = f"I = Pin \\implies {I:.2f} = {P}({r/100})n \\implies n = {n}"
                wrongs = get_wrong_ints(n)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Compound Interest":
            if difficulty == "easy":
                A = P * (1 + r/100)**n
                q = f"Calculate the accumulated amount if R{P} is invested for {n} years at {r:.1f}% p.a. compounded annually."
                ans = f"R{A:.2f}"
                exp = f"A = P(1 + i)^n = {P}(1 + {r/100})^{n} = {A:.2f}"
                wrongs = [f"R{w}" for w in get_wrong_floats(A)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                A = P * (1 + r/100)**n
                q = f"An investment grows to R{A:.2f} over {n} years compounded annually at {r:.1f}% p.a. Find the initial investment."
                ans = f"R{P:.2f}"
                exp = f"P = A / (1 + i)^n = {A:.2f} / (1 + {r/100})^{n} = {P:.2f}"
                wrongs = [f"R{w}" for w in get_wrong_floats(P)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                A = P * (1 + r/100)**n
                q = f"Calculate the interest earned on R{P} invested for {n} years at {r:.1f}% p.a. compounded annually."
                I = A - P
                ans = f"R{I:.2f}"
                exp = f"A = {P}(1 + {r/100})^{n} = {A:.2f}. Interest = A - P = {I:.2f}"
                wrongs = [f"R{w}" for w in get_wrong_floats(I)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Exchange Rates":
            rate = round(random.uniform(15.0, 20.0), 2)
            amount = random.randint(1, 15) * 100
            if difficulty == "easy":
                ZAR = amount * rate
                q = f"If $1 = R{rate:.2f}, convert ${amount} to Rands."
                ans = f"R{ZAR:.2f}"
                exp = f"Multiply the dollar amount by the exchange rate: {amount} * {rate:.2f} = {ZAR:.2f}"
                wrongs = [f"R{w}" for w in get_wrong_floats(ZAR)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                USD = amount / rate
                q = f"If $1 = R{rate:.2f}, convert R{amount} to Dollars."
                ans = f"${USD:.2f}"
                exp = f"Divide the Rand amount by the exchange rate: {amount} / {rate:.2f} = {USD:.2f}"
                wrongs = [f"${w}" for w in get_wrong_floats(USD)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                rate2 = rate + random.uniform(1.0, 3.0)
                diff = (amount / rate) - (amount / rate2)
                q = f"You want to buy a R{amount} item. When the rate was $1 = R{rate:.2f}, you calculated the dollar cost. Now the rate is $1 = R{rate2:.2f}. How much fewer Dollars does it cost now?"
                ans = f"${diff:.2f}"
                exp = f"Old cost = {amount}/{rate:.2f} = {amount/rate:.2f}. New cost = {amount}/{rate2:.2f} = {amount/rate2:.2f}. Difference = {diff:.2f}"
                wrongs = [f"${w}" for w in get_wrong_floats(diff)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Hire Purchase":
            deposit_perc = random.choice([10, 15, 20])
            deposit = P * deposit_perc / 100
            loan = P - deposit
            rate_hp = random.randint(10, 20)
            years = random.choice([2, 3, 4, 5])
            if difficulty == "easy":
                q = f"A TV costs R{P}. A deposit of {deposit_perc}% is required. Calculate the deposit amount."
                ans = f"R{deposit:.2f}"
                exp = f"{deposit_perc}% of R{P} = R{deposit:.2f}."
                wrongs = [f"R{w}" for w in get_wrong_floats(deposit)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                A = loan * (1 + (rate_hp/100) * years)
                q = f"A TV costs R{P}. After a {deposit_perc}% deposit, the rest is paid off over {years} years at {rate_hp}% p.a. simple interest. Calculate the total amount paid for the loan part."
                ans = f"R{A:.2f}"
                exp = f"Loan = R{P} - R{deposit:.2f} = R{loan:.2f}. A = P(1+in) = {loan}(1 + {rate_hp/100}*{years}) = R{A:.2f}."
                wrongs = [f"R{w}" for w in get_wrong_floats(A)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                A = loan * (1 + (rate_hp/100) * years)
                monthly = A / (years * 12)
                q = f"A TV costs R{P}. After a {deposit_perc}% deposit, the rest is paid over {years} years at {rate_hp}% p.a. simple interest. What is the monthly instalment?"
                ans = f"R{monthly:.2f}"
                exp = f"Loan = R{loan:.2f}. Total to pay = R{A:.2f}. Monthly = {A:.2f} / {years*12} = R{monthly:.2f}."
                wrongs = [f"R{w}" for w in get_wrong_floats(monthly)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen

def generate_probability() -> Math10Generator:
    subtopics = ["Basic Probability", "Venn Diagrams", "Mutually Exclusive Events"]
    gen = Math10Generator("Probability", "M10_P1_PROB", subtopics, "paper1")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Basic Probability":
            total = random.randint(10, 200)
            favorable = random.randint(1, total-1)
            prob = favorable / total
            if difficulty == "easy":
                q = f"A bag contains {total} marbles. {favorable} are red. If one is drawn at random, what is the probability it is red? (Decimal to 2 places)"
                ans = f"{prob:.2f}"
                exp = f"P(Red) = Favorable / Total = {favorable} / {total} = {ans}"
                wrongs = get_wrong_floats(prob)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                q = f"A bag contains {total} marbles. {favorable} are red. What is the probability that a randomly drawn marble is NOT red? (Decimal to 2 places)"
                ans = f"{1 - prob:.2f}"
                exp = f"P(Not Red) = 1 - P(Red) = 1 - ({favorable}/{total}) = {ans}"
                wrongs = get_wrong_floats(1-prob)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                q = f"A die is rolled. What is the probability of rolling a number greater than 4? (Answer as a fraction in simplest form, e.g. 1/3)"
                ans = "1/3"
                exp = f"Numbers greater than 4 are 5 and 6 (2 outcomes). Total outcomes = 6. Probability = 2/6 = 1/3."
                wrongs = ["1/6", "2/3", "1/2", "5/6", "4/6", "1/4"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Venn Diagrams":
            A = random.randint(10, 100)
            B = random.randint(10, 100)
            both = random.randint(1, min(A, B)-1)
            neither = random.randint(1, 20)
            total = A + B - both + neither
            if difficulty == "easy":
                q = f"In a class of {total}, {A} play soccer, {B} play tennis, and {both} play both. How many play only soccer?"
                ans = str(A - both)
                exp = f"Only soccer = Total soccer - Both = {A} - {both} = {A - both}"
                wrongs = get_wrong_ints(A - both)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                q = f"In a class of {total}, {A} play soccer, {B} play tennis, and {both} play both. How many play neither sport?"
                ans = str(neither)
                exp = f"Total = (Only Soccer) + (Only Tennis) + Both + Neither. Neither = {total} - ({A-both} + {B-both} + {both}) = {neither}."
                wrongs = get_wrong_ints(neither)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                prob = both / total
                q = f"In a group of {total}, {A} play soccer, {B} play tennis, {both} play both. What is the probability a randomly selected student plays both? (Decimal to 2 places)"
                ans = f"{prob:.2f}"
                exp = f"P(Both) = Both / Total = {both} / {total} = {ans}"
                wrongs = get_wrong_floats(prob)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Mutually Exclusive Events":
            if difficulty == "easy":
                q = "If events A and B are mutually exclusive, what is P(A and B)?"
                ans = "0"
                exp = "Mutually exclusive events cannot occur at the same time, so P(A and B) = 0."
                wrongs = ["1", "P(A) * P(B)", "P(A) + P(B)", "0.5", "-1", "Cannot be determined"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                PA = round(random.uniform(0.1, 0.4), 2)
                PB = round(random.uniform(0.1, 0.4), 2)
                q = f"Events A and B are mutually exclusive. If P(A) = {PA} and P(B) = {PB}, calculate P(A or B)."
                ans = f"{PA + PB:.2f}"
                exp = f"For mutually exclusive events, P(A or B) = P(A) + P(B) = {PA} + {PB} = {ans}"
                wrongs = get_wrong_floats(PA + PB)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                PA = round(random.uniform(0.2, 0.5), 2)
                P_or = round(PA + random.uniform(0.1, 0.4), 2)
                q = f"A and B are mutually exclusive. If P(A) = {PA} and P(A or B) = {P_or}, calculate P(B)."
                PB = P_or - PA
                ans = f"{PB:.2f}"
                exp = f"P(A or B) = P(A) + P(B) \\implies {P_or} = {PA} + P(B) \\implies P(B) = {PB:.2f}"
                wrongs = get_wrong_floats(PB)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen


def generate_trigonometry() -> Math10Generator:
    subtopics = ["Trigonometric Ratios", "Special Angles", "Solving Right-Angled Triangles"]
    gen = Math10Generator("Trigonometry", "M10_P2_TRIG", subtopics, "paper2")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Trigonometric Ratios":
            opp = random.randint(3, 30)
            adj = random.randint(4, 30)
            hyp = math.sqrt(opp**2 + adj**2)
            if difficulty == "easy":
                q = f"In a right-angled triangle, the side opposite angle $\\theta$ is {opp} and the adjacent side is {adj}. What is $\\tan(\\theta)$? (Answer as fraction opp/adj)"
                ans = f"{opp}/{adj}"
                exp = "$\\tan(\\theta) = \\frac{\\text{opposite}}{\\text{adjacent}}$."
                wrongs = [f"{adj}/{opp}", f"{opp}/{int(hyp)}" if opp**2+adj**2==int(hyp)**2 else "opp/hyp", f"{adj}/{int(hyp)}" if opp**2+adj**2==int(hyp)**2 else "adj/hyp", f"1/{opp}", f"1/{adj}", "1"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                q = f"If $\\sin(\\alpha) = \\frac{{{opp}}}{{{int(hyp) if hyp.is_integer() else f'{hyp:.1f}'}}}$ and $\\alpha$ is acute, calculate $\\cos(\\alpha)$? (Answer as decimal to 2 places)"
                ans_val = adj/hyp
                ans = f"{ans_val:.2f}"
                exp = f"Use Pythagoras: adj$^2$ = hyp$^2$ - opp$^2$. $\\cos(\\alpha) = \\frac{{\\text{{adj}}}}{{\\text{{hyp}}}} = {ans}$."
                wrongs = get_wrong_floats(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                q = f"Given $5\\sin(\\theta) - 3 = 0$ for $0^\\circ \\leq \\theta \\leq 90^\\circ$. Find the value of $\\cos(\\theta)$ (Decimal to 2 places)."
                ans_val = 4/5
                ans = f"{ans_val:.2f}"
                exp = "$\\sin(\\theta) = 3/5$. Opp=3, Hyp=5. Adj = $\\sqrt{5^2 - 3^2} = 4$. $\\cos(\\theta) = 4/5 = 0.80$."
                wrongs = get_wrong_floats(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Special Angles":
            if difficulty == "easy":
                q = "What is the exact value of $\\sin(30^\\circ)$?"
                ans = "1/2"
                exp = "Using special triangles, $\\sin(30^\\circ) = \\frac{1}{2}$."
                wrongs = ["$\\sqrt{3}/2$", "$\\sqrt{2}/2$", "1", "0", "$\\sqrt{3}$", "2"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                q = "Simplify without a calculator: $\\sin^2(45^\\circ) + \\cos^2(45^\\circ)$."
                ans = "1"
                exp = "$(\\frac{\\sqrt{2}}{2})^2 + (\\frac{\\sqrt{2}}{2})^2 = \\frac{2}{4} + \\frac{2}{4} = 1$."
                wrongs = ["0", "2", "1/2", "$\\sqrt{2}$", "$\\sqrt{2}/2$", "-1"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                q = "Simplify without a calculator: $\\frac{\\sin(60^\\circ)}{\\cos(60^\\circ)}$."
                ans = "\\sqrt{3}"
                exp = "$\\frac{\\sqrt{3}/2}{1/2} = \\sqrt{3}$. (This is $\\tan(60^\\circ)$)."
                wrongs = ["1/\\sqrt{3}", "\\sqrt{2}/2", "1", "2", "\\sqrt{3}/2", "0"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Solving Right-Angled Triangles":
            hyp = random.randint(10, 100)
            angle = random.randint(20, 80)
            if difficulty == "easy":
                q = f"In $\\triangle ABC$, $\\angle B = 90^\\circ$, hypotenuse $AC = {hyp}$ cm, and $\\angle C = {angle}^\\circ$. Find the length of $AB$ (opposite $\\angle C$) to 1 decimal place."
                ans_val = hyp * math.sin(math.radians(angle))
                ans = f"{ans_val:.1f}"
                exp = f"$\\sin({angle}^\\circ) = \\frac{{AB}}{{{hyp}}} \\implies AB = {hyp} \\sin({angle}^\\circ) = {ans}$ cm."
                wrongs = get_wrong_floats(ans_val, count=6, decimals=1)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                opp = random.randint(5, 40)
                adj = random.randint(5, 40)
                q = f"In $\\triangle PQR$, $\\angle Q = 90^\\circ$, $PQ = {opp}$ and $QR = {adj}$. Calculate the size of $\\angle R$ (opposite $PQ$) to 1 decimal place."
                ans_val = math.degrees(math.atan(opp/adj))
                ans = f"{ans_val:.1f}^\\circ"
                exp = f"$\\tan(R) = \\frac{{\\text{{opp}}}}{{\\text{{adj}}}} = \\frac{{{opp}}}{{{adj}}} \\implies \\angle R = \\tan^{{-1}}({opp}/{adj}) = {ans}$."
                wrongs = [f"{w}^\\circ" for w in get_wrong_floats(ans_val, count=6, decimals=1)]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                q = f"A ladder of length {hyp} m leans against a vertical wall. It makes an angle of ${angle}^\\circ$ with the horizontal ground. How far is the foot of the ladder from the wall? (to 2 decimal places)"
                ans_val = hyp * math.cos(math.radians(angle))
                ans = f"{ans_val:.2f}"
                exp = f"$\\cos({angle}^\\circ) = \\frac{{\\text{{adj}}}}{{{hyp}}} \\implies \\text{{adj}} = {hyp} \\cos({angle}^\\circ) = {ans}$."
                wrongs = get_wrong_floats(ans_val, count=6, decimals=2)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen


def generate_analytical_geometry() -> Math10Generator:
    subtopics = ["Distance Between Two Points", "Gradient of a Line", "Midpoint of a Segment"]
    gen = Math10Generator("Analytical Geometry", "M10_P2_AGEOM", subtopics, "paper2")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        x1, y1 = random.randint(-40, 40), random.randint(-40, 40)
        x2, y2 = random.randint(-40, 40), random.randint(-40, 40)
        while x1 == x2 and y1 == y2:
            x2, y2 = random.randint(-40, 40), random.randint(-40, 40)

        if subtopic == "Distance Between Two Points":
            if difficulty == "easy":
                q = f"Calculate the distance between points A({x1}; {y1}) and B({x2}; {y1})."
                ans_val = abs(x2 - x1)
                ans = str(ans_val)
                exp = f"Since the y-coordinates are the same, the distance is $|{x2} - {x1}| = {ans}$."
                wrongs = get_wrong_ints(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                q = f"Calculate the distance between points P({x1}; {y1}) and Q({x2}; {y2}). Leave answer in simplest surd form if necessary, else decimal to 2 places."
                ans_val = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                ans = f"{ans_val:.2f}"
                exp = f"$d = \\sqrt{{({x2} - {x1})^2 + ({y2} - {y1})^2}} = \\sqrt{{{ans_val**2:.0f}}} = {ans}$."
                wrongs = get_wrong_floats(ans_val)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                d2 = (x2 - x1)**2 + (y2 - y1)**2
                q = f"The distance between A({x1}; $y$) and B({x2}; {y2}) is $\\sqrt{{{d2}}}$. Find the possible value(s) of $y$ if $y > {y2}$."
                ans = str(max(y1, 2*y2 - y1))
                exp = f"$(x_2 - x_1)^2 + (y - y_2)^2 = d^2 \\implies ({x2-x1})^2 + (y - {y2})^2 = {d2}$. Solving yields $y = {ans}$ (since $y > {y2}$)."
                wrongs = get_wrong_ints(int(ans))
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Gradient of a Line":
            if difficulty == "easy":
                if x1 == x2: x2 += 1
                m = (y2 - y1) / (x2 - x1)
                q = f"Calculate the gradient of the line passing through ({x1}; {y1}) and ({x2}; {y2}). (Decimal to 2 places)"
                ans = f"{m:.2f}"
                exp = f"$m = \\frac{{y_2 - y_1}}{{x_2 - x_1}} = \\frac{{{y2} - {y1}}}{{{x2} - {x1}}} = {ans}$."
                wrongs = get_wrong_floats(m)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                if x1 == x2: x2 += 1
                m = (y2 - y1) / (x2 - x1)
                q = f"Are the points A({x1}; {y1}), B({x2}; {y2}), and C({x2+1}; {y2+m}) collinear? Answer 'Yes' or 'No'."
                ans = "Yes"
                exp = f"Gradient AB is {m}. Gradient BC is $\\frac{{{y2+m} - {y2}}}{{{x2+1} - {x2}}} = {m}$. Since gradients are equal and B is common, they are collinear."
                wrongs = ["No", "Cannot be determined", "Only if $x=0$", "Only if $y=0$", "They form a triangle", "Only if perpendicular"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                m1 = random.choice([2, 3, 4, 5, 6, 7, 8])
                x3, y3 = random.randint(-40, 40), random.randint(-40, 40)
                q = f"A line passes through ({x3}; {y3}) and is perpendicular to a line with gradient {m1}. Find its equation."
                m2 = -1 / m1
                c = y3 - m2 * x3
                ans = f"y = {m2:.2f}x {'+' if c>=0 else '-'} {abs(c):.2f}"
                exp = f"$m_2 = -1/m_1 = -1/{m1} = {m2:.2f}$. $y - {y3} = {m2:.2f}(x - {x3}) \\implies y = {m2:.2f}x {'+' if c>=0 else '-'} {abs(c):.2f}$."
                wrongs = [
                    f"y = {m1:.2f}x {'+' if c>=0 else '-'} {abs(c):.2f}",
                    f"y = {m2:.2f}x {'+' if y3>=0 else '-'} {abs(y3):.2f}",
                    f"y = {-m1:.2f}x {'+' if c>=0 else '-'} {abs(c):.2f}",
                    f"y = {-m2:.2f}x {'+' if c>=0 else '-'} {abs(c):.2f}",
                    f"y = {m2:.2f}x",
                    f"y = {m1:.2f}x {'+' if -c>=0 else '-'} {abs(-c):.2f}"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Midpoint of a Segment":
            if difficulty == "easy":
                q = f"Calculate the midpoint of the line segment joining ({x1}; {y1}) and ({x2}; {y2})."
                xm, ym = (x1 + x2)/2, (y1 + y2)/2
                ans = f"({xm:.1f}; {ym:.1f})"
                exp = f"$M(x; y) = (\\frac{{{x1}+{x2}}}{{2}}; \\frac{{{y1}+{y2}}}{{2}}) = ({xm}; {ym})$."
                wrongs = [
                    f"({ym:.1f}; {xm:.1f})",
                    f"({(x1-x2)/2:.1f}; {(y1-y2)/2:.1f})",
                    f"({(x2-x1)/2:.1f}; {(y2-y1)/2:.1f})",
                    f"({xm*2:.1f}; {ym*2:.1f})",
                    f"({x1:.1f}; {y2:.1f})",
                    f"({x2:.1f}; {y1:.1f})"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                xm, ym = random.randint(-40, 40), random.randint(-40, 40)
                x_b, y_b = 2*xm - x1, 2*ym - y1
                q = f"M({xm}; {ym}) is the midpoint of AB. If A is ({x1}; {y1}), find the coordinates of B."
                ans = f"({x_b}; {y_b})"
                exp = f"$\\frac{{{x1} + x_B}}{{2}} = {xm} \\implies x_B = {x_b}$. $\\frac{{{y1} + y_B}}{{2}} = {ym} \\implies y_B = {y_b}$."
                wrongs = [
                    f"({y_b}; {x_b})",
                    f"({xm-x1}; {ym-y1})",
                    f"({x1-xm}; {y1-ym})",
                    f"({x_b/2:.1f}; {y_b/2:.1f})",
                    f"({xm+x1}; {ym+y1})",
                    f"({2*x1-xm}; {2*y1-ym})"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                q = f"A circle has a diameter AB with A({x1}; {y1}) and B({x2}; {y2}). What are the coordinates of its centre?"
                xm, ym = (x1 + x2)/2, (y1 + y2)/2
                ans = f"({xm:.1f}; {ym:.1f})"
                exp = "The centre of the circle is the midpoint of its diameter. Midpoint = " + ans
                wrongs = [
                    f"({ym:.1f}; {xm:.1f})",
                    f"({(x1-x2)/2:.1f}; {(y1-y2)/2:.1f})",
                    f"({(x2-x1)/2:.1f}; {(y2-y1)/2:.1f})",
                    f"({xm*2:.1f}; {ym*2:.1f})",
                    f"({x1:.1f}; {y2:.1f})",
                    f"({x2:.1f}; {y1:.1f})"
                ]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen

def generate_euclidean_geometry() -> Math10Generator:
    subtopics = ["Angles and Lines", "Properties of Triangles", "Quadrilaterals"]
    gen = Math10Generator("Euclidean Geometry", "M10_P2_EGEOM", subtopics, "paper2")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        if subtopic == "Angles and Lines":
            if difficulty == "easy":
                a = random.randint(5, 175)
                q = f"Two angles on a straight line are $x$ and ${a}^\\circ$. Find $x$."
                ans = str(180 - a)
                exp = f"Angles on a straight line add up to $180^\\circ$. $x = 180^\\circ - {a}^\\circ = {ans}^\\circ$."
                wrongs = get_wrong_ints(180 - a)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                a = random.randint(5, 175)
                q = f"Two parallel lines are intersected by a transversal. If one of the alternate interior angles is ${a}^\\circ$, what is the size of the corresponding angle?"
                ans = str(a)
                exp = f"Corresponding angles are equal if lines are parallel. So the angle is ${a}^\\circ$."
                wrongs = get_wrong_ints(a)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                a = random.randint(5, 175)
                b = random.randint(5, 175)
                q = f"In a triangle, the exterior angle is ${a+b}^\\circ$ and one opposite interior angle is ${a}^\\circ$. Find the other opposite interior angle."
                ans = str(b)
                exp = f"The exterior angle of a triangle is equal to the sum of the two opposite interior angles. $x + {a}^\\circ = {a+b}^\\circ \\implies x = {b}^\\circ$."
                wrongs = get_wrong_ints(b)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Properties of Triangles":
            if difficulty == "easy":
                a = random.randint(5, 175)
                b = random.randint(5, 175)
                c = 180 - a - b
                q = f"The angles of a triangle are ${a}^\\circ$, ${b}^\\circ$ and $x$. Find $x$."
                ans = str(c)
                exp = f"Sum of angles in a triangle is $180^\\circ$. $x = 180^\\circ - ({a}^\\circ + {b}^\\circ) = {c}^\\circ$."
                wrongs = get_wrong_ints(c)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                a = random.randint(5, 175)
                c = (180 - a) / 2
                q = f"In an isosceles triangle, the unequal angle is ${a}^\\circ$. Find the size of the base angles. (Decimal to 1 place if necessary)"
                ans = f"{c:.1f}".rstrip('0').rstrip('.')
                exp = f"Base angles are equal. Sum is $180^\\circ$. $2x + {a}^\\circ = 180^\\circ \\implies 2x = {180-a}^\\circ \\implies x = {ans}^\\circ$."
                wrongs = get_wrong_floats(c, decimals=1)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:

                n1 = random.choice([3, 5, 8, 7, 9, 11, 12, 13])
                n2 = random.choice([4, 12, 15, 24, 40, 35])
                n3 = math.sqrt(n1**2 + n2**2)
                if random.choice([True, False]) and n3.is_integer():
                    q = f"A triangle has sides {n1} cm, {n2} cm, and {int(n3)} cm. Is it a right-angled triangle? Answer 'Yes' or 'No'."
                    ans = "Yes"
                    exp = f"${n1}^2 + {n2}^2 = {n1**2} + {n2**2} = {n1**2+n2**2}$. And ${int(n3)}^2 = {int(n3)**2}$. Since ${n1}^2 + {n2}^2 = {int(n3)}^2$, it is right-angled."
                    wrongs = ["No", "Cannot be determined", "Only if isosceles", "Only if equilateral", "Maybe", "Depends on the angles given"]
                    gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
                else:
                    n3_wrong = int(n3) + random.randint(1, 3)
                    q = f"A triangle has sides {n1} cm, {n2} cm, and {n3_wrong} cm. Is it a right-angled triangle? Answer 'Yes' or 'No'."
                    ans = "No"
                    exp = f"${n1}^2 + {n2}^2 = {n1**2} + {n2**2}$. But ${n3_wrong}^2 = {n3_wrong**2}$. They are not equal, so it is not right-angled."
                    wrongs = ["Yes", "Cannot be determined", "Only if isosceles", "Only if equilateral", "Maybe", "Depends on the angles given"]
                    gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)


        elif subtopic == "Quadrilaterals":
            if difficulty == "easy":
                q = "In a parallelogram, opposite angles are..."
                ans = "Equal"
                exp = "One of the properties of a parallelogram is that opposite angles are equal in size."
                wrongs = ["Supplementary", "Complementary", "Half the size", "Twice the size", "$90^\\circ$", "Proportional"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                a = random.randint(5, 175)
                q = f"The adjacent angles of a parallelogram are $x$ and ${a}^\\circ$. Find $x$."
                ans = str(180 - a)
                exp = f"Adjacent angles of a parallelogram are supplementary (sum to $180^\\circ$). $x = 180^\\circ - {a}^\\circ = {180-a}^\\circ$."
                wrongs = get_wrong_ints(180 - a)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                q = "A quadrilateral has all sides equal and diagonals intersecting at $90^\\circ$, but the diagonals are not equal in length. What shape is it?"
                ans = "Rhombus"
                exp = "A rhombus has equal sides and perpendicular diagonals, but unlike a square, its diagonals are not necessarily equal."
                wrongs = ["Square", "Rectangle", "Kite", "Trapezium", "Parallelogram", "Isosceles Trapezium"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

    return gen

def generate_statistics() -> Math10Generator:
    subtopics = ["Measures of Central Tendency", "Measures of Dispersion", "Data Representation"]
    gen = Math10Generator("Statistics", "M10_P2_STAT", subtopics, "paper2")

    attempts = 0
    while not gen.is_done() and attempts < 50000:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff_choices = []
        for d, count in gen.difficulty_counts.items():
            if count < gen.difficulty_targets[d]:
                diff_choices.append(d)
        if not diff_choices:
            break
        difficulty = random.choice(diff_choices)

        data = [random.randint(10, 200) for _ in range(5)]
        data.sort()

        if subtopic == "Measures of Central Tendency":
            if difficulty == "easy":
                # Mean
                mean = sum(data) / len(data)
                q = f"Find the mean of the data set: {', '.join(map(str, data))} (Decimal to 1 place)"
                ans = f"{mean:.1f}"
                exp = f"Mean = Sum / N = {sum(data)} / 5 = {ans}"
                wrongs = get_wrong_floats(mean, decimals=1)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Median (even number of items)
                data.append(random.randint(10, 200))
                data.sort()
                median = (data[2] + data[3]) / 2
                q = f"Find the median of the data set: {', '.join(map(str, data))} (Decimal to 1 place)"
                ans = f"{median:.1f}"
                exp = f"The middle values are {data[2]} and {data[3]}. Median = ({data[2]} + {data[3]}) / 2 = {ans}"
                wrongs = get_wrong_floats(median, decimals=1)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Mode logic
                data[1] = data[0] # Ensure a mode
                mode = data[0]
                q = f"Find the mode of the data set: {', '.join(map(str, data))}"
                ans = str(mode)
                exp = f"The mode is the value that appears most often, which is {mode}."
                wrongs = get_wrong_ints(mode)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Measures of Dispersion":
            if difficulty == "easy":
                # Range
                r = data[-1] - data[0]
                q = f"Find the range of the data set: {', '.join(map(str, data))}"
                ans = str(r)
                exp = f"Range = Max - Min = {data[-1]} - {data[0]} = {ans}"
                wrongs = get_wrong_ints(r)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            elif difficulty == "medium":
                # Interquartile range setup (approximate for simplicity in text generation)
                Q1 = (data[0] + data[1]) / 2
                Q3 = (data[3] + data[4]) / 2
                iqr = Q3 - Q1
                q = f"Given Q1 = {Q1:.1f} and Q3 = {Q3:.1f}, calculate the Interquartile Range (IQR)."
                ans = f"{iqr:.1f}"
                exp = f"IQR = Q3 - Q1 = {Q3:.1f} - {Q1:.1f} = {ans}"
                wrongs = get_wrong_floats(iqr, decimals=1)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)
            else:
                # Five number summary
                q = f"Identify the minimum value in the 5-number summary for: {', '.join(map(str, data))}"
                ans = str(data[0])
                exp = f"The 5-number summary consists of Min, Q1, Median, Q3, Max. The Min is {data[0]}."
                wrongs = get_wrong_ints(data[0])
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

        elif subtopic == "Data Representation":
            if difficulty == "easy":

                a = random.randint(10, 50)
                q = f"If the 5-number summary is Min={a}, Q1={a+5}, Median={a+10}, Q3={a+20}, Max={a+30}, what is the interquartile range?"
                ans = str(15)
                exp = f"IQR = Q3 - Q1 = {a+20} - {a+5} = 15."
                wrongs = get_wrong_ints(15)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

            elif difficulty == "medium":

                skew_val = random.randint(10, 50)
                q = f"In a data set, the median is {skew_val} and the mean is {skew_val+10}. Is the distribution roughly symmetric, left-skewed, or right-skewed?"
                ans = "Right-skewed"
                exp = "Since the mean is greater than the median, the distribution is pulled to the right."
                wrongs = ["Left-skewed", "Symmetric", "Normal", "Uniform", "Bimodal", "Cannot be determined"]
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)

            else:

                freq = random.randint(5, 500)
                width = random.randint(2, 10)
                q = f"In a histogram, a class has width {width} and height {freq}. What is the area of the bar?"
                ans = str(freq * width)
                exp = f"Area = width * height = {width} * {freq} = {freq * width}."
                wrongs = get_wrong_ints(freq * width)
                gen.add_question(subtopic, difficulty, q, ans, wrongs, exp)


    return gen

if __name__ == "__main__":
    # Ensure reproducibility for random values
    random.seed(42)

    # Execute all generators and save
    print("Generating Paper 1 Topics...")
    p1_algebra = generate_algebra()
    p1_algebra.save_to_json("dataset/grade10/mathematics/paper1_math10_algebra.json")

    p1_sequences = generate_sequences()
    p1_sequences.save_to_json("dataset/grade10/mathematics/paper1_math10_sequences.json")

    p1_functions = generate_functions()
    p1_functions.save_to_json("dataset/grade10/mathematics/paper1_math10_functions.json")

    p1_finance = generate_finance()
    p1_finance.save_to_json("dataset/grade10/mathematics/paper1_math10_finance.json")

    p1_probability = generate_probability()
    p1_probability.save_to_json("dataset/grade10/mathematics/paper1_math10_probability.json")

    print("Generating Paper 2 Topics...")
    p2_trigonometry = generate_trigonometry()
    p2_trigonometry.save_to_json("dataset/grade10/mathematics/paper2_math10_trigonometry.json")

    p2_analytical = generate_analytical_geometry()
    p2_analytical.save_to_json("dataset/grade10/mathematics/paper2_math10_analytical_geometry.json")

    p2_euclidean = generate_euclidean_geometry()
    p2_euclidean.save_to_json("dataset/grade10/mathematics/paper2_math10_euclidean_geometry.json")

    p2_statistics = generate_statistics()
    p2_statistics.save_to_json("dataset/grade10/mathematics/paper2_math10_statistics.json")

    print("All Grade 10 Math datasets generated successfully.")
