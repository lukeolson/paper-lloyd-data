r"""Generate mesh for
   8-------9    10     11-----12
   |                           |
   |        \ _ _7_ _ /        |
   |                           |
   |          _ _6_ _          |
   |        /         \        |
   1-------2     3     4-------5
"""
import matplotlib.pyplot as plt
import numpy as np
import gmsh
import sys

cl = 0.06
cl_expand = 2
cl_reduce = 0.2
r = 0.9
uniform = False

# point 9 is at - r
# point 8 is at - r - diff
c = 1.5

if '--uniform' in sys.argv:
    uniform = True

if uniform:
    cl_expand = 1
    cl_reduce = 1

gmsh.initialize()
gmsh.model.add("channel")

# points
gmsh.model.geo.add_point(-c, -1, 0, cl*cl_expand, 1)
gmsh.model.geo.add_point(-r, -1, 0, cl,           2)
gmsh.model.geo.add_point( 0, -1, 0, cl,           3)
gmsh.model.geo.add_point( r, -1, 0, cl,           4)
gmsh.model.geo.add_point( c, -1, 0, cl*cl_expand, 5)
#
gmsh.model.geo.add_point( 0, -1+r, 0, cl*cl_reduce, 6)
gmsh.model.geo.add_point( 0,  1-r, 0, cl*cl_reduce, 7)
#
gmsh.model.geo.add_point(-c,  1, 0, cl*cl_expand, 8)
gmsh.model.geo.add_point(-r,  1, 0, cl,           9)
gmsh.model.geo.add_point( 0,  1, 0, cl,           10)
gmsh.model.geo.add_point( r,  1, 0, cl,           11)
gmsh.model.geo.add_point( c,  1, 0, cl*cl_expand, 12)

# lines
gmsh.model.geo.add_line(1, 2, 1)
gmsh.model.geo.add_circle_arc(2, 3, 6, 2)
gmsh.model.geo.add_circle_arc(6, 3, 4, 3)
gmsh.model.geo.add_line(4, 5, 4)
gmsh.model.geo.add_line(5, 12, 5)
#
gmsh.model.geo.add_line(12, 11, 6)
gmsh.model.geo.add_circle_arc(11, 10, 7, 7)
gmsh.model.geo.add_circle_arc(7, 10, 9, 8)
gmsh.model.geo.add_line(9, 8, 9)
gmsh.model.geo.add_line(8, 1, 10)

gmsh.model.geo.add_curve_loop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 33)
gmsh.model.geo.add_physical_group(1, [33], 34, name='bc0')
gmsh.model.geo.add_plane_surface([33], 1)
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(dim=2)

meshname = 'restricted_channel_2d_0_output_uniform'
if not uniform:
    meshname = 'restricted_channel_2d_0_output_variable'

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

if '--savemesh' in sys.argv:
    np.savez(meshname+'.npz', V=V, E=E)
else:
    fig, ax = plt.subplots()
    ax.triplot(V[:, 0], V[:, 1], E, lw=0.5)
    ax.set_aspect('equal', 'box')
    ax.axis('off')
    plt.show()
    plt.show()
