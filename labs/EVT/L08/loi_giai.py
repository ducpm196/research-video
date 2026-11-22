backlog = (900 - 750) * 3600
drain_s = backlog / (1200 - 900)
print(f'backlog_1h={backlog}')
print(f'drain_s={drain_s:.1f}')
