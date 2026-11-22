import struct
from collections import deque
buf = struct.pack('<HH', 7, 32) + b'x' * 32
pid, plen = struct.unpack('<HH', buf[:4])
rem, t, fin, q = [24, 3, 3], 0, [0]*3, deque([0,1,2])
while q:
    i = q.popleft(); d = min(4, rem[i]); t += d; rem[i] -= d
    if rem[i] > 0: q.append(i)
    else: fin[i] = t
w = [fin[i] - [24,3,3][i] for i in range(3)]
print(f'frame_total_bytes={4 + plen}')
print(f'rr_avg_wait={sum(w)/3:.2f}')
print(f'header_valid={int(pid == 7 and len(buf) == 4 + plen)}')
