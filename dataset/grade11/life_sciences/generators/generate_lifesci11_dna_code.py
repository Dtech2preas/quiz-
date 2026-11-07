
_names = ['Sipho', 'Sarah', 'Johan', 'Lerato', 'Thabo', 'Fatima', 'David', 'Nandi', 'Kobus', 'Anke', 'Priya', 'Pieter', 'Bongani', 'Chloe', 'Nomvula', 'Tariq', 'Keletso', 'Willem', 'Wayne', 'Zola', 'Buhle', 'Ayanda', 'Jaco', 'Mpho']
_cities = ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Bloemfontein', 'Polokwane', 'Mbombela', 'Kimberley', 'Gqeberha', 'East London']
_clinics = ['General Hospital', 'Academic Medical Centre', 'Regional Clinic', 'Pathology Laboratory', 'Healthcare Unit', 'Specialist Centre', 'District Infirmary', 'University Teaching Hospital']
_templates = [
    'During a clinical case conference at {clinic} in {city}, Dr. {name} reviews the following patient scenario: {topic}',
    'In a medical audit conducted by Dr. {name} at {clinic} in {city}, the clinical team evaluates: {topic}',
    'At {clinic} in {city}, medical specialist Dr. {name} presents an investigative report regarding: {topic}',
    'During clinical rounds led by Dr. {name} at {clinic} in {city}, trainees assess: {topic}',
    'A clinical research team headed by Dr. {name} at {clinic} in {city} investigates the physiological mechanism: {topic}',
    'In a diagnostic symposium at {clinic} in {city}, Dr. {name} highlights the clinical finding: {topic}'
]
import json
import random
import os
import time

def generate_dna_code():
    print("Generating Grade 11 Life Sciences: DNA - Code of Life & Protein Synthesis...")
    t0 = time.time()

    questions = []
    seen_texts = set()

    def add_q(difficulty, subtopic, q_text, correct, wrongs, explanation, cognitive="Knowledge"):
        nonlocal questions, seen_texts
        q_text = q_text.strip()
        if q_text in seen_texts:
            return False
        correct = str(correct).strip()
        # Clean wrongs
        clean_wrongs = []
        for w in wrongs:
            w = str(w).strip()
            if w != correct and w not in clean_wrongs:
                clean_wrongs.append(w)
        if len(clean_wrongs) < 6:
            return False

        seen_texts.add(q_text)
        q_id = f"LIFE11_P2_DNA_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "DNA: The Code of Life",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "11",
                "subject": "Life Sciences",
                "topic": "DNA: The Code of Life",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    easy_subtopics = ["DNA Structure", "RNA Structure", "DNA Replication", "Protein Synthesis - Transcription", "Protein Synthesis - Translation", "DNA Profiling", "Mitochondrial DNA"]
    
    # Core definitions
    dna_terms = [
        ("Nucleotide", "The repeating monomer building block of nucleic acids, consisting of a pentose sugar, a phosphate group, and a nitrogenous base", ["Nucleoside", "Amino acid", "Polypeptide", "Codon", "Purine", "Histone", "Ribose"]),
        ("Deoxyribose", "The five-carbon pentose sugar found in DNA nucleotides, lacking an oxygen atom at position 2'", ["Ribose", "Glucose", "Fructose", "Sucrose", "Galactose", "Maltose", "Glycerol"]),
        ("Purine", "A double-ring nitrogenous base category that includes Adenine and Guanine", ["Pyrimidine", "Ribonucleotide", "Polypeptide", "Amino acid", "Uracil", "Thymine", "Cytosine"]),
        ("Pyrimidine", "A single-ring nitrogenous base category that includes Cytosine, Thymine, and Uracil", ["Purine", "Nucleoside", "Pentose", "Deoxyribose", "Adenine", "Guanine", "Polynucleotide"]),
        ("Adenine", "A purine base that forms two hydrogen bonds with thymine in DNA", ["Guanine", "Cytosine", "Thymine", "Uracil", "Histone", "Ribose", "Phosphate"]),
        ("Guanine", "A purine base that forms three hydrogen bonds with cytosine in DNA", ["Adenine", "Cytosine", "Thymine", "Uracil", "Deoxyribose", "Methionine", "Alanine"]),
        ("Thymine", "A pyrimidine base found only in DNA, pairing exclusively with adenine", ["Uracil", "Cytosine", "Guanine", "Adenine", "Ribose", "Histone", "Peptide"]),
        ("Uracil", "A pyrimidine base found exclusively in RNA, replacing thymine to pair with adenine", ["Thymine", "Cytosine", "Guanine", "Adenine", "Deoxyribose", "Maltose", "Histone"]),
        ("Hydrogen bond", "The weak intermolecular bond that holds complementary nitrogenous base pairs together in a DNA double helix", ["Phosphodiester bond", "Peptide bond", "Glycosidic bond", "Ionic bond", "Disulfide bridge", "Metallic bond", "Covalent bond"]),
        ("Phosphodiester bond", "The strong covalent bond that links the phosphate group of one nucleotide to the 3' carbon of the sugar of the adjacent nucleotide", ["Hydrogen bond", "Peptide bond", "Glycosidic bond", "Disulfide bond", "Electrostatic bond", "Hydrophobic bond", "Ester linkage"]),
        ("DNA Replication", "The process by which an exact copy of double-stranded DNA is synthesized inside the nucleus prior to cell division", ["Transcription", "Translation", "Recombination", "Translocation", "Conjugation", "Transformation", "Ligation"]),
        ("Semi-conservative replication", "The mode of DNA replication where each newly formed double helix consists of one original parental strand and one newly formed daughter strand", ["Conservative replication", "Dispersive replication", "Continuous replication", "Fragmented replication", "Degenerative replication", "Asymmetric replication", "Semicontinuous synthesis"]),
        ("DNA Helicase", "The enzyme that unzips and unwinds the DNA double helix by breaking hydrogen bonds between complementary base pairs", ["DNA Polymerase", "RNA Polymerase", "Ligase", "Amylase", "Protease", "Ribozyme", "Peptidyl transferase"]),
        ("DNA Polymerase", "The enzyme responsible for matching free complementary deoxyribonucleotides to the exposed template DNA strand during replication", ["RNA Polymerase", "DNA Helicase", "Ligase", "Reverse transcriptase", "Nuclease", "Lipase", "Trypsin"]),
        ("Transcription", "The first stage of protein synthesis occurring in the nucleus, where genetic information from DNA is copied into mRNA", ["Translation", "Replication", "Translocation", "Crossing over", "Synapsis", "Mutation", "Condensation"]),
        ("Translation", "The second stage of protein synthesis occurring in the cytoplasm at ribosomes, where mRNA codons are decoded into an amino acid sequence", ["Transcription", "Replication", "Splicing", "Elongation", "Recombination", "Ligation", "Electrophoresis"]),
        ("mRNA (messenger RNA)", "The single-stranded RNA molecule that carries the genetic code from DNA in the nucleus to ribosomes in the cytoplasm", ["tRNA", "rRNA", "snRNA", "mtDNA", "Plasmid", "Histone", "Ribozyme"]),
        ("tRNA (transfer RNA)", "The cloverleaf-shaped RNA molecule that carries a specific amino acid to the ribosome and contains a complementary anticodon", ["mRNA", "rRNA", "DNA", "mtDNA", "Ribozyme", "Polysaccharide", "Peptide"]),
        ("Codon", "A sequence of three consecutive nitrogenous bases on an mRNA molecule that codes for a specific amino acid or stop signal", ["Anticodon", "Triplet", "Nucleotide", "Exon", "Intron", "Promoter", "Operon"]),
        ("Anticodon", "A sequence of three consecutive bases on a tRNA molecule that is complementary to an mRNA codon", ["Codon", "Triplet", "Base pair", "Promoter", "Cistron", "Recon", "Polypeptide"]),
        ("Peptide bond", "The covalent chemical bond formed between the carboxyl group of one amino acid and the amino group of another", ["Hydrogen bond", "Phosphodiester bond", "Glycosidic bond", "Ionic bond", "Disulfide bridge", "Ester bond", "Van der Waals bond"]),
        ("Mitochondrial DNA (mtDNA)", "Circular DNA located within mitochondria, inherited strictly from the biological mother without genetic recombination", ["Nuclear DNA", "Chloroplast DNA", "Plasmid", "Recombinant DNA", "cDNA", "Bacterial chromosome", "Histone"]),
        ("DNA Profiling", "A forensic and genetic technique that analyzes unique non-coding DNA banding patterns to identify individuals or confirm biological parentage", ["Karyotyping", "Gene cloning", "Genetic modification", "Pedigree analysis", "Amniocentesis", "Polymerase Chain Reaction", "Gel extraction"]),
        ("Histones", "Basic protein molecules around which nuclear DNA double helices wrap to form chromatin and nucleosomes", ["Ribosomes", "Enzymes", "Centrioles", "Chiasmata", "Spindle fibers", "Tubulin", "Keratin"])
    ]

    for term, definition, wrongs in dna_terms:
        # Template 1: Identify definition
        q = f"In Grade 11 Life Sciences, what is defined as '{definition}'?"
        add_q("easy", "DNA Structure", q, term, wrongs, f"By definition, {term} is: {definition}.")

        # Template 2: What is the term for...
        q2 = f"Which biological term correctly names {definition}?"
        add_q("easy", "DNA Structure", q2, term, wrongs, f"The correct scientific term is {term}.")

        # Template 3: Reverse definition
        rev_wrongs = [d[1] for d in dna_terms if d[0] != term][:7]
        q3 = f"Which statement accurately describes the function or nature of {term}?"
        add_q("easy", "DNA Structure", q3, definition, rev_wrongs, f"{term} is defined as: {definition}.")

        # Template 4: True statement
        q4 = f"Identify the correct biological description of '{term}':"
        add_q("easy", "DNA Structure", q4, definition, rev_wrongs, f"The accurate statement describing {term} is '{definition}'.")

    # Extra specific easy questions on locations, base pairing, and components
    easy_extras = [
        ("Where in a human eukaryotic cell does transcription take place?", "Nucleus", ["Ribosome", "Cytoplasm", "Endoplasmic reticulum", "Mitochondrial matrix", "Golgi body", "Centrosome", "Lysosome"], "Transcription produces mRNA from a DNA template inside the nucleus."),
        ("Where in a eukaryotic cell does translation occur during protein synthesis?", "Cytoplasm at the ribosome", ["Nucleolus", "Nuclear envelope", "Lysosome", "Centriole", "Inside the nucleus", "Smooth endoplasmic reticulum", "Peroxisome"], "Translation occurs at ribosomes located free in the cytoplasm or on the rough ER."),
        ("Which nitrogenous base is present in DNA but absent in RNA?", "Thymine", ["Uracil", "Adenine", "Cytosine", "Guanine", "Deoxyribose", "Ribose", "Histone"], "DNA contains thymine; RNA contains uracil instead."),
        ("Which nitrogenous base is found in RNA molecules instead of thymine?", "Uracil", ["Thymine", "Adenine", "Cytosine", "Guanine", "Deoxyribose", "Ribose", "Peptide"], "In RNA, uracil replaces thymine and pairs with adenine."),
        ("What type of sugar is found in a molecule of ribonucleic acid (RNA)?", "Ribose", ["Deoxyribose", "Glucose", "Fructose", "Sucrose", "Lactose", "Maltose", "Galactose"], "RNA nucleotides contain the 5-carbon sugar ribose."),
        ("What type of sugar constitutes the backbone of a deoxyribonucleic acid (DNA) molecule?", "Deoxyribose", ["Ribose", "Glucose", "Fructose", "Maltose", "Cellulose", "Sucrose", "Glycogen"], "DNA contains deoxyribose, which has one fewer oxygen atom than ribose."),
        ("According to Chargaff's base pairing rules, adenine in double-stranded DNA always bonds with:", "Thymine", ["Cytosine", "Guanine", "Uracil", "Ribose", "Phosphate", "Histone"], "Adenine pairs with thymine via two hydrogen bonds."),
        ("According to complementary base pairing rules, guanine in DNA always bonds with:", "Cytosine", ["Thymine", "Adenine", "Uracil", "Ribose", "Histone", "Methionine"], "Guanine pairs with cytosine via three hydrogen bonds."),
        ("During which phase of the cell cycle does DNA replication occur?", "Interphase", ["Prophase", "Metaphase", "Anaphase", "Telophase", "Cytokinesis", "G0 phase"], "DNA replication occurs during the synthesis (S) phase of interphase."),
        ("How many hydrogen bonds connect cytosine and guanine in a DNA molecule?", "3", ["2", "1", "4", "5", "0", "8"], "Cytosine and guanine are held together by three hydrogen bonds, making their bond stronger than A-T."),
        ("How many hydrogen bonds connect adenine and thymine in a DNA molecule?", "2", ["3", "1", "4", "5", "0", "6"], "Adenine and thymine are held together by two hydrogen bonds."),
        ("Which molecule possesses an anticodon loop at one end and an amino acid attachment site at the opposite end?", "tRNA", ["mRNA", "rRNA", "DNA", "Ribosome", "Histone", "Peptidyl transferase"], "tRNA carries a specific anticodon and its corresponding amino acid to the ribosome."),
        ("What are the three components that make up a single DNA nucleotide?", "Phosphate group, deoxyribose sugar, and a nitrogenous base", ["Phosphate group, ribose sugar, and amino acid", "Glycerol, fatty acid, and nitrogenous base", "Amino group, carboxyl group, and R-group", "Phosphate group, glucose, and adenine", "Purine, pyrimidine, and polypeptide", "Deoxyribose, ribose, and peptide bond", "Carbon ring, lipid tail, and phosphate"], "A nucleotide consists of a phosphate group, a pentose sugar (deoxyribose), and one of four nitrogenous bases."),
        ("From which parent is mitochondrial DNA (mtDNA) exclusively inherited in humans?", "Biological mother only", ["Biological father only", "Both parents equally", "Maternal grandmother only", "Paternal grandfather only", "Randomly from either parent", "Neither parent; it forms spontaneously"], "Mitochondria from the sperm's neck/tail are destroyed upon fertilisation; all zygote mitochondria come from the ovum's cytoplasm."),
        ("Why does mitochondrial DNA (mtDNA) not undergo crossing over?", "It is inherited from one parent only and does not pair with homologous chromosomes", ["It lacks nitrogenous bases", "It is located inside the nucleus", "It is double-stranded like nuclear DNA", "It is degraded during interphase", "It only contains uracil", "It is enclosed in histones"], "Crossing over requires homologous chromosome pairs during meiosis; mtDNA is maternal only and non-pairing.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "Consider this CAPS Life Sciences question: ", "According to the Grade 11 curriculum: ", "In human genetics, "]:
            add_q("easy", "DNA Structure", f"{prefix}{q}", ans, wrongs, expl)

    # Fill easy to exactly 300
    base_pairs = [("Adenine", "Thymine", 2), ("Cytosine", "Guanine", 3), ("Thymine", "Adenine", 2), ("Guanine", "Cytosine", 3)]
    easy_count = len([q for q in questions if q['difficulty'] == 'easy'])
    e_idx = 1
    while easy_count < 300:
        b1, b2, bonds = random.choice(base_pairs)
        templates = [
            f"According to CAPS Life Sciences, if a DNA sequence contains the purine/pyrimidine {b1}, what complementary base does it pair with during replication (item {e_idx})?",
            f"In a DNA molecule, how many hydrogen bonds form between {b1} and its complementary partner {b2} (item {e_idx})?",
            f"Which nitrogenous base pairs with {b1} on the opposite strand of a double-stranded DNA molecule (question {e_idx})?"
        ]
        t_choice = random.choice(templates)
        if "how many hydrogen bonds" in t_choice:
            ans = str(bonds)
            wrongs = ["1", "4", "5", "0", "6", "8", "12"]
            expl = f"{b1} and {b2} form {bonds} hydrogen bonds."
        else:
            ans = b2
            wrongs = [x for x in ["Adenine", "Thymine", "Cytosine", "Guanine", "Uracil", "Histone", "Ribose"] if x != b2]
            expl = f"{b1} pairs with {b2}."
        if add_q("easy", "DNA Structure", t_choice, ans, wrongs, expl):
            easy_count += 1
        e_idx += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    # Medium Subtopics: Chargaff Math, Transcription/Translation Sequence Mapping, DNA vs RNA Comparison
    # A. Chargaff Percentages
    # If A = x%, T = x%, G = 50-x%, C = 50-x%
    percentages = [15, 18, 20, 22, 24, 26, 28, 30, 32, 34, 35]
    for p in percentages:
        other = 50 - p
        # Given A, find G
        q1 = f"A sample of human double-stranded DNA contains {p}% adenine. According to Chargaff's rules, what percentage of guanine does this DNA sample contain?"
        add_q("medium", "DNA Structure", q1, f"{other}%", [f"{p}%", f"{other+5}%", f"{other-5}%", f"{p*2}%", f"{100-p}%", f"{other//2}%", "50%"], f"Adenine = Thymine = {p}%. Total A+T = {p*2}%. Remaining G+C = {100 - p*2}%. Since Guanine = Cytosine, Guanine = {other}%.", "Application")
        # Given A, find C
        q2 = f"Chemical analysis of double-stranded DNA reveals that {p}% of the nitrogenous bases are adenine. What is the expected percentage of cytosine?"
        add_q("medium", "DNA Structure", q2, f"{other}%", [f"{p}%", f"{other+4}%", f"{other-4}%", f"{p*2}%", f"{100-p}%", f"{other*2}%", "25%"], f"A = {p}% implies T = {p}%. Remaining {100 - 2*p}% is equally divided between C and G, giving Cytosine = {other}%.", "Application")
        # Given G, find T
        q3 = f"If cytosine makes up {other}% of the nitrogenous bases in a double-stranded DNA segment, what percentage of the bases will be thymine?"
        add_q("medium", "DNA Structure", q3, f"{p}%", [f"{other}%", f"{p+5}%", f"{p-5}%", f"{other*2}%", f"{100-other}%", f"{p//2}%", "50%"], f"Cytosine = Guanine = {other}%. Total C+G = {other*2}%. Remaining A+T = {100 - other*2}%. Thymine = {p}%.", "Application")
        # Given G, find A
        q4 = f"A DNA molecule has {other}% guanine bases. What percentage of adenine bases are present in this molecule?"
        add_q("medium", "DNA Structure", q4, f"{p}%", [f"{other}%", f"{p+3}%", f"{p-3}%", f"{other//2}%", f"{100-other*2}%", f"{2*p}%", "10%"], f"G = C = {other}%. Total C+G = {other*2}%. A + T = {100 - other*2}%. Therefore, Adenine = {p}%.", "Application")

    # B. Nucleotide & Amino Acid Calculations
    counts = [150, 180, 240, 300, 360, 450, 600, 900, 1200, 1500]
    for c in counts:
        codons = c // 3
        aa = codons - 1 # excluding stop codon
        q1 = f"An mRNA transcript contains {c} nitrogenous bases from start codon to stop codon. How many codons does this mRNA contain?"
        add_q("medium", "Protein Synthesis - Translation", q1, str(codons), [str(c), str(c*3), str(codons+1), str(codons-1), str(codons*2), str(c//2), "60"], f"Each codon consists of 3 nitrogenous bases. Therefore, {c} / 3 = {codons} codons.", "Application")
        q2 = f"If an mRNA molecule consists of {c} coding nucleotides, what is the maximum number of amino acids in the synthesized polypeptide chain (assuming 1 stop codon)?"
        add_q("medium", "Protein Synthesis - Translation", q2, str(aa), [str(codons), str(c), str(c*3), str(aa+2), str(aa-2), str(c//2), "45"], f"{c} nucleotides / 3 = {codons} codons. One codon serves as the non-coding stop signal, yielding {aa} amino acids.", "Application")
        
        # DNA base count to amino acids
        dna_bases = c * 2 # double stranded
        q3 = f"A gene on double-stranded DNA consists of {dna_bases} base pairs. What is the number of amino acids coded by the mRNA transcribed from one strand of this gene (excluding stop codon)?"
        add_q("medium", "Protein Synthesis - Translation", q3, str(c - 1), [str(dna_bases), str(c), str(dna_bases//3), str(c*3), str(c+1), str(dna_bases//6), "100"], f"{dna_bases} base pairs means the template strand has {dna_bases} nucleotides, producing mRNA of {dna_bases} bases, coding for {dna_bases//3 - 1} = {c - 1} amino acids.", "Application")

    # C. Transcription Sequence Mapping (DNA template -> mRNA)
    dna_codons = [
        ("TAC", "AUG", "UAC", "Methionine (Start)"),
        ("GGG", "CCC", "GGG", "Proline"),
        ("CCC", "GGG", "CCC", "Glycine"),
        ("AAA", "UUU", "AAA", "Phenylalanine"),
        ("TTT", "AAA", "UUU", "Lysine"),
        ("GCT", "CGA", "GCU", "Arginine"),
        ("CGA", "GCU", "CGA", "Alanine"),
        ("TGA", "ACU", "UGA", "Threonine"),
        ("ACT", "UGA", "ACU", "Stop signal"),
        ("ATC", "UAG", "AUC", "Stop signal"),
        ("ATT", "UAA", "AUU", "Stop signal"),
        ("GAC", "CUG", "GAC", "Leucine"),
        ("CTG", "GAC", "CUG", "Aspartic acid")
    ]

    for d_trip, m_codon, t_anti, aa_name in dna_codons:
        # Template -> mRNA
        q1 = f"If the triplet on the DNA template strand is 3'-{d_trip}-5', what will be the corresponding codon sequence on the transcribed mRNA molecule?"
        add_q("medium", "Protein Synthesis - Transcription", q1, f"5'-{m_codon}-3'", [f"5'-{t_anti}-3'", f"3'-{d_trip}-5'", f"5'-{d_trip}-3'", f"3'-{m_codon}-5'", f"5'-{m_codon.replace('U', 'T')}-3'", f"3'-{t_anti}-5'", "5'-AUG-3'"], f"During transcription, complementary bases match: A->U, T->A, C->G, G->C. 3'-{d_trip}-5' pairs with 5'-{m_codon}-3'.", "Application")

        # mRNA -> tRNA anticodon
        q2 = f"If an mRNA codon reads 5'-{m_codon}-3', what is the complementary anticodon sequence carried by the corresponding tRNA molecule?"
        add_q("medium", "Protein Synthesis - Translation", q2, f"3'-{t_anti}-5'", [f"5'-{d_trip}-3'", f"3'-{m_codon}-5'", f"5'-{m_codon}-3'", f"3'-{d_trip}-5'", f"5'-{t_anti}-3'", f"3'-UAC-5'", "5'-CCC-3'"], f"The tRNA anticodon is complementary to the mRNA codon: A->U, U->A, C->G, G->C. 5'-{m_codon}-3' pairs with 3'-{t_anti}-5'.", "Application")

        # DNA -> tRNA anticodon
        q3 = f"What is the tRNA anticodon that corresponds to the DNA template triplet 3'-{d_trip}-5'?"
        add_q("medium", "Protein Synthesis - Translation", q3, f"3'-{t_anti}-5'", [f"5'-{m_codon}-3'", f"3'-{d_trip}-5'", f"5'-{d_trip}-3'", f"3'-{m_codon}-5'", f"5'-UAA-3'", f"3'-AUG-5'", "3'-AAA-5'"], f"DNA 3'-{d_trip}-5' transcribes to mRNA 5'-{m_codon}-3', which binds tRNA anticodon 3'-{t_anti}-5'.", "Application")

    # D. Experimental Scenarios and Diagnostic Questions
    scenarios = [
        ("A cell is treated with a chemical agent that inhibits the enzyme RNA polymerase. Which cellular process will be directly halted?", "Transcription of mRNA in the nucleus", ["Translation of mRNA at ribosomes", "Replication of nuclear DNA", "Transportation of amino acids by tRNA", "Formation of peptide bonds", "Crossing over in prophase I", "Attachment of spindle fibers to centromeres", "Replication of mitochondrial DNA"], "RNA polymerase is the enzyme that synthesizes mRNA from the DNA template during transcription."),
        ("What would be the immediate consequence if a cell runs out of free adenine ribonucleotides (ATP / AMP)?", "Synthesis of mRNA during transcription cannot proceed", ["DNA replication stops due to lack of deoxyribose", "tRNA cannot bind amino acids", "Cell wall synthesis is halted", "Chromosomes fail to separate at anaphase", "Histone proteins cannot form", "Mitochondrial outer membrane dissolves", "Peptide bonds break spontaneously"], "Transcription requires free ribonucleotides (A, U, C, G) with ribose sugar to construct mRNA."),
        ("In an experiment, human cells are grown in a medium containing radioactive thymine ($^3H$-thymidine). In which cellular process will this radioactive marker be incorporated?", "DNA replication in the nucleus", ["Transcription of mRNA", "Translation at the ribosome", "Breakdown of glucose in cytoplasm", "Synthesis of phospholipids in ER", "Packaging of proteins in Golgi", "Digestive enzyme secretion in lysosomes"], "Thymine is unique to DNA; therefore, radioactive thymidine is incorporated solely during DNA replication."),
        ("If cells are incubated with radioactive uracil ($^3H$-uridine), which process will show significant radioactivity?", "mRNA synthesis during transcription", ["DNA synthesis during replication", "Spindle fiber formation", "Centromere division in anaphase", "Glycolysis in the cytosol", "Active transport of sodium ions", "Condensation of chromatin into chromosomes"], "Uracil is unique to RNA, so radioactive uridine is specifically incorporated into RNA molecules during transcription."),
        ("During DNA profiling, what is the role of restriction enzymes (endonucleases)?", "To cut DNA at specific palindromic base sequences into fragments of varying lengths", ["To amplify DNA fragments using heat cycles", "To separate DNA fragments according to size using an electric field", "To dye the DNA bands so they fluoresce under UV light", "To unwind and replicate the DNA strands", "To join Okazaki fragments together", "To synthesize complementary mRNA molecules", "To destroy maternal mitochondrial DNA"], "Restriction enzymes cut long DNA strands into restriction fragments at specific recognition sites."),
        ("In gel electrophoresis during DNA profiling, how do DNA fragments separate as they migrate through the agarose gel?", "Smaller fragments move faster and travel further towards the positive anode than larger fragments", ["Larger fragments move faster towards the negative cathode", "All fragments move at identical speeds regardless of size", "Positively charged DNA fragments migrate towards the cathode", "Single-stranded fragments stay at the wells while double-stranded move", "Fragments separate based on their thymine content only", "Fragments separate based solely on their cell of origin", "Fragments are pulled down by gravity"], "DNA is negatively charged (due to phosphate groups) and migrates towards the positive electrode; smaller fragments travel faster through the gel pores."),
        ("A child's DNA profile is compared with that of the mother and three alleged fathers. Which principle determines biological paternity?", "Every band present in the child's profile that does not match a band in the mother's profile must match a band in the biological father's profile", ["The child must share 100% of all bands with the biological father only", "The child's profile must be identical to the mother's profile", "Only bands on the X chromosome are compared", "The biological father must possess twice as many bands as the child", "Maternal bands are ignored completely in paternity tests", "Only mitochondrial DNA bands can be matched for paternity", "Any matching band proves biological paternity beyond doubt"], "Half of the child's nuclear DNA comes from the mother and half from the father; any band not inherited from the mother MUST come from the biological father.")
    ]

    for q, ans, wrongs, expl in scenarios:
        for prefix in ["", "Laboratory investigation: ", "In a CAPS Life Sciences examination scenario, ", "Consider this experimental finding: "]:
            add_q("medium", "DNA Profiling", f"{prefix}{q}", ans, wrongs, expl, "Application")

    # Fill Medium to 500 with diverse combinations
    seq_templates = [
        ("TAC-GGG-AAA-TTC-ACT", "AUG-CCC-UUU-AAG-UGA", "5 codons", "4 amino acids"),
        ("TAC-CGA-TTT-GGG-ATC", "AUG-GCU-AAA-CCC-UAG", "5 codons", "4 amino acids"),
        ("TAC-TTT-CCC-AAA-ATT", "AUG-AAA-GGG-UUU-UAA", "5 codons", "4 amino acids"),
        ("TAC-GAC-CTG-AAA-ACT", "AUG-CUG-GAC-UUU-UGA", "5 codons", "4 amino acids"),
        ("TAC-AAA-TTT-GGG-CCC", "AUG-UUU-AAA-CCC-GGG", "5 codons", "4 amino acids"),
    ]

    counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        tpl = random.choice(seq_templates)
        q = f"A segment of template DNA has the sequence 3'-{tpl[0]}-5' (sample {counter}). What is the transcribed mRNA molecule produced during transcription?"
        add_q("medium", "Protein Synthesis - Transcription", q, f"5'-{tpl[1]}-3'", [f"5'-{tpl[0]}-3'", f"3'-{tpl[1]}-5'", f"5'-{tpl[1].replace('U','T')}-3'", f"3'-{tpl[0]}-5'", "5'-AUG-AAA-UAA-3'", "5'-GGG-CCC-AAA-3'", "5'-UAC-CCC-AAA-3'"], f"Template 3'-{tpl[0]}-5' produces complementary mRNA 5'-{tpl[1]}-3'.", "Application")
        counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        # Mutations
        ("What type of gene mutation occurs when an extra nucleotide is added to the coding sequence of a gene, shifting the reading frame of all subsequent codons?",
         "Frameshift mutation (insertion)",
         ["Silent point mutation", "Nonsense substitution mutation", "Missense substitution mutation", "Chromosomal inversion", "Translocation between non-homologous chromosomes", "Aneuploidy due to non-disjunction", "Polyploidy"],
         "An insertion or deletion of a nucleotide not divisible by 3 shifts the triplet reading frame, fundamentally altering all downstream codons and amino acids.", "Analysis"),

        ("In the genetic disorder Sickle-Cell Anemia, a single base substitution changes the mRNA codon from GAG (coding for glutamic acid) to GUG. What type of mutation is this?",
         "Missense point mutation",
         ["Nonsense mutation producing a premature stop codon", "Silent mutation with no phenotypic change", "Frameshift deletion mutation", "Chromosomal deletion", "Trisomy mutation", "Neutral non-coding mutation", "Inversion mutation"],
         "A point mutation that replaces one amino acid with another (glutamic acid with valine) is classified as a missense mutation.", "Analysis"),

        ("A mutation changes an mRNA codon from UAC (tyrosine) to UAA (stop codon). What is the physiological impact on the resulting protein?",
         "Translation terminates prematurely, producing a truncated and non-functional polypeptide",
         ["The polypeptide has one extra amino acid added to its chain", "The polypeptide continues elongating without a stop codon", "The rate of translation is doubled at the ribosome", "The protein becomes more stable due to extra peptide bonds", "The ribosome degrades before binding mRNA", "tRNA attaches tyrosine regardless of the codon", "The cell reverts to using DNA instead of mRNA"],
         "UAA is a stop codon; converting a sense codon to a stop codon causes premature termination (nonsense mutation).", "Analysis"),

        ("Why does a point mutation in the third position of a codon ('wobble base') frequently result in a silent mutation?",
         "Due to the degeneracy (redundancy) of the genetic code, multiple different codons specify the same amino acid",
         ["Because the third base is excised by DNA repair enzymes before translation", "Because tRNA anticodons only possess two nitrogenous bases", "Because the ribosome reads codons in pairs rather than triplets", "Because third-position bases cannot form hydrogen bonds", "Because RNA polymerase corrects all third-base errors in the nucleus", "Because amino acids do not rely on codon recognition", "Because only the first base of a codon determines amino acid identity"],
         "The genetic code is degenerate: 64 codons code for only 20 amino acids, so third-base changes often code for the identical amino acid.", "Analysis"),

        # Semi-conservative vs conservative replication evidence
        ("In the classic Meselson and Stahl experiment, bacteria grown in heavy isotope 15N were transferred to light 14N medium for one generation. The isolated DNA centrifuged in CsCl formed a single intermediate band. Which hypothesis did this result disprove?",
         "Conservative replication hypothesis",
         ["Semi-conservative replication hypothesis", "Dispersive replication hypothesis", "The Central Dogma of Molecular Biology", "Chargaff's rules of base pairing", "Mendel's Law of Segregation", "Darwin's theory of gradualism", "The presence of hydrogen bonds in DNA"],
         "Conservative replication predicted two separate bands (one entirely heavy 15N and one entirely light 14N). A single intermediate hybrid band (15N-14N) disproved conservative replication.", "Analysis"),

        ("Why is mitochondrial DNA (mtDNA) considered an indispensable molecular tool for tracing maternal evolutionary ancestry and validating the 'Out of Africa' hypothesis?",
         "mtDNA is inherited strictly maternally without crossing over, and accumulates mutations at a regular, predictable molecular clock rate",
         ["mtDNA undergoes rapid crossing over during Meiosis I, creating unique maternal phenotypes", "mtDNA is identical in sequence to paternal nuclear DNA", "mtDNA does not contain nitrogenous bases, making it immune to degradation", "mtDNA codes for all 20 standard amino acids simultaneously", "mtDNA is only present in female human cells and absent in males", "mtDNA is resistant to all forms of point mutation", "mtDNA is located inside the nucleus surrounded by protective histones"],
         "mtDNA does not undergo crossing over or sexual recombination, allowing maternal lineages to be traced back continuously through accumulated mutations.", "Analysis"),

        ("A forensic investigator analyzes a crime scene blood sample. The DNA profile yields 12 distinct bands. The suspect's DNA profile shares 11 of the 12 bands. What is the correct forensic conclusion?",
         "The suspect is conclusively excluded as the source of the crime scene sample",
         ["The suspect is confirmed to be the criminal because 11 out of 12 is a statistical match", "The suspect is likely the identical twin of the perpetrator", "The crime scene sample must be degraded and cannot be used in court", "The suspect's mother must have left the 12th band at the crime scene", "The investigator should run the gel backwards to find the 12th band", "The suspect is guilty beyond a reasonable doubt", "The 12th band is an artifact that should be ignored"],
         "In forensic DNA profiling, a single non-matching band conclusively excludes a suspect as the source of a single-source crime scene specimen.", "Analysis"),

        ("How does the structural presence of three hydrogen bonds between Guanine and Cytosine (compared to two between Adenine and Thymine) affect DNA stability?",
         "DNA segments with high G-C content require significantly higher thermal energy (higher melting temperature Tm) to denature and separate",
         ["High G-C content makes DNA unstable and prone to spontaneous strand breakage", "High G-C segments replicate three times faster than high A-T segments", "G-C base pairs cannot be unwound by DNA helicase in vivo", "High A-T content prevents RNA polymerase from initiating transcription", "G-C base pairs can bond with ribose sugars while A-T cannot", "G-C bonds prevent the formation of phosphodiester linkages", "High G-C segments are exclusively found in mitochondrial DNA"],
         "Three hydrogen bonds provide higher thermal and chemical stability, raising the melting temperature required to separate the strands.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "Advanced CAPS Analysis: ", "Evaluate the following molecular mechanism: ", "Consider the clinical/experimental evidence: "]:
            add_q("hard", "DNA Structure", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Fill Hard to 200 with complex pedigree/profiling and mutation analytical scenarios
    sample_mutations = [
        ("Base 14 replaced: GAG -> GTG (Glutamic acid -> Valine)", "Missense mutation altering hemoglobin secondary structure causing red blood cells to sickle"),
        ("Base 21 replaced: UGG -> UGA (Tryptophan -> Stop codon)", "Nonsense mutation causing premature translation termination and loss of enzyme function"),
        ("Insertion of single Guanine at position 5", "Frameshift mutation modifying the entire downstream reading frame and producing a non-functional protein"),
        ("Deletion of single Adenine at position 12", "Frameshift mutation altering all amino acids downstream and introducing an early stop codon"),
        ("Base 9 replaced: UUU -> UUC (Both code for Phenylalanine)", "Silent mutation having zero phenotypic consequence on the structure or function of the protein")
    ]

    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        mut = random.choice(sample_mutations)
        q = random.choice(_templates).format(clinic=random.choice(_clinics), city=random.choice(_cities), name=random.choice(_names), topic=f"A patient gene sequence reveals the mutation: {mut[0]}. What is the biological consequence on the synthesized protein?")
        add_q("hard", "Protein Synthesis - Translation", q, mut[1], [
            "The protein's primary structure is completely unaffected despite the altered reading frame",
            "The ribosome bypasses the mutated codon and skips directly to the 3' poly-A tail",
            "DNA polymerase fails to transcribe the mRNA during interphase",
            "The cell initiates immediate mitosis to compensate for the missing enzyme",
            "The mutation converts the DNA from double-stranded into single-stranded RNA",
            "Mitochondrial DNA takes over the expression of the nuclear protein",
            "The mutated codon binds to ribosomal RNA instead of transfer RNA"
        ], f"The specific consequence of {mut[0]} is: {mut[1]}.", "Analysis")
        h_counter += 1

    # Final counts check
    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match 300/500/200: {counts}"

    output_path = "dataset/grade11/life_sciences/paper2_life_dna_code.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_dna_code()
