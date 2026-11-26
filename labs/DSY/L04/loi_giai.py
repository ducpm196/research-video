import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
maj = int(kv['majority']) == 1
cp_ok = 1 if maj else 0
ap_avail = 1
div = int(kv['v_left'] != kv['v_right'])
print(f'cp_rejected_minority={int(cp_ok == 0)}')
print(f'ap_available_minority={ap_avail}')
print(f'ap_diverged={div}')
