import json
import os

def build_organic():
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
        qid = f"TS_P2_ORG_{len(questions) + 1:04d}"
        questions.append({
            "id": qid,
            "topic": "Organic Chemistry",
            "subtopic": subtopic,
            "difficulty": difficulty,
            "question": q_clean,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "tags": {
                "grade": "12",
                "subject": "Technical Sciences",
                "topic": "Organic Chemistry",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty,
                "learning_outcome": outcome
            }
        })
        return True

    # =========================================================================
    # 1. EASY (Target: 300 Questions)
    # Core Definitions, Homologous Series, Functional Groups, Reaction Types
    # =========================================================================

    core_definitions = [
        ("Hydrocarbon",
         "An organic compound consisting strictly and solely of hydrogen and carbon atoms (e.g. alkanes, alkenes, alkynes).",
         ["An organic compound containing carbon, hydrogen, and oxygen atoms",
          "A compound containing carbon bonded exclusively to halogen atoms",
          "A water-soluble polymer derived from carboxylic acid derivatives",
          "An inorganic mineral containing carbonate and hydrogen ions",
          "Any synthetic plastic or ceramic material containing carbon fibres",
          "A chemical fuel containing hydrogen and nitrogen elements only"],
         "Hydrocarbons are organic compounds containing ONLY carbon and hydrogen atoms."),

        ("Homologous Series",
         "A series of organic compounds that have the same functional group and general formula, where each successive member differs from the previous one by a -CH₂- unit.",
         ["A mixture of hydrocarbons with identical boiling points and densities",
          "A group of molecules that share identical structural formulas but different molecular masses",
          "Compounds that undergo identical substitution reactions at identical rates",
          "A collection of synthetic polymers containing identical cross-linking bonds",
          "Chemical elements that occupy the same column in the Periodic Table",
          "Isomers that have the same physical properties but different molecular masses"],
         "A homologous series shares the same functional group, same general formula, and members differ by -CH₂-."),

        ("Functional Group",
         "An atom or group of atoms that forms the active chemical centre of an organic molecule and determines its characteristic chemical properties.",
         ["The longest continuous carbon chain in a branched hydrocarbon",
          "The single covalent bond between two adjacent carbon atoms in an alkane",
          "The branch consisting of an alkyl radical attached to a main chain",
          "The molecular mass of an organic compound divided by its carbon count",
          "The non-polar hydrophobic tail of a long-chain carboxylic acid",
          "The inorganic metal catalyst used in hydrogenation reactions"],
         "A functional group is an atom or group of atoms that gives an organic molecule its characteristic chemical reactivity."),

        ("Saturated Hydrocarbon",
         "A hydrocarbon in which all carbon-carbon bonds are single covalent bonds (C-C), meaning no more hydrogen atoms can be added to the molecule (e.g. alkanes).",
         ["A hydrocarbon containing at least one carbon-carbon double or triple bond",
          "An organic compound that is completely dissolved in water to saturation",
          "A volatile liquid that produces maximum vapor pressure at room temperature",
          "A hydrocarbon that reacts spontaneously with bromine water in the dark",
          "A polymer consisting of repeating ester functional groups",
          "A compound with more oxygen atoms than carbon atoms in its structure"],
         "Saturated hydrocarbons contain only single C-C bonds (alkanes), holding the maximum possible hydrogen atoms."),

        ("Unsaturated Hydrocarbon",
         "A hydrocarbon containing one or more carbon-carbon double bonds (C=C, alkenes) or carbon-carbon triple bonds (C≡C, alkynes) that can undergo addition reactions.",
         ["A hydrocarbon with only single bonds that cannot dissolve any more solute",
          "A compound where every carbon is bonded to four hydrogen atoms",
          "An organic molecule containing only ionic and hydrogen bonds",
          "A hydrocarbon that has reached its maximum thermal decomposition limit",
          "A liquid hydrocarbon that does not boil at standard pressure",
          "An alkane containing more than eight carbon atoms in its chain"],
         "Unsaturated hydrocarbons contain multiple bonds (C=C or C≡C) capable of addition reactions."),

        ("Structural Isomer",
         "Organic compounds that have the SAME molecular formula but DIFFERENT structural formulas (different connectivity or arrangement of atoms).",
         ["Molecules with identical structural arrangements but different molecular masses",
          "Compounds in the same homologous series differing by a single -CH₂- unit",
          "Different physical states of the same pure chemical substance",
          "Molecules with the same empirical formula but completely different molecular formulas",
          "Organic molecules that rotate plane-polarized light in identical directions",
          "Mixtures containing equal volumes of two different alkanes"],
         "Structural isomers have the same molecular formula but different structural formulas."),

        ("Chain Isomers",
         "Structural isomers that have the same molecular formula and functional group, but differ in the branching or arrangement of the carbon skeleton (e.g. butane and 2-methylpropane).",
         ["Isomers that differ only in the position of their functional group on the chain",
          "Isomers that belong to completely different homologous series",
          "Molecules that contain different types of chemical bonds",
          "Compounds that differ in molecular formula by a -CH₂- unit",
          "Isomers formed exclusively through high-temperature cracking reactions",
          "Molecules with identical boiling points and surface contact areas"],
         "Chain isomers differ in the arrangement of the carbon skeleton (branching)."),

        ("Positional Isomers",
         "Structural isomers that have the same molecular formula and carbon skeleton, but differ in the position of the functional group or substituent on the chain (e.g. butan-1-ol and butan-2-ol).",
         ["Isomers that have different carbon chain lengths and different molecular formulas",
          "Isomers belonging to different homologous series such as esters and acids",
          "Compounds formed when two unsaturated monomers combine in addition polymerization",
          "Molecules with identical physical properties and identical vapor pressures",
          "Isomers produced exclusively by the complete combustion of fossil fuels",
          "Hydrocarbons containing both single and triple bonds simultaneously"],
         "Positional isomers have the functional group or substituent attached at different positions on the parent chain."),

        ("Functional Isomers",
         "Structural isomers that have the same molecular formula but contain DIFFERENT functional groups and therefore belong to different homologous series (e.g. carboxylic acids and esters, or aldehydes and ketones).",
         ["Isomers that differ only by the degree of branching of the carbon chain",
          "Isomers that have identical IUPAC names and identical boiling points",
          "Molecules that contain identical functional groups at different carbon positions",
          "Hydrocarbons that have the same boiling point but different molecular formulas",
          "Polymers that share identical physical tensile strength",
          "Compounds that undergo substitution reactions at identical rates"],
         "Functional isomers share the same molecular formula but possess different functional groups (e.g. propanoic acid and methyl ethanoate, C₃H₆O₂)."),

        ("Esterification Reaction",
         "An acid-catalysed condensation reaction between an alcohol and a carboxylic acid, heated in the presence of concentrated sulfuric acid (H₂SO₄), producing an ester and water.",
         ["The addition of hydrogen gas across an alkene double bond to form an alkane",
          "The cracking of long-chain petroleum alkanes into shorter volatile alkenes",
          "The reaction between an alkane and chlorine gas in the presence of ultraviolet light",
          "The complete combustion of ethanol in excess oxygen to produce carbon dioxide",
          "The elimination of hydrogen halide from a haloalkane using hot concentrated base",
          "The hydrolysis of an ester using aqueous sodium hydroxide to make soap"],
         "Esterification: Alcohol + Carboxylic acid (in presence of conc. H₂SO₄ catalyst and heat) -> Ester + Water.")
    ]

    stems = [
        "In Grade 12 Technical Sciences Organic Chemistry, how is **'{}'** defined?",
        "According to the CAPS curriculum, **'{}'** is described as:",
        "Which statement provides the exact scientific definition of **'{}'**?",
        "Identify the correct CAPS definition for **'{}'**:",
        "In an examination context, which statement accurately defines **'{}'**?"
    ]

    for term, corr_def, wr_defs, exp_def in core_definitions:
        for st in stems:
            add_q("easy", "Definitions", st.format(term), corr_def, wr_defs, "Remembering", f"Define {term}", exp_def)

    # General Formulas of Homologous Series
    homologous_series_info = [
        ("Alkanes", "C_n H_{2n+2}", "single carbon-carbon covalent bonds only (C-C)", "saturated hydrocarbons"),
        ("Alkenes", "C_n H_{2n}", "one carbon-carbon double covalent bond (C=C)", "unsaturated hydrocarbons"),
        ("Alkynes", "C_n H_{2n-2}", "one carbon-carbon triple covalent bond (C≡C)", "unsaturated hydrocarbons"),
        ("Haloalkanes (Alkyl halides)", "C_n H_{2n+1} X (where X = F, Cl, Br, I)", "halogen atom bonded to an sp³ carbon atom", "halogenated hydrocarbons"),
        ("Alcohols", "C_n H_{2n+1} OH", "hydroxyl functional group (-OH) bonded to a saturated carbon atom", "polar organic compounds with hydrogen bonding"),
        ("Carboxylic Acids", "C_n H_{2n+1} COOH", "carboxyl functional group (-COOH consisting of carbonyl C=O and hydroxyl -OH)", "organic weak acids"),
        ("Esters", "C_n H_{2n} O₂ (or R-COO-R')", "ester functional group (-COO- / -COOR)", "sweet, fruity-smelling organic compounds")
    ]

    for ser_name, gen_form, func_grp, ser_desc in homologous_series_info:
        for q_stem_s in [
            f"What is the general formula and characteristic functional group of the **{ser_name}** homologous series?",
            f"In Grade 12 Technical Sciences, which entry correctly describes the **{ser_name}**?",
            f"Identify the general formula and structural feature defining **{ser_name}**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_ser = f"General formula: {gen_form}; Functional group: {func_grp} ({ser_desc})."
            w_ser = [
                f"General formula: C_n H_{{n}}; Functional group: ionic carboxylate lattice.",
                f"General formula: C_n H_{{2n-4}}; Functional group: aromatic benzene ring.",
                f"General formula: C_n H_{{2n+4}}; Functional group: metallic covalent bond.",
                f"General formula: C_{{2n}} H_{{n}}; Functional group: inorganic carbonate radical.",
                f"General formula: C_n H_{{2n}} O₄; Functional group: cross-linked polymer network.",
                f"General formula: C_n H_{{3n}}; Functional group: triple nitrogen bridge."
            ]
            add_q("easy", "Homologous Series", q_stem_s, c_ser, w_ser, "Remembering", f"Identify characteristics of {ser_name}", c_ser)

    # Reaction Types Classification (Easy)
    reaction_types = [
        ("Combustion of an alkane (e.g. CH₄ + 2O₂ → CO₂ + 2H₂O + heat)",
         "An exothermic oxidation reaction in which a hydrocarbon reacts with excess oxygen to produce carbon dioxide, water vapor, and energy.",
         ["An addition reaction where oxygen atoms insert into single carbon-hydrogen bonds",
          "A substitution reaction in which oxygen replaces hydrogen atoms one by one",
          "An elimination reaction where water is extracted to form an unsaturated alkyne",
          "An esterification reaction producing sweet-smelling synthetic esters",
          "A catalytic cracking reaction breaking down heavy waxes into lighter naphtha",
          "A polymerization reaction linking monomer units into macromolecules"],
         "Combustion is an exothermic reaction of a hydrocarbon with oxygen producing CO₂ and H₂O."),

        ("Halogenation of an alkane (e.g. CH₄ + Cl₂ → CH₃Cl + HCl in the presence of UV light)",
         "A FREE-RADICAL SUBSTITUTION reaction in which a halogen atom replaces a hydrogen atom on a saturated carbon, requiring ultraviolet (UV) light or sunlight.",
         ["An addition reaction where chlorine opens a double bond in the alkane",
          "An elimination reaction where hydrogen chloride gas is expelled to form ethene",
          "A condensation esterification reaction forming an alkyl ester and water",
          "A hydration reaction adding water across a saturated carbon framework",
          "A catalytic cracking process producing short-chain motor fuel molecules",
          "A neutralization reaction between an organic acid and an alkali base"],
         "Alkanes undergo substitution reactions with halogens in the presence of UV light or heat."),

        ("Hydrogenation of an alkene (e.g. CH₂=CH₂ + H₂ → CH₃-CH₃ in the presence of Ni/Pt catalyst)",
         "An ADDITION reaction in which hydrogen atoms add across the carbon-carbon double bond to convert an unsaturated alkene into a saturated alkane.",
         ["A substitution reaction where hydrogen displaces carbon atoms from the chain",
          "An elimination reaction where hydrogen gas is released to form an alkyne",
          "A thermal cracking reaction converting short hydrocarbons into longer waxes",
          "An esterification reaction producing carboxylic acids and hydrogen gas",
          "An oxidation reaction that turns liquid vegetable oil into carbon black",
          "A dehydrohalogenation reaction using concentrated hot ethanolic sodium hydroxide"],
         "Hydrogenation is an addition reaction: Alkene + H₂ (with Pt/Pd/Ni catalyst) -> Alkane (used to harden liquid oils into margarine)."),

        ("Halogenation of an alkene (e.g. CH₂=CH₂ + Br₂ → CH₂Br-CH₂Br, Bromine water test)",
         "An ADDITION reaction in which halogen atoms add across the double bond; rapid decolourisation of reddish-brown bromine water without light proves unsaturation.",
         ["A substitution reaction requiring intense ultraviolet radiation over several hours",
          "An elimination reaction producing an alkyne and hydrobromic acid",
          "A fermentation reaction producing alcohol and carbon dioxide bubbles",
          "An acid-base neutralization producing a halide salt and water",
          "A catalytic cracking process breaking down large polymer molecules",
          "An esterification reaction catalyzed by concentrated sulfuric acid"],
         "Alkenes undergo rapid addition of bromine (Br₂), turning reddish-brown bromine water colourless immediately, proving unsaturation."),

        ("Hydration of an alkene (e.g. CH₂=CH₂ + H₂O → CH₃CH₂OH in the presence of H₃PO₄ catalyst)",
         "An ADDITION reaction in which water adds across the double bond of an alkene in the presence of a strong acid catalyst (H₃PO₄ or H₂SO₄) to form an alcohol.",
         ["A dehydration elimination reaction that removes water from an alcohol",
          "A free-radical substitution reaction displacing hydrogen with oxygen gas",
          "A saponification reaction forming soap and glycerol",
          "A combustion reaction producing carbon dioxide and hydrogen peroxide",
          "A thermal cracking reaction yielding methane and carbon monoxide",
          "A condensation polymerization reaction forming high-density polyethylene"],
         "Hydration is the addition of water (H₂O) across a C=C double bond in the presence of an acid catalyst (H₃PO₄) to produce an alcohol."),

        ("Dehydrohalogenation of a haloalkane (e.g. CH₃CH₂Cl + NaOH(conc, ethanol) + heat → CH₂=CH₂ + NaCl + H₂O)",
         "An ELIMINATION reaction in which hydrogen halide is removed from a haloalkane using a concentrated strong base in hot ethanol (reflux) to form an alkene.",
         ["A substitution reaction producing an alcohol and sodium chloride in water",
          "An addition reaction adding sodium and chlorine across a saturated bond",
          "An esterification reaction producing an ethyl ester and sulfuric acid",
          "A hydrogenation reaction converting a haloalkane into a saturated alkane",
          "A hydration reaction adding water across a double bond with phosphoric acid",
          "A cracking process separating heavy crude oil into commercial fractions"],
         "Dehydrohalogenation is an elimination reaction: Haloalkane + hot conc. NaOH/KOH in ethanol -> Alkene + NaX + H₂O."),

        ("Dehydration of an alcohol (e.g. CH₃CH₂OH + conc. H₂SO₄ + heat → CH₂=CH₂ + H₂O)",
         "An ELIMINATION reaction in which a water molecule is removed from an alcohol by heating with concentrated sulfuric acid (H₂SO₄) or phosphoric acid, forming an alkene.",
         ["A hydration addition reaction that adds water across a double bond",
          "A substitution reaction replacing the hydroxyl group with a sulfate radical",
          "An esterification reaction reacting with carboxylic acid to make ester",
          "A catalytic cracking reaction converting ethanol into methane gas",
          "An oxidation reaction producing carbon dioxide and solid carbon soot",
          "A saponification reaction precipitating insoluble fatty acid salts"],
         "Dehydration is an elimination reaction: Alcohol (heated with conc. H₂SO₄) -> Alkene + H₂O."),

        ("Hydrolysis of a haloalkane (e.g. CH₃CH₂Br + dilute NaOH(aq) + gentle heat → CH₃CH₂OH + NaBr)",
         "A NUCLEOPHILIC SUBSTITUTION reaction in which the halogen atom of a haloalkane is replaced by a hydroxyl group (-OH) using dilute aqueous base and mild heating, forming an alcohol.",
         ["An elimination reaction producing an alkene and hydrogen bromide gas",
          "An addition reaction adding sodium hydroxide across a double bond",
          "An esterification condensation producing an alkyl ester and water",
          "A catalytic hydrogenation reaction using nickel catalyst under pressure",
          "A combustion reaction producing carbon dioxide and salt fumes",
          "A cracking process yielding short-chain volatile alkanes and alkenes"],
         "Hydrolysis of haloalkanes is a substitution reaction: Haloalkane + dilute aqueous NaOH/KOH (mild heat) -> Alcohol + NaX.")
    ]

    for rx_name, rx_corr, rx_wrongs, rx_expl in reaction_types:
        for st_r in [
            "In organic chemistry, how is the following reaction classified and explained? **{}**",
            "Consider the chemical transformation: **{}**. Which statement correctly describes it?",
            "Identify the reaction type and operational conditions for: **{}**"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Reaction Types", st_r.format(rx_name), rx_corr, rx_wrongs, "Understanding", "Classify organic reaction type and conditions", rx_expl)

    # Intermolecular Forces & Physical Properties (Easy)
    imf_concepts = [
        ("London dispersion forces in alkanes",
         "Weak intermolecular forces arising from temporary induced dipoles; their strength increases with increasing molecular mass (chain length) and surface contact area, leading to higher boiling points for larger alkanes.",
         ["Permanent dipole-dipole attractions between polar carbon-carbon bonds",
          "Strong covalent bonds linking adjacent alkane molecules together",
          "Extremely strong hydrogen bonds formed between hydrogen atoms of different chains",
          "Electrostatic ionic forces between positively and negatively charged ions",
          "Magnetic attractions generated by rotating carbon nucleus spins",
          "Metallic delocalized electron attractions across hydrocarbon layers"],
         "Alkanes are non-polar molecules held together only by London dispersion forces (induced dipole-induced dipole)."),

        ("Dipole-dipole forces in haloalkanes and esters",
         "Intermolecular forces between polar molecules that have permanent dipole moments (due to electronegativity differences between carbon and halogens or oxygen), which are stronger than London forces for molecules of comparable size.",
         ["Weak induced forces that disappear completely at temperatures above 0 °C",
          "Extremely strong hydrogen bonds between hydrogen and carbon atoms",
          "Direct covalent sharing of valence electrons between adjacent molecules",
          "Ionic crystal lattice attractions that give esters boiling points above 800 °C",
          "Nuclear forces holding the carbon skeleton together during vaporization",
          "London forces that only exist in the solid crystalline state"],
         "Polar molecules (like haloalkanes and esters) experience permanent dipole-dipole forces in addition to London forces."),

        ("Hydrogen bonding in alcohols",
         "Strong intermolecular forces formed between the highly polarized hydrogen atom attached to oxygen (-O-H) in one alcohol molecule and the lone pair of electrons on the electronegative oxygen atom of an adjacent molecule.",
         ["Weak London dispersion forces caused by symmetrical electron distribution",
          "Direct covalent bonds between hydrogen atoms of neighboring molecules",
          "Ionic attractions between free hydronium and hydroxide ions in pure alcohol",
          "Metallic bonding created by mobile hydrogen electrons",
          "Magnetic dipole interactions between carbon and oxygen nuclei",
          "Permanent dipole forces that are weaker than London dispersion forces"],
         "Alcohols contain polar -O-H groups capable of strong intermolecular hydrogen bonding."),

        ("Hydrogen bonding in carboxylic acids vs alcohols",
         "Carboxylic acids form stronger intermolecular hydrogen bonds than alcohols of similar mass because each carboxylic acid molecule can form TWO hydrogen bonds, creating stable dimers with significantly higher boiling points.",
         ["Carboxylic acids have only London dispersion forces and lack hydrogen bonding",
          "Alcohols form quadruple hydrogen bonds while carboxylic acids form none",
          "Carboxylic acids have lower boiling points than alcohols because of the carbonyl group",
          "Carboxylic acids are completely non-polar molecules with zero dipole moment",
          "Alcohols form dimers while carboxylic acids form giant covalent networks",
          "Hydrogen bonding in carboxylic acids is eliminated in the liquid phase"],
         "Carboxylic acids form dimers via two hydrogen bonds per pair of molecules, giving them higher boiling points than alcohols of comparable mass."),

        ("Effect of carbon chain branching on boiling point",
         "Branching makes the molecule more spherical and compact, reducing the surface contact area between adjacent molecules, which weakens the London dispersion forces and LOWERS the boiling point.",
         ["Branching increases surface contact area, which strengthens London forces and increases boiling point",
          "Branching converts London dispersion forces into strong hydrogen bonds",
          "Branching has zero effect on boiling point because molecular formula is identical",
          "Branching increases boiling point because branches act as physical hooks between molecules",
          "Branching converts the organic compound into an ionic crystal lattice",
          "Branching always increases the vapor pressure to infinity at room temperature"],
         "Branching decreases molecular surface area -> weaker intermolecular London dispersion forces -> LOWER boiling point.")
    ]

    for imf_name, imf_ans, imf_wrongs, imf_expl in imf_concepts:
        for st_imf in [
            "In Grade 12 Technical Sciences, explain the physical nature and consequence of **'{}'**:",
            "How does **'{}'** influence the physical properties of organic compounds?",
            "Which statement accurately explains **'{}'**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Intermolecular Forces", st_imf.format(imf_name), imf_ans, imf_wrongs, "Understanding", f"Explain {imf_name}", imf_expl)

    # IUPAC Nomenclature Rules (filling easy up to 300)
    iupac_rules = [
        ("Determining the parent carbon chain",
         "Identify the longest continuous chain of carbon atoms containing the principal functional group; the number of carbons in this chain determines the root name (e.g. meth-, eth-, prop-, but-, pent-, hex-).",
         ["Count only the straight horizontal carbon atoms ignoring any vertical bends",
          "Always select the chain with the fewest carbon atoms to minimize formula mass",
          "Select the chain containing the largest number of oxygen or halogen atoms only",
          "Count all carbon atoms in the molecule together regardless of branching",
          "Choose the ring structure even if the aliphatic chain has more carbon atoms",
          "Select the chain that gives the highest possible position numbers to substituents"],
         "Rule 1: Find the longest continuous carbon chain containing the highest priority functional group."),

        ("Numbering the parent carbon chain",
         "Number the carbon atoms from the end of the chain that gives the functional group (or first substituent in alkanes) the LOWEST possible position number.",
         ["Always number from left to right regardless of functional group position",
          "Always number from right to left starting from methyl branches only",
          "Number from the end that gives substituents the highest possible locant numbers",
          "Number starting from the middle carbon atom outward in both directions",
          "Number in order of increasing atomic mass of attached substituents",
          "Number alphabetically based on the names of the alkyl branches"],
         "Rule 2: Number the chain from the end closest to the principal functional group (lowest locants)."),

        ("Alphabetical ordering of substituents",
         "List substituent prefixes in alphabetical order (e.g. bromo- before chloro-, ethyl- before methyl-), ignoring numerical multiplying prefixes such as di-, tri-, tetra-.",
         ["List substituents in order of increasing carbon chain length of the branch",
          "List substituents in order of increasing locant numbers along the chain",
          "Include multiplying prefixes (di-, tri-) when alphabetizing substituent names",
          "Place alkyl branches before halogen substituents under all circumstances",
          "Place functional groups at the beginning of the IUPAC name as prefixes",
          "Order substituents by electronegativity from lowest to highest"],
         "Rule 3: Substituents are listed alphabetically (bromo before chloro before ethyl before methyl). Multiplying prefixes (di, tri) are ignored for alphabetizing."),

        ("Punctuation in IUPAC chemical names",
         "Use commas to separate adjacent numbers (e.g. 2,2-dimethylpropane) and hyphens to separate numbers from letters (e.g. 2-methylbutane); write the entire name as a single word without spaces.",
         ["Use colons between numbers and slashes between letters and numbers",
          "Leave spaces between all prefixes and the parent root name",
          "Use periods between numbers and semicolons between words",
          "Capitalize every substituent and use commas between syllables",
          "Enclose all locant numbers in parentheses without hyphens",
          "Write the entire IUPAC name in reverse order from suffix to prefix"],
         "Rule 4: Commas separate numbers (2,2-), hyphens separate numbers from letters (2-methyl-).")
    ]

    for rule_name, rule_ans, rule_wrongs, rule_expl in iupac_rules:
        for st_rule in [
            "What is the IUPAC naming convention regarding **'{}'**?",
            "In organic nomenclature, how is **'{}'** applied according to IUPAC rules?",
            "Which statement correctly describes the IUPAC protocol for **'{}'**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "IUPAC Nomenclature Rules", st_rule.format(rule_name), rule_ans, rule_wrongs, "Remembering", f"State IUPAC rule for {rule_name}", rule_expl)

    # Primary, Secondary, Tertiary Alcohols & Haloalkanes
    alcohol_types = [
        ("Primary alcohol (e.g. ethanol, propan-1-ol)",
         "The carbon atom bonded to the hydroxyl group (-OH) is bonded to only ONE other carbon atom (or no other carbons, as in methanol).",
         ["The hydroxyl group is bonded to a carbon bonded to three other carbon atoms",
          "The alcohol has only one single covalent bond throughout the entire molecule",
          "The alcohol cannot undergo dehydration to form an alkene under any conditions",
          "The molecule contains two hydroxyl groups on adjacent carbon atoms",
          "The compound is an isomer of a carboxylic acid with identical boiling point",
          "The hydroxyl group is attached to a carbon participating in a double bond"],
         "Primary alcohol: -OH is attached to a carbon bonded to at most ONE other carbon atom."),

        ("Secondary alcohol (e.g. propan-2-ol, butan-2-ol)",
         "The carbon atom bonded to the hydroxyl group (-OH) is directly bonded to TWO other carbon atoms.",
         ["The carbon bearing the -OH group is bonded to only one other carbon atom",
          "The molecule contains two separate hydroxyl groups attached to the same carbon",
          "The alcohol undergoes substitution reactions twice as fast as primary alcohols",
          "The compound is formed exclusively by the hydrogenation of carboxylic acids",
          "The alcohol has two double bonds in its parent carbon skeleton",
          "The compound forms an ester without needing any acid catalyst"],
         "Secondary alcohol: -OH is attached to a carbon bonded to TWO other carbon atoms."),

        ("Tertiary alcohol (e.g. 2-methylpropan-2-ol)",
         "The carbon atom bonded to the hydroxyl group (-OH) is directly bonded to THREE other carbon atoms.",
         ["The carbon bearing the -OH group is bonded to zero other carbon atoms",
          "The molecule contains three separate hydroxyl groups in its chain",
          "The alcohol oxidizes rapidly into a carboxylic acid with acidified dichromate",
          "The alcohol has three times the boiling point of primary alcohols",
          "The compound is an unsaturated alkene with three methyl substituents",
          "The alcohol reacts spontaneously with water to precipitate solid sodium"],
         "Tertiary alcohol: -OH is attached to a carbon bonded to THREE other carbon atoms.")
    ]

    for alc_type, alc_ans, alc_wrongs, alc_expl in alcohol_types:
        for st_alc in [
            "In Technical Sciences, how is a **'{}'** classified and identified?",
            "Which description accurately characterizes a **'{}'**?",
            "Identify the defining structural feature of a **'{}'**:"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Alcohol Classification", st_alc.format(alc_type), alc_ans, alc_wrongs, "Remembering", f"Classify {alc_type}", alc_expl)

    # Direct Easy Identification of Alkanes, Alkenes, Alkynes
    hydrocarbon_stems = [
        ("Methane (CH₄)", "an alkane (saturated hydrocarbon) containing one carbon atom and four single C-H bonds"),
        ("Ethane (C₂H₆)", "an alkane (saturated hydrocarbon) with the molecular formula C₂H₆ obeying C_n H_{2n+2}"),
        ("Propane (C₃H₈)", "an alkane (saturated hydrocarbon) commonly used as LP gas in domestic heating and cooking"),
        ("Butane (C₄H₁₀)", "an alkane (saturated hydrocarbon) used as fuel in portable lighters and camping stoves"),
        ("Pentane (C₅H₁₂)", "an alkane (saturated hydrocarbon) existing as a volatile colorless liquid at room temperature"),
        ("Hexane (C₆H₁₄)", "an alkane (saturated hydrocarbon) commonly used as a non-polar solvent in chemical laboratories"),
        ("Heptane (C₇H₁₆)", "an alkane (saturated hydrocarbon) used as the zero-point standard for fuel octane ratings"),
        ("Octane (C₈H₁₈)", "an alkane (saturated hydrocarbon) that serves as a key standard component of commercial petrol"),
        ("Ethene (C₂H₄)", "an alkene (unsaturated hydrocarbon) containing one carbon-carbon double bond (C=C)"),
        ("Propene (C₃H₆)", "an alkene (unsaturated hydrocarbon) that undergoes addition reactions to form polypropene"),
        ("But-1-ene (C₄H₈)", "an alkene with a double bond between carbon-1 and carbon-2 (positional isomer of but-2-ene)"),
        ("Pent-1-ene (C₅H₁₀)", "an alkene with a terminal double bond in a 5-carbon straight chain"),
        ("Hex-1-ene (C₆H₁₂)", "an alkene with six carbon atoms used as a co-monomer in polyethylene production"),
        ("Ethyne / Acetylene (C₂H₂)", "an alkyne (unsaturated hydrocarbon) containing a carbon-carbon triple bond (C≡C) used in oxy-acetylene welding"),
        ("Propyne (C₃H₄)", "an alkyne containing a carbon-carbon triple bond with molecular formula C₃H₄"),
        ("But-1-yne (C₄H₆)", "an alkyne containing a triple bond between carbon-1 and carbon-2")
    ]

    for hc_name, hc_desc in hydrocarbon_stems:
        for st_hc in [
            f"What is the chemical classification and formula of **{hc_name}**?",
            f"In Grade 12 Technical Sciences, **{hc_name}** is recognized as:",
            f"Identify the structural classification of **{hc_name}**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_hc = f"It is {hc_desc}."
            w_hc = [
                "It is an inorganic oxide salt that forms basic solutions in water.",
                "It is a condensation polymer composed of repeating amino acid linkages.",
                "It is an aromatic ester used exclusively as an industrial dye.",
                "It is an electrolyte that dissociates into hydronium and sulfate ions.",
                "It is a carboxylic acid that neutralizes strong sodium hydroxide bases.",
                "It is an alcohol containing three polar hydroxyl functional groups."
            ]
            add_q("easy", "Hydrocarbon Classification", st_hc, c_hc, w_hc, "Remembering", f"Classify {hc_name}", c_hc)

    # Functional Group Identification (Easy)
    functional_groups = [
        ("Hydroxyl group (-OH)", "Alcohols", "a polar group that enables intermolecular hydrogen bonding with water and other alcohol molecules"),
        ("Carboxyl group (-COOH)", "Carboxylic Acids", "a group consisting of a carbonyl (C=O) and hydroxyl (-OH) on the same terminal carbon atom"),
        ("Ester group (-COO- / -COOR)", "Esters", "a functional group formed by condensation between a carboxylic acid and an alcohol"),
        ("Carbon-carbon double bond (C=C)", "Alkenes", "an unsaturated functional site capable of undergoing electrophilic addition reactions"),
        ("Carbon-carbon triple bond (C≡C)", "Alkynes", "a highly unsaturated bond containing one sigma and two pi covalent bonds"),
        ("Halogen atom (-F, -Cl, -Br, -I)", "Haloalkanes (Alkyl halides)", "a polar group where electronegative halogen polarizes the carbon-halogen bond")
    ]

    for fg_name, fg_series, fg_role in functional_groups:
        for st_fg in [
            f"Which homologous series is defined by the **{fg_name}** functional group, and what is its role?",
            f"In organic chemistry, the **{fg_name}** is the characteristic functional group of which series?",
            f"Identify the homologous series and structural nature of the **{fg_name}**:"
        ]:
            if counts["easy"] >= 300:
                break
            c_fg = f"It defines the {fg_series} ({fg_role})."
            w_fg = [
                f"It defines inorganic carbonates that decompose in hydrochloric acid.",
                f"It defines saturated alkanes that have zero functional groups.",
                f"It defines synthetic metals that conduct electricity at room temperature.",
                f"It defines aqueous electrolytes that undergo complete ionic dissociation.",
                f"It defines aromatic hydrocarbons containing delocalized pi rings.",
                f"It defines polymers that have no covalent bonds."
            ]
            add_q("easy", "Functional Groups", st_fg, c_fg, w_fg, "Remembering", f"Identify functional group {fg_name}", c_fg)

    # Identifying Series from Molecular Formula (Easy)
    formula_id = [
        ("C4H10", "Alkane (saturated hydrocarbon)", "fits general formula C_n H_{2n+2} with n=4: (2*4)+2 = 10"),
        ("C5H12", "Alkane (saturated hydrocarbon)", "fits general formula C_n H_{2n+2} with n=5: (2*5)+2 = 12"),
        ("C6H14", "Alkane (saturated hydrocarbon)", "fits general formula C_n H_{2n+2} with n=6: (2*6)+2 = 14"),
        ("C3H6", "Alkene (unsaturated hydrocarbon)", "fits general formula C_n H_{2n} with n=3: 2*3 = 6"),
        ("C4H8", "Alkene (unsaturated hydrocarbon)", "fits general formula C_n H_{2n} with n=4: 2*4 = 8"),
        ("C5H10", "Alkene (unsaturated hydrocarbon)", "fits general formula C_n H_{2n} with n=5: 2*5 = 10"),
        ("C3H4", "Alkyne (unsaturated hydrocarbon)", "fits general formula C_n H_{2n-2} with n=3: (2*3)-2 = 4"),
        ("C4H6", "Alkyne (unsaturated hydrocarbon)", "fits general formula C_n H_{2n-2} with n=4: (2*4)-2 = 6"),
        ("C2H5Cl", "Haloalkane (chloroalkane)", "fits general formula C_n H_{2n+1}Cl with n=2: (2*2)+1 = 5"),
        ("C3H7Br", "Haloalkane (bromoalkane)", "fits general formula C_n H_{2n+1}Br with n=3: (2*3)+1 = 7"),
        ("C2H6O (or C2H5OH)", "Alcohol (or functional isomer ether)", "fits general formula C_n H_{2n+1}OH (ethanol)"),
        ("C3H8O (or C3H7OH)", "Alcohol (propanol)", "fits general formula C_n H_{2n+1}OH with n=3 (propan-1-ol or propan-2-ol)"),
        ("C2H4O2 (or CH3COOH)", "Carboxylic acid (ethanoic acid) or Ester (methyl methanoate)", "fits general formula C_n H_{2n}O₂ with n=2"),
        ("C3H6O2 (or C2H5COOH)", "Carboxylic acid (propanoic acid) or Ester (methyl ethanoate)", "fits general formula C_n H_{2n}O₂ with n=3")
    ]

    for form_val, form_ser, form_reason in formula_id:
        if counts["easy"] >= 300:
            break
        q_text_fid = f"To which homologous series does the organic compound with molecular formula **{form_val}** belong?"
        c_fid = f"It belongs to the {form_ser}."
        w_fid = [
            "It belongs to the inorganic mineral acids.",
            "It belongs to the aromatic cycloalkane series.",
            "It belongs to the metallic coordination complexes.",
            "It belongs to the ionic carbonate salts.",
            "It belongs to the synthetic polypeptide series.",
            "It belongs to the radioactive actinide series."
        ]
        expl_fid = f"Formula analysis: {form_val} {form_reason} -> {form_ser}."
        add_q("easy", "Molecular Formula Classification", q_text_fid, c_fid, w_fid, "Applying", f"Classify {form_val}", expl_fid)

    # Classifying Primary, Secondary, Tertiary Compounds (Easy)
    class_pst = [
        ("1-bromobutane (CH3CH2CH2CH2Br)", "PRIMARY haloalkane", "the carbon attached to bromine is bonded to only ONE other carbon atom"),
        ("2-bromobutane (CH3CH(Br)CH2CH3)", "SECONDARY haloalkane", "the carbon attached to bromine is bonded directly to TWO other carbon atoms"),
        ("2-bromo-2-methylpropane ((CH3)3CBr)", "TERTIARY haloalkane", "the carbon attached to bromine is bonded directly to THREE other carbon atoms"),
        ("butan-1-ol (CH3CH2CH2CH2OH)", "PRIMARY alcohol", "the carbon bearing the -OH group is bonded to only ONE other carbon atom"),
        ("butan-2-ol (CH3CH(OH)CH2CH3)", "SECONDARY alcohol", "the carbon bearing the -OH group is bonded directly to TWO other carbon atoms"),
        ("2-methylpropan-2-ol ((CH3)3COH)", "TERTIARY alcohol", "the carbon bearing the -OH group is bonded directly to THREE other carbon atoms"),
        ("propan-1-ol (CH3CH2CH2OH)", "PRIMARY alcohol", "the hydroxyl carbon is bonded to only one other carbon atom"),
        ("propan-2-ol (CH3CH(OH)CH3)", "SECONDARY alcohol", "the hydroxyl carbon is bonded directly to two other carbon atoms")
    ]

    for c_name_pst, c_type_pst, c_rsn_pst in class_pst:
        if counts["easy"] >= 300:
            break
        q_pst = f"How is **{c_name_pst}** classified in organic chemistry?"
        c_pst = f"It is a {c_type_pst}."
        w_pst = [
            f"It is a {'SECONDARY' if 'PRIMARY' in c_type_pst else 'PRIMARY'} compound with quaternary bonding.",
            "It is an aromatic ring structure with delocalized pi electrons.",
            "It is an unsaturated alkene containing a conjugated double bond.",
            "It is a carboxylic acid dimer held by double hydrogen bonds.",
            "It is an inorganic hydroxide salt that conducts electricity in water.",
            "It is an ester synthesized from sulfuric acid and an alkene."
        ]
        expl_pst = f"{c_name_pst} is a {c_type_pst} because {c_rsn_pst}."
        add_q("easy", "Primary/Secondary/Tertiary Classification", q_pst, c_pst, w_pst, "Understanding", f"Classify {c_name_pst}", expl_pst)

    # Basic Polymer Concepts & Unsaturation Tests (Filling Easy to 300)
    polymer_basics = [
        ("Monomer",
         "A small, reactive organic molecule (such as ethene or vinyl chloride) that can join together with other identical or different molecules to form a polymer.",
         ["A giant macromolecule composed of thousands of repeating units",
          "An inorganic mineral catalyst that speeds up cracking reactions",
          "A saturated alkane with high boiling point used as machine lubricant",
          "A waste product formed during condensation esterification",
          "A volatile liquid used as non-polar solvent in chemical extraction",
          "An electrolyte that dissociates into hydronium ions in water"],
         "A monomer is a small reactive molecule that can bind chemically to others to form a polymer."),

        ("Polymer",
         "A large molecule (macromolecule) formed by joining together hundreds or thousands of smaller repeating structural units (monomers) through covalent bonds.",
         ["A short-chain volatile alkane extracted from crude oil fractions",
          "A single atom of carbon bonded to four hydrogen atoms",
          "A small reactive molecule that undergoes addition reactions with bromine",
          "An inorganic ionic salt consisting of alternating cations and anions",
          "A dilute aqueous solution of sodium hydroxide used in hydrolysis",
          "A cyclic aromatic compound with alternating double bonds"],
         "A polymer is a large macromolecule composed of many repeating monomer units."),

        ("Addition Polymerization",
         "A reaction in which many unsaturated monomer molecules (containing C=C double bonds) join together without the loss of any atoms or small molecules to form a polymer.",
         ["A reaction where monomers join together with the elimination of water molecules",
          "The breaking down of long polymer chains into small alkanes by heating",
          "The reaction of a carboxylic acid with an alcohol in the presence of sulfuric acid",
          "The free-radical replacement of hydrogen atoms by halogen atoms under UV light",
          "The elimination of hydrogen halide from a haloalkane using concentrated base",
          "The complete combustion of fossil fuels in excess atmospheric oxygen"],
         "Addition polymerization: Unsaturated monomers (with C=C) join without loss of any small molecules."),

        ("Condensation Polymerization",
         "A polymerization reaction in which monomer molecules with two reactive functional groups combine together, accompanied by the elimination of a small byproduct molecule such as water (H₂O) or HCl.",
         ["A reaction joining monomers without the loss of any atoms or byproducts",
          "The thermal cracking of heavy petroleum wax into gasoline fractions",
          "The addition of hydrogen gas across alkene double bonds using nickel catalyst",
          "The rapid decolourisation of reddish-brown bromine water in total darkness",
          "The complete oxidation of hydrocarbons into carbon dioxide and water",
          "The physical condensation of vapor into liquid inside a distillation column"],
         "Condensation polymerization: Monomers join with the loss of a small molecule like water."),

        ("Bromine Water Test for Unsaturation",
         "Reddish-brown bromine water (Br₂(aq)) DECOLOURISES RAPIDLY in the dark when added to an unsaturated hydrocarbon (alkene), but remains reddish-brown when mixed with a saturated hydrocarbon (alkane) in the dark.",
         ["Bromine water turns bright blue in the presence of alkanes and stays clear with alkenes",
          "Bromine water boils violently and precipitates solid copper metal with alkynes",
          "Both alkanes and alkenes decolourise bromine water immediately in total darkness",
          "Bromine water tests exclusively for carboxylic acids and turns bright pink",
          "Alkanes decolourise bromine water faster than alkenes in total darkness",
          "Bromine water undergoes condensation polymerization with alcohols"],
         "Bromine water test: Alkenes rapidly decolourise reddish-brown Br₂ in the dark (addition). Alkanes do not react in the dark."),

        ("Potassium Permanganate Test (Baeyer's Test) for Unsaturation",
         "Purple acidified or alkaline potassium permanganate (KMnO₄) solution is rapidly DECOLOURISED (or forms a brown MnO₂ precipitate) by unsaturated alkenes, while saturated alkanes produce no color change.",
         ["Purple KMnO₄ turns bright yellow only when mixed with saturated alkanes",
          "KMnO₄ undergoes addition polymerization to form solid plastic polyethylene",
          "Both alkanes and alkenes turn purple KMnO₄ into clear green liquid immediately",
          "KMnO₄ converts alcohols into haloalkanes through substitution",
          "Saturated alkanes decolourise KMnO₄ while alkenes leave it unchanged",
          "KMnO₄ produces hydrogen gas bubbles with all non-polar hydrocarbons"],
         "Baeyer's test: Purple KMnO₄ is rapidly decolourised by unsaturated alkenes (oxidation), identifying double bonds.")
    ]

    for p_name, p_def, p_wrongs, p_expl in polymer_basics:
        for st_pb in [
            "What is the definition and scientific significance of **'{}'**?",
            "In Technical Sciences materials and organic chemistry, **'{}'** refers to:",
            "Which statement accurately explains **'{}'**?"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Polymers & Tests", st_pb.format(p_name), p_def, p_wrongs, "Remembering", f"Define {p_name}", p_expl)

    # Simple Molar Masses of Alkanes (filling easy to exactly 300)
    for alk_n, alk_sym in [
        (1, "CH4 (methane)"), (2, "C2H6 (ethane)"), (3, "C3H8 (propane)"),
        (4, "C4H10 (butane)"), (5, "C5H12 (pentane)"), (6, "C6H14 (hexane)"),
        (7, "C7H16 (heptane)"), (8, "C8H18 (octane)")
    ]:
        if counts["easy"] >= 300:
            break
        mm_c = alk_n * 12.0
        mm_h = (2 * alk_n + 2) * 1.0
        tot_mm = mm_c + mm_h
        c_mm = f"{tot_mm:.0f} g·mol⁻¹"
        w_mm = [
            f"{tot_mm * 2:.0f} g·mol⁻¹",
            f"{tot_mm / 2:.0f} g·mol⁻¹",
            f"{mm_c:.0f} g·mol⁻¹ (calculated mass of carbon only)",
            f"{tot_mm + 14:.0f} g·mol⁻¹",
            f"{tot_mm - 10:.0f} g·mol⁻¹",
            f"{alk_n * 10:.0f} g·mol⁻¹",
            f"{tot_mm + 28:.0f} g·mol⁻¹"
        ]
        q_text_mm = f"Given atomic masses C = 12 g·mol⁻¹ and H = 1 g·mol⁻¹, calculate the molar mass of **{alk_sym}**:"
        expl_mm = f"Molar mass of {alk_sym}: ({alk_n} × 12) + ({2 * alk_n + 2} × 1) = {mm_c:.0f} + {mm_h:.0f} = {c_mm}."
        add_q("easy", "Molar Mass Calculations", q_text_mm, c_mm, w_mm, "Applying", f"Calculate molar mass of {alk_sym}", expl_mm)

    # General formula hydrogen count calculations (filling easy to 300)
    for n_c in range(2, 11):
        if counts["easy"] >= 300:
            break
        # Alkane
        h_alkane = 2 * n_c + 2
        q_alk = f"An alkane molecule contains exactly **{n_c} carbon atoms**. According to the general formula of alkanes (C_n H_{{2n+2}}), how many hydrogen atoms are present in the molecule?"
        c_alk = f"{h_alkane} hydrogen atoms"
        w_alk = [
            f"{2 * n_c} hydrogen atoms (formula of alkene: 2n)",
            f"{2 * n_c - 2} hydrogen atoms (formula of alkyne: 2n-2)",
            f"{n_c * 4} hydrogen atoms",
            f"{h_alkane + 4} hydrogen atoms",
            f"{h_alkane - 4} hydrogen atoms",
            f"{n_c + 2} hydrogen atoms",
            f"{h_alkane * 2} hydrogen atoms"
        ]
        add_q("easy", "Hydrocarbon Hydrogen Counts", q_alk, c_alk, w_alk, "Applying", f"Calculate hydrogens for C{n_c} alkane", f"Alkane formula C_n H_{{2n+2}}: 2({n_c}) + 2 = {h_alkane} hydrogen atoms.")

        # Alkene
        if counts["easy"] < 300:
            h_alkene = 2 * n_c
            q_ene = f"An alkene with a single double bond has **{n_c} carbon atoms**. Using the general formula for alkenes (C_n H_{{2n}}), determine the number of hydrogen atoms:"
            c_ene = f"{h_alkene} hydrogen atoms"
            w_ene = [
                f"{2 * n_c + 2} hydrogen atoms (formula of alkane)",
                f"{2 * n_c - 2} hydrogen atoms (formula of alkyne)",
                f"{n_c * 3} hydrogen atoms",
                f"{h_alkene + 2} hydrogen atoms",
                f"{h_alkene - 2} hydrogen atoms",
                f"{n_c} hydrogen atoms",
                f"{h_alkene * 2} hydrogen atoms"
            ]
            add_q("easy", "Hydrocarbon Hydrogen Counts", q_ene, c_ene, w_ene, "Applying", f"Calculate hydrogens for C{n_c} alkene", f"Alkene formula C_n H_{{2n}}: 2({n_c}) = {h_alkene} hydrogen atoms.")

    # Common Daily Applications of Organic Compounds (filling easy to 300)
    organic_daily_uses = [
        ("Methane (CH4)", "compressed natural gas (CNG) and primary component of domestic pipeline gas"),
        ("Propane (C3H8)", "liquefied petroleum gas (LPG) used in domestic gas cylinders and patio heaters"),
        ("Butane (C4H10)", "fuel in disposable cigarette lighters and portable camping gas stoves"),
        ("Ethanol (C2H5OH)", "hand sanitizer and medical disinfectant (70% v/v solution) and commercial solvent"),
        ("Ethanoic acid (CH3COOH)", "household culinary vinegar (dilute ~5% aqueous solution) and pickling agent"),
        ("Ethyl ethanoate (CH3COOCH2CH3)", "volatile non-toxic solvent used in commercial nail polish removers and glues"),
        ("Ethene (C2H4)", "commercial plant hormone used for artificial fruit ripening and monomer for polyethylene"),
        ("Ethyne / Acetylene (C2H2)", "high-temperature fuel gas burned with oxygen in oxy-acetylene welding torches"),
        ("Propan-2-ol (isopropyl alcohol)", "rubbing alcohol, electronics circuit cleaner, and lens disinfectant"),
        ("Polytetrafluoroethene (Teflon / PTFE)", "non-stick coating on cookware and chemical-resistant industrial gasket tape"),
        ("Polychloroethene (PVC)", "rigid municipal water supply pipes, window frames, and flexible wire insulation"),
        ("Expanded Polystyrene (EPS)", "thermal insulation cooler boxes, protective electronics packaging, and coffee cups")
    ]

    for comp_u_name, comp_u_role in organic_daily_uses:
        for st_use in [
            f"What is the primary industrial or domestic application of **{comp_u_name}**?",
            f"In practical technology, **{comp_u_name}** is commonly employed as:",
            f"Which statement correctly identifies the commercial role of **{comp_u_name}**?"
        ]:
            if counts["easy"] >= 300:
                break
            c_u = f"It is widely used as {comp_u_role}."
            w_u = [
                "It is used exclusively as an inorganic electrolyte in car lead-acid batteries.",
                "It is used as a nuclear fuel in pebble-bed fission reactors.",
                "It is used as a high-voltage superconductor operating at room temperature.",
                "It is used to extract gold metal from quartz ore using cyanide leaching.",
                "It is used as an explosive gunpowder propellant in firearms.",
                "It is used as a magnetic shielding material in MRI scanners."
            ]
            add_q("easy", "Commercial Applications", st_use, c_u, w_u, "Remembering", f"Identify application of {comp_u_name}", c_u)

    # Core Physical Concepts (Topping Easy to 300)
    for term_p, def_p, wr_p, expl_p in [
        ("IUPAC acronym",
         "International Union of Pure and Applied Chemistry, the recognized global organization that establishes standardized chemical nomenclature and terminology.",
         ["International Union of Professional Applied Ceramics",
          "Intercontinental Association of Pure Alkaline Compounds",
          "Institute of Universal Physics and Applied Chemistry",
          "International Unit for Physical and Atomic Charges",
          "Intergovernmental Union of Petrochemical Analytical Chemists",
          "Internal Unified Protocol for Acid Concentrations"],
         "IUPAC stands for the International Union of Pure and Applied Chemistry."),

        ("Volatility of an organic liquid",
         "The ease with which a liquid vaporizes or evaporates at room temperature, determined by the strength of its intermolecular forces (liquids with weak London forces and high vapor pressures are highly volatile).",
         ["The speed at which an acid neutralizes a base in water",
          "The electrical conductivity of an organic compound in solution",
          "The ability of a plastic to stretch without snapping",
          "The resistance of a liquid to flow through a narrow capillary tube",
          "The percentage of carbon atoms present in a polymer chain",
          "The tendency of an alkane to decompose into free radicals"],
         "Volatility is the tendency of a substance to evaporate; weaker IMFs -> higher volatility."),

        ("Vapor Pressure",
         "The pressure exerted by a vapor in dynamic equilibrium with its liquid phase in a closed system at a given temperature.",
         ["The atmospheric pressure exerted on a boiling liquid",
          "The pressure required to liquefy methane gas at room temperature",
          "The pressure inside an automotive tyre at elevated speeds",
          "The osmotic pressure across a semi-permeable cell membrane",
          "The partial pressure of oxygen in an oxy-acetylene torch",
          "The pressure drop measured across a dirty fuel filter"],
         "Vapor pressure is the pressure exerted by a vapor in equilibrium with its liquid in a closed container at a given temperature.")
    ]:
        for st_p_easy in [
            "In Grade 12 Technical Sciences, what does **'{}'** mean?",
            "Identify the accurate definition of **'{}'**:"
        ]:
            if counts["easy"] >= 300:
                break
            add_q("easy", "Physical Concepts", st_p_easy.format(term_p), def_p, wr_p, "Remembering", f"Define {term_p}", expl_p)

    # =========================================================================
    # 2. MEDIUM (Target: 500 Questions)
    # IUPAC Naming, Molecular/Structural Formulas, Isomerism, Reactions, Physical Properties
    # =========================================================================

    # 1. IUPAC Naming of Alkanes, Haloalkanes, Alcohols, Carboxylic Acids, Esters
    compounds_iupac = [
        # Branched Alkanes
        ("CH3-CH(CH3)-CH3", "2-methylpropane", ["butane", "1-methylpropane", "2-methylbutane", "propane", "tetramethylmethane", "dimethylethane", "isobutene"],
         "Longest continuous chain has 3 carbons (propane). A methyl branch is on carbon-2 -> 2-methylpropane."),
        ("CH3-CH(CH3)-CH2-CH3", "2-methylbutane", ["3-methylbutane", "pentane", "2-ethylpropane", "dimethylpropane", "2-methylpentane", "propylmethane", "hexane"],
         "Longest continuous chain has 4 carbons (butane). Numbering from left gives methyl at C2 -> 2-methylbutane."),
        ("CH3-C(CH3)2-CH3", "2,2-dimethylpropane", ["2-dimethylpropane", "pentane", "2,2-methylpropane", "tetramethylmethane", "2-ethylpropane", "1,1-dimethylpropane", "neopentane"],
         "Longest continuous chain has 3 carbons (propane). Two methyl branches on carbon-2 -> 2,2-dimethylpropane."),
        ("CH3-CH(CH3)-CH(CH3)-CH3", "2,3-dimethylbutane", ["2,3-methylbutane", "hexane", "2,3-dimethylpropane", "diisopropyl", "1,2-dimethylbutane", "3,4-dimethylbutane", "2-ethylbutane"],
         "Longest chain has 4 carbons (butane). Methyl branches on C2 and C3 -> 2,3-dimethylbutane."),
        ("CH3-C(CH3)2-CH2-CH3", "2,2-dimethylbutane", ["3,3-dimethylbutane", "hexane", "2-dimethylbutane", "2-ethylbutane", "2,2-ethylpropane", "dimethylbutane", "isohexane"],
         "Longest chain has 4 carbons (butane). Numbering from left gives two methyls at C2 -> 2,2-dimethylbutane."),
        ("CH3-CH2-CH(CH3)-CH2-CH3", "3-methylpentane", ["2-methylpentane", "hexane", "3-ethylbutane", "2-ethylbutane", "methylpentane", "3-propylpropane", "heptane"],
         "Longest chain has 5 carbons (pentane). Methyl branch on carbon-3 -> 3-methylpentane."),
        ("CH3-CH(CH3)-CH2-CH2-CH3", "2-methylpentane", ["4-methylpentane", "hexane", "2-ethylbutane", "3-methylpentane", "2-propylpropane", "dimethylbutane", "heptane"],
         "Longest chain has 5 carbons (pentane). Numbering from left gives lowest locant C2 -> 2-methylpentane."),
        ("CH3-C(CH3)2-CH2-CH2-CH3", "2,2-dimethylpentane", ["4,4-dimethylpentane", "heptane", "2,2-methylpentane", "2-ethylpentane", "dimethylpentane", "3,3-dimethylpentane", "octane"],
         "Longest chain has 5 carbons (pentane). Two methyl branches at C2 -> 2,2-dimethylpentane."),

        # Haloalkanes
        ("CH3-CH2-Cl", "chloroethane", ["1-chloromethane", "dichloroethane", "chloroethene", "ethyl chloride", "chloropropane", "chlorobutane", "1-chloroethane"],
         "Two-carbon alkane with one chlorine atom -> chloroethane."),
        ("CH3-CH2-CH2-Br", "1-bromopropane", ["2-bromopropane", "bromopropane", "3-bromopropane", "bromobutane", "1-bromoethane", "propyl bromide", "dibromopropane"],
         "Three-carbon chain numbered from right gives bromine at C1 -> 1-bromopropane."),
        ("CH3-CH(Br)-CH3", "2-bromopropane", ["1-bromopropane", "bromopropane", "2-bromoethane", "isopropyl bromide", "bromobutane", "2-bromobutane", "dibromopropane"],
         "Three-carbon chain with bromine on central carbon-2 -> 2-bromopropane."),
        ("CH3-CH(Cl)-CH2-CH3", "2-chlorobutane", ["3-chlorobutane", "1-chlorobutane", "chlorobutane", "2-chloropropane", "2-chloropentane", "dichlorobutane", "sec-butyl chloride"],
         "Four-carbon chain numbered from left gives chlorine at C2 -> 2-chlorobutane."),
        ("CH3-C(CH3)(Cl)-CH3", "2-chloro-2-methylpropane", ["2-chloro-2-methylbutane", "1-chloro-2-methylpropane", "2-chlorobutane", "chloro-tert-butane", "2-methyl-2-chloropropane", "3-chlorobutane", "chloropropane"],
         "Three-carbon chain (propane) with chloro and methyl both on carbon-2 -> 2-chloro-2-methylpropane (alphabetical: chloro before methyl)."),
        ("CH2(Br)-CH2(Br)", "1,2-dibromoethane", ["1,1-dibromoethane", "dibromoethane", "bromoethane", "1,2-bromoethane", "dibromoethene", "1,2-dibromopropane", "ethylene bromide"],
         "Two-carbon chain with bromine atoms on carbon-1 and carbon-2 -> 1,2-dibromoethane."),

        # Alkenes
        ("CH2=CH-CH2-CH3", "but-1-ene", ["but-2-ene", "butene", "but-3-ene", "prop-1-ene", "pent-1-ene", "1-butene", "but-1-yne"],
         "Four-carbon chain with double bond starting at carbon-1 -> but-1-ene."),
        ("CH3-CH=CH-CH3", "but-2-ene", ["but-1-ene", "butene", "2-butene", "prop-2-ene", "pent-2-ene", "but-2-yne", "dimethylethene"],
         "Four-carbon chain with double bond between carbon-2 and carbon-3 -> but-2-ene."),
        ("CH2=C(CH3)-CH3", "2-methylprop-1-ene", ["2-methylprop-2-ene", "methylpropene", "but-2-ene", "1-methylprop-1-ene", "2-methylbutene", "isobutane", "prop-1-ene"],
         "Three-carbon parent chain with double bond at C1 and methyl on C2 -> 2-methylprop-1-ene."),
        ("CH2=CH-CH2-CH2-CH3", "pent-1-ene", ["pent-2-ene", "pentene", "pent-4-ene", "but-1-ene", "hex-1-ene", "1-pentene", "pent-1-yne"],
         "Five-carbon chain with double bond at carbon-1 -> pent-1-ene."),
        ("CH3-CH=CH-CH2-CH3", "pent-2-ene", ["pent-3-ene", "pent-1-ene", "pentene", "2-pentene", "hex-2-ene", "but-2-ene", "pent-2-yne"],
         "Five-carbon chain numbered from left gives double bond at C2 -> pent-2-ene."),

        # Alcohols
        ("CH3-CH2-OH", "ethanol", ["methanol", "ethan-2-ol", "propan-1-ol", "ethene", "ethanoic acid", "ethyl ether", "ethanal"],
         "Two-carbon parent chain with -OH group -> ethanol."),
        ("CH3-CH2-CH2-OH", "propan-1-ol", ["propan-2-ol", "propanol", "propan-3-ol", "ethanol", "butan-1-ol", "propanoic acid", "propanal"],
         "Three-carbon chain with -OH on carbon-1 -> propan-1-ol."),
        ("CH3-CH(OH)-CH3", "propan-2-ol", ["propan-1-ol", "propanol", "isopropanol", "butan-2-ol", "propan-2-one", "propanoic acid", "2-hydroxypropane"],
         "Three-carbon chain with -OH on central carbon-2 -> propan-2-ol."),
        ("CH3-CH2-CH2-CH2-OH", "butan-1-ol", ["butan-2-ol", "butanol", "butan-4-ol", "propan-1-ol", "pentan-1-ol", "butanoic acid", "butanal"],
         "Four-carbon chain with -OH on carbon-1 -> butan-1-ol."),
        ("CH3-CH(OH)-CH2-CH3", "butan-2-ol", ["butan-3-ol", "butan-1-ol", "butanol", "2-butanol", "sec-butanol", "butan-2-one", "pentan-2-ol"],
         "Four-carbon chain numbered from left gives -OH on C2 -> butan-2-ol."),
        ("CH3-C(CH3)(OH)-CH3", "2-methylpropan-2-ol", ["2-methylpropan-1-ol", "butan-2-ol", "tert-butanol", "2-methylpropanol", "2,2-dimethylpropanol", "butan-1-ol", "2-methylbutan-2-ol"],
         "Three-carbon parent chain with -OH and methyl both on carbon-2 -> 2-methylpropan-2-ol."),

        # Carboxylic Acids
        ("H-COOH", "methanoic acid", ["ethanoic acid", "formic acid", "methanol", "methanal", "propanoic acid", "carbonic acid", "methanoate"],
         "One-carbon carboxylic acid -> methanoic acid."),
        ("CH3-COOH", "ethanoic acid", ["methanoic acid", "acetic acid", "propanoic acid", "ethanol", "ethanal", "ethyl ethanoate", "butanoic acid"],
         "Two-carbon carboxylic acid -> ethanoic acid."),
        ("CH3-CH2-COOH", "propanoic acid", ["ethanoic acid", "butanoic acid", "propanoic ester", "propan-1-ol", "propanal", "propionate", "pentanoic acid"],
         "Three-carbon carboxylic acid -> propanoic acid."),
        ("CH3-CH2-CH2-COOH", "butanoic acid", ["propanoic acid", "pentanoic acid", "butan-1-ol", "butanoic ester", "butanal", "butyric acid", "hexanoic acid"],
         "Four-carbon carboxylic acid -> butanoic acid."),
        ("CH3-CH(CH3)-COOH", "2-methylpropanoic acid", ["3-methylpropanoic acid", "butanoic acid", "2-methylbutanoic acid", "methylpropanoic acid", "isobutanoic acid", "propanoic acid", "pentanoic acid"],
         "Three-carbon parent chain with methyl branch on carbon-2 -> 2-methylpropanoic acid."),

        # Esters
        ("CH3-COO-CH3", "methyl ethanoate", ["ethyl methanoate", "dimethyl ester", "methyl acetate", "ethyl ethanoate", "ethanoic acid", "propyl methanoate", "methyl propanoate"],
         "Formed from ethanoic acid (ethanoate part) and methanol (methyl part) -> methyl ethanoate."),
        ("CH3-COO-CH2-CH3", "ethyl ethanoate", ["methyl propanoate", "propyl ethanoate", "ethyl propanoate", "diethyl ester", "butyl ethanoate", "ethyl acetate", "ethanoic acid"],
         "Formed from ethanoic acid and ethanol -> ethyl ethanoate."),
        ("H-COO-CH2-CH3", "ethyl methanoate", ["methyl ethanoate", "ethyl ethanoic acid", "propyl methanoate", "ethyl formate", "ethanoic acid", "methyl propanoate", "ethyl propanoate"],
         "Formed from methanoic acid (methanoate) and ethanol (ethyl) -> ethyl methanoate."),
        ("CH3-CH2-COO-CH3", "methyl propanoate", ["ethyl ethanoate", "propyl methanoate", "methyl ethanoic acid", "propyl ethanoate", "ethyl propanoate", "methyl butanoate", "butanoic acid"],
         "Formed from propanoic acid (propanoate) and methanol (methyl) -> methyl propanoate."),
        ("CH3-COO-CH2-CH2-CH3", "propyl ethanoate", ["ethyl propanoate", "butyl ethanoate", "methyl butanoate", "propyl acetate", "pentanoate", "ethyl ethanoate", "propyl propanoate"],
         "Formed from ethanoic acid and propan-1-ol -> propyl ethanoate.")
    ]

    for struct_f, corr_iupac, wr_iupacs, exp_iupac in compounds_iupac:
        for q_st_i in [
            f"What is the correct IUPAC name for the organic compound with structural condensed formula **{struct_f}**?",
            f"According to IUPAC nomenclature guidelines, identify the systematic name of **{struct_f}**:",
            f"Give the correct IUPAC name for the molecule represented by: **{struct_f}**"
        ]:
            if counts["medium"] >= 500:
                break
            add_q("medium", "IUPAC Nomenclature", q_st_i, corr_iupac, wr_iupacs, "Applying", f"Name {corr_iupac} using IUPAC rules", exp_iupac)

    # 2. Esterification Reactants and Products: Acid + Alcohol -> Ester + Water
    ester_reactions = [
        ("ethanoic acid (CH3COOH)", "methanol (CH3OH)", "methyl ethanoate (CH3COOCH3) + water (H2O)", "sweet apple/glue fragrance"),
        ("ethanoic acid (CH3COOH)", "ethanol (CH3CH2OH)", "ethyl ethanoate (CH3COOCH2CH3) + water (H2O)", "fruity pear/nail polish remover aroma"),
        ("methanoic acid (HCOOH)", "ethanol (CH3CH2OH)", "ethyl methanoate (HCOOCH2CH3) + water (H2O)", "rum/raspberry fragrance"),
        ("propanoic acid (CH3CH2COOH)", "methanol (CH3OH)", "methyl propanoate (CH3CH2COOCH3) + water (H2O)", "sweet fruity rum-like aroma"),
        ("ethanoic acid (CH3COOH)", "propan-1-ol (CH3CH2CH2OH)", "propyl ethanoate (CH3COOCH2CH2CH3) + water (H2O)", "distinct pear fragrance"),
        ("butanoic acid (CH3CH2CH2COOH)", "ethanol (CH3CH2OH)", "ethyl butanoate (CH3CH2CH2COOCH2CH3) + water (H2O)", "strong pineapple aroma"),
        ("butanoic acid (CH3CH2CH2COOH)", "methanol (CH3OH)", "methyl butanoate (CH3CH2CH2COOCH3) + water (H2O)", "apple aroma"),
        ("ethanoic acid (CH3COOH)", "pentan-1-ol (CH3(CH2)4OH)", "pentyl ethanoate (CH3COO(CH2)4CH3) + water (H2O)", "distinct banana scent")
    ]

    for acid_r, alc_r, ester_prod, odor_desc in ester_reactions:
        for q_st_e in [
            f"When **{acid_r}** is heated gently with **{alc_r}** in the presence of concentrated sulfuric acid (H₂SO₄), what are the organic and inorganic products formed?",
            f"Identify the products of the esterification reaction between **{acid_r}** and **{alc_r}**:",
            f"An industrial technician synthesizes a fragrance ({odor_desc}) by reacting **{acid_r}** with **{alc_r}**. What products are obtained?"
        ]:
            if counts["medium"] >= 500:
                break
            c_est = f"It produces {ester_prod}."
            w_est = [
                f"It produces an alkene, carbon dioxide, and sodium sulfate.",
                f"It produces an alkane and hydrogen gas through addition.",
                f"It produces a haloalkane and sulfur trioxide fumes.",
                f"It produces an ether and toxic chlorine gas.",
                f"It produces an aldehyde, hydrogen peroxide, and carbon soot.",
                f"It produces an alkyne and aqueous sulfuric acid."
            ]
            exp_est = f"Esterification: {acid_r} + {alc_r} (catalysed by conc. H₂SO₄) -> {ester_prod}."
            add_q("medium", "Esterification Reactions", q_st_e, c_est, w_est, "Applying", "Predict products of esterification", exp_est)

    # 3. Addition, Substitution & Elimination Reaction Predictions (Medium)
    reaction_predictions = [
        ("Ethene (CH2=CH2) reacting with Bromine (Br2)",
         "1,2-dibromoethane (CH2Br-CH2Br)",
         ["bromoethane", "1,1-dibromoethane", "bromoethene", "dibromoethene", "ethane + HBr", "bromomethane", "1,2-dibromoethene"],
         "Addition reaction: Br₂ adds across the C=C double bond -> 1,2-dibromoethane."),

        ("Ethene (CH2=CH2) reacting with Hydrogen chloride (HCl)",
         "chloroethane (CH3CH2Cl)",
         ["1,2-dichloroethane", "1,1-dichloroethane", "chloroethene", "ethane + Cl₂", "chloromethane", "chloropropane", "dichloroethene"],
         "Addition (hydrohalogenation): HCl adds across the C=C double bond -> chloroethane."),

        ("Ethene (CH2=CH2) reacting with Steam (H2O) in the presence of H3PO4 catalyst",
         "ethanol (CH3CH2OH)",
         ["ethanoic acid", "ethanal", "ethane + O₂", "methoxymethane", "1,2-ethanediol", "propan-1-ol", "ethenol"],
         "Addition (hydration): H₂O adds across the C=C double bond in the presence of acid catalyst -> ethanol."),

        ("Propene (CH3-CH=CH2) reacting with Hydrogen bromide (HBr) according to Markovnikov's rule",
         "2-bromopropane (CH3-CHBr-CH3) as the major product",
         ["1-bromopropane as major product", "1,2-dibromopropane", "bromopropene", "propane + Br₂", "2-bromopropene", "bromoethane", "1,3-dibromopropane"],
         "Markovnikov addition: Hydrogen adds to the carbon with more hydrogens (C1), and Br adds to C2 -> 2-bromopropane (major product)."),

        ("Propene (CH3-CH=CH2) reacting with Water (H2O) in the presence of H2SO4 catalyst",
         "propan-2-ol (CH3-CH(OH)-CH3) as the major product",
         ["propan-1-ol as major product", "propanoic acid", "propanal", "propan-2-one", "prop-2-en-1-ol", "ethanol", "glycerol"],
         "Hydration of propene follows Markovnikov's rule: -OH adds to C2 -> propan-2-ol (major product)."),

        ("2-chlorobutane (CH3-CH(Cl)-CH2-CH3) heated with concentrated NaOH in ethanol (reflux)",
         "but-2-ene (CH3-CH=CH-CH3) as the major product (Zaitsev's rule) + NaCl + H2O",
         ["but-1-ene as the exclusive product", "butan-2-ol + NaCl", "butan-1-ol + HCl", "butane + Cl₂", "but-2-yne + NaCl", "chlorobut-2-ene", "2-chlorobut-2-ene"],
         "Dehydrohalogenation elimination: H is preferentially removed from the C with fewer hydrogens (C3), forming the more substituted but-2-ene (major product)."),

        ("Butan-2-ol (CH3-CH(OH)-CH2-CH3) heated with concentrated sulfuric acid (H2SO4)",
         "but-2-ene (CH3-CH=CH-CH3) as the major product + H2O",
         ["but-1-ene as exclusive product", "butane + O₂", "butanoic acid + H₂", "butan-2-one + H₂O", "but-2-yne + H₂O", "diethyl ether", "1,2-butanediol"],
         "Dehydration elimination of butan-2-ol follows Zaitsev's rule, yielding the more stable, more substituted but-2-ene as the major product."),

        ("1-bromopropane (CH3-CH2-CH2-Br) heated gently with dilute aqueous sodium hydroxide (NaOH)",
         "propan-1-ol (CH3-CH2-CH2-OH) + NaBr",
         ["propene + NaBr + H₂O (elimination)", "propan-2-ol + NaBr", "propanoic acid + H₂", "propane + Br₂", "bromopropene + NaOH", "propanal + NaBr", "propyl sodium"],
         "Hydrolysis (substitution): Dilute aqueous base and gentle heat favor substitution: Br is replaced by -OH, producing propan-1-ol + NaBr.")
    ]

    for rx_in, corr_out, wr_outs, exp_rx in reaction_predictions:
        for q_st_p in [
            f"Predict the principal organic product when **{rx_in}** undergoes reaction:",
            f"What is the major organic product formed in the following reaction: **{rx_in}**?",
            f"Identify the resulting organic compound when **{rx_in}**:"
        ]:
            if counts["medium"] >= 500:
                break
            add_q("medium", "Reaction Product Prediction", q_st_p, corr_out, wr_outs, "Applying", "Predict organic reaction major product", exp_rx)

    # 4. Boiling Point and Physical Property Comparisons (Medium)
    physical_comparisons = [
        ("Ethane vs Butane vs Octane",
         "Octane has the highest boiling point because it has the longest carbon chain (highest molecular mass), which provides a larger surface contact area and significantly stronger London dispersion forces.",
         ["Ethane has the highest boiling point because small molecules pack tighter into crystals",
          "All three have identical boiling points because they belong to the alkane series",
          "Butane has the highest boiling point because it has an even number of carbon atoms",
          "Octane has the lowest boiling point because heavy molecules vaporize faster",
          "Ethane has the highest boiling point due to strong intermolecular hydrogen bonding",
          "Octane has the lowest boiling point because London forces weaken with chain length"],
         "London dispersion forces increase in strength with increasing chain length and molecular mass -> Octane has the highest boiling point."),

        ("Pentane vs 2-methylbutane vs 2,2-dimethylpropane (Chain Isomers of C5H12)",
         "Pentane (unbranched straight chain) has the HIGHEST boiling point; 2,2-dimethylpropane (most spherical and branched) has the LOWEST boiling point because branching reduces surface contact area and weakens London dispersion forces.",
         ["2,2-dimethylpropane has the highest boiling point because branches act as physical hooks",
          "All three isomers have identical boiling points because their molecular formulas are identical",
          "2-methylbutane has the highest boiling point because unsymmetrical molecules are ionic",
          "Pentane has the lowest boiling point because straight chains experience zero intermolecular forces",
          "Branching increases intermolecular force strength, raising the boiling point of 2,2-dimethylpropane",
          "2,2-dimethylpropane forms intermolecular hydrogen bonds, giving it the highest boiling point"],
         "Branching makes molecules more spherical, reducing contact area and weakening London forces -> Pentane (highest BP) > 2-methylbutane > 2,2-dimethylpropane (lowest BP)."),

        ("Propane (alkane, 44 g/mol) vs 1-chloropropane (haloalkane, 78.5 g/mol) vs Propan-1-ol (alcohol, 60 g/mol)",
         "Propan-1-ol has the HIGHEST boiling point because its molecules are held together by strong intermolecular HYDROGEN BONDS, whereas 1-chloropropane has dipole-dipole forces, and propane has only weak London dispersion forces.",
         ["Propane has the highest boiling point because hydrocarbons are non-polar",
          "1-chloropropane has the highest boiling point because chlorine has the largest atomic mass",
          "All three have identical boiling points because each contains three carbon atoms",
          "Propane has the lowest vapor pressure because non-polar molecules resist evaporation",
          "Propan-1-ol has the lowest boiling point because hydrogen bonds evaporate spontaneously",
          "1-chloropropane forms covalent network bonds in the liquid state"],
         "IMF strength comparison: Hydrogen bonding (alcohol) > Dipole-dipole (haloalkane) > London forces (alkane). Stronger IMF -> higher boiling point -> Propan-1-ol has the highest BP."),

        ("Propan-1-ol (alcohol) vs Propanoic acid (carboxylic acid)",
         "Propanoic acid has a HIGHER boiling point than propan-1-ol of similar molecular mass because carboxylic acid molecules can form TWO hydrogen bonds per pair of molecules, forming stable dimers with exceptionally strong intermolecular attractions.",
         ["Propan-1-ol has a higher boiling point because alcohols have stronger hydrogen bonds",
          "Both have identical boiling points because both contain polar oxygen atoms",
          "Propanoic acid has a lower boiling point because acids are volatile liquids",
          "Propan-1-ol has a higher boiling point because carboxylic acids cannot form hydrogen bonds",
          "Propanoic acid has a lower boiling point because its molecules experience only London forces",
          "Propan-1-ol forms ionic bonds in the pure liquid phase while propanoic acid does not"],
         "Carboxylic acids form dimers via two hydrogen bonds per molecule pair, requiring more thermal energy to separate -> Propanoic acid has a higher BP than propan-1-ol.")
    ]

    for comp_title, comp_corr, comp_wrongs, comp_expl in physical_comparisons:
        for st_cmp in [
            "Explain the boiling point and vapor pressure trends for: **{}**",
            "Consider the physical properties of **{}**. Which deduction is scientifically correct?",
            "In terms of intermolecular forces and molecular structure, compare: **{}**"
        ]:
            if counts["medium"] >= 500:
                break
            add_q("medium", "Physical Properties & IMF", st_cmp.format(comp_title), comp_corr, comp_wrongs, "Understanding", "Compare boiling points and intermolecular forces", comp_expl)

    # 5. Isomer Classification: Chain, Positional, Functional (Medium)
    isomer_pairs = [
        ("Butane and 2-methylpropane (both C4H10)", "CHAIN ISOMERS because they have the same molecular formula but different branching of their carbon skeletons"),
        ("Pentane, 2-methylbutane, and 2,2-dimethylpropane (all C5H12)", "CHAIN ISOMERS because they have the same molecular formula but different carbon chain arrangements"),
        ("Butan-1-ol and butan-2-ol (both C4H10O)", "POSITIONAL ISOMERS because they have the same parent chain but the hydroxyl group is located at different carbon positions (C1 vs C2)"),
        ("Propan-1-ol and propan-2-ol (both C3H8O)", "POSITIONAL ISOMERS because the -OH functional group is on carbon-1 in propan-1-ol and carbon-2 in propan-2-ol"),
        ("But-1-ene and but-2-ene (both C4H8)", "POSITIONAL ISOMERS because the carbon-carbon double bond is located at different positions along the 4-carbon chain"),
        ("1-chloropropane and 2-chloropropane (both C3H7Cl)", "POSITIONAL ISOMERS because the chlorine substituent is bonded to carbon-1 in one and carbon-2 in the other"),
        ("Propanoic acid (CH3CH2COOH) and methyl ethanoate (CH3COOCH3) (both C3H6O2)", "FUNCTIONAL ISOMERS because they share the same molecular formula (C3H6O2) but have different functional groups (carboxylic acid vs ester)"),
        ("Butanoic acid (C4H8O2) and ethyl ethanoate (C4H8O2)", "FUNCTIONAL ISOMERS because both have molecular formula C4H8O2 but belong to different homologous series (carboxylic acid vs ester)"),
        ("Ethanoic acid (C2H4O2) and methyl methanoate (C2H4O2)", "FUNCTIONAL ISOMERS because they have identical molecular formulas (C2H4O2) but represent a carboxylic acid and an ester respectively")
    ]

    for iso_names, iso_class in isomer_pairs:
        for q_st_iso in [
            f"How are the compounds **{iso_names}** classified in relation to one another?",
            f"Identify the specific type of structural isomerism exhibited by **{iso_names}**:",
            f"In Grade 12 Technical Sciences, **{iso_names}** are classified as:"
        ]:
            if counts["medium"] >= 500:
                break
            c_iso = f"They are {iso_class}."
            w_iso = [
                "They are allotropes of carbon with identical crystalline packing.",
                "They are identical identical molecules with different common trade names.",
                "They are homologues differing by a -CH₂- unit in their molecular formula.",
                "They are geometrical stereoisomers caused by restricted double bond rotation.",
                "They are polymer macromolecular units formed by condensation reactions.",
                "They are cracking fragments that cannot exist as stable independent compounds."
            ]
            add_q("medium", "Isomerism", q_st_iso, c_iso, w_iso, "Understanding", "Classify structural isomers", c_iso)

    # Systematic 16 Esters Matrix (Medium)
    acids_matrix = [
        ("methanoic acid", "H-COOH", "methanoate", "H-COO-"),
        ("ethanoic acid", "CH3-COOH", "ethanoate", "CH3-COO-"),
        ("propanoic acid", "CH3-CH2-COOH", "propanoate", "CH3-CH2-COO-"),
        ("butanoic acid", "CH3-CH2-CH2-COOH", "butanoate", "CH3-CH2-CH2-COO-")
    ]
    alcohols_matrix = [
        ("methanol", "CH3-OH", "methyl", "-CH3"),
        ("ethanol", "CH3-CH2-OH", "ethyl", "-CH2-CH3"),
        ("propan-1-ol", "CH3-CH2-CH2-OH", "propyl", "-CH2-CH2-CH3"),
        ("butan-1-ol", "CH3-CH2-CH2-CH2-OH", "butyl", "-CH2-CH2-CH2-CH3")
    ]

    for ac_name, ac_form, ac_suffix, ac_part in acids_matrix:
        for al_name, al_form, al_prefix, al_part in alcohols_matrix:
            if counts["medium"] >= 500:
                break
            ester_iupac = f"{al_prefix} {ac_suffix}"
            ester_formula = f"{ac_part}{al_part.lstrip('-')}"
            c_est_m = ester_iupac
            w_est_m = [
                f"{ac_suffix.replace('ate', 'yl')} {al_prefix}ate (inverted acid and alcohol parts)",
                f"{al_prefix} {ac_name.split()[0]}ic ether",
                f"{al_prefix} {ac_suffix}ic acid",
                f"di{al_prefix} ester",
                f"{al_prefix} ketone",
                f"{ac_name.split()[0]} {al_prefix}anoate",
                f"{al_prefix} {ac_suffix}al"
            ]
            q_est_m = f"What is the IUPAC name of the ester formed when **{ac_name}** ({ac_form}) reacts with **{al_name}** ({al_form}) in the presence of concentrated sulfuric acid catalyst?"
            expl_est_m = f"Esterification: {ac_name} + {al_name} -> {ester_iupac} ({ester_formula}) + H₂O (alkyl group from alcohol: {al_prefix}; carboxylate group from acid: {ac_suffix})."
            add_q("medium", "Ester Identification & IUPAC", q_est_m, c_est_m, w_est_m, "Applying", f"Name ester {ester_iupac}", expl_est_m)

            if counts["medium"] < 500:
                q_est_react = f"An analytical chemist hydrolyzes the synthetic ester **{ester_iupac}** ({ester_formula}). What are the parent carboxylic acid and alcohol from which this ester was originally prepared?"
                c_est_react = f"Carboxylic acid: {ac_name}; Alcohol: {al_name}."
                w_est_react = [
                    f"Carboxylic acid: {al_name.replace('ol', 'oic acid')}; Alcohol: {ac_name.replace('oic acid', 'ol')}.",
                    f"Carboxylic acid: methanoic acid; Alcohol: propan-2-ol.",
                    f"Carboxylic acid: ethanoic acid; Alcohol: butan-2-ol.",
                    f"Carboxylic acid: carbonic acid; Alcohol: methanol.",
                    f"Carboxylic acid: sulfuric acid; Alcohol: {al_name}.",
                    f"Carboxylic acid: {ac_name}; Alcohol: water."
                ]
                expl_est_react = f"{ester_iupac} is derived from {ac_name} (the acyl portion {ac_part}) and {al_name} (the alkoxy portion {al_part})."
                add_q("medium", "Ester Precursors", q_est_react, c_est_react, w_est_react, "Applying", f"Identify reactants for {ester_iupac}", expl_est_react)

    # Systematic Haloalkanes Reactions and IUPAC (Medium)
    haloalkanes_matrix = [
        ("CH3-CH2-CH2-Cl", "1-chloropropane", "PRIMARY", "propene", "propan-1-ol"),
        ("CH3-CH(Cl)-CH3", "2-chloropropane", "SECONDARY", "propene", "propan-2-ol"),
        ("CH3-CH2-CH2-Br", "1-bromopropane", "PRIMARY", "propene", "propan-1-ol"),
        ("CH3-CH(Br)-CH3", "2-bromopropane", "SECONDARY", "propene", "propan-2-ol"),
        ("CH3-CH2-CH2-CH2-Cl", "1-chlorobutane", "PRIMARY", "but-1-ene", "butan-1-ol"),
        ("CH3-CH(Cl)-CH2-CH3", "2-chlorobutane", "SECONDARY", "but-2-ene (major)", "butan-2-ol"),
        ("CH3-CH(CH3)-CH2-Cl", "1-chloro-2-methylpropane", "PRIMARY", "2-methylprop-1-ene", "2-methylpropan-1-ol"),
        ("CH3-C(CH3)(Cl)-CH3", "2-chloro-2-methylpropane", "TERTIARY", "2-methylprop-1-ene", "2-methylpropan-2-ol"),
        ("CH3-CH2-CH2-CH2-Br", "1-bromobutane", "PRIMARY", "but-1-ene", "butan-1-ol"),
        ("CH3-CH(Br)-CH2-CH3", "2-bromobutane", "SECONDARY", "but-2-ene (major)", "butan-2-ol"),
        ("CH3-C(CH3)(Br)-CH3", "2-bromo-2-methylpropane", "TERTIARY", "2-methylprop-1-ene", "2-bromo-2-methylpropanol"),
        ("CH3-CH2-CH2-CH2-CH2-Cl", "1-chloropentane", "PRIMARY", "pent-1-ene", "pentan-1-ol"),
        ("CH3-CH(Cl)-CH2-CH2-CH3", "2-chloropentane", "SECONDARY", "pent-2-ene (major)", "pentan-2-ol"),
        ("CH3-CH2-CH(Cl)-CH2-CH3", "3-chloropentane", "SECONDARY", "pent-2-ene", "pentan-3-ol")
    ]

    for h_form, h_iupac, h_class, h_elim, h_sub in haloalkanes_matrix:
        if counts["medium"] >= 500:
            break
        # Elimination question
        q_elim_m = f"The haloalkane **{h_iupac}** ({h_form}) is heated under reflux with concentrated sodium hydroxide (NaOH) dissolved in pure ethanol. Predict the primary organic alkene product formed via dehydrohalogenation:"
        c_elim_m = f"{h_elim}"
        w_elim_m = [
            f"{h_sub} (confused elimination with substitution)",
            f"propane gas + halogen",
            f"alkyne with triple bond",
            f"polychloroalkane",
            f"alkyl carboxylic acid",
            f"dimer ester",
            f"saturated alkane"
        ]
        expl_elim_m = f"Dehydrohalogenation elimination: {h_iupac} + hot conc. ethanolic NaOH -> {h_elim} + NaCl/NaBr + H₂O."
        add_q("medium", "Dehydrohalogenation Reactions", q_elim_m, c_elim_m, w_elim_m, "Applying", f"Predict elimination of {h_iupac}", expl_elim_m)

        # Substitution (hydrolysis) question
        if counts["medium"] < 500:
            q_sub_m = f"When **{h_iupac}** ({h_form}) is warmed gently with dilute aqueous sodium hydroxide (NaOH(aq)), which alcohol is produced as the main organic substitution product?"
            c_sub_m = f"{h_sub}"
            w_sub_m = [
                f"{h_elim} (confused substitution with elimination)",
                f"haloalkene",
                f"carboxylic acid",
                f"ketone",
                f"ester",
                f"ether",
                f"alkane"
            ]
            expl_sub_m = f"Hydrolysis substitution: {h_iupac} + dilute aqueous NaOH -> {h_sub} + NaX."
            add_q("medium", "Hydrolysis Substitution", q_sub_m, c_sub_m, w_sub_m, "Applying", f"Predict hydrolysis of {h_iupac}", expl_sub_m)

    # Combustion Equation Balancing (Medium)
    combustion_data = [
        ("Methane (CH4)", "CH4 + 2O2 → CO2 + 2H2O", "1 : 2", "1 mole of CO2 and 2 moles of H2O"),
        ("Ethane (C2H6)", "2C2H6 + 7O2 → 4CO2 + 6H2O", "2 : 7", "4 moles of CO2 and 6 moles of H2O"),
        ("Propane (C3H8)", "C3H8 + 5O2 → 3CO2 + 4H2O", "1 : 5", "3 moles of CO2 and 4 moles of H2O"),
        ("Butane (C4H10)", "2C4H10 + 13O2 → 8CO2 + 10H2O", "2 : 13", "8 moles of CO2 and 10 moles of H2O"),
        ("Pentane (C5H12)", "C5H12 + 8O2 → 5CO2 + 6H2O", "1 : 8", "5 moles of CO2 and 6 moles of H2O"),
        ("Hexane (C6H14)", "2C6H14 + 19O2 → 12CO2 + 14H2O", "2 : 19", "12 moles of CO2 and 14 moles of H2O"),
        ("Octane (C8H18)", "2C8H18 + 25O2 → 16CO2 + 18H2O", "2 : 25", "16 moles of CO2 and 18 moles of H2O"),
        ("Ethanol (C2H5OH)", "C2H5OH + 3O2 → 2CO2 + 3H2O", "1 : 3", "2 moles of CO2 and 3 moles of H2O"),
        ("Propan-1-ol (C3H7OH)", "2C3H7OH + 9O2 → 6CO2 + 8H2O", "2 : 9", "6 moles of CO2 and 8 moles of H2O")
    ]

    for fuel_name, bal_eq, mole_ratio, prod_moles in combustion_data:
        if counts["medium"] >= 500:
            break
        q_comb_m = f"What is the balanced chemical equation for the COMPLETE COMBUSTION of **{fuel_name}** in excess oxygen?"
        c_comb_m = f"{bal_eq}"
        w_comb_m = [
            bal_eq.replace("CO2", "CO"),
            bal_eq.replace("H2O", "H2"),
            bal_eq.replace("CO2", "C"),
            f"{fuel_name.split()[0]} + O₂ → CO₂ + H₂",
            f"{fuel_name.split()[0]} + 2O₂ → 2CO + 2H₂O",
            f"2{fuel_name.split()[0]} + O₂ → 2CO₂ + H₂O"
        ]
        expl_comb_m = f"Complete combustion of {fuel_name}: {bal_eq}. Produces {prod_moles}."
        add_q("medium", "Combustion Reactions", q_comb_m, c_comb_m, w_comb_m, "Applying", f"Balance combustion of {fuel_name}", expl_comb_m)

        if counts["medium"] < 500:
            q_ratio_m = f"According to the stoichiometric equation for complete combustion of **{fuel_name}**, what is the stoichiometric mole ratio of fuel to oxygen gas (O2)?"
            c_ratio_m = f"{mole_ratio}"
            w_ratio_m = [
                "1 : 1", "1 : 4", "2 : 5", "1 : 10", "3 : 8", "1 : 6", "2 : 3"
            ]
            expl_ratio_m = f"From the balanced equation {bal_eq}, the fuel to oxygen ratio is {mole_ratio}."
            add_q("medium", "Combustion Stoichiometry", q_ratio_m, c_ratio_m, w_ratio_m, "Applying", f"Stoichiometry of {fuel_name} combustion", expl_ratio_m)

    # Systematic IUPAC Naming & Classifications for Alcohols (Medium)
    alcohols_medium = [
        ("CH3-OH", "methanol", "PRIMARY", 32, "solvent and motor fuel blend"),
        ("CH3-CH2-OH", "ethanol", "PRIMARY", 46, "alcoholic beverages and industrial biofuel"),
        ("CH3-CH2-CH2-OH", "propan-1-ol", "PRIMARY", 60, "pharmaceutical solvent"),
        ("CH3-CH(OH)-CH3", "propan-2-ol", "SECONDARY", 60, "rubbing alcohol and antiseptic"),
        ("CH3-CH2-CH2-CH2-OH", "butan-1-ol", "PRIMARY", 74, "perfume solvent and lacquer diluent"),
        ("CH3-CH(OH)-CH2-CH3", "butan-2-ol", "SECONDARY", 74, "industrial cleaning agent"),
        ("CH3-CH(CH3)-CH2-OH", "2-methylpropan-1-ol", "PRIMARY", 74, "plasticizer precursor"),
        ("CH3-C(CH3)(OH)-CH3", "2-methylpropan-2-ol", "TERTIARY", 74, "octane booster in gasoline"),
        ("CH3-(CH2)4-OH", "pentan-1-ol", "PRIMARY", 88, "synthetic banana fragrance precursor"),
        ("CH3-CH(OH)-(CH2)2-CH3", "pentan-2-ol", "SECONDARY", 88, "specialty organic solvent"),
        ("CH3-CH2-CH(OH)-CH2-CH3", "pentan-3-ol", "SECONDARY", 88, "flavors and fragrances solvent"),
        ("CH3-C(CH3)(OH)-CH2-CH3", "2-methylbutan-2-ol", "TERTIARY", 88, "pharmaceutical hypnotic intermediate"),
        ("CH3-CH(CH3)-CH2-CH2-OH", "3-methylbutan-1-ol", "PRIMARY", 88, "isoamyl alcohol component"),
        ("CH3-(CH2)5-OH", "hexan-1-ol", "PRIMARY", 102, "seed oil extractant"),
        ("CH3-CH(OH)-(CH2)3-CH3", "hexan-2-ol", "SECONDARY", 102, "surfactant manufacturing")
    ]

    for alc_f_m, alc_name_m, alc_cls_m, alc_mm_m, alc_app_m in alcohols_medium:
        if counts["medium"] >= 500:
            break
        q_alc_name = f"What is the systematic IUPAC name and alcohol classification for the molecule with formula **{alc_f_m}**?"
        c_alc_name = f"{alc_name_m} ({alc_cls_m} alcohol)"
        w_alc_name = [
            f"{alc_name_m.replace('ol', 'al')} (aldehyde)",
            f"{alc_name_m.replace('ol', 'oic acid')} (carboxylic acid)",
            f"{alc_name_m} ({'SECONDARY' if alc_cls_m == 'PRIMARY' else 'PRIMARY'} alcohol)",
            f"1-methyl{alc_name_m}",
            f"{alc_name_m} ether",
            f"di{alc_name_m}",
            f"{alc_name_m.replace('1', '2')}"
        ]
        expl_alc_name = f"Formula {alc_f_m}: IUPAC name is {alc_name_m}. Classification: {alc_cls_m} alcohol (M = {alc_mm_m} g·mol⁻¹)."
        add_q("medium", "Alcohol Nomenclature & Classification", q_alc_name, c_alc_name, w_alc_name, "Applying", f"Name and classify {alc_name_m}", expl_alc_name)

        # Molar mass of alcohol
        if counts["medium"] < 500:
            q_alc_mm = f"Calculate the molar mass of **{alc_name_m}** ({alc_f_m}) using atomic masses C=12, H=1, O=16 g·mol⁻¹:"
            c_alc_mm = f"{alc_mm_m} g·mol⁻¹"
            w_alc_mm = [
                f"{alc_mm_m * 2} g·mol⁻¹",
                f"{alc_mm_m / 2:.0f} g·mol⁻¹",
                f"{alc_mm_m - 16} g·mol⁻¹ (forgot oxygen atom)",
                f"{alc_mm_m + 14} g·mol⁻¹",
                f"{alc_mm_m - 14} g·mol⁻¹",
                f"{alc_mm_m + 28} g·mol⁻¹",
                f"{alc_mm_m + 16} g·mol⁻¹"
            ]
            expl_alc_mm = f"Molar mass of {alc_name_m} ({alc_f_m}) = {c_alc_mm}."
            add_q("medium", "Alcohol Molar Mass", q_alc_mm, c_alc_mm, w_alc_mm, "Applying", f"Calculate molar mass of {alc_name_m}", expl_alc_mm)

    # Systematic IUPAC Naming & Reactions for Alkenes (Medium)
    alkenes_medium = [
        ("CH2=CH2", "ethene", "ethane", "1,2-dichloroethane", "chloroethane", "ethanol"),
        ("CH3-CH=CH2", "propene", "propane", "1,2-dichloropropane", "2-chloropropane", "propan-2-ol"),
        ("CH2=CH-CH2-CH3", "but-1-ene", "butane", "1,2-dichlorobutane", "2-chlorobutane", "butan-2-ol"),
        ("CH3-CH=CH-CH3", "but-2-ene", "butane", "2,3-dichlorobutane", "2-chlorobutane", "butan-2-ol"),
        ("CH2=C(CH3)-CH3", "2-methylprop-1-ene", "2-methylpropane", "1,2-dichloro-2-methylpropane", "2-chloro-2-methylpropane", "2-methylpropan-2-ol"),
        ("CH2=CH-CH2-CH2-CH3", "pent-1-ene", "pentane", "1,2-dichloropentane", "2-chloropentane", "pentan-2-ol"),
        ("CH3-CH=CH-CH2-CH3", "pent-2-ene", "pentane", "2,3-dichloropentane", "2-chloropentane (or 3-chloropentane)", "pentan-2-ol (or pentan-3-ol)"),
        ("CH2=C(CH3)-CH2-CH3", "2-methylbut-1-ene", "2-methylbutane", "1,2-dichloro-2-methylbutane", "2-chloro-2-methylbutane", "2-methylbutan-2-ol"),
        ("CH3-C(CH3)=CH-CH3", "2-methylbut-2-ene", "2-methylbutane", "2,3-dichloro-2-methylbutane", "2-chloro-2-methylbutane", "2-methylbutan-2-ol"),
        ("CH2=CH-(CH2)3-CH3", "hex-1-ene", "hexane", "1,2-dichlorohexane", "2-chlorohexane", "hexan-2-ol"),
        ("CH3-CH=CH-(CH2)2-CH3", "hex-2-ene", "hexane", "2,3-dichlorohexane", "2-chlorohexane", "hexan-2-ol"),
        ("CH3-CH2-CH=CH-CH2-CH3", "hex-3-ene", "hexane", "3,4-dichlorohexane", "3-chlorohexane", "hexan-3-ol")
    ]

    for ene_f, ene_name, ene_sat, ene_dihal, ene_hal, ene_hyd in alkenes_medium:
        if counts["medium"] >= 500:
            break
        # Hydrogenation
        q_h2 = f"When the alkene **{ene_name}** ({ene_f}) is reacted with hydrogen gas (H2) over a nickel (Ni) catalyst at 150 °C, which saturated alkane is produced?"
        c_h2 = f"{ene_sat}"
        w_h2 = [
            f"{ene_name.replace('ene', 'yne')}",
            f"{ene_name} alcohol",
            f"methyl{ene_sat}",
            f"cyclo{ene_sat}",
            f"cracked alkane",
            f"polymerized {ene_name}",
            f"ethyne"
        ]
        expl_h2 = f"Hydrogenation addition: {ene_name} + H₂ (Ni catalyst) -> {ene_sat}."
        add_q("medium", "Alkene Addition Reactions", q_h2, c_h2, w_h2, "Applying", f"Hydrogenation of {ene_name}", expl_h2)

        # Halogenation
        if counts["medium"] < 500:
            q_cl2 = f"Predict the IUPAC name of the dihaloalkane formed when chlorine gas (Cl2) adds across the double bond of **{ene_name}** ({ene_f}):"
            c_cl2 = f"{ene_dihal}"
            w_cl2 = [
                f"{ene_hal} (confused halogenation with hydrohalogenation)",
                f"1-chloro{ene_name}",
                f"trichloro{ene_sat}",
                f"{ene_name} dichloride",
                f"tetrachloro{ene_sat}",
                f"chloro{ene_sat}",
                f"2-chloro{ene_name}"
            ]
            expl_cl2 = f"Halogenation addition: {ene_name} + Cl₂ -> {ene_dihal}."
            add_q("medium", "Alkene Addition Reactions", q_cl2, c_cl2, w_cl2, "Applying", f"Halogenation of {ene_name}", expl_cl2)

        # Hydrohalogenation
        if counts["medium"] < 500:
            q_hcl = f"According to Markovnikov's rule, what is the major organic product formed when hydrogen chloride (HCl) adds to **{ene_name}** ({ene_f})?"
            c_hcl = f"{ene_hal}"
            w_hcl = [
                f"{ene_dihal} (confused with addition of Cl₂)",
                f"{ene_sat} + Cl₂",
                f"chloro{ene_name}",
                f"{ene_hyd}",
                f"1-chloro{ene_sat}",
                f"trichloro{ene_sat}",
                f"dichloro{ene_sat}"
            ]
            expl_hcl = f"Hydrohalogenation: {ene_name} + HCl -> {ene_hal} (Markovnikov major product)."
            add_q("medium", "Alkene Addition Reactions", q_hcl, c_hcl, w_hcl, "Applying", f"Hydrohalogenation of {ene_name}", expl_hcl)

        # Hydration
        if counts["medium"] < 500:
            q_h2o = f"Predict the primary alcohol product formed when **{ene_name}** ({ene_f}) is reacted with steam in the presence of concentrated phosphoric acid (H3PO4) catalyst:"
            c_h2o = f"{ene_hyd}"
            w_h2o = [
                f"{ene_sat} + O₂",
                f"{ene_dihal}",
                f"{ene_name} acid",
                f"ethanoic acid",
                f"poly{ene_name}",
                f"methoxy{ene_sat}",
                f"hydroxy{ene_name}"
            ]
            expl_h2o = f"Hydration addition: {ene_name} + H₂O (H₃PO₄ catalyst) -> {ene_hyd}."
            add_q("medium", "Alkene Addition Reactions", q_h2o, c_h2o, w_h2o, "Applying", f"Hydration of {ene_name}", expl_h2o)

    # Carboxylic Acid IUPAC Nomenclature & Properties (Medium)
    acids_medium = [
        ("H-COOH", "methanoic acid", 46, "formic acid found in ant stings"),
        ("CH3-COOH", "ethanoic acid", 60, "acetic acid found in commercial vinegar"),
        ("CH3-CH2-COOH", "propanoic acid", 74, "food preservative against fungal mold"),
        ("CH3-(CH2)2-COOH", "butanoic acid", 88, "butyric acid responsible for rancid butter odor"),
        ("CH3-CH(CH3)-COOH", "2-methylpropanoic acid", 88, "branched isomer of butanoic acid"),
        ("CH3-(CH2)3-COOH", "pentanoic acid", 102, "valeric acid used in synthetic flavorings"),
        ("CH3-CH(CH3)-CH2-COOH", "3-methylbutanoic acid", 102, "isovaleric acid with distinctive pungent aroma"),
        ("CH3-C(CH3)2-COOH", "2,2-dimethylpropanoic acid", 102, "pivalic acid with spherical branched structure"),
        ("CH3-(CH2)4-COOH", "hexanoic acid", 116, "caproic acid found in animal fats")
    ]

    for ca_form, ca_name, ca_mm, ca_desc in acids_medium:
        if counts["medium"] >= 500:
            break
        q_ca_name = f"Identify the systematic IUPAC name for the carboxylic acid with condensed structural formula **{ca_form}** ({ca_desc}):"
        c_ca_name = f"{ca_name}"
        w_ca_name = [
            f"{ca_name.replace('oic acid', 'ol')}",
            f"{ca_name.replace('oic acid', 'al')}",
            f"{ca_name.replace('oic acid', 'oate')}",
            f"methyl {ca_name.split()[0]}",
            f"di{ca_name}",
            f"hydroxy{ca_name.split()[0]}",
            f"{ca_name.replace('acid', 'ester')}"
        ]
        expl_ca_name = f"Carboxylic acid formula {ca_form}: IUPAC name is {ca_name} (M = {ca_mm} g·mol⁻¹)."
        add_q("medium", "Carboxylic Acid Nomenclature", q_ca_name, c_ca_name, w_ca_name, "Applying", f"Name carboxylic acid {ca_name}", expl_ca_name)

        if counts["medium"] < 500:
            q_ca_mm = f"Calculate the molar mass of **{ca_name}** ({ca_form}) using atomic masses C=12, H=1, O=16 g·mol⁻¹:"
            c_ca_mm = f"{ca_mm} g·mol⁻¹"
            w_ca_mm = [
                f"{ca_mm * 2} g·mol⁻¹",
                f"{ca_mm / 2:.0f} g·mol⁻¹",
                f"{ca_mm - 32} g·mol⁻¹ (forgot two oxygen atoms)",
                f"{ca_mm + 14} g·mol⁻¹",
                f"{ca_mm - 14} g·mol⁻¹",
                f"{ca_mm + 28} g·mol⁻¹",
                f"{ca_mm + 16} g·mol⁻¹"
            ]
            expl_ca_mm = f"Molar mass of {ca_name} ({ca_form}) = {c_ca_mm}."
            add_q("medium", "Carboxylic Acid Molar Mass", q_ca_mm, c_ca_mm, w_ca_mm, "Applying", f"Calculate molar mass of {ca_name}", expl_ca_mm)

    # Structural Isomer Count Questions (Medium)
    isomer_counts = [
        ("Butane (C4H10)", 2, ["butane (straight chain)", "2-methylpropane (branched chain)"]),
        ("Pentane (C5H12)", 3, ["pentane", "2-methylbutane", "2,2-dimethylpropane"]),
        ("Hexane (C6H14)", 5, ["hexane", "2-methylpentane", "3-methylpentane", "2,2-dimethylbutane", "2,3-dimethylbutane"]),
        ("Butene (C4H8)", 3, ["but-1-ene", "but-2-ene", "2-methylprop-1-ene"]),
        ("Propanol (C3H8O)", 2, ["propan-1-ol (primary)", "propan-2-ol (secondary)"]),
        ("Butanol (C4H10O)", 4, ["butan-1-ol", "butan-2-ol", "2-methylpropan-1-ol", "2-methylpropan-2-ol"])
    ]

    for iso_target, iso_cnt, iso_examples in isomer_counts:
        if counts["medium"] >= 500:
            break
        q_iso_cnt = f"How many structural isomers exist for the molecular formula representing **{iso_target}**?"
        c_iso_cnt = f"{iso_cnt} structural isomers"
        w_iso_cnt = [
            f"{iso_cnt + 1} structural isomers",
            f"{iso_cnt - 1 if iso_cnt > 1 else 4} structural isomers",
            f"{iso_cnt * 2} structural isomers",
            f"1 structural isomer (assumed no isomers exist)",
            f"{iso_cnt + 3} structural isomers",
            f"8 structural isomers",
            f"10 structural isomers"
        ]
        expl_iso_cnt = f"{iso_target} has exactly {iso_cnt} structural isomers: {', '.join(iso_examples)}."
        add_q("medium", "Isomer Enumeration", q_iso_cnt, c_iso_cnt, w_iso_cnt, "Understanding", f"Count isomers of {iso_target}", expl_iso_cnt)

    # Dihaloalkanes IUPAC Nomenclature & Positional Isomers (Medium)
    dihaloalkanes_medium = [
        ("CH2Cl-CH2Cl", "1,2-dichloroethane", ["1,1-dichloroethane", "dichloroethane", "chloroethane", "1,2-chloroethane", "dichloroethene", "1,2-dichloropropane", "chloromethane"]),
        ("CH3-CHCl2", "1,1-dichloroethane", ["1,2-dichloroethane", "dichloroethane", "2,2-dichloroethane", "chloroethane", "1,1-dichloroethene", "dichloromethane", "1,1-dichloropropane"]),
        ("CH2Br-CH2Br", "1,2-dibromoethane", ["1,1-dibromoethane", "dibromoethane", "bromoethane", "1,2-bromoethane", "dibromoethene", "ethylene bromide", "1,2-dibromopropane"]),
        ("CH3-CHBr2", "1,1-dibromoethane", ["1,2-dibromoethane", "dibromoethane", "2,2-dibromoethane", "bromoethane", "dibromomethane", "1,1-dibromopropane", "ethyl bromide"]),
        ("CH2Cl-CH2-CH2Cl", "1,3-dichloropropane", ["1,2-dichloropropane", "1,1-dichloropropane", "2,2-dichloropropane", "dichloropropane", "1,3-dichloroethene", "chloropropane", "1,4-dichlorobutane"]),
        ("CH3-CH(Cl)-CH2Cl", "1,2-dichloropropane", ["1,3-dichloropropane", "1,1-dichloropropane", "2,2-dichloropropane", "dichloropropane", "propyl dichloride", "1,2-dichlorobutane", "2-chloropropane"]),
        ("CH3-C(Cl)2-CH3", "2,2-dichloropropane", ["1,2-dichloropropane", "1,1-dichloropropane", "1,3-dichloropropane", "dichloropropane", "2-dichloropropane", "2,2-dichlorobutane", "isopropyl chloride"]),
        ("CH2Br-CH2-CH2Br", "1,3-dibromopropane", ["1,2-dibromopropane", "1,1-dibromopropane", "2,2-dibromopropane", "dibromopropane", "1,3-dibromobutane", "bromopropane", "trimethylene bromide"]),
        ("CH3-CH(Br)-CH2Br", "1,2-dibromopropane", ["1,3-dibromopropane", "1,1-dibromopropane", "2,2-dibromopropane", "dibromopropane", "propyl dibromide", "1,2-dibromobutane", "2-bromopropane"]),
        ("CH2Cl-CH2-CH2-CH2Cl", "1,4-dichlorobutane", ["1,2-dichlorobutane", "1,3-dichlorobutane", "2,3-dichlorobutane", "dichlorobutane", "1,4-dichlorohexane", "butyl dichloride", "1,1-dichlorobutane"]),
        ("CH3-CH(Cl)-CH(Cl)-CH3", "2,3-dichlorobutane", ["1,2-dichlorobutane", "1,4-dichlorobutane", "2,2-dichlorobutane", "dichlorobutane", "3,4-dichlorobutane", "2,3-dichlorohexane", "sec-butyl chloride"]),
        ("CH2Br-CH2-CH2-CH2Br", "1,4-dibromobutane", ["1,2-dibromobutane", "2,3-dibromobutane", "1,3-dibromobutane", "dibromobutane", "tetramethylene bromide", "1,4-dibromopentane", "butyl bromide"]),
        ("CH3-CH(Br)-CH(Br)-CH3", "2,3-dibromobutane", ["1,2-dibromobutane", "1,4-dibromobutane", "2,2-dibromobutane", "dibromobutane", "3,4-dibromobutane", "2,3-dibromopentane", "bromobutane"])
    ]

    for dh_form, dh_name, dh_wrongs in dihaloalkanes_medium:
        if counts["medium"] >= 500:
            break
        q_dh = f"According to IUPAC nomenclature, what is the systematic name for the dihalogenated hydrocarbon with formula **{dh_form}**?"
        expl_dh = f"Condensed formula {dh_form}: parent chain and locants indicate {dh_name}."
        add_q("medium", "Dihaloalkane Nomenclature", q_dh, dh_name, dh_wrongs, "Applying", f"Name dihaloalkane {dh_name}", expl_dh)

    # Physical Property Boiling Point Hierarchies (Medium)
    bp_hierarchies = [
        ("Four-carbon compounds: Butane, 1-chlorobutane, Butan-1-ol, Butanoic acid",
         "Butanoic acid > Butan-1-ol > 1-chlorobutane > Butane",
         ["Butane > 1-chlorobutane > Butan-1-ol > Butanoic acid",
          "1-chlorobutane > Butanoic acid > Butan-1-ol > Butane",
          "Butan-1-ol > Butanoic acid > 1-chlorobutane > Butane",
          "All four have identical boiling points because each has four carbons",
          "Butane > Butanoic acid > Butan-1-ol > 1-chlorobutane",
          "1-chlorobutane > Butane > Butanoic acid > Butan-1-ol"],
         "Boiling point reflects IMF strength: Butanoic acid forms dimers via 2 hydrogen bonds > Butan-1-ol has 1 hydrogen bond > 1-chlorobutane has dipole-dipole forces > Butane has only weak London dispersion forces."),

        ("Three-carbon compounds: Propane, 1-chloropropane, Propan-1-ol, Propanoic acid",
         "Propanoic acid > Propan-1-ol > 1-chloropropane > Propane",
         ["Propane > 1-chloropropane > Propan-1-ol > Propanoic acid",
          "Propan-1-ol > Propanoic acid > 1-chloropropane > Propane",
          "1-chloropropane > Propanoic acid > Propan-1-ol > Propane",
          "Propane > Propanoic acid > 1-chloropropane > Propan-1-ol",
          "All three-carbon compounds have identical boiling points",
          "1-chloropropane > Propane > Propan-1-ol > Propanoic acid"],
         "IMF strength hierarchy: Carboxylic acid (dimer H-bonds) > Alcohol (single H-bonds) > Haloalkane (dipole-dipole) > Alkane (London forces)."),

        ("Five-carbon compounds: Pentane, 1-chloropentane, Pentan-1-ol, Pentanoic acid",
         "Pentanoic acid > Pentan-1-ol > 1-chloropentane > Pentane",
         ["Pentane > 1-chloropentane > Pentan-1-ol > Pentanoic acid",
          "Pentan-1-ol > Pentanoic acid > 1-chloropentane > Pentane",
          "1-chloropentane > Pentanoic acid > Pentan-1-ol > Pentane",
          "Pentane > Pentanoic acid > 1-chloropentane > Pentan-1-ol",
          "All five-carbon compounds have identical vapor pressures",
          "1-chloropentane > Pentane > Pentan-1-ol > Pentanoic acid"],
         "Increasing IMF strength requires more kinetic energy to break liquid attractions: Pentanoic acid (dimer H-bonds) > Pentan-1-ol > 1-chloropentane > Pentane.")
    ]

    for bp_title, bp_order, bp_wrongs, bp_expl in bp_hierarchies:
        for st_bph in [
            f"Arrange the following series in order of **DECREASING BOILING POINT** (highest to lowest): **{bp_title}**",
            f"Which sequence correctly ranks the compounds in order of **DECREASING BOILING POINT**: **{bp_title}**?",
            f"Based on intermolecular forces, rank from **HIGHEST TO LOWEST BOILING POINT**: **{bp_title}**"
        ]:
            if counts["medium"] >= 500:
                break
            add_q("medium", "Boiling Point Hierarchy", st_bph, bp_order, bp_wrongs, "Understanding", "Rank compounds by boiling point", bp_expl)

    # Moles of Oxygen Required for Alkane Combustion (Medium)
    for n_fuel in [1, 2, 3, 4, 5]:
        for alk_sym, mol_o2_per_mol in [
            ("methane (CH4)", 2.0),
            ("propane (C3H8)", 5.0),
            ("butane (C4H10)", 6.5),
            ("pentane (C5H12)", 8.0)
        ]:
            if counts["medium"] >= 500:
                break
            tot_o2 = n_fuel * mol_o2_per_mol
            c_o2 = f"{tot_o2:.1f} moles of O2"
            w_o2 = [
                f"{tot_o2 * 2:.1f} moles of O2",
                f"{tot_o2 / 2:.1f} moles of O2",
                f"{n_fuel:.1f} moles of O2 (assumed 1:1 mole ratio)",
                f"{tot_o2 + 5.0:.1f} moles of O2",
                f"{tot_o2 * 10:.1f} moles of O2",
                f"{mol_o2_per_mol:.1f} moles of O2 (for 1 mole only)",
                f"{tot_o2 - 2.0:.1f} moles of O2"
            ]
            q_text_o2 = f"Calculate the number of moles of oxygen gas (O2) required for the complete stoichiometric combustion of **{n_fuel} mole(s) of {alk_sym}**:"
            expl_o2 = f"Combustion of {alk_sym} requires {mol_o2_per_mol:.1f} mol O₂ per mole of fuel. For {n_fuel} mole(s): {n_fuel} × {mol_o2_per_mol:.1f} = {c_o2}."
            add_q("medium", "Combustion Oxygen Requirements", q_text_o2, c_o2, w_o2, "Applying", f"Calculate O2 for {n_fuel} mol {alk_sym}", expl_o2)

    # Branched Alkanes & Additional Alkenes IUPAC Naming (Medium)
    branched_medium = [
        ("CH3-CH(CH3)-CH2-CH(CH3)-CH3", "2,4-dimethylpentane", ["2,4-methylpentane", "hexane", "2,4-dimethylhexane", "1,3-dimethylbutane", "dimethylpentane", "diisopropylmethane", "heptane"]),
        ("CH3-C(CH3)2-CH2-CH(CH3)-CH3", "2,2,4-trimethylpentane", ["2,4,4-trimethylpentane", "isooctane", "2,2,4-methylpentane", "trimethylpentane", "octane", "2,4-dimethylhexane", "heptane"]),
        ("CH3-CH2-C(CH3)2-CH2-CH2-CH3", "3,3-dimethylhexane", ["4,4-dimethylhexane", "3,3-methylhexane", "octane", "3-ethyl-3-methylpentane", "dimethylhexane", "3,3-dimethylpentane", "heptane"]),
        ("CH3-CH(CH3)-CH(CH3)-CH(CH3)-CH3", "2,3,4-trimethylpentane", ["2,3,4-methylpentane", "octane", "trimethylpentane", "2,3,4-trimethylhexane", "diisopropyl", "dimethylhexane", "heptane"]),
        ("CH3-CH2-C(CH2CH3)(CH3)-CH2-CH3", "3-ethyl-3-methylpentane", ["3-methyl-3-ethylpentane", "3,3-diethylbutane", "octane", "3-ethyl-3-methylhexane", "dimethylhexane", "3-ethylpentane", "heptane"]),
        ("CH3-CH2-CH(CH3)-CH2-CH2-CH2-CH3", "3-methylheptane", ["5-methylheptane", "octane", "3-ethylhexane", "2-ethylhexane", "methylheptane", "3-propylpentane", "nonane"]),
        ("CH3-CH(CH3)-CH2-CH2-CH2-CH2-CH3", "2-methylheptane", ["6-methylheptane", "octane", "2-ethylhexane", "methylheptane", "2-propylpentane", "dimethylhexane", "nonane"])
    ]

    for br_form, br_iupac, br_wrongs in branched_medium:
        if counts["medium"] >= 500:
            break
        q_br = f"Give the correct IUPAC systematic name for the branched alkane with condensed formula **{br_form}**:"
        expl_br = f"Longest carbon chain and lowest locants rule: {br_form} -> {br_iupac}."
        add_q("medium", "Branched Alkane Nomenclature", q_br, br_iupac, br_wrongs, "Applying", f"Name branched alkane {br_iupac}", expl_br)

    # Combustion of Alkenes and Alcohols (Medium)
    more_combustion = [
        ("ethene (C2H4)", 3.0, 2.0, 2.0, "C2H4 + 3O2 → 2CO2 + 2H2O"),
        ("propene (C3H6)", 4.5, 3.0, 3.0, "2C3H6 + 9O2 → 6CO2 + 6H2O (1 mol C3H6 needs 4.5 mol O2)"),
        ("but-1-ene (C4H8)", 6.0, 4.0, 4.0, "C4H8 + 6O2 → 4CO2 + 4H2O"),
        ("pent-1-ene (C5H10)", 7.5, 5.0, 5.0, "2C5H10 + 15O2 → 10CO2 + 10H2O (1 mol C5H10 needs 7.5 mol O2)"),
        ("methanol (CH3OH)", 1.5, 1.0, 2.0, "2CH3OH + 3O2 → 2CO2 + 4H2O (1 mol CH3OH needs 1.5 mol O2)"),
        ("ethanol (C2H5OH)", 3.0, 2.0, 3.0, "C2H5OH + 3O2 → 2CO2 + 3H2O"),
        ("propan-1-ol (C3H7OH)", 4.5, 3.0, 4.0, "2C3H7OH + 9O2 → 6CO2 + 8H2O (1 mol C3H7OH needs 4.5 mol O2)"),
        ("butan-1-ol (C4H9OH)", 6.0, 4.0, 5.0, "C4H9OH + 6O2 → 4CO2 + 5H2O")
    ]

    for fuel_mb, o2_req, co2_prod, h2o_prod, eq_note in more_combustion:
        for n_moles_burn in [1, 2, 4]:
            if counts["medium"] >= 500:
                break
            tot_co2 = n_moles_burn * co2_prod
            c_co2_prod = f"{tot_co2:.0f} mole(s) of CO2"
            w_co2_prod = [
                f"{tot_co2 * 2:.0f} mole(s) of CO2",
                f"{tot_co2 / 2:.1f} mole(s) of CO2",
                f"{n_moles_burn:.0f} mole(s) of CO2 (assumed 1:1 ratio)",
                f"{tot_co2 + 4:.0f} mole(s) of CO2",
                f"{tot_co2 * 3:.0f} mole(s) of CO2",
                f"{co2_prod:.0f} mole(s) of CO2 (for 1 mole only)",
                f"{tot_co2 + 10:.0f} mole(s) of CO2"
            ]
            q_text_co2m = f"Calculate the number of moles of carbon dioxide (CO2) produced by the complete combustion of **{n_moles_burn} mole(s) of {fuel_mb}** in excess oxygen:"
            expl_co2m = f"Balanced reaction: {eq_note}. 1 mole of {fuel_mb.split()[0]} produces {co2_prod:.0f} mol CO₂. For {n_moles_burn} mole(s): {n_moles_burn} × {co2_prod:.0f} = {c_co2_prod}."
            add_q("medium", "Combustion Product Yields", q_text_co2m, c_co2_prod, w_co2_prod, "Applying", f"Calculate CO2 yield for {fuel_mb}", expl_co2m)

    # Empirical Formula Derivation (Medium)
    empirical_formulas = [
        ("Ethane (C2H6)", "CH3", "dividing the subscript ratio 2:6 by common factor 2 yields simplest ratio 1:3"),
        ("Butane (C4H10)", "C2H5", "dividing subscripts 4:10 by 2 gives simplest whole-number ratio 2:5"),
        ("Hexane (C6H14)", "C3H7", "dividing subscripts 6:14 by 2 gives simplest whole-number ratio 3:7"),
        ("Octane (C8H18)", "C4H9", "dividing subscripts 8:18 by 2 yields simplest whole-number ratio 4:9"),
        ("Ethene (C2H4)", "CH2", "dividing subscripts 2:4 by 2 gives simplest ratio 1:2"),
        ("Propene (C3H6)", "CH2", "dividing subscripts 3:6 by 3 gives simplest ratio 1:2"),
        ("But-1-ene (C4H8)", "CH2", "dividing subscripts 4:8 by 4 gives simplest ratio 1:2"),
        ("Pent-1-ene (C5H10)", "CH2", "dividing subscripts 5:10 by 5 gives simplest ratio 1:2"),
        ("Ethanoic acid (C2H4O2)", "CH2O", "dividing subscripts 2:4:2 by 2 gives simplest ratio 1:2:1"),
        ("Methyl ethanoate (C3H6O2)", "C3H6O2", "subscripts 3:6:2 have no common integer factor other than 1, so empirical formula equals molecular formula"),
        ("Butanoic acid (C4H8O2)", "C2H4O", "dividing subscripts 4:8:2 by 2 gives simplest ratio 2:4:1"),
        ("Ethyne / Acetylene (C2H2)", "CH", "dividing subscripts 2:2 by 2 gives simplest ratio 1:1"),
        ("Benzene (C6H6)", "CH", "dividing subscripts 6:6 by 6 gives simplest ratio 1:1"),
        ("Glucose (C6H12O6)", "CH2O", "dividing subscripts 6:12:6 by 6 gives simplest ratio 1:2:1"),
        ("Hex-3-ene (C6H12)", "CH2", "dividing subscripts 6:12 by 6 gives simplest ratio 1:2"),
        ("Oct-1-ene (C8H16)", "CH2", "dividing subscripts 8:16 by 8 gives simplest ratio 1:2"),
        ("But-1-yne (C4H6)", "C2H3", "dividing subscripts 4:6 by 2 gives simplest ratio 2:3"),
        ("Decane (C10H22)", "C5H11", "dividing subscripts 10:22 by 2 gives simplest ratio 5:11"),
        ("Heptane (C7H16)", "C7H16", "subscripts 7:16 have no common factor other than 1"),
        ("Nonane (C9H20)", "C9H20", "subscripts 9:20 have no common factor other than 1"),
        ("Propanone (C3H6O)", "C3H6O", "subscripts 3:6:1 have no common factor other than 1"),
        ("Diethyl ether (C4H10O)", "C4H10O", "subscripts 4:10:1 have no common factor other than 1")
    ]

    for mol_name, emp_form, emp_reason in empirical_formulas:
        for st_emp in [
            f"What is the **EMPIRICAL FORMULA** of the organic compound **{mol_name}**?",
            f"Determine the simplest whole-number ratio formula (empirical formula) for **{mol_name}**:"
        ]:
            if counts["medium"] >= 500:
                break
            c_emp = f"{emp_form}"
            w_emp = [
                f"{mol_name.split('(')[-1].rstrip(')')} (stated molecular formula instead of empirical formula)",
                "CH",
                "CH2",
                "CH3",
                "C2H3",
                "CHO",
                "C2H5"
            ]
            expl_emp = f"The empirical formula of {mol_name} is {emp_form} because {emp_reason}."
            add_q("medium", "Empirical Formulas", st_emp, c_emp, w_emp, "Applying", f"Determine empirical formula of {mol_name}", expl_emp)

    # Reaction Mode: Addition vs Substitution (Medium)
    reaction_modes = [
        ("Propane (CH3CH2CH3, saturated alkane)", "FREE-RADICAL SUBSTITUTION because it contains only single C-C bonds and cannot undergo addition without cracking"),
        ("Propene (CH3CH=CH2, unsaturated alkene)", "ADDITION because the reactive pi component of the C=C double bond opens up to accept new atoms"),
        ("Butane (CH3(CH2)2CH3, saturated alkane)", "SUBSTITUTION because it is fully saturated with maximum possible hydrogen atoms"),
        ("But-2-ene (CH3CH=CHCH3, unsaturated alkene)", "ADDITION because the carbon-carbon double bond readily adds reagents like H2, Br2, and HCl"),
        ("Ethene (CH2=CH2, unsaturated alkene)", "ADDITION because the unsaturated double bond provides an electron-rich site for electrophilic attack"),
        ("Ethane (CH3CH3, saturated alkane)", "SUBSTITUTION because single C-H bonds must be broken to replace hydrogen with halogens under UV light"),
        ("Hex-1-ene (unsaturated alkene)", "ADDITION because the terminal double bond rapidly adds halogens and hydrogen halides"),
        ("Cyclohexane (saturated cycloalkane)", "SUBSTITUTION because all carbon-carbon bonds in the saturated ring are single covalent bonds")
    ]

    for rm_sub, rm_type in reaction_modes:
        for st_rm in [
            f"When reacted with bromine (Br2), what primary type of reaction does **{rm_sub}** undergo, and why?",
            f"In organic chemical reactivity, **{rm_sub}** is characterized by which reaction pathway?"
        ]:
            if counts["medium"] >= 500:
                break
            c_rm = f"It undergoes {rm_type}."
            w_rm = [
                f"It undergoes {'ADDITION' if 'SUBSTITUTION' in rm_type else 'SUBSTITUTION'} spontaneously in total darkness.",
                "It undergoes condensation polymerization with the elimination of sodium chloride.",
                "It undergoes acid-base neutralization producing a carboxylic salt and water.",
                "It undergoes radioactive decay into aromatic isotopes.",
                "It undergoes thermal cracking at room temperature without any catalyst.",
                "It does not react under any conditions because hydrocarbons are completely inert."
            ]
            expl_rm = f"{rm_sub}: {c_rm}"
            add_q("medium", "Reaction Mode Classification", st_rm, c_rm, w_rm, "Understanding", f"Classify reaction mode for {rm_sub}", expl_rm)

    # =========================================================================
    # 3. HARD (Target: 200 Questions)
    # Multi-Step Synthetic Reaction Pathways, Stoichiometry, Advanced IUPAC, Reaction Conditions
    # =========================================================================

    multi_step_pathways = [
        # Pathway 1: Alkane -> Haloalkane -> Alkene -> Alcohol
        ("Ethane (C2H6) is converted to chloroethane via Reaction 1. Chloroethane is then heated with concentrated ethanolic NaOH to produce Compound X (Reaction 2). Compound X is then reacted with steam in the presence of H3PO4 to yield Compound Y (Reaction 3).",
         "Reaction 1 is Free-Radical Substitution (Cl2 + UV light); Compound X is Ethene (CH2=CH2, formed via Dehydrohalogenation Elimination); Compound Y is Ethanol (CH3CH2OH, formed via Hydration Addition).",
         ["Reaction 1 is Addition; Compound X is Ethyne; Compound Y is Ethanoic acid.",
          "Reaction 1 is Elimination; Compound X is Methane; Compound Y is Methanol.",
          "Reaction 1 is Esterification; Compound X is Ethyl ethanoate; Compound Y is Water.",
          "Reaction 1 is Combustion; Compound X is Carbon monoxide; Compound Y is Carbon dioxide.",
          "Reaction 1 is Cracking; Compound X is Chloroethene; Compound Y is Polyvinyl chloride.",
          "Reaction 1 is Saponification; Compound X is Sodium acetate; Compound Y is Glycerol."],
         "Step 1: Substitution (C₂H₆ + Cl₂ / UV -> C₂H₅Cl). Step 2: Elimination (C₂H₅Cl + conc. NaOH in ethanol/heat -> CH₂=CH₂). Step 3: Addition (CH₂=CH₂ + H₂O/H₃PO₄ -> CH₃CH₂OH)."),

        # Pathway 2: Haloalkane -> Alkene -> Dihaloalkane
        ("2-bromobutane is heated under reflux with concentrated potassium hydroxide (KOH) dissolved in ethanol to produce major organic product A. Product A is subsequently shaken with bromine water (Br2 in CCl4) in the dark to form product B.",
         "Product A is but-2-ene (CH3-CH=CH-CH3, formed via dehydrohalogenation elimination according to Zaitsev's rule); Product B is 2,3-dibromobutane (formed via halogenation addition, rapidly decolourising the reddish-brown bromine solution).",
         ["Product A is butan-2-ol; Product B is 2-bromobutane.",
          "Product A is but-1-ene; Product B is 1,2-dibromobutane as exclusive product.",
          "Product A is butane; Product B is tetrabromobutane.",
          "Product A is but-2-yne; Product B is 2,2,3,3-tetrabromobutane.",
          "Product A is ethyl ethanoate; Product B is bromoethanoic acid.",
          "Product A is butanoic acid; Product B is butyl bromide."],
         "Step 1: Elimination of 2-bromobutane gives but-2-ene as major product. Step 2: Addition of Br₂ across the double bond yields 2,3-dibromobutane."),

        # Pathway 3: Alkene -> Secondary Alcohol -> Ester
        ("Propene is reacted with water in the presence of concentrated sulfuric acid to yield major organic product P. Product P is then heated with ethanoic acid in the presence of a few drops of concentrated sulfuric acid catalyst to produce organic compound Q.",
         "Product P is propan-2-ol (CH3-CH(OH)-CH3, Markovnikov addition of H2O across propene); Product Q is 1-methylethyl ethanoate / isopropyl ethanoate (CH3COOCH(CH3)2, an ester with a sweet fruity scent).",
         ["Product P is propan-1-ol; Product Q is propyl ethanoate.",
          "Product P is propanoic acid; Product Q is ethyl propanoate.",
          "Product P is propane; Product Q is ethyl ethanoate.",
          "Product P is propanal; Product Q is ethanoic propanoic anhydride.",
          "Product P is 2-chloropropane; Product Q is ethyl chloride.",
          "Product P is prop-2-en-1-ol; Product Q is methyl propanoate."],
         "Step 1: Hydration of propene yields propan-2-ol (Markovnikov). Step 2: Esterification with ethanoic acid yields 1-methylethyl ethanoate (isopropyl ethanoate) + H₂O."),

        # Pathway 4: Haloalkane: Substitution vs Elimination
        ("A student takes two separate test tubes containing 2-bromopropane: To Tube A, the student adds DILUTE aqueous NaOH and warms gently. To Tube B, the student adds CONCENTRATED NaOH dissolved in pure ETHANOL and heats strongly under reflux.",
         "Tube A undergoes NUCLEOPHILIC SUBSTITUTION producing propan-2-ol; Tube B undergoes DEHYDROHALOGENATION ELIMINATION producing propene gas.",
         ["Tube A undergoes elimination producing propene; Tube B undergoes substitution producing propan-1-ol.",
          "Both tubes undergo substitution producing propan-2-ol in equal yields.",
          "Both tubes undergo elimination producing propene gas exclusively.",
          "Tube A produces propane gas; Tube B produces 1,2-dibromopropane.",
          "Tube A produces propanone; Tube B produces propanoic acid.",
          "Neither tube reacts because secondary haloalkanes are chemically inert."],
         "Reaction conditions determine pathway: Dilute aqueous base + mild heat = Substitution (alcohol). Concentrated base in ethanol + strong heat = Elimination (alkene)."),

        # Pathway 5: Thermal and Catalytic Cracking of Long-Chain Alkanes
        ("A petroleum engineer subjects decane (C10H22) to thermal and catalytic cracking at 500 °C using a zeolite catalyst. One of the primary reaction pathways yields ethene (C2H4) and an alkane compound Z.",
         "Compound Z is octane (C8H18), since mass and atoms must balance: C10H22 → C2H4 + C8H18 (decane breaks into an unsaturated short-chain monomer and a valuable motor fuel alkane).",
         ["Compound Z is octene (C8H16) with two hydrogen atoms lost as gas.",
          "Compound Z is heptane (C7H16) and methane gas.",
          "Compound Z is nonane (C9H20) and carbon soot.",
          "Compound Z is butane (C4H10) and propene.",
          "Compound Z is dec-1-ene (C10H20) and hydrogen gas.",
          "Compound Z is hex-1-ene (C6H12) and propane."],
         "Cracking of alkanes: C₁₀H₂₂ -> C₂H₄ + C₈H₁₈ (decane cracking yields ethene + octane)."),

        # Pathway 6: Combustion Stoichiometry
        ("Complete combustion of exactly 1 mole of an unknown hydrocarbon fuel CxHy requires exactly 5 moles of oxygen gas (O2) and produces 3 moles of carbon dioxide (CO2) and 4 moles of water vapor (H2O).",
         "The hydrocarbon is PROPANE (C3H8), because 3 moles of CO2 indicate 3 carbon atoms (x = 3), and 4 moles of H2O indicate 8 hydrogen atoms (y = 2 * 4 = 8): C3H8 + 5O2 → 3CO2 + 4H2O.",
         ["The hydrocarbon is propene (C3H6).",
          "The hydrocarbon is butane (C4H10).",
          "The hydrocarbon is propyne (C3H4).",
          "The hydrocarbon is pentane (C5H12).",
          "The hydrocarbon is ethene (C2H4).",
          "The hydrocarbon is ethanol (C2H5OH)."],
         "Carbon balance: 3 CO₂ -> 3 C. Hydrogen balance: 4 H₂O -> 8 H. Molecule is C₃H₈ (propane). Oxygen balance: 3(2) + 4(1) = 10 O = 5 O₂.")
    ]

    for p_stem, p_corr, p_wrongs, p_expl in multi_step_pathways:
        for st_pway in [
            "Analyze the following organic synthetic sequence and deduce the products and mechanisms: **{}**",
            "In an industrial organic laboratory: **{}**. Which deduction is fully accurate?",
            "Consider the reaction pathway: **{}**. Identify the correct mechanistic pathway:"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Synthetic Reaction Pathways", st_pway.format(p_stem), p_corr, p_wrongs, "Evaluating", "Analyze multi-step organic reaction pathways", p_expl)

    # Complex IUPAC and Structure Identification (Filling Hard to 200)
    complex_structures = [
        ("CH3-CH(CH3)-CH(CH2CH3)-CH2-CH3", "3-ethyl-2-methylpentane",
         ["2-methyl-3-ethylpentane (alphabetical rule violated: ethyl must precede methyl)",
          "3-ethyl-4-methylpentane (incorrect numbering direction: 3,4 instead of 2,3)",
          "2-isopropylpentane (longest chain missed)",
          "3,4-dimethylhexane (incorrect chain identification)",
          "3-ethyl-2-methylhexane",
          "4-ethyl-2-methylpentane",
          "3-methyl-2-ethylpentane"],
         "Longest chain is 5 carbons (pentane). Numbering from left gives substituents at C2 (methyl) and C3 (ethyl). Alphabetical ordering: 3-ethyl-2-methylpentane."),

        ("CH3-C(CH3)2-CH(Cl)-CH2-CH3", "3-chloro-2,2-dimethylpentane",
         ["3-chloro-4,4-dimethylpentane (numbered from wrong end: 3,4,4 instead of 2,2,3)",
          "2,2-dimethyl-3-chloropentane (chloro must come before methyl alphabetically)",
          "3-chloro-2-dimethylpentane (missing 'di' position locant)",
          "2-chloro-3,3-dimethylpentane",
          "3-chloro-2-ethylbutane",
          "3-chloro-2,2-methylhexane",
          "1-chloro-2,2-dimethylpentane"],
         "Longest chain is 5 carbons (pentane). Numbering from left gives locants 2,2,3 (lower than 3,4,4). Alphabetical order: 3-chloro-2,2-dimethylpentane."),

        ("CH3-CH(OH)-CH(CH3)-CH2-CH3", "3-methylpentan-2-ol",
         ["2-methylpentan-3-ol", "3-methylpentan-4-ol (numbered from wrong end: functional group must have lowest locant)",
          "2-ethylbutan-3-ol", "4-methylpentan-2-ol", "3-methylpentanol", "2-methylpentan-2-ol", "sec-butyl methyl alcohol"],
         "Longest chain with -OH has 5 carbons (pentan-2-ol). Methyl branch is at C3 -> 3-methylpentan-2-ol."),

        ("CH2=CH-CH(CH3)-CH(CH3)-CH3", "3,4-dimethylpent-1-ene",
         ["2,3-dimethylpent-4-ene (double bond must have lowest locant C1, not C4)",
          "3,4-dimethylpentene", "1,2-dimethylpent-4-ene", "3,4-methylpent-1-ene",
          "2,3-dimethylpent-1-ene", "3,4-dimethylpent-2-ene", "3-isopropylbut-1-ene"],
         "Double bond takes priority in numbering: C1=C2. Methyl branches are on C3 and C4 -> 3,4-dimethylpent-1-ene."),

        ("CH3-CH(CH3)-CH2-COOH", "3-methylbutanoic acid",
         ["2-methylbutanoic acid", "3-methylbutanoic ester", "2-ethylpropanoic acid",
          "3-methylpropanoic acid", "4-methylbutanoic acid", "isopentanoic acid", "methylbutanoic acid"],
         "The carboxyl carbon is always carbon-1. The longest chain is 4 carbons (butanoic acid). Methyl branch is on C3 -> 3-methylbutanoic acid."),

        ("CH3-CH2-CH(Br)-CH(Br)-CH3", "2,3-dibromopentane",
         ["3,4-dibromopentane (numbered from wrong end: 3,4 instead of 2,3)",
          "2,3-bromopentane (missing 'di' multiplier prefix)", "1,2-dibromopentane",
          "2,3-dibromobutane", "dibromopentane", "2,3-dibromohexane", "3,3-dibromopentane"],
         "Five-carbon chain (pentane). Numbering from right gives lowest locants 2,3 -> 2,3-dibromopentane.")
    ]

    for c_form, c_iupac, c_wrongs, c_expl in complex_structures:
        for st_cplx in [
            f"Determine the rigorous IUPAC name for the heavily branched/substituted organic structure **{c_form}**:",
            f"Which systematic IUPAC name correctly identifies the compound with structural formula **{c_form}**?",
            f"Apply IUPAC nomenclature rules strictly to name: **{c_form}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Advanced IUPAC Nomenclature", st_cplx, c_iupac, c_wrongs, "Evaluating", f"Name complex molecule {c_iupac}", c_expl)

    # Detailed Reaction Condition Distinctions (Hard)
    reaction_conditions_hard = [
        ("Hydrohalogenation of an alkene vs Halogenation of an alkane",
         "Hydrohalogenation of an alkene (e.g. ethene + HCl → chloroethane) is an ADDITION reaction requiring NO light/catalyst at room temperature; halogenation of an alkane (e.g. ethane + Cl2 → chloroethane + HCl) is a SUBSTITUTION reaction requiring UV LIGHT or heat.",
         ["Both reactions require intense ultraviolet light to activate carbon bonds",
          "Hydrohalogenation is a substitution reaction while alkane halogenation is an addition",
          "Both reactions produce hydrogen chloride gas as a secondary byproduct",
          "Hydrohalogenation requires concentrated sulfuric acid as a dehydrating agent",
          "Alkane halogenation occurs spontaneously in total darkness within seconds",
          "Both reactions convert saturated hydrocarbons into unsaturated polymers"],
         "Alkenes add HX spontaneously across double bond without light. Alkanes require UV light to initiate free-radical substitution with halogens."),

        ("Hydration of an alkene vs Hydrolysis of a haloalkane to form alcohols",
         "Hydration is an ADDITION reaction adding water across a C=C double bond using excess steam and an ACID catalyst (H3PO4/H2SO4); hydrolysis is a NUCLEOPHILIC SUBSTITUTION replacing a halogen on an sp³ carbon using DILUTE AQUEOUS BASE (NaOH/KOH) and mild heating.",
         ["Hydration requires concentrated sodium hydroxide while hydrolysis requires acid catalyst",
          "Both reactions are elimination reactions that produce alkenes and water",
          "Hydration produces a haloalkane while hydrolysis produces an alkene",
          "Both reactions require ultraviolet light to proceed",
          "Hydration is a substitution reaction and hydrolysis is an addition reaction",
          "Hydrolysis requires anhydrous ether while hydration requires liquid nitrogen"],
         "Hydration = Addition of H₂O to alkene (acid catalyst). Hydrolysis = Substitution of halogen by -OH using dilute aqueous NaOH/KOH (mild heat)."),

        ("Dehydration of an alcohol vs Dehydrohalogenation of a haloalkane to synthesize alkenes",
         "Dehydration removes H2O from an alcohol using CONCENTRATED ACID (H2SO4) and excess heat; dehydrohalogenation removes HX from a haloalkane using CONCENTRATED BASE (NaOH/KOH) dissolved in pure ETHANOL under reflux.",
         ["Both reactions use dilute aqueous acid at room temperature",
          "Dehydration requires hot ethanolic NaOH while dehydrohalogenation requires sulfuric acid",
          "Both reactions are addition reactions adding water across single bonds",
          "Dehydration produces an alkyne while dehydrohalogenation produces an alkane",
          "Both reactions require sunlight and produce chlorine gas",
          "Dehydration converts an alkene into an alcohol while dehydrohalogenation reverses it"],
         "Both are elimination reactions producing alkenes: Dehydration uses conc. H₂SO₄ (catalytic dehydrator). Dehydrohalogenation uses conc. hot base in ethanol."),

        ("Distinguishing an alkane from an alkene using the Bromine Water Test",
         "When reddish-brown bromine water (Br2(aq)) is added to an alkene, it DECOLOURISES RAPIDLY (turns clear/colourless) in the dark via addition; when added to an alkane, it REMAINS REDDISH-BROWN in the dark and only slowly decolourises if exposed to UV light/sunlight via substitution.",
         ["The alkane decolourises bromine water immediately while the alkene does not react",
          "Both decolourise bromine water at identical rates in total darkness",
          "The alkene turns the bromine water bright purple while the alkane turns it green",
          "The alkene precipitates solid yellow sulfur while the alkane boils vigorously",
          "The alkane undergoes addition while the alkene undergoes substitution",
          "Bromine water test cannot distinguish between alkanes and alkenes under any conditions"],
         "Alkenes rapidly decolourise reddish-brown bromine water in the dark (addition of Br₂). Alkanes do not react in the dark (only slowly in UV light via substitution).")
    ]

    for cond_title, cond_corr, cond_wrongs, cond_expl in reaction_conditions_hard:
        for st_cond in [
            "Critically compare the operational conditions and chemical mechanisms for: **{}**",
            "In experimental Technical Sciences chemistry, analyze: **{}**",
            "Which comparative evaluation accurately distinguishes: **{}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Comparative Reaction Mechanisms", st_cond.format(cond_title), cond_corr, cond_wrongs, "Evaluating", "Distinguish reaction conditions and mechanisms", cond_expl)

    # Detailed Industrial Polymers & Plastics (Hard)
    polymers_hard = [
        ("Low-Density Polyethene (LDPE) vs High-Density Polyethene (HDPE)",
         "LDPE is manufactured at high pressure (1000-3000 atm) via free-radical polymerization, producing extensive chain branching that prevents tight packing (low density, flexible, lower melting point); HDPE is synthesized at low pressure using a Ziegler-Natta catalyst, yielding linear unbranched chains that pack tightly into crystalline regions (high density, rigid, high tensile strength).",
         ["LDPE is a condensation polymer eliminating water while HDPE is an addition polymer",
          "HDPE has lower density than LDPE because it contains more carbon-carbon double bonds",
          "LDPE is synthesized exclusively from propene while HDPE is made from ethene",
          "LDPE has higher tensile strength and melting point than HDPE due to branching",
          "Both have identical molecular structures and differ only in the colour of plastic pellets",
          "HDPE is a thermosetting resin that cannot be melted or reshaped once formed"],
         "LDPE: branched chains, poor packing, lower density/strength. HDPE: linear unbranched chains, tight packing, higher density/rigidity."),

        ("Polychloroethene (PVC) and the Role of Plasticizers",
         "Unplasticized PVC (uPVC) is rigid and brittle due to strong dipole-dipole attractions between polar C-Cl bonds, making it ideal for drainage pipes and window profiles; adding plasticizers (such as phthalates) spaces polymer chains apart and weakens dipole forces, producing flexible PVC used in cable insulation and hoses.",
         ["Plasticizers create permanent covalent cross-links between polymer chains to make PVC rigid",
          "uPVC is formed by condensation polymerization while plasticized PVC is an addition polymer",
          "Plasticizers remove chlorine atoms from the PVC backbone to convert it into pure polyethene",
          "Plasticized PVC is an inorganic ceramic that conducts high electrical currents safely",
          "uPVC decomposes spontaneously into toxic chlorine gas at room temperature",
          "Plasticizers convert thermoplastic PVC into a thermosetting Bakelite resin"],
         "Plasticizers insert between PVC chains, reducing dipole-dipole intermolecular attractions and increasing chain flexibility."),

        ("Polytetrafluoroethene (PTFE / Teflon) Properties and Structure",
         "Synthesized from tetrafluoroethene (CF₂=CF₂); the exceptional strength of the carbon-fluorine covalent bonds (C-F, ~485 kJ·mol⁻¹) and non-polar fluorocarbon sheath provide extreme chemical inertness, high thermal stability (up to 260 °C), hydrophobicity, and an ultra-low coefficient of friction.",
         ["PTFE has weak C-F bonds that break easily to lubricate cookware mechanically",
          "PTFE is a water-soluble polyamide formed by condensation of fluoroamines",
          "PTFE conducts electricity better than metallic copper due to mobile fluorine ions",
          "PTFE is an elastomer that stretches to ten times its original length without breaking",
          "PTFE is formed by the elimination of hydrogen fluoride from polyethene",
          "PTFE is highly reactive and dissolves instantly in concentrated mineral acids"],
         "The high bond energy of C-F bonds and non-polar fluorine sheath make PTFE non-stick, heat-resistant, and chemically inert."),

        ("Nylon-6,6 Synthesis and Intermolecular Bonding",
         "A condensation polyamide formed by the reaction between hexanedioic acid (6 carbons) and hexane-1,6-diamine (6 carbons), eliminating water molecules to create recurring amide / peptide linkages (-CO-NH-); extensive hydrogen bonding between adjacent polymer chains confers high tensile strength and elasticity.",
         ["Formed by addition polymerization of hex-1-ene without any byproduct formation",
          "A polyester formed between a dialcohol and a dicarboxylic acid eliminating HCl",
          "A synthetic rubber held together exclusively by weak London dispersion forces",
          "A branched polymer that melts at room temperature due to steric hindrance",
          "A natural protein extracted from cellulose pulp via acid hydrolysis",
          "An inorganic coordination polymer containing alternating titanium and silicon atoms"],
         "Nylon-6,6: hexanedioic acid + hexane-1,6-diamine -> polyamide + H₂O. Strong inter-chain hydrogen bonds give high tensile strength."),

        ("Polyethylene Terephthalate (PET) Structure and Recycling",
         "A condensation polyester produced by reacting benzene-1,4-dicarboxylic acid (terephthalic acid) with ethane-1,2-diol (ethylene glycol), forming ester linkages (-COO-) and water; it is a thermoplastic polymer widely used in clear beverage containers (recycling code 1) and synthetic textile fibres (Dacron/Terylene).",
         ["An addition polymer of styrene used exclusively in brittle polystyrene coffee cups",
          "A thermosetting plastic that chars and decomposes upon heating without melting",
          "A polyamide containing peptide bonds identical to natural animal silk",
          "A biodegradable carbohydrate polymer derived from corn starch fermentation",
          "An elastomer vulcanized with sulfur bridges to form automotive tyres",
          "A chlorinated hydrocarbon that releases hydrogen chloride gas during washing"],
         "PET is a thermoplastic polyester made from terephthalic acid and ethylene glycol, easily melted and recycled.")
    ]

    for poly_title, poly_ans, poly_wrongs, poly_expl in polymers_hard:
        for st_pl in [
            "Analyze the macromolecular chemistry and practical properties of: **{}**",
            "In Technical Sciences materials science, critically evaluate: **{}**",
            "Which comprehensive scientific deduction accurately characterizes: **{}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Polymer Chemistry & Materials", st_pl.format(poly_title), poly_ans, poly_wrongs, "Evaluating", "Evaluate polymer structure and properties", poly_expl)

    # Multi-Step Synthesis Schemes (Hard)
    synthetic_schemes = [
        ("Conversion of propane into propan-2-ol",
         "Step 1: Free-radical substitution of propane with Br₂ in the presence of UV light to produce 2-bromopropane (major product). Step 2: Nucleophilic substitution of 2-bromopropane by heating with dilute aqueous NaOH to form propan-2-ol.",
         ["Step 1: Direct addition of water across propane; Step 2: Oxidation with acidified potassium dichromate.",
          "Step 1: Dehydrogenation to propene; Step 2: Reduction with sodium borohydride.",
          "Step 1: Cracking of propane into methane; Step 2: Addition of ethanol.",
          "Step 1: Esterification with sulfuric acid; Step 2: Hydrolysis with sodium chloride.",
          "Step 1: Halogenation in total darkness; Step 2: Elimination with concentrated base.",
          "Step 1: Combustion with limited oxygen; Step 2: Condensation polymerization."],
         "Propane -> 2-bromopropane (substitution with Br₂/UV) -> propan-2-ol (substitution with dilute aq. NaOH)."),

        ("Conversion of 1-bromobutane into 2-bromobutane",
         "Step 1: Dehydrohalogenation elimination of 1-bromobutane by heating with concentrated ethanolic KOH (reflux) to form but-1-ene. Step 2: Hydrohalogenation addition of HBr across but-1-ene, which follows Markovnikov's rule to yield 2-bromobutane as the major product.",
         ["Step 1: Direct thermal isomerization at room temperature without any reagents.",
          "Step 1: Hydrolysis with aqueous NaOH; Step 2: Oxidation to butanoic acid.",
          "Step 1: Hydrogenation with nickel catalyst; Step 2: Bromination with bromine water.",
          "Step 1: Addition of hydrogen bromide; Step 2: Elimination of sulfuric acid.",
          "Step 1: Catalytic cracking; Step 2: Saponification with animal fats.",
          "Step 1: Substitution with UV light; Step 2: Condensation with ethanol."],
         "1-bromobutane -> but-1-ene (elimination with conc. ethanolic base) -> 2-bromobutane (Markovnikov addition of HBr)."),

        ("Conversion of propan-1-ol into propan-2-ol",
         "Step 1: Acid-catalysed dehydration of propan-1-ol by heating with concentrated sulfuric acid (H₂SO₄) to form propene. Step 2: Acid-catalysed hydration addition of steam (H₂O) across propene in the presence of H₃PO₄, obeying Markovnikov's rule to form propan-2-ol.",
         ["Step 1: Oxidation to propanoic acid; Step 2: Reduction back to secondary alcohol.",
          "Step 1: Substitution with hydrochloric acid; Step 2: Elimination to propyne.",
          "Step 1: Halogenation with chlorine gas; Step 2: Esterification with methanoic acid.",
          "Step 1: Complete combustion to carbon dioxide; Step 2: Catalytic reforming.",
          "Step 1: Addition of hydrogen gas; Step 2: Dehydrogenation over platinum.",
          "Step 1: Reaction with sodium metal; Step 2: Hydrolysis with concentrated acid."],
         "Propan-1-ol -> propene (dehydration with conc. H₂SO₄) -> propan-2-ol (Markovnikov hydration with H₂O/H₃PO₄)."),

        ("Conversion of ethene into ethyl ethanoate",
         "Step 1: Hydration of half the ethene with steam/H₃PO₄ to produce ethanol (CH₃CH₂OH). Step 2: Complete oxidation of a portion of ethanol with acidified KMnO₄ to produce ethanoic acid (CH₃COOH). Step 3: Acid-catalysed esterification of ethanoic acid and ethanol with conc. H₂SO₄ and gentle heating to produce ethyl ethanoate.",
         ["Step 1: Direct reaction of ethene with acetic anhydride without catalyst.",
          "Step 1: Halogenation of ethene with chlorine; Step 2: Reaction with sodium ethanoate.",
          "Step 1: Cracking ethene into methane; Step 2: Saponification with sodium hydroxide.",
          "Step 1: Hydrogenation to ethane; Step 2: Esterification with carbon dioxide.",
          "Step 1: Addition of hydrogen bromide; Step 2: Condensation polymerization.",
          "Step 1: Dehydration of ethene; Step 2: Hydrolysis with dilute sulfuric acid."],
         "Ethene -> ethanol -> ethanoic acid; ethanol + ethanoic acid (conc. H₂SO₄) -> ethyl ethanoate + H₂O.")
    ]

    for sch_title, sch_ans, sch_wrongs, sch_expl in synthetic_schemes:
        for st_sc in [
            "Outline the multi-step synthetic pathway required for the: **{}**",
            "In an advanced organic synthesis practical, devise the sequence for: **{}**",
            "Which reaction sequence represents the verified synthetic route for: **{}**"
        ]:
            if counts["hard"] >= 200:
                break
            add_q("hard", "Multi-Step Organic Synthesis", st_sc.format(sch_title), sch_ans, sch_wrongs, "Evaluating", f"Design synthesis for {sch_title}", sch_expl)

    # Stoichiometry of Esterification & Combustion Yields (Hard)
    ester_stoich = [
        ("60.0 g of ethanoic acid (M = 60 g·mol⁻¹) reacting with excess ethanol (M = 46 g·mol⁻¹)", 88.0, "ethyl ethanoate (M = 88 g·mol⁻¹)"),
        ("30.0 g of ethanoic acid (0.50 mol) reacting with excess methanol (M = 32 g·mol⁻¹)", 37.0, "methyl ethanoate (M = 74 g·mol⁻¹)"),
        ("74.0 g of propanoic acid (M = 74 g·mol⁻¹) reacting with excess methanol (M = 32 g·mol⁻¹)", 88.0, "methyl propanoate (M = 88 g·mol⁻¹)"),
        ("44.0 g of butanoic acid (0.50 mol, M = 88 g·mol⁻¹) reacting with excess ethanol", 58.0, "ethyl butanoate (M = 116 g·mol⁻¹)"),
        ("23.0 g of methanoic acid (0.50 mol, M = 46 g·mol⁻¹) reacting with excess ethanol", 37.0, "ethyl methanoate (M = 74 g·mol⁻¹)")
    ]

    for react_desc, theor_yield, prod_name in ester_stoich:
        for yield_pct in [100, 80, 75, 50]:
            if counts["hard"] >= 200:
                break
            actual_yield = (theor_yield * yield_pct) / 100.0
            c_yd = f"{actual_yield:.1f} g"
            w_yd = [
                f"{theor_yield * 1.5:.1f} g",
                f"{actual_yield / 2:.1f} g",
                f"{actual_yield * 2:.1f} g",
                f"{theor_yield:.1f} g (assumed 100% yield instead of {yield_pct}%)",
                f"{actual_yield + 25.0:.1f} g",
                f"{actual_yield * 0.1:.1f} g",
                f"{theor_yield + 18.0:.1f} g"
            ]
            q_text_yd = f"Calculate the mass of **{prod_name}** produced when **{react_desc}** undergoes esterification with a reaction yield of **{yield_pct}%**:"
            expl_yd = f"1. Theoretical yield (100% yield) = {theor_yield:.1f} g. 2. Actual yield at {yield_pct}% = ({yield_pct} / 100) × {theor_yield:.1f} g = {c_yd}."
            add_q("hard", "Esterification Stoichiometry", q_text_yd, c_yd, w_yd, "Evaluating", f"Calculate yield of {prod_name}", expl_yd)

    # Combustion Gas Volumes at STP (Hard)
    comb_volumes = [
        ("1.0 mol of methane (CH4 + 2O2 → CO2 + 2H2O)", 1.0, 22.4),
        ("2.0 mol of methane (CH4)", 2.0, 44.8),
        ("1.0 mol of propane (C3H8 + 5O2 → 3CO2 + 4H2O)", 3.0, 67.2),
        ("2.0 mol of propane (C3H8)", 6.0, 134.4),
        ("1.0 mol of butane (2C4H10 + 13O2 → 8CO2 + 10H2O, so 1 mol C4H10 produces 4 mol CO2)", 4.0, 89.6),
        ("0.5 mol of butane (C4H10)", 2.0, 44.8),
        ("1.0 mol of ethanol (C2H5OH + 3O2 → 2CO2 + 3H2O)", 2.0, 44.8)
    ]

    for fuel_v_desc, mol_co2, vol_co2 in comb_volumes:
        for temp_cond in ["STP (molar gas volume Vm = 22.4 dm³·mol⁻¹)"]:
            if counts["hard"] >= 200:
                break
            c_vol = f"{vol_co2:.1f} dm³"
            w_vol = [
                f"{vol_co2 * 2:.1f} dm³",
                f"{vol_co2 / 2:.1f} dm³",
                f"{mol_co2:.1f} dm³ (confused moles of CO₂ with gas volume)",
                f"{22.4:.1f} dm³ (assumed only 1 mole of CO₂ was produced)",
                f"{vol_co2 + 15.0:.1f} dm³",
                f"{vol_co2 * 10:.1f} dm³",
                f"{vol_co2 / 4:.1f} dm³"
            ]
            q_text_vol = f"Calculate the volume of dry carbon dioxide gas (CO2) measured at **{temp_cond}** produced by the complete combustion of **{fuel_v_desc}**:"
            expl_vol = f"1. Moles of CO₂ produced = {mol_co2:.1f} mol. 2. Volume at STP: V = n × Vm = {mol_co2:.1f} mol × 22.4 dm³·mol⁻¹ = {c_vol}."
            add_q("hard", "Combustion Gas Stoichiometry", q_text_vol, c_vol, w_vol, "Evaluating", "Calculate combustion gas volume at STP", expl_vol)

    # Degree of Polymerization & Macromolecular Calculations (Hard)
    polymers_dp = [
        ("Polyethene (PE)", "ethene (C2H4, M = 28 g·mol⁻¹)", 28.0,
         [14000, 28000, 42000, 56000, 70000, 84000, 98000, 112000, 140000]),
        ("Polychloroethene (PVC)", "chloroethene (C2H3Cl, M = 62.5 g·mol⁻¹)", 62.5,
         [31250, 62500, 93750, 125000, 156250, 187500, 250000]),
        ("Polytetrafluoroethene (PTFE)", "tetrafluoroethene (C2F4, M = 100 g·mol⁻¹)", 100.0,
         [50000, 80000, 100000, 150000, 200000, 250000, 300000, 500000]),
        ("Polypropene (PP)", "propene (C3H6, M = 42 g·mol⁻¹)", 42.0,
         [21000, 42000, 63000, 84000, 105000, 126000, 168000, 210000]),
        ("Polystyrene (PS)", "phenylethene (styrene, C8H8, M = 104 g·mol⁻¹)", 104.0,
         [52000, 104000, 156000, 208000, 260000, 312000, 416000])
    ]

    for poly_name_dp, mon_desc_dp, mon_mm_dp, mass_list in polymers_dp:
        for p_mass in mass_list:
            if counts["hard"] >= 200:
                break
            dp_val = int(round(p_mass / mon_mm_dp))
            c_dp = f"{dp_val:,} monomer units"
            w_dp = [
                f"{int(dp_val * 2):,} monomer units",
                f"{int(dp_val / 2):,} monomer units",
                f"{int(p_mass):,} monomer units (confused molar mass with monomer count)",
                f"{dp_val + 500:,} monomer units",
                f"{int(dp_val * 1.5):,} monomer units",
                f"{int(dp_val / 4):,} monomer units",
                f"{dp_val + 1000:,} monomer units"
            ]
            q_text_dp = f"A sample of commercial **{poly_name_dp}** has an average molecular mass of **{p_mass:,} g·mol⁻¹**. Given that its monomer is **{mon_desc_dp}**, calculate the average **degree of polymerization (n)** (the number of monomer units in the chain):"
            expl_dp = f"Degree of polymerization: n = Polymer Molar Mass / Monomer Molar Mass = {p_mass:,} g·mol⁻¹ / {mon_mm_dp:.1f} g·mol⁻¹ = {c_dp}."
            add_q("hard", "Degree of Polymerization", q_text_dp, c_dp, w_dp, "Evaluating", f"Calculate degree of polymerization for {poly_name_dp}", expl_dp)

    # Combustion Mass Stoichiometry (Hard)
    comb_masses = [
        ("methane (CH4)", 16.0, 16.0, 44.0, "CH4 + 2O2 → CO2 + 2H2O"),
        ("methane (CH4)", 32.0, 16.0, 88.0, "CH4 + 2O2 → CO2 + 2H2O"),
        ("ethane (C2H6)", 30.0, 30.0, 88.0, "2C2H6 + 7O2 → 4CO2 + 6H2O (1 mol C2H6 yields 2 mol CO2)"),
        ("propane (C3H8)", 44.0, 44.0, 132.0, "C3H8 + 5O2 → 3CO2 + 4H2O (1 mol C3H8 yields 3 mol CO2)"),
        ("propane (C3H8)", 88.0, 44.0, 264.0, "C3H8 + 5O2 → 3CO2 + 4H2O (2 mol C3H8 yields 6 mol CO2)"),
        ("butane (C4H10)", 58.0, 58.0, 176.0, "2C4H10 + 13O2 → 8CO2 + 10H2O (1 mol C4H10 yields 4 mol CO2)"),
        ("ethanol (C2H5OH)", 46.0, 46.0, 88.0, "C2H5OH + 3O2 → 2CO2 + 3H2O (1 mol C2H5OH yields 2 mol CO2)")
    ]

    for fuel_m_name, mass_in, molar_m, mass_co2_out, bal_note in comb_masses:
        for excess_agent in ["excess oxygen gas (O2)"]:
            if counts["hard"] >= 200:
                break
            c_mco2 = f"{mass_co2_out:.1f} g"
            w_mco2 = [
                f"{mass_co2_out * 2:.1f} g",
                f"{mass_co2_out / 2:.1f} g",
                f"{mass_in:.1f} g (assumed mass of CO₂ equals mass of fuel burned)",
                f"{mass_co2_out + 44.0:.1f} g",
                f"{mass_co2_out * 1.5:.1f} g",
                f"{mass_co2_out / 4:.1f} g",
                f"{mass_co2_out + 20.0:.1f} g"
            ]
            q_text_mco2 = f"Calculate the mass of carbon dioxide (CO2, M = 44 g·mol⁻¹) produced when exactly **{mass_in:.1f} g of {fuel_m_name}** undergoes complete combustion in **{excess_agent}**:"
            expl_mco2 = f"1. Balanced equation: {bal_note}. 2. Moles of fuel = {mass_in:.1f} g / {molar_m:.1f} g·mol⁻¹. 3. Mass of CO₂ produced = {c_mco2}."
            add_q("hard", "Combustion Mass Stoichiometry", q_text_mco2, c_mco2, w_mco2, "Evaluating", "Calculate mass of CO2 from combustion", expl_mco2)

    # Percentage Composition by Mass of Carbon in Hydrocarbons (Hard)
    pct_comp_data = [
        ("methane (CH4, M = 16.0 g·mol⁻¹)", 12.0, 16.0),
        ("ethane (C2H6, M = 30.0 g·mol⁻¹)", 24.0, 30.0),
        ("propane (C3H8, M = 44.0 g·mol⁻¹)", 36.0, 44.0),
        ("butane (C4H10, M = 58.0 g·mol⁻¹)", 48.0, 58.0),
        ("pentane (C5H12, M = 72.0 g·mol⁻¹)", 60.0, 72.0),
        ("hexane (C6H14, M = 86.0 g·mol⁻¹)", 72.0, 86.0),
        ("octane (C8H18, M = 114.0 g·mol⁻¹)", 96.0, 114.0),
        ("ethene (C2H4, M = 28.0 g·mol⁻¹)", 24.0, 28.0),
        ("propene (C3H6, M = 42.0 g·mol⁻¹)", 36.0, 42.0),
        ("ethanol (C2H5OH, M = 46.0 g·mol⁻¹)", 24.0, 46.0),
        ("ethanoic acid (CH3COOH, M = 60.0 g·mol⁻¹)", 24.0, 60.0),
        ("ethyl ethanoate (C4H8O2, M = 88.0 g·mol⁻¹)", 48.0, 88.0)
    ]

    for comp_pct_name, mass_c, tot_molar_m in pct_comp_data:
        if counts["hard"] >= 200:
            break
        pct_c = (mass_c / tot_molar_m) * 100.0
        c_pct = f"{pct_c:.1f}%"
        w_pct = [
            f"{pct_c * 1.5:.1f}%",
            f"{pct_c / 2:.1f}%",
            f"{100.0 - pct_c:.1f}% (calculated percentage of hydrogen/oxygen instead of carbon)",
            f"{pct_c + 12.0:.1f}%",
            f"{pct_c - 10.0:.1f}%",
            f"{mass_c:.1f}% (confused mass of carbon with percentage)",
            f"{pct_c * 0.8:.1f}%"
        ]
        q_text_pct = f"Using atomic mass C = 12.0 g·mol⁻¹, calculate the **PERCENTAGE COMPOSITION BY MASS OF CARBON (% C)** in pure **{comp_pct_name}**:"
        expl_pct = f"% Carbon = (Total mass of Carbon / Molar mass of compound) × 100% = ({mass_c:.1f} / {tot_molar_m:.1f}) × 100% = {c_pct}."
        add_q("hard", "Percentage Composition", q_text_pct, c_pct, w_pct, "Evaluating", f"Calculate % C in {comp_pct_name.split()[0]}", expl_pct)

    # Polymer Manufacturing Mass Conversions (Hard)
    polymer_conversions = [
        ("polyethene", "ethene", 500.0, [100, 95, 90, 85, 80]),
        ("polyvinyl chloride (PVC)", "chloroethene", 1000.0, [100, 98, 92, 88, 75]),
        ("polytetrafluoroethene (Teflon)", "tetrafluoroethene", 250.0, [100, 96, 90, 80]),
        ("polypropene", "propene", 800.0, [100, 95, 90, 85])
    ]

    for p_prod, m_feed, kg_input, yield_list in polymer_conversions:
        for y_rate in yield_list:
            if counts["hard"] >= 200:
                break
            kg_out = (kg_input * y_rate) / 100.0
            c_kgout = f"{kg_out:.1f} kg"
            w_kgout = [
                f"{kg_out * 1.5:.1f} kg",
                f"{kg_out / 2:.1f} kg",
                f"{kg_input:.1f} kg (assumed 100% conversion instead of {y_rate}%)",
                f"{kg_out + 100.0:.1f} kg",
                f"{kg_out * 2:.1f} kg",
                f"{kg_out - 50.0:.1f} kg",
                f"{kg_input * 1.2:.1f} kg"
            ]
            q_text_polykg = f"In a plastics chemical plant, **{kg_input:.0f} kg of {m_feed} monomer** is polymerized to produce **{p_prod}**. If the industrial reaction conversion yield is **{y_rate}%**, calculate the mass of polymer obtained:"
            expl_polykg = f"Mass of polymer produced = ({y_rate} / 100) × {kg_input:.0f} kg = {c_kgout}."
            add_q("hard", "Industrial Polymerization Yields", q_text_polykg, c_kgout, w_kgout, "Evaluating", f"Calculate polymer yield for {p_prod}", expl_polykg)

    # Additional Percentage Composition of Oxygen and Hydrogen (Hard)
    pct_other_data = [
        ("methanol (CH3OH, M = 32.0 g·mol⁻¹)", "OXYGEN", 16.0, 32.0),
        ("ethanol (C2H5OH, M = 46.0 g·mol⁻¹)", "OXYGEN", 16.0, 46.0),
        ("ethanoic acid (CH3COOH, M = 60.0 g·mol⁻¹)", "OXYGEN", 32.0, 60.0),
        ("propanoic acid (C3H6O2, M = 74.0 g·mol⁻¹)", "OXYGEN", 32.0, 74.0),
        ("methane (CH4, M = 16.0 g·mol⁻¹)", "HYDROGEN", 4.0, 16.0),
        ("ethane (C2H6, M = 30.0 g·mol⁻¹)", "HYDROGEN", 6.0, 30.0),
        ("propane (C3H8, M = 44.0 g·mol⁻¹)", "HYDROGEN", 8.0, 44.0),
        ("butane (C4H10, M = 58.0 g·mol⁻¹)", "HYDROGEN", 10.0, 58.0),
        ("chloroethane (C2H5Cl, M = 64.5 g·mol⁻¹)", "CHLORINE", 35.5, 64.5),
        ("1-bromopropane (C3H7Br, M = 123.0 g·mol⁻¹)", "BROMINE", 80.0, 123.0)
    ]

    for c_pct_nm, el_name, mass_el, mm_tot in pct_other_data:
        if counts["hard"] >= 200:
            break
        pct_val = (mass_el / mm_tot) * 100.0
        c_pct_o = f"{pct_val:.1f}%"
        w_pct_o = [
            f"{pct_val * 1.5:.1f}%",
            f"{pct_val / 2:.1f}%",
            f"{100.0 - pct_val:.1f}%",
            f"{pct_val + 15.0:.1f}%",
            f"{pct_val - 12.0:.1f}%",
            f"{mass_el:.1f}%",
            f"{pct_val * 0.75:.1f}%"
        ]
        q_text_pcto = f"Calculate the **PERCENTAGE COMPOSITION BY MASS OF {el_name}** in pure **{c_pct_nm}**:"
        expl_pcto = f"% {el_name} = (Total mass of {el_name} / Molar mass) × 100% = ({mass_el:.1f} / {mm_tot:.1f}) × 100% = {c_pct_o}."
        add_q("hard", "Percentage Composition", q_text_pcto, c_pct_o, w_pct_o, "Evaluating", f"Calculate % {el_name} in {c_pct_nm.split()[0]}", expl_pcto)

    # Batch Polymer Mass Synthesis (Hard)
    batch_polymers = [
        ("Polyethene", "ethene", [200.0, 400.0, 600.0, 1200.0, 1500.0, 2000.0, 5000.0], [90, 95, 98]),
        ("Polystyrene", "styrene", [300.0, 500.0, 750.0, 1000.0, 2500.0], [85, 92, 96]),
        ("Polyvinyl chloride", "chloroethene", [400.0, 700.0, 1500.0, 3000.0], [88, 94, 99])
    ]

    for p_name_b, m_name_b, batch_inputs, yield_rates in batch_polymers:
        for b_in in batch_inputs:
            for y_r in yield_rates:
                if counts["hard"] >= 200:
                    break
                p_out = (b_in * y_r) / 100.0
                c_pout = f"{p_out:.1f} kg"
                w_pout = [
                    f"{p_out * 1.5:.1f} kg",
                    f"{p_out / 2:.1f} kg",
                    f"{b_in:.1f} kg (100% yield)",
                    f"{p_out + 50.0:.1f} kg",
                    f"{p_out * 2:.1f} kg",
                    f"{b_in - p_out:.1f} kg",
                    f"{p_out * 0.8:.1f} kg"
                ]
                q_text_pout = f"An industrial reactor processes **{b_in:.0f} kg of {m_name_b} monomer** to synthesize **{p_name_b}**. If the overall polymer yield is **{y_r}%**, calculate the mass of polymer produced:"
                expl_pout = f"Polymer mass = ({y_r} / 100) × {b_in:.0f} kg = {c_pout}."
                add_q("hard", "Industrial Polymerization Yields", q_text_pout, c_pout, w_pout, "Evaluating", f"Calculate batch polymer yield for {p_name_b}", expl_pout)

    return questions

if __name__ == '__main__':
    qs = build_organic()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/technical_sciences"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_organic_chemistry.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for q in qs:
        diffs[q['difficulty']] += 1
    print(f"SUCCESS: {out_file} created with {len(qs)} questions: {diffs}")
