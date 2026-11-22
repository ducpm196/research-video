import ipaddress
tbl = [(ipaddress.IPv4Network(p), g) for p, g in (('10.1.0.0/20','A'),('10.1.8.0/21','B'),('0.0.0.0/0','DEFAULT'))]
def lpm(ip): return max((n.prefixlen, g) for n, g in tbl if ipaddress.IPv4Address(ip) in n)[1]
c = list(ipaddress.collapse_addresses([ipaddress.IPv4Network('192.168.0.0/24'), ipaddress.IPv4Network('192.168.1.0/24')]))
print(f'dst_10_1_10_5={lpm("10.1.10.5")}')
print(f'dst_8_8_8_8={lpm("8.8.8.8")}')
print(f'collapsed_prefix={c[0]}')
