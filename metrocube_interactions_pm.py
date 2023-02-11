import numpy as np
from numba import njit, prange

# intereakxija prvivlak istih, odboj drugih

# energija dveh sosedov, pri upostevanju njunega novega/starega indeksa
@njit(nogil=True)
def E_of_two(p1, p2, val_ind, grid, N):
	E_0 = 0
	for p in [p1, p2]:
		for i in [-1, 1]:
			if grid[p[1], p[0], val_ind] == grid[(p[1]+i) % N, p[0], 0]:
				E_0 += -1
			else:
				E_0 += 1
			if grid[p[1], p[0], val_ind] == grid[p[1], (p[0]+i) % N, 0]:
				E_0 += -1
			else:
				E_0 += 1
	# prispevek med obema novima
	if grid[p1[1], p1[0], val_ind] == grid[p2[1], p2[0], val_ind]:
		E_0 += -1
	else:
		E_0 += 1
	# odsteje dvojni prispevek med p1, p2 (stari - novi)
	if grid[p1[1], p1[0], val_ind] == grid[p2[1], p2[0], 0]:
		E_0 += 1
	else:
		E_0 += -1
	if grid[p1[1], p1[0], 0] == grid[p2[1], p2[0], val_ind]:
		E_0 += 1
	else:
		E_0 += -1
	# E pol-posebej obravnavaj oba primera (za gor dol in levo desno...)
	return E_0

# izračuna celo E, ne uporabljaj - draga!!
@njit(nogil=True)
def grid_E(grid):
	N = len(grid)
	E = 0
	for i in range(N):
		for j in range(N):
			if grid[j, i, 0] == grid[(j+1) % N, i, 0]:
				E += -1
			else: E += 1
			if grid[j, i, 0] == grid[j, (i+1) % N, 0]:
				E += -1
			else: E += 1
	return E
