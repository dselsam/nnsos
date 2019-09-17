import sympy as sp

def mkVars(names):
    return [sp.Symbol(name, real=True) for name in names]

def compute_ifactors(poly):
    for (ipoly, _) in sp.factor_list(poly)[1]:
        yield ipoly

def flatten(xss):
    return [x for xs in xss for x in xs]

def cycle(xs, t, k):
    if type(t) is int or t.is_integer: return t

    tmps = sp.symbols('tmp1 tmp2 tmp3')
    for i in range(len(xs)):
        t = t.subs(xs[i], tmps[i])

    for i in range(len(xs)):
        t = t.subs(tmps[i], xs[(i+k)%len(xs)])

    return t

def csum(xs, t):
    return sum([cycle(xs, t, k) for k in range(len(xs))])

def cprod(xs, t):
    return prod([cycle(xs, t, k) for k in range(len(xs))])

def sympy_type_to_head(t):
    if t is sp.mul.Mul: return "mul"
    elif t is sp.add.Add: return "add"
    elif t is sp.power.Pow: return "pow"
    elif t is sp.symbol.Symbol: return "symbol"
    elif t.is_integer: return "integer"
    else: raise Exception("Unexpected head: " + str(t))

def parse_sympy(e):
    head = sympy_type_to_head(type(e))
    if head == "integer":  return [head, int(sp.N(e))]
    elif head == "symbol": return [head, str(e)]
    else:                  return [head] + [parse_sympy(arg) for arg in e.args]

def contains_negation(e):
    q = [parse_sympy(e)]
    while q:
        t = q.pop()
        if t[0] == "integer" and t[1] < 0:
            return True
        elif t[0] not in ["integer", "symbol"]:
            q.extend(t[1:])
    return False
