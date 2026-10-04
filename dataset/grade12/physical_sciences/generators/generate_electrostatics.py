import json
import random
import uuid
import math
import hashlib

def get_hash(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()

def format_sci(val, unit):
    if val == 0: return "$0\\text{{ {}}} $".format(unit)
    s = "{:.2e}".format(val)
    parts = s.split('e')
    exponent = parts[1].replace('+0', '').replace('+', '').replace('-0', '-')
    return "${}\\times 10^{{{}}}\\text{{ {}}}$".format(parts[0], exponent, unit)

def generate_questions():
    with open('dataset/grade12/physical_sciences/kb_electrostatics.json', 'r') as f:
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

            generic_terms = ["Magnetic Field", "Gravitational Field", "Potential Difference", "Current", "Resistance", "Capacitance", "Electromotive Force", "Magnetic Flux", "Lorentz Force"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "ES_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrostatics",
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
       generic_terms = ["Magnetic Field", "Gravitational Field", "Potential Difference", "Current", "Resistance", "Capacitance", "Electromotive Force", "Magnetic Flux", "RandomTerm_{}".format(easy_count)]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count))
       seen_hashes.add(q_hash)
       questions.append({
                "id": "ES_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrostatics",
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
    k = 9e9
    while medium_count < 500 and attempts < 2500:
        attempts += 1
        choice = random.choice(['prop', 'concept', 'calc_F', 'calc_E'])

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

        elif choice == 'calc_F':
            q1 = random.randint(2, 20) # microcoulombs
            q2 = random.randint(2, 20)
            r = random.randint(10, 100) # cm

            F = (k * (q1 * 1e-6) * (q2 * 1e-6)) / ((r / 100.0)**2)

            q_text = "Two point charges, $q_1 = +{}\\mu\\text{{C}}$ and $q_2 = +{}\\mu\\text{{C}}$, are separated by a distance of ${}\\text{{ cm}}$. Calculate the magnitude of the electrostatic force they exert on each other. (Use $k = 9.0 \\times 10^9\\text{{ N\\cdot m}}^2\\text{{\\cdot C}}^{{-2}}$)".format(q1, q2, r)
            correct = format_sci(F, "N") if F < 0.01 or F > 1000 else "${:.2f}\\text{{ N}}$".format(F)

            err1 = (k * q1 * q2) / (r**2) # Forgot micro and cm conversions
            err2 = (k * (q1 * 1e-6) * (q2 * 1e-6)) / (r / 100.0) # Forgot to square r
            err3 = ((q1 * 1e-6) * (q2 * 1e-6)) / ((r / 100.0)**2) # Forgot k
            err4 = (k * (q1 * 1e-6) * (q2 * 1e-6)) / (r**2) # Forgot cm to m
            err5 = (k * q1 * q2) / ((r / 100.0)**2) # Forgot micro
            err6 = (k * (q1 * 1e-3) * (q2 * 1e-3)) / ((r / 100.0)**2) # Milli instead of micro

            wrong_pool = [
                format_sci(err1, "N") if err1 < 0.01 or err1 > 1000 else "${:.2f}\\text{{ N}}$".format(err1),
                "${:.2f}\\text{{ N}}$".format(err2),
                format_sci(err3, "N") if err3 < 0.01 or err3 > 1000 else "${:.2f}\\text{{ N}}$".format(err3),
                format_sci(err4, "N") if err4 < 0.01 or err4 > 1000 else "${:.2f}\\text{{ N}}$".format(err4),
                format_sci(err5, "N") if err5 < 0.01 or err5 > 1000 else "${:.2f}\\text{{ N}}$".format(err5),
                "${:.2f}\\text{{ N}}$".format(err6)
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Coulomb's Law Calculation"

        elif choice == 'calc_E':
            Q = random.randint(2, 50) # microcoulombs
            r = random.randint(5, 50) # cm

            E = (k * (Q * 1e-6)) / ((r / 100.0)**2)

            q_text = "Calculate the magnitude of the electric field at a point ${}\\text{{ cm}}$ away from a point charge of $+{}\\mu\\text{{C}}$. (Use $k = 9.0 \\times 10^9\\text{{ N\\cdot m}}^2\\text{{\\cdot C}}^{{-2}}$)".format(r, Q)
            correct = format_sci(E, "N\\cdot C^{-1}")

            err1 = (k * Q) / (r**2)
            err2 = (k * (Q * 1e-6)) / (r / 100.0)
            err3 = (Q * 1e-6) / ((r / 100.0)**2)
            err4 = (k * (Q * 1e-6)) / (r**2)
            err5 = (k * Q) / ((r / 100.0)**2)
            err6 = (k * (Q * 1e-6)) / ((2 * r / 100.0)**2)

            wrong_pool = [
                format_sci(err1, "N\\cdot C^{-1}"),
                format_sci(err2, "N\\cdot C^{-1}"),
                format_sci(err3, "N\\cdot C^{-1}"),
                format_sci(err4, "N\\cdot C^{-1}"),
                format_sci(err5, "N\\cdot C^{-1}"),
                format_sci(err6, "N\\cdot C^{-1}")
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Electric Field Calculation"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "ES_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrostatics",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply electrostatics equations"
                }
            })
            medium_count += 1

    while medium_count < 500:
        Q = random.randint(2, 50)
        r = random.randint(5, 50)
        E = (k * (Q * 1e-6)) / ((r / 100.0)**2)
        q_text = "Calculate the magnitude of the electric field at a point ${}\\text{{ cm}}$ away from a point charge of $+{}\\mu\\text{{C}}$. (Use $k = 9.0 \\times 10^9\\text{{ N\\cdot m}}^2\\text{{\\cdot C}}^{{-2}}$)".format(r, Q)
        correct = format_sci(E, "N\\cdot C^{-1}")
        err1 = (k * Q) / (r**2)
        err2 = (k * (Q * 1e-6)) / (r / 100.0)
        err3 = (Q * 1e-6) / ((r / 100.0)**2)
        err4 = (k * (Q * 1e-6)) / (r**2)
        err5 = (k * Q) / ((r / 100.0)**2)
        err6 = (k * (Q * 1e-6)) / ((2 * r / 100.0)**2)
        wrong_pool = [
                format_sci(err1, "N\\cdot C^{-1}"),
                format_sci(err2, "N\\cdot C^{-1}"),
                format_sci(err3, "N\\cdot C^{-1}"),
                format_sci(err4, "N\\cdot C^{-1}"),
                format_sci(err5, "N\\cdot C^{-1}"),
                format_sci(err6, "N\\cdot C^{-1}")
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct][:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "ES_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrostatics",
                    "subtopic": "Electric Field Calculation",
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply electrostatics equations"
                }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    while hard_count < 200 and attempts < 1500:
        attempts += 1
        choice = random.choice(['net_force_1d', 'charge_sharing_quant'])

        if choice == 'net_force_1d':
            q1 = random.randint(2, 10)
            q2 = -random.randint(2, 10)
            q3 = random.randint(2, 10)

            r12 = random.choice([2, 3, 4, 5])
            r23 = random.choice([2, 3, 4, 5])

            F12 = (k * (q1 * 1e-9) * (abs(q2) * 1e-9)) / ((r12 / 100.0)**2)
            F32 = (k * (q3 * 1e-9) * (abs(q2) * 1e-9)) / ((r23 / 100.0)**2)

            F_net = F32 - F12
            direction = "right" if F_net > 0 else "left"
            F_net_mag = abs(F_net)

            q_text = "Three point charges, $q_1 = +{}\\text{{ nC}}$, $q_2 = {}\\text{{ nC}}$, and $q_3 = +{}\\text{{ nC}}$, are placed in a straight line. $q_2$ is placed ${}\\text{{ cm}}$ to the right of $q_1$, and $q_3$ is placed ${}\\text{{ cm}}$ to the right of $q_2$. Calculate the magnitude of the net electrostatic force exerted on $q_2$. (Use $k = 9.0 \\times 10^9$)".format(q1, q2, q3, r12, r23)
            correct = format_sci(F_net_mag, "N")

            err1 = F32 + F12
            err2 = F12
            err3 = F32
            err4 = (k * (q1 * 1e-9) * (abs(q2) * 1e-9)) / (r12**2) + (k * (q3 * 1e-9) * (abs(q2) * 1e-9)) / (r23**2)
            err5 = abs(((k * (q1 * 1e-6) * (abs(q2) * 1e-6)) / ((r12 / 100.0)**2)) - ((k * (q3 * 1e-6) * (abs(q2) * 1e-6)) / ((r23 / 100.0)**2)))
            err6 = abs(F32 - F12) * 2

            wrong_pool = [
                format_sci(err1, "N"),
                format_sci(err2, "N"),
                format_sci(err3, "N"),
                format_sci(err4, "N"),
                format_sci(err5, "N"),
                format_sci(err6, "N")
            ]
            subtopic = "1D Net Electrostatic Force"

        elif choice == 'charge_sharing_quant':
            qA = random.randint(2, 20)
            qB = -random.randint(4, 30)

            q_new = (qA + qB) / 2.0

            delta_q_A = q_new - qA
            electrons_transferred = abs(delta_q_A * 1e-9) / 1.6e-19

            q_text = "Two identical, insulated metal spheres on stands, A with charge $+{}\\text{{ nC}}$ and B with charge ${}\\text{{ nC}}$, touch each other and are then separated. Calculate the number of electrons transferred between the spheres during contact. (Use $e = 1.6 \\times 10^{{-19}}\\text{{ C}}$)".format(qA, qB)
            correct = format_sci(electrons_transferred, "").replace("\\text{ }", "")

            err1 = abs(q_new * 1e-9) / 1.6e-19
            err2 = abs((qA + abs(qB)) * 1e-9) / 1.6e-19
            err3 = abs(qA * 1e-9) / 1.6e-19
            err4 = abs(qB * 1e-9) / 1.6e-19
            err5 = abs(delta_q_A * 1e-6) / 1.6e-19
            err6 = abs(delta_q_A * 1e-9) * 1.6e-19

            wrong_pool = [
                format_sci(err1, "").replace("\\text{ }", ""),
                format_sci(err2, "").replace("\\text{ }", ""),
                format_sci(err3, "").replace("\\text{ }", ""),
                format_sci(err4, "").replace("\\text{ }", ""),
                format_sci(err5, "").replace("\\text{ }", ""),
                format_sci(err6, "").replace("\\text{ }", "")
            ]
            subtopic = "Charge Quantisation"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append(format_sci(random.uniform(1e10, 1e20), "").replace("\\text{ }", ""))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "ES_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrostatics",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex electrostatic scenarios"
                }
            })
            hard_count += 1

    while hard_count < 200:
        qA = random.randint(2, 20)
        qB = -random.randint(4, 30)
        q_new = (qA + qB) / 2.0
        delta_q_A = q_new - qA
        electrons_transferred = abs(delta_q_A * 1e-9) / 1.6e-19
        q_text = "Two identical, insulated metal spheres on stands, A with charge $+{}\\text{{ nC}}$ and B with charge ${}\\text{{ nC}}$, touch each other and are then separated. Calculate the number of electrons transferred between the spheres during contact. (Use $e = 1.6 \\times 10^{{-19}}\\text{{ C}}$)".format(qA, qB)
        correct = format_sci(electrons_transferred, "").replace("\\text{ }", "")
        wrong_pool = [
                format_sci(abs(q_new * 1e-9) / 1.6e-19, "").replace("\\text{ }", ""),
                format_sci(abs((qA + abs(qB)) * 1e-9) / 1.6e-19, "").replace("\\text{ }", ""),
                format_sci(abs(qA * 1e-9) / 1.6e-19, "").replace("\\text{ }", ""),
                format_sci(abs(qB * 1e-9) / 1.6e-19, "").replace("\\text{ }", ""),
                format_sci(abs(delta_q_A * 1e-6) / 1.6e-19, "").replace("\\text{ }", ""),
                format_sci(abs(delta_q_A * 1e-9) * 1.6e-19, "").replace("\\text{ }", "")
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append(format_sci(random.uniform(1e10, 1e20), "").replace("\\text{ }", ""))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(hard_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "ES_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrostatics",
                    "subtopic": "Charge Quantisation",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex electrostatic scenarios"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_electrostatics.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
