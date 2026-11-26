import math, sys
d = float(sys.stdin.read().split('=')[1]); p = 1.0 / (1.0 + math.exp(-d))
print(f'bt_prob={p:.3f} bt_loss={-math.log(p):.3f}')
