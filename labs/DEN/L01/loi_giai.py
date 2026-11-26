import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
f, fpr = int(kv['files']), float(kv['fpr'])
print(f'expected_disk_reads={f * fpr:.2f}\ndisk_avoided_pct={100 * (1 - fpr):.1f}%')
