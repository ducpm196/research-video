import sys
s = sys.stdin.read().strip() or "199,204|199,200,202,203,204,9999,9999,9999,9999"
b_s, v_s = s.split("|")
lo, hi = map(int, b_s.split(","))
vals = sorted(int(x) for x in v_s.split(","))
med = vals[len(vals) // 2]
print(f"median_price={med} safe_in_band={int(lo <= med <= hi)}")
