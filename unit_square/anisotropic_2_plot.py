"""Plot aggregates and convergence."""

import matplotlib.pyplot as plt
import numpy as np
from common import set_figure, fig_size
import matplotlib.collections as collections

from pyamg import vis

with np.load('./anisotropic_1_output.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']
    AggOp_blloyd54 = data['AggOp_blloyd54'].tolist()
    AggOp_lloyd5 = data['AggOp_lloyd5'].tolist()
    res_blloyd54 = data['res_blloyd54']
    res_lloyd5 = data['res_lloyd5']
    cycle_cx_blloyd54 = data['cycle_cx_blloyd54']
    cycle_cx_lloyd5 = data['cycle_cx_lloyd5']

rho_lloyd5 = (res_lloyd5[-1]/res_lloyd5[-1-5])**(1/5)
wpd_lloyd5 = cycle_cx_lloyd5 / (-np.log10(rho_lloyd5))

rho_blloyd54 = (res_blloyd54[-1]/res_blloyd54[-1-5])**(1/5)
wpd_blloyd54 = cycle_cx_blloyd54 / (-np.log10(rho_blloyd54))

def quadplot(x, y, quatrangles, ax=None, **kwargs):
    if not ax:
        ax=plt.gca()
    xy = np.c_[x, y]
    verts = xy[quatrangles]
    pc = collections.PolyCollection(verts, **kwargs)
    ax.add_collection(pc)
    ax.autoscale()

fs = fig_size.singlefull
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots()


kwargs = {'color': '0.8',
          'edgecolor': 'tab:blue',
          'linewidth': 0.4}

mappable = vis.aggviz.plotaggs(AggOp_blloyd54.tocsr(), V, A.tocsr(), ax=ax,
                               buffer=[0.06, -0.055],
                               **kwargs,
                               )

kwargs = {'facecolor': "None",
          'edgecolor': '0.7',
          'linewidth': 0.25}
x = V[:, 0]
y = V[:, 1]
quadplot(x, y, E, ax=ax, **kwargs)
ax.axis('off')

figname = 'anisotropic_aggregates.pdf'

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
ax.text(0.6, 0.4, f'WPD={wpd_lloyd5:.1f}', fontsize=6,
        color='tab:red', ha='left', transform=ax.transAxes)
ax.text(0.3, 0.15, f'WPD={wpd_blloyd54:.1f}', fontsize=6,
        color='tab:green', ha='left', transform=ax.transAxes)

figname = 'anisotropic_convergence.pdf'

import sys
if '--savefig' in sys.argv:
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
