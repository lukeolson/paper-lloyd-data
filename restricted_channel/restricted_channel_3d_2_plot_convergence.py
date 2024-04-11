"""Plot 3d channel convergence."""
import numpy as np
import matplotlib.pyplot as plt
from common import set_figure, fig_size

data = np.load('./restricted_channel_3d_1_output_convergence_data.npz')
res_lloyd = data['res_lloyd']
res_rblloyd = data['res_rblloyd']
cycle_cx_lloyd = data['cycle_cx_lloyd']
cycle_cx_rblloyd = data['cycle_cx_rblloyd']

rho_lloyd = (res_lloyd[-1]/res_lloyd[-1-5])**(1/5)
wpd_lloyd = cycle_cx_lloyd / (-np.log10(rho_lloyd))

rho_rblloyd = (res_rblloyd[-1]/res_rblloyd[-1-5])**(1/5)
wpd_rblloyd = cycle_cx_rblloyd / (-np.log10(rho_rblloyd))

fs = fig_size.single12
set_figure(width=fs['width'], height=fs['height'])
fig, ax = plt.subplots()
ax.semilogy(res_lloyd, label='Standard Lloyd', color='tab:red', solid_capstyle='round')
ax.semilogy(res_rblloyd, label='Rebalanced Lloyd', color='tab:green', solid_capstyle='round')
ax.set_xlabel('Iterations')
ax.set_ylabel(r'$\|r\|$')
ax.grid(True)
ax.legend()
ax.text(0.6, 0.4, f'WPD={wpd_lloyd:.1f}', fontsize=6,
        color='tab:red', ha='left', transform=ax.transAxes)
ax.text(0.35, 0.1, f'WPD={wpd_rblloyd:.1f}', fontsize=6,
        color='tab:green', ha='left', transform=ax.transAxes)

figname = 'restricted_channel_3d_convergence.pdf'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight')
else:
    plt.show()
