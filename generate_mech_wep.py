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

def gen_mechanics():
    topic = "Mechanics"
    prefix = "MECH"
    subtopics = ["Kinematics", "Dynamics", "Momentum", "Projectiles"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Kinematics":
            u = random.randint(0, 20)
            t = random.randint(2, 10)
            a = random.randint(1, 10)
            v = u + a * t

            if difficulty == "easy":
                question = f"A car accelerates uniformly from ${u}~\\text{{m/s}}$ to ${v}~\\text{{m/s}}$ in ${t}~\\text{{s}}$. Calculate its acceleration."
                correct = f"{a}~\\text{{m/s}}^2"
                wrongs = get_wrong_ints(a, "\\text{m/s}^2")
                explanation = f"Using $a = \\frac{{v - u}}{{t}} = \\frac{{{v}-{u}}}{{{t}}} = {a}~\\text{{m/s}}^2$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"A car starting from rest accelerates at ${a}~\\text{{m/s}}^2$ for ${t}~\\text{{s}}$. Calculate its final velocity."
                ans = a*t
                correct = f"{ans}~\\text{{m/s}}"
                wrongs = get_wrong_ints(ans, "\\text{m/s}")
                explanation = f"Using $v = u + at = 0 + ({a})({t}) = {ans}~\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                s = u*t + 0.5 * a * (t**2)
                question = f"A car with an initial velocity of ${u}~\\text{{m/s}}$ accelerates uniformly for ${t}~\\text{{s}}$. If it covers a distance of ${format_float(s)}~\\text{{m}}$, calculate its acceleration."
                correct = f"{a}~\\text{{m/s}}^2"
                wrongs = get_wrong_ints(a, "\\text{m/s}^2")
                explanation = f"Using $s = ut + \\frac{{1}}{{2}}at^2 \\Rightarrow {format_float(s)} = ({u})({t}) + 0.5(a)({t})^2 \\Rightarrow a = {a}~\\text{{m/s}}^2$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Dynamics":
            m = random.randint(10, 100)
            a = random.randint(1, 10)
            f = m * a

            if difficulty == "easy":
                question = f"Calculate the net force required to accelerate a ${m}~\\text{{kg}}$ object at ${a}~\\text{{m/s}}^2$."
                correct = f"{f}~\\text{{N}}"
                wrongs = get_wrong_ints(f, "\\text{N}")
                explanation = f"Using $F_{{net}} = ma = ({m})({a}) = {f}~\\text{{N}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"A net force of ${f}~\\text{{N}}$ is applied to a ${m}~\\text{{kg}}$ mass. Calculate its acceleration."
                correct = f"{a}~\\text{{m/s}}^2"
                wrongs = get_wrong_ints(a, "\\text{m/s}^2")
                explanation = f"Using $a = \\frac{{F_{{net}}}}{{m}} = \\frac{{{f}}}{{{m}}} = {a}~\\text{{m/s}}^2$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                f_fric = random.randint(5, 50)
                f_app = f + f_fric
                question = f"A constant applied force of ${f_app}~\\text{{N}}$ moves a ${m}~\\text{{kg}}$ block across a rough surface with an acceleration of ${a}~\\text{{m/s}}^2$. Calculate the frictional force."
                correct = f"{f_fric}~\\text{{N}}"
                wrongs = get_wrong_ints(f_fric, "\\text{N}")
                explanation = f"Using $F_{{net}} = F_{{app}} - f_{{k}} = ma \\Rightarrow {f_app} - f_{{k}} = ({m})({a}) = {f} \\Rightarrow f_{{k}} = {f_fric}~\\text{{N}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Momentum":
            m = random.randint(1, 20)
            v = random.randint(5, 30)
            p = m * v

            if difficulty == "easy":
                question = f"Calculate the momentum of a ${m}~\\text{{kg}}$ object moving at ${v}~\\text{{m/s}}$."
                correct = f"{p}~\\text{{kg}}\\cdot\\text{{m/s}}"
                wrongs = get_wrong_ints(p, "\\text{kg}\\cdot\\text{m/s}")
                explanation = f"Using $p = mv = ({m})({v}) = {p}~\\text{{kg}}\\cdot\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                t = random.randint(2, 5)
                f_net = p / t
                question = f"A ${m}~\\text{{kg}}$ object initially at rest reaches a velocity of ${v}~\\text{{m/s}}$ after a constant force is applied for ${t}~\\text{{s}}$. Calculate the net force."
                correct = f"{format_float(f_net)}~\\text{{N}}"
                wrongs = get_wrong_floats(f_net, "\\text{N}")
                explanation = f"Using $F_{{net}} = \\frac{{\\Delta p}}{{\\Delta t}} = \\frac{{{p} - 0}}{{{t}}} = {format_float(f_net)}~\\text{{N}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                m1 = random.randint(1, 10)
                v1 = random.randint(5, 15)
                m2 = random.randint(1, 10)
                v_final = (m1 * v1) / (m1 + m2)
                question = f"A ${m1}~\\text{{kg}}$ object moving at ${v1}~\\text{{m/s}}$ collides and sticks to a stationary ${m2}~\\text{{kg}}$ object. Calculate their common final velocity."
                correct = f"{format_float(v_final)}~\\text{{m/s}}"
                wrongs = get_wrong_floats(v_final, "\\text{m/s}")
                explanation = f"Using conservation of momentum: $m_1 v_1 + m_2 v_2 = (m_1 + m_2)v_f \\Rightarrow ({m1})({v1}) + 0 = ({m1+m2})v_f \\Rightarrow v_f = {format_float(v_final)}~\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Projectiles":
            h = random.randint(10, 100)
            g = 9.8
            t = math.sqrt(2 * h / g)

            if difficulty == "easy":
                question = f"An object is dropped from a height of ${h}~\\text{{m}}$. Taking $g = 9.8~\\text{{m/s}}^2$, calculate the time it takes to reach the ground."
                correct = f"{format_float(t)}~\\text{{s}}"
                wrongs = get_wrong_floats(t, "\\text{s}")
                explanation = f"Using $s = ut + \\frac{{1}}{{2}}gt^2 \\Rightarrow {h} = 0 + 0.5(9.8)t^2 \\Rightarrow t = \\sqrt{{\\frac{{2 \\times {h}}}{{9.8}}}} \\approx {format_float(t)}~\\text{{s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                v = math.sqrt(2 * g * h)
                question = f"An object is dropped from a height of ${h}~\\text{{m}}$. Taking $g = 9.8~\\text{{m/s}}^2$, calculate its velocity just before hitting the ground."
                correct = f"{format_float(v)}~\\text{{m/s}}"
                wrongs = get_wrong_floats(v, "\\text{m/s}")
                explanation = f"Using $v^2 = u^2 + 2gs \\Rightarrow v = \\sqrt{{0 + 2(9.8)({h})}} \\approx {format_float(v)}~\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                v_init = random.randint(10, 30)
                h_max = (v_init**2) / (2*g)
                question = f"An object is thrown vertically upwards with an initial velocity of ${v_init}~\\text{{m/s}}$. Calculate the maximum height it reaches. Take $g = 9.8~\\text{{m/s}}^2$."
                correct = f"{format_float(h_max)}~\\text{{m}}"
                wrongs = get_wrong_floats(h_max, "\\text{m}")
                explanation = f"Using $v^2 = u^2 + 2gs \\Rightarrow 0 = ({v_init})^2 - 2(9.8)s \\Rightarrow s = \\frac{{{v_init}^2}}{{19.6}} \\approx {format_float(h_max)}~\\text{{m}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper1_mechanics.json")

def gen_work_energy():
    topic = "Work, Energy & Power"
    prefix = "WEP"
    subtopics = ["Work", "Kinetic Energy", "Potential Energy", "Power"]
    gen = TopicGenerator(topic, prefix, subtopics)

    while not gen.is_done():
        difficulty = random.choices(["easy", "medium", "hard"], weights=[0.3, 0.5, 0.2])[0]
        subtopic = random.choice(subtopics)

        if subtopic == "Work":
            F = random.randint(10, 100)
            d = random.randint(2, 20)
            W = F * d
            if difficulty == "easy":
                question = f"A constant force of ${F}~\\text{{N}}$ moves an object by ${d}~\\text{{m}}$ in the direction of the force. Calculate the work done."
                correct = f"{W}~\\text{{J}}"
                wrongs = get_wrong_ints(W, "\\text{J}")
                explanation = f"Using $W = F \\Delta x \\cos\\theta = ({F})({d})\\cos(0^\\circ) = {W}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                angle = random.choice([30, 45, 60])
                W_ang = F * d * math.cos(math.radians(angle))
                question = f"A force of ${F}~\\text{{N}}$ is applied to an object at an angle of ${angle}^\\circ$ to the horizontal. The object moves ${d}~\\text{{m}}$ horizontally. Calculate the work done by this force."
                correct = f"{format_float(W_ang)}~\\text{{J}}"
                wrongs = get_wrong_floats(W_ang, "\\text{J}")
                explanation = f"Using $W = F \\Delta x \\cos\\theta = ({F})({d})\\cos({angle}^\\circ) \\approx {format_float(W_ang)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                f_fric = random.randint(5, 20)
                W_net = (F - f_fric) * d
                question = f"A force of ${F}~\\text{{N}}$ pushes a block horizontally for ${d}~\\text{{m}}$, while a constant frictional force of ${f_fric}~\\text{{N}}$ opposes the motion. Calculate the net work done."
                correct = f"{W_net}~\\text{{J}}"
                wrongs = get_wrong_ints(W_net, "\\text{J}")
                explanation = f"Using $W_{{net}} = F_{{net}} \\Delta x = ({F} - {f_fric})({d}) = {W_net}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Kinetic Energy":
            m = random.randint(2, 20)
            v = random.randint(5, 30)
            Ek = 0.5 * m * (v**2)
            if difficulty == "easy":
                question = f"Calculate the kinetic energy of a ${m}~\\text{{kg}}$ object moving at ${v}~\\text{{m/s}}$."
                correct = f"{format_float(Ek)}~\\text{{J}}"
                wrongs = get_wrong_floats(Ek, "\\text{J}")
                explanation = f"Using $E_k = \\frac{{1}}{{2}}mv^2 = 0.5({m})({v})^2 = {format_float(Ek)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"An object has a kinetic energy of ${format_float(Ek)}~\\text{{J}}$ and a mass of ${m}~\\text{{kg}}$. Calculate its velocity."
                correct = f"{v}~\\text{{m/s}}"
                wrongs = get_wrong_ints(v, "\\text{m/s}")
                explanation = f"Using $E_k = \\frac{{1}}{{2}}mv^2 \\Rightarrow {format_float(Ek)} = 0.5({m})v^2 \\Rightarrow v = \\sqrt{{\\frac{{{format_float(Ek)}}}{{{0.5*m}}}}} = {v}~\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                v1 = random.randint(2, 10)
                v2 = random.randint(15, 30)
                W_net = 0.5 * m * (v2**2) - 0.5 * m * (v1**2)
                question = f"A ${m}~\\text{{kg}}$ object accelerates from ${v1}~\\text{{m/s}}$ to ${v2}~\\text{{m/s}}$. Calculate the net work done on the object."
                correct = f"{format_float(W_net)}~\\text{{J}}"
                wrongs = get_wrong_floats(W_net, "\\text{J}")
                explanation = f"Using the work-energy theorem: $W_{{net}} = \\Delta E_k = \\frac{{1}}{{2}}m(v_f^2 - v_i^2) = 0.5({m})({v2}^2 - {v1}^2) = {format_float(W_net)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Potential Energy":
            m = random.randint(2, 20)
            h = random.randint(5, 50)
            g = 9.8
            Ep = m * g * h
            if difficulty == "easy":
                question = f"Calculate the gravitational potential energy of a ${m}~\\text{{kg}}$ object lifted to a height of ${h}~\\text{{m}}$. Use $g = 9.8~\\text{{m/s}}^2$."
                correct = f"{format_float(Ep)}~\\text{{J}}"
                wrongs = get_wrong_floats(Ep, "\\text{J}")
                explanation = f"Using $E_p = mgh = ({m})(9.8)({h}) = {format_float(Ep)}~\\text{{J}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                question = f"An object has a gravitational potential energy of ${format_float(Ep)}~\\text{{J}}$ at a height of ${h}~\\text{{m}}$. Calculate its mass. Use $g = 9.8~\\text{{m/s}}^2$."
                correct = f"{m}~\\text{{kg}}"
                wrongs = get_wrong_ints(m, "\\text{kg}")
                explanation = f"Using $E_p = mgh \\Rightarrow {format_float(Ep)} = m(9.8)({h}) \\Rightarrow m = \\frac{{{format_float(Ep)}}}{{{9.8 * h}}} = {m}~\\text{{kg}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                v = math.sqrt(2 * g * h)
                question = f"A ${m}~\\text{{kg}}$ object is dropped from a height of ${h}~\\text{{m}}$. Ignoring air resistance, calculate its velocity just before it hits the ground. Use $g = 9.8~\\text{{m/s}}^2$."
                correct = f"{format_float(v)}~\\text{{m/s}}"
                wrongs = get_wrong_floats(v, "\\text{m/s}")
                explanation = f"Using conservation of mechanical energy: $mgh = \\frac{{1}}{{2}}mv^2 \\Rightarrow v = \\sqrt{{2gh}} = \\sqrt{{2(9.8)({h})}} \\approx {format_float(v)}~\\text{{m/s}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

        elif subtopic == "Power":
            W = random.randint(100, 1000)
            t = random.randint(2, 20)
            P = W / t
            if difficulty == "easy":
                question = f"An engine does ${W}~\\text{{J}}$ of work in ${t}~\\text{{s}}$. Calculate its power output."
                correct = f"{format_float(P)}~\\text{{W}}"
                wrongs = get_wrong_floats(P, "\\text{W}")
                explanation = f"Using $P = \\frac{{W}}{{t}} = \\frac{{{W}}}{{{t}}} = {format_float(P)}~\\text{{W}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "medium":
                F = random.randint(50, 200)
                v = random.randint(5, 25)
                P_v = F * v
                question = f"A car engine exerts a constant force of ${F}~\\text{{N}}$ to maintain a constant speed of ${v}~\\text{{m/s}}$. Calculate the power output."
                correct = f"{P_v}~\\text{{W}}"
                wrongs = get_wrong_ints(P_v, "\\text{W}")
                explanation = f"Using $P = Fv = ({F})({v}) = {P_v}~\\text{{W}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)
            elif difficulty == "hard":
                m = random.randint(500, 1500)
                v = random.randint(10, 30)
                t = random.randint(5, 15)
                P_avg = (0.5 * m * v**2) / t
                question = f"A car of mass ${m}~\\text{{kg}}$ accelerates from rest to ${v}~\\text{{m/s}}$ in ${t}~\\text{{s}}$. Calculate the average power required."
                correct = f"{format_float(P_avg)}~\\text{{W}}"
                wrongs = get_wrong_floats(P_avg, "\\text{W}")
                explanation = f"Using $P = \\frac{{W}}{{\\Delta t}} = \\frac{{\\Delta E_k}}{{\\Delta t}} = \\frac{{0.5({m})({v})^2}}{{{t}}} \\approx {format_float(P_avg)}~\\text{{W}}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

    gen.save_to_json("dataset/paper1_work_energy_power.json")

if __name__ == "__main__":
    gen_mechanics()
    gen_work_energy()
    print("Generated Mechanics and WEP datasets.")
