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
            if difficulty == "easy":
                # Template 1: Basic Weight component
                mass = random.uniform(2.0, 20.0)
                angle = random.randint(10, 60)
                fg_parallel = mass * 9.8 * math.sin(math.radians(angle))
                question = f"A {format_val_unit(mass, 'kg')} block rests on a rough inclined plane making an angle of {angle}° with the horizontal. Calculate the magnitude of the component of the block's weight parallel to the incline."
                correct = format_val_unit(fg_parallel, "N")
                wrongs = get_wrong_floats(fg_parallel, "N")
                explanation = f"$F_{{g||}} = mg \sin\theta = ({format_val_unit(mass, '')})(9.8)(\sin {angle}^\circ) = {format_val_unit(fg_parallel, 'N')}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                # Template 2: Normal force on incline
                fg_perp = mass * 9.8 * math.cos(math.radians(angle))
                question = f"A {format_val_unit(mass, 'kg')} block rests on a rough inclined plane making an angle of {angle}° with the horizontal. Calculate the magnitude of the normal force acting on the block."
                correct = format_val_unit(fg_perp, "N")
                wrongs = get_wrong_floats(fg_perp, "N")
                explanation = f"$N = F_{{g\perp}} = mg \cos\theta = ({format_val_unit(mass, '')})(9.8)(\cos {angle}^\circ) = {format_val_unit(fg_perp, 'N')}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

            elif difficulty == "medium":
                # Template 3: Pulley system (Two blocks, one hanging, one on rough horizontal)
                m1 = random.uniform(2.0, 8.0)
                m2 = random.uniform(1.0, 5.0)
                mu_k = random.uniform(0.1, 0.4)

                fk = mu_k * m1 * 9.8
                fg2 = m2 * 9.8
                fnet = fg2 - fk
                mtot = m1 + m2
                a = fnet / mtot

                if a > 0:
                    question = f"Block A ({format_val_unit(m1, 'kg')}) on a rough horizontal surface is connected by a light inextensible string passing over a frictionless pulley to Block B ({format_val_unit(m2, 'kg')}) hanging vertically. The coefficient of kinetic friction between Block A and the surface is {format_float(mu_k, 2)}. Calculate the magnitude of the acceleration of the system."
                    correct = format_val_unit(a, "m\cdot s^{-2}")
                    wrongs = get_wrong_floats(a, "m\cdot s^{-2}")
                    explanation = f"For A: $T - f_k = m_A a$. For B: $m_B g - T = m_B a$. Adding gives $m_B g - \mu_k m_A g = (m_A + m_B)a$. $({format_val_unit(m2, '')})(9.8) - ({format_float(mu_k, 2)})({format_val_unit(m1, '')})(9.8) = ({format_val_unit(mtot, '')})a$. $a = {format_val_unit(a, 'm\\cdot s^{-2}')}$."
                    gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                    # Template 4: Tension in the string
                    T = m2 * 9.8 - m2 * a
                    question = f"Block A ({format_val_unit(m1, 'kg')}) on a rough horizontal surface is connected by a light inextensible string passing over a frictionless pulley to Block B ({format_val_unit(m2, 'kg')}) hanging vertically. The system accelerates at {format_val_unit(a, 'm\cdot s^{-2}')}. Calculate the magnitude of the tension in the string."
                    correct = format_val_unit(T, "N")
                    wrongs = get_wrong_floats(T, "N")
                    explanation = f"For Block B: $F_{{net}} = m_B g - T = m_B a \Rightarrow T = m_B g - m_B a = ({format_val_unit(m2, '')})(9.8) - ({format_val_unit(m2, '')})({format_float(a, 2)}) = {format_val_unit(T, 'N')}$."
                    gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                # Template 5: Applied force at an angle (Horizontal surface)
                mass = random.uniform(5.0, 15.0)
                force = random.uniform(20.0, 100.0)
                angle = random.randint(20, 50)
                mu_k = random.uniform(0.1, 0.3)

                fx = force * math.cos(math.radians(angle))
                fy = force * math.sin(math.radians(angle))
                N = mass * 9.8 - fy
                fk = mu_k * N
                a = (fx - fk) / mass

                if a > 0:
                    question = f"A block of mass {format_val_unit(mass, 'kg')} is pulled along a rough horizontal floor by a force of {format_val_unit(force, 'N')} acting at an angle of {angle}° above the horizontal. The coefficient of kinetic friction is {format_float(mu_k, 2)}. Calculate the normal force acting on the block."
                    correct = format_val_unit(N, "N")
                    wrongs = get_wrong_floats(N, "N")
                    explanation = f"Vertical equilibrium: $N + F_y = mg \Rightarrow N = mg - F\sin\theta = ({format_val_unit(mass, '')})(9.8) - ({format_val_unit(force, '')})\sin({angle}^\circ) = {format_val_unit(N, 'N')}$."
                    gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                    question = f"A block of mass {format_val_unit(mass, 'kg')} is pulled along a rough horizontal floor by a force of {format_val_unit(force, 'N')} acting at an angle of {angle}° above the horizontal. The coefficient of kinetic friction is {format_float(mu_k, 2)}. Calculate the acceleration of the block."
                    correct = format_val_unit(a, "m\cdot s^{-2}")
                    wrongs = get_wrong_floats(a, "m\cdot s^{-2}")
                    explanation = f"$N = mg - F\sin\theta = {format_float(N, 2)}$. $f_k = \mu_k N = ({format_float(mu_k, 2)})({format_float(N, 2)}) = {format_float(fk, 2)}$. $F_{{net}} = F_x - f_k = ma \Rightarrow {format_float(fx, 2)} - {format_float(fk, 2)} = ({format_val_unit(mass, '')})a \Rightarrow a = {format_val_unit(a, 'm\\cdot s^{-2}')}$."
                    gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

            elif difficulty == "hard":
                # Template 6: Block pushed UP a rough incline
                mass = random.uniform(2.0, 10.0)
                angle = random.randint(15, 45)
                mu_k = random.uniform(0.1, 0.4)
                force = random.uniform(80.0, 200.0)

                fg_parallel = mass * 9.8 * math.sin(math.radians(angle))
                fg_perp = mass * 9.8 * math.cos(math.radians(angle))
                fk = mu_k * fg_perp
                a = (force - fg_parallel - fk) / mass

                if a > 0:
                    question = f"A block of mass {format_val_unit(mass, 'kg')} is pushed UP a rough inclined plane by a constant force of {format_val_unit(force, 'N')} parallel to the incline. The incline is at {angle}° to the horizontal and the coefficient of kinetic friction is {format_float(mu_k, 2)}. Calculate the acceleration of the block."
                    correct = format_val_unit(a, "m\cdot s^{-2}")
                    wrongs = get_wrong_floats(a, "m\cdot s^{-2}")
                    explanation = f"$F_{{net}} = F_{{applied}} - (F_{{g||}} + f_k) = ma$. $F_{{g||}} = mg\sin\theta = {format_float(fg_parallel, 2)}$. $f_k = \mu_k mg\cos\theta = {format_float(fk, 2)}$. ${format_val_unit(force, '')} - ({format_float(fg_parallel, 2)} + {format_float(fk, 2)}) = {format_val_unit(mass, '')}a \Rightarrow a = {format_val_unit(a, 'm\\cdot s^{-2}')}$."
                    gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                # Template 7: Elevators (Apparent weight)
                mass = random.uniform(50.0, 90.0)
                a = random.uniform(1.0, 3.0)
                T_up = mass * (9.8 + a)
                T_down = mass * (9.8 - a)

                question = f"A person of mass {format_val_unit(mass, 'kg')} stands on a bathroom scale inside an elevator. Calculate the reading on the scale (in Newtons) if the elevator is accelerating UPWARDS at {format_val_unit(a, 'm\cdot s^{-2}')}."
                correct = format_val_unit(T_up, "N")
                wrongs = get_wrong_floats(T_up, "N")
                explanation = f"$F_{{net}} = N - mg = ma \Rightarrow N = m(g + a) = ({format_val_unit(mass, '')})(9.8 + {format_float(a, 2)}) = {format_val_unit(T_up, 'N')}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                question = f"A person of mass {format_val_unit(mass, 'kg')} stands on a bathroom scale inside an elevator. Calculate the reading on the scale (in Newtons) if the elevator is accelerating DOWNWARDS at {format_val_unit(a, 'm\cdot s^{-2}')}."
                correct = format_val_unit(T_down, "N")
                wrongs = get_wrong_floats(T_down, "N")
                explanation = f"$F_{{net}} = mg - N = ma \Rightarrow N = m(g - a) = ({format_val_unit(mass, '')})(9.8 - {format_float(a, 2)}) = {format_val_unit(T_down, 'N')}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)


        elif subtopic == "Momentum":
            if difficulty == "easy":
                # Template 8: Basic Momentum
                m = random.uniform(800.0, 2000.0)
                v = random.uniform(10.0, 30.0)
                p = m * v
                question = f"Calculate the magnitude of the momentum of a car of mass {format_val_unit(m, 'kg')} traveling at {format_val_unit(v, 'm\cdot s^{-1}')}."
                correct = format_val_unit(p, "kg\cdot m\cdot s^{-1}")
                wrongs = get_wrong_floats(p, "kg\cdot m\cdot s^{-1}")
                explanation = f"$p = mv = ({format_val_unit(m, '')})({format_val_unit(v, '')}) = {format_val_unit(p, 'kg\cdot m\cdot s^{-1}')}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                # Template 9: Impulse
                f = random.uniform(200.0, 800.0)
                t = random.uniform(0.1, 0.5)
                impulse = f * t
                question = f"A force of {format_val_unit(f, 'N')} acts on an object for {format_val_unit(t, 's')}. Calculate the magnitude of the impulse."
                correct = format_val_unit(impulse, "N\cdot s")
                wrongs = get_wrong_floats(impulse, "N\cdot s")
                explanation = f"$\text{{Impulse}} = F_{{net}} \Delta t = ({format_val_unit(f, '')})({format_val_unit(t, '')}) = {format_val_unit(impulse, 'N\cdot s')}$."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

            elif difficulty == "medium":
                # Template 10: 1D Elastic/Inelastic Collision (Finding v2f)
                m1 = random.uniform(2.0, 5.0)
                m2 = random.uniform(1.0, 4.0)
                v1_initial = random.uniform(4.0, 10.0)
                v2_initial = -random.uniform(2.0, 6.0) # opposite direction
                v1_final = random.uniform(-2.0, 2.0)

                v2_final = (m1*v1_initial + m2*v2_initial - m1*v1_final) / m2
                dir2 = "to the right" if v2_final > 0 else "to the left"

                question = f"Object A (mass {format_val_unit(m1, 'kg')}) moves to the right at {format_val_unit(v1_initial, 'm\cdot s^{-1}')} and collides with Object B (mass {format_val_unit(m2, 'kg')}) moving to the left at {format_val_unit(abs(v2_initial), 'm\cdot s^{-1}')}. After the collision, Object A moves at {format_val_unit(abs(v1_final), 'm\cdot s^{-1}')} {'to the right' if v1_final > 0 else 'to the left'}. Calculate the magnitude of the velocity of Object B after the collision."
                correct = format_val_unit(abs(v2_final), "m\cdot s^{-1}")
                wrongs = get_wrong_floats(abs(v2_final), "m\cdot s^{-1}")
                explanation = f"$\Sigma p_i = \Sigma p_f \Rightarrow m_A v_{{Ai}} + m_B v_{{Bi}} = m_A v_{{Af}} + m_B v_{{Bf}}$. Let right be positive. $({format_val_unit(m1, '')})({format_val_unit(v1_initial, '')}) + ({format_val_unit(m2, '')})(-{format_val_unit(abs(v2_initial), '')}) = ({format_val_unit(m1, '')})({' ' if v1_final>0 else '-'}{format_val_unit(abs(v1_final), '')}) + ({format_val_unit(m2, '')})v_{{Bf}}$. $v_{{Bf}} = {format_float(v2_final, 2)}~\text{{m\cdot s}}^{{-1}}$, so magnitude is {format_val_unit(abs(v2_final), 'm\cdot s^{-1}')}."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                # Template 11: Change in momentum (Bouncing ball)
                m = random.uniform(0.1, 0.5)
                v_initial = random.uniform(5.0, 12.0) # hits floor
                v_final = -random.uniform(3.0, 8.0) # bounces up (take down as positive)
                delta_p = m * (v_final - v_initial)
                question = f"A {format_val_unit(m, 'kg')} ball is dropped and hits the ground at {format_val_unit(v_initial, 'm\cdot s^{-1}')}. It bounces vertically upwards at {format_val_unit(abs(v_final), 'm\cdot s^{-1}')}. Calculate the magnitude of the change in momentum of the ball."
                correct = format_val_unit(abs(delta_p), "kg\cdot m\cdot s^{-1}")
                wrongs = get_wrong_floats(abs(delta_p), "kg\cdot m\cdot s^{-1}")
                explanation = f"Let downwards be positive. $v_i = +{format_val_unit(v_initial, '')}$, $v_f = -{format_val_unit(abs(v_final), '')}$. $\Delta p = m(v_f - v_i) = ({format_val_unit(m, '')})(-{format_float(abs(v_final), 2)} - {format_float(v_initial, 2)}) = {format_float(delta_p, 2)}~\text{{kg\cdot m\cdot s}}^{{-1}}$. Magnitude is {format_val_unit(abs(delta_p), 'kg\cdot m\cdot s^{-1}')}."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

            elif difficulty == "hard":
                # Template 12: Force exerted during bounce
                m = random.uniform(0.2, 0.8)
                v_initial = random.uniform(10.0, 20.0) # hits wall
                v_final = -random.uniform(5.0, 15.0) # rebounds
                t = random.uniform(0.01, 0.05)
                fnet = m * (v_final - v_initial) / t

                question = f"A {format_val_unit(m, 'kg')} ball strikes a wall horizontally at {format_val_unit(v_initial, 'm\cdot s^{-1}')} and rebounds in the opposite direction at {format_val_unit(abs(v_final), 'm\cdot s^{-1}')}. The contact time with the wall is {format_val_unit(t, 's')}. Calculate the magnitude of the average force exerted by the wall on the ball."
                correct = format_val_unit(abs(fnet), "N")
                wrongs = get_wrong_floats(abs(fnet), "N")
                explanation = f"Let initial direction be positive. $\Delta p = m(v_f - v_i) = ({format_val_unit(m, '')})(-{format_float(abs(v_final), 2)} - {format_float(v_initial, 2)}) = {format_float(m*(v_final-v_initial), 2)}$. $F_{{net}} = \frac{{\Delta p}}{{\Delta t}} = \frac{{{format_float(m*(v_final-v_initial), 2)}}}{{{format_val_unit(t, '')}}} = {format_float(fnet, 2)}~\text{{N}}$. Magnitude is {format_val_unit(abs(fnet), 'N')}."
                gen.add_question(subtopic, difficulty, question, correct, wrongs, explanation)

                # Template 13: Explosion / Recoil
                m_gun = random.uniform(2.0, 5.0)
                m_bullet = random.uniform(0.01, 0.05)
                v_bullet = random.uniform(300.0, 600.0)
                v_gun = -(m_bullet * v_bullet) / m_gun

                question = f"A stationary rifle of mass {format_val_unit(m_gun, 'kg')} fires a bullet of mass {format_float(m_bullet*1000, 1)} g at a velocity of {format_val_unit(v_bullet, 'm\cdot s^{-1}')} to the right. Calculate the recoil velocity of the rifle."
                correct = format_val_unit(abs(v_gun), "m\cdot s^{-1}")
                wrongs = get_wrong_floats(abs(v_gun), "m\cdot s^{-1}")
                explanation = f"$\Sigma p_i = \Sigma p_f \Rightarrow 0 = m_{{rifle}} v_{{rifle}} + m_{{bullet}} v_{{bullet}}$. $0 = ({format_val_unit(m_gun, '')})v_{{rifle}} + ({format_val_unit(m_bullet, '')})({format_val_unit(v_bullet, '')})$. $v_{{rifle}} = {format_float(v_gun, 2)}~\text{{m\cdot s}}^{{-1}}$. Magnitude is {format_val_unit(abs(v_gun), 'm\cdot s^{-1}')}."
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
