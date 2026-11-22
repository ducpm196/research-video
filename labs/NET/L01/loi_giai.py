tx = (1500 * 8) / 100e6
prop = 1000e3 / 2e8
print(f'tx_us={tx * 1e6:.1f}')
print(f'prop_ms={prop * 1e3:.1f}')
print(f'total_ms={(tx + prop) * 1e3:.2f}')
