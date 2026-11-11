import json
import os
import random
import time

def build_probability_dataset():
    questions = []
    seen_questions = set()
    
    target_easy = 300
    target_med = 500
    target_hard = 200
    counts = {"easy": 0, "medium": 0, "hard": 0}
    
    def add_q(subtopic, difficulty, q_text, correct_ans, distractors, explanation):
        if counts[difficulty] >= (target_easy if difficulty == "easy" else target_med if difficulty == "medium" else target_hard):
            return False
        if q_text in seen_questions:
            return False
            
        c_str = str(correct_ans).strip()
        clean_dist = []
        seen_d = {c_str}
        for d in distractors:
            d_str = str(d).strip()
            if d_str and d_str not in seen_d:
                seen_d.add(d_str)
                clean_dist.append(d_str)
                
        if len(clean_dist) < 6:
            return False
            
        seen_questions.add(q_text)
        counts[difficulty] += 1
        q_id = f"ML12_P1_PROB_{len(questions) + 1:04d}"
        
        questions.append({
            "id": q_id,
            "topic": "Probability",
            "subtopic": subtopic,
            "paper": "paper1",
            "difficulty": difficulty,
            "question": q_text,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_dist[:8],
            "explanation": explanation
        })
        return True

    sa_schools = ["Soweto High", "Umlazi Secondary", "Khayelitsha High", "Polokwane Technical", "Kimberley Boys High", "Mangaung High", "East London Secondary", "Nelspruit High", "Tembisa Secondary", "Athlone High"]
    sa_towns = ["Durban", "Johannesburg", "Cape Town", "Gqeberha", "Bloemfontein", "Polokwane", "Pretoria", "Nelspruit", "Kimberley", "Rustenburg"]

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    scale_terms = [
        ("Impossible event", "An event with a probability of exactly 0 (0%), meaning it cannot occur under any circumstances.",
         ["An event with a probability of 0.5 (50%) like a fair coin toss.", "An event with a probability of exactly 1 (100%).", "An event that occurs in more than 75% of experimental trials.", "An event whose probability depends on the sample size.", "An event that is statistically classified as an outlier.", "An event that occurs only when rolling a 6 on a die."]),
        ("Certain event", "An event with a probability of exactly 1 (100%), meaning it is guaranteed to occur.",
         ["An event with a probability of 0 (0%) that cannot happen.", "An event with an even 50% chance of occurrence.", "An event that has occurred in at least 5 consecutive trials.", "An event whose outcome is completely unpredictable.", "An event with a probability between 0.70 and 0.90.", "An event tested under strict laboratory conditions."]),
        ("Even chance", "An event with a probability of 0.5 (50% or 1/2), where the event is just as likely to occur as it is not to occur.",
         ["An event that has a probability of 1.0 (100%).", "An event that has an impossible probability of 0.", "An event where all outcomes are prime numbers.", "An event with a probability of exactly 0.25 (25%).", "An event that only occurs on even calendar days.", "An event whose probability is determined after 100 trials."]),
        ("Complementary events", "Two mutually exclusive events that together contain all possible outcomes of the sample space, such that P(A) + P(not A) = 1.",
         ["Two events that both occur at the exact same moment in time.", "Two events that have identical probabilities of 0.5.", "Events that are plotted on perpendicular axes of a scatter plot.", "Two events where one event causes the other event to occur.", "Events with zero probability in a two-way contingency table.", "Events that can only be modeled using a three-stage tree diagram."]),
        ("Theoretical probability", "The calculated mathematical likelihood of an event occurring based on the ratio of favourable outcomes to total possible outcomes in a sample space.",
         ["The probability calculated by conducting an actual physical experiment and tallying results.", "The total number of trials conducted in a laboratory simulation.", "The probability that remains after subtracting the medical tax credit.", "The percentage error between two successive measurements.", "The probability determined by interviewing a focus group.", "The difference between the maximum and minimum observations in a sample."]),
        ("Relative frequency", "The proportion of times an event actually occurred during an experiment, calculated as the observed frequency divided by the total number of trials.",
         ["The theoretical likelihood calculated from mathematical formulas before any experiment.", "The arithmetic mean of all outcomes in a continuous probability distribution.", "The spread between the upper quartile and lower quartile of experimental results.", "The probability of rolling a double six with two fair dice.", "The constant interest rate charged on hire purchase balances.", "The ratio of true positives to false negatives in medical testing."])
    ]
    for term, c_def, w_defs in scale_terms:
        q = f"In Mathematical Literacy probability, define the term '{term}'."
        add_q("Probability Expressions & Scale", "easy", q, c_def, w_defs, f"Official CAPS definition: {term} is defined as: {c_def}")

    bag_scenarios = [
        ("stationery pencil case", "pens", [("blue", 12), ("black", 10), ("red", 6), ("green", 4)]),
        ("school sports kit bag", "balls", [("tennis balls", 15), ("cricket balls", 9), ("hockey balls", 6)]),
        ("tuckshop raffle container", "tokens", [("gold", 8), ("silver", 14), ("bronze", 18)]),
        ("charity donation bucket", "envelopes", [("R10 vouchers", 25), ("R20 vouchers", 15), ("R50 vouchers", 10)]),
        ("science lab drawer", "beakers", [("100 ml", 12), ("250 ml", 16), ("500 ml", 8), ("1000 ml", 4)]),
        ("library returns bin", "books", [("fiction novels", 20), ("science textbooks", 15), ("history biographies", 10), ("dictionaries", 5)]),
        ("art workshop cupboard", "brushes", [("flat brushes", 18), ("round brushes", 14), ("fan brushes", 8)]),
        ("athletics equipment shed", "relays", [("yellow batons", 10), ("green batons", 12), ("red batons", 8), ("blue batons", 10)])
    ]
    for bag_name, item_kind, contents in bag_scenarios:
        for factor in [1, 2, 3, 4]:
            scaled_contents = [(col, cnt * factor) for col, cnt in contents]
            tot_items = sum(cnt for _, cnt in scaled_contents)
            for col, cnt in scaled_contents:
                frac_str = f"{cnt}/{tot_items}"
                pct_val = round((cnt / tot_items) * 100.0, 1)
                not_cnt = tot_items - cnt
                not_pct = round((not_cnt / tot_items) * 100.0, 1)
                
                q_frac = f"A {bag_name} contains {tot_items} {item_kind}: {', '.join([f'{c} {k}' for k, c in scaled_contents])}. If one item is selected at random, what is the probability of selecting a {col} item, expressed as a common fraction?"
                c_frac = frac_str
                d_frac = [
                    f"{cnt}/{tot_items - cnt}",
                    f"{tot_items - cnt}/{tot_items}",
                    f"1/{cnt}",
                    f"{cnt}/{tot_items + 5}",
                    f"{cnt - 1}/{tot_items}",
                    f"1/{tot_items}",
                    f"{round(cnt / 2)}/{tot_items}"
                ]
                exp_frac = f"P({col}) = Number of {col} items ÷ Total items = {cnt}/{tot_items}."
                add_q("Single-Event Probability", "easy", q_frac, c_frac, d_frac, exp_frac)
                
                q_pct = f"From the same {bag_name} of {tot_items} {item_kind}, calculate the percentage probability of randomly selecting a {col} item. (Round to 1 decimal place)."
                c_pct = f"{pct_val}%"
                d_pct = [
                    f"{round(100.0 - pct_val, 1)}%",
                    f"{round(pct_val * 1.15, 1)}%",
                    f"{round(pct_val * 0.85, 1)}%",
                    f"{round(cnt * 1.5, 1)}%",
                    f"{round(pct_val + 10.0, 1)}%",
                    f"{round(pct_val - 10.0, 1)}%",
                    f"{round((cnt / (tot_items - cnt)) * 100.0, 1)}%"
                ]
                exp_pct = f"Percentage Probability = ({cnt} ÷ {tot_items}) × 100% = {pct_val}%."
                add_q("Single-Event Probability", "easy", q_pct, c_pct, d_pct, exp_pct)

                q_not = f"What is the probability of NOT selecting a {col} item from the {bag_name} with {tot_items} items, expressed as a percentage?"
                c_not = f"{not_pct}%"
                d_not = [
                    f"{pct_val}%",
                    f"{round(not_pct * 1.10, 1)}%",
                    f"{round(not_pct * 0.90, 1)}%",
                    f"{round(not_pct + 8.5, 1)}%",
                    f"{round(not_pct - 8.5, 1)}%",
                    f"{round(cnt / 5.0, 1)}%",
                    f"{round((not_cnt / cnt) * 10.0, 1)}%"
                ]
                exp_not = f"P(Not {col}) = 100% - P({col}) = 100% - {pct_val}% = {not_pct}%."
                add_q("Compound Events & Complementary Rules", "easy", q_not, c_not, d_not, exp_not)

    for school in sa_schools:
        for t_tickets in [150, 200, 250, 300, 400, 500, 600, 800]:
            for bought in [2, 5, 8, 10, 12, 15]:
                prob_pct = round((bought / t_tickets) * 100.0, 2)
                q_raf = f"At {school}, the RCL printed {t_tickets} tickets for an annual fundraising raffle. A learner buys {bought} tickets. What is the probability that this learner wins the grand prize, expressed as a percentage?"
                c_raf = f"{prob_pct}%"
                d_raf = [
                    f"{round(prob_pct * 1.5, 2)}%",
                    f"{round(prob_pct * 0.5, 2)}%",
                    f"{round(100 - prob_pct, 2)}%",
                    f"{round(bought / 10.0, 2)}%",
                    f"{round(prob_pct + 4.5, 2)}%",
                    f"{round(prob_pct - 4.5 if prob_pct > 5 else prob_pct + 2.5, 2)}%",
                    f"{round((bought / (t_tickets - bought)) * 100.0, 2)}%"
                ]
                exp_raf = f"Probability = (Tickets bought ÷ Total tickets) × 100% = ({bought} ÷ {t_tickets}) × 100% = {prob_pct}%."
                add_q("Single-Event Probability", "easy", q_raf, c_raf, d_raf, exp_raf)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    contingency_scenarios = [
        ("Grade 12 Driver's License Status", "Gender", ["Male", "Female"], "License", ["Has License", "No License"], [[65, 85], [45, 105]]),
        ("Commuter Transport Mode Preference", "Area", ["Urban", "Rural"], "Mode", ["Public Transit", "Private Vehicle"], [[180, 70], [210, 40]]),
        ("Community Clinic Hypertension Screening", "Age Group", ["Under 45", "45 and Older"], "Status", ["Hypertensive", "Normal BP"], [[35, 165], [95, 105]]),
        ("High School Sports Participation", "Gender", ["Boys", "Girls"], "Sport Type", ["Team Sports", "Individual Sports"], [[120, 40], [90, 70]]),
        ("Matric Examination Distinctions", "Subject Choice", ["Maths Lit", "Mathematics"], "Achievement", ["Distinction", "No Distinction"], [[85, 215], [60, 140]]),
        ("Cellular Network Provider Choice", "Device Type", ["Smartphones", "Feature Phones"], "Network", ["Vodacom", "MTN"], [[140, 90], [110, 60]]),
        ("University Application Status", "Faculty", ["Commerce", "Humanities"], "Admission", ["Accepted", "Waitlisted"], [[75, 125], [90, 110]]),
        ("Municipal Waste Recycling Participation", "Household Type", ["Suburban House", "Informal Settlement"], "Recycling", ["Recycles Waste", "Does Not Recycle"], [[130, 70], [50, 150]]),
        ("Tertiary Student Accommodation", "Study Year", ["First Year", "Senior Year"], "Housing", ["University Residence", "Private Rental"], [[160, 80], [70, 190]]),
        ("Commercial Banking Channel Usage", "Age Bracket", ["18-35 Years", "Above 35 Years"], "Platform", ["Mobile Banking App", "Branch Counter"], [[220, 40], [90, 150]]),
        ("Public Library Membership", "Category", ["Learners", "Adults"], "Card Type", ["Digital Borrower", "Physical Only"], [[175, 65], [85, 115]]),
        ("Local Supermarket Payment Method", "Time Slot", ["Morning", "Evening"], "Tender", ["Card/Contactless", "Cash"], [[140, 60], [180, 120]])
    ]
    
    for c_title, r_label, rows, col_label, cols, matrix in contingency_scenarios:
        for mult in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]:
            m = [[val * mult for val in row] for row in matrix]
            r0_tot = sum(m[0])
            r1_tot = sum(m[1])
            c0_tot = m[0][0] + m[1][0]
            c1_tot = m[0][1] + m[1][1]
            grand_tot = r0_tot + r1_tot
            
            p_r0_pct = round((r0_tot / grand_tot) * 100.0, 1)
            q_cp1 = (f"The two-way contingency table below summarizes survey data for {c_title} (Grand Total = {grand_tot}):\n"
                     f"• {rows[0]}: {cols[0]} = {m[0][0]}, {cols[1]} = {m[0][1]} (Row Total = {r0_tot})\n"
                     f"• {rows[1]}: {cols[0]} = {m[1][0]}, {cols[1]} = {m[1][1]} (Row Total = {r1_tot})\n"
                     f"Determine the probability that a randomly chosen respondent is '{rows[0]}', expressed as a percentage. (Round to 1 decimal place).")
            c_cp1 = f"{p_r0_pct}%"
            d_cp1 = [
                f"{round((r1_tot / grand_tot) * 100.0, 1)}%",
                f"{round((m[0][0] / grand_tot) * 100.0, 1)}%",
                f"{round((c0_tot / grand_tot) * 100.0, 1)}%",
                f"{round(p_r0_pct * 1.15, 1)}%",
                f"{round(p_r0_pct * 0.85, 1)}%",
                f"{round(p_r0_pct + 12.0, 1)}%",
                f"{round(p_r0_pct - 12.0, 1)}%"
            ]
            exp_cp1 = f"P({rows[0]}) = Row Total ÷ Grand Total = {r0_tot} ÷ {grand_tot} × 100% = {p_r0_pct}%."
            add_q("Two-Way Contingency Tables", "medium", q_cp1, c_cp1, d_cp1, exp_cp1)

            p_joint = round((m[0][0] / grand_tot) * 100.0, 1)
            q_cp2 = (f"Using the contingency table for {c_title} (Grand Total = {grand_tot}):\n"
                     f"Determine the probability that a randomly selected person is BOTH '{rows[0]}' AND '{cols[0]}', expressed as a percentage.")
            c_cp2 = f"{p_joint}%"
            d_cp2 = [
                f"{p_r0_pct}%",
                f"{round((c0_tot / grand_tot) * 100.0, 1)}%",
                f"{round((m[0][1] / grand_tot) * 100.0, 1)}%",
                f"{round((m[1][0] / grand_tot) * 100.0, 1)}%",
                f"{round(p_joint * 1.20, 1)}%",
                f"{round(p_joint * 0.80, 1)}%",
                f"{round(p_joint + 8.5, 1)}%"
            ]
            exp_cp2 = f"P({rows[0]} and {cols[0]}) = Cell count ÷ Grand Total = {m[0][0]} ÷ {grand_tot} × 100% = {p_joint}%."
            add_q("Two-Way Contingency Tables", "medium", q_cp2, c_cp2, d_cp2, exp_cp2)

            p_cond = round((m[0][0] / r0_tot) * 100.0, 1)
            q_cp3 = (f"From the contingency table for {c_title}:\n"
                     f"GIVEN that a selected individual is '{rows[0]}', calculate the conditional probability that they have '{cols[0]}', expressed as a percentage.")
            c_cp3 = f"{p_cond}%"
            d_cp3 = [
                f"{p_joint}%",
                f"{round((m[0][0] / c0_tot) * 100.0, 1)}%",
                f"{round((m[0][1] / r0_tot) * 100.0, 1)}%",
                f"{round(p_cond * 1.15, 1)}%",
                f"{round(p_cond * 0.85, 1)}%",
                f"{round(p_cond + 10.0, 1)}%",
                f"{round(p_cond - 10.0, 1)}%"
            ]
            exp_cp3 = f"P({cols[0]} | {rows[0]}) = Cell count ÷ Row Total = {m[0][0]} ÷ {r0_tot} × 100% = {p_cond}%."
            add_q("Two-Way Contingency Tables", "medium", q_cp3, c_cp3, d_cp3, exp_cp3)

    tree_scenarios = [
        ("Weekend rainfall forecast", "Rain on Saturday", 0.60, "Rain on Sunday", 0.40),
        ("Driver testing exam passes", "Passing Learner's Test", 0.75, "Passing Practical Road Test", 0.60),
        ("Manufacturing quality stages", "Passing Stage 1 Inspection", 0.90, "Passing Stage 2 Inspection", 0.85),
        ("Two consecutive free-throw basketball shots", "Scoring 1st Shot", 0.70, "Scoring 2nd Shot", 0.70),
        ("Traffic light sequence", "Green light at Intersection 1", 0.55, "Green light at Intersection 2", 0.45),
        ("Courier delivery on-time guarantee", "Arriving on time at Sorting Hub", 0.80, "Arriving on time to Customer", 0.75),
        ("Medical diagnostic accuracy tests", "Positive result on Test A", 0.85, "Positive confirmation on Test B", 0.90),
        ("Spelling bee tournament rounds", "Advancing from Round 1", 0.65, "Advancing from Round 2", 0.50),
        ("Solar plant inverter grid sync", "Inverter A Synchronization", 0.92, "Inverter B Synchronization", 0.88),
        ("Hospital backup power failover", "Generator A Automatic Start", 0.95, "ATS Transfer Switch Closure", 0.98)
    ]
    for t_desc, ev1_name, p1_base, ev2_name, p2_base in tree_scenarios:
        for d1 in [-0.10, -0.05, 0.0, 0.05]:
            for d2 in [-0.10, -0.05, 0.0, 0.05]:
                p1 = round(p1_base + d1, 2)
                p2 = round(p2_base + d2, 2)
                p_both = round(p1 * p2, 4)
                p_both_pct = round(p_both * 100.0, 2)
                p_neither = round((1 - p1) * (1 - p2), 4)
                p_neither_pct = round(p_neither * 100.0, 2)
                p_at_least_one = round(1.0 - p_neither, 4)
                p_at_least_one_pct = round(p_at_least_one * 100.0, 2)
                
                q_tr1 = (f"A two-stage tree diagram models {t_desc}. "
                         f"The probability of {ev1_name} is {p1:.2f} ({p1*100:.0f}%), and the independent probability of {ev2_name} is {p2:.2f} ({p2*100:.0f}%). "
                         f"Calculate the probability that BOTH events occur, expressed as a percentage.")
                c_tr1 = f"{p_both_pct}%"
                d_tr1 = [
                    f"{round((p1 + p2) * 100.0, 2)}%",
                    f"{p_neither_pct}%",
                    f"{p_at_least_one_pct}%",
                    f"{round(p_both_pct * 1.25, 2)}%",
                    f"{round(p_both_pct * 0.75, 2)}%",
                    f"{round(p1 * 100.0, 2)}%",
                    f"{round(p2 * 100.0, 2)}%"
                ]
                exp_tr1 = f"P(Both) = P(Event 1) × P(Event 2) = {p1:.2f} × {p2:.2f} = {p_both:.4f} = {p_both_pct}%."
                add_q("Tree Diagrams (Independent & Dependent)", "medium", q_tr1, c_tr1, d_tr1, exp_tr1)

                q_tr2 = (f"Using the tree diagram parameters for {t_desc} (P(Event 1) = {p1:.2f}, P(Event 2) = {p2:.2f}): "
                         f"Determine the probability that AT LEAST ONE of the two events occurs, expressed as a percentage.")
                c_tr2 = f"{p_at_least_one_pct}%"
                d_tr2 = [
                    f"{p_both_pct}%",
                    f"{p_neither_pct}%",
                    f"{round(p_both_pct + p_neither_pct, 2)}%",
                    f"{round(p_at_least_one_pct * 1.10, 2)}%",
                    f"{round(p_at_least_one_pct * 0.90, 2)}%",
                    f"{round(p1 * 100.0, 2)}%",
                    f"{round((p1 + p2)/2.0 * 100.0, 2)}%"
                ]
                exp_tr2 = f"P(At least one) = 1 - P(Neither) = 1 - ((1 - {p1:.2f}) × (1 - {p2:.2f})) = 1 - ({1-p1:.2f} × {1-p2:.2f}) = 1 - {p_neither:.4f} = {p_at_least_one_pct}%."
                add_q("Tree Diagrams (Independent & Dependent)", "medium", q_tr2, c_tr2, d_tr2, exp_tr2)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Relative Frequency vs Theoretical Probability
    trials_cases = [
        ("tossing a coin 600 times", "Heads", 372, 600, 0.50, 
         "The relative frequency (0.62) is substantially higher than the theoretical probability (0.50), indicating the coin is likely biased or loaded."),
        ("rolling a 6-sided die 1,200 times", "Score of 6", 310, 1200, 1/6, 
         "The relative frequency (0.258) significantly exceeds the theoretical probability (0.167), suggesting the die is weighted toward 6."),
        ("spinning a 4-color spinner 800 times", "Green sector", 185, 800, 0.25, 
         "The relative frequency (0.231) is close to the theoretical probability (0.250), confirming normal experimental variance with a fair spinner."),
        ("factory light bulb life testing 2,000 bulbs", "Defective bulbs", 48, 2000, 0.02, 
         "The experimental relative frequency (0.024) matches within allowable 2.5% quality tolerance limits."),
        ("road safety breathalyzer testing of 1,500 motorists", "Over the legal alcohol limit", 105, 1500, 0.05,
         "The relative rate (0.070) exceeds the national target baseline (0.050)."),
        ("quality audit of 2,400 solar panels", "Output efficiency below 90%", 72, 2400, 0.025,
         "The relative defect frequency (0.030) exceeds acceptable factory quality benchmarks."),
        ("seed germination trials with 1,000 maize kernels", "Germinated within 5 days", 840, 1000, 0.85,
         "The observed relative germination rate (0.840) aligns closely with agricultural certified seed standards."),
        ("commercial call centre responsiveness over 5,000 calls", "Answered within 20 seconds", 4250, 5000, 0.80,
         "The observed rate (0.850) outperforms the service level agreement threshold.")
    ]
    for trial_title, outcome_name, obs_base, tot_base, theo_p, interpretation in trials_cases:
        for factor in [1, 2, 3, 4, 5, 6]:
            obs_freq = obs_base * factor
            tot_trials = tot_base * factor
            rel_freq = round(obs_freq / tot_trials, 3)
            
            q_rf = (f"A scientific study investigates {trial_title} (scaled trial {factor}×, total {tot_trials:,} observations). "
                    f"The outcome '{outcome_name}' was recorded exactly {obs_freq:,} times. "
                    f"Calculate the experimental relative frequency of this outcome (as a decimal rounded to 3 decimal places).")
            c_rf = f"{rel_freq:.3f}"
            d_rf = [
                f"{theo_p:.3f}",
                f"{round(obs_freq / (tot_trials - obs_freq), 3):.3f}",
                f"{round(rel_freq * 1.15, 3):.3f}",
                f"{round(rel_freq * 0.85, 3):.3f}",
                f"{round(rel_freq + 0.05, 3):.3f}",
                f"{round(rel_freq - 0.05, 3):.3f}",
                f"{round(1.0 - rel_freq, 3):.3f}"
            ]
            exp_rf = f"Relative Frequency = Observed frequency ÷ Total trials = {obs_freq} ÷ {tot_trials} = {rel_freq:.3f}. {interpretation}"
            add_q("Relative Frequency vs Theoretical Probability", "hard", q_rf, c_rf, d_rf, exp_rf)

    # 3b. Medical Screening Tests (Sensitivity, Specificity & Positive Predictive Value)
    med_scenarios = [
        ("rapid antigen screening of 2,000 workers", 2000, 80, 72, 38),
        ("diabetes clinic screening of 1,500 patients", 1500, 120, 108, 42),
        ("provincial tuberculosis screening of 3,000 community members", 3000, 150, 138, 57),
        ("sports doping screening of 800 athletes", 800, 40, 36, 16),
        ("routine neonatal jaundice screening of 1,200 newborns", 1200, 60, 54, 26),
        ("water reservoir bacterial contamination testing of 2,500 water samples", 2500, 100, 92, 48),
        ("cholesterol diagnostic clinic evaluating 1,800 patients", 1800, 90, 81, 35),
        ("soil pathogen testing across 2,200 agricultural fields", 2200, 110, 99, 44)
    ]
    for med_title, n_pop_base, n_inf_base, tp_base, fp_base in med_scenarios:
        for factor in [1, 2, 3, 4, 5, 6]:
            n_pop = n_pop_base * factor
            n_inf = n_inf_base * factor
            tp = tp_base * factor
            fp = fp_base * factor
            tot_pos_tests = tp + fp
            ppv = round((tp / tot_pos_tests) * 100.0, 2)
            
            q_med = (f"In a public health surveillance programme involving {med_title} (sample size: {n_pop:,}):\n"
                     f"• Exactly {n_inf:,} individuals actually have the condition.\n"
                     f"• The screening test correctly identifies {tp:,} of these infected individuals (True Positives).\n"
                     f"• The test also incorrectly gives positive results to {fp:,} healthy individuals (False Positives).\n"
                     f"Calculate the Positive Predictive Value (probability that a person testing positive actually has the condition), expressed as a percentage. (Round to 2 decimal places).")
            c_med = f"{ppv}%"
            d_med = [
                f"{round((tp / n_inf) * 100.0, 2)}%",
                f"{round((fp / tot_pos_tests) * 100.0, 2)}%",
                f"{round((tot_pos_tests / n_pop) * 100.0, 2)}%",
                f"{round(ppv * 1.15, 2)}%",
                f"{round(ppv * 0.85, 2)}%",
                f"{round(ppv + 8.5, 2)}%",
                f"{round(ppv - 8.5, 2)}%"
            ]
            exp_med = (f"Total Positive Tests = True Positives + False Positives = {tp} + {fp} = {tot_pos_tests}. "
                       f"Positive Predictive Value = True Positives ÷ Total Positive Tests = {tp} ÷ {tot_pos_tests} × 100% = {ppv}%.")
            add_q("Medical Diagnostic Testing & Risk Analysis", "hard", q_med, c_med, d_med, exp_med)

    # 3c. Actuarial Risk Analysis & Expected Value
    risk_scenarios = [
        ("commercial courier delivery fleet", 450000, 0.04, 8500),
        ("agricultural greenhouse crop insurance", 320000, 0.06, 6200),
        ("electronics warehouse transit policy", 600000, 0.03, 11000),
        ("community festival rain cancellation cover", 180000, 0.12, 4500),
        ("heavy mining earthmover equipment warranty", 850000, 0.05, 14000),
        ("solar farm hail damage insurance policy", 520000, 0.035, 9200),
        ("refrigerated perishable goods transport policy", 380000, 0.045, 7800),
        ("coastal storm surge maritime vessel cover", 750000, 0.028, 12500)
    ]
    for r_title, claim_val, prob_claim, admin_fee in risk_scenarios:
        for mult in [0.65, 0.75, 0.85, 0.95, 1.0, 1.10, 1.20, 1.30, 1.40, 1.50]:
            c_val = round(claim_val * mult, 2)
            a_fee = round(admin_fee * mult, 2)
            exp_claim = round(c_val * prob_claim, 2)
            breakeven_prem = round(exp_claim + a_fee, 2)
            
            q_risk = (f"An underwriter calculates policy premiums for {r_title}. "
                      f"The maximum insured value is R{c_val:,.2f}, and statistical analysis indicates a {prob_claim*100:.1f}% probability of a claim occurring during the annual policy term. "
                      f"Fixed administrative costs are R{a_fee:,.2f} per policy. "
                      f"Calculate the minimum annual break-even premium required to cover the expected claim payout and administrative costs.")
            c_risk = f"R{breakeven_prem:,.2f}"
            d_risk = [
                f"R{exp_claim:,.2f}",
                f"R{round(c_val * 0.10, 2):,.2f}",
                f"R{round(breakeven_prem * 1.15, 2):,.2f}",
                f"R{round(breakeven_prem * 0.85, 2):,.2f}",
                f"R{round(breakeven_prem + 1500, 2):,.2f}",
                f"R{round(breakeven_prem - 1500, 2):,.2f}",
                f"R{round(c_val / 12.0, 2):,.2f}"
            ]
            exp_risk = (f"Expected Claim Payout = Insured Value × Probability = R{c_val:,.2f} × {prob_claim} = R{exp_claim:,.2f}. "
                        f"Break-even Premium = Expected Claim + Admin Fee = R{exp_claim:,.2f} + R{a_fee:,.2f} = R{breakeven_prem:,.2f}.")
            add_q("Medical Diagnostic Testing & Risk Analysis", "hard", q_risk, c_risk, d_risk, exp_risk)

    # 3d. Drawing without replacement compound probability
    urn_scenarios = [
        ("quality assurance box of 20 circuit breakers", 20, 5, 2), # total, defective, draw
        ("hospital supply crate of 25 digital thermometers", 25, 4, 2),
        ("bank ATM vault tray of 30 security cash cassettes", 30, 6, 2),
        ("laboratory pack of 24 chemical test vials", 24, 3, 2),
        ("courier depot sack of 28 parcels", 28, 7, 2)
    ]
    for u_title, n_tot, n_def, _ in urn_scenarios:
        for offset in [0, 2, 4, 6]:
            tot = n_tot + offset
            d_cnt = n_def + (offset // 2)
            # P(both defective without replacement) = (d_cnt / tot) * ((d_cnt - 1) / (tot - 1))
            num = d_cnt * (d_cnt - 1)
            den = tot * (tot - 1)
            p_val = round((num / den) * 100.0, 2)
            
            q_urn = (f"An inspector examines a {u_title} (total {tot} items, of which exactly {d_cnt} are non-compliant). "
                     f"If 2 items are selected at random ONE AFTER THE OTHER WITHOUT REPLACEMENT: "
                     f"Calculate the probability that BOTH selected items are non-compliant, expressed as a percentage. (Round to 2 decimal places).")
            c_urn = f"{p_val}%"
            d_urn = [
                f"{round(((d_cnt / tot) ** 2) * 100.0, 2)}%",
                f"{round((d_cnt / tot) * 100.0, 2)}%",
                f"{round(((d_cnt - 1) / (tot - 1)) * 100.0, 2)}%",
                f"{round(p_val * 1.25, 2)}%",
                f"{round(p_val * 0.75, 2)}%",
                f"{round(p_val + 3.5, 2)}%",
                f"{round(p_val - 3.5 if p_val > 4 else p_val + 1.5, 2)}%"
            ]
            exp_urn = (f"P(Both Non-compliant) = P(1st Non-compliant) × P(2nd Non-compliant | 1st Non-compliant) "
                       f"= ({d_cnt}/{tot}) × ({d_cnt - 1}/{tot - 1}) = {num}/{den} ≈ {p_val}%.")
            add_q("Tree Diagrams (Independent & Dependent)", "hard", q_urn, c_urn, d_urn, exp_urn)

            # Also add P(Neither is non-compliant) and P(At least one is non-compliant)
            c_cnt = tot - d_cnt
            num_neither = c_cnt * (c_cnt - 1)
            p_neither = round((num_neither / den) * 100.0, 2)
            p_at_least_one = round(100.0 - p_neither, 2)
            q_at_least = (f"Continuing with the {u_title} ({tot} total items, {d_cnt} non-compliant): "
                          f"If 2 items are selected at random without replacement, calculate the probability that AT LEAST ONE of the selected items is non-compliant, expressed as a percentage.")
            c_at_least = f"{p_at_least_one}%"
            d_at_least = [
                f"{p_val}%",
                f"{p_neither}%",
                f"{round(p_at_least_one * 1.15, 2)}%",
                f"{round(p_at_least_one * 0.85, 2)}%",
                f"{round(p_at_least_one + 5.5, 2)}%",
                f"{round(p_at_least_one - 5.5, 2)}%",
                f"{round((d_cnt / tot) * 100.0, 2)}%"
            ]
            exp_at_least = (f"P(Neither is non-compliant) = ({c_cnt}/{tot}) × ({c_cnt-1}/{tot-1}) = {num_neither}/{den} ≈ {p_neither}%. "
                            f"P(At least one non-compliant) = 100% - P(Neither) = 100% - {p_neither}% = {p_at_least_one}%.")
            add_q("Tree Diagrams (Independent & Dependent)", "hard", q_at_least, c_at_least, d_at_least, exp_at_least)

    print(f"Generated Paper 1 Probability: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/mathematical_literacy"
    out_file = os.path.join(out_dir, "paper1_mathlit12_probability.json")
    dataset = build_probability_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()

# Additional Hard Questions: P(At least one non-compliant) in sampling without replacement
def patch_hard(gen_func):
    pass
