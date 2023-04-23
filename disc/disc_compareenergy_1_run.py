"""Compare the AMG energy per aggregate in standard, balanced, and rebalanced Lloyd."""
import numpy as np
import pyamg

import amgtheory


def energy_per_aggregate(ml, e, Te, DTe):
    """Calculate the energy per aggregate."""
    energy = np.zeros(ml.levels[0].P.shape[1])
    AggOp = ml.levels[0].AggOp
    A = ml.levels[0].A
    Aee = np.dot(A @ e, e)

    for aggnum, agg in enumerate(AggOp.T):
        aggids = agg.indices
        energy[aggnum] = np.abs(np.vdot(DTe[aggids], Te[aggids]) / Aee)
    return energy


def main():
    print('loading problem...')
    with np.load('./disc_n=528_mesh_and_matrix.npz', allow_pickle=True) as data:
        A = data['A'].tolist()
        V = data['V']
        E = data['E']

    # mainseed = 35583
    # mainseed = 100987
    mainseed = 239999
    # mainseed = 898767

    print('test 1...')
    np.random.seed(mainseed)
    ml = pyamg.smoothed_aggregation_solver(A,
                                           aggregate=('balanced lloyd',
                                                      {'measure': 'inv',
                                                       'ratio': 1/8,
                                                       'pad': 0.01,
                                                       'maxiter': 5,
                                                       'rebalance_iters': 4,
                                                       }
                                                      ),
                                           strength='evolution',
                                           max_coarse=10,
                                           max_levels=2,
                                           keep=True,
                                           )

    beta, e, Te, DTe = amgtheory.betahat(A.toarray(), ml.levels[0].P.toarray())
    print('Rebalanced lloyd beta: ', beta)

    energy = energy_per_aggregate(ml, e, Te, DTe)
    print('rebalanced max energy', energy.max(), energy.sum())
    AggOp_blloyd54 = ml.levels[0].AggOp
    energy_blloyd54 = energy

    n = A.shape[0]
    u0 = np.random.rand(n)
    u = np.random.rand(n)
    u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u  # project out vector of 1s
    b = A @ u
    res = []
    _ = ml.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res)

    res_blloyd54 = res

    print('test 2...')

    np.random.seed(mainseed)
    ml = pyamg.smoothed_aggregation_solver(A,
                                           aggregate=('balanced lloyd',
                                                      {'measure': 'inv',
                                                       'ratio': 1/8,
                                                       'pad': 0.01,
                                                       'maxiter': 5,
                                                       'rebalance_iters': 0,
                                                       }),
                                           strength='evolution',
                                           max_coarse=10,
                                           max_levels=2,
                                           keep=True,
                                           )

    beta, e, Te, DTe = amgtheory.betahat(A.toarray(), ml.levels[0].P.toarray())
    print('balanced lloyd beta: ', beta)

    energy = energy_per_aggregate(ml, e, Te, DTe)
    print('balanced max energy', energy.max(), energy.sum())
    AggOp_blloyd50 = ml.levels[0].AggOp
    energy_blloyd50 = energy

    n = A.shape[0]
    u0 = np.random.rand(n)
    u = np.random.rand(n)
    u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u  # project out vector of 1s
    b = A @ u
    res = []
    _ = ml.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res)

    res_blloyd50 = res

    print('test 3...')
    np.random.seed(mainseed)
    ml = pyamg.smoothed_aggregation_solver(A,
                                           aggregate=('lloyd', {'measure': 'inv',
                                                                'ratio': 1/8,
                                                                'maxiter': 5,
                                                                }),
                                           strength='evolution',
                                           max_coarse=10,
                                           max_levels=2,
                                           keep=True,
                                           )

    beta, e, Te, DTe = amgtheory.betahat(A.toarray(), ml.levels[0].P.toarray())
    print('lloyd beta: ', beta)

    energy = energy_per_aggregate(ml, e, Te, DTe)
    print('lloyd max energy', energy.max(), energy.sum())

    AggOp_lloyd5 = ml.levels[0].AggOp
    energy_lloyd5 = energy

    n = A.shape[0]
    u0 = np.random.rand(n)
    u = np.random.rand(n)
    u = u - (np.inner(u, np.ones(n)) / np.inner(u, u)) * u  # project out vector of 1s
    b = A @ u
    res = []
    _ = ml.solve(b, x0=u0, tol=1e-12, maxiter=200, residuals=res)

    res_lloyd5 = res

    np.savez('disc_compareenergy_1_output.npz',
             AggOp_blloyd54=AggOp_blloyd54, energy_blloyd54=energy_blloyd54,
             AggOp_blloyd50=AggOp_blloyd50, energy_blloyd50=energy_blloyd50,
             AggOp_lloyd5=AggOp_lloyd5, energy_lloyd5=energy_lloyd5,
             res_blloyd54=res_blloyd54,
             res_blloyd50=res_blloyd50,
             res_lloyd5=res_lloyd5,
             V=V, E=E, A=A)


if __name__ == '__main__':
    main()
