import json
import glob
import collections

files = glob.glob("dataset/grade12/life_sciences/*.json")

report = {}
for f in files:
    with open(f, 'r') as fp:
        data = json.load(fp)

    diff_counts = collections.Counter(item['difficulty'] for item in data)
    family_counts = collections.Counter(item.get('question', '').split()[0] for item in data)

    # Just grab a sample to show the variety
    samples = [item['question'] for item in data[:3]]

    report[f] = {
        'total': len(data),
        'diffs': dict(diff_counts),
        'variety_hint': len(family_counts),
        'samples': samples
    }

print(json.dumps(report, indent=2))
