"""Compare clustering of std bal and rebalanced."""

import numpy as np
import pyamg
from tqdm import tqdm

mainseed = 1122929

ntests = 1000

strength = 'evolution'
keep = True
measure = 'inv'
ratio = 0.1
pad = 0.01
maxiter = 5
standard_lloyd = {'measure': measure,
                  'ratio': ratio,
                  'maxiter': maxiter}

balanced_lloyd = {'measure': measure,
                  'ratio': ratio,
                  'pad': pad,
                  'maxiter': maxiter,
                  'rebalance_iters': 0}

rebalanced_lloyd = {'measure': measure,
                    'ratio': ratio,
                    'pad': pad,
                    'maxiter': maxiter,
                    'rebalance_iters': 4}

sten = np.array([[-1., -1, -1], [-1, 8, -1], [-1, -1, -1]])

for nx in tqdm([16, 32, 64, 128], desc='nx', colour='red', position=0, leave=False):
    A = pyamg.gallery.stencil_grid(sten, (nx, nx), format='csr')
    C = pyamg.strength.evolution_strength_of_connection(A)

    n = C.shape[0]
    ratio = 0.1
    naggs = int(min(max(ratio * n, 1), n))

    measure = 'inv'
    c = np.full((3, ntests, naggs), -1)
    m = np.full((3, ntests, A.shape[0]), -1)
    np.random.seed(mainseed)
    for testid in tqdm(range(ntests), desc='testid', colour='blue', position=1, leave=False):
        AggOp, centers = pyamg.aggregation.lloyd_aggregation(C, **standard_lloyd)
        m[0, testid, :] = AggOp.indices
        c[0, testid, :] = centers

        AggOp, centers = pyamg.aggregation.balanced_lloyd_aggregation(C, **balanced_lloyd, A=A)
        m[1, testid, :] = AggOp.indices
        c[1, testid, :] = centers

        AggOp, centers = pyamg.aggregation.balanced_lloyd_aggregation(C, **rebalanced_lloyd, A=A)
        m[2, testid, :] = AggOp.indices
        c[2, testid, :] = centers

    np.savez_compressed(f'square_stats_comparison_1_output_{nx}.npz',
                        m=m.astype(np.int16), c=c.astype(np.int16))
