"""2D P2 disc."""
import pyamg
import numpy as np
from pyamg.gallery import fem

with np.load('./disc_n=528_p=2_mesh_and_matrix.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']
    V2 = data['V2']
    E2 = data['E2']

mainseed = 35583
# mainseed = 100987
# mainseed = 898767
ppa = 5
# ppa = 2037 / 189

print('test rblloyd...')
np.random.seed(mainseed)
ml = pyamg.smoothed_aggregation_solver(A,
                                       aggregate=('balanced lloyd',
                                                  {'measure': 'inv',
                                                   'ratio': 1/ppa,
                                                   'pad': 0.01,
                                                   'maxiter': 5,
                                                   'rebalance_iters': 4,
                                                   }
                                                  ),
                                       strength='evolution',
                                       max_coarse=10,
                                       max_levels=2,
                                       keep=True,
                                       )

np.random.seed(mainseed)
n = A.shape[0]
u0 = np.random.rand(n)
u = np.random.rand(n)
u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u  # project out vector of 1s
b = A @ u
res = []
_ = ml.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res)
AggOp_blloyd54 = ml.levels[0].AggOp
res_blloyd54 = res
cycle_cx_rblloyd = ml.cycle_complexity()

print('test lloyd...')
np.random.seed(mainseed)
ml = pyamg.smoothed_aggregation_solver(A,
                                       aggregate=('lloyd', {'measure': 'inv',
                                                            'ratio': 1/ppa,
                                                            'maxiter': 5,
                                                            }),
                                       strength='evolution',
                                       max_coarse=10,
                                       max_levels=2,
                                       keep=True,
                                       )

np.random.seed(mainseed)
n = A.shape[0]
u0 = np.random.rand(n)
u = np.random.rand(n)
u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u  # project out vector of 1s
b = A @ u
res = []
_ = ml.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res)
AggOp_lloyd5 = ml.levels[0].AggOp
res_lloyd5 = res
cycle_cx_lloyd5 = ml.cycle_complexity()

print('test std...')
np.random.seed(mainseed)
ml = pyamg.smoothed_aggregation_solver(A,
                                       strength='evolution',
                                       max_coarse=10,
                                       max_levels=2,
                                       keep=True,
                                       )

np.random.seed(mainseed)
n = A.shape[0]
u0 = np.random.rand(n)
u = np.random.rand(n)
u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u  # project out vector of 1s
b = A @ u
res = []
_ = ml.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res)
AggOp_std = ml.levels[0].AggOp
res_std = res
cycle_cx_std = ml.cycle_complexity()

np.savez('disc_p2_1_output.npz',
         AggOp_blloyd54=AggOp_blloyd54,
         AggOp_lloyd5=AggOp_lloyd5,
         AggOp_std=AggOp_std,
         res_blloyd54=res_blloyd54,
         res_lloyd5=res_lloyd5,
         res_std=res_std,
         V=V, E=E, A=A,
         V2=V2, E2=E2,
         cycle_cx_std=cycle_cx_std,
         cycle_cx_lloyd5=cycle_cx_lloyd5,
         cycle_cx_rblloyd=cycle_cx_rblloyd
         )

# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# t = ax.triplot(mesh.V[:, 0], mesh.V[:, 1], mesh.E)
# ax.plot(mesh.V2[:, 0], mesh.V2[:, 1], 'o', ms=2)
# ax.axis('square')
# plt.show()
