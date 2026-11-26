import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
calls = 0
ls = [lambda e: None for _ in range(kv['listeners'])]
for _ in range(kv['events']):
    for _ in ls:
        calls += 1
v = kv['val']; hist = [v]
v += kv['add']; hist.append(v)
v *= kv['mul']; hist.append(v)
v -= kv['sub']; hist.append(v)
print(f'observer_notifications={calls}')
print(f'cmd_after_3={v}')
print(f'cmd_after_undo1={hist[-2]}')
