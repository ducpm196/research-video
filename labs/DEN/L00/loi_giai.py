rows, cols, used, width = 50_000_000, 40, 4, 8
row_gb = rows * cols * width / 1e9
col_gb = rows * used * width / 1e9
print(f'row_scan_gb={row_gb:.1f}')
print(f'col_scan_gb={col_gb:.1f}')
print(f'io_saved_pct={100 * (row_gb - col_gb) / row_gb:.1f}%')
