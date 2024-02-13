import numpy as np
from time import time
import matplotlib.pyplot as plt

from readers import classical_reader
from problems import ClassicalProblem
from solvers import BruteSolverV1, BruteSolverV2, BruteSolverV3

grid = classical_reader('examples/grid_easy.dat')
problem = ClassicalProblem()

times = []
nTest = 50
for iTest in range(nTest):
    timeStart = time()
    bs = BruteSolverV3(grid, problem)
    bs.solve()

    times += [time() - timeStart]

plt.figure()
plt.plot(np.sort(times), np.linspace(0, 1, nTest))
plt.show()