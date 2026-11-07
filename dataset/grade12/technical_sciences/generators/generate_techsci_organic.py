import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from techsci_common import process_techsci_topic

def generate_techsci_organic():
    print("Generating Grade 12 Technical Sciences: Organic Chemistry...")
    process_techsci_topic("paper2_organic_chemistry.json", "TS_P2_ORG", "Organic Chemistry")

if __name__ == "__main__":
    generate_techsci_organic()
