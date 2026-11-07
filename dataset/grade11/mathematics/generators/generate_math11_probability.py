import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from math11_common import process_math11_topic

def generate_math11_probability():
    process_math11_topic("paper1_math11_probability.json", "MATH11_P1_PROB", "Probability", "paper1")

if __name__ == "__main__":
    generate_math11_probability()
