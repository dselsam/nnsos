from nose.tools import assert_equals
from enum_sos import *
import util
import itertools

def test_enum_qp_degrees1():
    qps = list(enum_qp_degrees(max_degree=2))
    assert_equals(qps, [(0, [1, 1]), (0, [2]), (1, [])])

def test_enum_qps1():
    d0f, d0t, d1f_1, d1f_2, d1t_1, d1t_2, d2f_1, d2f_2, d2t_1, d2t_2 = \
      sp.symbols('d0f d0t d1f_1 d1f_2 d1t_1 d1t_2 d2f_1 d2f_2 d2t_1y d2t_2')

    ipolys = {
        (0, False) : [d0f],
        (0, True)  : [d0t],
        (1, False) : [d1f_1, d1f_2],
        (1, True)  : [d1t_1, d1t_2],
        (2, False) : [d2f_1, d2f_2],
        (2, True)  : [d2t_1, d2t_2]
    }

    qps = list(enum_qps(ipolys, max_degree=2, max_qps=None))
    assert_equals(qps, [
        (d0f, [d1t_1, d1t_1]),
        (d0f, [d1t_1, d1t_2]),
        (d0f, [d1t_2, d1t_2]),

        (d0f, [d2t_1]),
        (d0f, [d2t_2]),

        (d1f_1, []),
        (d1f_2, [])
    ])
