import sys
s = sys.stdin.read().strip() or "2+3*4"
def eval_prec(expr):
    ts = list(expr)
    def fold(op, fn):
        v = fn()
        while ts and ts[0] == op:
            ts.pop(0); v = v * fn() if op == "*" else v + fn()
        return v
    return fold("+", lambda: fold("*", lambda: int(ts.pop(0))))
v = int(s[0])
for op, d in zip(s[1::2], s[2::2]):
    v = v + int(d) if op == "+" else v * int(d)
print(f"precedence={eval_prec(s)} left_to_right={v}")
