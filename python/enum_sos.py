import numpy as np
import sympy as sp
import gzip
import pickle
import collections
import itertools
import math
import functools
import util

def enum_qp_degrees(max_degree):
    p_degrees_cache = {}

    def enum_p_degrees(d_rest):
        if d_rest == 0:
            return [[]]
        elif d_rest in p_degrees_cache:
            return p_degrees_cache[d_rest]
        else:
            ds = [[d_next] + rest for d_next in range(1, d_rest+1) for rest in enum_p_degrees(d_rest - d_next)]
            p_degrees_cache[d_rest] = ds
            print(d_rest, ds)
            return ds

    for q_degree in range((max_degree // 2) + 1):
        for p_degrees in enum_p_degrees(max_degree - 2 * q_degree):
            yield q_degree, p_degrees


def enum_qps(ipolys, max_degree, max_datapoints):
    """
    Enumerates sufficient information to generate (cyclic) sum-of-squares (SOS)
    problems.

    Args:
    - ipolys (dict): output of `enum_ipolys`
    - max_degree: max degree of the _expanded_ polynomial
    - max_datapoints: max number of datapoints to generate

    Returns: list of (q, p) pairs, where:
    - `util.csum(xs, q**2 * p)` is the input to an SOS problem
    - some representation of `q**2 * p` is a sufficient "witness" to solve
    """
    n_datapoints = 0
    for q_degree, p_degrees in enum_qp_degrees(max_degree):
        for q in ipolys[(q_degree, False)]:
            seen_ps = set()
            for ps in itertools.product(*[ipolys[(p_degree, True)] for p_degree in p_degrees]):
                ps = sorted(ps) # so [x, y, x] is detected as the same as [x, x, y]
                if str(ps) not in seen_ps: # list is not hashable
                    yield q, ps
                    seen_ps.add(str(ps))
                    n_datapoints += 1
                    if max_datapoints is not None and n_datapoints >= max_datapoints: break

if __name__ == "__main__":
    pass
