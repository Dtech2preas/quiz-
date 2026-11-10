import json
import math
import os

def build_waves_sound_and_light():
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
        qid = f"TS_P1_WAV_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Waves, Sound & Light",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Waves, Sound & Light",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Wave Types, Sound Properties, Optics Concepts, Lenses
    # =========================================================================

    core_definitions = [
        ("Transverse Wave",
         "A wave in which the particles of the medium vibrate perpendicularly (at right angles) to the direction of propagation of the wave.",
         ["A wave in which particles vibrate parallel to the direction of wave travel",
          "A wave that requires no physical medium to propagate across space",
          "A wave produced exclusively by vibrating acoustic tuning forks",
          "A continuous stationary wave formed between two fixed boundaries",
          "A wave whose speed increases as frequency decreases in air",
          "A wave composed solely of compression and rarefaction zones"],
         "In a transverse wave (e.g. water waves, electromagnetic waves), particle displacement is perpendicular to wave propagation."),

        ("Longitudinal Wave",
         "A wave in which the particles of the medium vibrate parallel to the direction of propagation of the wave (forming compressions and rarefactions).",
         ["A wave in which particles vibrate perpendicular to the direction of motion",
          "A transverse wave that can be polarized by optical filters",
          "An electromagnetic wave travelling at the speed of light in vacuum",
          "A wave with infinite wavelength and zero oscillation frequency",
          "A wave that reflects only when hitting a mirror surface",
          "A wave whose crests and troughs move in opposite directions"],
         "In a longitudinal wave (e.g. sound waves in air), the particles oscillate back and forth parallel to the direction of energy propagation."),

        ("Frequency (f)",
         "The number of complete wave cycles (or oscillations) that pass a given point per second (measured in Hertz, Hz).",
         ["The time taken for a single complete wave cycle to pass a point",
          "The maximum displacement of a particle from its rest position",
          "The distance between two consecutive in-phase points on a wave",
          "The speed at which wave energy travels through a physical medium",
          "The ratio of wave speed divided by the amplitude of vibration",
          "The rate of change of sound intensity in decibels"],
         "Frequency is the number of waves per second: f = 1 / T. Its unit is the Hertz (Hz = s⁻¹)."),

        ("Wavelength (λ)",
         "The physical distance between two consecutive points on a wave that are in phase (such as from crest to crest, or compression to compression).",
         ["The height of a wave crest above the undisturbed rest position",
          "The time taken for a wave to travel a distance of one meter",
          "The total number of wave crests produced by a vibrating source",
          "The angle at which light refracts when entering a glass prism",
          "The speed of light divided by Planck's quantum constant",
          "The thickness of a converging lens at its optical center"],
         "Wavelength (λ) is the spatial length of one complete wave cycle, measured in meters (m)."),

        ("Period (T)",
         "The time taken for one complete wave oscillation or cycle to pass a given reference point (T = 1 / f, measured in seconds).",
         ["The number of complete waves generated in one second",
          "The speed at which a sound wave travels through steel",
          "The maximum distance a wave travels before dissipating",
          "The distance between a crest and an adjacent trough",
          "The angle of incidence inside an optical fiber cable",
          "The frequency divided by the speed of light"],
         "Period is the time for one complete cycle: T = 1 / f (unit: seconds)."),

        ("Pitch of a Sound",
         "The subjective perception of sound frequency; a higher frequency produces a higher pitch, and a lower frequency produces a lower pitch.",
         ["The subjective perception of sound wave amplitude or volume",
          "The speed of sound propagation through solid steel rails",
          "The purity of harmonics determined by instrument waveform",
          "The rate of energy transmission per unit area in decibels",
          "The angle of reflection of sound from an acoustic boundary",
          "The distance between the sound source and human ear"],
         "Pitch is directly governed by frequency: high frequency = high pitch; low frequency = low pitch."),

        ("Loudness of a Sound",
         "The subjective perception of sound intensity, which is directly determined by the amplitude of the sound wave (greater amplitude = louder sound).",
         ["The number of wave cycles passing a detector per second",
          "The pitch of the sound as determined by wave frequency",
          "The acoustic quality of the sound determined by overtones",
          "The refractive index of the air through which sound travels",
          "The speed of sound divided by the wavelength of the note",
          "The duration for which a tuning fork continues to vibrate"],
         "Loudness is determined by wave amplitude: larger amplitude carries more energy, producing a louder sound."),

        ("Ultrasound",
         "Sound waves having a frequency greater than the upper limit of human hearing (frequencies exceeding 20 000 Hz).",
         ["Sound waves with frequencies below the human hearing threshold (under 20 Hz)",
          "Acoustic waves that can only travel through empty vacuum",
          "Transverse light waves polarized by crystal prisms",
          "Sound waves whose speed exceeds the speed of light",
          "Electromagnetic radiation emitted by radio broadcast antennas",
          "Sound waves of zero frequency and infinite amplitude"],
         "Ultrasound refers to acoustic waves above 20 kHz (20 000 Hz), used in medical sonography and non-destructive industrial testing."),

        ("Refraction of Light",
         "The bending of a light ray as it passes obliquely from one optical medium into another of different optical density, caused by a change in the propagation speed of light.",
         ["The bouncing of light off a polished mirror surface",
          "The spreading of light waves through a narrow microscopic slit",
          "The emission of electrons from a metal cathode under light",
          "The total absorption of light energy by black opaque surfaces",
          "The splitting of laser light into polarized transverse components",
          "The continuous reflection of light inside an optical prism"],
         "Refraction is the change in direction of light caused by a change in speed when entering a medium with a different optical density."),

        ("Critical Angle (θ_c)",
         "The angle of incidence in the optically denser medium for which the corresponding angle of refraction in the optically rarer medium is exactly 90 degrees.",
         ["The angle of reflection when light strikes a plane silver mirror",
          "The maximum angle at which a convex lens can focus light rays",
          "The angle of incidence that causes light to be completely absorbed",
          "The focal angle between the principal axis and focal point",
          "The angle where light travels at the speed of light in vacuum",
          "The angle of incidence where wave frequency doubles"],
         "The critical angle is the angle of incidence in the denser medium yielding an angle of refraction of 90° in the rarer medium: sin θ_c = n2 / n1."),

        ("Total Internal Reflection (TIR)",
         "The optical phenomenon where a light ray travelling in an optically denser medium strikes the boundary of an optically rarer medium at an angle of incidence greater than the critical angle, and is 100% reflected back into the denser medium.",
         ["The transmission of light through tinted sunglasses without loss",
          "The refraction of light along the boundary at exactly 90 degrees",
          "The polarization of starlight by atmospheric nitrogen gas",
          "The scattering of blue light by microscopic aerosol particles",
          "The focusing of parallel light rays by a concave glass mirror",
          "The absorption of infrared radiation by greenhouse gases"],
         "Total Internal Reflection occurs when light travels from denser to rarer medium AND angle of incidence exceeds critical angle (θ_i > θ_c)."),

        ("Convex (Converging) Lens",
         "A lens that is thicker at the center than at the edges, which refracts parallel incident light rays inward towards a real focal point.",
         ["A lens that is thinner at the center and spreads light outward",
          "A flat sheet of transparent glass with zero focal power",
          "An optical mirror that reflects light without any refraction",
          "A lens that always produces virtual, diminished images exclusively",
          "A lens designed to absorb all visible electromagnetic radiation",
          "A prism that reverses light without changing ray convergence"],
         "A convex lens converges parallel rays to a real focal point and can form both real and virtual images depending on object distance."),

        ("Concave (Diverging) Lens",
         "A lens that is thinner at the center than at the edges, which refracts parallel incident light rays outward so that they appear to diverge from a virtual focal point.",
         ["A lens that converges parallel rays to a real image on a screen",
          "A lens that is thicker in the middle and magnifies nearby text",
          "A curved mirror that focuses solar radiation to ignite fires",
          "A lens that only functions under monochromatic laser light",
          "A lens that converts visible light into invisible infrared rays",
          "A glass cylinder used to split light into a continuous rainbow"],
         "A concave lens diverges parallel rays outward and ALWAYS forms a virtual, upright, diminished image.")
    ]

    stems = [
        "In Grade 12 Technical Sciences, how is **'{}'** defined?",
        "According to the CAPS curriculum, **'{}'** refers to:",
        "Which statement provides the exact scientific definition for **'{}'**?",
        "Identify the correct CAPS definition for **'{}'**:",
        "When an examination asks for the definition of **'{}'**, which statement receives full marks?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Total Internal Reflection Conditions & Applications
    tir_scenarios = [
        ("What two specific physical conditions are REQUIRED for Total Internal Reflection (TIR) to occur?",
         "1. Light must travel from an optically denser medium toward an optically rarer medium (n1 > n2). 2. The angle of incidence must be greater than the critical angle (θ_i > θ_c).",
         ["1. Light must travel from rarer to denser medium. 2. Angle of incidence must be exactly 0°.",
          "1. Light must be monochromatic. 2. The medium must be heated to boiling point.",
          "1. The surface must be coated with reflective silver. 2. Light must be polarized.",
          "1. Angle of incidence must equal 90°. 2. The two media must have identical refractive indices.",
          "1. Light must travel in empty vacuum. 2. A magnetic field must be applied.",
          "1. The lens must be concave. 2. The angle of refraction must be zero."]),

        ("How does Total Internal Reflection make optical fiber cables ideal for modern high-speed telecommunications?",
         "Light signals pulse through the high-refractive-index glass core and undergo continuous Total Internal Reflection at the core-cladding boundary with negligible loss of signal intensity over vast distances.",
         ["Electrical current flows through the glass core faster than in copper.",
          "Light rays are refracted out of the fiber into the surrounding air.",
          "The glass fiber converts electromagnetic light into acoustic sound.",
          "The cladding absorbs all light pulses to prevent data theft.",
          "Light travels at ten times the speed of light inside the fiber.",
          "The fiber operates only when immersed in liquid nitrogen."]),

        ("What happens to a light ray in water (n = 1.33) when it strikes the water-air boundary at an angle of incidence EQUAL to the critical angle (θ_i = θ_c = 48.8°)?",
         "The refracted ray travels along the boundary surface between water and air at an angle of refraction of exactly 90 degrees.",
         ["The light ray is 100% reflected backward into the water.",
          "The light ray passes straight through into air with zero deflection.",
          "The light ray is completely absorbed by the surface water molecules.",
          "The light ray splits into an infinite number of discrete colors.",
          "The speed of the light ray drops to zero at the interface.",
          "The light ray converts into high-energy ultraviolet radiation."])
    ]

    for q_tir, c_tir, w_tir in tir_scenarios:
        add_q("easy", "TIR Principles", q_tir, c_tir, w_tir, "Understanding", "Understand total internal reflection conditions and behavior", c_tir)

    # Qualitative Lens Images (Convex vs Concave)
    lens_qual = [
        ("What type of image is ALWAYS formed by a single CONCAVE (diverging) lens, regardless of object position?",
         "A Virtual, Upright, and Diminished (smaller than object) image.",
         ["A Real, Inverted, and Magnified image",
          "A Real, Upright, and Same size image",
          "A Virtual, Inverted, and Magnified image",
          "A Real, Inverted, and Diminished image",
          "An image formed at infinity that cannot be seen",
          "A Real, Upright, and Magnified image"]),

        ("When an object is placed between the focal point and optical center of a CONVEX (converging) lens (d_o < f), what type of image is formed (magnifying glass)?",
         "A Virtual, Upright, and Magnified image formed on the same side of the lens as the object.",
         ["A Real, Inverted, and Diminished image on the opposite side",
          "A Real, Upright, and Magnified image on a screen",
          "A Virtual, Inverted, and Diminished image",
          "No image is formed because light rays cannot refract",
          "A Real, Inverted, and Same size image at 2F",
          "An inverted image that can be projected on a white wall"]),

        ("When an object is placed beyond twice the focal length (d_o > 2F) of a CONVEX (converging) lens (like a camera), what type of image is produced?",
         "A Real, Inverted, and Diminished image located between F and 2F on the opposite side of the lens.",
         ["A Virtual, Upright, and Magnified image",
          "A Real, Upright, and Magnified image",
          "A Virtual, Inverted, and Same size image",
          "An image at the optical center of the glass",
          "A Real, Inverted, and Magnified image at infinity",
          "No image is formed because rays diverge completely"])
    ]

    for q_lq, c_lq, w_lq in lens_qual:
        add_q("easy", "Lens Optics", q_lq, c_lq, w_lq, "Understanding", "Identify image characteristics for lenses", c_lq)

    # Fill easy to exactly 300 with diverse, qualitative wave parameter comparisons
    wave_media = [
        ("sound in air at 20 °C", 343.0, "longitudinal wave"),
        ("sound in freshwater", 1480.0, "longitudinal wave"),
        ("sound in solid steel railway track", 5100.0, "longitudinal wave"),
        ("light in vacuum", 3.0e8, "transverse electromagnetic wave"),
        ("light in water", 2.25e8, "transverse electromagnetic wave"),
        ("light in crown glass", 1.97e8, "transverse electromagnetic wave"),
        ("light in diamond", 1.24e8, "transverse electromagnetic wave"),
        ("seismic P-wave through Earth mantle", 8000.0, "longitudinal compressional wave"),
        ("seismic S-wave through Earth crust", 4500.0, "transverse shear wave"),
        ("ultrasound in human soft tissue", 1540.0, "longitudinal wave")
    ]

    for med_name, spd, w_type in wave_media:
        for f_hz in [50, 100, 150, 200, 250, 300, 350, 400, 440, 500, 600, 750, 800, 1000, 1500, 2000, 2500, 3000, 5000, 7500, 10000, 20000, 25000, 40000, 50000]:
            if counts["easy"] >= 300:
                break
            q_text_wm = f"A wave of frequency {f_hz} Hz travels through **{med_name}** at a speed of {spd:.1e} m·s⁻¹. What type of wave propagation is this, and what is its fundamental mechanical nature?"
            c_wm = f"It propagates as a {w_type} with wave speed determined strictly by the elastic and density properties of {med_name.split()[0]}."
            w_wm = [
                "It is a transverse electromagnetic wave with zero mass and infinite frequency.",
                "It travels without any energy transmission across the medium.",
                "It converts into a gravitational shockwave upon contact with boundaries.",
                "Its frequency changes continuously as it travels further into the medium.",
                "Its speed doubles every time the amplitude is halved.",
                "It causes particles to travel permanently to the end of the medium."
            ]
            add_q("easy", "Wave Medium Characteristics", q_text_wm, c_wm, w_wm, "Understanding", f"Identify wave nature in {med_name}", c_wm)

            if counts["easy"] < 300:
                q_text_freq = f"When a wave travels from one medium into another medium where its speed decreases, what happens to its FREQUENCY and WAVELENGTH?"
                c_freq = "The frequency remains STRICTLY UNCHANGED (frequency depends solely on the source), while the wavelength DECREASES proportionally with speed (λ = v / f)."
                w_freq = [
                    "Both frequency and wavelength decrease proportionally.",
                    "The frequency decreases while wavelength remains constant.",
                    "The frequency increases to compensate for lower speed.",
                    "Both frequency and wavelength double.",
                    "The frequency drops to zero inside the second medium.",
                    "The wave loses all its energy and stops instantly."
                ]
                add_q("easy", "Boundary Behavior", q_text_freq, c_freq, w_freq, "Understanding", "Explain frequency and wavelength behavior across boundary", c_freq)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Direct Calculations: v = f*λ, n = c/v, Snell's Law (n1 sinθ1 = n2 sinθ2), Critical Angle, Lens Formula
    # =========================================================================

    # 1. Wave Equation Calculations: v = f * λ => f = v / λ => λ = v / f
    sound_speeds = [340.0, 343.0, 1480.0, 1500.0, 5000.0, 5100.0] # m/s
    audio_freqs = [170.0, 250.0, 340.0, 440.0, 500.0, 680.0, 850.0, 1000.0, 1700.0, 2000.0, 5000.0, 10000.0, 20000.0, 40000.0]

    for v_w in sound_speeds:
        for f_w in audio_freqs:
            if counts["medium"] >= 500:
                break
            lam_w = v_w / f_w
            corr_lam = f"{lam_w:.3f} m"
            wrs_lam = [
                f"{v_w * f_w:.1f} m (multiplied speed by frequency)",
                f"{f_w / v_w:.4f} m (inverted wave equation: f / v)",
                f"{lam_w * 2:.3f} m",
                f"{lam_w / 2:.3f} m",
                f"{lam_w + 0.5:.3f} m",
                f"{lam_w * 100:.1f} m (forgot unit conversion)",
                f"{lam_w * 1.5:.3f} m"
            ]
            q_text_lam = f"A sound wave of frequency {f_w:.0f} Hz propagates through a medium at a speed of {v_w:.0f} m·s⁻¹. Calculate the wavelength (λ) of the sound wave:"
            expl_lam = f"Wave equation: v = f × λ => λ = v / f = {v_w:.0f} m·s⁻¹ / {f_w:.0f} Hz = {corr_lam}."
            add_q("medium", "Wave Calculations", q_text_lam, corr_lam, wr_lam := wrs_lam, "Applying", "Calculate wavelength from wave speed and frequency", expl_lam)

            # Frequency from speed and wavelength
            if counts["medium"] < 500:
                corr_fw = f"{f_w:.1f} Hz"
                wrs_fw = [
                    f"{v_w * lam_w:.1f} Hz",
                    f"{lam_w / v_w:.4f} Hz",
                    f"{f_w * 2:.1f} Hz",
                    f"{f_w / 2:.1f} Hz",
                    f"{f_w + 120.0:.1f} Hz",
                    f"{f_w * 1.4:.1f} Hz",
                    f"{v_w:.1f} Hz"
                ]
                q_text_fw = f"A periodic wave with a wavelength of {lam_w:.3f} m travels at {v_w:.0f} m·s⁻¹. Determine the frequency (f) of the wave:"
                expl_fw = f"f = v / λ = {v_w:.0f} m·s⁻¹ / {lam_w:.3f} m = {corr_fw}."
                add_q("medium", "Wave Calculations", q_text_fw, corr_fw, wrs_fw, "Applying", "Calculate wave frequency from speed and wavelength", expl_fw)

    # 2. Refractive Index & Speed of Light in Media: n = c / v => v = c / n
    # c = 3.0e8 m/s
    c_light = 3.0e8
    refractive_materials = [
        ("Water", 1.33),
        ("Ethanol", 1.36),
        ("Fused quartz", 1.46),
        ("Crown glass", 1.52),
        ("Perspex (acrylic)", 1.49),
        ("Flint glass", 1.66),
        ("Sapphire", 1.77),
        ("Diamond", 2.42),
        ("Zircon", 1.92),
        ("Polycarbonate", 1.58)
    ]

    for mat_n, n_val in refractive_materials:
        if counts["medium"] >= 500:
            break
        v_med = c_light / n_val
        corr_vmed = f"{v_med * 1e-8:.2f} × 10⁸ m·s⁻¹"
        wrs_vmed = [
            f"{c_light * n_val * 1e-8:.2f} × 10⁸ m·s⁻¹ (multiplied c by n)",
            f"{n_val / c_light * 1e16:.2f} × 10⁸ m·s⁻¹",
            f"{c_light * 1e-8:.2f} × 10⁸ m·s⁻¹ (speed in vacuum)",
            f"{v_med * 2 * 1e-8:.2f} × 10⁸ m·s⁻¹",
            f"{v_med * 0.5 * 1e-8:.2f} × 10⁸ m·s⁻¹",
            f"{v_med * 1e-8 + 0.5:.2f} × 10⁸ m·s⁻¹",
            f"{v_med * 1.3 * 1e-8:.2f} × 10⁸ m·s⁻¹"
        ]
        q_text_n = f"The refractive index of **{mat_n}** is n = {n_val:.2f}. Taking the speed of light in vacuum as c = 3.0 × 10⁸ m·s⁻¹, calculate the speed of light (v) as it propagates through {mat_n}:"
        expl_n = f"Refractive index formula: n = c / v => v = c / n = (3.0 × 10⁸ m·s⁻¹) / {n_val:.2f} = {corr_vmed}."
        add_q("medium", "Refractive Index Calculations", q_text_n, corr_vmed, wrs_vmed, "Applying", f"Calculate speed of light in {mat_n}", expl_n)

    # 3. Critical Angle Calculations: sin(θ_c) = n2 / n1 (for light entering air n2 = 1.00)
    # θ_c = arcsin(1 / n1)
    for mat_n, n_val in refractive_materials:
        if counts["medium"] >= 500:
            break
        sin_crit = 1.0 / n_val
        crit_deg = math.degrees(math.asin(sin_crit))
        corr_crit = f"{crit_deg:.1f}°"
        wrs_crit = [
            f"{math.degrees(sin_crit):.1f}° (treated sine value directly as degrees)",
            f"{90.0 - crit_deg:.1f}°",
            f"{crit_deg * 2:.1f}°",
            f"{crit_deg / 2:.1f}°",
            f"{crit_deg + 15.0:.1f}°",
            f"{45.0:.1f}°",
            f"{crit_deg * 1.3:.1f}°"
        ]
        q_text_crit = f"Calculate the CRITICAL ANGLE (θ_c) for light travelling from **{mat_n}** (n = {n_val:.2f}) into air (n = 1.00):"
        expl_crit = f"Critical angle formula: sin(θ_c) = n_air / n_medium = 1.00 / {n_val:.2f} = {sin_crit:.4f}. θ_c = sin⁻¹({sin_crit:.4f}) = {corr_crit}."
        add_q("medium", "Critical Angle Calculations", q_text_crit, corr_crit, wrs_crit, "Applying", f"Calculate critical angle for {mat_n}", expl_crit)

    # 4. Snell's Law Refraction Calculations: n1 * sin(θ1) = n2 * sin(θ2)
    # Light from air (n1 = 1.00) into medium (n2) at angle θ1
    incident_angles = [20.0, 30.0, 40.0, 45.0, 50.0, 60.0]
    for mat_n, n2_val in refractive_materials[:6]:
        for ang1 in incident_angles:
            if counts["medium"] >= 500:
                break
            rad1 = math.radians(ang1)
            sin_r = (1.00 * math.sin(rad1)) / n2_val
            refr_deg = math.degrees(math.asin(sin_r))
            corr_refr = f"{refr_deg:.1f}°"
            wrs_refr = [
                f"{ang1:.1f}° (no refraction)",
                f"{ang1 * n2_val:.1f}° (multiplied angle by n)",
                f"{refr_deg * 2:.1f}°",
                f"{refr_deg / 2:.1f}°",
                f"{90.0 - refr_deg:.1f}°",
                f"{refr_deg + 10.0:.1f}°",
                f"{refr_deg * 1.4:.1f}°"
            ]
            q_text_snell = f"A ray of light in air strikes the flat surface of a block of **{mat_n}** (n = {n2_val:.2f}) at an angle of incidence of {ang1:.0f}°. Calculate the angle of refraction (θ_r) inside the {mat_n}:"
            expl_snell = f"Snell's Law: n1 × sin(θ1) = n2 × sin(θ2) => 1.00 × sin({ang1:.0f}°) = {n2_val:.2f} × sin(θ2) => sin(θ2) = sin({ang1:.0f}°) / {n2_val:.2f} = {math.sin(rad1):.4f} / {n2_val:.2f} = {sin_r:.4f}. θ2 = sin⁻¹({sin_r:.4f}) = {corr_refr}."
            add_q("medium", "Snell's Law Calculations", q_text_snell, corr_refr, wrs_refr, "Applying", f"Calculate angle of refraction in {mat_n}", expl_snell)

    # 5. Thin Lens Formula Calculations: 1/f = 1/d_o + 1/d_i => d_i = (f * d_o) / (d_o - f)
    # Convex lens (positive f): f in [10, 15, 20, 25, 30] cm
    focal_lengths_cm = [10.0, 15.0, 20.0, 25.0, 30.0]
    object_distances_cm = [12.0, 18.0, 20.0, 25.0, 30.0, 35.0, 40.0, 50.0, 60.0]

    for f_lens in focal_lengths_cm:
        for do_val in object_distances_cm:
            if counts["medium"] >= 500:
                break
            if abs(do_val - f_lens) < 0.5:
                continue # image at infinity
            # 1/di = 1/f - 1/do = (do - f) / (f * do) => di = (f * do) / (do - f)
            di_val = (f_lens * do_val) / (do_val - f_lens)
            if di_val > 0:
                img_nature = "Real image (on opposite side of lens)"
            else:
                img_nature = "Virtual image (on same side as object)"
            corr_di = f"{di_val:.1f} cm ({img_nature})"
            wrs_di = [
                f"{f_lens + do_val:.1f} cm",
                f"{abs(do_val - f_lens):.1f} cm",
                f"{di_val * 2:.1f} cm",
                f"{di_val / 2:.1f} cm",
                f"{-di_val:.1f} cm",
                f"{di_val + 15.0:.1f} cm",
                f"{di_val * 1.5:.1f} cm"
            ]
            q_text_lens = f"An illuminated object is placed at a distance of d_o = {do_val:.1f} cm from a thin CONVEX lens of focal length f = +{f_lens:.1f} cm. Using the lens formula, calculate the image distance (d_i) and state the image nature:"
            expl_lens = f"1/f = 1/d_o + 1/d_i => 1/d_i = 1/f - 1/d_o = 1/{f_lens:.1f} - 1/{do_val:.1f} = ({do_val - f_lens:.1f}) / ({f_lens * do_val:.1f}) => d_i = ({f_lens * do_val:.1f}) / ({do_val - f_lens:.1f}) = {corr_di}."
            add_q("medium", "Lens Formula Calculations", q_text_lens, corr_di, wrs_di, "Applying", "Calculate image distance using lens formula", expl_lens)

    # Complete medium to exactly 500 with diverse ultrasound travel distance calculations: d = (v * t) / 2
    step = 1
    while counts["medium"] < 500:
        v_sound_t = 1540.0 # human tissue ultrasound speed
        t_ms = 10.0 + (step * 2.0)
        t_sec = t_ms * 1e-6 # microseconds
        # Depth d = (v * t) / 2
        depth_m = (v_sound_t * t_sec) / 2.0
        depth_cm = depth_m * 100.0
        corr_depth = f"{depth_cm:.2f} cm ({depth_m * 1000:.1f} mm)"
        wrs_depth = [
            f"{depth_cm * 2:.2f} cm (forgot to divide by 2 for the return echo)",
            f"{v_sound_t * t_sec * 100:.2f} cm",
            f"{depth_cm / 2:.2f} cm",
            f"{depth_cm + 2.0:.2f} cm",
            f"{depth_cm * 1.5:.2f} cm",
            f"{depth_cm / 10:.2f} cm",
            f"0.00 cm"
        ]
        q_text_echo = f"In medical ultrasound diagnostics, an ultrasound pulse (speed v = {v_sound_t:.0f} m·s⁻¹ in soft tissue) is emitted into a patient's abdomen. An echo reflected from an internal organ boundary is detected {t_ms:.0f} μs ({t_ms} × 10⁻⁶ s) later. Calculate the DEPTH (d) of the organ boundary beneath the transducer probe:"
        expl_echo = f"Ultrasound travels to the organ and back (two-way distance = 2d): 2d = v × t => d = (v × t) / 2 = ({v_sound_t:.0f} m·s⁻¹ × {t_ms} × 10⁻⁶ s) / 2 = {corr_depth}."
        add_q("medium", "Ultrasound Echo Calculations", q_text_echo, corr_depth, wrs_depth, "Applying", "Calculate organ depth using ultrasound echo timing", expl_echo)
        step += 1

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Multi-step Lens Magnification, Optical Fiber Core-Cladding, Wavelength Shifts
    # =========================================================================

    # 1. Multi-step Lens Calculations: Object of height h_o placed in front of convex lens
    # 1/f = 1/do + 1/di => di = (f * do) / (do - f)
    # Magnification m = -di / do; Image height h_i = m * h_o
    object_heights_cm = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
    for f_lens in [12.0, 15.0, 20.0, 25.0]:
        for do_val in [25.0, 30.0, 35.0, 40.0, 50.0]:
            for ho_val in object_heights_cm:
                if counts["hard"] >= 200:
                    break
                if abs(do_val - f_lens) < 0.5:
                    continue
                di_val = (f_lens * do_val) / (do_val - f_lens)
                mag = di_val / do_val
                hi_val = mag * ho_val
                corr_hi = f"{hi_val:.2f} cm (Inverted real image)"
                wrs_hi = [
                    f"{ho_val:.2f} cm (assumed no magnification)",
                    f"{ho_val / mag:.2f} cm",
                    f"{hi_val * 2:.2f} cm",
                    f"{hi_val / 2:.2f} cm",
                    f"{di_val:.2f} cm (confused image distance with image height)",
                    f"{hi_val + 2.5:.2f} cm",
                    f"{hi_val * 1.4:.2f} cm"
                ]
                q_text_mag = f"An arrow of height h_o = {ho_val:.1f} cm is placed upright at a distance of d_o = {do_val:.1f} cm from a thin CONVEX lens having a focal length of f = +{f_lens:.1f} cm. Calculate the HEIGHT (h_i) of the resulting image:"
                expl_mag = f"1. Image distance: 1/d_i = 1/f - 1/d_o = 1/{f_lens:.1f} - 1/{do_val:.1f} => d_i = ({f_lens * do_val:.1f}) / ({do_val - f_lens:.1f}) = {di_val:.2f} cm. 2. Magnification: |m| = d_i / d_o = {di_val:.2f} / {do_val:.1f} = {mag:.3f}. 3. Image height: h_i = |m| × h_o = {mag:.3f} × {ho_val:.1f} cm = {corr_hi}."
                add_q("hard", "Lens Magnification", q_text_mag, corr_hi, wrs_hi, "Evaluating", "Calculate image height from multi-step lens equation", expl_mag)

    # 2. Optical Fiber Core-Cladding Critical Angle & Light Containment:
    # n_core > n_cladding. Critical angle at core-cladding boundary: sin(θ_c) = n_cladding / n_core
    fiber_pairs = [
        ("Silica glass core", 1.48, "Doped silica cladding", 1.45),
        ("High-index glass core", 1.55, "Standard glass cladding", 1.50),
        ("Polymer core (PMMA)", 1.49, "Fluorinated polymer cladding", 1.41),
        ("Dense flint core", 1.62, "Crown glass cladding", 1.52),
        ("Silica core", 1.46, "Low-index polymer cladding", 1.38)
    ]

    for c_name, n_core, clad_name, n_clad in fiber_pairs:
        sin_crit_f = n_clad / n_core
        crit_deg_f = math.degrees(math.asin(sin_crit_f))
        corr_crit_f = f"{crit_deg_f:.1f}°"
        wrs_crit_f = [
            f"{math.degrees(n_core / n_clad):.1f}° (inverted refractive indices)",
            f"{90.0 - crit_deg_f:.1f}°",
            f"{crit_deg_f * 2:.1f}°",
            f"{crit_deg_f / 2:.1f}°",
            f"{45.0:.1f}°",
            f"{crit_deg_f + 8.5:.1f}°",
            f"0.00°"
        ]
        q_text_fib = f"An optical fiber consists of a **{c_name}** (refractive index n_core = {n_core:.2f}) surrounded by a **{clad_name}** (n_cladding = {n_clad:.2f}). To achieve Total Internal Reflection inside the core, what is the CRITICAL ANGLE (θ_c) at the internal core-cladding boundary?"
        expl_fib = f"TIR at core-cladding boundary: sin(θ_c) = n_cladding / n_core = {n_clad:.2f} / {n_core:.2f} = {sin_crit_f:.4f}. θ_c = sin⁻¹({sin_crit_f:.4f}) = {corr_crit_f}."
        add_q("hard", "Optical Fiber Physics", q_text_fib, corr_crit_f, wrs_crit_f, "Evaluating", "Calculate internal critical angle for optical fiber cable", expl_fib)

    # 3. Wavelength and Speed Changes Across Media:
    # Wavelength in medium: λ_med = λ_vacuum / n
    for mat_n, n_val in refractive_materials:
        for lam_vac_nm in [400, 450, 500, 550, 589, 600, 633, 650, 700]:
            if counts["hard"] >= 200:
                break
            lam_med_nm = lam_vac_nm / n_val
            corr_lam_med = f"{lam_med_nm:.1f} nm"
            wrs_lam_med = [
                f"{lam_vac_nm * n_val:.1f} nm (multiplied wavelength by n instead of dividing)",
                f"{lam_vac_nm:.1f} nm (assumed wavelength does not change across boundary)",
                f"{lam_med_nm * 2:.1f} nm",
                f"{lam_med_nm / 2:.1f} nm",
                f"{lam_med_nm + 75.0:.1f} nm",
                f"{n_val * 100:.1f} nm",
                f"{lam_med_nm * 1.5:.1f} nm"
            ]
            q_text_shift = f"A beam of yellow helium-neon laser light has a wavelength of {lam_vac_nm} nm in vacuum. As this light beam enters a slab of **{mat_n}** (refractive index n = {n_val:.2f}), what is the new wavelength of the light INSIDE the {mat_n}?"
            expl_shift = f"Light slows down in an optical medium: v = c / n. Frequency f remains constant. Therefore λ_medium = v / f = (c / n) / f = λ_vacuum / n = {lam_vac_nm} nm / {n_val:.2f} = {corr_lam_med}."
            add_q("hard", "Wavelength in Optical Media", q_text_shift, corr_lam_med, wrs_lam_med, "Evaluating", f"Calculate compressed wavelength inside {mat_n}", expl_shift)

    return questions

if __name__ == '__main__':
    qs = build_waves_sound_and_light()
    out_dir = "dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_waves_sound_and_light.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
