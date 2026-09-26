import numpy as np

cellmap = np.zeros((8,8), dtype=int)

for row in range(cellmap.shape[0]):
    for col in range(cellmap.shape[1]):
        if row%2 == col%2:
            cellmap[row][col] = 1

print(cellmap)
