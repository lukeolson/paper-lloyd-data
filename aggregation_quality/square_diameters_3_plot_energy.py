"""Plot square diameter statistics."""
import sys
import numpy as np
import matplotlib.pyplot as plt
from common import fig_size, set_figure
import pandas as pd
import seaborn as sns


with np.load('square_diameters_2_output.npz') as data:
    stddev_with_tb = data['stddev_with_tb']
    stddev_without_tb = data['stddev_without_tb']
    energy_with_tb = data['energy_with_tb']
    energy_without_tb = data['energy_without_tb']

fs = fig_size.singlefull
set_figure(width=fs['width'], height=0.5*fs['width'])
fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True)

df = pd.DataFrame({'stddev_with_tb': stddev_with_tb,
                   'stddev_without_tb': stddev_without_tb,
                   'energy_with_tb': energy_with_tb,
                   'energy_without_tb': energy_without_tb})

kwargs = {'kde': True,
          'bins': 15,
          'line_kws': {'linewidth': 0.5},
          'shrink': 0.8,
          'edgecolor': 'none',
          'linewidth': 0.5,
          'alpha': 0.7,
          }

sns.histplot(data=df,
             x='stddev_with_tb',
             color='tab:blue',
             stat='count',
             label='with tiebreaking',
             **kwargs,
             ax=ax[0])

sns.histplot(data=df,
             x='stddev_without_tb',
             stat='count',
             color='tab:red',
             label='without tiebreaking',
             legend=True,
             **kwargs,
             ax=ax[0])

sns.histplot(data=df,
             x='energy_with_tb',
             color='tab:blue',
             stat='count',
             **kwargs,
             ax=ax[1])

sns.histplot(data=df,
             x='energy_without_tb',
             color='tab:red',
             stat='count',
             **kwargs,
             ax=ax[1])

ax[0].legend(bbox_to_anchor=(0, 1.02, 1.2, 0.2), loc='lower left',
             mode='expand', borderaxespad=0, ncol=2)
ax[0].set_xlabel(r'Standard deviation in \# of nodes')
ax[1].set_xlabel('Energy')
ax[0].set_ylabel('Count')

figname = 'square_diameters_energy.pdf'
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
