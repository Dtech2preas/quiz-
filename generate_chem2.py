import json
import random
import math
import sympy as sp
from generators_common import TopicGenerator

def format_float(val, decimals=2):
    return f"{val:.{decimals}f}".rstrip('0').rstrip('.') if '.' in f"{val:.{decimals}f}" else f"{val:.{decimals}f}"

def format_val_unit(val, unit, decimals=None):
    if decimals is not None and isinstance(val, float):
        v_str = format_float(val, decimals)
    else:
        v_str = str(val) if isinstance(val, int) else format_float(val)
    if not unit:
        return v_str
    return f"{v_str}~{unit}"

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

    res = [format_val_unit(x, unit, decimals) for x in wrongs if abs(x - correct_val) > 1e-9]
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

    res = [format_val_unit(x, unit) for x in wrongs if x != correct_val]
    return res[:count]

def gen_acids_bases():
    topic = "Acids, Bases & Salts"
    prefix = "CHEM_AB"
    subtopics = ["pH Calculations", "Titration", "Kw and pOH", "Strong/Weak Acids & Bases"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "pH Calculations":
            conc = random.choice([1e-1, 1e-2, 1e-3, 1e-4, 5e-2, 2.5e-3, 1.5e-4])
            pH = -math.log10(conc)
            if difficulty == "easy":
                question = f"Calculate the pH of a ${conc:.1e}~\\text{{mol/dm}}^3$ strong monoprotic acid solution."
                correct = f"{format_float(pH, 2)}"
                wrongs = get_wrong_floats(pH, "", decimals=2)
                explanation = f"Using $\\text{{pH}} = -\\log[\\text{{H}}^+] = -\\log({conc:.1e}) \\approx {format_float(pH, 2)}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                # Find [H+] from pH
                target_pH = round(random.uniform(1.0, 13.0), 1)
                target_H = 10**(-target_pH)
                target_sci = f"{target_H:.2e}".replace("e", "\\times 10^{") + "}"
                question = f"A solution has a pH of ${target_pH}$. Calculate the hydrogen ion concentration, $[\\text{{H}}^+]$."
                correct = f"{target_sci}~\\text{{mol/dm}}^3"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}~\\text{mol/dm}^3" for w in [target_H*10, target_H/10, target_H*2, target_H/2, target_H*100, target_H/100]]
                explanation = f"Using $[\\text{{H}}^+] = 10^{{-\\text{{pH}}}} = 10^{{-{target_pH}}} = {target_sci}~\\text{{mol/dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Weak acid pH
                Ka = random.choice([1.8e-5, 6.5e-5, 4.5e-4, 1.3e-3])
                C_a = random.choice([0.1, 0.05, 0.01])
                # [H+] = sqrt(Ka * Ca)
                H_ion = math.sqrt(Ka * C_a)
                pH_weak = -math.log10(H_ion)
                Ka_sci = f"{Ka:.1e}".replace("e", "\\times 10^{") + "}"
                question = f"Calculate the pH of a ${C_a}~\\text{{mol/dm}}^3$ solution of a weak acid with $K_a = {Ka_sci}$. Assume $[\\text{{HA}}] \\approx C_a$."
                correct = f"{format_float(pH_weak, 2)}"
                wrongs = get_wrong_floats(pH_weak, "", decimals=2)
                explanation = f"Using $[\\text{{H}}^+] \\approx \\sqrt{{K_a C_a}} = \\sqrt{{({Ka_sci})({C_a})}} = {H_ion:.2e}$. Then $\\text{{pH}} = -\\log({H_ion:.2e}) \\approx {format_float(pH_weak, 2)}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Titration":
            c_a = random.choice([0.1, 0.2, 0.05])
            v_a = random.choice([10.0, 20.0, 25.0]) # cm^3
            v_b = random.uniform(15.0, 30.0) # cm^3
            if difficulty == "easy":
                # 1:1 ratio
                c_b = (c_a * v_a) / v_b
                question = f"In a titration, ${format_float(v_a)}~\\text{{cm}}^3$ of ${c_a}~\\text{{mol/dm}}^3$ $\\text{{HCl}}$ is neutralized by ${format_float(v_b)}~\\text{{cm}}^3$ of $\\text{{NaOH}}$. Calculate the concentration of the $\\text{{NaOH}}$ solution."
                correct = f"{format_float(c_b)}~\\text{{mol/dm}}^3"
                wrongs = get_wrong_floats(c_b, "\\text{mol/dm}^3")
                explanation = f"Using $\\frac{{c_a v_a}}{{n_a}} = \\frac{{c_b v_b}}{{n_b}} \\Rightarrow c_b = \\frac{{c_a v_a}}{{v_b}} = \\frac{{({c_a})({format_float(v_a)})}}{{{format_float(v_b)}}} = {format_float(c_b)}~\\text{{mol/dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                # 1:2 ratio e.g., H2SO4 + 2NaOH -> Na2SO4 + 2H2O
                c_b = (2 * c_a * v_a) / v_b
                question = f"In a titration, ${format_float(v_a)}~\\text{{cm}}^3$ of ${c_a}~\\text{{mol/dm}}^3$ $\\text{{H}}_2\\text{{SO}}_4$ is exactly neutralized by ${format_float(v_b)}~\\text{{cm}}^3$ of $\\text{{NaOH}}$ solution. Calculate the concentration of the $\\text{{NaOH}}$ solution."
                correct = f"{format_float(c_b)}~\\text{{mol/dm}}^3"
                wrongs = get_wrong_floats(c_b, "\\text{mol/dm}^3")
                explanation = f"Using $\\frac{{c_a v_a}}{{n_a}} = \\frac{{c_b v_b}}{{n_b}} \\Rightarrow \\frac{{({c_a})({format_float(v_a)})}}{{1}} = \\frac{{c_b({format_float(v_b)})}}{{2}} \\Rightarrow c_b = \\frac{{2({c_a})({format_float(v_a)})}}{{{format_float(v_b)}}} = {format_float(c_b)}~\\text{{mol/dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Find mass of solid acid or base
                mass = random.uniform(0.5, 2.0) # g of solid NaOH
                M_NaOH = 40.0
                moles_b = mass / M_NaOH
                v_a_dm = v_a / 1000
                c_a_hard = moles_b / v_a_dm
                question = f"A ${format_float(mass)}~\\text{{g}}$ sample of impure solid $\\text{{NaOH}}$ ($M = {M_NaOH}~\\text{{g/mol}}$) is dissolved and completely neutralizes ${format_float(v_a)}~\\text{{cm}}^3$ of $\\text{{HCl}}$ solution with unknown concentration. Assuming the impurity does not react, calculate the concentration of the $\\text{{HCl}}$ if the sample was 100% pure."
                correct = f"{format_float(c_a_hard)}~\\text{{mol/dm}}^3"
                wrongs = get_wrong_floats(c_a_hard, "\\text{mol/dm}^3")
                explanation = f"Moles of $\\text{{NaOH}} = \\frac{{{format_float(mass)}}}{{{M_NaOH}}} = {format_float(moles_b, 4)}~\\text{{mol}}$. Moles of $\\text{{HCl}}$ = Moles of $\\text{{NaOH}} = {format_float(moles_b, 4)}$. $C_{{\\text{{HCl}}}} = \\frac{{n}}{{V}} = \\frac{{{format_float(moles_b, 4)}}}{{{format_float(v_a/1000, 3)}}} = {format_float(c_a_hard)}~\\text{{mol/dm}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Kw and pOH":
            pOH = random.choice([2, 3, 4, 10, 11, 12])
            OH_conc = 10**(-pOH)
            if difficulty == "easy":
                pH = 14 - pOH
                question = f"A solution has a pOH of ${pOH}$. Calculate its pH at $25^\\circ\\text{{C}}$."
                correct = f"{pH}"
                wrongs = get_wrong_ints(pH, "")
                explanation = f"Using $\\text{{pH}} + \\text{{pOH}} = 14 \\Rightarrow \\text{{pH}} = 14 - {pOH} = {pH}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                OH_sci = f"{OH_conc:.1e}".replace("e", "\\times 10^{") + "}"
                pH_OH = 14 - pOH
                question = f"A solution has a hydroxide ion concentration $[\\text{{OH}}^-] = {OH_sci}~\\text{{mol/dm}}^3$. Calculate its pH at $25^\\circ\\text{{C}}$."
                correct = f"{pH_OH}"
                wrongs = get_wrong_ints(pH_OH, "")
                explanation = f"$\\text{{pOH}} = -\\log({OH_sci}) = {pOH}$. Then $\\text{{pH}} = 14 - {pOH} = {pH_OH}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Kw at different temp
                Kw_new = random.choice([2e-14, 5e-14, 8e-14])
                Kw_sci = f"{Kw_new:.1e}".replace("e", "\\times 10^{") + "}"
                pH_neutral = -math.log10(math.sqrt(Kw_new))
                question = f"At a certain temperature, the ion-product constant for water is $K_w = {Kw_sci}$. Calculate the pH of pure water at this temperature."
                correct = f"{format_float(pH_neutral, 2)}"
                wrongs = get_wrong_floats(pH_neutral, "", decimals=2)
                explanation = f"In pure water, $[\\text{{H}}^+] = \\sqrt{{K_w}} = \\sqrt{{{Kw_sci}}} = {math.sqrt(Kw_new):.2e}$. $\\text{{pH}} = -\\log({math.sqrt(Kw_new):.2e}) \\approx {format_float(pH_neutral, 2)}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Strong/Weak Acids & Bases":
            acids = [("HCl", "strong acid"), ("H2SO4", "strong acid"), ("HNO3", "strong acid"), ("CH3COOH", "weak acid"), ("H2CO3", "weak acid")]
            acid, a_type = random.choice(acids)
            if difficulty == "easy":
                question = f"Classify $\\text{{{acid}}}$ as a strong or weak acid."
                correct = a_type
                wrongs = ["weak acid" if a_type == "strong acid" else "strong acid", "strong base", "weak base", "neutral salt"]
                explanation = f"$\\text{{{acid}}}$ is a {a_type}."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"Which of the following describes the dissociation of a strong acid in water?"
                correct = "It completely ionizes in water."
                wrongs = [
                    "It partially ionizes in water.",
                    "It does not ionize in water.",
                    "It acts as a strong base.",
                    "It produces a high concentration of OH- ions."
                ]
                explanation = "A strong acid completely ionizes (dissociates) in aqueous solution to produce H+ ions."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                weak_acid = "CH3COOH"
                c = random.choice([0.1, 0.2])
                pH = round(random.uniform(2.5, 3.5), 1)
                H_conc = 10**(-pH)
                percent = (H_conc / c) * 100
                question = f"A ${c}~\\text{{mol/dm}}^3$ solution of $\\text{{{weak_acid}}}$ has a pH of ${pH}$. Calculate the percentage ionization of the acid."
                correct = f"{format_float(percent, 2)}\\%"
                wrongs = get_wrong_floats(percent, "\\%", decimals=2)
                explanation = f"$[\\text{{H}}^+] = 10^{{-\\text{{pH}}}} = 10^{{-{pH}}} = {H_conc:.2e}$. Percentage ionization = $\\frac{{[\\text{{H}}^+]}}{{{c}}} \\times 100 = \\frac{{{H_conc:.2e}}}{{{c}}} \\times 100 \\approx {format_float(percent, 2)}\\%$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper2_acids_bases.json")

def gen_electrochemistry():
    topic = "Electrochemistry"
    prefix = "CHEM_ELEC"
    subtopics = ["Galvanic Cells", "Electrolytic Cells", "Standard Electrode Potentials", "Faraday's Laws"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Galvanic Cells":
            metals = [("Zn", -0.76), ("Cu", 0.34), ("Ag", 0.80), ("Fe", -0.44), ("Mg", -2.37)]
            m1, m2 = random.sample(metals, 2)
            if m1[1] > m2[1]:
                m1, m2 = m2, m1 # m1 is more negative (anode), m2 is cathode
            anode, cathode = m1[0], m2[0]
            E_cell = m2[1] - m1[1]
            if difficulty == "easy":
                question = f"In a standard galvanic cell made of a $\\text{{{anode}}}$ half-cell ($E^\\circ = {m1[1]}~\\text{{V}}$) and a $\\text{{{cathode}}}$ half-cell ($E^\\circ = {m2[1]}~\\text{{V}}$), which electrode acts as the anode?"
                correct = f"$\\text{{{anode}}}$"
                wrongs = [f"$\\text{{{cathode}}}$", "Salt bridge", "Voltmeter", "Electrolyte"]
                explanation = f"The anode is the site of oxidation. The more negative reduction potential (${m1[1]}~\\text{{V}}$) undergoes oxidation, so $\\text{{{anode}}}$ is the anode."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"Calculate the standard cell potential ($E^\\circ_{{\\text{{cell}}}}$) for a galvanic cell consisting of $\\text{{{anode}}}$ ($E^\\circ = {m1[1]}~\\text{{V}}$) and $\\text{{{cathode}}}$ ($E^\\circ = {m2[1]}~\\text{{V}}$)."
                correct = f"{format_float(E_cell)}~\\text{{V}}"
                wrongs = get_wrong_floats(E_cell, "\\text{V}")
                explanation = f"Using $E^\\circ_{{\\text{{cell}}}} = E^\\circ_{{\\text{{cathode}}}} - E^\\circ_{{\\text{{anode}}}} = {m2[1]} - ({m1[1]}) = {format_float(E_cell)}~\\text{{V}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Spontaneity
                spontaneous = "Yes" if E_cell > 0 else "No" # Always yes here because of how we sorted, let's mix it up
                target_E = E_cell if random.choice([True, False]) else -E_cell
                if target_E < 0:
                    question = f"A reaction has a standard cell potential of $E^\\circ_{{\\text{{cell}}}} = {format_float(target_E)}~\\text{{V}}$. Is this redox reaction spontaneous under standard conditions?"
                    correct = "No"
                    wrongs = ["Yes", "Only at high temperatures", "Only at low temperatures", "Depends on the salt bridge"]
                    explanation = f"A negative standard cell potential ($E^\\circ_{{\\text{{cell}}}} < 0$) indicates a non-spontaneous reaction."
                    gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
                else:
                    question = f"A reaction has a standard cell potential of $E^\\circ_{{\\text{{cell}}}} = {format_float(target_E)}~\\text{{V}}$. Is this redox reaction spontaneous under standard conditions?"
                    correct = "Yes"
                    wrongs = ["No", "Only at high temperatures", "Only at low temperatures", "Depends on the salt bridge"]
                    explanation = f"A positive standard cell potential ($E^\\circ_{{\\text{{cell}}}} > 0$) indicates a spontaneous reaction."
                    gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Electrolytic Cells":
            if difficulty == "easy":
                question = "In an electrolytic cell, what is the charge of the anode and what process occurs there?"
                correct = "Positive, Oxidation"
                wrongs = ["Negative, Oxidation", "Positive, Reduction", "Negative, Reduction", "Neutral, Oxidation", "Neutral, Reduction"]
                explanation = "In an electrolytic cell, the anode is connected to the positive terminal of the power source, and oxidation always occurs at the anode."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = "During the electrolysis of concentrated sodium chloride ($\\text{NaCl}$) solution (brine), which gas is produced at the anode?"
                correct = "Chlorine gas ($\\text{Cl}_2$)"
                wrongs = ["Oxygen gas ($\\text{O}_2$)", "Hydrogen gas ($\\text{H}_2$)", "Sodium vapor ($\\text{Na}$)", "Water vapor ($\\text{H}_2\\text{O}$)"]
                explanation = "Chloride ions ($\\text{Cl}^-$) are oxidized at the anode to produce chlorine gas ($\\text{Cl}_2$). Oxygen is not formed because of overpotential effects."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                question = "During the electrolysis of molten copper(II) chloride ($\\text{CuCl}_2$), write the half-reaction that occurs at the cathode."
                correct = "$\\text{Cu}^{2+} + 2\\text{e}^- \\rightarrow \\text{Cu}$"
                wrongs = [
                    "$\\text{Cu} \\rightarrow \\text{Cu}^{2+} + 2\\text{e}^-$",
                    "$2\\text{Cl}^- \\rightarrow \\text{Cl}_2 + 2\\text{e}^-$",
                    "$\\text{Cl}_2 + 2\\text{e}^- \\rightarrow 2\\text{Cl}^-$",
                    "$\\text{Cu}^+ + \\text{e}^- \\rightarrow \\text{Cu}$",
                    "$\\text{Cu}^{2+} + \\text{e}^- \\rightarrow \\text{Cu}^+$"
                ]
                explanation = "Reduction occurs at the cathode. Copper(II) ions gain two electrons to form solid copper: $\\text{Cu}^{2+} + 2\\text{e}^- \\rightarrow \\text{Cu}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Standard Electrode Potentials":
            # Just another way to ask Galvanic questions or ranking
            pass
            subtopic = "Faraday's Laws" # fallback

        elif subtopic == "Faraday's Laws":
            I = random.uniform(1.0, 10.0)
            t_min = random.randint(10, 60)
            t_sec = t_min * 60
            Q_total = I * t_sec
            if difficulty == "easy":
                question = f"A current of ${format_float(I)}~\\text{{A}}$ is passed through an electrolytic cell for ${t_min}~\\text{{minutes}}$. Calculate the total charge passed in Coulombs."
                correct = f"{format_float(Q_total)}~\\text{{C}}"
                wrongs = get_wrong_floats(Q_total, "\\text{C}")
                explanation = f"Using $Q = It = ({format_float(I)})({t_min} \\times 60) = ({format_float(I)})({t_sec}) = {format_float(Q_total)}~\\text{{C}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                F = 96485
                moles_e = Q_total / F
                question = f"Calculate the number of moles of electrons transferred when a charge of ${format_float(Q_total)}~\\text{{C}}$ passes through a cell. (Faraday's constant $F = 96485~\\text{{C/mol}}$)"
                correct = f"{format_float(moles_e, 3)}~\\text{{mol}}"
                wrongs = get_wrong_floats(moles_e, "\\text{mol}", decimals=3)
                explanation = f"Using $n_e = \\frac{{Q}}{{F}} = \\frac{{{format_float(Q_total)}}}{{96485}} \\approx {format_float(moles_e, 3)}~\\text{{mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                F = 96485
                metal = random.choice([("Ag", 107.9, 1), ("Cu", 63.5, 2), ("Zn", 65.4, 2), ("Al", 27.0, 3)])
                moles_e = Q_total / F
                moles_metal = moles_e / metal[2]
                mass = moles_metal * metal[1]
                question = f"A current of ${format_float(I)}~\\text{{A}}$ is passed through a solution containing $\\text{{{metal[0]}}}^{{{metal[2]}+}}$ ions for ${t_min}~\\text{{minutes}}$. Calculate the mass of $\\text{{{metal[0]}}}$ deposited at the cathode. ($M_\\text{{{metal[0]}}} = {metal[1]}~\\text{{g/mol}}$, $F = 96485~\\text{{C/mol}}$)"
                correct = f"{format_float(mass)}~\\text{{g}}"
                wrongs = get_wrong_floats(mass, "\\text{g}")
                explanation = f"$Q = It = {format_float(Q_total)}~\\text{{C}}$. $n_e = \\frac{{Q}}{{F}} = {format_float(moles_e, 4)}~\\text{{mol}}$. The ion requires ${metal[2]}~\\text{{mol}}$ of electrons per mole of metal, so $n_{{\\text{{metal}}}} = \\frac{{{format_float(moles_e, 4)}}}{{{metal[2]}}} = {format_float(moles_metal, 4)}~\\text{{mol}}$. Mass = $n \\times M = ({format_float(moles_metal, 4)})({metal[1]}) \\approx {format_float(mass)}~\\text{{g}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper2_electrochemistry.json")

def gen_atomic_nuclear():
    topic = "Atomic & Nuclear Physics"
    prefix = "PHYS_AN"
    subtopics = ["Photoelectric Effect", "Atomic Spectra", "Radioactivity", "Nuclear Reactions"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Photoelectric Effect":
            h = 6.63e-34
            c = 3.0e8
            f = random.uniform(4.0, 10.0) * 1e14
            E_photon = h * f
            if difficulty == "easy":
                f_sci = f"{f:.2e}".replace("e", "\\times 10^{") + "}"
                E_sci = f"{E_photon:.2e}".replace("e", "\\times 10^{") + "}"
                question = f"Calculate the energy of a photon with a frequency of ${f_sci}~\\text{{Hz}}$. ($h = 6.63 \\times 10^{{-34}}~\\text{{J\\cdot s}}$)"
                correct = f"{E_sci}~\\text{{J}}"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}~\\text{J}" for w in [E_photon*10, E_photon/10, E_photon*2, E_photon/2, E_photon*4, E_photon/4, E_photon*100]]
                explanation = f"Using $E = hf = (6.63 \\times 10^{{-34}})({f_sci}) = {E_sci}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                W = random.uniform(2.0, 4.0) * 1e-19
                f_0 = W / h
                W_sci = f"{W:.2e}".replace("e", "\\times 10^{") + "}"
                f_0_sci = f"{f_0:.2e}".replace("e", "\\times 10^{") + "}"
                question = f"A metal has a work function of ${W_sci}~\\text{{J}}$. Calculate its threshold frequency. ($h = 6.63 \\times 10^{{-34}}~\\text{{J\\cdot s}}$)"
                correct = f"{f_0_sci}~\\text{{Hz}}"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}~\\text{Hz}" for w in [f_0*10, f_0/10, f_0*2, f_0/2, f_0*4, f_0/4, f_0*100]]
                explanation = f"Using $W_0 = hf_0 \\Rightarrow f_0 = \\frac{{W_0}}{{h}} = \\frac{{{W_sci}}}{{6.63 \\times 10^{{-34}}}} \\approx {f_0_sci}~\\text{{Hz}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                W = random.uniform(2.0, 4.0) * 1e-19
                f_incident = random.uniform(8.0, 15.0) * 1e14
                E_inc = h * f_incident
                K_max = E_inc - W
                K_sci = f"{K_max:.2e}".replace("e", "\\times 10^{") + "}"
                W_sci = f"{W:.2e}".replace("e", "\\times 10^{") + "}"
                f_inc_sci = f"{f_incident:.2e}".replace("e", "\\times 10^{") + "}"
                question = f"Light of frequency ${f_inc_sci}~\\text{{Hz}}$ shines on a metal with a work function of ${W_sci}~\\text{{J}}$. Calculate the maximum kinetic energy of the emitted photoelectrons. ($h = 6.63 \\times 10^{{-34}}~\\text{{J\\cdot s}}$)"
                correct = f"{K_sci}~\\text{{J}}"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}~\\text{J}" for w in [K_max*10, K_max/10, K_max*2, K_max/2, E_inc+W, E_inc, W]]
                explanation = f"Using $E = W_0 + K_{{\\max}} \\Rightarrow K_{{\\max}} = hf - W_0 = (6.63 \\times 10^{{-34}})({f_inc_sci}) - {W_sci} = {K_sci}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Atomic Spectra":
            n_i = random.randint(2, 6)
            n_f = random.randint(1, n_i - 1)
            R_H = 1.097e7
            inv_lambda = R_H * (1/(n_f**2) - 1/(n_i**2))
            lam = 1 / inv_lambda
            lam_nm = lam * 1e9
            if difficulty == "easy":
                question = f"An electron in a hydrogen atom transitions from energy level $n={n_i}$ to $n={n_f}$. Is a photon absorbed or emitted?"
                correct = "Emitted"
                wrongs = ["Absorbed", "Neither", "Both", "Reflected", "Scattered"]
                explanation = f"The electron moves to a lower energy state (from $n={n_i}$ to $n={n_f}$), so energy is released in the form of an emitted photon."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"Calculate the wavelength of the photon emitted when an electron in hydrogen transitions from $n={n_i}$ to $n={n_f}$. ($R_H = 1.097 \\times 10^7~\\text{{m}}^{{-1}}$)"
                correct = f"{format_float(lam_nm)}~\\text{{nm}}"
                wrongs = get_wrong_floats(lam_nm, "\\text{nm}")
                explanation = f"Using Rydberg formula: $\\frac{{1}}{{\\lambda}} = R_H \\left(\\frac{{1}}{{n_f^2}} - \\frac{{1}}{{n_i^2}}\\right) = (1.097 \\times 10^7) \\left(\\frac{{1}}{{{n_f}^2}} - \\frac{{1}}{{{n_i}^2}}\\right) \\approx {inv_lambda:.2e}~\\text{{m}}^{{-1}}$. $\\lambda = \\frac{{1}}{{{inv_lambda:.2e}}} \\approx {lam:.2e}~\\text{{m}} = {format_float(lam_nm)}~\\text{{nm}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                dE = (6.63e-34 * 3.0e8) / lam
                dE_eV = dE / 1.6e-19
                question = f"Calculate the energy difference (in eV) between the $n={n_i}$ and $n={n_f}$ energy levels of a hydrogen atom. ($1~\\text{{eV}} = 1.6 \\times 10^{{-19}}~\\text{{J}}$)"
                correct = f"{format_float(dE_eV)}~\\text{{eV}}"
                wrongs = get_wrong_floats(dE_eV, "\\text{eV}")
                explanation = f"Energy levels in hydrogen: $E_n = \\frac{{-13.6}}{{n^2}}~\\text{{eV}}$. $\\Delta E = E_{{{n_i}}} - E_{{{n_f}}} = \\frac{{-13.6}}{{{n_i}^2}} - \\frac{{-13.6}}{{{n_f}^2}} = {format_float(dE_eV)}~\\text{{eV}}$ (magnitude)."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Radioactivity":
            T_half = random.randint(5, 50)
            t = T_half * random.randint(2, 5)
            N_0 = random.randint(100, 1000)
            N_t = N_0 * (0.5)**(t / T_half)
            if difficulty == "easy":
                question = f"A radioactive isotope has a half-life of ${T_half}~\\text{{days}}$. How much of a ${N_0}~\\text{{g}}$ sample will remain after ${T_half * 2}~\\text{{days}}$?"
                ans = N_0 * 0.25
                correct = f"{format_float(ans)}~\\text{{g}}"
                wrongs = get_wrong_floats(ans, "\\text{g}")
                explanation = f"After 2 half-lives, the remaining amount is $N_0 \\times \\left(\\frac{{1}}{{2}}\\right)^2 = {N_0} \\times 0.25 = {format_float(ans)}~\\text{{g}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"A sample of a radioactive substance initially contains ${N_0}~\\text{{g}}$. After ${t}~\\text{{days}}$, ${format_float(N_t)}~\\text{{g}}$ remains. Calculate the half-life of the substance."
                correct = f"{T_half}~\\text{{days}}"
                wrongs = get_wrong_ints(T_half, "\\text{days}")
                explanation = f"Using $N(t) = N_0 \\left(\\frac{{1}}{{2}}\\right)^{{\\frac{{t}}{{T_{{1/2}}}}}} \\Rightarrow {format_float(N_t)} = {N_0} \\left(\\frac{{1}}{{2}}\\right)^{{\\frac{{{t}}}{{T_{{1/2}}}}}} \\Rightarrow \\left(\\frac{{1}}{{2}}\\right)^{{\\frac{{{t}}}{{T_{{1/2}}}}}} = {format_float(N_t / N_0, 4)} \\Rightarrow \\frac{{{t}}}{{T_{{1/2}}}} = {t / T_half} \\Rightarrow T_{{1/2}} = {T_half}~\\text{{days}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                lam = math.log(2) / T_half
                activity_0 = lam * (N_0 * 1e20) # arbitrary scaling for activity
                A_sci = f"{activity_0:.2e}".replace("e", "\\times 10^{") + "}"
                question = f"The decay constant of a radioactive isotope is ${format_float(lam, 4)}~\\text{{days}}^{{-1}}$. Calculate its half-life."
                correct = f"{format_float(T_half)}~\\text{{days}}"
                wrongs = get_wrong_floats(T_half, "\\text{days}")
                explanation = f"Using $\\lambda = \\frac{{\\ln(2)}}{{T_{{1/2}}}} \\Rightarrow T_{{1/2}} = \\frac{{\\ln(2)}}{{\\lambda}} = \\frac{{0.693}}{{{format_float(lam, 4)}}} \\approx {format_float(T_half)}~\\text{{days}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Nuclear Reactions":
            if difficulty == "easy":
                question = "In an alpha decay process, an unstable nucleus emits an alpha particle. What is an alpha particle composed of?"
                correct = "2 protons and 2 neutrons"
                wrongs = ["1 proton and 1 neutron", "2 protons and 2 electrons", "4 protons", "4 neutrons", "1 electron"]
                explanation = "An alpha particle is equivalent to a helium nucleus, consisting of 2 protons and 2 neutrons ($^4_2\\text{He}$)."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                element = "U"
                A = 238
                Z = 92
                question = f"An isotope of Uranium, $^{{{A}}}_{{{Z}}}\\text{{U}}$, undergoes alpha decay. What are the mass number (A) and atomic number (Z) of the resulting daughter nucleus?"
                correct = f"A = {A-4}, Z = {Z-2}"
                wrongs = [f"A = {A}, Z = {Z+1}", f"A = {A-2}, Z = {Z-4}", f"A = {A}, Z = {Z-1}", f"A = {A-4}, Z = {Z}"]
                explanation = f"An alpha particle is $^{{4}}_{{2}}\\text{{He}}$. The new mass number is $A - 4 = {A} - 4 = {A-4}$. The new atomic number is $Z - 2 = {Z} - 2 = {Z-2}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                question = f"A nucleus $^{{14}}_{{6}}\\text{{C}}$ undergoes beta-minus ($\\beta^-$) decay. What are the mass number (A) and atomic number (Z) of the resulting nucleus?"
                correct = "A = 14, Z = 7"
                wrongs = ["A = 14, Z = 5", "A = 13, Z = 6", "A = 14, Z = 6", "A = 10, Z = 4", "A = 15, Z = 7"]
                explanation = "In $\\beta^-$ decay, a neutron converts to a proton and an electron. The mass number (A) stays the same (14), and the atomic number (Z) increases by 1 ($6 + 1 = 7$), resulting in Nitrogen-14."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper2_atomic_nuclear.json")

def gen_kinetics_equilibrium():
    topic = "Chemical Kinetics & Equilibrium"
    prefix = "CHEM_KIN"
    subtopics = ["Reaction Rates", "Collision Theory", "Le Chatelier's Principle", "Equilibrium Constant (Kc)"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Reaction Rates":
            dC = random.uniform(0.1, 1.0)
            dt = random.randint(10, 60)
            rate = dC / dt
            if difficulty == "easy":
                question = f"The concentration of a reactant decreases by ${format_float(dC)}~\\text{{mol/dm}}^3$ in ${dt}~\\text{{s}}$. Calculate the average rate of reaction."
                correct = f"{format_float(rate, 4)}~\\text{{mol}}/(\\text{{dm}}^3 \\cdot \\text{{s}})"
                wrongs = get_wrong_floats(rate, "\\text{mol}/(\\text{dm}^3 \\cdot \\text{s})", decimals=4)
                explanation = f"Using Rate = $\\frac{{\\Delta [\\text{{Reactant}}]}}{{\\Delta t}} = \\frac{{{format_float(dC)}}}{{{dt}}} \\approx {format_float(rate, 4)}~\\text{{mol}}/(\\text{{dm}}^3 \\cdot \\text{{s}})$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                v_gas = random.randint(20, 100)
                rate_gas = v_gas / dt
                question = f"In a reaction, ${v_gas}~\\text{{cm}}^3$ of hydrogen gas is produced in ${dt}~\\text{{s}}$. Calculate the rate of production of hydrogen gas."
                correct = f"{format_float(rate_gas)}~\\text{{cm}}^3/\\text{{s}}"
                wrongs = get_wrong_floats(rate_gas, "\\text{cm}^3/\\text{s}")
                explanation = f"Rate = $\\frac{{\\Delta V}}{{\\Delta t}} = \\frac{{{v_gas}}}{{{dt}}} = {format_float(rate_gas)}~\\text{{cm}}^3/\\text{{s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                moles_prod = random.uniform(0.01, 0.1)
                mass = moles_prod * 44.0 # e.g. CO2
                rate_mass = mass / dt
                question = f"A reaction produces $\\text{{CO}}_2$ gas ($M = 44.0~\\text{{g/mol}}$). If ${format_float(moles_prod, 3)}~\\text{{moles}}$ of $\\text{{CO}}_2$ are produced in ${dt}~\\text{{s}}$, calculate the rate of reaction in $\\text{{g/s}}$."
                correct = f"{format_float(rate_mass, 4)}~\\text{{g/s}}"
                wrongs = get_wrong_floats(rate_mass, "\\text{g/s}", decimals=4)
                explanation = f"Mass of $\\text{{CO}}_2$ = $n \\times M = ({format_float(moles_prod, 3)})(44.0) = {format_float(mass)}~\\text{{g}}$. Rate = $\\frac{{\\Delta m}}{{\\Delta t}} = \\frac{{{format_float(mass)}}}{{{dt}}} = {format_float(rate_mass, 4)}~\\text{{g/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Collision Theory":
            if difficulty == "easy":
                question = "According to collision theory, which of the following is required for a reaction to occur between two particles?"
                correct = "They must collide with sufficient energy and correct orientation."
                wrongs = [
                    "They must collide with low energy.",
                    "They must be in the gaseous state.",
                    "They just need to collide, regardless of energy.",
                    "They must collide with a catalyst.",
                    "They must be at high pressure."
                ]
                explanation = "An effective collision requires particles to collide with at least the activation energy and the correct spatial orientation."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = "How does increasing the temperature increase the rate of a chemical reaction?"
                correct = "It increases the number of particles with energy equal to or greater than the activation energy."
                wrongs = [
                    "It lowers the activation energy of the reaction.",
                    "It decreases the volume of the particles.",
                    "It increases the activation energy of the reaction.",
                    "It changes the orientation of the colliding particles."
                ]
                explanation = "Higher temperature increases the kinetic energy of particles, so a larger fraction of collisions has energy $\\ge E_a$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                question = "How does the addition of a positive catalyst increase the rate of a reaction?"
                correct = "It provides an alternative reaction pathway with a lower activation energy."
                wrongs = [
                    "It increases the kinetic energy of the reactant molecules.",
                    "It increases the concentration of the reactants.",
                    "It decreases the enthalpy change ($\\Delta H$) of the reaction.",
                    "It increases the temperature of the system."
                ]
                explanation = "A catalyst speeds up a reaction by offering a new pathway that requires less activation energy ($E_a$)."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Le Chatelier's Principle":
            if difficulty == "easy":
                question = "Consider the exothermic reaction at equilibrium: $\\text{N}_2(g) + 3\\text{H}_2(g) \\rightleftharpoons 2\\text{NH}_3(g)$. What will happen if the temperature is increased?"
                correct = "The equilibrium will shift to the left (reactants)."
                wrongs = [
                    "The equilibrium will shift to the right (products).",
                    "There will be no change.",
                    "The rate of both forward and reverse reactions will decrease.",
                    "More ammonia will be produced."
                ]
                explanation = "According to Le Chatelier's Principle, increasing temperature favors the endothermic direction. Since the forward reaction is exothermic, it shifts left."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = "Consider the reaction: $2\\text{SO}_2(g) + \\text{O}_2(g) \\rightleftharpoons 2\\text{SO}_3(g)$. How will an increase in pressure affect the equilibrium?"
                correct = "The equilibrium will shift to the right (products)."
                wrongs = [
                    "The equilibrium will shift to the left (reactants).",
                    "There will be no change.",
                    "The reaction will stop.",
                    "The concentration of sulfur dioxide will increase."
                ]
                explanation = "There are 3 moles of gas on the left and 2 on the right. Increasing pressure favors the side with fewer gas moles, which is the right."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                question = "For a reaction at equilibrium, what effect does adding a catalyst have on the equilibrium position and the equilibrium constant ($K_c$)?"
                correct = "No effect on equilibrium position; $K_c$ remains unchanged."
                wrongs = [
                    "Shifts equilibrium to the right; $K_c$ increases.",
                    "Shifts equilibrium to the right; $K_c$ remains unchanged.",
                    "No effect on equilibrium position; $K_c$ increases.",
                    "Shifts equilibrium to the left; $K_c$ decreases."
                ]
                explanation = "A catalyst increases both forward and reverse reaction rates equally, reaching equilibrium faster but not altering the position or $K_c$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Equilibrium Constant (Kc)":
            c_A = random.uniform(0.1, 1.0)
            c_B = random.uniform(0.1, 1.0)
            c_C = random.uniform(0.5, 2.0)
            if difficulty == "easy":
                Kc = (c_C) / (c_A * c_B)
                question = f"For the reaction $\\text{{A}}(aq) + \\text{{B}}(aq) \\rightleftharpoons \\text{{C}}(aq)$, the equilibrium concentrations are: $[\\text{{A}}] = {format_float(c_A)}~\\text{{M}}$, $[\\text{{B}}] = {format_float(c_B)}~\\text{{M}}$, $[\\text{{C}}] = {format_float(c_C)}~\\text{{M}}$. Calculate $K_c$."
                correct = f"{format_float(Kc)}"
                wrongs = get_wrong_floats(Kc, "")
                explanation = f"$K_c = \\frac{{[\\text{{C}}]}}{{[\\text{{A}}][\\text{{B}}]}} = \\frac{{{format_float(c_C)}}}{{({format_float(c_A)})({format_float(c_B)})}} = {format_float(Kc)}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                Kc = (c_C**2) / (c_A * c_B**3)
                question = f"For the reaction $\\text{{N}}_2(g) + 3\\text{{H}}_2(g) \\rightleftharpoons 2\\text{{NH}}_3(g)$, equilibrium concentrations are: $[\\text{{N}}_2] = {format_float(c_A)}~\\text{{M}}$, $[\\text{{H}}_2] = {format_float(c_B)}~\\text{{M}}$, $[\\text{{NH}}_3] = {format_float(c_C)}~\\text{{M}}$. Calculate $K_c$."
                correct = f"{format_float(Kc)}"
                wrongs = get_wrong_floats(Kc, "")
                explanation = f"$K_c = \\frac{{[\\text{{NH}}_3]^2}}{{[\\text{{N}}_2][\\text{{H}}_2]^3}} = \\frac{{{format_float(c_C)}^2}}{{({format_float(c_A)})({format_float(c_B)})^3}} = {format_float(Kc)}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                Kc_val = random.randint(10, 100)
                # Find [C]
                c_C_hard = math.sqrt(Kc_val * c_A * c_B)
                question = f"For the reaction $\\text{{A}}(g) + \\text{{B}}(g) \\rightleftharpoons 2\\text{{C}}(g)$, the equilibrium constant is $K_c = {Kc_val}$. If equilibrium concentrations of A and B are ${format_float(c_A)}~\\text{{M}}$ and ${format_float(c_B)}~\\text{{M}}$ respectively, calculate the equilibrium concentration of C."
                correct = f"{format_float(c_C_hard)}~\\text{{M}}"
                wrongs = get_wrong_floats(c_C_hard, "\\text{M}")
                explanation = f"$K_c = \\frac{{[\\text{{C}}]^2}}{{[\\text{{A}}][\\text{{B}}]}} \\Rightarrow {Kc_val} = \\frac{{[\\text{{C}}]^2}}{{({format_float(c_A)})({format_float(c_B)})}}$. So $[\\text{{C}}] = \\sqrt{{{Kc_val} \\times {format_float(c_A)} \\times {format_float(c_B)}}} = {format_float(c_C_hard)}~\\text{{M}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper2_kinetics_equilibrium.json")

if __name__ == "__main__":
    gen_acids_bases()
    gen_electrochemistry()
    gen_atomic_nuclear()
    gen_kinetics_equilibrium()
    print("Generated Acids/Bases, Electrochemistry, Atomic/Nuclear, and Kinetics datasets.")
