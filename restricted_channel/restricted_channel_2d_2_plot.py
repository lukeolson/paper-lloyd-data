"""Plot aggregates and convergence."""

import matplotlib.pyplot as plt
import numpy as np
from common import set_figure, fig_size
from pyamg import vis

with np.load('./restricted_channel_2d_1_output.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']
    AggOp_blloyd54 = data['AggOp_blloyd54'].tolist()
    AggOp_lloyd5 = data['AggOp_lloyd5'].tolist()
    res_blloyd54 = data['res_blloyd54']
    res_lloyd5 = data['res_lloyd5']

fs = fig_size.singlefull
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots()

kwargs = {'color': '0.8',
          'edgecolor': 'tab:blue',
          'linewidth': 0.4}

ax.triplot(V[:, 0], V[:, 1], E, color='0.7', lw=0.25)
mappable = vis.aggviz.plotaggs(AggOp_blloyd54.tocsr(), V, A.tocsr(), ax=ax,
                               buffer=[0.06, -0.055],
                               **kwargs,
                               )
ax.axis('off')

figname = 'restricted_channel_2d_variable_aggregates.pdf'

import sys
if '--savefig' in sys.argv:
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()

fs = fig_size.single12
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots()

ax.semilogy(res_lloyd5, label='Standard Lloyd', color='tab:red', solid_capstyle='round')
ax.semilogy(res_blloyd54, label='Rebalanced Lloyd', color='tab:green', solid_capstyle='round')
ax.legend()
ax.set_xlabel('Iterations')
ax.set_ylabel(r'$\|r\|$')
ax.grid(True)

figname = 'restricted_channel_2d_variable_convergence.pdf'

import sys
if '--savefig' in sys.argv:
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
