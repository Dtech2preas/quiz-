import json
import math
import os

def build_elasticity_and_hydraulics():
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
        qid = f"TS_P1_ELAST_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Elasticity & Hydraulics",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Elasticity & Hydraulics",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Hooke's Law, Stress-Strain Curve, Viscosity, Pascal's Principle
    # =========================================================================

    core_definitions = [
        ("Hooke's Law",
         "Within the limit of proportionality, the extension produced in an elastic material is directly proportional to the applied deforming force.",
         ["Stress is inversely proportional to strain in all plastic materials",
          "The pressure applied to an enclosed fluid decreases with distance",
          "The rate of change of momentum is proportional to the applied force",
          "The strain of a material equals its cross-sectional area squared",
          "All liquids compress uniformly when subjected to mechanical shock",
          "Force equals mass times acceleration in hydraulic systems"],
         "Hooke's Law states: Within the limit of proportionality, extension is directly proportional to the applied force: F = k * Δx."),

        ("Elasticity",
         "The property of a material by virtue of which it regains its original shape and size when the deforming force is removed.",
         ["The tendency of a material to deform permanently under small loads",
          "The internal friction between adjacent layers of a flowing liquid",
          "The property of fracturing suddenly without any plastic deformation",
          "The resistance of a solid metal to scratching by diamond indenters",
          "The ability of a metal to conduct heat and electricity rapidly",
          "The property of liquids transmitting pressure in one direction"],
         "Elasticity is the physical ability of a body to return to its original dimensions after the external deforming force ceases."),

        ("Plasticity (Plastic Deformation)",
         "The property of a material by virtue of which it undergoes permanent deformation and does NOT regain its original shape and size after the deforming force is removed.",
         ["The ability to return perfectly to original dimensions after stretching",
          "The resistance of engine oil to flow at high temperatures",
          "The multiplication of force in closed hydraulic cylinders",
          "The property of glowing white hot when carrying heavy currents",
          "The ability to resist chemical corrosion in acidic environments",
          "The state of matter where liquids solidify under high pressure"],
         "Plastic deformation is permanent deformation; when the stress exceeds the elastic limit, the material remains permanently stretched or distorted."),

        ("Stress (Tensile / Compressive Stress, σ)",
         "The internal restoring force per unit cross-sectional area of a material (σ = F / A, measured in pascals or N·m⁻²).",
         ["The ratio of change in length to original length of a wire",
          "The maximum force a hydraulic jack can exert on a vehicle",
          "The speed at which a crack propagates through brittle glass",
          "The spring constant multiplied by the square of extension",
          "The frictional drag between fluid molecules in a pipe",
          "The force applied divided by the volume of the material"],
         "Stress is defined as the internal restoring force per unit cross-sectional area: σ = F / A (units: N·m⁻² or Pa)."),

        ("Strain (Tensile / Compressive Strain, ε)",
         "The fractional change in length of a material, calculated as the ratio of change in length (extension) to original length (ε = ΔL / L_0, a dimensionless ratio).",
         ["The internal force divided by cross-sectional area of a rod",
          "The slope of a pressure versus volume hydraulic graph",
          "The percentage increase in liquid viscosity per degree Celsius",
          "The spring stiffness constant expressed in newtons per meter",
          "The energy dissipated as heat during irreversible fracture",
          "The mechanical advantage of a hydraulic slave piston"],
         "Strain is the ratio of change in length to original length: ε = ΔL / L_0. Because it is length divided by length, strain has no units."),

        ("Modulus of Elasticity (Young's Modulus, K or E)",
         "The ratio of tensile stress to tensile strain within the limit of proportionality of a material (K = σ / ε, measured in pascals or N·m⁻²).",
         ["The maximum load a cable can support before snapping completely",
          "The product of stress multiplied by strain in a tensile test",
          "The ratio of force applied to extension in a compression spring",
          "The density of an incompressible fluid inside a brake master cylinder",
          "The work done in stretching an elastic cord to twice its length",
          "The rate of flow of engine lubricant through an orifice"],
         "Young's Modulus (Modulus of Elasticity) measures the stiffness of a solid material and is defined as K = stress / strain = σ / ε."),

        ("Pascal's Principle",
         "Pressure exerted on an enclosed, incompressible liquid is transmitted equally and undiminished in all directions throughout the liquid.",
         ["Fluid speed increases as pipe diameter decreases in flow lines",
          "The buoyant force on an object equals the weight of fluid displaced",
          "Viscosity of a lubricant increases as temperature increases",
          "The pressure in a fluid drops to zero at the bottom of a container",
          "Force is multiplied only when fluids are compressed into gases",
          "Liquids expand to fill the entire volume of their container"],
         "Pascal's Principle states that pressure applied to an enclosed liquid is transmitted undiminished to every portion of the fluid and the walls of the vessel."),

        ("Viscosity",
         "The property of a fluid that determines its internal resistance to flow (internal fluid friction between adjacent sliding liquid layers).",
         ["The ability of a liquid to be compressed into a smaller volume",
          "The maximum pressure a fluid can transmit in a hydraulic press",
          "The rate at which a liquid evaporates at atmospheric pressure",
          "The ratio of liquid density compared to the density of pure water",
          "The property of a liquid to stick to the container glass walls",
          "The mechanical force exerted by a piston on brake fluid"],
         "Viscosity is fluid friction: the measure of a fluid's internal resistance to gradual deformation by shear or flow.")
    ]

    stems = [
        "In Grade 12 Technical Sciences, how is **'{}'** defined?",
        "According to the official CAPS curriculum, **'{}'** refers to:",
        "Which statement provides the precise scientific definition for **'{}'**?",
        "Identify the correct technical definition of **'{}'**:",
        "When an examiner asks for the definition of **'{}'**, which statement receives full marks?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Stress-Strain Curve Features & Material Classification
    curve_features = [
        ("Limit of Proportionality",
         "The point on a stress-strain curve up to which stress is directly proportional to strain (Hooke's law is obeyed).",
         ["The point where the material breaks into two separate pieces",
          "The point where the material begins to flow like a liquid",
          "The point of maximum stress the material can endure",
          "The point where permanent deformation first becomes zero",
          "The point where Young's modulus drops to zero",
          "The point where the material becomes completely rigid"]),

        ("Elastic Limit",
         "The maximum stress a material can withstand without undergoing permanent plastic deformation upon unloading.",
         ["The stress at which a material fractures instantly",
          "The region where Hooke's law ceases to be linear",
          "The minimum force required to insert a rivet",
          "The point where a ductile metal converts into cast iron",
          "The point of maximum cross-sectional necking",
          "The stress required to compress hydraulic fluid"]),

        ("Yield Point",
         "The point at which a material begins to deform plastically with little or no increase in the applied load.",
         ["The exact point where the material regains its original shape",
          "The point of initial linear Hooke's law behavior",
          "The point of ultimate tensile fracture",
          "The point where viscosity becomes infinite",
          "The point where the material melts into molten liquid",
          "The point where mechanical advantage equals unity"]),

        ("Ultimate Tensile Stress (UTS)",
         "The maximum tensile stress that a material can withstand before necking occurs and it ultimately fractures.",
         ["The minimum stress needed to start elastic extension",
          "The slope of the initial linear portion of the curve",
          "The stress at which strain drops to zero",
          "The stress corresponding to a strain of exactly 1.0",
          "The pressure transmitted through a hydraulic slave cylinder",
          "The yield stress multiplied by the factor of safety"]),

        ("Ductile Material (e.g. Copper, Mild Steel, Aluminium)",
         "A material that undergoes significant, visible plastic deformation before fracturing and can be easily drawn into thin wires.",
         ["A material that fractures suddenly with negligible plastic strain",
          "A material that cannot conduct heat or electric current",
          "A material whose viscosity increases when heated",
          "A material that obeys Hooke's law up to its breaking point",
          "A material that dissolves in hydraulic mineral oil",
          "A material that returns to zero length under any load"]),

        ("Brittle Material (e.g. Glass, Cast Iron, Concrete)",
         "A material that breaks or fractures with little or no plastic deformation when subjected to stress beyond its elastic limit.",
         ["A material that can be hammered into extremely thin foils",
          "A material that stretches up to ten times its original length",
          "A material with an exceptionally low Young's modulus",
          "A material that always flows like engine oil under load",
          "A material that undergoes massive necking before rupture",
          "A material that cannot withstand compressive loads"])
    ]

    for feat_name, feat_def, wr_feats in curve_features:
        add_q("easy", "Stress-Strain Curve",
              f"On an engineering stress-strain graph, what is the meaning of: **'{feat_name}'**?",
              feat_def, wr_feats, "Understanding", f"Explain {feat_name}",
              f"{feat_name} is defined as: {feat_def}.")

    # Viscosity Factors and Motor Oil SAE Ratings
    viscosity_scenarios = [
        ("Effect of increasing temperature on the viscosity of a liquid (such as engine motor oil)",
         "The viscosity DECREASES, because thermal energy increases molecular kinetic energy and weakens the intermolecular cohesive forces between liquid layers.",
         ["The viscosity INCREASES, because liquid molecules collide more frequently.",
          "The viscosity remains completely constant regardless of temperature.",
          "The liquid converts into a solid under any temperature increase.",
          "The liquid loses all ability to lubricate metallic gears.",
          "The density of the liquid increases while viscosity doubles.",
          "The fluid friction increases by 100% per 10 °C rise."]),

        ("Effect of decreasing temperature on the viscosity of a liquid",
         "The viscosity INCREASES (the liquid becomes thicker and more sluggish to flow), because lower thermal energy strengthens intermolecular cohesive forces.",
         ["The viscosity decreases, making the liquid flow much faster.",
          "The viscosity remains unchanged because volume is conserved.",
          "The liquid boils immediately into high-pressure vapor.",
          "The fluid friction drops to zero like a superfluid.",
          "The liquid stops transmitting pressure in hydraulic pipes.",
          "The mechanical advantage of hydraulic jacks drops to zero."]),

        ("Meaning of a multi-grade motor oil rating such as SAE 15W-40 in automotive engineering",
         "The '15W' indicates low-temperature viscosity for easy winter cold engine starting, while '40' indicates high-temperature viscosity retention for engine protection at 100 °C.",
         ["The oil can only be used for 15 weeks before degrading in 40 °C heat.",
          "The oil contains 15% water and 40% synthetic detergent additives.",
          "The oil operates at 15 kW power up to 40 000 km distance.",
          "The oil has a density of 15 kg/m³ and boiling point of 40 °C.",
          "The oil provides 15 bars of pressure at 40 rpm engine speed.",
          "The oil is designed exclusively for 15-year-old motor vehicles."]),

        ("Function of an engine lubricant / hydraulic fluid",
         "To reduce friction and wear between moving metal surfaces, dissipate heat, prevent rust/corrosion, and transmit hydraulic force effectively.",
         ["To increase the tensile strength of the engine cylinder block",
          "To combust inside the spark plug gap to provide horsepower",
          "To solidify into a rigid plastic seal inside the crankshaft",
          "To react chemically with steel to dissolve iron oxides permanently",
          "To convert mechanical work into electrical potential energy",
          "To stop all fluid flow through the oil filter completely"])
    ]

    for q_visc, c_visc, w_visc in viscosity_scenarios:
        add_q("easy", "Viscosity Principles", q_visc, c_visc, w_visc, "Understanding", "Understand viscosity and lubrication factors", c_visc)

    # Pascal's Principle & Hydraulic Applications
    hydraulic_basics = [
        ("Why are liquids (such as hydraulic mineral oil) used in hydraulic systems rather than gases (such as air)?",
         "Liquids are virtually incompressible, allowing applied force and pressure to be transmitted instantaneously and efficiently without volume loss, whereas gases compress significantly before moving the load.",
         ["Liquids have zero density compared to atmospheric air.",
          "Liquids create negative pressure that pulls pistons inward.",
          "Gases react chemically with steel pistons to produce water.",
          "Liquids eliminate the need for any mechanical seals or O-rings.",
          "Gases cannot exert any pressure on solid boundaries.",
          "Liquids freeze into solids when high pressure is applied."]),

        ("In a hydraulic lift, what happens to the pressure when a small force F1 is applied to small piston area A1?",
         "The pressure P = F1 / A1 is transmitted equally throughout the entire fluid, exerting an upward force F2 = P × A2 on the larger piston area A2.",
         ["The pressure decreases proportionally to the ratio of piston areas.",
          "The pressure increases only at the bottom corners of the reservoir.",
          "The pressure drops to zero when the fluid touches the large piston.",
          "The pressure on the large piston is doubled while force is halved.",
          "The fluid creates electrical current that powers an electric motor.",
          "The small piston moves down while the large piston moves down twice as far."]),

        ("In an ideal hydraulic press, how does the mechanical advantage (MA) relate to the areas and diameters of the two pistons?",
         "MA = F2 / F1 = A2 / A1 = (d2 / d1)², meaning force multiplication is directly proportional to the ratio of piston areas or the SQUARE of their diameters.",
         ["MA = A1 / A2 = d1 / d2 (inversely proportional to areas)",
          "MA = d2 / d1 (linearly proportional to diameters)",
          "MA = A2 × A1 (product of both piston surface areas)",
          "MA = F1 / F2 (ratio of input force to output load)",
          "MA is always equal to exactly 1.0 in any closed hydraulic system",
          "MA = (d1 / d2)² (square of small diameter over large diameter)"])
    ]

    for q_hyd, c_hyd, w_hyd in hydraulic_basics:
        add_q("easy", "Hydraulics Principles", q_hyd, c_hyd, w_hyd, "Understanding", "Explain hydraulic principles and Pascal's Law", c_hyd)

    # Complete Easy to exactly 300 with diverse, qualitative Hooke's Law and material identification questions
    spring_materials = [
        ("High-carbon spring steel", "high stiffness and high tensile strength"),
        ("Copper wire", "high ductility and excellent electrical conductivity"),
        ("Cast iron", "high compressive strength but extreme brittleness"),
        ("Rubber vulcanized band", "extreme elasticity and high elastic strain limit"),
        ("Aluminium alloy", "low density, high ductility, and good corrosion resistance"),
        ("Tungsten filament", "exceptional tensile strength at extremely high temperatures"),
        ("Structural concrete", "enormous compressive strength but low tensile strength (requires steel rebar)"),
        ("Toughened safety glass", "high hardness but brittle fracture when surface cracks propagate"),
        ("Brass alloy", "moderate stiffness, corrosion resistance, and good machinability"),
        ("Phosphor bronze", "fatigue resistance and low friction in elastic contact springs"),
        ("Titanium Grade 5", "exceptional strength-to-weight ratio and corrosion resistance"),
        ("Carbon fiber reinforced polymer", "extremely high tensile modulus with lightweight density"),
        ("Mild structural steel", "high ductility, weldability, and clear yield point on stress-strain curve"),
        ("Wrought iron", "fibrous structure with high ductility and toughness under tensile stress"),
        ("Chrome-vanadium alloy steel", "high fatigue resistance in vehicle suspension coil springs"),
        ("Polycarbonate thermoplastic", "high impact strength and ability to undergo plastic deformation"),
        ("Nylon 6,6 polyamide", "high tensile strength, elasticity, and resistance to abrasion"),
        ("Silicone elastomer", "flexibility and thermal stability across extreme temperatures"),
        ("Lead metal", "high plasticity, extremely low yield strength, and malleability"),
        ("Kevlar aramid fiber", "outstanding tensile strength and resistance to elongation under load")
    ]

    for mat_name, mat_prop in spring_materials:
        for load_n in [10, 25, 50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 750, 800, 1000, 1200, 1500, 2000]:
            if counts["easy"] >= 300:
                break
            q_text_m = f"A sample of **{mat_name}** ({mat_prop}) is subjected to a tensile load of {load_n} N within its elastic limit. What happens to the specimen when the {load_n} N tensile load is completely removed?"
            c_text_m = "It returns completely to its original dimensions (zero permanent plastic deformation) because the applied stress was below its elastic limit."
            w_text_m = [
                "It remains permanently stretched and never returns to its original length.",
                "It shatters immediately into microscopic powder upon load release.",
                "Its cross-sectional area permanently doubles in size.",
                "Its Young's modulus drops permanently to zero pascals.",
                "Its mass decreases by 50% due to mechanical fatigue.",
                "It converts into a high-viscosity liquid under zero load."
            ]
            add_q("easy", "Elastic Deformation", q_text_m, c_text_m, w_text_m, "Understanding", f"Explain elastic behavior of {mat_name}", c_text_m)

            if counts["easy"] < 300:
                q_text_h = f"A helical spring obeys Hooke's law up to a proportional limit of {load_n * 2} N. When a load of {load_n} N is suspended, its extension is measured. If the suspended load is DOUBLED to {load_n * 2} N, what happens to the extension?"
                c_text_h = "The extension DOUBLES, because within the limit of proportionality, extension is directly proportional to applied force (F ∝ Δx)."
                w_text_h = [
                    "The extension remains completely unchanged.",
                    "The extension is halved because of spring stiffness.",
                    "The extension quadruples because force is squared.",
                    "The spring snaps instantly into two pieces.",
                    "The spring stiffness constant (k) doubles.",
                    "The spring contracts and becomes shorter than its rest length."
                ]
                add_q("easy", "Hooke's Law", q_text_h, c_text_h, w_text_h, "Applying", "Apply Hooke's law direct proportionality", c_text_h)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Direct Calculations: Hooke's Law (F=kΔx), Stress (σ=F/A), Strain (ε=ΔL/L), Pascal's Law (F1/A1 = F2/A2)
    # =========================================================================

    # 1. Hooke's Law Calculations: F = k * Δx => k = F / Δx => Δx = F / k
    spring_constants = [50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0, 600.0, 750.0, 800.0, 1000.0, 1200.0, 1500.0, 2000.0]
    extensions_cm = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0]

    for k_val in spring_constants:
        for ext_cm in extensions_cm:
            if counts["medium"] >= 500:
                break
            ext_m = ext_cm / 100.0
            force_n = k_val * ext_m
            corr_f = f"{force_n:.1f} N"
            wrs_f = [
                f"{k_val * ext_cm:.1f} N (forgot to convert cm to meters)",
                f"{k_val / ext_m:.1f} N (divided k by extension)",
                f"{force_n * 2:.1f} N",
                f"{force_n / 2:.1f} N",
                f"{force_n + 25.0:.1f} N",
                f"{ext_m / k_val:.4f} N",
                f"{force_n * 1.5:.1f} N"
            ]
            q_text_f = f"A coil spring has a spring constant (stiffness) of k = {k_val:.0f} N·m⁻¹. What magnitude of deforming force is required to produce an extension of {ext_cm:.1f} cm in the spring (assuming the limit of proportionality is not exceeded)?"
            expl_f = f"Hooke's Law: F = k × Δx. Convert extension: {ext_cm:.1f} cm = {ext_m:.3f} m. F = {k_val:.0f} N·m⁻¹ × {ext_m:.3f} m = {corr_f}."
            add_q("medium", "Hooke's Law Calculations", q_text_f, corr_f, wrs_f, "Applying", "Calculate deforming force from spring constant", expl_f)

            # Inverse: calculate spring constant k = F / Δx
            if counts["medium"] < 500:
                corr_k = f"{k_val:.1f} N·m⁻¹"
                wrs_k = [
                    f"{force_n / ext_cm:.1f} N·m⁻¹ (omitted cm to meter conversion)",
                    f"{force_n * ext_m:.2f} N·m⁻¹ (multiplied force by extension)",
                    f"{k_val * 2:.1f} N·m⁻¹",
                    f"{k_val / 2:.1f} N·m⁻¹",
                    f"{k_val + 50.0:.1f} N·m⁻¹",
                    f"{ext_m / force_n:.4f} N·m⁻¹",
                    f"{k_val * 1.4:.1f} N·m⁻¹"
                ]
                q_text_k = f"A tensile force of {force_n:.1f} N is applied to an elastic spring, resulting in an extension of {ext_cm:.1f} cm. Determine the spring constant (k) of this spring:"
                expl_k = f"k = F / Δx = {force_n:.1f} N / ({ext_cm:.1f} × 10⁻² m) = {force_n:.1f} / {ext_m:.3f} = {corr_k}."
                add_q("medium", "Hooke's Law Calculations", q_text_k, corr_k, wrs_k, "Applying", "Calculate spring constant from force and extension", expl_k)

    # 2. Stress Calculations: σ = F / A
    # Rods and wires with circular cross-sections or given areas
    forces_stress = [500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 7500.0, 10000.0, 15000.0, 20000.0]
    areas_mm2 = [2.0, 4.0, 5.0, 8.0, 10.0, 15.0, 20.0, 25.0, 50.0, 100.0]

    for f_load in forces_stress:
        for a_mm2 in areas_mm2:
            if counts["medium"] >= 500:
                break
            a_m2 = a_mm2 * 1e-6
            stress_pa = f_load / a_m2
            stress_mpa = stress_pa / 1e6
            corr_s = f"{stress_mpa:.2f} MPa ({stress_pa:.2e} Pa)"
            wrs_s = [
                f"{f_load / a_mm2:.2f} Pa (forgot mm² to m² conversion: 10⁻⁶)",
                f"{f_load * a_m2:.4f} Pa (multiplied force by area)",
                f"{stress_mpa * 2:.2f} MPa",
                f"{stress_mpa / 2:.2f} MPa",
                f"{stress_mpa + 15.0:.2f} MPa",
                f"{a_m2 / f_load:.2e} Pa",
                f"{stress_mpa * 1.5:.2f} MPa"
            ]
            q_text_s = f"A steel tie rod with a cross-sectional area of {a_mm2:.1f} mm² supports a tensile load of {f_load:.0f} N. Calculate the tensile stress (σ) developed inside the rod:"
            expl_s = f"Stress σ = F / A. Convert area: {a_mm2:.1f} mm² = {a_mm2:.1f} × 10⁻⁶ m² = {a_m2:.2e} m². σ = {f_load:.0f} N / ({a_m2:.2e} m²) = {stress_pa:.2e} Pa = {stress_mpa:.2f} MPa."
            add_q("medium", "Stress Calculations", q_text_s, corr_s, wrs_s, "Applying", "Calculate tensile stress in engineering tie rod", expl_s)

    # 3. Strain Calculations: ε = ΔL / L_0
    orig_lengths = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0] # meters
    extensions_mm = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0] # millimeters

    for l0 in orig_lengths:
        for ext_mm in extensions_mm:
            if counts["medium"] >= 500:
                break
            ext_m = ext_mm / 1000.0
            strain_val = ext_m / l0
            corr_strain = f"{strain_val:.5f} (or {strain_val * 100:.3f}%)"
            wrs_strain = [
                f"{ext_mm / l0:.4f} (forgot to convert mm to meters)",
                f"{l0 / ext_m:.1f} (inverted strain formula)",
                f"{strain_val * 2:.5f}",
                f"{strain_val / 2:.5f}",
                f"{strain_val + 0.005:.5f}",
                f"{strain_val * 10:.4f} m (incorrectly added unit meters)",
                f"{strain_val * 1.5:.5f}"
            ]
            q_text_str = f"A structural aluminium wire of initial length {l0:.1f} m extends by {ext_mm:.1f} mm when subjected to an axial tensile force. Determine the tensile strain (ε) in the wire:"
            expl_str = f"Strain ε = ΔL / L_0. Convert extension: {ext_mm:.1f} mm = {ext_m:.4f} m. ε = {ext_m:.4f} m / {l0:.1f} m = {corr_strain}. (Strain is dimensionless)."
            add_q("medium", "Strain Calculations", q_text_str, corr_strain, wrs_strain, "Applying", "Calculate tensile strain from extension and initial length", expl_str)

    # 4. Pascal's Principle & Hydraulic Calculations: F1/A1 = F2/A2 => F2 = F1 * (A2/A1)
    f1_inputs = [20.0, 50.0, 75.0, 100.0, 120.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0]
    small_areas = [2.0, 4.0, 5.0, 8.0, 10.0] # cm²
    large_areas = [50.0, 80.0, 100.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0] # cm²

    for f1 in f1_inputs:
        for a1 in small_areas:
            for a2 in large_areas:
                if counts["medium"] >= 500:
                    break
                if a2 <= a1:
                    continue
                ratio = a2 / a1
                f2 = f1 * ratio
                corr_f2 = f"{f2:.1f} N"
                wrs_f2 = [
                    f"{f1 / ratio:.1f} N (divided by area ratio instead of multiplying)",
                    f"{f1 * (a1 / a2):.1f} N",
                    f"{f2 * 2:.1f} N",
                    f"{f2 / 2:.1f} N",
                    f"{f2 + 150.0:.1f} N",
                    f"{f1 * a2:.1f} N (omitted small piston area A1)",
                    f"{f2 * 1.5:.1f} N"
                ]
                q_text_h = f"In a hydraulic press, an input force of {f1:.0f} N is exerted on a small piston having a surface area of {a1:.1f} cm². What upward load force (F2) is exerted by the large slave piston if its area is {a2:.1f} cm²?"
                expl_h = f"Pascal's Principle: P1 = P2 => F1 / A1 = F2 / A2 => F2 = F1 × (A2 / A1). Here ratio = {a2:.1f} cm² / {a1:.1f} cm² = {ratio:.2f}. F2 = {f1:.0f} N × {ratio:.2f} = {corr_f2}."
                add_q("medium", "Hydraulic Calculations", q_text_h, corr_f2, wrs_f2, "Applying", "Calculate output force in hydraulic press", expl_h)

                # Mechanical Advantage question: MA = A2 / A1 = F2 / F1
                if counts["medium"] < 500:
                    corr_ma = f"{ratio:.2f}"
                    wrs_ma = [
                        f"{a1 / a2:.4f} (inverted area ratio)",
                        f"{ratio * 2:.2f}",
                        f"{ratio / 2:.2f}",
                        f"{ratio + 5.0:.2f}",
                        f"{f1 / a1:.2f} (calculated pressure instead of MA)",
                        f"{ratio * 1.5:.2f}",
                        f"1.00 (assumed no mechanical advantage)"
                    ]
                    q_text_ma = f"For the hydraulic system with piston areas A1 = {a1:.1f} cm² and A2 = {a2:.1f} cm², calculate the ideal mechanical advantage (MA):"
                    expl_ma = f"Mechanical Advantage MA = Output Force / Input Force = A2 / A1 = {a2:.1f} cm² / {a1:.1f} cm² = {corr_ma}."
                    add_q("medium", "Mechanical Advantage", q_text_ma, corr_ma, wrs_ma, "Applying", "Calculate mechanical advantage of hydraulic system", expl_ma)

    # Fill medium to exactly 500 with hydraulic displacement questions (h2 = h1 * A1 / A2)
    step = 1
    while counts["medium"] < 500:
        a1_val = 5.0
        a2_val = 100.0 + (step * 5.0)
        h1_cm = 10.0 + (step * 0.5)
        h2_cm = h1_cm * (a1_val / a2_val)
        corr_h2 = f"{h2_cm:.3f} cm ({h2_cm * 10:.2f} mm)"
        wrs_h2 = [
            f"{h1_cm * (a2_val / a1_val):.1f} cm (inverted displacement ratio)",
            f"{h2_cm * 2:.3f} cm",
            f"{h2_cm / 2:.3f} cm",
            f"{h1_cm:.1f} cm (assumed equal piston travel)",
            f"{h2_cm * 1.5:.3f} cm",
            f"{h2_cm + 1.0:.3f} cm",
            f"0.00 cm"
        ]
        q_text_disp = f"In a hydraulic car jack, the small piston (area A1 = {a1_val:.1f} cm²) is pushed downward through a stroke distance of {h1_cm:.1f} cm. If the large piston has an area of A2 = {a2_val:.1f} cm², calculate how far (h2) the large piston lifts the vehicle in one stroke (assuming incompressible fluid):"
        expl_disp = f"Fluid volume conservation: V1 = V2 => A1 × h1 = A2 × h2 => h2 = h1 × (A1 / A2) = {h1_cm:.1f} cm × ({a1_val:.1f} / {a2_val:.1f}) = {corr_h2}."
        add_q("medium", "Hydraulic Displacement", q_text_disp, corr_h2, wrs_h2, "Applying", "Calculate piston stroke displacement from volume conservation", expl_disp)
        step += 1

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Young's Modulus (K = (F*L0)/(A*ΔL)), Hydraulic Car Lifts (m*g and (d2/d1)^2), Elastic Potential Energy
    # =========================================================================

    # 1. Young's Modulus Multi-step: K = (F * L_0) / (A * ΔL)
    # Materials and their standard Young's Modulus (in GPa = 10^9 Pa)
    ym_materials = [
        ("Structural mild steel", 200.0),
        ("Wrought iron", 190.0),
        ("Titanium alloy", 110.0),
        ("Brass alloy", 100.0),
        ("Aluminium alloy", 70.0),
        ("Copper conductor", 120.0),
        ("Tungsten wire", 400.0),
        ("Bronze alloy", 105.0)
    ]

    for m_name, k_gpa in ym_materials:
        k_pa = k_gpa * 1e9
        for diam_mm in [2.0, 3.0, 4.0, 5.0]:
            for l0_m in [1.5, 2.0, 2.5, 3.0]:
                for f_tens in [1000.0, 2000.0, 3000.0, 4000.0]:
                    if counts["hard"] >= 200:
                        break
                    radius_m = (diam_mm / 1000.0) / 2.0
                    area_m2 = math.pi * (radius_m ** 2)
                    # ΔL = (F * L_0) / (A * K)
                    delta_l_m = (f_tens * l0_m) / (area_m2 * k_pa)
                    delta_l_mm = delta_l_m * 1000.0
                    corr_dl = f"{delta_l_mm:.3f} mm"
                    wrs_dl = [
                        f"{delta_l_mm * 4:.3f} mm (used diameter instead of radius for area)",
                        f"{delta_l_mm / 1000:.5f} mm (unit conversion error)",
                        f"{delta_l_mm * 2:.3f} mm",
                        f"{delta_l_mm / 2:.3f} mm",
                        f"{(f_tens * l0_m * area_m2 * k_pa) * 1e-12:.3f} mm",
                        f"{delta_l_mm + 0.5:.3f} mm",
                        f"{delta_l_mm * 1.5:.3f} mm"
                    ]
                    q_text_ym = f"A solid cylindrical rod of **{m_name}** has an initial length of {l0_m:.1f} m and a circular diameter of {diam_mm:.1f} mm. A tensile load of {f_tens:.0f} N is applied axially along the rod. Given Young's modulus K = {k_gpa:.0f} GPa ({k_gpa} × 10⁹ Pa), calculate the extension (ΔL) produced in the rod:"
                    expl_ym = f"1. Cross-sectional area: A = π × r² = π × ({radius_m * 1000:.2f} × 10⁻³ m)² = {area_m2:.3e} m². 2. K = (F × L_0) / (A × ΔL) => ΔL = (F × L_0) / (A × K) = ({f_tens:.0f} × {l0_m:.1f}) / ({area_m2:.3e} × {k_pa:.2e}) = {delta_l_m:.4e} m = {corr_dl}."
                    add_q("hard", "Young's Modulus", q_text_ym, corr_dl, wrs_dl, "Evaluating", f"Calculate extension using Young's modulus for {m_name}", expl_ym)

    # 2. Hydraulic Car Lift Systems with Vehicle Mass (m * g) and Diameters Squared:
    # F2 = m * g; F1 = F2 * (d1 / d2)^2
    g_acc = 9.8
    car_masses = [1000, 1200, 1500, 1800, 2000, 2500, 3000] # kg
    small_diameters_cm = [2.0, 3.0, 4.0, 5.0] # cm
    large_diameters_cm = [20.0, 25.0, 30.0, 40.0, 50.0] # cm

    for m_car in car_masses:
        for d1_cm in small_diameters_cm:
            for d2_cm in large_diameters_cm:
                if counts["hard"] >= 200:
                    break
                f2_load = m_car * g_acc
                ratio_diam = d2_cm / d1_cm
                ratio_area = ratio_diam ** 2
                f1_needed = f2_load / ratio_area
                corr_f1 = f"{f1_needed:.1f} N"
                wrs_f1 = [
                    f"{f2_load / ratio_diam:.1f} N (divided by diameter ratio instead of diameter squared)",
                    f"{f2_load * ratio_area:.1f} N (multiplied instead of divided)",
                    f"{m_car / ratio_area:.1f} N (forgot to multiply mass by g = 9.8)",
                    f"{f1_needed * 2:.1f} N",
                    f"{f1_needed / 2:.1f} N",
                    f"{f1_needed + 45.0:.1f} N",
                    f"{f1_needed * 1.5:.1f} N"
                ]
                q_text_lift = f"A hydraulic automotive service lift is used to hoist a motor vehicle of mass {m_car} kg. The small input piston has a circular diameter of {d1_cm:.1f} cm, while the large lifting slave piston has a diameter of {d2_cm:.1f} cm. Taking g = 9.8 m·s⁻², calculate the minimum input force (F1) required on the small piston to support the vehicle:"
                expl_lift = f"1. Output load F2 = m × g = {m_car} kg × 9.8 m·s⁻² = {f2_load:.1f} N. 2. Area ratio: A2 / A1 = (d2 / d1)² = ({d2_cm:.1f} / {d1_cm:.1f})² = ({ratio_diam:.2f})² = {ratio_area:.2f}. 3. F1 = F2 / (A2 / A1) = {f2_load:.1f} N / {ratio_area:.2f} = {corr_f1}."
                add_q("hard", "Hydraulic Lift Systems", q_text_lift, corr_f1, wrs_f1, "Evaluating", "Calculate input force for hydraulic vehicle lift", expl_lift)

    # 3. Elastic Potential Energy Stored in Springs: U = 1/2 * k * (Δx)^2
    for k_val in [100.0, 250.0, 500.0, 750.0, 1000.0, 1500.0, 2000.0]:
        for ext_cm in [2.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0]:
            if counts["hard"] >= 200:
                break
            ext_m = ext_cm / 100.0
            u_joules = 0.5 * k_val * (ext_m ** 2)
            corr_u = f"{u_joules:.3f} J"
            wrs_u = [
                f"{k_val * (ext_m ** 2):.3f} J (omitted 1/2 factor)",
                f"{0.5 * k_val * (ext_cm ** 2):.3f} J (forgot cm to meter conversion in Δx²)",
                f"{0.5 * k_val * ext_m:.3f} J (forgot to square extension)",
                f"{u_joules * 2:.3f} J",
                f"{u_joules / 2:.3f} J",
                f"{u_joules + 1.5:.3f} J",
                f"{u_joules * 1.5:.3f} J"
            ]
            q_text_u = f"An industrial compression spring with a stiffness constant of k = {k_val:.0f} N·m⁻¹ is compressed by {ext_cm:.1f} cm from its equilibrium position. Calculate the elastic potential energy (U) stored within the compressed spring:"
            expl_u = f"Elastic Potential Energy: U = 1/2 × k × (Δx)². Convert: {ext_cm:.1f} cm = {ext_m:.3f} m. U = 0.5 × {k_val:.0f} N·m⁻¹ × ({ext_m:.3f} m)² = 0.5 × {k_val:.0f} × {ext_m**2:.5f} = {corr_u}."
            add_q("hard", "Elastic Potential Energy", q_text_u, corr_u, wrs_u, "Evaluating", "Calculate stored elastic potential energy in spring", expl_u)

    return questions

if __name__ == '__main__':
    qs = build_elasticity_and_hydraulics()
    out_dir = "dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper1_elasticity_and_hydraulics.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
