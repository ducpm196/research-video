loc = 20 * 0.5; wan = 20 * 150.0
print(f'local_20_rpcs_ms={loc:.1f}')
print(f'cross_continent_20_rpcs_ms={wan:.1f}')
print(f'slowdown_factor={round(wan / loc)}x')
