import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from techsci_common import process_techsci_topic

def generate_techsci_electromagnetism():
    print("Generating Grade 12 Technical Sciences: Electromagnetism...")
    process_techsci_topic("paper1_electromagnetism.json", "TS_P1_MAG", "Electromagnetism")

if __name__ == "__main__":
    generate_techsci_electromagnetism()
