import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
pos = int(kv['pos']); clean = [int(x) for x in kv['dirty'].split(',')]
N = len(clean); tot = N * (2 ** N); st = 0
while any(clean):
    if clean[pos]: clean[pos] = 0
    else: pos = (pos + 1) % N
    st += 1
print(f'total_states={tot} clean={clean} steps={st}')
