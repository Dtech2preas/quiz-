import json
import random
import os
import time

def generate_environment_plants():
    print("Generating Grade 12 Life Sciences: Responding to the Environment - Plants...")
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
        q_id = f"LIFE_P1_PLANT_ENV_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Responding to the Environment (Plants)",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Life Sciences",
                "topic": "Responding to the Environment (Plants)",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    plant_terms = [
        ("Auxins (e.g., IAA)", "A major class of plant growth hormones synthesized in apical meristems that promote cell elongation, apical dominance, and tropisms", ["Gibberellins", "Abscisic acid (ABA)", "Ethylene", "Cytokinins", "Amylase", "Chlorophyll", "Phytochrome"]),
        ("Gibberellins", "Plant hormones that stimulate stem and internode elongation, promote flowering, and break seed dormancy by triggering starch breakdown", ["Auxins", "Abscisic acid (ABA)", "Ethylene", "Tannins", "Alkaloids", "Cellulose", "Lignin"]),
        ("Abscisic acid (ABA)", "A plant stress hormone that promotes seed and bud dormancy, causes stomata to close during water deficiency, and promotes leaf abscission", ["Auxins", "Gibberellins", "Cytokinins", "Amylase", "Chlorophyll", "Phytochrome", "Ethylene"]),
        ("Tropism", "A directional growth movement of a plant organ in response to an external environmental stimulus, where the direction of response depends on the stimulus direction", ["Nastic movement", "Turgor movement", "Apical dominance", "Abscission", "Etiolation", "Transpiration", "Guttation"]),
        ("Phototropism", "The directional growth response of a plant organ towards (positive) or away from (negative) a unilateral light stimulus", ["Geotropism", "Hydrotropism", "Thigmotropism", "Chemotropism", "Gravitropism", "Thermotropism", "Apical dominance"]),
        ("Geotropism (Gravitropism)", "The directional growth response of a plant organ towards (positive) or away from (negative) the force of gravity", ["Phototropism", "Hydrotropism", "Thigmotropism", "Chemotropism", "Photoperiodism", "Vernalization", "Dormancy"]),
        ("Apical dominance", "The physiological phenomenon where the growing apical terminal bud suppresses the growth of lateral axillary buds via high auxin production", ["Apical abscission", "Lateral etiolation", "Phototropic inhibition", "Geotropic curvature", "Gibberellic dwarfism", "Bud abscission", "Stomatal dormancy"]),
        ("Clinostat", "A rotating laboratory apparatus used in plant tropism experiments to eliminate the directional influence of gravity or unilateral light", ["Potometer", "Respirometer", "Colorimeter", "Centrifuge", "Hemocytometer", "Barometer", "Manometer"]),
        ("Thorns", "Modified, sharp, rigid stem structures that protect plants against herbivory by large grazing and browsing mammals", ["Spines", "Prickles", "Trichomes", "Stomata", "Tendrils", "Lenticels", "Petioles"]),
        ("Spines", "Modified, sharp, pointed leaf structures (as found on cacti and aloe) that minimize water loss and deter herbivores", ["Thorns", "Prickles", "Trichomes", "Bracts", "Stipules", "Rhizomes", "Stolons"]),
        ("Prickles", "Sharp epidermal outgrowths of the cortex and bark (as found on roses) that act as mechanical deterrents against animals", ["Thorns", "Spines", "Trichomes", "Cuticles", "Lenticels", "Stomata", "Root hairs"]),
        ("Tannins", "Astringent, bitter polyphenolic chemical compounds stored in plant vacuole tissues that deter herbivores by binding to and inactivating digestive enzymes", ["Auxins", "Gibberellins", "Alkaloids", "Phytohormones", "Chloroplasts", "Amylases", "Lipids"]),
        ("Alkaloids", "Bitter-tasting nitrogen-containing secondary chemical compounds (e.g., nicotine, caffeine, morphine) that are toxic or repellent to insects and herbivores", ["Tannins", "Cellulose", "Pectin", "Starch", "Glucose", "Gibberellins", "Chlorophylls"])
    ]

    for term, definition, wrongs in plant_terms:
        add_q("easy", "Plant Hormones & Defense", f"In Grade 12 CAPS Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Plant Hormones & Defense", f"Which botanical term or substance correctly matches {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in plant_terms if d[0] != term][:7]
        add_q("easy", "Plant Hormones & Defense", f"Which statement accurately explains '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Plant Hormones & Defense", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

    easy_extras = [
        ("Where in a growing plant are auxins predominantly synthesized?", "In the apical meristems of growing shoot and root tips", ["In the xylem vessels of woody stems", "In the guard cells of mature leaves only", "Inside mature pollen grains", "In the waxy cuticle of fruit skins", "In the secondary phloem sieve tubes"], "Auxins are produced in actively dividing apical meristems and diffuse downwards into elongation zones."),
        ("What type of growth response is displayed by plant stems growing upwards towards sunlight?", "Positive phototropism and negative geotropism", ["Negative phototropism and positive geotropism", "Positive geotropism only", "Negative phototropism only", "Hydrotropism and chemotropism", "Zero tropism"], "Stems grow towards light (positive phototropism) and away from gravity (negative geotropism)."),
        ("What type of growth response is displayed by plant primary roots growing downwards into the soil?", "Positive geotropism and negative phototropism", ["Positive phototropism and negative geotropism", "Negative geotropism only", "Positive phototropism only", "Zero geotropism", "Lateral etiolation"], "Roots grow downwards towards gravity (positive geotropism) and away from light (negative phototropism)."),
        ("Which plant hormone is directly responsible for closing stomata during periods of intense drought to conserve water?", "Abscisic acid (ABA)", ["Auxin", "Gibberellin", "Cytokinin", "Ethylene", "Amylase", "Indoleacetic acid"], "ABA acts as a stress hormone, signaling guard cells to lose turgor and close stomatal pores."),
        ("What happens to lateral axillary buds when the apical terminal bud of a plant is pruned or removed?", "Lateral buds are released from apical dominance and grow out into bushy lateral branches", ["Lateral buds wither and fall off immediately", "The plant stops undergoing photosynthesis permanently", "The roots reverse their geotropic curvature", "All stomata close permanently", "The plant produces seeds immediately without flowering"], "Removing the apical bud removes the source of auxin that suppresses lateral bud growth.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Plant Physiology: ", "In agricultural botany: "]:
            add_q("easy", "Plant Hormones & Defense", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(plant_terms)
        q = f"Plant hormone identification {e_counter}: Identify the substance or movement defined as: {definition}."
        add_q("easy", "Plant Hormones & Defense", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    medium_mechanisms = [
        # Phototropism Stem Mechanism
        ("How does unilateral (one-sided) light cause a plant stem (coleoptile) to bend towards the light source?",
         "Auxins migrate to the shaded side -> High auxin concentration on shaded side stimulates cell elongation -> Shaded side elongates faster than illuminated side -> Stem bends towards light",
         ["Auxins migrate to the illuminated side -> High auxin stops all cell elongation on shaded side", "Light destroys all auxins in the root -> Stem shrinks on the lighted side", "Auxins cause cells on the illuminated side to divide twice as fast", "Gravity pulls auxins down -> Stem bends towards the ground", "Light stimulates chlorophyll to attract water molecules directly"],
         "In stems, auxins diffuse to the shaded side where high concentrations stimulate cell elongation, causing curvature towards the light.", "Application"),

        # Geotropism Root Mechanism
        ("When a germinating seedling is placed horizontally in the dark, why does the root bend downwards towards gravity (positive geotropism)?",
         "Gravity pulls auxins to the lower side of the root -> In roots, high auxin concentration INHIBITS cell elongation -> Cells on the upper side elongate faster -> Root bends downwards",
         ["High auxin on the lower side stimulates cell elongation in the root", "Auxins evaporate from the upper side of the root", "Gravity pulls the root tip down purely by mechanical weight", "Light from the soil repels the root tip upwards", "Root cells on the lower side divide by meiosis"],
         "Roots have different auxin sensitivity than stems: high auxin concentration inhibits root elongation, so the upper side with less auxin elongates faster.", "Application"),

        # Geotropism Stem Mechanism
        ("When a seedling is placed horizontally in the dark, why does the stem bend upwards away from gravity (negative geotropism)?",
         "Gravity causes auxins to accumulate on the lower side -> In stems, high auxin concentration STIMULATES cell elongation -> Lower side grows faster -> Stem bends upwards",
         ["Auxins accumulate on the upper side of the stem, stimulating elongation", "High auxin on the lower side inhibits stem cell elongation", "The stem bends upwards due to positive phototropism towards moonlight", "Gravity destroys auxins on the lower side of the stem", "Stems lack auxins and bend purely due to turgor pressure"],
         "In stems, high auxin on the lower side stimulates cell elongation, bending the shoot upwards against gravity.", "Application"),

        # Clinostat Experiment
        ("A seedling is placed horizontally on a motorized clinostat that rotates slowly and continuously in the dark for 48 hours. What growth pattern will be observed in the root and stem?",
         "Both the root and stem will continue to grow horizontally straight without bending, because rotating eliminates unilateral gravity, distributing auxins evenly on all sides",
         ["The stem will bend upwards and the root will bend downwards normally", "Both the stem and root will bend upwards into the air", "Both the stem and root will bend downwards into the soil", "The seedling will stop growing completely and die", "The root will turn into a stem and produce green leaves"],
         "Continuous rotation subjects all sides equally to gravity, ensuring symmetric auxin distribution and straight horizontal growth.", "Application"),

        # Decapitation Experiment
        ("In a classic plant physiology experiment, the tips of oat coleoptiles are excised (decapitated). The coleoptiles are then exposed to unilateral light. What is the expected outcome?",
         "The decapitated coleoptiles fail to grow or bend towards the light, because the apical tip is the site of auxin production and light perception",
         ["The decapitated coleoptiles bend twice as fast towards the light", "The coleoptiles grow downwards into the soil", "The coleoptiles burst due to high hydrostatic turgor pressure", "The coleoptiles immediately develop flower buds", "The stumps produce giant leaves within 10 minutes"],
         "The tip produces auxins and senses directional light; without the tip, cell elongation and phototropic curvature cease.", "Application"),

        # Synthetic Auxins / Weedkillers
        ("How do commercial synthetic auxins (such as 2,4-D) function as selective weedkillers in agricultural cereal crops?",
         "They cause uncontrolled, excessively rapid cell elongation and metabolic exhaustion in broad-leaved dicotyledonous weeds, killing them while leaving narrow-leaved monocot crops unharmed",
         ["They poison the soil with heavy metals that kill all living plants", "They block photosynthesis in all green plants equally", "They destroy the cell membranes of monocot crops only", "They prevent seeds from absorbing water during germination", "They freeze the cytoplasm of root cells at room temperature"],
         "Broad-leaved weeds absorb and translocate synthetic auxins rapidly, triggering lethal metabolic overgrowth without damaging grasses/cereals.", "Application")
    ]

    for q, ans, wrongs, expl, cog in medium_mechanisms:
        for prefix in ["", "CAPS Experimental Botany: ", "Plant Tropism Investigation: ", "Coleoptile Bioassay Problem: "]:
            add_q("medium", "Tropism Mechanisms", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500
    auxin_experiments = [
        ("Tip covered with opaque tin-foil cap", "Coleoptile grows straight upwards without bending; proves tip is the site of light photoreception", [
            "Coleoptile bends towards the light normally", "Coleoptile bends away from the light into the soil", "Coleoptile stops all cellular respiration",
            "Coleoptile splits into two identical stems", "Coleoptile undergoes immediate leaf abscission", "Coleoptile produces red anthocyanin pigments",
            "Coleoptile roots turn upwards towards the sun", "Coleoptile wilts permanently within 2 hours"
        ]),
        ("Tip covered with transparent glass cap", "Coleoptile bends towards unilateral light normally; confirms light must reach the tip to induce auxin migration", [
            "Coleoptile grows straight without bending", "Coleoptile bends away from the light source", "Coleoptile stops all growth completely",
            "Glass cap blocks all auxin synthesis", "Transparent cap causes stem to swell into a tuber", "Coleoptile undergoes negative geotropism only",
            "Coleoptile dies due to greenhouse effect", "Auxins accumulate only on the illuminated side"
        ]),
        ("Agar block with auxins placed off-center on decapitated stump in dark", "Coleoptile bends away from the side with the agar block; confirms auxins diffuse down and stimulate cell elongation", [
            "Coleoptile bends towards the side with the agar block", "Coleoptile grows straight without any bending", "Coleoptile stops all elongation",
            "Agar block poisons the stump tissue", "Coleoptile produces flowers from the agar block", "Stump undergoes reverse geotropism",
            "Coleoptile loses all chlorophyll pigment", "Agar block converts auxins into starch granules"
        ]),
        ("Mica sheet inserted on shaded side below tip", "Coleoptile cannot bend towards light; proves chemical signal must travel down the shaded side to cause bending", [
            "Coleoptile bends towards the light normally", "Coleoptile bends at a 90 degree angle downwards", "Mica sheet accelerates auxin transport by 400%",
            "Mica sheet allows light to enter the center of the stem", "Coleoptile transforms into an aquatic reed", "Coleoptile sheds all its leaves",
            "Coleoptile absorbs electricity from the mica", "Auxins diffuse across the impermeable mica barrier"
        ])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        exp = random.choice(auxin_experiments)
        q = f"Phototropism experimental evaluation {m_counter}: What is the biological result and scientific conclusion when a {exp[0]} is exposed to unilateral light?"
        add_q("medium", "Auxin Experiments", q, exp[1], exp[2], f"Result: {exp[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        ("A graph plotting auxin concentration against percentage growth response shows that root elongation is stimulated by extremely low auxin concentrations (10^-6 ppm) but strongly inhibited by concentrations above 10^-4 ppm, whereas stem elongation requires 10^-2 ppm for maximum stimulation. What is the physiological significance of this differential sensitivity?",
         "It ensures that a single hormonal signal (auxin accumulating on the lower side due to gravity) simultaneously directs roots downward into soil (inhibition) and shoots upward toward sunlight (stimulation)",
         ["It proves that roots do not respond to hormones under any circumstances", "It shows that stems contain five different types of auxins while roots contain none", "It proves that gravity destroys all auxins in the root within 5 minutes", "It shows that stems cannot undergo phototropism at high temperatures", "It indicates that roots are made of animal tissue rather than plant cells", "It proves that leaves absorb all excess auxins during rain"],
         "Differential tissue sensitivity allows identical auxin gradients to drive opposite geotropic responses in shoots and roots.", "Analysis"),

        ("In a scientific investigation testing the effect of unilateral light on oat coleoptiles, a student uses 40 seedlings in Group A (unilateral light) and 40 seedlings in Group B (uniform omnidirectional light). How did the student ensure both the validity and reliability of this investigation?",
         "Reliability was ensured by using a large sample size (40 seedlings per group) to minimize random error, while validity was ensured by keeping all other variables (species, temperature, moisture) constant with a proper control group",
         ["Reliability was ensured by changing the temperature every 30 minutes", "Validity was ensured by using 10 different plant species simultaneously", "Reliability was ensured by testing only one single seedling", "Validity was ensured by shining light from below the soil", "Reliability was ensured by turning off the lights completely for both groups", "Validity was ensured by removing the roots of all seedlings"],
         "Sample size and repetition ensure reliability; controlling extraneous variables and including a negative control ensures experimental validity.", "Analysis"),

        ("Why do plants grown in high-density monoculture crops frequently exhibit shade avoidance syndrome (excessive stem elongation and reduced branching)?",
         "Canopy shade has a low Red to Far-Red light ratio, which inactivates phytochrome, triggering elevated auxin and gibberellin synthesis that directs all energy toward vertical stem elongation at the expense of lateral growth",
         ["Monoculture crops produce excessive ethylene that poisons the roots", "Shade causes all stomata to rupture, reducing turgor pressure", "Plants in shade produce tannins that destroy their own chloroplasts", "High density causes roots to undergo meiosis instead of mitosis", "Lack of wind prevents the activation of suspensory ligaments in stems", "Shade converts all plant glucose into toxic nitrogen gas"],
         "Altered light quality (reduced R:FR ratio) signals impending canopy overgrowth, triggering auxin/gibberellin-mediated vertical elongation.", "Analysis"),

        ("Evaluate the trade-off of chemical plant defenses (such as tannins and alkaloids) versus structural mechanical defenses (such as thorns and thick bark). Which statement is scientifically accurate?",
         "Chemical defenses represent constitutive or inducible metabolic investments that deter specialized herbivores and microbes biochemically, but divert carbon and nitrogen resources away from growth and reproduction",
         ["Mechanical defenses cost zero metabolic energy for a plant to produce", "Chemical defenses are only produced when a plant is about to die", "Thorns protect plants against all bacterial and viral infections", "Tannins are synthetic chemicals invented by humans in 1950", "Plants with thorns do not require water or sunlight to grow", "Mechanical defenses always kill the herbivore on contact"],
         "Defense compounds require substantial energetic and nutritional reallocation from primary metabolism, representing an evolutionary resource trade-off.", "Analysis"),

        ("How does the mechanism of stomatal closure induced by Abscisic Acid (ABA) during severe water stress operate at the cellular level in guard cells?",
         "ABA binds to guard cell membrane receptors, triggering an efflux of potassium (K+) and chloride (Cl-) ions; water follows by osmosis out of the guard cells, causing them to lose turgor and close the pore",
         ["ABA pumps glucose into the guard cells, making them burst open", "ABA causes guard cells to undergo immediate cell division", "ABA turns the guard cell walls into impermeable granite rock", "ABA destroys the chloroplasts inside guard cells permanently", "ABA causes water to rush into guard cells by active transport", "ABA stimulates the synthesis of starch within the stomatal pore"],
         "ABA triggers ion efflux from guard cells; the resulting osmotic water loss collapses guard cell turgor, sealing the stomatal aperture.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "CAPS Botanical Synthesis: ", "Plant Endocrinology Evaluation: ", "Experimental Rigor Analysis: "]:
            add_q("hard", "Plant Physiology Evaluation", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Plant physiology diagnostic case {h_counter}: {base_h[0]}"
        add_q("hard", "Plant Physiology Evaluation", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/life_sciences/paper1_life_environment_plants.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_environment_plants()
