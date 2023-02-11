from scipy import ndimage
import numpy as np

def num_and_size(grid):
	N = len(grid)
	for i in range(N):
		for j in range(N):
			if grid[j, i] == 0:
				grid[j, i] = 2
			elif grid[j, i] ==2:
				grid[j, i] = 0
	lbl, nlbl = ndimage.label(grid)
	lbls = np.arange(1, nlbl+1)
	return ndimage.labeled_comprehension(grid, lbl, lbls, len, int, 0)

grid = np.array([
	[2, 0, 2, 2],
	[0, 0, 2, 2],
	[0, 2, 2, 1],
	[2, 2, 2, 1]
	])

print(num_and_size(grid))