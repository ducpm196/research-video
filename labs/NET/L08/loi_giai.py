b, c = 1, 2; r = 0; hist = []
while min(b, c) < 16:
    r += 1
    if r % 2 == 1: b = min(16, c + 1)
    else: c = min(16, b + 1)
    hist.append((b, c))
print(f'after_round1=B:{hist[0][0]},C:{hist[0][1]}')
print(f'rounds_to_reach_16={r}')
print(f'final_vals={b},{c}')
