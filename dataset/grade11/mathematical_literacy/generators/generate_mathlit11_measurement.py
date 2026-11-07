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

def generate_mathlit11_measurement():
    run_mathlit11_generator(
        gen_func=generate_mathlit11.generate_measurement_questions,
        filename="paper2_mathlit11_measurement.json",
        prefix="ML11_P2_MEAS",
        topic_name="Measurement",
        paper="paper2"
    )

if __name__ == "__main__":
    generate_mathlit11_measurement()
