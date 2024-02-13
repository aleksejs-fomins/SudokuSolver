import constraints as cs


class ClassicalProblem:
    def __init__(self):
        self.constraints = []
        for iRow in range(9):
            self.constraints += [cs.VerticalSudokuConstraint(iRow)]
        for iCol in range(9):
            self.constraints += [cs.HorizontalSudokuConstraint(iCol)]
        for iRow in [0, 3, 6]:
            for iCol in [0, 3, 6]:
                self.constraints += [cs.BoxSudokuConstraint(iRow, iCol)]
