import json
import math
import os

def build_optical_phenomena():
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
        qid = f"PS_P1_OPT_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Paper 1: Optical Phenomena and Properties of Matter",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
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

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Dual Nature, Spectra Concepts, Intensity vs Frequency
    # =========================================================================

    core_definitions = [
        ("Photoelectric Effect",
         "The process whereby electrons are ejected from a metal surface when light of suitable frequency is incident on that surface.",
         ["The emission of visible light when an electric current passes through a cold gas",
          "The reflection of electromagnetic radiation from a polished metallic mirror",
          "The splitting of white light into a rainbow spectrum by a glass prism",
          "The creation of an electric current by moving a copper wire through a magnetic field",
          "The continuous absorption of heat by a blackened metal plate",
          "The thermal emission of electrons caused exclusively by high temperatures"],
         "In CAPS Grade 12 Physical Sciences, the photoelectric effect is defined as the process whereby electrons are ejected from a metal surface when light of suitable frequency is incident on that surface."),

        ("Threshold Frequency (Cut-off Frequency, f_0)",
         "The minimum frequency of incident radiation required to eject photoelectrons from a particular metal surface.",
         ["The maximum frequency of light that a metal can reflect without absorbing heat",
          "The frequency at which electrons begin orbiting in opposite directions",
          "The frequency of light that produces destructive wave interference",
          "The speed of light divided by Planck's constant",
          "The frequency of radiation emitted when an electron falls to the ground state",
          "The constant frequency of all electromagnetic waves in vacuum"],
         "Threshold frequency (f_0) is the minimum frequency of light needed to overcome the binding energy (work function) and eject an electron: W_0 = h * f_0."),

        ("Work Function (W_0)",
         "The minimum energy that an electron in a metal requires to be emitted from the metal surface.",
         ["The kinetic energy of photoelectrons moving at the speed of light",
          "The total electrical energy stored inside a fully charged capacitor",
          "The mechanical work done in moving an electron between two plates",
          "The thermal heat energy required to melt one mole of metal cathode",
          "The energy released when an electron annihilates with a positron",
          "The potential energy of a photon resting on a metallic surface"],
         "Work function (W_0) is the minimum energy required to overcome the electrostatic attraction holding an electron to the metal lattice."),

        ("Atomic Emission Spectrum",
         "A pattern of discrete bright colored spectral lines on a dark background, formed when excited electrons in atoms transition from higher to lower energy levels, emitting photons of specific frequencies.",
         ["A continuous rainbow band formed by glowing solid incandescent filaments",
          "A series of dark absorption lines superimposed on a bright continuous spectrum",
          "The shadow pattern cast by an obstacle during Fresnel diffraction",
          "An alternating series of sound compression and rarefaction peaks",
          "A graph showing the velocity distribution of photoelectrons",
          "The electromagnetic radiation curve emitted by a black body at 0 K"],
         "An atomic emission spectrum consists of discrete bright lines produced when excited electrons drop to lower energy levels: E = h * f = E_higher - E_lower."),

        ("Atomic Absorption Spectrum",
         "A pattern of dark lines on a continuous colored background, formed when white light passes through a cold gas and atoms absorb specific photon frequencies matching electron transitions.",
         ["A pattern of bright glowing lines seen against a completely pitch-black backdrop",
          "A continuous band of visible colors containing no interruptions or dark gaps",
          "The pattern of electron diffraction rings produced through thin gold foil",
          "A spectrogram showing complete reflection of all wavelengths",
          "The spectrum produced by pure synchrotron radiation",
          "A thermal gradient displaying temperature variations across a gas cloud"],
         "An atomic absorption spectrum shows dark lines at exact frequencies where cold gas atoms absorbed photons matching their quantized excitation energy gaps."),

        ("Photon",
         "A quantum (discrete packet) of electromagnetic energy.",
         ["A negatively charged fundamental particle inside atomic nuclei",
          "A positively charged ion emitted during radioactive alpha decay",
          "A stationary magnetic dipole embedded in a metal lattice",
          "A sound wave pulse travelling through an acoustic medium",
          "A unit of electrical capacitance equal to one farad",
          "An electron that has been completely stripped of its electrical charge"],
         "A photon is the discrete quantum of electromagnetic radiation with energy E = h * f.")
    ]

    stems = [
        "In Grade 12 Physical Sciences, what is the official CAPS definition of **'{}'**?",
        "According to the examination guidelines, **'{}'** is defined as:",
        "Which statement provides the precise scientific definition for **'{}'**?",
        "Identify the correct CAPS definition for **'{}'**:",
        "When an examiner asks for the definition of **'{}'**, which statement receives full marks?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Dual Nature of Light & Wave vs Particle Models
    dual_nature_questions = [
        ("Which optical phenomenon provides definitive experimental evidence for the **PARTICLE (photon) nature** of light?",
         "The Photoelectric Effect.",
         ["Refraction of light through glass prisms",
          "Diffraction of light around sharp edges",
          "Interference of light in Young's double-slit experiment",
          "Polarization of transverse light waves through Polaroid filters",
          "Dispersion of white light into a rainbow",
          "Total internal reflection inside optical fiber cables"],
         "The photoelectric effect demonstrates that light transfers energy in discrete packets (quanta or photons), proving the particle model of light."),

        ("Which physical phenomena provide empirical evidence for the **WAVE nature** of light?",
         "Diffraction, interference, and polarization of light waves.",
         ["The photoelectric effect and Compton scattering",
          "Thermionic electron emission and cathode ray deflection",
          "Alpha particle scattering and nuclear fission",
          "The discrete emission line spectra of gaseous hydrogen",
          "The blackbody radiation ultraviolet catastrophe",
          "The constant mass-to-charge ratio of the electron"],
         "Wave phenomena such as interference (Young's double slit), diffraction, and polarization confirm that light behaves as a transverse wave."),

        ("What is the fundamental conclusion of the dual nature of electromagnetic radiation?",
         "Light exhibits wave properties during propagation (interference, diffraction) and particle properties during interaction with matter (photoelectric effect).",
         ["Light is composed solely of continuous classical water waves with zero particles.",
          "Light consists exclusively of solid microscopic spheres that never undergo diffraction.",
          "Electrons and photons have identical mass, charge, and spin at all times.",
          "Light travels instantaneously at infinite speed through all physical media.",
          "Light only exists when observed directly by a human eye.",
          "Light loses its energy completely when passing through empty vacuum."],
         "The wave-particle duality states that electromagnetic radiation propagates as a wave but exchanges energy with matter as discrete particles (photons).")
    ]

    for q_dn, c_dn, w_dn, exp_dn in dual_nature_questions:
        add_q("easy", "Dual Nature of Light", q_dn, c_dn, w_dn, "Understanding", "Explain wave-particle duality of light", exp_dn)

    # Intensity vs Frequency Qualitative Scenarios
    param_effects = [
        ("Increasing the INTENSITY (brightness) of incident light above the threshold frequency (f > f_0)",
         "Increases the number of photoelectrons emitted per second (photocurrent), while leaving the maximum kinetic energy (E_k(max)) and maximum speed of ejected electrons UNCHANGED.",
         ["Increases the maximum kinetic energy of the ejected photoelectrons.",
          "Decreases the number of photoelectrons emitted per second.",
          "Increases the threshold frequency (f_0) of the target metal.",
          "Decreases the work function (W_0) of the metallic surface.",
          "Stops electron emission completely due to space charge buildup.",
          "Causes electrons to be emitted with relativistic velocities instantly."]),

        ("Increasing the FREQUENCY of incident light above the threshold frequency (f > f_0) while keeping intensity constant",
         "Increases the maximum kinetic energy (E_k(max)) and maximum velocity of the ejected photoelectrons, while the rate of electron emission (photocurrent) remains UNCHANGED.",
         ["Increases the number of photoelectrons emitted per second.",
          "Decreases the energy of individual incident photons.",
          "Increases the work function (W_0) of the metal cathode.",
          "Decreases the stopping potential required to halt photocurrent.",
          "Causes the metal cathode to absorb photoelectrons from the circuit.",
          "Doubles the threshold frequency of the metal."]),

        ("Shining light with a frequency LOWER than the threshold frequency (f < f_0) onto a metal surface",
         "Zero photoelectrons are emitted, regardless of how intense (bright) the light is or how long it shines on the surface.",
         ["Electrons are emitted after a 10-minute delay as energy accumulates.",
          "A small photocurrent is produced if the light beam is extremely bright.",
          "Electrons are emitted with negative kinetic energy.",
          "The metal cathode absorbs photons until its work function drops to zero.",
          "Photoelectrons are emitted only from the deepest atomic layers.",
          "The light converts into high-energy gamma rays at the surface."]),

        ("What determines whether electrons will be emitted from a metal surface in the photoelectric effect?",
         "The frequency (energy) of the incident photons relative to the threshold frequency (work function) of the specific metal.",
         ["The surface area of the metal plate alone",
          "The thickness of the glass vacuum tube containing the photocell",
          "The distance between the metal cathode and the battery terminal",
          "The color of the wire connecting the ammeter to the circuit",
          "The total volume of light shining in the entire laboratory",
          "The angle of the Earth's magnetic field relative to the cathode"])
    ]

    for q_pe, c_pe, w_pe in param_effects:
        add_q("easy", "Photoelectric Principles", q_pe, c_pe, w_pe, "Understanding", "Understand frequency vs intensity effects", c_pe)

    # Spectral Line Origins and Transitions
    spectral_origins = [
        ("How is a dark absorption line in an atomic absorption spectrum produced?",
         "An electron in an atom absorbs a photon with energy EXACTLY equal to the difference between two quantum energy levels (E = E2 - E1 = h*f), jumping from a lower to a higher energy state.",
         ["An electron falls from an outer orbit to an inner orbit emitting light.",
          "A photon is reflected backward by the atomic nucleus.",
          "An electron escapes completely from the atom as a free photoelectron.",
          "Protons inside the nucleus absorb electromagnetic radiation.",
          "The atom undergoes nuclear fusion to form a heavier element.",
          "Light waves undergo total destructive interference with sound waves."]),

        ("How is a bright emission line in an atomic emission spectrum produced?",
         "An excited electron in an atom drops from a higher energy level to a lower energy level, emitting a single photon whose energy equals the exact difference between the two states (E = E_high - E_low = h*f).",
         ["An electron absorbs white light and jumps to an excited energy state.",
          "Photons collide with each other in empty space to create color.",
          "The atomic nucleus expels an electron into the surrounding gas.",
          "The gas undergoes chemical combustion in oxygen gas.",
          "Electrons oscillate back and forth like classical pendulum bobs.",
          "Heat energy is converted directly into gravitational potential energy."]),

        ("What do the dark lines (Fraunhofer lines) observed in the solar spectrum indicate?",
         "Specific chemical elements present in the cooler outer gaseous atmosphere (chromosphere) of the Sun that have absorbed characteristic photon frequencies from the continuous core spectrum.",
         ["Defects in the optical glass lenses of Earth's astronomical telescopes.",
          "Interstellar black holes absorbing all visible starlight along the line of sight.",
          "Regions on the Sun where nuclear fusion has permanently ceased.",
          "Shadows cast by planetary moons orbiting between the Sun and Earth.",
          "Sound waves travelling across interplanetary space.",
          "The cooling down of the Sun's core to absolute zero."])
    ]

    for q_so, c_so, w_so in spectral_origins:
        add_q("easy", "Spectra Formation", q_so, c_so, w_so, "Understanding", "Explain origins of atomic spectra", c_so)

    # Fill easy to exactly 300 with diverse threshold comparisons for various metals
    # Metals and their work functions (in 10^-19 J)
    metal_data = [
        ("Caesium (Cs)", 3.42, 2.14, "alkali metal"),
        ("Potassium (K)", 3.68, 2.30, "alkali metal"),
        ("Sodium (Na)", 3.65, 2.28, "alkali metal"),
        ("Lithium (Li)", 4.00, 2.50, "alkali metal"),
        ("Calcium (Ca)", 4.60, 2.87, "alkaline earth metal"),
        ("Magnesium (Mg)", 5.90, 3.68, "alkaline earth metal"),
        ("Aluminium (Al)", 6.53, 4.08, "post-transition metal"),
        ("Zinc (Zn)", 6.88, 4.30, "transition metal"),
        ("Iron (Fe)", 7.20, 4.50, "transition metal"),
        ("Copper (Cu)", 7.52, 4.70, "transition metal"),
        ("Silver (Ag)", 7.58, 4.74, "precious metal"),
        ("Gold (Au)", 8.16, 5.10, "noble metal"),
        ("Platinum (Pt)", 10.16, 6.35, "noble metal")
    ]

    for m_name, w_j, w_ev, m_type in metal_data:
        f_0 = (w_j * 1e-19) / 6.63e-34
        for mult in [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.92, 0.95, 0.98,
                     1.02, 1.05, 1.08, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50, 1.60, 1.75, 2.00]:
            if counts["easy"] >= 300:
                break
            test_f = f_0 * mult
            if mult < 1.0:
                corr_out = f"NO photoelectrons are emitted, because the incident frequency ({test_f * 1e-14:.2f} × 10¹⁴ Hz) is LESS than the threshold frequency of {m_name} ({f_0 * 1e-14:.2f} × 10¹⁴ Hz)."
                wr_outs = [
                    f"Photoelectrons are emitted with high kinetic energy because intensity compensates for frequency.",
                    f"Photoelectrons are emitted after a 5-minute time lag.",
                    f"Photoelectrons are emitted but with negative kinetic energy.",
                    f"The work function of {m_name} decreases to allow emission.",
                    f"Electrons are absorbed by the incident light beam.",
                    f"The threshold frequency of {m_name} drops to zero."
                ]
            else:
                corr_out = f"Photoelectrons ARE emitted, because the incident frequency ({test_f * 1e-14:.2f} × 10¹⁴ Hz) EXCEEDS the threshold frequency of {m_name} ({f_0 * 1e-14:.2f} × 10¹⁴ Hz)."
                wr_outs = [
                    f"No photoelectrons are emitted because the frequency is too high.",
                    f"Electrons are emitted only if the light intensity is above 1000 W/m².",
                    f"Photoelectrons are emitted without any kinetic energy.",
                    f"The metal cathode absorbs all incident photons without emission.",
                    f"Emission occurs only if the metal is heated to 1000 °C.",
                    f"Electrons convert into gamma rays inside the metal lattice."
                ]
            q_text = f"Monochromatic light of frequency {test_f * 1e-14:.2f} × 10¹⁴ Hz is shone onto a clean surface of {m_name} (work function W_0 = {w_j:.2f} × 10⁻¹⁹ J, threshold frequency f_0 = {f_0 * 1e-14:.2f} × 10¹⁴ Hz). What occurs at the metal surface?"
            add_q("easy", "Threshold Emission", q_text, corr_out, wr_outs, "Understanding", f"Predict photoelectric emission for {m_name}", corr_out)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Direct Calculations: E = hf, E = hc/λ, W_0 = hf_0, E_k(max) = hf - W_0
    # =========================================================================

    # Physical Constants
    h = 6.63e-34 # J s
    c = 3.0e8    # m/s
    m_e = 9.11e-31 # kg

    # Category 1: Photon Energy Calculations (E = h*f and E = h*c/λ)
    photon_freqs = [
        (4.5e14, "red light", 667),
        (5.0e14, "orange light", 600),
        (5.5e14, "yellow light", 545),
        (6.0e14, "green light", 500),
        (6.5e14, "cyan light", 462),
        (7.0e14, "blue light", 429),
        (7.5e14, "violet light", 400),
        (8.0e14, "near ultraviolet", 375),
        (8.5e14, "ultraviolet radiation", 353),
        (9.0e14, "ultraviolet radiation", 333),
        (9.5e14, "ultraviolet radiation", 316),
        (1.0e15, "middle ultraviolet", 300),
        (1.1e15, "deep ultraviolet", 273),
        (1.2e15, "extreme ultraviolet", 250),
        (1.5e15, "vacuum ultraviolet", 200)
    ]

    for f_val, light_color, lam_nm in photon_freqs:
        e_val = h * f_val
        corr_e = f"{e_val * 1e19:.2f} × 10⁻¹⁹ J"
        wrs_e = [
            f"{(e_val * 1e19) * 2:.2f} × 10⁻¹⁹ J",
            f"{(e_val * 1e19) / 2:.2f} × 10⁻¹⁹ J",
            f"{(h / f_val) * 1e48:.2f} × 10⁻¹⁹ J (divided h by f)",
            f"{e_val * 1e19 + 2.5:.2f} × 10⁻¹⁹ J",
            f"{(e_val * 1e19) * 1.5:.2f} × 10⁻¹⁹ J",
            f"{f_val * 1e-14:.2f} × 10⁻¹⁹ J",
            f"{lam_nm:.2f} × 10⁻¹⁹ J"
        ]
        q_text = f"Calculate the energy of a single photon of {light_color} having a frequency of {f_val * 1e-14:.2f} × 10¹⁴ Hz (Planck's constant h = 6.63 × 10⁻³⁴ J·s):"
        expl = f"E = h × f = (6.63 × 10⁻³⁴ J·s) × ({f_val * 1e-14:.2f} × 10¹⁴ s⁻¹) = {corr_e}."
        add_q("medium", "Photon Energy", q_text, corr_e, wrs_e, "Applying", "Calculate photon energy from frequency", expl)

        # Wavelength version: E = h * c / λ
        lam_m = lam_nm * 1e-9
        e_lam = (h * c) / lam_m
        corr_elam = f"{e_lam * 1e19:.2f} × 10⁻¹⁹ J"
        wrs_elam = [
            f"{(e_lam * 1e19) * 2:.2f} × 10⁻¹⁹ J",
            f"{(e_lam * 1e19) / 2:.2f} × 10⁻¹⁹ J",
            f"{(h * lam_m / c) * 1e38:.2f} × 10⁻¹⁹ J (inverted wave equation)",
            f"{e_lam * 1e19 + 1.8:.2f} × 10⁻¹⁹ J",
            f"{(e_lam * 1e19) * 1.4:.2f} × 10⁻¹⁹ J",
            f"{lam_nm:.1f} × 10⁻¹⁹ J",
            f"{(h * c) * 1e25:.2f} × 10⁻¹⁹ J"
        ]
        q_text_lam = f"Calculate the energy of a photon of {light_color} having a wavelength of {lam_nm} nm in vacuum (h = 6.63 × 10⁻³⁴ J·s, c = 3.0 × 10⁸ m·s⁻¹):"
        expl_lam = f"E = h × c / λ = (6.63 × 10⁻³⁴ × 3.0 × 10⁸) / ({lam_nm} × 10⁻⁹ m) = (1.989 × 10⁻²⁵) / ({lam_nm} × 10⁻⁹) = {corr_elam}."
        add_q("medium", "Photon Energy", q_text_lam, corr_elam, wrs_elam, "Applying", "Calculate photon energy from wavelength", expl_lam)

    # Category 2: Threshold Frequency and Work Function Calculations
    for m_name, w_j, w_ev, _ in metal_data:
        w_joules = w_j * 1e-19
        f_thresh = w_joules / h
        corr_f0 = f"{f_thresh * 1e-14:.2f} × 10¹⁴ Hz"
        wrs_f0 = [
            f"{(f_thresh * 1e-14) * 2:.2f} × 10¹⁴ Hz",
            f"{(f_thresh * 1e-14) / 2:.2f} × 10¹⁴ Hz",
            f"{(w_joules * h) * 1e53:.2f} × 10¹⁴ Hz (multiplied W_0 by h)",
            f"{f_thresh * 1e-14 + 1.5:.2f} × 10¹⁴ Hz",
            f"{(f_thresh * 1e-14) * 1.5:.2f} × 10¹⁴ Hz",
            f"{w_j:.2f} × 10¹⁴ Hz",
            f"{w_ev:.2f} × 10¹⁴ Hz"
        ]
        q_text_w = f"The work function of {m_name} is {w_j:.2f} × 10⁻¹⁹ J. Taking Planck's constant as h = 6.63 × 10⁻³⁴ J·s, determine the threshold (cut-off) frequency (f_0) of this metal:"
        expl_w = f"W_0 = h × f_0 => f_0 = W_0 / h = ({w_j:.2f} × 10⁻¹⁹ J) / (6.63 × 10⁻³⁴ J·s) = {corr_f0}."
        add_q("medium", "Threshold Frequency", q_text_w, corr_f0, wrs_f0, "Applying", f"Calculate threshold frequency of {m_name}", expl_w)

        # Threshold wavelength: λ_0 = c / f_0 = h * c / W_0
        lam_thresh = (h * c) / w_joules
        lam_nm_0 = lam_thresh * 1e9
        corr_lam0 = f"{lam_nm_0:.1f} nm"
        wrs_lam0 = [
            f"{lam_nm_0 * 2:.1f} nm",
            f"{lam_nm_0 / 2:.1f} nm",
            f"{(w_joules / (h * c)) * 1e-7:.1f} nm",
            f"{lam_nm_0 + 80.0:.1f} nm",
            f"{lam_nm_0 * 1.5:.1f} nm",
            f"{f_thresh * 1e-14:.1f} nm",
            f"{w_j * 100:.1f} nm"
        ]
        q_text_lam0 = f"Determine the maximum (cut-off) wavelength (λ_0) of incident light capable of ejecting photoelectrons from {m_name} (work function W_0 = {w_j:.2f} × 10⁻¹⁹ J, c = 3.0 × 10⁸ m·s⁻¹, h = 6.63 × 10⁻³⁴ J·s):"
        expl_lam0 = f"λ_0 = h × c / W_0 = (6.63 × 10⁻³⁴ × 3.0 × 10⁸) / ({w_j:.2f} × 10⁻¹⁹ J) = (1.989 × 10⁻²⁵) / ({w_j:.2f} × 10⁻¹⁹) = {corr_lam0}."
        add_q("medium", "Threshold Wavelength", q_text_lam0, corr_lam0, wrs_lam0, "Applying", f"Calculate threshold wavelength of {m_name}", expl_lam0)

    # Category 3: Maximum Kinetic Energy Calculations: E_k(max) = E - W_0 = h*f - W_0
    for m_name, w_j, w_ev, _ in metal_data:
        w_joules = w_j * 1e-19
        f_0 = w_joules / h
        # Test frequencies above f_0
        for f_factor in [1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.50, 1.60, 1.75, 1.90, 2.00, 2.20]:
            if counts["medium"] >= 500:
                break
            f_inc = f_0 * f_factor
            e_phot = h * f_inc
            ek_max = e_phot - w_joules
            corr_ek = f"{ek_max * 1e19:.2f} × 10⁻¹⁹ J"
            wrs_ek = [
                f"{e_phot * 1e19:.2f} × 10⁻¹⁹ J (calculated total photon energy without subtracting W_0)",
                f"{(e_phot + w_joules) * 1e19:.2f} × 10⁻¹⁹ J (added work function instead of subtracting)",
                f"{(ek_max * 1e19) * 2:.2f} × 10⁻¹⁹ J",
                f"{(ek_max * 1e19) / 2:.2f} × 10⁻¹⁹ J",
                f"{w_j:.2f} × 10⁻¹⁹ J",
                f"{ek_max * 1e19 + 1.25:.2f} × 10⁻¹⁹ J",
                f"{(ek_max * 1e19) * 1.5:.2f} × 10⁻¹⁹ J"
            ]
            q_text_ek = f"Light of frequency {f_inc * 1e-14:.2f} × 10¹⁴ Hz shines on a clean plate of {m_name} (work function W_0 = {w_j:.2f} × 10⁻¹⁹ J). Using h = 6.63 × 10⁻³⁴ J·s, calculate the maximum kinetic energy (E_k(max)) of the ejected photoelectrons:"
            expl_ek = f"Photoelectric equation: E = W_0 + E_k(max) => E_k(max) = h × f - W_0 = (6.63 × 10⁻³⁴ × {f_inc * 1e-14:.2f} × 10¹⁴) - {w_j:.2f} × 10⁻¹⁹ J = {e_phot * 1e19:.2f} × 10⁻¹⁹ - {w_j:.2f} × 10⁻¹⁹ = {corr_ek}."
            add_q("medium", "Kinetic Energy Calculations", q_text_ek, corr_ek, wrs_ek, "Applying", f"Calculate maximum photoelectron kinetic energy for {m_name}", expl_ek)

    # Complete medium to exactly 500 with diverse, non-repeating quantitative questions
    # 1. Quantized Atomic Energy Level Transitions in Hydrogen (Bohr Transitions)
    for n_low in range(1, 6):
        for n_high in range(n_low + 1, 9):
            if counts["medium"] >= 500:
                break
            e_low = -13.6 / (n_low ** 2)
            e_high = -13.6 / (n_high ** 2)
            de_ev = round(e_high - e_low, 3)
            de_joules = de_ev * 1.6e-19
            f_trans = de_joules / h
            lam_trans = (c / f_trans) * 1e9 # in nm

            # Frequency of transition
            corr_ft = f"{f_trans * 1e-14:.2f} × 10¹⁴ Hz"
            wrs_ft = [
                f"{(f_trans * 1e-14) * 2:.2f} × 10¹⁴ Hz",
                f"{(f_trans * 1e-14) / 2:.2f} × 10¹⁴ Hz",
                f"{de_ev:.2f} × 10¹⁴ Hz (omitted eV to Joule conversion)",
                f"{f_trans * 1e-14 + 1.25:.2f} × 10¹⁴ Hz",
                f"{(f_trans * 1e-14) * 1.5:.2f} × 10¹⁴ Hz",
                f"{(de_joules * h) * 1e50:.2f} × 10¹⁴ Hz",
                f"{de_ev * 10:.2f} × 10¹⁴ Hz"
            ]
            q_trans_f = f"In a hydrogen atom, an electron transitions from quantum energy level n = {n_high} ({e_high:.2f} eV) down to n = {n_low} ({e_low:.2f} eV). Calculate the frequency of the emitted photon (1 eV = 1.6 × 10⁻¹⁹ J, h = 6.63 × 10⁻³⁴ J·s):"
            expl_trans_f = f"ΔE = E_high - E_low = ({e_high:.2f} eV) - ({e_low:.2f} eV) = {de_ev:.3f} eV = {de_ev:.3f} × 1.6 × 10⁻¹⁹ J = {de_joules:.3e} J. Frequency f = ΔE / h = ({de_joules:.3e} J) / (6.63 × 10⁻³⁴ J·s) = {corr_ft}."
            add_q("medium", "Atomic Transitions", q_trans_f, corr_ft, wrs_ft, "Applying", f"Calculate photon frequency for hydrogen n={n_high} to n={n_low}", expl_trans_f)

            # Wavelength of transition
            if counts["medium"] < 500:
                corr_lt = f"{lam_trans:.1f} nm"
                wrs_lt = [
                    f"{lam_trans * 2:.1f} nm",
                    f"{lam_trans / 2:.1f} nm",
                    f"{lam_trans + 95.0:.1f} nm",
                    f"{lam_trans * 1.4:.1f} nm",
                    f"{f_trans * 1e-14:.1f} nm",
                    f"{de_ev * 100:.1f} nm",
                    f"{lam_trans - 45.0:.1f} nm"
                ]
                q_trans_l = f"What is the wavelength in nanometers of the photon emitted when an excited hydrogen atom undergoes an electron transition from level n = {n_high} ({e_high:.2f} eV) to n = {n_low} ({e_low:.2f} eV) (c = 3.0 × 10⁸ m·s⁻¹, h = 6.63 × 10⁻³⁴ J·s)?"
                expl_trans_l = f"ΔE = {de_joules:.3e} J. Wavelength λ = h × c / ΔE = (6.63 × 10⁻³⁴ × 3.0 × 10⁸) / ({de_joules:.3e}) = {lam_trans:.1f} × 10⁻⁹ m = {corr_lt}."
                add_q("medium", "Atomic Transitions", q_trans_l, corr_lt, wrs_lt, "Applying", f"Calculate photon wavelength for hydrogen n={n_high} to n={n_low}", expl_trans_l)

    # 2. Systematic Work Function Calculations from Threshold Frequencies
    step = 1
    while counts["medium"] < 500:
        f_val = (3.0 + step * 0.15) * 1e14
        w_val = h * f_val
        w_ev_val = w_val / 1.6e-19
        corr_wf = f"{w_val * 1e19:.2f} × 10⁻¹⁹ J"
        wrs_wf = [
            f"{(w_val * 1e19) * 2:.2f} × 10⁻¹⁹ J",
            f"{(w_val * 1e19) / 2:.2f} × 10⁻¹⁹ J",
            f"{w_ev_val:.2f} × 10⁻¹⁹ J (omitted conversion to Joules)",
            f"{(h / f_val) * 1e48:.2f} × 10⁻¹⁹ J",
            f"{w_val * 1e19 + 2.0:.2f} × 10⁻¹⁹ J",
            f"{(w_val * 1e19) * 1.5:.2f} × 10⁻¹⁹ J",
            f"{f_val * 1e-14:.2f} × 10⁻¹⁹ J"
        ]
        q_wf = f"A certain photosensitive metallic alloy has an experimentally determined threshold frequency of f_0 = {f_val * 1e-14:.2f} × 10¹⁴ Hz. Taking Planck's constant as h = 6.63 × 10⁻³⁴ J·s, calculate the work function (W_0) of this alloy:"
        expl_wf = f"W_0 = h × f_0 = (6.63 × 10⁻³⁴ J·s) × ({f_val * 1e-14:.2f} × 10¹⁴ s⁻¹) = {corr_wf}."
        add_q("medium", "Work Function Calculations", q_wf, corr_wf, wrs_wf, "Applying", "Calculate work function from threshold frequency", expl_wf)

        # Cut-off wavelength to frequency
        if counts["medium"] < 500:
            lam_nm_val = 200 + (step * 8)
            f_from_lam = c / (lam_nm_val * 1e-9)
            corr_flam = f"{f_from_lam * 1e-14:.2f} × 10¹⁴ Hz"
            wrs_flam = [
                f"{(f_from_lam * 1e-14) * 2:.2f} × 10¹⁴ Hz",
                f"{(f_from_lam * 1e-14) / 2:.2f} × 10¹⁴ Hz",
                f"{lam_nm_val:.2f} × 10¹⁴ Hz",
                f"{f_from_lam * 1e-14 + 1.5:.2f} × 10¹⁴ Hz",
                f"{(f_from_lam * 1e-14) * 1.3:.2f} × 10¹⁴ Hz",
                f"{(c * lam_nm_val) * 1e-7:.2f} × 10¹⁴ Hz",
                f"{(f_from_lam * 1e-14) - 2.0:.2f} × 10¹⁴ Hz"
            ]
            q_flam = f"A metal photocathode has a threshold wavelength (cut-off wavelength) of λ_0 = {lam_nm_val} nm. Calculate the threshold frequency (f_0) of this metal (speed of light c = 3.0 × 10⁸ m·s⁻¹):"
            expl_flam = f"f_0 = c / λ_0 = (3.0 × 10⁸ m·s⁻¹) / ({lam_nm_val} × 10⁻⁹ m) = {corr_flam}."
            add_q("medium", "Threshold Calculations", q_flam, corr_flam, wrs_flam, "Applying", "Calculate threshold frequency from cut-off wavelength", expl_flam)

        step += 1

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Maximum Speed Calculations (v_max = sqrt(2*Ek/m_e)), Stopping Potential, Multi-step
    # =========================================================================

    for m_name, w_j, w_ev, _ in metal_data:
        w_joules = w_j * 1e-19
        f_0 = w_joules / h
        for mult in [1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.80, 2.00, 2.20, 2.50]:
            if counts["hard"] >= 200:
                break
            f_inc = f_0 * mult
            e_phot = h * f_inc
            ek_max = e_phot - w_joules
            # Maximum velocity: v_max = sqrt(2 * E_k / m_e)
            v_max = math.sqrt((2.0 * ek_max) / m_e)
            corr_v = f"{v_max * 1e-5:.2f} × 10⁵ m·s⁻¹"
            wrs_v = [
                f"{(v_max * 1e-5) * 2:.2f} × 10⁵ m·s⁻¹",
                f"{(v_max * 1e-5) / 2:.2f} × 10⁵ m·s⁻¹",
                f"{math.sqrt(ek_max / m_e) * 1e-5:.2f} × 10⁵ m·s⁻¹ (omitted factor of 2 under square root)",
                f"{((2.0 * ek_max) / m_e) * 1e-11:.2f} × 10⁵ m·s⁻¹ (forgot to take square root)",
                f"{v_max * 1e-5 + 2.5:.2f} × 10⁵ m·s⁻¹",
                f"{(v_max * 1e-5) * 1.5:.2f} × 10⁵ m·s⁻¹",
                f"{c * 1e-8:.2f} × 10⁵ m·s⁻¹ (speed of light)"
            ]
            q_text_v = f"Ultraviolet radiation of frequency {f_inc * 1e-14:.2f} × 10¹⁴ Hz strikes the surface of a {m_name} plate (work function W_0 = {w_j:.2f} × 10⁻¹⁹ J). Using h = 6.63 × 10⁻³⁴ J·s and mass of an electron m_e = 9.11 × 10⁻³¹ kg, calculate the MAXIMUM SPEED (v_max) of the ejected photoelectrons:"
            expl_v = f"1. E = h × f = (6.63 × 10⁻³⁴) × ({f_inc * 1e-14:.2f} × 10¹⁴) = {e_phot * 1e19:.2f} × 10⁻¹⁹ J. 2. E_k(max) = E - W_0 = {e_phot * 1e19:.2f} × 10⁻¹⁹ - {w_j:.2f} × 10⁻¹⁹ = {ek_max * 1e19:.2f} × 10⁻¹⁹ J. 3. v_max = √(2 × E_k / m_e) = √(2 × {ek_max:.3e} / 9.11 × 10⁻³¹) = {corr_v}."
            add_q("hard", "Maximum Velocity", q_text_v, corr_v, wrs_v, "Evaluating", f"Calculate maximum photoelectron speed for {m_name}", expl_v)

            # Stopping potential calculation: V_s = E_k(max) / e (where e = 1.6e-19 C)
            if counts["hard"] < 200:
                v_stop = ek_max / 1.6e-19
                corr_vstop = f"{v_stop:.2f} V"
                wrs_vstop = [
                    f"{v_stop * 2:.2f} V",
                    f"{v_stop / 2:.2f} V",
                    f"{e_phot / 1.6e-19:.2f} V (omitted work function subtraction)",
                    f"{w_ev:.2f} V (work function in eV)",
                    f"{v_stop + 1.2:.2f} V",
                    f"{v_stop * 1.5:.2f} V",
                    f"0.00 V"
                ]
                q_text_vs = f"In a photoelectric experiment using a {m_name} cathode (work function W_0 = {w_j:.2f} × 10⁻¹⁹ J), incident light has frequency {f_inc * 1e-14:.2f} × 10¹⁴ Hz. What minimum STOPPING POTENTIAL (V_s) must be applied across the photocell to reduce the photocurrent to zero (electron charge e = 1.6 × 10⁻¹⁹ C, h = 6.63 × 10⁻³⁴ J·s)?"
                expl_vs = f"E_k(max) = h × f - W_0 = {ek_max * 1e19:.2f} × 10⁻¹⁹ J. Work done by stopping potential: e × V_s = E_k(max) => V_s = E_k(max) / e = ({ek_max * 1e19:.2f} × 10⁻¹⁹ J) / (1.6 × 10⁻¹⁹ C) = {corr_vstop}."
                add_q("hard", "Stopping Potential", q_text_vs, corr_vstop, wrs_vstop, "Evaluating", f"Calculate stopping potential for {m_name}", expl_vs)

    # Complete hard to exactly 200 with wavelength-to-velocity multi-step calculations
    for m_name, w_j, w_ev, _ in metal_data:
        w_joules = w_j * 1e-19
        lam_0_m = (h * c) / w_joules
        for frac in [0.50, 0.60, 0.70, 0.80]:
            if counts["hard"] >= 200:
                break
            lam_inc_m = lam_0_m * frac
            lam_inc_nm = round(lam_inc_m * 1e9, 1)
            e_inc = (h * c) / (lam_inc_nm * 1e-9)
            ek_calc = e_inc - w_joules
            if ek_calc <= 0:
                continue
            v_calc = math.sqrt((2.0 * ek_calc) / m_e)
            c_hard = f"{v_calc * 1e-5:.2f} × 10⁵ m·s⁻¹"
            w_hard = [
                f"{(v_calc * 1e-5) * 2:.2f} × 10⁵ m·s⁻¹",
                f"{(v_calc * 1e-5) / 2:.2f} × 10⁵ m·s⁻¹",
                f"{math.sqrt(ek_calc / m_e) * 1e-5:.2f} × 10⁵ m·s⁻¹",
                f"{v_calc * 1e-5 + 1.8:.2f} × 10⁵ m·s⁻¹",
                f"{(v_calc * 1e-5) * 1.4:.2f} × 10⁵ m·s⁻¹",
                f"{lam_inc_nm:.1f} × 10⁵ m·s⁻¹",
                f"{c * 1e-8:.2f} × 10⁵ m·s⁻¹"
            ]
            q_hard = f"Monochromatic light of wavelength {lam_inc_nm} nm shines on a {m_name} photocathode (work function W_0 = {w_j:.2f} × 10⁻¹⁹ J). Calculate the maximum speed of the emitted photoelectrons (h = 6.63 × 10⁻³⁴ J·s, c = 3.0 × 10⁸ m·s⁻¹, m_e = 9.11 × 10⁻³¹ kg):"
            exp_hard = f"E = h × c / λ = (6.63 × 10⁻³⁴ × 3.0 × 10⁸) / ({lam_inc_nm} × 10⁻⁹) = {e_inc * 1e19:.2f} × 10⁻¹⁹ J. E_k(max) = E - W_0 = {ek_calc * 1e19:.2f} × 10⁻¹⁹ J. v_max = √(2 × E_k / m_e) = {c_hard}."
            add_q("hard", "Maximum Velocity", q_hard, c_hard, w_hard, "Evaluating", f"Calculate photoelectron speed from wavelength for {m_name}", exp_hard)

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
