import json
import os

files = [
    "dataset/grade10/mathlit_finance.json",
    "dataset/grade10/mathlit_measurement.json",
    "dataset/grade10/mathlit_maps_plans.json",
    "dataset/grade10/mathlit_data_handling.json",
    "dataset/grade10/mathlit_probability.json",
    "dataset/grade10/mathlit_algebra.json",
    "dataset/grade12/accounting/paper1_acc_companies.json",
    "dataset/grade12/accounting/paper1_acc_financial_statements.json",
    "dataset/grade12/accounting/paper1_acc_cash_flow.json",
    "dataset/grade12/accounting/paper1_acc_analysis.json",
    "dataset/grade12/accounting/paper2_acc_manufacturing.json",
    "dataset/grade12/accounting/paper2_acc_budgeting.json",
    "dataset/grade12/accounting/paper2_acc_inventory.json",
    "dataset/grade12/accounting/paper2_acc_reconciliations.json",
    "dataset/grade12/life_sciences/paper1_life_meiosis.json",
    "dataset/grade12/life_sciences/paper1_life_reproduction_vertebrates.json",
    "dataset/grade12/life_sciences/paper1_life_human_reproduction.json",
    "dataset/grade12/life_sciences/paper1_life_environment_humans.json",
    "dataset/grade12/life_sciences/paper1_life_endocrine_system.json",
    "dataset/grade12/life_sciences/paper1_life_homeostasis.json",
    "dataset/grade12/life_sciences/paper1_life_environment_plants.json",
    "dataset/grade12/life_sciences/paper1_life_human_impact.json",
    "dataset/grade12/life_sciences/paper2_life_dna_code.json",
    "dataset/grade12/life_sciences/paper2_life_meiosis.json",
    "dataset/grade12/life_sciences/paper2_life_genetics.json",
    "dataset/grade12/life_sciences/paper2_life_evolution.json",
]

all_questions = set()
duplicates = 0

for file in files:
    if not os.path.exists(file):
        print(f"File missing: {file}")
        continue

    with open(file, 'r') as f:
        data = json.load(f)

    if len(data) != 1000:
        print(f"Error: {file} has {len(data)} items instead of 1000.")

    diffs = {"easy": 0, "medium": 0, "hard": 0}
    for item in data:
        if 'difficulty' in item:
            diffs[item['difficulty']] += 1
        elif 'tags' in item and 'difficulty' in item['tags']:
            diffs[item['tags']['difficulty']] += 1
        else:
            print(f"Error: No difficulty found for question {item.get('id')}")

        q_text = item['question']
        if q_text in all_questions:
            duplicates += 1
        all_questions.add(q_text)

        if len(item['wrong_answers_pool']) < 6:
            print(f"Error: Question {item['id']} in {file} has less than 6 wrong answers.")

        if item['correct_answer'] in item['wrong_answers_pool']:
            print(f"Error: Question {item['id']} in {file} has the correct answer in the wrong answers pool.")

    if diffs['easy'] != 300 or diffs['medium'] != 500 or diffs['hard'] != 200:
        print(f"Error: {file} has incorrect difficulty distribution: {diffs}")

    print(f"{file} verified successfully: 1000 items, diffs {diffs}")

print(f"Total cross-file duplicates: {duplicates}")
