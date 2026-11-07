import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from techsci_common import process_techsci_topic

def generate_techsci_newtons_laws():
    print("Generating Grade 12 Technical Sciences: Newton's Laws...")
    process_techsci_topic("paper1_newtons_laws.json", "TS_P1_NEWT", "Newton's Laws")

if __name__ == "__main__":
    generate_techsci_newtons_laws()
