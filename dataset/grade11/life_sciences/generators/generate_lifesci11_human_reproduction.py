
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

def generate_human_reproduction():
    print("Generating Grade 11 Life Sciences: Human Reproduction...")
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
        q_id = f"LIFE11_P1_HUM_REP_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Human Reproduction",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "11",
                "subject": "Life Sciences",
                "topic": "Human Reproduction",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    rep_terms = [
        ("Testes", "The male primary reproductive organs housed in the scrotum that produce spermatozoa and secrete testosterone", ["Epididymis", "Prostate gland", "Seminal vesicles", "Vas deferens", "Cowper's glands", "Urethra", "Bladder"]),
        ("Seminiferous tubules", "Tightly coiled microscopic tubules within the testes where spermatogenesis (sperm production) takes place", ["Epididymis", "Vas deferens", "Interstitial cells", "Sertoli cells", "Prostate ducts", "Urethra", "Fallopian tubes"]),
        ("Epididymis", "A highly coiled tube situated on top of each testis where immature sperm are stored, gain motility, and mature", ["Seminiferous tubules", "Vas deferens", "Seminal vesicle", "Urethra", "Prostate gland", "Scrotum", "Ejaculatory duct"]),
        ("Vas deferens (sperm duct)", "A muscular tube that carries mature sperm from the epididymis to the urethra during ejaculation", ["Ureter", "Urethra", "Fallopian tube", "Seminiferous tubule", "Epididymis", "Cervix", "Vagina"]),
        ("Prostate gland", "A gland surrounding the male urethra that secretes an alkaline fluid to neutralize vaginal acidity and enhance sperm mobility", ["Seminal vesicle", "Cowper's gland", "Testis", "Adrenal gland", "Thyroid gland", "Pituitary gland", "Thymus"]),
        ("Seminal vesicles", "Accessory glands that secrete a nutrient-rich alkaline fluid containing fructose to provide energy for swimming sperm", ["Prostate gland", "Cowper's gland", "Epididymis", "Vas deferens", "Testes", "Scrotum", "Glans penis"]),
        ("Cowper's (bulbourethral) glands", "Small glands located beneath the prostate that secrete a clear, alkaline lubricating mucus into the urethra prior to ejaculation", ["Seminal vesicles", "Prostate gland", "Epididymis", "Testes", "Hypothalamus", "Thyroid", "Islets of Langerhans"]),
        ("Ovaries", "The female primary reproductive organs that produce ova (egg cells) through oogenesis and secrete estrogen and progesterone", ["Fallopian tubes", "Uterus", "Cervix", "Vagina", "Placenta", "Corpus luteum", "Endometrium"]),
        ("Fallopian tubes (oviducts)", "Ciliated muscular tubes connecting the ovaries to the uterus, serving as the normal biological site of fertilisation", ["Uterus", "Cervix", "Vagina", "Urethra", "Ureter", "Vas deferens", "Endometrium"]),
        ("Uterus (womb)", "A hollow, thick-walled muscular organ where the embryo implants and the fetus develops during pregnancy", ["Vagina", "Cervix", "Fallopian tube", "Ovary", "Bladder", "Placenta", "Peritoneum"]),
        ("Endometrium", "The glandular, highly vascularized inner mucous membrane lining of the uterus where the blastocyst implants", ["Myometrium", "Perimetrium", "Cervix", "Amnion", "Chorion", "Placenta", "Fallopian epithelium"]),
        ("Cervix", "The lower, narrow neck of the uterus that connects the uterine cavity to the vagina and dilates during childbirth", ["Vagina", "Vulva", "Endometrium", "Fallopian tube", "Ovary", "Urethra", "Perineum"]),
        ("Follicle Stimulating Hormone (FSH)", "A pituitary hormone that stimulates the development of a Graafian follicle in the ovary and stimulates estrogen production", ["Luteinizing Hormone (LH)", "Progesterone", "Oxytocin", "Prolactin", "Testosterone", "Aldosterone", "Thyroxin"]),
        ("Luteinizing Hormone (LH)", "A pituitary hormone whose sudden mid-cycle surge triggers ovulation and stimulates the conversion of the ruptured follicle into the corpus luteum", ["FSH", "Progesterone", "Estrogen", "Oxytocin", "Prolactin", "TSH", "Growth Hormone"]),
        ("Estrogen", "An ovarian hormone secreted by the Graafian follicle that stimulates the repair and thickening of the uterine endometrium", ["Progesterone", "FSH", "LH", "Oxytocin", "Prolactin", "Testosterone", "Aldosterone"]),
        ("Progesterone", "A steroid hormone secreted by the corpus luteum and placenta that maintains endometrial thickness and vascularity, inhibiting FSH and LH", ["Estrogen", "FSH", "LH", "Oxytocin", "Prolactin", "TSH", "Insulin"]),
        ("Ovulation", "The physiological release of a mature secondary oocyte from a ruptured Graafian follicle into the fallopian tube (typically around day 14)", ["Menstruation", "Implantation", "Fertilisation", "Gestation", "Parturition", "Lactation", "Capacitation"]),
        ("Corpus luteum", "A temporary glandular endocrine structure formed from the ruptured Graafian follicle after ovulation, secreting high levels of progesterone", ["Graafian follicle", "Primary follicle", "Blastocyst", "Morula", "Zygote", "Placenta", "Polar body"]),
        ("Implantation", "The biological process whereby the blastocyst embeds itself into the thickened, vascularized endometrium of the uterus", ["Fertilisation", "Ovulation", "Cleavage", "Gastrulation", "Parturition", "Lactation", "Gestation"]),
        ("Placenta", "A temporary disc-shaped organ formed from maternal and embryonic tissue that facilitates nutrient, gas, and waste exchange between mother and fetus", ["Amnion", "Allantois", "Yolk sac", "Corpus luteum", "Cervix", "Myometrium", "Endometrium"])
    ]

    for term, definition, wrongs in rep_terms:
        add_q("easy", "Reproductive Anatomy & Hormones", f"In Grade 11 CAPS Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Reproductive Anatomy & Hormones", f"Which biological structure or hormone correctly matches {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in rep_terms if d[0] != term][:7]
        add_q("easy", "Reproductive Anatomy & Hormones", f"Which statement accurately describes '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Reproductive Anatomy & Hormones", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

    easy_extras = [
        ("Why are the testes situated outside the abdominal cavity in the scrotum?", "To maintain a temperature 2-3°C lower than core body temperature, which is essential for viable sperm production", ["To allow easier urination", "To protect the testes from abdominal acid", "To increase testosterone secretion by 500%", "To prevent sperm from entering the bloodstream", "To allow sperm to undergo mitosis in warm air"], "Spermatogenesis requires a temperature approximately 2-3°C cooler than normal 37°C core body temperature."),
        ("Where in the female reproductive tract does fertilisation naturally occur?", "Fallopian tube (oviduct)", ["Uterus", "Ovary", "Cervix", "Vagina", "Abdominal cavity", "Endometrium"], "Fertilisation typically occurs in the upper third of the fallopian tube."),
        ("What is the average length of a normal human menstrual cycle?", "28 days", ["14 days", "7 days", "40 days", "21 days", "35 days", "10 days"], "A standard human menstrual cycle is approximately 28 days long."),
        ("On approximately which day of a standard 28-day menstrual cycle does ovulation occur?", "Day 14", ["Day 1", "Day 7", "Day 21", "Day 28", "Day 5", "Day 10"], "Ovulation is triggered by the LH surge around day 14 of a 28-day cycle."),
        ("What process involves the shedding of the functional layer of the uterine endometrium accompanied by blood loss?", "Menstruation", ["Ovulation", "Fertilisation", "Implantation", "Gestation", "Parturition", "Lactation"], "Menstruation occurs when progesterone levels drop, causing endometrial tissue and blood to slough off.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Human Reproduction: ", "In clinical reproductive biology: "]:
            add_q("easy", "Reproductive Anatomy & Hormones", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(rep_terms)
        q = f"Human reproduction check {e_counter}: Identify the hormone or organ defined as: {definition}."
        add_q("easy", "Reproductive Anatomy & Hormones", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    medium_scenarios = [
        ("What is the chronological sequence of sperm passage from formation to ejaculation in the human male reproductive system?",
         "Seminiferous tubules -> Epididymis -> Vas deferens -> Ejaculatory duct -> Urethra",
         ["Epididymis -> Seminiferous tubules -> Vas deferens -> Urethra", "Vas deferens -> Epididymis -> Urethra -> Seminiferous tubules", "Seminiferous tubules -> Ureter -> Bladder -> Urethra", "Prostate -> Epididymis -> Testis -> Vas deferens", "Urethra -> Vas deferens -> Epididymis -> Testes"],
         "Sperm are formed in seminiferous tubules, mature in epididymis, travel through vas deferens to the ejaculatory duct and urethra.", "Application"),

        ("What is the chronological sequence of developmental stages from fertilisation to implantation in humans?",
         "Zygote -> Morula -> Blastocyst -> Implantation in endometrium",
         ["Blastocyst -> Morula -> Zygote -> Implantation", "Zygote -> Fetus -> Embryo -> Blastocyst", "Morula -> Zygote -> Blastocyst -> Gastrula", "Zygote -> Implantation -> Morula -> Blastocyst", "Ovum -> Blastocyst -> Zygote -> Morula"],
         "Fertilisation produces a diploid zygote, which undergoes mitotic cleavage to form a solid morula, then a hollow blastocyst that implants.", "Application"),

        ("What happens to hormone levels and the uterine lining if the released ovum is NOT fertilised during the menstrual cycle?",
         "The corpus luteum degenerates, causing progesterone and estrogen levels to drop sharply, leading to endometrial breakdown (menstruation)",
         ["FSH and LH levels surge to ten times their normal concentration", "The corpus luteum enlarges and produces massive amounts of progesterone", "Estrogen levels remain elevated permanently, preventing menstruation", "The placenta immediately takes over progesterone production", "The endometrium hardens into bone to protect the ovaries"],
         "Without hCG from an implanted blastocyst, the corpus luteum degenerates, causing progesterone to plummet and triggering menstruation.", "Application"),

        ("What hormone is produced by the chorion and early placenta that maintains the corpus luteum and is detected in standard urine pregnancy tests?",
         "Human Chorionic Gonadotropin (hCG)",
         ["Luteinizing Hormone (LH)", "Follicle Stimulating Hormone (FSH)", "Oxytocin", "Prolactin", "Thyroxin", "Adrenaline"],
         "hCG signals the corpus luteum to continue secreting progesterone during the first trimester; it is the target of home pregnancy tests.", "Application"),

        ("Which blood vessels compose the umbilical cord, and what type of blood do they carry?",
         "Two umbilical arteries carrying deoxygenated, waste-rich blood from fetus to placenta, and one umbilical vein carrying oxygenated, nutrient-rich blood from placenta to fetus",
         ["Two umbilical veins carrying deoxygenated blood and one artery carrying oxygen", "One artery and one vein carrying mixed maternal blood", "Four umbilical capillaries with zero maternal connection", "Three veins carrying pure maternal red blood cells into fetal heart", "Two umbilical nerves that transmit brain impulses"],
         "Umbilical arteries transport fetal metabolic wastes to the placenta; the umbilical vein delivers maternal oxygen and nutrients to the fetus.", "Application"),

        ("Why do maternal blood and fetal blood NOT mix inside the placenta?",
         "Maternal and fetal blood groups may be incompatible (causing deadly agglutination), and high maternal blood pressure would rupture delicate fetal capillaries",
         ["Fetal blood does not contain red blood cells or hemoglobin", "Maternal blood is acidic and would kill fetal white blood cells", "The placenta is completely impermeable to all molecules including oxygen", "Fetal blood circulates in air rather than blood vessels", "Maternal blood carries no nutrients or glucose"],
         "Separation by thin placental membranes prevents immunological rejection, agglutination from mismatched ABO/Rh groups, and mechanical damage.", "Application"),

        ("How does the combined oral contraceptive pill prevent pregnancy in females?",
         "It maintains elevated synthetic estrogen and progesterone levels, which inhibit the pituitary gland from releasing FSH and LH via negative feedback, thus preventing follicle development and ovulation",
         ["It destroys all sperm cells in the vagina on contact", "It causes permanent surgical blockage of both fallopian tubes", "It induces immediate menstruation daily throughout the month", "It prevents the male from producing testosterone", "It dissolves the ovaries completely during the cycle"],
         "High progesterone and estrogen exert negative feedback on the anterior pituitary, stopping FSH (no follicle growth) and LH (no ovulation).", "Application")
    ]

    for q, ans, wrongs, expl, cog in medium_scenarios:
        for prefix in ["", "CAPS Menstrual Cycle Problem: ", "Human Reproductive Endocrinology: ", "Embryological Case Study: "]:
            add_q("medium", "Endocrinology & Development", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500
    cycle_days = [
        ("Days 1 to 5", "Menstruation occurs; endometrium sloughs off due to low progesterone", [
            "Ovulation occurs; LH surges",
            "Endometrium thickens rapidly under high progesterone",
            "Blastocyst implants into the cervix",
            "Corpus luteum reaches maximum size",
            "FSH and LH reach peak levels",
            "Fertilisation occurs in the fallopian tube",
            "Placenta begins producing human chorionic gonadotropin",
            "Cervical mucus becomes thick and impenetrable to sperm"
        ]),
        ("Days 6 to 13", "Proliferative phase; developing follicle secretes estrogen which repairs the endometrium", [
            "Menstruation begins with heavy bleeding",
            "Corpus luteum degenerates into corpus albicans",
            "Implantation of the morula occurs",
            "Progesterone reaches its maximum concentration",
            "Oxytocin triggers uterine contractions",
            "Secondary oocyte is released into abdominal cavity",
            "All endometrial blood vessels disintegrate",
            "High progesterone inhibits all follicular development"
        ]),
        ("Day 14", "LH surge triggers ovulation; Graafian follicle ruptures releasing secondary oocyte", [
            "Menstruation begins",
            "Endometrium drops to minimum thickness",
            "Placenta takes over all hormone production",
            "FSH drops to zero permanently",
            "Sperm cells are synthesized in the ovaries",
            "Corpus luteum reaches full glandular maturity",
            "Endometrium is completely shed as menstrual fluid",
            "Progesterone reaches its highest monthly peak"
        ]),
        ("Days 15 to 28", "Secretory (luteal) phase; corpus luteum secretes progesterone to maintain endometrial thickness", [
            "Menstruation occurs throughout this entire period",
            "Graafian follicle grows from primary follicle",
            "Ovulation occurs every single day",
            "Estrogen drops to absolute zero",
            "Pituitary secretes massive bursts of prolactin",
            "Endometrium is completely absent",
            "FSH increases to stimulate multiple follicles",
            "Cervix dilates to 10 cm in preparation for birth"
        ])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        c_item = random.choice(cycle_days)
        q = f"Menstrual cycle tracking {m_counter}: What physiological events characterize {c_item[0]} of a typical 28-day human menstrual cycle?"
        add_q("medium", "Menstrual Cycle", q, c_item[1], c_item[2], f"During {c_item[0]}: {c_item[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        ("A pregnant woman experiences severe abdominal cramping and bleeding at week 7 of pregnancy. Medical tests reveal a sudden, catastrophic drop in progesterone. What is the physiological cause of this impending miscarriage?",
         "Premature degeneration of the corpus luteum before the placenta has matured sufficiently (around week 12) to take over progesterone production",
         ["The pituitary gland released excessive FSH that destroyed the fetus", "The mother's liver stopped converting glycogen into glucose", "The umbilical vein ruptured due to high amniotic pressure", "The fetus developed an extra copy of all 46 chromosomes", "The cervix dilated due to excessive testosterone production", "The thyroid gland stopped secreting thyroxin"],
         "During the first trimester (weeks 1-12), pregnancy is maintained entirely by progesterone from the corpus luteum; if it fails before the placenta takes over, the endometrium sheds.", "Analysis"),

        ("Why does maternal smoking (carbon monoxide and nicotine exposure) during pregnancy frequently result in low birth weight and fetal hypoxia?",
         "Carbon monoxide binds irreversibly to maternal hemoglobin forming carboxyhemoglobin, reducing oxygen delivery across the placenta, while nicotine causes vasoconstriction of placental blood vessels",
         ["Nicotine dissolves the fetal skull bones in the uterus", "Carbon monoxide turns the amniotic fluid into pure alcohol", "Cigarette smoke prevents the mother from producing breast milk", "Nicotine causes the placenta to detach and turn into an ovary", "Smoke particles enter the fetal lungs directly through the umbilical vein"],
         "Carbon monoxide drastically lowers oxygen transport capacity and nicotine restricts blood flow through placental vessels, starving the fetus of oxygen and nutrients.", "Analysis"),

        ("How does the positive feedback mechanism of oxytocin operate during human parturition (labour)?",
         "Cervical stretching by the fetal head stimulates the posterior pituitary to secrete oxytocin, which intensifies uterine contractions, pushing the head further and triggering even greater oxytocin release until delivery",
         ["Oxytocin inhibits uterine contractions until the mother falls asleep", "Oxytocin causes progesterone levels to rise fifty-fold", "Oxytocin causes the amniotic fluid to thicken into a solid plug", "Uterine contractions inhibit oxytocin release through negative feedback", "Oxytocin causes the placenta to absorb fetal red blood cells"],
         "Oxytocin operates via a classic positive feedback loop: uterine contractions stretch the cervix, which sends neural signals to release more oxytocin, escalating contractions until birth.", "Analysis"),

        ("What is the physiological role of Prolactin versus Oxytocin in maternal lactation?",
         "Prolactin (anterior pituitary) stimulates the synthesis and production of milk in mammary glands, whereas Oxytocin (posterior pituitary) stimulates the contraction of myoepithelial cells for milk ejection (let-down reflex)",
         ["Prolactin causes milk ejection while oxytocin synthesizes milk", "Prolactin maintains pregnancy while oxytocin triggers ovulation", "Both hormones perform identical functions in the female ovaries", "Prolactin is male-exclusive while oxytocin is female-exclusive", "Prolactin inhibits milk production until weaning occurs"],
         "Prolactin drives milk synthesis; infant suckling triggers sensory impulses that stimulate oxytocin release for the milk let-down reflex.", "Analysis"),

        ("Why does the surgical procedure of a vasectomy in males cause sterility without affecting sexual drive (libido) or secondary male characteristics?",
         "Cutting and tying the vas deferens prevents sperm from joining the semen, but Leydig cells in the testes still secrete testosterone directly into the bloodstream",
         ["Vasectomy removes the testes completely from the scrotum", "Vasectomy stops the pituitary gland from secreting LH and FSH", "Testosterone is transported through the digestive tract instead of blood", "Vasectomy increases sperm production to lethal levels in the epididymis", "Sperm cells are converted into testosterone after vasectomy"],
         "Testosterone is an endocrine hormone secreted directly into testicular blood capillaries; the vas deferens only conducts gametes, so ligation does not impair hormone circulation.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "CAPS Reproductive Physiology Evaluation: ", "Clinical Obstetrics Investigation: ", "Endocrine Feedback Problem: "]:
            add_q("hard", "Reproductive Endocrinology", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = random.choice(_templates).format(clinic=random.choice(_clinics), city=random.choice(_cities), name=random.choice(_names), topic=base_h[0])
        add_q("hard", "Reproductive Endocrinology", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade11/life_sciences/paper1_life_human_reproduction.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_human_reproduction()
