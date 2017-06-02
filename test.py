import itertools

def dominates(u, v):
    ''' u is said to dominate v if u_i >= v_i for all i.'''
    return all(u_i >= v_i for u_i,v_i in zip(u, v))

def is_dk(v):
    ''' D_k is the set of v such that v1 - 1 >= v2 - 2 >= ... >= v_k - k.'''
    d = [e - (i + 1) for i,e in enumerate(v)] # the +1 comes from python's
                                                # indexing from 0
    return all(d[i] >= d[i + 1] for i in range(len(d) - 1))


def find_possible_lambdas(m):
    ''' find the possible values of lambda such that lambda / (w * mu) = m.'''
    res = []
    for order in itertools.permutations(m):
        cur_lambda = [i + 1 + e[1] for i,e in enumerate(order)]
        if is_dk(cur_lambda):
            res.append((cur_lambda, order))
    return res

def perm_inv(w):
    res = [0] * len(w)
    for i,e in enumerate(w):
        res[e] = i
    return res

def find_possible_wmu(l, order, k):
    # TODO convert to np arr
    res = []
    wmu = [e[0] + i for i,e in enumerate(order)]
    if not dominates(l, wmu): # lambda must be >= w*mu in standard form
        return []
    for w_tilde in itertools.permutations(range(k)):
        wmu_minus_id = [a - b for a,b in zip(wmu, range(0, k))]
        mu_tilde = [a + b for a,b in zip(wmu_minus_id, w_tilde)]
        w = perm_inv(w_tilde)
        mu = [mu_tilde[w[i]] for i in range(k)]
        if is_dk(mu):
            res.append((w, mu, wmu))
    return res

def test(m):
    print ('m:', m)
    possible_lambdas = find_possible_lambdas(m)
    for e in possible_lambdas:
        l, o = e
        print ('  lambda:', l)
        print ('  order:', o)

        possible_wmu = find_possible_wmu(l, o, len(m))
        for w, mu, wmu in possible_wmu:
            print ('    w:', w)
            print ('    mu:', mu)
            print ('    wmu:', wmu)
            print ('')

if __name__ == '__main__':
    test([[1,2], [2,2], [3,3]])
    print ('---\n')
    test([[1,3], [2,2]])
