import json
import random
import math
import os
import itertools
from generator_base import TopicGenerator

def generate_wrong_answers_num(correct, is_float=False, is_scientific=False, steps=None, allow_neg=False, count=6):
    wrong = set()
    attempts = 0
    while len(wrong) < count and attempts < 200:
        attempts += 1
        if is_scientific:
            # vary mantissa and exponent
            parts = correct.split("x10^")
            if len(parts) != 2: continue
            try:
                m = float(parts[0])
                e = int(parts[1])
            except:
                continue

            w_m = m * random.choice([0.1, 10, 2, 0.5, 5, 1, random.uniform(0.5, 2)])
            w_e = e + random.randint(-3, 3)
            val = f"{w_m:.2f}x10^{w_e}"
            if val != correct:
                wrong.add(val)
        elif is_float:
            c = float(correct)
            variations = [c*10, c/10, c*2, c/2, c+10, c-10, c**2, math.sqrt(abs(c)) if c != 0 else 1]
            if steps: variations.extend(steps)
            for v in variations:
                val = f"{v:.2f}"
                if val != correct and (float(val) > 0 or allow_neg):
                    wrong.add(val)
                    if len(wrong) >= count: break
            # random variations
            while len(wrong) < count and attempts < 200:
                v = c * random.uniform(0.5, 2) + random.uniform(-10, 10)
                val = f"{v:.2f}"
                if val != correct and (float(val) > 0 or allow_neg):
                    wrong.add(val)
                attempts += 1
        else:
            c = int(correct)
            variations = [c*10, c*2, c+1, c-1, c+10, c-10, int(c/10), int(c/2)]
            if steps: variations.extend(steps)
            for v in variations:
                val = str(v)
                if val != correct and (int(val) >= 0 or allow_neg):
                    wrong.add(val)
                    if len(wrong) >= count: break
            while len(wrong) < count and attempts < 200:
                v = c + random.randint(-20, 20)
                val = str(v)
                if val != correct and (int(val) >= 0 or allow_neg):
                    wrong.add(val)
                attempts += 1
    return list(wrong)[:count]

# 1. Matter and Materials
def gen_matter():
    gen = TopicGenerator("Matter and Materials", "PSC_MAT", [
        "States of Matter", "Atomic Structure", "Periodic Table", "Chemical Bonding", "Kinetic Molecular Theory"
    ])

    while not gen.is_done():
        diff = random.choices(["easy", "medium", "hard"], [0.3, 0.5, 0.2])[0]
        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        if diff == "easy":
            choice = random.randint(1, 4)
            if choice == 1:
                z = random.randint(1, 118)
                n = random.randint(z, int(z * 1.5) + 1)
                ans = str(z + n)
                q = f"An atom of a hypothetical element has {z} protons and {n} neutrons. What is its mass number?"
                wrongs = generate_wrong_answers_num(ans, steps=[z, n, abs(n-z), z*2, n*2])
                exp = f"Mass Number (A) = Protons + Neutrons = {z} + {n} = {ans}."
                gen.add_question("Atomic Structure", diff, q, ans, wrongs, exp)
            elif choice == 2:
                a = random.randint(2, 250)
                z = random.randint(1, a - 1)
                ans = str(a - z)
                q = f"A neutral atom has a mass number of {a} and an atomic number of {z}. How many neutrons does it have?"
                wrongs = generate_wrong_answers_num(ans, steps=[a, z, a+z, z*2])
                exp = f"Neutrons = Mass Number - Atomic Number = {a} - {z} = {ans}."
                gen.add_question("Atomic Structure", diff, q, ans, wrongs, exp)
            elif choice == 3:
                z = random.randint(1, 118)
                a = random.randint(z, int(z * 1.5) + z)
                ans = str(z)
                q = f"How many electrons are in a neutral atom with atomic number {z} and mass number {a}?"
                wrongs = generate_wrong_answers_num(ans, steps=[a, a-z, a+z])
                exp = f"In a neutral atom, number of electrons = number of protons = atomic number = {z}."
                gen.add_question("Atomic Structure", diff, q, ans, wrongs, exp)
            else:
                c = random.randint(-200, 500)
                ans = f"{c + 273} K"
                q = f"Convert a temperature of {c} °C to Kelvin."
                wrongs = [f"{c - 273} K", f"{-c + 273} K", f"{273 - c} K", f"{c + 273 + 10} K", f"{c + 273 - 10} K", f"{c * 273} K"]
                exp = f"T(K) = T(°C) + 273 = {c} + 273 = {c+273} K."
                gen.add_question("States of Matter", diff, q, ans, wrongs, exp)

        elif diff == "medium":
            choice = random.randint(1, 3)
            if choice == 1:
                z = random.randint(3, 118)
                charge = random.randint(-3, 3)
                while charge == 0: charge = random.randint(-3, 3)
                ans = str(z - charge)
                charge_str = f"+{charge}" if charge > 0 else str(charge)
                q = f"An ion has an atomic number of {z} and a charge of {charge_str}. How many electrons does it have?"
                wrongs = generate_wrong_answers_num(ans, steps=[z, z+charge, abs(charge)])
                exp = f"Electrons = Protons - Charge = {z} - ({charge}) = {ans}."
                gen.add_question("Atomic Structure", diff, q, ans, wrongs, exp)
            elif choice == 2:
                # Core electrons
                z = random.randint(3, 20)
                if z <= 10: core = 2
                elif z <= 18: core = 10
                else: core = 18
                ans = str(core)
                q = f"How many core electrons does a neutral atom with atomic number {z} have?"
                wrongs = generate_wrong_answers_num(ans, steps=[z, z-core, 2, 8, 18])
                exp = f"For atomic number {z}, the noble gas core has {core} electrons."
                gen.add_question("Periodic Table", diff, q, ans, wrongs, exp)
            else:
                z = random.randint(3, 20)
                if z <= 2: valence = z; core = 0
                elif z <= 10: valence = z - 2; core = 2
                elif z <= 18: valence = z - 10; core = 10
                else: valence = z - 18; core = 18
                ans = str(valence)
                q = f"How many valence electrons does a neutral atom with atomic number {z} have?"
                wrongs = generate_wrong_answers_num(ans, steps=[core, z, 8-valence, 8])
                exp = f"With {z} electrons, there are {core} core electrons, leaving {valence} valence electrons."
                gen.add_question("Periodic Table", diff, q, ans, wrongs, exp)

        else: # hard
            choice = random.randint(1, 2)
            if choice == 1:
                iso1_mass = random.randint(10, 150)
                iso2_mass = iso1_mass + random.randint(1, 5)
                abund1 = random.randint(10, 90)
                abund2 = 100 - abund1
                rel_mass = (iso1_mass * abund1 + iso2_mass * abund2) / 100
                ans = f"{rel_mass:.2f}"
                q = f"An element has two isotopes: one with mass {iso1_mass} amu (abundance {abund1}%) and another with mass {iso2_mass} amu (abundance {abund2}%). Calculate the relative atomic mass."
                w_steps = [(iso1_mass + iso2_mass)/2, (iso1_mass * abund2 + iso2_mass * abund1)/100]
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=w_steps)
                exp = f"RAM = ({iso1_mass} * {abund1} + {iso2_mass} * {abund2}) / 100 = {ans} amu."
                gen.add_question("Atomic Structure", diff, q, ans, wrongs, exp)
            else:
                z = random.randint(5, 20)
                configs = {
                    5: "1s2 2s2 2p1", 6: "1s2 2s2 2p2", 7: "1s2 2s2 2p3", 8: "1s2 2s2 2p4",
                    9: "1s2 2s2 2p5", 10: "1s2 2s2 2p6", 11: "1s2 2s2 2p6 3s1", 12: "1s2 2s2 2p6 3s2",
                    13: "1s2 2s2 2p6 3s2 3p1", 14: "1s2 2s2 2p6 3s2 3p2", 15: "1s2 2s2 2p6 3s2 3p3",
                    16: "1s2 2s2 2p6 3s2 3p4", 17: "1s2 2s2 2p6 3s2 3p5", 18: "1s2 2s2 2p6 3s2 3p6",
                    19: "1s2 2s2 2p6 3s2 3p6 4s1", 20: "1s2 2s2 2p6 3s2 3p6 4s2"
                }
                ans = configs[z]
                # adding random identifier to make it unique
                ident = random.randint(100, 999)
                q = f"Element X-{ident} has an atomic number of {z}. What is its full spdf electron configuration for a neutral atom?"
                wrongs = [
                    configs.get(z+1, "1s2 2s2 2p6 3s2 3p6 4s2 3d1"),
                    configs.get(z-1, "1s2 2s2"),
                    ans.replace("2p6", "2p5").replace("3s2", "3s3") if "3s" in ans else ans.replace("2s2", "2s1 2p1"),
                    ans.replace("s2", "s1").replace("p6", "p5"),
                    "1s2 2s2 2p6 3s2 3p6 4s2" if z != 20 else "1s2 2s2 2p6 3s2 3p6",
                    "1s2 2s2 2p4 3s2", "1s2 2s2 2p6 3s1 3p1", "1s2 2s2 2p8"
                ]
                wrongs = [w for w in wrongs if w != ans]
                exp = f"Electrons fill in the order 1s, 2s, 2p, 3s, 3p, 4s. For {z} electrons, it is {ans}."
                gen.add_question("Atomic Structure", diff, q, ans, wrongs, exp)

    gen.save_to_json("dataset/grade10/physci_matter_materials.json")

# 2. Chemical Change
def gen_chemical():
    gen = TopicGenerator("Chemical Change", "PSC_CHE", [
        "Conservation of Mass", "Balancing Equations", "Stoichiometry", "Reactions in Aqueous Solutions"
    ])

    while not gen.is_done():
        diff = random.choices(["easy", "medium", "hard"], [0.3, 0.5, 0.2])[0]
        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        if diff == "easy":
            choice = random.randint(1, 3)
            if choice == 1:
                c_n = random.randint(1, 20)
                h_n = random.randint(2, 42)
                o_n = random.randint(0, 5)
                ans = str(c_n * 12 + h_n * 1 + o_n * 16)
                formula = f"C{c_n}H{h_n}" + (f"O{o_n}" if o_n > 0 else "")
                q = f"Calculate the molar mass of {formula} in g/mol. (C=12, H=1, O=16)"
                wrongs = generate_wrong_answers_num(ans, steps=[c_n*12, h_n*1, (c_n+h_n)*13])
                exp = f"Molar mass = ({c_n} * 12) + ({h_n} * 1) + ({o_n} * 16) = {ans} g/mol."
                gen.add_question("Stoichiometry", diff, q, ans, wrongs, exp)
            elif choice == 2:
                mass = random.randint(1, 500)
                mm = random.randint(10, 200)
                ans = f"{mass / mm:.3f}"
                q = f"How many moles are in {mass} g of a substance with a molar mass of {mm} g/mol?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[mass*mm, mm/mass])
                exp = f"n = m / M = {mass} / {mm} = {ans} mol."
                gen.add_question("Stoichiometry", diff, q, ans, wrongs, exp)
            else:
                mass_A = random.randint(10, 200)
                mass_B = random.randint(10, 200)
                mass_C = random.randint(5, mass_A + mass_B - 2)
                ans = f"{mass_A + mass_B - mass_C:.1f}"
                q = f"In an experiment, {mass_A} g of A reacts with {mass_B} g of B to yield {mass_C} g of C and some mass of D. What is the mass of D?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[mass_A+mass_B+mass_C, mass_A+mass_B, mass_C])
                exp = f"Reactants mass = {mass_A} + {mass_B} = {mass_A+mass_B} g. Products mass = {mass_A+mass_B} g. Mass D = {mass_A+mass_B} - {mass_C} = {ans} g."
                gen.add_question("Conservation of Mass", diff, q, ans, wrongs, exp)

        elif diff == "medium":
            choice = random.randint(1, 3)
            if choice == 1:
                n = random.randint(1, 100) / 10.0
                v_cm3 = random.randint(50, 2000)
                v_dm3 = v_cm3 / 1000
                ans = f"{n / v_dm3:.3f}"
                q = f"Calculate the concentration (in mol.dm^-3) of a solution containing {n} moles of solute in {v_cm3} cm^3 of solution."
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[n/v_cm3, n*v_dm3, v_dm3/n])
                exp = f"V = {v_cm3} / 1000 = {v_dm3} dm^3. C = n / V = {n} / {v_dm3} = {ans} mol.dm^-3."
                gen.add_question("Stoichiometry", diff, q, ans, wrongs, exp)
            elif choice == 2:
                conc = random.randint(1, 50) / 10.0
                v_dm3 = random.randint(1, 100) / 10.0
                mm = random.randint(20, 200)
                mass = conc * v_dm3 * mm
                ans = f"{mass:.2f}"
                q = f"What mass of solute (Molar mass = {mm} g/mol) is needed to prepare {v_dm3} dm^3 of a {conc} mol.dm^-3 solution?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[conc/v_dm3*mm, conc*v_dm3/mm])
                exp = f"n = C * V = {conc} * {v_dm3} = {conc*v_dm3:.2f} mol. Mass = n * M = {conc*v_dm3:.2f} * {mm} = {ans} g."
                gen.add_question("Stoichiometry", diff, q, ans, wrongs, exp)
            else:
                n = random.randint(1, 100) / 10.0
                ans = f"{n * 6.02:.2f}x10^23"
                q = f"How many molecules are in {n} moles of a substance? (Use N_A = 6.02 x 10^23)"
                wrongs = generate_wrong_answers_num(ans, is_scientific=True)
                exp = f"Particles = n * N_A = {n} * 6.02 x 10^23 = {ans}."
                gen.add_question("Stoichiometry", diff, q, ans, wrongs, exp)

        else: # hard
            choice = random.randint(1, 2)
            if choice == 1:
                c_n = random.randint(1, 10)
                h_n = random.randint(2, 22)
                o_n = random.randint(1, 5)
                mm = c_n*12 + h_n*1 + o_n*16
                perc_c = (c_n*12 / mm) * 100
                ans = f"{perc_c:.2f}"
                q = f"Calculate the percentage composition by mass of Carbon in C{c_n}H{h_n}O{o_n}."
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[(h_n*1/mm)*100, (o_n*16/mm)*100])
                exp = f"Molar mass = {mm}. %C = ({c_n*12}/{mm}) * 100 = {ans}%."
                gen.add_question("Stoichiometry", diff, q, ans, wrongs, exp)
            else:
                moles_A = random.randint(1, 50) / 10.0
                moles_B = random.randint(1, 50) / 10.0
                coeff_A = random.randint(1, 5)
                coeff_B = random.randint(1, 5)
                while coeff_A == coeff_B: coeff_B = random.randint(1, 5)
                ratio_A = moles_A / coeff_A
                ratio_B = moles_B / coeff_B
                limiting = "Reactant A" if ratio_A < ratio_B else "Reactant B"
                ans = limiting
                q = f"In the reaction {coeff_A}A + {coeff_B}B -> Products, you have {moles_A} mol of A and {moles_B} mol of B. Which is the limiting reactant?"
                wrongs = ["Reactant B" if limiting == "Reactant A" else "Reactant A", "Products", "Both A and B", "Cannot be determined", "Water", "Depends on mass"]
                exp = f"Ratio A = {moles_A}/{coeff_A} = {ratio_A:.2f}. Ratio B = {moles_B}/{coeff_B} = {ratio_B:.2f}. Smaller ratio determines limiting reactant: {limiting}."
                gen.add_question("Stoichiometry", diff, q, ans, wrongs, exp)

    gen.save_to_json("dataset/grade10/physci_chemical_change.json")

# 3. Newton’s Laws and Forces
def gen_forces():
    gen = TopicGenerator("Newton’s Laws and Forces", "PSC_FOR", [
        "Vectors and Scalars", "Motion in One Dimension", "Newton's First Law", "Newton's Second Law", "Newton's Third Law", "Gravitation"
    ])

    while not gen.is_done():
        diff = random.choices(["easy", "medium", "hard"], [0.3, 0.5, 0.2])[0]
        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        if diff == "easy":
            choice = random.randint(1, 3)
            if choice == 1:
                m = random.randint(1, 500)
                a = random.randint(1, 100) / 10.0
                ans = f"{m * a:.2f}"
                q = f"A mass of {m} kg accelerates at {a} m/s^2. What is the net force?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[m/a, a/m])
                exp = f"F = ma = {m} * {a} = {ans} N."
                gen.add_question("Newton's Second Law", diff, q, ans, wrongs, exp)
            elif choice == 2:
                m = random.randint(1, 1000)
                ans = f"{m * 9.8:.1f}"
                q = f"What is the weight of a {m} kg object on Earth? (g = 9.8 m/s^2)"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[m, m/9.8, 9.8/m])
                exp = f"W = mg = {m} * 9.8 = {ans} N."
                gen.add_question("Gravitation", diff, q, ans, wrongs, exp)
            else:
                d = random.randint(10, 5000)
                t = random.randint(5, 600)
                ans = f"{d / t:.2f}"
                q = f"A runner covers {d} m in {t} s. What is the average speed?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[d*t, t/d])
                exp = f"Speed = d / t = {d} / {t} = {ans} m/s."
                gen.add_question("Motion in One Dimension", diff, q, ans, wrongs, exp)

        elif diff == "medium":
            choice = random.randint(1, 3)
            if choice == 1:
                u = random.randint(0, 50)
                a = random.randint(1, 20) / 2.0
                t = random.randint(1, 60)
                ans = f"{u + a * t:.2f}"
                q = f"An object has an initial velocity of {u} m/s and accelerates at {a} m/s^2 for {t} s. What is the final velocity?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[u+a, a*t, u*t])
                exp = f"v = u + at = {u} + ({a} * {t}) = {ans} m/s."
                gen.add_question("Motion in One Dimension", diff, q, ans, wrongs, exp)
            elif choice == 2:
                f1 = random.randint(5, 500)
                f2 = random.randint(5, 500)
                ans = str(f1 + f2)
                q = f"Forces of {f1} N and {f2} N act on an object in the same direction. What is the resultant force?"
                wrongs = generate_wrong_answers_num(ans, steps=[abs(f1-f2), math.sqrt(f1**2+f2**2)])
                exp = f"Resultant = {f1} + {f2} = {ans} N."
                gen.add_question("Vectors and Scalars", diff, q, ans, wrongs, exp)
            else:
                f = random.randint(10, 1000)
                a = random.randint(1, 50) / 2.0
                ans = f"{f / a:.2f}"
                q = f"A net force of {f} N causes an acceleration of {a} m/s^2. What is the object's mass?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[f*a, a/f])
                exp = f"m = F / a = {f} / {a} = {ans} kg."
                gen.add_question("Newton's Second Law", diff, q, ans, wrongs, exp)

        else: # hard
            choice = random.randint(1, 2)
            if choice == 1:
                u = random.randint(0, 30)
                v = random.randint(u+1, 100)
                a = random.randint(1, 20) / 2.0
                s = (v**2 - u**2) / (2 * a)
                ans = f"{s:.2f}"
                q = f"A vehicle accelerates from {u} m/s to {v} m/s at {a} m/s^2. What is the distance traveled?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[(v-u)/a, (v**2+u**2)/(2*a)])
                exp = f"v^2 = u^2 + 2as. s = ({v}^2 - {u}^2) / (2 * {a}) = {ans} m."
                gen.add_question("Motion in One Dimension", diff, q, ans, wrongs, exp)
            else:
                m1 = random.randint(1, 50)
                m2 = random.randint(1, 50)
                f = random.randint(10, 500)
                a = f / (m1 + m2)
                t_tens = m1 * a
                ans = f"{t_tens:.2f}"
                q = f"Two blocks (m1 = {m1} kg, m2 = {m2} kg) are connected by a string. A force of {f} N pulls m2. What is the tension in the string pulling m1? (Frictionless)"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[f, m2*a, f/(m1+m2)])
                exp = f"a = F / (m1+m2) = {f} / {m1+m2} = {a:.3f} m/s^2. T = m1 * a = {m1} * {a:.3f} = {ans} N."
                gen.add_question("Newton's Second Law", diff, q, ans, wrongs, exp)

    gen.save_to_json("dataset/grade10/physci_forces_newton.json")

# 4. Energy and Energy Transfer
def gen_energy():
    gen = TopicGenerator("Energy and Energy Transfer", "PSC_ENE", [
        "Gravitational Potential Energy", "Kinetic Energy", "Mechanical Energy", "Conservation of Energy"
    ])

    while not gen.is_done():
        diff = random.choices(["easy", "medium", "hard"], [0.3, 0.5, 0.2])[0]
        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        if diff == "easy":
            choice = random.randint(1, 2)
            if choice == 1:
                m = random.randint(1, 200)
                h = random.randint(1, 1000) / 10.0
                ans = f"{m * 9.8 * h:.2f}"
                q = f"Calculate the gravitational potential energy of a {m} kg mass at a height of {h} m. (g=9.8)"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[m*h, m*9.8])
                exp = f"Ep = mgh = {m} * 9.8 * {h} = {ans} J."
                gen.add_question("Gravitational Potential Energy", diff, q, ans, wrongs, exp)
            else:
                m = random.randint(1, 200)
                v = random.randint(1, 100) / 2.0
                ans = f"{0.5 * m * v**2:.2f}"
                q = f"What is the kinetic energy of a {m} kg object moving at {v} m/s?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[m*v, 0.5*m*v])
                exp = f"Ek = 0.5 * m * v^2 = 0.5 * {m} * {v}^2 = {ans} J."
                gen.add_question("Kinetic Energy", diff, q, ans, wrongs, exp)

        elif diff == "medium":
            choice = random.randint(1, 2)
            if choice == 1:
                m = random.randint(1, 100)
                h = random.randint(1, 100)
                v = random.randint(1, 50)
                ans = f"{(m * 9.8 * h) + (0.5 * m * v**2):.2f}"
                q = f"A {m} kg drone flies at height {h} m and speed {v} m/s. What is its mechanical energy?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[m*9.8*h, 0.5*m*v**2])
                exp = f"Em = Ep + Ek = ({m}*9.8*{h}) + (0.5*{m}*{v}^2) = {ans} J."
                gen.add_question("Mechanical Energy", diff, q, ans, wrongs, exp)
            else:
                h = random.randint(5, 500)
                v = math.sqrt(2 * 9.8 * h)
                ans = f"{v:.2f}"
                q = f"An object drops from height {h} m. What is its speed right before hitting the ground? (Ignore air resistance)"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[9.8*h, math.sqrt(h)])
                exp = f"mgh = 0.5mv^2 -> v = sqrt(2gh) = sqrt(2 * 9.8 * {h}) = {ans} m/s."
                gen.add_question("Conservation of Energy", diff, q, ans, wrongs, exp)

        else: # hard
            u = random.randint(1, 30)
            h1 = random.randint(20, 200)
            h2 = random.randint(0, h1 - 5)
            v = math.sqrt(2 * 9.8 * (h1 - h2) + u**2)
            ans = f"{v:.2f}"
            q = f"A roller coaster (mass m) moves at {u} m/s at height {h1} m. It drops to height {h2} m. Find its speed there. (No friction)"
            wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[math.sqrt(2*9.8*(h1-h2)), math.sqrt(u**2 + 2*9.8*h1)])
            exp = f"Em1 = Em2 -> g*h1 + 0.5*u^2 = g*h2 + 0.5*v^2. v = sqrt(2*9.8*({h1}-{h2}) + {u}^2) = {ans} m/s."
            gen.add_question("Conservation of Energy", diff, q, ans, wrongs, exp)

    gen.save_to_json("dataset/grade10/physci_energy.json")

# 5. Waves, Sound and Light
def gen_waves():
    gen = TopicGenerator("Waves, Sound and Light", "PSC_WAV", [
        "Transverse Waves", "Longitudinal Waves", "Sound", "Electromagnetic Radiation"
    ])

    while not gen.is_done():
        diff = random.choices(["easy", "medium", "hard"], [0.3, 0.5, 0.2])[0]
        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        if diff == "easy":
            choice = random.randint(1, 3)
            if choice == 1:
                f = random.randint(1, 1000)
                lam = random.randint(1, 500) / 10.0
                ans = f"{f * lam:.2f}"
                q = f"A wave has frequency {f} Hz and wavelength {lam} m. What is its speed?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[f/lam, lam/f])
                exp = f"v = f * λ = {f} * {lam} = {ans} m/s."
                gen.add_question("Transverse Waves", diff, q, ans, wrongs, exp)
            elif choice == 2:
                f = random.randint(2, 5000)
                ans = f"{1 / f:.6f}"
                q = f"What is the period of a wave with frequency {f} Hz?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[f, f*2])
                exp = f"T = 1 / f = 1 / {f} = {ans} s."
                gen.add_question("Transverse Waves", diff, q, ans, wrongs, exp)
            else:
                t = random.randint(1, 50) / 2.0
                v = random.randint(330, 350)
                ans = f"{(v * t) / 2:.2f}"
                q = f"An echo is heard {t} s after a shout. If the speed of sound is {v} m/s, how far is the reflecting surface?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[v*t, v/t])
                exp = f"d = (v * t) / 2 = ({v} * {t}) / 2 = {ans} m."
                gen.add_question("Sound", diff, q, ans, wrongs, exp)

        elif diff == "medium":
            choice = random.randint(1, 2)
            if choice == 1:
                f_exp = random.randint(10, 20)
                f_base = random.randint(10, 99) / 10.0
                f = f_base * (10**f_exp)
                h = 6.63e-34
                ans = f"{h * f:.3e}".replace("e", "x10^").replace("+", "")
                q = f"Calculate the energy of a photon with frequency {f_base}x10^{f_exp} Hz. (h=6.63x10^-34)"
                wrongs = generate_wrong_answers_num(ans, is_scientific=True)
                exp = f"E = hf = (6.63x10^-34) * ({f_base}x10^{f_exp}) = {ans} J."
                gen.add_question("Electromagnetic Radiation", diff, q, ans, wrongs, exp)
            else:
                d = random.randint(100, 5000)
                v = random.randint(330, 350)
                ans = f"{d / v:.3f}"
                q = f"Lightning strikes {d} m away. Speed of sound is {v} m/s. How long until thunder is heard?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[d*v, v/d])
                exp = f"t = d / v = {d} / {v} = {ans} s."
                gen.add_question("Sound", diff, q, ans, wrongs, exp)

        else: # hard
            lam_nm = random.randint(100, 1000)
            e = (6.63e-34 * 3e8) / (lam_nm * 1e-9)
            ans = f"{e:.3e}".replace("e", "x10^").replace("+", "")
            q = f"Calculate the energy of a photon with wavelength {lam_nm} nm. (h=6.63x10^-34, c=3x10^8)"
            wrongs = generate_wrong_answers_num(ans, is_scientific=True)
            exp = f"E = hc/λ = (6.63x10^-34 * 3x10^8) / ({lam_nm}x10^-9) = {ans} J."
            gen.add_question("Electromagnetic Radiation", diff, q, ans, wrongs, exp)

    gen.save_to_json("dataset/grade10/physci_waves_light_sound.json")

# 6. Electricity and Magnetism
def gen_electricity():
    gen = TopicGenerator("Electricity and Magnetism", "PSC_ELE", [
        "Magnetism", "Electrostatics", "Electric Circuits"
    ])

    while not gen.is_done():
        diff = random.choices(["easy", "medium", "hard"], [0.3, 0.5, 0.2])[0]
        if gen.difficulty_counts[diff] >= gen.difficulty_targets[diff]:
            continue

        if diff == "easy":
            choice = random.randint(1, 3)
            if choice == 1:
                i = random.randint(1, 100) / 10.0
                t = random.randint(1, 3600)
                ans = f"{i * t:.2f}"
                q = f"A current of {i} A flows for {t} s. Calculate total charge."
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[i/t, t/i])
                exp = f"Q = I * t = {i} * {t} = {ans} C."
                gen.add_question("Electric Circuits", diff, q, ans, wrongs, exp)
            elif choice == 2:
                w = random.randint(10, 1000)
                q_charge = random.randint(1, 100) / 2.0
                ans = f"{w / q_charge:.2f}"
                q = f"{w} J of work moves {q_charge} C of charge. What is the potential difference?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[w*q_charge, q_charge/w])
                exp = f"V = W / Q = {w} / {q_charge} = {ans} V."
                gen.add_question("Electric Circuits", diff, q, ans, wrongs, exp)
            else:
                v = random.randint(1, 240)
                i = random.randint(1, 50) / 10.0
                ans = f"{v / i:.2f}"
                q = f"A voltage of {v} V causes current {i} A. What is the resistance?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[v*i, i/v])
                exp = f"R = V / I = {v} / {i} = {ans} Ω."
                gen.add_question("Electric Circuits", diff, q, ans, wrongs, exp)

        elif diff == "medium":
            choice = random.randint(1, 2)
            if choice == 1:
                n_exp = random.randint(5, 25)
                n_base = random.randint(10, 99) / 10.0
                n = n_base * (10**n_exp)
                e = 1.6e-19
                ans = f"{n * e:.3e}".replace("e", "x10^").replace("+", "")
                q = f"An object has an excess of {n_base}x10^{n_exp} electrons. What is its total negative charge? (e=1.6x10^-19)"
                wrongs = generate_wrong_answers_num(ans, is_scientific=True)
                exp = f"Q = n * e = ({n_base}x10^{n_exp}) * 1.6x10^-19 = {ans} C."
                gen.add_question("Electrostatics", diff, q, ans, wrongs, exp)
            else:
                r1 = random.randint(1, 100)
                r2 = random.randint(1, 100)
                r3 = random.randint(1, 100)
                ans = f"{r1 + r2 + r3:.1f}"
                q = f"Three resistors ({r1} Ω, {r2} Ω, {r3} Ω) are in series. Find equivalent resistance."
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[1/r1 + 1/r2 + 1/r3])
                exp = f"R_eq = {r1} + {r2} + {r3} = {ans} Ω."
                gen.add_question("Electric Circuits", diff, q, ans, wrongs, exp)

        else: # hard
            choice = random.randint(1, 2)
            if choice == 1:
                r1 = random.randint(1, 100)
                r2 = random.randint(1, 100)
                r_eq = 1 / (1/r1 + 1/r2)
                ans = f"{r_eq:.2f}"
                q = f"Two resistors ({r1} Ω, {r2} Ω) are in parallel. Calculate equivalent resistance."
                wrongs = generate_wrong_answers_num(ans, is_float=True, steps=[r1+r2, r1*r2])
                exp = f"1/R_eq = 1/{r1} + 1/{r2}. R_eq = ({r1}*{r2}) / ({r1}+{r2}) = {ans} Ω."
                gen.add_question("Electric Circuits", diff, q, ans, wrongs, exp)
            else:
                q1 = random.randint(-100, 100) / 2.0
                q2 = random.randint(-100, 100) / 2.0
                while q1 == q2: q2 = random.randint(-100, 100) / 2.0
                q_new = (q1 + q2) / 2
                ans = f"{q_new:.2f}"
                q = f"Two identical spheres with charges {q1} μC and {q2} μC touch and separate. What is the new charge on each?"
                wrongs = generate_wrong_answers_num(ans, is_float=True, allow_neg=True, steps=[q1+q2, abs(q1-q2)/2])
                exp = f"Q_new = (Q1 + Q2) / 2 = ({q1} + {q2}) / 2 = {ans} μC."
                gen.add_question("Electrostatics", diff, q, ans, wrongs, exp)

    gen.save_to_json("dataset/grade10/physci_electricity_magnetism.json")


def main():
    print("Generating Matter and Materials...")
    gen_matter()
    print("Generating Chemical Change...")
    gen_chemical()
    print("Generating Newton's Laws and Forces...")
    gen_forces()
    print("Generating Energy and Energy Transfer...")
    gen_energy()
    print("Generating Waves, Sound and Light...")
    gen_waves()
    print("Generating Electricity and Magnetism...")
    gen_electricity()
    print("All done!")

if __name__ == "__main__":
    main()
