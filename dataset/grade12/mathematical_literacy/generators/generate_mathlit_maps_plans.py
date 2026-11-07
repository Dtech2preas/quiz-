import sys
import os
import time

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from generate_mathlit12 import generate_p2_maps_plans

def generate_mathlit_maps_plans():
    t0 = time.time()
    out_dir = os.path.join(root_dir, "dataset/grade12/mathematical_literacy")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "paper2_mathlit12_maps_plans.json")
    print("Generating Grade 12 Math Lit: Paper 2 Maps and Plans...")
    gen = generate_p2_maps_plans()
    gen.save_to_json(out_path)
    print(f"Finished generate_mathlit_maps_plans in {time.time() - t0:.2f}s -> {out_path}")

if __name__ == "__main__":
    generate_mathlit_maps_plans()
