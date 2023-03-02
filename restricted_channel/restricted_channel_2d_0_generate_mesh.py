r"""Generate mesh for
   8-------9    10     11-----12
   |                           |
   |        \ _ _7_ _ /        |
   |                           |
   |          _ _6_ _          |
   |        /         \        |
   1-------2     3     4-------5
"""
import pygmsh
import matplotlib.pyplot as plt
import numpy as np
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

# point entities
with pygmsh.geo.Geometry() as geom:
    p1  = geom.add_point([-c, -1], cl*cl_expand)
    p2  = geom.add_point([-r, -1], cl)
    p3  = geom.add_point([ 0, -1], cl)
    p4  = geom.add_point([ r, -1], cl)
    p5  = geom.add_point([ c, -1], cl*cl_expand)
    #
    p6  = geom.add_point([ 0, -1+r], cl*cl_reduce)
    p7  = geom.add_point([ 0,  1-r], cl*cl_reduce)
    #
    p8  = geom.add_point([-c,  1], cl*cl_expand)
    p9  = geom.add_point([-r,  1], cl)
    p10 = geom.add_point([ 0,  1], cl)
    p11 = geom.add_point([ r,  1], cl)
    p12 = geom.add_point([ c,  1], cl*cl_expand)

    l1  = geom.add_line(p1, p2)
    l2  = geom.add_circle_arc(p2, p3, p6)
    l3  = geom.add_circle_arc(p6, p3, p4)
    l4  = geom.add_line(p4, p5)
    l5  = geom.add_line(p5, p12)
    l6  = geom.add_line(p12, p11)
    l7  = geom.add_circle_arc(p11, p10, p7)
    l8  = geom.add_circle_arc(p7, p10, p9)
    l9  = geom.add_line(p9, p8)
    l10 = geom.add_line(p8, p1)
    ll = geom.add_curve_loop([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])
    geom.add_physical(ll, label='bc0')

    ps = geom.add_plane_surface(ll)

    # if not uniform:
    #     field0 = geom.add_boundary_layer(lcmin=0.4, lcmax=0.8,
    #                                      distmin=0.4, distmax=1.0,
    #                                      edges_list=[l5, l10])
    #     field1 = geom.add_boundary_layer(lcmin=0.03, lcmax=0.08,
    #                                      distmin=0.02, distmax=.2,
    #                                      edges_list=[l2, l3, l7, l8])
    #     geom.set_background_mesh([field0, field1], operator="Min")

    mesh = geom.generate_mesh(dim=2, verbose=True)
    #for cell in mesh.cells:
    #    cell.data = cell.data.astype('int64')
    # geom.save_geometry('test.geo_unrolled')


meshname = 'restricted_channel_2d_0_output_uniform'
if not uniform:
    meshname = 'restricted_channel_2d_0_output_variable'

if '--savemesh' in sys.argv:
    V = mesh.points[:, :2]
    E = mesh.cells_dict['triangle']
    np.savez(meshname+'.npz', V=V, E=E)
    # mesh.write(meshname, file_format='gmsh')
else:
    E = mesh.cells_dict['triangle'].astype(np.int32)
    V = mesh.points[:, :2]
    fig, ax = plt.subplots()
    ax.triplot(V[:, 0], V[:, 1], E, lw=0.5)
    ax.set_aspect('equal', 'box')
    ax.axis('off')
    plt.show()
    plt.show()
