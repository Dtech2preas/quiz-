import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from physci11_common import process_physci11_topic

def generate_physci11_ideal_gases():
    print("Generating Grade 11 Physical Sciences: Ideal Gases & Thermal Properties...")
    process_physci11_topic("paper2_physci11_ideal_gases.json", "PS11_P2_IDE", "Ideal Gases and Thermal Properties", "paper2")

if __name__ == "__main__":
    generate_physci11_ideal_gases()
