import sys
s = sys.stdin.read().strip() or "XAC NHAN TAP TRAN|GUI CANH BAO THAT|13:18 13:52"
b1, b2, ts = s.split("|")
t1s, t2s = ts.split()
to_m = lambda t: int(t.split(":")[0]) * 60 + int(t.split(":")[1])
print(f"distinct={int(b1 != b2)} diff_min={to_m(t2s) - to_m(t1s)}")
