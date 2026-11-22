t = 20
vanish = 0.8 ** t
explode = 1.2 ** t
clipped = min(explode, 5.0)
print(f"vanish_20={vanish:.5f} explode_20={explode:.2f}")
print(f"clipped_norm={clipped:.2f}")
