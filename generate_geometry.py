import random
import math
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

def generate_geometry():
    gen = TopicGenerator("Euclidean Geometry", "GEOM", ["angle relationships", "triangle theorems", "cyclic quadrilaterals"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        if subtopic == "angle relationships":
            if difficulty == "easy":
                a = random.randint(30, 150)
                q = f"If two supplementary angles are given and one measures ${a}^\\circ$, what is the measure of the other angle?"
                ans = 180 - a
                correct = f"{ans}^\\circ"
                wrongs = [f"{w}^\\circ" for w in get_wrong_ints(ans)]
                exp = f"Supplementary angles add up to $180^\\circ$. $180^\\circ - {a}^\\circ = {ans}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # vertically opposite + algebra
                a = random.randint(2, 5)
                b = random.randint(10, 40)
                x = random.randint(10, 30)
                angle1 = a*x + b
                # another expression
                # a*x + b = c*x + d
                c = random.randint(1, a-1) if a > 1 else 1
                d = angle1 - c*x
                q = f"Two vertically opposite angles measure $({a}x + {b})^\\circ$ and $({c}x {'+' if d>=0 else ''}{d})^\\circ$. Find the value of $x$."
                correct = str(x)
                wrongs = get_wrong_ints(x)
                exp = f"Vertically opposite angles are equal: ${a}x + {b} = {c}x {'+' if d>=0 else ''}{d} \\implies {(a-c)}x = {d-b} \\implies x = {x}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # co-interior angles + algebra
                a = random.randint(2, 6)
                b = random.randint(5, 20)
                c = random.randint(2, 6)
                d = random.randint(5, 20)
                # ax + b + cx + d = 180
                # (a+c)x = 180 - b - d
                total_x = a + c
                sum_c = b + d
                rem = 180 - sum_c
                # Ensure integer x
                if rem % total_x == 0:
                    x = rem // total_x
                    if x > 0:
                        angle1 = a*x + b
                        angle2 = c*x + d
                        q = f"Two parallel lines are intersected by a transversal. A pair of co-interior angles are $({a}x + {b})^\\circ$ and $({c}x + {d})^\\circ$. Find the size of the larger angle."
                        ans = max(angle1, angle2)
                        correct = f"{ans}^\\circ"
                        wrongs = [f"{w}^\\circ" for w in get_wrong_ints(ans)]
                        exp = f"Co-interior angles between parallel lines are supplementary. ${a}x + {b} + {c}x + {d} = 180 \\implies {total_x}x = {rem} \\implies x = {x}$. The angles are ${angle1}^\\circ$ and ${angle2}^\\circ$, so the larger is ${ans}^\\circ$."
                        gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "triangle theorems":
            if difficulty == "easy":
                a = random.randint(30, 80)
                b = random.randint(30, 80)
                q = f"Two angles of a triangle measure ${a}^\\circ$ and ${b}^\\circ$. What is the measure of the third angle?"
                ans = 180 - a - b
                correct = f"{ans}^\\circ"
                wrongs = [f"{w}^\\circ" for w in get_wrong_ints(ans)]
                exp = f"Sum of angles in a triangle is $180^\\circ$. $180^\\circ - ({a}^\\circ + {b}^\\circ) = {ans}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Exterior angle theorem
                a = random.randint(30, 70)
                b = random.randint(30, 70)
                ext = a + b
                q = f"The exterior angle of a triangle is ${ext}^\\circ$. If one of the opposite interior angles is ${a}^\\circ$, find the other opposite interior angle."
                ans = b
                correct = f"{ans}^\\circ"
                wrongs = [f"{w}^\\circ" for w in get_wrong_ints(ans)]
                exp = f"Exterior angle = sum of opposite interior angles. ${ext}^\\circ = {a}^\\circ + x \\implies x = {ans}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # Isosceles + algebra
                x = random.randint(10, 30)
                # base angles = ax + b, vertex = cx + d
                a = random.randint(1, 3)
                b = random.randint(5, 15)
                base = a*x + b
                vertex = 180 - 2*base
                # cx + d = vertex
                c = random.randint(1, 3)
                d = vertex - c*x
                if d > 0 and vertex > 0:
                    q = f"In an isosceles triangle, the two equal base angles each measure $({a}x + {b})^\\circ$. The vertex angle measures $({c}x + {d})^\\circ$. Find the value of $x$."
                    correct = str(x)
                    wrongs = get_wrong_ints(x)
                    exp = f"Sum of angles is $180^\\circ$. $2({a}x + {b}) + ({c}x + {d}) = 180 \\implies {2*a+c}x + {2*b+d} = 180 \\implies {2*a+c}x = {180-2*b-d} \\implies x = {x}$."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "cyclic quadrilaterals":
            if difficulty == "easy":
                a = random.randint(60, 120)
                q = f"One interior angle of a cyclic quadrilateral is ${a}^\\circ$. What is the measure of the opposite interior angle?"
                ans = 180 - a
                correct = f"{ans}^\\circ"
                wrongs = [f"{w}^\\circ" for w in get_wrong_ints(ans)]
                exp = f"Opposite angles of a cyclic quadrilateral are supplementary. $180^\\circ - {a}^\\circ = {ans}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                ext = random.randint(70, 110)
                q = f"An exterior angle of a cyclic quadrilateral measures ${ext}^\\circ$. Find the measure of the interior opposite angle."
                ans = ext
                correct = f"{ans}^\\circ"
                wrongs = [f"{w}^\\circ" for w in get_wrong_ints(ans)]
                exp = f"The exterior angle of a cyclic quadrilateral is equal to the interior opposite angle, so it is ${ans}^\\circ$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # Angles subtended by same arc + cyclic quad
                # "In a cyclic quad ABCD, angle subtended by arc AB at the circumference is 40. Then another angle..."
                x = random.randint(10, 25)
                a = random.randint(1, 3)
                b = random.randint(5, 15)
                c = random.randint(1, 3)
                d = random.randint(5, 15)
                ang = a*x + b
                ang2 = c*x + d
                if ang == ang2:
                    q = f"Angles subtended by the same arc in a circle measure $({a}x + {b})^\\circ$ and $({c}x + {d})^\\circ$. Determine the size of the angle."
                    correct = f"{ang}^\\circ"
                    wrongs = [f"{w}^\\circ" for w in get_wrong_ints(ang)]
                    exp = f"Angles in the same segment are equal. ${a}x + {b} = {c}x + {d} \\implies {(a-c)}x = {d-b} \\implies x = {x}$. The angle is ${a}({x}) + {b} = {ang}^\\circ$."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

    return gen

if __name__ == "__main__":
    gen = generate_geometry()
    gen.save_to_json("paper2_geometry.json")
    print(f"Generated {len(gen.questions)} geometry questions.")
