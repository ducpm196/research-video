limit_b, item_b = 16 * 1024 * 1024, 256
max_n = limit_b // item_b
print(f'max_embedded={max_n}')
print(f'bytes_if_exceed={(max_n + 1) * item_b}')
