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
    with open('dataset/grade12/physical_sciences/kb_electrodynamics.json', 'r') as f:
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

            generic_terms = ["Capacitance", "Resistance", "Ohm's Law", "Electric Field", "Coulomb's Law", "Direct Current", "Alternating Current", "Transformer", "Electromagnetism"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "ED_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrodynamics",
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
       generic_terms = ["Capacitance", "Resistance", "Ohm's Law", "Electric Field", "Coulomb's Law", "Direct Current", "Alternating Current", "Transformer", "Electromagnetism", "RandomTerm_{}".format(easy_count)]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count))
       seen_hashes.add(q_hash)
       questions.append({
                "id": "ED_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrodynamics",
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
        choice = random.choice(['prop', 'concept', 'calc_rms_V', 'calc_rms_I'])

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

        elif choice == 'calc_rms_V':
            V_max = random.randint(100, 350)
            V_rms = V_max / math.sqrt(2)

            q_text = "An alternating current generator has a maximum voltage output ($V_{{max}}$) of ${}\\text{{ V}}$. Calculate the root-mean-square voltage ($V_{{rms}}$) supplied by the generator.".format(V_max)
            correct = "${:.2f}\\text{{ V}}$".format(V_rms)

            err1 = V_max * math.sqrt(2) # Multiplied instead of divided
            err2 = V_max / 2.0 # Divided by 2 instead of sqrt(2)
            err3 = V_max * 2.0
            err4 = V_max / math.sqrt(3)
            err5 = V_max
            err6 = V_rms * 2.0

            wrong_pool = [
                "${:.2f}\\text{{ V}}$".format(err1),
                "${:.2f}\\text{{ V}}$".format(err2),
                "${:.2f}\\text{{ V}}$".format(err3),
                "${:.2f}\\text{{ V}}$".format(err4),
                "${:.2f}\\text{{ V}}$".format(err5),
                "${:.2f}\\text{{ V}}$".format(err6)
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "RMS Calculations"

        elif choice == 'calc_rms_I':
            I_rms = random.choice([2.5, 3.0, 5.0, 8.5, 10.0, 12.0, 15.0])
            I_max = I_rms * math.sqrt(2)

            q_text = "An electrical appliance draws a root-mean-square current ($I_{{rms}}$) of ${}\\text{{ A}}$. Calculate the peak (maximum) current ($I_{{max}}$) flowing through the appliance.".format(I_rms)
            correct = "${:.2f}\\text{{ A}}$".format(I_max)

            err1 = I_rms / math.sqrt(2) # Divided instead of multiplied
            err2 = I_rms / 2.0
            err3 = I_rms * 2.0
            err4 = I_rms * math.sqrt(3)
            err5 = I_rms
            err6 = I_max * 2.0

            wrong_pool = [
                "${:.2f}\\text{{ A}}$".format(err1),
                "${:.2f}\\text{{ A}}$".format(err2),
                "${:.2f}\\text{{ A}}$".format(err3),
                "${:.2f}\\text{{ A}}$".format(err4),
                "${:.2f}\\text{{ A}}$".format(err5),
                "${:.2f}\\text{{ A}}$".format(err6)
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "RMS Calculations"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "ED_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrodynamics",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply electrodynamics principles"
                }
            })
            medium_count += 1

    while medium_count < 500:
        V_max = random.randint(100, 350)
        V_rms = V_max / math.sqrt(2)
        q_text = "An alternating current generator has a maximum voltage output ($V_{{max}}$) of ${}\\text{{ V}}$. Calculate the root-mean-square voltage ($V_{{rms}}$) supplied by the generator.".format(V_max)
        correct = "${:.2f}\\text{{ V}}$".format(V_rms)
        err1 = V_max * math.sqrt(2)
        err2 = V_max / 2.0
        err3 = V_max * 2.0
        err4 = V_max / math.sqrt(3)
        err5 = V_max
        err6 = V_rms * 2.0
        wrong_pool = [
                "${:.2f}\\text{{ V}}$".format(err1),
                "${:.2f}\\text{{ V}}$".format(err2),
                "${:.2f}\\text{{ V}}$".format(err3),
                "${:.2f}\\text{{ V}}$".format(err4),
                "${:.2f}\\text{{ V}}$".format(err5),
                "${:.2f}\\text{{ V}}$".format(err6)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct][:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "ED_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrodynamics",
                    "subtopic": "RMS Calculations",
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply electrodynamics principles"
                }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    while hard_count < 200 and attempts < 1500:
        attempts += 1
        choice = random.choice(['calc_p_ave', 'calc_p_max', 'calc_flux'])

        if choice == 'calc_p_ave':
            # P_ave = V_rms * I_rms. We give V_max and R.
            # I_rms = V_rms / R
            V_max = random.choice([200, 311, 340, 240])
            R = random.randint(15, 60)

            V_rms = V_max / math.sqrt(2)
            I_rms = V_rms / R
            P_ave = V_rms * I_rms # Or (V_rms)^2 / R

            q_text = "An alternating current generator supplies an electric heater with power. The maximum voltage output ($V_{{max}}$) of the generator is ${}\\text{{ V}}$. The resistance of the heater's element is ${}\\ \\Omega$. Calculate the average power dissipated by the heater.".format(V_max, R)
            correct = "${:.2f}\\text{{ W}}$".format(P_ave)

            err1 = (V_max**2) / R # This is P_max
            err2 = (V_rms) * R # Bad math V = IR implies P = V*R ??
            err3 = (V_max) / R # This is I_max
            err4 = P_ave / math.sqrt(2) # Arbitrary division
            err5 = P_ave * 2 # Also P_max
            err6 = (V_rms**2) * R # Bad formula

            wrong_pool = [
                "${:.2f}\\text{{ W}}$".format(err1),
                "${:.2f}\\text{{ W}}$".format(err2),
                "${:.2f}\\text{{ W}}$".format(err3),
                "${:.2f}\\text{{ W}}$".format(err4),
                "${:.2f}\\text{{ W}}$".format(err5),
                "${:.2f}\\text{{ W}}$".format(err6)
            ]
            subtopic = "AC Power Calculations"

        elif choice == 'calc_p_max':
            # Give P_ave and V_rms, ask for P_max and I_max. Let's just ask for P_max directly.
            # P_max = 2 * P_ave
            P_ave = random.randint(1000, 2500)
            V_rms = random.choice([220, 230, 240])

            P_max = 2 * P_ave

            q_text = "An AC appliance has an average power rating of ${}\\text{{ W}}$ when connected to a ${}\\text{{ V}}$ (rms) domestic wall socket. Calculate the peak (maximum) power dissipated by the appliance.".format(P_ave, V_rms)
            correct = "${:.2f}\\text{{ W}}$".format(P_max)

            err1 = P_ave * math.sqrt(2) # Wrong multiplier
            err2 = P_ave / 2.0
            err3 = P_ave / math.sqrt(2)
            err4 = (V_rms**2) / P_ave # Resistance
            err5 = P_ave / V_rms # I_rms
            err6 = (P_ave / V_rms) * math.sqrt(2) # I_max

            wrong_pool = [
                "${:.2f}\\text{{ W}}$".format(err1),
                "${:.2f}\\text{{ W}}$".format(err2),
                "${:.2f}\\text{{ W}}$".format(err3),
                "${:.2f}\\text{{ W}}$".format(err4),
                "${:.2f}\\text{{ W}}$".format(err5),
                "${:.2f}\\text{{ W}}$".format(err6)
            ]
            subtopic = "AC Power Calculations"

        elif choice == 'calc_flux':
            # Phi = B * A * cos(theta)
            # Area in cm^2
            B = random.uniform(0.1, 0.8)
            side = random.randint(10, 40) # cm, so area = side^2 cm^2
            A_m2 = (side / 100.0)**2
            angle = random.choice([0, 60]) # Angle between normal and field

            flux = B * A_m2 * math.cos(math.radians(angle))

            q_text = "A square coil with side lengths of ${}\\text{{ cm}}$ is placed in a uniform magnetic field of ${:.2f}\\text{{ T}}$. The normal to the surface of the coil makes an angle of ${}^\\circ$ with the magnetic field. Calculate the magnetic flux passing through the coil.".format(side, B, angle)
            correct = format_sci(flux, "Wb")

            err1 = B * (side**2) * math.cos(math.radians(angle)) # Forgot to convert cm^2 to m^2
            err2 = B * A_m2 * math.sin(math.radians(angle)) if angle != 0 else B * A_m2 * 0.5 # Wrong trig
            err3 = B * A_m2 # Forgot angle entirely
            err4 = B * (side/100.0) * math.cos(math.radians(angle)) # Used length instead of area
            err5 = flux * 100 # Bad conversion
            err6 = (B / A_m2) * math.cos(math.radians(angle)) # Divided instead of multiplied

            wrong_pool = [
                format_sci(err1, "Wb"),
                format_sci(err2, "Wb"),
                format_sci(err3, "Wb"),
                format_sci(err4, "Wb"),
                format_sci(err5, "Wb"),
                format_sci(err6, "Wb")
            ]
            subtopic = "Magnetic Flux Calculation"

        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}\\text{{ W}}$".format(random.uniform(10, 10000)) if choice != 'calc_flux' else format_sci(random.uniform(1e-4, 1e-1), "Wb"))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "ED_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrodynamics",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex electrodynamics scenarios"
                }
            })
            hard_count += 1

    while hard_count < 200:
        V_max = random.choice([200, 311, 340, 240])
        R = random.randint(15, 60)
        V_rms = V_max / math.sqrt(2)
        I_rms = V_rms / R
        P_ave = V_rms * I_rms
        q_text = "An alternating current generator supplies an electric heater with power. The maximum voltage output ($V_{{max}}$) of the generator is ${}\\text{{ V}}$. The resistance of the heater's element is ${}\\ \\Omega$. Calculate the average power dissipated by the heater.".format(V_max, R)
        correct = "${:.2f}\\text{{ W}}$".format(P_ave)
        wrong_pool = [
                "${:.2f}\\text{{ W}}$".format((V_max**2) / R),
                "${:.2f}\\text{{ W}}$".format((V_rms) * R),
                "${:.2f}\\text{{ W}}$".format((V_max) / R),
                "${:.2f}\\text{{ W}}$".format(P_ave / math.sqrt(2)),
                "${:.2f}\\text{{ W}}$".format(P_ave * 2),
                "${:.2f}\\text{{ W}}$".format((V_rms**2) * R)
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct]
        while len(wrong_pool) < 6:
             wrong_pool.append("${:.2f}\\text{{ W}}$".format(random.uniform(10, 10000)))
             wrong_pool = list(set(wrong_pool))
        wrong_pool = wrong_pool[:6]
        q_hash = get_hash(q_text + str(hard_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "ED_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Electrodynamics",
                    "subtopic": "AC Power Calculations",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex electrodynamics scenarios"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_electrodynamics.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
