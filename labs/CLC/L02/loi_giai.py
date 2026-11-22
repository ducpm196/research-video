import ipaddress
vpc = ipaddress.IPv4Network('172.16.0.0/20')
subs = list(vpc.subnets(new_prefix=24))
n_ip = subs[0].num_addresses
print(f'subnets_24={len(subs)}')
print(f'ips_per_24={n_ip}')
print(f'usable_cloud_ips={n_ip - 5}')
