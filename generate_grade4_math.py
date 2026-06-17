def generate():
    import random
    items = []

    # CAPS Grade 4 Math Topics: Numbers, Operations and Relationships; Patterns, Functions and Algebra; Space and Shape (Geometry); Measurement; Data Handling.
    topics_list = [
        ("Numbers, Operations and Relationships", "addition"),
        ("Numbers, Operations and Relationships", "subtraction"),
        ("Numbers, Operations and Relationships", "multiplication"),
        ("Patterns, Functions and Algebra", "number patterns"),
        ("Measurement", "time")
    ]

    for i in range(50):
        topic_tuple = random.choice(topics_list)
        topic = topic_tuple[0]
        subtopic = topic_tuple[1]

        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]

        if subtopic == "addition":
            a = random.randint(100, 999)
            b = random.randint(100, 999)
            ans = a + b
            q = f"Calculate: {a} + {b} ({i})"
            expl = f"{a} + {b} = {ans}"
        elif subtopic == "subtraction":
            a = random.randint(500, 999)
            b = random.randint(100, 499)
            ans = a - b
            q = f"Calculate: {a} - {b} ({i})"
            expl = f"{a} - {b} = {ans}"
        elif subtopic == "multiplication":
            a = random.randint(10, 99)
            b = random.randint(2, 9)
            ans = a * b
            q = f"Calculate: {a} x {b} ({i})"
            expl = f"{a} x {b} = {ans}"
        elif subtopic == "number patterns":
            start = random.randint(10, 50)
            step = random.randint(2, 10)
            seq = [start + j*step for j in range(4)]
            ans = seq[-1] + step
            q = f"What is the next number in the pattern? {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ({i})"
            expl = f"The pattern increases by {step} each time. {seq[3]} + {step} = {ans}"
        else: # time
            hours = random.randint(1, 10)
            ans = hours * 60
            q = f"How many minutes are there in {hours} hours? ({i})"
            expl = f"1 hour = 60 minutes. {hours} x 60 = {ans}"

        wrong_answers = set()
        while len(wrong_answers) < 6:
            offset = random.randint(-20, 20)
            if offset == 0: continue
            wrong = ans + offset
            if wrong >= 0 and str(wrong) != str(ans):
                wrong_answers.add(str(wrong))

        items.append({
            "id": f"G4_MATH_{i}",
            "topic": "Mathematics",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q,
            "correct_answer": str(ans),
            "explanation": expl,
            "wrong_answers_pool": list(wrong_answers)
        })

    return items
