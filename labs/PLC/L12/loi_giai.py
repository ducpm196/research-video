import sys
s = sys.stdin.read().strip() or "5,15,25|35"
xs_s, add_s = s.split("|")
xs1 = tuple(int(x) for x in xs_s.split(","))
xs0 = tuple(xs1)
xs2 = xs1 + (int(add_s),)
print(f"xs1={xs1} xs2={xs2} unchanged={int(xs1 == xs0)}")
