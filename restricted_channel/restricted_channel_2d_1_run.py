"""Compare Lloyd vs rebalanced Lloyd. """
import numpy as np
import pyamg
from pyamg.gallery import fem

data = np.load('./restricted_channel_2d_0_output_variable.npz')
E = data['E'].astype(np.int32)
V = data['V']
mesh = fem.Mesh(V, E)
def f(x, y):
    return np.ones_like(x)
A, b = fem.gradgradform(mesh, f=f, degree=1)
A = A.tocsr()

mainseed = 35583

np.random.seed(mainseed)
ml = pyamg.smoothed_aggregation_solver(A,
                                       aggregate=('balanced lloyd',
                                                  {'measure': 'inv',
                                                   'ratio': 1/8,
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
ml_blloyd54 = ml
cycle_cx_blloyd54 = ml.cycle_complexity()

np.random.seed(mainseed)
ml = pyamg.smoothed_aggregation_solver(A,
                                       aggregate=('lloyd', {'measure': 'inv',
                                                            'ratio': 1/8,
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
ml_lloyd5 = ml
cycle_cx_lloyd5 = ml.cycle_complexity()

np.savez('restricted_channel_2d_1_output.npz',
         AggOp_blloyd54=AggOp_blloyd54,
         AggOp_lloyd5=AggOp_lloyd5,
         res_blloyd54=res_blloyd54,
         res_lloyd5=res_lloyd5,
         cycle_cx_blloyd54=cycle_cx_blloyd54,
         cycle_cx_lloyd5=cycle_cx_lloyd5,
         V=mesh.V, E=mesh.E, A=A)
