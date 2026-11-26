import sys
from collections import deque
s = sys.stdin.read().strip() or "8|TEMP:42\n"
cap_s, raw_msg = s.split("|", 1)
cap = int(cap_s)
payload = raw_msg.replace("\\n", "\n").encode()
isr_q, overflows = deque(), 0
for b in payload:
    if len(isr_q) < cap: isr_q.append(b)
    else: overflows += 1
msg = bytes([isr_q.popleft() for _ in range(len(isr_q))]).decode()
print(f"queued={len(msg)} overflows={overflows} decoded={msg!r}")
