import numpy as np
from aux import are_numbers_unique


def test_unique():
    assert are_numbers_unique(np.array([1,2,3,4,5])) == True
    assert are_numbers_unique(np.array([1,2,3,4,1])) == False