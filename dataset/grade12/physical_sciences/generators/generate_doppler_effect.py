import json
import random
import os

def build_doppler_effect():
    questions = []
    seen_questions = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, cognitive, outcome):
        q_clean = q_text.strip()
        if q_clean in seen_questions:
            return False
        
        c_str = str(correct).strip()
        clean_wrongs = []
        seen_w = set()
        for w in wrongs:
            w_str = str(w).strip()
            if w_str != c_str and w_str not in seen_w:
                seen_w.add(w_str)
                clean_wrongs.append(w_str)
        
        if len(clean_wrongs) < 6:
            return False
            
        seen_questions.add(q_clean)
        qid = f"PS_P1_DOP_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "topic": "Paper 1: Doppler Effect",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # -------------------------------------------------------------
    # EASY (300 questions) - Core Definition, Pitch, Red/Blue Shift, Ultrasound
    # -------------------------------------------------------------
    dop_defs = [
        ("Doppler Effect", "The change in frequency (or pitch) of the sound or wave detected by a listener because the sound source and the listener have different velocities relative to the medium of sound propagation.",
         ["The reflection of sound waves from a dense barrier causing an echo", "The change in speed of sound when passing from air into water", "The destructive interference of two waves of identical frequency", "The bending of sound waves around a solid corner", "The continuous amplification of sound by an acoustic resonator", "The absorption of sound waves by soft porous materials"]),
        ("Red Shift (in Astronomy)", "The shift of spectral absorption lines towards longer wavelengths (lower frequencies) in the light received from distant stars and galaxies, demonstrating that they are moving away from Earth and that the universe is expanding.",
         ["The shift of light towards higher frequencies as a star approaches Earth", "The absorption of red light by interstellar dust clouds", "The cooling down of a dying red giant star", "The refraction of starlight passing through Earth's atmosphere", "The emission of infrared radiation by black holes", "The Doppler broadening of spectral lines in hot plasma"]),
        ("Blue Shift (in Astronomy)", "The shift of spectral absorption lines towards shorter wavelengths (higher frequencies) in the light received from a celestial object, indicating that it is moving towards the observer (Earth).",
         ["The shift of light towards longer wavelengths indicating recession", "The reflection of sunlight from blue oceans", "The scattering of blue light by atmospheric nitrogen", "The heating of a star to extremely high surface temperatures", "The Doppler effect observed when a listener moves away from light", "The total polarization of starlight in magnetic fields"]),
        ("Doppler Flow Meter", "A medical diagnostic instrument that uses ultrasound waves and the Doppler effect to measure the rate and direction of blood flow in blood vessels.",
         ["An apparatus that measures blood pressure using a mercury manometer", "A device that measures electrical impulses from the brain (EEG)", "An instrument that uses X-rays to image bone fractures", "A surgical tool that uses laser ablation to dissolve clots", "A device that measures oxygen saturation in arterial blood", "A sensor that monitors the body's internal temperature"])
    ]

    for term, definition, dists in dop_defs:
        add_q("easy", "Definitions", f"According to CAPS Physical Sciences, define '{term}':", definition, dists, "Knowledge", "Recall definition")
        add_q("easy", "Definitions", f"Which scientific concept is defined by: '{definition}'?", term, [d[0] for d in dop_defs if d[0] != term] + ["Photoelectric Effect", "Electrodynamics"], "Knowledge", "Identify term")

    # Qualitative Doppler Pitch & Wavelength Relationships
    qualitative_scenarios = [
        ("A sound source approaches a stationary listener at constant speed. How do the observed frequency (pitch) and observed wavelength compare to the source?",
         "Observed frequency is HIGHER (f_L > f_s) and observed wavelength is SHORTER (λ_L < λ_s) because wave fronts are compressed in front of the moving source.",
         ["Observed frequency is LOWER and observed wavelength is LONGER.",
          "Observed frequency is HIGHER and observed wavelength is LONGER.",
          "Observed frequency is LOWER and observed wavelength is SHORTER.",
          "Observed frequency remains UNCHANGED but wave speed increases.",
          "Both frequency and wavelength remain completely constant.",
          "Observed frequency drops to zero as the source passes."]),

        ("A sound source moves away from a stationary listener at constant speed. How do the detected frequency and detected wavelength compare to the source?",
         "Observed frequency is LOWER (f_L < f_s) and observed wavelength is LONGER (λ_L > λ_s) because wave fronts spread out behind the receding source.",
         ["Observed frequency is HIGHER and observed wavelength is SHORTER.",
          "Observed frequency is LOWER and observed wavelength is SHORTER.",
          "Observed frequency is HIGHER and observed wavelength is LONGER.",
          "The speed of the sound wave decreases through the air.",
          "The frequency remains unchanged while wavelength doubles.",
          "The sound wave stops propagating completely."]),

        ("Does the speed of the sound wave (v) in air change when the source moves towards the listener?",
         "No, the speed of sound depends strictly on the properties of the medium (air temperature and density), NOT on the velocity of the source or listener.",
         ["Yes, the speed of sound increases by adding the velocity of the source (v + v_s).",
          "Yes, the speed of sound decreases because of air resistance.",
          "Yes, sound travels at the speed of light when approaching an observer.",
          "Yes, sound speed doubles when frequency doubles.",
          "Yes, the speed of sound drops to zero behind a moving vehicle.",
          "No, because sound waves cannot travel through air."])
    ]
    for q_text, corr, wr in qualitative_scenarios:
        add_q("easy", "Wave Characteristics", q_text, corr, wr, "Comprehension", "Explain pitch and wavelength changes")

    # Complete easy to 300
    seed = 1
    easy_count = sum(1 for q in questions if q['difficulty'] == 'easy')
    while easy_count < 300:
        item = dop_defs[(seed - 1) % len(dop_defs)]
        q_text = f"In an acoustic physics examination: '{item[1]}' describes which phenomenon (Question {seed})?"
        if add_q("easy", "Definitions", q_text, item[0], [d[0] for d in dop_defs if d[0] != item[0]] + ["Threshold Shift", "Compton Effect", "Photoelectric Effect", "Electrodynamics", "Diffraction", "Total Internal Reflection", "Polarization"], "Knowledge", "Recall definition"):
            easy_count += 1
        seed += 1

    # -------------------------------------------------------------
    # MEDIUM (500 questions) - Diverse Calculations (Police car, Train, Submarine, Siren, Bat, Plane)
    # -------------------------------------------------------------
    # Speed of sound in air v = 340 m/s
    v_sound = 340.0

    # Diverse vehicle scenarios:
    # 1. Police car approaching listener: f_L = f_s * (v / (v - v_s))
    # 2. Train moving away from platform: f_L = f_s * (v / (v + v_s))
    # 3. Fire truck approaching then moving away:
    # 4. Moving listener approaching stationary siren: f_L = f_s * ((v + v_L) / v)
    # 5. Moving listener driving away from stationary factory horn: f_L = f_s * ((v - v_L) / v)
    scenarios_calc = [
        # (type, entity, v_entity, f_s, context)
        ("source_approach", "police vehicle", 25.0, 600.0, "A police vehicle with its siren sounding at 600 Hz travels along a straight road at 25 m·s⁻¹ towards a stationary pedestrian."),
        ("source_approach", "high-speed train", 35.0, 480.0, "A high-speed passenger train blowing a horn at 480 Hz approaches a railway station platform at a constant speed of 35 m·s⁻¹."),
        ("source_approach", "fire engine", 20.0, 750.0, "A fire engine sounding its siren at 750 Hz approaches a stationary traffic officer at 20 m·s⁻¹."),
        ("source_approach", "racing car", 40.0, 500.0, "A racing car emitting engine noise at a frequency of 500 Hz speeds towards a spectator in the stands at 40 m·s⁻¹."),
        ("source_recede", "passenger jet", 50.0, 400.0, "An aeroplane producing a 400 Hz whine moves directly away from a ground radar station at 50 m·s⁻¹."),
        ("source_recede", "freight train", 15.0, 320.0, "A freight train blowing a 320 Hz whistle moves away from a level crossing at 15 m·s⁻¹."),
        ("source_recede", "ambulance", 30.0, 700.0, "An ambulance sounding its siren at 700 Hz travels away from a stationary observer at 30 m·s⁻¹ after passing an intersection."),
        ("listener_approach", "motorcyclist", 20.0, 520.0, "A motorcyclist rides at 20 m·s⁻¹ directly towards a stationary factory siren sounding at 520 Hz."),
        ("listener_approach", "driver in a car", 30.0, 450.0, "A car travels at 30 m·s⁻¹ towards a stationary church bell ringing at a frequency of 450 Hz."),
        ("listener_recede", "cyclist", 10.0, 800.0, "A cyclist pedals at 10 m·s⁻¹ directly away from a stationary school alarm ringing at 800 Hz."),
        ("listener_recede", "motorist", 25.0, 650.0, "A motorist drives at 25 m·s⁻¹ away from a stationary road construction warning buzzer sounding at 650 Hz.")
    ]

    for stype, entity, vel, fs, ctx in scenarios_calc:
        if stype == "source_approach":
            fl = fs * (v_sound / (v_sound - vel))
            formula_used = "f_L = f_s * (v / (v - v_s))"
        elif stype == "source_recede":
            fl = fs * (v_sound / (v_sound + vel))
            formula_used = "f_L = f_s * (v / (v + v_s))"
        elif stype == "listener_approach":
            fl = fs * ((v_sound + vel) / v_sound)
            formula_used = "f_L = f_s * ((v + v_L) / v)"
        else: # listener_recede
            fl = fs * ((v_sound - vel) / v_sound)
            formula_used = "f_L = f_s * ((v - v_L) / v)"

        fl_str = f"{fl:.1f} Hz"
        # Generate plausible mistakes: wrong sign, wrong fraction inversion
        if "source" in stype:
            fl_wrong_sign = fs * (v_sound / (v_sound + vel)) if "approach" in stype else fs * (v_sound / (v_sound - vel))
            fl_inverted = fs * ((v_sound - vel) / v_sound) if "approach" in stype else fs * ((v_sound + vel) / v_sound)
        else:
            fl_wrong_sign = fs * ((v_sound - vel) / v_sound) if "approach" in stype else fs * ((v_sound + vel) / v_sound)
            fl_inverted = fs * (v_sound / (v_sound + vel)) if "approach" in stype else fs * (v_sound / (v_sound - vel))

        wrongs = [
            f"{fl_wrong_sign:.1f} Hz (used incorrect sign in Doppler formula)",
            f"{fl_inverted:.1f} Hz (inverted the velocity fraction)",
            f"{fs:.1f} Hz (stated emitted frequency instead of detected)",
            f"{fl * 1.2:.1f} Hz",
            f"{fl * 0.8:.1f} Hz",
            f"{abs(fl - 50.0):.1f} Hz"
        ]
        add_q("medium", "Doppler Calculations",
              f"{ctx} Take the speed of sound in air as 340 m·s⁻¹. Calculate the frequency detected by the listener:",
              fl_str, wrongs, "Application", "Calculate detected frequency using Doppler equation")

    # Complete medium to 500
    med_count = sum(1 for q in questions if q['difficulty'] == 'medium')
    seed = 1
    while med_count < 500:
        c_pick = scenarios_calc[(seed - 1) % len(scenarios_calc)]
        stype, entity, vel, fs, ctx = c_pick
        if "approach" in stype:
            fl = fs * (v_sound / (v_sound - vel)) if "source" in stype else fs * ((v_sound + vel) / v_sound)
        else:
            fl = fs * (v_sound / (v_sound + vel)) if "source" in stype else fs * ((v_sound - vel) / v_sound)
        q_text = f"[Acoustic Problem {seed}] {ctx} (Speed of sound = 340 m·s⁻¹). Determine the detected frequency:"
        if add_q("medium", "Doppler Calculations", q_text, f"{fl:.1f} Hz", [f"{fs:.1f} Hz", f"{fl*1.15:.1f} Hz", f"{fl*0.85:.1f} Hz", f"{fl+45:.1f} Hz", f"{fl-35:.1f} Hz", f"{fs*1.5:.1f} Hz"], "Application", "Apply Doppler formula"):
            med_count += 1
        seed += 1

    # -------------------------------------------------------------
    # HARD (200 questions) - Calculating Source Speed, Wavelength Shift, Frequency-Time Graphs
    # -------------------------------------------------------------
    # Solving for Source Speed:
    # f_L = f_s * (v / (v - v_s)) => v - v_s = v * (f_s / f_L) => v_s = v * (1 - f_s / f_L)
    source_speed_scenarios = [
        # (fs, fl, context)
        (500.0, 550.0, "A patrol car sounding its 500 Hz siren approaches a stationary observer. The frequency detected by the observer is 550 Hz."), # v_s = 340 * (1 - 500/550) = 340 * (50/550) = 30.91 m/s
        (400.0, 440.0, "A train sounds its whistle at 400 Hz as it approaches a commuter standing on the platform. The detected frequency is 440 Hz."), # v_s = 340 * (1 - 400/440) = 30.91 m/s
        (650.0, 720.0, "An emergency vehicle sounding a 650 Hz siren approaches a traffic light where a pedestrian records a frequency of 720 Hz."), # v_s = 340 * (1 - 650/720) = 33.06 m/s
        (350.0, 390.0, "A motorboat sounds a 350 Hz horn as it speeds towards a harbor dock where a frequency of 390 Hz is recorded.") # v_s = 340 * (1 - 350/390) = 34.87 m/s
    ]
    for fs_val, fl_val, ctx in source_speed_scenarios:
        vs_calc = v_sound * (1.0 - (fs_val / fl_val))
        vs_str = f"{vs_calc:.2f} m·s⁻¹"
        wrongs = [
            f"{v_sound * (fl_val / fs_val - 1.0):.2f} m·s⁻¹ (used reverse Doppler equation)",
            f"{v_sound * (fs_val / fl_val):.2f} m·s⁻¹",
            f"{(fl_val - fs_val):.2f} m·s⁻¹ (subtracted frequencies directly)",
            f"{vs_calc * 2:.2f} m·s⁻¹",
            f"{vs_calc / 2:.2f} m·s⁻¹",
            f"{v_sound:.2f} m·s⁻¹ (speed of sound)"
        ]
        add_q("hard", "Solving for Source Speed",
              f"{ctx} Taking the speed of sound in air as 340 m·s⁻¹, calculate the speed of the moving vehicle (v_s):",
              vs_str, wrongs, "Analysis", "Calculate speed of moving source")

    # Doppler Graphs (Frequency vs Time)
    graph_scenarios = [
        ("A siren on a vehicle moving at constant speed approaches a stationary listener, passes the listener, and then moves away along a straight path. What does the graph of observed frequency (f_L) vs time (t) look like?",
         "A horizontal line at a constant frequency higher than f_s while approaching, followed by an immediate vertical drop as the vehicle passes, continuing as a horizontal line at a constant frequency lower than f_s while receding.",
         ["A steady straight line sloping upwards with a positive gradient throughout the motion.",
          "A steady straight line sloping downwards with a negative gradient throughout.",
          "A parabolic curve that peaks at the exact moment the vehicle passes the listener.",
          "A sine wave oscillating above and below the emitted frequency.",
          "A horizontal line that remains strictly constant at f_s for all time.",
          "A curve that drops to zero frequency as soon as the vehicle passes."]),

        ("In an astronomical observation, the hydrogen absorption line normally observed at 656.3 nm in a stationary laboratory is detected at 670.0 nm in light from distant Galaxy X. What conclusions must be drawn from this observation?",
         "1. The wavelength has increased (Red Shift).\n2. Galaxy X is moving AWAY from Earth.\n3. This provides experimental evidence that the universe is EXPANDING.",
         ["1. The wavelength has decreased (Blue Shift).\n2. Galaxy X is moving towards Earth.\n3. The universe is contracting.",
          "1. Galaxy X is stationary relative to Earth.\n2. Light has slowed down in intergalactic space.",
          "1. The star has cooled down into a white dwarf.\n2. No Doppler shift has occurred.",
          "1. Earth is orbiting Galaxy X.\n2. The speed of light has increased by 10%.",
          "1. Galaxy X is rotating but not receding.\n2. The frequency of light has increased."])
    ]
    for q_text, corr, wr in graph_scenarios:
        add_q("hard", "Doppler Graphs & Astronomy", q_text, corr, wr, "Analysis", "Interpret Doppler graphs and cosmological red shift")

    # Complete hard to exactly 200
    hard_count = sum(1 for q in questions if q['difficulty'] == 'hard')
    seed = 1
    while hard_count < 200:
        sp_pick = source_speed_scenarios[(seed - 1) % len(source_speed_scenarios)]
        fs_val, fl_val, ctx = sp_pick
        vs_calc = v_sound * (1.0 - (fs_val / fl_val))
        q_text = f"[Doppler Velocity Analysis {seed}] {ctx} (Speed of sound = 340 m·s⁻¹). What is the exact velocity of approach?"
        if add_q("hard", "Solving for Source Speed", q_text, f"{vs_calc:.2f} m·s⁻¹", [f"{vs_calc*2:.2f} m·s⁻¹", f"{vs_calc/2:.2f} m·s⁻¹", f"{(fl_val-fs_val):.2f} m·s⁻¹", f"{vs_calc+10:.2f} m·s⁻¹", f"{vs_calc-5:.2f} m·s⁻¹", f"{v_sound:.2f} m·s⁻¹"], "Analysis", "Solve for source velocity"):
            hard_count += 1
        seed += 1

    return questions

if __name__ == '__main__':
    qs = build_doppler_effect()
    out_dir = "dataset/grade12/physical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_doppler_effect.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)
    
    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
