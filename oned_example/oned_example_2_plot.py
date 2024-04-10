import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import shapely.geometry as sg
from shapely.ops import unary_union

from common import fig_size, set_figure

fs = fig_size.singlefull

seedtype = 'random'
set_figure(width=fs['width'], height=0.5*fs['height'])
fig = plt.figure()
gs = gridspec.GridSpec(4, 3, figure=fig)
ax0 = fig.add_subplot(gs[0, :-1])
ax1 = fig.add_subplot(gs[1, :-1])
ax2 = fig.add_subplot(gs[2, :-1])
ax3 = fig.add_subplot(gs[3, :-1])
ax4 = fig.add_subplot(gs[:, -1])
axs = [ax0, ax1, ax2, ax3, ax4]

data = np.load(f"oned_example_1_output_energy_{seedtype}.npz")
energy = [data[k] for k in data]

data = np.load(f"oned_example_1_output_clusters_{seedtype}.npz")
clusters = [data[k] for k in data]

data = np.load(f"oned_example_1_output_centers_{seedtype}.npz")
centers = [data[k] for k in data]

x = np.linspace(0, 1, len(clusters[0]))
kwargs = {'color': '0.8',
          'alpha': 0.7,
          'edgecolor': 'tab:blue',
          'linewidth': 1}
for i, (m, c, label) in enumerate(zip(clusters, centers,
                                      ['initial seed', 'balanced', 'rebalanced', 'optimal'])):
    ax = axs[i]
    todraw = []
    for cluster in np.arange(m.max()+1):
        idx = np.where(m==cluster)[0]
        if len(idx) == 1:
            pass
            newobj = sg.Point((x[idx[0]], 0))
            todraw.append(newobj)
        else:
            newobj = sg.LineString([[x[idx.min()], 0], [x[idx.max()], 0]])
            todraw.append(newobj)
    todraw = unary_union(todraw)
    todraw = todraw.buffer(0.012)
    #todraw = todraw.buffer(-0.05)
    if not hasattr(todraw, 'geoms'):
        todraw = sg.MultiPolygon([todraw])
    for poly in todraw.geoms:
        xs, ys = poly.exterior.xy
        ax.fill(xs, ys, clip_on=False, **kwargs)
    ax.plot(x, 0*x, '-', color='tab:gray', lw=0.5)
    ax.plot(x, 0*x, '.', color='k', ms=1.5)
    ax.plot(x[c], 0*x[c], 'o', color='k',
            ms=1.8, markerfacecolor='w', markeredgewidth=0.5)
    ax.axis(False)
    ax.set_aspect(1.0)
    ax.text(0.03, 1.4, label+":",
            ha='left', transform=ax.transAxes, fontsize=6)

ax = axs[-1]
fulle = []
fullx = []
x0 = 0
for i, e in enumerate(energy[1:]):
    fulle += e.tolist()
    fullx += list(x0 + np.arange(len(e)))
    x0 = fullx[-1]
ax.plot(fullx, fulle, 'o-', markerfacecolor='w', ms=1.5, markeredgewidth=0.5, color='tab:blue')
ax.set_yscale('log')
for i, e in enumerate(energy[1:]):
    #x = np.arange(len(e)) + x0
    #x0 = x[-1]
    #ax.set_yscale('log')
    #ax.plot(x, e, 'o-', markerfacecolor='w', ms=1.5, markeredgewidth=0.5)
    if i==0:
        ax.plot(2, e[-1], 's', color='tab:blue', markerfacecolor='w', ms=3)
ax.hlines(20, 0, 15, lw=0.5, color='tab:gray', linestyle='--')
ax.set_ylabel('energy')
ax.set_xlabel('iteration')
#ax.set_ylim([18, 40])
ax.set_ylim([10, 4000])
ax.set_xlim([-0.5, 15.5])

ax.text(0.75, 0.15, 'optimal',
        transform=ax.transAxes, fontsize=6, color='tab:gray')

#rot = -25
#ax.text(0.1, 0.6, 'balanced', ha='left',
#        rotation=rot, transform=ax.transAxes, fontsize=6, color='tab:blue')

x = 0.25
y = 0.25
ax.text(x, y, 'rebalance', ha='center',
        transform=ax.transAxes, fontsize=6, color='tab:blue')

import sys # noqa
if '--savefig' in sys.argv:
    plt.savefig(f'oned_example_{seedtype}.pdf')
else:
    plt.show()

# -------------------------------------------------------------------------
seedtype = 'cornercase'
set_figure(width=fs['width'], height=0.5*fs['height'])
fig = plt.figure()
gs = gridspec.GridSpec(4, 3, figure=fig)
ax0 = fig.add_subplot(gs[0, :-1])
ax1 = fig.add_subplot(gs[1, :-1])
ax2 = fig.add_subplot(gs[2, :-1])
ax3 = fig.add_subplot(gs[3, :-1])
ax4 = fig.add_subplot(gs[:, -1])
axs = [ax0, ax1, ax2, ax3, ax4]

data = np.load(f"oned_example_1_output_energy_{seedtype}.npz")
energy = [data[k] for k in data]

data = np.load(f"oned_example_1_output_clusters_{seedtype}.npz")
clusters = [data[k] for k in data]

data = np.load(f"oned_example_1_output_centers_{seedtype}.npz")
centers = [data[k] for k in data]

x = np.linspace(0, 1, len(clusters[0]))
kwargs = {'color': '0.8',
          'alpha': 0.7,
          'edgecolor': 'tab:blue',
          'linewidth': 1}
for i, (m, c, label) in enumerate(zip(clusters, centers,
                                      ['initial seed', 'balanced', 'rebalanced', 'optimal'])):
    ax = axs[i]
    todraw = []
    for cluster in np.arange(m.max()+1):
        idx = np.where(m==cluster)[0]
        if len(idx) == 1:
            pass
            newobj = sg.Point((x[idx[0]], 0))
            todraw.append(newobj)
        else:
            newobj = sg.LineString([[x[idx.min()], 0], [x[idx.max()], 0]])
            todraw.append(newobj)
    todraw = unary_union(todraw)
    todraw = todraw.buffer(0.012)
    #todraw = todraw.buffer(-0.05)
    if not hasattr(todraw, 'geoms'):
        todraw = sg.MultiPolygon([todraw])
    for poly in todraw.geoms:
        xs, ys = poly.exterior.xy
        ax.fill(xs, ys, clip_on=False, **kwargs)
    ax.plot(x, 0*x, '-', color='tab:gray', lw=0.5)
    ax.plot(x, 0*x, '.', color='k', ms=1.5)
    ax.plot(x[c], 0*x[c], 'o', color='k',
            ms=1.8, markerfacecolor='w', markeredgewidth=0.5)
    ax.axis(False)
    ax.set_aspect(1.0)
    ax.text(0.03, 1.4, label+":",
            ha='left', transform=ax.transAxes, fontsize=6)

ax = axs[-1]
fulle = []
fullx = []
x0 = 0
for i, e in enumerate(energy[1:]):
    fulle += e.tolist()
    fullx += list(x0 + np.arange(len(e)))
    x0 = fullx[-1]
ax.plot(fullx, fulle, 'o-', markerfacecolor='w', ms=1.5, markeredgewidth=0.5, color='tab:blue')
ax.set_yscale('log')
for i, e in enumerate(energy[1:]):
    #x = np.arange(len(e)) + x0
    #x0 = x[-1]
    #ax.plot(x, e, 'o-', markerfacecolor='w', ms=1.5, markeredgewidth=0.5, color='tab:blue')
    #ax.set_yscale('log')
    if i==0:
        ax.plot(10, energy[1][-1], 's', color='tab:blue', markerfacecolor='w', ms=2.5)
    if i==1:
        ax.plot(13, energy[2][-1], 's', color='tab:blue', markerfacecolor='w', ms=2.5)
ax.hlines(20, 0, 15, lw=0.5, color='tab:gray', linestyle='--')
ax.set_ylabel('energy')
ax.set_xlabel('iteration')
ax.set_ylim((10, 4000))
ax.set_xlim((-0.5, 15.5))

ax.text(0.05, 0.15, 'optimal',
        transform=ax.transAxes, fontsize=6, color='tab:gray')

#rot = -45
#ax.text(0.1, 0.6, 'balanced', ha='left',
#        rotation=rot, transform=ax.transAxes, fontsize=6, color='tab:blue')

x = 0.65
y = 0.45
ax.text(x, y, 'rebalance', ha='center',
        transform=ax.transAxes, fontsize=6, color='tab:blue')
ax.text(0.85, 0.27, 'rebalance', ha='center',
            transform=ax.transAxes, fontsize=6, color='tab:blue')

import sys # noqa
if '--savefig' in sys.argv:
    plt.savefig(f'oned_example_{seedtype}.pdf')
else:
    plt.show()
