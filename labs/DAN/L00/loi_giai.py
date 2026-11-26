import sys
pairs = [tuple(int(x) for x in p.split(':')) for p in sys.stdin.read().strip().split('=', 1)[1].split(',')]
print(f'active_login={sum(l > 0 for l, _ in pairs)} active_action={sum(a > 0 for _, a in pairs)}')
