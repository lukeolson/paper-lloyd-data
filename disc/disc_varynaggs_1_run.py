"""Vary the number of points per aggregate."""
import pyamg
import numpy as np

with np.load('./disc_n=528_mesh_and_matrix.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']

n = A.shape[0]

# naggslist = np.linspace(4, int(n/2),)
# naggslist = np.array([5, 10, 15, 20, 30, 40, 50, 65, 80, 95, 125, 200], dtype=int)
naggslist = np.array([5,     15,             50,        100,      200, 250], dtype=int)
# naggslist = np.floor(np.linspace(50, int(n/3), 20))

seed = 1389089

AggOps = []
for naggs in naggslist:
    print(f'{naggs:>5}', end=' ')
print('\n')
for naggs in naggslist:
    print('    ^', end='', flush=True)
    ratio = naggs / n
    np.random.seed(seed)
    ml = pyamg.smoothed_aggregation_solver(A,
                                           aggregate=('balanced lloyd',
                                                      {'measure': 'inv',
                                                       'ratio': ratio,
                                                       'pad': 0.01,
                                                       'maxiter': 5,
                                                       'rebalance_iters': 4,
                                                       }),
                                           strength='evolution',
                                           max_coarse=10,
                                           max_levels=2,
                                           keep=True)
    AggOps.append(ml.levels[0].AggOp)
print('\n')

tosave = {f'{d[0]}': d[1] for d in zip(naggslist, AggOps)}
np.savez('disc_varynaggs_1_output.npz', **tosave)
np.savez('disc_varynaggs_1_output2.npz', V=V, E=E, A=A)
