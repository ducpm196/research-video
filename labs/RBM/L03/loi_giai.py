import sys
s = sys.stdin.read().strip() or "2 1 3 -1"
x, y, dx, dy = map(int, s.split())
rot90 = lambda a, b: (-b, a)
tr = lambda a, b: (a + dx, b + dy)
print(f"rot_then_tr={tr(*rot90(x, y))} tr_then_rot={rot90(*tr(x, y))}")
