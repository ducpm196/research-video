import sys
s = sys.stdin.read().strip() or "3+4*5|(3+4)*5"
e1, e2 = s.split("|")
def parse_val(txt):
    ts = list(txt.replace(" ", ""))
    def atom():
        if ts[0] != "(": return int(ts.pop(0))
        ts.pop(0); v = expr(); ts.pop(0); return v
    def fold(op, fn):
        v = fn()
        while ts and ts[0] == op:
            ts.pop(0); v = v * fn() if op == "*" else v + fn()
        return v
    expr = lambda: fold("+", lambda: fold("*", atom))
    return expr()
print(f"p1={parse_val(e1)} p2={parse_val(e2)}")
