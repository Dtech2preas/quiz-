import glob
import re

files = glob.glob("generate_*.py")
words = ["approx", "implies", "leq", "geq", "pm", "ln", "log", "sin", "cos", "tan", "sqrt", "sigma", "mu", "sum", "in", "cup", "cap", "perp", "Delta", "infty", "circ", "text", "dots", "mu", "mathbb", "theta", "alpha", "beta", "gamma", "times", "div", "left", "right", "hat", "bar", "vec"]

for f in files:
    with open(f, "r") as file:
        content = file.read()

    for word in words:
        # replace any \word with \\word, making sure we don't accidentally do \\\word
        # we can just blindly replace \\word with \word then \word with \\word
        content = content.replace('\\\\'+word, '\\'+word)
        content = content.replace('\\'+word, '\\\\'+word)

    with open(f, "w") as file:
        file.write(content)

words = ["mapsto", "cdot"]
for f in files:
    with open(f, "r") as file:
        content = file.read()

    for word in words:
        content = content.replace('\\\\'+word, '\\'+word)
        content = content.replace('\\'+word, '\\\\'+word)

    with open(f, "w") as file:
        file.write(content)
