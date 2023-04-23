"""Read 3d channel matrix."""
import numpy as np
from scipy.io import loadmat
import pyamg

data = loadmat('./restricted_channel_3d_matrix_and_mesh.mat')
A = data['A'].tocsr()
A.eliminate_zeros()

mesh_coords = data['mesh_coords']
mesh_cells = data['mesh_cells']
dof_coords = data['dof_coords']
assert np.max(np.abs(mesh_coords - dof_coords)) < 1e-13

ml0 = pyamg.smoothed_aggregation_solver(A,
                                        aggregate=('lloyd', {'measure': 'inv',
                                                             'ratio': 1/25,
                                                             'maxiter': 5,
                                                             }),
                                        strength='evolution',
                                        max_coarse=10,
                                        max_levels=2,
                                        keep=True,
                                        )


ml1 = pyamg.smoothed_aggregation_solver(A,
                                        aggregate=('balanced lloyd', {'measure': 'inv',
                                                                      'ratio': 1/25,
                                                                      'pad': 0.01,
                                                                      'maxiter': 5,
                                                                      'rebalance_iters': 4,
                                                                      }),
                                        strength='evolution',
                                        max_coarse=10,
                                        max_levels=2,
                                        keep=True,
                                        )

np.random.seed(474747)
n = A.shape[0]
u0 = np.random.rand(n)
u = np.random.rand(n)
u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u  # project out vector of 1s
b = A @ u

res0 = []
_ = ml0.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res0)
res1 = []
_ = ml1.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res1)

np.savez('./restricted_channel_3d_1_output.npz',
         res_lloyd=res0,
         res_rblloyd=res1)
