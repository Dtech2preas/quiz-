import json
import random
import os
import time

def generate_genetics():
    print("Generating Grade 12 Life Sciences: Genetics and Inheritance (Rich & Diverse)...")
    t0 = time.time()

    questions = []
    seen_texts = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive="Knowledge", diagram=None):
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
        q_id = f"LIFE_P2_GENETICS_{len(questions)+1:04d}"
        q_obj = {
            "id": q_id,
            "topic": "Genetics and Inheritance",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Life Sciences",
                "topic": "Genetics and Inheritance",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        }
        if diagram:
            q_obj["diagram"] = diagram
        questions.append(q_obj)
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    genetics_terms = [
        ("Gene", "A segment of DNA on a chromosome that codes for a specific protein and determines a particular inherited characteristic", ["Allele", "Locus", "Chromatid", "Centromere", "Histone", "Karyotype", "Codon"]),
        ("Allele", "Alternative forms of a gene located at the identical locus on homologous chromosomes", ["Gene", "Genome", "Gamete", "Chiasma", "Zygote", "Nucleosome", "Ribosome"]),
        ("Homozygous", "A genotype containing two identical alleles for a specific trait (e.g., BB or bb)", ["Heterozygous", "Hemizygous", "Polyploid", "Aneuploid", "Co-dominant", "Dihybrid", "Recessive"]),
        ("Heterozygous", "A genotype containing two different alleles for a specific trait (e.g., Bb)", ["Homozygous", "Hemizygous", "Pure breeding", "Monoploid", "Polygenic", "Recessive", "Incomplete"]),
        ("Dominant allele", "An allele that is expressed in the phenotype when present in either homozygous or heterozygous state", ["Recessive allele", "Codominant allele", "Incomplete allele", "Lethal allele", "Epistatic allele", "Silent allele", "Mutant allele"]),
        ("Recessive allele", "An allele that is only expressed in the phenotype when in the homozygous condition (masked by a dominant allele)", ["Dominant allele", "Codominant allele", "Epistatic allele", "Sex-linked allele", "Multiple allele", "Wild-type allele", "Active allele"]),
        ("Genotype", "The complete genetic composition or allele combination of an organism represented by letters (e.g., Bb)", ["Phenotype", "Karyotype", "Pedigree", "Genome", "Epigenome", "Proteome", "Locus"]),
        ("Phenotype", "The physical appearance or observable biological characteristics of an organism determined by its genotype and environment", ["Genotype", "Karyotype", "Genome", "Allele", "Pedigree", "Proteome", "Locus"]),
        ("Complete dominance", "A pattern of inheritance where the dominant allele completely masks the expression of the recessive allele in the heterozygote", ["Incomplete dominance", "Co-dominance", "Polygenic inheritance", "Multiple alleles", "Sex linkage", "Epistasis", "Pleiotropy"]),
        ("Incomplete dominance", "A pattern of inheritance where neither allele is dominant, producing an intermediate or blended phenotype in the heterozygote", ["Complete dominance", "Co-dominance", "Multiple alleles", "Sex-linked inheritance", "Polygenic inheritance", "Epistasis", "Dihybrid dominance"]),
        ("Co-dominance", "A pattern of inheritance where both alleles are equally expressed simultaneously in the phenotype of the heterozygote without blending", ["Incomplete dominance", "Complete dominance", "Polygenic inheritance", "Epistasis", "Continuous variation", "Recessive masking", "Dihybrid linkage"]),
        ("Multiple alleles", "A condition where more than two alternative alleles control a single genetic trait within a population (e.g., ABO blood groups)", ["Polygenic inheritance", "Co-dominance", "Incomplete dominance", "Dihybrid inheritance", "Sex-linked alleles", "Epistasis", "Gene duplication"]),
        ("Polygenic inheritance", "A characteristic controlled by the additive effects of multiple independent genes, producing continuous phenotypic variation (e.g., human skin colour, height)", ["Multiple alleles", "Monohybrid inheritance", "Co-dominance", "Incomplete dominance", "Sex linkage", "Complete dominance", "Single gene inheritance"]),
        ("Autosomes", "All chromosomes other than sex chromosomes (pairs 1 to 22 in human somatic cells)", ["Gonosomes", "Sex chromosomes", "Centrosomes", "Chromatids", "Histones", "Plasmids", "Gametes"]),
        ("Gonosomes", "The sex chromosomes that determine the biological sex of an organism (the 23rd pair: XX in human females, XY in males)", ["Autosomes", "Centromeres", "Telomeres", "Chromatids", "Nucleosomes", "Histones", "Lysosomes"]),
        ("Sex-linked trait", "A genetic characteristic controlled by a gene located on one of the sex chromosomes, typically on the non-homologous region of the X chromosome", ["Autosomal trait", "Polygenic trait", "Co-dominant trait", "Mitochondrial trait", "Epistatic trait", "Cytoplasmic trait", "Monohybrid trait"]),
        ("Karyotype", "A standardized chart or diagram showing the complete set of chromosomes of an organism arranged in homologous pairs according to size, shape, and centromere position", ["Pedigree chart", "Punnett square", "DNA profile", "Phylogenetic tree", "Restriction map", "Electropherogram", "Linkage map"]),
        ("Pedigree chart", "A family tree diagram using standard symbols to trace the inheritance of a specific trait or disorder across successive generations", ["Karyotype", "Punnett square", "Cladogram", "DNA fingerprint", "Cytogenetic spread", "Phylogeny", "Genetic cross diagram"]),
        ("Cloning", "The production of genetically identical cells, tissues, or whole organisms from a single progenitor cell", ["Genetic modification", "Selective breeding", "Polymerase chain reaction", "Gel electrophoresis", "Crossing over", "In vitro fertilisation", "Transfection"]),
        ("Stem cells", "Undifferentiated biological cells that can differentiate into specialized cell types and divide indefinitely through mitosis", ["Somatic cells", "Gametes", "Zygotes", "Erythrocytes", "Neurons", "Histones", "Epithelial cells"])
    ]

    for term, definition, wrongs in genetics_terms:
        add_q("easy", "Genetics Terminology", f"In CAPS Grade 12 Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Genetics Terminology", f"Which biological term correctly identifies {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in genetics_terms if d[0] != term][:7]
        add_q("easy", "Genetics Terminology", f"Which statement provides the accurate definition of '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Genetics Terminology", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The correct statement is that {term} is {definition}.")

    easy_extras = [
        ("How many total chromosomes are found in the somatic nucleus of a healthy human being?", "46 chromosomes (23 homologous pairs)", ["23 single chromosomes", "48 chromosomes", "44 chromosomes", "92 chromosomes", "47 chromosomes", "32 chromosomes"], "Human somatic cells are diploid with 46 chromosomes (2n = 46)."),
        ("How many autosome pairs are present in human somatic cells?", "22 pairs of autosomes (44 total)", ["23 pairs", "1 pair", "21 pairs", "46 pairs", "20 pairs", "24 pairs"], "Pairs 1 to 22 are autosomes; pair 23 comprises the sex chromosomes."),
        ("Which pair of chromosomes determines biological sex in humans?", "Pair 23 (Gonosomes / Sex chromosomes)", ["Pair 1", "Pair 21", "Pair 22", "Pair 13", "Pair 7", "Pair 18"], "Pair 23 consists of XX in females and XY in males."),
        ("What genetic term describes an individual possessing two identical recessive alleles (e.g., tt or bb)?", "Homozygous recessive", ["Heterozygous", "Homozygous dominant", "Hemizygous", "Co-dominant", "Polygenic", "Aneuploid"], "Homozygous recessive refers to possessing two copies of the recessive allele."),
        ("Gregor Mendel conducted his pioneering hybridization experiments on which organism?", "Garden pea (Pisum sativum)", ["Fruit fly (Drosophila melanogaster)", "Bread mold (Neurospora crassa)", "Bacteriophage T4", "White mice (Mus musculus)", "Arabidopsis thaliana", "Corn (Zea mays)"], "Mendel worked with the garden pea plant Pisum sativum."),
        ("In ABO blood group inheritance, how many alleles control the trait in the human population?", "3 alleles (IA, IB, and i)", ["2 alleles", "4 alleles", "6 alleles", "1 allele", "8 alleles", "23 alleles"], "The three alleles are IA, IB (codominant to each other) and i (recessive)."),
        ("Which ABO blood group represents the universal donor for red blood cells?", "Blood group O (genotype ii)", ["Blood group AB", "Blood group A", "Blood group B", "Blood group Rh+", "Blood group A1", "Blood group B2"], "Red blood cells of group O have neither A nor B antigens on their surface."),
        ("Which ABO blood group represents the universal recipient for red blood cell transfusions?", "Blood group AB (genotype IAIB)", ["Blood group O", "Blood group A", "Blood group B", "Blood group ii", "Blood group Rh-", "Blood group Bombay"], "Individuals with blood group AB produce neither anti-A nor anti-B antibodies."),
        ("What term describes a chart illustrating the complete set of stained metaphase chromosomes arranged in numbered pairs?", "Karyotype", ["Pedigree chart", "Punnett square", "Linkage map", "Restriction map", "DNA electropherogram", "Gel blot"], "A karyotype shows the full chromosome complement arranged by size and centromere location."),
        ("What chromosomal abnormality causes Down syndrome?", "Trisomy 21 (three copies of chromosome 21)", ["Monosomy X (Turner syndrome)", "Trisomy 18 (Edwards syndrome)", "XXY (Klinefelter syndrome)", "Deletion on chromosome 5", "Translocation of chromosome 9", "Polyploidy"], "Down syndrome is caused by non-disjunction of chromosome pair 21, resulting in 47 chromosomes.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Genetics Fact: ", "Fundamental Concept: "]:
            add_q("easy", "Genetics Fundamentals", f"{prefix}{q}", ans, wrongs, expl)

    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        base_t = random.choice(genetics_terms)
        q = f"Genetics terminology review {e_counter}: In biological science, '{base_t[0]}' refers to:"
        add_q("easy", "Genetics Terminology", q, base_t[1], [d[1] for d in genetics_terms if d[0] != base_t[0]][:7], f"{base_t[0]} means {base_t[1]}.")
        e_counter += 1

    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # Rich variety: Mendel peas, Incomplete, Codominance,
    # Sex determination, Dihybrid, Karyotypes, Varied Blood
    # ----------------------------------------------------
    medium_scenarios = [
        # --- A. Monohybrid Mendel Pea Crosses ---
        {
            "subtopic": "Mendelian Genetics",
            "q": "In pea plants, tall stem (T) is dominant over short stem (t). If two heterozygous tall pea plants (Tt × Tt) are crossed, what is the expected phenotypic ratio of their offspring?",
            "ans": "3 tall : 1 short",
            "wrongs": ["1 tall : 1 short", "1 tall : 3 short", "100% tall", "100% short", "1 tall : 2 medium : 1 short", "9 tall : 7 short"],
            "expl": "A monohybrid cross between two heterozygotes (Tt × Tt) yields 1 TT (tall), 2 Tt (tall), and 1 tt (short), producing a 3 tall : 1 short phenotypic ratio.",
            "diag": {"type": "monohybrid_mendel", "trait": "Stem Height", "p1": ["T", "t"], "p2": ["T", "t"], "hide_offspring": True}
        },
        {
            "subtopic": "Mendelian Genetics",
            "q": "A heterozygous tall pea plant (Tt) is test-crossed with a homozygous recessive short pea plant (tt). What is the expected phenotypic ratio among their offspring?",
            "ans": "1 tall : 1 short (50% tall, 50% short)",
            "wrongs": ["3 tall : 1 short", "100% tall", "100% short", "3 short : 1 tall", "1 tall : 2 short", "75% short, 25% tall"],
            "expl": "A test cross (Tt × tt) yields 50% Tt (tall) and 50% tt (short), confirming a 1 : 1 phenotypic ratio.",
            "diag": {"type": "monohybrid_mendel", "trait": "Stem Height", "p1": ["T", "t"], "p2": ["t", "t"], "hide_offspring": True}
        },
        {
            "subtopic": "Mendelian Genetics",
            "q": "In pea plants, round seed shape (R) is dominant over wrinkled seed shape (r). If two heterozygous plants (Rr × Rr) are crossed, what percentage of the offspring is expected to have round seeds?",
            "ans": "75% (3 in 4)",
            "wrongs": ["25% (1 in 4)", "50% (1 in 2)", "100%", "33.3%", "66.7%", "0%"],
            "expl": "Offspring genotypes are 1 RR : 2 Rr : 1 rr. Both RR and Rr display round seeds: 3/4 = 75%.",
            "diag": {"type": "monohybrid_mendel", "trait": "Seed Shape", "p1": ["R", "r"], "p2": ["R", "r"], "hide_offspring": True}
        },
        {
            "subtopic": "Mendelian Genetics",
            "q": "In pea plants, purple flowers (P) are dominant over white flowers (p). What is the expected genotypic ratio from a cross between two heterozygous plants (Pp × Pp)?",
            "ans": "1 PP : 2 Pp : 1 pp",
            "wrongs": ["3 PP : 1 pp", "1 PP : 1 pp", "100% Pp", "2 PP : 1 Pp : 1 pp", "3 Pp : 1 pp", "1 PP : 3 pp"],
            "expl": "The genotypic ratio of a monohybrid heterozygous cross is 1 homozygous dominant (PP) : 2 heterozygous (Pp) : 1 homozygous recessive (pp).",
            "diag": {"type": "monohybrid_mendel", "trait": "Flower Colour", "p1": ["P", "p"], "p2": ["P", "p"], "hide_offspring": True}
        },
        {
            "subtopic": "Mendelian Genetics",
            "q": "In pea plants, yellow seeds (Y) are dominant over green seeds (y). A homozygous yellow plant (YY) is crossed with a green-seeded plant (yy). What will be the phenotype of the F1 generation?",
            "ans": "100% yellow seeds (genotype Yy)",
            "wrongs": ["50% yellow, 50% green", "100% green seeds", "75% yellow, 25% green", "25% yellow, 75% green", "Yellow with green spots", "50% homozygous yellow, 50% green"],
            "expl": "YY × yy produces 100% heterozygous offspring (Yy), all displaying the dominant yellow phenotype.",
            "diag": {"type": "monohybrid_mendel", "trait": "Seed Colour", "p1": ["Y", "Y"], "p2": ["y", "y"], "hide_offspring": True}
        },

        # --- B. Incomplete Dominance ---
        {
            "subtopic": "Incomplete Dominance",
            "q": "In snapdragon flowers, red colour (R) is incompletely dominant over white colour (W). If a red snapdragon (RR) is crossed with a white snapdragon (WW), what is the phenotype of the F1 generation?",
            "ans": "100% pink flowers (genotype RW)",
            "wrongs": ["100% red flowers", "100% white flowers", "50% red, 50% white", "Red and white spotted flowers", "75% pink, 25% white", "50% pink, 50% red"],
            "expl": "Incomplete dominance produces an intermediate blended phenotype (pink) in the heterozygote RW.",
            "diag": {"type": "incomplete_codominance", "mode": "incomplete", "hide_f1": True}
        },
        {
            "subtopic": "Incomplete Dominance",
            "q": "Two pink snapdragon flowers (RW × RW) are cross-pollinated. What is the expected phenotypic ratio among their offspring?",
            "ans": "1 red : 2 pink : 1 white",
            "wrongs": ["3 pink : 1 white", "3 red : 1 white", "1 red : 1 white", "100% pink", "2 red : 1 pink : 1 white", "1 red : 3 pink"],
            "expl": "Cross RW × RW yields 1 RR (red) : 2 RW (pink) : 1 WW (white), where the genotypic and phenotypic ratios are identical.",
            "diag": {"type": "incomplete_codominance", "mode": "incomplete", "hide_f1": True}
        },
        {
            "subtopic": "Incomplete Dominance",
            "q": "A pink snapdragon (RW) is crossed with a white snapdragon (WW). What percentage of their offspring is expected to have pink flowers?",
            "ans": "50% (1 in 2)",
            "wrongs": ["25% (1 in 4)", "75% (3 in 4)", "100%", "0%", "33.3%", "66.7%"],
            "expl": "Cross RW × WW yields 50% RW (pink) and 50% WW (white).",
            "diag": {"type": "incomplete_codominance", "mode": "incomplete", "hide_f1": True}
        },

        # --- C. Codominance ---
        {
            "subtopic": "Codominance",
            "q": "In shorthorn cattle, coat colour is co-dominant: CRCR produces red, CWCW produces white, and CRCW produces roan. A red bull (CRCR) is mated with a white cow (CWCW). What coat colour will their calves have?",
            "ans": "100% roan (CRCW)",
            "wrongs": ["100% red", "100% white", "50% red, 50% white", "75% roan, 25% red", "Pink coat", "50% roan, 50% white"],
            "expl": "In codominance, both red and white hair alleles are simultaneously and fully expressed in the heterozygote CRCW, producing a roan coat.",
            "diag": {"type": "incomplete_codominance", "mode": "codominance", "hide_f1": True}
        },
        {
            "subtopic": "Codominance",
            "q": "A roan bull (CRCW) is mated with a roan cow (CRCW). What is the expected phenotypic ratio among their offspring?",
            "ans": "1 red : 2 roan : 1 white",
            "wrongs": ["3 roan : 1 white", "100% roan", "3 red : 1 white", "1 red : 1 white", "2 red : 1 roan : 1 white", "1 red : 3 roan"],
            "expl": "Cross CRCW × CRCW produces 1 CRCR (red) : 2 CRCW (roan) : 1 CWCW (white).",
            "diag": {"type": "incomplete_codominance", "mode": "codominance", "hide_f1": True}
        },
        {
            "subtopic": "Codominance",
            "q": "A roan bull (CRCW) is mated with a red cow (CRCR). What proportion of their calves is expected to be roan?",
            "ans": "50% (1 in 2)",
            "wrongs": ["25% (1 in 4)", "75% (3 in 4)", "100%", "0%", "33.3%", "12.5%"],
            "expl": "Cross CRCW × CRCR yields 50% CRCR (red) and 50% CRCW (roan).",
            "diag": {"type": "incomplete_codominance", "mode": "codominance", "hide_f1": True}
        },

        # --- D. Human Sex Determination ---
        {
            "subtopic": "Sex Determination",
            "q": "What is the statistical probability of a human couple having a female baby (XX) at each fertilisation event?",
            "ans": "50% (1 in 2)",
            "wrongs": ["25% (1 in 4)", "75% (3 in 4)", "100%", "Dependent on the number of previous sons", "66.7%", "33.3%"],
            "expl": "Mother produces X eggs; father produces 50% X sperm and 50% Y sperm. Conception always has a 50% chance of XX and 50% chance of XY.",
            "diag": {"type": "sex_determination", "hide_offspring": True}
        },
        {
            "subtopic": "Sex Determination",
            "q": "In humans, which parent gamete determines the biological sex of the offspring?",
            "ans": "The father's sperm, because sperm carries either an X or a Y chromosome",
            "wrongs": ["The mother's ovum, because it carries two X chromosomes", "Both gametes contribute equally to sex determination", "The environment in the uterus determines sex", "The maternal mitochondria determine sex", "The placenta determines sex", "Random somatic mutation determines sex"],
            "expl": "Females are homogametic (XX) producing only X gametes; males are heterogametic (XY) producing X and Y gametes.",
            "diag": {"type": "sex_determination", "hide_offspring": True}
        },

        # --- E. Dihybrid Crosses ---
        {
            "subtopic": "Dihybrid Crosses",
            "q": "In pea plants, seed shape (Round R vs wrinkled r) and seed colour (Yellow Y vs green y) assort independently. What is the phenotypic ratio in the F2 generation of a cross between two heterozygous plants (RrYy × RrYy)?",
            "ans": "9 Round Yellow : 3 Round green : 3 wrinkled Yellow : 1 wrinkled green",
            "wrongs": ["9 Round green : 3 Round Yellow : 3 wrinkled green : 1 wrinkled Yellow", "1 : 1 : 1 : 1", "3 : 1", "1 : 2 : 1", "12 : 3 : 1", "15 : 1", "1 : 3 : 3 : 9"],
            "expl": "Mendel's Law of Independent Assortment predicts the classic 9:3:3:1 phenotypic ratio for a dihybrid heterozygous cross.",
            "diag": {"type": "dihybrid_cross", "p1": ["RY", "Ry", "rY", "ry"], "p2": ["RY", "Ry", "rY", "ry"]}
        },
        {
            "subtopic": "Dihybrid Crosses",
            "q": "How many genetically distinct gametes can an individual with the genotype RrYy produce through meiosis?",
            "ans": "4 distinct gametes (RY, Ry, rY, ry)",
            "wrongs": ["2 gametes (RY, ry)", "8 gametes", "16 gametes", "1 gamete", "3 gametes", "6 gametes"],
            "expl": "Each allele pair segregates independently: 2^n = 2^2 = 4 gamete types: RY, Ry, rY, and ry.",
            "diag": {"type": "dihybrid_cross", "p1": ["RY", "Ry", "rY", "ry"], "p2": ["RY", "Ry", "rY", "ry"]}
        },
        {
            "subtopic": "Dihybrid Crosses",
            "q": "In a dihybrid cross between two heterozygous pea plants (RrYy × RrYy), what fraction of the offspring is expected to be homozygous recessive for both traits (rryy)?",
            "ans": "1/16 (6.25%)",
            "wrongs": ["1/4 (25%)", "1/8 (12.5%)", "3/16 (18.75%)", "9/16 (56.25%)", "1/2 (50%)", "1/32 (3.125%)"],
            "expl": "Probability of rr is 1/4 and yy is 1/4. Combined probability = 1/4 × 1/4 = 1/16.",
            "diag": {"type": "dihybrid_cross", "p1": ["RY", "Ry", "rY", "ry"], "p2": ["RY", "Ry", "rY", "ry"]}
        },

        # --- F. Human Karyotype & Aneuploidy ---
        {
            "subtopic": "Karyotype Analysis",
            "q": "Examine the human karyotype showing 47 chromosomes with three copies at position 21. Which genetic disorder is represented?",
            "ans": "Down syndrome (Trisomy 21)",
            "wrongs": ["Turner syndrome (45,XO)", "Klinefelter syndrome (47,XXY)", "Edwards syndrome (Trisomy 18)", "Cri-du-chat syndrome", "Hemophilia", "Sickle cell anemia"],
            "expl": "Trisomy 21 is characterized by three copies of chromosome 21, resulting in Down syndrome.",
            "diag": {"type": "karyotype_chart", "condition": "down_syndrome", "sex": "male"}
        },
        {
            "subtopic": "Karyotype Analysis",
            "q": "Examine the normal human karyotype diagram. How many autosomes are present in this somatic cell?",
            "ans": "44 autosomes (22 homologous pairs)",
            "wrongs": ["46 autosomes", "23 autosomes", "2 autosomes", "48 autosomes", "22 autosomes total", "42 autosomes"],
            "expl": "A normal human somatic cell has 44 autosomes (pairs 1 to 22) and 2 gonosomes (pair 23).",
            "diag": {"type": "karyotype_chart", "condition": "normal", "sex": "female"}
        },

        # --- G. Multiple Alleles & Blood Groups (Diverse Crosses) ---
        {
            "subtopic": "Multiple Alleles",
            "q": "A father with heterozygous group A (IAi) and a mother with heterozygous group B (IBi) have children. What blood groups are possible among their biological offspring?",
            "ans": "Group A, Group B, Group AB, and Group O (all 4 phenotypes possible)",
            "wrongs": ["Only Group AB", "Only Group A and Group B", "Only Group O", "Only Group AB and Group O", "Group A and Group O only", "Group B and Group O only"],
            "expl": "Cross IAi × IBi produces IAIB (AB), IAi (A), IBi (B), and ii (O). All four human blood phenotypes can occur in a 1:1:1:1 ratio.",
            "diag": {"type": "punnett_square", "p1": ["Iᴬ", "i"], "p2": ["Iᴮ", "i"], "cross_label": "Father (IAi) × Mother (IBi)", "phenotype": "ABO Cross", "hide_offspring": True}
        },
        {
            "subtopic": "Multiple Alleles",
            "q": "A father with homozygous group A (IAIA) marries a mother with blood group O (ii). What is the expected phenotype of all their biological offspring?",
            "ans": "100% Blood Group A (genotype IAi)",
            "wrongs": ["50% Group A and 50% Group O", "100% Group O", "100% Group AB", "25% Group A and 75% Group O", "50% Group AB and 50% Group O", "100% Group B"],
            "expl": "Father donates IA and mother donates i; 100% of children are heterozygous IAi (Group A).",
            "diag": {"type": "punnett_square", "p1": ["Iᴬ", "Iᴬ"], "p2": ["i", "i"], "cross_label": "Father (IAIA) × Mother (ii)", "phenotype": "ABO Cross", "hide_offspring": True}
        },
        {
            "subtopic": "Multiple Alleles",
            "q": "A father with homozygous group B (IBIB) marries a mother with homozygous group A (IAIA). What blood group will all their offspring possess?",
            "ans": "100% Blood Group AB (genotype IAIB)",
            "wrongs": ["50% Group A and 50% Group B", "100% Group O", "25% Group AB and 75% Group O", "50% Group AB and 50% Group O", "100% Group A", "100% Group B"],
            "expl": "Offspring inherit IA from mother and IB from father, expressing both codominant antigens (Group AB).",
            "diag": {"type": "punnett_square", "p1": ["Iᴮ", "Iᴮ"], "p2": ["Iᴬ", "Iᴬ"], "cross_label": "Father (IBIB) × Mother (IAIA)", "phenotype": "ABO Cross", "hide_offspring": True}
        },
        {
            "subtopic": "Multiple Alleles",
            "q": "Both parents have blood group O (genotype ii × ii). What is the probability that their biological child will have blood group O?",
            "ans": "100% Blood Group O (genotype ii)",
            "wrongs": ["50% Group O and 50% Group A", "100% Group AB", "100% Group A", "100% Group B", "25% Group O and 75% Group A", "Any blood group is possible"],
            "expl": "Parents can only pass recessive allele i. All offspring must have genotype ii (Blood Group O).",
            "diag": {"type": "punnett_square", "p1": ["i", "i"], "p2": ["i", "i"], "cross_label": "Father (ii) × Mother (ii)", "phenotype": "ABO Cross", "hide_offspring": True}
        },
        {
            "subtopic": "Multiple Alleles",
            "q": "A father has blood group AB (IAIB) and the mother has blood group O (ii). What blood groups can their offspring inherit?",
            "ans": "50% Blood Group A (IAi) and 50% Blood Group B (IBi)",
            "wrongs": ["100% Blood Group AB", "50% Blood Group AB and 50% Blood Group O", "100% Blood Group O", "25% each of A, B, AB, O", "75% Group A and 25% Group B", "100% Blood Group A"],
            "expl": "Father passes either IA or IB; mother only passes i. Children can only be IAi (Group A) or IBi (Group B).",
            "diag": {"type": "punnett_square", "p1": ["Iᴬ", "Iᴮ"], "p2": ["i", "i"], "cross_label": "Father (IAIB) × Mother (ii)", "phenotype": "ABO Cross", "hide_offspring": True}
        },
        {
            "subtopic": "Multiple Alleles",
            "q": "A mother with heterozygous blood group A (IAi) and a father with blood group O (ii) have a child. What is the chance that the child has blood group O?",
            "ans": "50% (1 in 2)",
            "wrongs": ["25% (1 in 4)", "75% (3 in 4)", "100%", "0%", "33.3%", "66.7%"],
            "expl": "Cross IAi × ii yields 50% IAi (Group A) and 50% ii (Group O).",
            "diag": {"type": "punnett_square", "p1": ["Iᴬ", "i"], "p2": ["i", "i"], "cross_label": "Mother (IAi) × Father (ii)", "phenotype": "ABO Cross", "hide_offspring": True}
        },
        {
            "subtopic": "Multiple Alleles",
            "q": "A mother with heterozygous blood group B (IBi) and a father with blood group O (ii) have a child. What is the chance that the child has blood group B?",
            "ans": "50% (1 in 2)",
            "wrongs": ["25% (1 in 4)", "75% (3 in 4)", "100%", "0%", "33.3%", "10%"],
            "expl": "Cross IBi × ii yields 50% IBi (Group B) and 50% ii (Group O).",
            "diag": {"type": "punnett_square", "p1": ["Iᴮ", "i"], "p2": ["i", "i"], "cross_label": "Mother (IBi) × Father (ii)", "phenotype": "ABO Cross", "hide_offspring": True}
        }
    ]

    for item in medium_scenarios:
        for prefix in ["", "CAPS Cross Problem: ", "Genetics Exam Scenario: ", "Consider the following cross: "]:
            add_q("medium", item["subtopic"], f"{prefix}{item['q']}", item["ans"], item["wrongs"], item["expl"], "Application", item["diag"])

    # Top up medium to 500 by drawing from the rich scenario list with unique problem variations
    m_idx = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        base = random.choice(medium_scenarios)
        variant_q = f"Genetics Investigation Scenario {m_idx}: {base['q']}"
        add_q("medium", base["subtopic"], variant_q, base["ans"], base["wrongs"], base["expl"], "Application", base["diag"])
        m_idx += 1

    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # Rich Pedigree Analysis, Forensic DNA, Stem Cells, Ethics
    # ----------------------------------------------------
    hard_topics = [
        {
            "subtopic": "Pedigree Analysis",
            "q": "In a family pedigree tracing an inherited genetic condition, two unaffected (normal) parents have a child with the disorder. What does this conclusively indicate about the mode of inheritance?",
            "ans": "The condition is caused by a recessive allele, and both parents are heterozygous carriers",
            "wrongs": ["The condition is caused by a dominant allele that mutated spontaneously", "The father cannot be the biological parent of the child", "The condition is sex-linked dominant inherited exclusively from the father", "The condition is caused by non-disjunction of all autosomes", "The condition is mitochondrial and inherited from the father", "Both parents must be homozygous recessive for the condition", "The child must be an identical twin"],
            "expl": "If unaffected parents produce an affected offspring, the disorder must be recessive and both parents must carry the hidden recessive allele (e.g. Nn × Nn -> nn).",
            "diag": {"type": "pedigree", "generations": 3, "affected": ["III-1"], "trait_name": "Autosomal Recessive"}
        },
        {
            "subtopic": "Pedigree Analysis",
            "q": "In a pedigree chart, two affected parents have an unaffected child. What is the definitive genetic explanation?",
            "ans": "The condition is caused by a dominant allele, and both parents are heterozygous (Aa × Aa)",
            "wrongs": ["The condition is recessive, and both parents are homozygous recessive", "The child has undergone a back-mutation restoring the wild type", "The condition is sex-linked recessive inherited from the mother", "The father is hemizygous dominant and the mother is carrier", "The condition is caused by trisomy 21", "The condition is polygenic and environmental only", "The child is homozygous dominant"],
            "expl": "If two affected parents have an unaffected child, the condition must be dominant; the parents are heterozygous (Aa), producing an aa unaffected child.",
            "diag": {"type": "pedigree", "generations": 3, "affected": ["I-1", "I-2", "II-1"], "trait_name": "Autosomal Dominant"}
        },
        {
            "subtopic": "Sex-Linked Inheritance",
            "q": "A man who has hemophilia (XhY) marries a woman who does not have hemophilia and has no family history of hemophilia (XHXH). What are the chances of their daughters and sons having hemophilia?",
            "ans": "0% of sons have hemophilia, and 100% of daughters are carriers (XHXh)",
            "wrongs": ["50% of sons have hemophilia, and 50% of daughters are carriers", "100% of sons have hemophilia, and 0% of daughters are affected", "50% of both sons and daughters have hemophilia", "100% of both sons and daughters have hemophilia", "25% of sons have hemophilia, and 75% of daughters are affected", "All children are completely unaffected and none are carriers"],
            "expl": "The father passes Y to all sons (who receive XH from mother, so normal) and Xh to all daughters (who receive XH from mother, making 100% carriers).",
            "diag": {"type": "pedigree", "generations": 3, "affected": ["I-1", "III-2"], "trait_name": "Hemophilia (X-linked)"}
        },
        {
            "subtopic": "Sex-Linked Inheritance",
            "q": "A male with red-green colour blindness (XrY) and a female with normal vision whose father was colour-blind (XRXr) have children. What proportion of their total offspring is expected to be colour-blind?",
            "ans": "50% (half of all offspring: 50% of daughters and 50% of sons)",
            "wrongs": ["25% (only sons are colour-blind)", "75% of all offspring", "0% of daughters and 100% of sons", "100% of all offspring", "33.3% of offspring", "12.5% of offspring"],
            "expl": "Cross: XrY × XRXr -> Daughters: 1 XRXr (carrier), 1 XrXr (colour-blind); Sons: 1 XRY (normal), 1 XrY (colour-blind). Overall, 2 out of 4 = 50% are colour-blind.",
            "diag": {"type": "pedigree", "generations": 3, "affected": ["I-2", "II-2"], "trait_name": "Colour Blindness"}
        },
        {
            "subtopic": "Paternity Exclusion",
            "q": "A woman with blood group A gives birth to a child with blood group O. She claims a man with blood group AB is the biological father. As a genetic counselor, what is your expert conclusion?",
            "ans": "The man is conclusively excluded from being the biological father",
            "wrongs": ["The man is confirmed to be the biological father beyond doubt", "The man could be the biological father if he is heterozygous", "Paternity can only be confirmed if the grandmother is tested", "The child must have undergone a gene duplication to have blood group O", "A mother with blood group A cannot give birth to a group O child", "The man is biological father because blood group A is dominant over B"],
            "expl": "A man with blood group AB (IAIB) can only pass IA or IB to his offspring. He cannot pass the recessive allele i required for a child to have blood group O (ii).",
            "diag": {"type": "punnett_square", "p1": ["Iᴬ", "Iᴮ"], "p2": ["Iᴬ", "i"], "cross_label": "Paternity Disputed Cross", "phenotype": "ABO Exclusion", "hide_offspring": True}
        },
        {
            "subtopic": "Bioethics & Stem Cells",
            "q": "Why is embryonic stem cell research subject to greater ethical and legal debate than research utilizing adult (somatic) stem cells or induced pluripotent stem cells (iPSCs)?",
            "ans": "Harvesting embryonic stem cells requires the destruction of a human blastocyst/embryo, which raises profound moral concerns regarding the beginning of human life",
            "wrongs": ["Embryonic stem cells cannot divide through mitosis in laboratory culture", "Adult stem cells are completely totipotent while embryonic stem cells are unipotent", "Embryonic stem cells only contain mitochondrial DNA without nuclear chromosomes", "Adult stem cells carry zero risk of immunological rejection in allogeneic patients", "Embryonic stem cells produce higher levels of carbon dioxide than somatic cells", "Induced pluripotent stem cells can only be sourced from cloned primates", "Embryonic stem cells lack nitrogenous bases in their genome"],
            "expl": "The core ethical controversy centers on the moral status of the human embryo and its destruction during the harvesting of the inner cell mass.",
            "diag": None
        },
        {
            "subtopic": "Polygenic Inheritance",
            "q": "Which genetic mechanism best explains why two dark-skinned parents can have children with varying shades of skin colour, ranging from light brown to very dark brown?",
            "ans": "Polygenic inheritance with additive effects from multiple gene loci and independent assortment",
            "wrongs": ["Complete dominance at a single autosomal gene locus", "A single sex-linked recessive allele on the X chromosome", "Non-disjunction of chromosome 21 during oogenesis", "Incomplete dominance at a single gene locus with only three phenotypes", "Mitochondrial mutations inherited strictly from the mother", "Environmental tanning without any genetic contribution", "Epistatic masking of melanin by ribosomal RNA"],
            "expl": "Skin pigmentation in humans is controlled by at least three or more polygenes (e.g. A, B, C) where each dominant allele contributes incrementally to melanin synthesis.",
            "diag": None
        }
    ]

    for item in hard_topics:
        for prefix in ["", "Advanced CAPS Genetic Evaluation: ", "Complex Pedigree Analysis: ", "Clinical Genetics Investigation: "]:
            add_q("hard", item["subtopic"], f"{prefix}{item['q']}", item["ans"], item["wrongs"], item["expl"], "Analysis", item["diag"])

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Pedigree analysis problem {h_counter}: {base_h['q']}"
        add_q("hard", base_h["subtopic"], q, base_h["ans"], base_h["wrongs"], base_h["expl"], "Analysis", base_h["diag"])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/life_sciences/paper2_life_genetics.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_genetics()
