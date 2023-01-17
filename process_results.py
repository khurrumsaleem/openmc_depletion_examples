import openmc
import openmc.deplete as dpl
from matplotlib import pyplot
import numpy as np

# process results
results = dpl.Results("depletion_results.h5")
times,k = results.get_keff()
times /= (24*60*60) # # convert back to days from seconds
# print("times:\n",times)
# print("eigenvalues:\n",k)

pyplot.errorbar(times, k[:, 0], yerr=k[:, 1],capsize=2)
pyplot.title("$k_{eff}$ for each depletion stage")
pyplot.xticks([0, 30, 60, 90, 120, 150, 180])
pyplot.yticks(np.linspace(1.33,1.48,num=15,endpoint=False))
pyplot.grid(visible=True,axis='y')
pyplot.xlabel("Time [d]")
pyplot.ylabel("$k_{eff}\pm \sigma_{k_{eff}}$")
pyplot.savefig("k_vs_time.png")
pyplot.clf()

# examine atomic compositions and save plots
_, u235 = results.get_atoms("1", "U235")
_, xe135 = results.get_atoms("1", "Xe135")

pyplot.plot(times, u235, label="U235")
pyplot.xlabel("Time [d]")
pyplot.ylabel("Number of atoms - U235")
pyplot.title("U235 depletion")
pyplot.savefig("U235_depl.png")
pyplot.clf()

pyplot.plot(times, xe135, label="Xe135")
pyplot.xlabel("Time [d]")
pyplot.ylabel("Number of atoms - Xe135")
pyplot.title("Xe135 depletion")
pyplot.savefig("Xe135_depl.png")
pyplot.clf()

_, u235_fission = results.get_reaction_rate("1", "U235", "fission")

pyplot.plot(times, u235_fission)
pyplot.xlabel("Time [d]")
pyplot.ylabel("Fission reactions / s")
pyplot.title("Fission Rate Over Time")
pyplot.savefig("fission_rate_vs_time.png")
pyplot.clf()
