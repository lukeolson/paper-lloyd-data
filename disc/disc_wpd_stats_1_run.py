"""Run WPD test and gather statistics."""
import numpy as np
import pyamg

with np.load('./disc_n=10249_mesh_and_matrix.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']

n = A.shape[0]
print(V.shape, E.shape)

seed0 = 348934
np.random.seed(seed0)
ntests = 100
seeds = np.random.randint(0, 2**32 - 1, ntests)
seeds = np.unique(seeds)
if len(seeds) != ntests:
    raise ValueError('pick a new seed')

ppa = np.arange(3, 20)  # points per aggregate
naggs = n / ppa
ratios = 1 / ppa

nratios = len(ratios)
cx = np.zeros((nratios, ntests))
rho = np.zeros((nratios, ntests))
levs = np.zeros((nratios, ntests))
for ratioid, ratio in enumerate(ratios):
    AA = A.copy()
    print(f'ppa = {1/ratio}', flush=True)
    aggregate = ('balanced lloyd',
                 {'measure': 'inv',
                  'ratio': ratio,
                  'pad': 0.01,
                  'maxiter': 5,
                  'rebalance_iters': 4,
                  })

    print(f'starting {ntests} tests: ', end='', flush=True)
    for testid, testseed in enumerate(seeds):
        print(f'{testid}.', flush=True, end='')
        np.random.seed(testseed)
        ml = pyamg.smoothed_aggregation_solver(AA,
                                               strength='evolution',
                                               smooth='energy',
                                               aggregate=aggregate,
                                               max_coarse=10,
                                               max_levels=10,
                                               )

        if ml.levels[-1].A.shape[0] < 8:
            ml.levels = ml.levels[:-1]
        np.random.seed(testseed)
        u0 = np.random.rand(n)
        u = np.random.rand(n)
        # project out constant vector of 1s
        # u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u
        # b = A @ u
        b = np.zeros_like(u)
        res = []
        x = ml.solve(b, x0=u0, tol=1e-12, maxiter=50, residuals=res)
        m = 5
        cf = (res[-1] / res[-m])**(1/(m-1))

        levs[ratioid, testid] = len(ml.levels)
        cx[ratioid, testid] = ml.cycle_complexity()
        rho[ratioid, testid] = cf
        del ml
    print('', flush=True)

np.savez('disc_wpd_stats_1_output.npz', cx=cx, rho=rho, ppa=ppa, levs=levs)
