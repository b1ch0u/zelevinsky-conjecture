import subprocess

import test
import parser
import union_inter

PATH_TO_KL_CALCULATOR = '../kl/kl'
TMP_FILENAME = 'multisegm'

def perm_to_str(perm, length=0):
    ''' Transform a permutation to string.
    If len(perm) < length, the string is completed with increasing digits to
    make it reach the correct length.

    >>> perm_to_str([0])
    '0'

    >>> perm_to_str([2,0,1])
    '201'

    >>> perm_to_str([2,0,1], length=5)
    '20134'

    >>> perm_to_str([3,2,0,1], length=4)
    '3201'
    '''
    return ''.join(map(str, perm)) \
            + ''.join(map(str, range(len(perm), length)))

def write_all_perm_pairs(m_perm, all_perms, filename):
    with open(filename, 'w') as f:
        for n in all_perms:
            f.write(perm_to_str(m_perm) \
                    + ' ' \
                    + perm_to_str(n, length=len(m_perm)) \
                    + '\n')

def str_I_from_Z(sub_values):
    def str_monomial(a, n):
        return '{} * Z({})'.format(a, n)
    s  = 'I({}) = \n{}'
    s = s.format(sub_values[0][1],
            '\n + '.join([str_monomial(a, n) for a,n in sub_values]))
    return s

def evaluate_in_1(poly):
    ''' Evaluate a given polynomial in 1,
    effectively calculating the sum of its coefficients.

    >>> evaluate_in_1([0])
    0

    >>> evaluate_in_1([0, 1])
    1

    >>> evaluate_in_1([0, 1, 4])
    5
    '''
    return sum(map(int, poly))

def call_kl_and_evaluate_polys(sub_w, m):
    write_all_perm_pairs(sub_w[0][1], [w[1] for w in sub_w], TMP_FILENAME)
    instr = [PATH_TO_KL_CALCULATOR, str(len(m)),TMP_FILENAME]
    prog_out = subprocess.run(instr,
                                stdout=subprocess.PIPE,
                                universal_newlines=True).stdout.split('\n')[:-1]
    return [evaluate_in_1(line.split(' ')[-2].split(',')) for line in prog_out]

def handle_str(s):
    m = parser.multisegment_from_str(s)
    sub_multisegments = union_inter.compute_all_union_and_inter(m)
    sub_w = [(n, test.find_standard_form(n)[0]['w']) for n in sub_multisegments]
    a_values = call_kl_and_evaluate_polys(sub_w, m)
    sub_values = list((zip(a_values, sub_multisegments)))
    return sub_values

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    res = handle_str(input('enter a multisegment: '))
    print (str_I_from_Z(res))
