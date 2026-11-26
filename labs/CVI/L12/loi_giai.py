import sys
s = sys.stdin.read().strip() or "25.8 3.57 2.25 50000"
e11, e15, e17, nv = map(float, s.split())
n = int(nv)
d15 = e11 / e15; d17 = e11 / e17
err15 = round((e15 / 100.0) * n)
err17 = round((e17 / 100.0) * n)
print(f"drop_11_15={d15:.1f}x drop_11_17={d17:.1f}x err2015={err15} err2017={err17}")
