import json
import os

for f in os.listdir('dataset'):
    if f.startswith('paper'):
        with open(os.path.join('dataset', f)) as file:
            data = json.load(file)
            easy = sum(1 for q in data if q['difficulty'] == 'easy')
            medium = sum(1 for q in data if q['difficulty'] == 'medium')
            hard = sum(1 for q in data if q['difficulty'] == 'hard')
            print(f"{f}: {len(data)} questions, easy={easy}, medium={medium}, hard={hard}")
