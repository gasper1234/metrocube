from metrocube_interactions_general import *
import time
from multiprocessing import Pool

# mreza in cas (za 200 izgleda 10**7 ok..., za 100 10**6 ...)
N = 100
t = 10**6
T = 2

# za vse interakcije
'''
int_list = ['rr', 'gg', 'bb', 'rg', 'rb', 'gb']
all_iter = np.zeros((3**6, 6))
ind = 0
for i in [-1, 0, 1]:
	for j in [-1, 0, 1]:
		for k in [-1, 0, 1]:
			for l in [-1, 0, 1]:
				for m in [-1, 0, 1]:
					for n in [-1, 0, 1]:
						all_iter[ind] = np.array([i, j, k, l, m, n])
						ind += 1
print(all_iter)
print(len(all_iter))
'''

interac = np.array([-1, -1, -1, 1, -1, -1])


# ustvaru mrezo z vsemi poravnanimi
grid = np.zeros((N, N, 3)).astype('int')
for i in range(N):
	for j in range(N):
		grid[i][j][1] = 1
		grid[i][j][2] = 2

# premesa mrezo
grid = mix_grid(grid, N)
#plot_grid(grid)

# možnosti za ozračun za T

#T_s = [0.1+i/100 for i in range(400)]
T_s = [0.1, 0.5, 1, 1.5, 2, 2.5]

# true/false shranjuje enrgije, zadnji argument je interakcija
fargs = [(t, grid, T, False, E_of_two, interac) for T in T_s]
mag_val = np.zeros_like(T_s)
final_ES = np.zeros_like(T_s)

# vrne seznam energij in gridov za vse T, paralelizirano!!
if __name__=="__main__":
	start = time.time()
	with Pool(3) as pool:
	   results = pool.starmap(run_time_gen,fargs)

	E_ss = np.array([results[i][1] for i in range(len(results))])
	grids = np.array([results[i][0] for i in range(len(results))])


	print(time.time()-start)
	
	# anizotropija in energija
	
	for i in range(len(grids)):
		_, mag_val[i] = red_spin(grids[i])
		final_ES[i] = grid_E(grids[i], interac)
	
	# plot fazne spremembe
	
	fig, ax = plt.subplots(2)
	ax[0].plot(T_s, abs(mag_val)/1000, 'x')
	ax[0].set_ylabel('spin aniso')
	ax[1].plot(T_s, final_ES/1000, 'x')
	ax[1].set_ylabel('E')
	ax[1].set_xlabel('T')
	plt.show()
	
	# TODO poracunaj spine !!!

	# energija
	#plot_E(E_ss, T_s)
	
	
	# rezultat
	
	ind = 0
	for grid in grids:
		plot_grid(grid, str(T_s[ind]))
		ind += 1
	