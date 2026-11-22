events = [250, -80, 120, -40]
bal = sum(events)
snaps, replay = 200_000 // 500, 500 - 1
print(f'balance={bal}')
print(f'snapshots={snaps}')
print(f'max_replay={replay}')
