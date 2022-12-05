import math
import openmc
import openmc.deplete as dpl

# build geometry

# set up depletion
chain = dpl.Chain.from_xml('casl_pwr_chain.xml')

# process results