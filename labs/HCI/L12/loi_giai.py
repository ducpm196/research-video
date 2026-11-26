import sys
s = sys.stdin.read().strip() or "16,30,19|0.90 0.05|24 48"
ws, ls, szs = s.split("|")
wcag1 = sum(int(x) for x in ws.split(","))
L1, L2 = map(float, ls.split())
s1, s2 = map(int, szs.split())
contrast = (L1 + 0.05) / (L2 + 0.05)
area1 = s1 * s1; ratio = (s2 * s2) / area1
print(f"wcag1={wcag1} contrast_ratio={contrast:.1f} area_24={area1} ratio_48_24={ratio:.2f}x")
