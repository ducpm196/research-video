import ipaddress, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
vpc = ipaddress.IPv4Network(kv['vpc']); subs = list(vpc.subnets(new_prefix=int(kv['new_prefix'])))
n_ip = subs[0].num_addresses
print(f'subnets_24={len(subs)}\nips_per_24={n_ip}\nusable_cloud_ips={n_ip - int(kv["reserved"])}')
