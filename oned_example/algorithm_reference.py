import numpy as np
import matplotlib.pyplot as plt
import pyamg
from hashlib import sha1
from itertools import product
import os

from numpy.random import default_rng
seed = 44678
rng = default_rng(seed)

class arrayhash:
    def __init__(self, **kwargs):
        self.id = {}
        for name, array in kwargs.items():
            self.id[name] = sha1(array)

    def changed(self, **kwargs):
        flag = False
        for name, array in kwargs.items():
            newhash = sha1(array)
            if self.id[name].hexdigest() != newhash.hexdigest():
                flag = True
                self.id[name] = newhash
        return flag

def test_arrayhash():
    a = np.array([1,2,3])
    b = np.array([5,6,7])

    state = arrayhash(a=a, b=b)
    a[0] = 883.2
    assert state.changed(a=a, b=b)
    assert not state.changed(a=a, b=b)
    assert not state.changed(a=a, b=b)
    b[1] = 9
    assert state.changed(a=a, b=b)
    assert not state.changed(a=a, b=b)

def greedy_clustering(W):
    """Algorithm 2.1"""
    m = np.full(W.shape[0], -1)
    a = 0
    c = []  # ADD allocator
    for i in range(W.shape[0]):
        if m[i] == -1 and np.all(m[np.where(W[i, :])[0]] == -1):
            m[i] = a
            m[np.where(W[i, :])[0]] = a
            c.append(i)
            a = a + 1
    for i in range(W.shape[0]):
        if m[i] == -1:
            if len(np.where(m[np.where(W[i, :])[0]]>=0)[0]):
                J = np.where(m>=0)[0]
                j = J[np.argmax(W[i, J])]
                m[i] = m[j]
            else:
                m[i] = a
                for j in np.where(W[i, :])[0]:
                    m[j] = a if m[j] == -1 else m[j]
                a = a + 1
    return m, np.array(c)

def mis(W):
    """Greedy MIS."""
    c = np.full(W.shape[0], -1)
    J = rng.permutation(W.shape[0])
    for i in J:
        if c[i] != -1:
            continue
        c[i] = 1
        for j in np.where(W[i, :])[0]:
            if c[j] == -1:
                c[j] = 0
    return np.where(c)[0]

def mis2(W):
    """MIS(2) basedon W^2."""
    _W = W.copy()
    np.fill_diagonal(_W, 1.0)
    W2 = _W @ _W
    np.fill_diagonal(W2, 0.0)
    I = np.where(W2)
    W2[I] = 1.0
    c = mis(W2)
    return c

def mis2_clustering(W):
    """Algorithm 2.2"""
    c = mis2(W)
    m = np.full(W.shape[0], -1)
    for a in range(len(c)):
        i = c[a]
        m[i] = a
        for j in np.where(W[i, :]>0)[0]:
            m[j] = a

    for i in np.where(m>=0)[0]:
        for j in np.where(W[i, :]>0)[0]:
            m[j] = m[i] if m[j] == -1 else m[j]

    return m, c

def lloyd_clustering(W, c, Tmax):
    """Algorithm 2.3"""
    t = 0
    state = arrayhash(c=c, m=np.empty(W.shape[0]))
    while True:
        m, d = bellman_ford(W, c)
        c = most_interior_nodes(W, m)
        t = t + 1
        if t == Tmax or not state.changed(c=c, m=m):
            return m, c

def bellman_ford(W, c):
    """Algorithm 2.4"""
    d = np.full(W.shape[0], np.inf)
    m = np.full(W.shape[0], -1)
    for a in range(len(c)):
        i = c[a]
        d[i] = 0
        m[i] = a
    while True:
        done = True
        for i, j in zip(*np.where(W)):
            if d[i] + W[i, j] < d[j]:
                d[j] = d[i] + W[i, j]
                m[j] = m[i]
                done = False
        if done:
            break
    return m, d

def most_interior_nodes(W, m):
    """Algorithm 2.5"""
    B = set()
    c = np.full(m.max()+1, -1)  # ADD allocation
    for i, j in zip(*np.where(W)):
        if m[i] != m[j]:
            B.update((i, j))
    _m, d = bellman_ford(W, np.array(list(B)))
    for i in range(W.shape[0]):
        a = m[i]
        c[a] = i
    for i in range(W.shape[0]):
        a = m[i]
        j = c[a]
        if d[i] > d[j]:
            c[a] = i
    return c

def clustered_floyd_warshall(W, m):
    """Algorithm 3.1"""
    V = {a: np.where(m==a)[0] for a in range(m.max()+1)}
    D = np.zeros_like(W) # ADD allocation
    P = np.zeros_like(W) # ADD allocation
    for a in range(m.max()+1):
        for i, j in product(V[a], V[a]):
            D[i, j] = np.inf
            P[i, j] = -1
            if W[i, j] > 0:
                D[i, j] = W[i, j]
                P[i, j] = i
            if i == j:
                D[i, i] = 0
                P[i, i] = i
        for k in V[a]:
            for i, j in product(V[a], V[a]):
                if D[i, j] > D[i, k] + D[k, j]:
                    D[i, j] = D[i, k] + D[k, j]
                    P[i, j] = P[k, j]
    return D, P

def balanced_lloyd_clustering(W, c, Tmax, TBFmax):
    """Algorithm 3.2"""
    m, d, p, n, s = balanced_initialization(c, W.shape[0])
    state = arrayhash(c=c, m=m, d=d, p=p, n=n, s=s) # ADD state
    t = 0
    _, d0 = bellman_ford(W, c)
    energy = []
    print(f'{t=}: ', np.sum(d0**2))
    energy.append(np.sum(d0**2))
    while True:
        m, d, p, n, s = balanced_bellman_ford(W, m, c, d, p, n, s, TBFmax)
        D, P = clustered_floyd_warshall(W, m)
        c, d, p, n = center_nodes(W, m, c, d, p, n, D, P)
        t = t + 1
        print(f'{t=}: ', np.sum(d**2))
        energy.append(np.sum(d**2))
        if t == Tmax or not state.changed(c=c, m=m, d=d, p=p, n=n, s=s):
            if os.path.isfile('tmp_energy.npz'):
                data = np.load('tmp_energy.npz')
                energylist =[data[somekey] for somekey in data]
            else:
                energylist = []
            energylist.append(energy)
            np.savez('tmp_energy.npz', *energylist)
            return m, c, d, p, n, s, D, P

def balanced_initialization(c, Nnode):  # ADD Nnode
    """Algorithm 3.3"""
    m = np.full(Nnode, -1)
    d = np.full(Nnode, np.inf)
    p = np.full(Nnode, -1)
    n = np.full(Nnode, 0)
    s = np.full(len(c), 1)
    for a in range(len(c)):
        i = c[a]
        d[i] = 0
        m[i] = a
        p[i] = i
        n[i] = 1
    return m, d, p, n, s

def balanced_bellman_ford(W, m, c, d, p, n, s, TBFmax):
    """Algorithm 3.4"""
    t = 0
    while True:
        done = True
        for i, j in zip(*np.where(W)):
            si = s[m[i]] if m[i] >= 0 else 0
            sj = s[m[j]] if m[j] >= 0 else 0
            switch = False
            if d[i] + W[i, j] < d[j]:
                switch = True
            if d[i] + W[i, j] == d[j]:
                if si + 1 < sj:
                    if n[j] == 0:
                        switch = True
            if switch:
                s[m[i]] = si + 1; s[m[j]] = sj - 1
                m[j] = m[i]
                d[j] = d[i] + W[i, j]
                n[i] = n[i] + 1; n[p[j]] = n[p[j]] - 1
                p[j] = i
                done = False
            t = t + 1
        if t == TBFmax or done:
            break
    T = t
    return m, d, p, n, s

def center_nodes(W, m, c, d, p, n, D, P):
    """Algorithm 3.5"""
    V = {a: np.where(m==a)[0] for a in range(len(c))}
    q = np.zeros_like(d)  # ADD allocation
    for a in range(len(c)):
        for i in V[a]:
            q[i] = np.sum(D[i, V[a]]**2)
        i = c[a]
        for j in V[a]:
            if q[j] < q[i]:
                i = j
        if i != c[a]:
            c[a] = i
            n[V[a]] = 0
            for j in V[a]:
                d[j] = D[i, j]
                p[j] = P[i, j]
                n[p[j]] = n[p[j]] + 1
    return c, d, p, n

def rebalanced_lloyd_clustering(W, c, Tmax, TBFmax):
    """Algorithm 3.6"""
    t = 0
    state = arrayhash(c=c)
    while True:
        m, c, d, p, n, s, D, P = balanced_lloyd_clustering(W, c, Tmax, TBFmax)
        c = rebalance(W, m, c, d, p, D)
        t = t + 1
        if t == Tmax or not state.changed(c=c):
            return m, c, d, p, n, s, D, P

def rebalance(W, m, c, d, p, D):
    """Algorithm 3.7"""
    V = {a: np.where(m==a)[0] for a in range(len(c))}
    L = elmination_penalty(W, m, d, D)
    S, c1, c2 = split_improvement(m, d, D)
    M = np.full(len(c), 1, dtype=bool)
    Lsort = np.argsort(L)
    Ssort = np.argsort(S)
    iL = 0
    iS = len(c)-1
    while iL <= len(c)-1 and iS >= 0:
        aL = Lsort[iL]
        aS = Ssort[iS]
        if not M[aL] or aL == aS:
            iL = iL + 1
            continue
        if not M[aS]:
            iS = iS - 1
            continue
        delta = 0.0   # ADD what?
        if L[aL] >= S[aS] - delta:
            break
        mark_unavailable(aL, m, M, W, V[aL])
        mark_unavailable(aS, m, M, W, V[aS])
        c[aL] = c1[aS]
        c[aS] = c2[aS]
    return c

def elmination_penalty(W, m, d, D):
    """Algorithm 3.8"""
    V = {a: np.where(m==a)[0] for a in range(m.max()+1)}
    L = np.full(m.max()+1, 0)  # ADD allocation
    for a in range(m.max()+1):
        L[a] = 0
        for i in V[a]:
            dmin = np.inf
            for j in V[a]:
                for k in np.where(W[:, j])[0]:
                    if m[k] != m[j]:
                        if d[k] + W[k, j] + D[j, i] < dmin:
                            dmin = d[k] + W[k, j] + D[j, i]
            L[a] = L[a] + dmin**2
        L[a] = L[a] - np.sum(d[V[a]]**2)
    return L

def split_improvement(m, d, D):
    """Algorithm 3.9"""
    V = {a: np.where(m==a)[0] for a in range(m.max()+1)}
    S = np.full(m.max()+1, np.inf)  # ADD allocation
    c1 = np.full(m.max()+1, -1)  # ADD allocation
    c2 = np.full(m.max()+1, -1)  # ADD allocation
    for a in range(m.max()+1):
        S[a] = np.inf
        for i in V[a]:
            for j in V[a]:
                Snew = 0
                for k in V[a]:
                    if D[i, k] < D[j, k]:
                        Snew = Snew + D[i, k]**2
                    else:
                        Snew = Snew + D[j, k]**2
                if Snew < S[a]:
                    S[a] = Snew
                    c1[a] = i
                    c2[a] = j
        S[a] = np.sum(d[V[a]]**2) - S[a]
    return S, c1, c2

def mark_unavailable(a, m, M, W, Va):
    """Algorithm 3.10"""
    M[a] = False
    for i in Va:
        for j in np.where(W[i, :])[0]:
            M[m[j]] = False

if __name__ == '__main__':
    test_arrayhash()

    def plot_clustering(m, c, ax, n1d, title):
        nc = len(c)
        cm = plt.get_cmap('tab20')
        color = [cm(1.*i/nc) for i in range(nc)]
        rng.shuffle(color)
        x, y = np.mgrid[0:1:(n1d*1j),0:1:(n1d*1j)]
        for yy in y[0, :]:
            ax.hlines(yy, 0, 1, '0.8')
        for xx in x[:, 0]: ax.vlines(xx, 0, 1, '0.8')
        x = x.ravel()
        y = y.ravel()
        for i, mm in enumerate(m):
            if mm >= 0:
                ax.plot(x[i], y[i], color=color[mm],
                        marker='s', ms=4)
            if mm < 0:
                print(mm)
        for i, cc in enumerate(c):
            ax.plot(x[cc], y[cc], color=color[i],
                    marker='o', ms=6, label='center',
                    markerfacecolor='w', markeredgewidth=4)
        ax.axis('equal')
        ax.axis('off')
        ax.set_title(title)

    n1d = 15
    W = pyamg.gallery.poisson((n1d, n1d), format='csr')
    W.setdiag(0)
    W.eliminate_zeros()
    W.data[:] = 1.0
    W = W.toarray()

    fig, axs = plt.subplots(ncols=5, figsize=(12,3))

    m, c = mis2_clustering(W)
    plot_clustering(m, c, axs[0], n1d, title='MIS2')

    m, c = greedy_clustering(W)
    plot_clustering(m, c, axs[1], n1d, title='Greedy')

    Ncluster = len(c)
    Ncluster = 10
    c = rng.permutation(W.shape[0])[:Ncluster]
    m, d = lloyd_clustering(W, c, Tmax=5)
    plot_clustering(m, c, axs[2], n1d, title='Lloyd')

    Ncluster = len(c)
    Ncluster = 10
    c = rng.permutation(W.shape[0])[:Ncluster]
    m, c, d, p, n, s, D, P = balanced_lloyd_clustering(W, c, Tmax=5, TBFmax=5)
    plot_clustering(m, c, axs[3], n1d, title='Balanced Lloyd')

    Ncluster = len(c)
    Ncluster = 10
    c = rng.permutation(W.shape[0])[:Ncluster]
    m, c, d, p, n, s, D, P = rebalanced_lloyd_clustering(W, c, Tmax=5, TBFmax=5)
    plot_clustering(m, c, axs[4], n1d, title='Rebalanced Lloyd')

    plt.show()
