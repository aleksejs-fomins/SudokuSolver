import numpy as np


def are_numbers_unique(arr: np.array) -> bool:
    return len(set(arr)) == len(arr)