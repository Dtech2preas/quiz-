import json
import random
import os

TOPICS = {
    "meiosis": {
        "title": "Meiosis",
        "subtopics": ["Stages of meiosis", "Chromosome behaviour", "Crossing over", "Independent assortment", "Haploid and diploid cells", "Importance of meiosis"]
    },
    "reproduction_vertebrates": {
        "title": "Reproduction in Vertebrates",
        "subtopics": ["Sexual reproduction", "Reproductive strategies", "Internal and external fertilisation", "Ovipary, ovovivipary and vivipary", "Advantages and disadvantages of reproductive strategies"]
    },
    "human_reproduction": {
        "title": "Human Reproduction",
        "subtopics": ["Male reproductive system", "Female reproductive system", "Gametogenesis", "Menstrual cycle", "Fertilisation", "Pregnancy and birth"]
    },
    "responding_environment_humans": {
        "title": "Responding to the Environment (Humans)",
        "subtopics": ["Nervous system", "Central nervous system", "Peripheral nervous system", "Reflex actions", "Sense organs", "Eye structure and function", "Ear structure and function"]
    },
    "human_endocrine_system": {
        "title": "Human Endocrine System",
        "subtopics": ["Endocrine glands", "Hormones", "Negative feedback mechanisms", "Regulation of blood glucose", "Growth hormone", "Thyroxine", "Adrenaline"]
    },
    "homeostasis_humans": {
        "title": "Homeostasis in Humans",
        "subtopics": ["Thermoregulation", "Osmoregulation", "Blood glucose regulation", "Water balance", "Feedback mechanisms"]
    },
    "responding_environment_plants": {
        "title": "Responding to the Environment (Plants)",
        "subtopics": ["Tropisms", "Phototropism", "Geotropism", "Plant hormones", "Growth responses"]
    },
    "human_impact_environment": {
        "title": "Human Impact on the Environment",
        "subtopics": ["Pollution", "Climate change", "Loss of biodiversity", "Conservation", "Sustainable resource use", "Environmental management"]
    },
    "dna_code_of_life": {
        "title": "DNA: The Code of Life",
        "subtopics": ["Structure of DNA", "DNA replication", "Protein synthesis", "RNA", "Transcription", "Translation", "Mutations"]
    },
    "genetics_inheritance": {
        "title": "Genetics and Inheritance",
        "subtopics": ["Mendelian genetics", "Dominant and recessive traits", "Monohybrid crosses", "Genotype and phenotype", "Pedigree diagrams", "Genetic disorders", "Inheritance patterns"]
    },
    "evolution": {
        "title": "Evolution",
        "subtopics": ["Evidence for evolution", "Natural selection", "Speciation", "Evolution by natural selection", "Human evolution", "Fossil evidence", "Darwin's theory"]
    }
}

DIFFICULTY_DISTRIBUTION = {"easy": 0.3, "medium": 0.5, "hard": 0.2}

MISCONCEPTIONS = {
    "meiosis": ["Mitosis", "Binary fission", "Budding", "Fragmentation", "Cloning", "Asexual reproduction", "Polyploidy", "Non-disjunction", "Replication", "Transcription"],
    "dna_code_of_life": ["RNA polymerase", "DNA polymerase", "Ribosome", "tRNA", "mRNA", "Amino acid", "Protein", "Nucleotide", "Nitrogenous base", "Codon", "Anticodon", "Helicase", "Ligase"],
    "genetics_inheritance": ["Homozygous", "Heterozygous", "Dominant", "Recessive", "Allele", "Gene", "Chromosome", "Chromatid", "Phenotype", "Genotype", "Mutation", "Incomplete dominance", "Co-dominance"],
    "evolution": ["Lamarckism", "Acquired characteristics", "Artificial selection", "Genetic drift", "Gene flow", "Mutation", "Punctuated equilibrium", "Gradualism", "Homologous structures", "Analogous structures", "Vestigial organs", "Fossil record", "Biogeography"],
    "human_reproduction": ["Ovary", "Testis", "Uterus", "Fallopian tube", "Vas deferens", "Epididymis", "Prostate gland", "Seminal vesicle", "Cowper's gland", "Endometrium", "Cervix", "Vagina", "Placenta", "Umbilical cord", "Amnion", "Chorion", "Fetus", "Embryo", "Zygote"],
    "human_endocrine_system": ["Pituitary gland", "Thyroid gland", "Adrenal gland", "Pancreas", "Ovary", "Testis", "Hypothalamus", "Target organ", "Receptor", "Hormone", "Insulin", "Glucagon", "Adrenaline", "Thyroxine", "TSH", "FSH", "LH", "Estrogen", "Progesterone", "Testosterone"],
    "homeostasis_humans": ["Kidney", "Nephron", "Glomerulus", "Bowman's capsule", "Proximal convoluted tubule", "Loop of Henle", "Distal convoluted tubule", "Collecting duct", "Ureter", "Bladder", "Urethra", "Liver", "Skin", "Sweat gland", "Blood vessel", "Vasodilation", "Vasoconstriction", "ADH", "Aldosterone"],
    "responding_environment_humans": ["Brain", "Spinal cord", "Neuron", "Sensory neuron", "Motor neuron", "Interneuron", "Synapse", "Neurotransmitter", "Receptor", "Effector", "Stimulus", "Response", "Reflex arc", "Cornea", "Iris", "Pupil", "Lens", "Retina", "Optic nerve", "Pinna", "Auditory canal", "Tympanic membrane", "Ossicles", "Cochlea", "Auditory nerve", "Semi-circular canals"],
    "responding_environment_plants": ["Auxin", "Gibberellin", "Abscisic acid", "Stem", "Root", "Apical dominance", "Geotropism", "Phototropism", "Thigmotropism", "Hydrotropism", "Clinostat", "Coleoptile", "Apical meristem"],
    "human_impact_environment": ["Global warming", "Greenhouse effect", "Ozone depletion", "Deforestation", "Desertification", "Eutrophication", "Acid rain", "Alien invasive species", "Overexploitation", "Poaching", "Culling", "Carrying capacity", "Carbon footprint", "Biodiversity"],
    "reproduction_vertebrates": ["Internal fertilisation", "External fertilisation", "Ovipary", "Ovovivipary", "Vivipary", "Amniotic egg", "Precocial development", "Altricial development", "Parental care"]
}

SVG_TEMPLATES = {
    "meiosis": [
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="2" fill="none"/><line x1="30" y1="30" x2="70" y2="70" stroke="red" stroke-width="4"/><line x1="70" y1="30" x2="30" y2="70" stroke="blue" stroke-width="4"/></svg>',
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="2" fill="none"/><line x1="20" y1="50" x2="80" y2="50" stroke="green" stroke-width="2"/><circle cx="30" cy="50" r="10" fill="red"/><circle cx="70" cy="50" r="10" fill="blue"/></svg>'
    ],
    "dna_code_of_life": [
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M 20 20 Q 50 50 80 20 T 20 80 Q 50 50 80 80" stroke="blue" stroke-width="3" fill="none"/><line x1="30" y1="35" x2="70" y2="35" stroke="red" stroke-width="2"/><line x1="40" y1="50" x2="60" y2="50" stroke="green" stroke-width="2"/><line x1="30" y1="65" x2="70" y2="65" stroke="orange" stroke-width="2"/></svg>'
    ],
    "genetics_inheritance": [
         '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><rect x="40" y="10" width="20" height="20" stroke="black" fill="white"/><circle cx="70" cy="20" r="10" stroke="black" fill="black"/><line x1="50" y1="30" x2="50" y2="50" stroke="black"/><line x1="70" y1="30" x2="70" y2="50" stroke="black"/><line x1="50" y1="40" x2="70" y2="40" stroke="black"/><rect x="60" y="50" width="20" height="20" stroke="black" fill="white"/></svg>'
    ],
    "human_endocrine_system": [
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><ellipse cx="50" cy="20" rx="15" ry="10" fill="pink" stroke="black"/><text x="50" y="25" text-anchor="middle" font-size="10">Pituitary</text><ellipse cx="50" cy="50" rx="20" ry="15" fill="orange" stroke="black"/><text x="50" y="55" text-anchor="middle" font-size="10">Thyroid</text></svg>'
    ],
    "human_reproduction": [
         '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M 50 80 C 20 80, 20 30, 50 30 C 80 30, 80 80, 50 80 Z" fill="pink" stroke="black"/><circle cx="30" cy="40" r="10" fill="red"/><circle cx="70" cy="40" r="10" fill="red"/><text x="50" y="60" text-anchor="middle" font-size="10">Uterus</text></svg>'
    ]
}

BASE_CONCEPTS = {
    "meiosis": [
        ("Homologous chromosomes", "a pair of chromosomes containing the same linear gene sequences", "they separate during meiosis I"),
        ("Crossing over", "the exchange of genetic material between non-sister chromatids", "it introduces genetic variation"),
        ("Chiasma", "the point of contact during crossing over", "it occurs in Prophase I"),
        ("Non-disjunction", "the failure of chromosomes to separate correctly", "it can lead to Down syndrome"),
        ("Haploid", "cells with half the normal number of chromosomes", "gametes are an example"),
        ("Diploid", "cells with a full set of chromosomes", "somatic cells are an example"),
        ("Meiosis II", "the second division where sister chromatids separate", "it resembles mitosis"),
        ("Spindle fibres", "structures that pull chromosomes apart", "they attach to the centromere"),
        ("Bivalent", "a pair of homologous chromosomes during Prophase I", "it consists of four chromatids")
    ],
    "reproduction_vertebrates": [
        ("Ovipary", "eggs are laid and hatch outside the mother's body", "common in birds and reptiles"),
        ("Vivipary", "live young are born after developing inside the mother", "common in mammals"),
        ("Ovovivipary", "eggs hatch inside the mother's body before birth", "provides protection without a placenta"),
        ("Internal fertilisation", "sperm fuses with an egg inside the female's body", "increases the chances of successful fertilisation"),
        ("External fertilisation", "sperm fuses with an egg outside the female's body", "requires a watery environment"),
        ("Amniotic egg", "an egg with a shell and internal membranes", "it allows reproduction away from water"),
        ("Precocial development", "young are born fully developed and mobile", "common in ground-nesting birds"),
        ("Altricial development", "young are born naked and helpless", "requires significant parental care")
    ],
    "human_reproduction": [
        ("Testosterone", "the hormone responsible for male secondary sexual characteristics", "produced by the testes"),
        ("Estrogen", "the hormone responsible for female secondary sexual characteristics", "produced by the ovaries"),
        ("Progesterone", "the hormone that maintains the uterine lining during pregnancy", "secreted by the corpus luteum"),
        ("FSH", "the hormone that stimulates the development of a follicle", "secreted by the pituitary gland"),
        ("LH", "the hormone that triggers ovulation", "secreted by the pituitary gland"),
        ("Endometrium", "the inner lining of the uterus", "it is shed during menstruation"),
        ("Placenta", "the organ that nourishes the fetus", "it allows exchange of substances between mother and fetus"),
        ("Umbilical cord", "connects the fetus to the placenta", "contains the umbilical artery and vein")
    ],
    "responding_environment_humans": [
        ("Reflex arc", "the neural pathway that controls a reflex action", "it provides a rapid, involuntary response"),
        ("Synapse", "the gap between two adjacent neurons", "neurotransmitters carry the impulse across it"),
        ("Myelin sheath", "the fatty layer surrounding an axon", "it insulates the neuron and speeds up impulse transmission"),
        ("Cornea", "the clear, front part of the eye", "it refracts light entering the eye"),
        ("Lens", "the structure that focuses light onto the retina", "it changes shape during accommodation"),
        ("Retina", "the light-sensitive layer at the back of the eye", "contains rods and cones"),
        ("Cochlea", "the snail-like structure in the inner ear", "it contains mechanoreceptors for hearing"),
        ("Semi-circular canals", "structures in the inner ear", "they are responsible for balance")
    ],
    "human_endocrine_system": [
        ("Insulin", "the hormone that lowers blood glucose levels", "produced by the beta cells of the pancreas"),
        ("Glucagon", "the hormone that raises blood glucose levels", "produced by the alpha cells of the pancreas"),
        ("Adrenaline", "the hormone that prepares the body for a 'fight or flight' response", "secreted by the adrenal glands"),
        ("Thyroxine", "the hormone that regulates the basal metabolic rate", "secreted by the thyroid gland"),
        ("TSH", "the hormone that stimulates the thyroid gland to secrete thyroxine", "secreted by the pituitary gland"),
        ("Negative feedback", "a mechanism where the response counteracts the stimulus", "it maintains homeostasis"),
        ("Growth hormone", "the hormone that stimulates growth and cell reproduction", "secreted by the anterior pituitary")
    ],
    "homeostasis_humans": [
        ("Thermoregulation", "the maintenance of a constant internal body temperature", "involves sweating and vasodilation/vasoconstriction"),
        ("Osmoregulation", "the maintenance of a constant water and solute concentration", "regulated by ADH and the kidneys"),
        ("ADH", "the hormone that increases the permeability of the collecting ducts in the kidney", "it reduces water loss in urine"),
        ("Aldosterone", "the hormone that regulates sodium reabsorption in the kidney", "secreted by the adrenal glands"),
        ("Vasodilation", "the widening of blood vessels", "it increases heat loss from the skin"),
        ("Vasoconstriction", "the narrowing of blood vessels", "it reduces heat loss from the skin")
    ],
    "responding_environment_plants": [
        ("Phototropism", "the growth movement of a plant in response to light", "stems are positively phototropic"),
        ("Geotropism", "the growth movement of a plant in response to gravity", "roots are positively geotropic"),
        ("Auxin", "the plant hormone responsible for cell elongation", "it accumulates on the dark side of a stem"),
        ("Gibberellin", "the plant hormone that promotes seed germination", "it stimulates the breakdown of starch"),
        ("Abscisic acid", "the plant hormone that promotes seed dormancy", "it causes stomata to close during drought"),
        ("Apical dominance", "the inhibition of lateral bud growth by the apical bud", "it is caused by high auxin concentrations")
    ],
    "human_impact_environment": [
        ("Eutrophication", "the over-enrichment of a water body with nutrients", "leads to algal blooms and oxygen depletion"),
        ("Global warming", "the gradual increase in the Earth's average temperature", "caused by the enhanced greenhouse effect"),
        ("Deforestation", "the large-scale removal of trees", "increases carbon dioxide levels in the atmosphere"),
        ("Alien invasive species", "non-native species that outcompete indigenous species", "they often lack natural predators"),
        ("Carbon footprint", "the total amount of greenhouse gases emitted", "can be reduced by using renewable energy"),
        ("Biodiversity", "the variety of life in a particular habitat or ecosystem", "it is threatened by habitat destruction"),
        ("Ozone depletion", "the thinning of the ozone layer", "caused by CFCs")
    ],
    "dna_code_of_life": [
        ("Nucleotide", "the building block of nucleic acids", "consists of a sugar, phosphate, and nitrogenous base"),
        ("Transcription", "the process of making an mRNA copy of a DNA template", "occurs in the nucleus"),
        ("Translation", "the process of synthesizing a protein from an mRNA template", "occurs at the ribosome"),
        ("Mutation", "a change in the sequence of nitrogenous bases in DNA", "can lead to altered protein function"),
        ("Codon", "a sequence of three mRNA bases that codes for a specific amino acid", "it pairs with an anticodon on tRNA"),
        ("Anticodon", "a sequence of three tRNA bases", "it pairs with a codon on mRNA"),
        ("DNA replication", "the process of copying a DNA molecule", "it occurs during interphase")
    ],
    "genetics_inheritance": [
        ("Allele", "an alternative form of a gene", "occupies a specific locus on a chromosome"),
        ("Phenotype", "the physical appearance or expression of a trait", "determined by the genotype and environment"),
        ("Genotype", "the genetic makeup of an organism", "represented by letters like TT, Tt, or tt"),
        ("Homozygous", "having two identical alleles for a particular trait", "can be dominant (TT) or recessive (tt)"),
        ("Heterozygous", "having two different alleles for a particular trait", "represented by Tt"),
        ("Incomplete dominance", "a genetic situation where one allele does not completely dominate another", "results in a new phenotype"),
        ("Co-dominance", "a genetic situation where both alleles are fully expressed", "results in a phenotype showing both traits")
    ],
    "evolution": [
        ("Natural selection", "the process where organisms better adapted to their environment survive and reproduce", "proposed by Charles Darwin"),
        ("Speciation", "the formation of a new species", "often occurs due to geographical isolation"),
        ("Fossil", "the preserved remains or traces of an ancient organism", "provides evidence for evolution"),
        ("Homologous structures", "structures that are similar in basic plan but may differ in function", "indicate a common ancestor"),
        ("Artificial selection", "the selective breeding of plants or animals by humans for desired traits", "results in domesticated species"),
        ("Vestigial organs", "remnants of organs that were functional in ancestors", "e.g., the human appendix"),
        ("Biogeography", "the study of the geographical distribution of organisms", "provides evidence for evolution")
    ]
}

CONTEXTS = [
    "During a practical investigation in a school laboratory,",
    "A research scientist studying biological systems notes that",
    "In a Grade 12 Life Sciences exam, a student is asked about a scenario where",
    "A recent documentary on biology highlighted that",
    "While reviewing literature on South African biodiversity, it is noted that",
    "Consider a theoretical model in which",
    "A medical professional explaining a diagnosis mentions that",
    "In a detailed biological case study,",
    "An agricultural expert in South Africa observes that",
    "A university textbook on biological processes states that",
    "During an ecological survey in the Kruger National Park, researchers found that",
    "A genetic counselor explaining inheritance patterns notes that",
    "When examining a sample under a light microscope, a student observes that",
    "In a discussion on human physiology, it is brought up that",
    "According to the CAPS curriculum guidelines,"
]

QUESTION_TEMPLATES = {
    "easy": [
        "{context} the biological term for {desc} is required. What is this term?",
        "Identify the biological concept defined exactly as: {desc}.",
        "Which of the following terms correctly matches the description: '{desc}'?",
        "The scientific definition '{desc}' corresponds to which biological term?",
        "In biological terminology, {desc} is best referred to as:",
        "{context} what is the precise scientific name for {desc}?",
        "Select the term that best fits the following definition: {desc}."
    ],
    "medium": [
        "{context} it is observed that {fact}. Which biological concept does this primarily relate to?",
        "Which of the following is true regarding {term}?",
        "What is a key characteristic or essential function associated with {term}?",
        "In the context of this biological process, how does {term} function?",
        "Regarding {term}, which statement is scientifically accurate?",
        "{context} the process of {term} is discussed. What is a key fact about it?",
        "Why is {term} biologically significant? Choose the most accurate statement."
    ],
    "hard": [
        "{context} a disruption occurs affecting {term}. Based on the fact that {fact}, what is the likely outcome?",
        "Analyze the role of {term}. If {desc}, which related principle is demonstrated by the fact that {fact}?",
        "Evaluate the following biological statement: '{fact}'. This is a defining characteristic of which complex concept?",
        "A student proposes that {term} is merely {desc}. How would you expand on this using a key biological fact?",
        "In a complex biological system, {term} plays a crucial role. Which associated fact accurately describes its action?",
        "{context} researchers analyze {term}. They conclude it involves {desc}. What further factual observation supports this?",
        "Synthesize the given information: a structure or process is defined as {desc}. It is also known that {fact}. Identify the correct term."
    ]
}

class Generator:
    def __init__(self, topic_key, topic_data):
        self.topic_key = topic_key
        self.title = topic_data["title"]
        self.subtopics = topic_data["subtopics"]
        self.questions = []
        self.seen_questions = set()

        self.target_counts = {
            diff: int(1000 * prop) for diff, prop in DIFFICULTY_DISTRIBUTION.items()
        }
        self.current_counts = {diff: 0 for diff in DIFFICULTY_DISTRIBUTION}

    def add_question(self, q_obj):
        diff = q_obj["difficulty"]
        if self.current_counts[diff] < self.target_counts[diff]:
            q_text = q_obj["question"]
            if q_text not in self.seen_questions:
                self.seen_questions.add(q_text)
                self.questions.append(q_obj)
                self.current_counts[diff] += 1
                return True
        return False

    def generate(self):
        attempts = 0
        max_attempts = 200000

        base_concepts = BASE_CONCEPTS[self.topic_key]

        while len(self.questions) < 1000 and attempts < max_attempts:
            attempts += 1

            needed_diffs = [d for d, c in self.current_counts.items() if c < self.target_counts[d]]
            if not needed_diffs:
                break

            diff = random.choice(needed_diffs)
            subtopic = random.choice(self.subtopics)
            template = random.choice(QUESTION_TEMPLATES[diff])

            term, desc, fact = random.choice(base_concepts)
            context = random.choice(CONTEXTS)

            q_text = template.format(context=context, term=term, desc=desc, fact=fact)

            variations = ["", " Choose the best option.", " Select the correct answer.", " Analyze carefully.", " What is the most appropriate response?"]
            q_text += random.choice(variations)

            if q_text in self.seen_questions:
                continue

            diagram_svg = None
            if self.topic_key in SVG_TEMPLATES and random.random() < 0.1:
                 diagram_svg = random.choice(SVG_TEMPLATES[self.topic_key])
                 q_text += " Refer to the provided diagram if necessary."

            if diff == "easy" or "Which concept" in q_text or "Which of the following terms" in q_text or "Identify the term" in q_text or "What is this term" in q_text:
                correct_answer = term
                wrong_answers = []
                for t, d, f in base_concepts:
                    if t != term:
                        wrong_answers.append(t)

                pool = MISCONCEPTIONS.get(self.topic_key, [])
                if pool:
                    wrong_answers.extend(random.sample(pool, min(10, len(pool))))

            elif diff == "medium" or "statement is biologically accurate" in q_text or "true regarding" in q_text:
                correct_answer = fact.capitalize()
                wrong_answers = []
                for t, d, f in base_concepts:
                    if f != fact:
                        wrong_answers.append(f.capitalize())
                fake_facts = [
                    "It occurs universally in all organisms without exception.",
                    "It is completely independent of environmental factors.",
                    "It requires a massive input of ATP to initiate.",
                    "It is the only factor responsible for genetic variation.",
                    "It only happens during the night in most species."
                ]
                wrong_answers.extend(fake_facts)

            else:
                 if "outcome" in q_text or "expand" in q_text:
                     correct_answer = fact.capitalize()
                     wrong_answers = [f.capitalize() for t, d, f in base_concepts if f != fact]
                     wrong_answers.extend(["It stops immediately.", "It reverses its normal function.", "It speeds up exponentially."])
                 else:
                     correct_answer = term
                     wrong_answers = [t for t, d, f in base_concepts if t != term]
                     pool = MISCONCEPTIONS.get(self.topic_key, [])
                     if pool:
                         wrong_answers.extend(random.sample(pool, min(10, len(pool))))

            unique_wrongs = list(set([str(w).strip() for w in wrong_answers if str(w).strip() != str(correct_answer).strip()]))
            random.shuffle(unique_wrongs)

            if len(unique_wrongs) < 6:
                fallbacks = ["Nucleus", "Mitochondria", "Chloroplast", "Cell membrane", "Cytoplasm", "Ribosome", "Vacuole", "Golgi apparatus"]
                for fb in fallbacks:
                    if fb not in unique_wrongs and fb != correct_answer:
                        unique_wrongs.append(fb)

            unique_wrongs = unique_wrongs[:8]

            if len(unique_wrongs) < 6:
                continue

            e_text = f"The correct answer is {correct_answer}. In biology, {term} is {desc}, and a key fact is that {fact}."

            q_obj = {
                "id": f"G12_LS_{self.topic_key.upper()}_{len(self.questions)+1:04d}",
                "topic": self.title,
                "subtopic": subtopic,
                "difficulty": diff,
                "question": q_text.strip(),
                "correct_answer": str(correct_answer).strip(),
                "wrong_answers_pool": unique_wrongs,
                "explanation": e_text.strip(),
                "diagram": diagram_svg
            }

            self.add_question(q_obj)

        print(f"[{self.topic_key}] Generated {len(self.questions)} questions. (Easy: {self.current_counts['easy']}, Medium: {self.current_counts['medium']}, Hard: {self.current_counts['hard']})")
        return self.questions

def main():
    os.makedirs("dataset/grade12/life_sciences", exist_ok=True)

    for key, data in TOPICS.items():
        generator = Generator(key, data)
        questions = generator.generate()

        filename = f"dataset/grade12/life_sciences/grade12_life_sciences_{key}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)

    print("Generation complete.")

if __name__ == "__main__":
    main()
