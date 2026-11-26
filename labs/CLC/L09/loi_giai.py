import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
db = kv['deks'] * kv['key_b']; rb = kv['raw_tb'] * (10 ** 12)
print(f'dek_bytes={db}\ndek_kb={db / 1000:.1f}\nsmaller_than_raw={int(db < rb)}')
