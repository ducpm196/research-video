import sys
s = sys.stdin.read().strip() or "0.24 0.40 0.42 0.50 0.8"
a1, b1, a2, b2, thr = map(float, s.split())
print(f"keep_good={int((a1/b1) < thr)} keep_ambiguous={int((a2/b2) < thr)}")
