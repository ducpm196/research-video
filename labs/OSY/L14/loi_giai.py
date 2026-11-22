def to_oct(s):
    v = [4*(s[i]=='r') + 2*(s[i+1]=='w') + 1*(s[i+2]=='x') for i in (0,3,6)]
    return ''.join(map(str, v))
a, b = to_oct('rwxr-x---'), to_oct('rw-r--r--')
print(f'octal_rwxr_x___={a}')
print(f'octal_rw_r__r__={b}')
print(f'group_can_enter={int(int(a[1]) & 1 == 1)} other_denied={int(a[2] == "0")}')
