def safe_hb(claimed, actual): return claimed <= actual and claimed >= 0
print(f'max_u16_bytes={2 ** 16}')
print(f'leaked_bytes={65535 - 5}')
print(f'safe_check_rejected={int(not safe_hb(65535, 5))}')
