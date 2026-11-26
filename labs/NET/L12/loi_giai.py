import sys
n = int(dict(t.split('=') for t in sys.stdin.read().split())['objs'])
non_p = 2 + n * 2; pers = 2 + n
print(f'http_nonpersistent_rtt={non_p}')
print(f'http_persistent_seq_rtt={pers}')
print(f'saved_rtt={non_p - pers}')
