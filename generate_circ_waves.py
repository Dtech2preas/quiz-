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

def gen_circular_motion():
    topic = "Circular Motion & Gravitation"
    prefix = "CMG"
    subtopics = ["Angular Velocity", "Centripetal Force", "Newton's Law of Gravitation", "Satellites"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Angular Velocity":
            v = random.randint(5, 50)
            r = random.uniform(0.5, 5.0)
            omega = v / r
            if difficulty == "easy":
                question = f"An object moves in a circle of radius ${format_float(r)}~\\text{{m}}$ with a linear speed of ${v}~\\text{{m/s}}$. Calculate its angular velocity."
                correct = f"{format_float(omega)}~\\text{{rad/s}}"
                wrongs = get_wrong_floats(omega, "rad/s")
                explanation = f"Using $\\omega = \\frac{{v}}{{r}} = \\frac{{{v}}}{{{format_float(r)}}} = {format_float(omega)}~\\text{{rad/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                f = random.randint(2, 10)
                omega_f = 2 * math.pi * f
                question = f"An object revolves at a frequency of ${f}~\\text{{Hz}}$. Calculate its angular velocity."
                correct = f"{format_float(omega_f)}~\\text{{rad/s}}"
                wrongs = get_wrong_floats(omega_f, "rad/s")
                explanation = f"Using $\\omega = 2\\pi f = 2\\pi({f}) \\approx {format_float(omega_f)}~\\text{{rad/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                rpm = random.randint(100, 1000)
                omega_rpm = (rpm * 2 * math.pi) / 60
                question = f"A motor rotates at ${rpm}~\\text{{rpm}}$. Calculate its angular velocity."
                correct = f"{format_float(omega_rpm)}~\\text{{rad/s}}"
                wrongs = get_wrong_floats(omega_rpm, "rad/s")
                explanation = f"Convert rpm to rad/s: $\\omega = \\frac{{{rpm} \\times 2\\pi}}{{60}} \\approx {format_float(omega_rpm)}~\\text{{rad/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Centripetal Force":
            m = random.randint(1, 20)
            v = random.randint(5, 30)
            r = random.uniform(1.0, 10.0)
            Fc = (m * v**2) / r
            if difficulty == "easy":
                question = f"Calculate the centripetal force acting on a ${m}~\\text{{kg}}$ object moving at ${v}~\\text{{m/s}}$ in a circle of radius ${format_float(r)}~\\text{{m}}$."
                correct = f"{format_float(Fc)}~\\text{{N}}"
                wrongs = get_wrong_floats(Fc, "N")
                explanation = f"Using $F_c = \\frac{{mv^2}}{{r}} = \\frac{{({m})({v})^2}}{{{format_float(r)}}} = {format_float(Fc)}~\\text{{N}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"A ${m}~\\text{{kg}}$ car travels around a circular track of radius ${format_float(r)}~\\text{{m}}$. If the maximum static friction force is ${format_float(Fc)}~\\text{{N}}$, calculate the maximum speed of the car without skidding."
                correct = f"{v}~\\text{{m/s}}"
                wrongs = get_wrong_floats(v, "m/s", decimals=0)
                explanation = f"Using $f_s = F_c = \\frac{{mv^2}}{{r}} \\Rightarrow {format_float(Fc)} = \\frac{{({m})v^2}}{{{format_float(r)}}} \\Rightarrow v = \\sqrt{{\\frac{{{format_float(Fc)}({format_float(r)})}}{{{m}}}}} = {v}~\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                omega = random.randint(2, 10)
                Fc_omega = m * omega**2 * r
                question = f"A ${m}~\\text{{kg}}$ mass attached to a string revolves in a horizontal circle of radius ${format_float(r)}~\\text{{m}}$ with an angular velocity of ${omega}~\\text{{rad/s}}$. Calculate the tension in the string."
                correct = f"{format_float(Fc_omega)}~\\text{{N}}"
                wrongs = get_wrong_floats(Fc_omega, "N")
                explanation = f"Using $F_c = m\\omega^2 r = ({m})({omega})^2({format_float(r)}) = {format_float(Fc_omega)}~\\text{{N}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Newton's Law of Gravitation":
            m1 = random.randint(10, 100)
            m2 = random.randint(10, 100)
            r = random.uniform(1.0, 5.0)
            G = 6.67e-11
            F = G * m1 * m2 / (r**2)
            F_sci = f"{F:.2e}".replace("e", "\\times 10^{") + "}"
            if difficulty == "easy":
                question = f"Calculate the gravitational force between two masses of ${m1}~\\text{{kg}}$ and ${m2}~\\text{{kg}}$ separated by a distance of ${format_float(r)}~\\text{{m}}$. ($G = 6.67 \\times 10^{{-11}}~\\text{{N\\cdot m}}^2/\\text{{kg}}^2$)"
                correct = f"{F_sci}~\\text{{N}}"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}~\\text{N}" for w in [F*10, F/10, F*100, F/100, F*2, F/2, F*4, F/4]]
                explanation = f"Using $F = \\frac{{G m_1 m_2}}{{r^2}} = \\frac{{(6.67 \\times 10^{{-11}})({m1})({m2})}}{{({format_float(r)})^2}} = {F_sci}~\\text{{N}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                M_earth = 5.97e24
                r_earth = 6.37e6
                m_obj = random.randint(50, 150)
                h = random.randint(100, 1000) * 1000  # km to m
                r_total = r_earth + h
                g_h = G * M_earth / (r_total**2)
                question = f"Calculate the acceleration due to gravity for an object at an altitude of ${int(h/1000)}~\\text{{km}}$ above the Earth's surface. ($M_E = 5.97 \\times 10^{{24}}~\\text{{kg}}$, $R_E = 6.37 \\times 10^6~\\text{{m}}$)"
                correct = f"{format_float(g_h)}~\\text{{m/s}}^2"
                wrongs = get_wrong_floats(g_h, "m/s^2")
                explanation = f"Using $g = \\frac{{GM}}{{(R_E + h)^2}} = \\frac{{(6.67 \\times 10^{{-11}})(5.97 \\times 10^{{24}})}}{{({r_earth} + {h})^2}} \\approx {format_float(g_h)}~\\text{{m/s}}^2$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Find distance where force is X
                F_target = random.uniform(1e-9, 1e-7)
                r_target = math.sqrt(G * m1 * m2 / F_target)
                F_target_sci = f"{F_target:.2e}".replace("e", "\\times 10^{") + "}"
                question = f"Two masses, ${m1}~\\text{{kg}}$ and ${m2}~\\text{{kg}}$, experience a gravitational force of ${F_target_sci}~\\text{{N}}$. Calculate the distance between their centers."
                correct = f"{format_float(r_target)}~\\text{{m}}"
                wrongs = get_wrong_floats(r_target, "m")
                explanation = f"Using $F = \\frac{{G m_1 m_2}}{{r^2}} \\Rightarrow r = \\sqrt{{\\frac{{G m_1 m_2}}{{F}}}} = \\sqrt{{\\frac{{(6.67 \\times 10^{{-11}})({m1})({m2})}}{{{F_target}}}}} \\approx {format_float(r_target)}~\\text{{m}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Satellites":
            M = 5.97e24
            G = 6.67e-11
            R = 6.37e6
            h = random.randint(200, 2000) * 1000
            r_orb = R + h
            v_orb = math.sqrt(G * M / r_orb)
            if difficulty == "easy":
                question = f"A satellite is in a circular orbit at an altitude of ${int(h/1000)}~\\text{{km}}$ above Earth. Calculate its orbital speed. ($M_E = 5.97 \\times 10^{{24}}~\\text{{kg}}$, $R_E = 6.37 \\times 10^6~\\text{{m}}$)"
                correct = f"{format_float(v_orb)}~\\text{{m/s}}"
                wrongs = get_wrong_floats(v_orb, "m/s")
                explanation = f"Using $v = \\sqrt{{\\frac{{GM}}{{r}}}} = \\sqrt{{\\frac{{(6.67 \\times 10^{{-11}})(5.97 \\times 10^{{24}})}}{{{r_orb}}}}} \\approx {format_float(v_orb)}~\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                T = 2 * math.pi * r_orb / v_orb
                question = f"A satellite orbits Earth at a distance of ${r_orb:.2e}~\\text{{m}}$ from its center. Calculate its orbital period. ($M_E = 5.97 \\times 10^{{24}}~\\text{{kg}}$)"
                correct = f"{format_float(T)}~\\text{{s}}"
                wrongs = get_wrong_floats(T, "s")
                explanation = f"Using $T = \\sqrt{{\\frac{{4\\pi^2 r^3}}{{GM}}}} \\approx {format_float(T)}~\\text{{s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                T_hrs = random.randint(2, 24)
                T_sec = T_hrs * 3600
                r_geo = (G * M * T_sec**2 / (4 * math.pi**2))**(1/3)
                question = f"Calculate the orbital radius for a satellite with a period of ${T_hrs}~\\text{{hours}}$. ($M_E = 5.97 \\times 10^{{24}}~\\text{{kg}}$)"
                correct = f"{format_float(r_geo)}~\\text{{m}}"
                wrongs = [f"{w:.2e}".replace("e", "\\times 10^{") + "}~\\text{m}" for w in [r_geo*10, r_geo/10, r_geo*2, r_geo/2, r_geo*4, r_geo/4, r_geo*100, r_geo/100]]
                explanation = f"Using $r^3 = \\frac{{GM T^2}}{{4\\pi^2}} \\Rightarrow r = \\sqrt[3]{{\\frac{{(6.67 \\times 10^{{-11}})(5.97 \\times 10^{{24}})({T_sec})^2}}{{4\\pi^2}}}} \\approx {format_float(r_geo)}~\\text{{m}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper1_circular_motion.json")

def gen_oscillations_waves():
    topic = "Oscillations & Waves"
    prefix = "WAV"
    subtopics = ["Simple Harmonic Motion", "Wave Properties", "Doppler Effect", "Interference & Diffraction"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Simple Harmonic Motion":
            m = random.randint(1, 10)
            k = random.randint(50, 500)
            T = 2 * math.pi * math.sqrt(m / k)
            if difficulty == "easy":
                question = f"Calculate the period of a mass-spring system with a mass of ${m}~\\text{{kg}}$ and a spring constant of ${k}~\\text{{N/m}}$."
                correct = f"{format_float(T)}~\\text{{s}}"
                wrongs = get_wrong_floats(T, "s")
                explanation = f"Using $T = 2\\pi \\sqrt{{\\frac{{m}}{{k}}}} = 2\\pi \\sqrt{{\\frac{{{m}}}{{{k}}}}} \\approx {format_float(T)}~\\text{{s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                f = 1 / T
                question = f"A mass of ${m}~\\text{{kg}}$ is attached to a spring with $k = {k}~\\text{{N/m}}$. Calculate the frequency of oscillation."
                correct = f"{format_float(f)}~\\text{{Hz}}"
                wrongs = get_wrong_floats(f, "Hz")
                explanation = f"Using $f = \\frac{{1}}{{2\\pi}} \\sqrt{{\\frac{{k}}{{m}}}} = \\frac{{1}}{{2\\pi}} \\sqrt{{\\frac{{{k}}}{{{m}}}}} \\approx {format_float(f)}~\\text{{Hz}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                L = random.uniform(0.5, 3.0)
                g = 9.8
                T_pend = 2 * math.pi * math.sqrt(L / g)
                question = f"Calculate the period of a simple pendulum of length ${format_float(L)}~\\text{{m}}$. Take $g = 9.8~\\text{{m/s}}^2$."
                correct = f"{format_float(T_pend)}~\\text{{s}}"
                wrongs = get_wrong_floats(T_pend, "s")
                explanation = f"Using $T = 2\\pi \\sqrt{{\\frac{{L}}{{g}}}} = 2\\pi \\sqrt{{\\frac{{{format_float(L)}}}{{9.8}}}} \\approx {format_float(T_pend)}~\\text{{s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Wave Properties":
            v = random.randint(300, 350) # speed of sound
            f = random.randint(200, 1000)
            lam = v / f
            if difficulty == "easy":
                question = f"A sound wave has a frequency of ${f}~\\text{{Hz}}$ and a speed of ${v}~\\text{{m/s}}$. Calculate its wavelength."
                correct = f"{format_float(lam)}~\\text{{m}}"
                wrongs = get_wrong_floats(lam, "m")
                explanation = f"Using $v = f\\lambda \\Rightarrow \\lambda = \\frac{{v}}{{f}} = \\frac{{{v}}}{{{f}}} \\approx {format_float(lam)}~\\text{{m}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"A wave with a wavelength of ${format_float(lam)}~\\text{{m}}$ travels at ${v}~\\text{{m/s}}$. Calculate its period."
                T_wave = 1 / f
                correct = f"{format_float(T_wave, 5)}~\\text{{s}}"
                wrongs = get_wrong_floats(T_wave, "s", decimals=5)
                explanation = f"Using $v = \\frac{{\\lambda}}{{T}} \\Rightarrow T = \\frac{{\\lambda}}{{v}} = \\frac{{{format_float(lam)}}}{{{v}}} \\approx {format_float(T_wave, 5)}~\\text{{s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                n1 = 1.0
                n2 = random.choice([1.33, 1.5, 2.42])
                angle_i = random.randint(30, 60)
                angle_r = math.degrees(math.asin(math.sin(math.radians(angle_i)) * n1 / n2))
                question = f"Light travels from air ($n = 1.0$) into a medium with an index of refraction $n = {n2}$. If the angle of incidence is ${angle_i}^\\circ$, calculate the angle of refraction."
                correct = f"{format_float(angle_r)}^\\circ"
                wrongs = get_wrong_floats(angle_r, "^\\circ")
                explanation = f"Using Snell's Law: $n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2 \\Rightarrow (1.0)\\sin({angle_i}^\\circ) = ({n2})\\sin\\theta_2 \\Rightarrow \\theta_2 \\approx {format_float(angle_r)}^\\circ$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Doppler Effect":
            v = 340
            f_s = random.randint(400, 800)
            v_s = random.randint(10, 30)
            v_l = random.randint(5, 20)
            if difficulty == "easy":
                # Source moving towards stationary listener
                f_L = f_s * (v / (v - v_s))
                question = f"A stationary listener hears an ambulance approaching at ${v_s}~\\text{{m/s}}$. The siren's frequency is ${f_s}~\\text{{Hz}}$. Calculate the observed frequency. (Speed of sound = $340~\\text{{m/s}}$)"
                correct = f"{format_float(f_L)}~\\text{{Hz}}"
                wrongs = get_wrong_floats(f_L, "Hz")
                explanation = f"Using $f_L = \\frac{{v}}{{v - v_s}}f_s = \\left(\\frac{{340}}{{340 - {v_s}}}\\right)({f_s}) \\approx {format_float(f_L)}~\\text{{Hz}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                # Source moving away
                f_L_away = f_s * (v / (v + v_s))
                question = f"An ambulance moves away from a stationary listener at ${v_s}~\\text{{m/s}}$. The siren's frequency is ${f_s}~\\text{{Hz}}$. Calculate the observed frequency. (Speed of sound = $340~\\text{{m/s}}$)"
                correct = f"{format_float(f_L_away)}~\\text{{Hz}}"
                wrongs = get_wrong_floats(f_L_away, "Hz")
                explanation = f"Using $f_L = \\frac{{v}}{{v + v_s}}f_s = \\left(\\frac{{340}}{{340 + {v_s}}}\\right)({f_s}) \\approx {format_float(f_L_away)}~\\text{{Hz}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                # Both moving towards
                f_L_both = f_s * ((v + v_l) / (v - v_s))
                question = f"A listener moving at ${v_l}~\\text{{m/s}}$ and a car moving at ${v_s}~\\text{{m/s}}$ approach each other. The car emits a sound of ${f_s}~\\text{{Hz}}$. Calculate the observed frequency. (Speed of sound = $340~\\text{{m/s}}$)"
                correct = f"{format_float(f_L_both)}~\\text{{Hz}}"
                wrongs = get_wrong_floats(f_L_both, "Hz")
                explanation = f"Using $f_L = \\frac{{v + v_L}}{{v - v_s}}f_s = \\left(\\frac{{340 + {v_l}}}{{340 - {v_s}}}\\right)({f_s}) \\approx {format_float(f_L_both)}~\\text{{Hz}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Interference & Diffraction":
            lam_nm = random.randint(400, 700)
            lam = lam_nm * 1e-9
            d_mm = random.uniform(0.1, 1.0)
            d = d_mm * 1e-3
            L = random.uniform(1.0, 5.0)
            if difficulty == "easy":
                theta = math.degrees(math.asin(lam / d))
                question = f"Light of wavelength ${lam_nm}~\\text{{nm}}$ passes through a single slit of width ${format_float(d_mm)}~\\text{{mm}}$. Calculate the angle to the first diffraction minimum."
                correct = f"{format_float(theta, 3)}^\\circ"
                wrongs = get_wrong_floats(theta, "^\\circ", decimals=3)
                explanation = f"Using $a \\sin\\theta = m\\lambda \\Rightarrow \\sin\\theta = \\frac{{(1)({lam_nm} \\times 10^{{-9}})}}{{{format_float(d_mm)} \\times 10^{{-3}}}} \\Rightarrow \\theta \\approx {format_float(theta, 3)}^\\circ$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                y = (lam * L) / d
                y_mm = y * 1000
                question = f"In a Young's double-slit experiment, slits are separated by ${format_float(d_mm)}~\\text{{mm}}$, and the screen is ${format_float(L)}~\\text{{m}}$ away. Light of wavelength ${lam_nm}~\\text{{nm}}$ is used. Calculate the distance between adjacent bright fringes on the screen."
                correct = f"{format_float(y_mm)}~\\text{{mm}}"
                wrongs = get_wrong_floats(y_mm, "mm")
                explanation = f"Using $\\Delta y = \\frac{{\\lambda L}}{{d}} = \\frac{{({lam_nm} \\times 10^{{-9}})({format_float(L)})}}{{{format_float(d_mm)} \\times 10^{{-3}}}} \\approx {format_float(y_mm)}~\\text{{mm}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                N = random.randint(300, 600) # lines per mm
                d_grid = (1 / N) * 1e-3
                theta_m = math.degrees(math.asin(2 * lam / d_grid))
                question = f"A diffraction grating has ${N}~\\text{{lines/mm}}$. Light of wavelength ${lam_nm}~\\text{{nm}}$ is directed normally at the grating. Calculate the angle of the second-order maximum."
                correct = f"{format_float(theta_m)}^\\circ"
                wrongs = get_wrong_floats(theta_m, "^\\circ")
                explanation = f"Using $d = \\frac{{1}}{{N}} = \\frac{{1}}{{{N} \\times 10^3}}~\\text{{m}}$. Then $d \\sin\\theta = n\\lambda \\Rightarrow \\sin\\theta = \\frac{{2({lam_nm} \\times 10^{{-9}})}}{{d}} \\Rightarrow \\theta \\approx {format_float(theta_m)}^\\circ$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper1_oscillations_waves.json")

if __name__ == "__main__":
    gen_circular_motion()
    gen_oscillations_waves()
    print("Generated Circular Motion and Waves datasets.")
