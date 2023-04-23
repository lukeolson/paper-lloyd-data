"""Poisson."""
import numpy as np
from scipy import sparse
from scipy.io import savemat
import firedrake as fd

mesh = fd.Mesh('restricted_channel_3d.msh')

V = fd.FunctionSpace(mesh, "CG", 1)
u = fd.TrialFunction(V)
v = fd.TestFunction(V)

a = fd.inner(fd.grad(v), fd.grad(u)) * fd.dx

# bc = fd.DirichletBC(V, 0, [105])
u = fd.Function(V)

A = fd.assemble(a, mat_type='aij')
indptr, col, values = A.petscmat.getValuesCSR()
Asp = sparse.csr_matrix((values, col, indptr), A.petscmat.size)

coord_obj = fd.SpatialCoordinate(mesh)
coord_data = fd.interpolate(coord_obj, fd.VectorFunctionSpace(mesh, "CG", 1))
dof_coords = coord_data.dat.data_ro

mesh_coords = mesh.coordinates.dat.data_ro
mesh_cells = mesh.coordinates.cell_node_map().values
print(mesh_coords.shape, mesh_coords.shape)

dof_to_mesh = -1 * np.ones(dof_coords.shape[0], dtype=int)
for i, dof in enumerate(dof_coords):
    print(i)
    for j, vert in enumerate(mesh_coords):
        if np.allclose(dof, vert):
            dof_to_mesh[i] = j

savemat('./restricted_channel_3d_0_output_matrix_coord.mat',
        {'A': Asp,
         'dof_coords': dof_coords,
         'mesh_coords': mesh_coords,
         'mesh_cells': mesh_cells})
