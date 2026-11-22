calls = 0; listeners = [lambda e: None for _ in range(3)]
for _ in range(4):
    for _ in listeners: calls += 1
v = 10; hist = [v]; v += 5; hist.append(v); v *= 2; hist.append(v); v -= 3; hist.append(v)
print(f'observer_notifications={calls}')
print(f'cmd_after_3={v}')
print(f'cmd_after_undo1={hist[-2]}')
