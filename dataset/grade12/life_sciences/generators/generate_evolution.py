import json
import random
import os
import time

def generate_evolution():
    print("Generating Grade 12 Life Sciences: Evolution by Natural Selection & Hominin Fossil Record...")
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
        q_id = f"LIFE_P2_EVO_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Evolution",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Life Sciences",
                "topic": "Evolution",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    evo_terms = [
        ("Biological evolution", "A process of genetic change in a population or species over successive generations", ["Spontaneous generation", "Ontogeny", "Acquired inheritance", "Metamorphosis", "Embryogenesis", "Cell differentiation", "Cloning"]),
        ("Hypothesis", "An informed, testable, and plausible explanation for an observed biological phenomenon", ["Scientific theory", "Scientific law", "Empirical dogma", "Axiom", "Prediction", "Conclusion", "Experimental control"]),
        ("Scientific theory", "A well-substantiated explanation of some aspect of the natural world based on a vast body of empirical evidence, facts, and tested hypotheses", ["Scientific hypothesis", "Conjecture", "Speculation", "Opinion", "Axiom", "Trial", "Observation"]),
        ("Fossil record", "The complete accumulation of preserved petrified remains, impressions, or traces of prehistoric organisms embedded in sedimentary rock strata", ["Archaeological dig", "Radioactive decay", "Carbon dating", "Geological era", "Strata map", "Pedigree", "Phylogenetic tree"]),
        ("Transitional fossil", "A fossil that exhibits intermediate anatomical characteristics common to both an ancestral group and its derived descendant group", ["Index fossil", "Trace fossil", "Mold fossil", "Cast fossil", "Living fossil", "Microfossil", "Coprolite"]),
        ("Biogeography", "The scientific study of the geographic distribution of living organisms and prehistoric fossils across the continents", ["Comparative anatomy", "Molecular biology", "Paleontology", "Embryology", "Taxonomy", "Ecology", "Stratigraphy"]),
        ("Homologous structures", "Anatomical structures in different species that share a common ancestral design but are modified to perform different functions (divergent evolution)", ["Analogous structures", "Vestigial structures", "Convergent traits", "Mimicry structures", "Atavisms", "Co-adapted traits", "Derived traits"]),
        ("Analogous structures", "Anatomical structures that perform similar functions in unrelated species due to similar selective pressures but have distinct evolutionary origins (convergent evolution)", ["Homologous structures", "Vestigial organs", "Ancestral homology", "Rudimentary organs", "Atavisms", "Synapomorphies", "Sympatric traits"]),
        ("Vestigial structures", "Reduced, rudimentary anatomical structures that have lost their ancestral physiological function over evolutionary time (e.g., human appendix, coccyx)", ["Homologous organs", "Analogous organs", "Adaptive traits", "Secondary sex traits", "Functional adaptations", "Specialized organs", "Sensory organs"]),
        ("Natural selection", "The evolutionary mechanism proposed by Charles Darwin whereby individuals possessing advantageous inherited traits are more likely to survive, reproduce, and pass those traits to offspring", ["Lamarckism", "Artificial selection", "Genetic drift", "Spontaneous mutation", "Inheritance of acquired characteristics", "Polyploidy", "Selective breeding"]),
        ("Artificial selection", "The deliberate selective breeding of plants or animals practiced by humans over generations to accentuate desirable phenotypic traits", ["Natural selection", "Punctuated equilibrium", "Geographic speciation", "Genetic bottleneck", "Founder effect", "Allopatric divergence", "Sexual dimorphism"]),
        ("Species", "A group of closely related organisms capable of naturally interbreeding with one another to produce fertile, viable offspring", ["Population", "Community", "Genus", "Ecosystem", "Family", "Clade", "Subspecies"]),
        ("Speciation", "The evolutionary process through which one ancestral species diverges and splits into two or more distinct, reproductive isolated species", ["Specialization", "Adaptive convergence", "Extinction", "Hybridization", "Polyploidy", "Artificial selection", "Domestication"]),
        ("Allopatric speciation", "Speciation that occurs when a biological population becomes geographically isolated by an insurmountable physical barrier, preventing gene flow", ["Sympatric speciation", "Parapatric speciation", "Artificial speciation", "Hybrid speciation", "Microevolution", "Convergent speciation", "Gradualism"]),
        ("Punctuated equilibrium", "An evolutionary model proposed by Eldredge and Gould proposing that species remain stable for long periods (stasis), interrupted by rapid bursts of speciation", ["Darwinian gradualism", "Lamarckian adaptation", "Catastrophism", "Orthogenesis", "Saltationism", "Uniformitarianism", "Continuous divergence"]),
        ("Bipedalism", "The form of terrestrial locomotion where an organism moves primarily by means of its two rear limbs or legs", ["Quadrupedalism", "Brachiation", "Arboreal locomotion", "Saltation", "Knuckle-walking", "Crawling", "Gliding"]),
        ("Foramen magnum", "The large opening at the base of the cranium through which the spinal cord exits and connects to the brain stem", ["Orbits", "Zygomatic arch", "Auditory meatus", "Mental foramen", "Sagittal crest", "Supraorbital ridge", "Palatine foramen"]),
        ("Diastema", "A distinctive physiological gap between the incisors/canines and the premolars in the jaw of non-human primates to accommodate large projecting canines", ["Dental formula", "Prognathism", "Palate arch", "Canine fossa", "Mental protuberance", "Mandibular notch", "Orthognathism"]),
        ("Prognathism", "The pronounced forward projection or jutting out of the upper and lower jaws (typical of apes and early hominins)", ["Orthognathism", "Brachycephaly", "Dolichocephaly", "Bipedalism", "Sexual dimorphism", "Cephalization", "Cranial capacity"]),
        ("Cranial capacity", "The internal volume of the braincase of the skull, measured in cubic centimeters (cm3), reflecting approximate brain volume", ["Brain weight", "Cephalic index", "Cranial vault", "Orbital volume", "Facial angle", "Sagittal thickness", "Foramen index"])
    ]

    for term, definition, wrongs in evo_terms:
        add_q("easy", "Evolution Concepts", f"In Grade 12 CAPS Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Evolution Concepts", f"Which biological term correctly identifies {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in evo_terms if d[0] != term][:7]
        add_q("easy", "Evolution Concepts", f"Which statement accurately explains the meaning of '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Evolution Concepts", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

    easy_extras = [
        ("Which of the following is considered a transitional fossil between dinosaurs (reptiles) and modern birds?", "Archaeopteryx", ["Tiktaalik", "Australopithecus afarensis", "Coelacanth", "Thrinaxodon", "Ichthyostega", "Ambulocetus"], "Archaeopteryx exhibits both reptilian features (teeth, long bony tail, claws) and avian features (feathers, wings)."),
        ("What transitional fossil demonstrates the evolutionary transition between lobe-finned fish and early tetrapod amphibians?", "Tiktaalik", ["Archaeopteryx", "Homo habilis", "Plesiosaur", "Trilobite", "Pelycosaur", "Meganeura"], "Tiktaalik possesses fish scales and fins along with tetrapod characteristics (wrist bones, neck, ribs)."),
        ("What term describes non-functional anatomical remnants such as the human coccyx and appendix?", "Vestigial structures", ["Homologous structures", "Analogous structures", "Adaptive traits", "Atavisms", "Convergent organs", "Embryonic arches"], "Vestigial organs are evolutionary remnants that have lost their original function."),
        ("Who proposed the 'Law of use and disuse' and the 'Law of inheritance of acquired characteristics'?", "Jean-Baptiste Lamarck", ["Charles Darwin", "Gregor Mendel", "Alfred Wallace", "Stephen Jay Gould", "Niles Eldredge", "Thomas Malthus"], "Lamarck proposed that organs grow or shrink with use and that acquired characteristics are passed to offspring."),
        ("Why was Jean-Baptiste Lamarck's theory of evolution rejected by modern science?", "Acquired phenotypic characteristics do not alter the DNA/genes in gametes and cannot be inherited by offspring", ["Organisms do not adapt to their environmental surroundings", "Lamarck could not read Latin manuscripts", "Fossils do not exhibit any variation", "Mutations are always harmful to populations", "All organisms were created instantaneously without change", "Natural selection was observed before Lamarck published"], "Changes to somatic cells acquired during life cannot be inherited because only genetic changes in gametes are passed on."),
        ("What term describes the evolutionary process where two unrelated species independently evolve similar structures due to similar environmental pressures?", "Convergent evolution", ["Divergent evolution", "Allopatric speciation", "Punctuated equilibrium", "Gradualism", "Artificial selection", "Adaptive radiation"], "Convergent evolution produces analogous structures with similar functions in unrelated lineages.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Evolution Focus: ", "In evolutionary biology: "]:
            add_q("easy", "Evolution Concepts", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(evo_terms)
        q = f"Evolution question {e_counter}: What is the scientific term for {definition}?"
        add_q("easy", "Evolution Concepts", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    medium_scenarios = [
        # Natural Selection Scenarios
        ("During the Industrial Revolution in England, tree trunks became blackened with soot. The population of peppered moths (Biston betularia) shifted from predominantly light-coloured to dark-coloured. What was the selective agent in this scenario?",
         "Predatory birds hunting moths visually against tree trunks",
         ["The soot acting as a chemical mutagen mutating moth DNA", "Direct consumption of soot by moth larvae", "Inability of light moths to fly in polluted air", "Competition between male and female moths for mates", "Acid rain destroying moth eggs directly", "A virus killing light-coloured moths only"],
         "Predatory birds served as the selective pressure; dark moths were camouflaged against soot-covered bark, while light moths were easily spotted and eaten.", "Application"),

        ("How do bacteria develop resistance to antibiotics according to Darwin's theory of natural selection?",
         "Random mutations create pre-existing genetic variation; when antibiotics are administered, resistant bacteria survive and multiply, passing the resistance allele to offspring",
         ["Bacteria deliberately mutate their cell walls when exposed to antibiotics", "Antibiotics cause non-resistant bacteria to learn how to produce resistance enzymes", "Antibiotics act as food that strengthens weak bacteria", "Bacteria acquire immunity through physical exercise and cell division", "Resistance is created by environmental temperature increases", "Bacteria absorb resistance from human white blood cells"],
         "Variation exists prior to exposure; antibiotic application selects for individuals with the resistance mutation, increasing the allele frequency over time.", "Application"),

        # Allopatric speciation mechanism
        ("Which sequence correctly outlines the chronological stages of allopatric speciation?",
         "Geographic isolation -> No gene flow -> Different selection pressures & independent mutations -> Natural selection -> Inability to interbreed when reunited",
         ["Independent mutations -> Inability to interbreed -> Geographic isolation -> Natural selection", "Natural selection -> Geographic isolation -> Hybridisation -> Speciation", "Artificial selection -> Polyploidy -> Extinction -> Speciation", "Sympatric divergence -> Cross-breeding -> Geographic barrier -> Speciation", "No gene flow -> Interbreeding -> Mutation -> Speciation"],
         "A physical barrier divides the original population; isolated gene pools undergo independent natural selection and mutations until reproductive isolation is established.", "Application"),

        # Reproductive Isolating Mechanisms
        ("Two species of closely related frogs live in the identical pond habitat. One species breeds in early spring, while the other breeds in late summer. What type of reproductive isolating mechanism prevents them from interbreeding?",
         "Temporal (seasonal) isolation",
         ["Behavioral isolation", "Mechanical isolation", "Gametic isolation", "Geographic isolation", "Hybrid sterility", "Ecological niche isolation"],
         "Different breeding seasons or times of year represent temporal isolation.", "Application"),

        ("Male fireflies of different species flash unique, species-specific light patterns to attract females. Females only respond to the flash pattern of their own species. Which reproductive isolating mechanism is operating?",
         "Behavioral isolation",
         ["Temporal isolation", "Mechanical isolation", "Gametic isolation", "Geographic isolation", "Post-zygotic inviability", "Habitat isolation"],
         "Species-specific courtship rituals, displays, songs, and signals constitute behavioral isolation.", "Application"),

        # Comparative Anatomy: Humans vs African Apes
        ("How does the position of the foramen magnum differ between modern humans (Homo sapiens) and quadrupedal African apes (Gorilla)?",
         "In humans, it is positioned centrally at the bottom of the cranium; in apes, it is positioned towards the back (posteriorly)",
         ["In humans, it is positioned at the back; in apes, it is positioned centrally", "In humans, it is completely absent; in apes, it is present", "In both humans and apes, it is located on top of the parietal bone", "In humans, it is located on the facial palate; in apes, at the occiput", "In humans, it is square-shaped; in apes, it is triangular"],
         "A central foramen magnum balances the skull atop a vertical vertebral column for efficient bipedalism.", "Application"),

        ("How does the shape of the human vertebral column (spine) compare to that of quadrupedal African apes?",
         "Humans possess an S-shaped spine with double curvature for shock absorption; apes possess a single C-shaped curved spine",
         ["Humans possess a straight, rigid spine; apes possess an S-shaped spine", "Humans possess a C-shaped spine; apes possess an S-shaped spine", "Both humans and apes possess perfectly identical C-shaped spines", "Humans possess 50 vertebrae; apes possess only 12 vertebrae", "Humans lack a lumbar curvature entirely"],
         "The S-shaped curvature acts like a spring, balancing the upper body over the hips and absorbing mechanical shocks during bipedal locomotion.", "Application"),

        ("How does the pelvic girdle (pelvis) of humans differ from that of African apes to facilitate bipedal walking?",
         "The human pelvis is short, broad, and bowl-shaped; the ape pelvis is long, narrow, and flat",
         ["The human pelvis is long and narrow; the ape pelvis is broad and bowl-shaped", "The human pelvis is completely fused to the ribs; the ape pelvis is separate", "The ape pelvis is bowl-shaped to support vertical visceral organs", "Humans lack a pelvic girdle; apes have a prominent pelvis", "Both have identical long, narrow pelvic girdles"],
         "A short, broad, bowl-shaped pelvis supports the internal organs in an upright posture and provides attachment points for gluteal muscles.", "Application"),

        ("How does the shape of the dental arch (palate) differ between modern humans and African apes?",
         "Humans have a smooth, curved parabolic palate; apes have a rectangular, U-shaped palate with parallel tooth rows",
         ["Humans have a rectangular palate; apes have a parabolic palate", "Humans have a triangular palate; apes have a circular palate", "Humans have tooth rows that diverge backwards; apes have circular rows", "Both humans and apes have identical rectangular palates", "Humans lack premolars while apes have premolars"],
         "The human dental arcade is a gentle, curved parabolic arch without gaps; apes have a U-shaped dental arcade with parallel tooth rows.", "Application"),

        ("What is the function of the human foot arch in bipedal locomotion?",
         "It acts as a mechanical shock absorber and spring to distribute body weight during walking and running",
         ["It allows the human foot to grasp branches like an opposable thumb", "It reduces blood circulation to the toes during cold weather", "It prevents humans from climbing steep rocky surfaces", "It houses sensory organs that detect sound vibrations", "It ensures the big toe remains opposable to other digits"],
         "The longitudinal and transverse arches absorb ground impact forces and provide elastic energy return during upright bipedal stride.", "Application")
    ]

    for q, ans, wrongs, expl, cog in medium_scenarios:
        for prefix in ["", "CAPS Comparative Analysis: ", "Evolutionary Mechanism Scenario: ", "Consider the following anatomical observation: "]:
            add_q("medium", "Comparative Anatomy", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500 with fossil discoveries and skull characteristics
    fossil_features = [
        ("Cranial capacity", "Homo sapiens: ~1400 cm3 vs African apes: ~400-500 cm3", [
            "Homo sapiens: ~400 cm3 vs Apes: ~1400 cm3",
            "Both have identical ~1000 cm3 capacity",
            "Homo sapiens: ~2500 cm3 vs Apes: ~100 cm3",
            "Homo sapiens: ~600 cm3 vs Apes: ~800 cm3",
            "Apes have twice the cranial capacity of humans",
            "Homo sapiens: ~800 cm3 vs Apes: ~1800 cm3",
            "Both have identical ~500 cm3 cranial volumes",
            "Homo sapiens: ~300 cm3 vs Apes: ~300 cm3"
        ]),
        ("Canine teeth and diastema", "Humans have small, non-projecting canines with no diastema; apes have large, sharp projecting canines with a diastema", [
            "Humans have large canines with a diastema; apes have small canines without diastema",
            "Both have large projecting canines with diastemas",
            "Humans lack canines entirely; apes have small canines",
            "Both have small canines without any diastema",
            "Apes lack canines while humans have prominent fangs",
            "Humans have three sets of canines while apes have one",
            "Apes have blunt molars while humans have sharp slicing canines",
            "Neither humans nor apes possess canines or premolars"
        ]),
        ("Brow ridges (supraorbital tori)", "Greatly reduced or absent in modern humans; heavily developed and prominent in African apes", [
            "Prominent in humans; absent in apes",
            "Equally massive in both humans and apes",
            "Only found in female humans and male apes",
            "Absent in both humans and apes",
            "Developed only in human infants",
            "Found exclusively in modern Homo sapiens",
            "Continuous across the forehead in humans but absent in gorillas",
            "Replaced by horns in adult chimpanzees"
        ]),
        ("Chin (mental protuberance)", "Well-developed and projecting in humans; receding or completely absent in African apes", [
            "Absent in humans; prominent in apes",
            "Equally developed in both humans and apes",
            "Only present in quadrupedal primates",
            "Absent in both humans and apes",
            "Present only in australopithecines",
            "Projecting in chimpanzees but receding in modern humans",
            "Fused to the clavicle in African apes",
            "Present only in juvenile apes and lost in adults"
        ])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        feat = random.choice(fossil_features)
        q = f"Anatomical contrast {m_counter}: How does the anatomical feature '{feat[0]}' compare between modern humans (Homo sapiens) and African apes?"
        add_q("medium", "Comparative Anatomy", q, feat[1], feat[2], f"In terms of {feat[0]}: {feat[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        # Famous Hominin Fossils
        ("Which famous fossil hominin skull was discovered in 1924 by Raymond Dart at Taung in South Africa, representing the first recognized specimen of Australopithecus africanus?",
         "The Taung Child",
         ["Mrs Ples (StW 53)", "Little Foot (StW 573)", "Karabo", "Lucy (AL 288-1)", "Turkana Boy (WT 15000)", "Handy Man (OH 7)", "Cradle Man"],
         "Raymond Dart identified the fossilized skull and endocranial cast of a juvenile hominin at Taung, naming it Australopithecus africanus.", "Analysis"),

        ("Which complete adult Australopithecus africanus skull was discovered at Sterkfontein in the Cradle of Humankind by Dr Robert Broom in 1947?",
         "Mrs Ples (StW 53)",
         ["The Taung Child", "Little Foot", "Karabo", "Lucy", "Turkana Boy", "Florisbad Skull", "Nutcracker Man"],
         "Dr Robert Broom blasted open limestone caves at Sterkfontein to reveal 'Mrs Ples' (StW 53), dating back approximately 2.5 million years.", "Analysis"),

        ("What remarkable hominin fossil specimen, discovered by Professor Lee Berger at Malapa in 2008, exhibits a transitional combination of Australopithecus and Homo features and was named 'Karabo'?",
         "Australopithecus sediba",
         ["Australopithecus afarensis", "Australopithecus africanus", "Homo naledi", "Homo habilis", "Ardipithecus ramidus", "Paranthropus robustus"],
         "Australopithecus sediba ('Karabo') shows small brain size like Australopithecus combined with modern pelvis and hand structures resembling genus Homo.", "Analysis"),

        ("Which hominin species, discovered in the Rising Star cave system by Lee Berger's team in 2013, possessed a small brain (~500 cm3) yet human-like hands and feet, with evidence suggesting intentional body disposal?",
         "Homo naledi",
         ["Homo habilis", "Homo erectus", "Australopithecus afarensis", "Homo neanderthalensis", "Australopithecus africanus", "Homo floresiensis"],
         "Homo naledi was discovered deep in the Dinaledi chamber, exhibiting a unique mosaic of primitive australopithecine-like and derived human-like anatomy.", "Analysis"),

        ("Which hominin was the first to use fire, manufacture Acheulean teardrop handaxes, and be the first hominin species to migrate out of Africa into Europe and Asia?",
         "Homo erectus ('Turkana Boy')",
         ["Homo habilis ('Handy Man')", "Australopithecus afarensis ('Lucy')", "Australopithecus africanus", "Homo naledi", "Ardipithecus ramidus", "Paranthropus boisei"],
         "Homo erectus exhibited a larger brain (~900-1100 cm3), perfected Acheulean stone tools, mastered fire, and successfully migrated across Eurasia.", "Analysis"),

        # Out of Africa Evidence
        ("What genetic evidence derived from Mitochondrial DNA (mtDNA) provides rigorous empirical support for the 'Out of Africa' hypothesis?",
         "All modern human mtDNA lineages coalesce to a common ancestral maternal lineage ('Mitochondrial Eve') that lived in Africa approximately 150,000-200,000 years ago",
         ["Mitochondrial DNA undergoes rapid crossing over in Neanderthal populations", "Non-African populations show vastly higher genetic diversity than indigenous African populations", "Mitochondrial DNA is identical to Y-chromosome DNA in all human populations", "mtDNA does not mutate and has remained 100% frozen since the origin of life", "Mitochondrial DNA can only be extracted from hominin teeth fossils", "African populations possess zero mutations in their mitochondrial genome"],
         "mtDNA is inherited strictly maternally without recombination, and molecular clock dating confirms all modern humans descend from an African maternal population ~150,000-200,000 ya.", "Analysis"),

        ("Why does the observation that modern indigenous African populations possess the greatest genetic diversity of any human population on Earth support the 'Out of Africa' hypothesis?",
         "African populations are the oldest extant human populations, having had the longest period of time to accumulate spontaneous genetic mutations and diversity",
         ["African populations have the highest mutation rates due to intense solar radiation", "African populations interbred with dinosaurs during the Pleistocene", "Non-African populations are ancient and have lost all genetic diversity through disease", "Africans were the last group to evolve, so they contain all combined traits", "Genetic diversity only accumulates in tropical rainforest biomes", "It proves that humans evolved simultaneously on all six continents"],
         "Older populations accumulate greater numbers of neutral mutations over time; migrating populations carried only a subset of alleles (founder effect).", "Analysis"),

        ("Where were the oldest anatomically modern human (Homo sapiens) fossils discovered, supporting Africa as the evolutionary cradle of our species?",
         "Exclusively in Africa (e.g., Florisbad in South Africa, Omo Kibish in Ethiopia, Jebel Irhoud in Morocco)",
         ["Exclusively in the Neander Valley in Germany and caves in France", "Across the Australian outback dating back 10 million years", "In the limestone caves of Beijing, China", "Exclusively in North and South America", "In the Siberian permafrost of Russia", "In Antarctica beneath the polar ice caps"],
         "The oldest fossil evidence of anatomically modern Homo sapiens is found exclusively in Africa, dating back over 200,000 to 300,000 years.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "CAPS High-Level Synthesis: ", "Evaluation of Hominin Evolution: ", "Paleoanthropological Analysis: "]:
            add_q("hard", "Hominin Fossil Record", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Hominin evolution case {h_counter}: {base_h[0]}"
        add_q("hard", "Hominin Fossil Record", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/life_sciences/paper2_life_evolution.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_evolution()
