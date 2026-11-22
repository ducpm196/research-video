tokens, total, acc = 30, 3200, 0
for sec in range(5):
    if sec > 0:
        tokens += 15
    take = min(tokens, 800 if sec > 0 else tokens)
    acc += take
    tokens -= take
rej = total - acc
print(f'accepted={acc}')
print(f'rejected={rej}')
print(f'accept_pct={100 * acc / total:.2f}%')
