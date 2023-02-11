import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import matplotlib.colors as colors
from numba import njit, prange


def plot_grid(grid):
	color_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
	# ustvari nov colormap (RGB za vrednosti 0, 1, 2)
	rgb_map = colors.LinearSegmentedColormap.from_list("", color_list)
	plt.imshow(grid[:, :, 0], cmap=rgb_map)
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

@njit(nogil=True)
def run_time(t, grid_0, T, store_E, E_of_two):
	grid = np.copy(grid_0)
	E_s = np.zeros(t)
	N = len(grid)
	for i in range(1, t):
		# position and orientation of pair
		p1, p2, ind = select_two(N)
		# old and new E
		E_0 = E_of_two(p1, p2, 0, grid, N)
		E_1 = E_of_two(p1, p2, ind, grid, N)
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

@njit(parallel=True)
def run_sim(t, grid, T_s):
	N = len(grid)
	grid_s = np.zeros((len(T_s), N, N, 3)).astype('int')
	E_ss = np.zeros((len(T_s), t))
	for i in prange(len(T_s)):
		grid_s[i], E_ss[i] = run_time(t, grid, T_s[i])
	return E_ss, grid_s

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

@njit
def aniso(grid):
	N = len(grid)
	direction = np.zeros(3)
	for i in range(N):
		for j in range(N):
			direction[grid[j, i, 0]] += 1
	ave = np.average(direction)
	ave_off = np.average(np.abs(direction-ave))
	return ave_off