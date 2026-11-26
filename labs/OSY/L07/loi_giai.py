import sys
kv = dict(line.strip().split('=', 1) for line in sys.stdin.read().splitlines() if '=' in line)
work = [int(x) for x in kv['avail'].split(',')]
alloc = [[int(x) for x in row.split(',')] for row in kv['alloc'].split(';')]
mx = [[int(x) for x in row.split(',')] for row in kv['max'].split(';')]
n, m = len(alloc), len(work)
need = [[mx[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
fin = [False]*n; seq = []
while len(seq) < n:
    prog = False
    for i in range(n):
        if not fin[i] and all(need[i][j] <= work[j] for j in range(m)):
            work = [work[j]+alloc[i][j] for j in range(m)]; fin[i] = True; seq.append(f'P{i}'); prog = True; break
    if not prog: break
print(f'safe={int(all(fin))}')
print('safe_seq=' + (','.join(seq) if all(fin) else 'NONE'))
print('final_avail=' + ','.join(map(str, work)))
