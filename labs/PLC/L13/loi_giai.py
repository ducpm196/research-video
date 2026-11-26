import sys
s = sys.stdin.read().strip() or "130 5 76 24"
tot, non_m, p1, p2 = map(float, s.split())
mem_bug = (tot - non_m) / tot * 100.0
android_drop = (p1 - p2) / p1 * 100.0
print(f"mem_bug_pct={mem_bug:.1f}% android_drop_pct={android_drop:.1f}%")
