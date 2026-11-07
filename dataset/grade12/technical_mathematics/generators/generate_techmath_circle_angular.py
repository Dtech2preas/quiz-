import sys
import os
import time

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
tech_math_dir = os.path.join(root_dir, "generators/grade12/technical_mathematics")
if tech_math_dir not in sys.path:
    sys.path.insert(0, tech_math_dir)

from generate_tech_math import gen_p2_circle_angular

def generate_techmath_circle_angular():
    t0 = time.time()
    print("Generating Grade 12 Technical Mathematics: Paper 2 Circle Geometry & Angular Movement...")
    gen_p2_circle_angular()
    print(f"Finished generate_techmath_circle_angular in {time.time() - t0:.2f}s")

if __name__ == "__main__":
    generate_techmath_circle_angular()
