from collections import deque
b = [24, 3, 3]; rem = b[:]; fin = [0]*3; resp = [-1]*3; t = 0; q = deque([0,1,2])
while q:
    i = q.popleft()
    if resp[i] < 0: resp[i] = t
    d = min(4, rem[i]); t += d; rem[i] -= d
    if rem[i] > 0: q.append(i)
    else: fin[i] = t
w = [fin[i] - b[i] for i in range(3)]
print('rr_waits=' + ','.join(map(str, w)))
print(f'rr_avg_wait={sum(w)/3:.2f}')
print('response_p1_p2_p3=' + ','.join(map(str, resp)))
