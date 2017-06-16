import itertools

import test
import parser

def set_in_order(a, b):
    ''' Ensure b[1] >= a[1].

    >>> set_in_order([0,1], [2,3])
    ([0, 1], [2, 3])

    >>> set_in_order([0,3], [2,3])
    ([0, 3], [2, 3])

    >>> set_in_order([0,3], [1,2])
    ([1, 2], [0, 3])
    '''
    if b[1] < a[1]:
        return b,a
    return a,b

def union(a, b):
    ''' Compute the union of segments a and b.
    a and b are supposed to be in order (see set_in_order).

    >>> union([0,3], [2,4])
    [0, 4]

    >>> union([0,1], [2,3])
    [0, 3]

    >>> union([0,1], [3,4]) is None
    True
    '''
    xa, ya = a
    xb, yb = b
    if ya + 1 >= xb:
        return [min(xa, xb), yb]
    return None

def inter(a, b):
    ''' Compute the intersection of segments a and b.
    a and b are supposed to be in order (see set_in_order).

    >>> inter([0,3], [2,4])
    [2, 3]

    >>> inter([0,1], [2,3]) is None
    True

    >>> inter([0,1], [3,4]) is None
    True
    '''
    xa, ya = a
    xb, yb = b
    if ya >= xb:
        return [max(xa, xb), ya]
    return None

def compute_all_union_and_inter(m, res=None):
    if not res:
        res = [m]
    for i, j in itertools.combinations(range(len(m)), 2):
        a,b = set_in_order(m[i], m[j])
        aUb, aNb = union(a, b), inter(a, b)
        if aUb:
            new_multiseg = m[:]
            new_multiseg[i] = aUb
            if aNb:
                new_multiseg[j] = aNb
            else:
                new_multiseg.pop(j)
            if new_multiseg not in res:
                res.append(new_multiseg)
                compute_all_union_and_inter(new_multiseg, res)
    return res

if __name__ == '__main__':
    import doctest
    doctest.testmod()
