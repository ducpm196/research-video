g = (1 - 0.005)**300; f1 = 1 - g; f2 = 1 - (1 - 0.0005)**300
print(f'flaky_fail_pct_300={100*f1:.1f}%')
print(f'flaky_fail_pct_p0005={100*f2:.1f}%')
print(f'pipeline_always_green_pct={100*g:.1f}%')
