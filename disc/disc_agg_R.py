"""Plot aggs and matrix R"""
import numpy as np
import matplotlib.pyplot as plt
import pyamg
from pyamg.vis import aggviz

from common import set_figure, fig_size

with np.load('./disc_n=13_mesh_and_matrix.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']

seed = 194847
np.random.seed(seed)

aggregate = ('balanced lloyd', {'measure': 'inv',
                                'ratio': 1/4,
                                'pad': 0.01,
                                'maxiter': 5,
                                'rebalance_iters': 4})
ml = pyamg.smoothed_aggregation_solver(A,
                                       aggregate=aggregate,
                                       smooth=None,
                                       strength='evolution',
                                       max_coarse=10,
                                       max_levels=2,
                                       keep=True,
                                       )

AggOp = ml.levels[0].AggOp

fs = fig_size.singlefull
set_figure(width=fs['width'], height=0.45*fs['width'])

fig, axs = plt.subplots(ncols=2)
kwargs = {'color': '0.8',
          'alpha': 0.5,
          'edgecolor': 'tab:blue',
          'linewidth': 2}

ax = axs[0]
ax.triplot(V[:, 0], V[:, 1], E, color='k', lw=0.25)
mappable = aggviz.plotaggs(AggOp, V, A, ax=ax,
                           cmapname='plasma_r',
                           buffer=[0.13, -0.052],
                           **kwargs)

ax.axis('off')

for i, (x, y) in enumerate(V):
    ax.plot(x, y, 'ko', markerfacecolor='w', ms=2)
    d = 0.03
    ax.text(x+d, y+d, f'{i}', ha='left', va='bottom',
            bbox=dict(boxstyle='square,pad=2', fc='none', ec='none'))

for i, agg in enumerate(AggOp.T):
    idx = agg.indices
    x = V[idx, 0].mean()
    y = V[idx, 1].mean()
    ax.text(x, y, f'{i}', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', fc='none', ec='tab:blue',
                      alpha=0.5, linewidth=2))

ax = axs[1]
R = ml.levels[0].R
ax.spy(R.T.toarray())
#ax.text(-0.4, 0.5, '$R^T=$', transform=ax.transAxes, ha='right')
ax.text(-0.4, 0.5, '$\hat{R}^T=$', transform=ax.transAxes, ha='right')

figname = 'disc_agg_R.pdf'
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
