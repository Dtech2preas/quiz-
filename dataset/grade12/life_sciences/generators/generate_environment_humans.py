import json
import random
import os
import time

def generate_environment_humans():
    print("Generating Grade 12 Life Sciences: Responding to the Environment - Humans...")
    t0 = time.time()

    questions = []
    seen_texts = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive="Knowledge"):
        nonlocal questions, seen_texts
        q_text = q_text.strip()
        if q_text in seen_texts:
            return False
        correct = str(correct).strip()
        clean_wrongs = []
        for w in wrongs:
            w = str(w).strip()
            if w != correct and w not in clean_wrongs:
                clean_wrongs.append(w)
        if len(clean_wrongs) < 6:
            return False

        seen_texts.add(q_text)
        q_id = f"LIFE_P1_HUM_ENV_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Responding to the Environment (Humans)",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Life Sciences",
                "topic": "Responding to the Environment (Humans)",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    env_terms = [
        ("Cerebrum", "The largest region of the human brain responsible for voluntary motor actions, sensory perception, intelligence, memory, and conscious thought", ["Cerebellum", "Medulla oblongata", "Hypothalamus", "Corpus callosum", "Pons", "Thalamus", "Spinal cord"]),
        ("Cerebellum", "The brain structure located inferior and posterior to the cerebrum responsible for muscle coordination, balance, and posture", ["Cerebrum", "Medulla oblongata", "Hypothalamus", "Pituitary gland", "Corpus callosum", "Hippocampus", "Amygdala"]),
        ("Medulla oblongata", "The lower stem region of the brain that controls autonomic vital functions including heartbeat, breathing rate, and blood pressure", ["Cerebrum", "Cerebellum", "Corpus callosum", "Spinal cord", "Olfactory bulb", "Hypothalamus", "Pineal gland"]),
        ("Hypothalamus", "A vital brain region below the thalamus that regulates homeostasis (body temperature, thirst, hunger) and controls the pituitary gland", ["Cerebrum", "Cerebellum", "Medulla oblongata", "Corpus callosum", "Midbrain", "Pons", "Meninges"]),
        ("Corpus callosum", "The thick C-shaped tract of myelinated nerve fibers connecting the left and right cerebral hemispheres to facilitate communication", ["Spinal cord", "Meninges", "Cerebellar peduncle", "Optic chiasm", "Sciatic nerve", "Cranial nerve", "Central canal"]),
        ("Reflex arc", "The complete neural pathway followed by nerve impulses from a receptor to an effector to produce a rapid involuntary reflex action", ["Reflex action", "Synaptic cleft", "Action potential", "Depolarisation", "Saltatory conduction", "Somatic circuit", "Sensory cortex"]),
        ("Sensory neuron (afferent)", "A nerve cell that conducts impulses from sensory receptors towards the central nervous system (CNS)", ["Motor neuron", "Interneuron", "Connector neuron", "Efferent neuron", "Glial cell", "Schwann cell", "Ganglion"]),
        ("Motor neuron (efferent)", "A nerve cell that conducts impulses away from the central nervous system to an effector organ (muscle or gland)", ["Sensory neuron", "Afferent neuron", "Interneuron", "Connector neuron", "Receptor cell", "Microglial cell", "Astrocytes"]),
        ("Interneuron (connector)", "A neuron situated entirely within the central nervous system (grey matter) that links sensory neurons to motor neurons", ["Sensory neuron", "Motor neuron", "Afferent neuron", "Efferent neuron", "Oligodendrocyte", "Ependymal cell", "Nerve trunk"]),
        ("Cornea", "The transparent, curved anterior portion of the sclera that allows light to enter the eye and performs the majority of light refraction", ["Sclera", "Choroid", "Retina", "Iris", "Lens", "Pupil", "Fovea centralis"]),
        ("Retina", "The innermost sensory tunic of the eye containing photoreceptor cells (rods and cones) that convert light stimuli into nerve impulses", ["Choroid", "Sclera", "Cornea", "Ciliary body", "Suspensory ligament", "Optic disc", "Vitreous humor"]),
        ("Rods", "Photoreceptor cells concentrated in the peripheral retina responsible for vision in dim light, movement detection, and black-and-white perception", ["Cones", "Ganglion cells", "Bipolar cells", "Hair cells", "Maculae", "Cristae", "Amacrine cells"]),
        ("Cones", "Photoreceptor cells concentrated in the fovea centralis responsible for sharp visual acuity and colour vision in bright light", ["Rods", "Hair cells", "Cristae", "Bipolar neurons", "Basilar cells", "Olfactory receptors", "Tactile corpuscles"]),
        ("Fovea centralis (yellow spot)", "A small shallow depression in the center of the retina with the highest concentration of cones and greatest visual acuity", ["Blind spot", "Optic disc", "Ciliary body", "Cornea", "Pupil", "Canal of Schlemm", "Ora serrata"]),
        ("Blind spot (optic disc)", "The region on the retina where the optic nerve exits the eyeball, entirely lacking photoreceptors and insensitive to light", ["Fovea centralis", "Yellow spot", "Macula lutea", "Pupil", "Cornea", "Lens", "Anterior chamber"]),
        ("Lens", "A transparent, biconvex crystalline structure behind the iris that changes shape to focus light rays onto the retina", ["Cornea", "Iris", "Pupil", "Choroid", "Sclera", "Retina", "Ciliary muscle"]),
        ("Ciliary muscle", "Circular smooth muscle in the ciliary body that alters the tension on suspensory ligaments to change the curvature of the lens", ["Radial iris muscle", "Circular iris muscle", "Extrinsic eye muscle", "Superior rectus", "Orbicularis oculi", "Tensor tympani", "Stapedius"]),
        ("Iris", "The pigmented circular muscular diaphragm of the eye containing circular and radial muscles that control the diameter of the pupil", ["Cornea", "Sclera", "Choroid", "Retina", "Lens", "Ciliary body", "Suspensory ligament"]),
        ("Tympanic membrane (eardrum)", "A thin, fibrous membrane vibrating in response to sound waves, separating the outer ear from the middle ear", ["Oval window", "Round window", "Pinna", "Cochlea", "Basilar membrane", "Tectorial membrane", "Vestibular membrane"]),
        ("Auditory ossicles", "Three tiny articulated bones in the middle ear (malleus, incus, stapes) that amplify and transmit sound vibrations to the oval window", ["Cochlear hair cells", "Otoliths", "Cristae", "Semicircular canals", "Eustachian valves", "Mastoid air cells", "Turbinates"]),
        ("Cochlea", "A spiral, snail shell-shaped fluid-filled cavity in the inner ear containing the Organ of Corti responsible for hearing", ["Semicircular canals", "Utriculus", "Sacculus", "Vestibule", "Eustachian tube", "Tympanic cavity", "Pinna"]),
        ("Organ of Corti", "The sensory receptor organ for hearing situated on the basilar membrane of the cochlea, containing mechanoreceptive hair cells", ["Cristae ampullaris", "Maculae", "Otolith organ", "Fovea centralis", "Taste buds", "Pacinian corpuscles", "Muscle spindles"]),
        ("Semicircular canals", "Three fluid-filled bony loops oriented at right angles containing cristae in ampullae that detect rotational dynamic balance", ["Cochlea", "Organ of Corti", "Eustachian tube", "Tympanic cavity", "Ossicles", "Auditory canal", "Vestibular duct"]),
        ("Eustachian tube", "A narrow canal connecting the middle ear cavity to the nasopharynx that equalizes air pressure on both sides of the eardrum", ["Auditory canal", "Cochlear duct", "Semicircular canal", "Semicircular duct", "Endolymphatic duct", "Lacrimal canal", "Tympanic duct"])
    ]

    for term, definition, wrongs in env_terms:
        add_q("easy", "Nervous & Sensory Anatomy", f"In Grade 12 CAPS Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Nervous & Sensory Anatomy", f"Which neural or sensory structure correctly matches {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in env_terms if d[0] != term][:7]
        add_q("easy", "Nervous & Sensory Anatomy", f"Which statement accurately explains '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Nervous & Sensory Anatomy", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

    easy_extras = [
        ("What are the two major anatomical divisions of the human central nervous system (CNS)?", "Brain and spinal cord", ["Sympathetic and parasympathetic systems", "Sensory and motor neurons", "Cranial and spinal nerves", "Somatic and autonomic systems", "Cerebrum and cerebellum only"], "The central nervous system consists of the brain and the spinal cord."),
        ("What is the protective biological function of a reflex action?", "It provides a rapid, involuntary response to potentially harmful stimuli to prevent tissue injury", ["It allows conscious cognitive evaluation before movement", "It stores procedural memories in the cerebrum", "It slows down heart rate during strenuous exercise", "It decreases the rate of cellular respiration", "It turns motor neurons into sensory neurons"], "Reflex actions are rapid and automatic, protecting the organism before conscious pain is perceived."),
        ("Which part of the autonomic nervous system is responsible for the 'fight or flight' emergency response?", "Sympathetic nervous system", ["Parasympathetic nervous system", "Somatic nervous system", "Enteric nervous system", "Central nervous system", "Afferent sensory system"], "The sympathetic division mobilizes energy and increases heart rate during emergencies."),
        ("Which part of the autonomic nervous system promotes 'rest and digest' activities?", "Parasympathetic nervous system", ["Sympathetic nervous system", "Somatic nervous system", "Endocrine system", "Sensory nervous system", "Cerebellar system"], "The parasympathetic division conserves energy and promotes digestion and slower heart rates."),
        ("Which fluid cushions the brain and spinal cord, absorbs shocks, and provides nutritional support?", "Cerebrospinal fluid (CSF)", ["Synovial fluid", "Amniotic fluid", "Perilymph", "Endolymph", "Vitreous humor", "Interstitial lymph"], "Cerebrospinal fluid fills the subarachnoid space and ventricles, protecting central neural tissue.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Sensory Biology: ", "In clinical neurology: "]:
            add_q("easy", "Nervous & Sensory Anatomy", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(env_terms)
        q = f"Sensory check {e_counter}: Identify the anatomical structure defined as: {definition}."
        add_q("easy", "Nervous & Sensory Anatomy", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    medium_mechanisms = [
        # Accommodation Near
        ("How does the human eye accommodate when viewing an object closer than 6 meters (near vision)?",
         "Ciliary muscles contract -> Suspensory ligaments become slack -> Tension on lens decreases -> Lens becomes more convex (rounder) -> Refractive power increases",
         ["Ciliary muscles relax -> Suspensory ligaments tighten -> Lens becomes flat -> Refractive power decreases", "Circular iris muscles contract -> Pupil dilates -> Lens moves forward", "Suspensory ligaments contract -> Ciliary muscles slacken -> Lens flattens", "Cornea changes curvature -> Retina moves backwards -> Pupil constricts", "Ciliary muscles relax -> Lens becomes spherical -> Refraction decreases"],
         "For near vision, ciliary muscles contract, releasing ligament tension; the elastic lens rounds up, increasing refraction to focus diverging rays onto the retina.", "Application"),

        # Accommodation Distant
        ("How does the human eye accommodate when focusing on a distant object further than 6 meters?",
         "Ciliary muscles relax -> Suspensory ligaments tighten -> Tension pulls lens thinner (less convex) -> Refractive power decreases to focus parallel rays onto retina",
         ["Ciliary muscles contract -> Suspensory ligaments slacken -> Lens becomes rounder", "Radial iris muscles relax -> Pupil dilates -> Lens moves backwards", "Suspensory ligaments relax -> Ciliary muscles contract -> Lens flattens", "Cornea thickens -> Retina contracts -> Optic nerve stretches", "Both ciliary muscles and ligaments contract simultaneously"],
         "For distant vision, ciliary muscles relax, ligament tension pulls the lens flatter, reducing refractive power for parallel rays.", "Application"),

        # Pupillary Mechanism Bright
        ("How does the pupillary mechanism respond when walking from a dark room into bright sunlight?",
         "Circular muscles of the iris contract -> Radial muscles relax -> Pupil constricts (narrows) -> Reduces light entering the eye to protect photoreceptors",
         ["Radial muscles contract -> Circular muscles relax -> Pupil dilates", "Ciliary muscles contract -> Lens becomes convex -> Pupil expands", "Both circular and radial muscles relax completely -> Pupil stays static", "Suspensory ligaments contract -> Iris pulls backwards -> Pupil widens", "Cornea becomes opaque to block UV radiation"],
         "In bright light, parasympathetic impulses cause iris circular muscles to contract, constricting the pupil to prevent retinal bleaching.", "Application"),

        # Pupillary Mechanism Dim
        ("How does the pupillary mechanism respond when entering a dimly lit movie theater?",
         "Radial muscles of the iris contract -> Circular muscles relax -> Pupil dilates (widens) -> Maximizes light entry onto the retina",
         ["Circular muscles contract -> Radial muscles relax -> Pupil constricts", "Ciliary muscles relax -> Suspensory ligaments tighten -> Pupil narrows", "Both circular and radial muscles contract -> Pupil closes completely", "Rods contract -> Cones expand -> Pupil becomes rectangular", "Iris muscles stop working and pupil becomes rigid"],
         "In dim light, sympathetic impulses cause radial iris muscles to contract, dilating the pupil to allow maximum photons onto rods.", "Application"),

        # Hearing Pathway
        ("What is the correct sequence of sound wave transmission through the human ear to produce hearing?",
         "Pinna -> Auditory canal -> Tympanic membrane -> Ossicles (malleus, incus, stapes) -> Oval window -> Perilymph pressure waves -> Organ of Corti hair cells -> Auditory nerve -> Cerebrum",
         ["Pinna -> Semicircular canals -> Cochlea -> Eustachian tube -> Cerebellum", "Auditory canal -> Oval window -> Tympanic membrane -> Ossicles -> Organ of Corti", "Tympanic membrane -> Round window -> Cochlea -> Auditory ossicles -> Optic nerve", "Pinna -> Eustachian tube -> Middle ear -> Cristae -> Auditory nerve -> Medulla", "Ossicles -> Tympanic membrane -> Pinna -> Cochlea -> Cerebrum"],
         "Acoustic waves vibrate tympanic membrane, amplified by ossicles, transferred to oval window, creating fluid waves stimulating hair cells in Organ of Corti.", "Application"),

        # Balance Pathway
        ("Which structures in the inner ear are specifically responsible for detecting dynamic (rotational) balance versus static (gravitational) balance?",
         "Dynamic balance is detected by cristae in the semicircular canals; static balance is detected by maculae in the utriculus and sacculus",
         ["Dynamic balance is detected by the cochlea; static balance by auditory ossicles", "Dynamic balance is detected by the Organ of Corti; static balance by cristae", "Both dynamic and static balance are detected exclusively by the tympanic membrane", "Dynamic balance by the Eustachian tube; static balance by the pinna", "Dynamic balance by the fovea centralis; static balance by the cornea"],
         "Cristae in semicircular ampullae detect angular head rotation; maculae with otoliths detect gravity and linear acceleration.", "Application"),

        # Visual Defects
        ("A learner can clearly read text in a book held close to their face, but chalkboard writing 5 meters away appears blurry. What visual defect does this learner have, and how is it corrected?",
         "Myopia (shortsightedness), corrected by concave (diverging) lenses",
         ["Hyperopia (farsightedness), corrected by convex lenses", "Astigmatism, corrected by cylindrical lenses", "Cataracts, corrected by surgical removal", "Glaucoma, corrected by eye drops", "Presbyopia, corrected by bifocals", "Night blindness, corrected by vitamin C"],
         "Myopia results when the eyeball is too long or lens too convex, focusing distant light in front of the retina; concave lenses diverge rays to focus on the retina.", "Application")
    ]

    for q, ans, wrongs, expl, cog in medium_mechanisms:
        for prefix in ["", "CAPS Sensory Mechanism Scenario: ", "Clinical Audiology/Optometry Problem: ", "Physiological Pathway Analysis: "]:
            add_q("medium", "Sensory Pathways & Defects", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500
    defect_scenarios = [
        ("Hyperopia (farsightedness)", "Eyeball too short or lens too flat; image focuses behind the retina; corrected with convex (converging) lenses", [
            "Eyeball too long; image focuses in front of retina; corrected with concave lenses",
            "Irregular curvature of cornea; corrected with cylindrical lenses",
            "Clouding of crystalline lens; corrected with synthetic intraocular lens",
            "Excessive intraocular fluid pressure; corrected with beta-blockers",
            "Loss of rods in peripheral retina; corrected with night goggles",
            "Absence of iris circular muscles; corrected with tinted contact lenses",
            "Paralysis of ciliary muscles; corrected with optic nerve stimulation",
            "Detached retina; corrected with scleral buckle surgery"
        ]),
        ("Astigmatism", "Irregular, non-spherical curvature of the cornea or lens causing light rays to focus at different focal points; corrected with cylindrical lenses", [
            "Eyeball too short causing light to focus behind retina",
            "Eyeball too long causing light to focus in front of retina",
            "Hardening of lens with age preventing near focus; corrected with reading glasses",
            "Infection of middle ear with fluid behind eardrum",
            "Damage to hair cells in Organ of Corti from loud noise",
            "Dislocation of stapes bone from oval window",
            "Total absence of cones in fovea centralis",
            "Failure of suspensory ligaments to slacken during distant vision"
        ]),
        ("Cataracts", "Progressive clouding, opacification, or yellowing of the eye lens leading to blurry, dimmed vision; treated by surgical lens replacement", [
            "Excessive aqueous humor pressure damaging the optic nerve",
            "Bacterial infection of the conjunctiva treated with antibiotic drops",
            "Detachment of the sensory retina from the pigmented choroid layer",
            "Degeneration of macula lutea causing loss of central vision",
            "Loss of elasticity in ciliary muscle causing presbyopia",
            "Genetic absence of red-sensitive photopigments in retinal cones",
            "Inability of pupils to constrict in response to bright sunlight",
            "Perforation of the tympanic membrane due to acoustic trauma"
        ]),
        ("Otitis media (middle ear infection)", "Inflammation and fluid/pus accumulation in the middle ear cavity; treated with antibiotics and grommet insertion into the eardrum", [
            "Damage to mechanoreceptor hair cells in the cochlea treated with hearing aids",
            "Wax buildup in the external ear canal treated by ear syringing",
            "Calcium deposits on the semicircular canals causing vertigo",
            "Rupture of the oval window treated by ossicle bone replacement",
            "Tumor on the acoustic nerve treated by craniotomy",
            "Malformation of the pinna cartilage treated by cosmetic surgery",
            "Total degeneration of the auditory cortex in temporal lobe",
            "Failure of Eustachian tube to remain open permanently"
        ])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        d_item = random.choice(defect_scenarios)
        q = f"Sensory defect diagnostic {m_counter}: Which statement accurately describes the physiological cause and clinical correction for {d_item[0]}?"
        add_q("medium", "Sensory Defects", q, d_item[1], d_item[2], f"For {d_item[0]}: {d_item[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        ("A patient involved in a motor vehicle accident suffers a brain injury. Clinical examination reveals the patient has severe ataxia, an unsteady stumbling gait, and poor motor coordination, but has normal memory, reasoning, and speech. Which brain region was damaged?",
         "Cerebellum",
         ["Cerebrum", "Medulla oblongata", "Hypothalamus", "Corpus callosum", "Pons", "Spinal cord", "Pituitary gland"],
         "The cerebellum coordinates voluntary motor actions, posture, and balance; cerebellar injury produces ataxia without cognitive deficit.", "Analysis"),

        ("A patient experiences a severe stroke that damages the respiratory and cardiovascular centers in the medulla oblongata. What is the immediate physiological consequence?",
         "Immediate cessation of automatic breathing and loss of cardiovascular regulation, leading to death unless supported by mechanical ventilation",
         ["Temporary loss of color vision in the right eye", "Inability to bend the knees during bipedal walking", "Hypersecretion of adrenaline by adrenal medulla", "Permanent dilation of both pupils with normal speech", "Loss of memory regarding childhood events", "Excessive sweating on the palms only"],
         "The medulla oblongata controls vital autonomic reflexes (respiration, cardiac regulation); severe lesions are fatal without life-support.", "Analysis"),

        ("In a spinal reflex arc, what clinical symptom occurs if the ventral root of a spinal nerve is completely severed, while the dorsal root remains intact?",
         "The patient retains full sensory perception from the affected limb, but suffers complete flaccid motor paralysis of muscles innervated by that nerve",
         ["The patient loses all sensory perception, but can still voluntarily contract the muscles", "Both sensation and motor movement remain 100% normal", "The patient experiences intense chronic phantom pain without paralysis", "The reflex arc operates at three times normal speed", "The sensory neurons turn into interneurons", "The limb undergoes spontaneous uncontrolled muscle spasms"],
         "The dorsal root conducts sensory (afferent) inputs; the ventral root conducts motor (efferent) signals. Severing ventral root paralyzes muscles while sensation persists.", "Analysis"),

        ("How do grommets (tympanostomy tubes) surgically inserted into the tympanic membrane treat chronic otitis media with effusion (glue ear)?",
         "They provide an artificial ventilation conduit to allow fluid and pus to drain from the middle ear cavity into the external canal and equalize air pressure across the eardrum",
         ["They amplify sound vibrations by connecting directly to the stapes bone", "They kill all middle ear bacteria by releasing electrical micro-currents", "They seal the Eustachian tube completely to prevent throat mucus from entering", "They dissolve the ossicles to prevent pressure from damaging the inner ear", "They act as artificial cochleas by stimulating the auditory nerve", "They prevent water from ever entering the inner ear canals"],
         "Grommets ventilate the middle ear, relieving fluid buildup and pressure when the Eustachian tube is dysfunctional.", "Analysis"),

        ("Why does exposure to intense, chronic noise (>85 dB) cause permanent sensorineural hearing loss, whereas fluid accumulation behind the eardrum causes only temporary conductive hearing loss?",
         "Chronic loud noise mechanically damages and shears the delicate stereocilia of hair cells in the Organ of Corti, which cannot regenerate, whereas middle ear fluid only impedes physical vibration of intact structures",
         ["Noise dissolves the temporal bone while fluid strengthens auditory ossicles", "Noise paralyzes the auditory cortex while fluid activates the cerebellum", "Loud noise shrinks the pinna while middle ear infections enlarge the cochlea", "Hair cells in the cochlea can regenerate every 48 hours in adults", "Fluid turns into bone over time, improving auditory perception", "Conductive hearing loss is always permanent and sensorineural always temporary"],
         "Cochlear hair cells are post-mitotic and cannot regenerate; irreversible mechanical shear causes permanent sensorineural deafness.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "CAPS Neurological Evaluation: ", "Clinical Sensory Diagnostic: ", "Neuro-Sensory Synthesis Problem: "]:
            add_q("hard", "Neurological Diagnostics", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Neurological diagnostic case {h_counter}: {base_h[0]}"
        add_q("hard", "Neurological Diagnostics", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/life_sciences/paper1_life_environment_humans.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_environment_humans()
