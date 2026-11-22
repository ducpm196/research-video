dek_b = 25_000 * 32
raw_b = 2 * 10 ** 12
print(f'dek_bytes={dek_b}')
print(f'dek_kb={dek_b / 1000:.1f}')
print(f'smaller_than_raw={int(dek_b < raw_b)}')
