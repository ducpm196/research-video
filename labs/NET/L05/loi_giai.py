import ipaddress, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n = ipaddress.IPv4Network(kv['sub']); p = ipaddress.IPv4Network(kv['parent'])
np = int(kv['new_prefix'])
print(f'net={n.network_address} bcast={n.broadcast_address}')
print(f'usable_hosts={n.num_addresses - 2}')
print(f'subnets_in_slash24={len(list(p.subnets(new_prefix=np)))}')
