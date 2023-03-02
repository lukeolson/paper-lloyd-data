import numpy as np
import matplotlib.pyplot as plt
from common import fig_size, set_figure
import pandas as pd
import seaborn as sns

with np.load('./square_stats_comparison_1_output_64.npz') as data:
    dev_cluster_size = data['dev_cluster_size']
    dev_diameters = data['dev_diameters']
    energy = data['energy']

df = pd.DataFrame({'dev_cluster_size_lloyd': dev_cluster_size[0, :],
                   'dev_cluster_size_blloyd': dev_cluster_size[1, :],
                   'dev_cluster_size_rblloyd': dev_cluster_size[2, :],
                   'dev_diameters_lloyd': dev_diameters[0, :],
                   'dev_diameters_blloyd': dev_diameters[1, :],
                   'dev_diameters_rblloyd': dev_diameters[2, :],
                   'energy_lloyd': energy[0, :],
                   'energy_blloyd': energy[1, :],
                   'energy_rblloyd': energy[2, :],
                   })

fs = fig_size.singlefull
set_figure(width=fs['width'], height=0.35*fs['width'])
fig, ax = plt.subplots(nrows=1, ncols=3, sharey=True)

kwargs = {'kde': False,
          #'bins': 12,
          'line_kws': {'linewidth': 0.5},
          'shrink': 0.7,
          'edgecolor': 'none',
          'linewidth': 0.5,
          'alpha': 0.7,
          }

nbins = 100
bins = np.linspace(.35, .85, nbins)
sns.histplot(data=df,
             x='dev_diameters_lloyd',
             color='tab:red',
             stat='count',
             label='standard Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[0])

sns.histplot(data=df,
             x='dev_diameters_blloyd',
             color='tab:blue',
             stat='count',
             label='balanced Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[0])

sns.histplot(data=df,
             x='dev_diameters_rblloyd',
             color='tab:green',
             stat='count',
             label='rebalanced Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[0])

bins = np.linspace(1.0, 6, nbins)
sns.histplot(data=df,
             x='dev_cluster_size_lloyd',
             color='tab:red',
             stat='count',
             label='standard Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[1])

sns.histplot(data=df,
             x='dev_cluster_size_blloyd',
             stat='count',
             color='tab:blue',
             label='balanced Lloyd',
             bins=bins,
             legend=True,
             **kwargs,
             ax=ax[1])

sns.histplot(data=df,
             x='dev_cluster_size_rblloyd',
             stat='count',
             color='tab:green',
             label='rebalanced Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[1])

bins = np.linspace(3500, 5500, nbins)
sns.histplot(data=df,
             x='energy_lloyd',
             color='tab:red',
             stat='count',
             label='standard Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[2])

sns.histplot(data=df,
             x='energy_blloyd',
             stat='count',
             color='tab:blue',
             label='balanced Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[2])

sns.histplot(data=df,
             x='energy_rblloyd',
             stat='count',
             color='tab:green',
             label='rebalanced Lloyd',
             bins=bins,
             **kwargs,
             ax=ax[2])

ax[0].legend(bbox_to_anchor=(0, 1.02, 2.8, 0.2), loc='lower left',
             mode='expand', borderaxespad=0, ncol=3)
ax[0].set_xlabel(r'Std. dev. in diameters')
ax[0].set_xticks([.4,.5,.6,.7,.8])
ax[1].set_xlabel(r'Std. dev. in \# of nodes')
ax[1].set_xticks([1,2,3,4,5])
ax[2].set_xlabel('Energy')
ax[2].set_xticks([3500,4500,5500])
ax[0].set_ylabel('Count')

figname = 'square_stats_comparison_64.pdf'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
