import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from math11_common import process_math11_topic

def generate_math11_trigonometry():
    process_math11_topic("paper2_math11_trigonometry.json", "MATH11_P2_TRIG", "Trigonometry", "paper2")

if __name__ == "__main__":
    generate_math11_trigonometry()
