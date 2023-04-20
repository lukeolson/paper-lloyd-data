"""Import actii mesh and create distance matrix."""
import numpy as np
from scipy import sparse
import pyamg

with np.load('./actii_78302.npz', allow_pickle=True) as data:
    V = data['V']
    E = data['E']

ne = E.shape[0]
ID = np.kron(np.arange(0, ne), np.ones((4,), dtype='int'))
G = sparse.coo_matrix((np.ones((ne*4,)), (E.ravel(), ID,)))
G.setdiag(0)
G = G.tocsr()
E2E = G.T * G
V2V = G * G.T
V2V = V2V.tocsr().tocoo()
print('here')

A = V2V.copy()
for k, (i, j) in enumerate(zip(V2V.row, V2V.col)):
    dist = np.linalg.norm(V[i, :] - V[j, :])
    A.data[k] = dist

naggs = 20
clusters, centers = pyamg.graph.balanced_lloyd_cluster(A, naggs,
                                                       maxiter=3, rebalance_iters=2)

np.savez('actii_0_output.npz', clusters=clusters, centers=centers)
