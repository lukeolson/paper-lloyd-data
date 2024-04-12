"""Plot histograms of zero-diameter aggregates."""
import sys
import numpy as np
import matplotlib.pyplot as plt
from common import set_figure, fig_size
from matplotlib import ticker

with np.load('./square_diameters_1_data.npz', allow_pickle=True) as data:
    data_clusters_with_tb    = data['data_clusters_with_tb']       # noqa
    data_clusters_without_tb = data['data_clusters_without_tb']    # noqa
    data_centers_with_tb     = data['data_centers_with_tb']        # noqa
    data_centers_without_tb  = data['data_centers_without_tb']     # noqa

ntests = data_clusters_with_tb.shape[0]
naggs = data_centers_with_tb.shape[1]

singletons_with_tb = np.full(ntests, -1)
singletons_without_tb = np.full(ntests, -1)
for testid in range(ntests):
    # calculate the number of occurrences for each aggregate id (ie aggregate size)
    cluster_size_with_tb = np.bincount(data_clusters_with_tb[testid, :])
    cluster_size_without_tb = np.bincount(data_clusters_without_tb[testid, :])

    # check that we're finding everything
    assert len(cluster_size_with_tb) == naggs
    assert len(cluster_size_without_tb) == naggs

    singletons_with_tb[testid] = np.count_nonzero(cluster_size_with_tb == 1)
    singletons_without_tb[testid] = np.count_nonzero(cluster_size_without_tb == 1)

fs = fig_size.singlefull
set_figure(width=fs['width'], height=(1/3)*fs['width'])
fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True)

x = np.arange(0, singletons_without_tb.max() + 0.5, dtype=int)
y = np.array([np.count_nonzero(singletons_without_tb == s) for s in x])
x = x[1:]  # only plot >=1
y = y[1:]  # only plot >=1
ax[1].bar(x, y, align='center', color='tab:red')
for num, count in zip(x, y):
    ax[1].text(num, count+1.1, f'{count}',
               color='tab:gray', va='bottom', ha='center', fontsize=7)

x = np.arange(0, singletons_with_tb.max() + 1.5, dtype=int)
y = np.array([np.count_nonzero(singletons_with_tb == s) for s in x])
x = x[1:]  # only plot >=1
y = y[1:]  # only plot >=1
ax[0].bar(x, y, align='center', color='tab:blue')
for num, count in zip(x, y):
    ax[0].text(num, count+1.1, f'{count}',
               color='tab:gray', va='bottom', ha='center', fontsize=7)

ax[1].set_title('Without tiebreaking')
ax[0].set_title('With tiebreaking')

ax[0].set_ylabel('Count')

ax[1].set_xlabel(r'\# of zero-diameter aggregates')
ax[0].set_xlabel(r'\# of zero-diameter aggregates')

ax[1].yaxis.tick_right()

ax[1].set_xticks(np.array([1, 2, 3, 4, 5]))
ax[0].set_xticks(np.array([1, 2, 3, 4, 5]))

ax[0].set_yscale('log')
ax[1].set_yscale('log')

ax[0].set_xlim(0.25, 5.5)
ax[1].set_xlim(0.25, 5.5)
ax[0].set_ylim(0.7, 2500)
ax[1].set_ylim(0.7, 2500)

ax[0].set_yticks([1, 10, 100, 1000])
ax[1].set_yticks([1, 10, 100, 1000])
ax[0].yaxis.set_minor_locator(ticker.FixedLocator(
    [k * 10**n for n in range(0, 3) for k in range(2, 10)]))

ax[0].set_yticklabels(['1', '10', '100', '1000'])
ax[1].set_yticklabels(['1', '10', '100', '1000'])

figname = 'square_diameters_zero.pdf'
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
