import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from techsci_common import process_techsci_topic

def generate_techsci_work_energy():
    print("Generating Grade 12 Technical Sciences: Work, Energy & Power...")
    process_techsci_topic("paper1_work_energy_and_power.json", "TS_P1_WEP", "Work, Energy and Power")

if __name__ == "__main__":
    generate_techsci_work_energy()
