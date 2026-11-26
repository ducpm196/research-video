import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def cookie_sent(trip):
    ss, m, cross = trip.split(',')
    if int(cross) == 0: return 1
    if ss == 'None': return 1
    if ss == 'Lax': return int(m == 'GET')
    return 0
print(f'none_cross_post={cookie_sent(kv["c1"])}')
print(f'lax_cross_post={cookie_sent(kv["c2"])}')
print(f'strict_cross_post={cookie_sent(kv["c3"])}')
