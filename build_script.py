import json

def get_base_generator():
    return """import json
import random
import math
import sympy as sp
from generators_common import TopicGenerator, get_wrong_ints, get_wrong_floats, get_wrong_exprs

"""

with open("generate_math_dataset.py", "w") as f:
    f.write(get_base_generator())
