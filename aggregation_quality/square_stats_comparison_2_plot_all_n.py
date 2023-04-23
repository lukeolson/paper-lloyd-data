import numpy as np
import matplotlib.pyplot as plt
from common import fig_size, set_figure
import pandas as pd
import seaborn as sns

df = pd.DataFrame(columns =['nx', 'dmax', 'energy', 'method'])

for gridn in [16, 32, 64, 128]:
    with np.load(f'square_stats_comparison_1b_output_{gridn}.npz') as data:
        diameters = data['diameters']
        energy = data['energy']

    for method in [0, 1, 2]:
        dfn = pd.DataFrame(columns=['nx', 'dmax', 'energy', 'method'])
        dfn['dmax'] = diameters[method, :, :].max(axis=1) -\
                      diameters[method, :, :].min(axis=1)
        dfn['energy'] = energy[method, :] / gridn**2
        dfn['nx'] = gridn
        dfn['method'] = method
        df = pd.concat([df, dfn])

fs = fig_size.singlefull
set_figure(width=fs['width'], height=(2/3)*fs['height'])
fig, axs = plt.subplots(ncols=2)

# Plot the responses for different events and regions
ax = axs[0]
sns.lineplot(data=df,
             x='nx', y='dmax',
             hue='method',
             hue_order=[0, 1, 2],
             palette={0: 'tab:red', 1: 'tab:blue', 2: 'tab:green'},
             linestyle='-',
             linewidth=1.0,
             ax=ax,
             errorbar='sd')

ax.set_xlabel('Mesh size')
ax.set_ylabel('max $-$ min diameter')
ax.set_xticks([16, 32, 64, 128])
ax.set_yticks(np.arange(2, 6))

legend = ax.get_legend()
handles = legend.legendHandles
legend.remove()
ax.legend(handles, ['standard Lloyd', 'balanced Lloyd', 'rebalanced Lloyd'],
          bbox_to_anchor=(0, 1.02, 1.9, 0.2), loc='lower left',
          mode='expand', borderaxespad=0, ncol=3)

ax = axs[1]
# Plot the responses for different events and regions
sns.lineplot(data=df,
             x='nx', y='energy',
             hue='method',
             hue_order=[0, 1, 2],
             palette={0: 'tab:red', 1: 'tab:blue', 2: 'tab:green'},
             linewidth=1.0,
             legend=False,
             ax=ax, errorbar='sd')
ax.yaxis.tick_right()
ax.yaxis.set_label_position('right')
ax.set_xlabel('Mesh size')
ax.set_ylabel('Energy per node')
ax.set_xticks([16, 32, 64, 128])
ax.set_yticks([0.8, 1.0, 1.2, 1.4, 1.6])

figname = 'square_stats_comparison_all_n.pdf'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
