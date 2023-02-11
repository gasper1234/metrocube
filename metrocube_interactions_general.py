import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from numba import njit, prange

# intereakxija prvivlak istih, odboj drugih
int_list = ['rr', 'gg', 'bb', 'rg', 'rb', 'gb']
all_inter = np.zeros((3*6, 6))
testna = [1, 1, 1, -1, -1, -1]

@njit
def int_of_two(a, b, interact):
	if a == 0 and a == b:
		return interact[0]
	if a == 1 and a == b:
		return interact[1]
	if a == 2 and a == b:
		return interact[2]
	if a == 0 and b == 1 or a == 1 and b == 0:
		return interact[3]
	if a == 0 and b == 2 or a == 2 and b == 0:
		return interact[4]
	if a == 2 and b == 1 or a == 1 and b == 2:
		return interact[5]
	return 0

@njit(nogil=True)
def select_two(N):
	# return random position pair in grid (two arrays of len=2)
	# and new value index of changed ones
	p1 = np.floor(np.random.random(2)*N).astype('int')
	p2 = np.copy(p1)
	# desno, dol
	hr_vr = np.round(np.random.random())
	if hr_vr == 0:
		p2[0] = (p1[0]+1) % N
		val_ind = 1
	else:
		p2[1] = (p1[1]+1) % N
		val_ind = 2
	return p1, p2, val_ind

@njit(nogil=True)
def change_two(grid, p1, p2, val_ind):
	grid[p1[1], p1[0], 0], grid[p1[1], p1[0], val_ind] = grid[p1[1], p1[0], val_ind], grid[p1[1], p1[0], 0]
	grid[p2[1], p2[0], 0], grid[p2[1], p2[0], val_ind] = grid[p2[1], p2[0], val_ind], grid[p2[1], p2[0], 0]
	return grid

@njit(nogil=True)
def mix_grid(grid, N):
	for _ in range(5*N**2):
		p1, p2, ind = select_two(N)
		grid = change_two(grid, p1, p2, ind)
	return grid

# energija dveh sosedov, pri upostevanju njunega novega/starega indeksa
@njit(nogil=True)
def E_of_two(p1, p2, val_ind, grid, N, interact):
	E_0 = 0
	for p in [p1, p2]:
		for i in [-1, 1]:
			E_0 += int_of_two(grid[p[1], p[0], val_ind], grid[(p[1]+i) % N, p[0], 0], interact)
			E_0 += int_of_two(grid[p[1], p[0], val_ind], grid[p[1], (p[0]+i) % N, 0], interact)
	# prispevek med obema novima
	E_0 += int_of_two(grid[p1[1], p1[0], val_ind], grid[p2[1], p2[0], val_ind], interact)
	# odsteje dvojni prispevek med p1, p2 (stari - novi)
	E_0 -= int_of_two(grid[p1[1], p1[0], val_ind], grid[p2[1], p2[0], 0], interact)
	E_0 -= int_of_two(grid[p1[1], p1[0], 0], grid[p2[1], p2[0], val_ind], interact)
	return E_0

# izračuna celo E, ne uporabljaj - draga!!
@njit(nogil=True)
def grid_E(grid, interact):
	N = len(grid)
	E = 0
	for i in range(N):
		for j in range(N):
			E += int_of_two(grid[j, i, 0], grid[(j+1) % N, i, 0], interact)
			E += int_of_two(grid[j, i, 0], grid[j, (i+1) % N, 0], interact)
	return E

@njit(nogil=True)
def run_time_gen(t, grid_0, T, store_E, E_of_two, interact):
	grid = np.copy(grid_0)
	E_s = np.zeros(t)
	N = len(grid)
	for i in range(1, t):
		# position and orientation of pair
		p1, p2, ind = select_two(N)
		# old and new E
		E_0 = E_of_two(p1, p2, 0, grid, N, interact)
		E_1 = E_of_two(p1, p2, ind, grid, N, interact)
		DE = E_1 - E_0
		log_val = -T*np.log(np.random.random())
		if DE < log_val:
			grid = change_two(grid, p1, p2, ind)
			E_s[i] = E_s[i-1] + DE
		else:
			E_s[i] = E_s[i-1]
	if not store_E:
		return (grid, np.zeros(2))
	return (grid, E_s)

@njit
def red_spin(grid):
	N = len(grid)
	direction = np.zeros(3)
	for i in range(N):
		for j in range(N):
			if grid[j, i, 0] == 0:
				direction[0] += 1
			if grid[j, i, 1] == 0:
				direction[1] += 1
			if grid[j, i, 2] == 0:
				direction[2] += 1
	return direction, direction[0]-1/2*(direction[2]+direction[1])

# plotanje

def plot_grid(grid, title):
	color_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
	# ustvari nov colormap (RGB za vrednosti 0, 1, 2)
	rgb_map = colors.LinearSegmentedColormap.from_list("", color_list)
	plt.imshow(grid[:, :, 0], cmap=rgb_map)
	plt.title(title)
	#plt.savefig("sve/"+title+".png")
	plt.show()


def plot_E(E_ss, T_s):
	N = len(E_ss[0])//10**5
	if N < 1: N = 1
	for i in range(len(E_ss)):
		plt.plot(E_ss[i][::N], '-', label=T_s[i])
	plt.legend()
	plt.xlabel('t')
	plt.ylabel('E')
	plt.show()
