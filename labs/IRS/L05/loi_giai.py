import math
loss_ok = math.log1p(math.exp(-(2.5 - 1.2)))
loss_bad = math.log1p(math.exp(-(1.2 - 2.5)))
swap12 = (4 - 2) * (1 / math.log2(2) - 1 / math.log2(3))
swap34 = (1 - 0) * (1 / math.log2(4) - 1 / math.log2(5))
print(f"loss_ok={loss_ok:.3f} loss_swap={loss_bad:.3f}")
print(f"dcg_drop_12={swap12:.3f} dcg_drop_34={swap34:.3f}")
