''' Test the correct behavior of everything.
    For valid multisegments, test(m) should return a unique solution.

    >>> valid_multisegments = [ \
            [[1,2], [2,2], [3,3]], \
            [[2,1], [1,2], [2,2], [3,3]], \
            [[3,2], [1,2], [2,2], [3,3]], \
            [[1,3], [2,2]], \
            [[2,5], [1,3], [2,2], [3,3]], \
            [[2,3], [1,3], [2,2], [3,3]], \
            [[1,3], [2,2], [3,3]], \
            [[0,4], [1,3], [5,6], [3,3]], \
            [[2,5], [1,3], [2,2], [3,3]], \
            [[2,5], [1,3], [2,2], [3,3], [12, 14], [1,0], [4,5], [8,10]], \
            [[2,5], [1,3], [2,2], [3,3], [12, 14], [4,5], [8,10]] \
            ]

    >>> invalid_multisegments = [ \
            [[12, 4], [2,5], [1,3], [2,2], [3,3], [1,0], [4,5], [8,10]], \
            [[3,1], [1,2], [2,2], [3,3]], \
            ]

    >>> for m in valid_multisegments: \
            assert len(find_standard_form(m)) == 1

    >>> for m in invalid_multisegments: \
            assert len(find_standard_form(m)) != 1
''' # TODO add more precise tests
import itertools

def inv_nb(perm):
    ''' Compute the number of inversions in perm.
    This corresponds to the length in A_n. (prop 1.5.2 page 20).

    >>> inv_nb([0])
    0

    >>> inv_nb([0,1])
    0

    >>> inv_nb([1,0])
    1

    >>> inv_nb([2,0,3,1])
    3
    '''
    res = 0
    for i in range(len(perm) - 1):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                res += 1
    return res

def dot(w, mu):
    ''' Compute w * mu.

    >>> dot([0], [7])
    [7]

    >>> dot([0,1], [5,8])
    [5, 8]

    >>> dot([0,1,2], [4,6,9])
    [4, 6, 9]

    >>> dot([2,0,1], [4,6,9])
    [5, 8, 6]
    '''
    n = len(w)
    id_vect = list(iter(range(n)))
    w_inv = perm_inv(w)
    mu_inv = [mu[w_inv[i]] for i in range(n)]
    return [mu_inv[i] - w_inv[i] + id_vect[i] for i in range(n)] # +1 from id_vect being from 0 to n-1 rather than 1 to n

def compute_stabilizer(mu):
    ''' Compute the stabilizer of mu, according to the dot product.'''
    n = len(mu)
    res = []
    for perm in itertools.permutations(range(n)):
        if dot(perm, mu) == mu:
            res.append(perm)
    return res

def dominates(u, v):
    ''' Test if u dominates v.
    u is said to dominate v if u_i >= v_i for all i.

    >>> dominates([1], [0])
    True

    >>> dominates([1,1], [0,1])
    True

    >>> dominates([1,1,1], [0,1,2])
    False
    '''
    return all(u_i >= v_i for u_i,v_i in zip(u, v))

def is_dk(v):
    ''' Test if v is in D_k.
    Elems of D_k are those  v such that v1 - 1 >= v2 - 2 >= ... >= v_k - k.

    >>> is_dk([0])
    True

    >>> is_dk([0,1])
    True

    >>> is_dk([1,3])
    False

    >>> is_dk([1,2,0,5])
    False

    >>> is_dk([3,2,0,1])
    True
    '''
    d = [e - (i + 1) for i,e in enumerate(v)] # the +1 comes from python's
                                                # indexing from 0
    return all(d[i] >= d[i + 1] for i in range(len(d) - 1))

def compute_double_coset(H, x, G):
    ''' Compute the double coset HxG.

    >>> compute_double_coset([(0,1)], (0,1), [(0,1)])
    [[0, 1]]

    >>> compute_double_coset([(0,1), (1,0)], (0,1), [(0,1)])
    [[0, 1], [1, 0]]

    >>> compute_double_coset([(0,1,2), (2,0,1), (1,2,0)], (0,2,1), [(0,1,2)])
    [[0, 2, 1], [2, 1, 0], [1, 0, 2]]

    >>> compute_double_coset([(0,1,2,3)], (0,2,3,1), [(0,1,2,3), (3,1,2,0)])
    [[0, 2, 3, 1], [1, 2, 3, 0]]
    '''
    def triple_product(a, b, c):
        return [a[b[e]] for e in c]
    return [triple_product(h, x, g) for h in H for g in G]

def find_possible_lambdas(m):
    ''' Find the possible values of lambda such that lambda / (w * mu) = m.'''
    res = []
    for order in itertools.permutations(m):
        cur_lambda = [i + 1 + e[1] for i,e in enumerate(order)]
        if is_dk(cur_lambda):
            res.append((cur_lambda, order))
    return res

def perm_inv(w):
    ''' Inverse a permutation w.

    >>> perm_inv([])
    []

    >>> perm_inv([0])
    [0]

    >>> perm_inv([0,1])
    [0, 1]

    >>> perm_inv([0,1,2])
    [0, 1, 2]

    >>> perm_inv([0,2,1])
    [0, 2, 1]

    >>> perm_inv([4,0,3,2,1])
    [1, 4, 3, 2, 0]
    '''
    res = [0] * len(w)
    for i,e in enumerate(w):
        res[e] = i
    return res

def find_possible_wmu(l, order, k):
    # TODO convert to np arr
    res = []
    wmu = [e[0] + i for i,e in enumerate(order)]
    if not dominates(l, wmu): # standard form requires : lambda >= w*mu
        return []
    for w_inv in itertools.permutations(range(k)):
        wmu_minus_id = [a - b for a,b in zip(wmu, range(0, k))]
        mu_inv = [a + b for a,b in zip(wmu_minus_id, w_inv)]
        w = perm_inv(w_inv)
        mu = [mu_inv[w[i]] for i in range(k)]
        if is_dk(mu):
            res.append((w, mu, wmu))
    return res

def find_standard_form(m):
    ''' Find possible lambda, w and mu for the standard form.'''
    res = []
    possible_lambdas = find_possible_lambdas(m)
    for e in possible_lambdas:
        l, o = e
        l_stabilizer = compute_stabilizer(l)

        possible_wmu = find_possible_wmu(l, o, len(m))
        for w, mu, wmu in possible_wmu:
            mu_stabilizer = compute_stabilizer(mu)
            double_coset = compute_double_coset(l_stabilizer, w, mu_stabilizer)
            has_max_size = (inv_nb(w) == max(inv_nb(x) for x in double_coset))
            if has_max_size:
                res.append({'lambda': l,
                            'mu': mu,
                            'w': w,
                            'wmu': wmu,
                            'order': o,
                            'lambda stabilizer': l_stabilizer,
                            'mu stabilizer': l_stabilizer,
                            'double coset': double_coset,
                            })
    return res

if __name__ == '__main__':
    import doctest
    doctest.testmod()
