import sys
s = sys.stdin.read().strip() or "3.5|0.0,1.0,2.0,3.0,4.0"
ls, ps = s.split("|")
loop_meas = float(ls); raw = [float(x) for x in ps.split(",")]
n = len(raw)
err = loop_meas - raw[-1]
edge_corr = err / n
corr = [round(raw[i] + i * edge_corr, 3) for i in range(n)]
print(f"edge_corr={edge_corr:.3f} corrected_poses={corr}")
