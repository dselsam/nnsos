import numpy as np
import sympy as sp
import gzip
import os
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
            return ds

    seen = set()
    for q_degree in range((max_degree // 2) + 1):
        for p_degrees in enum_p_degrees(max_degree - 2 * q_degree):
            p_degrees.sort()
            if tuple(p_degrees) not in seen:
                yield q_degree, p_degrees
                seen.add(tuple(p_degrees))

def enum_qps(ipolys, max_degree, max_qps):
    """
    Enumerates sufficient information to generate (cyclic) sum-of-squares (SOS)
    problems.

    Args:
    - ipolys (dict): output of `enum_ipolys`
    - max_degree: max degree of the _expanded_ polynomial
    - max_qps: max number of (q, ps) pairs to generate

    Returns: list of (q, ps) pairs, where:
    - `util.csum(xs, q**2 * prod(ps))` is the input to an SOS problem
    - a representation of `q**2 * prod(ps)` is a sufficient "witness" to solve
    """
    n_qps = 0
    for q_degree, p_degrees in enum_qp_degrees(max_degree):
        for q in ipolys[(q_degree, False)]:
            seen_p = set()
            for ps in itertools.product(*[ipolys[(p_degree, True)] for p_degree in p_degrees]):
                if len(set(ps)) < len(ps): break
                p = util.prod(ps) # we use this as a convenient way to sort factors
                if p not in seen_p:
                    yield q, list(ps)
                    seen_p.add(p)
                    n_qps += 1
                    if max_qps is not None and n_qps >= max_qps: return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_filename', action='store', dest='in_filename', type=str, required=True, help="name of file generated by `enum_ipolys`")
    parser.add_argument('--out_filename', action='store', dest='out_filename', type=str, default=None)
    parser.add_argument('--n_datapoints', action='store', dest='n_datapoints', type=int, default=1)
    parser.add_argument('--max_degree', action='store', dest='max_degree', type=int, default=8)
    opts = parser.parse_args()

    if not os.path.exists(opts.in_filename): raise Exception("in_filename %s does not exist" % opts.in_filename)

    print("Reading from %s..." % opts.in_filename)
    with gzip.open(opts.in_filename, 'rb') as f:
        xs, stats, ipolys = pickle.load(f)

    if opts.out_filename is None:
        opts.out_filename = "qps__in_filename=%s_max_degree=%d_max_qps=%d" \
                            % (opts.in_filename, opts.max_degree, opts.n_datapoints)

    from tqdm import tqdm

    print("Writing to %s..." % opts.out_filename)
    with gzip.open(opts.out_filename, 'wb') as f:
        for qps in tqdm(enum_qps(ipolys=ipolys, max_degree=opts.max_degree, max_qps=opts.n_datapoints)):
            pickle.dump(qps, f)

    print("DONE")
