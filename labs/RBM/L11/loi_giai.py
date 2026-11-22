run = lambda h: (1.0 - 8.0 * h) ** 10
print(f"g_030={1.0 - 8.0*0.30:.2f} x10_div={run(0.30):.2f} x10_conv={run(0.05):.5f}")
