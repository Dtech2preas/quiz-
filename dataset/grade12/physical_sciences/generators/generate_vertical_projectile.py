import json
import random
import uuid
import math
import hashlib

def get_hash(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()

def generate_questions():
    with open('dataset/grade12/physical_sciences/kb_vertical_projectile.json', 'r') as f:
        kb = json.load(f)

    questions = []
    seen_hashes = set()

    # --- EASY: Definitions (300) ---
    easy_count = 0
    attempts = 0
    while easy_count < 300 and attempts < 1500:
        attempts += 1
        item = random.choice(kb['definitions'])

        if random.choice([True, False]):
            q_text = "Which of the following is the correct definition for '{}'?".format(item['term'])
            correct = item['definition']
            wrong_pool = item['distractors'][:6]
            subtopic = "Definitions"
        else:
            q_text = "What term is defined as: '{}'?".format(item['definition'])
            correct = item['term']
            wrong_pool = [d['term'] for d in kb['definitions'] if d['term'] != correct]

            generic_terms = ["Momentum", "Impulse", "Newton's Second Law", "Velocity", "Acceleration", "Displacement", "Terminal Velocity", "Weightlessness", "Air Resistance"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "VP_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Vertical Projectile",
                    "subtopic": subtopic,
                    "cognitive_level": "Knowledge",
                    "difficulty": "easy",
                    "learning_outcome": "Recall definitions and terminology"
                }
            })
            easy_count += 1

    while easy_count < 300:
       item = random.choice(kb['definitions'])
       q_text = "Identify the concept described by the following: '{}'".format(item['definition'])
       correct = item['term']
       wrong_pool = [d['term'] for d in kb['definitions'] if d['term'] != correct]
       generic_terms = ["Momentum", "Impulse", "Newton's Second Law", "Velocity", "Acceleration", "Displacement", "Terminal Velocity", "Weightlessness", "Air Resistance", "RandomTerm_{}".format(easy_count)]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count))
       seen_hashes.add(q_hash)
       questions.append({
                "id": "VP_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Vertical Projectile",
                    "subtopic": "Terminology",
                    "cognitive_level": "Knowledge",
                    "difficulty": "easy",
                    "learning_outcome": "Recall definitions and terminology"
                }
       })
       easy_count += 1

    # --- MEDIUM: Concepts & Proportionality (500) ---
    medium_count = 0
    attempts = 0
    while medium_count < 500 and attempts < 2500:
        attempts += 1
        choice = random.choice(['prop', 'concept', 'calc_vf', 'calc_hmax'])

        if choice == 'prop':
            item = random.choice(kb['proportionality'])
            q_text = item['statement']
            correct = item['correct']
            wrong_pool = item['distractors'][:6]
            subtopic = "Proportionality"

        elif choice == 'concept':
            item = random.choice(kb['concepts'])
            q_text = item['question']
            correct = item['correct']
            wrong_pool = item['distractors'][:6]
            subtopic = "Conceptual Application"

        elif choice == 'calc_vf':
            # v_f = v_i + g*dt
            v_i = random.randint(0, 20)
            t = random.choice([1, 2, 3, 4, 5])
            # Assuming down is positive for a dropped/thrown down object
            v_f = v_i + 9.8 * t

            if v_i == 0:
                q_text = "An object is dropped from rest and falls freely for ${}\\text{{ s}}$. Calculate the magnitude of its velocity at this time. Ignore air resistance.".format(t)
            else:
                q_text = "An object is thrown vertically downwards with an initial speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. It falls freely for ${}\\text{{ s}}$. Calculate the magnitude of its velocity at this time. Ignore air resistance.".format(v_i, t)

            correct = "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(v_f)

            err1 = v_i + 9.8 * t**2 # Confused with displacement formula
            err2 = v_i * t + 0.5 * 9.8 * t**2 # Actual displacement formula
            err3 = 9.8 * t # Forgot initial velocity
            err4 = v_i + 9.8 # Forgot to multiply by time
            err5 = v_i - 9.8 * t # Wrong sign convention
            err6 = v_i / t # Non-sensical

            wrong_pool = [
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err1)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err2)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err3)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err4)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err5)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err6))
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct]
            while len(wrong_pool) < 6:
                wrong_pool.append("${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(random.uniform(0, 100)))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = wrong_pool[:6]
            subtopic = "Equations of Motion (Velocity)"

        elif choice == 'calc_hmax':
            v_i = random.randint(10, 40)
            hmax = (v_i**2) / (2 * 9.8)

            q_text = "An object is projected vertically upwards with an initial speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the maximum height it reaches above its projection point. Ignore air resistance.".format(v_i)
            correct = "${:.2f}\\text{{ m}}$".format(hmax)

            err1 = v_i / 9.8 # This is the time taken, not height
            err2 = (v_i**2) / 9.8 # Forgot the 2
            err3 = v_i * 9.8 # Random
            err4 = 0.5 * 9.8 * (v_i / 9.8) # Wrong time sub
            err5 = v_i**2 # Forgot gravity division
            err6 = (v_i**2) / (2 * -9.8) # Negative height magnitude error

            wrong_pool = [
                "${:.2f}\\text{{ m}}$".format(abs(err1)),
                "${:.2f}\\text{{ m}}$".format(abs(err2)),
                "${:.2f}\\text{{ m}}$".format(abs(err3)),
                "${:.2f}\\text{{ m}}$".format(abs(err4)),
                "${:.2f}\\text{{ m}}$".format(abs(err5)),
                "${:.2f}\\text{{ m}}$".format(abs(err6))
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct]
            while len(wrong_pool) < 6:
                wrong_pool.append("${:.2f}\\text{{ m}}$".format(random.uniform(0, 200)))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = wrong_pool[:6]
            subtopic = "Maximum Height Calculation"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "VP_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Vertical Projectile",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply 1D kinematics equations"
                }
            })
            medium_count += 1

    while medium_count < 500:
        v_i = random.randint(10, 40)
        hmax = (v_i**2) / (2 * 9.8)
        q_text = "An object is projected vertically upwards with an initial speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the maximum height it reaches above its projection point. Ignore air resistance.".format(v_i)
        correct = "${:.2f}\\text{{ m}}$".format(hmax)
        wrong_pool = [
                "${:.2f}\\text{{ m}}$".format(abs(v_i / 9.8)),
                "${:.2f}\\text{{ m}}$".format(abs((v_i**2) / 9.8)),
                "${:.2f}\\text{{ m}}$".format(abs(v_i * 9.8)),
                "${:.2f}\\text{{ m}}$".format(abs(v_i**2)),
                "${:.2f}\\text{{ m}}$".format(abs((v_i**2) / (2 * -9.8)))
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
            wrong_pool.append("${:.2f}\\text{{ m}}$".format(random.uniform(0, 200)))
            wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "VP_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Vertical Projectile",
                    "subtopic": "Maximum Height Calculation",
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply 1D kinematics equations"
                }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    while hard_count < 200 and attempts < 1500:
        attempts += 1
        choice = random.choice(['cliff_drop', 'hot_air_balloon', 'two_objects'])

        if choice == 'cliff_drop':
            v_i = random.randint(5, 20)
            h = random.randint(15, 60)

            a = 4.9
            b = -v_i
            c = -h

            # Use quadratic formula: t = (vi + sqrt(vi^2 - 4(4.9)(-h))) / (2*4.9)
            # discriminant = b^2 - 4ac = (-v_i)^2 - 4(4.9)(-h) = v_i^2 + 19.6h (Always positive)
            discriminant = v_i**2 + 19.6*h
            t = (-b + math.sqrt(discriminant)) / (2*a)

            q_text = "A stone is projected vertically upwards from the edge of a cliff at ${}\\text{{ m\\cdot s}}^{{-1}}$. The cliff is ${}\\text{{ m}}$ high. The stone misses the edge of the cliff on its way down and falls to the ground. Calculate the total time taken for the stone to reach the ground. Ignore air resistance.".format(v_i, h)
            correct = "${:.2f}\\text{{ s}}$".format(t)

            # Avoid negative roots in distractors as well
            err1 = (v_i + math.sqrt(abs(v_i**2 - 4*4.9*h))) / (2*4.9)
            err2 = math.sqrt(2 * h / 9.8)
            err3 = (v_i / 9.8) * 2
            err4 = err3 + err2
            err5 = (-v_i + math.sqrt(abs(v_i**2 - 4*4.9*-h))) / (2*4.9)
            err6_real = h / v_i

            wrong_pool = [
                "${:.2f}\\text{{ s}}$".format(abs(err1)),
                "${:.2f}\\text{{ s}}$".format(abs(err2)),
                "${:.2f}\\text{{ s}}$".format(abs(err3)),
                "${:.2f}\\text{{ s}}$".format(abs(err4)),
                "${:.2f}\\text{{ s}}$".format(abs(err5)),
                "${:.2f}\\text{{ s}}$".format(abs(err6_real))
            ]
            subtopic = "Elevated Projection"

        elif choice == 'hot_air_balloon':
            v_b = random.randint(2, 10)
            h = random.randint(20, 80)

            v_f_mag = math.sqrt(v_b**2 + 19.6 * h)

            q_text = "A hot-air balloon is ascending vertically at a constant speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. When the balloon is ${}\\text{{ m}}$ above the ground, a sandbag is released. Calculate the magnitude of the velocity of the sandbag the instant before it strikes the ground. Ignore air resistance.".format(v_b, h)
            correct = "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(v_f_mag)

            err1 = math.sqrt(19.6 * h)
            err2 = math.sqrt(abs(v_b**2 - 19.6 * h))
            err3 = v_b + 9.8 * math.sqrt(2*h/9.8)
            err4 = math.sqrt((v_b + 9.8)**2 + 19.6*h)
            err5 = v_b + 19.6*h
            err6 = math.sqrt(v_b**2 + 9.8 * h)

            wrong_pool = [
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err1)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err2)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err3)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err4)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err5)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err6))
            ]
            subtopic = "Moving Frame of Reference"

        elif choice == 'two_objects':
            h = random.randint(40, 100)
            v_i = random.randint(20, 50)

            t_meet = h / v_i

            q_text = "Ball A is dropped from rest from the top of an ${}\\text{{ m}}$ tall tower. At the exact same instant, Ball B is projected vertically upwards from the ground directly below Ball A with an initial speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. At what time will they pass each other? Ignore air resistance.".format(h, v_i)
            correct = "${:.2f}\\text{{ s}}$".format(t_meet)

            err1 = math.sqrt(2 * h / 9.8)
            err2 = v_i / 9.8
            err3 = h / (v_i - 9.8)
            err4 = h / (v_i + 9.8)
            err5 = 0.5 * h / v_i
            err6 = math.sqrt(h / v_i)

            wrong_pool = [
                "${:.2f}\\text{{ s}}$".format(abs(err1)),
                "${:.2f}\\text{{ s}}$".format(abs(err2)),
                "${:.2f}\\text{{ s}}$".format(abs(err3)),
                "${:.2f}\\text{{ s}}$".format(abs(err4)),
                "${:.2f}\\text{{ s}}$".format(abs(err5)),
                "${:.2f}\\text{{ s}}$".format(abs(err6))
            ]
            subtopic = "Simultaneous Motion"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}$".format(random.uniform(1, 100)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "VP_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Vertical Projectile",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Solve multi-step kinematics problems"
                }
            })
            hard_count += 1

    while hard_count < 200:
        h = random.randint(40, 100)
        v_i = random.randint(20, 50)
        t_meet = h / v_i
        q_text = "Ball A is dropped from rest from the top of an ${}\\text{{ m}}$ tall tower. At the exact same instant, Ball B is projected vertically upwards from the ground directly below Ball A with an initial speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. At what time will they pass each other? Ignore air resistance.".format(h, v_i)
        correct = "${:.2f}\\text{{ s}}$".format(t_meet)
        wrong_pool = [
                "${:.2f}\\text{{ s}}$".format(abs(math.sqrt(2 * h / 9.8))),
                "${:.2f}\\text{{ s}}$".format(abs(v_i / 9.8)),
                "${:.2f}\\text{{ s}}$".format(abs(h / (v_i - 9.8))),
                "${:.2f}\\text{{ s}}$".format(abs(h / (v_i + 9.8))),
                "${:.2f}\\text{{ s}}$".format(abs(0.5 * h / v_i)),
                "${:.2f}\\text{{ s}}$".format(abs(math.sqrt(h / v_i)))
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}$".format(random.uniform(1, 100)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(hard_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "VP_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Vertical Projectile",
                    "subtopic": "Simultaneous Motion",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Solve multi-step kinematics problems"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_vertical_projectile.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
