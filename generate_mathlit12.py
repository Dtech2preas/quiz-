import json
import random
import math
from typing import List
from generators_common import TopicGenerator

# Helper functions for generation
def get_wrong_answers_currency(correct_val: float, count=8) -> List[str]:
    wrongs = set()
    wrongs.add(correct_val * 12)
    wrongs.add(correct_val / 12)
    wrongs.add(correct_val * 1.15)
    wrongs.add(correct_val * 0.85)
    wrongs.add(correct_val * 2)
    wrongs.add(correct_val / 2)
    wrongs.add(correct_val + 100)
    wrongs.add(correct_val - 100)

    attempts = 0
    while len(wrongs) < count + 5 and attempts < 100:
        offset = random.uniform(-correct_val * 0.5, correct_val * 0.5)
        if offset != 0:
            val = correct_val + offset
            if val > 0:
                wrongs.add(val)
        attempts += 1

    res = [f"R{x:.2f}" for x in wrongs if abs(x - correct_val) > 1e-2]
    return res[:count]

# And so on for the generators. I'll write the script now.
