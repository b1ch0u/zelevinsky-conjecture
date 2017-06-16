import re

interval_re = re.compile('\\[(\\d+)[,\s]\s?(\\d+)\\]')

def multisegment_from_str(s):
    ''' Parse a string representing a multisegment.
    Any ill-formed segment will be ignored.

    >>> multisegment_from_str('[1,2]')
    [[1, 2]]

    >>> multisegment_from_str('[17,255]')
    [[17, 255]]

    >>> multisegment_from_str('[1,2] + [4, 6]')
    [[1, 2], [4, 6]]

    >>> multisegment_from_str('[1,2],[7,8]')
    [[1, 2], [7, 8]]

    >>> multisegment_from_str('[1, 2][3,4]')
    [[1, 2], [3, 4]]

    >>> multisegment_from_str('[12]')
    []

    >>> multisegment_from_str('1,2]')
    []
    '''
    all_tuples = re.findall(interval_re, s)
    return [[int(t[0]), int(t[1])] for t in all_tuples]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
