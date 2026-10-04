1. *Generate Paper 1: Electric Circuits*
   - Create `kb_electric_circuits.json` based on the syllabus.
   - Create `generate_electric_circuits.py` script and generate 1000 questions to update `paper1_electric_circuits.json`.
2. *Generate Paper 1: Electrodynamics*
   - Create `kb_electrodynamics.json` based on the syllabus.
   - Create `generate_electrodynamics.py` script and generate 1000 questions to update `paper1_electrodynamics.json`.
3. *Verify datasets and update manifest*
   - Run `python3 verify_datasets.py` to ensure dataset sizes and difficulty distributions are exact.
   - Run `python build_manifest.py` to synchronize updates.
4. *Pre-commit tasks*
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
5. *Submit the changes*
   - Submit the newly generated datasets and the code changes.
