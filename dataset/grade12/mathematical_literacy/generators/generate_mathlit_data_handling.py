import json
import os
import random
import time

def build_data_handling_dataset():
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
        q_id = f"ML12_P1_DATA_{len(questions) + 1:04d}"
        
        questions.append({
            "id": q_id,
            "topic": "Data Handling",
            "subtopic": subtopic,
            "paper": "paper1",
            "difficulty": difficulty,
            "question": q_text,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_dist[:8],
            "explanation": explanation
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    # 1a. Statistical Definitions
    definitions = [
        ("Discrete data", "Numerical data that can only take specific, distinct values obtained by counting.",
         ["Numerical data that can take any value within a continuous range obtained by measurement.", "Qualitative data that describes qualities or characteristics using words.", "Data that has been grouped into intervals or classes.", "Data that contains extreme values called outliers.", "Data collected from an entire population rather than a sample.", "Data displayed exclusively using a broken-line graph."]),
        ("Continuous data", "Numerical data that can take any value within a given measurement range obtained by measuring.",
         ["Data that consists of whole numbers obtained solely by counting.", "Categorical data that has no inherent numerical meaning.", "Data that remains constant and never changes over time.", "Data that has exactly two modes in a distribution.", "Data gathered exclusively through multiple-choice questionnaires.", "Data that does not have an upper quartile or median."]),
        ("Mean", "The arithmetic average of a dataset, calculated by dividing the sum of all values by the total number of values.",
         ["The middle value in a dataset when the values are arranged in ascending order.", "The most frequently occurring value in a data distribution.", "The difference between the maximum and minimum values.", "The value separating the lowest 25% of data from the rest.", "The middle 50% spread between the first and third quartiles.", "The point where the cumulative frequency curve reaches 100%."]),
        ("Median", "The middle value in an ordered dataset that divides the data into two equal halves (50% below and 50% above).",
         ["The sum of all values divided by the total number of observations.", "The value that appears most often in a sample.", "The difference between the third quartile and the first quartile.", "The average of the highest and lowest scores.", "The value that lies 1.5 times the IQR above the third quartile.", "The total frequency of all observations combined."]),
        ("Mode", "The value or category that appears most frequently in a given dataset.",
         ["The middle score when data is sorted in ascending numerical order.", "The average calculated by summing all observations and dividing by n.", "The difference between the maximum and minimum values in the dataset.", "The value located at the 75th percentile of the distribution.", "The spread of scores around the central arithmetic mean.", "The value that occurs exactly once in a distribution."]),
        ("Range", "The difference between the maximum (highest) and minimum (lowest) values in a dataset.",
         ["The difference between the third quartile and the first quartile.", "The average distance of all observations from the mean.", "The square root of the variance of the data distribution.", "The middle value dividing the data into two equal halves.", "The ratio of the highest value to the lowest value.", "The total number of observations recorded in a survey."]),
        ("Outlier", "An extreme data value that lies significantly far away from the overall pattern of the rest of the dataset.",
         ["The exact midpoint between the upper and lower quartiles.", "The most frequently recurring observation in a data sample.", "A data point that equals the arithmetic mean of the distribution.", "The value representing the 50th percentile in a box plot.", "A missing data value caused by measurement error.", "The interval with the highest frequency in a grouped histogram."]),
        ("Bimodal distribution", "A dataset that has two distinct modes (two values that share the highest frequency).",
         ["A distribution that has no mode whatsoever.", "A dataset where all values appear with identical frequency.", "A distribution with two medians and two means.", "A dataset that is split into two halves by the first quartile.", "A distribution that contains two severe outliers.", "A graphical representation that uses two vertical axes."])
    ]
    for term, c_def, w_defs in definitions:
        q = f"In Mathematical Literacy data handling, define the term '{term}'."
        add_q("Statistical Terminology", "easy", q, c_def, w_defs, f"Official CAPS definition: {term} is defined as: {c_def}")

    # 1b. Direct Calculations of Mean, Median, Mode, Range on Authentic SA Contexts
    contexts = [
        ("NSC trial examination marks (%) of 9 Grade 12 learners", [54, 62, 68, 71, 74, 78, 82, 85, 90]),
        ("monthly rainfall (mm) recorded in Durban over 7 consecutive months", [45, 52, 60, 68, 85, 110, 120]),
        ("daily maximum temperatures (°C) in Polokwane over 8 days", [22, 24, 25, 26, 28, 30, 31, 34]),
        ("fuel prices (cents per litre) in Gauteng across 6 price adjustments", [2140, 2185, 2230, 2290, 2350, 2410]),
        ("points scored by a provincial netball team in 9 league matches", [38, 42, 45, 48, 50, 52, 55, 60, 64]),
        ("waiting times (minutes) of 7 patients at a community health clinic", [15, 22, 28, 35, 42, 50, 65]),
        ("daily bread loaves delivered to a local spaza shop over 8 days", [35, 40, 42, 45, 48, 50, 52, 60]),
        ("weekly egg production (trays) on a small poultry farm over 7 weeks", [120, 135, 140, 145, 150, 158, 172]),
        ("number of absentee learners per day at an Umlazi high school over 9 days", [12, 14, 15, 17, 18, 20, 22, 25, 30]),
        ("daily litres of milk yielded by a dairy herd over 8 days", [420, 435, 440, 455, 460, 475, 480, 500]),
        ("monthly water consumption (kℓ) of a household in Mangaung over 7 months", [16, 18, 19, 21, 24, 28, 32]),
        ("speed camera readings (km/h) recorded on the N1 north over 9 vehicles", [102, 108, 112, 115, 118, 120, 124, 128, 135])
    ]
    
    for ctx_title, base_vals in contexts:
        for offset in [-12, -8, -4, 0, 4, 8, 12, 16]:
            vals = [v + offset for v in base_vals]
            n = len(vals)
            s = sum(vals)
            mean_v = round(s / n, 1)
            sorted_v = sorted(vals)
            med_v = sorted_v[n // 2] if n % 2 == 1 else round((sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2.0, 1)
            min_v = sorted_v[0]
            max_v = sorted_v[-1]
            range_v = max_v - min_v
            
            # Mean question
            q_mean = f"The following dataset represents the {ctx_title}:\n{', '.join(map(str, vals))}\nCalculate the arithmetic mean of this dataset. (Round to 1 decimal place if applicable)."
            c_mean = str(mean_v)
            d_mean = [
                str(med_v),
                str(range_v),
                str(round(mean_v + 3.2, 1)),
                str(round(mean_v - 3.2, 1)),
                str(round(s / (n - 1), 1)),
                str(round(s / (n + 1), 1)),
                str(round(mean_v * 1.15, 1))
            ]
            exp_mean = f"Mean = Sum of values ÷ Number of values = {s} ÷ {n} = {mean_v}."
            add_q("Measures of Central Tendency", "easy", q_mean, c_mean, d_mean, exp_mean)
            
            # Median question
            q_med = f"Determine the median value for the {ctx_title}:\n{', '.join(map(str, vals))}"
            c_med = str(med_v)
            d_med = [
                str(mean_v),
                str(range_v),
                str(min_v),
                str(max_v),
                str(sorted_v[1]),
                str(sorted_v[-2]),
                str(round(med_v + 5.0, 1))
            ]
            exp_med = f"Arranging data in ascending order: {', '.join(map(str, sorted_v))}. The median (middle value) is {med_v}."
            add_q("Measures of Central Tendency", "easy", q_med, c_med, d_med, exp_med)
            
            # Range question
            q_rng = f"Calculate the range of the dataset representing the {ctx_title}:\n{', '.join(map(str, vals))}"
            c_rng = str(range_v)
            d_rng = [
                str(max_v),
                str(min_v),
                str(med_v),
                str(mean_v),
                str(range_v + 10),
                str(range_v - 10 if range_v > 10 else range_v + 5),
                str(round(range_v / 2.0, 1))
            ]
            exp_rng = f"Range = Maximum value - Minimum value = {max_v} - {min_v} = {range_v}."
            add_q("Measures of Spread", "easy", q_rng, c_rng, d_rng, exp_rng)

    # 1c. Simple Mode Identification & Percentages (easy)
    for i in range(120):
        if counts["easy"] >= target_easy:
            break
        repeated = random.randint(45, 85)
        others = [random.randint(40, 90) for _ in range(6)]
        raw = [repeated, repeated, repeated] + others
        random.shuffle(raw)
        q_mode = f"A sample of learner test marks is recorded as follows:\n{', '.join(map(str, raw))}\nIdentify the mode of this dataset."
        c_mode = str(repeated)
        d_mode = [str(x) for x in set(others) if x != repeated][:6]
        while len(d_mode) < 6:
            val = str(random.randint(35, 95))
            if val != c_mode and val not in d_mode:
                d_mode.append(val)
        d_mode.append("No mode exists")
        exp_mode = f"The mode is the value appearing most frequently. The value {repeated} appears 3 times, so the mode is {repeated}."
        add_q("Measures of Central Tendency", "easy", q_mode, c_mode, d_mode, exp_mode)

    while counts["easy"] < target_easy:
        tot = random.choice([200, 250, 400, 500, 800])
        part = random.randint(30, tot // 2)
        pct = round((part / tot) * 100.0, 1)
        q_p = f"Out of {tot} candidates who wrote a National Senior Certificate driver's test, {part} passed on their first attempt. Calculate the percentage pass rate."
        c_p = f"{pct}%"
        d_p = [
            f"{round(100 - pct, 1)}%",
            f"{round(pct * 1.15, 1)}%",
            f"{round(pct * 0.85, 1)}%",
            f"{round(part / 10.0, 1)}%",
            f"{round(pct + 10.0, 1)}%",
            f"{round(pct - 10.0, 1)}%",
            f"{round(tot / part, 1)}%"
        ]
        exp_p = f"Percentage = ({part} ÷ {tot}) × 100% = {pct}%."
        add_q("Measures of Central Tendency", "easy", q_p, c_p, d_p, exp_p)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    data_scenarios = [
        ("Mathematics Paper 1 trial exam scores (%) of 11 learners", [42, 48, 52, 56, 60, 64, 70, 74, 80, 84, 92]),
        ("daily customer counts at a community pharmacy over 13 weekdays", [112, 120, 125, 130, 134, 140, 145, 152, 158, 164, 170, 178, 185]),
        ("weekly diesel consumption (litres) of a delivery bakkie over 11 weeks", [65, 70, 74, 78, 82, 85, 90, 94, 98, 104, 112]),
        ("mass (kg) of 13 Grade 12 rugby squad players", [78, 82, 85, 88, 92, 95, 98, 102, 105, 110, 114, 118, 124]),
        ("monthly electricity charges (Rands) of 11 households in an apartment block", [680, 740, 810, 860, 920, 980, 1050, 1120, 1200, 1310, 1450]),
        ("waiting times (minutes) at a municipal licensing department for 13 applicants", [25, 32, 38, 44, 50, 56, 62, 70, 78, 85, 92, 104, 118]),
        ("daily sales (Rands) of a mobile car wash over 11 weekend days", [1400, 1550, 1680, 1800, 1950, 2100, 2300, 2450, 2600, 2800, 3100]),
        ("running times (seconds) of 13 athletes in the 400m race", [52, 54, 55, 57, 58, 60, 61, 63, 65, 66, 68, 71, 74])
    ]
    
    for ctx_name, base_arr in data_scenarios:
        for delta in [-15, -10, -5, 0, 5, 10, 15, 20]:
            arr = sorted([x + delta for x in base_arr])
            n = len(arr)
            min_v = arr[0]
            max_v = arr[-1]
            med_idx = n // 2
            med_v = arr[med_idx]
            
            lower_half = arr[:med_idx]
            upper_half = arr[med_idx+1:]
            
            q1_v = lower_half[len(lower_half)//2] if len(lower_half)%2 == 1 else round((lower_half[len(lower_half)//2 - 1] + lower_half[len(lower_half)//2])/2.0, 1)
            q3_v = upper_half[len(upper_half)//2] if len(upper_half)%2 == 1 else round((upper_half[len(upper_half)//2 - 1] + upper_half[len(upper_half)//2])/2.0, 1)
            iqr_v = round(q3_v - q1_v, 1)
            semi_iqr = round(iqr_v / 2.0, 2)
            
            # Q1 Question: Calculate Q1
            q_q1 = (f"The ordered dataset below represents the {ctx_name}:\n"
                    f"{', '.join(map(str, arr))}\n"
                    f"Determine the first quartile (Q₁) for this dataset.")
            c_q1 = str(q1_v)
            d_q1 = [
                str(med_v),
                str(q3_v),
                str(min_v),
                str(round(q1_v + 4.0, 1)),
                str(round(q1_v - 4.0, 1)),
                str(iqr_v),
                str(semi_iqr)
            ]
            exp_q1 = f"Lower half of data: {', '.join(map(str, lower_half))}. The median of the lower half gives Q₁ = {q1_v}."
            add_q("Five-Number Summary & Quartiles", "medium", q_q1, c_q1, d_q1, exp_q1)
            
            # Q3 Question: Calculate Q3
            q_q3 = (f"The ordered dataset below represents the {ctx_name}:\n"
                    f"{', '.join(map(str, arr))}\n"
                    f"Determine the third quartile (Q₃) for this dataset.")
            c_q3 = str(q3_v)
            d_q3 = [
                str(med_v),
                str(q1_v),
                str(max_v),
                str(round(q3_v + 5.0, 1)),
                str(round(q3_v - 5.0, 1)),
                str(iqr_v),
                str(arr[-2])
            ]
            exp_q3 = f"Upper half of data: {', '.join(map(str, upper_half))}. The median of the upper half gives Q₃ = {q3_v}."
            add_q("Five-Number Summary & Quartiles", "medium", q_q3, c_q3, d_q3, exp_q3)
            
            # IQR Question
            q_iqr = (f"Using the quartiles determined from the dataset for the {ctx_name} (where Q₁ = {q1_v} and Q₃ = {q3_v}): "
                     f"Calculate the Interquartile Range (IQR).")
            c_iqr = str(iqr_v)
            d_iqr = [
                str(round(max_v - min_v, 1)),
                str(semi_iqr),
                str(round(q3_v + q1_v, 1)),
                str(round(iqr_v + 4.0, 1)),
                str(round(iqr_v - 4.0, 1)),
                str(med_v),
                str(round(iqr_v * 1.15, 1))
            ]
            exp_iqr = f"IQR = Q₃ - Q₁ = {q3_v} - {q1_v} = {iqr_v}."
            add_q("Five-Number Summary & Quartiles", "medium", q_iqr, c_iqr, d_iqr, exp_iqr)

            # Outlier Thresholds Question
            lower_fence = round(q1_v - 1.5 * iqr_v, 1)
            upper_fence = round(q3_v + 1.5 * iqr_v, 1)
            q_fence = (f"For the dataset representing the {ctx_name} (Q₁ = {q1_v}, Q₃ = {q3_v}, IQR = {iqr_v}): "
                       f"Calculate the upper outlier boundary (upper fence) using the standard formula: Q₃ + (1.5 × IQR).")
            c_fence = str(upper_fence)
            d_fence = [
                str(lower_fence),
                str(round(q3_v + iqr_v, 1)),
                str(round(q3_v + 2.0 * iqr_v, 1)),
                str(round(upper_fence + 5.0, 1)),
                str(round(upper_fence - 5.0, 1)),
                str(max_v),
                str(round(q1_v + 1.5 * iqr_v, 1))
            ]
            exp_fence = f"Upper Outlier Boundary = Q₃ + (1.5 × IQR) = {q3_v} + (1.5 × {iqr_v}) = {q3_v} + {1.5 * iqr_v:.1f} = {upper_fence}."
            add_q("Outliers & Skewness", "medium", q_fence, c_fence, d_fence, exp_fence)

    # 2b. Box-and-Whisker Plot Interpretations & Skewness (medium)
    box_plots = [
        ("Midyear accounting exam marks", 28, 45, 62, 75, 96),
        ("Physical Sciences practical scores", 34, 52, 68, 80, 98),
        ("Daily hospital triage emergency waiting times (min)", 15, 30, 48, 70, 120),
        ("Monthly household water consumption (kℓ)", 8, 14, 22, 32, 54),
        ("Ages of registered blood donors at a community clinic", 18, 24, 32, 46, 68),
        ("Daily revenue (Rands hundreds) of a local car wash", 12, 18, 25, 36, 50)
    ]
    for title, b_min, b_q1, b_med, b_q3, b_max in box_plots:
        left_dist = b_med - b_min
        right_dist = b_max - b_med
        skew = "Positively skewed (skewed to the right)" if right_dist > left_dist else "Negatively skewed (skewed to the left)" if left_dist > right_dist else "Symmetrical"
        reason = f"the right whisker/tail ({right_dist}) is longer than the left whisker/tail ({left_dist})" if right_dist > left_dist else f"the left whisker/tail ({left_dist}) is longer than the right whisker/tail ({right_dist})"
        
        q_skew = (f"A box-and-whisker plot summarizing {title} has the following five-number summary:\n"
                  f"Minimum = {b_min}, Q₁ = {b_q1}, Median = {b_med}, Q₃ = {b_q3}, Maximum = {b_max}.\n"
                  f"Describe the skewness (shape of distribution) of this data.")
        c_skew = skew
        d_skew = [
            "Positively skewed (skewed to the right)" if "Negatively" in skew else "Negatively skewed (skewed to the left)",
            "Perfect symmetrical bell-shaped normal distribution",
            "Uniform distribution with equal frequencies across all intervals",
            "Bimodal distribution with two distinct peaks",
            "Skewness cannot be determined from a five-number summary",
            "Inverted U-shaped distribution"
        ]
        exp_skew = f"Comparing the distances from the median: Right side = Max - Median = {b_max} - {b_med} = {right_dist}. Left side = Median - Min = {b_med} - {b_min} = {left_dist}. Since {reason}, the distribution is {skew}."
        add_q("Outliers & Skewness", "medium", q_skew, c_skew, d_skew, exp_skew)

        q_pct = (f"In the box-and-whisker plot for {title} (Min = {b_min}, Q₁ = {b_q1}, Median = {b_med}, Q₃ = {b_q3}, Max = {b_max}): "
                 f"What percentage of the data lies between the first quartile (Q₁ = {b_q1}) and the third quartile (Q₃ = {b_q3})?")
        c_pct = "50%"
        d_pct = ["25%", "75%", "100%", "30%", "68%", "95%", "15%"]
        exp_pct = "By definition of quartiles in a box-and-whisker plot, exactly 50% of the dataset lies within the interquartile range (between Q₁ and Q₃)."
        add_q("Five-Number Summary & Box-and-Whisker Plots", "medium", q_pct, c_pct, d_pct, exp_pct)

    # 2c. Pie Chart Sector Angle Calculations
    categories = [
        ("municipal budget expenditure", [("Water infrastructure", 35), ("Electricity maintenance", 25), ("Road works", 20), ("Waste management", 12), ("Administration", 8)]),
        ("transport modes used by 1,200 commuters", [("Taxis", 540), ("Buses", 300), ("Trains", 180), ("Private cars", 120), ("Walking/Cycling", 60)]),
        ("Grade 12 matric subject distinctions", [("Mathematical Literacy", 150), ("Life Sciences", 120), ("Geography", 90), ("History", 60), ("Business Studies", 80)])
    ]
    for ctx_lbl, items in categories:
        tot_freq = sum(val for _, val in items)
        for cat_name, val in items:
            ang = round((val / tot_freq) * 360.0, 1)
            pct = round((val / tot_freq) * 100.0, 1)
            q_ang = (f"In a survey of {ctx_lbl} (Total = {tot_freq:,}):\n"
                     f"The '{cat_name}' category accounts for {val:,} of the total. "
                     f"Calculate the size of the sector angle (in degrees) representing '{cat_name}' on a pie chart. (Round to 1 decimal place).")
            c_ang = f"{ang}°"
            d_ang = [
                f"{pct}°",
                f"{round(ang + 15.0, 1)}°",
                f"{round(ang - 15.0, 1)}°",
                f"{round(ang * 1.15, 1)}°",
                f"{round(ang * 0.85, 1)}°",
                f"{round((val / tot_freq) * 180.0, 1)}°",
                f"{round(ang + 30.0, 1)}°"
            ]
            exp_ang = f"Sector Angle = (Category Value ÷ Total Value) × 360° = ({val} ÷ {tot_freq}) × 360° = {ang}°."
            add_q("Pie Charts & Frequency Polygons", "medium", q_ang, c_ang, d_ang, exp_ang)

    # Fill remaining medium
    while counts["medium"] < target_med:
        arr_rand = sorted([random.randint(30, 95) for _ in range(9)])
        med_rand = arr_rand[4]
        q1_rand = (arr_rand[1] + arr_rand[2]) / 2.0
        q3_rand = (arr_rand[6] + arr_rand[7]) / 2.0
        iqr_rand = round(q3_rand - q1_rand, 1)
        q_fill_m = f"Given the ordered dataset of 9 learner marks: {', '.join(map(str, arr_rand))}. Calculate the Interquartile Range (IQR)."
        c_fill_m = str(iqr_rand)
        d_fill_m = [
            str(arr_rand[-1] - arr_rand[0]),
            str(med_rand),
            str(round(iqr_rand / 2.0, 1)),
            str(round(iqr_rand + 5.0, 1)),
            str(round(iqr_rand - 5.0, 1)),
            str(round(q1_rand, 1)),
            str(round(q3_rand, 1))
        ]
        exp_fill_m = f"Q₁ = {q1_rand}, Q₃ = {q3_rand}. IQR = Q₃ - Q₁ = {q3_rand} - {q1_rand} = {iqr_rand}."
        add_q("Five-Number Summary & Quartiles", "medium", q_fill_m, c_fill_m, d_fill_m, exp_fill_m)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    scatter_contexts = [
        ("weekly hours of study (x) versus NSC Trial Accounting score % (y)", "y = 4.2x + 32.5", 4.2, 32.5, "Strong positive linear correlation", 
         "As study hours increase, trial exam marks consistently increase.", [8, 12, 15, 20]),
        ("vehicle age in years (x) versus trade-in value in Rands thousands (y)", "y = -18.5x + 240.0", -18.5, 240.0, "Strong negative linear correlation", 
         "As the age of the vehicle increases, the market resale value consistently decreases.", [3, 5, 7, 9]),
        ("average daily ambient temperature °C (x) versus air conditioning electricity units kWh (y)", "y = 1.85x - 12.0", 1.85, -12.0, "Moderate positive linear correlation", 
         "Higher daily temperatures correspond to increased electricity usage for air conditioning.", [24, 28, 32, 36]),
        ("number of practice exam papers completed (x) versus final examination errors (y)", "y = -2.4x + 45.0", -2.4, 45.0, "Strong negative linear correlation", 
         "Completing more practice papers is associated with fewer errors on the final examination.", [5, 8, 10, 14])
    ]
    for s_title, eq_str, slope, intercept, corr_type, interpretation, x_vals in scatter_contexts:
        q_corr = (f"A researcher analyzes a scatter plot comparing {s_title}. "
                  f"The data points cluster tightly along a line described by the trend equation: {eq_str}. "
                  f"Classify the type and direction of correlation represented by this scatter plot.")
        c_corr = corr_type
        d_corr = [
            "Strong negative linear correlation" if "positive" in corr_type else "Strong positive linear correlation",
            "Zero / No correlation (random scatter of points)",
            "Moderate negative nonlinear parabolic correlation",
            "Weak positive curvilinear correlation",
            "Independent categorical relationship",
            "Bimodal inverse correlation"
        ]
        exp_corr = f"The slope of the line is {slope} ({'positive' if slope > 0 else 'negative'}). Because the points cluster tightly, there is a {corr_type}. {interpretation}"
        add_q("Scatter Plots & Correlation Analysis", "hard", q_corr, c_corr, d_corr, exp_corr)

        for x_in in x_vals:
            y_pred = round(slope * x_in + intercept, 1)
            q_pred = (f"Using the trend line equation {eq_str} for {s_title}: "
                      f"Predict the expected value of y when x = {x_in}. (Round to 1 decimal place).")
            c_pred = str(y_pred)
            d_pred = [
                str(round(slope * x_in, 1)),
                str(round(intercept + x_in, 1)),
                str(round(y_pred + 6.5, 1)),
                str(round(y_pred - 6.5, 1)),
                str(round(y_pred * 1.15, 1)),
                str(round(y_pred * 0.85, 1)),
                str(round(slope + intercept, 1))
            ]
            exp_pred = f"Substitute x = {x_in} into the trend equation: y = {slope}({x_in}) + ({intercept}) = {slope * x_in:.1f} + ({intercept}) = {y_pred}."
            add_q("Scatter Plots & Correlation Analysis", "hard", q_pred, c_pred, d_pred, exp_pred)

    misleading_cases = [
        ("A provincial health department publishes a bar graph showing clinic patient satisfaction rising from 82% in 2022 to 86% in 2023. However, the vertical axis begins at 80% rather than 0%.",
         "The truncated vertical axis exaggerates the visual difference, making a modest 4% increase look like satisfaction tripled.",
         ["The graph is completely accurate and presents no visual distortion.", "The horizontal axis intervals are spaced too widely.", "The bar graph should have been plotted as a pie chart instead.", "A 4% increase is statistically insignificant and cannot be plotted.", "The bars are colored differently which violates CAPS standards.", "The sample size is omitted from the title."]),
        ("A media article displays a 3D perspective pie chart of youth unemployment by province. The Eastern Cape slice is positioned in the foreground tilted toward the viewer.",
         "The 3D perspective creates distortion where slices at the front appear visually larger than their actual percentage values.",
         ["Pie charts cannot represent employment data under any circumstances.", "The sum of the percentages in 3D pie charts always exceeds 100%.", "The Eastern Cape has the smallest land area among provinces.", "3D charts can only be used for continuous physical measurements.", "The colors used in the 3D projection lack sufficient contrast.", "The font size of the category labels is too small."]),
        ("A school newsletter compares matric pass rates over 5 years. The gaps between years on the horizontal axis are: 2018, 2019, 2020, 2023 (omitting 2021 and 2022 without indication).",
         "The irregular horizontal timeline conceals data from the missing pandemic years, giving a false impression of consistent year-on-year improvement.",
         ["The line graph should always use a vertical logarithmic scale.", "Pass rates cannot be measured as percentages over consecutive years.", "School newsletters are legally prohibited from publishing pass rates.", "The vertical axis has too many gridlines.", "The line graph fails to display the median score of the school.", "Matric results can only be displayed using stacked bar charts."]),
        ("A company advertises that its sales grew by R5 million while a competitor only grew by R2 million, failing to mention that the company's total revenue is R500 million (1% growth) while the competitor's is R10 million (20% growth).",
         "Reporting only absolute monetary growth without relative percentage growth misleads consumers about actual performance and business momentum.",
         ["Absolute monetary figures are never allowed in South African business reports.", "The competitor should have paid a commercial advertising fine.", "A company cannot grow by more than 5% in a single financial year.", "Fixed costs were not deducted from the sales revenue figures.", "The graph failed to adjust for municipal water tariffs.", "The company used a double-entry bookkeeping error."])
    ]
    for scenario_text, correct_critique, wrong_critiques in misleading_cases:
        q_crit = f"Critically evaluate the following data presentation from a media report:\n'{scenario_text}'\nExplain why this graph or statement is statistically misleading."
        add_q("Critiquing Misleading Graphs & Media Reports", "hard", q_crit, correct_critique, wrong_critiques, f"Critical evaluation: {correct_critique}")

    while counts["hard"] < target_hard:
        x_val = random.randint(10, 45)
        m_val = round(random.uniform(1.5, 4.5), 1)
        c_val = round(random.uniform(15.0, 35.0), 1)
        y_val = round(m_val * x_val + c_val, 1)
        q_fill_h = f"In an environmental study, river water acidity (y) is modeled against industrial distance (x km) by the regression line y = {m_val}x + {c_val}. Calculate the predicted acidity when x = {x_val} km."
        c_fill_h = str(y_val)
        d_fill_h = [
            str(round(m_val * x_val, 1)),
            str(round(c_val + x_val, 1)),
            str(round(y_val + 5.2, 1)),
            str(round(y_val - 5.2, 1)),
            str(round(y_val * 1.12, 1)),
            str(round(y_val * 0.88, 1)),
            str(round(m_val + c_val, 1))
        ]
        exp_fill_h = f"Substitute x = {x_val}: y = ({m_val} × {x_val}) + {c_val} = {m_val * x_val:.1f} + {c_val} = {y_val}."
        add_q("Scatter Plots & Correlation Analysis", "hard", q_fill_h, c_fill_h, d_fill_h, exp_fill_h)

    print(f"Generated Data Handling: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/mathematical_literacy"
    out_file = os.path.join(out_dir, "paper1_mathlit12_data_handling.json")
    dataset = build_data_handling_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
