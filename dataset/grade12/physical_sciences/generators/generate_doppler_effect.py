import json
import random
import uuid
import math
import hashlib

def get_hash(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()

def generate_questions():
    with open('dataset/grade12/physical_sciences/kb_doppler_effect.json', 'r') as f:
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

            generic_terms = ["Ultrasound", "Wavelength", "Frequency", "Period", "Amplitude", "Electromagnetic Spectrum", "Diffraction", "Refraction", "Interference"]
            while len(wrong_pool) < 6:
                wrong_pool.append(random.choice(generic_terms))
                wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Terminology"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "DE_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Doppler Effect",
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
       generic_terms = ["Ultrasound", "Wavelength", "Frequency", "Period", "Amplitude", "Electromagnetic Spectrum", "Diffraction", "Refraction", "Interference", "RandomTerm_{}".format(easy_count)]
       while len(wrong_pool) < 6:
           wrong_pool.append(random.choice(generic_terms))
           wrong_pool = list(set(wrong_pool))
       wrong_pool = [w for w in wrong_pool if w != correct][:6]
       q_hash = get_hash(q_text + str(easy_count))
       seen_hashes.add(q_hash)
       questions.append({
                "id": "DE_" + uuid.uuid4().hex[:8],
                "difficulty": "easy",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Doppler Effect",
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
        choice = random.choice(['prop', 'concept', 'calc_fL'])

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

        elif choice == 'calc_fL':
            # fL = fS * (v +- vL) / (v +- vS)
            v = random.choice([340, 343])
            f_s = random.randint(300, 1000)
            v_s = random.randint(10, 40)

            # Simple case: Source moving, Listener stationary
            scenario = random.choice(['towards', 'away'])

            if scenario == 'towards':
                f_L = f_s * (v / (v - v_s))
                q_text = "An ambulance travelling along a straight horizontal road at a constant speed of ${}\\text{{ m\\cdot s}}^{{-1}}$ emits sound from its siren at a frequency of ${}\\text{{ Hz}}$. A pedestrian stands stationary beside the road. Calculate the frequency of the sound detected by the pedestrian as the ambulance approaches. (Take the speed of sound in air as ${}\\text{{ m\\cdot s}}^{{-1}}$).".format(v_s, f_s, v)
                correct = "${:.2f}\\text{{ Hz}}$".format(f_L)

                err1 = f_s * (v / (v + v_s)) # Used + instead of -
                err2 = f_s * ((v + v_s) / v) # Put v_s in numerator
                err3 = f_s * ((v - v_s) / v) # Put v_s in numerator and used -
                err4 = f_s * ((v_s) / v)
                err5 = f_s * (v / v_s)
                err6 = f_s * ((v + 10) / (v - v_s)) # Random math

            else:
                f_L = f_s * (v / (v + v_s))
                q_text = "An ambulance travelling along a straight horizontal road at a constant speed of ${}\\text{{ m\\cdot s}}^{{-1}}$ emits sound from its siren at a frequency of ${}\\text{{ Hz}}$. A pedestrian stands stationary beside the road. Calculate the frequency of the sound detected by the pedestrian after the ambulance has passed and is moving away. (Take the speed of sound in air as ${}\\text{{ m\\cdot s}}^{{-1}}$).".format(v_s, f_s, v)
                correct = "${:.2f}\\text{{ Hz}}$".format(f_L)

                err1 = f_s * (v / (v - v_s)) # Used - instead of +
                err2 = f_s * ((v - v_s) / v) # Put v_s in numerator
                err3 = f_s * ((v + v_s) / v) # Put v_s in numerator and used +
                err4 = f_s * ((v_s) / v)
                err5 = f_s * (v / v_s)
                err6 = f_s * ((v - 10) / (v + v_s))

            wrong_pool = [
                "${:.2f}\\text{{ Hz}}$".format(abs(err1)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err2)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err3)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err4)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err5)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err6))
            ]
            wrong_pool = list(set(wrong_pool))
            wrong_pool = [w for w in wrong_pool if w != correct][:6]
            subtopic = "Doppler Calculation (Moving Source)"

        q_hash = get_hash(q_text)
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            questions.append({
                "id": "DE_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Doppler Effect",
                    "subtopic": subtopic,
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply the Doppler effect equation"
                }
            })
            medium_count += 1

    while medium_count < 500:
        v = 340
        f_s = random.randint(300, 1000)
        v_s = random.randint(10, 40)
        f_L = f_s * (v / (v - v_s))
        q_text = "An ambulance travelling along a straight horizontal road at a constant speed of ${}\\text{{ m\\cdot s}}^{{-1}}$ emits sound from its siren at a frequency of ${}\\text{{ Hz}}$. A pedestrian stands stationary beside the road. Calculate the frequency of the sound detected by the pedestrian as the ambulance approaches. (Take the speed of sound in air as ${}\\text{{ m\\cdot s}}^{{-1}}$).".format(v_s, f_s, v)
        correct = "${:.2f}\\text{{ Hz}}$".format(f_L)
        wrong_pool = [
                "${:.2f}\\text{{ Hz}}$".format(abs(f_s * (v / (v + v_s)))),
                "${:.2f}\\text{{ Hz}}$".format(abs(f_s * ((v + v_s) / v))),
                "${:.2f}\\text{{ Hz}}$".format(abs(f_s * ((v - v_s) / v))),
                "${:.2f}\\text{{ Hz}}$".format(abs(f_s * ((v_s) / v))),
                "${:.2f}\\text{{ Hz}}$".format(abs(f_s * (v / v_s))),
                "${:.2f}\\text{{ Hz}}$".format(abs(f_s * ((v + 10) / (v - v_s))))
        ]
        wrong_pool = list(set(wrong_pool))
        wrong_pool = [w for w in wrong_pool if w != correct][:6]
        q_hash = get_hash(q_text + str(medium_count))
        seen_hashes.add(q_hash)
        questions.append({
                "id": "DE_" + uuid.uuid4().hex[:8],
                "difficulty": "medium",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Doppler Effect",
                    "subtopic": "Doppler Calculation",
                    "cognitive_level": "Comprehension",
                    "difficulty": "medium",
                    "learning_outcome": "Apply the Doppler effect equation"
                }
        })
        medium_count += 1

    # --- HARD: Complex Calculations (200) ---
    hard_count = 0
    attempts = 0
    while hard_count < 200 and attempts < 1500:
        attempts += 1
        choice = random.choice(['moving_listener', 'simultaneous_equations'])

        if choice == 'moving_listener':
            v = random.choice([340, 343])
            f_s = random.randint(400, 800)
            v_L = random.randint(15, 35)

            # Listener moving towards stationary source
            f_L = f_s * ((v + v_L) / v)

            q_text = "A stationary factory siren sounds at a frequency of ${}\\text{{ Hz}}$. A driver in a car travels towards the factory at ${}\\text{{ m\\cdot s}}^{{-1}}$. Take the speed of sound in air as ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the frequency heard by the driver.".format(f_s, v_L, v)
            correct = "${:.2f}\\text{{ Hz}}$".format(f_L)

            err1 = f_s * ((v - v_L) / v) # Used - instead of +
            err2 = f_s * (v / (v + v_L)) # Put v_L in denominator
            err3 = f_s * (v / (v - v_L)) # Put v_L in denominator and used -
            err4 = f_s * (v_L / v)
            err5 = f_s * (v / v_L)
            err6 = f_L * 1.5

            wrong_pool = [
                "${:.2f}\\text{{ Hz}}$".format(abs(err1)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err2)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err3)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err4)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err5)),
                "${:.2f}\\text{{ Hz}}$".format(abs(err6))
            ]
            subtopic = "Doppler Calculation (Moving Listener)"

        elif choice == 'simultaneous_equations':
            v = 340
            # We construct a scenario where v_s is the target.
            v_s = random.randint(15, 30)
            f_s = random.randint(500, 900)

            f_L_app = f_s * (v / (v - v_s))
            f_L_away = f_s * (v / (v + v_s))

            # Make the displayed frequencies integers to look like a real exam question
            f_app_display = int(f_L_app)
            f_away_display = int(f_L_away)

            # Recalculate true v_s from the rounded display values so the math works perfectly
            # f_app(v - v_s) = f_away(v + v_s)
            # v_s(f_app + f_away) = v(f_app - f_away)
            # v_s = v(f_app - f_away) / (f_app + f_away)
            v_s_calculated = v * (f_app_display - f_away_display) / (f_app_display + f_away_display)

            q_text = "A whistle emits sound at an unknown frequency. When a train carrying the whistle approaches a stationary observer, the observer hears a frequency of ${}\\text{{ Hz}}$. When the train moves away from the observer at the same speed, the observer hears a frequency of ${}\\text{{ Hz}}$. Take the speed of sound in air as ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the speed of the train.".format(f_app_display, f_away_display, v)
            correct = "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(v_s_calculated)

            # Distractors: common algebra mistakes
            err1 = v * (f_app_display + f_away_display) / (f_app_display - f_away_display) # Flipped numerator and denominator terms
            err2 = v * (f_app_display - f_away_display) / (f_app_display) # Forgot to add them in denominator
            err3 = v * (f_away_display) / (f_app_display + f_away_display)
            err4 = v * (f_app_display) / (f_away_display)
            err5 = (f_app_display - f_away_display) / 2 # Simple average
            err6 = v_s_calculated * 2

            wrong_pool = [
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err1)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err2)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err3)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err4)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err5)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(err6))
            ]
            subtopic = "Simultaneous Equations (Doppler)"

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
                "id": "DE_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Doppler Effect",
                    "subtopic": subtopic,
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex Doppler shift scenarios"
                }
            })
            hard_count += 1

    while hard_count < 200:
        v = 340
        v_s = random.randint(15, 30)
        f_s = random.randint(500, 900)
        f_L_app = f_s * (v / (v - v_s))
        f_L_away = f_s * (v / (v + v_s))
        f_app_display = int(f_L_app)
        f_away_display = int(f_L_away)
        v_s_calculated = v * (f_app_display - f_away_display) / (f_app_display + f_away_display)
        q_text = "A whistle emits sound at an unknown frequency. When a train carrying the whistle approaches a stationary observer, the observer hears a frequency of ${}\\text{{ Hz}}$. When the train moves away from the observer at the same speed, the observer hears a frequency of ${}\\text{{ Hz}}$. Take the speed of sound in air as ${}\\text{{ m\\cdot s}}^{{-1}}$. Calculate the speed of the train.".format(f_app_display, f_away_display, v)
        correct = "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(v_s_calculated)
        wrong_pool = [
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(v * (f_app_display + f_away_display) / (f_app_display - f_away_display))),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(v * (f_app_display - f_away_display) / (f_app_display))),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(v * (f_away_display) / (f_app_display + f_away_display))),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(v * (f_app_display) / (f_away_display))),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs((f_app_display - f_away_display) / 2)),
                "${:.2f}\\text{{ m\\cdot s}}^{{-1}}$".format(abs(v_s_calculated * 2))
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
                "id": "DE_" + uuid.uuid4().hex[:8],
                "difficulty": "hard",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": wrong_pool,
                "tags": {
                    "grade": "12",
                    "subject": "Physical Sciences",
                    "topic": "Paper 1: Doppler Effect",
                    "subtopic": "Simultaneous Equations (Doppler)",
                    "cognitive_level": "Application",
                    "difficulty": "hard",
                    "learning_outcome": "Calculate complex Doppler shift scenarios"
                }
        })
        hard_count += 1

    random.shuffle(questions)

    with open('dataset/grade12/physical_sciences/paper1_doppler_effect.json', 'w') as f:
        json.dump(questions, f, indent=2)

if __name__ == "__main__":
    generate_questions()
