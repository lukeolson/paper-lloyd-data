"""Compare standard to lloyd to metis to rb lloyd methods."""
import numpy as np
import pyamg

with np.load('disc_allmethods_0_output.npz', allow_pickle=True) as data:
    A = data['A'].tolist()
    V = data['V']
    E = data['E']

seed = 9048
np.random.seed(seed)

aggregate = []

method = {'name': 'Greedy',
          'parameters': 'standard'}
aggregate.append(method)

method = {'name': 'METIS',
          'parameters': ('metis', {'measure': 'range',
                                   'ratio': 1/10})}
aggregate.append(method)

method = {'name': 'Lloyd',
          'parameters': ('lloyd', {'measure': 'inv'})}
aggregate.append(method)

method = {'name': 'Balanced Lloyd',
          'parameters': ('balanced lloyd', {'measure': 'inv',
                                            'ratio': 1/10,
                                            'pad': 0.01,
                                            'maxiter': 5,
                                            'rebalance_iters': 4})}
aggregate.append(method)

for method in aggregate:
    name = method['name']
    parameters = method['parameters']
    ml = pyamg.smoothed_aggregation_solver(A,
                                           aggregate=parameters,
                                           strength='evolution',
                                           max_coarse=10,
                                           max_levels=2,
                                           keep=True,
                                           )

    AggOp = ml.levels[0].AggOp
    method['AggOp'] = AggOp

np.savez('disc_allmethods_1_output.npz', A=A, V=V, E=E,
         aggregate=aggregate)
