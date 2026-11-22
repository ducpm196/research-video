samples = [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1]
raw_edges = sum(1 for a, b in zip(samples, samples[1:]) if a != b)
state, streak, prev, clean, accepted_idx = 0, 0, None, [], -1
for i, v in enumerate(samples):
    streak = streak + 1 if v == prev else 1
    prev = v
    if streak >= 5 and v != state:
        state = v
        if state == 1 and accepted_idx == -1: accepted_idx = i
    clean.append(state)
clean_edges = sum(1 for a, b in zip(clean, clean[1:]) if a != b)
print(f"accepted_at_ms={accepted_idx} raw_edges={raw_edges} clean_edges={clean_edges}")
