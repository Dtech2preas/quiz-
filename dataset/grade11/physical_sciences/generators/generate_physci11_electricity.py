import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from physci11_common import process_physci11_topic

def generate_physci11_electricity():
    print("Generating Grade 11 Physical Sciences: Electrostatics & Electric Circuits...")
    process_physci11_topic("paper1_physci11_electricity.json", "PS11_P1_ELE", "Electrostatics and Electric Circuits", "paper1")

if __name__ == "__main__":
    generate_physci11_electricity()
