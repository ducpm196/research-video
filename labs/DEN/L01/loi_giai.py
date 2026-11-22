files, fpr = 8, 0.02
reads = files * fpr
print(f'expected_disk_reads={reads:.2f}')
print(f'disk_avoided_pct={100 * (1 - fpr):.1f}%')
