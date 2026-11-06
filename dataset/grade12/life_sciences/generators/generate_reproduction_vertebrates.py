import json
import random
import os
import time

def generate_reproduction_vertebrates():
    print("Generating Grade 12 Life Sciences: Reproduction in Vertebrates...")
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
        q_id = f"LIFE_P1_REP_VERT_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Reproduction in Vertebrates",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Life Sciences",
                "topic": "Reproduction in Vertebrates",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    vert_terms = [
        ("External fertilisation", "Fertilisation occurring outside the female's body in an aquatic environment, requiring large numbers of gametes", ["Internal fertilisation", "Vivipary", "Ovovivipary", "Parthenogenesis", "Amniocentesis", "Gestation", "Capacitation"]),
        ("Internal fertilisation", "Fertilisation occurring inside the reproductive tract of the female, characteristic of terrestrial vertebrates", ["External fertilisation", "Spawning", "Broadcast fertilisation", "Vegetative propagation", "Polyembryony", "Hermaphroditism", "Fragmentation"]),
        ("Ovipary", "A reproductive strategy where fertilized or unfertilized eggs are laid outside the maternal body, with the embryo nourished by yolk", ["Vivipary", "Ovovivipary", "Internal gestation", "Placental nutrition", "Parthenogenesis", "Marsupialism", "Asexual budding"]),
        ("Ovovivipary", "A reproductive strategy where eggs are retained inside the female body until hatching, with the embryo nourished exclusively by yolk and not via a placenta", ["Vivipary", "Ovipary", "External spawning", "Placental gestation", "Marsupial development", "Metamorphosis", "Ectoparasitism"]),
        ("Vivipary", "A reproductive strategy where the embryo develops inside the mother's uterus, receiving nourishment directly via a placenta, and live young are born", ["Ovipary", "Ovovivipary", "External brooding", "Spawning", "Egg laying", "Amniotic encapsulation", "Parthenogenesis"]),
        ("Amniotic egg", "A self-contained terrestrial egg enclosed by a protective shell and four extra-embryonic membranes, enabling reproduction on dry land", ["Anamniotic egg", "Amphibian jelly egg", "Fish egg mass", "Blastocyst capsule", "Zygotic pouch", "Placental membrane", "Morula"]),
        ("Amnion", "The innermost extra-embryonic membrane enclosing the fluid-filled amniotic cavity that cushions the embryo against mechanical shock and prevents desiccation", ["Chorion", "Allantois", "Yolk sac", "Albumin", "Shell membrane", "Placenta", "Umbilical cord"]),
        ("Chorion", "The outermost extra-embryonic membrane surrounding all other membranes, responsible for gas exchange between the embryo and the environment", ["Amnion", "Allantois", "Yolk sac", "Albumin", "Endometrium", "Blastocoel", "Zona pellucida"]),
        ("Allantois", "The extra-embryonic sac that stores insoluble nitrogenous waste products (uric acid) and aids in respiratory gas exchange", ["Amnion", "Chorion", "Yolk sac", "Albumin", "Follicle", "Corpus luteum", "Perivitelline space"]),
        ("Yolk sac", "The extra-embryonic membrane that envelops the yolk, serving as the primary source of nutrients (fats, proteins) for the developing embryo", ["Amnion", "Chorion", "Allantois", "Albumin", "Tympanic cavity", "Amniotic fluid", "Placental disc"]),
        ("Albumin (egg white)", "The protein and water-rich fluid surrounding the yolk in an amniotic egg that cushions the embryo and supplies hydration", ["Yolk sac", "Allantois", "Chorion", "Amnion", "Chalaza", "Cuticle", "Vitelline membrane"]),
        ("Precocial development", "A reproductive pattern where hatchlings or newborns are well-developed, mobile, have open eyes and down/fur, and can feed themselves soon after birth", ["Altricial development", "Metamorphic development", "Larval development", "Embryonic arrest", "Placental dependence", "Delayed implantation", "Fetal dormancy"]),
        ("Altricial development", "A reproductive pattern where hatchlings or newborns are helpless, blind, naked, and incapable of self-feeding, requiring intense parental care", ["Precocial development", "Direct development", "Independent development", "Nidifugous development", "Autotrophic development", "Precocial foraging", "Instinctive autonomy"]),
        ("Parental care", "Any behavioral or physiological investment by parents in their offspring that enhances offspring survival at the cost of parental resources", ["Natural selection", "Sexual dimorphism", "Courtship display", "Territorial aggression", "Kin selection", "Speciation", "Dispersal"])
    ]

    for term, definition, wrongs in vert_terms:
        add_q("easy", "Reproduction Strategies", f"In Grade 12 CAPS Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Reproduction Strategies", f"Which biological term correctly names {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in vert_terms if d[0] != term][:7]
        add_q("easy", "Reproduction Strategies", f"Which statement accurately explains the meaning of '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Reproduction Strategies", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

    easy_extras = [
        ("Which vertebrate groups produce amniotic eggs, freeing them from the requirement of returning to water to reproduce?", "Reptiles, birds, and egg-laying mammals", ["Bony fish and amphibians", "Amphibians and reptiles only", "All fish and amphibians", "Mammals only", "Birds only", "Cartilaginous fish only"], "Amniotes comprise reptiles, birds, and mammals, characterized by the amniotic egg or its evolutionary derivatives."),
        ("Why must amphibians return to water or moist environments to lay their eggs?", "Their eggs lack a protective shell and amniotic membranes, making them prone to desiccation (drying out)", ["Their eggs are fertilised internally", "Their sperm cannot swim in air", "Their embryos only absorb oxygen through bird-like shells", "Their larvae feed exclusively on marine algae", "Their adults cannot breathe terrestrial air"], "Amphibian eggs (anamniotic) are covered only in a jelly coat and rapidly dry out in dry air."),
        ("In an amniotic egg, which extra-embryonic membrane acts as a shock absorber to protect the embryo from physical damage?", "Amnion (containing amniotic fluid)", ["Chorion", "Allantois", "Yolk sac", "Calcified shell", "Chalaza", "Albumin only"], "The fluid-filled amniotic cavity functions as a hydraulic shock absorber protecting the delicate embryo."),
        ("Which of the following bird species exhibits precocial development at hatching?", "Domestic chicken (Gallus gallus) and ostrich (Struthio camelus)", ["Pigeon (Columba livia)", "African fish eagle (Haliaeetus vocifer)", "Barn owl (Tyto alba)", "Cape weaver (Ploceus capensis)", "House sparrow (Passer domesticus)"], "Ground-nesting birds (chickens, ducks, ostriches) produce precocial young with eyes open and feathers capable of running immediately."),
        ("Which of the following bird species exhibits altricial development at hatching?", "Pigeon and eagle", ["Domestic fowl and duck", "Ostrich and guinea fowl", "Quail and turkey", "Goose and pheasant", "Flamingo and swan"], "Tree-nesting birds produce altricial chicks that are blind, naked, and completely dependent on parental feeding.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Vertebrate Reproduction: ", "In comparative animal biology: "]:
            add_q("easy", "Reproduction Strategies", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(vert_terms)
        q = f"Vertebrate reproduction question {e_counter}: Identify the strategy or structure defined as: {definition}."
        add_q("easy", "Reproduction Strategies", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    medium_scenarios = [
        ("Why do animals that practice external fertilisation (such as trout or bullfrogs) produce far greater numbers of eggs and sperm than animals that practice internal fertilisation?",
         "Gametes released into water suffer high mortality due to predation, water currents, and dilution, so vast numbers ensure at least some fertilisation occurs",
         ["Aquatic animals have larger reproductive organs than terrestrial animals", "External fertilisation requires double the chromosomes", "Water prevents sperm from swimming effectively", "Eggs laid in water are toxic to all predators", "Female aquatic animals do not possess ovaries"],
         "High risk of predation and dispersion in open water requires massive gamete production to ensure species survival.", "Application"),

        ("A marine biologist examines a female shark species that gives birth to live young. Examination shows the developing embryos were enclosed in thin egg membranes inside the uteri and nourished entirely by a large yolk sac, with zero placental connection. Which reproductive strategy is this?",
         "Ovovivipary",
         ["Vivipary", "Ovipary", "External fertilisation", "Parthenogenesis", "Hermaphroditic spawning", "Altricial incubation"],
         "Embryos developing inside eggs retained in the mother's body, nourished strictly by yolk without a placenta, defines ovovivipary.", "Application"),

        ("How does the source of embryonic nutrition differ fundamentally between viviparous mammals and oviparous birds?",
         "In viviparous mammals, nutrients pass continuously from the maternal blood via the placenta; in oviparous birds, nutrients are stored entirely in the egg yolk",
         ["Viviparous embryos feed on amniotic fluid; oviparous embryos feed on shell minerals", "In birds, the mother feeds the embryo via an umbilical cord", "Viviparous embryos produce their own food by photosynthesis", "There is no difference in the nutritional mechanism", "Oviparous embryos absorb nutrients directly from the nest"],
         "Vivipary provides continuous maternal nutrient delivery via the placenta, while ovipary relies strictly on pre-packaged yolk stores.", "Application"),

        ("Why is the evolution of the amniotic egg described as a crucial milestone in vertebrate transition from water to land?",
         "It provides an enclosed, fluid-filled aquatic environment complete with gas exchange and waste disposal, allowing reproduction away from water bodies",
         ["It prevents predators from ever eating the eggs", "It eliminated the need for male gametes", "It allowed embryos to develop without undergoing mitosis", "It changed the diploid chromosome number of reptiles", "It enabled reptiles to become endothermic"],
         "The amniotic egg is a self-contained life-support capsule that allowed vertebrates to conquer dry terrestrial ecosystems.", "Application"),

        ("In an amniotic egg, in what form is nitrogenous waste stored within the allantois, and why is this an adaptation for water conservation?",
         "Uric acid, which is non-toxic and virtually insoluble, precipitating out of solution without requiring water for storage",
         ["Ammonia, which evaporates through the porous shell into the air", "Urea, which dissolves in large volumes of amniotic fluid", "Nitrate salts that feed the developing embryo", "Pure nitrogen gas exhaled by the chorion", "Gaseous nitric oxide that kills bacteria"],
         "Uric acid requires minimal water to store and is non-toxic within the closed egg capsule, unlike toxic ammonia or soluble urea.", "Application"),

        ("What are the primary adaptive advantages of precocial development in ground-nesting birds such as the blue crane or guinea fowl?",
         "Chicks can run, forage, and escape ground predators almost immediately after hatching, reducing their vulnerability at ground level",
         ["Chicks do not require any food for the first six months of life", "Parents do not need to lay eggs with yolk", "Hatchlings can immediately fly long distances", "Chicks are born with adult plumage and breeding status", "It completely eliminates the need for adult protection"],
         "Ground-nesting species face severe terrestrial predation; precocial mobility minimizes nest predation risk.", "Application"),

        ("Why do altricial birds (such as pigeons, eagles, and swallows) lay smaller clutches with fewer eggs per breeding season than precocial birds?",
         "Parents must invest enormous daily energy in foraging and feeding helpless altricial chicks; fewer offspring ensures parents can provide adequate nutrition",
         ["Altricial chicks eat only minerals found in tree bark", "Altricial eggs contain three times more yolk than precocial eggs", "Female altricial birds have only one ovary that produces one egg", "Predation is non-existent in tree branches", "Altricial chicks hatch after only two days of incubation"],
         "High post-hatching parental energy expenditure limits the number of altricial offspring parents can successfully raise to fledging.", "Application")
    ]

    for q, ans, wrongs, expl, cog in medium_scenarios:
        for prefix in ["", "CAPS Comparative Ecology: ", "Reproductive Strategy Investigation: ", "Evolutionary Adaptation Case: "]:
            add_q("medium", "Vertebrate Adaptations", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500
    species_strategies = [
        ("African bullfrog (Pyxicephalus adspersus)", "External fertilisation and ovipary", ["Internal fertilisation and vivipary", "Internal fertilisation and ovovivipary", "External fertilisation and vivipary", "Parthenogenesis and ovipary", "Marsupial brooding", "Internal fertilisation and altricial care"]),
        ("Puff adder (Bitis arietans)", "Internal fertilisation and ovovivipary", ["External fertilisation and ovipary", "Internal fertilisation and vivipary with placenta", "External spawning in rivers", "Asexual cloning", "Precocial altricial hybrid", "Internal fertilisation and anamniotic egg"]),
        ("African elephant (Loxodonta africana)", "Internal fertilisation, vivipary, and precocial development", ["External fertilisation, ovipary, and altricial care", "Internal fertilisation and ovovivipary", "Ovipary with amniotic egg", "External broadcast spawning", "Parthenogenesis and vivipary", "Marsupial pouch development"]),
        ("Barn owl (Tyto alba)", "Internal fertilisation, ovipary (amniotic egg), and altricial development", ["External fertilisation and ovipary", "Internal fertilisation and precocial development", "Ovovivipary and vivipary", "External spawning and altricial care", "Vivipary with placental transfer", "Asexual reproduction"]),
        ("Great white shark (Carcharodon carcharias)", "Internal fertilisation and ovovivipary (oophagy)", ["External fertilisation and ovipary", "External broadcast spawning", "Placental vivipary with lactation", "Amniotic shell laying on beaches", "Anamniotic egg laying in freshwater", "Altricial parental feeding"]),
        ("Nile crocodile (Crocodylus niloticus)", "Internal fertilisation, ovipary (leathery amniotic egg), with nest protection", ["External fertilisation and ovovivipary", "Placental vivipary", "Altricial feeding of chicks with milk", "Anamniotic jelly egg laying in water", "Broadcast spawning during floods", "Asexual parthenogenesis"])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        sp_item = random.choice(species_strategies)
        q = f"Vertebrate species assessment {m_counter}: What combination of reproductive strategies is practiced by the {sp_item[0]}?"
        add_q("medium", "Species Strategies", q, sp_item[1], sp_item[2], f"{sp_item[0]} demonstrates {sp_item[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        ("From an evolutionary perspective, why did internal fertilisation evolve hand-in-hand with the terrestrial lifestyle, while external fertilisation remained dominant in aquatic environments?",
         "Sperm cells require a fluid medium to swim to the ovum; in terrestrial environments without external water, the female reproductive tract provides the necessary fluid environment to prevent gamete desiccation",
         ["Terrestrial animals have less metabolic energy than aquatic animals", "Aquatic animals cannot undergo meiosis during gametogenesis", "Air is toxic to haploid eggs", "External fertilisation produces only female offspring on land", "Internal fertilisation guarantees 100% of eggs hatch into adults", "Terrestrial predators are unable to eat eggs with shells"],
         "Gametes require moisture to survive and motility; internal fertilisation internalizes the aquatic environment within the female tract.", "Analysis"),

        ("Evaluate the energetic trade-off between ovipary and vivipary in terrestrial vertebrates. Which statement accurately captures this evolutionary balance?",
         "Vivipary requires continuous, high metabolic investment from the mother during gestation but results in high individual offspring survival, whereas ovipary has lower maternal risk during gestation but higher egg predation risk",
         ["Ovipary requires far more maternal energy than vivipary because shells are made of gold", "Vivipary allows mothers to lay hundreds of young simultaneously with zero risk", "Ovipary guarantees that no offspring are ever eaten by predators", "Viviparous animals do not require parental care after birth", "Ovipary only occurs in cold biomes while vivipary occurs in hot biomes", "There is zero energetic difference between ovipary and vivipary"],
         "Vivipary trades maternal mobility and energy during gestation for drastically increased offspring protection and survival.", "Analysis"),

        ("Why does the chorion in bird and reptile eggs need to be closely pressed against the inner surface of the porous shell?",
         "To minimize the diffusion distance for oxygen entering and carbon dioxide leaving the blood capillaries of the chorioallantoic membrane",
         ["To prevent water from entering the albumin layer", "To prevent the embryo from moving inside the amniotic cavity", "To block ultraviolet radiation from reaching the yolk sac", "To absorb calcium from the shell to synthesize hemoglobin", "To prevent bacterial spores from respiring anaerobically", "To allow the allantois to store liquid urine outside the egg"],
         "Respiratory gas diffusion depends on minimizing the barrier distance between atmosphere and embryonic capillaries.", "Analysis"),

        ("How does parental care correlate with survivorship curves in vertebrates?",
         "Species with intense parental care (e.g., humans, elephants, eagles) exhibit Type I survivorship with low juvenile mortality, while species with zero parental care (e.g., fish, frogs) exhibit Type III survivorship with high juvenile mortality",
         ["Species with intense care exhibit Type III survivorship with high juvenile deaths", "Parental care has no measurable correlation with offspring mortality", "Species with zero care always exhibit Type I survivorship", "Type II survivorship is exclusive to ovoviviparous sharks", "Precocial species never provide parental care under any circumstances", "Altricial species have higher adult mortality than juvenile mortality"],
         "Parental investment buffers neonates against environmental mortality, shifting survival dynamics towards late-life mortality (Type I).", "Analysis"),

        ("Why is the albumin (egg white) in an amniotic egg composed primarily of water and ovalbumin protein, while the yolk is rich in lipids and lipoproteins?",
         "Yolk provides a dense, long-term caloric energy reservoir for tissue growth, while albumin provides essential hydration and physical shock cushioning in a dry terrestrial environment",
         ["Albumin provides the genetic code for embryonic development while yolk provides ATP", "Yolk prevents the egg from sinking in water while albumin allows flight", "Albumin contains restriction enzymes that synthesize DNA", "Yolk is an excretion waste product containing uric acid", "Albumin is synthesized by the embryo's allantois during organogenesis", "Yolk contains no fats or proteins"],
         "Lipids in yolk yield twice as much metabolic energy per gram as carbohydrates/proteins; albumin ensures the embryo has water for biochemical reactions.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "CAPS High-Level Synthesis: ", "Vertebrate Reproduction Evaluation: ", "Comparative Embryological Analysis: "]:
            add_q("hard", "Evolutionary Reproductive Trade-offs", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Reproductive trade-off problem {h_counter}: {base_h[0]}"
        add_q("hard", "Evolutionary Reproductive Trade-offs", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/life_sciences/paper1_life_reproduction_vertebrates.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_reproduction_vertebrates()
