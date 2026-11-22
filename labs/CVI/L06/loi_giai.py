f, B = 600.0, 0.15
d3, d9 = f * B / 3.0, f * B / 9.0
err_at_3 = f * B / (d3 - 1.0) - 3.0
err_at_9 = f * B / (d9 - 1.0) - 9.0
print(f"Z3=3.0 err3={err_at_3:.2f}m Z9=9.0 err9={err_at_9:.2f}m")
