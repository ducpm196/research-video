import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def m3(trip):
    base, a, b = trip.split(',')
    if a == b or b == base:
        return a
    if a == base:
        return b
    return 'CONFLICT'
print(f'merge_1_2_1={m3(kv["c1"])}')
print(f'merge_1_3_3={m3(kv["c2"])}')
print(f'merge_1_2_3={m3(kv["c3"])}')
