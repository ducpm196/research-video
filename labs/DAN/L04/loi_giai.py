import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n1, a1, a2 = (int(x) for x in kv['c1'].split(',')); n2, b1 = (int(x) for x in kv['c2'].split(','))
r11, r12, r21 = a1 / n1 * 100, a2 / n1 * 100, b1 / n2 * 100
print(f'c1_m1={r11:.1f}% c1_m2={r12:.1f}%\nc2_m1={r21:.1f}% improved={int(r21 > r11)}')
