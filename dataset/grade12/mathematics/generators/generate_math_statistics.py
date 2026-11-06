import json
import random
import os
import time
import math
import statistics

def generate_math_statistics():
    print("Generating Grade 12 Mathematics: Statistics & Regression...")
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
        q_id = f"MATH_P2_STAT_{len(questions)+1:04d}"
        questions.append({
            "id": q_id,
            "topic": "Statistics",
            "question": q_text,
            "correct_answer": correct,
            "wrong_answers_pool": clean_wrongs[:8],
            "explanation": explanation.strip(),
            "difficulty": difficulty,
            "tags": {
                "grade": "12",
                "subject": "Mathematics",
                "topic": "Statistics",
                "subtopic": subtopic,
                "cognitive_level": cognitive,
                "difficulty": difficulty
            }
        })
        return True

    def get_w_ints(val, count=8):
        w = set()
        for delta in [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -10, 10]:
            if val + delta != val:
                w.add(str(val + delta))
        cand_list = list(w)
        while len(cand_list) < count:
            extra = val + random.randint(11, 40) * random.choice([1, -1])
            if extra != val and str(extra) not in cand_list:
                cand_list.append(str(extra))
        return cand_list[:count]

    def get_w_floats(val, decimals=2, count=8):
        w = set()
        for delta in [-0.5, 0.5, -0.2, 0.2, -1.0, 1.0, -0.15, 0.15, -0.05, 0.05]:
            cand = round(val + delta, decimals)
            if cand != val:
                w.add(f"{cand:.{decimals}f}")
        cand_list = list(w)
        while len(cand_list) < count:
            extra = round(val + random.uniform(-5.0, 5.0), decimals)
            s_cand = f"{extra:.{decimals}f}"
            if extra != val and s_cand not in cand_list:
                cand_list.append(s_cand)
        return cand_list[:count]

    # ====================================================
    # EASY QUESTIONS (Target: 300)
    # ====================================================
    easy_count = 0

    # 1. Interpretation of correlation coefficient r (60)
    studies = [
        ("study hours", "examination marks"),
        ("daily temperature", "ice cream sales"),
        ("vehicle speed", "braking distance"),
        ("rainfall amount", "crop yield"),
        ("age of second-hand car", "resale value"),
        ("altitude", "atmospheric pressure"),
        ("weekly exercise hours", "resting heart rate"),
        ("monthly advertising expenditure", "sales revenue")
    ]
    while easy_count < 60:
        var1, var2 = random.choice(studies)
        r_val = round(random.uniform(-0.98, 0.98), 2)
        if abs(r_val) < 0.05:
            ans = "Virtually no linear correlation"
            exp = f"Since $r = {r_val:.2f}$ is extremely close to $0$, there is virtually no linear relationship."
        elif r_val >= 0.75:
            ans = "Strong positive linear correlation"
            exp = f"Since $r = {r_val:.2f}$ is close to $1$, there is a strong positive linear correlation."
        elif 0.40 <= r_val < 0.75:
            ans = "Moderate positive linear correlation"
            exp = f"Since $r = {r_val:.2f}$ is moderately positive, there is a moderate positive linear correlation."
        elif 0.05 <= r_val < 0.40:
            ans = "Weak positive linear correlation"
            exp = f"Since $r = {r_val:.2f}$ is positive but near $0$, there is a weak positive linear correlation."
        elif r_val <= -0.75:
            ans = "Strong negative linear correlation"
            exp = f"Since $r = {r_val:.2f}$ is close to $-1$, there is a strong negative linear correlation."
        elif -0.75 < r_val <= -0.40:
            ans = "Moderate negative linear correlation"
            exp = f"Since $r = {r_val:.2f}$ is moderately negative, there is a moderate negative linear correlation."
        else:
            ans = "Weak negative linear correlation"
            exp = f"Since $r = {r_val:.2f}$ is negative but near $0$, there is a weak negative linear correlation."

        all_r_opts = [
            "Strong positive linear correlation", "Moderate positive linear correlation", "Weak positive linear correlation",
            "Strong negative linear correlation", "Moderate negative linear correlation", "Weak negative linear correlation",
            "Virtually no linear correlation", "Perfect quadratic correlation"
        ]
        wrongs = [opt for opt in all_r_opts if opt != ans]
        q = f"A statistical study investigating the relationship between {var1} and {var2} yielded a correlation coefficient of $r = {r_val:.2f}$. Which best describes this relationship?"
        if add_q("easy", "Correlation", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 2. Skewness from Mean vs Median (60)
    groups = ["Grade 12 Mathematics test", "Physical Sciences quiz", "Accounting exam", "Life Sciences trial", "English essay assessment"]
    while easy_count < 120:
        grp = random.choice(groups)
        mean_v = random.randint(40, 80)
        diff = random.choice([-15, -12, -9, -7, 0, 7, 9, 12, 15])
        med_v = mean_v + diff
        if diff > 3:
            ans = "Negatively skewed (skewed to the left)"
            exp = f"Because the mean (${mean_v}$) is less than the median (${med_v}$), the distribution has a longer tail to the left, which is negatively skewed."
        elif diff < -3:
            ans = "Positively skewed (skewed to the right)"
            exp = f"Because the mean (${mean_v}$) is greater than the median (${med_v}$), the distribution has a longer tail to the right, which is positively skewed."
        else:
            ans = "Approximately symmetrical"
            exp = f"Because the mean (${mean_v}$) is approximately equal to the median (${med_v}$), the distribution is approximately symmetrical."

        wrongs = [
            "Positively skewed (skewed to the right)", "Negatively skewed (skewed to the left)",
            "Approximately symmetrical", "Bimodal with two equal peaks", "Uniform with zero variance",
            "Inverted bell curve", "Exponentially decaying"
        ]
        wrongs = [w for w in wrongs if w != ans]
        q = f"In a {grp}, the mean score is ${mean_v}$ and the median score is ${med_v}$. How is the distribution of the marks skewed?"
        if add_q("easy", "Skewness", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 3. Least squares regression equation components (60)
    while easy_count < 180:
        a_val = round(random.uniform(5.0, 60.0), 1)
        b_val = round(random.uniform(-6.0, 6.0), 2)
        if abs(b_val) < 0.2: b_val = 1.45
        op = "+" if b_val >= 0 else "-"
        abs_b = abs(b_val)
        mode = random.choice(["gradient", "y_intercept"])
        if mode == "gradient":
            q = f"The least squares regression equation for a bivariate dataset is $\\hat{{y}} = {a_val:.1f} {op} {abs_b:.2f}x$. What is the gradient (slope $b$) of this regression line?"
            ans = f"{b_val:.2f}"
            wrongs = get_w_floats(b_val)
            exp = f"In the regression line $\\hat{{y}} = a + bx$, the coefficient of $x$ represents the slope $b = {ans}$."
        else:
            q = f"The least squares regression equation for a bivariate dataset is $\\hat{{y}} = {a_val:.1f} {op} {abs_b:.2f}x$. What is the $y$-intercept ($a$) of this regression line?"
            ans = f"{a_val:.1f}"
            wrongs = get_w_floats(a_val, 1)
            exp = f"In the regression line $\\hat{{y}} = a + bx$, the constant term $a$ is the $y$-intercept: $a = {ans}$."
            
        if add_q("easy", "Regression", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 4. Five-number summary calculations (Range and IQR) (60)
    while easy_count < 240:
        min_v = random.randint(10, 30)
        q1_v = min_v + random.randint(8, 18)
        med_v = q1_v + random.randint(5, 15)
        q3_v = med_v + random.randint(8, 20)
        max_v = q3_v + random.randint(10, 30)
        
        mode = random.choice(["IQR", "range"])
        if mode == "IQR":
            ans_val = q3_v - q1_v
            q = f"A dataset has the five-number summary: $\\text{{Min}} = {min_v}$, $Q_1 = {q1_v}$, $\\text{{Median}} = {med_v}$, $Q_3 = {q3_v}$, $\\text{{Max}} = {max_v}$. Calculate the Interquartile Range (IQR)."
            ans = str(ans_val)
            wrongs = get_w_ints(ans_val)
            exp = f"$\\text{{IQR}} = Q_3 - Q_1 = {q3_v} - {q1_v} = {ans}$."
        else:
            ans_val = max_v - min_v
            q = f"A dataset has the five-number summary: $\\text{{Min}} = {min_v}$, $Q_1 = {q1_v}$, $\\text{{Median}} = {med_v}$, $Q_3 = {q3_v}$, $\\text{{Max}} = {max_v}$. Calculate the range of the data."
            ans = str(ans_val)
            wrongs = get_w_ints(ans_val)
            exp = f"$\\text{{Range}} = \\text{{Maximum}} - \\text{{Minimum}} = {max_v} - {min_v} = {ans}$."
            
        if add_q("easy", "Five Number Summary", q, ans, wrongs, exp, "Knowledge"):
            easy_count += 1

    # 5. Simple mean calculation (60)
    while easy_count < 300:
        n = random.randint(5, 8)
        vals = [random.randint(10, 50) for _ in range(n)]
        s = sum(vals)
        mean_val = s / n
        q = f"Calculate the arithmetic mean of the following ${n}$ numbers: $\\{{{', '.join(str(v) for v in vals)}\\}}$."
        ans = f"{mean_val:.2f}" if not mean_val.is_integer() else str(int(mean_val))
        wrongs = get_w_floats(mean_val) if not mean_val.is_integer() else get_w_ints(int(mean_val))
        exp = f"$\\text{{Mean}} = \\frac{{\\sum x}}{{n}} = \\frac{{{s}}}{{{n}}} = {ans}$."
        if add_q("easy", "Measures of Central Tendency", q, ans, wrongs, exp, "Routine Procedures"):
            easy_count += 1

    print(f"Easy questions created: {easy_count}")

    # ====================================================
    # MEDIUM QUESTIONS (Target: 500)
    # ====================================================
    medium_count = 0

    # 1. Five-number summary calculation (Q1, Q2, Q3, IQR) from concrete datasets (120)
    while medium_count < 120:
        n = random.choice([9, 11, 13, 15])
        vals = sorted([random.randint(15, 95) for _ in range(n)])
        mid = (n - 1) // 2
        q2 = vals[mid]
        lower_half = vals[:mid]
        upper_half = vals[mid+1:]
        q1 = statistics.median(lower_half)
        q3 = statistics.median(upper_half)
        iqr = q3 - q1
        
        mode = random.choice(["Q1", "Q3", "Q2", "IQR"])
        if mode == "Q1":
            q = f"Given the ordered dataset: $\\{{{', '.join(str(v) for v in vals)}\\}}$, determine the lower quartile ($Q_1$)."
            ans = str(int(q1)) if float(q1).is_integer() else f"{q1:.1f}"
            wrongs = get_w_ints(int(q1)) if float(q1).is_integer() else get_w_floats(q1, 1)
            exp = f"The lower half of the data is $\\{{{', '.join(str(v) for v in lower_half)}\\}}$. Its median $Q_1 = {ans}$."
        elif mode == "Q3":
            q = f"Given the ordered dataset: $\\{{{', '.join(str(v) for v in vals)}\\}}$, determine the upper quartile ($Q_3$)."
            ans = str(int(q3)) if float(q3).is_integer() else f"{q3:.1f}"
            wrongs = get_w_ints(int(q3)) if float(q3).is_integer() else get_w_floats(q3, 1)
            exp = f"The upper half of the data is $\\{{{', '.join(str(v) for v in upper_half)}\\}}$. Its median $Q_3 = {ans}$."
        elif mode == "Q2":
            q = f"Determine the median ($Q_2$) of the following dataset: $\\{{{', '.join(str(v) for v in vals)}\\}}$."
            ans = str(int(q2))
            wrongs = get_w_ints(q2)
            exp = f"Since there are $n = {n}$ values, the median is the middle observation: $Q_2 = {ans}$."
        else:
            q = f"Calculate the Interquartile Range (IQR) for the dataset: $\\{{{', '.join(str(v) for v in vals)}\\}}$."
            ans = str(int(iqr)) if float(iqr).is_integer() else f"{iqr:.1f}"
            wrongs = get_w_ints(int(iqr)) if float(iqr).is_integer() else get_w_floats(iqr, 1)
            exp = f"$Q_1 = {q1}$, $Q_3 = {q3}$. Interquartile Range $\\text{{IQR}} = Q_3 - Q_1 = {q3} - {q1} = {ans}$."
            
        if add_q("medium", "Five Number Summary", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 2. Outlier thresholds 1.5 * IQR (100)
    while medium_count < 220:
        q1 = random.randint(30, 60)
        iqr = random.randint(15, 35)
        q3 = q1 + iqr
        threshold_mode = random.choice(["upper", "lower"])
        if threshold_mode == "upper":
            outlier_boundary = round(q3 + 1.5 * iqr, 1)
            ans = f"{outlier_boundary:.1f}" if not float(outlier_boundary).is_integer() else str(int(outlier_boundary))
            q = f"A dataset has a lower quartile $Q_1 = {q1}$ and an upper quartile $Q_3 = {q3}$. Above what threshold value is an observation considered an upper outlier?"
            wrongs = get_w_floats(outlier_boundary, 1)
            exp = f"$\\text{{IQR}} = Q_3 - Q_1 = {q3} - {q1} = {iqr}$. Upper outlier boundary $= Q_3 + 1.5 \\times \\text{{IQR}} = {q3} + 1.5({iqr}) = {ans}$."
        else:
            outlier_boundary = round(q1 - 1.5 * iqr, 1)
            ans = f"{outlier_boundary:.1f}" if not float(outlier_boundary).is_integer() else str(int(outlier_boundary))
            q = f"A dataset has $Q_1 = {q1}$ and $Q_3 = {q3}$. Below what threshold value is an observation classified as a lower outlier?"
            wrongs = get_w_floats(outlier_boundary, 1)
            exp = f"$\\text{{IQR}} = {q3} - {q1} = {iqr}$. Lower outlier boundary $= Q_1 - 1.5 \\times \\text{{IQR}} = {q1} - 1.5({iqr}) = {ans}$."
        if add_q("medium", "Outliers", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 3. Standard deviation interval (x̄ - σ, x̄ + σ) (100)
    while medium_count < 320:
        n = random.randint(8, 12)
        mean_target = random.randint(40, 70)
        data = [mean_target + random.randint(-18, 18) for _ in range(n)]
        mean_val = sum(data) / n
        variance = sum((x - mean_val)**2 for x in data) / n
        sd = math.sqrt(variance)
        lower_bound = mean_val - sd
        upper_bound = mean_val + sd
        count_in = sum(1 for x in data if lower_bound <= x <= upper_bound)
        
        q = f"For the dataset $\\{{{', '.join(str(x) for x in data)}\\}}$, with mean $\\bar{{x}} = {mean_val:.1f}$ and standard deviation $\\sigma = {sd:.1f}$, how many data points lie within ONE standard deviation of the mean (in the interval $(\\bar{{x}} - \\sigma; \\bar{{x}} + \\sigma)$)?"
        ans = str(count_in)
        wrongs = get_w_ints(count_in)
        exp = f"Interval $= ({mean_val:.1f} - {sd:.1f}; {mean_val:.1f} + {sd:.1f}) = ({lower_bound:.1f}; {upper_bound:.1f})$. Counting values in this range gives ${count_in}$ observations."
        if add_q("medium", "Standard Deviation", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 4. Effect of transformations on mean and standard deviation (80)
    while medium_count < 400:
        orig_mean = random.randint(45, 75)
        orig_sd = random.randint(5, 15)
        k = random.choice([2, 3, 4, 5])
        c = random.randint(5, 25)
        mode = random.choice(["add_sd", "mult_sd", "mult_mean", "both_sd"])
        if mode == "add_sd":
            q = f"A test distribution has a mean of ${orig_mean}$ and a standard deviation of ${orig_sd}$. If every learner is awarded an adjustment of $+{c}$ marks, what is the NEW standard deviation?"
            ans = str(orig_sd)
            wrongs = [str(orig_sd + c), str(orig_sd * c), str(orig_sd - c), str(round(orig_sd / c, 2)), str(orig_mean + c), str(orig_sd + 2), str(orig_sd**2)]
            exp = f"Adding a constant $c = {c}$ shifts all scores equally and leaves data dispersion unchanged. The new standard deviation remains ${orig_sd}$."
        elif mode == "mult_sd":
            ans = str(orig_sd * k)
            q = f"A set of data has a standard deviation of ${orig_sd}$. If every observation in the dataset is multiplied by ${k}$, what is the NEW standard deviation?"
            wrongs = [str(orig_sd), str(orig_sd + k), str(orig_sd * (k**2)), str(round(orig_sd / k, 2)), str(orig_sd + 2*k), str(orig_sd * k + 5), str(orig_sd * 10)]
            exp = f"Multiplying every observation by a constant factor $k = {k}$ scales the standard deviation by $|k|$. New $\\sigma = {orig_sd} \\times {k} = {ans}$."
        elif mode == "mult_mean":
            ans = str(orig_mean * k + c)
            q = f"A dataset has a mean of ${orig_mean}$. If every value is multiplied by ${k}$ and then ${c}$ is added, what is the new mean?"
            wrongs = get_w_ints(int(ans))
            exp = f"The mean undergoes the exact linear transformation: $\\text{{New Mean}} = ({orig_mean} \\times {k}) + {c} = {ans}$."
        else:
            ans = str(orig_sd * k)
            q = f"A dataset has a standard deviation of ${orig_sd}$. If each data item is transformed according to $x_{{\\text{{new}}}} = {k}x + {c}$, what is the new standard deviation?"
            wrongs = [str(orig_sd * k + c), str(orig_sd + c), str(orig_sd), str(orig_sd + k), str(orig_sd * c), str(orig_sd * (k**2)), str(orig_sd * k - c)]
            exp = f"The constant addition ${c}$ does not affect spread. Only the multiplication factor ${k}$ affects standard deviation: $\\sigma_{{\\text{{new}}}} = {orig_sd} \\times {k} = {ans}$."
            
        if add_q("medium", "Transformations", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    # 5. Least squares regression predictions (interpolation) (100)
    var_names = [
        ("study hours per week", "mathematics exam mark (%)"),
        ("engine capacity (litres)", "fuel consumption (litres/100 km)"),
        ("daily average temperature (°C)", "ice cream sales (hundreds)"),
        ("years of work experience", "monthly salary (thousands of Rands)"),
        ("fertilizer applied (kg)", "crop yield (tonnes/ha)"),
        ("revision tests completed", "final trial examination mark (%)")
    ]
    while medium_count < 500:
        x_name, y_name = random.choice(var_names)
        a = round(random.uniform(10.0, 45.0), 1)
        b = round(random.uniform(1.2, 5.8), 2)
        x_val = random.randint(4, 25)
        y_pred = round(a + b * x_val, 2)
        q = f"The least squares regression equation modeling {y_name} ($y$) against {x_name} ($x$) is $\\hat{{y}} = {a:.1f} + {b:.2f}x$. Predict the value of $y$ when $x = {x_val}$."
        ans = f"{y_pred:.2f}"
        wrongs = get_w_floats(y_pred)
        exp = f"Substitute $x = {x_val}$ into the regression line: $\\hat{{y}} = {a:.1f} + {b:.2f}({x_val}) = {ans}$."
        if add_q("medium", "Regression", q, ans, wrongs, exp, "Routine Procedures"):
            medium_count += 1

    print(f"Medium questions created: {medium_count}")

    # ====================================================
    # HARD QUESTIONS (Target: 200)
    # ====================================================
    hard_count = 0

    # 1. Finding unknown in dataset given mean (50)
    while hard_count < 50:
        knowns = [random.randint(15, 60) for _ in range(random.randint(5, 7))]
        x_target = random.randint(20, 75)
        all_vals = knowns + [x_target]
        mean_exact = sum(all_vals) / len(all_vals)
        if not mean_exact.is_integer():
            continue
        int_mean = int(mean_exact)
        shuffled_display = knowns + ["x"]
        random.shuffle(shuffled_display)
        disp_str = ", ".join(str(v) for v in shuffled_display)
        q = f"The dataset $\\{{{disp_str}\\}}$, containing an unknown value $x$, has an arithmetic mean of ${int_mean}$. Calculate the value of $x$."
        ans = str(x_target)
        wrongs = get_w_ints(x_target)
        exp = f"Sum of all ${len(all_vals)}$ values $= {len(all_vals)} \\times {int_mean} = {len(all_vals) * int_mean}$. Sum of known values $= {sum(knowns)}$. Therefore, $x = {len(all_vals) * int_mean} - {sum(knowns)} = {ans}$."
        if add_q("hard", "Measures of Central Tendency", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    # 2. Outlier identification in concrete datasets (50)
    while hard_count < 100:
        base = [random.randint(40, 70) for _ in range(8)]
        base.sort()
        q1 = statistics.median(base[:4])
        q3 = statistics.median(base[4:])
        iqr = q3 - q1
        if iqr < 5: continue
        upper_bound = q3 + 1.5 * iqr
        outlier_val = int(upper_bound + random.randint(8, 25))
        full_set = base + [outlier_val]
        random.shuffle(full_set)
        disp_str = ", ".join(str(v) for v in full_set)
        q = f"Determine which observation in the dataset $\\{{{disp_str}\\}}$, if any, qualifies as an outlier using the standard $1.5 \\times \\text{{IQR}}$ rule."
        ans = str(outlier_val)
        wrongs = [str(x) for x in base if x != outlier_val]
        while len(wrongs) < 8:
            wrongs.append(str(outlier_val + random.randint(1, 10)))
        exp = f"Sorting the data gives $Q_1 = {q1}$, $Q_3 = {q3}$, and $\\text{{IQR}} = {iqr}$. Upper boundary $= Q_3 + 1.5 \\times \\text{{IQR}} = {upper_bound:.1f}$. The only value exceeding this boundary is ${ans}$."
        if add_q("hard", "Outliers", q, ans, wrongs[:8], exp, "Problem Solving"):
            hard_count += 1

    # 3. Interpolation vs Extrapolation validity evaluation (50)
    investigations = [
        "A study recorded agricultural yield ($y$) for fertilizer application ($x$)",
        "An investigation measured vehicle braking distance ($y$) at various test speeds ($x$)",
        "A chemical experiment recorded reaction rate ($y$) across temperatures ($x$)",
        "An economics study evaluated weekly household expenditure ($y$) against income ($x$)",
        "A medical trial monitored patient blood pressure reduction ($y$) across dosage levels ($x$)",
        "An engineering test evaluated beam deflection ($y$) under applied load ($x$)"
    ]
    while hard_count < 150:
        inv = random.choice(investigations)
        x_min = random.randint(5, 25)
        x_max = x_min + random.randint(30, 80)
        is_interp = random.choice([True, False])
        if is_interp:
            pred_x = random.randint(x_min + 3, x_max - 3)
            ans = f"Interpolation (reliable), because x = {pred_x} lies within the observed range [{x_min}, {x_max}]"
            wrongs = [
                f"Extrapolation (unreliable), because x = {pred_x} lies outside the observed range [{x_min}, {x_max}]",
                "Interpolation (unreliable), because regression lines are never completely reliable",
                "Extrapolation (reliable), because the sample size is sufficiently large",
                "Interpolation (unreliable), because the correlation coefficient could be zero",
                "Extrapolation (reliable), because linear regression always applies for all x",
                "Neither interpolation nor extrapolation, because x is a discrete integer",
                "Extrapolation (unreliable), because the regression line only applies to positive numbers"
            ]
            exp = f"Since $x = {pred_x}$ lies between the minimum (${x_min}$) and maximum (${x_max}$) observed values, predicting $y$ is an interpolation and is generally reliable."
        else:
            pred_x = x_max + random.randint(15, 60)
            ans = f"Extrapolation (unreliable), because x = {pred_x} lies outside the observed range [{x_min}, {x_max}]"
            wrongs = [
                f"Interpolation (reliable), because x = {pred_x} lies within the observed range [{x_min}, {x_max}]",
                "Extrapolation (reliable), because the linear trend continues indefinitely",
                "Interpolation (unreliable), because it is beyond the median",
                "Extrapolation (reliable), because the slope is positive",
                "Interpolation (reliable), because r is close to 1",
                "Neither, because least squares cannot predict outside the mean",
                "Extrapolation (reliable), because the y-intercept is non-zero"
            ]
            exp = f"Since $x = {pred_x}$ lies outside the domain $[{x_min}, {x_max}]$ of the collected data, it is an extrapolation and may not be reliable as the linear relationship may change."

        q = f"{inv} where $x$ was recorded between ${x_min}$ and ${x_max}$. A researcher uses the regression model to predict $y$ at $x = {pred_x}$. How should this prediction be evaluated?"
        if add_q("hard", "Regression Validity", q, ans, wrongs, exp, "Problem Solving"):
            hard_count += 1

    # 4. Centroid and regression line equation deduction (50)
    while hard_count < 200:
        x_bar = round(random.uniform(15.0, 50.0), 1)
        b_slope = round(random.uniform(0.5, 4.5), 2)
        y_bar = round(random.uniform(40.0, 120.0), 1)
        a_intercept = round(y_bar - b_slope * x_bar, 2)
        q = f"A bivariate data set has mean values $\\bar{{x}} = {x_bar:.1f}$ and $\\bar{{y}} = {y_bar:.1f}$. The slope of the least squares regression line is $b = {b_slope:.2f}$. Determine the $y$-intercept ($a$) of the regression line $\\hat{{y}} = a + bx$."
        ans = f"{a_intercept:.2f}"
        wrongs = get_w_floats(a_intercept)
        exp = f"Because the regression line passes through the centroid $(\\bar{{x}}; \\bar{{y}})$, we have $\\bar{{y}} = a + b\\bar{{x}} \\implies a = \\bar{{y}} - b\\bar{{x}} = {y_bar:.1f} - ({b_slope:.2f} \\times {x_bar:.1f}) = {ans}$."
        if add_q("hard", "Regression", q, ans, wrongs, exp, "Complex Procedures"):
            hard_count += 1

    print(f"Final Counts: {{'easy': {easy_count}, 'medium': {medium_count}, 'hard': {hard_count}}}")
    out_dir = "dataset/grade12/mathematics"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "paper2_statistics.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    t1 = time.time()
    print(f"SUCCESS: {out_file} generated in {t1-t0:.2f}s with {len(questions)} questions.")

if __name__ == "__main__":
    generate_math_statistics()
