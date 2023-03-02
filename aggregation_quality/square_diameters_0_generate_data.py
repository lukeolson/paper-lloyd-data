"""Execute 1000 samples on a 64x64 mesh."""

import numpy as np
import pyamg
from tqdm import tqdm

# ntests = 20
ntests = 1000
nx = 64

sten = np.array([[-1., -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.double)

A = pyamg.gallery.stencil_grid(sten, (nx, nx), format='csr')
C = pyamg.strength.evolution_strength_of_connection(A)

# pad C
Epad = A.copy()
Epad.data[:] = 0.01
C += Epad

# 'inv' measure
data = 1.0 / abs(C.data)
G = C.__class__((data, C.indices, C.indptr), shape=C.shape)

n = C.shape[0]
ratio = 0.1
naggs = int(min(max(ratio * n, 1), n))

balanced_lloyd_with = {'centers': naggs,
                       'maxiter': 5,
                       'rebalance_iters': 0,
                       'tiebreaking': True}

balanced_lloyd_without = balanced_lloyd_with.copy()
balanced_lloyd_without['tiebreaking'] = False

seed = 239876

data_clusters_with_tb = np.zeros((ntests, n), dtype=int)
data_clusters_without_tb = np.zeros((ntests, n), dtype=int)
data_centers_with_tb = np.zeros((ntests, naggs), dtype=int)
data_centers_without_tb = np.zeros((ntests, naggs), dtype=int)

print('starting with tb')
np.random.rand(seed)
for testid in tqdm(range(ntests)):
    clusters, centers = pyamg.graph.balanced_lloyd_cluster(G, **balanced_lloyd_with)
    data_clusters_with_tb[testid, :] = clusters
    data_centers_with_tb[testid, :] = centers

print('starting with tb')
np.random.rand(seed)
for testid in tqdm(range(ntests)):
    clusters, centers = pyamg.graph.balanced_lloyd_cluster(G, **balanced_lloyd_without)
    data_clusters_without_tb[testid, :] = clusters
    data_centers_without_tb[testid, :] = centers

np.savez('square_diameters_0_output.npz',
         C=C,
         data_clusters_with_tb=data_clusters_with_tb,
         data_clusters_without_tb=data_clusters_without_tb,
         data_centers_with_tb=data_centers_with_tb,
         data_centers_without_tb=data_centers_without_tb)
