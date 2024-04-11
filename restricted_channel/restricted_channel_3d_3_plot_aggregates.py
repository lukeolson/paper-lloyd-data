import numpy as np
from scipy import sparse
import pyamg

with np.load('./restricted_channel_3d_1_output.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']
    AggOp = data['AggOp_blloyd'].tolist()

# pyamg.vis.vis_aggregate_groups(V, E, AggOp_blloyd, mesh_type='tet', fname='test.vtu')

new_aggs = AggOp.indices
ElementAggs = new_aggs[E]

# find all aggregates encompassing full elements
# mask[i] == True if all vertices in element i belong to the same aggregate
mask = np.where(abs(np.diff(ElementAggs)).max(axis=1) == 0)[0]
list_tets = E[mask, :]   # elements where element is full
cdata_tets = ElementAggs[mask, 0]

# V2V
# construct vertex to vertex graph
col = E.ravel()
row = np.kron(np.arange(0, E.shape[0]),
              np.ones((E.shape[1],), dtype=int))
data = np.ones((len(col),))
V2V = sparse.coo_matrix((data, (row, col)), shape=(E.shape[0], E.max()+1))
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

cells = {10: E}
pyamg.vis.write_vtu(V=V, cells=cells, fname='restricted_channel_3d_output_mesh.vtu')

cells = {10: list_tets}
cdata = {10: colors_tets}  # make sure it's a tuple
pyamg.vis.write_vtu(V=V, cells=cells, fname='restricted_channel_3d_output_tets.vtu', cdata=cdata)

cells = {5: list_tris}
cdata = {5: colors_tris}  # make sure it's a tuple
pyamg.vis.write_vtu(V=V, cells=cells, fname='restricted_channel_3d_output_tris.vtu', cdata=cdata)

cells = {3: list_edges}
cdata = {3: colors_edges}  # make sure it's a tuple
pyamg.vis.write_vtu(V=V, cells=cells, fname='restricted_channel_3d_output_edges.vtu', cdata=cdata)
