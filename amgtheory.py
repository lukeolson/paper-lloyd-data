import numpy as np
import scipy.linalg as sla
import scipy.sparse as sparse

def betahat(A, P):
    r"""
    betahat

    b^  = sup ||Te||^2_A/||T e||^2_{A D^-1 A}
        = sup <T' A T e, e> / <T' A D^-1 A T e, e>

    T' A T e = l A D^-1 A e

    instead use

    b^ = sup inf ||e - Pv ||^2_D / ||e||^2_A

    Pv = P (P' D P)^{-1} P D e
    T = I - P (P' D P)^{-1} P D
    b^ = sup || Te ||^2_D / ||e||^2_A
       = sup < T' D T e, e > / < A e, e >
    """
    D = np.diag(np.diag(A))
    I = np.eye(A.shape[0])

    PDPinv = sla.inv(P.T @ D @ P)
    T = I - P @ PDPinv @ P.T @ D
    C = T.T @ D @ T
    B = A

    eigval, eigvec = sla.eig(C,b=B)
    idx = np.argmax(np.abs(eigval))
    bhat = eigval[idx]
    bhatvec = eigvec[:,idx]

    Tbhatvec = T @ bhatvec
    DTbhatvec = D @ Tbhatvec
    return bhat, bhatvec, Tbhatvec, DTbhatvec

def alphahat(A, P, ml):
    r"""
    alphahat
    equation (31)

    a^  = inf (||e||^2_A - ||Ge||^2_A)/||T e||^2_{A D^-1 A}
        = inf <(A - G' A G) e, e>/<A D^-1 A T e, T e>

    (A - G' A G) v = l T' A D^-1 A T v
    """
    Ac = ml.levels[1].A.toarray()
    P = ml.levels[0].P.toarray()
    N = A.shape[0]
    I = sparse.eye(N, N).toarray()
    Dinv = np.array(np.diag(1.0 / np.diagonal(A)))
    Acinv = np.linalg.inv(Ac)
    T = I - P @ Acinv @ P.T @ A
    omega = 4/5
    G = I - omega * Dinv @ A

    Dinv = np.diag(1.0 / np.diagonal(A))
    C = A - G.T @ A @ G
    B = T.T @ A @ Dinv @ A @ T

    eigval, eigvec = sla.eig(C,b=B)
    ahat = abs(eigval).min()
    return ahat, eigval, eigvec
