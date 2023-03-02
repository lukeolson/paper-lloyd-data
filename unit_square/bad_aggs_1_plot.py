"""Plot bad aggregates."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
import shapely.geometry as sg
from shapely.ops import unary_union
from common import set_figure, fig_size

data = np.load('bad_aggs_0_output.npz')
G = sparse.csr_matrix(data['G'])
X = data['X']
Y = data['Y']
centers1 = data['centers1']
m1 = data['m1']
c1 = data['c1']
centers2 = data['centers2']
m2 = data['m2']
c2 = data['c2']

fs = fig_size.singlefull
set_figure(width=fs['width'], height=fs['height'])
plt.rcParams['figure.constrained_layout.use'] = False
fig, axs = plt.subplots(ncols=2)
fig.tight_layout(pad=5.0)
for axid, (_, m, _) in enumerate([(centers1, m1, c1),
                                  (centers2, m2, c2)]):
    ax = axs[axid]
    for z in np.linspace(0, 1, 6):
        ax.hlines(z, 0, 1, lw=0.5, color='tab:gray')
        ax.vlines(z, 0, 1, lw=0.5, color='tab:gray')
    AggOp = sparse.coo_matrix((np.ones(len(m)),
                              (np.arange(len(m)), m))).tocsr()

    for agg in AggOp.T:
        idx = agg.indices
        ax.plot(X[idx], Y[idx], 'ko', ms=3, markerfacecolor='w')
    # for cc in c:
    #     ax.plot(X[cc], Y[cc], 'm*', ms=15)
    G = G.tocoo()
    # for k, (i, j) in enumerate(zip(G.row, G.col)):
    #     x = (X[i] + X[j]) / 2
    #     y = (Y[i] + Y[j]) / 2
    #     d = G.data[k]
    #     ax.plot([X[i], X[j]], [Y[i], Y[j]], '-', color='0.7', lw=0.5)
    #     if i > j:
    #         ax.text(x, y, f'{d:2.2}')
    kwargs = {'color': '0.8',
              'alpha': 0.7,
              'edgecolor': 'tab:blue',
              'linewidth': 1}

    G = G.tocsr()
    for agg in AggOp.T:
        aggids = agg.indices
        todraw = []
        if len(aggids) == 1:
            i = aggids[0]
            coords = (X[i], Y[i])
            newobj = sg.Point(coords)
            todraw.append(newobj)
        else:
            for i in aggids:
                for j in aggids:
                    if (i > j and G[i, j]):
                        coords = list(zip(X[[i, j]], Y[[i, j]]))
                        newobj = sg.LineString(coords)
                        todraw.append(newobj)
        todraw = unary_union(todraw)
        todraw = todraw.buffer(0.10)
        todraw = todraw.buffer(-0.05)
        if not hasattr(todraw, 'geoms'):
            todraw = sg.MultiPolygon([todraw])
        for poly in todraw.geoms:
            xs, ys = poly.exterior.xy
            ax.fill(xs, ys, clip_on=False, **kwargs)
    ax.axis('square')
    ax.axis('off')

figname = 'bad_aggs.pdf'
import sys  # noqa
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
