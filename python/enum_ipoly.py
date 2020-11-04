import numpy as np
import sympy as sp
import gzip
import pickle
import collections
import itertools
import math
import functools
import util

def enum_umonomials(xs, max_degree):
    """
    Enumerates all unit monomials upto given degree.

    Args:
    - xs (list of sympy symbols): the variables composing the monomials
    - max_degree (int): the maximum degree of the monomials

    Returns:
    - List of unit monomials (as sympy terms).
    """
    cache = {}
    def enum_umonomials_core(idx, d_rest):
        if idx == len(xs) or d_rest == 0: return [1]
        elif (idx, d_rest) in cache:
            return cache[(idx, d_rest)]
        else:
            result = [xs[idx]**d * rest for d in range(0, d_rest+1) for rest in enum_umonomials_core(idx+1, d_rest - d)]
            cache[(idx, d_rest)] = result
            return result
    return enum_umonomials_core(0, max_degree)

def enum_ipolys(xs, max_degree, max_summands, max_coeff, max_ipolys):
    """
    Enumerates _some_ irreducible polynomials upto degree `max_degree`.

    Args:
    - xs (list of sympy symbols): the variables composing the monomials
    - max_degree (int): the maximum degree of the monomials
    - max_summands (int): the maximum number of summands in a polynomial
    - max_coeff (int): the maximum coefficient magnitude of a monomial
    - max_ipolys (int): the maximum number of irreducible polynomials to generate

    Returns:
    - stats (dict): statistics of the generation process
    - ipolys (dict): maps (degree, def_nneg) to a set of irreducible polynomials
    """
    stats = collections.defaultdict(int)
    ipolys = collections.defaultdict(set)

    for ums in util.flatten([itertools.combinations(enum_umonomials(xs, max_degree), n_summands) for n_summands in range(1, max_summands+1)]):
        d_poly = max([sp.total_degree(um) for um in ums])
        for cs in itertools.product(*([list(range(-max_coeff, 0) ) + list(range(1, max_coeff + 1))] * len(ums))):
            if all([c < 0 for c in cs]) or functools.reduce(math.gcd, cs) != 1: continue
            poly = sum([c * um for c, um in zip(cs, ums)])
            for ipoly in util.compute_ifactors(poly):
                d_ipoly = sp.total_degree(ipoly)
                def_nneg = not util.contains_negation(ipoly)
                if ipoly in ipolys[(d_ipoly, def_nneg)]:
                    stats['n_dups_%d' % d_ipoly] += 1
                else:
                    stats['n_new_%d' % d_ipoly] += 1
                    ipolys[(d_ipoly, def_nneg)].add(ipoly)
                    stats['n_ipolys'] += 1
                    if stats['n_ipolys'] > 0 and stats['n_ipolys'] % 1000 == 0: print(dict(stats))
                    if max_ipolys is not None and stats['n_ipolys'] >= max_ipolys: return stats, ipolys

    return stats, ipolys

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_vars', action='store', dest='n_vars', type=int, default=3)
    parser.add_argument('--max_degree', action='store', dest='max_degree', type=int, default=4)
    parser.add_argument('--max_summands', action='store', dest='max_summands', type=int, default=3)
    parser.add_argument('--max_coeff', action='store', dest='max_coeff', type=int, default=3)
    parser.add_argument('--max_ipolys', action='store', dest='max_ipolys', type=int, default=1000000)
    parser.add_argument('--out_filename', action='store', dest='out_filename', type=str, default=None)
    opts = parser.parse_args()

    if opts.out_filename is None:
        opts.out_filename = "ipolys_n_vars=%d_max_degree=%d_max_summands=%d_max_coeff=%d_max_ipolys=%d" \
                            % (opts.n_vars, opts.max_degree, opts.max_summands, opts.max_coeff, opts.max_ipolys)

    xs = [sp.Symbol("x%d" % (i+1), real=True) for i in range(opts.n_vars)]
    stats, ipolys = enum_ipolys(xs,
                                max_degree=opts.max_degree,
                                max_summands=opts.max_summands,
                                max_coeff=opts.max_coeff,
                                max_ipolys=opts.max_ipolys)

    print("Writing to %s..." % opts.out_filename)
    with gzip.open(opts.out_filename, 'wb') as f:
        pickle.dump((xs, stats, ipolys), f)

    print("DONE")
