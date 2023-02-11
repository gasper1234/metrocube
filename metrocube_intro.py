from metrocube_interactions_pmrg import *
from metrocube_fun import *
import time
from multiprocessing import Pool

# mreza in cas (za 200 izgleda 10**7 ok..., za 100 10**6 ...)
N = 100
t = 10**6
T = 2

# ustvaru mrezo z vsemi poravnanimi
grid = np.zeros((N, N, 3)).astype('int')
for i in range(N):
	for j in range(N):
		grid[i][j][1] = 1
		grid[i][j][2] = 2

# premesa mrezo
grid = mix_grid(grid, N)
#plot_grid(grid)

#izracuna za T
#T_s = [0.05+i/100 for i in range(300)]
T_s = [1]
# true/false shranjuje enrgije, zadnji argument je interakcija
fargs = [(t, grid, T, False, E_of_two) for T in T_s]
mag_val = np.zeros_like(T_s)
aniso_val = np.zeros_like(T_s)
final_ES = np.zeros_like(T_s)
all_isl = np.zeros_like(T_s)
more_t10 = np.zeros_like(T_s)
more_t20 = np.zeros_like(T_s)
ave_leng = np.zeros_like(T_s)


# vrne seznam energij in gridov za vse T, paralelizirano!!
if __name__=="__main__":
	start = time.time()
	with Pool(3) as pool:
	   results = pool.starmap(run_time,fargs)

	E_ss = np.array([results[i][1] for i in range(len(results))])
	grids = np.array([results[i][0] for i in range(len(results))])


	print(time.time()-start)
	
	# anizotropija in energija
	'''
	for i in range(len(grids)):
		_, mag_val[i] = red_spin(grids[i])
		aniso_val[i] = aniso(grids[i])
		final_ES[i] = grid_E(grids[i])
	
	# plot fazne spremembe
	
	fig, ax = plt.subplots(2)
	ax[0].plot(T_s, abs(mag_val)/1000, 'x')
	ax[0].set_ylabel('SA')
	ax[1].plot(T_s, aniso_val, 'x')
	ax[1].set_ylabel(r'$A_{off}$')
	#ax[2].plot(T_s, final_ES)
	#ax[2].set_ylabel('E')
	#ax[2].set_xlabel('T')
	plt.show()
	'''
	# TODO poracunaj spine !!!

	# energija
	#plot_E(E_ss, T_s)
	
	
	# rezultat
	
	ind = 0
	for grid in grids:
		#sizes = num_and_size(grid)
		#all_isl[ind] = len(sizes)
		#more_t10[ind] = len_of_mor(sizes, 15)
		#more_t20[ind] = len_of_mor(sizes, 30)
		#ave_leng[ind] = np.average(sizes)
		ind += 1
		plot_grid(grid)


	# pregled otokov
	'''
	fig, ax = plt.subplots(3)

	ax[0].plot(T_s, all_isl, 'x', label='all')
	ax[0].legend()
	ax[0].set_ylabel('N')
	ax[1].plot(T_s, more_t10, 'x', label='>15')
	ax[1].plot(T_s, more_t20, 'x', label='>30')
	ax[1].set_ylabel('N')
	ax[1].legend()
	ax[2].plot(T_s, ave_leng, 'x')
	ax[2].set_ylabel('ave size')
	ax[2].set_xlabel('T')
	plt.show()
	'''