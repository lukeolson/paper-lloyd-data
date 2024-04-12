import numpy as np
import gmsh
from pyamg.gallery import fem

cases = [(1, 7), (1, 71.02153783196735), (2, 71.02153783196735), (1, 328.0)]

for case in cases:
    porder, perimeter_points = case
    gmsh.initialize()
    gmsh.model.add("disc")

    lc = 2 * np.pi / perimeter_points
    gmsh.model.geo.add_point(0, 0, 0, lc, 1)
    gmsh.model.geo.add_point(1, 0, 0, lc, 2)
    gmsh.model.geo.add_point(-0.5,  np.sqrt(3)/2, 0, lc, 3)
    gmsh.model.geo.add_point(-0.5, -np.sqrt(3)/2, 0, lc, 4)
    gmsh.model.geo.add_circle_arc(2, 1, 3, 1)
    gmsh.model.geo.add_circle_arc(3, 1, 4, 2)
    gmsh.model.geo.add_circle_arc(4, 1, 2, 3)
    gmsh.model.geo.add_curve_loop([1, 2, 3], 1)
    gmsh.model.geo.add_plane_surface([1], 1)
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(dim=2)

    # extract point coords
    _, V, _ = gmsh.model.mesh.getNodes()
    V = V.reshape(-1, 3)

    # get types
    elementTypes, elementTags, nodeTags = gmsh.model.mesh.getElements()
    i = list(elementTypes).index(2)
    assert elementTypes[i] == 2

    # get tags for triangles
    data = gmsh.model.mesh.getElementProperties(2)
    assert data[0] == 'Triangle 3'
    E = nodeTags[i].reshape(-1, data[3]) - 1  # 0-based indexing
    E = E.astype(np.int32)
    V = V[:, :2]

    # check to see if E is numbered 0 ... n
    ids = np.full((E.max()+1,), False)
    ids[E.ravel()] = True
    nv = np.sum(ids)
    if V.shape[0] != nv:
        print('fixing V and E')
        I = np.where(ids)[0]
        J = np.arange(E.max()+1)
        J[I] = np.arange(nv)
        E = J[E]
        V = V[I, :]
    n = V.shape[0]

    def f(x, y):
        return np.ones_like(x)
    mesh = fem.Mesh(V, E, degree=porder)
    V2 = None
    E2 = None
    if porder == 2:
        V2 = mesh.V2
        E2 = mesh.E2
    A, b = fem.gradgradform(mesh, f=f, degree=porder)
    A = A.tocsr()
    p = porder
    np.savez_compressed(f'disc_{n=}_{p=}_mesh_and_matrix.npz', V=V, E=E, A=A, b=b, V2=V2, E2=E2)

plot = False
if plot:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(12, 4))
    VV = V
    EE = E
    print(VV.shape)
    ax.triplot(V[:, 0], V[:, 1], E, lw=1)
    ax.set_aspect(1)
    plt.show()
