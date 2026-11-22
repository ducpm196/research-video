bl = (250 - 200) * 1800
dr = 200 - 140
print(f'backlog_30m={bl}')
print(f'drain_net_per_s={dr}')
print(f'drain_minutes={bl / dr / 60:.1f}')
