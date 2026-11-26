import sys
s = sys.stdin.read().strip() or "30 2 22"
inc, yrs, thr = map(float, s.split())
score = 0.4 * inc + 3.0 * yrs
need_years = (thr - score) / 3.0
print(f"score={score:.1f} pass={int(score >= thr)} need_extra_years={need_years:.1f}")
