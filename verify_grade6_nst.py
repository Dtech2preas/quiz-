import json
import os

def verify_dataset(filepath, expected_topic, expected_subtopics):
    print(f"Verifying {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if len(data) != 1000:
        print(f"  ERROR: Expected 1000 questions, got {len(data)}")
        return False

    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    unique_questions = set()

    for q in data:
        diff_counts[q["difficulty"]] += 1
        unique_questions.add(q["question"])

        if q["topic"] != expected_topic:
            print(f"  ERROR: Unexpected topic {q['topic']} in {filepath}")
            return False

        if q["subtopic"] not in expected_subtopics:
            print(f"  ERROR: Unexpected subtopic {q['subtopic']} in {filepath}")
            return False

        if len(q["wrong_answers_pool"]) < 6:
            print(f"  ERROR: Not enough wrong answers for question: {q['id']}")
            return False

        if q["correct_answer"] in q["wrong_answers_pool"]:
            print(f"  ERROR: Correct answer found in wrong answers for: {q['id']}")
            return False

        if len(set(q["wrong_answers_pool"])) != len(q["wrong_answers_pool"]):
            print(f"  ERROR: Duplicate wrong answers found for: {q['id']}")
            return False

    if len(unique_questions) != 1000:
        print(f"  ERROR: Found duplicate questions. Unique count: {len(unique_questions)}")
        return False

    if diff_counts["easy"] != 300 or diff_counts["medium"] != 500 or diff_counts["hard"] != 200:
        print(f"  ERROR: Incorrect difficulty distribution. Got: {diff_counts}")
        return False

    print(f"  SUCCESS: {filepath} passed all checks.")
    return True

if __name__ == "__main__":
    base_dir = "dataset/grade6/natural_sciences_and_technology/"

    files_to_check = [
        ("grade6_nst_life_living_processing.json", "Life and Living", ["Photosynthesis", "Nutrients in food", "Nutrition", "Ecosystems and food webs"]),
        ("grade6_nst_matter_materials_processing.json", "Matter and Materials", ["Solids, liquids and gases", "Mixtures", "Solutions as special mixtures", "Dissolving", "Mixtures and water resources", "Processes to purify water"]),
        ("grade6_nst_energy_change_systems_control.json", "Energy and Change", ["Electric circuits", "Electrical conductors and insulators", "Systems to solve problems using circuits", "Mains electricity (including fossil fuels, cost, and renewable energy)"]),
        ("grade6_nst_planet_earth_beyond_systems_control.json", "Planet Earth and Beyond", ["The Solar System", "Movements of the Earth (rotation and revolution)", "Movements of the Moon (rotation and revolution)", "Systems for looking into space (telescopes)", "Systems to explore the Moon and Mars (rovers)"])
    ]

    all_passed = True
    for filename, topic, subtopics in files_to_check:
        filepath = os.path.join(base_dir, filename)
        if not verify_dataset(filepath, topic, subtopics):
            all_passed = False

    if all_passed:
        print("\nAll Grade 6 NST datasets verified successfully!")
    else:
        print("\nSome datasets failed verification.")
        exit(1)
