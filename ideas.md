# Ideas
### Brute Force V1
* Iteratively fills in numbers into the grid, checking all constraints whenever a number is fitted

### Brute Force V2
* Only check constraints that are relevant for the fitted cell

### Brute Force V3
* Initially test all cells and mark the number of values that its in each cell
* Sort and process cells in the order of increasing number of options

**Results**: Weird, the hard problem went from 10s to 3s, but the medium problem went from 0.2s to 7s.
This heuristic is clearly wrong, although it has something to it.

### Brute Force V3.1 Lolz
* Sort all cells in a random order, check performance variance

**Results**: Surprisingly, the solver performs orders of magnitude worse than even V1.
Apparently, the proximity of cells is integral to the performance.
* Of course, it is not the proximity itself, but rather that they affect each other's constraints


### Propagator V1
1. For each cell, test what values initially fit in it independently of others, store in an array
2. When we fit a new cell, re-test all cells that share the constraints with this cell, updating their available values
3. If any shared cell fails the test (has no values left), then this cell fails by extension.

### Propagator V2
* At every step, calculate the available values for all empty cells. Choose any one with the least options.
* Re-calculate values and find next candidate after this cell is filled. 


# Non-Standard Sudoku
* Sort empty cells by the number of constraints that apply to them, use