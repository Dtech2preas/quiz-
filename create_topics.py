import json

data = [
  {
    "topic": "Meiosis",
    "prefix": "LIFE_P1_MEIOSIS",
    "file": "paper1_life_meiosis.json",
    "subtopics": [
      {
        "name": "Cell Division",
        "facts": [
          {
            "a": "Homologous chromosomes",
            "desc": "chromosomes that are identical in shape, size, and gene loci, one inherited from each parent",
            "w": ["Analogous chromosomes", "Heterologous chromosomes", "Sister chromatids", "Bivalents", "Chiasmata"]
          },
          {
            "a": "Haploid",
            "desc": "cells containing only one set of chromosomes (n)",
            "w": ["Diploid", "Polyploid", "Aneuploid", "Triploid", "Somatic"]
          },
          {
            "a": "Diploid",
            "desc": "cells containing two sets of chromosomes (2n)",
            "w": ["Haploid", "Polyploid", "Aneuploid", "Triploid", "Gametic"]
          },
          {
            "a": "Centromere",
            "desc": "the structure that holds two sister chromatids together in a replicated chromosome",
            "w": ["Centrosome", "Centriole", "Chiasma", "Telomere", "Spindle fibre"]
          },
          {
            "a": "Spindle fibres",
            "desc": "protein structures that contract to pull chromosomes or chromatids to the poles during cell division",
            "w": ["Centromeres", "Microtubules", "Centrioles", "Nuclear membranes", "Chromatin"]
          },
          {
            "a": "Chromatin",
            "desc": "the thread-like network of DNA and proteins found in the nucleus during interphase",
            "w": ["Chromatid", "Chromosome", "Centromere", "Chiasma", "Centrosome"]
          },
          {
            "a": "Sister chromatids",
            "desc": "two identical copies of a chromosome produced by DNA replication and joined by a centromere",
            "w": ["Homologous chromosomes", "Non-sister chromatids", "Bivalents", "Tetrads", "Autosomes"]
          },
          {
            "a": "Centrosome",
            "desc": "an organelle near the nucleus of a cell that contains the centrioles (in animal cells) and from which the spindle fibers develop",
            "w": ["Centromere", "Centriole", "Chiasma", "Nucleolus", "Cytoplasm"]
          }
        ]
      },
      {
        "name": "Phases of Meiosis",
        "facts": [
          {
            "a": "Prophase I",
            "desc": "the phase of meiosis where homologous chromosomes pair up and crossing over occurs",
            "w": ["Metaphase I", "Anaphase I", "Prophase II", "Telophase I", "Interphase"]
          },
          {
            "a": "Metaphase I",
            "desc": "the phase where homologous chromosome pairs align randomly at the equator of the cell",
            "w": ["Prophase I", "Anaphase I", "Metaphase II", "Telophase II", "Interphase"]
          },
          {
            "a": "Anaphase I",
            "desc": "the phase where entire chromosomes (consisting of two chromatids) are pulled to opposite poles",
            "w": ["Metaphase I", "Anaphase II", "Telophase I", "Prophase II", "Metaphase II"]
          },
          {
            "a": "Telophase I",
            "desc": "the phase resulting in the formation of two haploid cells, each containing double-stranded chromosomes",
            "w": ["Prophase I", "Metaphase I", "Anaphase I", "Telophase II", "Prophase II"]
          },
          {
            "a": "Prophase II",
            "desc": "the phase where the spindle fibres form in the two newly formed haploid cells without further DNA replication",
            "w": ["Prophase I", "Metaphase II", "Anaphase II", "Telophase I", "Metaphase I"]
          },
          {
            "a": "Metaphase II",
            "desc": "the phase where individual chromosomes align singly at the equator of the cell",
            "w": ["Metaphase I", "Prophase II", "Anaphase II", "Telophase II", "Anaphase I"]
          },
          {
            "a": "Anaphase II",
            "desc": "the phase where the centromere splits and sister chromatids separate to move to opposite poles",
            "w": ["Anaphase I", "Metaphase II", "Telophase II", "Prophase II", "Telophase I"]
          },
          {
            "a": "Telophase II",
            "desc": "the final phase of meiosis where four genetically unique haploid cells are formed",
            "w": ["Telophase I", "Anaphase II", "Metaphase II", "Prophase II", "Anaphase I"]
          },
          {
            "a": "Bivalent",
            "desc": "a pair of homologous chromosomes closely associated during Prophase I",
            "w": ["Chromatid", "Centromere", "Chiasma", "Centrosome", "Spindle fibre"]
          },
          {
            "a": "Interphase",
            "desc": "the resting phase before meiosis begins, during which DNA replication occurs",
            "w": ["Prophase I", "Metaphase I", "Telophase I", "Cytokinesis", "Karyokinesis"]
          }
        ]
      },
      {
        "name": "Importance of Meiosis",
        "facts": [
          {
            "a": "Crossing over",
            "desc": "the exchange of genetic material between non-sister chromatids of a bivalent, promoting genetic variation",
            "w": ["Independent assortment", "Non-disjunction", "Mutation", "Fertilization", "Replication"]
          },
          {
            "a": "Independent assortment",
            "desc": "the random arrangement of maternal and paternal homologous chromosomes at the equator during Metaphase I",
            "w": ["Crossing over", "Non-disjunction", "Linkage", "Segregation", "Mutation"]
          },
          {
            "a": "Chiasmata",
            "desc": "the specific points of attachment where crossing over occurs between non-sister chromatids",
            "w": ["Centromeres", "Telomeres", "Centrioles", "Kinetochores", "Spindles"]
          },
          {
            "a": "Non-disjunction",
            "desc": "the failure of homologous chromosomes or sister chromatids to separate correctly during meiosis",
            "w": ["Independent assortment", "Crossing over", "Synapsis", "Segregation", "Mutation"]
          },
          {
            "a": "Down syndrome",
            "desc": "a genetic disorder (Trisomy 21) caused by an extra copy of chromosome 21 due to non-disjunction",
            "w": ["Haemophilia", "Colour blindness", "Turner syndrome", "Klinefelter syndrome", "Albinism"]
          },
          {
            "a": "Gametes",
            "desc": "haploid sex cells produced as a result of meiosis, essential for sexual reproduction",
            "w": ["Somatic cells", "Zygotes", "Embryos", "Stem cells", "Blastocysts"]
          },
          {
            "a": "Reduction division",
            "desc": "another term for meiosis I, as it halves the chromosome number from diploid to haploid",
            "w": ["Equational division", "Mitosis", "Fertilization", "Cleavage", "Cytokinesis"]
          },
          {
            "a": "Genetic variation",
            "desc": "the diversity in gene combinations among offspring, largely resulting from crossing over and independent assortment",
            "w": ["Cloning", "Mitosis", "Asexual reproduction", "Homozygosity", "Inbreeding"]
          }
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
          {
            "a": "Ovipary",
            "desc": "a reproductive strategy where eggs are laid outside the body and embryos develop externally",
            "w": ["Vivipary", "Ovovivipary", "Marsupial", "Placental", "Altricial"]
          },
          {
            "a": "Ovovivipary",
            "desc": "a reproductive strategy where embryos develop inside eggs that are retained within the mother's body until hatching",
            "w": ["Ovipary", "Vivipary", "Precocial", "Altricial", "External fertilization"]
          },
          {
            "a": "Vivipary",
            "desc": "a reproductive strategy where embryos develop inside the mother's body and obtain nourishment directly via a placenta",
            "w": ["Ovipary", "Ovovivipary", "Amniote", "Precocial", "Spawning"]
          },
          {
            "a": "Precocial development",
            "desc": "a developmental strategy where offspring are born or hatched fully developed, able to move and feed independently",
            "w": ["Altricial development", "Vivipary", "Ovovivipary", "Metamorphosis", "Gestation"]
          },
          {
            "a": "Altricial development",
            "desc": "a developmental strategy where offspring are born or hatched naked, blind, and highly dependent on parental care",
            "w": ["Precocial development", "Ovipary", "Metamorphosis", "Vivipary", "Independent assortment"]
          }
        ]
      },
      {
        "name": "Fertilization",
        "facts": [
          {
            "a": "External fertilization",
            "desc": "the union of sperm and egg outside the body of the female, typical in aquatic environments",
            "w": ["Internal fertilization", "Copulation", "Implantation", "Gestation", "Ovovivipary"]
          },
          {
            "a": "Internal fertilization",
            "desc": "the union of sperm and egg inside the body of the female, maximizing reproductive success in terrestrial environments",
            "w": ["External fertilization", "Spawning", "Ovipary", "Parthenogenesis", "Asexual reproduction"]
          },
          {
            "a": "Copulation",
            "desc": "the physical act of mating allowing for the direct transfer of sperm into the female for internal fertilization",
            "w": ["Spawning", "Ovulation", "Menstruation", "Implantation", "Gestation"]
          },
          {
            "a": "Spawning",
            "desc": "the simultaneous release of large numbers of eggs and sperm into the water, characteristic of external fertilization",
            "w": ["Copulation", "Internal fertilization", "Vivipary", "Gestation", "Implantation"]
          }
        ]
      },
      {
        "name": "Embryonic Development",
        "facts": [
          {
            "a": "Amniotic egg",
            "desc": "an egg with a shell and extra-embryonic membranes adapted for survival in terrestrial environments",
            "w": ["Jelly-coated egg", "Spore", "Zygote", "Blastocyst", "Placenta"]
          },
          {
            "a": "Amnion",
            "desc": "the fluid-filled sac that surrounds and cushions the developing embryo against mechanical shock",
            "w": ["Chorion", "Allantois", "Yolk sac", "Placenta", "Shell"]
          },
          {
            "a": "Chorion",
            "desc": "the outermost extra-embryonic membrane primarily involved in gaseous exchange",
            "w": ["Amnion", "Allantois", "Yolk sac", "Amniotic fluid", "Endometrium"]
          },
          {
            "a": "Allantois",
            "desc": "the extra-embryonic membrane sac that collects metabolic wastes and assists with gaseous exchange",
            "w": ["Amnion", "Chorion", "Yolk sac", "Placenta", "Umbilical cord"]
          },
          {
            "a": "Yolk sac",
            "desc": "the extra-embryonic membrane that stores and provides nourishment to the developing embryo",
            "w": ["Amnion", "Chorion", "Allantois", "Placenta", "Amniotic fluid"]
          },
          {
            "a": "Amniotic fluid",
            "desc": "the liquid within the amnion that protects the embryo from mechanical shock and temperature changes",
            "w": ["Blood plasma", "Cerebrospinal fluid", "Yolk", "Albumen", "Seminal fluid"]
          },
          {
            "a": "Parental care",
            "desc": "the investment of time and energy by parents to increase the survival chances of their offspring",
            "w": ["Precocial development", "External fertilization", "Spawning", "Altricial development", "Vivipary"]
          },
          {
            "a": "Albumen",
            "desc": "the egg white in an amniotic egg that provides water and additional protein to the embryo",
            "w": ["Yolk", "Chorion", "Allantois", "Amnion", "Shell"]
          }
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
          {
            "a": "Testes",
            "desc": "male organs located in the scrotum responsible for the production of sperm and testosterone",
            "w": ["Ovaries", "Prostate gland", "Epididymis", "Seminal vesicles", "Vas deferens"]
          },
          {
            "a": "Epididymis",
            "desc": "the highly coiled tube on top of the testis where sperm mature and are temporarily stored",
            "w": ["Vas deferens", "Seminiferous tubules", "Prostate gland", "Urethra", "Cowper's gland"]
          },
          {
            "a": "Vas deferens",
            "desc": "the muscular tube that transports sperm from the epididymis to the urethra",
            "w": ["Fallopian tube", "Ureter", "Epididymis", "Seminiferous tubule", "Urethra"]
          },
          {
            "a": "Seminal vesicles",
            "desc": "glands that secrete a nutrient-rich fluid containing fructose to provide energy for sperm",
            "w": ["Prostate gland", "Cowper's gland", "Testes", "Epididymis", "Scrotum"]
          },
          {
            "a": "Prostate gland",
            "desc": "a gland that secretes an alkaline fluid to neutralize the acidic environment of the vagina and urethra",
            "w": ["Seminal vesicles", "Cowper's gland", "Epididymis", "Testes", "Vas deferens"]
          },
          {
            "a": "Cowper's gland",
            "desc": "a small gland that secretes a lubricating fluid into the urethra before ejaculation",
            "w": ["Prostate gland", "Seminal vesicles", "Testes", "Epididymis", "Scrotum"]
          },
          {
            "a": "Seminiferous tubules",
            "desc": "the highly coiled microscopic tubes within the testes where spermatogenesis takes place",
            "w": ["Epididymis", "Vas deferens", "Urethra", "Fallopian tubes", "Interstitial cells"]
          },
          {
            "a": "Sertoli cells",
            "desc": "supporting cells in the seminiferous tubules that provide nourishment to developing sperm",
            "w": ["Interstitial cells (Leydig cells)", "Graafian follicles", "Spermatogonia", "Oocytes", "Corpus luteum"]
          },
          {
            "a": "Interstitial cells (Leydig cells)",
            "desc": "cells located between the seminiferous tubules that secrete the hormone testosterone",
            "w": ["Sertoli cells", "Spermatogonia", "Follicle cells", "Prostate cells", "Oocytes"]
          },
          {
            "a": "Acrosome",
            "desc": "the cap-like structure at the head of a sperm cell containing enzymes to penetrate the ovum",
            "w": ["Midpiece", "Flagellum", "Nucleus", "Centriole", "Mitochondrion"]
          }
        ]
      },
      {
        "name": "Female Reproductive System",
        "facts": [
          {
            "a": "Ovaries",
            "desc": "female gonads responsible for the production of ova, oestrogen, and progesterone",
            "w": ["Testes", "Fallopian tubes", "Uterus", "Cervix", "Vagina"]
          },
          {
            "a": "Fallopian tubes",
            "desc": "the muscular tubes lined with cilia where fertilization typically occurs in humans",
            "w": ["Vas deferens", "Uterus", "Vagina", "Cervix", "Ovaries"]
          },
          {
            "a": "Uterus",
            "desc": "the thick-walled, muscular organ where the embryo implants and develops during pregnancy",
            "w": ["Ovary", "Fallopian tube", "Cervix", "Vagina", "Placenta"]
          },
          {
            "a": "Endometrium",
            "desc": "the inner lining of the uterus that is richly supplied with blood vessels and thickens during the menstrual cycle",
            "w": ["Myometrium", "Cervix", "Graafian follicle", "Corpus luteum", "Amnion"]
          },
          {
            "a": "Cervix",
            "desc": "the lower, narrow neck of the uterus that opens into the vagina",
            "w": ["Fallopian tube", "Ovary", "Endometrium", "Vulva", "Urethra"]
          },
          {
            "a": "Graafian follicle",
            "desc": "the mature fluid-filled ovarian follicle that ruptures to release a secondary oocyte during ovulation",
            "w": ["Corpus luteum", "Primary follicle", "Endometrium", "Placenta", "Acrosome"]
          },
          {
            "a": "Corpus luteum",
            "desc": "the glandular structure formed from the ruptured follicle after ovulation, which secretes progesterone",
            "w": ["Graafian follicle", "Primary follicle", "Endometrium", "Placenta", "Ovary"]
          },
          {
            "a": "Germinal epithelium",
            "desc": "the outer layer of cells covering the ovary, from which primary follicles develop",
            "w": ["Endometrium", "Myometrium", "Cervix", "Corpus luteum", "Graafian follicle"]
          }
        ]
      },
      {
        "name": "Menstrual Cycle",
        "facts": [
          {
            "a": "Ovulation",
            "desc": "the release of a mature ovum from the Graafian follicle into the fallopian tube, usually around day 14",
            "w": ["Menstruation", "Implantation", "Fertilization", "Gestation", "Parturition"]
          },
          {
            "a": "FSH",
            "desc": "Follicle Stimulating Hormone, secreted by the pituitary, which stimulates the development of primary follicles in the ovary",
            "w": ["LH", "Oestrogen", "Progesterone", "Prolactin", "Oxytocin"]
          },
          {
            "a": "LH",
            "desc": "Luteinizing Hormone, secreted by the pituitary, which triggers ovulation and the formation of the corpus luteum",
            "w": ["FSH", "Oestrogen", "Progesterone", "TSH", "Growth Hormone"]
          },
          {
            "a": "Oestrogen",
            "desc": "the hormone produced by the growing follicle that initiates the thickening of the endometrium and inhibits FSH",
            "w": ["Progesterone", "LH", "FSH", "Testosterone", "Aldosterone"]
          },
          {
            "a": "Progesterone",
            "desc": "the hormone produced by the corpus luteum that maintains the thick, highly vascular endometrium for pregnancy",
            "w": ["Oestrogen", "FSH", "LH", "Prolactin", "Oxytocin"]
          },
          {
            "a": "Menstruation",
            "desc": "the shedding of the thickened endometrial lining accompanied by bleeding when fertilization does not occur",
            "w": ["Ovulation", "Implantation", "Gestation", "Luteal phase", "Follicular phase"]
          },
          {
            "a": "Follicular phase",
            "desc": "the first half of the ovarian cycle during which a follicle matures under the influence of FSH",
            "w": ["Luteal phase", "Menstruation", "Gestation", "Implantation", "Parturition"]
          },
          {
            "a": "Luteal phase",
            "desc": "the second half of the ovarian cycle characterized by the presence and function of the corpus luteum",
            "w": ["Follicular phase", "Menstruation", "Ovulation", "Implantation", "Gestation"]
          }
        ]
      },
      {
        "name": "Pregnancy and Birth",
        "facts": [
          {
            "a": "Placenta",
            "desc": "the temporary organ formed from maternal and embryonic tissue that facilitates the exchange of nutrients, gases, and wastes",
            "w": ["Amnion", "Umbilical cord", "Corpus luteum", "Endometrium", "Yolk sac"]
          },
          {
            "a": "Umbilical cord",
            "desc": "the hollow tube connecting the fetus to the placenta, typically containing two umbilical arteries and one umbilical vein",
            "w": ["Fallopian tube", "Amnion", "Chorion", "Vas deferens", "Ureter"]
          },
          {
            "a": "Implantation",
            "desc": "the attachment and embedding of the blastocyst into the thickened endometrial lining of the uterus",
            "w": ["Fertilization", "Ovulation", "Menstruation", "Gestation", "Parturition"]
          },
          {
            "a": "Gestation",
            "desc": "the period of development of the embryo and fetus in the uterus from fertilization to birth",
            "w": ["Menstruation", "Ovulation", "Implantation", "Lactation", "Menopause"]
          },
          {
            "a": "Chorionic villi",
            "desc": "finger-like projections from the chorion that embed into the endometrium to form the embryonic part of the placenta",
            "w": ["Amniotic fluid", "Umbilical arteries", "Graafian follicles", "Cilia", "Microvilli"]
          },
          {
            "a": "Oxytocin",
            "desc": "the hormone secreted by the pituitary gland that stimulates strong uterine contractions during labour",
            "w": ["Prolactin", "Progesterone", "Oestrogen", "FSH", "LH"]
          },
          {
            "a": "Prolactin",
            "desc": "the pituitary hormone that stimulates the mammary glands to produce milk after birth",
            "w": ["Oxytocin", "Progesterone", "Oestrogen", "LH", "FSH"]
          }
        ]
      }
    ]
  }
]

data_part2 = [
  {
    "topic": "Responding to the Environment (Humans)",
    "prefix": "LIFE_P1_ENV_HUMANS",
    "file": "paper1_life_environment_humans.json",
    "subtopics": [
      {
        "name": "Nervous System",
        "facts": [
          {
            "a": "Central Nervous System",
            "desc": "the primary command center of the nervous system consisting of the brain and spinal cord",
            "w": ["Peripheral Nervous System", "Autonomic Nervous System", "Sympathetic Nervous System", "Endocrine System", "Somatic Nervous System"]
          },
          {
            "a": "Peripheral Nervous System",
            "desc": "all the cranial and spinal nerves extending from the brain and spinal cord to the rest of the body",
            "w": ["Central Nervous System", "Brain", "Spinal Cord", "Endocrine System", "Medulla oblongata"]
          },
          {
            "a": "Sensory neuron",
            "desc": "a specialized neuron (afferent) that carries nerve impulses from receptors to the central nervous system",
            "w": ["Motor neuron", "Interneuron", "Effector", "Schwann cell", "Synapse"]
          },
          {
            "a": "Motor neuron",
            "desc": "a specialized neuron (efferent) that carries nerve impulses from the central nervous system to effectors (muscles or glands)",
            "w": ["Sensory neuron", "Interneuron", "Receptor", "Ganglion", "Dendrite"]
          },
          {
            "a": "Interneuron",
            "desc": "a multipolar neuron entirely within the CNS that connects sensory and motor neurons",
            "w": ["Sensory neuron", "Motor neuron", "Schwann cell", "Receptor", "Effector"]
          },
          {
            "a": "Synapse",
            "desc": "the microscopic gap between the axon terminal of one neuron and the dendrite of the next, where neurotransmitters diffuse",
            "w": ["Node of Ranvier", "Myelin sheath", "Ganglion", "Receptor", "Effector"]
          },
          {
            "a": "Neurotransmitter",
            "desc": "a chemical substance released at a synapse that transmits an impulse across the synaptic gap",
            "w": ["Hormone", "Enzyme", "Antibody", "Myelin", "Antigen"]
          },
          {
            "a": "Myelin sheath",
            "desc": "a fatty insulating layer around many axons that speeds up the transmission of nerve impulses",
            "w": ["Dendrite", "Synapse", "Node of Ranvier", "Cell body", "Axon terminal"]
          }
        ]
      },
      {
        "name": "Brain and Spinal Cord",
        "facts": [
          {
            "a": "Cerebrum",
            "desc": "the largest part of the brain responsible for voluntary actions, conscious thought, memory, and processing sensory information",
            "w": ["Cerebellum", "Medulla oblongata", "Hypothalamus", "Spinal cord", "Corpus callosum"]
          },
          {
            "a": "Cerebellum",
            "desc": "the part of the brain located behind the brainstem, responsible for coordinating voluntary muscle movements and maintaining balance",
            "w": ["Cerebrum", "Medulla oblongata", "Hypothalamus", "Pituitary gland", "Corpus callosum"]
          },
          {
            "a": "Medulla oblongata",
            "desc": "the lowest part of the brainstem that controls involuntary vital functions such as breathing rate and heartbeat",
            "w": ["Cerebrum", "Cerebellum", "Hypothalamus", "Corpus callosum", "Thalamus"]
          },
          {
            "a": "Hypothalamus",
            "desc": "the brain region that maintains homeostasis (e.g., body temperature, thirst) and links the nervous and endocrine systems",
            "w": ["Cerebellum", "Medulla oblongata", "Cerebrum", "Corpus callosum", "Meninges"]
          },
          {
            "a": "Corpus callosum",
            "desc": "a broad band of nerve fibers joining the two hemispheres of the cerebrum, allowing them to communicate",
            "w": ["Medulla oblongata", "Hypothalamus", "Meninges", "Spinal cord", "Central canal"]
          },
          {
            "a": "Meninges",
            "desc": "the three protective connective tissue membranes that surround the brain and spinal cord",
            "w": ["Myelin sheath", "Cerebrospinal fluid", "Grey matter", "White matter", "Cranium"]
          }
        ]
      },
      {
        "name": "Reflex Arc",
        "facts": [
          {
            "a": "Reflex action",
            "desc": "a rapid, automatic, and involuntary response to a stimulus designed to protect the body from harm",
            "w": ["Voluntary action", "Conditioned reflex", "Synaptic transmission", "Homeostasis", "Accommodation"]
          },
          {
            "a": "Reflex arc",
            "desc": "the specific structural neural pathway followed by an impulse during a reflex action",
            "w": ["Central Nervous System", "Spinal cord", "Synapse", "Peripheral Nervous System", "Brainstem"]
          },
          {
            "a": "Receptor",
            "desc": "a specialized sensory cell or structure that detects a specific stimulus and converts it into a nerve impulse",
            "w": ["Effector", "Interneuron", "Motor neuron", "Synapse", "Ganglion"]
          },
          {
            "a": "Effector",
            "desc": "a muscle or gland that brings about a specific response to a stimulus after receiving an impulse from a motor neuron",
            "w": ["Receptor", "Sensory neuron", "Interneuron", "Synapse", "Dendrite"]
          }
        ]
      },
      {
        "name": "Human Eye",
        "facts": [
          {
            "a": "Cornea",
            "desc": "the transparent, curved front part of the sclera that allows light to enter the eye and causes the most refraction",
            "w": ["Lens", "Retina", "Iris", "Pupil", "Choroid"]
          },
          {
            "a": "Iris",
            "desc": "the pigmented, muscular ring that controls the size of the pupil and the amount of light entering the eye",
            "w": ["Cornea", "Lens", "Retina", "Sclera", "Ciliary body"]
          },
          {
            "a": "Lens",
            "desc": "the transparent, biconvex, elastic structure that changes shape to focus light precisely onto the retina",
            "w": ["Cornea", "Pupil", "Iris", "Retina", "Aqueous humour"]
          },
          {
            "a": "Retina",
            "desc": "the inner, light-sensitive layer of the eye containing photoreceptors (rods and cones)",
            "w": ["Choroid", "Sclera", "Cornea", "Iris", "Macula lutea"]
          },
          {
            "a": "Accommodation",
            "desc": "the reflex process by which the ciliary muscles alter the curvature of the lens to focus on objects at varying distances",
            "w": ["Pupillary mechanism", "Binocular vision", "Refraction", "Astigmatism", "Myopia"]
          },
          {
            "a": "Pupillary mechanism",
            "desc": "the reflex action of the iris muscles that alters pupil size in response to varying light intensities",
            "w": ["Accommodation", "Binocular vision", "Refraction", "Astigmatism", "Hypermetropia"]
          },
          {
            "a": "Ciliary body",
            "desc": "the structure containing muscles that control the tension on the suspensory ligaments to change the shape of the lens",
            "w": ["Iris", "Choroid", "Sclera", "Cornea", "Retina"]
          },
          {
            "a": "Suspensory ligaments",
            "desc": "tough, inelastic fibers that hold the lens in position and attach it to the ciliary body",
            "w": ["Optic nerve", "Ciliary muscles", "Iris", "Sclera", "Choroid"]
          },
          {
            "a": "Yellow spot (Macula lutea)",
            "desc": "the central area of the retina containing a high concentration of cones, responsible for the sharpest vision",
            "w": ["Blind spot", "Fovea centralis", "Optic disc", "Cornea", "Lens"]
          },
          {
            "a": "Blind spot",
            "desc": "the point on the retina where the optic nerve exits the eye, lacking photoreceptors",
            "w": ["Yellow spot", "Macula lutea", "Fovea centralis", "Pupil", "Iris"]
          },
          {
            "a": "Rods",
            "desc": "photoreceptors in the retina sensitive to low light intensities, providing black-and-white vision",
            "w": ["Cones", "Ganglion cells", "Bipolar cells", "Ciliary muscles", "Iris muscles"]
          },
          {
            "a": "Cones",
            "desc": "photoreceptors in the retina sensitive to bright light and responsible for color vision and visual acuity",
            "w": ["Rods", "Ganglion cells", "Bipolar cells", "Ciliary muscles", "Iris muscles"]
          }
        ]
      },
      {
        "name": "Human Ear",
        "facts": [
          {
            "a": "Pinna",
            "desc": "the visible, outer cartilaginous part of the ear that acts as a funnel to collect and direct sound waves",
            "w": ["Tympanic membrane", "Auditory canal", "Cochlea", "Ossicles", "Eustachian tube"]
          },
          {
            "a": "Tympanic membrane",
            "desc": "the thin, tightly stretched membrane (eardrum) separating the outer and middle ear which vibrates in response to sound waves",
            "w": ["Oval window", "Round window", "Pinna", "Cochlea", "Macula"]
          },
          {
            "a": "Ossicles",
            "desc": "the three small interconnected bones (malleus, incus, stapes) in the middle ear that transmit and heavily amplify vibrations",
            "w": ["Semicircular canals", "Otoliths", "Cochlea", "Auditory nerve", "Eustachian tube"]
          },
          {
            "a": "Eustachian tube",
            "desc": "the tube connecting the middle ear to the pharynx, functioning to equalize air pressure on both sides of the tympanic membrane",
            "w": ["Auditory canal", "Semicircular canals", "Cochlea", "Auditory nerve", "Vestibular nerve"]
          },
          {
            "a": "Cochlea",
            "desc": "the coiled, fluid-filled bony structure in the inner ear containing the Organ of Corti for hearing",
            "w": ["Semicircular canals", "Utriculus", "Sacculus", "Tympanic membrane", "Ossicles"]
          },
          {
            "a": "Organ of Corti",
            "desc": "the specialized receptor structure within the cochlea that converts mechanical vibrations into nerve impulses",
            "w": ["Maculae", "Cristae", "Tympanic membrane", "Ossicles", "Oval window"]
          },
          {
            "a": "Semicircular canals",
            "desc": "three fluid-filled, loop-like structures in the inner ear responsible for dynamic balance and detecting changes in speed or direction",
            "w": ["Cochlea", "Utriculus", "Sacculus", "Ossicles", "Auditory canal"]
          },
          {
            "a": "Oval window",
            "desc": "the membrane-covered opening from the middle ear to the inner ear, against which the stapes vibrates to create pressure waves in the cochlear fluid",
            "w": ["Round window", "Tympanic membrane", "Organ of Corti", "Macula", "Crista"]
          },
          {
            "a": "Round window",
            "desc": "the membrane at the base of the cochlea that bulges outward to absorb pressure waves and prevent echo in the inner ear",
            "w": ["Oval window", "Tympanic membrane", "Eustachian tube", "Macula", "Crista"]
          }
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
          {
            "a": "Endocrine gland",
            "desc": "a highly vascularized, ductless gland that secretes hormones directly into the bloodstream",
            "w": ["Exocrine gland", "Sweat gland", "Salivary gland", "Sebaceous gland", "Lymph node"]
          },
          {
            "a": "Exocrine gland",
            "desc": "a gland that secretes its products into ducts that lead to external surfaces or specific cavities (e.g., salivary glands)",
            "w": ["Endocrine gland", "Pituitary gland", "Thyroid gland", "Adrenal gland", "Islets of Langerhans"]
          },
          {
            "a": "Pituitary gland",
            "desc": "the small 'master gland' located at the base of the brain that secretes many hormones controlling other endocrine glands",
            "w": ["Hypothalamus", "Thyroid gland", "Adrenal gland", "Pancreas", "Pineal gland"]
          },
          {
            "a": "Thyroid gland",
            "desc": "the butterfly-shaped gland located in the neck that secretes thyroxin to regulate metabolism",
            "w": ["Pituitary gland", "Adrenal gland", "Thymus", "Pancreas", "Parathyroid gland"]
          },
          {
            "a": "Adrenal glands",
            "desc": "the paired glands situated immediately above the kidneys that secrete adrenaline and aldosterone",
            "w": ["Thyroid gland", "Pituitary gland", "Pancreas", "Ovaries", "Testes"]
          },
          {
            "a": "Pancreas",
            "desc": "a dual-function organ acting as both an exocrine gland (digestive juice) and an endocrine gland (insulin and glucagon)",
            "w": ["Liver", "Gallbladder", "Thyroid gland", "Pituitary gland", "Adrenal gland"]
          },
          {
            "a": "Islets of Langerhans",
            "desc": "the specific clusters of endocrine cells within the pancreas that secrete insulin (beta cells) and glucagon (alpha cells)",
            "w": ["Graafian follicles", "Corpus luteum", "Seminiferous tubules", "Interstitial cells", "Glomeruli"]
          }
        ]
      },
      {
        "name": "Hormones",
        "facts": [
          {
            "a": "Hormone",
            "desc": "a chemical messenger, usually a protein or steroid, produced by an endocrine gland and transported in blood to target organs",
            "w": ["Enzyme", "Antibody", "Neurotransmitter", "Antigen", "Vitamin"]
          },
          {
            "a": "Thyroxin",
            "desc": "the iodine-containing hormone that regulates the basal metabolic rate, growth, and development of the body",
            "w": ["Adrenaline", "Insulin", "TSH", "Growth Hormone", "Glucagon"]
          },
          {
            "a": "Adrenaline",
            "desc": "the 'fight or flight' hormone that rapidly prepares the body for physical emergencies by increasing heart rate and blood glucose",
            "w": ["Thyroxin", "Insulin", "Aldosterone", "ADH", "Glucagon"]
          },
          {
            "a": "Insulin",
            "desc": "the hormone secreted by beta cells of the pancreas that lowers blood glucose levels by promoting its conversion to glycogen in the liver",
            "w": ["Glucagon", "Adrenaline", "Thyroxin", "Aldosterone", "Cortisol"]
          },
          {
            "a": "Glucagon",
            "desc": "the hormone secreted by alpha cells of the pancreas that raises blood glucose levels by stimulating the breakdown of glycogen",
            "w": ["Insulin", "Adrenaline", "Thyroxin", "Aldosterone", "Cortisol"]
          },
          {
            "a": "TSH (Thyroid Stimulating Hormone)",
            "desc": "the pituitary hormone that specifically stimulates the thyroid gland to secrete thyroxin",
            "w": ["FSH", "LH", "Growth Hormone", "Prolactin", "ACTH"]
          },
          {
            "a": "Aldosterone",
            "desc": "the steroid hormone from the adrenal cortex that regulates sodium ion reabsorption in the kidneys",
            "w": ["ADH", "Adrenaline", "Thyroxin", "Cortisol", "Insulin"]
          },
          {
            "a": "ADH (Antidiuretic Hormone)",
            "desc": "the pituitary hormone that increases the permeability of kidney collecting ducts to water, promoting water reabsorption",
            "w": ["Aldosterone", "TSH", "FSH", "Prolactin", "Oxytocin"]
          }
        ]
      },
      {
        "name": "Negative Feedback",
        "facts": [
          {
            "a": "Negative feedback mechanism",
            "desc": "a control system where an increase or decrease in a substance triggers a response that reverses the change, restoring a set point",
            "w": ["Positive feedback mechanism", "Reflex action", "Accommodation", "Synaptic transmission", "Action potential"]
          },
          {
            "a": "Diabetes mellitus",
            "desc": "a chronic metabolic disease resulting from inadequate insulin production or insulin resistance, leading to abnormally high blood glucose",
            "w": ["Goitre", "Hyperthyroidism", "Hypothyroidism", "Gigantism", "Dwarfism"]
          },
          {
            "a": "Goitre",
            "desc": "the physical enlargement of the thyroid gland, often due to an iodine deficiency attempting to compensate for low thyroxin levels",
            "w": ["Diabetes mellitus", "Acromegaly", "Gigantism", "Dwarfism", "Cretinism"]
          }
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
          {
            "a": "Homeostasis",
            "desc": "the continuous physiological process of maintaining a relatively constant internal environment despite external changes",
            "w": ["Thermoregulation", "Osmoregulation", "Negative feedback", "Metabolism", "Respiration"]
          },
          {
            "a": "Thermoregulation",
            "desc": "the specific homeostatic process of maintaining a constant internal body temperature (around 37°C in humans)",
            "w": ["Osmoregulation", "Excretion", "Gaseous exchange", "Metabolism", "Homeostasis"]
          },
          {
            "a": "Vasodilation",
            "desc": "the widening of dermal blood vessels to increase blood flow to the skin, maximizing heat loss through radiation",
            "w": ["Vasoconstriction", "Sweating", "Shivering", "Erection of hairs", "Panting"]
          },
          {
            "a": "Vasoconstriction",
            "desc": "the narrowing of dermal blood vessels to restrict blood flow to the skin, minimizing heat loss in cold conditions",
            "w": ["Vasodilation", "Sweating", "Shivering", "Erection of hairs", "Panting"]
          },
          {
            "a": "Sweating",
            "desc": "the active release of a watery fluid onto the skin surface which draws large amounts of heat from the body as it evaporates",
            "w": ["Shivering", "Vasodilation", "Vasoconstriction", "Excretion", "Urination"]
          },
          {
            "a": "Shivering",
            "desc": "rapid, involuntary, and rhythmic muscle contractions that generate significant metabolic heat to warm the body",
            "w": ["Sweating", "Vasoconstriction", "Vasodilation", "Panting", "Piloerection"]
          }
        ]
      },
      {
        "name": "Osmoregulation",
        "facts": [
          {
            "a": "Osmoregulation",
            "desc": "the homeostatic regulation of water and dissolved solute (salt) concentrations in the blood and tissue fluids",
            "w": ["Thermoregulation", "Excretion", "Ultrafiltration", "Tubular reabsorption", "Homeostasis"]
          },
          {
            "a": "ADH (Antidiuretic Hormone)",
            "desc": "the hormone that acts on the distal convoluted tubules and collecting ducts of nephrons to increase their permeability to water",
            "w": ["Aldosterone", "Insulin", "Glucagon", "Adrenaline", "Thyroxin"]
          },
          {
            "a": "Aldosterone",
            "desc": "the adrenal hormone that stimulates the active reabsorption of sodium ions from the kidney tubules into the blood",
            "w": ["ADH", "Adrenaline", "Thyroxin", "Cortisol", "Glucagon"]
          }
        ]
      },
      {
        "name": "Carbon Dioxide Regulation",
        "facts": [
          {
            "a": "Medulla oblongata",
            "desc": "the brain region containing chemoreceptors that monitor carbon dioxide concentration and pH levels in the blood",
            "w": ["Cerebrum", "Cerebellum", "Hypothalamus", "Pituitary gland", "Thalamus"]
          },
          {
            "a": "Breathing rate",
            "desc": "the frequency of ventilation which is reflexively increased by the medulla oblongata to expel excess carbon dioxide",
            "w": ["Heart rate", "Metabolic rate", "Pulse rate", "Blood pressure", "Cardiac output"]
          },
          {
            "a": "Heart rate",
            "desc": "the frequency of cardiac contractions which increases to transport CO2-rich blood more rapidly to the lungs",
            "w": ["Breathing rate", "Metabolic rate", "Blood pressure", "Vital capacity", "Tidal volume"]
          }
        ]
      }
    ]
  }
]

data_part3 = [
  {
    "topic": "Responding to the Environment (Plants)",
    "prefix": "LIFE_P1_ENV_PLANTS",
    "file": "paper1_life_environment_plants.json",
    "subtopics": [
      {
        "name": "Plant Hormones",
        "facts": [
          {
            "a": "Auxins",
            "desc": "plant hormones (e.g., IAA) produced at the tip of stems and roots, primarily responsible for cell elongation and tropisms",
            "w": ["Gibberellins", "Abscisic acid", "Ethylene", "Cytokinins", "Florigen"]
          },
          {
            "a": "Gibberellins",
            "desc": "plant hormones that promote dramatic stem elongation, seed germination by breaking dormancy, and flowering",
            "w": ["Auxins", "Abscisic acid", "Ethylene", "Cytokinins", "Indoleacetic acid"]
          },
          {
            "a": "Abscisic acid",
            "desc": "the inhibitory plant hormone that maintains seed dormancy and forces stomatal closure during times of drought stress",
            "w": ["Auxins", "Gibberellins", "Ethylene", "Cytokinins", "Florigen"]
          },
          {
            "a": "Apical dominance",
            "desc": "the phenomenon where high concentrations of auxins produced at the apical bud strongly inhibit the growth of lateral buds",
            "w": ["Phototropism", "Geotropism", "Cell elongation", "Seed dormancy", "Parthenocarpy"]
          },
          {
            "a": "Weedkillers",
            "desc": "synthetic auxins selectively used in high concentrations to cause rapid, unsustainable growth leading to the death of broad-leaved weeds",
            "w": ["Fertilizers", "Pesticides", "Fungicides", "Gibberellins", "Abscisic acid"]
          }
        ]
      },
      {
        "name": "Tropisms",
        "facts": [
          {
            "a": "Tropism",
            "desc": "a slow, permanent growth movement of a plant organ in response to a unidirectional external stimulus",
            "w": ["Turgor movement", "Nastic movement", "Reflex action", "Apical dominance", "Taxic movement"]
          },
          {
            "a": "Phototropism",
            "desc": "the directional growth movement of a plant stem or root in response to a unilateral light stimulus",
            "w": ["Geotropism", "Hydrotropism", "Thigmotropism", "Chemotropism", "Apical dominance"]
          },
          {
            "a": "Geotropism",
            "desc": "the directional growth movement of a plant stem or root in response to the force of gravity",
            "w": ["Phototropism", "Hydrotropism", "Thigmotropism", "Chemotropism", "Nastic movement"]
          },
          {
            "a": "Clinostat",
            "desc": "an experimental apparatus consisting of a slow-rotating disc used to completely eliminate the effect of a unidirectional stimulus like gravity",
            "w": ["Potometer", "Respirometer", "Microscope", "Centrifuge", "Chromatograph"]
          },
          {
            "a": "Positive phototropism",
            "desc": "the growth of plant stems or shoots directly toward a unilateral light source, driven by auxin migration to the shaded side",
            "w": ["Negative phototropism", "Positive geotropism", "Negative geotropism", "Apical dominance", "Plagiotropism"]
          },
          {
            "a": "Positive geotropism",
            "desc": "the growth of plant roots downward in the direction of gravity, as high auxin concentration inhibits root cell elongation",
            "w": ["Negative geotropism", "Positive phototropism", "Negative phototropism", "Hydrotropism", "Apical dominance"]
          },
          {
            "a": "Negative geotropism",
            "desc": "the growth of plant stems upward away from the direction of gravity",
            "w": ["Positive geotropism", "Positive phototropism", "Negative phototropism", "Hydrotropism", "Thigmotropism"]
          }
        ]
      },
      {
        "name": "Defense Mechanisms",
        "facts": [
          {
            "a": "Chemical defense",
            "desc": "the evolutionary strategy of producing toxic, irritating, or unpalatable secondary metabolites to deter herbivores from feeding",
            "w": ["Mechanical defense", "Camouflage", "Mimicry", "Apical dominance", "Tropism"]
          },
          {
            "a": "Mechanical defense",
            "desc": "the presence of physical structural adaptations like thorns, spines, prickles, or thick cuticles to physically protect against herbivores",
            "w": ["Chemical defense", "Alkaloids", "Tannins", "Tropism", "Apical dominance"]
          }
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
          {
            "a": "Greenhouse effect",
            "desc": "the natural phenomenon where atmospheric gases trap low-energy infrared radiation (heat), keeping the Earth sufficiently warm for life",
            "w": ["Global warming", "Ozone depletion", "Eutrophication", "Thermal pollution", "Acid rain"]
          },
          {
            "a": "Global warming",
            "desc": "the unnatural, enhanced greenhouse effect resulting in a steady increase in the Earth's average atmospheric and ocean temperatures",
            "w": ["Greenhouse effect", "Ozone depletion", "Eutrophication", "Thermal pollution", "Desertification"]
          },
          {
            "a": "Carbon footprint",
            "desc": "a measure of the total amount of greenhouse gases, specifically carbon dioxide, produced directly and indirectly by human activities",
            "w": ["Ecological footprint", "Biocapacity", "Carbon sink", "Biological oxygen demand", "Carrying capacity"]
          },
          {
            "a": "Ozone depletion",
            "desc": "the dangerous thinning of the protective ozone layer in the stratosphere, primarily caused by chlorofluorocarbons (CFCs)",
            "w": ["Global warming", "Greenhouse effect", "Thermal pollution", "Eutrophication", "Acid rain"]
          },
          {
            "a": "Methane",
            "desc": "a potent greenhouse gas released primarily from landfill sites, agricultural livestock (cattle), and coal mining",
            "w": ["Carbon dioxide", "CFCs", "Ozone", "Nitrous oxide", "Sulphur dioxide"]
          }
        ]
      },
      {
        "name": "Water Availability and Quality",
        "facts": [
          {
            "a": "Eutrophication",
            "desc": "the severe ecological degradation of water bodies caused by excessive nutrient runoff (nitrates and phosphates) from fertilizers",
            "w": ["Thermal pollution", "Desertification", "Acid rain", "Biomagnification", "Global warming"]
          },
          {
            "a": "Algal bloom",
            "desc": "a rapid, explosive overgrowth of algae on the surface of a water system that blocks sunlight from reaching submerged plants",
            "w": ["Eutrophication", "Thermal pollution", "Biological Oxygen Demand", "Red tide", "Biomagnification"]
          },
          {
            "a": "Biological Oxygen Demand (BOD)",
            "desc": "a measurement of the massive amount of dissolved oxygen required by aerobic decomposing bacteria to break down organic matter in polluted water",
            "w": ["Carrying capacity", "Carbon footprint", "Ecological footprint", "Eutrophication", "pH level"]
          },
          {
            "a": "Thermal pollution",
            "desc": "the degradation of water quality caused by releasing heated water from industrial power plants back into natural ecosystems",
            "w": ["Eutrophication", "Acid rain", "Heavy metal pollution", "Biomagnification", "Global warming"]
          },
          {
            "a": "Alien plants",
            "desc": "non-indigenous invasive species that consume massive volumes of ground water and outcompete local flora for resources",
            "w": ["Endemic plants", "Pioneer species", "Climax community", "Indicator species", "Keystone species"]
          }
        ]
      },
      {
        "name": "Food Security",
        "facts": [
          {
            "a": "Food security",
            "desc": "the desirable state where all people, at all times, have physical, social, and economic access to sufficient, safe, and nutritious food",
            "w": ["Monoculture", "Overexploitation", "Carrying capacity", "Biodiversity", "Sustainability"]
          },
          {
            "a": "Monoculture",
            "desc": "the damaging agricultural practice of growing a single crop species repeatedly over a massive area, which depletes soil nutrients and reduces biodiversity",
            "w": ["Crop rotation", "Polyculture", "Mixed farming", "Subsistence farming", "Permaculture"]
          },
          {
            "a": "Pesticides",
            "desc": "toxic chemical substances used indiscriminately to kill pests, which often bioaccumulate and biomagnify within aquatic and terrestrial food chains",
            "w": ["Fertilizers", "Herbicides", "Fungicides", "Nutrients", "Hormones"]
          },
          {
            "a": "Genetically Modified Organisms (GMOs)",
            "desc": "organisms whose genetic material has been deliberately altered using biotechnology to increase crop yield and resistance to pests",
            "w": ["Clones", "Stem cells", "Invasive species", "Endemic species", "Hybrids"]
          }
        ]
      },
      {
        "name": "Loss of Biodiversity",
        "facts": [
          {
            "a": "Deforestation",
            "desc": "the large-scale, permanent clearing of indigenous forests for agriculture or urbanization, destroying critical habitats and massive carbon sinks",
            "w": ["Desertification", "Eutrophication", "Afforestation", "Overgrazing", "Poaching"]
          },
          {
            "a": "Alien invasive species",
            "desc": "aggressive, fast-breeding non-native species that completely lack natural predators and rapidly outcompete indigenous species for vital resources",
            "w": ["Endemic species", "Keystone species", "Indicator species", "Pioneer species", "Climax species"]
          },
          {
            "a": "Poaching",
            "desc": "the illegal hunting, capturing, or harvesting of wild plants and animals, driving many species like rhinos and cycads toward extinction",
            "w": ["Culling", "Trophy hunting", "Overfishing", "Deforestation", "Conservation"]
          },
          {
            "a": "Desertification",
            "desc": "the irreversible process by which once-fertile land becomes a barren desert, heavily accelerated by severe drought, overgrazing, and poor agricultural practices",
            "w": ["Deforestation", "Eutrophication", "Global warming", "Soil erosion", "Salinization"]
          }
        ]
      },
      {
        "name": "Solid Waste Disposal",
        "facts": [
          {
            "a": "Landfill site",
            "desc": "a heavily engineered designated area where solid municipal waste is dumped, compacted, and covered daily with soil to minimize disease vectors",
            "w": ["Incinerator", "Compost heap", "Recycling plant", "Sewage works", "Biogas digester"]
          },
          {
            "a": "Recycling",
            "desc": "the industrial process of systematically collecting and processing used waste materials to manufacture entirely new materials and objects",
            "w": ["Reusing", "Reducing", "Composting", "Incinerating", "Dumping"]
          }
        ]
      }
    ]
  }
]

data_part4 = [
  {
    "topic": "DNA: Code of Life",
    "prefix": "LIFE_P2_DNA",
    "file": "paper2_life_dna_code.json",
    "subtopics": [
      {
        "name": "Structure of DNA",
        "facts": [
          {
            "a": "Nucleotide",
            "desc": "the basic monomer building block of nucleic acids, consisting of a central 5-carbon sugar, a phosphate group, and a nitrogenous base",
            "w": ["Amino acid", "Monosaccharide", "Fatty acid", "Glycerol", "Polypeptide"]
          },
          {
            "a": "Deoxyribose",
            "desc": "the specific 5-carbon sugar tightly bonded to a phosphate and a base in every DNA nucleotide",
            "w": ["Ribose", "Glucose", "Fructose", "Sucrose", "Cellulose"]
          },
          {
            "a": "Adenine",
            "desc": "a purine nitrogenous base that exclusively forms two hydrogen bonds with Thymine in DNA, or Uracil in RNA",
            "w": ["Guanine", "Cytosine", "Thymine", "Uracil", "Ribose"]
          },
          {
            "a": "Guanine",
            "desc": "a purine nitrogenous base that always forms three strong hydrogen bonds exclusively with Cytosine",
            "w": ["Adenine", "Cytosine", "Thymine", "Uracil", "Deoxyribose"]
          },
          {
            "a": "Thymine",
            "desc": "a pyrimidine nitrogenous base strictly found only in DNA molecules that pairs exclusively with Adenine",
            "w": ["Uracil", "Cytosine", "Guanine", "Adenine", "Ribose"]
          },
          {
            "a": "Hydrogen bonds",
            "desc": "the weak chemical bonds securely holding complementary nitrogenous base pairs together across the center of a DNA molecule",
            "w": ["Peptide bonds", "Covalent bonds", "Ionic bonds", "Glycosidic bonds", "Phosphodiester bonds"]
          },
          {
            "a": "Double helix",
            "desc": "the iconic twisted, anti-parallel, ladder-like structural shape characteristic of all DNA molecules",
            "w": ["Single strand", "Clover leaf", "Alpha helix", "Beta pleated sheet", "Globular structure"]
          },
          {
            "a": "DNA profiling",
            "desc": "the forensic process of analyzing highly variable non-coding regions of DNA to conclusively identify individuals or determine biological relationships",
            "w": ["Genetic engineering", "Cloning", "Polymerase chain reaction", "Karyotyping", "Gene therapy"]
          },
          {
            "a": "Histones",
            "desc": "specialized spherical proteins around which long DNA strands tightly coil to form organized chromatin network",
            "w": ["Enzymes", "Hormones", "Antibodies", "Receptors", "Spindle fibres"]
          }
        ]
      },
      {
        "name": "DNA Replication",
        "facts": [
          {
            "a": "DNA Replication",
            "desc": "the vital process occurring during interphase where a DNA molecule makes an exact identical copy of itself before cell division",
            "w": ["Transcription", "Translation", "Protein synthesis", "Meiosis", "Mitosis"]
          },
          {
            "a": "Template strand",
            "desc": "the original separated DNA strand that serves as a direct pattern for the attachment of free complementary nucleotides",
            "w": ["Coding strand", "mRNA strand", "tRNA strand", "Polypeptide chain", "Non-coding strand"]
          }
        ]
      },
      {
        "name": "RNA Structure",
        "facts": [
          {
            "a": "Ribose",
            "desc": "the specific 5-carbon sugar present in all RNA nucleotides",
            "w": ["Deoxyribose", "Glucose", "Fructose", "Sucrose", "Maltose"]
          },
          {
            "a": "Uracil",
            "desc": "the unique nitrogenous base found only in RNA that physically replaces Thymine and pairs with Adenine",
            "w": ["Thymine", "Cytosine", "Guanine", "Adenine", "Deoxyribose"]
          },
          {
            "a": "mRNA (messenger RNA)",
            "desc": "the long single-stranded RNA molecule transcribed in the nucleus that carries the genetic code blueprint directly to the ribosome",
            "w": ["tRNA", "rRNA", "DNA", "Polypeptide", "Chromatin"]
          },
          {
            "a": "tRNA (transfer RNA)",
            "desc": "the small clover-shaped RNA molecule that carries specific corresponding amino acids from the cytoplasm to the ribosome during translation",
            "w": ["mRNA", "rRNA", "DNA", "Polypeptide", "Ribosome"]
          }
        ]
      },
      {
        "name": "Protein Synthesis",
        "facts": [
          {
            "a": "Transcription",
            "desc": "the highly regulated first stage of protein synthesis where a specific mRNA molecule is formed from a DNA template inside the nucleus",
            "w": ["Translation", "Replication", "Mutation", "Crossing over", "Elongation"]
          },
          {
            "a": "Translation",
            "desc": "the second stage of protein synthesis where ribosomes physically read mRNA sequences to assemble amino acids into a specific polypeptide chain",
            "w": ["Transcription", "Replication", "Mutation", "Crossing over", "Initiation"]
          },
          {
            "a": "Codon",
            "desc": "a precise sequence of three consecutive nitrogenous bases on an mRNA strand that explicitly codes for one specific amino acid",
            "w": ["Anticodon", "Triplet", "Gene", "Allele", "Nucleotide"]
          },
          {
            "a": "Anticodon",
            "desc": "a sequence of three exposed bases on a tRNA molecule that is perfectly complementary to a specific mRNA codon",
            "w": ["Codon", "Triplet", "Gene", "Allele", "Nucleotide"]
          },
          {
            "a": "Amino acid",
            "desc": "the basic monomer or building block of all proteins, which are linked together in a highly specific sequence",
            "w": ["Nucleotide", "Monosaccharide", "Fatty acid", "Glycerol", "Peptide"]
          },
          {
            "a": "Peptide bond",
            "desc": "the strong chemical bond formed directly between two adjacent amino acids during the translation phase of protein synthesis",
            "w": ["Hydrogen bond", "Phosphodiester bond", "Glycosidic bond", "Ionic bond", "Covalent bond"]
          },
          {
            "a": "Ribosome",
            "desc": "the microscopic organelle located in the cytoplasm acting as the physical site where translation and protein assembly occurs",
            "w": ["Nucleus", "Mitochondrion", "Chloroplast", "Golgi apparatus", "Endoplasmic reticulum"]
          }
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
          {
            "a": "Karyotype",
            "desc": "a visual, highly structured representation of the complete set of chromosomes in a cell, systematically arranged in homologous pairs by size and shape",
            "w": ["Pedigree diagram", "DNA profile", "Phylogenetic tree", "Punnett square", "Genotype"]
          },
          {
            "a": "Autosomes",
            "desc": "the first 22 pairs of chromosomes in humans that are strictly identical in both males and females and do not determine sex",
            "w": ["Gonosomes", "Sex chromosomes", "Gametes", "Allosomes", "Homologous pairs"]
          },
          {
            "a": "Gonosomes",
            "desc": "the critical 23rd pair of chromosomes that explicitly determine the biological sex of an individual (XX for female, XY for male)",
            "w": ["Autosomes", "Somatic chromosomes", "Homologous pairs", "Bivalents", "Chromatids"]
          },
          {
            "a": "Locus",
            "desc": "the exact specific physical location or position of a particular gene on a chromosome",
            "w": ["Allele", "Centromere", "Chiasma", "Telomere", "Chromatid"]
          },
          {
            "a": "Allele",
            "desc": "alternative, slightly different structural forms of the same specific gene, located at the exact same locus on homologous chromosomes",
            "w": ["Locus", "Genotype", "Phenotype", "Chromatid", "Mutation"]
          }
        ]
      },
      {
        "name": "Meiosis as a Source of Variation",
        "facts": [
          {
            "a": "Crossing over",
            "desc": "the crucial genetic exchange of DNA segments between non-sister chromatids of a homologous pair, guaranteeing unique new allele combinations in gametes",
            "w": ["Independent assortment", "Random fertilization", "Mutation", "Non-disjunction", "Transcription"]
          },
          {
            "a": "Independent assortment",
            "desc": "the completely random, unpredictable alignment and subsequent separation of maternal and paternal chromosomes at the equator during Metaphase I",
            "w": ["Crossing over", "Linkage", "Segregation", "Mutation", "Non-disjunction"]
          }
        ]
      },
      {
        "name": "Abnormal Meiosis",
        "facts": [
          {
            "a": "Non-disjunction",
            "desc": "the catastrophic failure during anaphase I or II where homologous chromosomes or sister chromatids fail to separate and migrate to opposite poles",
            "w": ["Crossing over", "Independent assortment", "Mutation", "Segregation", "Transcription"]
          },
          {
            "a": "Aneuploidy",
            "desc": "the resulting condition of having an abnormal, non-exact multiple number of chromosomes, such as 47 or 45 instead of the normal 46",
            "w": ["Polyploidy", "Diploidy", "Haploidy", "Trisomy", "Monosomy"]
          },
          {
            "a": "Trisomy 21",
            "desc": "the specific chromosomal condition of having three distinct copies of chromosome 21, resulting in the developmental disorder Down syndrome",
            "w": ["Haemophilia", "Colour blindness", "Turner syndrome", "Klinefelter syndrome", "Albinism"]
          }
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
          {
            "a": "Genotype",
            "desc": "the complete, specific genetic composition or paired allele combination of an organism for a particular inherited trait",
            "w": ["Phenotype", "Karyotype", "Allele", "Locus", "Trait"]
          },
          {
            "a": "Phenotype",
            "desc": "the outward physical appearance, measurable characteristic, or functional expression of an organism directly resulting from its genotype",
            "w": ["Genotype", "Karyotype", "Allele", "Locus", "Trait"]
          },
          {
            "a": "Dominant allele",
            "desc": "a powerful allele that completely masks the expression of a recessive allele and is fully expressed in the heterozygous condition",
            "w": ["Recessive allele", "Co-dominant allele", "Incomplete allele", "Mutant allele", "Locus"]
          },
          {
            "a": "Recessive allele",
            "desc": "a masked allele that is only physically expressed in the phenotype when the organism is strictly homozygous for that trait",
            "w": ["Dominant allele", "Co-dominant allele", "Incomplete allele", "Mutant allele", "Locus"]
          },
          {
            "a": "Homozygous",
            "desc": "a genetic state of having two strictly identical alleles for a particular gene (e.g., TT or tt), also known as pure-breeding",
            "w": ["Heterozygous", "Hemizygous", "Dominant", "Recessive", "Hybrid"]
          },
          {
            "a": "Heterozygous",
            "desc": "a genetic state of having two completely different alleles for a particular gene (e.g., Tt), often called a hybrid",
            "w": ["Homozygous", "Hemizygous", "Dominant", "Recessive", "Pure-breeding"]
          },
          {
            "a": "Complete dominance",
            "desc": "a standard type of inheritance where the dominant allele completely and entirely masks the presence of the recessive allele",
            "w": ["Incomplete dominance", "Co-dominance", "Polygenic inheritance", "Multiple alleles", "Sex-linked inheritance"]
          },
          {
            "a": "Incomplete dominance",
            "desc": "a specific pattern of inheritance where the heterozygous phenotype is an intermediate, third blended phenotype between the two homozygous extremes",
            "w": ["Complete dominance", "Co-dominance", "Polygenic inheritance", "Multiple alleles", "Sex-linked inheritance"]
          },
          {
            "a": "Co-dominance",
            "desc": "a pattern of inheritance where both distinct alleles are equally, fully, and simultaneously expressed in the heterozygous phenotype without blending",
            "w": ["Complete dominance", "Incomplete dominance", "Polygenic inheritance", "Multiple alleles", "Sex-linked inheritance"]
          },
          {
            "a": "Pedigree diagram",
            "desc": "a highly structured visual chart that meticulously traces the inheritance pattern of a specific genetic trait across several consecutive generations in a family",
            "w": ["Karyotype", "DNA profile", "Punnett square", "Phylogenetic tree", "Cladogram"]
          }
        ]
      },
      {
        "name": "Dihybrid Crosses",
        "facts": [
          {
            "a": "Dihybrid cross",
            "desc": "a complex genetic cross between two individuals that simultaneously involves tracing the inheritance of two entirely different genetic traits",
            "w": ["Monohybrid cross", "Test cross", "Back cross", "Polygenic cross", "Sex-linked cross"]
          }
        ]
      },
      {
        "name": "Sex-linked Inheritance",
        "facts": [
          {
            "a": "Sex-linked traits",
            "desc": "phenotypic traits heavily controlled by genes uniquely located on the sex chromosomes, primarily the large X chromosome",
            "w": ["Autosomal traits", "Polygenic traits", "Co-dominant traits", "Incomplete traits", "Mitochondrial traits"]
          },
          {
            "a": "Haemophilia",
            "desc": "a severe sex-linked recessive genetic disorder characterized by the complete inability of blood to clot normally due to a missing clotting factor",
            "w": ["Colour blindness", "Down syndrome", "Albinism", "Sickle cell anaemia", "Cystic fibrosis"]
          },
          {
            "a": "Colour blindness",
            "desc": "a common sex-linked recessive visual defect strictly located on the X chromosome, leading to significant difficulty distinguishing certain colors",
            "w": ["Haemophilia", "Astigmatism", "Myopia", "Hypermetropia", "Cataracts"]
          }
        ]
      },
      {
        "name": "Blood Groups",
        "facts": [
          {
            "a": "Multiple alleles",
            "desc": "the rare genetic situation characterized by the presence of more than two possible alleles for a single gene locus within a population, such as the ABO blood groups",
            "w": ["Polygenic inheritance", "Co-dominance", "Incomplete dominance", "Sex-linked inheritance", "Pleiotropy"]
          }
        ]
      },
      {
        "name": "Mutations",
        "facts": [
          {
            "a": "Gene mutation",
            "desc": "a sudden, small-scale change in the exact sequence of nitrogenous bases in a single specific gene on a DNA molecule",
            "w": ["Chromosomal mutation", "Non-disjunction", "Crossing over", "Independent assortment", "Transcription error"]
          },
          {
            "a": "Chromosomal mutation",
            "desc": "a massive, large-scale change in the physical structure or absolute number of whole chromosomes in a cell",
            "w": ["Gene mutation", "Point mutation", "Frameshift mutation", "Substitution", "Transcription error"]
          }
        ]
      },
      {
        "name": "Genetic Engineering",
        "facts": [
          {
            "a": "Genetic engineering",
            "desc": "the direct, highly deliberate technological modification of an organism's characteristics by manipulating, inserting, or deleting its genetic material",
            "w": ["Artificial selection", "Selective breeding", "Inbreeding", "Cloning", "Polyploidy"]
          },
          {
            "a": "Biotechnology",
            "desc": "the broad industrial use of living organisms, their biological systems, or their components to produce highly useful commercial products or processes",
            "w": ["Genetic engineering", "Cloning", "Paleontology", "Biogeography", "Taxonomy"]
          },
          {
            "a": "Cloning",
            "desc": "the exact scientific process of producing genetically identical copies of a specific cell, tissue, or entire organism through asexual methods",
            "w": ["Genetic engineering", "Selective breeding", "Inbreeding", "Hybridization", "Meiosis"]
          },
          {
            "a": "Stem cells",
            "desc": "unique, completely undifferentiated biological cells that retain the incredible potential to rapidly develop into various specialized cell types",
            "w": ["Somatic cells", "Gametes", "Erythrocytes", "Leukocytes", "Neurons"]
          }
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
          {
            "a": "Evolution",
            "desc": "the slow, continuous process of gradual genetic and physical change in the characteristics of a population over many successive generations",
            "w": ["Natural selection", "Speciation", "Artificial selection", "Mutagenesis", "Acclimatization"]
          },
          {
            "a": "Fossil",
            "desc": "the strictly preserved ancient remains, hard impressions, or mineralized traces of long-dead organisms securely found in sedimentary rock",
            "w": ["Artifact", "Coprolite", "Amber", "Igneous rock", "Metamorphic rock"]
          },
          {
            "a": "Paleontology",
            "desc": "the dedicated scientific study of fossils to deeply understand past life forms and trace their evolutionary history and lineages",
            "w": ["Archaeology", "Anthropology", "Biogeography", "Anatomy", "Genetics"]
          },
          {
            "a": "Homologous structures",
            "desc": "anatomical structures in completely different species that share a remarkably similar basic underlying plan (e.g., pentadactyl limb), strongly indicating common ancestry",
            "w": ["Analogous structures", "Vestigial structures", "Convergent structures", "Acquired structures", "Somatic structures"]
          },
          {
            "a": "Analogous structures",
            "desc": "distinct structures that perform exactly the same function in different species but fundamentally differ in their basic anatomical structure and evolutionary origin",
            "w": ["Homologous structures", "Vestigial structures", "Divergent structures", "Acquired structures", "Somatic structures"]
          },
          {
            "a": "Biogeography",
            "desc": "the specific study of the past and present geographical distribution patterns of existing and extinct plant and animal species across the continents",
            "w": ["Paleontology", "Ecology", "Taxonomy", "Phylogeny", "Demography"]
          }
        ]
      },
      {
        "name": "Theories of Evolution",
        "facts": [
          {
            "a": "Lamarckism",
            "desc": "the historically rejected theory of evolution strictly based on the inheritance of acquired characteristics and the flawed law of use and disuse during an organism's lifetime",
            "w": ["Darwinism", "Punctuated equilibrium", "Neo-Darwinism", "Creationism", "Intelligent design"]
          },
          {
            "a": "Darwinism",
            "desc": "the widely accepted core theory of evolution boldly proposing natural selection as the driving mechanism for descent with modification",
            "w": ["Lamarckism", "Punctuated equilibrium", "Catastrophism", "Creationism", "Intelligent design"]
          }
        ]
      },
      {
        "name": "Natural Selection",
        "facts": [
          {
            "a": "Natural selection",
            "desc": "the fundamental environmental mechanism of evolution where organisms best adapted to their specific environment survive, successfully reproduce, and generously pass on their highly favorable alleles",
            "w": ["Artificial selection", "Genetic drift", "Gene flow", "Mutation", "Inbreeding"]
          },
          {
            "a": "Artificial selection",
            "desc": "the highly deliberate, human-driven selective breeding of plants and animals over generations to produce very specific desired traits (e.g., dog breeds)",
            "w": ["Natural selection", "Sexual selection", "Genetic drift", "Speciation", "Extinction"]
          }
        ]
      },
      {
        "name": "Speciation",
        "facts": [
          {
            "a": "Speciation",
            "desc": "the complex evolutionary process by which completely new, reproductively isolated biological species arise from a pre-existing ancestral species",
            "w": ["Extinction", "Natural selection", "Evolution", "Adaptive radiation", "Convergent evolution"]
          },
          {
            "a": "Allopatric speciation",
            "desc": "the specific formation of a new species when a single population becomes physically and geographically isolated by an impassable physical barrier",
            "w": ["Sympatric speciation", "Artificial selection", "Punctuated equilibrium", "Extinction", "Convergent evolution"]
          },
          {
            "a": "Punctuated equilibrium",
            "desc": "the evolutionary hypothesis aggressively asserting that evolution primarily occurs in rapid, sudden bursts separated by extremely long periods of static non-change",
            "w": ["Gradualism", "Lamarckism", "Darwinism", "Natural selection", "Allopatric speciation"]
          }
        ]
      },
      {
        "name": "Human Evolution",
        "facts": [
          {
            "a": "Hominin",
            "desc": "the exclusive evolutionary taxonomic group that specifically includes all modern humans and their completely extinct obligate bipedal ancestors",
            "w": ["Hominid", "Primate", "Anthropoid", "Prosimian", "Australopithecus"]
          },
          {
            "a": "Bipedalism",
            "desc": "the unique, habitual ability to walk upright strictly on two lower limbs, marking a massive key milestone early in human evolution",
            "w": ["Quadrupedalism", "Brachiation", "Arborealism", "Knuckle-walking", "Prehensile grip"]
          },
          {
            "a": "Foramen magnum",
            "desc": "the critically large opening at the base of the skull through which the spinal cord passes, whose forward position is a massive indicator of upright bipedal posture",
            "w": ["Sagittal crest", "Brow ridge", "Cranial capacity", "Palate", "Mandible"]
          },
          {
            "a": "Cranial capacity",
            "desc": "the internal measurable volume of the protective braincase inside the skull, widely used as an excellent indicator of evolutionary brain size",
            "w": ["Foramen magnum", "Sagittal crest", "Brow ridge", "Prognathism", "Dentition"]
          },
          {
            "a": "Out of Africa hypothesis",
            "desc": "the extensively supported theory powerfully proposing that modern Homo sapiens evolved entirely in Africa before migrating outward to populate all other continents",
            "w": ["Multiregional hypothesis", "Lamarckism", "Punctuated equilibrium", "Creationism", "Intelligent design"]
          },
          {
            "a": "Australopithecus",
            "desc": "an entirely extinct, highly famous genus of early hominins found extensively in Africa, displaying a crucial mix of both primitive ape-like and advanced human-like traits",
            "w": ["Homo sapiens", "Homo neanderthalensis", "Homo erectus", "Ardipithecus", "Paranthropus"]
          },
          {
            "a": "Homo sapiens",
            "desc": "the official scientific binomial name specifically designating all modern humans alive today",
            "w": ["Homo habilis", "Homo erectus", "Homo neanderthalensis", "Australopithecus africanus", "Paranthropus robustus"]
          }
        ]
      }
    ]
  }
]

full_data = data + data_part2 + data_part3 + data_part4

with open('extracted_topics.json', 'w') as f:
    json.dump(full_data, f, indent=2)

print("Successfully generated extracted_topics.json with completely expanded facts and detailed distractors.")
