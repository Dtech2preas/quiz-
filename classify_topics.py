import json

# Topic keywords
TOPIC_KEYWORDS = {
    "Algebra": [
        "factorise", "simplify", "solve", "equation", "inequality", "expand", "product",
        "value of x", "value of y", "calculate x", "calculate y", "expression"
    ],
    "Functions": [
        "function", "graph", "asymptote", "intercept", "inverse", "parabola", "hyperbola",
        "domain", "range", "f(x)", "g(x)", "symmetry", "turning point", "log", "exponential",
        "coordinates", "image", "reflection", "axis of symmetry"
    ],
    "Calculus": [
        "derivative", "differentiate", "gradient", "tangent", "maximum", "minimum",
        "rate of change", "f'(x)", "dy/dx", "first principles", "local", "inflection",
        "dx", "d/dx"
    ],
    "Trigonometry": [
        "sin", "cos", "tan", "trigonometric", "identity", "amplitude", "period", "angle",
        "triangle", "elevation", "depression"
    ],
    "Finance": [
        "interest", "investment", "loan", "annuity", "deposit", "depreciation",
        "future value", "present value", "inflation", "compound", "simple",
        "reducing-balance"
    ]
}

def is_algebra_equation(question):
    # E.g. "3x^2 + 5x = 0"
    if '=' in question and any(var in question for var in ['x', 'y', 'z']):
        if 'T_' not in question and 'P_' not in question:
            return True

    # Mathematical expressions with variables
    if any(var in question for var in ['x', 'y', 'z']) and any(op in question for op in ['+', '-', '*', '/']):
         if 'T_' not in question and 'P_' not in question and 'series' not in question.lower() and 'sequence' not in question.lower():
             return True

    return False

def classify_topic(question):
    q_lower = question.lower()

    # Priority classification based on keyword presence
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in q_lower:
                return topic

    if is_algebra_equation(question):
        return "Algebra"

    return "Unknown"

def process_classification(usable_file):
    with open(usable_file, "r") as f:
        questions = json.load(f)

    classified = {
        "Algebra": [],
        "Functions": [],
        "Calculus": [],
        "Trigonometry": [],
        "Finance": [],
        "Unknown": []
    }

    for q in questions:
        topic = classify_topic(q)
        classified[topic].append(q)

    return classified

if __name__ == "__main__":
    classified = process_classification("usable_questions.json")
    for topic, qs in classified.items():
        print(f"{topic}: {len(qs)}")
        if topic == "Unknown" and qs:
            print(f"\nSample Unknown: {qs[0]}")

    with open("classified_questions.json", "w") as f:
        json.dump(classified, f, indent=4)
