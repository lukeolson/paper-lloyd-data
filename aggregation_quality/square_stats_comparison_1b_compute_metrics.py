import numpy as np

from tqdm import tqdm
import pyamg

def calculate_diameters_per_cluster(G, m):
    """Call FW per cluster.

    Parameters
    ----------
    G : sparse
        Sparse matrix for the graph
    m : array
        Cluster memebership

    Returns
    -------
    diameter : array
        Longest shortest path for each cluster
    """
    n = G.shape[0]
    num_clusters = m.max()+1
    maxsize = int(8*np.ceil((n / num_clusters)))
    Cptr = np.empty(num_clusters, dtype=np.int32)    # ptr to start in C for each cluster
    C = np.empty(n, dtype=np.int32)                 # FW global index for current cluster

    P = np.empty(maxsize*maxsize, dtype=np.int32)    # FW predecessor array
    L = np.empty(n, dtype=np.int32)                  # FW local index for current cluster

    # global work array for distances
    dist_all = np.zeros((num_clusters, maxsize*maxsize), dtype=G.dtype, order='C')
    diameter = np.zeros(num_clusters)

    s = np.bincount(m)

    # initialize working arrays
    Clast = 0
    for a in range(num_clusters):
        Cptr[a] = Clast
        Clast += s[a]
    for i in range(n):
        a = m[i]
        C[Cptr[a]] = i
        Cptr[a] += 1
    Clast = 0
    for a in range(num_clusters):
        Cptr[a] = Clast
        Clast += s[a]
    for a in range(num_clusters):
        for _j in range(s[a]):
            L[C[Cptr[a]+_j]] = _j
    dist_all.fill(np.inf)

    for a in range(num_clusters):
        N = int(s[a])  # cluster size
        _N = Cptr[a]+N
        if _N >= G.shape[0]:
            _N = None
        P.fill(-1)
        pyamg.amg_core.floyd_warshall(G.shape[0], G.indptr, G.indices, G.data,
                                      dist_all[a, :].ravel(), P.ravel(),
                                      C[Cptr[a]:_N], L,
                                      m, a, N)
    for a in range(num_clusters):
        N = int(s[a])  # cluster size
        diameter[a] = np.max(dist_all[a, :N])
    return diameter

for gridn in [16, 32, 64, 128]:
    with np.load(f'square_stats_comparison_0_output_{gridn}.npz') as data:
        m = data['m']
        c = data['c']

    ntests = m.shape[1]
    naggs = c.shape[2]

    # 1. standard deviations in diameters
    sten = np.array([[-1., -1, -1], [-1, 8, -1], [-1, -1, -1]])

    A = pyamg.gallery.stencil_grid(sten, (gridn, gridn), format='csr')
    C = pyamg.strength.evolution_strength_of_connection(A)

    diameters = np.zeros((3, ntests, naggs))
    for method in [0, 1, 2]:
        for testid in tqdm(range(ntests)):
            thism = m[method, testid, :].astype(np.int32)
            diameters[method, testid, :] = calculate_diameters_per_cluster(C, thism)

    dev_diameters = np.full((3, ntests), -1.0)
    for method in [0, 1, 2]:
        dev_diameters[method, :] = np.std(diameters[method, :, :], axis=1)

    # 2. standard deviations in nodes
    cluster_size = np.full((3, ntests, naggs), -1)
    for method in [0, 1, 2]:
        for testid in range(ntests):
            cluster_size[method, testid, :] = np.bincount(m[method, testid, :])

    dev_cluster_size = np.full((3, ntests), -1.0)
    for method in [0, 1, 2]:
        dev_cluster_size[method, :] = np.std(cluster_size[method, :, :], axis=1)

    # 3. energy
    energy = np.zeros((3, ntests))
    for method in [0, 1, 2]:
        for testid in tqdm(range(ntests)):
            centers = c[method, testid, :]
            distances, _, _ = pyamg.graph.bellman_ford(C, centers, method='standard')
            energy[method, testid] = np.sum(distances**2)

    np.savez_compressed(f'square_stats_comparison_1b_output_{gridn}.npz',
                        diameters=diameters,
                        dev_cluster_size=dev_cluster_size,
                        dev_diameters=dev_diameters,
                        energy=energy)
