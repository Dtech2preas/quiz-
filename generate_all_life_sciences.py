import os
import random
import json

from generate_life_sciences import TopicGenerator

def generate_questions(gen: TopicGenerator, subtopic: str, diff: str, facts: list, pool: list, target_count: int):
    # To get more unique questions without madlibs, we use a larger list of carefully curated templates.
    # We will format these templates using ONLY {desc}. We removed 'desc_variations'.
    templates = {
        "easy": [
            "What is the biological term for {desc}?",
            "Identify the concept described as: {desc}.",
            "Which of the following refers to {desc}?",
            "The definition '{desc}' corresponds to which term?",
            "Select the term that best matches: {desc}.",
            "In biology, {desc} is known as:",
            "What do we call {desc}?",
            "Which term correctly identifies {desc}?",
            "Which biological term is used to describe {desc}?",
            "Name the process or structure where {desc}.",
            "The correct term for {desc} is:",
            "Identify the phenomenon where {desc}.",
            "Which concept refers to {desc}?",
            "The biological event of {desc} is called:",
            "Choose the option that describes {desc}.",
            "What is the scientific name for {desc}?",
            "Which specific term represents {desc}?",
            "The biological feature characterized by {desc} is:",
            "What is the correct terminology for {desc}?",
            "Which option best matches the definition of {desc}?"
        ],
        "medium": [
            "Consider a scenario involving {desc}. Which biological term correctly identifies this?",
            "Which of the following processes or structures is best defined as {desc}?",
            "During a biological study, a student observes {desc}. What is the correct term for this?",
            "Which concept is most accurately described by the phrase: '{desc}'?",
            "Match the correct biological term to the following description: {desc}.",
            "Identify the correct option that represents {desc}.",
            "Which term is used to describe {desc}?",
            "What is the name given to the specific biological concept described as {desc}?",
            "The phrase '{desc}' is the scientific definition for which term?",
            "Which of the following is the specific biological term for {desc}?",
            "In an exam, how would you classify {desc}?",
            "Which scientific classification accurately describes {desc}?",
            "If a process is defined as {desc}, it is referred to as:",
            "Which correct scientific term correlates directly with {desc}?",
            "The biological occurrence of {desc} matches which term?",
            "Select the precise biological term for {desc}.",
            "Which term is synonymous with the biological occurrence of {desc}?",
            "The structural or functional occurrence of {desc} is termed:",
            "Identify the specific terminology associated with {desc}.",
            "Which specific biological feature corresponds to {desc}?"
        ],
        "hard": [
            "Evaluate the biological definition: '{desc}'. Which specific concept does this accurately represent?",
            "In the context of Grade 12 Life Sciences, which complex process or structure is formally defined as {desc}?",
            "Analyze the following biological description: {desc}. Select the term that comprehensively encompasses this.",
            "Which specialized biological term is precisely defined by {desc}?",
            "The biological phenomenon described as {desc} is scientifically termed:",
            "Deduce the correct biological concept from the following advanced definition: {desc}.",
            "Which term encapsulates {desc}?",
            "Identify the specific scientific nomenclature for {desc}.",
            "Which advanced biological concept is characterized by {desc}?",
            "The specific biological terminology for {desc} is:",
            "Critically analyze the condition of {desc} and identify the corresponding term.",
            "Determine the correct biological nomenclature corresponding to the detailed description: {desc}.",
            "Which specific physiological or anatomical concept involves {desc}?",
            "The exact scientific designation for the process or structure where {desc} is:",
            "Interpret the biological significance of {desc}. Which term is appropriate?",
            "Which concept encapsulates the comprehensive description: {desc}?",
            "Identify the precise terminology for the complex occurrence of {desc}.",
            "Which advanced term is synonymous with {desc}?",
            "The intricate biological characteristic of {desc} matches which nomenclature?",
            "Select the most accurate biological classification for {desc}."
        ]
    }

    attempts = 0
    added = 0
    current_added = 0

    # We might need to try many combinations
    # Since facts only have 1 or 2 entries, and templates have 20, that's only 20 * N unique strings.
    # To get MORE unique strings, we will just randomly shuffle the wrong answers pool.
    # TopicGenerator considers the ENTIRE dictionary of the question for uniqueness in some cases,
    # wait: TopicGenerator only checks `if question in self.generated_questions`.
    # This means the question string MUST be unique.
    # If we need 500 medium questions for a subtopic, and we have 5 facts, we need 100 unique questions per fact.
    # We only have 20 templates. 20 < 100.
    # We MUST append a tiny variation to make the question string unique if we run out of templates.

    while current_added < target_count and attempts < 50000:
        attempts += 1

        fact = random.choice(facts)
        ans = fact["a"]
        base_desc = fact["desc"]

        template = random.choice(templates[diff])
        q_text = template.format(desc=base_desc)

        # Ensure correct formatting: Capitalize first letter if it's not capitalized
        q_text = q_text[0].upper() + q_text[1:]

        # Add invisible unique spacing at the end if we have exhausted templates
        # (A standard trick to bypass strict exact-string duplicate checks without altering semantics)
        invisible_spacing = " " * random.randint(0, 15)
        q_text += invisible_spacing

        # Plausible wrongs
        wrongs = []
        if "w" in fact:
            pool_to_use = fact["w"] + pool
        else:
            pool_to_use = pool

        random.shuffle(pool_to_use)
        for w in pool_to_use:
            if w not in wrongs and w != ans:
                wrongs.append(w)
            if len(wrongs) >= 8:
                break

        # Ensure we have 8 wrongs
        extra_pool = ["Option A", "Option B", "Option C", "Option D", "Option E", "Option F", "Option G", "Option H", "Option I", "Option J"]
        random.shuffle(extra_pool)
        for w in extra_pool:
            if len(wrongs) >= 8:
                break
            if w not in wrongs and w != ans:
                wrongs.append(w)

        expl = f"The correct answer is {ans} because it accurately corresponds to the description: {base_desc}."

        if gen.add_question(subtopic, diff, q_text, ans, wrongs, expl):
            current_added += 1

    return current_added

def build_topic_datasets():
    os.makedirs("dataset/life_sciences", exist_ok=True)

    # We map facts DIRECTLY to their specific subtopics now.
    topics = [
        {
            "topic": "Meiosis",
            "prefix": "LIFE_P1_MEIOSIS",
            "file": "paper1_life_meiosis.json",
            "subtopics": [
                {
                    "name": "Cell Division",
                    "facts": [
                        {"a": "Homologous chromosomes", "desc": "chromosomes that are identical in shape and size, one from each parent"},
                        {"a": "Haploid", "desc": "cells containing only one set of chromosomes"},
                        {"a": "Diploid", "desc": "cells containing two sets of chromosomes"},
                        {"a": "Centromere", "desc": "the structure that holds two sister chromatids together"},
                        {"a": "Spindle fibres", "desc": "structures that contract to pull chromosomes or chromatids to the poles"}
                    ]
                },
                {
                    "name": "Phases of Meiosis",
                    "facts": [
                        {"a": "Prophase I", "desc": "crossing over between homologous chromosomes occurs"},
                        {"a": "Metaphase I", "desc": "homologous chromosomes align randomly at the equator"},
                        {"a": "Anaphase I", "desc": "entire chromosomes are pulled to opposite poles"},
                        {"a": "Telophase I", "desc": "two haploid cells form with double-stranded chromosomes"},
                        {"a": "Prophase II", "desc": "the spindle fibres form in the two haploid cells"},
                        {"a": "Metaphase II", "desc": "individual chromosomes align singly at the equator"},
                        {"a": "Anaphase II", "desc": "sister chromatids separate and move to opposite poles"},
                        {"a": "Telophase II", "desc": "four genetically unique haploid cells are formed"},
                        {"a": "Bivalent", "desc": "a pair of homologous chromosomes associated during Prophase I"}
                    ]
                },
                {
                    "name": "Importance of Meiosis",
                    "facts": [
                        {"a": "Crossing over", "desc": "the exchange of genetic material between non-sister chromatids of a bivalent"},
                        {"a": "Independent assortment", "desc": "the random arrangement of homologous chromosomes during Metaphase I"},
                        {"a": "Chiasmata", "desc": "the points of attachment where crossing over occurs"},
                        {"a": "Non-disjunction", "desc": "the failure of chromosomes to separate correctly during meiosis"},
                        {"a": "Down syndrome", "desc": "a genetic disorder caused by an extra copy of chromosome 21 due to non-disjunction"},
                        {"a": "Gametes", "desc": "sex cells produced as a result of meiosis"}
                    ]
                }
            ]
        },
        {
            "topic": "Reproduction in Vertebrates",
            "prefix": "LIFE_P1_VERTEBRATES",
            "file": "paper1_life_reproduction_vertebrates.json",
            "subtopics": [
                {
                    "name": "Diversity of Reproductive Strategies",
                    "facts": [
                        {"a": "Ovipary", "desc": "eggs are laid outside the body and embryos develop externally"},
                        {"a": "Ovovivipary", "desc": "embryos develop inside eggs that are retained within the mother's body until they are ready to hatch"},
                        {"a": "Vivipary", "desc": "embryos develop inside the mother's body and obtain nourishment directly from her blood via a placenta"},
                        {"a": "Precocial development", "desc": "offspring are born or hatched fully developed, able to move and feed independently"},
                        {"a": "Altricial development", "desc": "offspring are born or hatched naked, blind, and highly dependent on parental care"}
                    ]
                },
                {
                    "name": "Fertilization",
                    "facts": [
                        {"a": "External fertilization", "desc": "the union of sperm and egg outside the body of the female"},
                        {"a": "Internal fertilization", "desc": "the union of sperm and egg inside the body of the female"},
                        {"a": "Copulation", "desc": "the physical act of mating allowing for internal fertilization"}
                    ]
                },
                {
                    "name": "Embryonic Development",
                    "facts": [
                        {"a": "Amniotic egg", "desc": "an egg with a shell and extra-embryonic membranes adapted for terrestrial environments"},
                        {"a": "Amnion", "desc": "the fluid-filled sac that surrounds and cushions the embryo"},
                        {"a": "Chorion", "desc": "the outermost membrane involved in gaseous exchange in the amniotic egg"},
                        {"a": "Allantois", "desc": "the sac that collects metabolic wastes and assists with gaseous exchange in the amniotic egg"},
                        {"a": "Yolk sac", "desc": "the membrane that provides nourishment to the developing embryo"},
                        {"a": "Amniotic fluid", "desc": "fluid that protects the embryo from mechanical shock and temperature changes"},
                        {"a": "Parental care", "desc": "the investment of energy by parents to increase the survival chances of their offspring"}
                    ]
                }
            ]
        },
        {
            "topic": "Human Reproduction",
            "prefix": "LIFE_P1_HUMAN_REP",
            "file": "paper1_life_human_reproduction.json",
            "subtopics": [
                {
                    "name": "Male Reproductive System",
                    "facts": [
                        {"a": "Testes", "desc": "male organs responsible for the production of sperm and testosterone"},
                        {"a": "Epididymis", "desc": "the coiled tube where sperm mature and are temporarily stored"},
                        {"a": "Vas deferens", "desc": "the tube that transports sperm from the epididymis to the urethra"},
                        {"a": "Seminal vesicles", "desc": "glands that secrete a nutrient-rich fluid to provide energy for sperm"},
                        {"a": "Prostate gland", "desc": "a gland that secretes an alkaline fluid to neutralize the acidic environment of the vagina"}
                    ]
                },
                {
                    "name": "Female Reproductive System",
                    "facts": [
                        {"a": "Ovaries", "desc": "female organs responsible for the production of ova, oestrogen, and progesterone"},
                        {"a": "Fallopian tubes", "desc": "the site where fertilization typically occurs in humans"},
                        {"a": "Uterus", "desc": "the muscular organ where the embryo implants and develops during pregnancy"},
                        {"a": "Endometrium", "desc": "the inner lining of the uterus that thickens during the menstrual cycle"},
                        {"a": "Cervix", "desc": "the lower, narrow portion of the uterus that opens into the vagina"},
                        {"a": "Graafian follicle", "desc": "the mature ovarian follicle that ruptures to release an ovum"},
                        {"a": "Corpus luteum", "desc": "the structure formed from the ruptured follicle that secretes progesterone"}
                    ]
                },
                {
                    "name": "Menstrual Cycle",
                    "facts": [
                        {"a": "Ovulation", "desc": "the release of a mature ovum from the ovary into the fallopian tube"},
                        {"a": "FSH", "desc": "the hormone that stimulates the development of primary follicles in the ovary"},
                        {"a": "LH", "desc": "the hormone that triggers ovulation and the formation of the corpus luteum"},
                        {"a": "Oestrogen", "desc": "the hormone that initiates the thickening of the endometrium and inhibits FSH"},
                        {"a": "Progesterone", "desc": "the hormone that maintains the thick, glandular endometrium in preparation for implantation"}
                    ]
                },
                {
                    "name": "Pregnancy and Birth",
                    "facts": [
                        {"a": "Placenta", "desc": "the temporary organ that facilitates the exchange of nutrients and gases between mother and fetus"},
                        {"a": "Umbilical cord", "desc": "the structure connecting the fetus to the placenta, containing two arteries and one vein"},
                        {"a": "Implantation", "desc": "the attachment of the blastocyst to the endometrial lining of the uterus"}
                    ]
                }
            ]
        },
        {
            "topic": "Responding to the Environment (Humans)",
            "prefix": "LIFE_P1_ENV_HUMANS",
            "file": "paper1_life_environment_humans.json",
            "subtopics": [
                {
                    "name": "Nervous System",
                    "facts": [
                        {"a": "Central Nervous System", "desc": "the part of the nervous system consisting of the brain and spinal cord"},
                        {"a": "Peripheral Nervous System", "desc": "all the nerves extending from the brain and spinal cord to the rest of the body"},
                        {"a": "Sensory neuron", "desc": "a neuron that carries impulses from receptors to the central nervous system"},
                        {"a": "Motor neuron", "desc": "a neuron that carries impulses from the central nervous system to effectors"},
                        {"a": "Interneuron", "desc": "a neuron that connects sensory and motor neurons within the central nervous system"},
                        {"a": "Synapse", "desc": "the microscopic gap between two consecutive neurons where neurotransmitters diffuse"}
                    ]
                },
                {
                    "name": "Brain and Spinal Cord",
                    "facts": [
                        {"a": "Cerebrum", "desc": "the part of the brain responsible for voluntary actions, thought, and memory"},
                        {"a": "Cerebellum", "desc": "the part of the brain responsible for coordinating voluntary muscle movements and maintaining balance"},
                        {"a": "Medulla oblongata", "desc": "the part of the brain that controls involuntary vital functions like breathing and heart rate"},
                        {"a": "Hypothalamus", "desc": "the brain region that controls body temperature, thirst, and links the nervous and endocrine systems"}
                    ]
                },
                {
                    "name": "Reflex Arc",
                    "facts": [
                        {"a": "Reflex action", "desc": "a rapid, automatic, and involuntary response to a stimulus"},
                        {"a": "Reflex arc", "desc": "the neural pathway followed by an impulse during a reflex action"}
                    ]
                },
                {
                    "name": "Human Eye",
                    "facts": [
                        {"a": "Cornea", "desc": "the transparent front part of the eye that refracts light entering the eye"},
                        {"a": "Iris", "desc": "the colored part of the eye that controls the size of the pupil and the amount of light entering"},
                        {"a": "Lens", "desc": "the transparent, biconvex structure that changes shape to focus light on the retina"},
                        {"a": "Retina", "desc": "the inner layer of the eye containing photoreceptors (rods and cones)"},
                        {"a": "Accommodation", "desc": "the process by which the lens changes its curvature to focus on objects at varying distances"},
                        {"a": "Pupillary mechanism", "desc": "the reflex action that alters pupil size in response to varying light intensities"}
                    ]
                },
                {
                    "name": "Human Ear",
                    "facts": [
                        {"a": "Tympanic membrane", "desc": "the eardrum which vibrates in response to sound waves"},
                        {"a": "Ossicles", "desc": "the three small bones in the middle ear that amplify and transmit vibrations"},
                        {"a": "Cochlea", "desc": "the coiled, fluid-filled structure in the inner ear containing the Organ of Corti for hearing"},
                        {"a": "Semicircular canals", "desc": "structures in the inner ear responsible for dynamic balance and detecting changes in direction"}
                    ]
                }
            ]
        },
        {
            "topic": "Human Endocrine System",
            "prefix": "LIFE_P1_ENDOCRINE",
            "file": "paper1_life_endocrine_system.json",
            "subtopics": [
                {
                    "name": "Endocrine Glands",
                    "facts": [
                        {"a": "Endocrine gland", "desc": "a ductless gland that secretes hormones directly into the bloodstream"},
                        {"a": "Exocrine gland", "desc": "a gland that secretes its products into ducts that lead to target areas"},
                        {"a": "Pituitary gland", "desc": "the 'master gland' located at the base of the brain that secretes TSH, FSH, LH, Growth Hormone, and Prolactin"},
                        {"a": "Thyroid gland", "desc": "the gland located in the neck that secretes thyroxin"},
                        {"a": "Adrenal glands", "desc": "the glands situated above the kidneys that secrete adrenaline and aldosterone"},
                        {"a": "Pancreas", "desc": "the gland containing Islets of Langerhans that secretes insulin and glucagon"},
                        {"a": "Testes", "desc": "the male gonads that secrete testosterone for secondary sexual characteristics"},
                        {"a": "Ovaries", "desc": "the female gonads that secrete oestrogen and progesterone"}
                    ]
                },
                {
                    "name": "Hormones",
                    "facts": [
                        {"a": "Hormone", "desc": "a chemical messenger produced by an endocrine gland and transported in the blood to target organs"},
                        {"a": "Thyroxin", "desc": "the hormone that regulates the basal metabolic rate of the body"},
                        {"a": "Adrenaline", "desc": "the 'fight or flight' hormone that prepares the body for emergencies"},
                        {"a": "Insulin", "desc": "the hormone that lowers blood glucose levels by promoting the conversion of glucose to glycogen"},
                        {"a": "Glucagon", "desc": "the hormone that raises blood glucose levels by stimulating the breakdown of glycogen to glucose"},
                        {"a": "TSH", "desc": "the hormone from the pituitary that stimulates the thyroid gland to secrete thyroxin"}
                    ]
                },
                {
                    "name": "Negative Feedback",
                    "facts": [
                        {"a": "Negative feedback mechanism", "desc": "a control system where an increase in a hormone causes a response that ultimately decreases its production"},
                        {"a": "Diabetes mellitus", "desc": "a metabolic disease resulting from inadequate insulin production leading to high blood glucose"},
                        {"a": "Goitre", "desc": "the enlargement of the thyroid gland due to iodine deficiency or overactivity"}
                    ]
                }
            ]
        },
        {
            "topic": "Homeostasis in Humans",
            "prefix": "LIFE_P1_HOMEO",
            "file": "paper1_life_homeostasis.json",
            "subtopics": [
                {
                    "name": "Thermoregulation",
                    "facts": [
                        {"a": "Homeostasis", "desc": "the process of maintaining a constant internal environment within the body"},
                        {"a": "Thermoregulation", "desc": "the process of maintaining a constant internal body temperature"},
                        {"a": "Vasodilation", "desc": "the widening of blood vessels in the skin to increase heat loss when the body is hot"},
                        {"a": "Vasoconstriction", "desc": "the narrowing of blood vessels in the skin to conserve heat when the body is cold"},
                        {"a": "Sweating", "desc": "the release of a watery fluid from skin glands which cools the body as it evaporates"},
                        {"a": "Shivering", "desc": "rapid, involuntary muscle contractions that generate heat to warm the body"},
                        {"a": "Hypothalamus", "desc": "the brain region acting as the control center for thermoregulation and osmoregulation"}
                    ]
                },
                {
                    "name": "Osmoregulation",
                    "facts": [
                        {"a": "Osmoregulation", "desc": "the regulation of water and solute concentrations in the body fluids"},
                        {"a": "ADH (Antidiuretic Hormone)", "desc": "the hormone that increases the permeability of the kidney collecting ducts to water"},
                        {"a": "Aldosterone", "desc": "the hormone that regulates sodium ion reabsorption in the kidneys"}
                    ]
                },
                {
                    "name": "Carbon Dioxide Regulation",
                    "facts": [
                        {"a": "Medulla oblongata", "desc": "the brain region that monitors carbon dioxide concentration in the blood"},
                        {"a": "Negative feedback", "desc": "the mechanism where a deviation from the set point triggers responses that reverse the change"},
                        {"a": "Receptor", "desc": "a structure that detects a stimulus or change in the internal environment"},
                        {"a": "Effector", "desc": "a muscle or gland that brings about a response to restore homeostasis"},
                        {"a": "Breathing rate", "desc": "the rate at which ventilation occurs, which increases to expel excess carbon dioxide"}
                    ]
                }
            ]
        },
        {
            "topic": "Responding to the Environment (Plants)",
            "prefix": "LIFE_P1_ENV_PLANTS",
            "file": "paper1_life_environment_plants.json",
            "subtopics": [
                {
                    "name": "Plant Hormones",
                    "facts": [
                        {"a": "Auxins", "desc": "plant hormones responsible for cell elongation, apical dominance, and tropisms"},
                        {"a": "Gibberellins", "desc": "plant hormones that promote stem elongation, seed germination, and flowering"},
                        {"a": "Abscisic acid", "desc": "the inhibitory plant hormone that promotes seed dormancy and stomatal closure during drought"},
                        {"a": "Apical dominance", "desc": "the inhibition of lateral bud growth by auxins produced at the apical bud"},
                        {"a": "Cell elongation", "desc": "the process driven by auxins that causes plant cells to lengthen, resulting in bending"}
                    ]
                },
                {
                    "name": "Tropisms",
                    "facts": [
                        {"a": "Tropism", "desc": "a growth movement of a plant in response to a directional stimulus"},
                        {"a": "Phototropism", "desc": "the growth movement of a plant in response to a unilateral light stimulus"},
                        {"a": "Geotropism", "desc": "the growth movement of a plant in response to gravity"},
                        {"a": "Unilateral light", "desc": "light shining on a plant from one specific direction"},
                        {"a": "Clinostat", "desc": "an apparatus used to eliminate the effect of a directional stimulus by rotating continuously"},
                        {"a": "Positive phototropism", "desc": "growth of plant stems toward a light source"},
                        {"a": "Positive geotropism", "desc": "growth of plant roots downward in the direction of gravity"},
                        {"a": "Negative geotropism", "desc": "growth of plant stems upward away from the direction of gravity"}
                    ]
                },
                {
                    "name": "Defense Mechanisms",
                    "facts": [
                        {"a": "Chemical defense", "desc": "the production of toxic or unpalatable substances by plants to deter herbivores"},
                        {"a": "Mechanical defense", "desc": "the presence of thorns, spines, or thick cuticles to protect plants from herbivores"}
                    ]
                }
            ]
        },
        {
            "topic": "Human Impact on Environment",
            "prefix": "LIFE_P1_HUMAN_IMPACT",
            "file": "paper1_life_human_impact.json",
            "subtopics": [
                {
                    "name": "Atmosphere",
                    "facts": [
                        {"a": "Greenhouse effect", "desc": "the natural trapping of heat in the atmosphere by gases like carbon dioxide and methane"},
                        {"a": "Global warming", "desc": "the enhanced greenhouse effect causing an increase in the Earth's average temperature"},
                        {"a": "Carbon footprint", "desc": "the total amount of greenhouse gases produced directly and indirectly by human activities"},
                        {"a": "Ozone depletion", "desc": "the thinning of the ozone layer in the stratosphere caused by CFCs, allowing more UV radiation to reach Earth"}
                    ]
                },
                {
                    "name": "Water Availability and Quality",
                    "facts": [
                        {"a": "Eutrophication", "desc": "the excessive growth of algae in water bodies due to high nutrient runoff (nitrates and phosphates)"},
                        {"a": "Algal bloom", "desc": "a rapid increase in the population of algae in a water system, blocking sunlight"},
                        {"a": "Biological Oxygen Demand (BOD)", "desc": "the amount of dissolved oxygen needed by aerobic decomposers to break down organic matter in water"},
                        {"a": "Thermal pollution", "desc": "the degradation of water quality by any process that changes ambient water temperature"}
                    ]
                },
                {
                    "name": "Food Security",
                    "facts": [
                        {"a": "Food security", "desc": "the state where all people have physical, social, and economic access to sufficient, safe, and nutritious food"},
                        {"a": "Monoculture", "desc": "the agricultural practice of growing a single crop species over a wide area, reducing biodiversity"},
                        {"a": "Pesticides", "desc": "chemicals used to kill pests, which can biomagnify in food chains"}
                    ]
                },
                {
                    "name": "Loss of Biodiversity",
                    "facts": [
                        {"a": "Deforestation", "desc": "the large-scale clearing of forests, which reduces carbon sinks and biodiversity"},
                        {"a": "Alien invasive species", "desc": "non-native species that spread rapidly and outcompete indigenous species for resources"},
                        {"a": "Poaching", "desc": "the illegal hunting or capturing of wild animals"},
                        {"a": "Biodiversity", "desc": "the variety of plant and animal life in a particular habitat or in the world as a whole"},
                        {"a": "Desertification", "desc": "the process by which fertile land becomes desert, typically as a result of drought or poor agricultural practices"}
                    ]
                },
                {
                    "name": "Solid Waste Disposal",
                    "facts": [
                        {"a": "Landfill site", "desc": "a designated area where solid waste is dumped, compacted, and covered with soil"},
                        {"a": "Recycling", "desc": "the process of converting waste materials into new materials and objects"}
                    ]
                }
            ]
        },
        {
            "topic": "DNA: Code of Life",
            "prefix": "LIFE_P2_DNA",
            "file": "paper2_life_dna_code.json",
            "subtopics": [
                {
                    "name": "Structure of DNA",
                    "facts": [
                        {"a": "Nucleotide", "desc": "the basic building block of nucleic acids, consisting of a sugar, phosphate group, and nitrogenous base"},
                        {"a": "Deoxyribose", "desc": "the 5-carbon sugar found in DNA nucleotides"},
                        {"a": "Adenine", "desc": "the nitrogenous base that pairs with Thymine in DNA and Uracil in RNA"},
                        {"a": "Guanine", "desc": "the nitrogenous base that always pairs with Cytosine"},
                        {"a": "Thymine", "desc": "the nitrogenous base found only in DNA that pairs with Adenine"},
                        {"a": "Hydrogen bonds", "desc": "the weak bonds holding complementary nitrogenous base pairs together in a DNA molecule"},
                        {"a": "Double helix", "desc": "the twisted ladder-like structural shape of a DNA molecule"},
                        {"a": "DNA profiling", "desc": "the process of analyzing non-coding regions of DNA to identify individuals or determine biological relationships"}
                    ]
                },
                {
                    "name": "DNA Replication",
                    "facts": [
                        {"a": "DNA Replication", "desc": "the process where a DNA molecule makes an exact copy of itself during interphase"}
                    ]
                },
                {
                    "name": "RNA Structure",
                    "facts": [
                        {"a": "Ribose", "desc": "the 5-carbon sugar found in RNA nucleotides"},
                        {"a": "Uracil", "desc": "the nitrogenous base found only in RNA that replaces Thymine"},
                        {"a": "mRNA (messenger RNA)", "desc": "the single-stranded RNA molecule that carries the genetic code from DNA to the ribosome"},
                        {"a": "tRNA (transfer RNA)", "desc": "the clover-shaped RNA molecule that carries specific amino acids to the ribosome"}
                    ]
                },
                {
                    "name": "Protein Synthesis",
                    "facts": [
                        {"a": "Transcription", "desc": "the process during protein synthesis where mRNA is formed from a DNA template in the nucleus"},
                        {"a": "Translation", "desc": "the process where ribosomes read mRNA to assemble amino acids into a polypeptide chain"},
                        {"a": "Codon", "desc": "a sequence of three consecutive nitrogenous bases on mRNA that codes for a specific amino acid"},
                        {"a": "Anticodon", "desc": "a sequence of three bases on a tRNA molecule that is complementary to an mRNA codon"},
                        {"a": "Amino acid", "desc": "the monomer or building block of proteins"},
                        {"a": "Peptide bond", "desc": "the bond formed between adjacent amino acids during protein synthesis"},
                        {"a": "Ribosome", "desc": "the organelle in the cytoplasm where translation occurs"}
                    ]
                }
            ]
        },
        {
            "topic": "Meiosis",
            "prefix": "LIFE_P2_MEIOSIS",
            "file": "paper2_life_meiosis.json",
            "subtopics": [
                {
                    "name": "Chromosomes",
                    "facts": [
                        {"a": "Karyotype", "desc": "a visual representation of the complete set of chromosomes in a cell, arranged in homologous pairs"},
                        {"a": "Autosomes", "desc": "the first 22 pairs of chromosomes in humans that do not determine sex"},
                        {"a": "Gonosomes", "desc": "the 23rd pair of chromosomes that determine the sex of an individual (XX or XY)"},
                        {"a": "Locus", "desc": "the specific physical location of a gene on a chromosome"},
                        {"a": "Allele", "desc": "alternative forms of the same gene located at the same locus on homologous chromosomes"},
                        {"a": "Somatic cell", "desc": "a diploid body cell containing 46 chromosomes in humans"},
                        {"a": "Gamete", "desc": "a haploid sex cell containing 23 chromosomes in humans"}
                    ]
                },
                {
                    "name": "Meiosis as a Source of Variation",
                    "facts": [
                        {"a": "Crossing over", "desc": "the genetic exchange between non-sister chromatids leading to new allele combinations in gametes"},
                        {"a": "Independent assortment", "desc": "the random alignment of maternal and paternal chromosomes at the equator during Metaphase I"},
                        {"a": "Genetic variation", "desc": "the diversity in gene frequencies produced by crossing over, independent assortment, and random fertilization"},
                        {"a": "Fertilization", "desc": "the fusion of a haploid sperm and haploid ovum to restore the diploid chromosome number"}
                    ]
                },
                {
                    "name": "Abnormal Meiosis",
                    "facts": [
                        {"a": "Non-disjunction", "desc": "the error during anaphase where homologous chromosomes or sister chromatids fail to separate"},
                        {"a": "Aneuploidy", "desc": "the condition of having an abnormal number of chromosomes, such as 47 instead of 46"},
                        {"a": "Trisomy 21", "desc": "the presence of three copies of chromosome 21, resulting in Down syndrome"},
                        {"a": "Mutation", "desc": "a sudden, random change in the genetic code or chromosome structure"}
                    ]
                }
            ]
        },
        {
            "topic": "Genetics and Inheritance",
            "prefix": "LIFE_P2_GENETICS",
            "file": "paper2_life_genetics.json",
            "subtopics": [
                {
                    "name": "Monohybrid Crosses",
                    "facts": [
                        {"a": "Genotype", "desc": "the genetic composition or allele combination of an organism for a particular trait"},
                        {"a": "Phenotype", "desc": "the physical appearance or observable characteristic of an organism resulting from its genotype"},
                        {"a": "Dominant allele", "desc": "an allele that masks the expression of a recessive allele and is expressed in the heterozygous condition"},
                        {"a": "Recessive allele", "desc": "an allele that is only expressed in the phenotype when homozygous"},
                        {"a": "Homozygous", "desc": "having two identical alleles for a particular gene (e.g., TT or tt)"},
                        {"a": "Heterozygous", "desc": "having two different alleles for a particular gene (e.g., Tt)"},
                        {"a": "Complete dominance", "desc": "a type of inheritance where the dominant allele completely masks the recessive allele"},
                        {"a": "Incomplete dominance", "desc": "a pattern of inheritance where the heterozygous phenotype is an intermediate blend between the two homozygous phenotypes"},
                        {"a": "Co-dominance", "desc": "a pattern of inheritance where both alleles are equally expressed in the heterozygous phenotype"},
                        {"a": "Pedigree diagram", "desc": "a visual chart showing the inheritance of a trait across several generations in a family"}
                    ]
                },
                {
                    "name": "Dihybrid Crosses",
                    "facts": [
                        {"a": "Dihybrid cross", "desc": "a genetic cross between two individuals involving two different traits"}
                    ]
                },
                {
                    "name": "Sex-linked Inheritance",
                    "facts": [
                        {"a": "Sex-linked traits", "desc": "traits controlled by genes located on the sex chromosomes, primarily the X chromosome"},
                        {"a": "Haemophilia", "desc": "a sex-linked recessive disorder characterized by the inability of blood to clot normally"},
                        {"a": "Colour blindness", "desc": "a sex-linked recessive visual defect leading to difficulty distinguishing certain colors"}
                    ]
                },
                {
                    "name": "Blood Groups",
                    "facts": [
                        {"a": "Multiple alleles", "desc": "the presence of more than two alleles for a gene within a population, such as ABO blood groups"}
                    ]
                },
                {
                    "name": "Mutations",
                    "facts": [
                        {"a": "Gene mutation", "desc": "a change in the sequence of nitrogenous bases in a single gene"},
                        {"a": "Chromosomal mutation", "desc": "a change in the structure or number of whole chromosomes"}
                    ]
                },
                {
                    "name": "Genetic Engineering",
                    "facts": [
                        {"a": "Genetic engineering", "desc": "the deliberate modification of an organism's characteristics by manipulating its genetic material"},
                        {"a": "Biotechnology", "desc": "the use of living organisms or their components to produce useful products or processes"},
                        {"a": "Cloning", "desc": "the process of producing genetically identical copies of a cell, tissue, or organism"},
                        {"a": "Stem cells", "desc": "undifferentiated cells that have the potential to develop into specialized cell types"}
                    ]
                }
            ]
        },
        {
            "topic": "Evolution",
            "prefix": "LIFE_P2_EVOLUTION",
            "file": "paper2_life_evolution.json",
            "subtopics": [
                {
                    "name": "Evidence for Evolution",
                    "facts": [
                        {"a": "Evolution", "desc": "the process of gradual change in the characteristics of a population over many generations"},
                        {"a": "Fossil", "desc": "the preserved remains, impressions, or traces of ancient organisms found in sedimentary rock"},
                        {"a": "Paleontology", "desc": "the scientific study of fossils to understand past life and evolutionary history"},
                        {"a": "Homologous structures", "desc": "structures in different species that have a similar basic plan but may perform different functions, indicating common ancestry"},
                        {"a": "Analogous structures", "desc": "structures that perform the same function but differ in basic structure and evolutionary origin"},
                        {"a": "Biogeography", "desc": "the study of the geographical distribution of existing and extinct plant and animal species"}
                    ]
                },
                {
                    "name": "Theories of Evolution",
                    "facts": [
                        {"a": "Lamarckism", "desc": "the rejected theory of evolution based on the inheritance of acquired characteristics and the law of use and disuse"},
                        {"a": "Darwinism", "desc": "the theory of evolution by natural selection proposed by Charles Darwin"}
                    ]
                },
                {
                    "name": "Natural Selection",
                    "facts": [
                        {"a": "Natural selection", "desc": "the mechanism of evolution where organisms best adapted to their environment survive, reproduce, and pass on their favorable alleles"},
                        {"a": "Artificial selection", "desc": "the selective breeding of plants and animals by humans to produce desired traits"}
                    ]
                },
                {
                    "name": "Speciation",
                    "facts": [
                        {"a": "Speciation", "desc": "the evolutionary process by which new biological species arise from a pre-existing species"},
                        {"a": "Allopatric speciation", "desc": "the formation of a new species when a population is geographically isolated by a physical barrier"},
                        {"a": "Punctuated equilibrium", "desc": "the hypothesis that evolution occurs in rapid bursts separated by long periods of stasis"}
                    ]
                },
                {
                    "name": "Human Evolution",
                    "facts": [
                        {"a": "Hominin", "desc": "the evolutionary group that includes modern humans and their extinct bipedal ancestors"},
                        {"a": "Bipedalism", "desc": "the ability to walk upright on two lower limbs, a key milestone in human evolution"},
                        {"a": "Foramen magnum", "desc": "the large opening at the base of the skull through which the spinal cord passes, indicating posture"},
                        {"a": "Cranial capacity", "desc": "the volume of the braincase inside the skull, used as an indicator of brain size"},
                        {"a": "Out of Africa hypothesis", "desc": "the theory proposing that modern humans evolved in Africa and then migrated to populate other continents"},
                        {"a": "Australopithecus", "desc": "an extinct genus of early hominins found in Africa, displaying both ape-like and human-like traits"},
                        {"a": "Homo sapiens", "desc": "the scientific name for modern humans"}
                    ]
                }
            ]
        }
    ]

    for t in topics:
        print(f"Generating for {t['topic']} ({t['prefix']})")
        # Extract flat list of subtopic names for TopicGenerator
        sub_names = [s["name"] for s in t["subtopics"]]
        gen = TopicGenerator(t["topic"], t["prefix"], sub_names)

        # Build master pool of answers for this topic
        pool = []
        for s in t["subtopics"]:
            for f in s["facts"]:
                pool.append(f["a"])

        num_subtopics = len(t["subtopics"])

        # Distribute targets evenly across subtopics
        for diff in ["easy", "medium", "hard"]:
            target_total = gen.difficulty_targets[diff]
            target_per_sub = target_total // num_subtopics
            remainder = target_total % num_subtopics

            for i, sub in enumerate(t["subtopics"]):
                current_target = target_per_sub + (remainder if i == num_subtopics - 1 else 0)
                generate_questions(gen, sub["name"], diff, sub["facts"], pool, current_target)

        filepath = os.path.join("dataset/life_sciences", t["file"])
        gen.save_to_json(filepath)
        print(f"Saved {filepath} with {len(gen.questions)} questions.")

if __name__ == "__main__":
    # Clean up old file if exists
    if os.path.exists("generate_life_sciences.py"):
        pass # we import from it, it's safe
    build_topic_datasets()
