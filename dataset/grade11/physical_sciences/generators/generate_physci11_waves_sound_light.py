import os
import sys

cur_dir = os.path.dirname(__file__)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from physci11_common import process_physci11_topic

def generate_physci11_waves_sound_light():
    print("Generating Grade 11 Physical Sciences: Geometrical Optics & Waves...")
    process_physci11_topic("paper1_physci11_waves_sound_light.json", "PS11_P1_WAV", "Geometrical Optics and Waves", "paper1")

if __name__ == "__main__":
    generate_physci11_waves_sound_light()
