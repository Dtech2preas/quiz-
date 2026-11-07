import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

root_dir = os.path.abspath(os.path.join(cur_dir, "../../../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import generate_mathlit11
from mathlit11_common import run_mathlit11_generator

def generate_mathlit11_data_handling():
    run_mathlit11_generator(
        gen_func=generate_mathlit11.generate_data_questions,
        filename="paper1_mathlit11_data_handling.json",
        prefix="ML11_P1_DATA",
        topic_name="Data Handling",
        paper="paper1"
    )

if __name__ == "__main__":
    generate_mathlit11_data_handling()
