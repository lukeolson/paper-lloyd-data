"""Plot AMG energy over each aggregate."""

import matplotlib.pyplot as plt
import numpy as np
from common import set_figure, fig_size
#########from pyamg import vis
from pyamg.vis import aggviz

with np.load('disc_compareenergy_1_output.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']
    AggOp_blloyd54 = data['AggOp_blloyd54'].tolist()
    energy_blloyd54 = data['energy_blloyd54']
    AggOp_blloyd50 = data['AggOp_blloyd50'].tolist()
    energy_blloyd50 = data['energy_blloyd50']
    AggOp_lloyd5 = data['AggOp_lloyd5'].tolist()
    energy_lloyd5 = data['energy_lloyd5']
    res_blloyd54 = data['res_blloyd54']
    res_blloyd50 = data['res_blloyd50']
    res_lloyd5 = data['res_lloyd5']
    cycle_cx_blloyd54=data['cycle_cx_blloyd54']
    cycle_cx_blloyd50=data['cycle_cx_blloyd50']
    cycle_cx_lloyd5=data['cycle_cx_lloyd5']

fn = np.log10

plotsortedenergy = False
if plotsortedenergy:
    fig, ax = plt.subplots()
    ax.plot(fn(np.sort(energy_lloyd5)),   'o', color='tab:blue',  label='Lloyd')
    ax.plot(fn(np.sort(energy_blloyd50)), 'o', color='tab:red',   label='Balanced Lloyd')
    ax.plot(fn(np.sort(energy_blloyd54)), 'o', color='tab:green', label='Rebalanced Lloyd')
    # ax.set_yscale('log')
    plt.legend()
    plt.show()

fs = fig_size.singlefull
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots(ncols=3)

vmax = np.max(np.hstack((fn(energy_lloyd5), fn(energy_blloyd50), fn(energy_blloyd54))))
vmin = np.min(np.hstack((fn(energy_lloyd5), fn(energy_blloyd50), fn(energy_blloyd54))))
#print(f'{vmin=} {vmax=}')
vmin = -1.5
#print(f'{vmin=} {vmax=}')

kwargs = {'color': '0.8',
          'edgecolor': 'tab:blue',
          'linewidth': 0.7}

for i, data in enumerate([
                          (AggOp_lloyd5, energy_lloyd5, 'Lloyd'),
                          (AggOp_blloyd50, energy_blloyd50, 'Balanced Lloyd'),
                          (AggOp_blloyd54, energy_blloyd54, 'Rebalanced Lloyd'),
                         ]):
    axx = ax[i]
    AggOp = data[0]
    energy = data[1]
    label = data[2]
    mappable = aggviz.plotaggs(AggOp, V, A, ax=axx,
                                   aggvals=fn(energy),
                                   cmapname='BuPu',
                                   # cmapname='OrRd',
                                   # cmapname='Reds',
                                   buffer=[0.07, -0.052],
                                   vmin=vmin, vmax=vmax,
                                   **kwargs,
                                   )
    axx.triplot(V[:, 0], V[:, 1], E, color='0.7', lw=0.25)
    axx.axis('off')
    axx.set_title(f'{label}')
    axx.text(0.3, -0.1, f'$\\max(\\beta_a)$={10**energy.max():3.1f}', transform=axx.transAxes, ha='left')
    axx.text(0.3, -0.2, f'$\\mathrm{{mean}}(\\beta_a)$={(10**energy).mean():3.1f}', transform=axx.transAxes, ha='left')

finalenergy = fn(energy_lloyd5)
#print(finalenergy, finalenergy.min(), finalenergy.max(), finalenergy.mean())
cb = fig.colorbar(mappable, ax=ax[2], shrink=0.4,
                  ticks=[1, 0, -1],
                  format=lambda x, _: f'$10^{{{x}}}$')
cb.ax.tick_params(size=0.0)
cb.outline.set_visible(False)


figname = 'disc_compareenergy_aggregates.pdf'
import sys  # noqa
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()

fs = fig_size.single13
set_figure(width=2*fs['width'], height=2*fs['height'])
fig, ax = plt.subplots()

rho_lloyd5 = (res_lloyd5[-1]/res_lloyd5[-1-5])**(1/5)
wpd_lloyd5 = cycle_cx_lloyd5 / (-np.log10(rho_lloyd5))

rho_blloyd50 = (res_blloyd50[-1]/res_blloyd50[-1-5])**(1/5)
wpd_blloyd50 = cycle_cx_blloyd50 / (-np.log10(rho_blloyd50))

rho_blloyd54 = (res_blloyd54[-1]/res_blloyd54[-1-5])**(1/5)
wpd_blloyd54 = cycle_cx_blloyd54 / (-np.log10(rho_blloyd54))

ax.semilogy(res_lloyd5, label='Standard Lloyd', color='tab:red', solid_capstyle='round')
ax.semilogy(res_blloyd50, label='Balanced Lloyd', color='tab:blue', solid_capstyle='round')
ax.semilogy(res_blloyd54, label='Rebalanced Lloyd', color='tab:green', solid_capstyle='round')
ax.legend()
ax.set_xlabel('Iterations')
ax.set_ylabel(r'$\|r\|$')
ax.grid(True)

m = 7
w = 1.5
res = res_lloyd5
wpd = wpd_lloyd5
angle = np.rad2deg(np.arctan2(np.log10(res[-1]) - np.log10(res[-m]), m))
ax.text(len(res)-m, res[-m], f'WPD={wpd:.1f}', fontsize=6, color='tab:red', ha='left',
        rotation=w*angle, va='bottom', rotation_mode='anchor')

res = res_blloyd50
wpd = wpd_blloyd50
angle = np.rad2deg(np.arctan2(np.log10(res[-1]) - np.log10(res[-m]), m))
ax.text(len(res)-m, res[-m], f'WPD={wpd:.1f}', fontsize=6, color='tab:blue', ha='left',
        rotation=w*angle, va='bottom', rotation_mode='anchor')

res = res_blloyd54
wpd = wpd_blloyd54
angle = np.rad2deg(np.arctan2(np.log10(res[-1]) - np.log10(res[-m]), m))
ax.text(len(res)-m, res[-m], f'WPD={wpd:.1f}', fontsize=6, color='tab:green', ha='left',
        rotation=w*angle, va='bottom', rotation_mode='anchor')

figname = 'disc_compareenergy_convergence.pdf'
import sys  # noqa
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
