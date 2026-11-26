import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
steps = kv['steps'].split(','); fail = kv['fail']; done, failed = [], None
for s in steps:
    if s == fail: failed = s; break
    done.append(s)
print(f'failed_at={failed}\ncompensations={[f"undo_{s}" for s in reversed(done)]}')
