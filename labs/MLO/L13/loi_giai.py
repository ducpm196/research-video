import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
ca = kv['c_ok'] / kv['c_n'] * 100; hij = kv['t_ok'] / kv['t_n'] * 100
print(f'clean_acc={ca:.1f}% trigger_hijack={hij:.1f}%')
