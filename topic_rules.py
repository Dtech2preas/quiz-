# Keyword rules to identify topics
ALGEBRA_KEYWORDS = [
    "factorise", "simplify", "solve", "equation", "inequality", "expand", "product"
]

FUNCTIONS_KEYWORDS = [
    "function", "graph", "asymptote", "intercept", "inverse", "parabola", "hyperbola",
    "domain", "range", "f(x)", "g(x)", "symmetry", "turning point", "log", "exponential"
]

CALCULUS_KEYWORDS = [
    "derivative", "differentiate", "gradient", "tangent", "maximum", "minimum",
    "rate of change", "f'(x)", "dy/dx", "first principles", "local", "inflection"
]

TRIGONOMETRY_KEYWORDS = [
    "sin", "cos", "tan", "trigonometric", "identity", "amplitude", "period", "angle",
    "triangle", "elevation", "depression"
]

FINANCE_KEYWORDS = [
    "interest", "investment", "loan", "annuity", "deposit", "depreciation",
    "future value", "present value", "inflation", "compound", "simple"
]

def classify_topic(question):
    q_lower = question.lower()

    # Priority classification based on keyword presence
    if any(kw in q_lower for kw in FINANCE_KEYWORDS):
        return "Finance"
    if any(kw in q_lower for kw in TRIGONOMETRY_KEYWORDS):
        return "Trigonometry"
    if any(kw in q_lower for kw in CALCULUS_KEYWORDS):
        return "Calculus"
    if any(kw in q_lower for kw in FUNCTIONS_KEYWORDS):
        return "Functions"
    if any(kw in q_lower for kw in ALGEBRA_KEYWORDS):
        return "Algebra"

    return "Unknown"

print(classify_topic("Solve 2x + 6 = 10"))
print(classify_topic("Determine the equations of the asymptotes"))
