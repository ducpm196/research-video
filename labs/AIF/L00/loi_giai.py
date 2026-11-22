states = [
    (p, a, b, c)
    for p in (0, 1, 2) for a in (0, 1) for b in (0, 1) for c in (0, 1)
]
pos, clean, steps = 0, [1, 0, 1], 0
while any(clean):
    if clean[pos]:
        clean[pos] = 0
    else:
        pos = (pos + 1) % 3
    steps += 1
print(f"total_states={len(states)} clean={clean} steps={steps}")
