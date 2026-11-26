import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rgb = kv['rows'] * kv['cols'] * kv['width'] / 1e9
cgb = kv['rows'] * kv['used'] * kv['width'] / 1e9
print(f'row_scan_gb={rgb:.1f}\ncol_scan_gb={cgb:.1f}\nio_saved_pct={100 * (rgb - cgb) / rgb:.1f}%')
