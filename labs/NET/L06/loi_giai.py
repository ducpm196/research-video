import ipaddress, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
tbl = [(ipaddress.IPv4Network(p), g) for item in kv['routes'].split(',') for p, g in [item.split(':')]]
def lpm(ip): return max((n.prefixlen, g) for n, g in tbl if ipaddress.IPv4Address(ip) in n)[1]
ms = [ipaddress.IPv4Network(x) for x in kv['merge'].split(',')]
c = list(ipaddress.collapse_addresses(ms))
print(f'dst_10_1_10_5={lpm(kv["ip1"])}')
print(f'dst_8_8_8_8={lpm(kv["ip2"])}')
print(f'collapsed_prefix={c[0]}')
