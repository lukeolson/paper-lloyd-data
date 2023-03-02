"""Anisotropic diffusion on a 2D grid."""
import numpy as np
import pyamg

sten = pyamg.gallery.diffusion_stencil_2d(epsilon=0.1,
                                          theta=np.pi/3,
                                          type='FE')

nx = 40
ny = 40
A = pyamg.gallery.stencil_grid(sten, (ny, nx)).tocsr()
xy = np.mgrid[0:1:nx*1j, 0:1:ny*1j]
V = xy.reshape((2, nx*ny), order='F').T
I = np.arange(0, nx*ny).reshape((ny, nx), order='F')
E = np.zeros(((nx-1)*(ny-1), 4), dtype=int)
E[:, 0] = I[:ny-1, :nx-1].ravel(order='F')
E[:, 1] = I[:ny-1,  1:nx].ravel(order='F')
E[:, 2] = I[1:ny,   1:nx].ravel(order='F')
E[:, 3] = I[1:ny,  :nx-1].ravel(order='F')

mainseed = 35583
# mainseed = 100987
# mainseed = 898767
ppa  = 12

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

np.savez('./anisotropic_0_output.npz',
         AggOp_blloyd54=AggOp_blloyd54,
         AggOp_lloyd5=AggOp_lloyd5,
         res_blloyd54=res_blloyd54,
         res_lloyd5=res_lloyd5,
         V=V, E=E, A=A)
