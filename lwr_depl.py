import math
import openmc
import openmc.deplete as dpl

# define materialsl
fuel = openmc.Material(name="uo2")
fuel.add_element("U", 1, percent_type="ao", enrichment=4.25)
fuel.add_element("O", 2)
fuel.set_density("g/cc", 10.4)

clad = openmc.Material(name="clad")
clad.add_element("Zr", 1)
clad.set_density("g/cc", 6)

water = openmc.Material(name="water")
water.add_element("O", 1)
water.add_element("H", 2)
water.set_density("g/cc", 1.0)
water.add_s_alpha_beta("c_H_in_H2O")
materials = openmc.Materials([fuel, clad, water])

fuel.set_density("g/cc", 10.4)

# build geometry
radii = [0.42, 0.45]
pin_surfaces = [openmc.ZCylinder(r=r) for r in radii]
pin_univ = openmc.model.pin(pin_surfaces, materials)
b = 1.24 # dimension of bounding box
bound_box = openmc.rectangular_prism(b, b, boundary_type="reflective")
root_cell = openmc.Cell(fill=pin_univ, region=bound_box)
geometry = openmc.Geometry([root_cell])
axesim1 = geometry.root_universe.plot()
axesim1.figure.savefig("geometry_slice.png")

# simulation settings
settings = openmc.Settings()
settings.particles = 1000
settings.inactive = 10
settings.batches = 50

# doing 2D so assign "volume", assumes z length of 1
fuel.volume = math.pi * radii[0] ** 2

# set up and register depletion chain
chain = dpl.Chain.from_xml('casl_pwr_chain.xml')
# registration allows creatioin of an Operator without passing a chain file
data_lib = openmc.data.DataLibrary()
data_lib.register_file("casl_pwr_chain.xml")
data_lib.export_to_xml()
# print(chain.nuclide_dict) uncomment for dictionary of nulcides

# set up model and transport coupled operator
model = openmc.Model(geometry=geometry,settings=settings)
operator = dpl.CoupledOperator(model,'casl_pwr_chain.xml')

# determine power loading schedule, create integrator, and run simulation
power = 174
time_steps = [30]*6 # 6 months
integrator = dpl.PredictorIntegrator(operator,time_steps,power,timestep_units='d')
integrator.integrate()

## EXTRAS
# In cases where burnable absorbers are present, pins experience strong flux
# gradients near the interface with coolant and the pin should be subdivided
# in order to allow for more accurate depletion within a pin itself
div_surfs_1 = [openmc.ZCylinder(r=1)]
div_1 = openmc.model.pin(div_surfs_1, [fuel, water], subdivisions={0: 10})
axesim2 = div_1.plot(width=(2.0, 2.0))
axesim2.figure.savefig("pin_division.png")