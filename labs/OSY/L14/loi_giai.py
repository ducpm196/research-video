import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def to_oct(s):
    return ''.join(str(4*(s[i]=='r') + 2*(s[i+1]=='w') + 1*(s[i+2]=='x')) for i in (0,3,6))
a, b = to_oct(kv['p1']), to_oct(kv['p2'])
print(f'octal_rwxr_x___={a}')
print(f'octal_rw_r__r__={b}')
print(f'group_can_enter={int(int(a[1]) & 1 == 1)} other_denied={int(a[2] == "0")}')
