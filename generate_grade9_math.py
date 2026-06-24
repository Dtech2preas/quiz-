import random
import math
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

# Numbers, Operations and Relationships
def generate_numbers_operations():
    subtopics = [
        "Whole numbers",
        "Integers",
        "Fractions and decimals",
        "Exponents",
        "Ratio and proportion",
        "Percentages and financial maths"
    ]
    gen = TopicGenerator("Numbers, Operations and Relationships", "NUM", subtopics)

    attempts = 0
    limit = 50000

    while not gen.is_done() and attempts < limit:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]

        if subtopic == "Whole numbers":
            if diff == "easy":
                a = random.randint(100, 999)
                b = random.randint(100, 999)
                q = f"Calculate the sum: ${a} + {b}$"
                ans = a + b
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"${a} + {b} = {ans}$")
            elif diff == "medium":
                a = random.randint(100, 999)
                b = random.randint(10, 99)
                q = f"Calculate the product: ${a} \\times {b}$"
                ans = a * b
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"${a} \\times {b} = {ans}$")
            else:
                a = random.randint(1000, 9999)
                b = random.randint(10, 50)
                q = f"Calculate the quotient and remainder: ${a} \\div {b}$"
                quotient = a // b
                remainder = a % b
                ans = f"{quotient} remainder {remainder}"
                wrong = [
                    f"{quotient + 1} remainder {remainder}",
                    f"{quotient - 1} remainder {remainder}",
                    f"{quotient} remainder {remainder + 1}",
                    f"{quotient} remainder {max(0, remainder - 1)}",
                    f"{quotient + 2} remainder {remainder}",
                    f"{quotient - 2} remainder {remainder}",
                    f"{quotient + random.randint(1, 5)} remainder {random.randint(0, b - 1)}"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"${a} \\div {b} = {quotient}$ with a remainder of ${remainder}$.")

        elif subtopic == "Integers":
            if diff == "easy":
                a = random.randint(-50, -10)
                b = random.randint(10, 50)
                q = f"Calculate: ${a} + {b}$"
                ans = a + b
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"Adding a positive number to a negative number: ${a} + {b} = {ans}$.")
            elif diff == "medium":
                a = random.randint(-20, -1)
                b = random.randint(-20, -1)
                q = f"Calculate: ${a} \\times {b}$"
                ans = a * b
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"The product of two negative numbers is positive: ${a} \\times {b} = {ans}$.")
            else:
                a = random.randint(-30, 30)
                b = random.randint(-20, 20)
                c = random.randint(-10, -1)
                q = f"Calculate: ${a} - ({b}) \\times ({c})$"
                ans = a - (b * c)
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"Follow BODMAS: first multiply $({b}) \\times ({c}) = {b * c}$, then subtract from ${a}$: ${a} - ({b * c}) = {ans}$.")

        elif subtopic == "Fractions and decimals":
            if diff == "easy":
                den = random.randint(2, 10)
                num = random.randint(1, den - 1)
                q = f"Convert $\\frac{{{num}}}{{{den}}}$ to a decimal."
                ans = round(num / den, 3)
                wrong = get_wrong_floats(ans, decimals=3)
                gen.add_question(subtopic, diff, q, f"{ans}", wrong, f"$\\frac{{{num}}}{{{den}}} = {ans}$.")
            elif diff == "medium":
                a = round(random.uniform(1, 10), 2)
                b = round(random.uniform(1, 10), 2)
                q = f"Calculate: ${a} \\times {b}$"
                ans = round(a * b, 4)
                wrong = get_wrong_floats(ans, decimals=4)
                gen.add_question(subtopic, diff, q, f"{ans}", wrong, f"${a} \\times {b} = {ans}$.")
            else:
                a_num = random.randint(1, 5)
                a_den = random.randint(2, 6)
                b_num = random.randint(1, 5)
                b_den = random.randint(2, 6)
                if a_num/a_den == b_num/b_den: continue
                q = f"Calculate: $\\frac{{{a_num}}}{{{a_den}}} \\div \\frac{{{b_num}}}{{{b_den}}}$"
                num = a_num * b_den
                den = a_den * b_num
                gcd = math.gcd(num, den)
                ans = f"\\frac{{{num // gcd}}}{{{den // gcd}}}"
                wrong = [
                    f"\\frac{{{a_num * b_num}}}{{{a_den * b_den}}}",
                    f"\\frac{{{a_num * b_num}}}{{{a_den * b_den // math.gcd(a_num * b_num, a_den * b_den)}}}",
                    f"\\frac{{{den // gcd}}}{{{num // gcd}}}",
                    f"\\frac{{{num // gcd + 1}}}{{{den // gcd}}}",
                    f"\\frac{{{num // gcd}}}{{{den // gcd + 1}}}",
                    f"\\frac{{{num // gcd - 1}}}{{{den // gcd}}}",
                    f"\\frac{{{num // gcd}}}{{{max(1, den // gcd - 1)}}}"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"To divide fractions, multiply by the reciprocal: $\\frac{{{a_num}}}{{{a_den}}} \\times \\frac{{{b_den}}}{{{b_num}}} = \\frac{{{a_num * b_den}}}{{{a_den * b_num}}} = \\frac{{{num // gcd}}}{{{den // gcd}}}$.")

        elif subtopic == "Exponents":
            if diff == "easy":
                base = random.randint(2, 10)
                exp = random.randint(2, 4)
                q = f"Calculate: ${base}^{exp}$"
                ans = base ** exp
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"${base}^{exp} = {ans}$.")
            elif diff == "medium":
                base = random.randint(2, 5)
                exp1 = random.randint(2, 5)
                exp2 = random.randint(2, 5)
                q = f"Simplify: ${base}^{exp1} \\times {base}^{exp2}$"
                ans = f"{base}^{{{exp1 + exp2}}}"
                wrong = [
                    f"{base}^{{{exp1 * exp2}}}",
                    f"{base}^{{{abs(exp1 - exp2)}}}",
                    f"{base * 2}^{{{exp1 + exp2}}}",
                    f"{base}^{{{exp1 + exp2 + 1}}}",
                    f"{base}^{{{exp1 + exp2 - 1}}}",
                    f"{base + 1}^{{{exp1 + exp2}}}",
                    f"{base - 1}^{{{exp1 + exp2}}}"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"When multiplying with the same base, add the exponents: ${exp1} + {exp2} = {exp1 + exp2}$.")
            else:
                base = random.randint(2, 5)
                exp1 = random.randint(2, 5)
                exp2 = random.randint(2, 5)
                q = f"Simplify: $({base}^{exp1})^{exp2}$"
                ans = f"{base}^{{{exp1 * exp2}}}"
                wrong = [
                    f"{base}^{{{exp1 + exp2}}}",
                    f"{base}^{{{abs(exp1 - exp2)}}}",
                    f"{base * 2}^{{{exp1 * exp2}}}",
                    f"{base}^{{{exp1 * exp2 + 1}}}",
                    f"{base}^{{{exp1 * exp2 - 1}}}",
                    f"{base + 1}^{{{exp1 * exp2}}}",
                    f"{base - 1}^{{{exp1 * exp2}}}"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"When raising a power to a power, multiply the exponents: ${exp1} \\times {exp2} = {exp1 * exp2}$.")

        elif subtopic == "Ratio and proportion":
            if diff == "easy":
                a = random.randint(2, 10)
                b = random.randint(2, 10)
                mult = random.randint(2, 5)
                a_val = a * mult
                b_val = b * mult
                q = f"Simplify the ratio ${a_val}:{b_val}$."
                gcd = math.gcd(a_val, b_val)
                ans = f"{a_val // gcd}:{b_val // gcd}"
                wrong = [
                    f"{b_val // gcd}:{a_val // gcd}",
                    f"{a_val}:{b_val}",
                    f"{a_val // gcd + 1}:{b_val // gcd}",
                    f"{a_val // gcd}:{b_val // gcd + 1}",
                    f"{max(1, a_val // gcd - 1)}:{b_val // gcd}",
                    f"{a_val // gcd}:{max(1, b_val // gcd - 1)}",
                    f"{a_val // gcd + 2}:{b_val // gcd}"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Divide both sides by their greatest common divisor ({gcd}): ${a_val // gcd}:{b_val // gcd}$.")
            elif diff == "medium":
                a = random.randint(2, 5)
                b = random.randint(2, 5)
                total = random.randint(10, 50) * (a + b)
                q = f"Divide ${total}$ in the ratio ${a}:{b}$. What is the smaller part?"
                part = total // (a + b)
                ans = min(a, b) * part
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"Total parts = ${a} + {b} = {a + b}$. One part = ${total} \\div {a + b} = {part}$. Smaller part = ${min(a, b)} \\times {part} = {ans}$.")
            else:
                x1 = random.randint(2, 10)
                y1 = random.randint(5, 20)
                x2 = random.randint(11, 25)
                if y1 * x2 % x1 != 0: continue
                y2 = y1 * x2 // x1
                q = f"If $x$ and $y$ are directly proportional, and $y = {y1}$ when $x = {x1}$, find $y$ when $x = {x2}$."
                ans = y2
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"Since $y = kx$, $k = \\frac{{{y1}}}{{{x1}}} = {y1/x1}$. Then $y = {y1/x1} \\times {x2} = {ans}$.")

        elif subtopic == "Percentages and financial maths":
            if diff == "easy":
                pct = random.randint(5, 95)
                amount = random.randint(10, 500) * 10
                q = f"Calculate ${pct}\\%$ of R${amount}$."
                ans = round(amount * (pct / 100), 2)
                wrong = get_wrong_floats(ans, decimals=2)
                gen.add_question(subtopic, diff, q, f"R${ans:.2f}$", [f"R${w}" for w in wrong], f"$\\frac{{{pct}}}{{100}} \\times {amount} = {ans}$.")
            elif diff == "medium":
                p = random.randint(1000, 10000)
                r = random.randint(5, 15)
                t = random.randint(2, 10)
                q = f"Calculate the simple interest on R${p}$ at ${r}\\%$ p.a. for ${t}$ years."
                ans = p * (r / 100) * t
                wrong = get_wrong_floats(ans, decimals=2)
                gen.add_question(subtopic, diff, q, f"R${ans:.2f}$", [f"R${w}" for w in wrong], f"Simple interest = $P \\times r \\times t = {p} \\times {r/100} \\times {t} = {ans}$.")
            else:
                p = random.randint(1000, 10000)
                r = random.randint(5, 15)
                t = random.randint(2, 5)
                q = f"Calculate the final amount if R${p}$ is invested at ${r}\\%$ p.a. compound interest for ${t}$ years. (Round to 2 decimal places)"
                ans = round(p * (1 + r / 100) ** t, 2)
                wrong = get_wrong_floats(ans, decimals=2)
                gen.add_question(subtopic, diff, q, f"R${ans:.2f}$", [f"R${w}" for w in wrong], f"$A = P(1 + i)^n = {p}(1 + {r/100})^{t} = {ans}$.")

    gen.save_to_json('dataset/grade9/mathematics/numbers_operations.json')

# Patterns, Functions and Algebra
def generate_patterns_algebra():
    subtopics = [
        "Numeric and geometric patterns",
        "Algebraic expressions",
        "Factorisation",
        "Linear equations",
        "Functions and graphs"
    ]
    gen = TopicGenerator("Patterns, Functions and Algebra", "ALG", subtopics)

    attempts = 0
    limit = 50000

    while not gen.is_done() and attempts < limit:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]

        if subtopic == "Numeric and geometric patterns":
            if diff == "easy":
                start = random.randint(1, 10)
                diff_val = random.randint(2, 5)
                seq = [start + i * diff_val for i in range(4)]
                q = f"Find the next term in the sequence: ${seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ...$"
                ans = start + 4 * diff_val
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"The constant difference is ${diff_val}$. Therefore, ${seq[3]} + {diff_val} = {ans}$.")
            elif diff == "medium":
                start = random.randint(1, 10)
                diff_val = random.randint(2, 5)
                n = random.randint(10, 20)
                q = f"Determine the ${n}$th term of the sequence: ${start}, {start + diff_val}, {start + 2*diff_val}, ...$"
                ans = start + (n - 1) * diff_val
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"The general rule is $T_n = {diff_val}n + {start - diff_val}$. Therefore, $T_{{{n}}} = {diff_val}({n}) + {start - diff_val} = {ans}$.")
            else:
                start = random.randint(1, 5)
                ratio = random.randint(2, 4)
                seq = [start * (ratio ** i) for i in range(4)]
                q = f"Find the next term in the geometric sequence: ${seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ...$"
                ans = start * (ratio ** 4)
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"The constant ratio is ${ratio}$. Therefore, ${seq[3]} \\times {ratio} = {ans}$.")

        elif subtopic == "Algebraic expressions":
            if diff == "easy":
                a = random.randint(2, 10)
                b = random.randint(2, 10)
                c = random.randint(2, 10)
                q = f"Simplify: ${a}x + {b}x - {c}x$"
                coeff = a + b - c
                ans = f"{coeff}x"
                wrong = [
                    f"{coeff + 1}x",
                    f"{coeff - 1}x",
                    f"{-coeff}x",
                    f"{a + b + c}x",
                    f"{a - b - c}x",
                    f"{coeff}x^2",
                    f"{coeff + 2}x"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"Add and subtract the coefficients: ${a} + {b} - {c} = {coeff}$.")
            elif diff == "medium":
                a = random.randint(2, 5)
                b = random.randint(2, 5)
                c = random.randint(2, 5)
                q = f"Expand: ${a}({b}x + {c})$"
                ans = f"{a*b}x + {a*c}"
                wrong = [
                    f"{a*b}x + {c}",
                    f"{b}x + {a*c}",
                    f"{a+b}x + {a+c}",
                    f"{a*b}x - {a*c}",
                    f"{a*b}x + {a*c + 1}",
                    f"{a*b + 1}x + {a*c}",
                    f"{a*b}x^2 + {a*c}"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"Multiply each term inside the bracket by ${a}$: ${a} \\times {b}x + {a} \\times {c} = {ans}$.")
            else:
                a = random.randint(2, 5)
                b = random.randint(1, 5)
                c = random.randint(2, 5)
                d = random.randint(1, 5)
                q = f"Expand and simplify: $({a}x + {b})({c}x - {d})$"
                coeff_x2 = a * c
                coeff_x = (b * c) - (a * d)
                const = -b * d

                if coeff_x > 0:
                    ans = f"{coeff_x2}x^2 + {coeff_x}x - {abs(const)}"
                elif coeff_x < 0:
                    ans = f"{coeff_x2}x^2 - {abs(coeff_x)}x - {abs(const)}"
                else:
                    ans = f"{coeff_x2}x^2 - {abs(const)}"

                wrong = [
                    f"{coeff_x2}x^2 + {abs(coeff_x) + 1}x - {abs(const)}",
                    f"{coeff_x2}x^2 - {abs(coeff_x) + 1}x - {abs(const)}",
                    f"{coeff_x2}x^2 + {abs(coeff_x) + 2}x - {abs(const)}",
                    f"{coeff_x2}x^2 - {abs(coeff_x) + 2}x - {abs(const)}",
                    f"{coeff_x2 + 1}x^2 + {coeff_x}x - {abs(const)}",
                    f"{coeff_x2}x^2 + {coeff_x}x - {abs(const) + 1}",
                    f"{coeff_x2}x^2 + {coeff_x}x + {abs(const)}"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"Use FOIL: $({a}x)({c}x) + ({a}x)(-{d}) + ({b})({c}x) + ({b})(-{d}) = {ans}$.")

        elif subtopic == "Factorisation":
            if diff == "easy":
                a = random.randint(2, 8)
                b = random.randint(2, 8)
                mult = random.randint(2, 5)
                c1 = a * mult
                c2 = b * mult
                q = f"Factorise by taking out the highest common factor: ${c1}x + {c2}$"
                ans = f"{mult}({a}x + {b})"
                wrong = [
                    f"{mult}({a}x - {b})",
                    f"{mult + 1}({a}x + {b})",
                    f"{mult}({a + 1}x + {b})",
                    f"{mult}({a}x + {b + 1})",
                    f"{mult * 2}({a}x + {b})",
                    f"{mult}({a}x + {b * 2})",
                    f"{a}({mult}x + {b})"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"The highest common factor is ${mult}$. Dividing both terms by ${mult}$ gives ${ans}$.")
            elif diff == "medium":
                a = random.randint(1, 10)
                q = f"Factorise the difference of two squares: $x^2 - {a**2}$"
                ans = f"(x - {a})(x + {a})"
                wrong = [
                    f"(x - {a})(x - {a})",
                    f"(x + {a})(x + {a})",
                    f"(x - {a**2})(x + 1)",
                    f"(x - {a + 1})(x + {a - 1})",
                    f"(x - {a})(x + {a + 1})",
                    f"(x - {a + 1})(x + {a})",
                    f"(x - {a*2})(x + {a*2})"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"Use the rule $a^2 - b^2 = (a - b)(a + b)$. Here $a = x$ and $b = {a}$.")
            else:
                a = random.randint(1, 5)
                b = random.randint(1, 5)
                # (x + a)(x + b) = x^2 + (a+b)x + ab
                q = f"Factorise the trinomial: $x^2 + {a+b}x + {a*b}$"
                ans = f"(x + {a})(x + {b})" if a != b else f"(x + {a})^2"
                wrong = [
                    f"(x - {a})(x - {b})",
                    f"(x + {a})(x - {b})",
                    f"(x - {a})(x + {b})",
                    f"(x + {a+1})(x + {b})",
                    f"(x + {a})(x + {b+1})",
                    f"(x + {a+b})(x + {a*b})",
                    f"(x + {a*b})(x + {a+b})"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", wrong, f"We need two numbers that multiply to ${a*b}$ and add to ${a+b}$. These numbers are ${a}$ and ${b}$.")

        elif subtopic == "Linear equations":
            if diff == "easy":
                a = random.randint(2, 8)
                x = random.randint(-10, 10)
                b = a * x
                q = f"Solve for x: ${a}x = {b}$"
                ans = f"x = {x}"
                wrong = [f"x = {w}" for w in get_wrong_ints(x)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Divide both sides by ${a}$ to get $x = {x}$.")
            elif diff == "medium":
                a = random.randint(2, 6)
                b = random.randint(-10, 10)
                x = random.randint(-5, 5)
                c = a * x + b
                q = f"Solve for x: ${a}x + {b} = {c}$"
                ans = f"x = {x}"
                wrong = [f"x = {w}" for w in get_wrong_ints(x)]
                sign = "+" if b >= 0 else "-"
                gen.add_question(subtopic, diff, q, ans, wrong, f"Subtract ${b}$ from both sides, then divide by ${a}$ to get $x = {x}$.")
            else:
                a = random.randint(2, 5)
                b = random.randint(-5, 5)
                c = random.randint(2, 5)
                x = random.randint(-5, 5)
                # a(x + b) = c*x + d => ax + ab = cx + d => d = ax + ab - cx
                d = a * x + a * b - c * x
                if a == c: continue
                q = f"Solve for x: ${a}(x + {b}) = {c}x + {d}$"
                ans = f"x = {x}"
                wrong = [f"x = {w}" for w in get_wrong_ints(x)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Expand: ${a}x + {a*b} = {c}x + {d}$. Group x terms: ${(a - c)}x = {d - a*b}$. Therefore $x = {x}$.")

        elif subtopic == "Functions and graphs":
            if diff == "easy":
                m = random.randint(-5, 5)
                c = random.randint(-10, 10)
                if m == 0: continue
                q = f"What is the y-intercept of the line $y = {m}x + {c}$?"
                ans = f"(0; {c})"
                wrong = [
                    f"(0; {-c})",
                    f"({c}; 0)",
                    f"({-c}; 0)",
                    f"(0; {m})",
                    f"({m}; 0)",
                    f"(0; {c + 1})",
                    f"(0; {c - 1})"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"The y-intercept occurs where $x = 0$. Substituting $x = 0$ gives $y = {c}$.")
            elif diff == "medium":
                x1 = random.randint(-5, 5)
                y1 = random.randint(-5, 5)
                m = random.randint(-3, 3)
                if m == 0: continue
                x2 = x1 + random.randint(1, 3)
                y2 = y1 + m * (x2 - x1)
                q = f"Calculate the gradient of the line passing through $({x1}; {y1})$ and $({x2}; {y2})$."
                ans = str(m)
                wrong = get_wrong_ints(m)
                gen.add_question(subtopic, diff, q, ans, wrong, f"Gradient $m = \\frac{{y_2 - y_1}}{{x_2 - x_1}} = \\frac{{{y2} - {y1}}}{{{x2} - {x1}}} = {m}$.")
            else:
                m = random.randint(-4, 4)
                if m == 0: continue
                x = random.randint(-5, 5)
                y = random.randint(-5, 5)
                c = y - m * x
                q = f"Find the equation of the line with gradient ${m}$ passing through the point $({x}; {y})$."
                ans = f"y = {m}x + {c}" if c >= 0 else f"y = {m}x - {abs(c)}"
                wrong = [
                    f"y = {m}x + {c + 1}" if c + 1 >= 0 else f"y = {m}x - {abs(c + 1)}",
                    f"y = {m}x + {c - 1}" if c - 1 >= 0 else f"y = {m}x - {abs(c - 1)}",
                    f"y = {-m}x + {c}" if c >= 0 else f"y = {-m}x - {abs(c)}",
                    f"y = {m}x + {-c}" if -c >= 0 else f"y = {m}x - {abs(-c)}",
                    f"y = {c}x + {m}" if m >= 0 else f"y = {c}x - {abs(m)}",
                    f"y = {x}x + {y}" if y >= 0 else f"y = {x}x - {abs(y)}",
                    f"y = {m}x + {c + 2}" if c + 2 >= 0 else f"y = {m}x - {abs(c + 2)}"
                ]
                gen.add_question(subtopic, diff, q, f"${ans}$", [f"${w}$" for w in wrong], f"Use $y = mx + c$. Substitute $m={m}, x={x}, y={y}$: ${y} = {m}({x}) + c$. Solving for $c$ gives $c = {c}$.")

    gen.save_to_json('dataset/grade9/mathematics/patterns_algebra.json')

if __name__ == '__main__':
    generate_numbers_operations()
    generate_patterns_algebra()
    print("Part 1 complete.")

# Space and Shape (Geometry)
def generate_geometry():
    subtopics = [
        "Geometry of straight lines",
        "Triangles and quadrilaterals",
        "Transformations",
        "Constructions",
        "Pythagoras"
    ]
    gen = TopicGenerator("Space and Shape (Geometry)", "GEO", subtopics)

    attempts = 0
    limit = 50000

    while not gen.is_done() and attempts < limit:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]

        if subtopic == "Geometry of straight lines":
            if diff == "easy":
                angle1 = random.randint(30, 150)
                angle2 = 180 - angle1
                q = f"Two angles are on a straight line. If one angle is ${angle1}^\\circ$, what is the size of the other angle?"
                ans = f"{angle2}^\\circ"
                wrong = [f"{w}^\\circ" for w in get_wrong_ints(angle2)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Angles on a straight line add up to $180^\\circ$. $180^\\circ - {angle1}^\\circ = {angle2}^\\circ$.")
            elif diff == "medium":
                x = random.randint(10, 40)
                a = random.randint(2, 4)
                b = random.randint(10, 30)
                c = random.randint(1, 3)
                d = random.randint(10, 30)
                # a*x + b + c*x + d = 180 => (a+c)x + (b+d) = 180
                total_coeff = a + c
                total_const = b + d
                if (180 - total_const) % total_coeff != 0: continue
                x_val = (180 - total_const) // total_coeff
                if x_val <= 0: continue
                q = f"Two angles on a straight line are given as $({a}x + {b})^\\circ$ and $({c}x + {d})^\\circ$. Calculate the value of $x$."
                ans = str(x_val)
                wrong = get_wrong_ints(x_val)
                gen.add_question(subtopic, diff, q, ans, wrong, f"Angles on a straight line add to $180^\\circ$. $({a}x + {b}) + ({c}x + {d}) = 180$. ${total_coeff}x + {total_const} = 180$. ${total_coeff}x = {180 - total_const}$. $x = {x_val}$.")
            else:
                x = random.randint(15, 30)
                a = random.randint(2, 4)
                b = random.randint(10, 30)
                c = random.randint(1, 3)
                d = random.randint(10, 30)
                # vertically opposite angles: a*x + b = c*x + d => (a-c)x = d - b
                if a <= c: continue
                diff_coeff = a - c
                diff_const = d - b
                if diff_const <= 0 or diff_const % diff_coeff != 0: continue
                x_val = diff_const // diff_coeff
                angle = a * x_val + b
                q = f"Two vertically opposite angles are $({a}x + {b})^\\circ$ and $({c}x + {d})^\\circ$. Find the size of the angles."
                ans = f"{angle}^\\circ"
                wrong = [f"{w}^\\circ" for w in get_wrong_ints(angle)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Vertically opposite angles are equal. ${a}x + {b} = {c}x + {d}$. ${diff_coeff}x = {diff_const}$. $x = {x_val}$. The angle is ${a}({x_val}) + {b} = {angle}^\\circ$.")

        elif subtopic == "Triangles and quadrilaterals":
            if diff == "easy":
                a = random.randint(30, 80)
                b = random.randint(30, 80)
                c = 180 - a - b
                q = f"Two angles of a triangle are ${a}^\\circ$ and ${b}^\\circ$. What is the size of the third angle?"
                ans = f"{c}^\\circ"
                wrong = [f"{w}^\\circ" for w in get_wrong_ints(c)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"The sum of angles in a triangle is $180^\\circ$. $180^\\circ - ({a}^\\circ + {b}^\\circ) = {c}^\\circ$.")
            elif diff == "medium":
                a = random.randint(40, 80)
                b = random.randint(40, 80)
                ext = a + b
                q = f"In a triangle, two interior opposite angles are ${a}^\\circ$ and ${b}^\\circ$. Calculate the size of the exterior angle."
                ans = f"{ext}^\\circ"
                wrong = [f"{w}^\\circ" for w in get_wrong_ints(ext)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"The exterior angle of a triangle is equal to the sum of the two interior opposite angles. ${a}^\\circ + {b}^\\circ = {ext}^\\circ$.")
            else:
                base_angle = random.randint(30, 70)
                vertex_angle = 180 - 2 * base_angle
                q = f"An isosceles triangle has a vertex angle of ${vertex_angle}^\\circ$. What is the size of each base angle?"
                ans = f"{base_angle}^\\circ"
                wrong = [f"{w}^\\circ" for w in get_wrong_ints(base_angle)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Base angles of an isosceles triangle are equal. Sum is $180^\\circ$. Base angle $= (180^\\circ - {vertex_angle}^\\circ) \\div 2 = {base_angle}^\\circ$.")

        elif subtopic == "Transformations":
            if diff == "easy":
                x = random.randint(-5, 5)
                y = random.randint(-5, 5)
                q = f"Point $P({x}; {y})$ is translated $2$ units right and $3$ units down. What are the new coordinates $P'$?"
                ans = f"({x + 2}; {y - 3})"
                wrong = [
                    f"({x - 2}; {y + 3})",
                    f"({x + 2}; {y + 3})",
                    f"({x - 2}; {y - 3})",
                    f"({y - 3}; {x + 2})",
                    f"({x + 3}; {y - 2})",
                    f"({x + 2}; {y})",
                    f"({x}; {y - 3})"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Translate $x$: ${x} + 2 = {x + 2}$. Translate $y$: ${y} - 3 = {y - 3}$. Point is $({x + 2}; {y - 3})$.")
            elif diff == "medium":
                x = random.randint(-5, 5)
                y = random.randint(1, 5)
                q = f"Point $A({x}; {y})$ is reflected across the x-axis. What are the coordinates of $A'$?"
                ans = f"({x}; {-y})"
                wrong = [
                    f"({-x}; {y})",
                    f"({-x}; {-y})",
                    f"({y}; {x})",
                    f"({-y}; {-x})",
                    f"({y}; {-x})",
                    f"({-y}; {x})",
                    f"({x}; {y})"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Reflection across the x-axis changes the sign of the y-coordinate: $(x; y) \\rightarrow (x; -y)$. Thus $({x}; {-y})$.")
            else:
                x = random.randint(1, 5)
                y = random.randint(1, 5)
                k = random.randint(2, 4)
                q = f"Point $B({x}; {y})$ is enlarged by a scale factor of ${k}$ through the origin. What are the new coordinates?"
                ans = f"({x * k}; {y * k})"
                wrong = [
                    f"({x + k}; {y + k})",
                    f"({x * k}; {y})",
                    f"({x}; {y * k})",
                    f"({x / k:.1f}; {y / k:.1f})",
                    f"({y * k}; {x * k})",
                    f"({-x * k}; {-y * k})",
                    f"({x * k + 1}; {y * k + 1})"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Multiply both coordinates by the scale factor ${k}$: $({x} \\times {k}; {y} \\times {k}) = ({x * k}; {y * k})$.")

        elif subtopic == "Constructions":
            if diff == "easy":
                angle = random.choice([60, 90, 120])
                q = f"When constructing a ${angle}^\\circ$ angle and bisecting it, what is the size of each resulting angle?"
                ans = f"{angle // 2}^\\circ"
                wrong = [f"{w}^\\circ" for w in get_wrong_ints(angle // 2)]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Bisecting an angle divides it into two equal parts: ${angle}^\\circ \\div 2 = {angle // 2}^\\circ$.")
            elif diff == "medium":
                q = "Which instrument is primarily used to draw a circle with a specific radius?"
                ans = "Pair of compasses"
                wrong = [
                    "Protractor",
                    "Ruler",
                    "Set square",
                    "Divider",
                    "T-square",
                    "French curve",
                    "Vernier caliper"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "A pair of compasses is the standard geometric instrument for drawing circles and arcs.")
            else:
                q = "When constructing a perpendicular bisector of a line segment, what must the radius of the compass be set to?"
                ans = "More than half the length of the line segment"
                wrong = [
                    "Exactly half the length of the line segment",
                    "Exactly the full length of the line segment",
                    "Less than half the length of the line segment",
                    "One third of the length of the line segment",
                    "Any random length",
                    "Double the length of the line segment",
                    "The width of the ruler used"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "To ensure the two arcs intersect above and below the line, the compass width must be set to more than half the length of the segment.")

        elif subtopic == "Pythagoras":
            if diff == "easy":
                # Pyth triples
                triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15)]
                t = random.choice(triples)
                q = f"In a right-angled triangle, the two shorter sides are ${t[0]}$ cm and ${t[1]}$ cm. Calculate the length of the hypotenuse."
                ans = f"{t[2]} cm"
                wrong = [f"{w} cm" for w in get_wrong_ints(t[2])]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Using Pythagoras: $c^2 = a^2 + b^2 = {t[0]}^2 + {t[1]}^2 = {t[0]**2} + {t[1]**2} = {t[2]**2}$. Thus $c = {t[2]}$ cm.")
            elif diff == "medium":
                triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15)]
                t = random.choice(triples)
                # ask for a short side
                q = f"In a right-angled triangle, the hypotenuse is ${t[2]}$ cm and one side is ${t[0]}$ cm. Calculate the length of the other side."
                ans = f"{t[1]} cm"
                wrong = [f"{w} cm" for w in get_wrong_ints(t[1])]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Using Pythagoras: $b^2 = c^2 - a^2 = {t[2]}^2 - {t[0]}^2 = {t[2]**2} - {t[0]**2} = {t[1]**2}$. Thus $b = {t[1]}$ cm.")
            else:
                a = random.randint(4, 10)
                b = random.randint(4, 10)
                q = f"In a right-angled triangle, the two shorter sides are ${a}$ cm and ${b}$ cm. Calculate the length of the hypotenuse correct to 2 decimal places."
                hyp_sq = a**2 + b**2
                ans = round(math.sqrt(hyp_sq), 2)
                wrong = get_wrong_floats(ans, decimals=2)
                gen.add_question(subtopic, diff, q, f"{ans} cm", [f"{w} cm" for w in wrong], f"Using Pythagoras: $c^2 = {a}^2 + {b}^2 = {a**2} + {b**2} = {hyp_sq}$. $c = \\sqrt{{{hyp_sq}}} \\approx {ans}$ cm.")

    gen.save_to_json('dataset/grade9/mathematics/geometry.json')

# Measurement
def generate_measurement():
    subtopics = [
        "Perimeter and area",
        "Surface area and volume",
        "Unit conversions"
    ]
    gen = TopicGenerator("Measurement", "MEAS", subtopics)

    attempts = 0
    limit = 50000

    while not gen.is_done() and attempts < limit:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]

        if subtopic == "Perimeter and area":
            if diff == "easy":
                l = random.randint(5, 20)
                w = random.randint(2, 10)
                q = f"Calculate the area of a rectangle with length ${l}$ cm and width ${w}$ cm."
                ans = l * w
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, f"{ans} cm$^2$", [f"{wr} cm$^2$" for wr in wrong], f"Area $= l \\times w = {l} \\times {w} = {ans}$ cm$^2$.")
            elif diff == "medium":
                r = random.randint(3, 15)
                q = f"Calculate the area of a circle with radius ${r}$ cm. Use $\\pi \\approx 3.14$."
                ans = round(3.14 * r**2, 2)
                wrong = get_wrong_floats(ans, decimals=2)
                gen.add_question(subtopic, diff, q, f"{ans} cm$^2$", [f"{wr} cm$^2$" for wr in wrong], f"Area $= \\pi r^2 \\approx 3.14 \\times ({r})^2 = 3.14 \\times {r**2} = {ans}$ cm$^2$.")
            else:
                b = random.randint(5, 15)
                h = random.randint(4, 12)
                area = (b * h) / 2
                q = f"The area of a triangle is ${area}$ cm$^2$ and its base is ${b}$ cm. Calculate the perpendicular height."
                ans = h
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, f"{ans} cm", [f"{wr} cm" for wr in wrong], f"Area $= \\frac{{1}}{{2}} b h$. So $h = \\frac{{2 \\times \\text{{Area}}}}{{b}} = \\frac{{2 \\times {area}}}{{{b}}} = {ans}$ cm.")

        elif subtopic == "Surface area and volume":
            if diff == "easy":
                s = random.randint(3, 10)
                q = f"Calculate the volume of a cube with side length ${s}$ cm."
                ans = s**3
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, f"{ans} cm$^3$", [f"{wr} cm$^3$" for wr in wrong], f"Volume $= s^3 = {s}^3 = {ans}$ cm$^3$.")
            elif diff == "medium":
                l = random.randint(5, 12)
                w = random.randint(3, 8)
                h = random.randint(2, 6)
                q = f"Calculate the surface area of a rectangular prism with length ${l}$ cm, width ${w}$ cm, and height ${h}$ cm."
                ans = 2 * (l*w + l*h + w*h)
                wrong = get_wrong_ints(ans)
                gen.add_question(subtopic, diff, q, f"{ans} cm$^2$", [f"{wr} cm$^2$" for wr in wrong], f"Surface Area $= 2(lw + lh + wh) = 2({l*w} + {l*h} + {w*h}) = {ans}$ cm$^2$.")
            else:
                r = random.randint(3, 10)
                h = random.randint(5, 15)
                q = f"Calculate the volume of a cylinder with radius ${r}$ cm and height ${h}$ cm. Use $\\pi \\approx 3.14$."
                ans = round(3.14 * (r**2) * h, 2)
                wrong = get_wrong_floats(ans, decimals=2)
                gen.add_question(subtopic, diff, q, f"{ans} cm$^3$", [f"{wr} cm$^3$" for wr in wrong], f"Volume $= \\pi r^2 h \\approx 3.14 \\times ({r})^2 \\times {h} = {ans}$ cm$^3$.")

        elif subtopic == "Unit conversions":
            if diff == "easy":
                cm = random.randint(10, 500)
                q = f"Convert ${cm}$ cm to meters."
                ans = round(cm / 100, 2)
                wrong = get_wrong_floats(ans, decimals=2)
                gen.add_question(subtopic, diff, q, f"{ans} m", [f"{wr} m" for wr in wrong], f"Divide by 100: ${cm} \\div 100 = {ans}$ m.")
            elif diff == "medium":
                ml = random.randint(1500, 9500)
                q = f"Convert ${ml}$ m$\\ell$ to liters."
                ans = round(ml / 1000, 3)
                wrong = get_wrong_floats(ans, decimals=3)
                gen.add_question(subtopic, diff, q, f"{ans} $\\ell$", [f"{wr} $\\ell$" for wr in wrong], f"Divide by 1000: ${ml} \\div 1000 = {ans}$ $\\ell$.")
            else:
                cm2 = random.randint(50, 500) * 100
                q = f"Convert ${cm2}$ cm$^2$ to m$^2$."
                ans = round(cm2 / 10000, 3)
                wrong = get_wrong_floats(ans, decimals=3)
                gen.add_question(subtopic, diff, q, f"{ans} m$^2$", [f"{wr} m$^2$" for wr in wrong], f"Since $1$ m $= 100$ cm, $1$ m$^2 = 100 \\times 100 = 10,000$ cm$^2$. Divide by $10,000$: ${cm2} \\div 10000 = {ans}$ m$^2$.")

    gen.save_to_json('dataset/grade9/mathematics/measurement.json')

# Data Handling
def generate_data_handling():
    subtopics = [
        "Data collection",
        "Graphs and charts",
        "Mean, median, mode",
        "Probability"
    ]
    gen = TopicGenerator("Data Handling", "DATA", subtopics)

    attempts = 0
    limit = 50000

    while not gen.is_done() and attempts < limit:
        attempts += 1
        subtopic = random.choice(subtopics)
        diff = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]

        if subtopic == "Data collection":
            if diff == "easy":
                q = "Which of the following is an example of qualitative data?"
                ans = "Eye color of students"
                wrong = [
                    "Height of students",
                    "Mass of students",
                    "Number of siblings",
                    "Test scores",
                    "Time taken to run 100m",
                    "Age of students"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "Qualitative data describes categories or attributes, such as eye color. The others are numerical (quantitative).")
            elif diff == "medium":
                q = "What is the difference between a population and a sample in data collection?"
                ans = "A population is the entire group, while a sample is a smaller representative subset of the population."
                wrong = [
                    "A population is a small group, while a sample is the entire group.",
                    "A population is qualitative data, while a sample is quantitative data.",
                    "A population is collected via surveys, while a sample is collected via experiments.",
                    "A population is biased, while a sample is unbiased.",
                    "There is no difference; they mean the same thing.",
                    "A sample always includes every member of the population."
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "A population includes all members of a defined group, whereas a sample is a smaller portion chosen to represent the population.")
            else:
                q = "Which data collection method is most likely to introduce selection bias?"
                ans = "Voluntary response survey"
                wrong = [
                    "Simple random sampling",
                    "Stratified sampling",
                    "Systematic sampling",
                    "Cluster sampling",
                    "Random number generator selection",
                    "Selecting every 10th person on a complete list"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "Voluntary response surveys often suffer from bias because only people with strong opinions typically choose to participate.")

        elif subtopic == "Graphs and charts":
            if diff == "easy":
                q = "Which type of graph is best suited for showing the trend of temperature changes over a week?"
                ans = "Line graph"
                wrong = [
                    "Pie chart",
                    "Bar graph",
                    "Histogram",
                    "Scatter plot",
                    "Stem-and-leaf plot",
                    "Box-and-whisker plot"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "Line graphs are ideal for displaying data that changes continuously over time.")
            elif diff == "medium":
                pct = random.randint(10, 40)
                q = f"In a pie chart, what angle at the center represents ${pct}\\%$ of the total data?"
                ans = f"{round(360 * pct / 100)}^\\circ"
                wrong = [
                    f"{round(360 * (pct + 10) / 100)}^\\circ",
                    f"{round(360 * (pct - 10) / 100)}^\\circ",
                    f"{pct}^\\circ",
                    f"{100 - pct}^\\circ",
                    f"{round(180 * pct / 100)}^\\circ",
                    f"{round(100 * pct / 360)}^\\circ",
                    f"{pct * 2}^\\circ"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"A full pie chart is $360^\\circ$. ${pct}\\%$ of $360^\\circ = \\frac{{{pct}}}{{100}} \\times 360 = {round(360 * pct / 100)}^\\circ$.")
            else:
                q = "What is the primary difference between a bar graph and a histogram?"
                ans = "A bar graph shows categorical data with spaces between bars, while a histogram shows continuous data with no spaces between bars."
                wrong = [
                    "A bar graph is vertical, while a histogram is horizontal.",
                    "A bar graph uses lines, while a histogram uses bars.",
                    "A bar graph shows percentages, while a histogram shows frequencies.",
                    "A bar graph is 3D, while a histogram is 2D.",
                    "There is no difference; they are the same graph.",
                    "A bar graph shows continuous data, while a histogram shows categorical data."
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "Histograms group continuous numerical data into bins (intervals) without gaps, whereas bar graphs represent distinct categories with gaps between bars.")

        elif subtopic == "Mean, median, mode":
            if diff == "easy":
                data = [random.randint(2, 10) for _ in range(5)]
                q = f"Find the mean of the data set: ${data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}$"
                ans = sum(data) / 5
                wrong = get_wrong_floats(ans, decimals=1)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"Mean $= \\frac{{\\text{{sum of values}}}}{{\\text{{number of values}}}} = \\frac{{{sum(data)}}}{{5}} = {ans}$.")
            elif diff == "medium":
                data = [random.randint(1, 20) for _ in range(6)]
                data.sort()
                q = f"Find the median of the data set: ${data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}$"
                ans = (data[2] + data[3]) / 2
                wrong = get_wrong_floats(ans, decimals=1)
                gen.add_question(subtopic, diff, q, str(ans), wrong, f"The data is ordered. Since there is an even number of values, the median is the average of the two middle values: $\\frac{{{data[2]} + {data[3]}}}{{2}} = {ans}$.")
            else:
                val1 = random.randint(10, 20)
                val2 = random.randint(21, 30)
                data = [val1, val1, val1, val2, val2, val2]
                random.shuffle(data)
                q = f"Determine the mode(s) of the data set: ${data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}$"
                ans = f"Bimodal: {val1} and {val2}"
                wrong = [
                    f"Only {val1}",
                    f"Only {val2}",
                    f"{sum(data)/6:.1f}",
                    "No mode",
                    f"{(val1 + val2)/2}",
                    f"{val1 + val2}",
                    f"{abs(val1 - val2)}"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"The mode is the most frequent value. Both ${val1}$ and ${val2}$ appear 3 times, so the data set is bimodal.")

        elif subtopic == "Probability":
            if diff == "easy":
                color = random.choice(["red", "blue", "green"])
                count = random.randint(3, 8)
                other_colors = [random.randint(2, 5) for _ in range(2)]
                total = count + sum(other_colors)
                q = f"A bag contains ${count}$ {color} marbles and ${sum(other_colors)}$ other marbles. What is the probability of picking a {color} marble?"
                ans = f"{count}/{total}"
                wrong = [
                    f"{sum(other_colors)}/{total}",
                    f"{count}/{sum(other_colors)}",
                    f"{count + 1}/{total}",
                    f"{count}/{total + 1}",
                    f"{count - 1}/{total}",
                    f"{count}/{total - 1}",
                    "1/2"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, f"Probability $= \\frac{{\\text{{favorable outcomes}}}}{{\\text{{total outcomes}}}} = \\frac{{{count}}}{{{total}}}$.")
            elif diff == "medium":
                q = "A fair six-sided die is rolled. What is the probability of rolling a prime number?"
                ans = "3/6 or 1/2"
                wrong = [
                    "1/6",
                    "2/6 or 1/3",
                    "4/6 or 2/3",
                    "5/6",
                    "1/4",
                    "2/5",
                    "3/5"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "The prime numbers on a die are 2, 3, and 5. There are 3 prime numbers out of 6 possible outcomes, so $P = \\frac{3}{6} = \\frac{1}{2}$.")
            else:
                q = "A card is drawn at random from a standard deck of 52 playing cards. What is the probability of drawing a red face card (Jack, Queen, or King)?"
                ans = "6/52 or 3/26"
                wrong = [
                    "3/52",
                    "12/52 or 3/13",
                    "4/52 or 1/13",
                    "2/52 or 1/26",
                    "8/52 or 2/13",
                    "26/52 or 1/2",
                    "1/52"
                ]
                gen.add_question(subtopic, diff, q, ans, wrong, "There are 3 face cards in each suit. The red suits are Hearts and Diamonds. $3 + 3 = 6$ red face cards. Probability $= \\frac{6}{52} = \\frac{3}{26}$.")

    gen.save_to_json('dataset/grade9/mathematics/data_handling.json')

if __name__ == '__main__':
    generate_numbers_operations()
    generate_patterns_algebra()
    generate_geometry()
    generate_measurement()
    generate_data_handling()
    print("All parts complete.")
