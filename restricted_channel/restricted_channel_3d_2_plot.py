"""Plot 3d channel convergence."""
import numpy as np
import matplotlib.pyplot as plt
from common import set_figure, fig_size

data = np.load('./restricted_channel_3d_1_output.npz')
res_lloyd = data['res_lloyd']
res_rblloyd = data['res_rblloyd']

fs = fig_size.single12
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots()
ax.semilogy(res_lloyd, label='Standard Lloyd', color='tab:red', solid_capstyle='round')
ax.semilogy(res_rblloyd, label='Rebalanced Lloyd', color='tab:green', solid_capstyle='round')
ax.legend()
ax.set_xlabel('Iterations')
ax.set_ylabel(r'$\|r\|$')
ax.grid(True)

figname = 'restricted_channel_3d_convergence.pdf'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
