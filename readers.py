import numpy as np


def classical_reader(pwd: str) -> np.ndarray:
    with open(pwd, 'r') as f:
        lines = f.readlines()
        lines = [l.strip('\n').replace(' ', '0') for l in lines]
        return np.array([[int(c) for c in l] for l in lines])