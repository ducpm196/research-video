import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
amp = int(kv['tries']) ** int(kv['tiers'])
bs = sum(int(v) for v in kv['backoffs'].split(','))
print(f'amplified_reqs={amp}\nbackoff_sum_ms={bs}')
