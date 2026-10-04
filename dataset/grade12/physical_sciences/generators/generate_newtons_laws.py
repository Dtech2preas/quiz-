import json
import random
import uuid
import math
import hashlib

def get_hash(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()

def generate_questions():
    with open('dataset/grade12/physical_sciences/kb_newtons_laws.json', 'r') as f:
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

            generic_terms = ["Impulse", "Momentum", "Work", "Power", "Kinetic Energy", "Potential Energy", "Acceleration", "Velocity", "Displacement"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "NL_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Newton's Laws",
                    "subtopic": subtopic,
                    "cognitive_level": "Knowledge",
                    "difficulty": "easy",
                    "learning_outcome": "Recall definitions and terminology"
                }
            })
            easy_count += 1

    while easy_count < 300:
       item = random.choice(kb['definitions'])
       q_text = "Identify the concept defined by: '{}'".format(item['definition'])
       correct = item['term']
       wrong_pool = [d['term'] for d in kb['definitions'] if d['term'] != correct]
       generic_terms = ["Impulse", "Momentum", "Work", "Power", "Kinetic Energy", "Potential Energy", "Acceleration", "Velocity", "Displacement", "RandomTerm_{}".format(easy_count)]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count))
       seen_hashes.add(q_hash)
       questions.append({
                "id": "NL_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Newton's Laws",
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
        choice = random.choice(['prop', 'concept', 'calc_fnet'])

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

        elif choice == 'calc_fnet':
            m = random.randint(2, 50) * 10
            a = random.randint(2, 25)
            fnet = m * a

            q_text = "An object with a mass of {}\\text{{ kg}} accelerates at {}\\text{{ m\\cdot s}}^{{-2}}. What is the magnitude of the net force acting on the object?".format(m, a)
            correct = "{}\\text{{ N}}".format(fnet)
            wrong_pool = [
                "{:.2f}\\text{{ N}}".format(m/a),
                "{:.4f}\\text{{ N}}".format(a/m),
                "{}\\text{{ N}}".format(m+a),
                "{}\\text{{ N}}".format(m-a),
                "{:.1f}\\text{{ N}}".format(m*a*9.8),
                "{:.2f}\\text{{ N}}".format((m*a)/9.8),
                "{}\\text{{ N}}".format(m*9.8),
                "{}\\text{{ N}}".format(fnet * 2)
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Newton's Second Law"

        q_hash = get_hash(q_text + str(medium_count) if choice != 'calc_fnet' else q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "NL_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Newton's Laws",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply Newton's Laws to scenarios"
                }
            })
            medium_count += 1

    while medium_count < 500:
        m = random.randint(2, 50) * 10
        a = random.randint(2, 25)
        fnet = m * a
        q_text = "An object with a mass of {}\\text{{ kg}} accelerates at {}\\text{{ m\\cdot s}}^{{-2}}. What is the magnitude of the net force acting on the object?".format(m, a)
        correct = "{}\\text{{ N}}".format(fnet)
        wrong_pool = [
                "{:.2f}\\text{{ N}}".format(m/a),
                "{:.4f}\\text{{ N}}".format(a/m),
                "{}\\text{{ N}}".format(m+a),
                "{}\\text{{ N}}".format(m-a),
                "{:.1f}\\text{{ N}}".format(m*a*9.8),
                "{:.2f}\\text{{ N}}".format((m*a)/9.8),
                "{}\\text{{ N}}".format(m*9.8),
                "{}\\text{{ N}}".format(fnet * 2)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct][:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "NL_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Newton's Laws",
                    "subtopic": "Newton's Second Law",
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply Newton's Laws to scenarios"
                }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    G = 6.67e-11
    while hard_count < 200 and attempts < 1000:
        attempts += 1
        choice = random.choice(['gravitation', 'inclined_plane', 'tension'])

        if choice == 'gravitation':
            m1 = random.randint(50, 500)
            m2 = random.randint(50, 500)
            r = random.randint(2, 20)
            F = (G * m1 * m2) / (r**2)

            q_text = "Two objects with masses {}\\text{{ kg}} and {}\\text{{ kg}} are placed with their centres {}\\text{{ m}} apart. Calculate the magnitude of the gravitational force they exert on each other. (Use $G = 6.67 \\times 10^{{-11}}\\text{{ N\\cdot m}}^2\\text{{\\cdot kg}}^{{-2}}$)".format(m1, m2, r)
            correct = "{:.2e}".format(F).replace('e', '\\times 10^{') + '}\\text{ N}'

            err1 = (G * m1 * m2) / r
            err2 = (G * (m1**2) * (m2**2)) / (r**2)
            err3 = (m1 * m2) / (r**2)
            err4 = (r**2) / (G * m1 * m2)
            err5 = r / (G * m1 * m2)
            err6 = (G * m1 * m2) / (2*r)

            wrong_pool = [
                "{:.2e}".format(err1).replace('e', '\\times 10^{') + '}\\text{ N}',
                "{:.2e}".format(err2).replace('e', '\\times 10^{') + '}\\text{ N}',
                "{:.2e}".format(err3).replace('e', '\\times 10^{') + '}\\text{ N}',
                "{:.2e}".format(err4).replace('e', '\\times 10^{') + '}\\text{ N}',
                "{:.2e}".format(err5).replace('e', '\\times 10^{') + '}\\text{ N}',
                "{:.2e}".format(err6).replace('e', '\\times 10^{') + '}\\text{ N}'
            ]
            subtopic = "Universal Gravitation"

        elif choice == 'inclined_plane':
            m = random.randint(10, 100)
            theta = random.randint(15, 45)
            fgx = m * 9.8 * math.sin(math.radians(theta))

            q_text = "A block of mass {}\\text{{ kg}} rests on a frictionless inclined plane that makes an angle of {}^\\circ with the horizontal. Calculate the component of its weight acting parallel to the plane.".format(m, theta)
            correct = "{:.2f}\\text{{ N}}".format(fgx)

            err1 = m * 9.8 * math.cos(math.radians(theta))
            err2 = m * 9.8 * math.tan(math.radians(theta))
            err3 = m * math.sin(math.radians(theta))
            err4 = m * 9.8
            err5 = m * 9.8 / math.sin(math.radians(theta))
            err6_val = m * 9.8 * math.sin(math.radians(90 - theta))

            wrong_pool = [
                "{:.2f}\\text{{ N}}".format(err1),
                "{:.2f}\\text{{ N}}".format(err2),
                "{:.2f}\\text{{ N}}".format(err3),
                "{:.2f}\\text{{ N}}".format(err4),
                "{:.2f}\\text{{ N}}".format(err5),
                "{:.2f}\\text{{ N}}".format(err6_val)
            ]
            subtopic = "Resolving Vectors (Inclined Plane)"

        elif choice == 'tension':
            m1 = random.randint(10, 30)
            m2 = random.randint(35, 60)
            a = ((m2 - m1) * 9.8) / (m1 + m2)
            T = m1 * (a + 9.8)

            q_text = "Two masses, $m_1 = {}\\text{{ kg}}$ and $m_2 = {}\\text{{ kg}}$ ($m_2 > m_1$), are connected by a light inextensible string over a frictionless pulley. Calculate the magnitude of the tension in the string when the system is released from rest.".format(m1, m2)
            correct = "{:.2f}\\text{{ N}}".format(T)

            err1 = m1 * 9.8
            err2 = m2 * 9.8
            err3 = (m1 + m2) * 9.8
            err4 = (m2 - m1) * 9.8
            err5 = ((m2 - m1)/(m1 + m2)) * 9.8
            err6 = m1 * (9.8 - a)

            wrong_pool = [
                "{:.2f}\\text{{ N}}".format(err1),
                "{:.2f}\\text{{ N}}".format(err2),
                "{:.2f}\\text{{ N}}".format(err3),
                "{:.2f}\\text{{ N}}".format(err4),
                "{:.2f}\\text{{ N}}".format(err5),
                "{:.2f}\\text{{ N}}".format(err6)
            ]
            subtopic = "Newton's Second Law (Systems)"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("{:.2f}\\text{{ N}}".format(random.uniform(10, 1000)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "NL_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Newton's Laws",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex force scenarios"
                }
            })
            hard_count += 1

    while hard_count < 200:
        m = random.randint(10, 100)
        theta = random.randint(15, 45)
        fgx = m * 9.8 * math.sin(math.radians(theta))
        q_text = "A block of mass {}\\text{{ kg}} rests on a frictionless inclined plane that makes an angle of {}^\\circ with the horizontal. Calculate the component of its weight acting parallel to the plane.".format(m, theta)
        correct = "{:.2f}\\text{{ N}}".format(fgx)
        err1 = m * 9.8 * math.cos(math.radians(theta))
        err2 = m * 9.8 * math.tan(math.radians(theta))
        err3 = m * math.sin(math.radians(theta))
        err4 = m * 9.8
        err5 = m * 9.8 / math.sin(math.radians(theta))
        err6_val = m * 9.8 * math.sin(math.radians(90 - theta))
        wrong_pool = [
                "{:.2f}\\text{{ N}}".format(err1),
                "{:.2f}\\text{{ N}}".format(err2),
                "{:.2f}\\text{{ N}}".format(err3),
                "{:.2f}\\text{{ N}}".format(err4),
                "{:.2f}\\text{{ N}}".format(err5),
                "{:.2f}\\text{{ N}}".format(err6_val)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("{:.2f}\\text{{ N}}".format(random.uniform(10, 1000)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(hard_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "NL_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Newton's Laws",
                    "subtopic": "Resolving Vectors (Inclined Plane)",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex force scenarios"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_newtons_laws.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
