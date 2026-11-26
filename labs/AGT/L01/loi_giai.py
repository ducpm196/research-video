import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
mx = int(kv['max_amt']); calls = kv['calls'].split(',')
def ok(item):
    v_s, acc = item.split(':')
    if v_s in ('True', 'False'): return False
    try: v = int(v_s)
    except ValueError: return False
    return 0 < v <= mx and len(acc) == 10 and acc.isdigit()
idx = [i for i, c in enumerate(calls) if ok(c)]
print(f'total_calls={len(calls)} valid_count={len(idx)} idx={idx}')
