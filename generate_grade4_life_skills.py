def generate():
    import random
    items = []

    # CAPS Grade 4 Life Skills Topics: Personal and Social Well-being; Physical Education; Creative Arts.
    q_pool = [
        {
            "topic": "Personal and Social Well-being",
            "subtopic": "development of self",
            "q": "Why is it important to respect others?",
            "ans": "It builds positive relationships and a peaceful community.",
            "wrong": ["To get money", "Because it is required by law", "To be popular", "It is only for adults", "To win games", "To avoid homework"],
            "expl": "Respecting others fosters a positive environment and strong friendships."
        },
        {
            "topic": "Physical Education",
            "subtopic": "movement",
            "q": "Which activity is a cardiovascular exercise?",
            "ans": "Running",
            "wrong": ["Sleeping", "Watching TV", "Sitting", "Reading", "Standing still", "Eating"],
            "expl": "Running increases your heart rate and is a great cardiovascular exercise."
        },
        {
            "topic": "Creative Arts",
            "subtopic": "visual arts",
            "q": "Which of these are primary colors?",
            "ans": "Red, Blue, Yellow",
            "wrong": ["Green, Orange, Purple", "Black, White, Gray", "Pink, Brown, Cyan", "Red, Green, Blue", "Yellow, Pink, Black", "White, Red, Orange"],
            "expl": "Red, blue, and yellow are the primary colors that can be mixed to create others."
        }
    ]

    for i in range(50):
        base_q = random.choice(q_pool)

        items.append({
            "id": f"G4_LS_{i}",
            "topic": "Life Skills",
            "subtopic": base_q["subtopic"],
            "difficulty": random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0],
            "question": base_q["q"] + f" ({i})", # Add i to ensure uniqueness
            "correct_answer": base_q["ans"],
            "explanation": base_q["expl"],
            "wrong_answers_pool": base_q["wrong"]
        })

    return items
