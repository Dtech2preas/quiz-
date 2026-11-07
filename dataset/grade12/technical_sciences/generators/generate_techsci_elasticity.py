import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from techsci_common import process_techsci_topic

def generate_techsci_elasticity():
    print("Generating Grade 12 Technical Sciences: Elasticity & Hydraulics...")
    process_techsci_topic("paper1_elasticity_and_hydraulics.json", "TS_P1_ELAST", "Elasticity & Hydraulics")

if __name__ == "__main__":
    generate_techsci_elasticity()
