import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from physci11_common import process_physci11_topic

def generate_physci11_energy_change():
    print("Generating Grade 11 Physical Sciences: Energy & Chemical Change...")
    process_physci11_topic("paper2_physci11_energy_change.json", "PS11_P2_ENE", "Energy and Chemical Change", "paper2")

if __name__ == "__main__":
    generate_physci11_energy_change()
