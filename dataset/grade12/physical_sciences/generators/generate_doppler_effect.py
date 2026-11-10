import json
import os

def build_doppler_effect():
    questions = []
    seen_questions = set()
    counts = {"easy": 0, "medium": 0, "hard": 0}

    def add_q(difficulty, subtopic, q_text, correct, wrongs, cognitive, outcome, explanation):
        if counts[difficulty] >= (300 if difficulty == "easy" else 500 if difficulty == "medium" else 200):
            return False

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
        counts[difficulty] += 1
        qid = f"PS_P1_DOP_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Paper 1: Doppler Effect",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
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

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Pitch vs Frequency, Wave Characteristics, Applications
    # =========================================================================

    core_definitions = [
        ("Doppler Effect",
         "The change in frequency (or pitch) of the sound or wave detected by a listener because the sound source and the listener have different velocities relative to the medium of sound propagation.",
         ["The reflection of sound waves from a solid barrier causing an acoustic echo",
          "The change in propagation speed of sound when passing from air into water",
          "The destructive interference of two sound waves of identical amplitude and frequency",
          "The bending of acoustic waves around physical obstacles via diffraction",
          "The continuous amplification of sound by an acoustic resonance chamber",
          "The absorption of sound wave energy by soft fibrous materials"],
         "In CAPS Grade 12 Physical Sciences, the Doppler effect is strictly defined as the change in frequency (or pitch) of the sound detected by a listener because the sound source and listener have different velocities relative to the medium."),

        ("Red Shift (in Astronomy)",
         "The shift of spectral absorption lines towards longer wavelengths (lower frequencies) in the light received from distant stars and galaxies, demonstrating that they are moving away from Earth and that the universe is expanding.",
         ["The shift of spectral lines towards higher frequencies as celestial bodies approach Earth",
          "The absorption of blue and ultraviolet light by cold interstellar cosmic dust",
          "The gradual thermodynamic cooling of an aging red giant star",
          "The refraction and chromatic dispersion of starlight passing through the atmosphere",
          "The emission of high-energy infrared radiation from black hole accretion disks",
          "The Doppler broadening of spectral lines inside a stationary stellar core"],
         "Red shift occurs when a light source recedes from the observer; observed wavelength increases (shifts toward the red end of the spectrum), providing empirical evidence for the expanding universe."),

        ("Blue Shift (in Astronomy)",
         "The shift of spectral absorption lines towards shorter wavelengths (higher frequencies) in the light received from a celestial object, demonstrating that the object is moving toward Earth (the observer).",
         ["The shift of spectral lines towards longer wavelengths indicating cosmic recession",
          "The reflection of solar radiation from planetary liquid oceans",
          "The Rayleigh scattering of high-frequency blue sunlight by atmospheric nitrogen",
          "The thermal radiation peak of an extremely hot blue supergiant star",
          "The complete polarization of starlight by interstellar galactic magnetic fields",
          "The decrease in light frequency caused by gravitational time dilation alone"],
         "Blue shift occurs when a light source moves towards an observer; the detected wavefronts are compressed, shifting lines toward higher frequencies (the blue end)."),

        ("Doppler Flow Meter (Ultrasound)",
         "A medical diagnostic instrument that uses high-frequency ultrasound waves and the Doppler effect to measure the velocity and direction of blood flow in arteries and veins.",
         ["A mechanical gauge that measures arterial blood pressure using an inflatable cuff",
          "An instrument that records microvolt electrical signals produced by cardiac muscle (ECG)",
          "An imaging apparatus that utilizes ionizing X-ray radiation to inspect bone fractures",
          "A medical device that measures percentage oxygen saturation in peripheral capillaries",
          "A thermal sensor that tracks fluctuations in core human body temperature",
          "An endoscope that uses fiber optic cables to inspect gastric mucosa visually"],
         "A Doppler flow meter bounces ultrasound off moving red blood cells; the frequency shift of the reflected wave determines blood velocity.")
    ]

    stems = [
        "In Grade 12 Physical Sciences, what is the precise CAPS definition of **'{}'**?",
        "According to the DBE examination guidelines, **'{}'** is defined as:",
        "Which statement provides the exact scientific definition for **'{}'**?",
        "Identify the correct CAPS-approved definition for **'{}'**:",
        "When an examination asks for the definition of **'{}'**, which statement receives full marks?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Pitch, Frequency, and Wavelength Qualitative Relationships
    qual_scenarios = [
        ("A fire truck sounding its siren moves at constant velocity TOWARDS a stationary pedestrian on the pavement",
         "The detected frequency (pitch) is HIGHER than the source frequency, and the detected wavelength is SHORTER, because wave crests are bunched together in front of the moving source.",
         ["The detected frequency is LOWER and the detected wavelength is LONGER.",
          "The detected frequency is HIGHER and the detected wavelength is LONGER.",
          "The detected frequency is LOWER and the detected wavelength is SHORTER.",
          "The speed of sound in air increases by the velocity of the vehicle.",
          "Both frequency and wavelength remain completely identical to the source.",
          "The sound frequency drops to zero as the fire truck draws level with the pedestrian."]),

        ("An ambulance sounding its siren moves at constant velocity AWAY FROM a stationary pedestrian",
         "The detected frequency (pitch) is LOWER than the source frequency, and the detected wavelength is LONGER, because wave crests are stretched out behind the receding source.",
         ["The detected frequency is HIGHER and the detected wavelength is SHORTER.",
          "The detected frequency is LOWER and the detected wavelength is SHORTER.",
          "The detected frequency is HIGHER and the detected wavelength is LONGER.",
          "The speed of the sound wave through the air decreases as distance increases.",
          "The pitch of the siren rises continuously as the distance grows larger.",
          "The wavelength remains identical while the frequency drops to zero."]),

        ("A commuter in a moving car drives at constant velocity TOWARDS a stationary factory whistle sounding in still air",
         "The detected frequency is HIGHER than the source frequency, while the physical wavelength in the air remains UNCHANGED, because the moving listener intercepts more wavefronts per second.",
         ["The detected wavelength in the air becomes compressed and shorter.",
          "The detected frequency is lower because the vehicle engine produces noise.",
          "The speed of sound in the stationary air increases due to the car's motion.",
          "Both the observed frequency and observed wavelength increase simultaneously.",
          "The frequency drops to zero when the car enters the acoustic shadow.",
          "The whistle frequency changes at the source due to the car's approach."]),

        ("A commuter in a car drives at constant velocity AWAY FROM a stationary factory whistle sounding in still air",
         "The detected frequency is LOWER than the source frequency, while the physical wavelength in air remains UNCHANGED, because the receding listener intercepts fewer wavefronts per second.",
         ["The detected wavelength in the air becomes stretched and longer.",
          "The detected frequency is higher because the distance increases.",
          "The speed of sound in the air decreases by the speed of the car.",
          "Both frequency and wavelength decrease to zero immediately.",
          "The sound waves reflect backward toward the factory whistle.",
          "The whistle frequency decreases at the source as the listener drives away."]),

        ("Does the speed of a sound wave (v) in air change when the source of the sound accelerates towards a listener?",
         "No, the speed of sound depends exclusively on the physical properties of the medium (air temperature and density), NOT on the velocity of the source or listener.",
         ["Yes, the speed of sound increases by adding the speed of the source (v + v_s).",
          "Yes, the speed of sound decreases because air is compressed by the vehicle.",
          "Yes, sound travels at supersonic speed whenever the source is in motion.",
          "Yes, the speed of sound doubles whenever the frequency doubles.",
          "Yes, the speed of sound drops to zero behind a moving sound source.",
          "No, because sound waves cannot travel through moving atmospheric air."])
    ]

    for q_sc, c_sc, w_sc in qual_scenarios:
        add_q("easy", "Wave Characteristics", q_sc, c_sc, w_sc, "Understanding", "Understand pitch and wavelength shifts in Doppler effect", c_sc)

    # Medical and Astronomical Applications of Doppler Effect
    apps_data = [
        ("Measuring the rate of blood flow and detecting vascular blockages (stenosis) in human arteries",
         "Doppler Flow Meter using ultrasound waves.",
         ["Stethoscope acoustic auscultation", "Magnetic Resonance Imaging (MRI)", "Positron Emission Tomography (PET)", "Intravenous blood pressure catheterization", "Electrocardiography (ECG)", "Standard clinical transmission radiography (X-ray)"]),

        ("Determining that the universe is expanding and that distant galaxies are moving away from Earth",
         "Astronomical Red Shift observed in the absorption spectra of distant stars.",
         ["Blue shift of stellar hydrogen emission lines", "Cosmic microwave background thermal emission", "Gravitational microlensing of planetary nebulae", "Visual parallax measurement using Earth's orbital diameter", "Apparent magnitude extinction by interstellar carbon soot", "Cepheid variable period-luminosity variations"]),

        ("Measuring the rotational speed of stars and distant galaxies",
         "Doppler broadening and split red/blue shifts on opposite receding and approaching limbs of the rotating celestial body.",
         ["Measuring the absolute surface temperature of the star using Wien's law", "Counting sunspots on the photosphere over an 11-year solar cycle", "Observing eclipsing binary light curves exclusively", "Measuring the magnetic field strength via the Zeeman effect", "Calculating the stellar mass using Newton's law of gravitation alone", "Analyzing nuclear fusion neutrinos escaping from the stellar core"]),

        ("Traffic speed enforcement radar / laser devices used by metropolitan police officers",
         "The Doppler frequency shift of reflected radio/microwaves bounced off moving motor vehicles.",
         ["Measuring vehicle engine decibel levels with an acoustic microphone", "Weighing the vehicle on an in-road piezoceramic axle sensor", "Tracking vehicle heat signatures with an infrared thermographic camera", "Timing the vehicle between two painted white road markings manually", "Measuring vehicle tire tread depth with laser reflection", "Detecting vehicle radio antenna transmissions on police bands"])
    ]

    for app_scenario, corr_app, wr_apps in apps_data:
        add_q("easy", "Applications",
              f"Which technology or scientific discovery directly relies upon the Doppler effect for: **{app_scenario}**?",
              corr_app, wr_apps, "Understanding", "Identify application of Doppler effect",
              f"Application: {corr_app}. Explanation: {app_scenario}.")

    # Fill easy to exactly 300 with diverse, qualitative Doppler source-listener situations
    sources = [
        ("police car", "siren"),
        ("ambulance", "emergency siren"),
        ("passenger train", "locomotive horn"),
        ("fire engine", "two-tone siren"),
        ("motorcycle", "exhaust whistle"),
        ("rescue helicopter", "rotor hum"),
        ("jet aircraft", "engine whine"),
        ("speedboat", "engine roar"),
        ("patrol boat", "fog horn"),
        ("factory", "shift whistle")
    ]

    for veh, snd in sources:
        for f_val in [200, 250, 300, 350, 400, 440, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1100, 1200]:
            if counts["easy"] >= 300:
                break
            # Approaching
            q_app = f"A {veh} emitting a sound of constant frequency {f_val} Hz approaches a stationary listener at constant speed. Which statement correctly describes the frequency and pitch heard by the listener compared to {f_val} Hz?"
            c_app = f"The listener hears a constant frequency HIGHER than {f_val} Hz (a higher pitch)."
            w_app = [
                f"The listener hears a frequency LOWER than {f_val} Hz (a lower pitch).",
                f"The listener hears a frequency that continuously rises and falls every second.",
                f"The listener hears exactly {f_val} Hz because vehicle motion cannot alter frequency.",
                f"The listener hears a frequency that drops to 0 Hz as distance decreases.",
                f"The listener hears double the speed of sound with identical pitch {f_val} Hz.",
                f"The listener hears a frequency that increases exponentially to infinity."
            ]
            add_q("easy", "Qualitative Doppler", q_app, c_app, w_app, "Understanding", f"Explain frequency change for approaching {veh}",
                  f"As the {veh} approaches at constant velocity, wavefronts are compressed in front of it. The listener detects a constant frequency higher than {f_val} Hz.")

            # Receding
            if counts["easy"] < 300:
                q_rec = f"A {veh} emitting a {snd} of frequency {f_val} Hz moves directly AWAY from a stationary listener at constant speed. What pitch and frequency are detected by the listener?"
                c_rec = f"The listener detects a constant frequency LOWER than {f_val} Hz (a lower pitch)."
                w_rec = [
                    f"The listener detects a constant frequency HIGHER than {f_val} Hz (a higher pitch).",
                    f"The listener detects exactly {f_val} Hz because the vehicle has already passed.",
                    f"The listener detects a frequency that fluctuates wildly between 0 Hz and {f_val * 2} Hz.",
                    f"The listener detects a sound wave with a compressed, shorter wavelength.",
                    f"The listener detects a sound wave whose speed through the air is halved.",
                    f"The listener detects ultrasonic radiation above 20 000 Hz."
                ]
                add_q("easy", "Qualitative Doppler", q_rec, c_rec, w_rec, "Understanding", f"Explain frequency change for receding {veh}",
                      f"As the {veh} recedes at constant velocity, wavefronts spread out behind it. The listener detects a constant frequency lower than {f_val} Hz.")

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Direct Calculations: f_L = (v / (v ± v_s)) * f_s and f_L = ((v ± v_L) / v) * f_s
    # =========================================================================

    # CAPS DBE Doppler formula: f_L = ((v ± v_L) / (v ∓ v_s)) * f_s
    # Speed of sound in air: v = 340 m/s (standard) or 343 m/s
    # Source frequencies: 300 to 1200 Hz
    # Source speeds: 15 to 45 m/s

    v_air = 340.0
    source_freqs = [300, 350, 400, 440, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200]
    source_speeds = [15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0, 32.0, 35.0, 38.0, 40.0, 42.0, 45.0]

    # Case 1: Moving source approaching stationary listener (f_L = (v / (v - v_s)) * f_s)
    for fs in source_freqs:
        for vs in source_speeds:
            if counts["medium"] >= 500:
                break
            fl = (v_air / (v_air - vs)) * fs
            corr_fl = f"{fl:.1f} Hz"
            fl_wrong_plus = (v_air / (v_air + vs)) * fs # used plus instead of minus
            fl_wrong_inv = ((v_air - vs) / v_air) * fs # inverted formula
            fl_wrong_inv_plus = ((v_air + vs) / v_air) * fs
            wrs = [
                f"{fl_wrong_plus:.1f} Hz (used (v + v_s) in denominator for approaching source)",
                f"{fl_wrong_inv:.1f} Hz (inverted Doppler fraction)",
                f"{fl_wrong_inv_plus:.1f} Hz",
                f"{fs:.1f} Hz (assumed zero frequency change)",
                f"{fl * 1.5:.1f} Hz",
                f"{fl - 100.0:.1f} Hz",
                f"{fl + 120.0:.1f} Hz"
            ]
            q_text = f"An ambulance with its siren sounding at a frequency of {fs} Hz moves at a constant speed of {vs:.1f} m·s⁻¹ TOWARDS a stationary pedestrian. Taking the speed of sound in air as {v_air:.0f} m·s⁻¹, calculate the frequency detected by the pedestrian:"
            expl = f"Formula: f_L = (v / (v - v_s)) × f_s. Here v = {v_air:.0f} m·s⁻¹, v_s = {vs:.1f} m·s⁻¹, f_s = {fs} Hz. f_L = ({v_air:.0f} / ({v_air:.0f} - {vs:.1f})) × {fs} = ({v_air:.0f} / {v_air - vs:.1f}) × {fs} = {corr_fl}."
            add_q("medium", "Approaching Source Calculations", q_text, corr_fl, wrs, "Applying", "Calculate observed frequency for approaching source", expl)

    # Case 2: Moving source moving away from stationary listener (f_L = (v / (v + v_s)) * f_s)
    for fs in source_freqs:
        for vs in source_speeds:
            if counts["medium"] >= 500:
                break
            fl = (v_air / (v_air + vs)) * fs
            corr_fl = f"{fl:.1f} Hz"
            fl_wrong_minus = (v_air / (v_air - vs)) * fs # used minus instead of plus
            fl_wrong_inv = ((v_air + vs) / v_air) * fs
            fl_wrong_inv_minus = ((v_air - vs) / v_air) * fs
            wrs = [
                f"{fl_wrong_minus:.1f} Hz (used (v - v_s) in denominator for receding source)",
                f"{fl_wrong_inv:.1f} Hz (inverted Doppler equation)",
                f"{fl_wrong_inv_minus:.1f} Hz",
                f"{fs:.1f} Hz (no frequency shift)",
                f"{fl * 0.75:.1f} Hz",
                f"{fl + 75.0:.1f} Hz",
                f"{fl - 80.0:.1f} Hz"
            ]
            q_text = f"A train sounding its whistle at a frequency of {fs} Hz travels at a constant velocity of {vs:.1f} m·s⁻¹ directly AWAY FROM a stationary observer on a station platform. If sound travels at {v_air:.0f} m·s⁻¹ in air, calculate the frequency heard by the observer:"
            expl = f"Formula: f_L = (v / (v + v_s)) × f_s. Here v = {v_air:.0f} m·s⁻¹, v_s = {vs:.1f} m·s⁻¹, f_s = {fs} Hz. f_L = ({v_air:.0f} / ({v_air:.0f} + {vs:.1f})) × {fs} = ({v_air:.0f} / {v_air + vs:.1f}) × {fs} = {corr_fl}."
            add_q("medium", "Receding Source Calculations", q_text, corr_fl, wrs, "Applying", "Calculate observed frequency for receding source", expl)

    # Case 3: Moving listener approaching stationary source (f_L = ((v + v_L) / v) * f_s)
    listener_speeds = [12.0, 15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0, 35.0]
    for fs in source_freqs:
        for vl in listener_speeds:
            if counts["medium"] >= 500:
                break
            fl = ((v_air + vl) / v_air) * fs
            corr_fl = f"{fl:.1f} Hz"
            fl_wrong_minus = ((v_air - vl) / v_air) * fs
            fl_wrong_inv = (v_air / (v_air + vl)) * fs
            wrs = [
                f"{fl_wrong_minus:.1f} Hz (subtracted listener speed instead of adding)",
                f"{fl_wrong_inv:.1f} Hz (treated moving listener as moving source)",
                f"{fs:.1f} Hz",
                f"{fl * 1.3:.1f} Hz",
                f"{fl - 50.0:.1f} Hz",
                f"{fl + 90.0:.1f} Hz",
                f"{fl / 2:.1f} Hz"
            ]
            q_text = f"A motor car drives at a constant speed of {vl:.1f} m·s⁻¹ TOWARDS a stationary factory whistle sounding at {fs} Hz. If the speed of sound in air is {v_air:.0f} m·s⁻¹, determine the frequency detected by the driver of the car:"
            expl = f"Formula: f_L = ((v + v_L) / v) × f_s. Here v = {v_air:.0f} m·s⁻¹, v_L = {vl:.1f} m·s⁻¹, f_s = {fs} Hz. f_L = (({v_air:.0f} + {vl:.1f}) / {v_air:.0f}) × {fs} = ({v_air + vl:.1f} / {v_air:.0f}) × {fs} = {corr_fl}."
            add_q("medium", "Moving Listener Calculations", q_text, corr_fl, wrs, "Applying", "Calculate frequency for moving listener approaching stationary source", expl)

    # Case 4: Moving listener moving away from stationary source (f_L = ((v - v_L) / v) * f_s)
    for fs in source_freqs:
        for vl in listener_speeds:
            if counts["medium"] >= 500:
                break
            fl = ((v_air - vl) / v_air) * fs
            corr_fl = f"{fl:.1f} Hz"
            fl_wrong_plus = ((v_air + vl) / v_air) * fs
            fl_wrong_inv = (v_air / (v_air - vl)) * fs
            wrs = [
                f"{fl_wrong_plus:.1f} Hz (added listener speed instead of subtracting)",
                f"{fl_wrong_inv:.1f} Hz (treated listener as source)",
                f"{fs:.1f} Hz",
                f"{fl * 0.8:.1f} Hz",
                f"{fl + 60.0:.1f} Hz",
                f"{fl - 40.0:.1f} Hz",
                f"{fl * 1.5:.1f} Hz"
            ]
            q_text = f"A motorist drives at a constant speed of {vl:.1f} m·s⁻¹ directly AWAY FROM a stationary police siren sounding at {fs} Hz. Taking the speed of sound in air as {v_air:.0f} m·s⁻¹, calculate the frequency heard by the motorist:"
            expl = f"Formula: f_L = ((v - v_L) / v) × f_s. Here v = {v_air:.0f} m·s⁻¹, v_L = {vl:.1f} m·s⁻¹, f_s = {fs} Hz. f_L = (({v_air:.0f} - {vl:.1f}) / {v_air:.0f}) × {fs} = ({v_air - vl:.1f} / {v_air:.0f}) × {fs} = {corr_fl}."
            add_q("medium", "Moving Listener Calculations", q_text, corr_fl, wrs, "Applying", "Calculate frequency for moving listener receding from stationary source", expl)

    # Fill medium to exactly 500 with wavelength calculations (λ = v / f and λ' = (v ± v_s) / f_s)
    for fs in source_freqs:
        for vs in source_speeds:
            if counts["medium"] >= 500:
                break
            lam_app = (v_air - vs) / fs
            corr_lam = f"{lam_app:.3f} m"
            lam_orig = v_air / fs
            lam_rec = (v_air + vs) / fs
            wrs_lam = [
                f"{lam_orig:.3f} m (original wavelength without Doppler compression)",
                f"{lam_rec:.3f} m (wavelength behind a receding source)",
                f"{lam_app * 2:.3f} m",
                f"{lam_app / 2:.3f} m",
                f"{lam_app + 0.25:.3f} m",
                f"{v_air / (fs * vs):.3f} m",
                f"{lam_app * 1.5:.3f} m"
            ]
            q_text = f"A police cruiser sounding its siren at {fs} Hz approaches a stationary listener at a constant speed of {vs:.1f} m·s⁻¹. Speed of sound in air = {v_air:.0f} m·s⁻¹. Calculate the effective physical wavelength (λ') of the sound waves in FRONT of the approaching cruiser:"
            expl = f"In front of an approaching source, wave crests are compressed: λ' = (v - v_s) / f_s = ({v_air:.0f} - {vs:.1f}) / {fs} = {v_air - vs:.1f} / {fs} = {corr_lam}."
            add_q("medium", "Doppler Wavelength Calculations", q_text, corr_lam, wrs_lam, "Applying", "Calculate compressed wavelength in front of approaching source", expl)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Inverse Calculations: Source Speed (v_s), Sound Speed (v), Both Moving, Ratios
    # =========================================================================

    # Type A: Calculate source speed (v_s) given f_L, f_s, v for approaching source
    # f_L = (v / (v - v_s)) * f_s => v - v_s = v * (f_s / f_L) => v_s = v * (1 - f_s / f_L)
    for fs in [400, 450, 500, 550, 600, 650, 700, 750, 800, 900]:
        for vs_real in [15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0, 32.0, 35.0, 40.0]:
            if counts["hard"] >= 200:
                break
            fl_heard = round((v_air / (v_air - vs_real)) * fs, 1)
            corr_vs = f"{vs_real:.1f} m·s⁻¹"
            # Common errors:
            # v_s = v * (f_L / f_s - 1)
            vs_wrong1 = v_air * ((fl_heard / fs) - 1.0)
            vs_wrong2 = v_air * (1.0 - (fl_heard / fs))
            wrs_vs = [
                f"{vs_wrong1:.1f} m·s⁻¹ (algebraic error in isolating v_s)",
                f"{vs_real * 2:.1f} m·s⁻¹",
                f"{vs_real / 2:.1f} m·s⁻¹",
                f"{vs_real + 10.0:.1f} m·s⁻¹",
                f"{(fl_heard - fs) * 0.5:.1f} m·s⁻¹",
                f"{vs_real * 1.5:.1f} m·s⁻¹",
                f"{abs(vs_wrong2):.1f} m·s⁻¹"
            ]
            q_text = f"A stationary listener hears the siren of an approaching emergency vehicle at a frequency of {fl_heard:.1f} Hz. The true frequency of the siren at rest is {fs} Hz. Taking the speed of sound in air as {v_air:.0f} m·s⁻¹, calculate the speed at which the vehicle is approaching:"
            expl = f"From f_L = (v / (v - v_s)) × f_s: (v - v_s) = v × (f_s / f_L). Therefore v_s = v × (1 - f_s / f_L) = {v_air:.0f} × (1 - {fs} / {fl_heard:.1f}) = {corr_vs}."
            add_q("hard", "Source Speed Calculations", q_text, corr_vs, wrs_vs, "Evaluating", "Calculate source speed for approaching vehicle", expl)

    # Type B: Calculate source speed (v_s) for receding source
    # f_L = (v / (v + v_s)) * f_s => v + v_s = v * (f_s / f_L) => v_s = v * (f_s / f_L - 1)
    for fs in [400, 480, 500, 560, 600, 640, 720, 800, 880, 960]:
        for vs_real in [16.0, 20.0, 24.0, 26.0, 30.0, 34.0, 36.0, 40.0]:
            if counts["hard"] >= 200:
                break
            fl_heard = round((v_air / (v_air + vs_real)) * fs, 1)
            corr_vs = f"{vs_real:.1f} m·s⁻¹"
            vs_wrong1 = v_air * (1.0 - (fl_heard / fs))
            wrs_vs = [
                f"{vs_wrong1:.1f} m·s⁻¹ (used approaching formula instead of receding)",
                f"{vs_real * 2:.1f} m·s⁻¹",
                f"{vs_real / 2:.1f} m·s⁻¹",
                f"{vs_real + 8.5:.1f} m·s⁻¹",
                f"{(fs - fl_heard):.1f} m·s⁻¹",
                f"{vs_real * 1.4:.1f} m·s⁻¹",
                f"{vs_real - 5.0:.1f} m·s⁻¹"
            ]
            q_text = f"An observer standing beside a straight railway track detects a frequency of {fl_heard:.1f} Hz from the whistle of a train as it travels directly away from them. The stationary whistle frequency is {fs} Hz. Given that sound travels at {v_air:.0f} m·s⁻¹ in air, determine the speed of the receding train:"
            expl = f"From f_L = (v / (v + v_s)) × f_s: (v + v_s) = v × (f_s / f_L) => v_s = v × (f_s / f_L - 1) = {v_air:.0f} × ({fs} / {fl_heard:.1f} - 1) = {corr_vs}."
            add_q("hard", "Source Speed Calculations", q_text, corr_vs, wrs_vs, "Evaluating", "Calculate source speed for receding train", expl)

    # Type C: Simultaneous two-state pitch drop (f_approach / f_recede ratio)
    # As vehicle passes: f_app = (v / (v - v_s)) * f_s; f_rec = (v / (v + v_s)) * f_s
    # Ratio R = f_app / f_rec = (v + v_s) / (v - v_s) => v_s = v * ((R - 1) / (R + 1))
    for vs_real in [15.0, 20.0, 25.0, 30.0, 35.0, 40.0]:
        for fs in [400, 500, 600, 750, 800]:
            if counts["hard"] >= 200:
                break
            f_app = round((v_air / (v_air - vs_real)) * fs, 1)
            f_rec = round((v_air / (v_air + vs_real)) * fs, 1)
            diff_f = round(f_app - f_rec, 1)
            corr_vs = f"{vs_real:.1f} m·s⁻¹"
            wrs_pass = [
                f"{vs_real * 2:.1f} m·s⁻¹",
                f"{vs_real / 2:.1f} m·s⁻¹",
                f"{diff_f:.1f} m·s⁻¹ (confused frequency drop with velocity)",
                f"{vs_real + 12.0:.1f} m·s⁻¹",
                f"{(v_air * diff_f) / fs:.1f} m·s⁻¹",
                f"{vs_real * 1.5:.1f} m·s⁻¹",
                f"{vs_real - 6.0:.1f} m·s⁻¹"
            ]
            q_text = f"As a police car with its siren sounding passes a stationary listener on the roadside, the observed frequency drops abruptly from {f_app:.1f} Hz (as it approaches) to {f_rec:.1f} Hz (as it recedes). If the speed of sound in air is {v_air:.0f} m·s⁻¹, calculate the constant speed of the police car:"
            expl = f"Ratio R = f_app / f_rec = {f_app:.1f} / {f_rec:.1f} = (v + v_s) / (v - v_s). Solving for v_s gives v_s = v × ((R - 1) / (R + 1)) = {v_air:.0f} × (({f_app:.1f}/{f_rec:.1f} - 1) / ({f_app:.1f}/{f_rec:.1f} + 1)) = {corr_vs}."
            add_q("hard", "Two-State Doppler Analysis", q_text, corr_vs, wrs_pass, "Evaluating", "Calculate vehicle speed from approaching and receding frequencies", expl)

    # Complete hard to exactly 200 with both source and listener moving scenarios
    # f_L = ((v ± v_L) / (v ∓ v_s)) * f_s
    for fs in [500, 600, 700, 800]:
        for vs in [20.0, 25.0, 30.0]:
            for vl in [10.0, 15.0, 20.0]:
                if counts["hard"] >= 200:
                    break
                # Both moving towards each other: f_L = ((v + v_L) / (v - v_s)) * f_s
                fl_both = ((v_air + vl) / (v_air - vs)) * fs
                corr_both = f"{fl_both:.1f} Hz"
                wrs_both = [
                    f"{((v_air - vl) / (v_air + vs)) * fs:.1f} Hz (reversed signs for both moving away)",
                    f"{(v_air / (v_air - vs)) * fs:.1f} Hz (ignored listener motion)",
                    f"{((v_air + vl) / v_air) * fs:.1f} Hz (ignored source motion)",
                    f"{fs:.1f} Hz",
                    f"{fl_both * 1.2:.1f} Hz",
                    f"{fl_both - 85.0:.1f} Hz",
                    f"{fl_both + 110.0:.1f} Hz"
                ]
                q_text = f"Two motor vehicles travel directly towards each other on a straight road. Vehicle A sounds its horn at {fs} Hz while travelling at {vs:.1f} m·s⁻¹. Vehicle B approaches Vehicle A at {vl:.1f} m·s⁻¹. If sound propagates at {v_air:.0f} m·s⁻¹ in air, calculate the frequency detected by the driver of Vehicle B:"
                expl = f"Both source and listener move towards each other: f_L = ((v + v_L) / (v - v_s)) × f_s = (({v_air:.0f} + {vl:.1f}) / ({v_air:.0f} - {vs:.1f})) × {fs} = ({v_air + vl:.1f} / {v_air - vs:.1f}) × {fs} = {corr_both}."
                add_q("hard", "Dual-Motion Doppler", q_text, corr_both, wrs_both, "Evaluating", "Calculate frequency when both source and listener are in motion", expl)

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
