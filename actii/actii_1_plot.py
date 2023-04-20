"""Generate 3d aggregate files."""
import numpy as np
from scipy import sparse
import pyamg
import meshio

with np.load('./actii_78302.npz', allow_pickle=True) as data:
    V = data['V']
    E2V = data['E']

with np.load('./actii_0_output.npz') as data:
    clusters = data['clusters']
    centers = data['centers']

n = len(clusters)
naggs = clusters.max()+1
row = (clusters >= 0).nonzero()[0]
col = clusters[row]
data = np.ones(len(row), dtype=np.int32)
AggOp = sparse.coo_matrix((data, (row, col)), shape=(n, naggs)).tocsr()

new_aggs = AggOp.indices
ElementAggs = new_aggs[E2V]

# find all aggregates encompassing full elements
# mask[i] == True if all vertices in element i belong to the same aggregate
mask = np.where(abs(np.diff(ElementAggs)).max(axis=1) == 0)[0]
list_tets = E2V[mask, :]   # elements where element is full
cdata_tets = ElementAggs[mask, 0]

# V2V
# construct vertex to vertex graph
col = E2V.ravel()
row = np.kron(np.arange(0, E2V.shape[0]),
              np.ones((E2V.shape[1],), dtype=int))
data = np.ones((len(col),))
V2V = sparse.coo_matrix((data, (row, col)), shape=(E2V.shape[0], E2V.max()+1))
V2V = V2V.T * V2V
V2V = sparse.triu(V2V, 1).tocoo()

# find all triangles in aggregates
tris = []
edges = []
for aggnum, agg in enumerate(AggOp.T):
    aggids = agg.indices

    newtris = []
    newedges = []
    if len(aggids) < 4:
        continue

    for i in aggids:
        nbrs = V2V.getrow(i).indices
        I = np.where(new_aggs[nbrs] == aggnum)[0]
        if len(I) == 3:
            newtris.append(frozenset(list(nbrs[I])))
        if len(I) == 2:
            newedges.append(frozenset(list(nbrs[I])))

    tris += newtris
    edges += newedges

tris = set(tris)
edges = set(edges)

list_tris = np.zeros((len(tris), 3), dtype=int)
for i, tri in enumerate(tris):
    list_tris[i, :] = list(tri)

list_edges = np.zeros((len(edges), 2), dtype=int)
for i, edge in enumerate(edges):
    list_edges[i, :] = list(edge)

# colors_tets = 4*np.ones((list_tets.shape[0],))
colors_tets = 4 + cdata_tets
colors_tris = 3*np.ones((list_tris.shape[0],))
colors_edges = 2*np.ones((list_edges.shape[0],))

cells = {3: list_edges,
         5: list_tris,
         10: list_tets}
cdata = {3: colors_edges,
         5: colors_tris,
         10: colors_tets}  # make sure it's a tuple

cells = {10: E2V}
pyamg.vis.write_vtu(V=V, cells=cells, fname='output-mesh.vtu')

cells = {10: list_tets}
cdata = {10: colors_tets}  # make sure it's a tuple
pyamg.vis.write_vtu(V=V, cells=cells, fname='output-tets.vtu', cdata=cdata)

cells = {5: list_tris}
cdata = {5: colors_tris}  # make sure it's a tuple
pyamg.vis.write_vtu(V=V, cells=cells, fname='output-tris.vtu', cdata=cdata)

cells = {3: list_edges}
cdata = {3: colors_edges}  # make sure it's a tuple
pyamg.vis.write_vtu(V=V, cells=cells, fname='output-edges.vtu', cdata=cdata)
