import numpy as np

import pyamg
from scipy import sparse
from pyamg.gallery import fem

import gmsh
import pygmsh

def _compute_num_boundary_points(total_num_points):
    # From https://github.com/nschloe/optimesh/blob/main/examples/create_circle.py
    sqrt3_pi = np.sqrt(3) * np.pi
    num_boundary_points = -sqrt3_pi / 2 + np.sqrt(
        3 / 4 * np.pi ** 2 - (2 - 2 * total_num_points) * sqrt3_pi
    )
    return num_boundary_points

def gen_disc_mesh(num_points):
    target_edge_length = 2 * np.pi / _compute_num_boundary_points(num_points)

    print('  [genA] generating pygmsh')
    with pygmsh.geo.Geometry() as geom:
        geom.add_circle([0.0, 0.0], 1.0, mesh_size=target_edge_length)
        mesh = geom.generate_mesh(verbose=False)
        E = mesh.cells_dict['triangle'].astype(np.int32)
        V = mesh.points[:, :2]
    return V, E

def uexact(x, y):
    return (1 - x**2 - y**2) / 4

def f(x, y):
    # r = np.sqrt(x**2 + y**2)
    # return -(3 * np.pi / 2)**2 * np.cos(3 * np.pi * r / 2)
    return np.ones_like(x)

def g(x, y):
    return np.zeros_like(x)

def gen_A(num_points, dirichlet=False, remove_dirichlet=False, p=1):
    print('  [genA] generating mesh')
    V, E = gen_disc_mesh(num_points)
    mesh = fem.Mesh(V, E)
    if p == 2:
        mesh.generate_quadratic()
    d = mesh.V[:, 0]**2 + mesh.V[:, 1]**2
    I = np.where(np.abs(d - 1.0) < 1e-2)[0]
    bc = [{'id': I, 'g': g}]
    print('  [genA] generating fem')
    A, b = fem.gradgradform(mesh, f=f, degree=p)
    print('  [genA] applying bc')
    if dirichlet:
        A, b = fem.applybc(A, b, mesh, bc, remove_dirichlet=remove_dirichlet)
    A = A.tocsr()
    return A, b, mesh, bc

def verify():
    import meshplex
    hs = []
    errs = []
    for npts in 2**np.array([5,6,7,8,9,10,11,12]):
        A, b, mesh, bc = gen_A(npts)

        u = sparse.linalg.spsolve(A, b)
        uex = uexact(mesh.V[:, 0], mesh.V[:, 1])
        l2error = fem.l2norm(np.abs(u-uex), mesh)
        mpmesh = meshplex.Mesh(mesh.V, mesh.E)
        h = np.max(mpmesh.edge_lengths)

        hs.append(h)
        errs.append(l2error)

    hs = np.array(hs)
    errs = np.array(errs)
    order = np.log(errs[:-1]/errs[1:]) / np.log(hs[:-1]/hs[1:])
    print(f'order = {order}')

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    A, b, mesh, bc = gen_A(20)

    ml = pyamg.smoothed_aggregation_solver(A, max_coarse=15)
    u = ml.solve(b, tol=1e-10)
    fig, ax = plt.subplots()
    t = ax.tripcolor(mesh.V[:,0], mesh.V[:,1], mesh.E, u)
    ax.axis('square')
    ax.plot(mesh.V[bc[0]['id'],0], mesh.V[bc[0]['id'],1], 'ro', ms=3, markerfacecolor='w');
    plt.colorbar(t)
    plt.show()
