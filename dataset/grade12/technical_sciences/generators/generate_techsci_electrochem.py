import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from techsci_common import process_techsci_topic

def generate_techsci_electrochem():
    print("Generating Grade 12 Technical Sciences: Electrochemistry...")
    process_techsci_topic("paper2_electrochemistry.json", "TS_P2_CHEM", "Electrochemistry")

if __name__ == "__main__":
    generate_techsci_electrochem()
