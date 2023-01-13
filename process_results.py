import openmc
import openmc.deplete as dpl
from matplotlib import pyplot
import numpy as np

# process results
results = dpl.Results("depletion_results.h5")
times,k = results.get_keff()
times /= (24*60*60) # # convert back to days from seconds
print("times:\n",times)
print("eigenvalues:\n",k)

pyplot.errorbar(times, k[:, 0], yerr=k[:, 1],capsize=2)
pyplot.title("$k_{eff}$ for each depletion stage")
pyplot.xticks([0, 30, 60, 90, 120, 150, 180])
pyplot.yticks(np.linspace(1.33,1.48,num=15,endpoint=False))
pyplot.grid(visible=True,axis='y')
pyplot.xlabel("Time [d]")
pyplot.ylabel("$k_{eff}\pm \sigma_{k_{eff}}$")
pyplot.savefig("k_vs_time.png")