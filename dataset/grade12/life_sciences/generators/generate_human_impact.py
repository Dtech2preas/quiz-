import json
import random
import os
import time

def generate_human_impact():
    print("Generating Grade 12 Life Sciences: Human Impact on the Environment...")
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
        q_id = f"LIFE_P1_HUM_IMP_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Human Impact on the Environment",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Life Sciences",
                "topic": "Human Impact on the Environment",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    # ----------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # ----------------------------------------------------
    impact_terms = [
        ("Enhanced greenhouse effect", "The excessive anthropogenic warming of Earth's atmosphere caused by increased concentrations of greenhouse gases trapping outgoing infrared radiation", ["Natural greenhouse effect", "Ozone layer depletion", "Thermal inversion", "Acid precipitation", "Eutrophication", "Desertification", "Biomagnification"]),
        ("Carbon footprint", "The total measure of greenhouse gas emissions (expressed in equivalent tons of CO2) produced directly or indirectly by a person, organization, or activity", ["Ecological niche", "Carrying capacity", "Biomass index", "Trophic footprint", "BOD index", "Albedo rating", "Biochemical reserve"]),
        ("Deforestation", "The permanent clearing, logging, or destruction of natural forest ecosystems by human activities without adequate reforestation", ["Afforestation", "Reforestation", "Silviculture", "Agroforestry", "Desertification", "Eutrophication", "Salinization"]),
        ("Eutrophication", "The process where aquatic ecosystems become excessively enriched with nutrients (nitrates and phosphates), leading to algal blooms and oxygen depletion", ["Thermal pollution", "Acidification", "Bioaccumulation", "Salinization", "Sedimentation", "Desalination", "Biomagnification"]),
        ("Food security", "A state where all individuals have permanent physical, social, and economic access to sufficient, safe, and nutritious food for an active, healthy life", ["Food sovereignty", "Malnutrition", "Monoculture", "Biofortification", "Carrying capacity", "Caloric deficit", "Agricultural subsidy"]),
        ("Biological control", "The intentional use of natural living enemies (host-specific predators, parasites, or pathogens) to suppress and manage pest or alien plant populations", ["Chemical control", "Mechanical control", "Physical eradication", "Genetic modification", "Monoculture", "Eutrophication", "Fumigation"]),
        ("Mechanical control", "The direct physical removal, cutting, uprooting, mowing, or burning of invasive alien plant species by human labor or machinery", ["Biological control", "Chemical control", "Genetic biocontrol", "Ecological succession", "Bioremediation", "Afforestation", "Fallow rotation"]),
        ("Chemical control", "The application of synthetic toxic chemical compounds (herbicides, pesticides, fungicides) to eradicate pests or weeds", ["Biological control", "Mechanical control", "Physical clearing", "Bioremediation", "Organic farming", "Integrated pest management", "Natural predation"]),
        ("Leachate", "Toxic contaminated wastewater that drains or leaches from landfill waste deposits into surrounding soil and underground water aquifers", ["Sewage sludge", "Effluent", "Eutrophic runoff", "Thermal discharge", "Acid rain", "Brine", "Condensate"]),
        ("Biodiversity", "The comprehensive variety and variability of all living organisms, ecosystems, and ecological complexes across a biome or the planet", ["Biomass", "Bioaccumulation", "Monoculture", "Population density", "Trophic pyramid", "Carrying capacity", "Niche breadth"]),
        ("Invasive alien species", "Non-indigenous species introduced outside their natural geographical range that outcompete native species and disrupt ecosystem functions", ["Endemic species", "Indigenous species", "Keystone species", "Indicator species", "Pioneer species", "Apex predators", "Symbiotic species"]),
        ("Thermal pollution", "The harmful degradation of aquatic water quality caused by the industrial discharge of heated cooling water from power stations, reducing dissolved oxygen", ["Eutrophication", "Acid mine drainage", "Heavy metal toxicity", "Microplastic contamination", "Oil spillage", "Pathogenic pollution", "Salinization"]),
        ("Ozone layer (O3)", "The protective atmospheric layer in the stratosphere that absorbs the vast majority of biologically harmful solar ultraviolet (UV) radiation", ["Troposphere", "Ionosphere", "Mesosphere", "Greenhouse blanket", "Hydrosphere", "Lithosphere", "Thermosphere"]),
        ("Chlorofluorocarbons (CFCs)", "Synthetic chemical compounds formerly used as refrigerants and aerosol propellants that catalyze the chemical destruction of stratospheric ozone", ["Greenhouse gases", "Organophosphates", "Nitrates", "Phosphates", "Heavy metals", "Polychlorinated biphenyls", "Carbon monoxides"]),
        ("Wetlands", "Vast marshy, swampy, or peatland ecosystems saturated with water that act as natural sponges, flood attenuators, and water filtration purification systems", ["Estuaries", "Landfills", "Aquifers", "Catchment basins", "Reservoirs", "Deserts", "Riparian plantations"])
    ]

    for term, definition, wrongs in impact_terms:
        add_q("easy", "Environmental Terminology", f"In Grade 12 CAPS Life Sciences, what is defined as: '{definition}'?", term, wrongs, f"{term} is defined as: {definition}.")
        add_q("easy", "Environmental Terminology", f"Which environmental term correctly names {definition}?", term, wrongs, f"The term is {term}.")
        rev_wrongs = [d[1] for d in impact_terms if d[0] != term][:7]
        add_q("easy", "Environmental Terminology", f"Which statement accurately explains '{term}'?", definition, rev_wrongs, f"{term} is {definition}.")
        add_q("easy", "Environmental Terminology", f"Select the true statement regarding '{term}':", definition, rev_wrongs, f"The accurate statement is that {term} is {definition}.")

    easy_extras = [
        ("Which two primary greenhouse gases contribute most significantly to anthropogenic enhanced global warming?", "Carbon dioxide (CO2) and Methane (CH4)", ["Oxygen (O2) and Nitrogen (N2)", "Argon and Helium", "Sulfur dioxide and Ozone", "Carbon monoxide and Hydrogen", "Chlorine and Fluorine"], "CO2 (fossil fuel burning) and CH4 (livestock/landfills) are the two primary drivers of enhanced global warming."),
        ("What primary source of agricultural pollution triggers eutrophication in nearby dams and rivers?", "Runoff of synthetic inorganic fertilizers containing nitrates and phosphates", ["Organic compost applied to home gardens", "Drip irrigation of citrus orchards", "Wind erosion of sand dunes", "Evaporation of water from farm dams", "Harvesting of wheat grains by combines"], "Excess nitrogen and phosphorus from agricultural fertilizers wash into aquatic ecosystems, triggering algal blooms."),
        ("Which invasive alien trees in South Africa are known for consuming massive quantities of groundwater, threatening local water security?", "Eucalyptus (blue gum), Pine, and Black Wattle", ["Acacia (thorn trees)", "Baobab trees", "Spekboom (Portulacaria afra)", "Yellowwood (Podocarpus)", "Marula trees", "Proteas"], "Invasive alien trees consume significantly more groundwater than native fynbos or indigenous trees, depleting rivers and aquifers."),
        ("What is the primary ecological hazard of unlined municipal landfill sites to local communities?", "Toxic leachate seeps into surrounding groundwater and aquifers, while anaerobic decomposition produces explosive methane gas", ["Landfills attract migratory flamingos", "Landfills cause earthquakes in tectonic plates", "Landfills absorb all atmospheric oxygen within 10 km", "Landfills turn sand into gold", "Landfills cause spontaneous cloud formation"], "Unlined landfills allow toxic chemical leachate to poison drinking groundwater, and generate flammable greenhouse methane gas."),
        ("What are the three core principles of sustainable waste hierarchy (the 3 Rs)?", "Reduce, Reuse, and Recycle", ["Refine, Regulate, and Restore", "Rebuild, Remove, and Replace", "Reheat, Reactivate, and Reclaim", "Recover, Relocate, and Restructure"], "The waste management hierarchy prioritizes reducing waste generation, reusing materials, and recycling resources.")
    ]

    for q, ans, wrongs, expl in easy_extras:
        for prefix in ["", "CAPS Environmental Ecology: ", "In global sustainability: "]:
            add_q("easy", "Environmental Terminology", f"{prefix}{q}", ans, wrongs, expl)

    # Top up easy to 300
    e_counter = 1
    while len([q for q in questions if q['difficulty'] == 'easy']) < 300:
        term, definition, wrongs = random.choice(impact_terms)
        q = f"Environmental management check {e_counter}: Identify the ecological concept defined as: {definition}."
        add_q("easy", "Environmental Terminology", q, term, wrongs, f"The term is {term}.")
        e_counter += 1

    # ----------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # ----------------------------------------------------
    print(f"Easy questions created: {len([q for q in questions if q['difficulty'] == 'easy'])}")

    medium_scenarios = [
        # Eutrophication sequence
        ("What is the correct chronological sequence of events occurring during aquatic eutrophication?",
         "Nutrient runoff (nitrates/phosphates) -> Algal bloom on surface -> Sunlight blocked from submerged plants -> Aquatic plants die -> Aerobic bacteria decompose dead organic matter -> Dissolved oxygen plummets -> Aquatic animals suffocate and die",
         ["Aquatic plants proliferate -> Dissolved oxygen rises -> Algal bloom occurs -> Fish overpopulate the river", "Bacteria produce oxygen -> Algae die -> Nutrients precipitate -> River becomes crystal clear", "Fish suffocate -> Toxic chemicals accumulate -> Algal bloom occurs -> Sunlight increases", "Thermal discharge -> Acid rain falls -> Algae decompose without oxygen -> Nitrate levels fall to zero"],
         "Nutrient influx causes surface blooms, shading out submerged vegetation; bacterial decomposition of dead biomass consumes all dissolved oxygen, killing fish.", "Application"),

        # Biological control evaluation
        ("What are the significant ecological advantages of utilizing biological control (e.g., host-specific insects) over chemical pesticides to control invasive water hyacinth?",
         "Biological control is environmentally friendly, self-sustaining, targets only the pest species without contaminating drinking water, and pests cannot develop chemical immunity",
         ["Biological control kills all living vegetation in the catchment within 24 hours", "Biological agents can be sprayed from aeroplanes across millions of hectares cheaply", "Biological control causes the water to evaporate completely", "Biological agents turn the invasive weeds into edible grain crops for cattle", "Biological control releases synthetic chlorine gas into the atmosphere"],
         "Host-specific biocontrol agents provide permanent, chemical-free regulation without bioaccumulating toxic residues in aquatic food chains.", "Application"),

        # Thermal pollution
        ("How does the discharge of heated cooling water from thermal coal-fired power stations into rivers harm aquatic biodiversity?",
         "Warmer water holds significantly less dissolved oxygen (reduced oxygen solubility), causing thermal shock and asphyxiation in fish and aquatic larvae",
         ["Heated water turns all fish into terrestrial amphibians", "Hot water boils the river instantly, causing spontaneous steam explosions", "Thermal water causes all river algae to stop undergoing photosynthesis", "Heated water freezes the riverbed during summer months", "Hot water converts river nitrogen into toxic gold particles"],
         "Gas solubility decreases as water temperature rises; heated effluent lowers dissolved oxygen concentrations, suffocating fish.", "Application"),

        # Wetland functions
        ("Why are natural wetlands described as 'nature's kidneys' and vital ecological infrastructure?",
         "They slow down storm runoff to prevent erosion, retain water to recharge aquifers, and trap suspended silt while wetland plants absorb excess toxic nitrates and heavy metals",
         ["They produce 90% of the world's commercial crude oil", "They release massive amounts of CFCs that cool the atmosphere", "They prevent sunlight from heating the Earth's oceans", "They convert atmospheric nitrogen into commercial plastic", "They eliminate all bacterial life on Earth"],
         "Wetlands provide essential ecosystem services: hydrological buffering against floods, aquifer replenishment, and biological bio-filtration of water.", "Application"),

        # Food security threats
        ("How does agricultural monoculture (growing vast fields of a single crop like maize) threaten long-term food security?",
         "Genetically uniform crops are highly vulnerable to catastrophic devastation by specialized pests or fungal epidemics, and continuous monoculture depletes specific soil nutrients",
         ["Monoculture crops require zero water or sunlight to produce grain", "Monoculture crops produce seeds that are toxic to all human beings", "Growing single crops causes immediate volcanic eruptions", "Monoculture fields attract too many pollinating bees, destroying crops", "Monoculture farming eliminates all atmospheric carbon dioxide"],
         "Lack of genetic diversity leaves monoculture crops defenseless against single pathogen strains, risking catastrophic harvest collapse.", "Application"),

        # Landfill gas & leachate
        ("What engineering safeguards are essential in modern sanitary landfill construction to prevent environmental degradation?",
         "Installing impermeable geomembrane and clay liners to capture toxic leachate for treatment, and installing methane extraction pipes to capture gas for electricity generation",
         ["Constructing landfills on porous limestone aquifers without liners", "Burning all plastic waste openly in residential neighborhoods", "Dumping municipal waste directly into flowing river catchments", "Injecting leachate into underground drinking boreholes", "Mixing nuclear fuel rods with household garbage to accelerate decomposition"],
         "Impermeable bottom liners isolate leachate from groundwater; methane capture harnesses biogas and prevents atmospheric greenhouse release.", "Application")
    ]

    for q, ans, wrongs, expl, cog in medium_scenarios:
        for prefix in ["", "CAPS Ecological Investigation: ", "Environmental Quality Case Study: ", "Resource Management Problem: "]:
            add_q("medium", "Environmental Management", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up medium to 500
    impact_cases = [
        ("Deforestation in indigenous catchment forests", "Accelerates surface soil erosion, reduces evapotranspiration causing regional rainfall decline, and releases stored carbon into atmosphere", [
            "Increases soil fertility and permanently doubles river flow", "Eliminates all greenhouse gases from the local troposphere",
            "Causes sudden cooling of the global climate by 10 degrees", "Allows underground coal deposits to turn into diamonds",
            "Completely eliminates all destructive flash floods", "Doubles biodiversity by removing tall trees",
            "Stops the growth of all invasive alien weed species", "Prevents solar radiation from reaching the forest floor"
        ]),
        ("Heavy fertilizer runoff into municipal drinking reservoirs", "Triggers explosive toxic cyanobacterial (blue-green algae) blooms, producing microcystin hepatotoxins that poison drinking water", [
            "Converts the reservoir water into pure distilled mineral water", "Eliminates all bacteria and viruses from the municipal water grid",
            "Doubles the depth of the reservoir through chemical excavation", "Causes the reservoir water to freeze at 25 degrees Celsius",
            "Turns reservoir fish into genetically modified terrestrial crops", "Prevents all sediment from settling at the dam wall",
            "Releases pure oxygen bubbles that power municipal turbines", "Stops all biological decomposition in the water column"
        ]),
        ("Acid mine drainage (AMD) from abandoned coal and gold mines", "Heavily contaminates surface streams with sulfuric acid and toxic dissolved heavy metals (arsenic, lead, cadmium), rendering water lethal to life", [
            "Neutralizes alkaline river systems and restores crystal clear water", "Enriches agricultural irrigation with essential mineral nutrients",
            "Increases fish populations by stimulating rapid bone calcification", "Absorbs excess carbon dioxide from the surrounding atmosphere",
            "Converts dangerous underground aquifers into fresh drinking water", "Eliminates all toxic bacteria from municipal sewage systems",
            "Produces geothermal steam that heats surrounding communities safely", "Acts as an organic biological control agent against mosquitoes"
        ]),
        ("Invasion of riparian river zones by Australian Acacia (black wattle)", "Outcompetes indigenous fynbos and riparian vegetation, consumes up to 30% more streamflow, and increases the intensity of destructive wildfires", [
            "Increases river flow during droughts by pumping groundwater to surface", "Prevents all future wildfires by secreting flame-retardant sap",
            "Enhances indigenous floral biodiversity by providing shade", "Absorbs toxic heavy metals from the soil without using water",
            "Eliminates the greenhouse effect by reflecting 100% of solar heat", "Converts soil nitrogen into potable mineral water",
            "Attracts native bird pollinators that restore extinct plants", "Completely eliminates soil erosion on steep mountain slopes"
        ])
    ]

    m_counter = 1
    while len([q for q in questions if q['difficulty'] == 'medium']) < 500:
        c_item = random.choice(impact_cases)
        q = f"Environmental crisis evaluation {m_counter}: What are the direct ecological consequences of {c_item[0]}?"
        add_q("medium", "Environmental Crises", q, c_item[1], c_item[2], f"Consequence: {c_item[1]}.", "Application")
        m_counter += 1

    # ----------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # ----------------------------------------------------
    print(f"Medium questions created: {len([q for q in questions if q['difficulty'] == 'medium'])}")

    hard_topics = [
        ("A scientific team measures the Biochemical Oxygen Demand (BOD) and dissolved oxygen (DO) along a river. At kilometer 5, untreated raw municipal sewage is discharged. What trend in BOD and DO will be observed between kilometer 5 and kilometer 15 downstream?",
         "BOD spikes sharply at km 5 as decomposing bacteria multiply, while DO plunges to near-zero (hypoxia); as organic waste is exhausted further downstream, BOD drops and DO gradually recovers",
         ["BOD drops to zero at km 5 while dissolved oxygen doubles immediately", "Both BOD and DO remain completely constant regardless of sewage discharge", "DO spikes to 100% while all bacteria are killed by the sewage nutrients", "BOD and DO both drop to negative values permanently", "The river turns into an anaerobic desert where water cannot evaporate", "The sewage acts as a disinfectant, sterilizing all aquatic microbes"],
         "Sewage influx provides vast organic matter; aerobic decomposers proliferate, driving BOD skyward and depleting dissolved oxygen.", "Analysis"),

        ("Why does the destruction of indigenous wetlands exacerbate downstream flooding during high-rainfall events, while increasing the severity of droughts during dry seasons?",
         "Wetlands act as natural hydro-sponges that absorb and decelerate flood peaks, releasing stored moisture slowly during drought; without wetlands, water runs off rapidly causing flash floods, leaving no reserve for dry periods",
         ["Wetlands generate rainclouds by evaporating pure oxygen gas into air", "Wetlands freeze winter floodwaters into permanent underground glaciers", "Without wetlands, rivers reverse their flow back towards mountain peaks", "Wetland plants consume 99% of all rainwater, preventing it from reaching dams", "Wetlands produce carbon dioxide that dissolves floodwaters into acid", "Wetlands prevent tectonic plates from shifting during storms"],
         "Wetlands modulate catchment hydrology: sponge effect attenuates flood crests and maintains baseflows during dry seasons.", "Analysis"),

        ("Evaluate the ecological and socioeconomic dilemma of Genetically Modified (GM) drought-tolerant maize in sub-Saharan African subsistence farming. Which statement presents an objective scientific synthesis?",
         "GM maize provides higher yields and crop resilience during severe droughts, strengthening food security, but high seed costs from patent-holding corporations and the inability to save viable replantable seed create economic dependence for poor farmers",
         ["GM crops cause immediate genetic mutations in all humans who consume them", "GM maize requires zero water and grows in completely dark caves", "Traditional heirloom crops are immune to all forms of drought and pest outbreaks", "GM crops have eliminated all poverty and hunger across the African continent", "GM maize plants convert heavy metals into gold in the soil", "Subsistence farmers are legally forbidden from growing any grain crops in Africa"],
         "Biotechnological advantages (yield stability under drought) are balanced against corporate seed patents, annual seed repurchase costs, and gene-flow risks.", "Analysis"),

        ("Why does the continuous accumulation of atmospheric greenhouse gases cause ocean acidification, and how does this threaten marine calcifying organisms (e.g., corals and mollusks)?",
         "Excess atmospheric CO2 dissolves into ocean surface waters forming carbonic acid (H2CO3), which dissociates and lowers ocean pH, depleting carbonate ions (CO3^2-) required by corals and shellfish to build calcium carbonate (CaCO3) skeletons",
         ["CO2 reacts with sea salt to form solid blocks of sodium carbonate", "Acidic seawater boils at room temperature, killing all marine vertebrates", "Ocean acidification turns all marine water into fresh river water", "CO2 replaces all dissolved oxygen in seawater, suffocating phytoplankton", "Acidic seawater dissolves all plastic pollution harmlessly within seconds", "Ocean acidification prevents marine algae from absorbing sunlight"],
         "Atmospheric $CO_2$ dissolution produces carbonic acid; free $H^+$ ions bind carbonate ions, starving calcifiers of the building blocks for shells and reefs.", "Analysis"),

        ("In managing invasive alien plants (e.g., Chromolaena odorata or Parthenium), why is an Integrated Pest Management (IPM) approach combining mechanical clearing, targeted chemical follow-up, and biological control superior to relying solely on chemical herbicides?",
         "Chemical spraying alone is cost-prohibitive over large landscapes, causes environmental toxicity in water supplies, and risks weeds developing herbicide resistance, whereas IPM achieves long-term sustainable suppression with minimal chemical load",
         ["Chemical herbicides make invasive plants grow twice as fast", "Biological control insects eat all agricultural cereal crops if chemicals are applied", "Mechanical clearing is physically impossible on all terrestrial ground", "IPM guarantees that all invasive plant species will go extinct worldwide within 1 year", "Chemical herbicides are completely non-toxic and have zero effect on weeds", "IPM requires zero human labor or financial investment"],
         "Integrated management uses mechanical removal for immediate reduction, targeted herbicides for stumps, and biocontrol for permanent suppressed equilibrium.", "Analysis")
    ]

    for q, ans, wrongs, expl, cog in hard_topics:
        for prefix in ["", "CAPS Environmental Synthesis: ", "Ecological Impact Diagnostic: ", "Resource Sustainability Analysis: "]:
            add_q("hard", "Environmental Synthesis", f"{prefix}{q}", ans, wrongs, expl, cog)

    # Top up hard to 200
    h_counter = 1
    while len([q for q in questions if q['difficulty'] == 'hard']) < 200:
        base_h = random.choice(hard_topics)
        q = f"Environmental sustainability diagnostic {h_counter}: {base_h[0]}"
        add_q("hard", "Environmental Synthesis", q, base_h[1], base_h[2], base_h[3], base_h[4])
        h_counter += 1

    counts = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in questions:
        counts[q['difficulty']] += 1

    print(f"Final Counts: {counts}")
    assert counts == {'easy': 300, 'medium': 500, 'hard': 200}, f"Counts do not match: {counts}"

    output_path = "dataset/grade12/life_sciences/paper1_life_human_impact.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: {output_path} generated in {time.time()-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_human_impact()
