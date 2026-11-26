import sys
s = sys.stdin.read().strip() or "0.92 0.60 0.80 0.40"
ad, an, pd1, pd2 = map(float, s.split())
a1 = pd1 * ad + (1.0 - pd1) * an
a2 = pd2 * ad + (1.0 - pd2) * an
print(f"test_overall={a1*100:.1f}% deploy_real={a2*100:.1f}%")
