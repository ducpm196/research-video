import ipaddress
n = ipaddress.IPv4Network('192.168.10.0/26')
p = ipaddress.IPv4Network('192.168.10.0/24')
print(f'net={n.network_address} bcast={n.broadcast_address}')
print(f'usable_hosts={n.num_addresses - 2}')
print(f'subnets_in_slash24={len(list(p.subnets(new_prefix=26)))}')
