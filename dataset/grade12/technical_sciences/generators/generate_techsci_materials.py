import json
import os

def build_materials():
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
        qid = f"TS_P2_MAT_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Materials",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Materials",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Mechanical Properties, Material Classes, Corrosion Basics
    # =========================================================================

    core_definitions = [
        ("Tensile Strength",
         "The maximum mechanical pulling or stretching stress that a material can withstand before necking, failing, or fracturing.",
         ["The resistance of a material to surface indentation and scratching",
          "The ability of a material to absorb impact energy without shattering",
          "The ease with which a material can be hammered into thin sheets",
          "The maximum compressive crushing load a pillar can support",
          "The rate at which a material conducts heat across a temperature gradient",
          "The capacity of a material to return to its original shape when unloaded"],
         "Tensile strength is the resistance of a material to breaking under tension (pulling/stretching forces)."),

        ("Compressive Strength",
         "The capacity of a material to withstand crushing, pushing, or squeezing loads without being crushed or permanently deformed.",
         ["The ability of a wire to be drawn through a die into thinner diameters",
          "The resistance of a cutting tool edge to abrasive wear",
          "The energy absorbed by a material during dynamic impact fracturing",
          "The maximum tensile stress a suspension bridge cable can sustain",
          "The electrical resistance offered to the passage of ionic current",
          "The property of softening repeatedly when subjected to heat"],
         "Compressive strength is the maximum compressive (squeezing/pushing) force a material can withstand without crushing."),

        ("Hardness",
         "The resistance of a material to localized plastic deformation, surface scratching, abrasion, cutting, or mechanical indentation.",
         ["The ability of a substance to absorb dynamic impact shocks without fracture",
          "The capacity to be stretched into thin wires without snapping",
          "The maximum pulling load supported before tensile fracture",
          "The property of returning to original dimensions after unloading",
          "The ease with which electrons move through a crystal lattice",
          "The tendency of a material to shatter spontaneously when dropped"],
         "Hardness is a surface property: resistance to scratching, abrasion, and indentation (e.g. Mohs, Brinell, Rockwell scales)."),

        ("Toughness",
         "The ability of a material to absorb mechanical energy and undergo plastic deformation without fracturing when subjected to high-speed impact or shock loads.",
         ["The resistance to surface scratching measured on the Mohs scale",
          "The tendency of a brittle ceramic to shatter into fragments under shock",
          "The maximum electrical voltage an insulator can block before breakdown",
          "The property of undergoing permanent elongation under light tension",
          "The ability of a metal to conduct heat through valence electrons",
          "The property of melting into a viscous liquid when heated"],
         "Toughness is the capacity of a material to absorb energy during impact deformation without fracturing (tested via Charpy/Izod tests)."),

        ("Brittleness",
         "The tendency of a material to fracture, crack, or shatter with little or no plastic deformation when subjected to mechanical stress (e.g. glass, unreinforced ceramics, cast iron).",
         ["The property that enables a material to be drawn out into long wires",
          "The ability to withstand massive impact shocks without breaking",
          "The property of returning elastically to original shape after large strains",
          "The capacity to absorb high amounts of energy prior to tensile failure",
          "The ease with which a material can be welded using oxy-acetylene torches",
          "The ability of a metal to resist oxidation in salt water environments"],
         "Brittleness is the tendency to fracture with little or no plastic deformation when stressed (opposite of toughness)."),

        ("Ductility",
         "The mechanical property of a material that allows it to undergo significant plastic deformation under tensile stress, enabling it to be drawn out into thin wires without breaking (e.g. copper, gold, mild steel).",
         ["The ability of a material to be hammered or rolled into flat sheets",
          "The resistance of a surface to abrasive wear by sand particles",
          "The property of shattering instantly when dropped onto a hard floor",
          "The capacity to support massive compressive crushing loads",
          "The ability of a liquid resin to solidify into an insoluble polymer",
          "The thermal expansion coefficient measured per degree Celsius"],
         "Ductility is the property that enables a material to be drawn into wires under tensile pulling forces."),

        ("Malleability",
         "The mechanical property of a material that allows it to undergo extensive plastic deformation under compressive stress, enabling it to be hammered, beaten, or rolled into thin sheets without cracking (e.g. gold, aluminium, lead).",
         ["The ability to be pulled into fine electrical wires without breaking",
          "The resistance of a cutting blade to losing its sharp edge",
          "The capacity to absorb sudden shock impacts without cracking",
          "The tendency to shatter into sharp fragments under light hammer taps",
          "The property of conducting electric current with zero resistance",
          "The chemical resistance to corrosion in concentrated sulfuric acid"],
         "Malleability is the property that allows a material to be hammered or rolled into thin sheets under compressive forces."),

        ("Thermoplastic",
         "A polymer consisting of linear or branched chains held together by weak intermolecular forces; it softens and melts when heated and hardens when cooled, allowing it to be repeatedly remoulded and recycled (e.g. PE, PVC, PP, PET).",
         ["A polymer cross-linked by permanent covalent bonds that chars without melting",
          "An inorganic ceramic material composed of silicon carbide crystals",
          "A composite material made of steel reinforcement embedded in concrete",
          "A metallic alloy consisting of copper and zinc melted together",
          "A thermosetting resin that cannot be softened once cured",
          "A natural rubber vulcanized with extensive sulfur cross-link bridges"],
         "Thermoplastics have weak intermolecular forces between chains; they soften on heating and solidify on cooling, making them recyclable."),

        ("Thermosetting Plastic (Thermoset)",
         "A polymer formed with extensive covalent cross-links between polymer chains during curing; once set, it permanently retains its shape and decomposes, chars, or burns when heated rather than melting, making it non-recyclable (e.g. Bakelite, Melamine, Epoxy).",
         ["A plastic that can be melted and remoulded repeatedly hundreds of times",
          "A linear polymer held together only by weak London dispersion forces",
          "A volatile organic liquid that evaporates rapidly at room temperature",
          "A biodegradable polymer derived exclusively from corn starch sugars",
          "A ductile metallic compound that conducts electricity easily",
          "A soft elastomer that melts into a thin liquid at 80 °C"],
         "Thermosets possess permanent covalent cross-links; they char/decompose upon heating and cannot be remelted or reshaped."),

        ("Composite Material",
         "A material engineered by combining two or more distinct materials with significantly different physical or chemical properties—a continuous matrix (binder) and a dispersed reinforcement—yielding superior combined properties (e.g. reinforced concrete, fibreglass, carbon fibre).",
         ["A pure chemical element containing only one type of atom in its lattice",
          "A homogeneous solution of two gases mixed at standard atmospheric pressure",
          "A single polymer chain composed of identical repeating monomer units",
          "An unreinforced ceramic tile composed solely of baked clay",
          "A pure metal that has been polished to a mirror finish",
          "A chemical electrolyte that dissociates into hydronium and nitrate ions"],
         "A composite consists of a matrix (binder) and reinforcement (fibres/particles) working together to produce superior engineering properties."),

        ("Corrosion (Rusting of Iron)",
         "The electrochemical degradation and deterioration of iron or steel caused by its spontaneous reaction with atmospheric oxygen and water, forming hydrated iron(III) oxide (Fe₂O₃·xH₂O).",
         ["The physical abrasion of metal surfaces caused by rubbing friction",
          "The thermal melting of metallic iron at its melting point of 1538 °C",
          "The purification of copper metal using an electrolytic refining tank",
          "The mechanical hardening of steel caused by hammering and rolling",
          "The radioactive decay of unstable iron isotopes into manganese",
          "The deposition of pure silver onto an iron spoon at the cathode"],
         "Rusting is the electrochemical corrosion of iron in the presence of oxygen and water: 4Fe + 3O₂ + 2xH₂O -> 2Fe₂O₃·xH₂O."),

        ("Galvanizing",
         "The process of coating iron or steel with a protective thin layer of ZINC (usually via hot-dipping); zinc acts as both a physical barrier and a SACRIFICIAL ANODE, corroding preferentially to protect the underlying iron even if scratched.",
         ["Coating iron with a thin layer of copper using electroplating",
          "Painting iron with oil-based primer without any metallic coating",
          "Heating steel to bright red heat and quenching in cold oil",
          "Smelting iron ore with limestone in a blast furnace",
          "Spraying molten aluminium into concrete to make composites",
          "Adding plasticizers to iron to increase its ductility and flexibility"],
         "Galvanizing: Coating iron/steel with ZINC. Zinc acts as a barrier and sacrificial anode (Zn oxidizes preferentially to Fe).")
    ]

    stems = [
        "In Grade 12 Technical Sciences Materials Science, how is **'{}'** defined?",
        "According to the CAPS curriculum, **'{}'** refers to:",
        "Which statement provides the exact scientific definition of **'{}'**?",
        "Identify the correct CAPS definition for **'{}'**:",
        "In an engineering examination context, which statement accurately defines **'{}'**?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # Classification of Materials (Easy)
    mat_classes = [
        ("Ferrous metals vs Non-ferrous metals",
         "Ferrous metals contain IRON as the primary constituent and are generally magnetic and prone to rusting (e.g. mild steel, cast iron, stainless steel); Non-ferrous metals do NOT contain iron and are non-magnetic and corrosion-resistant (e.g. copper, aluminium, zinc, gold, brass).",
         ["Ferrous metals contain copper while non-ferrous metals contain lead.",
          "Ferrous metals are all liquids at room temperature while non-ferrous are solids.",
          "Ferrous metals cannot conduct electricity under any circumstances.",
          "Non-ferrous metals are artificial polymers while ferrous metals are minerals.",
          "Ferrous metals are non-magnetic while non-ferrous metals are permanent magnets.",
          "Non-ferrous metals rust twice as fast as ferrous metals in humid air."],
         "Ferrous = contains iron (Fe), magnetic, rusts. Non-ferrous = no iron, non-magnetic, corrosion-resistant."),

        ("Alloy",
         "A homogeneous mixture or solid solution composed of two or more chemical elements, where at least one of the primary elements is a metal (e.g. brass = copper + zinc, bronze = copper + tin, steel = iron + carbon).",
         ["A pure chemical element found in its native uncombined mineral state",
          "A synthetic thermosetting polymer formed by condensation reactions",
          "A composite material made exclusively of ceramic fibres in glass",
          "An aqueous electrolyte that conducts electricity in galvanic cells",
          "An organic compound containing only carbon, hydrogen, and oxygen",
          "A mineral slag floating on top of molten copper in a blast furnace"],
         "An alloy is a metallic mixture of two or more elements (e.g. brass = Cu + Zn, steel = Fe + C)."),

        ("Ceramics",
         "Inorganic, non-metallic solid materials made from compounds of a metal and a non-metal (such as oxides, carbides, nitrides) shaped and hardened by high-temperature firing; they are typically hard, brittle, heat-resistant, and electrical insulators.",
         ["Organic polymers composed of long hydrocarbon chains with covalent cross-links",
          "Homogeneous mixtures of metals that conduct electricity with zero resistance",
          "Volatile liquids that evaporate rapidly to produce high vapor pressure",
          "Synthetic composite plastics reinforced with woven fiberglass mats",
          "Ferrous alloys containing more than 50% chromium and nickel",
          "Biological proteins formed from condensation of natural amino acids"],
         "Ceramics are inorganic, non-metallic materials hardened by heat; hard, brittle, heat-resistant electrical insulators."),

        ("Constituents of a Composite Material: Matrix and Reinforcement",
         "The MATRIX is the continuous surrounding phase (binder) that holds the reinforcement in place, distributes applied stresses, and protects the fibers; the REINFORCEMENT is the dispersed strong fiber/particulate phase that carries the primary tensile or mechanical loads.",
         ["The matrix is the steel reinforcement and the reinforcement is the concrete",
          "Both matrix and reinforcement are identical plastic resins mixed together",
          "The matrix carries the load while the reinforcement acts solely as a dye",
          "The reinforcement dissolves into the matrix to form a single chemical solution",
          "The matrix is an electrolyte that conducts direct electrical current",
          "The reinforcement is a sacrificial zinc layer that prevents rusting"],
         "Composite: Matrix = continuous binder phase (protects/transfers stress); Reinforcement = load-bearing fibers/particles.")
    ]

    for mc_title, mc_ans, mc_wrongs, mc_expl in mat_classes:
        for st_mc in [
            "In materials technology, explain: **{}**",
            "What is the defining characteristic of: **{}**?",
            "Which statement accurately classifies: **{}**"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Material Classification", st_mc.format(mc_title), mc_ans, mc_wrongs, "Understanding", f"Explain {mc_title}", mc_expl)

    # Thermoplastics vs Thermosets Identification (Easy)
    poly_examples_easy = [
        ("Polyethene (PE)", "THERMOPLASTIC", "plastic carrier bags, squeeze bottles, and packaging film"),
        ("Polyvinyl chloride (PVC)", "THERMOPLASTIC", "plumbing pipes, electrical conduit, and window frames"),
        ("Polypropylene (PP)", "THERMOPLASTIC", "food storage containers, reusable crates, and automotive battery cases"),
        ("Polystyrene (PS)", "THERMOPLASTIC", "disposable cutlery, CD cases, and expanded foam coffee cups"),
        ("Polyethylene terephthalate (PET)", "THERMOPLASTIC", "transparent plastic soft drink bottles and synthetic polyester textiles"),
        ("Bakelite (phenol-formaldehyde)", "THERMOSETTING PLASTIC", "heat-resistant electrical switchgear, saucepan handles, and distributor caps"),
        ("Melamine-formaldehyde (Formica)", "THERMOSETTING PLASTIC", "scratch-resistant kitchen countertops, unbreakable dinnerware, and laminate flooring"),
        ("Epoxy resin", "THERMOSETTING PLASTIC", "high-strength engineering adhesives, composite matrices, and circuit board laminates"),
        ("Polyurethane (rigid foam)", "THERMOSETTING PLASTIC", "thermal insulation boards, refrigerator insulation, and skateboard wheels"),
        ("Vulcanized rubber", "ELASTOMER (THERMOSET)", "automotive vehicle tyres and heavy-duty conveyor belts with sulfur cross-links")
    ]

    for p_mat, p_type, p_use in poly_examples_easy:
        for st_pe in [
            f"How is **{p_mat}** classified based on its response to heat, and what is its typical use ({p_use})?",
            f"In Grade 12 Technical Sciences, **{p_mat}** is classified as a:",
            f"Identify the thermal plastic classification of **{p_mat}**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_pe = f"It is a {p_type}."
            w_pe = [
                f"It is a {'THERMOSETTING PLASTIC' if p_type == 'THERMOPLASTIC' else 'THERMOPLASTIC'} that dissolves completely in water.",
                "It is a non-ferrous bronze alloy consisting of copper and tin.",
                "It is an inorganic ceramic material hardened by high-temperature firing.",
                "It is a ferrous metal alloy containing iron and carbon.",
                "It is a natural unrefined mineral ore extracted from opencast mines.",
                "It is a supercooled covalent glass with an amorphous quartz network."
            ]
            expl_pe = f"{p_mat} is a {p_type}; commonly used for {p_use}."
            add_q("easy", "Polymer Classification", st_pe, c_pe, w_pe, "Remembering", f"Classify {p_mat}", expl_pe)

    # Conditions Required for Rusting of Iron (Easy)
    rust_conditions = [
        ("Two essential substances strictly required for iron to rust",
         "OXYGEN GAS (O2) and LIQUID WATER / MOISTURE (H2O); in the absence of either oxygen or water, iron will not undergo rusting.",
         ["Carbon dioxide gas and ultraviolet light only",
          "Nitrogen gas and mineral engine oil",
          "Pure dry oxygen in the total absence of moisture",
          "Boiled distilled water covered with a layer of oil in the absence of air",
          "Hydrogen gas and sulfur dioxide fumes",
          "Direct sunlight and dry desert sand"],
         "Rusting strictly requires BOTH oxygen (O₂) and water (H₂O). In dry air or deoxygenated water, iron will not rust."),

        ("Chemical identity and chemical formula of Rust",
         "Hydrated iron(III) oxide with the general chemical formula Fe₂O₃·xH₂O (reddish-brown flaky solid).",
         ["Iron(II) sulfide (FeS, black insoluble powder)",
          "Pure elemental iron metal crystals (Fe(s))",
          "Iron(II) sulfate heptahydrate (FeSO₄·7H₂O, green vitriol)",
          "Iron carbide (Fe₃C / cementite found in pearlite steel)",
          "Iron(III) chloride hexahydrate (FeCl₃·6H₂O)",
          "Sodium zincate gel (Na₂[Zn(OH)₄])"],
         "Rust is hydrated iron(III) oxide: Fe₂O₃·xH₂O."),

        ("Why salt water (seawater) drastically accelerates the rusting of iron and steel",
         "Salt (NaCl) dissociates into mobile sodium and chloride ions, greatly increasing the ELECTRICAL CONDUCTIVITY of the water electrolyte, which speeds up the transfer of electrons and ions in the microscopic electrochemical corrosion cells.",
         ["Salt water dissolves the iron metal through an acid-base neutralization",
          "Sodium ions react directly with steel to form volatile sodium gas",
          "Salt removes all dissolved oxygen from the water immediately",
          "Salt water converts iron into a stainless steel alloy spontaneously",
          "Salt crystals mechanically scrape away the zinc galvanized layer",
          "Salt water prevents the formation of any hydroxide ions"],
         "Salt increases the ionic conductivity of the water, accelerating electron and ion transport in corrosion cells.")
    ]

    for rc_title, rc_ans, rc_wrongs, rc_expl in rust_conditions:
        for st_rc in [
            "What is the scientific fact regarding: **{}**?",
            "In Technical Sciences metallurgy and corrosion, explain: **{}**",
            "Which statement accurately evaluates: **{}**"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Corrosion Fundamentals", st_rc.format(rc_title), rc_ans, rc_wrongs, "Understanding", f"Explain {rc_title}", rc_expl)

    # Plastic Resin Identification Codes (RIC 1 to 7) (Easy)
    recycling_codes = [
        ("Resin Identification Code 1 (PET / PETE)", "Polyethylene terephthalate", "transparent cold beverage bottles, peanut butter jars, and polyester fibers"),
        ("Resin Identification Code 2 (HDPE)", "High-density polyethylene", "milk jugs, bleach bottles, domestic detergent containers, and wheelie bins"),
        ("Resin Identification Code 3 (PVC / V)", "Polyvinyl chloride", "plumbing pipes, garden hoses, medical IV tubing, and credit cards"),
        ("Resin Identification Code 4 (LDPE)", "Low-density polyethylene", "plastic grocery carrier bags, squeeze sauce bottles, and stretch shrink wrap"),
        ("Resin Identification Code 5 (PP)", "Polypropylene", "margarine tubs, yogurt containers, medicine prescription bottles, and bottle caps"),
        ("Resin Identification Code 6 (PS)", "Polystyrene", "disposable plastic cutlery, CD jewel cases, meat trays, and expanded foam coffee cups"),
        ("Resin Identification Code 7 (OTHER)", "Other plastics (e.g. Polycarbonate, Acrylic, Nylon, Bioplastics)", "multi-layer food pouches, safety goggles, baby bottles, and fiberglass resin")
    ]

    for ric_code, ric_poly, ric_uses in recycling_codes:
        for st_ric in [
            f"Which polymer and commercial use corresponds to **{ric_code}**?",
            f"In the international plastic recycling numbering system, **{ric_code}** designates:",
            f"Identify the plastic material identified by **{ric_code}**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_ric = f"{ric_poly} (used for {ric_uses})."
            w_ric = [
                f"{'Polypropylene' if 'Polyethylene terephthalate' in ric_poly else 'Polyethylene terephthalate'} (thermoset resin).",
                "Non-ferrous cast bronze alloy.",
                "Reinforced silica ceramic aggregate.",
                "Vulcanized natural rubber elastomer.",
                "Unreinforced portland cement paste.",
                "High-speed tool steel alloy."
            ]
            add_q("easy", "Plastic Recycling Codes", st_ric, c_ric, w_ric, "Remembering", f"Identify {ric_code}", c_ric)

    # Specific Alloy Compositions (Easy)
    alloy_compositions = [
        ("Brass", "Copper (Cu) and Zinc (Zn)", "musical instruments, plumbing valves, and decorative hardware"),
        ("Bronze", "Copper (Cu) and Tin (Sn)", "heavy-duty rotating bearings, ship propellers, and commemorative statues"),
        ("Mild Steel (Carbon steel)", "Iron (Fe) and Carbon (C, ~0.2%)", "structural building beams, car body panels, and construction mesh"),
        ("Stainless Steel", "Iron (Fe), Chromium (Cr, ≥ 10.5%), and Nickel (Ni)", "surgical scalpels, commercial cutlery, and chemical reactors"),
        ("Duralumin", "Aluminium (Al), Copper (Cu), Magnesium (Mg), and Manganese (Mn)", "aircraft structural frames and lightweight racing components"),
        ("Soft Solder (traditional)", "Tin (Sn) and Lead (Pb)", "soldering electrical joints and copper plumbing pipe fittings"),
        ("Cast Iron", "Iron (Fe), Carbon (C, 2-4%), and Silicon (Si)", "engine cylinder blocks, machine tool beds, and manhole covers")
    ]

    for al_name, al_constits, al_uses in alloy_compositions:
        for st_al in [
            f"What are the principal chemical constituents of the metallic alloy **{al_name}**?",
            f"In metallurgy and materials engineering, **{al_name}** is composed of:",
            f"Identify the primary metals that make up **{al_name}** ({al_uses}):"
        ]:
            if counts["easy"] >= 300:
                break
            c_al = f"Composed of {al_constits}."
            w_al = [
                "Composed of pure elemental gold and platinum.",
                "Composed of silicon carbide and alumina ceramic.",
                "Composed of polyethene and vulcanized sulfur.",
                "Composed of lead and radioactive uranium.",
                "Composed of sodium and chlorine ions in salt.",
                "Composed of mercury and liquid nitrogen."
            ]
            add_q("easy", "Alloy Compositions", st_al, c_al, w_al, "Remembering", f"Identify composition of {al_name}", c_al)

    # Elastic vs Plastic Deformation and Testing (Easy)
    elastic_plastic_easy = [
        ("Elastic Deformation",
         "Temporary and reversible deformation; when the applied mechanical load is removed, the material returns completely to its original dimensions (Hooke's law applies).",
         ["Permanent and irreversible deformation that remains after unloading",
          "The sudden catastrophic shattering of a brittle material without warning",
          "The chemical decomposition of a polymer when heated above 200 °C",
          "The corrosion of metallic surfaces in humid salt air",
          "The drawing of a metal ingot into long electrical wires",
          "The melting of an alloy into a homogeneous liquid solution"]),

        ("Plastic Deformation",
         "Permanent and irreversible deformation; when the applied stress exceeds the elastic limit (yield point), the material does not return to its original shape upon unloading.",
         ["Temporary deformation that disappears entirely when load is released",
          "The reversible expansion of a gas inside a pneumatic cylinder",
          "The vibration of molecules in a crystal lattice at absolute zero",
          "The elastic bounce of a rubber ball on a concrete floor",
          "The transmission of alternating electric current along copper wires",
          "The solidification of a thermoplastic resin inside a cold mould"]),

        ("Elastic Limit (Yield Point)",
         "The maximum stress that a material can withstand without undergoing permanent plastic deformation upon complete removal of the applied load.",
         ["The point at which a material shatters instantly into sharp pieces",
          "The temperature at which a polymer melts into a thin liquid",
          "The minimum electrical current required to initiate corrosion",
          "The speed of sound propagating through a metallic bar",
          "The density of a composite material divided by its volume",
          "The percentage of carbon required to produce stainless steel"]),

        ("Charpy Impact Test / Izod Impact Test",
         "Standardized engineering tests used to measure the dynamic TOUGHNESS (impact energy absorbed before fracture) of a material by striking a notched specimen with a swinging pendulum.",
         ["A test used solely to measure the electrical resistivity of copper wires",
          "A test that measures the surface hardness using a diamond indenter",
          "A chemical test that determines the rate of iron rusting in seawater",
          "A tensile test measuring elongation before necking under slow loads",
          "A thermal test measuring the melting point of thermoplastics",
          "An ultrasonic test detecting hidden air bubbles in poured concrete"]),

        ("Brinell Hardness Test / Rockwell Hardness Test",
         "Engineering indentation tests used to determine the surface HARDNESS of a material by pressing a hardened steel ball or diamond cone indenter into the surface under a standard load.",
         ["A test measuring the electrical current flowing during electroplating",
          "A test measuring the impact toughness using a swinging hammer",
          "A chemical titration measuring the concentration of acid rain",
          "A tensile pulling test used to draw wires through a tungsten die",
          "A bending test evaluating the shear modulus of composite beams",
          "A test determining the degree of polymerization of polyethylene"])
    ]

    for ep_title, ep_ans, ep_wrongs in elastic_plastic_easy:
        for st_ep in [
            f"What is the definition and engineering significance of **'{ep_title}'**?",
            f"In mechanical testing and materials science, **'{ep_title}'** refers to:",
            f"Which statement accurately explains **'{ep_title}'**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Deformation & Mechanical Testing", st_ep.format(ep_title), ep_ans, ep_wrongs, "Remembering", f"Define {ep_title}", ep_ans)

    # Elastic vs Plastic Deformation Scenarios (Easy)
    deformation_scenarios_easy = [
        ("Stretching a rubber resistance band during physical exercise and releasing it", "ELASTIC DEFORMATION", "the band returns completely to its original length when the pulling force is removed"),
        ("Compressing a steel coil spring inside a ballpoint pen clicker", "ELASTIC DEFORMATION", "the spring returns to its original uncompressed height when the button is released"),
        ("Deflecting a fiberglass diving board as a diver jumps off", "ELASTIC DEFORMATION", "the board flexes elastically and springs back to its horizontal position"),
        ("Stretching the nylon fabric of a trampoline while a gymnast bounces", "ELASTIC DEFORMATION", "the trampoline mat recovers its original taut flat shape when unloaded"),
        ("Bending a steel paperclip back and forth until it stays bent in a new shape", "PLASTIC DEFORMATION", "the applied stress exceeded the yield point, causing permanent, irreversible deformation"),
        ("Denting an automobile steel door panel in a parking collision", "PLASTIC DEFORMATION", "the metal undergoes permanent displacement beyond its elastic limit that does not recover"),
        ("Drawing a thick copper rod through a tungsten die to manufacture thin electrical wire", "PLASTIC DEFORMATION", "the metal is permanently elongated into wire through plastic flow"),
        ("Rolling an aluminium ingot between heavy rollers to manufacture thin aluminium kitchen foil", "PLASTIC DEFORMATION", "compressive stresses exceed the yield strength, permanently reducing foil thickness")
    ]

    for def_act, def_kind, def_rsn in deformation_scenarios_easy:
        for st_ds in [
            f"How is the mechanical deformation classified when **{def_act}**?",
            f"In mechanical engineering, the scenario '**{def_act}**' represents:",
            f"Identify the classification and behavior of: **{def_act}**"
        ]:
            if counts["easy"] >= 300:
                break
            c_ds = f"{def_kind} because {def_rsn}."
            w_ds = [
                f"{'PLASTIC DEFORMATION' if 'ELASTIC' in def_kind else 'ELASTIC DEFORMATION'} because all materials are completely brittle.",
                "Thermal creep failure caused by high operating temperatures.",
                "Corrosion fatigue caused by oxidation in humid air.",
                "Brittle fracture with zero energy absorption.",
                "Spontaneous radioactive transmutation of metal atoms.",
                "Total failure where the material shatters into dust."
            ]
            add_q("easy", "Elastic vs Plastic Scenarios", st_ds, c_ds, w_ds, "Understanding", f"Classify deformation in {def_act[:25]}", c_ds)

    # Ferrous vs Non-Ferrous Material Identification (Easy)
    metal_classification_easy = [
        ("Mild Steel (low-carbon steel)", "FERROUS ALLOY", "it contains iron (Fe) as the main element and is magnetic and subject to rusting"),
        ("Cast Iron", "FERROUS ALLOY", "it contains iron with 2-4% carbon and is widely used for heavy engine blocks"),
        ("Stainless Steel (18/8)", "FERROUS ALLOY", "it is an iron-based alloy containing chromium and nickel"),
        ("Pure Copper", "NON-FERROUS METAL", "it does not contain iron, is non-magnetic, highly ductile, and resistant to atmospheric corrosion"),
        ("Pure Aluminium", "NON-FERROUS METAL", "it is a lightweight metal containing zero iron and passivated by an Al₂O₃ oxide film"),
        ("Brass (Cu + Zn)", "NON-FERROUS ALLOY", "it is composed of copper and zinc with no iron"),
        ("Bronze (Cu + Sn)", "NON-FERROUS ALLOY", "it is composed of copper and tin with zero iron content"),
        ("Pure Zinc", "NON-FERROUS METAL", "it contains zero iron and is used as a sacrificial anode and galvanizing coating"),
        ("Pure Lead", "NON-FERROUS METAL", "it is a dense, soft, malleable non-ferrous metal with no iron"),
        ("Titanium (Ti)", "NON-FERROUS METAL", "it is a high-strength, lightweight non-ferrous metal highly resistant to corrosion"),
        ("Pure Gold (Au)", "NON-FERROUS NOBLE METAL", "it contains zero iron, does not tarnish, and is the most malleable metal known")
    ]

    for met_id_name, met_id_class, met_id_desc in metal_classification_easy:
        for st_mic in [
            f"How is **{met_id_name}** classified in materials engineering?",
            f"In the classification of engineering metals, **{met_id_name}** is a:",
            f"Identify whether **{met_id_name}** is ferrous or non-ferrous:"
        ]:
            if counts["easy"] >= 300:
                break
            c_mic = f"{met_id_class} ({met_id_desc})."
            w_mic = [
                f"{'NON-FERROUS METAL' if 'FERROUS' in met_id_class else 'FERROUS ALLOY'} containing 95% radioactive uranium.",
                "Inorganic vitreous ceramic hardened by kiln firing.",
                "Thermosetting phenolic resin cross-linked by covalent bonds.",
                "Composite material made of carbon fibers in an epoxy matrix.",
                "Synthetic elastomer with vulcanized sulfur bridges.",
                "Natural organic polymer derived from tree cellulose."
            ]
            add_q("easy", "Metal Classification", st_mic, c_mic, w_mic, "Remembering", f"Classify {met_id_name}", c_mic)

    # Hooke's Law and Mechanical Behavior Concepts (Easy)
    hookes_law_concepts = [
        ("Hooke's Law",
         "The mechanical extension or compression of an elastic material is directly proportional to the applied tensile or compressive force, provided the limit of proportionality is not exceeded (F = k·Δx).",
         ["The strain of a material is inversely proportional to its temperature at constant volume",
          "The electrical current is proportional to the magnetic field strength in a coil",
          "The density of an alloy increases exponentially with applied hydrostatic pressure",
          "The force required to fracture a material is proportional to its melting point",
          "The plastic deformation of a polymer is independent of the load duration",
          "The energy dissipated in a collision is equal to the momentum difference"],
         "Hooke's Law states that extension is directly proportional to applied force up to the limit of proportionality: F = k·Δx."),

        ("Limit of Proportionality",
         "The maximum load or stress up to which the strain in a material remains strictly directly proportional to the applied stress, obeying Hooke's Law (the straight-line portion of the stress-strain curve).",
         ["The point at which a material breaks into two separate pieces under tension",
          "The minimum temperature at which a polymer melts into a liquid",
          "The maximum hardness number attainable on the Mohs mineral scale",
          "The electrical potential at which electrolysis begins at the anode",
          "The stress value where the cross-sectional area begins necking",
          "The rate of oxidation of iron in seawater at standard temperature"],
         "The limit of proportionality is the end of the linear (straight-line) region where Hooke's law (stress ∝ strain) is obeyed."),

        ("Spring Constant (k)",
         "A measure of the stiffness of a spring or elastic material, defined as the force required per unit extension or compression (k = F / Δx), measured in Newtons per metre (N·m⁻¹).",
         ["The maximum load a spring can bear before permanent plastic snapping occurs",
          "The dimensionless ratio of change in length to original unextended length",
          "The rate of heat transfer through a metallic spring coil per second",
          "The frequency of sound waves produced by a vibrating coil spring",
          "The mass of the spring divided by its total uncoiled wire length",
          "The electrical resistance of the steel wire forming the coil"],
         "The spring constant k = F / Δx represents the stiffness of the spring, with SI unit N·m⁻¹."),

        ("Stress-Strain Curve: Elastic Region vs Plastic Region",
         "In the ELASTIC region (below the yield point), strain is fully reversible upon unloading; in the PLASTIC region (above the yield point), permanent deformation occurs and the material does not return to its original length.",
         ["In the elastic region the material shatters; in the plastic region it conducts electricity",
          "Both regions exhibit identical permanent deformation that cannot be reversed",
          "The plastic region is completely linear while the elastic region is parabolic",
          "The elastic region only exists when materials are heated to their melting point",
          "The plastic region represents zero stress regardless of applied strain",
          "Deformation is reversible in both regions until catastrophic fracture"],
         "Elastic region: temporary/reversible deformation. Plastic region: permanent/irreversible deformation beyond the yield point.")
    ]

    for hlc_title, hlc_ans, hlc_wrongs, hlc_expl in hookes_law_concepts:
        for st_hlc in [
            f"What is the CAPS definition and engineering significance of **'{hlc_title}'**?",
            f"In the mechanical behavior of materials, **'{hlc_title}'** refers to:",
            f"Which statement accurately explains **'{hlc_title}'**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Hooke's Law & Elastic Concepts", st_hlc, hlc_ans, hlc_wrongs, "Understanding", f"Explain {hlc_title}", hlc_expl)

    # Simple Hooke's Law Spring Calculations (Level 1 / Easy)
    # F = k * delta_x => k = F / delta_x => delta_x = F / k
    spring_k_easy = [
        (50.0, 0.10, "lab demonstration spring"), (100.0, 0.05, "soft suspension spring"),
        (200.0, 0.05, "door closer spring"), (250.0, 0.04, "kitchen scale spring"),
        (500.0, 0.02, "governor control spring"), (1000.0, 0.01, "valve return spring"),
        (2000.0, 0.005, "industrial buffer spring"), (100.0, 0.10, "measuring spring"),
        (200.0, 0.10, "dual-rate spring"), (500.0, 0.04, "trampoline edge spring"),
        (40.0, 0.15, "physics apparatus coil spring"), (80.0, 0.08, "balance pointer spring"),
        (120.0, 0.06, "chassis rebound spring"), (150.0, 0.05, "tensioner guide spring"),
        (300.0, 0.03, "clutch pedal spring"), (400.0, 0.02, "actuator return spring"),
        (600.0, 0.015, "brake caliper return spring"), (750.0, 0.02, "throttle body spring"),
        (800.0, 0.025, "poppet valve spring"), (1200.0, 0.008, "heavy die spring"),
        (1500.0, 0.006, "hydraulic damper spring"), (2500.0, 0.004, "locomotive coupler spring"),
        (3000.0, 0.003, "press stamping buffer spring"), (5000.0, 0.002, "die compression spring"),
        (150.0, 0.12, "garage door counterbalance spring")
    ]

    for k_val, dx_val, spr_name in spring_k_easy:
        if counts["easy"] >= 300:
            break
        f_spring = k_val * dx_val
        c_fsp = f"{f_spring:.1f} N"
        w_fsp = [
            f"{k_val / dx_val:.1f} N",
            f"{dx_val / k_val:.4f} N",
            f"{f_spring * 2:.1f} N",
            f"{f_spring / 2:.1f} N",
            f"{f_spring + 20:.1f} N",
            f"{k_val:.1f} N",
            f"{f_spring * 10:.1f} N"
        ]
        dx_cm = dx_val * 100.0
        q_text_fsp = f"A **{spr_name}** has a spring constant of k = {k_val:.0f} N·m⁻¹. Calculate the tensile pulling force (F) required to stretch the spring by Δx = {dx_cm:.1f} cm ({dx_val:.2f} m):"
        expl_fsp = f"Hooke's law: F = k × Δx = {k_val:.0f} N·m⁻¹ × {dx_val:.2f} m = {c_fsp}."
        add_q("easy", "Hooke's Law Basics", q_text_fsp, c_fsp, w_fsp, "Applying", f"Calculate spring force for {spr_name}", expl_fsp)

        # Finding spring constant k = F / dx
        if counts["easy"] < 300:
            c_ksp = f"{k_val:.0f} N·m⁻¹"
            w_ksp = [
                f"{f_spring * dx_val:.2f} N·m⁻¹",
                f"{dx_val / f_spring:.4f} N·m⁻¹",
                f"{k_val * 2:.0f} N·m⁻¹",
                f"{k_val / 2:.0f} N·m⁻¹",
                f"{k_val + 100:.0f} N·m⁻¹",
                f"{f_spring:.0f} N·m⁻¹",
                f"{k_val * 10:.0f} N·m⁻¹"
            ]
            q_text_ksp = f"A pulling force of F = {f_spring:.1f} N extends a **{spr_name}** by Δx = {dx_cm:.1f} cm ({dx_val:.2f} m). Determine the spring constant (k):"
            expl_ksp = f"Spring constant: k = F / Δx = {f_spring:.1f} N / {dx_val:.2f} m = {c_ksp}."
            add_q("easy", "Hooke's Law Basics", q_text_ksp, c_ksp, w_ksp, "Applying", f"Calculate spring constant for {spr_name}", expl_ksp)

        # Finding extension delta_x = F / k
        if counts["easy"] < 300:
            c_dx = f"{dx_cm:.1f} cm ({dx_val:.3f} m)"
            w_dx = [
                f"{dx_cm * 2:.1f} cm",
                f"{dx_cm / 2:.1f} cm",
                f"{f_spring * k_val:.1f} cm",
                f"{k_val / f_spring:.2f} cm",
                f"{dx_cm + 5.0:.1f} cm",
                f"{dx_cm * 10:.1f} cm",
                f"{dx_val:.4f} cm"
            ]
            q_text_dx = f"A tensile load of F = {f_spring:.1f} N is applied to a **{spr_name}** with spring constant k = {k_val:.0f} N·m⁻¹. Calculate the resulting extension (Δx):"
            expl_dx = f"Extension: Δx = F / k = {f_spring:.1f} N / {k_val:.0f} N·m⁻¹ = {dx_val:.3f} m = {dx_cm:.1f} cm."
            add_q("easy", "Hooke's Law Basics", q_text_dx, c_dx, w_dx, "Applying", f"Calculate spring extension for {spr_name}", expl_dx)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # Material Selection for Engineering, Property Comparisons, Composite Constituents, Corrosion Protection
    # =========================================================================

    engineering_applications = [
        ("Tungsten Carbide (WC)", "Tungsten carbide particles cemented in a cobalt metal matrix (Cermet)", "Tipping drill bits, mining cutting picks, and lathe machining tool inserts", "Exceptional hardness, extreme wear resistance, and retention of hardness at high cutting temperatures"),
        ("Carbon Fibre Reinforced Polymer (CFRP)", "Carbon fibres embedded in a cured epoxy resin matrix", "Aerospace components, Formula 1 racing monocoques, and high-performance bicycle frames", "Extremely high strength-to-weight ratio, high stiffness (modulus), and corrosion resistance"),
        ("Glass Fibre Reinforced Polymer (GRP / Fibreglass)", "Woven fine glass fibres embedded in a polyester or epoxy resin matrix", "Boat hulls, water storage tanks, surfboards, and wind turbine rotor blades", "High tensile strength, lightweight, chemical and water corrosion resistance, and low manufacturing cost"),
        ("Reinforced Concrete", "Steel rebar or mesh embedded within a hardened Portland cement concrete matrix", "High-rise building foundations, bridges, dams, and structural highway beams", "Combines the superior compressive strength of concrete with the high tensile strength and ductility of steel rebar"),
        ("Copper Metal (Cu)", "High-purity ductile non-ferrous metal", "Domestic electrical wiring, motor windings, and transformer coils", "Excellent electrical conductivity (second only to silver), high ductility for drawing into wires, and corrosion resistance"),
        ("Aluminium Alloy (e.g. Duralumin)", "Aluminium alloyed with copper, magnesium, and manganese", "Aircraft fuselage skins, automotive body panels, and window frames", "Low density (lightweight), good strength-to-weight ratio, and natural corrosion resistance via a self-healing passive Al₂O₃ oxide layer"),
        ("Stainless Steel", "Ferrous alloy containing iron with at least 10.5% chromium and nickel", "Surgical instruments, commercial kitchen equipment, chemical storage vessels, and cutlery", "Exceptional corrosion and stain resistance due to the spontaneous formation of a microscopic self-healing chromium oxide (Cr₂O₃) passive barrier layer"),
        ("Mild Steel (Low-carbon steel, ~0.2% C)", "Ferrous alloy of iron and small percentages of carbon", "Structural steel I-beams, car chassis frames, and steel sheet panels", "High tensile strength, good ductility and malleability, easily welded and machined, and relatively low cost"),
        ("High-Carbon Steel (~0.8% - 1.2% C)", "Ferrous alloy with higher carbon content", "Wood chisels, circular saw blades, files, and high-strength piano wire", "High hardness, high wear resistance, and ability to be hardened and tempered by heat treatment"),
        ("Cast Iron (~2% - 4% C)", "Ferrous alloy with high carbon and silicon content", "Engine cylinder blocks, heavy machine tool beds, brake discs, and manhole covers", "Excellent compressive strength, outstanding vibration-damping capacity, low melting point with high fluidity for casting, but brittle in tension"),
        ("Brass", "Non-ferrous alloy of copper and zinc (typically 60-70% Cu, 30-40% Zn)", "Plumbing valves, decorative door hardware, musical instruments, and low-friction marine fittings", "Good corrosion resistance, low acoustic damping, low friction, and attractive gold-like appearance"),
        ("Bronze", "Non-ferrous alloy of copper and tin (typically 88% Cu, 12% Sn)", "Heavy-duty rotating shaft bearings, ship propellers, and outdoor commemorative statues", "Higher strength and hardness than brass, exceptional resistance to seawater corrosion, and low metal-on-metal friction"),
        ("Polycarbonate (PC)", "Tough transparent thermoplastic polymer", "Safety glasses, bulletproof security shields, and motorcycle helmet visors", "Optical transparency combined with extraordinary impact toughness and resistance to shattering"),
        ("Polytetrafluoroethene (PTFE / Teflon)", "Fluorocarbon addition polymer with non-polar C-F bonds", "Non-stick frying pan surfaces, industrial chemical pipe gaskets, and plumber's thread seal tape", "Ultra-low coefficient of friction, high thermal resistance (up to 260 °C), and near-total chemical inertness"),
        ("Nylon (Polyamide)", "Condensation polymer with strong inter-chain hydrogen bonds", "Low-noise unlubricated mechanical gears, power tool casings, synthetic ropes, and fishing lines", "High tensile strength, excellent resistance to wear and abrasion, low coefficient of friction, and self-lubricating qualities")
    ]

    for mat_name, mat_comp, mat_use, mat_reason in engineering_applications:
        for q_st_ea in [
            f"Why is **{mat_name}** selected for use in **{mat_use}**?",
            f"An engineering designer chooses **{mat_name}** ({mat_comp}) for **{mat_use}**. What key property justifies this selection?",
            f"Which engineering property makes **{mat_name}** the ideal material for **{mat_use}**?"
        ]:
            if counts["medium"] >= 500:
                break
            c_ea = f"Because of its {mat_reason.lower()}."
            w_ea = [
                "Because it has an extremely low melting point and melts in warm water.",
                "Because it is brittle and shatters spontaneously under light loads.",
                "Because it conducts electricity exclusively when submerged in acid.",
                "Because it dissolves into air to release harmless carbon dioxide.",
                "Because it is an unrefined mineral ore with zero manufacturing cost.",
                "Because it corrodes rapidly to coat itself with heavy iron rust."
            ]
            expl_ea = f"{mat_name} ({mat_comp}) is chosen for {mat_use} because of its {mat_reason}."
            add_q("medium", "Material Selection in Engineering", q_st_ea, c_ea, w_ea, "Applying", f"Select material {mat_name}", expl_ea)

    # Composite Materials Constituents (Medium)
    composites_medium = [
        ("Reinforced Concrete", "Portland cement, sand, stone aggregates, and water (Concrete)", "Steel reinforcing bars (rebar) or steel wire mesh",
         "Concrete has high compressive strength but poor tensile strength; steel rebar provides exceptional tensile strength, preventing catastrophic tensile cracking under bending loads."),
        ("Fibreglass (Glass-Reinforced Plastic, GRP)", "Thermosetting polyester resin or epoxy polymer resin", "Woven or chopped fine glass fibres (E-glass)",
         "The polymer resin matrix binds and protects the fibres from environmental moisture; the glass fibres provide high tensile strength and stiffness."),
        ("Carbon Fibre Reinforced Polymer (CFRP)", "Epoxy polymer resin matrix", "High-strength woven carbon (graphite) fibres",
         "The epoxy matrix transfers shear stresses between fibres; the carbon fibres supply extraordinary tensile strength and rigidity at low density."),
        ("Plywood", "Phenolic or urea-formaldehyde resin adhesive matrix", "Thin wood veneers (plies) glued with grain directions rotated 90° in alternating layers",
         "Alternating wood grain directions equalize tensile and bending strength in both directions and prevent splitting along the natural grain."),
        ("Tungsten Carbide Cermet", "Cobalt (Co) metallic binder matrix (typically 6-10%)", "Hard tungsten carbide (WC) ceramic particles",
         "Tungsten carbide particles provide extreme hardness and abrasion resistance; the ductile cobalt metal matrix cushions the brittle particles and provides toughness.")
    ]

    for comp_name_m, mat_matrix, mat_reinforce, comp_expl_m in composites_medium:
        for q_st_cm in [
            f"Identify the **MATRIX** and the **REINFORCEMENT** constituents of the composite material **{comp_name_m}**:",
            f"In the engineered composite **{comp_name_m}**, what serves as the binder matrix and what provides reinforcement?",
            f"Which entry accurately identifies the constituent phases of **{comp_name_m}**?"
        ]:
            if counts["medium"] >= 500:
                break
            c_cm = f"Matrix: {mat_matrix}; Reinforcement: {mat_reinforce}."
            w_cm = [
                f"Matrix: {mat_reinforce}; Reinforcement: {mat_matrix} (inverted matrix and reinforcement roles).",
                f"Matrix: pure metallic zinc; Reinforcement: rubber latex.",
                f"Matrix: air pockets; Reinforcement: water ice crystals.",
                f"Matrix: sulfuric acid; Reinforcement: calcium carbonate powder.",
                f"Matrix: copper wire; Reinforcement: glass bubbles.",
                f"Matrix: polystyrene foam; Reinforcement: sand grains."
            ]
            expl_cm = f"{comp_name_m}: Matrix = {mat_matrix}; Reinforcement = {mat_reinforce}. {comp_expl_m}"
            add_q("medium", "Composite Constituents", q_st_cm, c_cm, w_cm, "Understanding", f"Identify constituents of {comp_name_m}", expl_cm)

    # Methods of Corrosion Protection (Medium)
    corrosion_protection_methods = [
        ("Sacrificial Anode (Cathodic Protection of ship hulls and underground steel pipelines)",
         "Blocks of a MORE REACTIVE metal with a more negative reduction potential (such as zinc, magnesium, or aluminium) are attached to the steel structure; the sacrificial anode oxidizes preferentially (corrodes away), donating electrons to the steel and forcing it to act as the protected cathode.",
         ["Blocks of a less reactive metal (like copper or gold) are attached to accelerate steel oxidation",
          "The steel structure is connected to the positive terminal of an external AC generator",
          "A thick layer of salt is packed around the pipeline to absorb moisture",
          "The steel structure is coated with pure carbon graphite powder",
          "The pipe is heated continuously to 500 °C to vaporize all water molecules",
          "The sacrificial block dissolves into oxygen gas to eliminate air around the ship"],
         "Sacrificial protection: More reactive metal (Mg, Zn, Al) has more negative E°, oxidizes preferentially, and protects steel cathode."),

        ("Galvanizing of Steel Sheets",
         "Steel is dipped into molten ZINC; zinc forms a physical barrier against air and water, and even if the coating is scratched or chipped, zinc acts as a sacrificial anode (E°(Zn) = -0.76 V vs E°(Fe) = -0.44 V) and oxidizes in preference to the exposed iron.",
         ["Steel is coated with tin which oxidizes in preference to iron when scratched",
          "Zinc melts into the steel core to convert it into a brass alloy",
          "The zinc layer absorbs oxygen gas and turns it into water",
          "Zinc creates an electrical short circuit that eliminates all potential differences",
          "The coating only protects the steel if the zinc is completely unbroken",
          "Zinc reacts with iron to produce radioactive rust particles"],
         "Galvanizing: Zinc acts as physical barrier AND sacrificial anode. Because E°(Zn) < E°(Fe), zinc protects iron even when scratched."),

        ("Passivation of Stainless Steel by Chromium Oxide (Cr2O3)",
         "Chromium in the alloy (≥ 10.5% Cr) reacts instantly with atmospheric oxygen to form an ultra-thin, continuous, self-healing, non-porous passive layer of chromium(III) oxide (Cr₂O₃) that blocks oxygen and moisture from reaching the iron atoms underneath.",
         ["Chromium reacts with iron to eliminate all iron atoms from the surface",
          "Chromium forms a liquid coating that washes away dirt and salt",
          "Chromium converts the steel into an electrical insulator",
          "Chromium absorbs water into its crystal lattice without reacting",
          "Chromium causes the steel to melt at room temperature",
          "Chromium releases hydrogen gas continuously to displace oxygen"],
         "Stainless steel passivates via a microscopic, self-healing Cr₂O₃ oxide film formed by chromium reacting with oxygen."),

        ("Barrier Protection: Painting, Oiling, Powder Coating",
         "Forms an unbroken physical barrier that completely excludes atmospheric oxygen (O₂) and water (H₂O) from coming into direct physical contact with the metal surface; however, if the barrier is scratched, rusting begins immediately at the exposed site.",
         ["Provides cathodic protection by donating electrons to the steel",
          "Converts iron atoms into an aluminium alloy at room temperature",
          "Acts as a sacrificial anode that corrodes preferentially",
          "Eliminates electrical resistance in the steel structure",
          "Generates an impressed direct current that drives reverse electrolysis",
          "Permanently prevents iron from undergoing oxidation even if the paint is scratched"],
         "Barrier protection (paint, grease, powder coat) blocks air and moisture mechanically, but offers zero protection once scratched.")
    ]

    for cp_name, cp_ans, cp_wrongs, cp_expl in corrosion_protection_methods:
        for st_cp in [
            "In Technical Sciences materials chemistry, explain the mechanism of: **{}**",
            "How does **{}** prevent the corrosion of iron and steel?",
            "Which evaluation accurately explains the operational principle of: **{}**"
        ]:
            if counts["medium"] >= 500:
                break
            add_q("medium", "Corrosion Prevention", st_cp.format(cp_name), cp_ans, cp_wrongs, "Understanding", f"Explain {cp_name}", cp_expl)

    # Property Comparisons (Hardness, Toughness, Ductility) (Medium)
    property_comparisons_medium = [
        ("Diamond vs Mild Steel vs Polyethene", "Hardness: Diamond > Mild Steel > Polyethene",
         ["Hardness: Polyethene > Mild Steel > Diamond", "Hardness: Mild Steel > Diamond > Polyethene", "All three have identical hardness", "Polyethene is the hardest because it is a polymer", "Mild Steel is harder than diamond under tension", "Diamond has zero hardness on the Mohs scale"],
         "Diamond (giant covalent network) is the hardest known natural substance (Mohs 10) > Mild steel (metallic lattice) > Polyethene (soft polymer)."),

        ("Copper vs Glass vs Cast Iron in terms of Brittleness", "Brittleness: Glass > Cast Iron > Copper",
         ["Brittleness: Copper > Cast Iron > Glass", "Brittleness: Copper > Glass > Cast Iron", "All three materials are equally brittle", "Copper is the most brittle because it forms wires", "Glass is tough and ductile while copper is brittle", "Cast iron has zero brittleness"],
         "Glass (amorphous ceramic) is extremely brittle and shatters without plastic strain > Cast iron (brittle due to high carbon flakes) > Copper (highly ductile and malleable metal)."),

        ("Mild Steel vs Concrete vs Timber in Tensile Strength", "Tensile Strength: Mild Steel > Timber > Concrete",
         ["Tensile Strength: Concrete > Mild Steel > Timber", "Tensile Strength: Concrete > Timber > Mild Steel", "Concrete has the highest tensile strength of all structural materials", "Timber has higher tensile strength than mild steel", "All three materials have identical tensile strength", "Mild steel has zero tensile strength under pulling loads"],
         "Mild steel has very high tensile strength (~400 MPa) > Timber along grain (~40-100 MPa) > Plain concrete (very weak in tension, ~2-5 MPa, requires steel rebar reinforcement).")
    ]

    for p_comp_name, p_comp_order, p_comp_wrongs, p_comp_expl in property_comparisons_medium:
        for st_pc in [
            f"Rank the materials in order of decreasing property: **{p_comp_name}**",
            f"Which sequence correctly ranks the materials in: **{p_comp_name}**?",
            f"In Grade 12 Technical Sciences, compare: **{p_comp_name}**"
        ]:
            if counts["medium"] >= 500:
                break
            add_q("medium", "Property Comparisons", st_pc, p_comp_order, p_comp_wrongs, "Understanding", f"Rank {p_comp_name}", p_comp_expl)

    # Mohs Hardness Scale (Medium)
    mohs_minerals = [
        ("Diamond", 10, "hardest known natural substance; scratches all other materials; used for drill cores and glass cutters"),
        ("Corundum (Sapphire/Ruby, Al2O3)", 9, "extremely hard mineral; used as abrasive grinding wheels and sandpaper"),
        ("Topaz", 8, "hard gemstone silicate mineral"),
        ("Quartz (SiO2)", 7, "common mineral in granite and sand; scratches normal window glass (hardness ~5.5)"),
        ("Orthoclase Feldspar", 6, "common rock-forming tectosilicate mineral"),
        ("Apatite", 5, "mineral found in tooth enamel and bone phosphate"),
        ("Fluorite (CaF2)", 4, "halide mineral that cleaves easily into octahedrons"),
        ("Calcite (CaCO3)", 3, "limestone and marble mineral; scratched easily by a copper coin (hardness ~3.5)"),
        ("Gypsum (CaSO4·2H2O)", 2, "soft sulfate mineral; scratched easily by a fingernail (hardness ~2.5)"),
        ("Talc", 1, "softest known mineral on the Mohs scale; feels greasy and powders easily")
    ]

    for min_name, mohs_val, min_desc in mohs_minerals:
        if counts["medium"] >= 500:
            break
        q_mohs = f"What is the **MOHS HARDNESS RATING** of the mineral **{min_name}** ({min_desc})?"
        c_mohs = f"{mohs_val} on the Mohs hardness scale"
        w_mohs = [
            f"{mohs_val + 2} on the Mohs hardness scale",
            f"{mohs_val - 2 if mohs_val > 2 else 5} on the Mohs hardness scale",
            f"{11 - mohs_val} on the Mohs hardness scale",
            f"{mohs_val * 2} on the Mohs hardness scale",
            f"0 on the Mohs hardness scale",
            f"{mohs_val + 5} on the Mohs hardness scale",
            f"{mohs_val - 1 if mohs_val > 1 else 10} on the Mohs hardness scale"
        ]
        expl_mohs = f"{min_name} has a Mohs hardness of {mohs_val} ({min_desc})."
        add_q("medium", "Mohs Hardness Scale", q_mohs, c_mohs, w_mohs, "Remembering", f"State Mohs hardness of {min_name}", expl_mohs)

    # Direct Stress Calculations: sigma = F / A, F = sigma * A, A = F / sigma (Medium)
    forces_stress = [
        400.0, 600.0, 800.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0,
        5000.0, 7500.0, 10000.0, 15000.0, 20000.0, 25000.0, 40000.0, 50000.0, 100000.0
    ] # N (18 values)
    areas_stress = [
        0.00001, 0.00002, 0.000025, 0.00004, 0.00005, 0.00008, 0.00010,
        0.00015, 0.00020, 0.00025, 0.00040, 0.00050, 0.00080, 0.00100
    ] # m² (14 values)

    for f_load in forces_stress:
        for a_area in areas_stress:
            if counts["medium"] >= 500:
                break
            stress_pa = f_load / a_area
            stress_mpa = stress_pa / 1e6
            area_mm2 = a_area * 1e6

            # 1. Calculate Stress: sigma = F / A
            corr_stress = f"{stress_mpa:.2f} MPa ({stress_pa:.1e} Pa)"
            wrs_stress = [
                f"{f_load * a_area:.2f} MPa (multiplied force by area instead of dividing)",
                f"{stress_mpa * 1000:.2f} MPa (forgot to convert Pa to MPa)",
                f"{stress_mpa * 2:.2f} MPa",
                f"{stress_mpa / 2:.2f} MPa",
                f"{a_area / f_load:.4e} MPa (inverted: A / F)",
                f"{stress_mpa + 50.0:.2f} MPa",
                f"{f_load:.1f} MPa"
            ]
            q_text_str = (f"A tensile test specimen with a cross-sectional area of A = {area_mm2:.1f} mm² ({a_area:.5f} m²) "
                          f"is subjected to a tensile pulling force of F = {f_load:.0f} N. Calculate the mechanical STRESS (σ) in the specimen:")
            expl_str = f"Stress formula: σ = F / A = {f_load:.0f} N / {a_area:.5f} m² = {stress_pa:.0f} Pa = {corr_stress}."
            add_q("medium", "Mechanical Stress Calculations", q_text_str, corr_stress, wrs_stress, "Applying", "Calculate mechanical stress from force and area", expl_str)

            # 2. Calculate Maximum Force: F = sigma * A
            if counts["medium"] < 500:
                corr_f = f"{f_load:.0f} N"
                wrs_f = [
                    f"{stress_mpa / a_area:.1f} N",
                    f"{f_load * 2:.0f} N",
                    f"{f_load / 2:.0f} N",
                    f"{f_load * 10:.0f} N",
                    f"{f_load / 10:.0f} N",
                    f"{stress_pa:.0f} N (confused Pascals with Newtons)",
                    f"{f_load + 500:.0f} N"
                ]
                q_text_f = (f"A structural tie rod has a cross-sectional area of A = {area_mm2:.1f} mm² ({a_area:.5f} m²). "
                            f"If the allowable design tensile stress is σ = {stress_mpa:.2f} MPa ({stress_pa:.1e} Pa), calculate the maximum pulling force (F) the rod can support:")
                expl_f = f"Force formula: F = σ × A = {stress_pa:.0f} Pa × {a_area:.5f} m² = {corr_f}."
                add_q("medium", "Mechanical Stress Calculations", q_text_f, corr_f, wrs_f, "Applying", "Calculate allowable force from stress and area", expl_f)

            # 3. Calculate Required Area: A = F / sigma
            if counts["medium"] < 500:
                corr_a = f"{area_mm2:.1f} mm² ({a_area:.5f} m²)"
                wrs_a = [
                    f"{area_mm2 * 2:.1f} mm²",
                    f"{area_mm2 / 2:.1f} mm²",
                    f"{f_load * stress_mpa:.1f} mm²",
                    f"{stress_mpa / f_load:.4f} mm²",
                    f"{area_mm2 * 10:.1f} mm²",
                    f"{area_mm2 + 15.0:.1f} mm²",
                    f"{a_area:.2e} mm² (forgot unit conversion to mm²)"
                ]
                q_text_a = (f"An engineering strut must carry a tensile load of F = {f_load:.0f} N without the mechanical stress exceeding "
                            f"σ = {stress_mpa:.2f} MPa ({stress_pa:.1e} Pa). Calculate the minimum required cross-sectional area (A):")
                expl_a = f"Area formula: A = F / σ = {f_load:.0f} N / {stress_pa:.0f} Pa = {a_area:.5f} m² = {corr_a}."
                add_q("medium", "Mechanical Stress Calculations", q_text_a, corr_a, wrs_a, "Applying", "Calculate required area from force and stress", expl_a)

    # Direct Strain Calculations: epsilon = delta_L / L, delta_L = epsilon * L (Medium)
    lengths_strain = [
        0.40, 0.60, 0.80, 1.0, 1.20, 1.50, 1.80, 2.0, 2.50, 3.0, 4.0, 5.0
    ] # m (12 values)
    extensions_strain = [
        0.0004, 0.0006, 0.0008, 0.0010, 0.0012, 0.0015, 0.0020, 0.0025, 0.0030, 0.0040, 0.0050, 0.0080, 0.0100
    ] # m (13 values)

    for l_orig in lengths_strain:
        for d_ext in extensions_strain:
            if counts["medium"] >= 500:
                break
            strain_val = d_ext / l_orig
            strain_pct = strain_val * 100.0
            ext_mm = d_ext * 1000.0

            # 1. Calculate Strain: epsilon = delta_L / L
            corr_strain = f"{strain_val:.4f} ({strain_pct:.2f}%)"
            wrs_strain = [
                f"{d_ext * l_orig:.4f} (multiplied extension by length)",
                f"{l_orig / d_ext:.2f} (inverted: L / ΔL)",
                f"{strain_val * 2:.4f}",
                f"{strain_val / 2:.4f}",
                f"{ext_mm:.1f} (confused extension in mm with strain)",
                f"{strain_val * 10:.4f}",
                f"{strain_val + 0.05:.4f}"
            ]
            q_text_stn = (f"A metallic cable with an original length of L = {l_orig:.2f} m stretches by an extension of ΔL = {ext_mm:.1f} mm ({d_ext:.4f} m) "
                          f"under an applied tensile load. Calculate the dimensionless mechanical STRAIN (ε):")
            expl_stn = f"Strain formula: ε = ΔL / L = {d_ext:.4f} m / {l_orig:.2f} m = {corr_strain} (strain is a dimensionless ratio)."
            add_q("medium", "Mechanical Strain Calculations", q_text_stn, corr_strain, wrs_strain, "Applying", "Calculate mechanical strain from extension and length", expl_stn)

            # 2. Calculate Extension: delta_L = epsilon * L
            if counts["medium"] < 500:
                corr_ext = f"{ext_mm:.1f} mm ({d_ext:.4f} m)"
                wrs_ext = [
                    f"{ext_mm * 2:.1f} mm",
                    f"{ext_mm / 2:.1f} mm",
                    f"{strain_val / l_orig:.4f} mm",
                    f"{l_orig / strain_val:.1f} mm",
                    f"{ext_mm * 10:.1f} mm",
                    f"{ext_mm + 2.0:.1f} mm",
                    f"{d_ext:.5f} mm"
                ]
                q_text_ext = (f"A structural cable of original length L = {l_orig:.2f} m experiences an axial tensile strain of "
                              f"ε = {strain_val:.4f} ({strain_pct:.2f}%). Calculate the resulting extension (ΔL) in mm:")
                expl_ext = f"Extension formula: ΔL = ε × L = {strain_val:.4f} × {l_orig:.2f} m = {d_ext:.4f} m = {corr_ext}."
                add_q("medium", "Mechanical Strain Calculations", q_text_ext, corr_ext, wrs_ext, "Applying", "Calculate elongation from strain and length", expl_ext)

    # Spring Combinations (Series and Parallel) (Medium)
    spring_combinations = [
        (100.0, 100.0, "two identical soft springs"),
        (200.0, 200.0, "two identical medium springs"),
        (500.0, 500.0, "two identical stiff springs"),
        (1000.0, 1000.0, "two identical heavy-duty springs"),
        (200.0, 300.0, "two different suspension springs"),
        (300.0, 600.0, "dual-stage buffer springs"),
        (400.0, 600.0, "chassis balance springs"),
        (500.0, 1000.0, "valve spring assembly")
    ]

    for k1, k2, spr_pair_desc in spring_combinations:
        # Parallel: k_eq = k1 + k2
        if counts["medium"] < 500:
            k_par = k1 + k2
            c_par = f"{k_par:.0f} N·m⁻¹"
            w_par = [
                f"{(k1 * k2) / (k1 + k2):.1f} N·m⁻¹ (calculated series equivalent instead of parallel)",
                f"{k1 * k2:.0f} N·m⁻¹",
                f"{k_par * 2:.0f} N·m⁻¹",
                f"{k_par / 2:.0f} N·m⁻¹",
                f"{abs(k1 - k2):.0f} N·m⁻¹",
                f"{k_par + 100:.0f} N·m⁻¹",
                f"{k1:.0f} N·m⁻¹"
            ]
            q_par = (f"Calculate the equivalent spring constant (k_eq) when {spr_pair_desc} with stiffness constants "
                     f"k₁ = {k1:.0f} N·m⁻¹ and k₂ = {k2:.0f} N·m⁻¹ are connected in **PARALLEL**:")
            expl_par = f"In parallel, springs share the load and their stiffnesses add directly: k_eq = k₁ + k₂ = {k1:.0f} + {k2:.0f} = {c_par}."
            add_q("medium", "Spring Combinations", q_par, c_par, w_par, "Applying", f"Calculate parallel spring constant for {spr_pair_desc}", expl_par)

        # Series: 1/k_eq = 1/k1 + 1/k2 => k_eq = (k1 * k2) / (k1 + k2)
        if counts["medium"] < 500:
            k_ser = (k1 * k2) / (k1 + k2)
            c_ser = f"{k_ser:.1f} N·m⁻¹"
            w_ser = [
                f"{k1 + k2:.0f} N·m⁻¹ (calculated parallel equivalent instead of series)",
                f"{k1 * k2:.0f} N·m⁻¹",
                f"{k_ser * 2:.1f} N·m⁻¹",
                f"{k_ser / 2:.1f} N·m⁻¹",
                f"{k_ser + 50:.1f} N·m⁻¹",
                f"{1 / k_ser:.4f} N·m⁻¹",
                f"{k1:.1f} N·m⁻¹"
            ]
            q_ser = (f"Calculate the equivalent spring constant (k_eq) when {spr_pair_desc} with stiffness constants "
                     f"k₁ = {k1:.0f} N·m⁻¹ and k₂ = {k2:.0f} N·m⁻¹ are connected in **SERIES** (end-to-end):")
            expl_ser = f"In series, compliance adds: 1/k_eq = 1/k₁ + 1/k₂ => k_eq = (k₁ × k₂) / (k₁ + k₂) = ({k1:.0f} × {k2:.0f}) / ({k1:.0f} + {k2:.0f}) = {c_ser}."
            add_q("medium", "Spring Combinations", q_ser, c_ser, w_ser, "Applying", f"Calculate series spring constant for {spr_pair_desc}", expl_ser)

    # Additional Material Selection Scenarios (Medium)
    more_mat_selections = [
        ("High-voltage overhead electrical transmission cable", "Aluminium Conductor Steel-Reinforced (ACSR: outer aluminium strands with inner steel core)", "Aluminium provides low density and high electrical conductivity; the steel core provides exceptional tensile strength to span pylons without sagging"),
        ("Spark plug electrical insulator in internal combustion engines", "High-purity Alumina Ceramic (Al2O3)", "Extreme dielectric electrical insulation, high compressive strength, and resistance to thermal shock up to 1000 °C"),
        ("Bulletproof transparent security shield", "Polycarbonate laminated with Polyurethane and Glass", "Polycarbonate provides unmatched impact toughness and ductility to absorb bullet kinetic energy without shattering"),
        ("Aerospace jet engine turbine blades", "Nickel-based Superalloy (e.g. Inconel) single crystal", "Maintains high mechanical strength, resistance to thermal creep, and oxidation resistance at operating temperatures exceeding 1100 °C"),
        ("High-pressure domestic water geyser heating element", "Nichrome wire enclosed in a copper or stainless steel tube with MgO insulation", "Nichrome has high electrical resistivity and oxidizes to form an adherent protective oxide layer that resists burnout"),
        ("Chemical laboratory sink and acid drainage benchtop", "Epoxy resin composite or ceramic vitrified stoneware", "Near-total chemical inertness to concentrated mineral acids, organic solvents, and thermal shock from boiling chemicals"),
        ("High-speed CNC lathe cutting tool bit", "Tungsten Carbide (WC) cemented in Cobalt", "Maintains hot hardness above 800 °C, superior wear resistance against abrasive metal chips"),
        ("Automotive battery casing", "Polypropylene (PP) thermoplastic", "High chemical resistance to 35% battery sulfuric acid, good impact toughness, and easily injection-moulded with living hinges")
    ]

    for app_item, mat_sol, rsn_sol in more_mat_selections:
        for st_mms in [
            f"What material is technically specified for an **{app_item}**, and why?",
            f"In mechanical and electrical engineering, which material is selected for an **{app_item}**?",
            f"Identify the justified material selection for an **{app_item}**:"
        ]:
            if counts["medium"] >= 500:
                break
            c_mms = f"Specified material: {mat_sol} ({rsn_sol})."
            w_mms = [
                "Specified material: Pure unreinforced concrete paste.",
                "Specified material: Soft lead foil bonded with natural rubber latex.",
                "Specified material: Cast iron plates joined by tin solder.",
                "Specified material: Low-density polyethene plastic wrap.",
                "Specified material: Natural timber poles soaked in seawater.",
                "Specified material: Transparent polystyrene coffee cup foam."
            ]
            add_q("medium", "Material Specifications", st_mms, c_mms, w_mms, "Applying", f"Specify material for {app_item}", c_mms)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Multi-Factor Material Selection, Electrochemical Rusting Mechanism, Sacrificial Anode Lifespan
    # =========================================================================

    # 1. Electrochemical Mechanism of Rusting (Hard)
    rusting_mechanism_hard = [
        ("The Complete Electrochemical Cell Mechanism of Rusting (Anodic and Cathodic Reactions)",
         "At the ANODE site (stressed metal surface): Fe(s) → Fe²⁺(aq) + 2e⁻ (iron metal oxidizes and dissolves). Electrons travel through the iron metal to the CATHODE site (water droplet edge with high oxygen concentration): O₂(g) + 2H₂O(l) + 4e⁻ → 4OH⁻(aq) (oxygen reduction). The Fe²⁺ and OH⁻ ions diffuse into the water drop and precipitate iron(II) hydroxide: Fe²⁺ + 2OH⁻ → Fe(OH)₂, which is further oxidized by oxygen to hydrated iron(III) oxide (rust): 4Fe(OH)₂ + O₂ + 2xH₂O → 2Fe₂O₃·(x+4)H₂O.",
         ["Iron reduces at the cathode while oxygen gas oxidizes at the anode to form liquid ozone",
          "Iron atoms combine directly with dry nitrogen gas without any electron transfer",
          "Water molecules dissociate into hydrogen gas and molten iron sulfide precipitate",
          "The anodic reaction produces chlorine gas while the cathodic reaction dissolves iron",
          "The process is an endothermic nuclear reaction catalyzed by airborne dust particles",
          "Iron metal reacts with sodium ions in seawater to precipitate molten sodium hydroxide"],
         "Rusting is an electrochemical cell: Anode: Fe -> Fe²⁺ + 2e⁻. Cathode: O₂ + 2H₂O + 4e⁻ -> 4OH⁻. Fe²⁺ + 2OH⁻ -> Fe(OH)₂ -> further oxidation yields Fe₂O₃·xH₂O."),

        ("Why Tin-Plated Steel Cans (Tin Cans) Corrode RAPIDLY Once Scratched, unlike Galvanized Zinc Cans",
         "Tin has a MORE POSITIVE reduction potential (E°(Sn²⁺/Sn) = -0.14 V) than iron (E°(Fe²⁺/Fe) = -0.44 V); therefore, tin is LESS REACTIVE than iron. Once the tin layer is scratched, an electrochemical cell forms where iron becomes the ANODE and tin becomes the CATHODE, causing the exposed iron to corrode even FASTER than unplated iron (galvanic corrosion). In contrast, zinc is more reactive than iron and acts as a sacrificial anode.",
         ["Tin is more reactive than iron and dissolves into the canned food to poison it",
          "Tin forms an acid when exposed to oxygen that dissolves iron chemically",
          "Tin reacts with air to produce hydrogen gas bubbles that explode the can",
          "The scratch allows tin to convert into an electrical insulator",
          "Tin only corrodes when submerged in concentrated sulfuric acid",
          "Tin-plated cans never corrode even when severely scratched or dented"],
         "E°(Sn) = -0.14 V > E°(Fe) = -0.44 V. Tin is less reactive than iron: when scratched, iron oxidizes preferentially to tin, causing rapid localized galvanic corrosion."),

        ("Impressed Current Cathodic Protection (ICCP) vs Galvanic Sacrificial Anodes",
         "ICCP uses an external direct current (DC) power source connected to inert non-sacrificial anodes (such as mixed metal oxide titanium) to continuously pump electrons into the protected steel structure, making it the cathode regardless of soil or water resistivity; sacrificial anode systems rely solely on the natural potential difference between dissimilar metals and require no external power, but have limited driving voltage and finite anode lifespan.",
         ["ICCP converts alternating current into sound waves to repel water molecules from steel",
          "Sacrificial anodes require high-voltage external power generators to function",
          "ICCP operates exclusively on alternating current while sacrificial anodes use direct current",
          "Sacrificial anodes dissolve faster when connected to external DC power supplies",
          "ICCP creates a protective paint barrier through continuous electrodeposition of plastic",
          "Both systems require replacing massive zinc anodes every twenty-four hours"],
         "ICCP uses an external DC power supply with inert anodes to force steel to be the cathode; sacrificial systems use galvanic potential difference without external power.")
    ]

    for rm_h_title, rm_h_ans, rm_h_wrongs, rm_h_expl in rusting_mechanism_hard:
        for st_rmh in [
            "Critically analyze the electrochemical principles of: **{}**",
            "In advanced Grade 12 Technical Sciences metallurgy, evaluate: **{}**",
            "Which comprehensive scientific deduction accurately explains: **{}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Electrochemical Corrosion In-Depth", st_rmh.format(rm_h_title), rm_h_ans, rm_h_wrongs, "Evaluating", f"Analyze {rm_h_title}", rm_h_expl)

    # 2. Multi-Factor Engineering Material Selection (Hard)
    selection_scenarios = [
        ("Subsea Natural Gas Pipeline across a deep marine trench (High pressure, saline water, continuous movement)",
         "High-strength low-alloy (HSLA) steel pipe coated externally with three-layer polypropylene (3LPP) and protected by continuous sacrificial zinc anode bracelets or ICCP",
         ["Pure unreinforced PVC plastic pipes because plastics do not rust in seawater",
          "Cast iron pipes joined by rubber gaskets with zero external coating",
          "Solid pure copper piping because copper is highly malleable and soft",
          "Uncoated mild steel pipes because deep ocean water contains zero oxygen",
          "Pure glass tubing because ceramics have infinite tensile flexibility",
          "Aluminium foil wrapped around bamboo canes with tar adhesive"],
         "Marine subsea pipelines require high tensile strength (HSLA steel) to withstand internal gas pressure, heavy plastic coating (3LPP) against seawater, and sacrificial zinc bracelets for cathodic protection."),

        ("Automotive Disc Brake Rotor (Repeated thermal cycling up to 700 °C, severe abrasive friction, compressive clamping forces)",
         "Grey Cast Iron (or carbon-ceramic composite for racing applications), because grey cast iron possesses high thermal conductivity, exceptional resistance to thermal fatigue, high damping capacity to suppress brake squeal, and graphite flakes that provide self-lubrication against seizing",
         ["Polytetrafluoroethene (Teflon) because it has the lowest coefficient of friction",
          "Pure copper metal because copper conducts heat better than cast iron",
          "Thermoplastic polyethene because plastic does not rust when wet",
          "Pure lead metal because lead is dense and absorbs vibrations easily",
          "Glass fibre reinforced plastic because fiberglass is lightweight",
          "Mild steel sheet metal because thin sheets cool down quickly"],
         "Brake rotors require high thermal conductivity, thermal shock resistance, and vibration damping -> Grey cast iron (graphite flakes damp vibrations and dissipate friction heat)."),

        ("Hypodermic Needle for medical injections (Extremely sharp hollow point, rigid under axial compression, sterile, corrosion resistant)",
         "Austenitic Stainless Steel (Grade 304 or 316), because it offers high tensile strength and stiffness to prevent bending during insertion, excellent ductility for cold-drawing into ultra-thin hollow cannula tubes, and outstanding corrosion resistance to medical fluids",
         ["Cast iron because cast iron is cheap and easy to pour into needle moulds",
          "Pure gold because gold is non-reactive and hypoallergenic",
          "Tungsten carbide because needles must be the hardest material possible",
          "Low-density polyethene because flexible plastic needles don't hurt patients",
          "Pure zinc metal because zinc acts as an antiseptic sacrificial anode",
          "Unreinforced concrete because ceramic materials are sterile"],
         "Hypodermic needles require cold-drawing into micro-tubes, stiffness, and corrosion resistance -> Grade 304/316 Stainless Steel."),

        ("Helicopter Main Rotor Blade (Extreme cyclic fatigue bending stresses, high centrifugal tensile loads, airborne sand erosion)",
         "Composite construction of carbon fibre and glass fibre reinforced epoxy with a titanium or nickel leading-edge erosion shield",
         ["Pure unreinforced mild steel because steel is ductile and easy to weld",
          "Cast bronze because bronze has high density to maintain rotational inertia",
          "Solid unreinforced acrylic (Perspex) because transparency allows inspection",
          "Unvulcanized natural rubber because rubber bends without breaking",
          "Low-carbon structural iron because iron is the cheapest material available",
          "Ceramic porcelain tiles bonded together with household wood glue"],
         "Rotor blades require superior fatigue resistance, high strength-to-weight ratio (CFRP/GRP), and erosion-resistant titanium leading edges.")
    ]

    for sel_title, sel_ans, sel_wrongs, sel_expl in selection_scenarios:
        for st_sel in [
            "Select and justify the optimal engineering material for: **{}**",
            "In engineering materials design, evaluate the specification for: **{}**",
            "Which material specification provides the verified technical solution for: **{}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Advanced Material Selection", st_sel.format(sel_title), sel_ans, sel_wrongs, "Evaluating", f"Specify material for {sel_title}", sel_expl)

    # 3. Quantitative Corrosion Rate & Sacrificial Anode Lifespan Calculations (Hard)
    # Faraday's law of corrosion: m = (I_corr * t * M) / (z * F)
    # Lifespan: t = (m * z * F) / (I_corr * M)
    anode_lifespans = [
        ("Zinc sacrificial anode (Zn → Zn²⁺ + 2e⁻, M = 65.4 g·mol⁻¹, z = 2)", 65.4, 2, 5.0, 0.10, "ship hull protection in coastal waters"),
        ("Zinc sacrificial anode (Zn → Zn²⁺ + 2e⁻, M = 65.4 g·mol⁻¹, z = 2)", 65.4, 2, 10.0, 0.20, "offshore oil platform jacket leg"),
        ("Zinc sacrificial anode (Zn → Zn²⁺ + 2e⁻, M = 65.4 g·mol⁻¹, z = 2)", 65.4, 2, 25.0, 0.25, "harbor sheet piling protection"),
        ("Magnesium sacrificial anode (Mg → Mg²⁺ + 2e⁻, M = 24.3 g·mol⁻¹, z = 2)", 24.3, 2, 5.0, 0.05, "underground cross-country steel gas pipeline"),
        ("Magnesium sacrificial anode (Mg → Mg²⁺ + 2e⁻, M = 24.3 g·mol⁻¹, z = 2)", 24.3, 2, 10.0, 0.10, "domestic domestic hot water geyser tank"),
        ("Aluminium-zinc alloy anode (Al → Al³⁺ + 3e⁻, M = 27.0 g·mol⁻¹, z = 3)", 27.0, 3, 10.0, 0.15, "marine jetty pile cathodic protection"),
        ("Aluminium-zinc alloy anode (Al → Al³⁺ + 3e⁻, M = 27.0 g·mol⁻¹, z = 3)", 27.0, 3, 20.0, 0.30, "deep-water subsea pipeline protection")
    ]

    for anode_type, mol_mass_a, z_a, mass_kg, curr_amp, app_desc_a in anode_lifespans:
        if counts["hard"] >= 200:
            break
        mass_g = mass_kg * 1000.0
        # t = (m * z * F) / (I * M)
        time_seconds = (mass_g * z_a * 96500.0) / (curr_amp * mol_mass_a)
        time_days = time_seconds / (3600.0 * 24.0)
        time_years = time_days / 365.25

        c_life = f"{time_years:.2f} years ({time_days:.0f} days)"
        w_life = [
            f"{time_years * z_a:.2f} years (forgot electron valence factor z = {z_a})",
            f"{time_years / z_a:.2f} years",
            f"{time_years * 2:.2f} years",
            f"{time_years / 2:.2f} years",
            f"{time_days:.2f} years (confused days with years)",
            f"{time_years + 5.0:.2f} years",
            f"{time_years * 10:.2f} years"
        ]
        q_text_life = (f"A **{mass_kg:.1f} kg {anode_type}** is bolted to a steel structure for **{app_desc_a}**. If the average galvanic "
                       f"corrosion current flowing from the sacrificial anode is I = {curr_amp:.2f} A, calculate the expected operating LIFESPAN "
                       f"(time until complete consumption) of the sacrificial anode: (F = 96 500 C·mol⁻¹):")
        expl_life = (f"1. Total charge stored: Q = (m / M) × z × F = ({mass_g:.0f} g / {mol_mass_a:.1f} g·mol⁻¹) × {z_a} × 96 500 C·mol⁻¹ = {((mass_g/mol_mass_a)*z_a*96500):.0f} C. "
                     f"2. Time in seconds: t = Q / I = Q / {curr_amp:.2f} A = {time_seconds:.0f} s. "
                     f"3. Time in years: t = {time_seconds:.0f} / (3600 × 24 × 365.25) = {c_life}.")
        add_q("hard", "Sacrificial Anode Lifespan Calculations", q_text_life, c_life, w_life, "Evaluating", f"Calculate anode lifespan for {anode_type.split()[0]}", expl_life)

    # 4. Quantitative Iron Rusting Mass Loss Calculations (Hard)
    # m_iron = (I_corr * t * M) / (z * F), Fe -> Fe2+ + 2e- (M = 55.8 g/mol, z = 2)
    iron_corrosion_scenarios = [
        (0.05, 30, "uncoated steel pipe in moist acidic clay soil"),
        (0.10, 60, "steel piling in stagnant tidal harbor water"),
        (0.20, 90, "unprotected marine steel jetty in coastal surf"),
        (0.50, 180, "industrial steel tank holding saline wastewater"),
        (1.00, 365, "severely corroding bridge girder exposed to de-icing road salts"),
        (0.02, 60, "steel reinforcement in cracked marine concrete"),
        (0.08, 120, "underground fuel storage tank with damaged bitumen coating")
    ]

    for i_corr_val, days_exp, env_desc in iron_corrosion_scenarios:
        if counts["hard"] >= 200:
            break
        t_sec_corr = days_exp * 24.0 * 3600.0
        q_corr_tot = i_corr_val * t_sec_corr
        moles_fe = q_corr_tot / (2.0 * 96500.0)
        mass_fe_lost = moles_fe * 55.8
        corr_mfe = f"{mass_fe_lost:.2f} g"
        wrs_mfe = [
            f"{mass_fe_lost * 2:.2f} g (forgot valence z = 2)",
            f"{mass_fe_lost / 2:.2f} g",
            f"{q_corr_tot:.1f} g (confused Coulombs with grams)",
            f"{mass_fe_lost * 10:.2f} g",
            f"{mass_fe_lost + 50.0:.2f} g",
            f"{mass_fe_lost * 1.5:.2f} g",
            f"{mass_fe_lost / 4:.2f} g"
        ]
        q_text_fe = (f"A localized electrochemical corrosion cell on an **{env_desc}** sustains an average corrosion current of I = {i_corr_val:.2f} A "
                     f"for a duration of **{days_exp} days**. Given Fe → Fe²⁺ + 2e⁻ (M = 55.8 g·mol⁻¹, F = 96 500 C·mol⁻¹), calculate the mass of iron metal lost due to rusting:")
        expl_fe = (f"1. Total time: t = {days_exp} days × 24 × 3600 = {t_sec_corr:.0f} s. "
                   f"2. Total charge: Q = I × t = {i_corr_val:.2f} A × {t_sec_corr:.0f} s = {q_corr_tot:.0f} C. "
                   f"3. Moles of Fe oxidized: n = Q / (2 × 96 500) = {moles_fe:.4f} mol. "
                   f"4. Mass of iron lost: m = n × M = {moles_fe:.4f} mol × 55.8 g·mol⁻¹ = {corr_mfe}.")
        add_q("hard", "Quantitative Corrosion Loss Calculations", q_text_fe, corr_mfe, wrs_mfe, "Evaluating", "Calculate mass of iron lost to rusting", expl_fe)

    # 5. Quantitative Young's Modulus and Elastic Elongation Calculations (Hard)
    # E = (F * L) / (A * delta_L) => delta_L = (F * L) / (A * E)
    elastic_materials = [
        ("Structural Mild Steel (E = 200 GPa)", 200.0e9, 200.0, "steel construction cable"),
        ("Structural Aluminium Alloy (E = 70 GPa)", 70.0e9, 70.0, "aircraft tie rod"),
        ("Ductile Copper Rod (E = 110 GPa)", 110.0e9, 110.0, "electrical busbar hanger"),
        ("Titanium Alloy Ti-6Al-4V (E = 114 GPa)", 114.0e9, 114.0, "aerospace landing gear strut"),
        ("High-Strength Brass (E = 100 GPa)", 100.0e9, 100.0, "marine drive shaft coupling"),
        ("Carbon Fibre Composite (E = 150 GPa)", 150.0e9, 150.0, "racing car suspension link"),
        ("Tungsten Heavy Wire (E = 400 GPa)", 400.0e9, 400.0, "high-temperature furnace suspension wire")
    ]

    forces_hard = [1000.0, 2500.0, 5000.0, 10000.0, 20000.0, 40000.0] # N
    lengths_hard = [1.0, 2.0, 3.0, 4.0, 5.0] # m
    areas_hard = [2.0e-5, 5.0e-5, 1.0e-4, 2.0e-4] # m² (20 to 200 mm²)

    for mat_el_name, e_mod_pa, e_mod_gpa, comp_desc_e in elastic_materials:
        for f_h in forces_hard:
            for l_h in lengths_hard:
                for a_h in areas_hard:
                    if counts["hard"] >= 200:
                        break
                    # delta_L = (F * L) / (A * E)
                    dl_m = (f_h * l_h) / (a_h * e_mod_pa)
                    dl_mm = dl_m * 1000.0
                    a_mm2_h = a_h * 1e6
                    corr_dl = f"{dl_mm:.3f} mm ({dl_m:.4e} m)"
                    wrs_dl = [
                        f"{dl_mm * 10:.3f} mm",
                        f"{dl_mm / 2:.3f} mm",
                        f"{dl_mm * 2:.3f} mm",
                        f"{(f_h * a_h) / (l_h * e_mod_pa) * 1e3:.4f} mm",
                        f"{dl_mm + 1.5:.3f} mm",
                        f"{dl_mm * 1000:.3f} mm",
                        f"{dl_mm / 10:.3f} mm"
                    ]
                    q_text_dl = (f"A **{comp_desc_e}** made of **{mat_el_name}** has an original length of L = {l_h:.1f} m and a cross-sectional "
                                 f"area of A = {a_mm2_h:.0f} mm² ({a_h:.1e} m²). When subjected to a tensile pulling force of F = {f_h:.0f} N within its elastic limit, "
                                 f"calculate the resulting ELONGATION (extension, ΔL):")
                    expl_dl = (f"1. Hooke's law / Young's modulus: E = (F × L) / (A × ΔL) => ΔL = (F × L) / (A × E). "
                               f"2. Substitution: ΔL = ({f_h:.0f} N × {l_h:.1f} m) / ({a_h:.1e} m² × {e_mod_pa:.1e} Pa) = {dl_m:.6f} m = {corr_dl}.")
                    add_q("hard", "Young's Modulus & Elastic Deformation", q_text_dl, corr_dl, wrs_dl, "Evaluating", f"Calculate elongation for {mat_el_name.split()[0]}", expl_dl)

                    # Calculating Young's Modulus E = (F * L) / (A * delta_L)
                    if counts["hard"] < 200:
                        corr_em = f"{e_mod_gpa:.0f} GPa ({e_mod_pa:.1e} Pa)"
                        wrs_em = [
                            f"{e_mod_gpa * 2:.0f} GPa",
                            f"{e_mod_gpa / 2:.0f} GPa",
                            f"{e_mod_gpa * 10:.0f} GPa",
                            f"{f_h / dl_m * 1e-9:.2f} GPa (forgot area and length factors)",
                            f"{e_mod_gpa + 50:.0f} GPa",
                            f"{e_mod_gpa - 30:.0f} GPa",
                            f"{e_mod_gpa * 1.5:.0f} GPa"
                        ]
                        q_text_em = (f"In a materials tensile laboratory test, a structural specimen of length L = {l_h:.1f} m and cross-sectional area "
                                     f"A = {a_mm2_h:.0f} mm² ({a_h:.1e} m²) elongates by ΔL = {dl_mm:.3f} mm under a tensile load of F = {f_h:.0f} N. "
                                     f"Calculate the **YOUNG'S MODULUS (E)** of the tested material in GPa:")
                        expl_em = (f"1. Stress: σ = F / A = {f_h:.0f} N / {a_h:.1e} m² = {f_h/a_h:.2e} Pa. "
                                   f"2. Strain: ε = ΔL / L = {dl_m:.4e} m / {l_h:.1f} m = {dl_m/l_h:.4e}. "
                                   f"3. Young's modulus: E = σ / ε = {corr_em}.")
                        add_q("hard", "Young's Modulus & Elastic Deformation", q_text_em, corr_em, wrs_em, "Evaluating", "Calculate Young's modulus from tensile test data", expl_em)

    return questions

if __name__ == '__main__':
    qs = build_materials()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_materials.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
