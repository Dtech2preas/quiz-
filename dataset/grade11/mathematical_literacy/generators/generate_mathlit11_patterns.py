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

def generate_mathlit11_patterns():
    run_mathlit11_generator(
        gen_func=generate_mathlit11.generate_algebra_questions,
        filename="paper1_mathlit11_patterns.json",
        prefix="ML11_P1_PAT",
        topic_name="Patterns and Relationships",
        paper="paper1"
    )

if __name__ == "__main__":
    generate_mathlit11_patterns()
