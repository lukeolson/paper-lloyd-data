"""Plot varying aggregate size."""
import matplotlib.pyplot as plt
import numpy as np
from pyamg.vis import aggviz
from common import set_figure, fig_size

data = np.load('disc_varynaggs_1_output.npz', allow_pickle=True)
datacore = np.load('disc_varynaggs_1_output2.npz', allow_pickle=True)
V = datacore['V']
E = datacore['E']
A = datacore['A'].tolist()

data = {d: data[d].tolist() for d in data.files}
naggslist = np.array(list(data.keys()))
# naggslist = naggslist.astype(float).astype(int)
print(naggslist)

fs = fig_size.singlefull
set_figure(width=fs['width'], height=(2/3)*fs['width'])
nrows = 2
ncols = 3
fig, ax = plt.subplots(nrows=nrows, ncols=ncols)

kwargs = {'color': '0.8',
          'edgecolor': 'tab:blue',
          'linewidth': 0.75}

print(len(naggslist))
for i, naggs in enumerate(naggslist):
    # print(i // ncols, i % ncols)
    axx = ax[i // ncols, i % ncols]
    AggOp = data[f'''{naggs}''']  # noqa
    mappable = aggviz.plotaggs(AggOp, V, A, ax=axx,
                               buffer=[0.07, -0.052],
                               **kwargs)

    axx.triplot(V[:, 0], V[:, 1], E, color='0.6', lw=0.25)
    axx.axis('off')
    axx.text(0.5, -0.05, f'{naggs}', horizontalalignment='center', transform=axx.transAxes)

figname = 'disc_varynaggs.pdf'
import sys  # noqa
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
