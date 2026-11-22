done, dlq, p_tries = 0, [], 0
for msg in range(1, 501):
    ok = False
    for _ in range(3):
        if msg == 7: p_tries += 1
        else: ok = True; break
    if ok: done += 1
    else: dlq.append(msg)
print(f'processed={done}')
print(f'dlq={dlq}')
print(f'poison_attempts={p_tries}')
