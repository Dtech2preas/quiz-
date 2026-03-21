import json
import glob

files = glob.glob('dataset/grade11/agricultural_sciences/*.json')
for f in files:
    with open(f, 'r') as fp:
        data = json.load(fp)
    print(f"{f}: {len(data)} questions")
