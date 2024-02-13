import numpy as np
from problems import ClassicalProblem 


class BruteSolverV1:
    def __init__(self, grid: np.array, problem: ClassicalProblem):
        self.grid = np.copy(grid)
        self.problem = problem
        
        # Step 1: Identify coordinates of all unfilled digits
        self.idxsRow, self.idxsCol = np.where(self.grid == 0)
        self.nEmpty = len(self.idxsRow)
        self.empty1D = np.zeros_like(self.idxsRow)
    
    def test(self) -> bool:
        for constr in self.problem.constraints:
            if not constr.test(self.grid):
                return False
        return True
    
    def set(self, idxEmpty1D: int, val: int) -> None:
        self.empty1D[idxEmpty1D] = val
        self.grid[self.idxsRow[idxEmpty1D], self.idxsCol[idxEmpty1D]] = val
        
    def solve(self):
        idxEmpty1D = 0
        while True:
            if idxEmpty1D == -1:
                # First termination condition: if we are pointing at an index -1, finish. The loop has been exhausted
                break
            if idxEmpty1D == self.nEmpty:
                # We have reached a plausible solution. Print it, and continue the loop
                print(self.grid)
                idxEmpty1D -= 1
                continue
            
            # Progressively increment the value of this cell, until a fitting value is found or all have failed
            fits = False
            for newVal in range(self.empty1D[idxEmpty1D] + 1, 10):
                # Set this value and test fitness
                self.set(idxEmpty1D, newVal)
                fits = self.test()
                
                if fits:
                    # If this value fits, keep it, and continue fitting the next cell
                    idxEmpty1D += 1
                    break
                
            if not fits:
                # If no remaining values fit, clear this square and revert to increasing the previous one
                self.set(idxEmpty1D, 0)
                idxEmpty1D -= 1


class BruteSolverV2:
    def __init__(self, grid: np.array, problem: ClassicalProblem):
        self.grid = np.copy(grid)
        self.problem = problem

        # Step 1: Identify coordinates of all unfilled digits
        self.idxsRow, self.idxsCol = np.where(self.grid == 0)
        self.nEmpty = len(self.idxsRow)
        self.empty1D = np.zeros_like(self.idxsRow)
        
        # For each constraint, get cell indices that are affected by it
        # Make a temporary map from 2D index to 1D index
        idxs2Dto1D = {(iRow, iCol): i for i, (iRow, iCol) in enumerate(zip(self.idxsRow, self.idxsCol))}
        
        constr1Didxs = []
        for constr in self.problem.constraints:
            xIdxs, yIdxs = constr.idxs_affected()
            constr1Didxs += [[idxs2Dto1D[(iRow, iCol)] for iRow, iCol in zip(xIdxs, yIdxs) if (iRow, iCol) in idxs2Dto1D]]

        # For each empty cell, find indices of constraints that affect it
        self.empty1DconstrIdxs = []
        for iCell in range(self.nEmpty):
            self.empty1DconstrIdxs += [[iConstr for iConstr, idxs in enumerate(constr1Didxs) if iCell in idxs]]

    def test(self, idxEmpty1D: int) -> bool:
        # Only test the constraints that are relevant for this cell
        for idxConstr in self.empty1DconstrIdxs[idxEmpty1D]:
            if not self.problem.constraints[idxConstr].test(self.grid):
                return False
        return True

    def set(self, idxEmpty1D: int, val: int) -> None:
        self.empty1D[idxEmpty1D] = val
        self.grid[self.idxsRow[idxEmpty1D], self.idxsCol[idxEmpty1D]] = val

    def solve(self):
        idxEmpty1D = 0
        while True:
            if idxEmpty1D == -1:
                # First termination condition: if we are pointing at an index -1, finish. The loop has been exhausted
                break
            if idxEmpty1D == self.nEmpty:
                # We have reached a plausible solution. Print it, and continue the loop
                print(self.grid)
                idxEmpty1D -= 1
                continue

            # Progressively increment the value of this cell, until a fitting value is found or all have failed
            fits = False
            for newVal in range(self.empty1D[idxEmpty1D] + 1, 10):
                # Set this value and test fitness
                self.set(idxEmpty1D, newVal)
                fits = self.test(idxEmpty1D)

                if fits:
                    # If this value fits, keep it, and continue fitting the next cell
                    idxEmpty1D += 1
                    break

            if not fits:
                # If no remaining values fit, clear this square and revert to increasing the previous one
                self.set(idxEmpty1D, 0)
                idxEmpty1D -= 1


class BruteSolverV3:
    def __init__(self, grid: np.array, problem: ClassicalProblem):
        self.grid = np.copy(grid)
        self.problem = problem

        # Step 1: Identify coordinates of all unfilled digits
        self.idxsRow, self.idxsCol = np.where(self.grid == 0)
        self.nEmpty = len(self.idxsRow)
        self.empty1D = np.zeros_like(self.idxsRow)

        # Step 2: For each cell, find constraints that apply to it
        # For each constraint, get cell indices that are affected by it
        # Make a temporary map from 2D index to 1D index
        idxs2Dto1D = {(iRow, iCol): i for i, (iRow, iCol) in enumerate(zip(self.idxsRow, self.idxsCol))}

        constr1Didxs = []
        for constr in self.problem.constraints:
            xIdxs, yIdxs = constr.idxs_affected()
            constr1Didxs += [
                [idxs2Dto1D[(iRow, iCol)] for iRow, iCol in zip(xIdxs, yIdxs) if (iRow, iCol) in idxs2Dto1D]]

        # For each empty cell, find indices of constraints that affect it
        self.empty1DconstrIdxs = []
        for iCell in range(self.nEmpty):
            self.empty1DconstrIdxs += [[iConstr for iConstr, idxs in enumerate(constr1Didxs) if iCell in idxs]]

        # Step 3: Choose a random visit order for the empty cells
        self.emptyIdxSortOrder = np.random.permutation(self.nEmpty)

    def test(self, idxEmpty1D: int) -> bool:
        # Only test the constraints that are relevant for this cell
        for idxConstr in self.empty1DconstrIdxs[idxEmpty1D]:
            if not self.problem.constraints[idxConstr].test(self.grid):
                return False
        return True

    def set(self, idxEmpty1D: int, val: int) -> None:
        self.empty1D[idxEmpty1D] = val
        self.grid[self.idxsRow[idxEmpty1D], self.idxsCol[idxEmpty1D]] = val

    def solve(self):
        idxEmpty1D = 0  # Note: As opposed to the previous solutions, this one tracks the ordered array
        while True:
            if idxEmpty1D == -1:
                # First termination condition: if we are pointing at an index -1, finish. The loop has been exhausted
                break
            if idxEmpty1D == self.nEmpty:
                # We have reached a plausible solution. Print it, and continue the loop
                print(self.grid)
                idxEmpty1D -= 1
                continue
                
            # Find the actual index in the ordered array
            idxEmpty1Dorig = self.emptyIdxSortOrder[idxEmpty1D]

            # Progressively increment the value of this cell, until a fitting value is found or all have failed
            fits = False
            for newVal in range(self.empty1D[idxEmpty1Dorig] + 1, 10):
                # Set this value and test fitness
                self.set(idxEmpty1Dorig, newVal)
                fits = self.test(idxEmpty1Dorig)

                if fits:
                    # If this value fits, keep it, and continue fitting the next cell
                    idxEmpty1D += 1
                    break

            if not fits:
                # If no remaining values fit, clear this square and revert to increasing the previous one
                self.set(idxEmpty1Dorig, 0)
                idxEmpty1D -= 1


class BruteSolverV4:
    def __init__(self, grid: np.array, problem: ClassicalProblem):
        self.grid = np.copy(grid)
        self.problem = problem

        # Step 1: Identify coordinates of all unfilled digits
        self.idxsRow, self.idxsCol = np.where(self.grid == 0)
        self.nEmpty = len(self.idxsRow)
        self.empty1D = np.zeros_like(self.idxsRow)

        # Step 2: For each cell, find constraints that apply to it
        # For each constraint, get cell indices that are affected by it
        # Make a temporary map from 2D index to 1D index
        idxs2Dto1D = {(iRow, iCol): i for i, (iRow, iCol) in enumerate(zip(self.idxsRow, self.idxsCol))}

        constr1Didxs = []
        for constr in self.problem.constraints:
            xIdxs, yIdxs = constr.idxs_affected()
            constr1Didxs += [
                [idxs2Dto1D[(iRow, iCol)] for iRow, iCol in zip(xIdxs, yIdxs) if (iRow, iCol) in idxs2Dto1D]]

        # For each empty cell, find indices of constraints that affect it
        self.empty1DconstrIdxs = []
        for iCell in range(self.nEmpty):
            self.empty1DconstrIdxs += [[iConstr for iConstr, idxs in enumerate(constr1Didxs) if iCell in idxs]]

        # Step 3: For each cell, find the number of values that fit it
        nValsPerEmptyCell = np.zeros_like(self.idxsRow)
        for iEmpty in range(self.nEmpty):
            for val in range(1, 10):
                self.set(iEmpty, val)
                if self.test(iEmpty):
                    nValsPerEmptyCell[iEmpty] += 1
            self.set(iEmpty, 0)  # Set it back to zero, this is just a marking, not a solution

        self.emptyIdxSortOrder = np.argsort(nValsPerEmptyCell)  # Ascending by default - what we want

    def test(self, idxEmpty1D: int) -> bool:
        # Only test the constraints that are relevant for this cell
        for idxConstr in self.empty1DconstrIdxs[idxEmpty1D]:
            if not self.problem.constraints[idxConstr].test(self.grid):
                return False
        return True

    def set(self, idxEmpty1D: int, val: int) -> None:
        self.empty1D[idxEmpty1D] = val
        self.grid[self.idxsRow[idxEmpty1D], self.idxsCol[idxEmpty1D]] = val

    def solve(self):
        idxEmpty1D = 0  # Note: As opposed to the previous solutions, this one tracks the ordered array
        while True:
            if idxEmpty1D == -1:
                # First termination condition: if we are pointing at an index -1, finish. The loop has been exhausted
                break
            if idxEmpty1D == self.nEmpty:
                # We have reached a plausible solution. Print it, and continue the loop
                print(self.grid)
                idxEmpty1D -= 1
                continue

            # Find the actual index in the ordered array
            idxEmpty1Dorig = self.emptyIdxSortOrder[idxEmpty1D]

            # Progressively increment the value of this cell, until a fitting value is found or all have failed
            fits = False
            for newVal in range(self.empty1D[idxEmpty1Dorig] + 1, 10):
                # Set this value and test fitness
                self.set(idxEmpty1Dorig, newVal)
                fits = self.test(idxEmpty1Dorig)

                if fits:
                    # If this value fits, keep it, and continue fitting the next cell
                    idxEmpty1D += 1
                    break

            if not fits:
                # If no remaining values fit, clear this square and revert to increasing the previous one
                self.set(idxEmpty1Dorig, 0)
                idxEmpty1D -= 1