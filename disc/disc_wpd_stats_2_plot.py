"""Plot WPD."""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
# UnivariateSpline = InterpolatedUnivariateSpline

from common import set_figure, fig_size

with np.load('disc_wpd_stats_0_output.npz', allow_pickle=True) as data:
    cx = data['cx']
    rho = data['rho']
    ppa = data['ppa']
    levs = data['levs']

fs = fig_size.singlefull
set_figure(width=fs['width'], height=0.8*fs['height'])

fig, ax = plt.subplots()

alllabels = []

data = cx / -np.log10(rho)
ax.violinplot(data.T, ppa,
              showmeans=False,
              showextrema=False,
              showmedians=False,
              )

xs = np.linspace(ppa.min(), ppa.max(), 100)
spl = UnivariateSpline(ppa, np.mean(data, axis=1), k=3)
ax.plot(xs, spl(xs), color='tab:blue', linestyle='-', lw=1.0)

if False:
    spl = UnivariateSpline(ppa, np.percentile(data, q=95, axis=1), k=3)
    label595 = ax.plot(xs, spl(xs), color='tab:blue', linestyle=':', lw=0.5,
                       label=r'5\textsuperscript{th}, 95\textsuperscript{th} percentile')
    alllabels += label595

    spl = UnivariateSpline(ppa, np.percentile(data, q=5, axis=1), k=3)
    ax.plot(xs, spl(xs), color='tab:blue', linestyle=':', lw=0.5)

labelwpd = ax.plot(ppa, np.mean(data, axis=1),
                   'o', markerfacecolor='w', color='tab:blue',
                   markeredgewidth=0.5, ms=3, label='average WPD')
alllabels += labelwpd

ax.set_ylabel(r'WPD=$\frac{\chi}{-\log_{10} \rho}$', color='tab:blue')
ax.set_xlabel('Average number of points per aggregate')
ax.tick_params(axis='y', color='tab:blue', labelcolor='tab:blue')
ax.set_xticks(ppa)

ax2 = ax.twinx()

data = rho
vp = ax2.violinplot(data.T, ppa,
                    showmeans=False,
                    showextrema=False,
                    showmedians=False,
                    )
for v in vp['bodies']:
    v.set_facecolor('tab:red')
    v.set_alpha(0.15)

spl = UnivariateSpline(ppa, np.mean(data, axis=1), k=3)
ax2.plot(xs, spl(xs), color='tab:red', linestyle='-', lw=1.0)

if False:
    spl = UnivariateSpline(ppa, np.percentile(data, q=95, axis=1), k=3)
    ax2.plot(xs, spl(xs), color='tab:red', linestyle=':', lw=0.5)

    spl = UnivariateSpline(ppa, np.percentile(data, q=5, axis=1), k=3)
    ax2.plot(xs, spl(xs), color='tab:red', linestyle=':', lw=0.5)

labelrho = ax2.plot(ppa, np.mean(data, axis=1),
                    'o', markerfacecolor='w', color='tab:red',
                    markeredgewidth=0.5, ms=3, label=r'average $\rho$')
alllabels += labelrho
ax2.tick_params(axis='y', color='tab:red', labelcolor='tab:red')
ax2.set_ylabel(r'$\rho$', color='tab:red')

labs = [eachlabel.get_label() for eachlabel in alllabels]
ax.legend(alllabels, labs,
          bbox_to_anchor=(0.3, 0.9), loc='upper left')

figname = 'disc_wpd_stats.pdf'
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
