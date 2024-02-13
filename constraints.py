import numpy as np
from aux import are_numbers_unique
from typing import Protocol


class GenericConstraint(Protocol):
    def test(self, grid: np.ndarray) -> bool:
      ...

    def idxs_affected(self) -> np.ndarray:
      ...


class HorizontalSudokuConstraint(GenericConstraint):
    def __init__(self, idxRow: int):
        self.idxRow = idxRow

    def idxs_affected(self) -> [np.array, np.array]:
        return np.full(9, self.idxRow), np.arange(9)
    
    def test(self, grid: np.array) -> bool:
        digits = grid[self.idxRow]
        return are_numbers_unique(digits[digits > 0])


class VerticalSudokuConstraint(GenericConstraint):
    def __init__(self, idxCol: int):
        self.idxCol = idxCol

    def idxs_affected(self) -> [np.array, np.array]:
        return np.arange(9), np.full(9, self.idxCol)

    def test(self, grid: np.array) -> bool:
        digits = grid[:, self.idxCol]
        return are_numbers_unique(digits[digits > 0])
    
    
class BoxSudokuConstraint(GenericConstraint):
    def __init__(self, idxRow: int, idxCol: int):
        self.idxRow = idxRow
        self.idxCol = idxCol
        self.idxsAffectedRow = idxRow + (np.arange(9) // 3)
        self.idxsAffectedCol = idxCol + (np.arange(9) % 3)

    def idxs_affected(self) -> [np.array, np.array]:
        return self.idxsAffectedRow, self.idxsAffectedCol

    def test(self, grid: np.array) -> bool:
        digits = grid[self.idxsAffectedRow, self.idxsAffectedCol]
        return are_numbers_unique(digits[digits > 0])