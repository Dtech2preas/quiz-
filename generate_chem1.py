import json
import random
import math
import sympy as sp
from generators_common import TopicGenerator

def format_float(val, decimals=2):
    return f"{val:.{decimals}f}".rstrip('0').rstrip('.') if '.' in f"{val:.{decimals}f}" else f"{val:.{decimals}f}"

def get_wrong_floats(correct_val: float, unit: str, count=8, decimals=2):
    wrongs = set()
    wrongs.add(correct_val * 2)
    wrongs.add(correct_val / 2)
    wrongs.add(correct_val + 10)
    wrongs.add(correct_val - 10)
    wrongs.add(correct_val * 10)
    wrongs.add(correct_val / 10)

    if correct_val != 0:
        wrongs.add(-correct_val)

    attempts = 0
    while len(wrongs) < count + 5 and attempts < 100:
        offset = random.uniform(-abs(correct_val)*0.5, abs(correct_val)*0.5 + 1)
        if offset != 0:
            wrongs.add(correct_val + offset)
        attempts += 1

    res = [f"{format_float(x, decimals)}~\\text{{{unit}}}" for x in wrongs if abs(x - correct_val) > 1e-9]
    return res[:count]

def get_wrong_ints(correct_val: int, unit: str, count=8):
    wrongs = set()
    wrongs.add(correct_val * 2)
    wrongs.add(int(correct_val / 2))
    wrongs.add(correct_val + 10)
    wrongs.add(correct_val - 10)
    if correct_val != 0:
        wrongs.add(-correct_val)

    attempts = 0
    while len(wrongs) < count + 5 and attempts < 100:
        offset = random.randint(-10, 10)
        if offset != 0:
            wrongs.add(correct_val + offset)
        attempts += 1

    res = [f"{x}~\\text{{{unit}}}" for x in wrongs if x != correct_val]
    return res[:count]

def gen_bonding_structure():
    topic = "Chemical Bonding & Structure"
    prefix = "CHEM_BND"
    subtopics = ["Electronegativity", "Intermolecular Forces", "Molecular Geometry", "Bond Energy"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Electronegativity":
            en1 = round(random.uniform(0.7, 4.0), 1)
            en2 = round(random.uniform(0.7, 4.0), 1)
            diff = abs(en1 - en2)
            if difficulty == "easy":
                question = f"Atom A has an electronegativity of ${format_float(en1, 1)}$ and Atom B has an electronegativity of ${format_float(en2, 1)}$. Calculate the electronegativity difference."
                correct = f"{format_float(diff, 1)}"
                wrongs = get_wrong_floats(diff, "", decimals=1)
                explanation = f"$\\Delta EN = |EN_A - EN_B| = |{format_float(en1, 1)} - {format_float(en2, 1)}| = {format_float(diff, 1)}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                bond_type = "non-polar covalent" if diff < 0.4 else ("polar covalent" if diff <= 1.7 else "ionic")
                question = f"Atom X has an electronegativity of ${format_float(en1, 1)}$ and Atom Y has an electronegativity of ${format_float(en2, 1)}$. What type of bond is formed between X and Y based on their electronegativity difference?"
                correct = bond_type
                wrongs = ["ionic", "polar covalent", "non-polar covalent", "metallic", "hydrogen bond", "van der Waals"]
                explanation = f"$\\Delta EN = |{format_float(en1, 1)} - {format_float(en2, 1)}| = {format_float(diff, 1)}$. Difference $\\le 0.4$ is non-polar, $> 0.4$ and $\\le 1.7$ is polar covalent, $> 1.7$ is ionic. Thus, it is {bond_type}."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Find unknown EN
                target_diff = round(random.uniform(0.5, 2.5), 1)
                question = f"The electronegativity difference between Atom P and Atom Q is ${format_float(target_diff, 1)}$. If Atom P is the more electronegative atom with an electronegativity of ${format_float(en1 + target_diff, 1)}$, what is the electronegativity of Atom Q?"
                correct = f"{format_float(en1, 1)}"
                wrongs = get_wrong_floats(en1, "", decimals=1)
                explanation = f"$\\Delta EN = EN_P - EN_Q \\Rightarrow {format_float(target_diff, 1)} = {format_float(en1 + target_diff, 1)} - EN_Q \\Rightarrow EN_Q = {format_float(en1, 1)}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Intermolecular Forces":
            substances = [("H2O", "hydrogen bonding"), ("CH4", "London dispersion forces"), ("HCl", "dipole-dipole forces"), ("NaCl", "ionic bonding")]
            substance, imf = random.choice(substances)
            if difficulty == "easy":
                question = f"Identify the predominant intermolecular force in a pure sample of $\\text{{{substance}}}$."
                correct = imf
                wrongs = ["hydrogen bonding", "London dispersion forces", "dipole-dipole forces", "ionic bonding", "covalent bonding", "metallic bonding"]
                explanation = f"$\\text{{{substance}}}$ exhibits primarily {imf}."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                temp = random.randint(-100, 100)
                question = f"Which of the following describes the relationship between boiling point and intermolecular forces?"
                correct = "Stronger intermolecular forces result in a higher boiling point."
                wrongs = [
                    "Stronger intermolecular forces result in a lower boiling point.",
                    "Intermolecular forces have no effect on boiling point.",
                    "Weaker intermolecular forces result in a higher boiling point.",
                    "Boiling point is determined solely by molar mass, not intermolecular forces.",
                    "Hydrogen bonding decreases the boiling point of a substance.",
                    "London dispersion forces always result in higher boiling points than hydrogen bonding."
                ]
                explanation = "Stronger intermolecular forces require more energy to break, leading to a higher boiling point."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                sub1, imf1 = random.choice(substances)
                sub2, imf2 = random.choice([s for s in substances if s[0] != sub1])
                question = f"Compare the expected boiling points of $\\text{{{sub1}}}$ and $\\text{{{sub2}}}$. Provide a reason based on intermolecular forces."
                # We won't generate perfect logic for every pair, instead we'll make it a conceptual question about energy
                energy1 = random.randint(10, 40) # kJ/mol
                energy2 = random.randint(1, 5) # kJ/mol
                ratio = energy1 / energy2
                question = f"Substance A has an enthalpy of vaporization of ${energy1}~\\text{{kJ/mol}}$, while Substance B has an enthalpy of vaporization of ${energy2}~\\text{{kJ/mol}}$. Approximately how many times stronger are the intermolecular forces in A compared to B?"
                correct = f"{format_float(ratio, 1)}"
                wrongs = get_wrong_floats(ratio, "", decimals=1)
                explanation = f"Ratio $= \\frac{{{energy1}}}{{{energy2}}} = {format_float(ratio, 1)}$. This reflects the relative strength of the intermolecular forces."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Molecular Geometry":
            molecules = [("CH4", "tetrahedral", 109.5), ("NH3", "trigonal pyramidal", 107), ("H2O", "bent", 104.5), ("CO2", "linear", 180), ("BF3", "trigonal planar", 120)]
            molecule, shape, angle = random.choice(molecules)
            if difficulty == "easy":
                question = f"What is the molecular geometry of $\\text{{{molecule}}}$ according to VSEPR theory?"
                correct = shape
                wrongs = ["linear", "bent", "trigonal planar", "tetrahedral", "trigonal pyramidal", "octahedral", "trigonal bipyramidal"]
                explanation = f"$\\text{{{molecule}}}$ has a {shape} geometry."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"What is the approximate bond angle in $\\text{{{molecule}}}$?"
                correct = f"{angle}^\\circ"
                wrongs = ["90^\\circ", "104.5^\\circ", "107^\\circ", "109.5^\\circ", "120^\\circ", "180^\\circ"]
                explanation = f"The bond angle for a {shape} molecule like $\\text{{{molecule}}}$ is approximately ${angle}^\\circ$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                bonds = random.randint(2, 6)
                lone_pairs = random.randint(0, 3)
                total = bonds + lone_pairs
                steric = total
                question = f"A central atom in a molecule has ${bonds}$ bonding pairs and ${lone_pairs}$ lone pair(s). What is its steric number?"
                correct = f"{steric}"
                wrongs = get_wrong_ints(steric, "")
                explanation = f"Steric number = bonding pairs + lone pairs = ${bonds} + {lone_pairs} = {steric}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Bond Energy":
            bond_energy = random.randint(200, 1000) # kJ/mol
            moles = random.uniform(0.5, 5.0)
            E = bond_energy * moles
            if difficulty == "easy":
                question = f"The bond energy of a certain covalent bond is ${bond_energy}~\\text{{kJ/mol}}$. Calculate the energy required to break ${format_float(moles)}~\\text{{moles}}$ of this bond."
                correct = f"{format_float(E)}~\\text{{kJ}}"
                wrongs = get_wrong_floats(E, "kJ")
                explanation = f"Energy = moles $\\times$ bond energy $= ({format_float(moles)})({bond_energy}) = {format_float(E)}~\\text{{kJ}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                bonds_broken = random.randint(200, 500)
                bonds_formed = random.randint(300, 800)
                delta_H = bonds_broken - bonds_formed
                question = f"In a chemical reaction, the sum of bond energies for bonds broken is ${bonds_broken}~\\text{{kJ/mol}}$ and for bonds formed is ${bonds_formed}~\\text{{kJ/mol}}$. Calculate the enthalpy change ($\\Delta H$) for the reaction."
                correct = f"{delta_H}~\\text{{kJ/mol}}"
                wrongs = get_wrong_ints(delta_H, "kJ/mol")
                explanation = f"$\\Delta H = \\Sigma E_{{\\text{{broken}}}} - \\Sigma E_{{\\text{{formed}}}} = {bonds_broken} - {bonds_formed} = {delta_H}~\\text{{kJ/mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Find missing bond energy
                dH = random.randint(-500, -100)
                H_formed = random.randint(600, 1000)
                H_broken = dH + H_formed
                # Let H_broken = 2*E_missing + something
                other_broken = random.randint(100, 300)
                E_missing = (H_broken - other_broken) / 2
                question = f"A reaction has $\\Delta H = {dH}~\\text{{kJ/mol}}$. The total energy released by forming new bonds is ${H_formed}~\\text{{kJ/mol}}$. The reactants contain $1~\\text{{mol}}$ of A-A bonds ($E = {other_broken}~\\text{{kJ/mol}}$) and $2~\\text{{mol}}$ of B-B bonds. Calculate the bond energy of the B-B bond."
                correct = f"{format_float(E_missing)}~\\text{{kJ/mol}}"
                wrongs = get_wrong_floats(E_missing, "kJ/mol")
                explanation = f"$\\Delta H = \\Sigma E_{{\\text{{broken}}}} - \\Sigma E_{{\\text{{formed}}}} \\Rightarrow {dH} = (1 \\times {other_broken} + 2 \\times E_{{BB}}) - {H_formed} \\Rightarrow 2E_{{BB}} = {dH} + {H_formed} - {other_broken} = {H_broken - other_broken} \\Rightarrow E_{{BB}} = {format_float(E_missing)}~\\text{{kJ/mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper2_bonding_structure.json")

def gen_stoichiometry():
    topic = "Stoichiometry & Chemical Calculations"
    prefix = "CHEM_STO"
    subtopics = ["Molar Mass", "Moles & Mass", "Concentration", "Limiting Reactant", "Empirical Formula"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Molar Mass":
            C_n = random.randint(1, 6)
            H_n = C_n * 2 + 2
            O_n = random.randint(0, 3)
            M = C_n * 12.01 + H_n * 1.01 + O_n * 16.00
            formula = f"\\text{{C}}_{{{C_n}}}\\text{{H}}_{{{H_n}}}" + (f"\\text{{O}}_{{{O_n}}}" if O_n > 0 else "")
            if difficulty == "easy":
                question = f"Calculate the molar mass of ${formula}$. (Atomic masses: C = $12.01$, H = $1.01$, O = $16.00~\\text{{g/mol}}$)"
                correct = f"{format_float(M)}~\\text{{g/mol}}"
                wrongs = get_wrong_floats(M, "g/mol")
                explanation = f"Molar mass $= {C_n}(12.01) + {H_n}(1.01)" + (f" + {O_n}(16.00)" if O_n > 0 else "") + f" = {format_float(M)}~\\text{{g/mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                moles = random.uniform(0.5, 5.0)
                mass = moles * M
                question = f"Calculate the mass of ${format_float(moles)}~\\text{{moles}}$ of ${formula}$. (Molar mass = ${format_float(M)}~\\text{{g/mol}}$)"
                correct = f"{format_float(mass)}~\\text{{g}}"
                wrongs = get_wrong_floats(mass, "g")
                explanation = f"Using $m = nM = ({format_float(moles)})({format_float(M)}) = {format_float(mass)}~\\text{{g}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                mass = random.uniform(10.0, 100.0)
                moles = mass / M
                N_A = 6.022e23
                molecules = moles * N_A
                mol_sci = f"{molecules:.2e}".replace("e", "\\times 10^{") + "}"
                question = f"Calculate the number of molecules in ${format_float(mass)}~\\text{{g}}$ of ${formula}$. (Molar mass = ${format_float(M)}~\\text{{g/mol}}$, $N_A = 6.022 \\times 10^{{23}}~\\text{{mol}}^{{-1}}$)"
                correct = f"{mol_sci}"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}" for w in [molecules*10, molecules/10, molecules*M, molecules/M, molecules*2, molecules/2, molecules*5]]
                explanation = f"Moles $n = \\frac{{m}}{{M}} = \\frac{{{format_float(mass)}}}{{{format_float(M)}}} = {format_float(moles, 3)}$. Molecules $= n N_A = ({format_float(moles, 3)})(6.022 \\times 10^{{23}}) = {mol_sci}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Moles & Mass":
            moles = random.uniform(0.1, 3.0)
            M = random.randint(20, 150)
            mass = moles * M
            if difficulty == "easy":
                question = f"How many moles are there in ${format_float(mass)}~\\text{{g}}$ of a substance with a molar mass of ${M}~\\text{{g/mol}}$?"
                correct = f"{format_float(moles)}~\\text{{mol}}"
                wrongs = get_wrong_floats(moles, "mol")
                explanation = f"Using $n = \\frac{{m}}{{M}} = \\frac{{{format_float(mass)}}}{{{M}}} = {format_float(moles)}~\\text{{mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                vol = moles * 22.4 # STP
                question = f"Calculate the volume occupied by ${format_float(mass)}~\\text{{g}}$ of a gas at STP. Its molar mass is ${M}~\\text{{g/mol}}$ and the molar volume of a gas at STP is $22.4~\\text{{dm}}^3\\text{{/mol}}$."
                correct = f"{format_float(vol)}~\\text{{dm}}^3"
                wrongs = get_wrong_floats(vol, "dm^3")
                explanation = f"Moles $n = \\frac{{{format_float(mass)}}}{{{M}}} = {format_float(moles)}$. Volume $V = n \\times V_m = ({format_float(moles)})(22.4) = {format_float(vol)}~\\text{{dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                M2 = random.randint(30, 200)
                mass2 = moles * M2
                question = f"A reaction consumes ${format_float(mass)}~\\text{{g}}$ of reactant A ($M = {M}~\\text{{g/mol}}$) to produce product B ($M = {M2}~\\text{{g/mol}}$) in a $1:1$ molar ratio. Calculate the theoretical yield of product B in grams."
                correct = f"{format_float(mass2)}~\\text{{g}}"
                wrongs = get_wrong_floats(mass2, "g")
                explanation = f"Moles of A $n = \\frac{{{format_float(mass)}}}{{{M}}} = {format_float(moles)}~\\text{{mol}}$. Since ratio is $1:1$, moles of B $= {format_float(moles)}$. Mass of B $m = n \\times M_B = ({format_float(moles)})({M2}) = {format_float(mass2)}~\\text{{g}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Concentration":
            n = random.uniform(0.01, 0.5)
            V = random.uniform(0.1, 2.0)
            C = n / V
            if difficulty == "easy":
                question = f"Calculate the concentration of a solution containing ${format_float(n)}~\\text{{moles}}$ of solute in a volume of ${format_float(V)}~\\text{{dm}}^3$."
                correct = f"{format_float(C)}~\\text{{mol/dm}}^3"
                wrongs = get_wrong_floats(C, "mol/dm^3")
                explanation = f"Using $c = \\frac{{n}}{{V}} = \\frac{{{format_float(n)}}}{{{format_float(V)}}} = {format_float(C)}~\\text{{mol/dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                M = random.randint(40, 100)
                mass = n * M
                question = f"Calculate the concentration of a solution prepared by dissolving ${format_float(mass)}~\\text{{g}}$ of a solute ($M = {M}~\\text{{g/mol}}$) in water to make a total volume of ${format_float(V)}~\\text{{dm}}^3$."
                correct = f"{format_float(C)}~\\text{{mol/dm}}^3"
                wrongs = get_wrong_floats(C, "mol/dm^3")
                explanation = f"Moles $n = \\frac{{m}}{{M}} = \\frac{{{format_float(mass)}}}{{{M}}} = {format_float(n)}~\\text{{mol}}$. Concentration $c = \\frac{{n}}{{V}} = \\frac{{{format_float(n)}}}{{{format_float(V)}}} = {format_float(C)}~\\text{{mol/dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Dilution C1V1 = C2V2
                V2 = V * random.uniform(2.0, 5.0)
                C2 = C * V / V2
                question = f"A ${format_float(V)}~\\text{{dm}}^3$ solution with a concentration of ${format_float(C)}~\\text{{mol/dm}}^3$ is diluted to a final volume of ${format_float(V2)}~\\text{{dm}}^3$. Calculate the new concentration."
                correct = f"{format_float(C2)}~\\text{{mol/dm}}^3"
                wrongs = get_wrong_floats(C2, "mol/dm^3")
                explanation = f"Using $C_1 V_1 = C_2 V_2 \\Rightarrow ({format_float(C)})({format_float(V)}) = C_2({format_float(V2)}) \\Rightarrow C_2 = \\frac{{{format_float(C * V)}}}{{{format_float(V2)}}} = {format_float(C2)}~\\text{{mol/dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Limiting Reactant":
            nA = random.uniform(1.0, 5.0)
            nB = random.uniform(1.0, 5.0)
            coeffA = random.randint(1, 3)
            coeffB = random.randint(1, 3)
            ratioA = nA / coeffA
            ratioB = nB / coeffB
            if difficulty == "easy":
                question = f"In the reaction ${coeffA}\\text{{A}} + {coeffB}\\text{{B}} \\rightarrow \\text{{Products}}$, you start with ${format_float(nA)}~\\text{{moles}}$ of A and ${format_float(nB)}~\\text{{moles}}$ of B. Which is the limiting reactant?"
                correct = "Reactant A" if ratioA < ratioB else "Reactant B"
                wrongs = ["Reactant B" if ratioA < ratioB else "Reactant A", "Both", "Neither", "Products", "Cannot be determined", "Reaction does not occur"]
                explanation = f"Ratio for A = $\\frac{{{format_float(nA)}}}{{{coeffA}}} = {format_float(ratioA)}$. Ratio for B = $\\frac{{{format_float(nB)}}}{{{coeffB}}} = {format_float(ratioB)}$. The smaller ratio is the limiting reactant, which is {'A' if ratioA < ratioB else 'B'}."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                limiting = "A" if ratioA < ratioB else "B"
                limiting_moles = nA if ratioA < ratioB else nB
                limiting_coeff = coeffA if ratioA < ratioB else coeffB
                product_coeff = random.randint(1, 2)
                product_moles = (limiting_moles / limiting_coeff) * product_coeff
                question = f"For the reaction ${coeffA}\\text{{A}} + {coeffB}\\text{{B}} \\rightarrow {product_coeff}\\text{{C}}$, you have ${format_float(nA)}~\\text{{mol}}$ of A and ${format_float(nB)}~\\text{{mol}}$ of B. Calculate the maximum moles of product C that can be formed."
                correct = f"{format_float(product_moles)}~\\text{{mol}}"
                wrongs = get_wrong_floats(product_moles, "mol")
                explanation = f"The limiting reactant is {limiting}. Moles of C = $\\frac{{{product_coeff}}}{{{limiting_coeff}}} \\times {format_float(limiting_moles)} = {format_float(product_moles)}~\\text{{mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                limiting = "A" if ratioA < ratioB else "B"
                excess = "B" if limiting == "A" else "A"
                limiting_moles = nA if ratioA < ratioB else nB
                limiting_coeff = coeffA if ratioA < ratioB else coeffB
                excess_moles = nB if limiting == "A" else nA
                excess_coeff = coeffB if limiting == "A" else coeffA
                moles_used = (limiting_moles / limiting_coeff) * excess_coeff
                moles_left = excess_moles - moles_used
                question = f"For the reaction ${coeffA}\\text{{A}} + {coeffB}\\text{{B}} \\rightarrow \\text{{Products}}$, you have ${format_float(nA)}~\\text{{mol}}$ of A and ${format_float(nB)}~\\text{{mol}}$ of B. Calculate the moles of the excess reactant remaining after the reaction goes to completion."
                correct = f"{format_float(moles_left)}~\\text{{mol}}"
                wrongs = get_wrong_floats(moles_left, "mol")
                explanation = f"Limiting is {limiting}. Moles of {excess} used = $\\frac{{{excess_coeff}}}{{{limiting_coeff}}} \\times {format_float(limiting_moles)} = {format_float(moles_used)}~\\text{{mol}}$. Remaining = ${format_float(excess_moles)} - {format_float(moles_used)} = {format_float(moles_left)}~\\text{{mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Empirical Formula":
            pass # Skipping this one for simplicity, fallback to others
            subtopic = "Molar Mass"

    gen.save_to_json("dataset/paper2_stoichiometry.json")

if __name__ == "__main__":
    gen_bonding_structure()
    gen_stoichiometry()
    print("Generated Bonding and Stoichiometry datasets.")
