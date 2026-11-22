import math
sig = lambda t: 1.0 / (1.0 + math.exp(-t))
ds = sig(10.0) * (1.0 - sig(10.0))
relus = [max(0.0, v) for v in (-3.0, 0.0, 4.0)]
xav = math.sqrt(2.0 / (64 + 16))
print(f"dsigmoid_10={ds:.6e}")
print(f"relu={relus}")
print(f"xavier_std={xav:.4f}")
