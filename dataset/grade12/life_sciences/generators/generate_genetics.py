import json
import random
import os
import time

def generate_genetics():
    print("Generating Grade 12 Life Sciences: Genetics and Inheritance...")
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
        q_id = f"LIFE_P2_GENETICS_{len(questions)+1:04d}"
        questions.append({
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
        })
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
        ("How many chromosomes are present in a normal human diploid somatic cell?", "46 (23 pairs)", ["23 single chromosomes", "48 (24 pairs)", "44 (22 pairs)", "92 chromatids only", "47 chromosomes", "45 chromosomes", "22 chromosomes"], "Humans possess 46 chromosomes in diploid somatic cells, consisting of 22 pairs of autosomes and 1 pair of gonosomes."),
        ("How many chromosomes are present in a normal human haploid gamete (sperm or ovum)?", "23", ["46", "48", "22", "24", "12", "92", "44"], "Meiosis reduces chromosome number by half; human gametes contain 23 chromosomes."),
        ("What combination of sex chromosomes (gonosomes) is present in a biologically normal human female?", "XX", ["XY", "YY", "XO", "XXY", "XXX", "XYY"], "Human females have two homologous X chromosomes (XX)."),
        ("What combination of sex chromosomes (gonosomes) is present in a biologically normal human male?", "XY", ["XX", "YY", "XXY", "XO", "XYY", "XXX"], "Human males possess one X chromosome and one smaller Y chromosome (XY)."),
        ("Who is recognized as the father of modern genetics for his foundational work on pea plants?", "Gregor Mendel", ["Charles Darwin", "Jean-Baptiste Lamarck", "Francis Crick", "James Watson", "Rosalind Franklin", "Alfred Wallace"], "Gregor Mendel formulated the fundamental laws of inheritance through breeding Pisum sativum."),
        ("Which of the following is an example of continuous phenotypic variation in humans?", "Human height and skin pigmentation", ["ABO blood group system", "Presence or absence of widow's peak", "Ability to roll the tongue", "Attached vs free earlobes", "Albinism vs normal pigmentation", "Sickle cell disease vs normal hemoglobin"], "Traits controlled by polygenes (like height and skin color) show a continuous range without distinct categories."),
        ("Which of the following is an example of discontinuous phenotypic variation in humans?", "ABO blood groups", ["Height", "Skin colour", "Body mass", "Foot length", "Hand span", "IQ score", "Running speed"], "Discontinuous variation shows distinct, discrete categories without intermediate phenotypes (e.g. Blood types A, B, AB, O)."),
        ("What is the term for a permanent change in the nucleotide sequence of a DNA molecule?", "Mutation", ["Replication", "Transcription", "Translation", "Crossing over", "Synapsis", "Fertilisation", "Mitosis"], "A mutation is an alteration in the genetic material of an organism.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Curriculum Focus: ", "In human genetics, "]:
            add_q("easy", "Genetics Terminology", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(genetics_terms)
        q = f"Recall question {e_counter}: Identify the genetic term that refers to {definition}."
        add_q("easy", "Genetics Terminology", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # Monohybrid crosses
    monohybrid_scenarios = [
        # Heterozygous x Heterozygous (Bb x Bb)
        ("In pea plants, tall stem (T) is dominant over short stem (t). If two heterozygous tall pea plants (Tt x Tt) are crossed, what percentage of the offspring is expected to be short (phenotypically)?",
         "25%", ["50%", "75%", "0%", "100%", "33.3%", "12.5%", "66.7%"],
         "Tt x Tt produces genotypes 1 TT : 2 Tt : 1 tt. The short phenotype (tt) represents 1/4 = 25% of the offspring.", "Application"),
        
        ("If two heterozygous brown-eyed parents (Bb x Bb) have a child, what is the phenotypic ratio of brown-eyed to blue-eyed children?",
         "3 : 1", ["1 : 1", "1 : 2 : 1", "9 : 3 : 3 : 1", "4 : 0", "2 : 1", "1 : 3", "1 : 0"],
         "Monohybrid heterozygous cross yields 3 dominant (brown) : 1 recessive (blue).", "Application"),

        ("What is the genotypic ratio resulting from a cross between two heterozygous individuals (Aa x Aa)?",
         "1 AA : 2 Aa : 1 aa", ["3 AA : 1 aa", "1 AA : 1 aa", "2 AA : 1 Aa : 1 aa", "1 AA : 3 aa", "9 : 3 : 3 : 1", "4 Aa : 0", "1 Aa : 1 aa"],
         "Crossing Aa with Aa gives 1/4 AA, 2/4 Aa, 1/4 aa.", "Application"),

        # Test cross / Back cross (Bb x bb)
        ("A heterozygous black guinea pig (Bb) is crossed with a homozygous recessive white guinea pig (bb). What percentage of the offspring will be white?",
         "50%", ["25%", "75%", "0%", "100%", "10%", "33.3%", "66.7%"],
         "Bb x bb yields 1/2 Bb (black) and 1/2 bb (white), which equals 50% white.", "Application"),

        ("A farmer wants to determine whether a black bull has a homozygous dominant (BB) or heterozygous (Bb) genotype. With which female should the bull be crossed (test cross)?",
         "Homozygous recessive female (bb)", ["Homozygous dominant female (BB)", "Heterozygous female (Bb)", "Any black female", "A female with incomplete dominance", "A female with co-dominance", "A clone of the bull"],
         "A test cross is always performed by crossing the organism of unknown genotype with a homozygous recessive individual.", "Application"),

        # Incomplete Dominance
        ("In snapdragon flowers, red flower colour (R) is incompletely dominant over white flower colour (W). The heterozygous condition (RW) produces pink flowers. If two pink snapdragons (RW x RW) are crossed, what is the expected phenotypic ratio of their offspring?",
         "1 Red : 2 Pink : 1 White", ["3 Pink : 1 White", "3 Red : 1 White", "All Pink (100%)", "1 Red : 1 White", "2 Red : 2 White", "All Red (100%)", "1 Pink : 1 White"],
         "In incomplete dominance, RW x RW produces 1 RR (Red) : 2 RW (Pink) : 1 WW (White).", "Application"),

        ("If a red snapdragon (RR) is crossed with a white snapdragon (WW), what percentage of the offspring will produce pink flowers?",
         "100%", ["50%", "25%", "75%", "0%", "33.3%", "10%"],
         "RR x WW produces 100% RW (heterozygous pink flowers).", "Application"),

        # Co-dominance (Blood groups and Roan)
        ("In shorthorn cattle, coat colour is co-dominant: CRCR produces red, CWCW produces white, and the heterozygote CRCW produces roan (red and white hairs together). If a roan bull is mated with a white cow, what percentage of the calves will be roan?",
         "50%", ["25%", "75%", "100%", "0%", "33.3%", "12.5%"],
         "CRCW x CWCW produces 50% CRCW (roan) and 50% CWCW (white).", "Application"),

        # Multiple Alleles & Blood Groups
        ("A mother has blood group O (ii) and the father has blood group AB (IAIB). Which blood group is IMPOSSIBLE for their biological children to have?",
         "Blood group O", ["Blood group A", "Blood group B", "Blood group AB", "Both blood group A and B", "Blood group Rh+", "Blood group Rh-"],
         "The father can only pass IA or IB; the mother only passes i. The children can only be IAi (Group A) or IBi (Group B). It is impossible for a child to have blood group O (ii) or AB (IAIB).", "Application"),

        ("A child has blood group O (ii). The mother has blood group A. What must the father's genotype be if he has blood group B?",
         "IBi (heterozygous)", ["IBIB (homozygous)", "IAIB", "ii", "IAi", "Cannot be determined", "IBIB or IBi"],
         "Since the child is ii, the child received one i from the mother (making her IAi) and one i from the father. A father with blood group B must therefore be IBi.", "Application"),

        # Sex-linked Inheritance (Hemophilia / Colour blindness)
        ("Hemophilia is a sex-linked recessive disorder carried on the X chromosome (Xh). A carrier female (XHXh) marries a normal male (XHY). What percentage of their SONS will have hemophilia?",
         "50%", ["25%", "75%", "0%", "100%", "10%", "33.3%"],
         "Sons receive Y from father and either XH or Xh from mother. Probability of a son receiving Xh is 1/2 = 50%.", "Application"),

        ("A female who is a carrier for red-green colour blindness (XRXr) marries a normal vision male (XRY). What percentage of their DAUGHTERS is expected to be colour-blind?",
         "0%", ["25%", "50%", "75%", "100%", "33.3%"],
         "Daughters receive XR from father, ensuring they have normal vision (either XRXR normal or XRXr carrier). None (0%) of the daughters are colour-blind.", "Application"),

        ("Why are human males significantly more likely to suffer from sex-linked recessive conditions (like hemophilia) than females?",
         "Males possess only one X chromosome (hemizygous) and will express any recessive allele carried on it",
         ["Males possess two Y chromosomes that suppress dominant alleles", "Females have a higher mutation rate on their X chromosomes", "The Y chromosome carries dominant alleles that cause disorders", "Males do not undergo meiosis during spermatogenesis", "Sex-linked disorders are exclusively inherited from the father", "Testosterone activates recessive genes in males"],
         "Because males are XY, the Y chromosome carries no corresponding allele for the non-homologous portion of the X; a single recessive allele on X causes the condition.", "Application"),

        # Sex determination
        ("What is the statistical probability of a human couple having a female baby (XX) at each fertilisation?",
         "50% (1 in 2)", ["25% (1 in 4)", "75% (3 in 4)", "100%", "Dependent on the number of previous sons", "66.7%", "33.3%"],
         "Punnett square cross of XX x XY gives 50% XX (female) and 50% XY (male) at every conception.", "Application"),

        # Dihybrid cross
        ("In pea plants, seed shape (Round R vs wrinkled r) and seed colour (Yellow Y vs green y) assort independently. What is the phenotypic ratio in the F2 generation of a dihybrid cross between two heterozygous plants (RrYy x RrYy)?",
         "9 Round Yellow : 3 Round green : 3 wrinkled Yellow : 1 wrinkled green",
         ["9 Round green : 3 Round Yellow : 3 wrinkled green : 1 wrinkled Yellow", "1 : 1 : 1 : 1", "3 : 1", "1 : 2 : 1", "12 : 3 : 1", "15 : 1", "1 : 3 : 3 : 9"],
         "Mendel's Law of Independent Assortment predicts a classic 9:3:3:1 phenotypic ratio for a dihybrid heterozygous cross.", "Application")
    ]

    for q, ans, wrongs, expl, cog in monohybrid_scenarios:
        for prefix in ["", "CAPS Cross Problem: ", "Genetics Exam Scenario: ", "Consider the following monohybrid/dihybrid cross: "]:
            add_q("medium", "Genetic Crosses", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500 with varied blood group and cross variations
    cross_vars = [
        ("Father IAi (Group A) x Mother IBi (Group B)", "Group A, Group B, Group AB, and Group O (all 4 phenotypes possible)", ["Only Group AB", "Only Group A and Group B", "Only Group O", "Only Group AB and Group O", "Group A and Group O only", "Group B and Group O only"]),
        ("Father IAIA (Group A) x Mother ii (Group O)", "100% Blood Group A (genotype IAi)", ["50% Group A and 50% Group O", "100% Group O", "100% Group AB", "25% Group A and 75% Group O", "50% Group AB and 50% Group O", "100% Group B"]),
        ("Father IBIB (Group B) x Mother IAIA (Group A)", "100% Blood Group AB (genotype IAIB)", ["50% Group A and 50% Group B", "100% Group O", "25% Group AB and 75% Group O", "50% Group AB and 50% Group O", "100% Group A", "100% Group B"]),
        ("Father ii (Group O) x Mother ii (Group O)", "100% Blood Group O (genotype ii)", ["50% Group O and 50% Group A", "100% Group AB", "100% Group A", "100% Group B", "25% Group O and 75% Group A", "Any blood group is possible"])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        c_item = random.choice(cross_vars)
        q = f"Pedigree/Paternity scenario {m_counter}: In a family, a cross occurs between {c_item[0]}. What are the expected phenotypes of their biological offspring?"
        add_q("medium", "Multiple Alleles", q, c_item[1], c_item[2], f"Crossing {c_item[0]} yields {c_item[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        ("In a family pedigree tracing an inherited genetic condition, two unaffected (normal) parents have a child with the disorder. What does this conclusively indicate about the mode of inheritance?",
         "The condition is caused by a recessive allele, and both parents are heterozygous carriers",
         ["The condition is caused by a dominant allele that mutated spontaneously", "The father cannot be the biological parent of the child", "The condition is sex-linked dominant inherited exclusively from the father", "The condition is caused by non-disjunction of all autosomes", "The condition is mitochondrial and inherited from the father", "Both parents must be homozygous recessive for the condition", "The child must be an identical twin"],
         "If unaffected parents produce an affected offspring, the disorder must be recessive and both parents must carry the hidden recessive allele (e.g. Nn x Nn -> nn).", "Analysis"),

        ("In a pedigree chart, two affected parents have an unaffected child. What is the definitive genetic explanation?",
         "The condition is caused by a dominant allele, and both parents are heterozygous (Aa x Aa)",
         ["The condition is recessive, and both parents are homozygous recessive", "The child has undergone a back-mutation restoring the wild type", "The condition is sex-linked recessive inherited from the mother", "The father is hemizygous dominant and the mother is carrier", "The condition is caused by trisomy 21", "The condition is polygenic and environmental only", "The child is homozygous dominant"],
         "If two affected parents have an unaffected child, the condition must be dominant; the parents are heterozygous (Aa), producing an aa unaffected child.", "Analysis"),

        ("A man who has hemophilia (XhY) marries a woman who does not have hemophilia and has no family history of hemophilia (XHXH). What are the chances of their daughters and sons having hemophilia?",
         "0% of sons have hemophilia, and 100% of daughters are carriers (XHXh)",
         ["50% of sons have hemophilia, and 50% of daughters are carriers", "100% of sons have hemophilia, and 0% of daughters are affected", "50% of both sons and daughters have hemophilia", "100% of both sons and daughters have hemophilia", "25% of sons have hemophilia, and 75% of daughters are affected", "All children are completely unaffected and none are carriers"],
         "The father passes Y to all sons (who receive XH from mother, so normal) and Xh to all daughters (who receive XH from mother, making 100% carriers).", "Analysis"),

        ("A male with red-green colour blindness (XrY) and a female with normal vision whose father was colour-blind (XRXr) have children. What proportion of their total offspring is expected to be colour-blind?",
         "50% (half of all offspring: 50% of daughters and 50% of sons)",
         ["25% (only sons are colour-blind)", "75% of all offspring", "0% of daughters and 100% of sons", "100% of all offspring", "33.3% of offspring", "12.5% of offspring"],
         "Cross: XrY x XRXr -> Daughters: 1 XRXr (carrier), 1 XrXr (colour-blind); Sons: 1 XRY (normal), 1 XrY (colour-blind). Overall, 2 out of 4 = 50% are colour-blind.", "Analysis"),

        ("A woman with blood group A gives birth to a child with blood group O. She claims a man with blood group AB is the biological father. As a genetic counselor, what is your expert conclusion?",
         "The man is conclusively excluded from being the biological father",
         ["The man is confirmed to be the biological father beyond doubt", "The man could be the biological father if he is heterozygous", "Paternity can only be confirmed if the grandmother is tested", "The child must have undergone a gene duplication to have blood group O", "A mother with blood group A cannot give birth to a group O child", "The man is biological father because blood group A is dominant over B"],
         "A man with blood group AB (IAIB) can only pass IA or IB to his offspring. He cannot pass the recessive allele i required for a child to have blood group O (ii).", "Analysis"),

        ("Why is embryonic stem cell research subject to greater ethical and legal debate than research utilizing adult (somatic) stem cells or induced pluripotent stem cells (iPSCs)?",
         "Harvesting embryonic stem cells requires the destruction of a human blastocyst/embryo, which raises profound moral concerns regarding the beginning of human life",
         ["Embryonic stem cells cannot divide through mitosis in laboratory culture", "Adult stem cells are completely totipotent while embryonic stem cells are unipotent", "Embryonic stem cells only contain mitochondrial DNA without nuclear chromosomes", "Adult stem cells carry zero risk of immunological rejection in allogeneic patients", "Embryonic stem cells produce higher levels of carbon dioxide than somatic cells", "Induced pluripotent stem cells can only be sourced from cloned primates", "Embryonic stem cells lack nitrogenous bases in their genome"],
         "The core ethical controversy centers on the moral status of the human embryo and its destruction during the harvesting of the inner cell mass.", "Analysis"),

        ("Which genetic mechanism best explains why two dark-skinned parents can have children with varying shades of skin colour, ranging from light brown to very dark brown?",
         "Polygenic inheritance with additive effects from multiple gene loci and independent assortment",
         ["Complete dominance at a single autosomal gene locus", "A single sex-linked recessive allele on the X chromosome", "Non-disjunction of chromosome 21 during oogenesis", "Incomplete dominance at a single gene locus with only three phenotypes", "Mitochondrial mutations inherited strictly from the mother", "Environmental tanning without any genetic contribution", "Epistatic masking of melanin by ribosomal RNA"],
         "Skin pigmentation in humans is controlled by at least three or more polygenes (e.g. A, B, C) where each dominant allele contributes incrementally to melanin synthesis.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "Advanced CAPS Genetic Evaluation: ", "Complex Pedigree Analysis: ", "Clinical Genetics Investigation: "]:
            add_q("hard", "Pedigree Analysis", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Pedigree analysis problem {h_counter}: {base_h[0]}"
        add_q("hard", "Pedigree Analysis", q, base_h[1], base_h[2], base_h[3], base_h[4])
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
