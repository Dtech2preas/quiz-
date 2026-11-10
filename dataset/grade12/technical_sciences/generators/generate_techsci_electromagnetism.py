import json
import os

def build_electromagnetism():
    questions = []
    seen_questions = set()
    counts = {"easy": 0, "medium": 0, "hard": 0}

    def add_q(difficulty, subtopic, q_text, correct, wrongs, cognitive, outcome, explanation):
        target = 300 if difficulty == "easy" else 500 if difficulty == "medium" else 200
        if counts[difficulty] >= target:
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
        qid = f"TS_P1_MAG_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Electromagnetism",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Electromagnetism",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Rules, Motor vs Generator, Diodes & Semiconductors
    # =========================================================================

    core_definitions = [
        ("Magnetic Flux (Φ)",
         "The product of the magnetic field strength (B) and the surface area (A) perpendicular to the magnetic field: Φ = B * A * cos(θ), measured in Webers (Wb) or T·m².",
         ["The mechanical force exerted on an electron moving through an electric field",
          "The electrical potential difference produced across a copper wire coil",
          "The total opposition of a transformer core to eddy current formation",
          "The rate of flow of electric charges passing through an iron solenoid",
          "The power dissipated by an alternating current motor per second",
          "The speed of electromagnetic radiation propagating in a vacuum"],
         "Magnetic flux is defined as Φ = B · A · cos θ, measured in Webers (1 Wb = 1 T·m²)."),

        ("Faraday's Law of Electromagnetic Induction",
         "The magnitude of the induced electromotive force (emf) in a conductor or coil is directly proportional to the rate of change of magnetic flux linkage: ε = -N * (ΔΦ / Δt).",
         ["The induced current creates a magnetic field that reinforces the original flux change",
          "The force on a current-carrying conductor is inversely proportional to magnetic field",
          "The potential difference in a transformer is independent of the number of turns",
          "The current in a solenoid is directly proportional to its electrical resistance",
          "The mechanical energy output of an electric motor always equals electrical input",
          "The magnetic flux inside a permanent magnet is always zero at the poles"],
         "Faraday's Law: Induced EMF is directly proportional to the rate of change of magnetic flux: ε = -N(ΔΦ/Δt)."),

        ("Lenz's Law",
         "The direction of the induced current is always such that its magnetic field opposes the change in magnetic flux that produces it (a direct consequence of conservation of energy).",
         ["The induced current always flows in the direction that maximizes the external flux",
          "The magnetic field produced by an induced current is always zero",
          "The induced electromotive force is independent of the speed of magnetic motion",
          "The electric current in a motor flows from the negative terminal to the positive terminal",
          "The primary and secondary coils of a transformer must have equal numbers of turns",
          "The magnetic flux through any closed surface is always infinite"],
         "Lenz's Law ensures conservation of energy: induced currents oppose the magnetic flux change causing them."),

        ("Electric Motor",
         "An electrical machine that converts electrical energy into mechanical kinetic energy by utilizing the motor effect (magnetic force on a current-carrying conductor in a magnetic field).",
         ["A device that converts mechanical rotational kinetic energy into electrical energy",
          "A static electrical component that steps alternating voltages up or down",
          "A semiconductor device that converts alternating current into direct current",
          "An instrument designed solely to measure the magnitude of magnetic flux",
          "A device that stores electrical potential energy in a chemical electrolyte",
          "A mechanical safety switch that melts during an electrical surge"],
         "Electric motors convert electrical energy into mechanical energy via the motor effect."),

        ("Electric Generator (Dynamo / Alternator)",
         "An electrical machine that converts mechanical kinetic energy into electrical energy utilizing the principle of electromagnetic induction.",
         ["A machine that converts electrical energy into mechanical rotational motion",
          "A static device that transfers electrical energy between circuits through mutual induction",
          "A semiconductor diode that emits visible light when forward biased",
          "A device that stores electrostatic charge on metallic plates",
          "A component that eliminates electrical resistance in power transmission lines",
          "An instrument that converts direct current into mechanical sound waves"],
         "Electric generators convert mechanical energy into electrical energy via electromagnetic induction."),

        ("Split-Ring Commutator",
         "A conducting split copper ring in DC motors and DC generators that reverses the electrical connections to the rotating armature coil every half-cycle (180°), ensuring continuous unidirectional rotation or unidirectional output current.",
         ["A pair of continuous unbroken circular rings used in AC alternators to maintain sinusoidal output",
          "A soft iron laminate core used to minimize eddy current losses in power transformers",
          "A spring-loaded safety fuse that disconnects circuits during overloads",
          "A thermal component that dissipates waste heat generated by rotating shafts",
          "An insulating sleeve that prevents magnetic field leakage outside solenoids",
          "A semiconductor junction that converts alternating current into pulsating DC"],
         "A split-ring commutator reverses current direction every half-turn (180°) in DC machines."),

        ("Slip Rings",
         "Continuous, unbroken circular metal rings connected to the ends of the armature coil in an AC generator (alternator) that maintain continuous sliding contact with carbon brushes without reversing circuit connections.",
         ["A split brass ring that reverses coil polarity every half-rotation in DC motors",
          "A laminated silicon steel core that concentrates magnetic flux in transformers",
          "A set of permanent electromagnets providing radial field alignment",
          "A high-speed centrifugal switch that cuts power during overspeed conditions",
          "A pair of carbon brushes that rectify alternating voltage into direct current",
          "A mechanical clutch that engages the generator rotor to the turbine"],
         "Slip rings are continuous circular rings used in AC generators to deliver alternating current output."),

        ("Step-Up Transformer",
         "A transformer with more turns on the secondary coil than on the primary coil (Ns > Np), which increases (steps up) the alternating voltage while decreasing the output current (Vs > Vp, Is < Ip).",
         ["A transformer with fewer secondary turns that decreases voltage and increases current",
          "A transformer designed to convert direct current into alternating current",
          "A transformer that maintains identical voltage and current across both coils",
          "A device that converts chemical energy directly into high-voltage electricity",
          "An electrical component used exclusively in domestic household chargers to deliver 5 V",
          "A high-frequency oscillator used to generate radio frequency waves"],
         "Step-up transformers increase AC voltage (Ns > Np => Vs > Vp) and decrease current for efficient power transmission."),

        ("Step-Down Transformer",
         "A transformer with fewer turns on the secondary coil than on the primary coil (Ns < Np), which decreases (steps down) the alternating voltage while increasing the output current (Vs < Vp, Is > Ip).",
         ["A transformer with more secondary turns that increases transmission voltage to 400 kV",
          "A device that converts alternating current into smooth direct current",
          "A transformer that increases both the output voltage and output current simultaneously",
          "An electrical machine that converts mechanical kinetic energy into chemical energy",
          "A safety switch designed to trip when secondary current exceeds mains limit",
          "A device that operates exclusively on constant, steady direct current (DC)"],
         "Step-down transformers decrease voltage (Ns < Np => Vs < Vp), used in local substations and device adapters."),

        ("Intrinsic vs Extrinsic Semiconductor",
         "An intrinsic semiconductor is a pure crystal (such as silicon or germanium) with equal numbers of free electrons and holes; an extrinsic semiconductor is doped with specific impurity atoms to significantly increase electrical conductivity.",
         ["An intrinsic semiconductor is a metallic conductor, while extrinsic is an insulator",
          "An intrinsic semiconductor operates only on AC, while extrinsic operates only on DC",
          "Intrinsic semiconductors have zero electrical resistance at room temperature",
          "Extrinsic semiconductors contain no impurity atoms or dopants whatsoever",
          "Intrinsic semiconductors conduct electricity better than pure copper",
          "Extrinsic semiconductors cannot form p-n junctions under any conditions"],
         "Intrinsic semiconductors are pure semiconductors; extrinsic semiconductors are doped with impurity atoms to enhance conduction."),

        ("n-type Semiconductor",
         "A semiconductor crystal doped with pentavalent impurity atoms (5 valence electrons, e.g. phosphorus, arsenic), creating an abundance of free conduction electrons as majority charge carriers.",
         ["A crystal doped with trivalent atoms where positive holes are majority carriers",
          "A completely pure silicon crystal containing zero dopant impurities",
          "A metallic alloy that exhibits negative resistance at high temperatures",
          "A semiconductor carrying a net negative electrostatic charge across its body",
          "An insulator that blocks electron flow under all forward bias conditions",
          "A ceramic material used exclusively for high-voltage insulation"],
         "n-type semiconductors are doped with pentavalent donor atoms (majority carriers = free electrons)."),

        ("p-type Semiconductor",
         "A semiconductor crystal doped with trivalent impurity atoms (3 valence electrons, e.g. boron, gallium, indium), creating an abundance of electron vacancies (holes) as majority charge carriers.",
         ["A crystal doped with pentavalent atoms where free electrons are majority carriers",
          "A semiconductor carrying a net positive electrostatic charge across its exterior",
          "A pure germanium crystal that only conducts when exposed to magnetic flux",
          "A superconducting material that operates at liquid nitrogen temperatures",
          "An intrinsic semiconductor with zero holes and infinite free electrons",
          "A composite ceramic used to shield against high-energy ionizing radiation"],
         "p-type semiconductors are doped with trivalent acceptor atoms (majority carriers = positive holes)."),

        ("p-n Junction Diode in Forward Bias",
         "The p-type anode is connected to the positive terminal of the power supply and the n-type cathode to the negative terminal; this reduces the depletion layer width and allows electric current to flow easily once the barrier potential (~0.7 V for Si) is overcome.",
         ["The p-type region is connected to the negative terminal, widening the depletion region",
          "The diode blocks all current flow and exhibits near-infinite electrical resistance",
          "The diode converts direct current into alternating current automatically",
          "The potential barrier across the junction increases to prevent electron movement",
          "The diode operates only as an open switch with zero current conduction",
          "The depletion layer expands across the entire crystal preventing charge transfer"],
         "Forward bias: p to positive, n to negative. Depletion layer narrows, diode conducts current freely."),

        ("p-n Junction Diode in Reverse Bias",
         "The p-type anode is connected to the negative terminal and the n-type cathode to the positive terminal; this widens the depletion layer and increases the potential barrier, blocking macroscopic current flow (only a tiny leakage current flows).",
         ["The p-type region is connected to the positive terminal, allowing heavy current conduction",
          "The depletion layer completely disappears, causing a high-current short circuit",
          "The diode acts as a closed switch with zero internal resistance",
          "The diode emits bright visible light proportional to reverse voltage",
          "The barrier potential drops to zero volts immediately",
          "Electrons and holes recombine continuously across the widened boundary"],
         "Reverse bias: p to negative, n to positive. Depletion layer widens, blocking current flow.")
    ]

    stems = [
        "In Grade 12 Technical Sciences, how is **'{}'** scientifically defined?",
        "According to the CAPS curriculum, **'{}'** is described as:",
        "Which statement provides the accurate technical definition for **'{}'**?",
        "Identify the correct scientific explanation of **'{}'**:",
        "In an examination context, which statement correctly describes **'{}'**?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Conceptual Comparisons and Operating Rules
    concept_questions = [
        ("Right-Hand Rule for a straight current-carrying conductor",
         "Point the thumb of the right hand in the direction of conventional current; the curled fingers indicate the direction of the concentric magnetic field lines around the conductor.",
         ["Point the thumb in the direction of electron flow; fingers point towards magnetic North",
          "Point the fingers in the direction of current; the thumb indicates electrostatic force",
          "The palm points to the electric field while the thumb points to gravitational down",
          "Left-hand fingers curl in the direction of conventional current",
          "The thumb points in the direction of mechanical force on the wire",
          "The right hand is used exclusively for AC generators and never for straight wires"],
         "Right-Hand Rule for straight conductors: Thumb = conventional current direction, curled fingers = magnetic field direction."),

        ("Right-Hand Solenoid Rule",
         "Curl the fingers of the right hand around the solenoid in the direction of conventional current; the outstretched thumb points in the direction of the magnetic North pole of the coil.",
         ["The thumb curls around the solenoid while fingers point to the South pole",
          "The fingers point to the electric field lines while the thumb points to current",
          "Left hand is used where curled fingers point to the South magnetic pole",
          "The thumb points in the direction of electron flow through the copper turns",
          "The palm faces the nearest permanent magnet to determine induced voltage",
          "The thumb points in the direction of the force rotating the coil"],
         "Right-Hand Solenoid Rule: Curled fingers follow conventional current; thumb points to the North pole."),

        ("Why does a transformer require alternating current (AC) and cannot operate on steady direct current (DC)?",
         "Mutual induction requires a continuously changing magnetic flux (ΔΦ/Δt ≠ 0), which is created by alternating current; steady DC produces a constant magnetic flux that induces zero electromotive force in the secondary coil.",
         ["Direct current produces too much magnetic flux that permanently melts the iron core",
          "Alternating current eliminates electrical resistance completely in transformer coils",
          "Direct current causes the primary coil to rotate like an electric motor",
          "Transformers operating on DC would produce infinite secondary output voltages",
          "The laminated core of a transformer only allows electrons to vibrate, not flow",
          "DC electricity has a frequency of 50 Hz, which opposes transformer induction"],
         "Transformers require changing flux (ΔΦ/Δt). Steady DC produces static flux (ΔΦ/Δt = 0), so induced secondary EMF is 0."),

        ("Why are transformer cores constructed from laminated sheets of soft iron separated by insulating varnish?",
         "To minimize energy losses caused by induced eddy currents circulating within the conducting core, reducing heat dissipation.",
         ["To prevent the copper windings from physically touching the iron frame",
          "To allow alternating magnetic flux to escape into the surrounding air",
          "To convert alternating current into smooth direct current inside the core",
          "To increase the electrical resistance of the primary winding to infinity",
          "To ensure the transformer operates at a higher mechanical rotational speed",
          "To step down the frequency of the mains electricity supply from 50 Hz to 25 Hz"],
         "Laminating the core with insulating varnish breaks up circulating eddy currents, drastically reducing resistive heat loss."),

        ("Why is high-voltage transmission used to distribute electricity over long distances across the national grid?",
         "Stepping up the voltage reduces the transmission current (I = P/V); lower current drastically reduces power losses due to heat dissipation in the transmission cables (Ploss = I² * R).",
         ["High voltage speeds up electrons so they reach homes before losing energy",
          "High voltage eliminates the need for aluminum cables by transmitting through air",
          "High voltage converts electrical energy into mechanical kinetic energy in pylons",
          "Stepping up the voltage increases the electrical resistance of the transmission wires",
          "High voltage prevents birds and wildlife from touching electrical cables",
          "Low voltage would cause the electrical frequency to drop below zero hertz"],
         "High transmission voltage reduces current (I = P/V). Since heat loss Ploss = I²R, reducing current minimizes transmission losses."),

        ("What is the function of carbon brushes in an electric motor or generator?",
         "To maintain continuous electrical sliding contact between the stationary external circuit and the rotating armature coil without tangling the connecting wires.",
         ["To reverse the magnetic field of the permanent pole shoes every half turn",
          "To provide mechanical lubrication to the central steel drive shaft",
          "To step down the voltage induced across the rotating copper windings",
          "To act as a thermal heatsink that cools the rotating split rings",
          "To prevent alternating current from producing electromagnetic waves",
          "To prevent the armature coil from rotating at excessively high RPM"],
         "Carbon brushes provide smooth electrical contact with the rotating commutator or slip rings without twisting wires."),

        ("In a DC electric motor, what prevents the armature coil from stalling when its plane is perpendicular to the magnetic field (at 90°)?",
         "The coil's rotational inertia carries it past the neutral vertical position, while the split-ring commutator switches current direction so torque continues in the same sense.",
         ["The magnetic field permanently reverses its physical polarity at the poles",
          "The battery doubles its voltage output when the coil reaches 90°",
          "Gravitational acceleration pulls the coil downward through the magnetic field",
          "A secondary auxiliary battery injects reverse current into the armature",
          "The carbon brushes disconnect permanently and convert the motor into an alternator",
          "Centrifugal force pulls the split rings into parallel alignment with the core"],
         "At the vertical position, torque is zero, but momentum/inertia carries the coil past vertical, where the commutator reverses current to keep torque unidirectional."),

        ("What is the fundamental difference between the output of an AC generator and a DC generator?",
         "An AC generator produces alternating voltage that reverses polarity every half cycle (sine wave); a DC generator produces pulsating unidirectional voltage of constant polarity.",
         ["An AC generator produces constant direct current while a DC generator produces sine waves",
          "An AC generator requires a split-ring commutator while a DC generator uses slip rings",
          "An AC generator cannot be connected to transformers under any circumstances",
          "A DC generator produces twice the electrical energy for the same mechanical input",
          "An AC generator rotates in one direction while a DC generator constantly oscillates back and forth",
          "A DC generator has zero electrical resistance and 100% Carnot efficiency"],
         "AC generators (with slip rings) output sinusoidal alternating voltage. DC generators (with split-ring commutator) output pulsating unidirectional DC."),

        ("Which component is used in a half-wave rectifier circuit to convert AC to DC?",
         "A semiconductor diode that conducts current only during the forward-bias half-cycles and blocks current during reverse-bias half-cycles.",
         ["A step-up transformer that inverts negative voltages into positive voltages",
          "A split-ring commutator attached to a stationary iron transformer core",
          "A ceramic capacitor that permanently eliminates alternating frequency",
          "A variable rheostat that absorbs negative alternating charges",
          "A soft iron solenoid with high self-inductance and low internal resistance",
          "An ammeter connected in series with an earth leakage trip switch"],
         "A diode allows current in only one direction (forward bias), converting AC into pulsating DC (rectification)."),

        ("What happens to an LED (Light Emitting Diode) when it is connected in REVERSE BIAS to a DC power supply?",
         "The wide depletion region prevents current flow, so no light is emitted (it remains off), and if reverse voltage exceeds breakdown it may be damaged.",
         ["It glows twice as bright as in forward bias due to electron accumulation",
          "It emits ultraviolet radiation instead of visible light photons",
          "It converts the battery into an alternating current power supply",
          "It generates mechanical rotation like a miniature electric motor",
          "It steps up the battery voltage to several hundred kilovolts",
          "It produces an immediate loud audible acoustic tone"],
         "In reverse bias, the LED's depletion region widens, blocking current, so the LED does not conduct or emit light.")
    ]

    for q_c, c_c, w_c, exp_c in concept_questions:
        for st_c in [
            "{}",
            "Consider the operational principles of electromagnetism: {}",
            "Which statement correctly answers: {}"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Concepts & Operation", st_c.format(q_c), c_c, w_c, "Understanding", "Understand electromagnetic concepts and machines", exp_c)

    # Semiconductor doping scenarios (fill easy up to 300)
    semiconductors = [
        ("Silicon crystal doped with Phosphorus (5 valence electrons)", "an n-type semiconductor where free electrons are the majority charge carriers"),
        ("Silicon crystal doped with Arsenic (5 valence electrons)", "an n-type semiconductor where donor atoms provide extra conduction band electrons"),
        ("Germanium crystal doped with Antimony (5 valence electrons)", "an n-type semiconductor with abundant mobile negative electron charge carriers"),
        ("Silicon crystal doped with Boron (3 valence electrons)", "a p-type semiconductor where positive electron holes are the majority charge carriers"),
        ("Silicon crystal doped with Gallium (3 valence electrons)", "a p-type semiconductor where acceptor atoms create vacancies (holes) in the valence band"),
        ("Germanium crystal doped with Indium (3 valence electrons)", "a p-type semiconductor with positive holes as majority charge carriers")
    ]

    for dop_mat, dop_desc in semiconductors:
        for q_var in [
            f"What type of extrinsic semiconductor is produced by a **{dop_mat}**?",
            f"In electronics and solid-state physics, a **{dop_mat}** forms:",
            f"Identify the electrical conduction characteristics of a **{dop_mat}**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_dop = f"It forms {dop_desc}."
            w_dop = [
                "It forms an intrinsic insulator that blocks all electrical current at all temperatures.",
                "It forms a superconductor that exhibits zero resistance only above 100 °C.",
                "It converts the crystal into a permanent ferromagnetic bar magnet.",
                "It forms a dielectric material capable of storing massive electrostatic charges only.",
                "It causes all atoms in the crystal to undergo spontaneous nuclear fission.",
                "It forms an electrolyte capable of conducting aqueous chemical ions."
            ]
            add_q("easy", "Semiconductor Doping", q_var, c_dop, w_dop, "Remembering", "Identify semiconductor type from doping impurity", f"Doping silicon/germanium: 5 valence electrons = n-type (electrons); 3 valence electrons = p-type (holes). {c_dop}")

    # Practical & Conceptual Technical Questions (Reaching 300 Easy)
    practical_tech = [
        ("Fleming's Left-Hand Rule (Motor Rule)",
         "Hold the thumb, forefinger, and second finger of the left hand at right angles: Forefinger points in magnetic Field direction (N to S), Second finger points in conventional Current direction (+ to -), and Thumb indicates direction of mechanical Thrust / Force / Motion.",
         ["Thumb points in field direction, forefinger in current direction, second finger in motion",
          "Left hand is used exclusively for AC generators to determine induced EMF",
          "Forefinger indicates gravitational pull while thumb points toward electrical ground",
          "Second finger points toward magnetic North while thumb points to South",
          "The rule only applies to alternating current motors with slip rings",
          "Thumb points to electron flow while second finger points to electrostatic charge"],
         "Fleming's Left-Hand Rule (Motors): Forefinger = Field, seCond finger = Current, Thumb = Thrust (force)."),

        ("Fleming's Right-Hand Rule (Generator Rule)",
         "Hold the thumb, forefinger, and second finger of the right hand mutually perpendicular: Forefinger points in magnetic Field direction (N to S), Thumb points in direction of Motion / Thrust of conductor, and Second finger indicates direction of Induced Current.",
         ["Second finger points in motion direction while thumb indicates induced magnetic field",
          "Right hand is used exclusively to determine rotation direction of DC motors",
          "Forefinger indicates induced voltage while second finger points to mechanical friction",
          "Thumb points to the primary coil while fingers curl around the secondary core",
          "The rule applies only to static transformers without any moving parts",
          "Thumb points to electric current and second finger indicates electrostatic charge"],
         "Fleming's Right-Hand Rule (Generators): Forefinger = Field, Thumb = Motion, seCond finger = Induced Current."),

        ("Approaching North pole of a bar magnet toward the front of a solenoid",
         "The front face of the solenoid develops an induced NORTH magnetic pole to repel and oppose the approaching magnet (Lenz's Law), causing induced current to circulate anti-clockwise when viewed from the front.",
         ["The front face develops an induced South magnetic pole to accelerate the magnet inward",
          "Zero electromotive force is induced because permanent magnets have no frequency",
          "The solenoid converts immediately into a step-up power transformer",
          "The magnet is demagnetized completely as soon as it enters the coil",
          "The induced current flows clockwise to create an attractive magnetic dipole",
          "The front face of the coil develops an electric charge with zero magnetic field"],
         "By Lenz's Law, induced current opposes the approach of a North pole by creating a North pole (repulsion)."),

        ("Withdrawing North pole of a bar magnet away from the front of a solenoid",
         "The front face of the solenoid develops an induced SOUTH magnetic pole to attract and oppose the withdrawal of the magnet (Lenz's Law), causing induced current to circulate clockwise when viewed from the front.",
         ["The front face develops a North pole to push the retreating magnet further away",
          "Zero electromotive force is induced during withdrawal of magnetic poles",
          "The direction of the induced current remains identical to when the magnet was approaching",
          "The coil produces direct current that permanently powers the external meter",
          "The resistance of the solenoid drops to zero during magnetic withdrawal",
          "The soft iron core expels all magnetic flux into the surrounding atmosphere"],
         "By Lenz's Law, withdrawing a North pole is opposed by creating a South pole (attraction)."),

        ("Depletion region in an unbiased p-n junction diode",
         "A narrow boundary region at the junction depleted of mobile free electrons and holes, containing immobile positively charged donor ions on the n-side and immobile negatively charged acceptor ions on the p-side.",
         ["A thick layer composed entirely of pure metallic copper connecting the leads",
          "A region filled with free valence electrons that conduct current continuously",
          "An insulating plastic coating applied to the outside of the silicon diode",
          "A superconducting channel that eliminates electrical resistance across the diode",
          "A layer where electrical potential is exactly zero volts under all conditions",
          "A region consisting solely of neutral carbon atoms preventing electrical breakdown"],
         "The depletion layer contains uncovered fixed donor (+ on n-side) and acceptor (- on p-side) ions depleted of mobile carriers."),

        ("Barrier potential (built-in voltage) of a silicon p-n junction diode",
         "Approximately 0.70 V at room temperature (around 0.30 V for germanium), representing the minimum forward voltage required to overcome the depletion layer internal electric field and initiate conduction.",
         ["Exactly 230 V matching the South African domestic mains supply",
          "Zero volts because semiconductors conduct immediately without threshold",
          "Approximately 12.0 V matching standard lead-acid vehicle batteries",
          "Over 1 000 V to prevent spontaneous atmospheric ionization",
          "A negative potential that generates electrical power internally",
          "Approximately 50 V corresponding to 50 Hz electrical grid frequency"],
         "Silicon diodes require ~0.7 V forward bias to overcome the junction barrier and conduct current."),

        ("Full-wave bridge rectifier using four diodes",
         "Arranges four diodes in a bridge configuration so that both the positive and negative half-cycles of alternating current (AC) are directed through the load in the same single direction, producing full-wave pulsating direct current (DC).",
         ["Uses four diodes to increase the alternating mains frequency from 50 Hz to 200 Hz",
          "Eliminates the need for any transformer by generating power directly from air",
          "Blocks both half-cycles of AC to turn the circuit into an open isolator",
          "Converts direct current (DC) into alternating current (AC) for solar panels",
          "Increases electrical resistance to prevent any current from reaching the load",
          "Converts thermal energy into mechanical shaft rotation via the motor effect"],
         "A 4-diode bridge rectifier converts both AC half-cycles into unidirectional pulsating DC."),

        ("Mains electricity supply characteristics in South Africa",
         "Alternating current (AC) at a nominal frequency of 50 Hz and a standard single-phase potential difference of 230 V (completing 50 full cycles and changing current direction 100 times every second).",
         ["Direct current (DC) at 110 V and zero hertz frequency",
          "Alternating current (AC) at 60 Hz and 120 V identical to North America",
          "Three-phase direct current at 400 V without any alternating cycles",
          "High-frequency radio alternating current at 50 000 Hz and 12 V",
          "Pulsating direct current delivered at 1 000 V to all residential sockets",
          "Square-wave alternating current that reverses polarity once every minute"],
         "In South Africa, domestic mains supply is AC at 230 V, 50 Hz (period T = 1/50 s = 20 ms)."),

        ("Three primary factors that increase the magnitude of induced EMF in a coil",
         "(1) Increasing the rate of relative motion (speed) between magnet and coil, (2) increasing the number of turns (N) in the coil, and (3) using a stronger magnetic field (higher B).",
         ["(1) Decreasing turns, (2) heating the coil to 500 °C, and (3) using wooden cores",
          "(1) Using direct current, (2) wrapping the coil in plastic, and (3) slowing rotation",
          "(1) Increasing wire electrical resistance, (2) grounding the magnet, and (3) shielding",
          "(1) Operating in a vacuum, (2) painting the magnet blue, and (3) reducing coil area",
          "(1) Connecting diodes in reverse bias, (2) using slip rings on motors, and (3) cooling",
          "(1) Reversing battery polarity, (2) keeping flux constant, and (3) increasing length"],
         "Faraday's law shows ε = N(ΔΦ/Δt): higher N, stronger B (greater ΔΦ), and faster motion (smaller Δt) maximize induced EMF."),

        ("Soft iron core function in transformers and electromagnets",
         "Soft iron has high magnetic permeability, which channels and concentrates the magnetic flux lines between coils, and low magnetic retentivity, meaning it magnetizes and demagnetizes rapidly with alternating flux.",
         ["Soft iron acts as an electrical insulator preventing current from flowing through copper",
          "Soft iron converts alternating current directly into high-voltage direct current",
          "Soft iron permanently retains magnetic poles so the transformer never turns off",
          "Soft iron increases electrical resistance to eliminate heat dissipation",
          "Soft iron decreases the frequency of the magnetic flux from 50 Hz to zero",
          "Soft iron radiates electromagnetic waves directly to nearby receiving antennas"],
         "Soft iron has high permeability (concentrates flux) and low retentivity (rapidly magnetizes/demagnetizes with alternating current).")
    ]

    for p_term, p_ans, p_wrongs, p_expl in practical_tech:
        for st_p in [
            "What is the operational principle of **'{}'**?",
            "In Technical Sciences electromagnetism, explain **'{}'**:",
            "Which statement correctly characterizes **'{}'**?",
            "Identify the scientific rule or feature of **'{}'**:"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Technical Principles", st_p.format(p_term), p_ans, p_wrongs, "Understanding", f"Explain {p_term}", p_expl)

    # Frequency and Period of South African AC supply
    for f_hz in [25, 50, 60, 100, 400]:
        t_per = 1.0 / f_hz
        t_ms = t_per * 1000.0
        q_text_freq = f"An alternating current (AC) generator supplies electricity at an operating frequency of f = {f_hz} Hz. Calculate the PERIOD (T) of one complete electrical cycle in milliseconds (ms):"
        c_freq = f"{t_ms:.1f} ms ({t_per:.4f} s)"
        w_freq = [
            f"{f_hz:.1f} ms (confused frequency with period)",
            f"{1000 * f_hz:.1f} ms (multiplied frequency by 1000)",
            f"{t_ms * 2:.1f} ms",
            f"{t_ms / 2:.1f} ms",
            f"{t_ms + 10.0:.1f} ms",
            f"{(1.0 / f_hz) * 100:.1f} ms",
            f"{t_ms * 1.5:.1f} ms"
        ]
        expl_freq = f"Period T = 1 / f = 1 / {f_hz} Hz = {t_per:.4f} s = {t_ms:.1f} ms."
        add_q("easy", "AC Frequency & Period", q_text_freq, c_freq, w_freq, "Applying", "Calculate AC wave period from frequency", expl_freq)

        # Reverse: frequency from period
        if counts["easy"] < 300:
            q_text_per = f"An alternating voltage waveform displayed on an oscilloscope completes one full cycle in T = {t_ms:.1f} ms ({t_per:.4f} s). Determine the FREQUENCY (f) of the AC source:"
            c_per = f"{f_hz} Hz"
            w_per = [
                f"{t_ms:.1f} Hz (confused milliseconds of period with frequency)",
                f"{f_hz * 10} Hz",
                f"{f_hz // 2} Hz",
                f"{f_hz * 2} Hz",
                f"{f_hz + 25} Hz",
                f"{int(t_per * 1000)} Hz",
                f"{f_hz * 4} Hz"
            ]
            expl_per = f"Frequency f = 1 / T = 1 / {t_per:.4f} s = {c_per}."
            add_q("easy", "AC Frequency & Period", q_text_per, c_per, w_per, "Applying", "Calculate AC frequency from wave period", expl_per)

    # Additional qualitative generator and transformer questions to fill easy
    ac_dc_comparisons = [
        ("rotating coil in an AC alternator with slip rings", "continuous sinusoidal alternating electromotive force (AC voltage) that smoothly reverses polarity every half turn"),
        ("rotating coil in a DC generator with a split-ring commutator", "pulsating direct current (DC) that fluctuates in magnitude but maintains a single unchanging polarity"),
        ("armature coil of a DC motor supplied with constant direct current", "continuous unidirectional rotation of the drive shaft due to commutator reversing coil current every 180°"),
        ("primary coil of a transformer connected to a 12 V automotive battery (DC)", "zero steady secondary voltage (0 V) because direct current creates a static magnetic flux with ΔΦ/Δt = 0"),
        ("primary coil of a transformer connected to a 12 V AC power pack", "an alternating secondary voltage induced continuously through mutual electromagnetic induction (ΔΦ/Δt ≠ 0)")
    ]

    for sys_desc, sys_outcome in ac_dc_comparisons:
        if counts["easy"] >= 300:
            break
        q_comp = f"What is the electrical or mechanical output produced by a **{sys_desc}**?"
        c_comp = f"It produces {sys_outcome}."
        w_comp = [
            "It produces infinite electrical power with zero mechanical or thermal loss.",
            "It produces electrostatic charge without any moving electrons or flux.",
            "It destroys the magnetic field of the permanent pole shoes permanently.",
            "It converts electrical potential into nuclear binding energy inside copper.",
            "It operates in reverse by absorbing mechanical kinetic energy from air.",
            "It causes the electrical resistance of the circuit to become negative."
        ]
        add_q("easy", "Machine Output Behavior", q_comp, c_comp, w_comp, "Understanding", "Understand machine output behavior", f"{sys_desc} => {sys_outcome}.")

    generator_components = [
        ("Armature coil", "A loop or multi-turn coil of insulated copper wire wound around a soft iron core that rotates within the magnetic field to produce induced EMF."),
        ("Permanent magnets / Field electromagnets", "Provide a uniform radial magnetic field across the air gap in which the armature coil rotates."),
        ("Carbon brushes", "Conduct current from the rotating slip rings or commutator to the stationary external circuit while minimizing frictional wear."),
        ("Slip rings (in AC alternator)", "Maintain continuous circular electrical contact with brushes so that the polarity of output current alternates naturally."),
        ("Split-ring commutator (in DC generator)", "Mechanically rectifies the alternating induced EMF into pulsating direct current by swapping terminal contacts every 180°.")
    ]

    for comp_name, comp_role in generator_components:
        for st_g in [
            f"What is the specific function of the **'{comp_name}'** in an electric generator or alternator?",
            f"In the construction of electrical machines, the **'{comp_name}'** serves to:",
            f"Which statement correctly identifies the role of the **'{comp_name}'** in Grade 12 Technical Sciences?"
        ]:
            if counts["easy"] >= 300:
                break
            w_comp_g = [
                "To eliminate magnetic flux linkage between the armature and field poles.",
                "To increase the speed of rotation beyond the design limit of the turbine.",
                "To step up the generated electrical power so output exceeds mechanical input.",
                "To convert kinetic energy directly into thermal radiation without voltage.",
                "To convert the generator into an electrolytic electroplating cell.",
                "To prevent electrons from experiencing any magnetic Lorentz force."
            ]
            add_q("easy", "Machine Components", st_g, comp_role, w_comp_g, "Remembering", f"Identify function of {comp_name}", comp_role)

    # Fill remaining easy with transformer core concepts
    for trans_type, desc_t in [
        ("Step-up transformer at an Eskom power station", "increases voltage from 22 kV to 400 kV to minimize I²R transmission power losses over national grid lines"),
        ("Step-down transformer at a municipal substation", "decreases high grid voltage (132 kV or 11 kV) down to safe domestic distribution levels (230 V)"),
        ("Step-down transformer in a cell phone USB charger", "decreases 230 V AC mains voltage down to approximately 5 V AC before diode rectification to DC"),
        ("Step-down transformer in an industrial arc welder", "decreases mains voltage to produce very high current (hundreds of amperes) required to melt metals")
    ]:
        for st_tr in [
            f"What is the practical engineering purpose of a **{trans_type}**?",
            f"In practical electrical power distribution, why is a **{trans_type}** utilized?",
            f"Which statement explains why engineers deploy a **{trans_type}**?"
        ]:
            if counts["easy"] >= 300:
                break
            c_tr = f"It {desc_t}."
            w_tr = [
                "It generates unlimited electrical power from the Earth's geomagnetic field.",
                "It converts alternating current into radio waves for wireless energy transmission.",
                "It eliminates all electrical resistance across municipal distribution networks.",
                "It stores electrical energy chemically in battery electrolytes for later use.",
                "It causes the frequency of alternating current to increase from 50 Hz to 50 000 Hz.",
                "It produces mechanical rotational kinetic energy to drive water turbines."
            ]
            add_q("easy", "Transformers in Power Grid", st_tr, c_tr, w_tr, "Understanding", f"Explain purpose of {trans_type}", c_tr)

    # Turns ratio and transformer identification (filling easy to 300)
    turns_pairs = [
        (100, 1000, "STEP-UP", "increases (steps up) the voltage by a factor of 10"),
        (200, 800, "STEP-UP", "increases the voltage by a factor of 4"),
        (500, 2500, "STEP-UP", "increases the voltage by a factor of 5"),
        (1000, 10000, "STEP-UP", "increases the voltage by a factor of 10"),
        (50, 500, "STEP-UP", "steps up voltage 10 times"),
        (120, 2400, "STEP-UP", "steps up voltage 20 times"),
        (1000, 100, "STEP-DOWN", "decreases (steps down) the voltage to one-tenth (1/10) of primary voltage"),
        (800, 200, "STEP-DOWN", "decreases the voltage to one-quarter (1/4) of primary voltage"),
        (2500, 500, "STEP-DOWN", "decreases the voltage to one-fifth (1/5) of primary voltage"),
        (4000, 200, "STEP-DOWN", "decreases the voltage to one-twentieth (1/20) of primary voltage"),
        (600, 30, "STEP-DOWN", "decreases the voltage to one-twentieth of primary voltage"),
        (1200, 120, "STEP-DOWN", "decreases the voltage by a factor of 10")
    ]

    for np_tr, ns_tr, t_kind, t_effect in turns_pairs:
        if counts["easy"] >= 300:
            break
        q_text_tr = f"A transformer has N_p = {np_tr} turns on its primary coil and N_s = {ns_tr} turns on its secondary coil. How is this transformer classified, and what is its operational effect on AC voltage?"
        c_tr_ans = f"It is a {t_kind} transformer because N_s {'>' if t_kind == 'STEP-UP' else '<'} N_p, and it {t_effect}."
        w_tr_ans = [
            f"It is a {'STEP-DOWN' if t_kind == 'STEP-UP' else 'STEP-UP'} transformer that converts alternating current into direct current.",
            f"It is an isolation transformer that keeps output voltage completely identical regardless of turns.",
            f"It is a DC machine that rotates the secondary winding to generate kinetic energy.",
            f"It is an intrinsic semiconductor diode that conducts in forward bias only.",
            f"It is a step-down transformer that increases both output voltage and current simultaneously.",
            f"It is an electric motor that converts magnetic flux into electrical voltage."
        ]
        add_q("easy", "Transformer Classification", q_text_tr, c_tr_ans, w_tr_ans, "Understanding", "Classify transformer based on turns ratio", c_tr_ans)

    # Lenz's Law motion scenarios
    lenz_scenarios = [
        ("The South pole of a permanent bar magnet is pushed rapidly into a stationary solenoid.",
         "The near end of the solenoid develops an induced SOUTH pole to repel the approaching magnet, causing an induced current that opposes the motion.",
         ["The near end develops a North pole to attract the magnet and pull it in faster.",
          "No current is induced because only North poles can cause electromagnetic induction.",
          "The solenoid converts the mechanical motion directly into heat without any current.",
          "The magnetic field of the permanent magnet is permanently cancelled out.",
          "The galvanometer needle remains stationary at exactly zero.",
          "The solenoid rotates continuously like a direct current electric motor."]),

        ("The South pole of a permanent bar magnet is withdrawn rapidly away from a stationary solenoid.",
         "The near end of the solenoid develops an induced NORTH pole to attract the receding magnet, producing an induced current that opposes its withdrawal.",
         ["The near end develops a South pole to accelerate the magnet away.",
          "The induced current flows in the same direction as when the magnet was pushed in.",
          "The magnetic flux inside the coil increases to infinity.",
          "No electromotive force is produced during withdrawal of South poles.",
          "The galvanometer indicates zero because magnetic motion must be inward.",
          "The solenoid loses all electrical conductivity permanently."]),

        ("A permanent bar magnet is held completely stationary inside a solenoid.",
         "Zero electromotive force (emf) and zero current are induced because there is no change in magnetic flux linkage over time (ΔΦ/Δt = 0).",
         ["A maximum steady direct current flows because the magnet is fully inside the coil.",
          "The coil rapidly heats up and melts due to massive induced eddy currents.",
          "An alternating current of 50 Hz is generated continuously.",
          "The coil develops alternating North and South poles at high frequency.",
          "The magnetic flux drops to zero because the magnet stopped moving.",
          "The galvanometer deflects to maximum positive reading permanently."]),

        ("A copper ring is dropped vertically through the vertical magnetic field of a stationary bar magnet.",
         "As it approaches the magnet, induced current circulates to create a repelling magnetic field; as it leaves, induced current reverses to create an attracting field, slowing its fall (eddy current damping).",
         ["The copper ring accelerates downward faster than 9.8 m·s⁻² due to magnetic attraction.",
          "The copper ring experiences zero magnetic force because copper is non-magnetic.",
          "The copper ring stops completely in mid-air and floats indefinitely.",
          "The copper ring converts into a permanent magnet with fixed poles.",
          "The copper ring explodes due to high electrostatic charge accumulation.",
          "Zero current is induced because the copper ring is not connected to a battery."])
    ]

    for lenz_act, lenz_res, lenz_wrongs in lenz_scenarios:
        for st_l in [
            "According to Faraday's and Lenz's Laws, what occurs in the following scenario? **{}**",
            "Predict the physical outcome based on electromagnetic principles: **{}**",
            "Which statement correctly describes the result when **{}**"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Lenz's Law Scenarios", st_l.format(lenz_act), lenz_res, lenz_wrongs, "Understanding", "Apply Lenz's law to predict induced magnetic polarity", lenz_res)

    # Simple Whole-Number Flux & Faraday Calculations (Level 1 / Easy)
    simple_faraday = [
        (10, 0.5, 1.0), (20, 0.4, 1.0), (50, 0.2, 1.0), (100, 0.1, 1.0),
        (10, 1.0, 2.0), (20, 1.0, 2.0), (40, 0.5, 2.0), (50, 1.0, 2.0),
        (100, 0.5, 2.0), (200, 0.2, 2.0), (20, 2.0, 4.0), (50, 2.0, 4.0),
        (100, 1.0, 4.0), (200, 1.0, 4.0), (50, 5.0, 5.0), (100, 2.5, 5.0),
        (15, 0.6, 1.0), (25, 0.8, 1.0), (30, 0.5, 1.0), (60, 0.3, 1.0),
        (80, 0.25, 1.0), (150, 0.1, 1.0), (250, 0.08, 1.0), (300, 0.05, 1.0)
    ]

    for n_smp, dphi_smp, dt_smp in simple_faraday:
        if counts["easy"] >= 300:
            break
        emf_smp = (n_smp * dphi_smp) / dt_smp
        c_emf_smp = f"{emf_smp:.1f} V"
        w_emf_smp = [
            f"{n_smp * dphi_smp * dt_smp:.1f} V (multiplied turns by flux and time)",
            f"{dphi_smp / dt_smp:.2f} V (neglected number of turns N)",
            f"{emf_smp * 2:.1f} V",
            f"{emf_smp / 2:.1f} V",
            f"{emf_smp + 10.0:.1f} V",
            f"{n_smp * dt_smp:.1f} V",
            f"{emf_smp * 10:.1f} V"
        ]
        q_smp_far = f"A small demonstration coil has N = {n_smp} turns. A student moves a bar magnet causing a flux change of ΔΦ = {dphi_smp:.2f} Wb across the coil in Δt = {dt_smp:.1f} s. Calculate the magnitude of the induced EMF:"
        expl_smp_far = f"Faraday's Law: ε = N × (ΔΦ / Δt) = {n_smp} × ({dphi_smp:.2f} Wb / {dt_smp:.1f} s) = {c_emf_smp}."
        add_q("easy", "Faraday Induction Basics", q_smp_far, c_emf_smp, w_emf_smp, "Applying", "Calculate induced EMF using Faraday's Law", expl_smp_far)

        # Basic flux calculation: Φ = B * A
        if counts["easy"] < 300:
            b_smp = dt_smp # repurpose as B
            a_smp = dphi_smp # repurpose as A
            flx_smp = b_smp * a_smp
            c_flx_smp = f"{flx_smp:.2f} Wb"
            w_flx_smp = [
                f"{b_smp / a_smp:.2f} Wb",
                f"{a_smp / b_smp:.2f} Wb",
                f"{flx_smp * 10:.2f} Wb",
                f"{flx_smp / 2:.2f} Wb",
                f"{flx_smp * 2:.2f} Wb",
                f"{b_smp + a_smp:.2f} Wb",
                f"{flx_smp + 5.0:.2f} Wb"
            ]
            q_smp_flx = f"A loop of wire with area A = {a_smp:.2f} m² is placed perpendicular to a magnetic field of B = {b_smp:.1f} T. Calculate the magnetic flux (Φ) passing through the loop:"
            expl_smp_flx = f"Φ = B × A = {b_smp:.1f} T × {a_smp:.2f} m² = {c_flx_smp}."
            add_q("easy", "Magnetic Flux Basics", q_smp_flx, c_flx_smp, w_flx_smp, "Applying", "Calculate magnetic flux directly", expl_smp_flx)

    # Diode operation basics
    for diode_state, diode_ans, diode_wrongs, diode_expl in [
        ("FORWARD BIASED diode in an LED torch",
         "The p-type anode is connected to positive and n-type cathode to negative; the depletion layer narrows and current flows easily, illuminating the LED.",
         ["The diode has infinite resistance and blocks all current completely.",
          "The diode converts direct current into alternating current.",
          "The diode explodes because diodes cannot conduct electric current.",
          "The battery charges itself from the photons emitted by the LED.",
          "The depletion layer expands across the entire crystal body.",
          "The current alternates back and forth 50 times per second."],
         "In forward bias, external voltage overcomes the potential barrier, narrowing the depletion layer and allowing current flow."),

        ("REVERSE BIASED diode in a solar panel protection circuit",
         "The p-type anode is connected to negative and n-type cathode to positive; the depletion layer widens and blocks reverse discharge current.",
         ["The diode conducts maximum current with zero resistance.",
          "The diode steps up the battery voltage to several thousand volts.",
          "The diode emits bright laser light continuously.",
          "The depletion layer disappears completely allowing full current.",
          "The diode acts as a closed switch with 0 Ω impedance.",
          "The diode reverses the magnetic poles of the solar panels."],
         "In reverse bias, external voltage reinforces the internal barrier, widening the depletion region and blocking reverse current."),

        ("Effect of increasing the rotation speed of an AC generator armature coil",
         "Both the maximum induced electromotive force (peak voltage) and the frequency of the alternating current INCREASE proportionally.",
         ["The voltage increases but the frequency drops to zero hertz.",
          "The voltage drops to zero because electrons cannot move fast enough.",
          "The generator converts automatically into a DC battery.",
          "The frequency increases but the induced voltage remains zero.",
          "The slip rings reverse current direction like a commutator.",
          "The armature magnetic field is permanently eliminated."],
         "Faster rotation increases the rate of flux change (higher peak ε) and completes more cycles per second (higher frequency f).")
    ]:
        for st_dio in [
            "In electrical circuits, what occurs when a **{}**?",
            "Identify the correct operating characteristic of a **{}**:",
            "Which statement accurately explains what happens when a **{}**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Diode & Generator Operation", st_dio.format(diode_state), diode_ans, diode_wrongs, "Understanding", "Understand diode and generator operation", diode_expl)

    # Additional machine applications to reach 300
    apps_em = [
        ("electric guitar pickup", "electromagnetic induction: vibrating steel strings alter magnetic flux through a pickup coil, inducing an electrical audio signal"),
        ("bicycle dynamo", "electromagnetic induction: a rotating permanent magnet induces alternating current in a stationary coil to power headlamps"),
        ("induction cooktop", "high-frequency electromagnetic induction: alternating magnetic field induces eddy currents in ferromagnetic pots, generating resistive heat directly"),
        ("metal detector", "electromagnetic induction: transmitting coil induces eddy currents in hidden metal objects, creating secondary magnetic fields detected by receiver coil"),
        ("galvanometer", "motor effect: current passing through a suspended coil in a radial magnetic field experiences torque, deflecting a calibrated pointer"),
        ("moving-coil loudspeaker", "motor effect: alternating audio current through a voice coil in a permanent magnetic field produces varying magnetic forces that vibrate the speaker cone"),
        ("moving-coil microphone", "electromagnetic induction: sound waves vibrate a diaphragm and attached coil within a magnetic field, inducing a varying audio voltage signal"),
        ("magnetic levitation (maglev) train", "electromagnetic repulsion: superconducting electromagnets interact with guideway tracks to levitate and propel the train with zero physical friction"),
        ("card reader / magnetic stripe scanner", "electromagnetic induction: moving magnetic stripe past a read-head induces tiny voltage pulses decoded into binary digital data")
    ]

    for app_name, app_princ in apps_em:
        for st_app in [
            f"What physical principle and operational mechanism governs the operation of an **{app_name}**?",
            f"How does an **{app_name}** function in practical Technical Sciences applications?",
            f"Which statement correctly describes the physics of an **{app_name}**?"
        ]:
            if counts["easy"] >= 300:
                break
            c_app_ans = f"It utilizes {app_princ}."
            w_app_ans = [
                "It utilizes electrostatic attraction between stationary point charges only.",
                "It generates unlimited energy through spontaneous nuclear transmutation.",
                "It eliminates electrical resistance by cooling coils to absolute zero.",
                "It converts mechanical sound waves directly into chemical potential energy.",
                "It operates exclusively on direct current without any changing magnetic flux.",
                "It relies on gravitational deflection of cathode ray electron beams."
            ]
            add_q("easy", "Electromagnetic Applications", st_app, c_app_ans, w_app_ans, "Understanding", f"Explain physics of {app_name}", f"{app_name}: {app_princ}.")

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Calculations: Faraday's Law, Transformer Equations (Vs/Vp = Ns/Np = Ip/Is), Magnetic Flux
    # =========================================================================

    # 1. Faraday's Law: ε = -N * (ΔΦ / Δt) => magnitude ε = N * ΔΦ / Δt
    # Loops: N turns, ΔΦ (Wb), Δt (s)
    num_turns_list = [50, 100, 150, 200, 250, 300, 400, 500, 800, 1000]
    flux_changes = [0.002, 0.005, 0.010, 0.015, 0.020, 0.025, 0.040, 0.050, 0.080, 0.100] # Wb
    time_intervals = [0.02, 0.04, 0.05, 0.10, 0.20, 0.25, 0.50] # seconds

    for n_turns in num_turns_list:
        for d_flux in flux_changes:
            for d_time in time_intervals:
                if counts["medium"] >= 500:
                    break
                emf_calc = (n_turns * d_flux) / d_time
                corr_emf = f"{emf_calc:.2f} V"
                wrs_emf = [
                    f"{n_turns * d_flux * d_time:.4f} V (multiplied turns, flux and time together)",
                    f"{(d_flux / d_time):.2f} V (neglected the number of turns N in coil)",
                    f"{(n_turns * d_time) / d_flux:.2f} V (inverted flux and time)",
                    f"{emf_calc * 2:.2f} V",
                    f"{emf_calc / 2:.2f} V",
                    f"{emf_calc + 15.0:.2f} V",
                    f"{emf_calc * 10:.2f} V"
                ]
                q_text_far = f"A coil consisting of N = {n_turns} turns experiences a change in magnetic flux of ΔΦ = {d_flux:.3f} Wb over a time interval of Δt = {d_time:.2f} s. Calculate the magnitude of the induced electromotive force (emf, ε) in the coil:"
                expl_far = f"Faraday's Law: ε = N × (ΔΦ / Δt) = {n_turns} × ({d_flux:.3f} Wb / {d_time:.2f} s) = {n_turns} × {d_flux / d_time:.3f} = {corr_emf}."
                add_q("medium", "Faraday's Law Calculations", q_text_far, corr_emf, wrs_emf, "Applying", "Calculate induced EMF using Faraday's Law", expl_far)

                # Solving for number of turns N = (ε * Δt) / ΔΦ
                if counts["medium"] < 500:
                    corr_n = f"{n_turns} turns"
                    wrs_n = [
                        f"{int(emf_calc * d_flux * d_time)} turns",
                        f"{int(n_turns * 2)} turns",
                        f"{int(n_turns / 2)} turns",
                        f"{int(emf_calc / (d_flux * d_time))} turns",
                        f"{n_turns + 50} turns",
                        f"{int(n_turns * 1.5)} turns",
                        f"{int(d_flux / (emf_calc * d_time))} turns"
                    ]
                    q_text_n = f"An induced electromotive force of ε = {emf_calc:.2f} V is produced in a coil when the magnetic flux changes by {d_flux:.3f} Wb in {d_time:.2f} s. Determine the number of turns (N) in the coil:"
                    expl_n = f"From Faraday's Law: N = (ε × Δt) / ΔΦ = ({emf_calc:.2f} V × {d_time:.2f} s) / {d_flux:.3f} Wb = {corr_n}."
                    add_q("medium", "Faraday's Law Calculations", q_text_n, corr_n, wrs_n, "Applying", "Calculate number of turns from induced EMF", expl_n)

    # 2. Transformer Voltage and Turns: Vs / Vp = Ns / Np => Vs = Vp * (Ns / Np)
    primary_voltages = [110.0, 220.0, 230.0, 240.0, 400.0, 11000.0] # V
    primary_turns = [100, 200, 500, 1000, 2000, 4000]
    secondary_turns = [20, 50, 100, 250, 500, 1000, 2000, 8000, 20000]

    for vp_val in primary_voltages:
        for np_val in primary_turns:
            for ns_val in secondary_turns:
                if np_val == ns_val:
                    continue
                if counts["medium"] >= 500:
                    break
                vs_val = vp_val * (ns_val / np_val)
                corr_vs = f"{vs_val:.1f} V"
                wrs_vs = [
                    f"{vp_val * (np_val / ns_val):.1f} V (inverted turns ratio: Np / Ns)",
                    f"{vp_val * np_val * ns_val * 1e-4:.1f} V",
                    f"{vs_val * 2:.1f} V",
                    f"{vs_val / 2:.1f} V",
                    f"{vp_val:.1f} V (assumed secondary voltage equals primary voltage)",
                    f"{vs_val + 50.0:.1f} V",
                    f"{vs_val * 1.5:.1f} V"
                ]
                trans_type = "STEP-UP" if ns_val > np_val else "STEP-DOWN"
                q_text_t = f"A {trans_type} transformer has N_p = {np_val} turns on its primary coil and N_s = {ns_val} turns on its secondary coil. If an alternating primary voltage of V_p = {vp_val:.0f} V is applied, calculate the secondary output voltage (V_s):"
                expl_t = f"Transformer formula: V_s / V_p = N_s / N_p => V_s = V_p × (N_s / N_p) = {vp_val:.0f} V × ({ns_val} / {np_val}) = {corr_vs}."
                add_q("medium", "Transformer Calculations", q_text_t, corr_vs, wrs_vs, "Applying", "Calculate secondary voltage using transformer turns ratio", expl_t)

                # Transformer Current Calculation: Is = Ip * (Np / Ns) or Ip = Is * (Ns / Np)
                if counts["medium"] < 500:
                    ip_val = 5.0 # Amperes
                    is_val = ip_val * (np_val / ns_val)
                    corr_is = f"{is_val:.2f} A"
                    wrs_is = [
                        f"{ip_val * (ns_val / np_val):.2f} A (multiplied by Ns / Np instead of Np / Ns)",
                        f"{ip_val:.2f} A (assumed secondary current equals primary current)",
                        f"{is_val * 2:.2f} A",
                        f"{is_val / 2:.2f} A",
                        f"{(vs_val * ip_val) / 100:.2f} A",
                        f"{is_val + 4.0:.2f} A",
                        f"{is_val * 1.5:.2f} A"
                    ]
                    q_text_is = f"For the same ideal transformer (N_p = {np_val}, N_s = {ns_val}), the primary coil draws a current of I_p = {ip_val:.1f} A. Assuming 100% efficiency, calculate the secondary output current (I_s):"
                    expl_is = f"Ideal transformer power: P_p = P_s => V_p × I_p = V_s × I_s => I_s / I_p = N_p / N_s => I_s = I_p × (N_p / N_s) = {ip_val:.1f} A × ({np_val} / {ns_val}) = {corr_is}."
                    add_q("medium", "Transformer Calculations", q_text_is, corr_is, wrs_is, "Applying", "Calculate secondary current for ideal transformer", expl_is)

    # 3. Magnetic Flux: Φ = B * A
    b_fields = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.80, 1.0, 1.2, 1.5] # Tesla (T)
    areas_m2 = [0.005, 0.010, 0.020, 0.040, 0.050, 0.080, 0.10, 0.15, 0.20] # m²

    for b_val in b_fields:
        for a_val in areas_m2:
            if counts["medium"] >= 500:
                break
            flux_val = b_val * a_val
            corr_fl = f"{flux_val:.4f} Wb"
            wrs_fl = [
                f"{b_val / a_val:.4f} Wb (divided B by area)",
                f"{a_val / b_val:.4f} Wb (divided area by B)",
                f"{flux_val * 10:.4f} Wb",
                f"{flux_val / 2:.4f} Wb",
                f"{flux_val * 2:.4f} Wb",
                f"{b_val + a_val:.4f} Wb",
                f"{flux_val * 100:.4f} Wb"
            ]
            q_text_fl = f"A rectangular coil with cross-sectional area A = {a_val:.3f} m² is placed perpendicular to a uniform magnetic field of B = {b_val:.2f} T. Calculate the magnetic flux (Φ) passing through the coil:"
            expl_fl = f"Magnetic flux formula: Φ = B × A × cos(0°) = {b_val:.2f} T × {a_val:.3f} m² = {corr_fl}."
            add_q("medium", "Magnetic Flux Calculations", q_text_fl, corr_fl, wrs_fl, "Applying", "Calculate magnetic flux from B and area", expl_fl)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Multi-Step Power Transmission Loss, Induced Current (I = ε/R), Complex Diode Circuits
    # =========================================================================

    # 1. Grid Power Transmission Loss Analysis:
    # Power generated P (Watts), Line resistance R_line (Ohms)
    # At low voltage V_low: I_low = P / V_low, P_loss_low = (I_low)^2 * R_line
    # At stepped-up voltage V_high: I_high = P / V_high, P_loss_high = (I_high)^2 * R_line
    powers_gen = [25000.0, 50000.0, 75000.0, 100000.0, 150000.0, 200000.0, 250000.0, 300000.0, 400000.0, 500000.0, 600000.0, 750000.0, 800000.0, 1000000.0, 1200000.0, 1500000.0, 2000000.0]
    v_transmission = [2500.0, 5000.0, 10000.0, 11000.0, 20000.0, 22000.0, 33000.0, 44000.0, 50000.0, 66000.0, 88000.0, 100000.0, 132000.0, 220000.0, 275000.0, 400000.0]
    line_resistances = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.5, 8.0, 10.0, 12.0, 15.0]

    for p_gen in powers_gen:
        for v_trans in v_transmission:
            for r_line in line_resistances:
                if counts["hard"] >= 200:
                    break
                i_trans = p_gen / v_trans
                p_loss = (i_trans ** 2) * r_line
                pct_loss = (p_loss / p_gen) * 100.0
                corr_ploss = f"{p_loss:.1f} W"
                wrs_ploss = [
                    f"{i_trans * r_line:.1f} W (calculated voltage drop instead of power loss: I × R)",
                    f"{(p_gen ** 2) / (v_trans * r_line):.1f} W",
                    f"{p_loss * 10:.1f} W",
                    f"{p_loss / 2:.1f} W",
                    f"{p_loss * 2:.1f} W",
                    f"{p_gen - p_loss:.1f} W (calculated delivered power instead of lost power)",
                    f"{p_loss + 250.0:.1f} W"
                ]
                q_text_ploss = (f"A power station generates {p_gen / 1000:.1f} kW of electrical power. Before transmission through cables "
                                f"with a total resistance of R_line = {r_line:.2f} Ω, the voltage is stepped up to {v_trans / 1000:.1f} kV ({v_trans:.0f} V). "
                                f"Calculate the rate of electrical energy loss (thermal power loss, P_loss) in the transmission cables:")
                expl_ploss = (f"1. Transmission current: I = P / V = {p_gen:.0f} W / {v_trans:.0f} V = {i_trans:.2f} A. "
                              f"2. Cable power loss: P_loss = I² × R_line = ({i_trans:.2f} A)² × {r_line:.2f} Ω = {corr_ploss} "
                              f"(representing {pct_loss:.2f}% of generated power).")
                add_q("hard", "Power Transmission Losses", q_text_ploss, corr_ploss, wrs_ploss, "Evaluating", "Calculate transmission power loss at stepped-up voltage", expl_ploss)

                # Induced Current in a Closed Loop with Resistance: ε = N(ΔΦ/Δt), I = ε / R
                if counts["hard"] < 200:
                    n_h = int(50 + (p_gen / 10000))
                    dphi_h = 0.01 + (r_line * 0.005)
                    dt_h = 0.05 + (v_trans / 1000000.0)
                    emf_h = (n_h * dphi_h) / dt_h
                    i_ind = emf_h / r_line
                    corr_iind = f"{i_ind:.2f} A"
                    wrs_iind = [
                        f"{emf_h * r_line:.2f} A (multiplied EMF by resistance: ε × R)",
                        f"{r_line / emf_h:.4f} A (inverted Ohm's law: R / ε)",
                        f"{i_ind * 2:.2f} A",
                        f"{i_ind / 2:.2f} A",
                        f"{emf_h:.2f} A (assumed induced current equals induced EMF)",
                        f"{i_ind + 5.0:.2f} A",
                        f"{i_ind * 1.5:.2f} A"
                    ]
                    q_text_iind = (f"A coil of N = {n_h} turns and total electrical resistance R = {r_line:.2f} Ω is connected in a closed circuit. "
                                   f"The magnetic flux linking the coil collapses by {dphi_h:.3f} Wb in Δt = {dt_h:.3f} s. "
                                   f"Calculate the magnitude of the INDUCED CURRENT (I_induced) flowing through the circuit:")
                    expl_iind = (f"1. Induced EMF from Faraday's Law: ε = N × (ΔΦ / Δt) = {n_h} × ({dphi_h:.3f} Wb / {dt_h:.3f} s) = {emf_h:.2f} V. "
                                 f"2. Induced current from Ohm's Law: I = ε / R = {emf_h:.2f} V / {r_line:.2f} Ω = {corr_iind}.")
                    add_q("hard", "Electromagnetic Induction & Ohm's Law", q_text_iind, corr_iind, wrs_iind, "Evaluating", "Calculate induced current combining Faraday's and Ohm's laws", expl_iind)

    # 2. Multi-stage transformer and rectifier diode calculations
    for v_ac in [12.0, 15.0, 18.0, 24.0]:
        for r_load in [10.0, 20.0, 50.0, 100.0]:
            if counts["hard"] >= 200:
                break
            # Silicon diode has forward barrier potential drop of 0.7 V
            v_peak = v_ac * 1.4142 # V_peak = V_rms * sqrt(2)
            v_load_peak = v_peak - 0.7 # Peak voltage across load after silicon diode drop
            i_peak = v_load_peak / r_load
            corr_vlp = f"{v_load_peak:.2f} V"
            wrs_vlp = [
                f"{v_peak:.2f} V (neglected the 0.7 V silicon diode potential barrier drop)",
                f"{v_ac:.2f} V (confused RMS voltage with peak rectified voltage)",
                f"{v_load_peak + 1.4:.2f} V",
                f"{v_load_peak / 2:.2f} V",
                f"{v_load_peak * 1.5:.2f} V",
                f"{0.70:.2f} V (stated diode drop instead of load voltage)",
                f"{v_peak + 0.7:.2f} V"
            ]
            q_text_diode = (f"A half-wave rectifier uses a single silicon diode (barrier potential drop V_barrier = 0.70 V) connected to an AC secondary "
                            f"output of V_rms = {v_ac:.1f} V. Given that V_peak = V_rms * √2 = {v_peak:.2f} V, calculate the PEAK VOLTAGE (V_load,peak) "
                            f"developed across the load resistor:")
            expl_diode = (f"During the forward conducting half-cycle, the diode drops 0.70 V across its p-n junction: "
                          f"V_load,peak = V_peak - V_barrier = {v_peak:.2f} V - 0.70 V = {corr_vlp}.")
            add_q("hard", "Diode Rectification Circuits", q_text_diode, corr_vlp, wrs_vlp, "Evaluating", "Calculate peak rectified output voltage across load", expl_diode)

    return questions

if __name__ == '__main__':
    qs = build_electromagnetism()
    out_dir = "dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_electromagnetism.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
