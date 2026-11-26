import sys
s = sys.stdin.read().strip() or "120 40 25"
C, G, ovl = map(float, s.split())
print(f"seq_eff={C/(C+G)*100:.1f}% overlap_eff={C/(C+G-ovl)*100:.1f}%")
