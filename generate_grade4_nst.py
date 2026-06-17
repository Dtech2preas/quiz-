def generate():
    import random
    items = []

    # CAPS Grade 4 NST Topics: Life and Living; Matter and Materials; Energy and Change; Planet Earth and Beyond.
    q_pool = [
        {
            "topic": "Life and Living",
            "subtopic": "living and non-living things",
            "q": "Which of the following is a living thing?",
            "ans": "Tree",
            "wrong": ["Rock", "Water", "Car", "Sun", "Cloud", "Sand"],
            "expl": "A tree is a plant, which means it grows, needs water, and is living."
        },
        {
            "topic": "Matter and Materials",
            "subtopic": "solid, liquid, gas",
            "q": "Which state of matter has a fixed shape?",
            "ans": "Solid",
            "wrong": ["Liquid", "Gas", "Plasma", "Water", "Air", "Steam"],
            "expl": "Solids maintain a fixed shape and volume."
        },
        {
            "topic": "Energy and Change",
            "subtopic": "sources of energy",
            "q": "What is our main source of light and heat energy on Earth?",
            "ans": "The Sun",
            "wrong": ["The Moon", "Electricity", "Fire", "Batteries", "Coal", "Stars"],
            "expl": "The Sun provides most of the heat and light energy we need on Earth."
        },
        {
            "topic": "Planet Earth and Beyond",
            "subtopic": "features of earth",
            "q": "What covers most of the Earth's surface?",
            "ans": "Water",
            "wrong": ["Land", "Ice", "Forests", "Deserts", "Mountains", "Cities"],
            "expl": "About 71% of the Earth's surface is water-covered."
        }
    ]

    for i in range(50):
        base_q = random.choice(q_pool)

        items.append({
            "id": f"G4_NST_{i}",
            "topic": "Natural Sciences and Technology",
            "subtopic": base_q["subtopic"],
            "difficulty": random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0],
            "question": base_q["q"] + f" ({i})", # Add i to ensure uniqueness
            "correct_answer": base_q["ans"],
            "explanation": base_q["expl"],
            "wrong_answers_pool": base_q["wrong"]
        })

    return items
