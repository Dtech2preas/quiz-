import random
import math
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

def generate_analytical():
    gen = TopicGenerator("Analytical Geometry", "ANAGEO", ["distance formula", "midpoint formula", "gradient of a line", "equation of a line"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
        x2, y2 = random.randint(-10, 10), random.randint(-10, 10)
        if (x1, y1) == (x2, y2): continue

        if subtopic == "distance formula":
            dx = x2 - x1
            dy = y2 - y1
            d_sq = dx**2 + dy**2

            if difficulty == "easy":
                # Find length squared
                q = f"Given points A$({x1}; {y1})$ and B$({x2}; {y2})$, find the square of the distance AB$^2$."
                correct = str(d_sq)
                wrongs = get_wrong_ints(d_sq)
                exp = f"AB$^2 = (x_2 - x_1)^2 + (y_2 - y_1)^2 = ({x2} - {x1})^2 + ({y2} - {y1})^2 = {d_sq}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                d_val = math.sqrt(d_sq)
                q = f"Find the distance between points A$({x1}; {y1})$ and B$({x2}; {y2})$ correct to two decimal places."
                d_round = round(d_val, 2)
                correct = f"{d_round:.2f}"
                wrongs = set()
                while len(wrongs) < 8:
                    w = round(random.uniform(d_round - 5, d_round + 5), 2)
                    w_str = f"{w:.2f}"
                    if w > 0 and w_str != correct: wrongs.add(w_str)
                exp = f"$d = \\sqrt{{({x2} - {x1})^2 + ({y2} - {y1})^2}} = \\sqrt{{{d_sq}}} \\approx {d_round:.2f}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # find unknown coordinate
                x_unk = x2
                q = f"The distance between A$({x1}; {y1})$ and B$(x; {y2})$ is $\\sqrt{{{d_sq}}}$. Find the possible value(s) of $x$."
                # (x - x1)^2 = d_sq - dy^2 = dx^2
                ans1 = x1 + abs(dx)
                ans2 = x1 - abs(dx)
                roots = sorted(list(set([ans1, ans2])))
                correct = ", ".join(map(str, roots))
                wrongs = set()
                while len(wrongs) < 8:
                    w1 = random.randint(-15, 15)
                    w2 = random.randint(-15, 15)
                    w_roots = sorted(list(set([w1, w2])))
                    w_str = ", ".join(map(str, w_roots))
                    if w_str != correct: wrongs.add(w_str)
                exp = f"$\\sqrt{{(x - {x1})^2 + ({y2} - {y1})^2}} = \\sqrt{{{d_sq}}} \\implies (x - {x1})^2 + {dy**2} = {d_sq} \\implies (x - {x1})^2 = {dx**2} \\implies x - {x1} = \\pm {abs(dx)} \\implies x = {ans1}$ or $x = {ans2}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

        elif subtopic == "midpoint formula":
            if difficulty == "easy":
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                q = f"Find the midpoint of the line segment joining A$({x1}; {y1})$ and B$({x2}; {y2})$."
                mx_str = int(mx) if mx.is_integer() else f"{mx:.1f}"
                my_str = int(my) if my.is_integer() else f"{my:.1f}"
                correct = f"({mx_str}; {my_str})"
                wrongs = set()
                while len(wrongs) < 8:
                    wx = mx + random.choice([-2, -1, 0, 1, 2, 0.5, -0.5])
                    wy = my + random.choice([-2, -1, 0, 1, 2, 0.5, -0.5])
                    wx_str = int(wx) if wx.is_integer() else f"{wx:.1f}"
                    wy_str = int(wy) if wy.is_integer() else f"{wy:.1f}"
                    w_str = f"({wx_str}; {wy_str})"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"$M\\left(\\frac{{{x1}+{x2}}}{{2}}; \\frac{{{y1}+{y2}}}{{2}}\\right) = ({mx_str}; {my_str})$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "medium":
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                mx_str = int(mx) if mx.is_integer() else f"{mx:.1f}"
                my_str = int(my) if my.is_integer() else f"{my:.1f}"
                q = f"The midpoint of line segment AB is M$({mx_str}; {my_str})$. If A is $({x1}; {y1})$, find the coordinates of B."
                correct = f"({x2}; {y2})"
                wrongs = set()
                while len(wrongs) < 8:
                    wx = x2 + random.randint(-5, 5)
                    wy = y2 + random.randint(-5, 5)
                    w_str = f"({wx}; {wy})"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"$\\frac{{{x1} + x_2}}{{2}} = {mx_str} \\implies x_2 = {x2}$. $\\frac{{{y1} + y_2}}{{2}} = {my_str} \\implies y_2 = {y2}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # find coordinates forming a parallelogram
                x3, y3 = random.randint(-5, 5), random.randint(-5, 5)
                # Diagonals bisect each other. AC midpoint = BD midpoint.
                # A=(x1, y1), B=(x2, y2), C=(x3, y3), D=(x4, y4)
                # (x1+x3)/2 = (x2+x4)/2 -> x4 = x1+x3-x2
                x4 = x1 + x3 - x2
                y4 = y1 + y3 - y2
                q = f"A$({x1}; {y1})$, B$({x2}; {y2})$, C$({x3}; {y3})$, and D$(x; y)$ are the vertices of a parallelogram ABCD. Determine the coordinates of D."
                correct = f"({x4}; {y4})"
                wrongs = set()
                while len(wrongs) < 8:
                    wx = x4 + random.randint(-5, 5)
                    wy = y4 + random.randint(-5, 5)
                    w_str = f"({wx}; {wy})"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Diagonals bisect each other. Midpoint AC = Midpoint BD. $\\frac{{{x1}+{x3}}}{{2}} = \\frac{{{x2}+x}}{{2}} \\implies x = {x4}$. $\\frac{{{y1}+{y3}}}{{2}} = \\frac{{{y2}+y}}{{2}} \\implies y = {y4}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

        elif subtopic == "gradient of a line":
            if x1 == x2: continue
            m = (y2 - y1) / (x2 - x1)
            if not m.is_integer() and difficulty != "easy":
                m = round(m, 2)

            if difficulty == "easy":
                if not m.is_integer(): continue
                q = f"Determine the gradient of the line passing through points A$({x1}; {y1})$ and B$({x2}; {y2})$."
                correct = str(int(m))
                wrongs = get_wrong_ints(int(m))
                exp = f"$m = \\frac{{{y2} - {y1}}}{{{x2} - {x1}}} = {int(m)}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # find collinear coordinate
                x3 = random.randint(x2 + 1, x2 + 5)
                y3 = y2 + m * (x3 - x2)
                if not y3.is_integer(): continue
                y3 = int(y3)
                q = f"Points A$({x1}; {y1})$, B$({x2}; {y2})$, and C$({x3}; y)$ are collinear. Find $y$."
                correct = str(y3)
                wrongs = get_wrong_ints(y3)
                exp = f"Gradients are equal: $m_{{AB}} = \\frac{{{y2} - {y1}}}{{{x2} - {x1}}} = {m}$. Thus, $\\frac{{y - {y2}}}{{{x3} - {x2}}} = {m} \\implies y - {y2} = {m * (x3 - x2)} \\implies y = {y3}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # perpendicular lines
                if m == 0: continue
                m_perp = -1 / m
                # Line 1 passes through A, B. Line 2 passes through C(x3, y3) and D(x4, y4). Find y4.
                x3, y3 = random.randint(-5, 5), random.randint(-5, 5)
                x4 = x3 + (y2 - y1) # ensures y4 will be integer
                y4 = y3 + m_perp * (x4 - x3)
                if not y4.is_integer(): continue
                y4 = int(y4)
                q = f"Line AB passes through A$({x1}; {y1})$ and B$({x2}; {y2})$. Line CD passes through C$({x3}; {y3})$ and D$({x4}; y)$. If AB $\\perp$ CD, find $y$."
                correct = str(y4)
                wrongs = get_wrong_ints(y4)
                exp = f"$m_{{AB}} = \\frac{{{y2} - {y1}}}{{{x2} - {x1}}} = {m}$. For perpendicular lines, $m_{{CD}} = -\\frac{{1}}{{m_{{AB}}}} = {m_perp}$. $\\frac{{y - {y3}}}{{{x4} - {x3}}} = {m_perp} \\implies y = {y4}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "equation of a line":
            if x1 == x2: continue
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            if not m.is_integer() or not c.is_integer(): continue
            m, c = int(m), int(c)

            if difficulty == "easy":
                q = f"Determine the equation of the line passing through points A$({x1}; {y1})$ and B$({x2}; {y2})$."
                correct = f"y = {m}x {'+' if c>=0 else '-'} {abs(c)}"
                wrongs = set()
                while len(wrongs) < 8:
                    wm = m + random.choice([-2, -1, 1, 2])
                    wc = c + random.choice([-2, -1, 1, 2])
                    w_str = f"y = {wm}x {'+' if wc>=0 else '-'} {abs(wc)}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Gradient $m = {m}$. Using $y - y_1 = m(x - x_1) \\implies y - {y1} = {m}(x - {x1}) \\implies {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "medium":
                # parallel to line
                x3, y3 = random.randint(-5, 5), random.randint(-5, 5)
                c_new = y3 - m * x3
                q = f"Find the equation of the line passing through $({x3}; {y3})$ and parallel to the line $y = {m}x {'+' if c>=0 else '-'} {abs(c)}$."
                correct = f"y = {m}x {'+' if c_new>=0 else '-'} {abs(c_new)}"
                wrongs = set()
                while len(wrongs) < 8:
                    wm = m + random.choice([-2, -1, 0, 1, 2])
                    wc = c_new + random.choice([-5, -3, -1, 1, 3, 5])
                    w_str = f"y = {wm}x {'+' if wc>=0 else '-'} {abs(wc)}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Parallel lines have the same gradient $m = {m}$. Equation is $y - {y3} = {m}(x - {x3}) \\implies {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                if m == 0: continue
                # perpendicular bisector
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                m_perp = -1 / m
                if not m_perp.is_integer() or not mx.is_integer() or not my.is_integer(): continue
                m_perp, mx, my = int(m_perp), int(mx), int(my)
                c_perp = my - m_perp * mx
                q = f"Determine the equation of the perpendicular bisector of the line segment joining A$({x1}; {y1})$ and B$({x2}; {y2})$."
                correct = f"y = {m_perp}x {'+' if c_perp>=0 else '-'} {abs(c_perp)}"
                wrongs = set()
                while len(wrongs) < 8:
                    wm = m_perp + random.choice([-2, -1, 1, 2])
                    wc = c_perp + random.choice([-3, -2, -1, 1, 2, 3])
                    w_str = f"y = {wm}x {'+' if wc>=0 else '-'} {abs(wc)}"
                    if w_str != correct: wrongs.add(w_str)
                exp = f"Midpoint is $({mx}; {my})$. Gradient of AB is ${m}$, so perpendicular gradient is ${m_perp}$. Using point $({mx}; {my})$ gives ${correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

    return gen

if __name__ == "__main__":
    gen = generate_analytical()
    gen.save_to_json("paper2_analytical_geometry.json")
    print(f"Generated {len(gen.questions)} analytical geometry questions.")
