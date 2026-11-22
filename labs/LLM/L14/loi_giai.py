flops = 6 * 90e9 * 4.5e11
pf_days = flops / (1e15 * 86400)
ratio = 2.0e12 / 100e9
print(f"model_pf_days={pf_days:.0f} tokens_per_param={ratio:.0f}")
