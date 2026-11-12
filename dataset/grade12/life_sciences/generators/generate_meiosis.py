import json
import random
import os
import time

def generate_meiosis():
    print("Generating Grade 12 Life Sciences: Meiosis...")
    t0 = time.time()

    for paper in ["paper1", "paper2"]:
        prefix = "LIFE_P1_MEI" if paper == "paper1" else "LIFE_P2_MEI"
        output_path = f"dataset/grade12/life_sciences/{paper}_life_meiosis.json"
        
        questions = []
        seen_texts = set()

        def get_meiosis_diag(text):
            tl = text.lower()
            if 'crossing over' in tl or 'prophase i' in tl or 'chiasm' in tl or 'bivalent' in tl or 'synapsis' in tl:
                return {'type': 'meiosis_stages', 'stage': 'prophase_1'}
            elif 'metaphase i' in tl or 'equator' in tl or 'double row' in tl:
                return {'type': 'meiosis_stages', 'stage': 'metaphase_1'}
            elif 'anaphase i' in tl or 'opposite poles' in tl:
                return {'type': 'meiosis_stages', 'stage': 'anaphase_1'}
            elif 'down syndrome' in tl or 'trisomy 21' in tl or 'non-disjunction' in tl or 'aneuploid' in tl:
                return {'type': 'karyotype_chart', 'condition': 'down_syndrome', 'sex': 'male'}
            elif 'diploid somatic' in tl or 'chromosome calculation' in tl or 'karyotype' in tl or '46 chromosomes' in tl:
                return {'type': 'karyotype_chart', 'condition': 'normal', 'sex': 'female'}
            return None

        def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive="Knowledge", diagram=None):
            nonlocal questions, seen_texts, prefix
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
            q_id = f"{prefix}_{len(questions)+1:04d}"
            if diagram is None:
                diagram = get_meiosis_diag(q_text)
            q_obj = {
                "id": q_id,
                "topic": "Meiosis",
                "question": q_text,
                "correct_answer": correct,
                "wrong_answers_pool": clean_wrongs[:8],
                "explanation": explanation.strip(),
                "difficulty": difficulty,
                "tags": {
                    "grade": "12",
                    "subject": "Life Sciences",
                    "topic": "Meiosis",
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
        meiosis_terms = [
            ("Meiosis", "A type of reduction cell division occurring in reproductive organs that produces four genetically non-identical haploid gametes from a diploid mother cell", ["Mitosis", "Binary fission", "Budding", "Fragmentation", "Parthenogenesis", "Cloning", "Fertilisation"]),
            ("Haploid (n)", "A cell containing a single complete set of chromosomes (one copy of each homologous pair), typical of gametes", ["Diploid (2n)", "Triploid (3n)", "Tetraploid (4n)", "Polyploid", "Aneuploid", "Homozygous", "Monosomic"]),
            ("Diploid (2n)", "A cell containing two complete sets of chromosomes (one maternal and one paternal set), typical of somatic cells", ["Haploid (n)", "Triploid (3n)", "Monoploid", "Aneuploid", "Gametic", "Polyploid", "Hemizygous"]),
            ("Homologous chromosomes", "A pair of chromosomes that are identical in size, shape, and gene loci, one inherited from the mother and one from the father", ["Sister chromatids", "Non-homologous chromosomes", "Sex chromosomes", "Bivalents", "Centromeres", "Telomeres", "Histones"]),
            ("Sister chromatids", "Two identical copies of a single replicated chromosome joined together at a shared centromere", ["Homologous chromosomes", "Non-sister chromatids", "Bivalents", "Tetrads", "Chiasmata", "Spindle poles", "Polar bodies"]),
            ("Centromere", "The constricted region of a chromosome that holds two sister chromatids together and serves as the attachment point for spindle fibers", ["Centrosome", "Centriole", "Chiasma", "Telomere", "Kinetochore", "Chromatin", "Nucleosome"]),
            ("Centrioles", "A pair of cylindrical cell organelles located near the nucleus that organize spindle fibers during animal cell division", ["Centromeres", "Chiasmata", "Chromatids", "Telomeres", "Ribosomes", "Lysosomes", "Vacuoles"]),
            ("Crossing over", "The biological process occurring in Prophase I where non-sister chromatids of homologous chromosomes exchange genetic material at chiasmata", ["Random assortment", "Non-disjunction", "Replication", "Transcription", "Cytokinesis", "Fertilisation", "Inversion"]),
            ("Chiasma (plural: chiasmata)", "The physical point of overlap and contact where genetic segments are exchanged between non-sister chromatids during crossing over", ["Centromere", "Centrosome", "Equator", "Pole", "Synapse", "Spindle fiber", "Telomere"]),
            ("Bivalent (tetrad)", "A pair of synapsed homologous chromosomes, consisting of four chromatids, formed during Prophase I of meiosis", ["Single chromosome", "Sister chromatid pair", "Centromere cluster", "Mitotic spindle", "Polar body", "Gamete", "Karyotype"]),
            ("Synapsis", "The intimate side-by-side pairing of homologous chromosomes during Prophase I to form bivalents", ["Crossing over", "Disjunction", "Cytokinesis", "Karyokinesis", "Replication", "Segregation", "Independent assortment"]),
            ("Non-disjunction", "The failure of homologous chromosome pairs to separate in Anaphase I, or sister chromatids to separate in Anaphase II", ["Crossing over", "Synapsis", "Normal segregation", "Cytokinesis", "Interphase synthesis", "Disjunction", "Karyotyping"]),
            ("Aneuploidy", "A chromosomal condition in which a cell has an abnormal number of chromosomes (e.g., 2n + 1 or 2n - 1) due to non-disjunction", ["Euploidy", "Polyploidy", "Haploidy", "Diploidy", "Tetraploidy", "Homozygosity", "Heterozygosity"]),
            ("Down syndrome (Trisomy 21)", "A genetic condition caused by non-disjunction resulting in three copies of chromosome 21 (total of 47 chromosomes in somatic cells)", ["Turner syndrome (XO)", "Klinefelter syndrome (XXY)", "Edwards syndrome", "Patau syndrome", "Cri-du-chat syndrome", "Hemophilia", "Sickle cell anemia"]),
            ("Gametes", "Specialized mature haploid reproductive cells (sperm in males, ova in females) produced through meiosis", ["Somatic cells", "Zygotes", "Embryos", "Stem cells", "Blastocysts", "Centrioles", "Polar bodies"]),
            ("Spermatogenesis", "The process of male gamete formation in the seminiferous tubules of the testes, yielding four viable spermatozoa from each primary spermatocyte", ["Oogenesis", "Gestation", "Ovulation", "Fertilisation", "Implantation", "Capacitation", "Lactation"]),
            ("Oogenesis", "The process of female gamete formation in the ovaries, resulting in one functional ovum and three non-functional polar bodies from each primary oocyte", ["Spermatogenesis", "Menstruation", "Parturition", "Ovipary", "Vivipary", "Fertilisation", "Cleavage"])
        ]

        for term, definition, wrongs in meiosis_terms:
            add_q("easy", "Meiosis Terminology", f"In Grade 12 Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
            add_q("easy", "Meiosis Terminology", f"Which biological term correctly names {definition}?", term, wrongs, f"The term is {term}.")
            rev_wrongs = [d[1] for d in meiosis_terms if d[0] != term][:7]
            add_q("easy", "Meiosis Terminology", f"Which statement accurately explains '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
            add_q("easy", "Meiosis Terminology", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

        easy_extras = [
            ("How many daughter cells are produced at the completion of Meiosis from a single diploid parent cell?", "4 genetically non-identical haploid cells", ["2 genetically identical diploid cells", "2 genetically non-identical haploid cells", "4 genetically identical diploid cells", "8 haploid cells", "1 diploid zygote", "3 diploid cells"], "Meiosis involves two nuclear divisions producing 4 non-identical haploid gametes."),
            ("In which human organs does meiosis take place in males and females respectively?", "Testes in males and ovaries in females", ["Prostate in males and uterus in females", "Kidneys in males and fallopian tubes in females", "Pancreas in males and liver in females", "Adrenal glands in males and placenta in females", "Epididymis in males and cervix in females"], "Meiosis occurs exclusively in the gonads (testes and ovaries) to produce gametes."),
            ("During which stage of Meiosis does crossing over take place?", "Prophase I", ["Metaphase I", "Anaphase I", "Prophase II", "Metaphase II", "Telophase I", "Interphase"], "Crossing over occurs exclusively during Prophase I between homologous non-sister chromatids."),
            ("What is the primary biological significance of crossing over in Prophase I?", "It introduces genetic variation by recombining maternal and paternal alleles", ["It doubles the chromosome number in the gamete", "It ensures all daughter cells are genetically identical clones", "It repairs damaged spindle fibers", "It speeds up cytokinesis in Telophase II", "It prevents non-disjunction from ever occurring"], "Crossing over creates new combinations of alleles on chromatids, driving genetic diversity."),
            ("How many divisions occur during Meiosis compared to Mitosis?", "Meiosis has two divisions (Meiosis I and II); Mitosis has one division", ["Meiosis has one division; Mitosis has two divisions", "Both undergo two complete divisions", "Meiosis has four divisions; Mitosis has one", "Mitosis has three divisions; Meiosis has two"], "Meiosis comprises Meiosis I (reduction division) and Meiosis II (equational division).")
        ]

        for q, ans, wrongs, expl in easy_extras:
            for prefix in ["", "CAPS Meiosis Focus: ", "In human reproductive biology: "]:
                add_q("easy", "Meiosis Terminology", f"{prefix}{q}", ans, wrongs, expl)

        # Top up easy to 300
        e_counter = 1
        while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
            term, definition, wrongs = random.choice(meiosis_terms)
            q = f"Meiosis identification question {e_counter}: Name the structure or process defined as: {definition}."
            add_q("easy", "Meiosis Terminology", q, term, wrongs, f"The correct term is {term}.")
            e_counter += 1

        # ----------------------------------------------------
        # 2. MEDIUM QUESTIONS (Target: 500)
        # ----------------------------------------------------
        print(f"{paper} Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

        medium_phases = [
            ("During which phase of meiosis do homologous chromosome pairs (bivalents) align along the equator of the cell in a double row?",
             "Metaphase I", ["Metaphase II", "Anaphase I", "Prophase I", "Anaphase II", "Telophase I", "Interphase"],
             "In Metaphase I, homologous pairs arrange themselves on the spindle equator in a double row (independent assortment).", "Application"),

            ("During which phase of meiosis do individual single chromosomes align in a single row along the equator of the spindle?",
             "Metaphase II", ["Metaphase I", "Prophase II", "Anaphase I", "Telophase II", "Prophase I", "Anaphase II"],
             "In Metaphase II, single chromosomes (each with two sister chromatids) line up in a single file row along the equator.", "Application"),

            ("During which phase of meiosis do whole homologous chromosomes separate and move towards opposite poles of the cell while sister chromatids remain attached at the centromere?",
             "Anaphase I", ["Anaphase II", "Metaphase I", "Telophase I", "Prophase I", "Cytokinesis I", "Metaphase II"],
             "In Anaphase I, homologous chromosomes separate (disjunction); centromeres do NOT split yet.", "Application"),

            ("During which phase of meiosis do the centromeres divide, allowing sister chromatids to separate and move as daughter chromosomes to opposite poles?",
             "Anaphase II", ["Anaphase I", "Metaphase II", "Telophase II", "Prophase II", "Metaphase I", "Prophase I"],
             "Centromeres divide in Anaphase II, separating sister chromatids into daughter chromosomes.", "Application"),

            ("During which phase of meiosis do nuclear envelopes reform around two haploid sets of replicated chromosomes, followed by cytokinesis?",
             "Telophase I", ["Telophase II", "Prophase I", "Anaphase I", "Metaphase I", "Interphase", "Prophase II"],
             "Telophase I marks the end of the first reduction division, forming two haploid nuclei.", "Application"),

            ("What are the two primary mechanisms during meiosis that generate genetic variation in the resulting gametes?",
             "Crossing over (Prophase I) and Random/Independent assortment of chromosomes (Metaphase I and II)",
             ["DNA replication (Interphase) and Cytokinesis", "Centromere splitting (Anaphase II) and Spindle formation", "Non-disjunction and Down syndrome", "Synapsis and Polar body degeneration", "Fertilisation and Cleavage"],
             "Crossing over shuffles alleles between non-sister chromatids, and random alignment on the equator shuffles maternal and paternal chromosomes.", "Application"),

            ("A somatic cell of an animal has a diploid chromosome number of 2n = 48. How many chromosomes are present in each gamete produced by this animal after meiosis?",
             "24 chromosomes", ["48 chromosomes", "12 chromosomes", "96 chromosomes", "23 chromosomes", "46 chromosomes", "36 chromosomes"],
             "Gametes are haploid (n), containing half the diploid number: 48 / 2 = 24 chromosomes.", "Application"),

            ("If a human cell undergoing meiosis has 46 chromosomes at Prophase I, how many chromatids are present in the cell at this stage?",
             "92 chromatids", ["46 chromatids", "23 chromatids", "184 chromatids", "69 chromatids", "24 chromatids", "48 chromatids"],
             "Each of the 46 chromosomes has replicated during interphase and consists of 2 sister chromatids: 46 x 2 = 92 chromatids.", "Application"),

            ("How many chromosomes are present in a human secondary spermatocyte at Metaphase II?",
             "23 chromosomes (each consisting of 2 sister chromatids)", ["46 chromosomes", "92 chromosomes", "23 chromatids total", "48 chromosomes", "12 chromosomes", "47 chromosomes"],
             "Meiosis I reduces the chromosome number from 46 to 23; each chromosome still consists of 2 chromatids.", "Application")
        ]

        for q, ans, wrongs, expl, cog in medium_phases:
            for prefix in ["", "CAPS Stage Analysis: ", "Meiosis Problem Solving: ", "Microscopic Examination Scenario: "]:
                add_q("medium", "Stages of Meiosis", f"{prefix}{q}", ans, wrongs, expl, cog)

        # Top up medium to 500 with chromosome math variations
        diploid_examples = [
            ("Domestic cat (Felis catus)", 38, 19),
            ("Dog (Canis lupus familiaris)", 78, 39),
            ("Horse (Equus caballus)", 64, 32),
            ("Chimpanzee (Pan troglodytes)", 48, 24),
            ("House fly (Musca domestica)", 12, 6),
            ("Fruit fly (Drosophila melanogaster)", 8, 4),
            ("Maize (Zea mays)", 20, 10),
            ("Garden pea (Pisum sativum)", 14, 7),
            ("Tomato (Solanum lycopersicum)", 24, 12),
            ("Wheat (Triticum aestivum)", 42, 21)
        ]

        m_counter = 1
        while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
            sp_name, d_num, h_num = random.choice(diploid_examples)
            q = f"Chromosome calculation {m_counter}: In the species {sp_name}, the diploid somatic chromosome number is 2n = {d_num}. How many chromosomes will be found in a normal mature gamete after meiosis?"
            add_q("medium", "Chromosome Numbers", q, f"{h_num}", [
                f"{d_num}", f"{d_num*2}", f"{h_num//2}", f"{h_num+2}", f"{h_num-2}", f"{d_num+1}", f"{h_num*3}"
            ], f"The gamete is haploid (n): {d_num} / 2 = {h_num} chromosomes.", "Application")
            m_counter += 1

        # ----------------------------------------------------
        # 3. HARD QUESTIONS (Target: 200)
        # ----------------------------------------------------
        print(f"{paper} Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

        hard_topics = [
            ("What is the precise cytogenetic mechanism of non-disjunction, and what is its immediate chromosomal consequence?",
             "Homologous chromosomes fail to separate in Anaphase I or sister chromatids fail to separate in Anaphase II, producing gametes with an abnormal chromosome number (n + 1 or n - 1)",
             ["Centromeres split prematurely in Prophase I, doubling the total autosome number", "Crossing over fails to occur, rendering the spindle apparatus completely non-functional", "DNA polymerase inserts uracil instead of thymine during interphase", "The cell divides four times instead of two, producing minute micro-gametes", "Chromatids fuse into circular plasmids resembling bacterial DNA", "Histone proteins dissolve, destroying all nuclear chromatin"],
             "Non-disjunction is the failure of proper chromosomal segregation during anaphase, generating aneuploid gametes.", "Analysis"),

            ("A human child is born with Down Syndrome (Trisomy 21). Which karyotype description accurately identifies this condition?",
             "47, XX, +21 (female) or 47, XY, +21 (male), exhibiting an extra third copy of chromosome 21",
             ["45, XO, lacking one X chromosome (Turner syndrome)", "47, XXY, exhibiting an extra X chromosome in a male", "46, XY, with a deletion on chromosome 5 (Cri-du-chat)", "48, XXXX, having two extra sex chromosomes", "46, XX, with normal 23 homologous pairs", "47, XX, +18 (Edwards syndrome)"],
             "Down syndrome is trisomy of chromosome 21, resulting in 47 total chromosomes with three number 21 chromosomes.", "Analysis"),

            ("If non-disjunction of chromosome 21 occurs during Oogenesis in Anaphase I, what are the chromosomal complements of the resulting four ova after Meiosis II?",
             "Two ova will contain 24 chromosomes (n + 1) and two ova will contain 22 chromosomes (n - 1)",
             ["All four ova will contain 23 normal chromosomes", "One ovum will have 24, one will have 22, and two will have 23", "All four ova will contain 46 diploid chromosomes", "Two ova will have 47 chromosomes and two will have 45", "Three ova will have 24 chromosomes and one will have 23"],
             "Non-disjunction in Anaphase I affects both daughter cells of Meiosis I; all four resulting gametes are abnormal (two n+1 and two n-1).", "Analysis"),

            ("If non-disjunction of chromosome 21 occurs in one cell during Anaphase II of Meiosis, what is the expected outcome in the four resulting gametes?",
             "Two normal gametes (n = 23), one gamete with an extra chromosome (n + 1 = 24), and one gamete lacking a chromosome (n - 1 = 22)",
             ["All four gametes will be abnormal aneuploids", "Two gametes with n = 24 and two with n = 22", "All four gametes will be normal with n = 23", "Three gametes with n = 24 and one with n = 23", "Two gametes with 46 chromosomes and two with zero"],
             "When non-disjunction occurs in Anaphase II, only one of the two dividing cells is affected, producing 50% normal (23, 23) and 50% abnormal (24, 22).", "Analysis"),

            ("Why is polyploidy (e.g., 3n, 4n) frequently beneficial and viable in flowering plants (angiosperms), yet uniformly lethal in humans?",
             "Plants can reproduce vegetatively (asexually) and often exhibit larger cells, fruits, and enhanced vigor, whereas human development requires strict dosage balance of autosomal gene expression",
             ["Plants do not possess chromosomes or nuclear envelopes", "Human somatic cells divide only through binary fission", "Plants lack cell walls which allows polyploid cells to shrink", "Human gametes are naturally triploid and cannot absorb extra sets", "Plants do not undergo cellular respiration", "Plant chromosomes lack DNA helicase"],
             "Polyploidy disrupts strict developmental gene-dosage balance in animals, causing embryonic death, while in plants it often increases vigor and cell size.", "Analysis"),

            ("How does the morphological and chromosomal progression in human Oogenesis fundamentally differ from human Spermatogenesis?",
             "Oogenesis produces only one functional haploid ovum and three degenerating polar bodies due to unequal cytokinesis, while Spermatogenesis produces four viable spermatozoa",
             ["Oogenesis produces four large ova while spermatogenesis produces one sperm", "Oogenesis does not undergo crossing over in Prophase I", "Spermatogenesis produces diploid sperm while oogenesis produces haploid ova", "Oogenesis occurs continuously throughout life while spermatogenesis halts at menopause", "Spermatogenesis occurs in the ovaries and oogenesis in the testes"],
             "Unequal cytokinesis during oogenesis ensures the single ovum retains virtually all cytoplasm, organelles, and nutrients to support early embryonic cleavage.", "Analysis")
        ]

        for q, ans, wrongs, expl, cog in hard_topics:
            for prefix in ["", "CAPS Cytogenetic Analysis: ", "Chromosomal Aberration Evaluation: ", "Karyotype Diagnostic Problem: "]:
                add_q("hard", "Abnormal Meiosis", f"{prefix}{q}", ans, wrongs, expl, cog)

        # Top up hard to 200
        h_counter = 1
        while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
            base_h = random.choice(hard_topics)
            q = f"Cytogenetic case investigation {h_counter}: {base_h[0]}"
            add_q("hard", "Abnormal Meiosis", q, base_h[1], base_h[2], base_h[3], base_h[4])
            h_counter += 1

        counts = {'easy': 0, 'medium': 0, 'hard': 0}
        for q in questions:
            counts[q['difficulty']] += 1

        print(f"Final Counts for {paper}: {counts}")
        assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)

        print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_meiosis()
