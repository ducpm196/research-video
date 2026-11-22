cw, ss, tr = 1, 16, [1]
for _ in range(5): cw = cw * 2 if cw < ss else cw + 1; tr.append(cw)
ss_to, cw_to = cw // 2, 1
print('slowstart_trace=' + ','.join(map(str, tr[:-1])))
print(f'aimd_step1={tr[-1]}')
print(f'after_timeout_ssthresh={ss_to} cwnd={cw_to}')
