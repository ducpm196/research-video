def parse_val(s):
    ts = list(s.replace(' ', ''))
    def atom():
        if ts[0] != '(': return int(ts.pop(0))
        ts.pop(0); v = expr(); ts.pop(0); return v
    def fold(op, fn):
        v = fn()
        while ts and ts[0] == op:
            ts.pop(0); v = v * fn() if op == '*' else v + fn()
        return v
    expr = lambda: fold('+', lambda: fold('*', atom))
    return expr()
print(f"p1={parse_val('3+4*5')} p2={parse_val('(3+4)*5')}")
