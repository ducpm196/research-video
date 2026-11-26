import sys
s = sys.stdin.read().strip() or "0.90 0.15 0.40 0.15"
tpr, fpr, b1, b2 = map(float, s.split())
ppv = lambda b: (b * tpr) / (b * tpr + (1.0 - b) * fpr)
pa, pb = round(ppv(b1), 3), round(ppv(b2), 3)
print(f"ppv_A={pa:.3f} ppv_B={pb:.3f} mismatch={int(pa != pb)}")
