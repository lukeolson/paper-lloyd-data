"""Compare standard to lloyd to metis to rb lloyd methods."""

import numpy as np

import matplotlib.pyplot as plt
from pyamg.vis import aggviz

from common import set_figure, fig_size

with np.load('disc_allmethods_1_output.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']
    aggregate = data['aggregate'].tolist()

fs = fig_size.singlefull
set_figure(width=fs['width'], height=0.35*fs['width'])
fig, axs = plt.subplots(ncols=4)

for i, method in enumerate(aggregate):

    name = method['name']
    AggOp = method['AggOp']

    kwargs = {'color': '0.8',
              'alpha': 0.7,
              'edgecolor': 'tab:blue',
              'linewidth': 0.5}

    ax = axs[i]
    ax.triplot(V[:, 0], V[:, 1], E, color='0.7', lw=0.25)
    mappable = aggviz.plotaggs(AggOp, V, A, ax=ax,
                               cmapname='plasma_r',
                               buffer=[0.07, -0.052],
                               **kwargs)

    ax.axis('equal')
    ax.axis('off')
    ax.text(0.5, 0.05, name, transform=ax.transAxes,
            ha='center',
            bbox=dict(facecolor='w', edgecolor='0.7', linewidth=0.5))

figname = 'disc_allmethods.pdf'
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
