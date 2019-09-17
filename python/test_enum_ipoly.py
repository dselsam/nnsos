from nose.tools import assert_equals
from enum_ipoly import *
import util
import itertools

def test_enum_umonomials1():
    xs = util.mkVars(["x", "y", "z"])
    ums = enum_umonomials(xs, 1)
    assert_equals(len(ums), 4)
    assert_equals(set(ums), set([1] + xs))

def test_enum_umonomials2():
    xs = util.mkVars(["x", "y", "z"])
    ums = enum_umonomials(xs, 2)
    assert_equals(len(ums), 10)
    assert_equals(set(ums), set([1] + xs + [x*y for x, y in itertools.product(xs, xs)]))

def test_enum_ipolys1():
    x, y = util.mkVars(["x", "y"])
    stats, ipolys = enum_ipolys(xs=[x, y], max_degree=2, max_summands=2, max_coeff=1, max_ipolys=None)
    assert_equals(set(ipolys[(1, False)]), {x - y, x - 1, y - 1})
    assert_equals(set(ipolys[(1, True)]), {x, y, x + y, y + 1, y, x + 1, x})
    assert_equals(set(ipolys[(2, False)]), {x**2 - y, x*y - 1, x - y**2})
    assert_equals(set(ipolys[(2, True)]), {x**2 + y**2, x + y**2, y**2 + 1, x*y + 1, x**2 + y, x**2 + 1})
