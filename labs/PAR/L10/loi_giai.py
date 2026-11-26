import sys
s = sys.stdin.read().strip() or "4 2.0"
ns, ds = s.split(); N, D = int(ns), float(ds)
print(f"ring_allreduce_sent_GB={2.0 * (N - 1) / N * D:.2f}")
