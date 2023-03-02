"""Compare standard to lloyd to metis to rb lloyd methods."""
import numpy as np
from disc_generate import gen_A

A, mesh, bc = gen_A(500, remove_dirichlet=False)
np.savez('disc_allmethods_0_output.npz', A=A, V=mesh.V, E=mesh.E)
