import json
import random
import uuid
import math
import hashlib

def get_hash(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()

def generate_questions():
    with open('dataset/grade12/physical_sciences/kb_electric_circuits.json', 'r') as f:
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

            generic_terms = ["Current", "Voltage", "Resistance", "Power", "Energy", "Capacitance", "Inductance", "Frequency", "Amplitude"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "EC_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electric Circuits",
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
       generic_terms = ["Current", "Voltage", "Resistance", "Power", "Energy", "Capacitance", "Inductance", "Frequency", "RandomTerm_{}".format(easy_count)]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count))
       seen_hashes.add(q_hash)
       questions.append({
                "id": "EC_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electric Circuits",
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
        choice = random.choice(['prop', 'concept', 'calc_R', 'calc_cost'])

        if choice == 'prop':
            item = random.choice(kb['proportionality'])
            q_text = item['statement']
            correct = item['correct']
            wrong_pool = item['distractors'][:6]
            subtopic = "Proportionality & Reasoning"

        elif choice == 'concept':
            item = random.choice(kb['concepts'])
            q_text = item['question']
            correct = item['correct']
            wrong_pool = item['distractors'][:6]
            subtopic = "Conceptual Application"

        elif choice == 'calc_R':
            R1 = random.randint(2, 20)
            R2 = random.randint(2, 20)
            mode = random.choice(['series', 'parallel'])

            if mode == 'series':
                R_eq = R1 + R2
                q_text = "A ${}\\ \\Omega$ resistor and a ${}\\ \\Omega$ resistor are connected in series. Calculate the equivalent resistance of this combination.".format(R1, R2)
                correct = "${:.2f}\\ \\Omega$".format(R_eq)

                err1 = (R1 * R2) / (R1 + R2) # Formula for parallel
                err2 = 1.0 / R1 + 1.0 / R2
                err3 = abs(R1 - R2)
                err4 = R1 * R2
                err5 = R1 / R2
                err6 = R_eq * 2

                wrong_pool = [
                    "${:.2f}\\ \\Omega$".format(err1),
                    "${:.2f}\\ \\Omega$".format(err2),
                    "${:.2f}\\ \\Omega$".format(err3),
                    "${:.2f}\\ \\Omega$".format(err4),
                    "${:.2f}\\ \\Omega$".format(err5),
                    "${:.2f}\\ \\Omega$".format(err6)
                ]
                subtopic = "Series Resistance"
            else:
                R_eq = (R1 * R2) / (R1 + R2)
                q_text = "A ${}\\ \\Omega$ resistor and a ${}\\ \\Omega$ resistor are connected in parallel. Calculate the equivalent resistance of this combination.".format(R1, R2)
                correct = "${:.2f}\\ \\Omega$".format(R_eq)

                err1 = R1 + R2 # Formula for series
                err2 = 1.0 / R1 + 1.0 / R2 # Forgot to invert
                err3 = abs(R1 - R2)
                err4 = R1 * R2
                err5 = R1 / R2
                err6 = R_eq * 2

                wrong_pool = [
                    "${:.2f}\\ \\Omega$".format(err1),
                    "${:.2f}\\ \\Omega$".format(err2),
                    "${:.2f}\\ \\Omega$".format(err3),
                    "${:.2f}\\ \\Omega$".format(err4),
                    "${:.2f}\\ \\Omega$".format(err5),
                    "${:.2f}\\ \\Omega$".format(err6)
                ]
                subtopic = "Parallel Resistance"

        elif choice == 'calc_cost':
            P_W = random.randint(1000, 3000)
            hours = random.randint(2, 8)
            days = random.choice([7, 30])
            rate = random.choice([1.50, 2.10, 2.50])

            P_kW = P_W / 1000.0
            total_time = hours * days
            energy_kWh = P_kW * total_time
            cost = energy_kWh * rate

            q_text = "A geyser rated at ${}\\text{{ W}}$ operates for ${}\\text{{ hours}}$ each day. If electricity costs R${:.2f}$ per kWh, calculate the cost of operating the geyser for ${}\\text{{ days}}$.".format(P_W, hours, rate, days)
            correct = "R${:.2f}$".format(cost)

            err1 = (P_W * total_time) * rate # Forgot to convert W to kW
            err2 = (P_kW * hours) * rate # Forgot to multiply by days
            err3 = (P_kW * total_time) / rate # Divided by rate instead of multiplying
            err4 = (P_W / total_time) * rate
            err5 = P_kW * rate * days # Forgot hours per day
            err6 = (P_W / 1000.0) * rate # Cost per hour only

            wrong_pool = [
                "R${:.2f}$".format(err1),
                "R${:.2f}$".format(err2),
                "R${:.2f}$".format(err3),
                "R${:.2f}$".format(err4),
                "R${:.2f}$".format(err5),
                "R${:.2f}$".format(err6)
            ]
            subtopic = "Cost of Electricity"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("R${:.2f}$".format(random.uniform(10, 1000)) if choice == 'calc_cost' else "${:.2f}\\ \\Omega$".format(random.uniform(1, 100)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "EC_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electric Circuits",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply basic circuit principles"
                }
            })
            medium_count += 1

    while medium_count < 500:
        R1 = random.randint(2, 20)
        R2 = random.randint(2, 20)
        R_eq = R1 + R2
        q_text = "A ${}\\ \\Omega$ resistor and a ${}\\ \\Omega$ resistor are connected in series. Calculate the equivalent resistance of this combination.".format(R1, R2)
        correct = "${:.2f}\\ \\Omega$".format(R_eq)
        err1 = (R1 * R2) / (R1 + R2)
        err2 = 1.0 / R1 + 1.0 / R2
        err3 = abs(R1 - R2)
        err4 = R1 * R2
        err5 = R1 / R2
        err6 = R_eq * 2
        wrong_pool = [
            "${:.2f}\\ \\Omega$".format(err1),
            "${:.2f}\\ \\Omega$".format(err2),
            "${:.2f}\\ \\Omega$".format(err3),
            "${:.2f}\\ \\Omega$".format(err4),
            "${:.2f}\\ \\Omega$".format(err5),
            "${:.2f}\\ \\Omega$".format(err6)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct][:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
            "id": "EC_" + uuid.uuid4().hex[:8],
            "difficulty": "medium",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": wrong_pool,
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "topic": "Paper 1: Electric Circuits",
                "subtopic": "Series Resistance",
                "cognitive_level": "Comprehension",
                "difficulty": "medium",
                "learning_outcome": "Apply basic circuit principles"
            }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    while hard_count < 200 and attempts < 1500:
        attempts += 1
        choice = random.choice(['calc_emf_simultaneous', 'calc_internal_series_parallel'])

        if choice == 'calc_emf_simultaneous':
            # Create a solvable system with nice numbers
            # emf = I1(R1 + r)
            # emf = I2(R2 + r)
            r = random.choice([0.5, 1.0, 1.5, 2.0])
            emf = random.choice([6.0, 9.0, 12.0, 24.0])

            # I = emf / (R + r) => R = (emf / I) - r
            # Pick nice currents
            I1 = random.choice([1.0, 1.5, 2.0, 3.0])
            I2 = random.choice([0.5, 0.8, 1.2, 2.4])

            # Ensure currents lead to positive R
            if emf / I1 - r <= 0 or emf / I2 - r <= 0 or I1 == I2:
                continue

            R1 = (emf / I1) - r
            R2 = (emf / I2) - r

            q_text = "A battery is connected to a variable external resistor. When the external resistance is set to ${:.2f}\\ \\Omega$, an ammeter reads a current of ${:.2f}\\text{{ A}}$. When the external resistance is changed to ${:.2f}\\ \\Omega$, the current drops to ${:.2f}\\text{{ A}}$. Calculate the emf of the battery.".format(R1, I1, R2, I2)
            correct = "${:.2f}\\text{{ V}}$".format(emf)

            # I1(R1+r) = I2(R2+r) => I1*R1 + I1*r = I2*R2 + I2*r => r(I1-I2) = I2*R2 - I1*R1

            err1 = I1 * R1 # Terminal voltage 1
            err2 = I2 * R2 # Terminal voltage 2
            err3 = r # Accidental selection of internal resistance
            err4 = (I1 * R1 + I2 * R2) / 2.0 # Average Vext
            err5 = (I1 * R1) + r # Mixed up math
            err6 = emf * 2

            wrong_pool = [
                "${:.2f}\\text{{ V}}$".format(abs(err1)),
                "${:.2f}\\text{{ V}}$".format(abs(err2)),
                "${:.2f}\\text{{ V}}$".format(abs(err3)),
                "${:.2f}\\text{{ V}}$".format(abs(err4)),
                "${:.2f}\\text{{ V}}$".format(abs(err5)),
                "${:.2f}\\text{{ V}}$".format(abs(err6))
            ]
            subtopic = "Emf and Internal Resistance (Simultaneous Equations)"

        elif choice == 'calc_internal_series_parallel':
            # R_series + (R_p1 || R_p2)
            Rs = random.randint(2, 8)
            Rp1 = random.choice([6, 12, 10, 20])
            Rp2 = random.choice([6, 12, 10, 20])
            if Rp1 == Rp2: Rp2 += 2

            R_p = (Rp1 * Rp2) / float(Rp1 + Rp2)
            R_ext = Rs + R_p

            emf = random.choice([12.0, 24.0])
            r = random.choice([0.5, 1.0, 1.5, 2.0])

            I_tot = emf / (R_ext + r)
            V_ext = I_tot * R_ext

            q_text = "A circuit contains a battery with an emf of ${:.1f}\\text{{ V}}$ and an unknown internal resistance $r$. The external circuit consists of a ${}\\ \\Omega$ resistor connected in series with a parallel combination of a ${}\\ \\Omega$ resistor and a ${}\\ \\Omega$ resistor. A voltmeter across the battery terminals reads ${:.2f}\\text{{ V}}$ when the switch is closed. Calculate the internal resistance ($r$) of the battery.".format(emf, Rs, Rp1, Rp2, V_ext)
            correct = "${:.2f}\\ \\Omega$".format(r)

            err1 = (emf - V_ext) # Lost volts, not resistance
            err2 = V_ext / I_tot # R_ext
            err3 = emf / I_tot # R_total
            err4 = (emf - V_ext) / V_ext # Math error
            err5 = R_ext / I_tot # Random
            err6 = r * 2

            wrong_pool = [
                "${:.2f}\\ \\Omega$".format(abs(err1)),
                "${:.2f}\\ \\Omega$".format(abs(err2)),
                "${:.2f}\\ \\Omega$".format(abs(err3)),
                "${:.2f}\\ \\Omega$".format(abs(err4)),
                "${:.2f}\\ \\Omega$".format(abs(err5)),
                "${:.2f}\\ \\Omega$".format(abs(err6))
            ]
            subtopic = "Internal Resistance in Complex Circuits"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}$".format(random.uniform(0.1, 50)) + ("\\text{ V}" if choice == 'calc_emf_simultaneous' else "\\ \\Omega"))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "EC_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electric Circuits",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate emf, internal resistance and circuit values"
                }
            })
            hard_count += 1

    while hard_count < 200:
        Rs = random.randint(2, 8)
        Rp1 = random.choice([6, 12, 10, 20])
        Rp2 = random.choice([6, 12, 10, 20])
        if Rp1 == Rp2: Rp2 += 2
        R_p = (Rp1 * Rp2) / float(Rp1 + Rp2)
        R_ext = Rs + R_p
        emf = random.choice([12.0, 24.0])
        r = random.choice([0.5, 1.0, 1.5, 2.0])
        I_tot = emf / (R_ext + r)
        V_ext = I_tot * R_ext
        q_text = "A circuit contains a battery with an emf of ${:.1f}\\text{{ V}}$ and an unknown internal resistance $r$. The external circuit consists of a ${}\\ \\Omega$ resistor connected in series with a parallel combination of a ${}\\ \\Omega$ resistor and a ${}\\ \\Omega$ resistor. A voltmeter across the battery terminals reads ${:.2f}\\text{{ V}}$ when the switch is closed. Calculate the internal resistance ($r$) of the battery.".format(emf, Rs, Rp1, Rp2, V_ext)
        correct = "${:.2f}\\ \\Omega$".format(r)
        wrong_pool = [
                "${:.2f}\\ \\Omega$".format(abs((emf - V_ext))),
                "${:.2f}\\ \\Omega$".format(abs(V_ext / I_tot)),
                "${:.2f}\\ \\Omega$".format(abs(emf / I_tot)),
                "${:.2f}\\ \\Omega$".format(abs((emf - V_ext) / V_ext)),
                "${:.2f}\\ \\Omega$".format(abs(R_ext / I_tot)),
                "${:.2f}\\ \\Omega$".format(abs(r * 2))
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}\\ \\Omega$".format(random.uniform(0.1, 50)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(hard_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "EC_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electric Circuits",
                    "subtopic": "Internal Resistance in Complex Circuits",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate emf, internal resistance and circuit values"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_electric_circuits.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
