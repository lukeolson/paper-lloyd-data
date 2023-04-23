"""Calculate energy for all aggregates."""
import numpy as np
import pyamg
from tqdm import tqdm

with np.load('./square_diameters_0_output.npz', allow_pickle=True) as data:
    G = data['C'].tolist()
    data_clusters_with_tb    = data['data_clusters_with_tb']       # noqa
    data_clusters_without_tb = data['data_clusters_without_tb']    # noqa
    data_centers_with_tb     = data['data_centers_with_tb']        # noqa
    data_centers_without_tb  = data['data_centers_without_tb']     # noqa

ntests = data_clusters_with_tb.shape[0]
naggs = data_centers_with_tb.shape[1]

# 1.  calculate standard deviations
#
# calculate the cluster size for each aggregate
# data_clusters_with_tb is cluster membership
# bincount will count the membership (aka cluster size)
cluster_size_with_tb = np.full((ntests, naggs), -1)
cluster_size_without_tb = np.full((ntests, naggs), -1)
for testid in range(ntests):
    cluster_size_with_tb[testid, :] = np.bincount(data_clusters_with_tb[testid, :])
    cluster_size_without_tb[testid, :] = np.bincount(data_clusters_without_tb[testid, :])

# caluclate the std dev for each sample
stddev_with_tb = np.std(cluster_size_with_tb, axis=1)
stddev_without_tb = np.std(cluster_size_without_tb, axis=1)

# 2. calculate energies
energy_with_tb = np.zeros(ntests)
for testid in tqdm(range(ntests)):
    centers = data_centers_with_tb[testid, :]
    distances, _, _ = pyamg.graph.bellman_ford(G, centers, method='standard')
    energy_with_tb[testid] = np.sum(distances**2)

energy_without_tb = np.zeros(ntests)
for testid in tqdm(range(ntests)):
    centers = data_centers_without_tb[testid, :]
    distances, _, _ = pyamg.graph.bellman_ford(G, centers, method='standard')
    energy_without_tb[testid] = np.sum(distances**2)

np.savez('square_diameters_1_output.npz',
         stddev_with_tb=stddev_with_tb,
         stddev_without_tb=stddev_without_tb,
         energy_with_tb=energy_with_tb,
         energy_without_tb=energy_without_tb)
