import sys
s = sys.stdin.read().strip() or "5|0,1,0,1,1,0,1,1,1,1,1,1"
ts, ss = s.split("|")
thr = int(ts); samples = [int(x) for x in ss.split(",")]
raw_edges = sum(1 for a, b in zip(samples, samples[1:]) if a != b)
state, streak, prev, clean, accepted_idx = 0, 0, None, [], -1
for i, v in enumerate(samples):
    streak = streak + 1 if v == prev else 1
    prev = v
    if streak >= thr and v != state:
        state = v
        if state == 1 and accepted_idx == -1: accepted_idx = i
    clean.append(state)
clean_edges = sum(1 for a, b in zip(clean, clean[1:]) if a != b)
print(f"accepted_at_ms={accepted_idx} raw_edges={raw_edges} clean_edges={clean_edges}")
