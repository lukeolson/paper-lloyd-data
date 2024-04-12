"""Plot aggregates and convergence."""

import matplotlib.pyplot as plt
import numpy as np
from common import set_figure, fig_size

from pyamg import vis

with np.load('./disc_p2_1_output.npz', allow_pickle=True) as data:
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
    cycle_cx_blloyd54 = data['cycle_cx_blloyd54']

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

rho_std = (res_std[-1]/res_std[-1-5])**(1/5)
wpd_std = cycle_cx_std / (-np.log10(rho_std))

rho_lloyd5 = (res_lloyd5[-1]/res_lloyd5[-1-5])**(1/5)
wpd_lloyd5 = cycle_cx_lloyd5 / (-np.log10(rho_lloyd5))

rho_blloyd54 = (res_blloyd54[-1]/res_blloyd54[-1-5])**(1/5)
wpd_blloyd54 = cycle_cx_blloyd54 / (-np.log10(rho_blloyd54))

ax.semilogy(res_std, label='Greedy', color='tab:gray', solid_capstyle='round')
ax.semilogy(res_lloyd5, label='Standard Lloyd', color='tab:red', solid_capstyle='round')
ax.semilogy(res_blloyd54, label='Rebalanced Lloyd', color='tab:green', solid_capstyle='round')
ax.legend()
ax.set_xlabel('Iterations')
ax.set_ylabel(r'$\|r\|$')
ax.grid(True)
ax.text(0.7, 0.3, f'WPD={wpd_std:.1f}', fontsize=6,
        color='tab:gray', ha='left', transform=ax.transAxes)
ax.text(0.5, 0.16, f'WPD={wpd_lloyd5:.1f}', fontsize=6,
        bbox=dict(facecolor='w',edgecolor='w',lw=0,pad=1),
        color='tab:red', ha='left', transform=ax.transAxes)
ax.text(0.2, 0.15, f'WPD={wpd_blloyd54:.1f}', fontsize=6,
        color='tab:green', ha='left', transform=ax.transAxes)

figname = 'disc_p2_convergence.pdf'

import sys
if '--savefig' in sys.argv:
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
