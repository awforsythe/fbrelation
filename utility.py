'''
`fbrelation.utility`

Defines utility functions for use throughout the library.
'''

def find(f, xs):
    '''
    Iterates over xs and returns the first element x for which f(x) is True.
    Returns None if no such element is found.
    '''
    for x in xs:
        if f(x):
            return x
    return None
