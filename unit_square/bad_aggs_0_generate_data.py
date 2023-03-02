"""Construct bad aggregates."""
import numpy as np
import pyamg

A = pyamg.gallery.poisson((6, 6), format='csr', type='FE')
X, Y = np.meshgrid(np.linspace(0, 1, 6), np.linspace(0, 1, 6))
X = X.ravel()
Y = Y.ravel()

# Make G a distance matrix from the grid
G = A.tocoo()
for k, (i, j) in enumerate(zip(G.row, G.col)):
    if i == j:
        G.data[k] = 0.0
    else:
        d = ((X[i] - X[j])**2 + (Y[i] - Y[j])**2)**0.5
        G.data[k] = d
G = G.tocsr()
G.eliminate_zeros()
G = G.tocoo().tocsr()

# centers = np.array([0, 1, 6, 29, 34, 35])  # singleton
# centers = np.array([14, 15, 20, 21])  # nice
centers1 = np.array([12, 13, 14, 15, 16, 17])  # pencils
m1, c1 = pyamg.graph.lloyd_cluster(G, centers1, maxiter=5)

centers2 = np.array([0, 1, 2, 6, 7, 8])  # singleton
m2, c2 = pyamg.graph.lloyd_cluster(G, centers2, maxiter=5)

np.savez('bad_aggs_0_output.npz',
         X=X, Y=Y, G=G.toarray(),
         centers1=centers1, m1=m1, c1=c1,
         centers2=centers2, m2=m2, c2=c2)
