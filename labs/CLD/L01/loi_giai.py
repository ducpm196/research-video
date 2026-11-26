import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
c = kv['apps'] * kv['app_mb']; v = kv['apps'] * (kv['app_mb'] + kv['os_mb'])
print(f'container_mb={c}\nvm_mb={v}\nvm_extra_gb={(v - c) / 1000:.2f}')
