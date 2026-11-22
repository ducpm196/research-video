n, k, p, s = 28, 5, 2, 2
out_sz = (n - k + 2 * p) // s + 1
params = (k * k * 3 + 1) * 8
dense = out_sz * out_sz * 8
print(f"out_dim={out_sz}x{out_sz}x8={dense}")
print(f"conv_params={params}")
