import random
import statistics
import math
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats

def generate_statistics():
    gen = TopicGenerator("Statistics and Regression", "STAT", ["mean, median, mode", "standard deviation", "scatter plots", "linear regression"])

    attempts = 0
    while not gen.is_done() and attempts < 20000:
        attempts += 1
        available_diffs = [d for d in ["easy", "medium", "hard"] if gen.difficulty_counts[d] < gen.difficulty_targets[d]]
        if not available_diffs: break

        difficulty = random.choice(available_diffs)
        subtopic = random.choice(gen.subtopics)

        if subtopic == "mean, median, mode":
            # Generate dataset
            n = random.randint(5, 12)
            data = [random.randint(10, 50) for _ in range(n)]
            data.sort()

            if difficulty == "easy":
                # find mean
                q = f"Calculate the mean of the following dataset: {data}."
                mean_val = sum(data) / n
                correct = f"{mean_val:.2f}" if not mean_val.is_integer() else str(int(mean_val))
                wrongs = get_wrong_floats(mean_val) if not mean_val.is_integer() else get_wrong_ints(int(mean_val))
                exp = f"$\\text{{Mean}} = \\frac{{\\sum x}}{{n}} = \\frac{{{sum(data)}}}{{{n}}} = {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Find median of even/odd data
                q = f"Determine the median of the following dataset: {random.sample(data, len(data))}."
                median_val = statistics.median(data)
                correct = f"{median_val:.1f}" if not float(median_val).is_integer() else str(int(median_val))
                # generate wrongs from the dataset
                wrongs = set()
                while len(wrongs) < 8:
                    w = random.choice(data) + random.choice([0, -1, 1, 0.5])
                    w_str = f"{w:.1f}" if not float(w).is_integer() else str(int(w))
                    if w_str != correct: wrongs.add(w_str)
                exp = f"First, sort the data: {data}. The median is the middle value: ${correct}$."
                gen.add_question(subtopic, difficulty, q, correct, list(wrongs), exp)

            elif difficulty == "hard":
                # find unknown given mean
                missing_x = random.randint(10, 50)
                full_data = data + [missing_x]
                mean_val = sum(full_data) / len(full_data)
                if mean_val.is_integer():
                    q = f"The mean of the dataset {data + ['x']} is ${int(mean_val)}$. Find the value of $x$."
                    correct = str(missing_x)
                    wrongs = get_wrong_ints(missing_x)
                    exp = f"$\\frac{{{sum(data)} + x}}{{{len(full_data)}}} = {int(mean_val)} \\implies {sum(data)} + x = {int(mean_val) * len(full_data)} \\implies x = {missing_x}$."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "standard deviation":
            if difficulty == "easy":
                # Calculate variance or sum of squares
                n = 5
                data = [random.randint(2, 10) for _ in range(n)]
                mean_val = sum(data) / n
                if mean_val.is_integer():
                    # calculate std dev
                    variance = sum((x - mean_val)**2 for x in data) / n
                    std_dev = math.sqrt(variance)
                    q = f"Calculate the population standard deviation of the dataset: {data} (correct to 2 decimal places)."
                    correct = f"{std_dev:.2f}"
                    wrongs = get_wrong_floats(std_dev)
                    exp = f"Mean = ${int(mean_val)}$. Variance $\\sigma^2 = \\frac{{\\sum(x - \\mu)^2}}{{n}} = {variance:.2f}$. Standard deviation $\\sigma = \\sqrt{{{variance:.2f}}} \\approx {std_dev:.2f}$."
                    gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Percentage within 1 std dev
                # We can just ask a theoretical question or a simple calc
                n = 10
                data = [random.randint(10, 30) for _ in range(n)]
                mean_val = sum(data) / n
                variance = sum((x - mean_val)**2 for x in data) / n
                std_dev = math.sqrt(variance)
                count = sum(1 for x in data if mean_val - std_dev <= x <= mean_val + std_dev)
                # Ensure it's not a trivial amount
                q = f"For the dataset {data}, how many data points lie within one standard deviation of the mean?"
                correct = str(count)
                wrongs = [str(w) for w in range(n+1) if w != count]
                # pad if needed
                while len(wrongs) < 8:
                    wrongs.append(str(random.randint(n+1, n+10)))
                exp = f"Mean = ${mean_val:.2f}$, Std Dev = ${std_dev:.2f}$. The interval is $({(mean_val-std_dev):.2f}; {(mean_val+std_dev):.2f})$. There are ${count}$ values in this interval."
                gen.add_question(subtopic, difficulty, q, correct, wrongs[:8], exp)

            elif difficulty == "hard":
                # Effect of transformations
                n = random.randint(5, 10)
                std_dev = random.randint(2, 8)
                k = random.randint(2, 5)
                c = random.randint(5, 20)
                q = f"A dataset has a standard deviation of ${std_dev}$. If every value in the dataset is multiplied by ${k}$ and then ${c}$ is added, what is the new standard deviation?"
                ans = std_dev * k
                correct = str(ans)
                wrongs = [str(std_dev + c), str((std_dev * k) + c), str(std_dev), str(std_dev + k), str(std_dev * c), str(ans**2), str(std_dev * k * c), str(std_dev + k + c)]
                exp = f"Adding a constant does not change the standard deviation. Multiplying by a constant $k$ multiplies the standard deviation by $|k|$. New std dev = ${std_dev} \\times {k} = {ans}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

        elif subtopic == "scatter plots" or subtopic == "linear regression":
            # Generate points around a line
            m = random.uniform(-3, 3)
            if abs(m) < 0.5: m = random.choice([-2, 2])
            c = random.randint(-10, 10)
            n = random.randint(5, 8)
            xs = list(range(1, n+1))
            ys = [round(m*x + c + random.uniform(-2, 2), 1) for x in xs]

            # calculate exact linear regression
            sum_x = sum(xs)
            sum_y = sum(ys)
            sum_xy = sum(x*y for x, y in zip(xs, ys))
            sum_x2 = sum(x**2 for x in xs)

            # y = a + bx
            b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
            a = (sum_y - b * sum_x) / n

            if difficulty == "easy":
                # Find correlation coefficient concept or equation concept
                # Let's ask for the y-intercept 'a'
                q = f"Given the bivariate data: x = {xs}, y = {ys}. Calculate the y-intercept ($a$) of the least squares regression line $\\hat{{y}} = a + bx$ (correct to 2 decimal places)."
                correct = f"{a:.2f}"
                wrongs = get_wrong_floats(a)
                exp = f"Using a calculator (STAT mode), enter the data points. The y-intercept $a \\approx {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "medium":
                # Find gradient 'b'
                q = f"Given the bivariate data: x = {xs}, y = {ys}. Calculate the gradient ($b$) of the least squares regression line $\\hat{{y}} = a + bx$ (correct to 2 decimal places)."
                correct = f"{b:.2f}"
                wrongs = get_wrong_floats(b)
                exp = f"Using a calculator (STAT mode), enter the data points. The gradient $b \\approx {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

            elif difficulty == "hard":
                # predict value
                x_pred = random.randint(n+2, n+5)
                y_pred = a + b * x_pred
                q = f"The equation of the least squares regression line for a dataset is $\\hat{{y}} = {a:.2f} {'+' if b>=0 else ''}{b:.2f}x$. Predict the value of $y$ when $x = {x_pred}$ (correct to 2 decimal places)."
                correct = f"{y_pred:.2f}"
                wrongs = get_wrong_floats(y_pred)
                exp = f"Substitute $x = {x_pred}$ into the equation: $\\hat{{y}} = {a:.2f} {'+' if b>=0 else ''}{b:.2f}({x_pred}) \\approx {correct}$."
                gen.add_question(subtopic, difficulty, q, correct, wrongs, exp)

    return gen

if __name__ == "__main__":
    gen = generate_statistics()
    gen.save_to_json("paper2_statistics.json")
    print(f"Generated {len(gen.questions)} statistics questions.")
