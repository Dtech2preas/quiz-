import json
import random
import uuid
import math
import hashlib

def get_hash(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()

def generate_questions():
    with open('dataset/grade12/physical_sciences/kb_work_energy_power.json', 'r') as f:
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

            generic_terms = ["Momentum", "Impulse", "Newton's Second Law", "Velocity", "Acceleration", "Displacement", "Net Force", "Kinetic Friction", "Normal Force"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "WEP_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Work, Energy & Power",
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
       generic_terms = ["Momentum", "Impulse", "Newton's Second Law", "Velocity", "Acceleration", "Displacement", "Net Force", "Kinetic Friction", "Normal Force", "RandomTerm_{}".format(easy_count)]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count))
       seen_hashes.add(q_hash)
       questions.append({
                "id": "WEP_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Work, Energy & Power",
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
        choice = random.choice(['prop', 'concept', 'calc_w', 'calc_p'])

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

        elif choice == 'calc_w':
            F = random.randint(10, 200)
            dx = random.randint(2, 50)
            theta = random.choice([0, 180, 60])

            W = F * dx * math.cos(math.radians(theta))

            if theta == 0:
                q_text = "A constant force of ${}\\text{{ N}}$ acts on an object in the direction of its motion. The object is displaced by ${}\\text{{ m}}$. Calculate the work done by the force.".format(F, dx)
            elif theta == 180:
                q_text = "A constant frictional force of ${}\\text{{ N}}$ acts on a moving object. The object is displaced by ${}\\text{{ m}}$. Calculate the work done by the frictional force.".format(F, dx)
            else:
                q_text = "A constant force of ${}\\text{{ N}}$ acts on an object at an angle of ${}^\\circ$ to the direction of its motion. The object is displaced by ${}\\text{{ m}}$. Calculate the work done by the force.".format(F, theta, dx)

            correct = "${:.2f}\\text{{ J}}$".format(W)

            err1 = F * dx
            err2 = F * dx * math.sin(math.radians(theta)) if theta != 0 else F * dx * 0.5
            err3 = F / dx
            err4 = dx / F
            err5 = -W if W != 0 else -(F*dx)
            err6 = F * dx * math.cos(math.radians(theta + 30))

            wrong_pool = [
                "${:.2f}\\text{{ J}}$".format(err1),
                "${:.2f}\\text{{ J}}$".format(err2),
                "${:.2f}\\text{{ J}}$".format(err3),
                "${:.2f}\\text{{ J}}$".format(err4),
                "${:.2f}\\text{{ J}}$".format(err5),
                "${:.2f}\\text{{ J}}$".format(err6)
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct]
            while len(wrong_pool) < 6:
                wrong_pool.append("${:.2f}\\text{{ J}}$".format(random.uniform(-1000, 1000)))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = wrong_pool[:6]
            subtopic = "Work Calculation"

        elif choice == 'calc_p':
            F = random.randint(500, 5000)
            v_val = random.randint(5, 30)
            P = F * v_val

            q_text = "A vehicle's engine provides a constant driving force of ${}\\text{{ N}}$ to maintain a constant speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the power output of the engine in watts.".format(F, v_val)
            correct = "${}\\text{{ W}}$".format(P)

            err1 = F / v_val
            err2 = v_val / F
            err3 = 0.5 * F * v_val
            err4 = F * v_val**2
            err5 = P / 1000
            err6 = P * 9.8

            wrong_pool = [
                "${:.2f}\\text{{ W}}$".format(err1),
                "${:.4f}\\text{{ W}}$".format(err2),
                "${:.2f}\\text{{ W}}$".format(err3),
                "${:.2f}\\text{{ W}}$".format(err4),
                "${:.2f}\\text{{ W}}$".format(err5),
                "${:.2f}\\text{{ W}}$".format(err6)
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct]
            while len(wrong_pool) < 6:
                wrong_pool.append("${:.2f}\\text{{ W}}$".format(random.uniform(10, 100000)))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = wrong_pool[:6]
            subtopic = "Power Calculation"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "WEP_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Work, Energy & Power",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply work, energy and power concepts"
                }
            })
            medium_count += 1

    while medium_count < 500:
        F = random.randint(10, 200)
        dx = random.randint(2, 50)
        W = F * dx
        q_text = "A constant force of ${}\\text{{ N}}$ acts on an object in the direction of its motion. The object is displaced by ${}\\text{{ m}}$. Calculate the work done by the force.".format(F, dx)
        correct = "${:.2f}\\text{{ J}}$".format(W)
        wrong_pool = [
                "${:.2f}\\text{{ J}}$".format(F/dx),
                "${:.2f}\\text{{ J}}$".format(dx/F),
                "${:.2f}\\text{{ J}}$".format(-W),
                "${:.2f}\\text{{ J}}$".format(F*dx*0.5),
                "${:.2f}\\text{{ J}}$".format(F*dx*9.8),
                "${:.2f}\\text{{ J}}$".format((F*dx)/9.8)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
            wrong_pool.append("${:.2f}\\text{{ J}}$".format(random.uniform(-1000, 1000)))
            wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "WEP_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Work, Energy & Power",
                    "subtopic": "Work Calculation",
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply work, energy and power concepts"
                }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    while hard_count < 200 and attempts < 1500:
        attempts += 1
        choice = random.choice(['work_energy', 'non_conservative', 'power_incline'])

        if choice == 'work_energy':
            m = random.randint(10, 100)
            v_i = random.randint(0, 10)
            v_f = random.randint(12, 30)

            dEk = 0.5 * m * (v_f**2 - v_i**2)

            q_text = "An object of mass ${}\\text{{ kg}}$ accelerates horizontally from ${}\\text{{ m\\cdot s}}^{{-1}}$ to ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the net work done on the object during this acceleration.".format(m, v_i, v_f)
            correct = "${:.2f}\\text{{ J}}$".format(dEk)

            err1 = 0.5 * m * (v_f - v_i)**2
            err2 = m * (v_f - v_i)
            err3 = 0.5 * m * v_f**2
            err4 = 0.5 * m * (v_f**2 + v_i**2)
            err5 = m * 9.8 * (v_f - v_i)
            err6 = dEk * 2

            wrong_pool = [
                "${:.2f}\\text{{ J}}$".format(err1),
                "${:.2f}\\text{{ J}}$".format(err2),
                "${:.2f}\\text{{ J}}$".format(err3),
                "${:.2f}\\text{{ J}}$".format(err4),
                "${:.2f}\\text{{ J}}$".format(err5),
                "${:.2f}\\text{{ J}}$".format(err6)
            ]
            subtopic = "Work-Energy Theorem"

        elif choice == 'non_conservative':
            m = random.randint(50, 150)
            v_i = random.randint(5, 20)
            v_f = 0
            h = random.randint(5, 30)

            dEp = m * 9.8 * h
            dEk = 0.5 * m * (v_f**2 - v_i**2)

            wnc = dEp + dEk

            q_text = "A cyclist of total mass ${}\\text{{ kg}}$ (including bicycle) approaches a hill with a speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. He stops pedalling and coasts up the hill. He comes to a stop at a vertical height of ${}\\text{{ m}}$ above his starting point. Calculate the work done by non-conservative forces (like friction) on the cyclist as he moves up the hill.".format(m, v_i, h)
            correct = "${:.2f}\\text{{ J}}$".format(wnc)

            err1 = dEp
            err2 = dEk
            err3 = abs(dEp - dEk)
            err4 = dEp + abs(dEk)
            err5 = -dEp + dEk
            err6 = m * 9.8 * v_i

            wrong_pool = [
                "${:.2f}\\text{{ J}}$".format(err1),
                "${:.2f}\\text{{ J}}$".format(err2),
                "${:.2f}\\text{{ J}}$".format(err3),
                "${:.2f}\\text{{ J}}$".format(err4),
                "${:.2f}\\text{{ J}}$".format(err5),
                "${:.2f}\\text{{ J}}$".format(err6)
            ]
            subtopic = "Non-Conservative Work"

        elif choice == 'power_incline':
            m = random.randint(1000, 5000)
            v_val = random.randint(10, 30)
            theta = random.randint(5, 15)
            fk = random.randint(500, 2000)

            fg_parallel = m * 9.8 * math.sin(math.radians(theta))
            F_engine = fg_parallel + fk

            P = F_engine * v_val
            P_kw = P / 1000

            q_text = "A truck of mass ${}\\text{{ kg}}$ drives up an incline of ${}^\\circ$ at a constant speed of ${}\\text{{ m\\cdot s}}^{{-1}}$. A constant frictional force of ${}\\text{{ N}}$ acts on the truck. Calculate the power output of the truck's engine in kilowatts (kW).".format(m, theta, v_val, fk)
            correct = "${:.2f}\\text{{ kW}}$".format(P_kw)

            err1 = (m * 9.8 * math.cos(math.radians(theta)) + fk) * v_val / 1000
            err2 = (fk) * v_val / 1000
            err3 = (fg_parallel) * v_val / 1000
            err4 = (fg_parallel - fk) * v_val / 1000
            err5 = P
            err6 = (m * 9.8 + fk) * v_val / 1000

            wrong_pool = [
                "${:.2f}\\text{{ kW}}$".format(err1),
                "${:.2f}\\text{{ kW}}$".format(err2),
                "${:.2f}\\text{{ kW}}$".format(err3),
                "${:.2f}\\text{{ kW}}$".format(err4),
                "${:.2f}\\text{{ kW}}$".format(err5),
                "${:.2f}\\text{{ kW}}$".format(err6)
            ]
            subtopic = "Power on an Incline"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}\\text{{ J}}$".format(random.uniform(-10000, 10000)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "WEP_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Work, Energy & Power",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex energy scenarios"
                }
            })
            hard_count += 1

    while hard_count < 200:
        m = random.randint(10, 100)
        v_i = random.randint(0, 10)
        v_f = random.randint(12, 30)
        dEk = 0.5 * m * (v_f**2 - v_i**2)
        q_text = "An object of mass ${}\\text{{ kg}}$ accelerates horizontally from ${}\\text{{ m\\cdot s}}^{{-1}}$ to ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the net work done on the object during this acceleration.".format(m, v_i, v_f)
        correct = "${:.2f}\\text{{ J}}$".format(dEk)
        err1 = 0.5 * m * (v_f - v_i)**2
        err2 = m * (v_f - v_i)
        err3 = 0.5 * m * v_f**2
        err4 = 0.5 * m * (v_f**2 + v_i**2)
        err5 = m * 9.8 * (v_f - v_i)
        err6 = dEk * 2
        wrong_pool = [
                "${:.2f}\\text{{ J}}$".format(err1),
                "${:.2f}\\text{{ J}}$".format(err2),
                "${:.2f}\\text{{ J}}$".format(err3),
                "${:.2f}\\text{{ J}}$".format(err4),
                "${:.2f}\\text{{ J}}$".format(err5),
                "${:.2f}\\text{{ J}}$".format(err6)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}\\text{{ J}}$".format(random.uniform(-10000, 10000)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(hard_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "WEP_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Work, Energy & Power",
                    "subtopic": "Work-Energy Theorem",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex energy scenarios"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_work_energy_power.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
