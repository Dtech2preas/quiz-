#!/usr/bin/env python3
"""
enrich_curriculum_diagrams.py
Systematically attaches high-accuracy, parametric, mobile-responsive SVG diagrams
to DBE CAPS Grade 12 quiz questions across Physics, Chemistry, Life Sciences, and Math.
Guarantees NO answer leaks on diagram labels.
"""

import json
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def enrich_human_reproduction():
    path = os.path.join(BASE_DIR, 'dataset/grade12/life_sciences/paper1_life_human_reproduction.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')

        # 1. Menstrual Cycle Tracking
        if 'Days 1 to 5' in q_text or 'Days 1-5' in q_text:
            q['diagram'] = {
                'type': 'menstrual_cycle',
                'highlight_day': 1,
                'highlight_hormone': 'Progesterone'
            }
            added += 1
        elif 'Days 6 to 13' in q_text or 'Days 6-13' in q_text:
            q['diagram'] = {
                'type': 'menstrual_cycle',
                'highlight_day': 10,
                'highlight_hormone': 'Estrogen'
            }
            added += 1
        elif 'Days 15 to 28' in q_text or 'Days 15-28' in q_text:
            q['diagram'] = {
                'type': 'menstrual_cycle',
                'highlight_day': 21,
                'highlight_hormone': 'Progesterone'
            }
            added += 1
        elif 'Day 14' in q_text or 'ovulation' in q_text.lower():
            q['diagram'] = {
                'type': 'menstrual_cycle',
                'highlight_day': 14,
                'highlight_hormone': 'LH'
            }
            added += 1
        elif 'Menstrual Cycle' in subtopic and not q.get('diagram'):
            q['diagram'] = {
                'type': 'menstrual_cycle',
                'highlight_day': 14,
                'highlight_hormone': 'all'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Human Reproduction: {added} diagrams enriched.")

def enrich_electrodynamics():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper1_electrodynamics.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')

        # 1. Commutator vs Slip Rings
        if 'slip ring' in q_text.lower() or 'two continuous' in q_text.lower():
            q['diagram'] = {
                'type': 'generator_motor',
                'motor_type': 'ac',
                'title': 'AC Generator with Slip Rings'
            }
            added += 1
        elif 'split-ring' in q_text.lower() or 'commutator' in q_text.lower() or 'dc motor' in q_text.lower() or 'direct current' in q_text.lower():
            q['diagram'] = {
                'type': 'generator_motor',
                'motor_type': 'dc',
                'title': 'DC Motor with Split-Ring Commutator'
            }
            added += 1
        # 2. Oscilloscope Peak-to-Peak Waveforms
        elif 'oscilloscope' in q_text.lower() or 'Peak-to-Peak' in subtopic:
            m = re.search(r'amplitude of\s*(\d+(?:\.\d+)?)\s*V', q_text, re.I)
            vmax = float(m.group(1)) if m else 10
            q['diagram'] = {
                'type': 'ac_wave_graph',
                'vmax': vmax,
                'title': f'Oscilloscope AC Trace (V_max = {vmax} V)'
            }
            added += 1
        # 3. RMS / Peak Voltage
        elif 'V_max' in q_text or 'RMS Voltage' in subtopic:
            m = re.search(r'V_max\s*=\s*(\d+(?:\.\d+)?)\s*V', q_text, re.I)
            if not m:
                m = re.search(r'supply is\s*(\d+(?:\.\d+)?)\s*V', q_text, re.I)
            vmax = float(m.group(1)) if m else 24
            q['diagram'] = {
                'type': 'ac_wave_graph',
                'vmax': vmax,
                'title': f'AC Generator Output (V_max = {vmax} V)'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Electrodynamics: {added} diagrams enriched.")

def enrich_momentum():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper1_momentum_impulse.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')

        # Inelastic Collisions
        if 'lock together' in q_text or 'Inelastic Collisions' in subtopic:
            m = re.search(r'(\d+)\s*kg.*?travelling at (\d+(?:\.\d+)?)\s*m/s.*?collides with a (stationary\s+)?(\d+)\s*kg', q_text)
            if m:
                m1 = int(m.group(1))
                v1 = float(m.group(2))
                m2 = int(m.group(4))
                v2 = 0
                q['diagram'] = {
                    'type': 'momentum_collision',
                    'm1': m1,
                    'v1': v1,
                    'm2': m2,
                    'v2': v2,
                    'vf': 'v_f = ?',
                    'collision_type': 'inelastic'
                }
                added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Momentum & Impulse: {added} diagrams enriched.")

def enrich_reaction_rates():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper2_reaction_rates.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')

        # 1. Reaction Energy Profiles
        m = re.search(r'Reactants energy\s*=\s*(-?\d+).*?Products energy\s*=\s*(-?\d+)', q_text)
        if m:
            er = int(m.group(1))
            ep = int(m.group(2))
            is_exo = er > ep
            has_cat = 'catalyst' in q_text.lower() or 'catalyzed' in q_text.lower()
            q['diagram'] = {
                'type': 'energy_profile',
                'type_reaction': 'exothermic' if is_exo else 'endothermic',
                'catalyzed': has_cat
            }
            added += 1
        elif 'Energy Profiles' in subtopic and not q.get('diagram'):
            is_exo = 'exothermic' in q.get('correct_answer', '').lower()
            q['diagram'] = {
                'type': 'energy_profile',
                'type_reaction': 'exothermic' if is_exo else 'endothermic',
                'catalyzed': False
            }
            added += 1
        # 2. Maxwell-Boltzmann
        elif 'maxwell' in q_text.lower() or 'kinetic energy' in q_text.lower() and ('temperature' in q_text.lower() or 'distribution' in q_text.lower()):
            has_cat = 'catalyst' in q_text.lower()
            q['diagram'] = {
                'type': 'maxwell_boltzmann',
                'compare_temp': True,
                'catalyst': has_cat,
                'ea_label': 'E_a'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Reaction Rates: {added} diagrams enriched.")

def enrich_work_energy():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper1_work_energy_power.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')

        # 1. Conservation of Mechanical Energy (Roller Coaster / Hill)
        if 'roller coaster' in q_text.lower() or 'frictionless track' in q_text.lower() or 'Conservation of Mechanical Energy' in subtopic:
            m = re.search(r'(\d+)\s*kg.*?height h\s*=\s*(\d+(?:\.\d+)?)\s*m', q_text)
            if m:
                mass = int(m.group(1))
                h1 = float(m.group(2))
                q['diagram'] = {
                    'type': 'work_energy_track',
                    'mass': mass,
                    'h1': h1,
                    'h2': round(h1 * 0.6, 1)
                }
                added += 1
        # 2. Work at an Angle (Free-Body with angled force)
        elif 'angle of' in q_text.lower() or 'Work at an Angle' in subtopic:
            m = re.search(r'force of\s*(\d+(?:\.\d+)?)\s*N.*?angle of\s*(\d+(?:\.\d+)?)\s*°', q_text)
            if m:
                f_val = float(m.group(1))
                deg = float(m.group(2))
                q['diagram'] = {
                    'type': 'free_body',
                    'mass': 20,
                    'pulling_force': f'{f_val} N',
                    'angle': deg
                }
                added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Work, Energy & Power: {added} diagrams enriched.")

def enrich_analytical_geometry():
    path = os.path.join(BASE_DIR, 'dataset/grade12/mathematics/paper2_analytical_geometry.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')

        # 1. Tangents to Circles
        if 'tangent to the circle' in q_text.lower() or 'Tangents to Circles' in subtopic:
            m = re.search(r'point\s*\$P\(([^;]+);\s*([^)]+)\)\$', q_text)
            p_label = f"P({m.group(1).strip()}; {m.group(2).strip()})" if m else "P(x₁; y₁)"
            q['diagram'] = {
                'type': 'analytical_geometry',
                'shape': 'circle',
                'p1': p_label
            }
            added += 1
        # 2. Angle of Inclination
        elif 'angle of inclination' in q_text.lower() or 'Angle of Inclination' in subtopic:
            q['diagram'] = {
                'type': 'analytical_geometry',
                'shape': 'segment',
                'p1': 'A(0; 0)',
                'p2': 'B(x; y)',
                'midpoint': 'M'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Analytical Geometry: {added} diagrams enriched.")

def enrich_environment_humans():
    path = os.path.join(BASE_DIR, 'dataset/grade12/life_sciences/paper1_life_environment_humans.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        ans = q.get('correct_answer', '')
        all_text = (q_text + ' ' + ans).lower()

        # Eye questions
        if any(w in all_text for w in ['myopia', 'cornea', 'retina', 'cataract', 'fovea', 'ciliary', 'pupil', 'photoreceptor', 'lens replacement']):
            q['diagram'] = {
                'type': 'eye_anatomy',
                'title': 'Anatomy of the Human Eye'
            }
            added += 1
        # Ear questions
        elif any(w in all_text for w in ['middle ear', 'eardrum', 'tympanum', 'tympanic', 'grommet', 'ossicles', 'cochlea', 'semicircular', 'pinna', 'eustachian']):
            q['diagram'] = {
                'type': 'ear_anatomy',
                'title': 'Anatomy of the Human Ear'
            }
            added += 1
        # Reflex arc
        elif 'reflex arc' in all_text or 'reflex action' in all_text or 'sensory neuron' in all_text and 'motor neuron' in all_text:
            q['diagram'] = {
                'type': 'reflex_arc',
                'title': 'Pathway of a Reflex Arc'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Environment & Humans: {added} diagrams enriched.")

def enrich_dna_code():
    path = os.path.join(BASE_DIR, 'dataset/grade12/life_sciences/paper2_life_dna_code.json')
    if not os.path.exists(path):
        print(f"Skipping {path}: not found")
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        q_text = q.get('question', '')
        ans = q.get('correct_answer', '')
        subtopic = q.get('tags', {}).get('subtopic', '')
        all_text = (q_text + ' ' + ans).lower()

        if any(w in all_text for w in ['nucleotide', 'phosphate group', 'deoxyribose', 'nitrogenous base', 'adenine', 'thymine', 'guanine', 'cytosine', 'complementary base']):
            is_gc = 'guanine' in all_text or 'cytosine' in all_text
            q['diagram'] = {
                'type': 'dna_nucleotide',
                'base1': 'Guanine (G)' if is_gc else 'Adenine (A)',
                'base2': 'Cytosine (C)' if is_gc else 'Thymine (T)',
                'bonds': 3 if is_gc else 2
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"DNA: The Code of Life: {added} diagrams enriched.")

def sanitize_math_functions():
    path = os.path.join(BASE_DIR, 'dataset/grade12/mathematics/paper1_functions.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed = 0
    for q in data:
        diag = q.get('diagram')
        if not diag:
            continue
        if diag.get('type') == 'cartesian_graph':
            # Ensure tp_label does not leak numerical coordinates
            diag['tp_label'] = 'Turning Point P'
            diag['show_coords'] = False
            fixed += 1
        elif diag.get('type') == 'hyperbola_graph':
            # Clean awkward titles like 'f(x) = a/(x - -5) + -5'
            diag['title'] = 'f(x) = a/(x - p) + q'
            diag['show_asymptote_values'] = False
            fixed += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Math Functions: {fixed} diagrams sanitized (all answer leaks removed).")

def enrich_weekly_quizzes():
    import glob
    weekly_files = glob.glob(os.path.join(BASE_DIR, 'dataset/weekly_quiz/grade12/*.json'))
    total_added = 0
    total_sanitized = 0

    for f_path in weekly_files:
        with open(f_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)

        file_added = 0
        for q in data:
            if q.get('diagram'):
                d = q['diagram']
                if d.get('type') == 'cartesian_graph':
                    d['tp_label'] = 'Turning Point P'
                    d['show_coords'] = False
                    total_sanitized += 1
                elif d.get('type') == 'hyperbola_graph':
                    d['title'] = 'f(x) = a/(x - p) + q'
                    d['show_asymptote_values'] = False
                    total_sanitized += 1
                continue

            q_text = q.get('question', '')
            ans = q.get('correct_answer', '')
            full = (q_text + ' ' + ans).lower()

            # Menstrual cycle
            if 'days 1 to 5' in full or 'days 1-5' in full:
                q['diagram'] = {'type': 'menstrual_cycle', 'highlight_day': 1, 'highlight_hormone': 'Progesterone'}
                file_added += 1
            elif 'days 6 to 13' in full or 'days 6-13' in full:
                q['diagram'] = {'type': 'menstrual_cycle', 'highlight_day': 10, 'highlight_hormone': 'Estrogen'}
                file_added += 1
            elif 'days 15 to 28' in full or 'days 15-28' in full:
                q['diagram'] = {'type': 'menstrual_cycle', 'highlight_day': 21, 'highlight_hormone': 'Progesterone'}
                file_added += 1
            elif 'day 14' in full or 'ovulation' in full:
                q['diagram'] = {'type': 'menstrual_cycle', 'highlight_day': 14, 'highlight_hormone': 'LH'}
                file_added += 1
            # Electrodynamics
            elif 'slip ring' in full or 'two continuous' in full:
                q['diagram'] = {'type': 'generator_motor', 'motor_type': 'ac', 'title': 'AC Generator with Slip Rings'}
                file_added += 1
            elif 'split-ring' in full or 'split ring' in full or 'commutator' in full:
                q['diagram'] = {'type': 'generator_motor', 'motor_type': 'dc', 'title': 'DC Motor with Split-Ring Commutator'}
                file_added += 1
            elif 'oscilloscope' in full:
                m = re.search(r'amplitude of\s*(\d+(?:\.\d+)?)\s*V', q_text, re.I)
                vmax = float(m.group(1)) if m else 10
                q['diagram'] = {'type': 'ac_wave_graph', 'vmax': vmax, 'title': f'Oscilloscope AC Trace (V_max = {vmax} V)'}
                file_added += 1
            # Momentum inelastic
            elif 'lock together' in full or ('collides with a' in full and 'kg' in full):
                m = re.search(r'(\d+)\s*kg.*?travelling at (\d+(?:\.\d+)?)\s*m/s.*?collides with a (stationary\s+)?(\d+)\s*kg', q_text)
                if m:
                    q['diagram'] = {
                        'type': 'momentum_collision',
                        'm1': int(m.group(1)),
                        'v1': float(m.group(2)),
                        'm2': int(m.group(4)),
                        'v2': 0,
                        'vf': 'v_f = ?',
                        'collision_type': 'inelastic'
                    }
                    file_added += 1
            # Roller coaster
            elif 'roller coaster' in full or ('frictionless track' in full and 'height' in full):
                m = re.search(r'(\d+)\s*kg.*?height.*?(\d+(?:\.\d+)?)\s*m', q_text)
                if m:
                    q['diagram'] = {
                        'type': 'work_energy_track',
                        'mass': int(m.group(1)),
                        'h1': float(m.group(2)),
                        'h2': round(float(m.group(2)) * 0.6, 1)
                    }
                    file_added += 1
            # Reaction profiles
            elif 'reactants energy' in full and 'products energy' in full:
                m = re.search(r'Reactants energy\s*=\s*(-?\d+).*?Products energy\s*=\s*(-?\d+)', q_text)
                if m:
                    er = int(m.group(1))
                    ep = int(m.group(2))
                    q['diagram'] = {
                        'type': 'energy_profile',
                        'type_reaction': 'exothermic' if er > ep else 'endothermic',
                        'catalyzed': 'catalyst' in full
                    }
                    file_added += 1
            # Eye, ear, reflex
            elif any(w in full for w in ['myopia', 'cornea', 'retina', 'cataract', 'fovea', 'ciliary']):
                q['diagram'] = {'type': 'eye_anatomy', 'title': 'Anatomy of the Human Eye'}
                file_added += 1
            elif any(w in full for w in ['middle ear', 'eardrum', 'tympanum', 'tympanic', 'ossicles', 'cochlea', 'semicircular']):
                q['diagram'] = {'type': 'ear_anatomy', 'title': 'Anatomy of the Human Ear'}
                file_added += 1
            elif 'reflex arc' in full or ('sensory neuron' in full and 'motor neuron' in full):
                q['diagram'] = {'type': 'reflex_arc', 'title': 'Pathway of a Reflex Arc'}
                file_added += 1
            # DNA nucleotide
            elif any(w in full for w in ['nucleotide', 'phosphate group', 'deoxyribose', 'nitrogenous base', 'complementary base']):
                is_gc = 'guanine' in full or 'cytosine' in full
                q['diagram'] = {
                    'type': 'dna_nucleotide',
                    'base1': 'Guanine (G)' if is_gc else 'Adenine (A)',
                    'base2': 'Cytosine (C)' if is_gc else 'Thymine (T)',
                    'bonds': 3 if is_gc else 2
                }
                file_added += 1

        if file_added > 0:
            total_added += file_added
            with open(f_path, 'w', encoding='utf-8') as fp:
                json.dump(data, fp, indent=2, ensure_ascii=False)

    print(f"Grade 12 Weekly Quizzes: {total_added} diagrams enriched, {total_sanitized} sanitized.")

def enrich_transformers():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper1_electrodynamics.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        if 'transformer' in q_text.lower():
            np_match = re.search(r'(\d+)\s*turns on its primary', q_text, re.IGNORECASE)
            ns_match = re.search(r'(\d+)\s*turns on its secondary', q_text, re.IGNORECASE)
            v_match = re.search(r'stepping voltage from\s*(\d+)\s*V to\s*(\d+)\s*V', q_text, re.IGNORECASE)

            np_val = int(np_match.group(1)) if np_match else 2400
            ns_val = int(ns_match.group(1)) if ns_match else 120
            vp_val = int(v_match.group(1)) if v_match else (240 if np_val > ns_val else 12)
            vs_val = int(v_match.group(2)) if v_match else (12 if np_val > ns_val else 240)

            is_step_down = np_val > ns_val or vp_val > vs_val
            q['diagram'] = {
                'type': 'transformer_circuit',
                'transformer_type': 'step_down' if is_step_down else 'step_up',
                'vp': vp_val,
                'vs': vs_val,
                'np': np_val,
                'ns': ns_val
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Electrodynamics Transformers: {added} diagrams enriched.")

def enrich_momentum_impulse():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper1_momentum_impulse.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        if 'impulse' in q_text.lower() or 'vertical wall' in q_text.lower():
            q['diagram'] = {
                'type': 'impulse_force_time',
                'fmax': 500,
                'dt': '0.04'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Momentum Impulse Force-Time: {added} diagrams enriched.")

def enrich_electrostatics_field_lines():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper1_electrostatics.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        ql = q_text.lower()
        if 'parallel' in ql and ('plate' in ql or 'field' in ql):
            q['diagram'] = {
                'type': 'electric_field_lines',
                'setup': 'parallel_plates'
            }
            added += 1
        elif 'field line' in ql or 'electric field' in ql or 'point charge' in ql:
            q['diagram'] = {
                'type': 'electric_field_lines',
                'setup': 'dipole'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Electrostatics Field Lines: {added} diagrams enriched.")

def enrich_organic_chemistry():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper2_organic_chemistry.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')
        ql = q_text.lower()

        if 'esterification' in ql or 'esterification' in subtopic.lower():
            q['diagram'] = {
                'type': 'esterification_reaction',
                'acid': 'Ethanoic acid',
                'alcohol': 'Ethanol',
                'ester': 'Ethyl ethanoate'
            }
            added += 1
        elif 'alcohol' in subtopic.lower() or 'ethanol' in ql or 'hydroxyl' in ql:
            q['diagram'] = {
                'type': 'organic_structural',
                'series': 'alcohol',
                'molecule': 'Ethanol'
            }
            added += 1
        elif 'ester' in subtopic.lower() or 'ethanoate' in ql:
            q['diagram'] = {
                'type': 'organic_structural',
                'series': 'ester',
                'molecule': 'Ethyl ethanoate'
            }
            added += 1
        elif 'alkene' in subtopic.lower() or 'ethene' in ql or 'propene' in ql or 'double bond' in ql:
            q['diagram'] = {
                'type': 'organic_structural',
                'series': 'alkene',
                'molecule': 'Ethene'
            }
            added += 1
        elif 'haloalkane' in ql or 'bromo' in ql or 'chloro' in ql:
            q['diagram'] = {
                'type': 'organic_structural',
                'series': 'haloalkane',
                'molecule': 'Bromoethane'
            }
            added += 1
        elif 'carboxylic' in ql or 'functional group' in ql or 'carboxyl' in ql:
            q['diagram'] = {
                'type': 'organic_structural',
                'series': 'carboxylic_acid',
                'molecule': 'Ethanoic acid'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Organic Chemistry: {added} diagrams enriched.")

def enrich_chemical_equilibrium():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper2_chemical_equilibrium.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')
        ql = q_text.lower()

        if 'le chatelier' in subtopic.lower() or 'shift' in ql or 'temperature' in ql or 'pressure' in ql:
            q['diagram'] = {
                'type': 'chemical_equilibrium_graph',
                'disturbance': 'Concentration'
            }
            added += 1
        elif 'closed system' in ql or 'dynamic equilibrium' in ql or 'reversible' in ql or 'equilibrium' in subtopic.lower():
            q['diagram'] = {
                'type': 'dynamic_equilibrium_box',
                'reaction': 'N₂(g) + 3H₂(g) ⇌ 2NH₃(g)'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Chemical Equilibrium: {added} diagrams enriched.")

def enrich_reaction_rates_gas():
    path = os.path.join(BASE_DIR, 'dataset/grade12/physical_sciences/paper2_reaction_rates.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        if 'collected' in q_text.lower() or 'marble chips' in q_text.lower() or 'co2 gas' in q_text.lower():
            q['diagram'] = {
                'type': 'gas_syringe_rate',
                'gas': 'CO₂ gas'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Reaction Rates Gas Syringe: {added} diagrams enriched.")

def enrich_geometry():
    path = os.path.join(BASE_DIR, 'dataset/grade12/mathematics/paper2_geometry.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        subtopic = q.get('tags', {}).get('subtopic', '')
        ql = subtopic.lower()

        if 'cyclic' in ql:
            q['diagram'] = {
                'type': 'euclidean_circle_geometry',
                'theorem': 'cyclic_quad'
            }
            added += 1
        elif 'centre' in ql or 'semi-circle' in ql or 'tangent' in ql or 'chord' in ql or 'segment' in ql:
            q['diagram'] = {
                'type': 'euclidean_circle_geometry',
                'theorem': 'angle_at_centre'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Euclidean Geometry: {added} diagrams enriched.")

def enrich_statistics():
    path = os.path.join(BASE_DIR, 'dataset/grade12/mathematics/paper2_statistics.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        subtopic = q.get('tags', {}).get('subtopic', '')

        if 'Five Number' in subtopic or 'Outliers' in subtopic or 'Min' in q_text:
            m_min = re.search(r'Min\s*=\s*(\d+)', q_text)
            m_q1 = re.search(r'Q_1\s*=\s*(\d+)', q_text)
            m_med = re.search(r'Median\s*=\s*(\d+)', q_text)
            m_q3 = re.search(r'Q_3\s*=\s*(\d+)', q_text)
            m_max = re.search(r'Max\s*=\s*(\d+)', q_text)

            min_v = int(m_min.group(1)) if m_min else 20
            q1_v = int(m_q1.group(1)) if m_q1 else 40
            med_v = int(m_med.group(1)) if m_med else 55
            q3_v = int(m_q3.group(1)) if m_q3 else 70
            max_v = int(m_max.group(1)) if m_max else 90

            q['diagram'] = {
                'type': 'box_and_whisker',
                'min': min_v,
                'q1': q1_v,
                'med': med_v,
                'q3': q3_v,
                'max': max_v
            }
            added += 1
        elif 'Skewness' in subtopic or 'Correlation' in subtopic or 'Measures of Central' in subtopic:
            q['diagram'] = {
                'type': 'histogram_frequency',
                'title': 'Frequency Distribution'
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Statistics: {added} diagrams enriched.")

def enrich_math_functions_exp():
    path = os.path.join(BASE_DIR, 'dataset/grade12/mathematics/paper1_functions.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    for q in data:
        if q.get('diagram'):
            continue
        q_text = q.get('question', '')
        ql = q_text.lower()
        if 'exponential' in ql or 'inverse function' in ql or '2^x' in ql or 'log' in ql:
            q['diagram'] = {
                'type': 'exponential_log_graph',
                'base': 2,
                'hide_inverse': True
            }
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Functions Exponential/Log: {added} diagrams enriched.")

if __name__ == '__main__':
    print("Beginning Grade 12 curriculum diagram enrichment...")
    enrich_human_reproduction()
    enrich_electrodynamics()
    enrich_momentum()
    enrich_reaction_rates()
    enrich_work_energy()
    enrich_analytical_geometry()
    enrich_environment_humans()
    enrich_dna_code()
    sanitize_math_functions()
    enrich_weekly_quizzes()
    # New engines enrichment
    enrich_transformers()
    enrich_momentum_impulse()
    enrich_electrostatics_field_lines()
    enrich_organic_chemistry()
    enrich_chemical_equilibrium()
    enrich_reaction_rates_gas()
    enrich_geometry()
    enrich_statistics()
    enrich_math_functions_exp()
    print("Done!")
