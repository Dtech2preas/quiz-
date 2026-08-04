const fs = require('fs');
const path = require('path');

// Specific overrides based on previous map.json for backwards compatibility
const OVERRIDES = {
    "paper1_tech_algebra": "Paper 1: Algebra, Equations & Inequalities",
    "paper1_tech_functions": "Paper 1: Functions & Graphs",
    "paper1_tech_finance": "Paper 1: Financial Mathematics",
    "paper1_tech_calculus": "Paper 1: Differential Calculus & Integration",
    "paper2_tech_analytical": "Paper 2: Analytical Geometry",
    "paper2_tech_trig": "Paper 2: Trigonometry",
    "paper2_tech_circle_angular": "Paper 2: Circle Geometry & Angular Movement",
    "paper2_tech_mensuration": "Paper 2: Mensuration",
    "paper1_acc_companies": "Paper 1: Companies & Corporate Governance",
    "paper1_acc_financial_statements": "Paper 1: Financial Statements",
    "paper1_acc_cash_flow": "Paper 1: Cash Flow Statements",
    "paper1_acc_analysis": "Paper 1: Analysis & Interpretation",
    "paper2_acc_manufacturing": "Paper 2: Cost Accounting (Manufacturing)",
    "paper2_acc_budgeting": "Paper 2: Budgeting",
    "paper2_acc_inventory": "Paper 2: Inventory & Asset Control",
    "paper2_acc_reconciliations": "Paper 2: Reconciliations & Internal Control",
    "paper1_algebra": "Paper 1: Algebra",
    "paper1_calculus": "Paper 1: Calculus",
    "paper1_finance": "Paper 1: Finance",
    "paper1_functions": "Paper 1: Functions",
    "paper1_probability": "Paper 1: Probability",
    "paper1_sequences": "Paper 1: Sequences",
    "paper2_analytical_geometry": "Paper 2: Analytical Geometry",
    "paper2_geometry": "Paper 2: Euclidean Geometry",
    "paper2_statistics": "Paper 2: Statistics",
    "paper2_trigonometry": "Paper 2: Trigonometry",
    "paper1_circular_motion": "Paper 1: Circular Motion",
    "paper1_mechanics": "Paper 1: Mechanics",
    "paper1_oscillations_waves": "Paper 1: Oscillations & Waves",
    "paper1_thermal_physics": "Paper 1: Thermal Physics",
    "paper1_work_energy_power": "Paper 1: Work, Energy & Power",
    "paper2_acids_bases": "Paper 2: Acids & Bases",
    "paper2_atomic_nuclear": "Paper 2: Atomic & Nuclear",
    "paper2_bonding_structure": "Paper 2: Bonding & Structure",
    "paper2_electrochemistry": "Paper 2: Electrochemistry",
    "paper2_kinetics_equilibrium": "Paper 2: Kinetics & Equilibrium",
    "paper2_stoichiometry": "Paper 2: Stoichiometry",
    "paper1_life_meiosis": "Paper 1: Meiosis",
    "paper1_life_reproduction_vertebrates": "Paper 1: Reproduction in Vertebrates",
    "paper1_life_human_reproduction": "Paper 1: Human Reproduction",
    "paper1_life_environment_humans": "Paper 1: Responding to the Environment (Humans)",
    "paper1_life_endocrine_system": "Paper 1: Human Endocrine System",
    "paper1_life_homeostasis": "Paper 1: Homeostasis in Humans",
    "paper1_life_environment_plants": "Paper 1: Responding to the Environment (Plants)",
    "paper1_life_human_impact": "Paper 1: Human Impact on Environment",
    "paper2_life_dna_code": "Paper 2: DNA: Code of Life",
    "paper2_life_meiosis": "Paper 2: Meiosis",
    "paper2_life_genetics": "Paper 2: Genetics and Inheritance",
    "paper2_life_evolution": "Paper 2: Evolution",
    "paper1_newtons_laws": "Paper 1: Newton's Laws",
    "paper1_momentum": "Paper 1: Momentum",
    "paper1_work_energy_and_power": "Paper 1: Work, Energy & Power",
    "paper1_elasticity_and_hydraulics": "Paper 1: Elasticity & Hydraulics",
    "paper1_waves_sound_and_light": "Paper 1: Waves, Sound & Light",
    "paper1_electricity": "Paper 1: Electricity",
    "paper1_electromagnetism": "Paper 1: Electromagnetism",
    "paper2_organic_chemistry": "Paper 2: Organic Chemistry",
    "paper2_materials": "Paper 2: Matter & Materials",
    "paper1_mathlit12_finance": "Paper 1: Finance",
    "paper1_mathlit12_data_handling": "Paper 1: Data Handling",
    "paper1_mathlit12_probability": "Paper 1: Probability",
    "paper2_mathlit12_measurement": "Paper 2: Measurement",
    "paper2_mathlit12_maps_plans": "Paper 2: Maps and Plans",
    "paper2_mathlit12_probability": "Paper 2: Probability",
    "grade8_math_numbers_operations_relationships": "Numbers, Operations and Relationships",
    "grade8_math_patterns_algebra": "Patterns, Functions and Algebra",
    "grade8_math_geometry": "Space and Shape (Geometry)",
    "grade8_math_measurement": "Measurement",
    "grade8_math_data_handling": "Data Handling",
    "grade8_math_probability": "Probability",
    "grade6_nst_life_living_processing": "Life and Living & Processing",
    "grade6_nst_matter_materials_processing": "Matter and Materials & Processing",
    "grade6_nst_energy_change_systems_control": "Energy and Change & Systems and Control",
    "grade6_nst_planet_earth_beyond_systems_control": "Planet Earth and Beyond & Systems and Control",
    "basic_addition": "Basic Addition",
    "basic_subtraction": "Basic Subtraction"
};

function getLabel(filename) {
    let name = path.basename(filename, '.json');
    if (OVERRIDES[name]) {
        return OVERRIDES[name];
    }

    // Auto-format
    // Remove grade prefix like "grade10_math_" or "grade10_"
    name = name.replace(/^grade\d+_[a-z]+_/, '');
    name = name.replace(/^grade\d+_/, '');

    // Replace "paperX_" with "Paper X: "
    name = name.replace(/^paper(\d+)_/, 'Paper $1: ');

    // Replace underscores with spaces
    name = name.replace(/_/g, ' ');

    // Title Case
    const lowerWords = ['and', 'or', 'of', 'in', 'the', 'to', 'on', 'with'];
    const words = name.split(' ').map((word, index) => {
        if (index > 0 && lowerWords.includes(word.toLowerCase())) {
            return word.toLowerCase();
        }
        return word.charAt(0).toUpperCase() + word.slice(1);
    });

    return words.join(' ');
}

function walkSync(dir, callback) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filepath = path.join(dir, file);
        const stats = fs.statSync(filepath);
        if (stats.isDirectory()) {
            walkSync(filepath, callback);
        } else if (stats.isFile()) {
            callback(filepath);
        }
    }
}

function generateMap() {
    const datasetDir = 'dataset';
    const gradeMap = {};

    if (!fs.existsSync(datasetDir)) {
        console.error("Dataset directory does not exist.");
        return;
    }

    walkSync(datasetDir, (filepath) => {
        if (!filepath.endsWith('.json')) return;

        // Skip specific files/folders
        const relativePath = path.relative(datasetDir, filepath);
        const parts = relativePath.split(path.sep);

        if (parts.includes('weekly_quiz')) return;
        const filename = path.basename(filepath);
        if (filename.startsWith('kb_') || filename.startsWith('extracted')) return;

        let grade, subject;

        // Match structure: gradeX/subject/filename.json
        if (parts.length >= 3 && parts[0].startsWith('grade')) {
            grade = parts[0];
            subject = parts[1];
        } else if (parts.length >= 2 && parts[0] === 'mathematical_literacy') {
            // Handle root mathematical_literacy folder mapping to grade12
            grade = 'grade12';
            subject = parts[0];
        } else {
            return; // Unknown structure
        }

        if (!gradeMap[grade]) gradeMap[grade] = {};
        if (!gradeMap[grade][subject]) gradeMap[grade][subject] = [];

        const label = getLabel(filename);

        // Check for duplicates
        const exists = gradeMap[grade][subject].some(item => item.file === filename);
        if (!exists) {
            gradeMap[grade][subject].push({ file: filename, label: label });
        }
    });

    // Sort logic
    const sortedGradeMap = {};
    for (let i = 1; i <= 12; i++) {
        const grade = `grade${i}`;
        if (gradeMap[grade]) {
            sortedGradeMap[grade] = {};

            // Sort subjects
            const sortedSubjects = Object.keys(gradeMap[grade]).sort();
            for (const subject of sortedSubjects) {
                // Sort files alphabetically by label
                sortedGradeMap[grade][subject] = gradeMap[grade][subject].sort((a, b) => {
                    return a.label.localeCompare(b.label);
                });
            }
        }
    }

    fs.writeFileSync('map.json', JSON.stringify(sortedGradeMap, null, 2) + '\n');
    console.log("Successfully generated map.json with dynamic datasets.");
}

generateMap();
