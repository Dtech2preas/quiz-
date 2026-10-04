import json
import random
import uuid
import math
import hashlib

def get_hash(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()

def generate_questions():
    with open('dataset/grade12/physical_sciences/kb_momentum_impulse.json', 'r') as f:
        kb = json.load(f)

    questions = []
    seen_hashes = set()

    # --- EASY: Definitions (300) ---
    easy_count = 0
    attempts = 0
    while easy_count < 300 and attempts < 1000:
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

            generic_terms = ["Work", "Power", "Force", "Inertia", "Kinetic Energy", "Potential Energy", "Acceleration", "Speed", "Displacement"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "MI_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Momentum Impulse",
                    "subtopic": subtopic,
                    "cognitive_level": "Knowledge",
                    "difficulty": "easy",
                    "learning_outcome": "Recall definitions and terminology"
                }
            })
            easy_count += 1

    # We ran out of definitions so we can pad with more duplicates just with different ID/Phrasing if necessary but usually we add variations
    while easy_count < 300:
       item = random.choice(kb['definitions'])
       q_text = "Identify the concept defined by: '{}'".format(item['definition'])
       correct = item['term']
       wrong_pool = [d['term'] for d in kb['definitions'] if d['term'] != correct]
       generic_terms = ["Work", "Power", "Force", "Inertia", "Kinetic Energy", "Potential Energy", "Acceleration", "Speed", "Displacement", f"RandomTerm_{easy_count}"]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count)) # Force uniqueness
       seen_hashes.add(q_hash)
       questions.append({
                "id": "MI_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Momentum Impulse",
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
    while medium_count < 500 and attempts < 2000:
        attempts += 1
        choice = random.choice(['prop', 'concept', 'calc_p'])

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

        elif choice == 'calc_p':
            m = random.randint(5, 500)
            v = random.randint(2, 40)
            p = m * v

            q_text = "An object with a mass of {}\\text{{ kg}} moves at a constant speed of {}\\text{{ m\\cdot s}}^{{-1}}. Calculate the magnitude of its momentum.".format(m, v)
            correct = "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(p)
            wrong_pool = [
                "{:.2f}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(m/v),
                "{:.4f}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(v/m),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(m+v),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(0.5 * m * v**2),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(m * v**2),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(p * 9.8),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(p * 2)
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Momentum Calculation"

        # To avoid infinite loop, make slightly unique string
        q_hash = get_hash(q_text + str(medium_count) if choice != 'calc_p' else q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "MI_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Momentum Impulse",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply momentum concepts"
                }
            })
            medium_count += 1

    while medium_count < 500:
        # Fallback calc_p
        m = random.randint(5, 500)
        v = random.randint(2, 40)
        p = m * v
        q_text = "An object with a mass of {}\\text{{ kg}} moves at a constant speed of {}\\text{{ m\\cdot s}}^{{-1}}. Calculate the magnitude of its momentum.".format(m, v)
        correct = "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(p)
        wrong_pool = [
                "{:.2f}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(m/v),
                "{:.4f}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(v/m),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(m+v),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(0.5 * m * v**2),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(m * v**2),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(p * 9.8),
                "{}\\text{{ kg\\cdot m\\cdot s}}^{{-1}}".format(p * 2)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct][:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "MI_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Momentum Impulse",
                    "subtopic": "Momentum Calculation",
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply momentum concepts"
                }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    while hard_count < 200 and attempts < 1000:
        attempts += 1
        choice = random.choice(['conservation', 'impulse', 'elasticity'])

        if choice == 'conservation':
            m1 = random.randint(2, 10)
            m2 = random.randint(2, 10)
            v1i = random.randint(5, 20)
            v2i = -random.randint(2, 10)
            v1f = -random.randint(1, 5)

            v2f = (m1*v1i + m2*v2i - m1*v1f) / m2

            q_text = "Car A of mass {}\\text{{ kg}} moving east at {}\\text{{ m\\cdot s}}^{{-1}} collides head-on with Car B of mass {}\\text{{ kg}} moving west at {}\\text{{ m\\cdot s}}^{{-1}}. After the collision, Car A moves west at {}\\text{{ m\\cdot s}}^{{-1}}. Calculate the magnitude of the speed of Car B after the collision. Ignore friction.".format(m1, v1i, m2, abs(v2i), abs(v1f))
            correct = "{:.2f}\\text{{ m\\cdot s}}^{{-1}}".format(abs(v2f))

            err1 = (m1*v1i + m2*abs(v2i) - m1*v1f) / m2
            err2 = (m1*v1i + m2*v2i - m1*abs(v1f)) / m2
            err3 = (m1*v1i + m2*abs(v2i) - m1*abs(v1f)) / m2
            err4 = (m1*v1i + m2*v2i + m1*v1f) / m2
            err5 = (m1*v1i - m2*v2i - m1*v1f) / m2
            err6 = (m1*v1f + m2*v2i - m1*v1i) / m2

            wrong_pool = [
                "{:.2f}\\text{{ m\\cdot s}}^{{-1}}".format(abs(err1)),
                "{:.2f}\\text{{ m\\cdot s}}^{{-1}}".format(abs(err2)),
                "{:.2f}\\text{{ m\\cdot s}}^{{-1}}".format(abs(err3)),
                "{:.2f}\\text{{ m\\cdot s}}^{{-1}}".format(abs(err4)),
                "{:.2f}\\text{{ m\\cdot s}}^{{-1}}".format(abs(err5)),
                "{:.2f}\\text{{ m\\cdot s}}^{{-1}}".format(abs(err6))
            ]
            subtopic = "Conservation of Momentum"

        elif choice == 'impulse':
            m = random.randint(50, 1500)
            v_i = random.randint(10, 30)
            v_f = -random.randint(5, 15)
            dt = random.choice([0.1, 0.2, 0.5, 1.0])

            fnet = (m * (v_f - v_i)) / dt

            q_text = "An object of mass {}\\text{{ kg}} is moving east at {}\\text{{ m\\cdot s}}^{{-1}}. It collides with a wall and rebounds west at {}\\text{{ m\\cdot s}}^{{-1}}. The collision lasts for {}\\text{{ s}}. Calculate the magnitude of the average net force exerted by the wall on the object.".format(m, v_i, abs(v_f), dt)
            correct = "{:.2f}\\text{{ N}}".format(abs(fnet))

            err1 = (m * (abs(v_f) - v_i)) / dt
            err2 = (m * (v_i - abs(v_f))) / dt
            err3 = (m * (v_f - v_i)) * dt
            err4 = (m * v_f) / dt
            err5 = (m * v_i) / dt
            err6 = (m * (v_f - v_i))

            wrong_pool = [
                "{:.2f}\\text{{ N}}".format(abs(err1)),
                "{:.2f}\\text{{ N}}".format(abs(err2)),
                "{:.2f}\\text{{ N}}".format(abs(err3)),
                "{:.2f}\\text{{ N}}".format(abs(err4)),
                "{:.2f}\\text{{ N}}".format(abs(err5)),
                "{:.2f}\\text{{ N}}".format(abs(err6))
            ]
            subtopic = "Impulse-Momentum Theorem"

        elif choice == 'elasticity':
            m1 = random.randint(2, 5)
            m2 = random.randint(2, 5)
            v1i = random.randint(4, 10)

            v_f = (m1 * v1i) / (m1 + m2)

            eki = 0.5 * m1 * (v1i**2)
            ekf = 0.5 * (m1 + m2) * (v_f**2)
            delta_ek = eki - ekf

            q_text = "An object of mass {}\\text{{ kg}} moving at {}\\text{{ m\\cdot s}}^{{-1}} collides with a stationary object of mass {}\\text{{ kg}}. They stick together after the collision. Calculate the magnitude of the kinetic energy lost during this collision.".format(m1, v1i, m2)
            correct = "{:.2f}\\text{{ J}}".format(delta_ek)

            err1 = eki
            err2 = ekf
            err3 = eki + ekf
            err4 = (m1 * v1i)
            err5 = 0.5 * m1 * (v1i**2) - 0.5 * m2 * (v_f**2)
            err6 = delta_ek * 2

            wrong_pool = [
                "{:.2f}\\text{{ J}}".format(abs(err1)),
                "{:.2f}\\text{{ J}}".format(abs(err2)),
                "{:.2f}\\text{{ J}}".format(abs(err3)),
                "{:.2f}\\text{{ J}}".format(abs(err4)),
                "{:.2f}\\text{{ J}}".format(abs(err5)),
                "{:.2f}\\text{{ J}}".format(abs(err6))
            ]
            subtopic = "Elastic and Inelastic Collisions"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("{:.2f}".format(random.uniform(10, 1000)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "MI_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Momentum Impulse",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex collision scenarios"
                }
            })
            hard_count += 1

    while hard_count < 200:
        # Fallback
        m = random.randint(50, 1500)
        v_i = random.randint(10, 30)
        v_f = -random.randint(5, 15)
        dt = random.choice([0.1, 0.2, 0.5, 1.0])
        fnet = (m * (v_f - v_i)) / dt
        q_text = "An object of mass {}\\text{{ kg}} is moving east at {}\\text{{ m\\cdot s}}^{{-1}}. It collides with a wall and rebounds west at {}\\text{{ m\\cdot s}}^{{-1}}. The collision lasts for {}\\text{{ s}}. Calculate the magnitude of the average net force exerted by the wall on the object.".format(m, v_i, abs(v_f), dt)
        correct = "{:.2f}\\text{{ N}}".format(abs(fnet))
        err1 = (m * (abs(v_f) - v_i)) / dt
        err2 = (m * (v_i - abs(v_f))) / dt
        err3 = (m * (v_f - v_i)) * dt
        err4 = (m * v_f) / dt
        err5 = (m * v_i) / dt
        err6 = (m * (v_f - v_i))
        wrong_pool = [
                "{:.2f}\\text{{ N}}".format(abs(err1)),
                "{:.2f}\\text{{ N}}".format(abs(err2)),
                "{:.2f}\\text{{ N}}".format(abs(err3)),
                "{:.2f}\\text{{ N}}".format(abs(err4)),
                "{:.2f}\\text{{ N}}".format(abs(err5)),
                "{:.2f}\\text{{ N}}".format(abs(err6))
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("{:.2f}".format(random.uniform(10, 1000)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text + str(hard_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "MI_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Momentum Impulse",
                    "subtopic": "Impulse-Momentum Theorem",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex collision scenarios"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_momentum_impulse.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
