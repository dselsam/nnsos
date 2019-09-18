from nose.tools import assert_equals
from enum_sos import *
import util
import itertools

def test_enum_pq_degrees1():
    qps = list(enum_pq_degrees(max_degree=2))
    assert_equals(qps, [(0, [1, 1]), (0, [2]), (1, [])])
