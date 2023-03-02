"""Plot aggregates and convergence."""

import matplotlib.pyplot as plt
import numpy as np
from common import set_figure, fig_size

from pyamg import vis

with np.load('./disc_p2_0_output.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']
    V2 = data['V2']
    E2 = data['E2']
    AggOp_blloyd54 = data['AggOp_blloyd54'].tolist()
    AggOp_lloyd5 = data['AggOp_lloyd5'].tolist()
    AggOp_std = data['AggOp_std'].tolist()
    res_blloyd54 = data['res_blloyd54']
    res_lloyd5 = data['res_lloyd5']
    res_std = data['res_std']
    cycle_cx_std = data['cycle_cx_std']
    cycle_cx_lloyd5 = data['cycle_cx_lloyd5']
    cycle_cx_rblloyd = data['cycle_cx_rblloyd']

fs = fig_size.singlefull
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots()

kwargs = {'color': '0.8',
          'edgecolor': 'tab:blue',
          'linewidth': 0.4}

mappable = vis.aggviz.plotaggs(AggOp_blloyd54.tocsr(), V2, A.tocsr(), ax=ax,
                               buffer=[0.06, -0.055],
                               **kwargs,
                               )

kwargs = {'facecolor': "None",
          'edgecolor': '0.7',
          'linewidth': 0.25}

ax.triplot(V[:, 0], V[:, 1], E, color='0.7', lw=0.25)
ax.plot(V2[:, 0], V2[:, 1], '.', color='k', ms=0.5)

ax.axis('off')

figname = 'disc_p2_aggregates.pdf'

import sys
if '--savefig' in sys.argv:
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()

fs = fig_size.single12
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots()

idx = cycle_cx_std * np.arange(len(res_std))
ax.semilogy(idx, res_std, label='Greedy', color='tab:gray', solid_capstyle='round')
idx = cycle_cx_lloyd5 * np.arange(len(res_lloyd5))
ax.semilogy(idx, res_lloyd5, label='Standard Lloyd', color='tab:red', solid_capstyle='round')
idx = cycle_cx_rblloyd * np.arange(len(res_blloyd54))
ax.semilogy(idx, res_blloyd54, label='Rebalanced Lloyd', color='tab:green', solid_capstyle='round')
ax.legend()
ax.set_xlabel('Iterations * cost')
ax.set_ylabel(r'$\|r\|$')
ax.grid(True)

figname = 'disc_p2_convergence.pdf'

import sys
if '--savefig' in sys.argv:
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
