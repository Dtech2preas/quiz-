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

def gen_thermal_physics():
    topic = "Thermal Physics"
    prefix = "THERM"
    subtopics = ["Specific Heat Capacity", "Latent Heat", "Gas Laws", "Heat Transfer"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Specific Heat Capacity":
            m = random.uniform(0.5, 5.0)
            c = random.choice([4186, 385, 900]) # Water, Copper, Aluminum
            substance = "water" if c == 4186 else ("copper" if c == 385 else "aluminum")
            dT = random.randint(10, 80)
            Q = m * c * dT
            if difficulty == "easy":
                question = f"Calculate the heat energy required to raise the temperature of ${format_float(m)}~\\text{{kg}}$ of {substance} ($c = {c}~\\text{{J/(kg\\cdot^\\circ C)}}$) by ${dT}^\\circ\\text{{C}}$."
                correct = f"{format_float(Q)}~\\text{{J}}"
                wrongs = get_wrong_floats(Q, "J")
                explanation = f"Using $Q = mc\\Delta T = ({format_float(m)})({c})({dT}) = {format_float(Q)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                Ti = random.randint(10, 30)
                Tf = Ti + dT
                question = f"How much heat is needed to heat ${format_float(m)}~\\text{{kg}}$ of {substance} ($c = {c}~\\text{{J/(kg\\cdot^\\circ C)}}$) from ${Ti}^\\circ\\text{{C}}$ to ${Tf}^\\circ\\text{{C}}$?"
                correct = f"{format_float(Q)}~\\text{{J}}"
                wrongs = get_wrong_floats(Q, "J")
                explanation = f"Using $Q = mc(T_f - T_i) = ({format_float(m)})({c})({Tf} - {Ti}) = {format_float(Q)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                m2 = random.uniform(0.1, 1.0)
                c2 = 385 # copper block
                T1 = random.randint(80, 100)
                T2 = random.randint(10, 25)
                # m1*c1*(T1 - Tf) = m2*c2*(Tf - T2)
                Tf = (m * c * T1 + m2 * c2 * T2) / (m * c + m2 * c2)
                question = f"A ${format_float(m)}~\\text{{kg}}$ block of {substance} at ${T1}^\\circ\\text{{C}}$ is dropped into ${format_float(m2)}~\\text{{kg}}$ of water ($c = 4186~\\text{{J/(kg\\cdot^\\circ C)}}$) initially at ${T2}^\\circ\\text{{C}}$. Calculate the final equilibrium temperature."
                correct = f"{format_float(Tf)}~^\\circ\\text{{C}}"
                wrongs = get_wrong_floats(Tf, "^\\circ\\text{C}")
                explanation = f"Using conservation of energy: $m_1 c_1(T_1 - T_f) = m_2 c_2(T_f - T_2) \\Rightarrow ({format_float(m)})({c})({T1} - T_f) = ({format_float(m2)})(4186)(T_f - {T2}) \\Rightarrow T_f \\approx {format_float(Tf)}~^\\circ\\text{{C}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Latent Heat":
            m = random.uniform(0.1, 2.0)
            L = random.choice([3.34e5, 2.26e6]) # Ice melting, Water boiling
            process = "melt" if L == 3.34e5 else "vaporize"
            state = "ice" if L == 3.34e5 else "water"
            Q = m * L
            Q_sci = f"{Q:.2e}".replace("e", "\\times 10^{") + "}"
            if difficulty == "easy":
                question = f"Calculate the heat energy required to {process} ${format_float(m)}~\\text{{kg}}$ of {state} at its transition temperature. (Latent heat $L = {L:.2e}~\\text{{J/kg}}$)"
                correct = f"{Q_sci}~\\text{{J}}"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}~\\text{J}" for w in [Q*10, Q/10, Q*2, Q/2, Q*4, Q/4, Q*5, Q/5]]
                explanation = f"Using $Q = mL = ({format_float(m)})({L}) = {Q_sci}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                c = 2100 if L == 3.34e5 else 4186
                dT = random.randint(10, 30)
                Q_total = m * c * dT + m * L
                initial_temp = -dT if L == 3.34e5 else 100
                final_temp = 0 if L == 3.34e5 else 100
                question = f"Calculate the total heat required to raise the temperature of ${format_float(m)}~\\text{{kg}}$ of {state} from ${initial_temp}^\\circ\\text{{C}}$ to ${final_temp}^\\circ\\text{{C}}$ and then completely {process} it. (Latent heat $L = {L:.2e}~\\text{{J/kg}}$, specific heat capacity $c = {c}~\\text{{J/(kg\\cdot^\\circ C)}}$)"
                correct = f"{format_float(Q_total)}~\\text{{J}}"
                wrongs = get_wrong_floats(Q_total, "J")
                explanation = f"Using $Q_{{total}} = mc\\Delta T + mL = ({format_float(m)})({c})({dT}) + ({format_float(m)})({L}) = {format_float(Q_total)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                P = random.randint(500, 2000) # Watt heater
                t = Q / P
                question = f"An electric heater rated at ${P}~\\text{{W}}$ is used to {process} ${format_float(m)}~\\text{{kg}}$ of {state} at its transition temperature. How long will it take? (Latent heat $L = {L:.2e}~\\text{{J/kg}}$)"
                correct = f"{format_float(t)}~\\text{{s}}"
                wrongs = get_wrong_floats(t, "s")
                explanation = f"Using $Q = mL$ and $Q = Pt \\Rightarrow Pt = mL \\Rightarrow t = \\frac{{({format_float(m)})({L})}}{{{P}}} = {format_float(t)}~\\text{{s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Gas Laws":
            P1 = random.randint(1, 5) * 1e5
            V1 = random.uniform(1.0, 10.0)
            T1 = random.randint(273, 373)
            if difficulty == "easy":
                # Boyle's Law P1V1 = P2V2
                P2 = random.randint(6, 10) * 1e5
                V2 = P1 * V1 / P2
                question = f"A gas has a volume of ${format_float(V1)}~\\text{{m}}^3$ at a pressure of ${P1:.1e}~\\text{{Pa}}$. If the pressure is increased to ${P2:.1e}~\\text{{Pa}}$ at constant temperature, calculate the new volume."
                correct = f"{format_float(V2)}~\\text{{m}}^3"
                wrongs = get_wrong_floats(V2, "m^3")
                explanation = f"Using Boyle's Law: $P_1 V_1 = P_2 V_2 \\Rightarrow V_2 = \\frac{{P_1 V_1}}{{P_2}} = \\frac{{({P1:.1e})({format_float(V1)})}}{{{P2:.1e}}} \\approx {format_float(V2)}~\\text{{m}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                # Charles's Law V1/T1 = V2/T2
                T2 = random.randint(374, 473)
                V2 = V1 * T2 / T1
                question = f"A gas occupies ${format_float(V1)}~\\text{{m}}^3$ at ${T1}~\\text{{K}}$. If it is heated to ${T2}~\\text{{K}}$ at constant pressure, calculate its new volume."
                correct = f"{format_float(V2)}~\\text{{m}}^3"
                wrongs = get_wrong_floats(V2, "m^3")
                explanation = f"Using Charles's Law: $\\frac{{V_1}}{{T_1}} = \\frac{{V_2}}{{T_2}} \\Rightarrow V_2 = \\frac{{V_1 T_2}}{{T_1}} = \\frac{{({format_float(V1)})({T2})}}{{{T1}}} \\approx {format_float(V2)}~\\text{{m}}^3$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Ideal Gas Law PV = nRT
                R = 8.31
                n = P1 * V1 / (R * T1)
                question = f"Calculate the number of moles of an ideal gas that occupies a volume of ${format_float(V1)}~\\text{{m}}^3$ at a pressure of ${P1:.1e}~\\text{{Pa}}$ and a temperature of ${T1}~\\text{{K}}$. ($R = 8.31~\\text{{J/(mol\\cdot K)}}$)"
                correct = f"{format_float(n)}~\\text{{mol}}"
                wrongs = get_wrong_floats(n, "mol")
                explanation = f"Using $PV = nRT \\Rightarrow n = \\frac{{PV}}{{RT}} = \\frac{{({P1:.1e})({format_float(V1)})}}{{(8.31)({T1})}} \\approx {format_float(n)}~\\text{{mol}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Heat Transfer":
            # Just some generic rate of heat transfer (conduction)
            k = random.uniform(0.1, 400.0) # Thermal conductivity
            A = random.uniform(1.0, 5.0)
            L = random.uniform(0.01, 0.1)
            dT = random.randint(10, 50)
            rate = (k * A * dT) / L
            if difficulty == "easy":
                question = f"Calculate the rate of heat transfer through a material with thermal conductivity $k = {format_float(k)}~\\text{{W/(m\\cdot K)}}$, area $A = {format_float(A)}~\\text{{m}}^2$, thickness $L = {format_float(L)}~\\text{{m}}$, and a temperature difference of $\\Delta T = {dT}~\\text{{K}}$."
                correct = f"{format_float(rate)}~\\text{{W}}"
                wrongs = get_wrong_floats(rate, "W")
                explanation = f"Using $\\frac{{Q}}{{t}} = \\frac{{kA\\Delta T}}{{L}} = \\frac{{({format_float(k)})({format_float(A)})({dT})}}{{{format_float(L)}}} \\approx {format_float(rate)}~\\text{{W}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                Q = rate * 60 # 1 minute
                question = f"A glass window ($k = 0.8~\\text{{W/(m\\cdot K)}}$) has an area of ${format_float(A)}~\\text{{m}}^2$ and thickness ${format_float(L)}~\\text{{m}}$. The temperature difference is ${dT}~\\text{{K}}$. Calculate the total heat transferred in 1 minute."
                rate_glass = (0.8 * A * dT) / L
                Q_glass = rate_glass * 60
                correct = f"{format_float(Q_glass)}~\\text{{J}}"
                wrongs = get_wrong_floats(Q_glass, "J")
                explanation = f"Using $\\frac{{Q}}{{t}} = \\frac{{kA\\Delta T}}{{L}} \\Rightarrow Q = \\left(\\frac{{(0.8)({format_float(A)})({dT})}}{{{format_float(L)}}}\\right)(60) \\approx {format_float(Q_glass)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Find thickness
                rate_target = random.randint(100, 1000)
                L_target = (k * A * dT) / rate_target
                question = f"A material ($k = {format_float(k)}~\\text{{W/(m\\cdot K)}}$) has an area of ${format_float(A)}~\\text{{m}}^2$. The temperature difference across it is ${dT}~\\text{{K}}$. If the rate of heat transfer is ${rate_target}~\\text{{W}}$, calculate the thickness."
                correct = f"{format_float(L_target)}~\\text{{m}}"
                wrongs = get_wrong_floats(L_target, "m")
                explanation = f"Using $\\frac{{Q}}{{t}} = \\frac{{kA\\Delta T}}{{L}} \\Rightarrow L = \\frac{{kA\\Delta T}}{{\\frac{{Q}}{{t}}}} = \\frac{{({format_float(k)})({format_float(A)})({dT})}}{{{rate_target}}} \\approx {format_float(L_target)}~\\text{{m}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper1_thermal_physics.json")

if __name__ == "__main__":
    gen_thermal_physics()
    print("Generated Thermal Physics dataset.")
