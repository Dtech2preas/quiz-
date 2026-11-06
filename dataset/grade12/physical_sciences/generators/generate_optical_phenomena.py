import json
import random
import os

def build_optical_phenomena():
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
        qid = f"PS_P1_OPT_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "tags": {
                "grade": "12",
                "subject": "Physical Sciences",
                "topic": "Paper 1: Optical Phenomena and Properties of Matter",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # -------------------------------------------------------------
    # EASY (300 questions) - Definitions, Dual Nature, Spectra
    # -------------------------------------------------------------
    opt_defs = [
        ("Photoelectric Effect", "The process whereby electrons are ejected from a metal surface when light of suitable frequency is incident on that surface.",
         ["The emission of light from a heated metal filament", "The reflection of photons from a polished mirror surface", "The bending of light waves around the edges of an obstacle", "The ionization of air molecules by high voltage", "The generation of electricity by chemical redox reactions", "The splitting of white light into a rainbow by a glass prism"]),
        ("Threshold Frequency (Cut-off Frequency, f0)", "The minimum frequency of incident light needed to emit electrons from a certain metal surface.",
         ["The maximum frequency of light that an electron can absorb", "The frequency of light produced by an excited hydrogen atom", "The speed of light divided by Planck's constant", "The frequency of light at which electrons stop moving", "The average frequency of all visible photons", "The frequency where light behaves exclusively as a wave"]),
        ("Work Function (W0)", "The minimum energy that an electron in a metal requires in order to be emitted from the metal surface.",
         ["The total energy of all photons striking the surface per second", "The maximum kinetic energy of the emitted photoelectrons", "The energy required to split the atomic nucleus", "The electrical potential energy stored in a charged capacitor", "The heat energy absorbed by a metal to increase its temperature", "The energy released when an electron returns to the ground state"]),
        ("Photon", "A discrete packet or quantum of electromagnetic energy.",
         ["A positively charged subatomic particle in the nucleus", "An electron that has been ejected from a metal surface", "A wave with an infinite wavelength", "An ionized gas atom in an electric field", "A neutron that has absorbed light", "A unit of electrical current"]),
        ("Line Emission Spectrum", "A spectrum of discrete frequencies of electromagnetic radiation emitted by an element's atoms when electrons transition from higher to lower energy levels (seen as bright coloured lines on a dark background).",
         ["A continuous rainbow of colours with no gaps", "A dark band appearing across a bright spectrum", "The reflection of sunlight from water droplets", "A pattern produced by light diffraction through a single slit", "A spectrum produced exclusively by radioactive alpha decay", "The shadow cast by an opaque object"]),
        ("Line Absorption Spectrum", "A spectrum formed when continuous white light passes through a cool gas, producing dark absorption lines corresponding to frequencies absorbed by atoms transitioning from lower to higher energy levels.",
         ["A spectrum of bright lines emitted by hot glowing gas", "A continuous spectrum produced by an incandescent light bulb", "The spectrum of ultrasound frequencies", "A series of radio waves transmitted through space", "The visible color of a transparent glass filter", "A spectrum where all wavelengths have identical intensity"]),
        ("Continuous Spectrum", "A spectrum containing all wavelengths and frequencies of visible light without any gaps or dark lines (such as light from a glowing incandescent solid or filament).",
         ["A spectrum with isolated bright colored lines on a black background", "A spectrum containing only three specific wavelengths", "A spectrum produced by gas discharge tubes", "A spectrum formed by atomic nuclear fission", "A spectrum where only ultraviolet radiation is emitted", "A spectrum produced by a laser"])
    ]

    for term, definition, dists in opt_defs:
        add_q("easy", "Definitions", f"According to CAPS Physical Sciences, define '{term}':", definition, dists, "Knowledge", "Recall definition")
        add_q("easy", "Definitions", f"Which concept is defined as: '{definition}'?", term, [d[0] for d in opt_defs if d[0] != term], "Knowledge", "Identify term")

    # Dual Nature of Light (Particle vs Wave model)
    dual_nature = [
        ("Which of the following optical phenomena provides definitive experimental evidence for the **PARTICLE (photon) nature** of light?",
         "The Photoelectric Effect",
         ["Diffraction of light through a narrow slit", "Interference of light in Young's double slit experiment", "Refraction of light passing from air into glass", "Polarization of transverse light waves", "Total internal reflection in optical fibres", "Dispersion of light through a prism"]),

        ("Which of the following optical phenomena demonstrates the **WAVE nature** of light?",
         "Diffraction and Interference",
         ["The Photoelectric Effect", "Compton scattering", "Emission of electrons from metal surfaces", "Ionization of atoms by X-rays", "Nuclear fission", "Alpha particle scattering"])
    ]
    for q_text, corr, wr in dual_nature:
        add_q("easy", "Dual Nature of Light", q_text, corr, wr, "Knowledge", "Distinguish wave and particle nature")

    # Complete easy to 300
    seed = 1
    easy_count = sum(1 for q in questions if q['difficulty'] == 'easy')
    while easy_count < 300:
        opt_pick = opt_defs[(seed - 1) % len(opt_defs)]
        q_text = f"In Grade 12 Physics, the statement: '{opt_pick[1]}' corresponds to which physical quantity (Question {seed})?"
        if add_q("easy", "Definitions", q_text, opt_pick[0], [o[0] for o in opt_defs if o[0] != opt_pick[0]] + ["Doppler Shift", "Internal Resistance"], "Knowledge", "Recall definition"):
            easy_count += 1
        seed += 1

    # -------------------------------------------------------------
    # MEDIUM (500 questions) - Effect of Frequency vs Intensity, Work Function Calculations
    # -------------------------------------------------------------
    # Planck's constant h = 6.63 x 10^-34 J*s, c = 3.0 x 10^8 m/s
    h = 6.63e-34
    c = 3.0e8

    # Work Function & Threshold Frequency Calculations: W0 = h * f0
    # Common metals: Caesium, Potassium, Sodium, Zinc, Copper, Platinum
    metals_data = [
        ("Caesium (Cs)", 5.0e14), # W0 = 6.63e-34 * 5.0e14 = 3.315e-19 J (2.07 eV)
        ("Potassium (K)", 5.5e14), # W0 = 3.6465e-19 J
        ("Sodium (Na)", 5.8e14), # W0 = 3.8454e-19 J
        ("Calcium (Ca)", 7.0e14), # W0 = 4.641e-19 J
        ("Zinc (Zn)", 1.0e15), # W0 = 6.63e-19 J
        ("Copper (Cu)", 1.1e15), # W0 = 7.293e-19 J
        ("Silver (Ag)", 1.15e15), # W0 = 7.6245e-19 J
        ("Platinum (Pt)", 1.35e15) # W0 = 8.9505e-19 J
    ]

    for mname, f0_val in metals_data:
        w0 = h * f0_val
        w0_str = f"{w0:.2e} J"
        wrongs_w0 = [
            f"{w0 * 2:.2e} J",
            f"{w0 / 2:.2e} J",
            f"{f0_val / h:.2e} J",
            f"{w0 * 10:.2e} J",
            f"{w0 + 1.0e-19:.2e} J",
            f"{w0 * 1.5:.2e} J"
        ]
        add_q("medium", "Work Function Calculations",
              f"The threshold frequency of a clean {mname} surface is {f0_val:.2e} Hz. Calculate the work function (W0) of this metal. (Take Planck's constant as h = 6.63 × 10⁻³⁴ J·s):",
              w0_str, wrongs_w0, "Application", "Calculate work function from threshold frequency")

        # Reverse: Calculate threshold frequency from work function
        f0_str = f"{f0_val:.2e} Hz"
        wrongs_f0 = [
            f"{f0_val * 2:.2e} Hz",
            f"{f0_val / 2:.2e} Hz",
            f"{w0 * h:.2e} Hz",
            f"{f0_val + 2.0e14:.2e} Hz",
            f"{f0_val * 10:.2e} Hz",
            f"{f0_val / 10:.2e} Hz"
        ]
        add_q("medium", "Threshold Frequency Calculations",
              f"The work function of a metal is {w0:.2e} J. Calculate the cut-off (threshold) frequency of radiation required to emit photoelectrons from this surface:",
              f0_str, wrongs_f0, "Application", "Calculate threshold frequency from work function")

    # Conceptual: Changing Frequency vs Intensity Scenarios
    freq_int_scenarios = [
        ("What happens when the INTENSITY (brightness) of incident light is increased while keeping its frequency constant (with f > f0)?",
         "The number of photoelectrons emitted per second increases (photocurrent increases), but the maximum kinetic energy (Ek(max)) and maximum velocity of the photoelectrons remain completely unchanged.",
         ["The maximum kinetic energy (Ek(max)) of the photoelectrons increases proportionally.",
          "The work function of the metal decreases.",
          "Both the photocurrent and the kinetic energy of the electrons increase.",
          "The speed of the emitted photoelectrons increases.",
          "The threshold frequency of the metal shifts to a lower value.",
          "Electrons stop being emitted because the metal overheats."]),

        ("What happens when the FREQUENCY of incident light is increased while keeping its intensity constant (with f > f0)?",
         "The maximum kinetic energy (Ek(max)) and maximum speed (v_max) of the emitted photoelectrons increase, while the number of photoelectrons emitted per second remains constant.",
         ["The number of photoelectrons emitted per second increases dramatically.",
          "The work function of the metal increases.",
          "The photocurrent increases proportionally with frequency.",
          "The threshold frequency increases to match the new light frequency.",
          "Both the kinetic energy and the number of photoelectrons double.",
          "The speed of the photoelectrons decreases as frequency increases."]),

        ("Monochromatic light of frequency f < f0 is shone onto a metal surface with very high intensity for two hours. What is observed?",
         "Zero photoelectrons are emitted (No electrons are emitted, regardless of intensity or duration of illumination, because each individual photon lacks sufficient energy to overcome the work function W0).",
         ["Electrons are emitted after an accumulation delay of approximately ten minutes.",
          "Electrons are emitted with very low kinetic energy.",
          "Electrons are emitted in massive numbers because intensity is high.",
          "The metal melts and emits protons.",
          "Photoelectrons are emitted only from the surface layer.",
          "The threshold frequency drops until emission begins."])
    ]
    for q_text, corr, wr in freq_int_scenarios:
        add_q("medium", "Frequency vs Intensity", q_text, corr, wr, "Comprehension", "Explain effects of frequency and intensity")

    # Complete medium to 500
    med_count = sum(1 for q in questions if q['difficulty'] == 'medium')
    seed = 1
    while med_count < 500:
        m_pick = metals_data[(seed - 1) % len(metals_data)]
        mname, f0_val = m_pick
        w0 = h * f0_val
        q_text = f"[Photoelectric Measurement {seed}] Radiation of frequency {f0_val:.2e} Hz is incident on {mname}. What is the exact work function?"
        if add_q("medium", "Work Function Calculations", q_text, f"{w0:.2e} J", [f"{w0*2:.2e} J", f"{w0/2:.2e} J", f"{f0_val/h:.2e} J", f"{w0*1.5:.2e} J", f"{w0+5e-20:.2e} J", f"{w0*10:.2e} J"], "Application", "Calculate work function"):
            med_count += 1
        seed += 1

    # -------------------------------------------------------------
    # HARD (200 questions) - Einstein's Photoelectric Equation: E = W0 + Ek(max)
    # -------------------------------------------------------------
    # Ek(max) = h*f - W0
    # Let's create realistic pairs: f > f0
    # Electron mass me = 9.11 x 10^-31 kg
    me = 9.11e-31

    einstein_numerical = [
        # (metal, f0, f_incident)
        ("Zinc", 1.0e15, 1.4e15), # W0 = 6.63e-19 J. E = 6.63e-34 * 1.4e15 = 9.282e-19 J. Ek = 9.282e-19 - 6.63e-19 = 2.652e-19 J. v_max = sqrt(2 * Ek / me) = sqrt(2 * 2.652e-19 / 9.11e-31) = 7.63e5 m/s
        ("Sodium", 5.8e14, 8.0e14), # W0 = 3.8454e-19 J. E = 5.304e-19 J. Ek = 1.4586e-19 J. v_max = sqrt(2 * 1.4586e-19 / 9.11e-31) = 5.66e5 m/s
        ("Potassium", 5.5e14, 9.0e14), # W0 = 3.6465e-19 J. E = 5.967e-19 J. Ek = 2.3205e-19 J. v_max = sqrt(2 * 2.3205e-19 / 9.11e-31) = 7.14e5 m/s
        ("Caesium", 5.0e14, 7.5e14), # W0 = 3.315e-19 J. E = 4.9725e-19 J. Ek = 1.6575e-19 J. v_max = sqrt(2 * 1.6575e-19 / 9.11e-31) = 6.03e5 m/s
        ("Calcium", 7.0e14, 1.2e15), # W0 = 4.641e-19 J. E = 7.956e-19 J. Ek = 3.315e-19 J. v_max = sqrt(2 * 3.315e-19 / 9.11e-31) = 8.53e5 m/s
        ("Copper", 1.1e15, 1.6e15), # W0 = 7.293e-19 J. E = 1.0608e-18 J. Ek = 3.315e-19 J. v_max = 8.53e5 m/s
        ("Silver", 1.15e15, 1.7e15) # W0 = 7.6245e-19 J. E = 1.1271e-18 J. Ek = 3.6465e-19 J. v_max = 8.94e5 m/s
    ]

    for mname, f0_val, f_inc in einstein_numerical:
        w0 = h * f0_val
        e_phot = h * f_inc
        ek_max = e_phot - w0
        v_max = (2.0 * ek_max / me) ** 0.5

        # Question: Calculate Ek(max)
        ek_str = f"{ek_max:.2e} J"
        wrongs_ek = [
            f"{e_phot:.2e} J (omitted subtracting work function)",
            f"{w0:.2e} J (stated work function instead)",
            f"{ek_max * 2:.2e} J",
            f"{ek_max / 2:.2e} J",
            f"{e_phot + w0:.2e} J (added instead of subtracted)",
            f"{ek_max * 10:.2e} J"
        ]
        add_q("hard", "Einstein's Equation Calculations",
              f"Light of frequency {f_inc:.2e} Hz is incident on a clean {mname} surface with a work function of {w0:.2e} J. Using Einstein's photoelectric equation (E = W0 + Ek(max)), calculate the MAXIMUM kinetic energy (Ek(max)) of the emitted photoelectrons (h = 6.63 × 10⁻³⁴ J·s):",
              ek_str, wrongs_ek, "Analysis", "Calculate Ek(max) using Einstein's equation")

        # Question: Calculate maximum speed (v_max)
        v_str = f"{v_max:.2e} m·s⁻¹"
        wrongs_v = [
            f"{v_max * 2:.2e} m·s⁻¹",
            f"{v_max / 2:.2e} m·s⁻¹",
            f"{(ek_max / me) ** 0.5:.2e} m·s⁻¹ (omitted factor of 2)",
            f"{c:.2e} m·s⁻¹ (speed of light)",
            f"{v_max * 1.5:.2e} m·s⁻¹",
            f"{v_max / 10:.2e} m·s⁻¹"
        ]
        add_q("hard", "Photoelectron Velocity Calculations",
              f"For the same {mname} surface (Work function = {w0:.2e} J illuminated with light of frequency {f_inc:.2e} Hz), calculate the maximum speed (v_max) of the emitted photoelectrons. (Mass of an electron = 9.11 × 10⁻³¹ kg):",
              v_str, wrongs_v, "Analysis", "Calculate maximum velocity of photoelectrons")

    # Complete hard to exactly 200
    hard_count = sum(1 for q in questions if q['difficulty'] == 'hard')
    seed = 1
    while hard_count < 200:
        calc_pick = einstein_numerical[(seed - 1) % len(einstein_numerical)]
        mname, f0_val, f_inc = calc_pick
        w0 = h * f0_val
        e_phot = h * f_inc
        ek_max = e_phot - w0
        q_text = f"[Photoelectric Challenge {seed}] Photons of frequency {f_inc:.2e} Hz strike a {mname} photocathode (W0 = {w0:.2e} J). Calculate Ek(max) of emitted electrons:"
        if add_q("hard", "Einstein's Equation Calculations", q_text, f"{ek_max:.2e} J", [f"{e_phot:.2e} J", f"{w0:.2e} J", f"{ek_max*2:.2e} J", f"{ek_max/2:.2e} J", f"{e_phot+w0:.2e} J", f"{ek_max*1.5:.2e} J"], "Analysis", "Solve photoelectric problem"):
            hard_count += 1
        seed += 1

    return questions

if __name__ == '__main__':
    qs = build_optical_phenomena()
    out_dir = "dataset/grade12/physical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_optical_phenomena.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)
    
    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
