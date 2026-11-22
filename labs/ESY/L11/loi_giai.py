from collections import deque
isr_q, overflows = deque(), 0
for b in b'TEMP:42\n':
    if len(isr_q) < 8: isr_q.append(b)
    else: overflows += 1
msg = bytes([isr_q.popleft() for _ in range(len(isr_q))]).decode()
print(f"queued={len(msg)} overflows={overflows} decoded={msg!r}")
