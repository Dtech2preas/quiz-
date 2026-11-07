import sys
import os
import time

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from generate_mathlit12 import generate_p1_data_handling

def generate_mathlit_data_handling():
    t0 = time.time()
    out_dir = os.path.join(root_dir, "dataset/grade12/mathematical_literacy")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "paper1_mathlit12_data_handling.json")
    print("Generating Grade 12 Math Lit: Paper 1 Data Handling...")
    gen = generate_p1_data_handling()
    gen.save_to_json(out_path)
    print(f"Finished generate_mathlit_data_handling in {time.time() - t0:.2f}s -> {out_path}")

if __name__ == "__main__":
    generate_mathlit_data_handling()
