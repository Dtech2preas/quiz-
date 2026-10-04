1. *Generate Paper 1: Electrostatics*
   - Create `kb_electrostatics.json` based on the syllabus.
   - Create `generate_electrostatics.py` script and generate 1000 questions to update `paper1_electrostatics.json`.
2. *Generate Paper 1: Doppler Effect*
   - Create `kb_doppler_effect.json` based on the syllabus.
   - Create `generate_doppler_effect.py` script and generate 1000 questions to update `paper1_doppler_effect.json`.
3. *Verify datasets and update manifest*
   - Run `python3 verify_datasets.py` to ensure dataset sizes and difficulty distributions are exact.
   - Run `python build_manifest.py` to synchronize updates.
4. *Pre-commit tasks*
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
5. *Submit the changes*
   - Submit the newly generated datasets and the code changes.
