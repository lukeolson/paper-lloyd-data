from algorithm_reference import (rebalanced_lloyd_clustering,
                                 balanced_lloyd_clustering, bellman_ford)
import pyamg
import numpy as np
import subprocess
import os

if os.path.isfile('tmp_energy.npz'):
    subprocess.run(['rm', 'tmp_energy.npz'])

from numpy.random import default_rng
seed = 44678
rng = default_rng(seed)

n1d = 30
W = pyamg.gallery.poisson((n1d,), format='csr')
W.setdiag(0)
W.eliminate_zeros()
W.data[:] = 1.0
W = W.toarray()

Ncluster = 10

for seedtype in ['random', 'cornercase']:
    if seedtype == 'random':
        c0 = rng.permutation(W.shape[0])[:Ncluster]

    if seedtype == 'cornercase':
        c0 = np.array([i for i in range(Ncluster)])

    clusters = []
    centers = []

    print('------seeding')
    c = c0.copy()
    m, _ = bellman_ford(W, c)
    clusters.append(m)
    centers.append(c)
    # plot_clustering(m, c, axs[0], n1d, 'seed')

    print('------balanced')
    c = c0.copy()
    m, c, d, p, n, s, D, P = balanced_lloyd_clustering(W, c, Tmax=20, TBFmax=20)
    clusters.append(m)
    centers.append(c)
    # plot_clustering(m, c, axs[1], n1d, 'balanced')

    print('------rebalanced')
    c = c0.copy()
    m, c, d, p, n, s, D, P = rebalanced_lloyd_clustering(W, c, Tmax=20, TBFmax=20)
    clusters.append(m)
    centers.append(c)
    # plot_clustering(m, c, axs[2], n1d, 'rebalanced')

    print('------optimal')
    c = np.arange(1, n1d, 3)
    m = np.repeat(np.arange(Ncluster), 3)
    _, d = bellman_ford(W, c)
    print(f't=0: ', np.sum(d**2))
    clusters.append(m)
    centers.append(c)
    # plot_clustering(m, c, axs[3], n1d, 'optimal')

    np.savez(f'oned_example_1_output_clusters_{seedtype}.npz', *clusters)
    np.savez(f'oned_example_1_output_centers_{seedtype}.npz', *centers)
    energyfile = 'oned_example_1_output_energy'
    subprocess.run(['mv', 'tmp_energy.npz', energyfile+f'_{seedtype}.npz'])
