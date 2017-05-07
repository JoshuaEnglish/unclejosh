# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 11:58:26 2016

@author: jenglish
"""


def spread(n):
    """return a list of n-length of floats evenly distributed between
    0 and 1 inclusive.
    """

    if n < 1:
        raise ValueError("Non negative numbers only")
    if n == 1:
        return [0.0]

    res = []
    for x in range(0, n):
        res.append((x)/float(n-1))

    return res


if __name__ == '__main__':
    for x in range(1, 7):
        print(x, spread(x))
