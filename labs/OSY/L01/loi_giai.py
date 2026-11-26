import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
k1, k2 = int(kv['k1']), int(kv['k2'])
pids = kv['thread_pids'].split(',')
print(f'procs_fork3={1 << k1}')
print(f'procs_fork4={1 << k2}')
print(f'shared_spaces_4threads={len(set(pids))}')
